import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


tips = sns.load_dataset('tips')

# 创建分组柱状图
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.barplot(x="day", y="total_bill", hue="sex", data=tips, palette="Set3")
plt.title('Total Bill by Day and Gender', fontsize=14, fontweight='bold')
plt.xlabel('Day', fontsize=12)
plt.ylabel('Total Bill', fontsize=12)

plt.show()
