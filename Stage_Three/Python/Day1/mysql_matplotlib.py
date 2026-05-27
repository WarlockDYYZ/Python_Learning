import pandas as pd
import pymysql
from sqlalchemy import create_engine

import matplotlib.pyplot as plt
import numpy as np


# 创建数据库连接引擎
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/data_analysis")

# 从数据库读取数据到DataFrame
df = pd.read_sql("SELECT * FROM income_data2", engine)
print("数据读取成功，共有%d条记录" % len(df))
# 显示前5条记录
print("n数据预览：")
print(df.head())


# 设置中文字体（避免乱码）
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False
# 创建画布
plt.figure(figsize=(12, 8))

# 1. 折线图：城乡收入趋势对比
plt.subplot(2, 2, 1)
plt.plot(df["year"], df["urban_income"], label="城镇居民收入", color="red", marker="o", linewidth=2)
plt.plot(df["year"], df["rural_income"], label="农村居民收入", color="blue", marker="s", linewidth=2)
plt.title("2015-2024年城乡居民人均可支配收入趋势", fontsize=12, fontweight="bold")
plt.xlabel("年份")
plt.ylabel("收入（元）")
plt.legend()
plt.grid(True, alpha=0.3)

# 2. 柱状图：城乡收入对比
plt.subplot(2, 2, 2)
x = np.arange(len(df["year"]))
width = 0.35
plt.bar(x - width/2, df["urban_income"], width, label="城镇", alpha=0.8)
plt.bar(x + width/2, df["rural_income"], width, label="农村", alpha=0.8)
plt.title("2015-2024年城乡居民收入对比", fontsize=12, fontweight="bold")
plt.xlabel("年份")
plt.ylabel("收入（元）")
plt.xticks(x, df["year"])
plt.legend()

# 3. 饼图：2024年城乡收入占比
plt.subplot(2, 2, 3)
df_2024 = df[df["year"] == 2024]
labels = ["城镇", "农村"]
sizes = [df_2024["urban_income"].values[0], df_2024["rural_income"].values[0]]
colors = ["lightcoral", "lightskyblue"]
explode = (0.05, 0)  # 突出城镇部分
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
        autopct="%1.1f%%", shadow=True, startangle=90)
plt.title("2024年城乡居民收入占比", fontsize=12, fontweight="bold")

# 4. 箱线图：收入分布对比
plt.subplot(2, 2, 4)
data_to_plot = [df["urban_income"], df["rural_income"]]
box_labels = ["城镇", "农村"]
plt.boxplot(data_to_plot, labels=box_labels, patch_artist=True)
plt.title("城乡居民收入分布对比", fontsize=12, fontweight="bold")
plt.ylabel("收入（元）")
plt.tight_layout()
plt.show()