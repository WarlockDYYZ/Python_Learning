import seaborn as sns
import matplotlib.pyplot as plt


# 加载内置数据
tips = sns.load_dataset('tips')

# 创建箱线图
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

sns.boxplot(
    data=tips,
    x="day",
    y="total_bill",
    hue="smoker",
    palette="Set2"
)

plt.title('Total Bill Distribution by Day and Smoker Status',
         fontsize=14, fontweight='bold')

plt.xlabel('Day', fontsize=12)
plt.ylabel('Total Bill', fontsize=12)

plt.show()
