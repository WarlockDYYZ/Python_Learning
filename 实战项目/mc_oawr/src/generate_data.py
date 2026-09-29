#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""D1: 模拟多渠道销售数据生成脚本

生成约365天 x 5渠道 = 1825行的每日销售数据，包含：
- 缺失值（约1%的GMV缺失）
- 异常尖峰（约0.5%的GMV异常高值）
- 重复行（约0.4%的重复数据）
- 周末效应（周六日GMV略低）
- 节假日效应（模拟双十一/618等促销高峰）

用法: python src/generate_data.py
输出: data/raw/sales_daily.csv
"""
import os
import sys
import numpy as np
import pandas as pd

# 确保可以从项目根目录运行
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def generate_sales_data(n_days=365, seed=42):
    """生成模拟销售数据"""
    np.random.seed(seed)

    # 日期范围和渠道
    start_date = pd.Timestamp("2025-09-01")
    dates = pd.date_range(start_date, periods=n_days, freq='D')
    channels = ["抖音", "小红书", "淘宝", "微信", "自然流量"]

    # 基础GMV（不同渠道有不同的基础水平）
    base_gmv = {"抖音": 1200, "小红书": 800, "淘宝": 1500, "微信": 600, "自然流量": 400}

    # 构建DataFrame
    rows = []
    for d in dates:
        for ch in channels:
            # 基础值 + 随机波动
            base = base_gmv[ch]
            noise = np.random.lognormal(0, 0.25)

            # 周末效应
            weekend_factor = 0.85 if d.weekday() >= 5 else 1.0

            # 节假日/促销效应（模拟）
            holiday_factor = 1.0
            if d.month == 11 and d.day >= 11 and d.day <= 11:  # 双十一
                holiday_factor = 3.5
            elif d.month == 6 and d.day >= 1 and d.day <= 3:  # 618预热
                holiday_factor = 2.0
            elif d.month == 12 and d.day >= 20:  # 双十二
                holiday_factor = 2.2
            elif d.month == 1 and d.day >= 1 and d.day <= 3:  # 元旦
                holiday_factor = 1.8

            gmv = base * noise * weekend_factor * holiday_factor

            # 其他指标
            exposure = int(gmv * np.random.uniform(8, 12))
            clicks = int(exposure * np.random.uniform(0.02, 0.06))
            cost = round(gmv * np.random.uniform(0.08, 0.15), 2)
            new_users = max(0, int(clicks * np.random.uniform(0.3, 0.6)))

            rows.append({
                "date": d.strftime("%Y-%m-%d"),
                "channel": ch,
                "exposure": exposure,
                "clicks": clicks,
                "cost": cost,
                "gmv": round(gmv, 2),
                "new_users": new_users,
            })

    df = pd.DataFrame(rows)

    # === 埋入数据质量问题（才有调试价值）===

    # 1. 缺失值：随机选20行的gmv设为NaN
    nan_indices = np.random.choice(len(df), size=20, replace=False)
    df.loc[nan_indices, "gmv"] = np.nan

    # 2. 异常尖峰：随机选10行，gmv放大6倍
    spike_indices = np.random.choice(len(df), size=10, replace=False)
    spike_indices = [i for i in spike_indices if i not in nan_indices]
    df.loc[spike_indices, "gmv"] = df.loc[spike_indices, "gmv"] * 6

    # 3. 重复行：复制8行追加
    dup_indices = np.random.choice(len(df), size=8, replace=False)
    df_dup = df.loc[dup_indices].copy()
    df = pd.concat([df, df_dup], ignore_index=True)

    # 4. 排序并重置索引
    df = df.sort_values(["date", "channel"]).reset_index(drop=True)

    return df


def main():
    """主函数：生成数据并保存"""
    output_dir = os.path.join(os.path.dirname(__file__), '..', "data", "raw")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "sales_daily.csv")

    df = generate_sales_data()
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

    print(f"数据已生成: {output_path}")
    print(f"总行数: {len(df)}")
    print(f"列名: {list(df.columns)}")
    print(f"日期范围: {df.date.min()} ~ {df.date.max()}")
    print(f"渠道: {sorted(df.channel.unique())}")
    print(f"缺失值统计:\n{df.isnull().sum()}")
    print(f"重复行数: {df.duplicated().sum()}")


if __name__ == "__main__":
    main()