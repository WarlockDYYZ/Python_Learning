import numpy as np

# 从一维列表创建
arr1d = np.array([1, 2, 3, 4, 5])
print("一维数组：", arr1d)
print("数组类型：", type(arr1d))  # <class 'numpy.ndarray'>
# 从二维列表创建
arr2d = np.array([[1, 2, 3], [4, 5, 6]])
print("n二维数组：")
print(arr2d)
# 从列表的列表创建三维数组
arr3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
print("n三维数组：")
print(arr3d)

# 创建全零数组
zeros = np.zeros((3, 4))  # 3行4列
print("全零数组：")
print(zeros)
# 创建全一数组
ones = np.ones((2, 3), dtype=int)  # 指定数据类型
print("n全一数组：")
print(ones)
# 创建未初始化数组（内容随机）
empty = np.empty((2, 2))
print("n空数组（随机值）：")
print(empty)
# 创建单位矩阵
eye = np.eye(3)  # 3×3单位矩阵
print("n单位矩阵：")
print(eye)

# arange函数：类似Python的range，但返回数组
a_range1 = np.arange(10)  # 0-9
a_range2 = np.arange(1, 10, 2)  # 1,3,5,7,9
a_range3 = np.arange(10, 30, 5)  # 10,15,20,25
print("arange示例：")
print(a_range1)
print(a_range2)
print(a_range3)
# linspace函数：线性等距序列
line_space1 = np.linspace(0, 10, 5)  # 5个点，从0到10
line_space2 = np.linspace(0, 10, 5, endpoint=False)  # 不包含终点
print("nlinspace示例：")
print(line_space1)
print(line_space2)

# 均匀分布随机数（0-1）
rand1 = np.random.rand(2, 3)  # 2行3列
rand2 = np.random.randn(2, 3)  # 标准正态分布
print("随机数组：")
print(rand1)
print(rand2)
# 整数随机数
randint = np.random.randint(1, 10, (2, 3))  # 1-9之间的随机整数
print("n随机整数数组：")
print(randint)

# 一维数组的索引与切片
arr = np.arange(10)
print("原始数组：", arr)
# 索引操作（从0开始）
print("n索引操作：")
print("第一个元素：", arr[0])
print("最后一个元素：", arr[-1])
print("倒数第二个元素：", arr[-2])
# 切片操作：start:stop:step（左闭右开）
print("n切片操作：")
print("前3个元素：", arr[:3])  # 0-2
print("第3-5个元素：", arr[2:5])  # 2,3,4
print("步长为2：", arr[::2])  # 0,2,4,6,8
print("逆序：", arr[::-1])  # 9,8,7,6,5,4,3,2,1,0)

# 多维数组的索引与切片
arr2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("二维数组：")
print(arr2d)
# 访问单个元素
print("n访问单个元素：")
print("第1行第2列：", arr2d[0, 1])  # 等同于arr2d[0][1]
print("第2行第3列：", arr2d[1, 2])
# 切片操作
print("n切片操作：")
print("前两行：")
print(arr2d[:2])  # 前两行所有列
print("n第2-3行，第1-2列：")
print(arr2d[1:3, :2])
print("n隔行取，所有列：")
print(arr2d[::2, :])
# 访问特定行或列
print("n第2行：", arr2d[1])  # 或 arr2d[1, :]
print("n第2列：", arr2d[:, 1])
print("n对角线元素：", arr2d.diagonal())
# 默认操作行，省略操作列的“，”

# 高级索引（整数数组索引）
arr = np.arange(12).reshape(3, 4)
print("原始数组：")
print(arr)
# 使用整数数组索引
print("n高级索引：")
rows = np.array([0, 1, 2])
cols = np.array([0, 1, 2])
print("选取(0,0),(1,1),(2,2)：", arr[rows, cols])
# 布尔索引
print("n布尔索引：")
mask = arr > 5
print("大于5的元素：")
print(arr[mask])
# 同时使用多个条件
print("n复合条件：")
print("大于5且小于9的元素：")
print(arr[(arr > 5) & (arr < 9)])
# 花式索引（使用列表或数组选择任意元素）
print("n花式索引：")
print("选择第0行和第2行：")
print(arr[[0, 2]])
print("n选择第0行第0列和第2行第2列：")
print(arr[[0, 2], [0, 2]])

# 算术运算（向量化运算）
a = np.array([10, 20, 30, 40])
b = np.array([1, 2, 3, 4])
print("数组a：", a)
print("数组b：", b)
# 加法
print("n加法：", a + b)
a += b
print("加法（原地）：", a)  # 改变原数组
# 减法
print("n减法：", a - b)
# 乘法（元素级）
print("n乘法（元素级）：", a * b)
# 除法
print("n除法：", a / b)
print("整除：", a // b)
print("取余：", a % b)
# 幂运算
print("n幂运算：", a ** 2)

# 矩阵运算
A = np.array([[1, 1], [0, 1]])
B = np.array([[2, 0], [3, 4]])
print("矩阵A：")
print(A)
print("n矩阵B：")
print(B)
# 矩阵乘法（使用@或dot函数）
print("n矩阵乘法（@）：")
print(A @ B)
print("n矩阵乘法（dot）：")
# 与标量乘法推荐使用dot 如np.dot(a, 2)
print(np.dot(A, B))
# 矩阵转置
print("n矩阵转置：")
print(A.T)
# 矩阵求逆（需要方阵）
print("n矩阵求逆：")
print(np.linalg.inv(A))

# 广播机制是一个强大的特性，允许不同形状的数组进行运算而无需显式复制数据
# 广播示例1：标量与数组运算
a = np.array([1.0, 2.0, 3.0])
b = 2.0
print("广播示例1：")
print(a + b)  # 等价于 [1+2, 2+2, 3+2]
# 广播示例2：形状不同的数组运算
a = np.array([[1, 2, 3], [4, 5, 6]])
b = np.array([10, 20, 30])
print("n广播示例2：")
print(a + b)  # b被广播为2×3的数组
# 广播示例3：使用newaxis增加维度
a = np.array([1, 2, 3])  # 形状(3,)，a自动扩展
b = np.array([[1], [2], [3]])  # 形状(3,1)
print("n广播示例3：")
print(a + b)  # 输出形状(3,3)
# 说明
# shape(3, )     →  3个元素排成一行（只有"长度"）
#                   [1, 2, 3]
# shape(3, 1)   →  3行1列（有"行"和"列"两个维度）
#                   [[1],
#                    [2],
#                    [3]]
# 补充
# 广播遵循以下规则
# 1. 从右往左（尾部）比较两个数组的维度
# 2. 维度必须相等，或其中一个为 1
# 3. 较小的数组会在左侧补 1 以匹配维度
# 4. 广播不会实际复制数据，而是在计算时虚拟扩展

# 统计运算
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("数组：")
print(arr)
# 求和
print("n求和：")
print("所有元素和：", arr.sum())
print("按行求和：", arr.sum(axis=1))  # 每一行的和
print("按列求和：", arr.sum(axis=0))  # 每一列的和
# 平均值
print("n平均值：")
print("所有元素平均值：", arr.mean())
print("按行平均值：", arr.mean(axis=1))
print("按列平均值：", arr.mean(axis=0))
# 其他统计函数
print("n其他统计：")
print("最大值：", arr.max())
print("最小值：", arr.min())
print("标准差：", arr.std())
print("方差：", arr.var())
print("累计和：", arr.cumsum())