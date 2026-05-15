import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 创建疾病分布饼图
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
# 疾病类型分布
disease_labels = ['心脏病', '糖尿病', '高血压', '癌症', '其他']
disease_counts = [120, 85, 95, 60, 40]
# 绘制饼图
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc']
wedges, texts, autotexts = ax1.pie(disease_counts, labels=disease_labels,
                                   colors=colors, autopct='%1.1f%%',
                                   startangle=90, shadow=True)
ax1.set_title('疾病类型分布', fontsize=14, fontweight='bold')


# 2. 创建年龄分布直方图
# 生成年龄数据（模拟）
np.random.seed(42)
ages = []
for _ in range(500):
    age = np.random.normal(50, 15)
    ages.append(max(0, min(100, age)))
# 绘制直方图
ax2.hist(ages, bins=20, alpha=0.7, color='skyblue',
         edgecolor='black', density=True)
ax2.set_title('患者年龄分布', fontsize=14, fontweight='bold')
ax2.set_xlabel('年龄', fontsize=12)
ax2.set_ylabel('频率', fontsize=12)
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 3. 创建治疗效果对比柱状图
fig, ax = plt.subplots(figsize=(10, 6))
# 治疗方案对比
treatments = ['方案A', '方案B', '方案C', '方案D']
success_rates = [65, 78, 82, 75]
failure_rates = [35, 22, 18, 25]
# 设置位置
x = np.arange(len(treatments))
width = 0.35
# 绘制堆叠柱状图
bars1 = ax.bar(x, success_rates, width, label='成功', color='green', alpha=0.7)
bars2 = ax.bar(x, failure_rates, width, bottom=success_rates,
               label='失败', color='red', alpha=0.7)
# 设置标签和标题
ax.set_title('不同治疗方案效果对比', fontsize=14, fontweight='bold')
ax.set_xlabel('治疗方案', fontsize=12)
ax.set_ylabel('患者数 (%)', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(treatments)
ax.legend()
# 添加数值标签
for bar in bars1:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{int(height)}%', ha='center', va='bottom')

plt.tight_layout()
plt.show()