# 1. 简单的 NumPy 程序
import numpy as np

# 创建一个简单的一维数组
arr = np.array([1, 2, 3, 4, 5])
print("一维数组：", arr)
print("数组类型：", type(arr))
print("数组维度：", arr.ndim)
print("数组形状：", arr.shape)
# 数组形状为(5,)
# (5,) → 1 维，5 个元素, ","后为空，表示所有元素在一行
# (5,1) → 2 维，5 行 1 列
# (2,3) → 2 维，2 行 3 列
# 把形状 (5,) -> (5,1)
# 1. b = a.reshape(5, 1)， 最常用# 2. b = a.reshape(-1, 1)， 更通用
# 3. b = a[:, np.newaxis]， 增加维度
# 4. np.expand_dims(a, axis=1)
# (5,1) -> (1,5)
# a = np.array([[1],
#               [2],
#               [3],
#               [4],
#               [5]])
# 1. b = a.T
# 2. b = a.reshape(1, 5)
# 3. b = a.reshape(1, -1)
# 创建一个二维数组
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
print("二维数组：")
print(arr_2d)
print("数组维度：", arr_2d.ndim)
print("数组形状：", arr_2d.shape)
# 基本运算
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
print("数组加法：", arr1 + arr2)
print("数组乘法：", arr1 * arr2)
# 与标量运算
print("数组乘以标量：", arr1 * 2)
print("*" * 50)

# 2. 数组创建与基本操作
# 2.1 数组创建方法
# 2.1.1 从 Python 序列创建
# NumPy 数组可以从 Python 列表和元组创建

# 一维数组
# 从列表创建
arr1 = np.array([1, 2, 3, 4, 5])
print("从列表创建一维数组：", arr1)
# 从元组创建
arr2 = np.array((1.5, 2.5, 3.5))
print("从元组创建一维数组：", arr2)
print("." * 50)

# 二维数组
# 从嵌套列表创建二维数组
arr_2d = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("二维数组：")
print(arr_2d)
print("数组形状：", arr_2d.shape)
print("." * 50)

# 指定数据类型
# 创建整数类型数组
int_arr = np.array([1, 2, 3], dtype=np.int32)
print("整数数组：", int_arr)
print("数据类型：", int_arr.dtype)
# 创建浮点类型数组
float_arr = np.array([1, 2, 3], dtype=np.float64)
print("浮点数组：", float_arr)
print("数据类型：", float_arr.dtype)
# 创建布尔类型数组
bool_arr = np.array([True, False, True])
print("布尔数组：", bool_arr)
print("数据类型：", bool_arr.dtype)
print("*" * 50)

# 2.1.2 特殊数组创建
# 全零数组
# 创建全零数组
zeros_1d = np.zeros(5)  # 一维
zeros_2d = np.zeros((3, 4))  # 二维
zeros_3d = np.zeros((2, 3, 4))  # 三维 2个3x4
print("一维全零数组：", zeros_1d)
print("二维全零数组：")
print(zeros_2d)
print("三维维全零数组：")
print(zeros_3d)
print("三维全零数组形状：", zeros_3d.shape)
print("." * 50)

# 全一数组：
# 创建全一数组
ones_1d = np.ones(5)
ones_2d = np.ones((3, 4))
print("一维全一数组：", ones_1d)
print("二维全一数组：")
print(ones_2d)
print("." * 50)

# 空数组
# 创建空数组（未初始化）
empty_arr = np.empty((2, 3))
print("空数组：")
print(empty_arr)
print("注意：空数组的初始内容是随机的，取决于内存状态")
print("." * 50)

# 单位矩阵
# 创建单位矩阵
eye_3 = np.eye(3)  # 3x3单位矩阵
eye_4 = np.eye(4)  # 4x4单位矩阵
print("3x3单位矩阵：")
print(eye_3)
print("4x4单位矩阵：")
print(eye_4)
print("*" * 50)

# 2.1.3 数值范围数组
# arange函数
# np.arange类似Python的range，但返回数组
arr1 = np.arange(10)  # 0到9
arr2 = np.arange(1, 10)  # 1到9
arr3 = np.arange(1, 10, 2)  # 步长为2
print("arange(10):", arr1)
print("arange(1, 10):", arr2)
print("arange(1, 10, 2):", arr3)
# 支持浮点步长
arr4 = np.arange(0, 1, 0.1)
print("浮点步长：", arr4)
print("." * 50)

# linspace函数
# np.linspace创建等间距数组
# np.linspace 是 NumPy 里最常用的函数之一
# 作用是：在指定区间内，生成均匀间隔的数字
# 全称：linear space（线性等分）
arr1 = np.linspace(0, 10, num=5)  # 5个元素
arr2 = np.linspace(0, 10, num=5, endpoint=False)  # 不包含终点
# 意思：从 0 到 2π（一圈），生成 100 个均匀的角度值专门用来 画正弦波 / 余弦波
arr3 = np.linspace(0, 2 * np.pi, num=100)  # 用于生成正弦波数据
print("linspace(0, 10, 5):", arr1)
print("linspace(0, 10, 5, endpoint=False):", arr2)
print("linspace(0, 2π, 100)的前5个元素：", arr3[: 5])

# 1）默认情况：endpoint=True（包含终点）
# np.linspace(0, 10, 5)
# 要生成 5 个点
# 这 5 个点要刚好把 0~10 铺满
# 所以间隔数 = 点数 - 1 = 4 段
# 步长 = (10 - 0) / (5 - 1) = 2.5

# 2）endpoint=False（不包含终点）
# np.linspace(0, 10, 5, endpoint=False)
# 要生成 5 个点
# 但不要最后一个点
# NumPy 会把 0~10 看成 5 段等长
# 步长 = (10 - 0) / 5 = 2

# 为什么步长不一样
# 包含终点：间隔数 = 点数 − 1
# 不包含终点：间隔数 = 点数
# 所以同样是 0~10、同样 5 个点，一个除以 4，一个除以 5，步长自然不一样

print("*" * 50)

# 2.1.4 随机数组
# 均匀分布随机数
# 生成[0, 1)之间的均匀分布随机数
rand_1d = np.random.rand(5)  # 一维
rand_2d = np.random.rand(3, 4)  # 二维
print("一维均匀分布随机数：", rand_1d)
print("二维均匀分布随机数：")
print(rand_2d)
# 设置随机种子以确保结果可重现
np.random.seed(42)
rand_seed = np.random.rand(5)
print("设置种子后的随机数：", rand_seed)
print("." * 50)

# 正态分布随机数
# 生成标准正态分布随机数（均值0，标准差1）
randn_1d = np.random.randn(5)
randn_2d = np.random.randn(3, 4)
print("一维标准正态分布随机数：", randn_1d)
print("二维标准正态分布随机数：")
print(randn_2d)
# 生成指定均值和标准差的正态分布
mean = 5
std = 2
rand_normal = np.random.normal(mean, std, size=(3, 4))
print(f"均值{mean}，标准差{std}的正态分布：")
print(rand_normal)
print("." * 50)

# 随机整数
# 生成随机整数
randint1 = np.random.randint(0, 10, size=5)  # [0, 10)之间的5个整数
randint2 = np.random.randint(0, 10, size=(3, 4))  # 二维数组
print("一维随机整数：", randint1)
print("二维随机整数：")
print(randint2)
print("*" * 50)

# 2.2数组基本属性
# 2.2.1维度与形状
# ndim属性
# ndim表示数组的维度数
arr_1d = np.array([1, 2, 3])
arr_2d = np.array([[1, 2], [3, 4]])
arr_3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
print("一维数组维度：", arr_1d.ndim)
print("二维数组维度：", arr_2d.ndim)
print("三维数组维度：", arr_3d.ndim)
print("." * 50)

# shape属性
# shape返回各维度长度的元组
print("一维数组形状：", arr_1d.shape)
print("二维数组形状：", arr_2d.shape)
print("三维数组形状：", arr_3d.shape)
# 对于二维数组，shape的第一个元素是行数，第二个是列数
print(f"二维数组有{arr_2d.shape[0]}行{arr_2d.shape[1]}列")
print("*" * 50)

# 2.2.2 数据类型
# dtype属性
# dtype表示数组元素的数据类型
int_arr = np.array([1, 2, 3], dtype=np.int32)
float_arr = np.array([1.0, 2.0, 3.0], dtype=np.float64)
bool_arr = np.array([True, False, True])
print("整数数组数据类型：", int_arr.dtype)
print("浮点数组数据类型：", float_arr.dtype)
print("布尔数组数据类型：", bool_arr.dtype)
print("." * 50)

# astype方法
# 使用astype(), numpy 数组专门用来【转换数据类型】的方法
# 把数组里所有数字的类型，改成你想要的类型
float_to_int = float_arr.astype(np.int32)
int_to_float = int_arr.astype(np.float64)
print("浮点转整数：", float_to_int)
print("整数转浮点：", int_to_float)
# 注意：astype返回新数组，不改变原数组
print("原浮点数组：", float_arr)
print("原整数数组：", int_arr)
print("*" * 50)

# 2.2.3 元素数量与内存占用
# size 属性
# size返回数组元素总数
arr1 = np.array([1, 2, 3])
arr2 = np.array([[1, 2], [3, 4]])
print("一维数组元素数：", arr1.size)
print("二维数组元素数：", arr2.size)
# shape[0] = 多少行
# shape[1] = 多少列
# 相乘 = 一共有多少个数字
print("验证：形状乘积", arr2.shape[0] * arr2.shape[1])
print("." * 50)

# itemsize 和 nbytes 属性
# itemsize表示每个元素占用的字节数
# nbytes表示整个数组占用的字节数
int_arr = np.array([1, 2, 3], dtype=np.int32)
float_arr = np.array([1.0, 2.0, 3.0], dtype=np.float64)
print("int32数组：")
print(f"  每个元素占用：{int_arr.itemsize}字节")
print(f"  总占用内存：{int_arr.nbytes}字节")
print("float64数组：")
print(f"  每个元素占用：{float_arr.itemsize}字节")
print(f"  总占用内存：{float_arr.nbytes}字节")
print("*" * 50)

# 2.3数组类型转换与视图操作
# 2.3.1 数组转换方法 tolist 方法
# 将NumPy数组转换为Python列表
arr = np.array([[1, 2], [3, 4]])
# 两行两列的数组 转换 成大列表嵌套两个小列表
list_2d = arr.tolist()
print("NumPy数组：")
print(arr)
print("转换为Python列表：")
print(list_2d)
print("列表类型：", type(list_2d))
print("列表元素类型：", type(list_2d[0]))
print("." * 50)

# astype转换注意事项
# astype转换的注意事项
arr = np.array([1.9, 2.9, 3.9])
# 浮点转整数会截断小数部分
int_arr = arr.astype(np.int32)
# 把 NumPy 数组里的所有数字，强制转换成 32 位整数类型

# astype(int)
# → 转成系统默认整数（通常是 int64）
# astype(np.int32)
# → 明确指定转成 32 位整数

print("浮点数组：", arr)
print("转整数后：", int_arr)
# 整数转布尔
bool_arr = np.array([0, 1, 2, 3]).astype(np.bool_)
print("整数转布尔：", bool_arr)  # 0为False，非0为True
print("*" * 50)

# 2.3.2 视图与副本的区别
# 视图（View）
# 视图是原数组的一个"窗口"，共享同一块内存
arr = np.array([1, 2, 3, 4, 5])
view = arr[1: 3]  # 切片返回视图
print("原数组：", arr)
print("视图：", view)
# 修改视图会影响原数组
view[0] = 100
print("修改视图后：")
print("原数组：", arr)
print("视图：", view)
# 验证是否共享内存
print(f"是否共享内存：{np.shares_memory(arr, view)}")
print("." * 50)

# 副本（Copy）
# 副本是数据的完整拷贝，拥有独立的内存空间
arr = np.array([1, 2, 3, 4, 5])
copy = arr.copy()  # 使用copy方法创建副本
print("原数组：", arr)
print("副本：", copy)
# 修改副本不会影响原数组
copy[0] = 100
print("修改副本后：")
print("原数组：", arr)
print("副本：", copy)
# 验证是否共享内存
print(f"是否共享内存：{np.shares_memory(arr, copy)}")
print("*" * 50)

# 视图与副本的判断
# 使用base属性判断是否为视图
# arr.base 是 NumPy 数组的一个属性，用来判断这个数组的数据是自己的，还是从别的数组 “借” 来的（共享内存）
#  一句话说清
# arr.base == None → 自己拥有数据（副本），改它不影响别人。
# arr.base 是另一个数组 → 共享别人的数据（视图），改它会改原数组
arr = np.array([1, 2, 3])
view = arr[1:]
copy = arr.copy()
print(view)
print(copy)
print("视图的base属性：", view.base)  # 指向原数组
print("副本的base属性：", copy.base)  # None，表示是独立数组
print("." * 50)


# 判断是否为视图
def is_view(arr):
    return arr.base is not None


print(f"view是否为视图：{is_view(view)}")
print(f"copy是否为视图：{is_view(copy)}")
print("*" * 50)


# 3. 索引、切片与形状操作
# 3.1 一维数组索引与切片

# 3.1.1 基本索引操作
# 正向索引
# 一维数组的基本索引（从0开始）
# 类似列表
arr = np.array([85, 92, 78, 90, 88, 76, 95, 81, 89, 93])
print("原始数组：", arr)
print("第1个元素（索引0）：", arr[0])
print("第3个元素（索引2）：", arr[2])
print("第5个元素（索引4）：", arr[4])
print("." * 50)
# 负向索引
# 负索引从数组末尾开始计数
print("最后一个元素（索引-1）：", arr[-1])
print("倒数第二个元素（索引-2）：", arr[-2])
print("倒数第五个元素（索引-5）：", arr[-5])
print("." * 50)
# 索引赋值
# 通过索引修改数组元素
print("修改前：", arr)
arr[4] = 99  # 将第5个元素改为99
arr[-1] = 100  # 将最后一个元素改为100
print("修改后：", arr)
print("*" * 50)


# 3.1.2 切片操作详解
# 基本切片语法
# 切片语法：arr[start:stop:step]
# start：起始索引（包含，默认0）
# stop：结束索引（不包含，默认数组长度）
# step：步长（默认1）
arr = np.array([85, 92, 78, 90, 88, 76, 95, 81, 89, 93])
print("前5个元素：", arr[:5])  # 0-4索引
print("第3-7个元素（不包含7）：", arr[2:6])  # 2-5索引
print("所有偶数索引元素：", arr[::2])  # 步长2
print("所有元素：", arr[:])
# 等同于arr.copy()
# arr.copy()作用：完整复制一个 NumPy 数组，生成一个全新、独立的副本
print("." * 50)

# 步长切片:
print("反向数组: ", arr[::-1])  # 步长-1，实现反转
print("每隔一个元素取一个（从索引1开始）: ", arr[1::2])
print("从后往前每隔一个元素: ", arr[-1::-2])
print("." * 50)

# 切片赋值:
# 切片赋值会修改原数组（因为切片是视图）
print("切片赋值前: ", arr)
arr[2: 5] = [100, 100, 100]  # 将索引2-4的元素设为100
print("切片赋值后: ", arr)
# 可以使用标量进行切片赋值
arr[5: 8] = 90
print("再次切片赋值后: ", arr)
print("*" * 50)


# 3.2 多维数组索引与切片
# 3.2.1 二维数组索引基本索引
# 二维数组的索引: arr[row, column]
temp_2d = np.array([
    [5.2, 6.1, 7.3, 8.2],
    [4.8, 5.5, 6.7, 7.9],
    [6.3, 7.2, 8.1, 9.0]
])
print("二维温度数组: ")
print(temp_2d)
# 访问单个元素
print("第1天第2小时温度: ", temp_2d[0, 1])  # 行0，列1
print("第2天第3小时温度: ", temp_2d[1, 2])  # 行1，列2
print("第3天第4小时温度: ", temp_2d[2, 3])  # 行2，列3
# 行和列的访问: 
# 访问整行
print("第2天所有小时温度: ", temp_2d[1, :])  # 行1，所有列
# 不指定时默认操作行
print("第2天所有小时温度（简写）: ", temp_2d[1])
# 访问整列
print("所有天的第3小时温度: ", temp_2d[:, 2])  # 所有行，列2
print("所有天的第1小时温度: ", temp_2d[:, 0])
# 访问子数组
sub_arr = temp_2d[0: 2, 1: 3]  # 行0-1，列1-2
print("子数组（第1-2天，第2-3小时）: ")
print(sub_arr)
print("*" * 50)

# 3.2.2 多维数组切片
# 三维数组索引 
# 三维数组: 2个班级 × 3个学生 × 4门科目分数
scores_3d = np.array([
    [
        [85, 92, 78, 90],  # 班级1，学生1
        [88, 76, 95, 81],  # 班级1，学生2
        [89, 93, 79, 87]  # 班级1，学生3
    ],
    [
        [77, 89, 91, 84],  # 班级2，学生1
        [82, 94, 75, 88],  # 班级2，学生2
        [90, 86, 83, 92]  # 班级2，学生3
    ]
])
print("三维数组形状: ", scores_3d.shape)  # (2, 3, 4)
# 访问单个元素: 班级0，学生1，科目2
print("1班2号学生3门科目分数: ", scores_3d[0, 1, 2])
# 访问整个班级的所有学生
print("2班所有学生所有科目: ")
print(scores_3d[1, :, :])
# 访问所有班级的特定学生
print("所有班级的2号学生: ")
print(scores_3d[:, 1, :])
# 访问特定班级的特定科目
print("1班所有学生的前2门科目: ")
print(scores_3d[0, :, :2])
# 其中 ":" 应该是全部的意思
print("." * 50)

# 高级切片技巧
# 使用...表示多个冒号
print("等价于scores_3d[0, :, :]: ", scores_3d[0, ...])
print("等价于scores_3d[:, :, 2]: ", scores_3d[..., 2])
print("等价于scores_3d[1, :, :2]: ", scores_3d[1, ..., : 2])
print("*" * 50)


# 3.3高级索引操作
# 3.3.1 整数数组索引
# 一维整数数组索引
# 整数数组索引允许使用另一个数组来指定要选取的元素位置
arr = np.array([85, 92, 78, 90, 88, 76, 95, 81, 89, 93])
# 选取索引1、3、5的元素
indices = [1, 3, 5]
selected = arr[indices]
print("原数组: ", arr)
print("选取的索引: ", indices)
print("选取的元素: ", selected)
# 可以使用数组作为索引
index_arr = np.array([2, 4, 6])
selected_arr = arr[index_arr]
print("使用数组索引选取的元素: ", selected_arr)
print("." * 50)

# 二维整数数组索引
# 二维数组的整数数组索引
temp_2d = np.array([
    [5.2, 6.1, 7.3, 8.2],
    [4.8, 5.5, 6.7, 7.9],
    [6.3, 7.2, 8.1, 9.0]
])
# 选取第0行和第2行的第1列和第3列
rows = [0, 2]
cols = [1, 3]
# 行列索引会按列表索引自行组合为, (0, 1)、(2, 3)
selected_temp = temp_2d[rows, cols]
print("二维数组: ")
print(temp_2d)
print("选取的元素: ", selected_temp)
# 注意: 返回的是一维数组，元素为(0,1)和(2,3)位置的值
print("." * 50)

# 多维整数数组索引
# 使用np.ix_函数获取子矩阵
# np.ix_ 是用来帮你快速选中「多行 + 多列」交叉位置的工具
# 会把普通列表变成能广播的索引，专门用于二维数组精准取值
sub_temp = temp_2d[np.ix_([0, 2], [1, 3])]
print("使用np.ix_获取的子矩阵: ")
print(sub_temp)
print("形状: ", sub_temp.shape)  # (2, 2)
print("*" * 50)


# 3.3.2 布尔索引
# 基本布尔索引
# 布尔索引通过布尔数组筛选元素
arr = np.array([85, 92, 78, 90, 88, 76, 95, 81, 89, 93])
# 找出分数≥90的元素
mask = arr >= 90
print("布尔掩码: ", mask)
high_scores = arr[mask]
print("90分以上的分数: ", high_scores)
# 直接使用条件表达式进行布尔索引
high_scores_direct = arr[arr >= 90]
print("直接使用条件表达式: ", high_scores_direct)
print("." * 50)

# 复合条件
# 使用逻辑运算组合多个条件
# 找出80≤分数<90的元素
mask1 = arr >= 80
mask2 = arr < 90
combined_mask = np.logical_and(mask1, mask2)
mid_scores = arr[combined_mask]
print("80-90分之间的分数: ", mid_scores)
# 等价写法
mid_scores_direct = arr[(arr >= 80) & (arr < 90)]
print("等价写法: ", mid_scores_direct)
# 找出分数<60或≥90的元素
low_or_high = arr[(arr < 60) | (arr >= 90)]
print("不及格或优秀的分数: ", low_or_high)
not_num = arr[arr != 81]
print("提出成绩为81的分数: ", not_num)
print("." * 50)

# 二维数组布尔索引
# 二维数组的布尔索引
temp_2d = np.array([
    [5.2, 6.1, 7.3, 8.2],
    [4.8, 5.5, 6.7, 7.9],
    [6.3, 7.2, 8.1, 9.0]
])
# 找出温度>7℃的所有值
# 输出为1行
temp_high = temp_2d[temp_2d > 7]
print("温度>7℃的所有值: ", temp_high)
# 找出温度在5-7℃之间的值
temp_medium = temp_2d[(temp_2d >= 5) & (temp_2d <= 7)]
print("温度在5-7℃之间的值: ", temp_medium)
print("*" * 50)


# 3.4 数组形状修改
# 3.4 .1 reshape 函数
# 基本 reshape 操作
# reshape在不改变数据的情况下修改数组形状
arr = np.arange(12)
print("原始数组: ", arr)
# 重塑为3行4列的二维数组
arr_2d = arr.reshape(3, 4)
print("重塑为3x4数组: ")
print(arr_2d)
# 重塑为2行2列3层的三维数组
arr_3d = arr.reshape(2, 2, 3)
print("重塑为2x2x3数组: ")
print(arr_3d)
print("." * 50)

# 自动计算维度
# 使用-1让NumPy自动计算维度
arr = np.arange(12)
# 重塑为4行，列数自动计算
arr_auto = arr.reshape(4, -1)
print("自动计算列数: ")
print(arr_auto)
print("形状: ", arr_auto.shape)
# 重塑为3层，其他维度自动计算
arr_auto2 = arr.reshape(-1, 2, 2)
print("自动计算其他维度: ")
print(arr_auto2)
print("形状: ", arr_auto2.shape)
print("." * 50)

# 注意事项
# reshape要求元素总数不变
try:
    arr.reshape(3, 5)  # 3*5=15≠12，会报错
except ValueError as e:
    print("错误: ", e)
print("*" * 50)


# 3.4.2 其他形状操作函数
# ravel 和 flatten
# ravel和flatten都用于展平数组
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
# ravel返回视图
ravel_view = arr_2d.ravel()
print("原数组: ")
print(arr_2d)
print("ravel返回的视图: ", ravel_view)
# 修改视图会影响原数组
ravel_view[0] = 100
print("修改ravel视图后: ")
print("原数组: ")
print(arr_2d)
print("视图: ", ravel_view)

# flatten返回副本
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])  # 重置数组
flatten_copy = arr_2d.flatten()
print("flatten返回的副本: ", flatten_copy)
# 修改副本不影响原数组
flatten_copy[0] = 100
print("修改flatten副本后: ")
print("原数组: ")
print(arr_2d)
print("副本: ", flatten_copy)
print("." * 50)

# resize 函数
# resize会改变原数组的形状和大小
arr = np.array([1, 2, 3, 4])
print("原数组: ", arr)
# 调整为2x2，原数组被修改
arr.resize(2, 2)
print("resize为2x2后: ")
print(arr)
# 调整为1x5，元素不足时用0填充
arr.resize(1, 5)
print("resize为1x5后（用0填充）: ")
print(arr)
# 调整为3x3，元素不足
try:
    # arr.resize(3, 3)不会抛异常，它会自动用0补齐，把数组强行变成3x3
    # resize(3, 3) 直接修改原数组
    # reshape(3, 3)
    # 必须元素数量完全匹配
    # 不匹配 → 直接报错
    # 不修改原数组，返回新数组
    # 用括号包起来，代表一个形状元组, 不会出现编辑器错误
    arr.resize((3, 3))
    print(arr)
except ValueError as e:
    print("错误: ", e)
print("*" * 50)

# transpose 和 T 属性
# 转置数组
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
print("原数组: ")
print(arr_2d)
# 转置
transposed = arr_2d.transpose()
print("转置后: ")
print(transposed)
# 使用T属性
transposed_t = arr_2d.T
print("使用T属性转置: ")
print(transposed_t)
# 三维数组的转置
arr_3d = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
print("三维数组原形状: ", arr_3d.shape)
transposed_3d = arr_3d.transpose(1, 0, 2)
print("转置后形状: ", transposed_3d.shape)
