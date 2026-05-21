import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# 创建3D数据
iris = sns.load_dataset("iris")


# 创建3D图形
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 绘制3D散点图
colors = {'setosa': 'r', 'versicolor': 'g', 'virginica': 'b'}
for species, color in colors.items():
   mask = iris['species'] == species
   ax.scatter(
       iris[mask]['sepal_length'],
       iris[mask]['sepal_width'],
       iris[mask]['petal_length'],
       c=color,
       label=species,
       s=100,
       alpha=0.8
   )

ax.set_xlabel('Sepal Length')
ax.set_ylabel('Sepal Width')
ax.set_zlabel('Petal Length')
ax.set_title('Iris Dataset 3D Visualization')
ax.legend()
plt.show()