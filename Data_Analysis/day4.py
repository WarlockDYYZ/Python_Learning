import numpy as np
import time

# 4 数组运算与广播机制
# 4.1 算术运算
# 4.1.1 基本算术运算
# 加减乘除运算
# NumPy数组的算术运算是逐元素进行的
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])
print("数组1：", arr1)
print("数组2：", arr2)
print("加法：", arr1 + arr2)
print("减法：", arr1 - arr2)
print("乘法：", arr1 * arr2)
print("除法：", arr1 / arr2)
# 与标量运算
print("数组1乘以2：", arr1 * 2)
print("数组2除以2：", arr2 / 2)
print("." * 50)

# 其他算术运算
# 幂运算
arr = np.array([1, 2, 3, 4])
print("平方: ", arr ** 2)
print("立方: ", arr ** 3)
print("平方根: ", np.sqrt(arr))
# 取余运算
print("5除以2的余数: ", 5 % 2)
print("数组取余: ", arr % 2)
# 整除运算
print("数组整除: ", arr // 2)
print("*" * 50)

# 4.1.2 矩阵运算
# 点积运算
# np.dot用于矩阵乘法和向量点积
# 一维数组的点积
vec1 = np.array([1, 2, 3])
vec2 = np.array([4, 5, 6])
dot_product = np.dot(vec1, vec2)
print("向量点积: ", dot_product)  # 1*4 + 2*5 + 3*6 = 32
print("." * 50)

# 二维数组的矩阵乘法
mat1 = np.array([[1, 2],
                 [3, 4]])
mat2 = np.array([[5, 6],
                 [7, 8]])
mat_product = np.dot(mat1, mat2)
print("矩阵乘法: ")
print(mat_product)
# 使用@运算符（Python 3.5+）
mat_product2 = mat1 @ mat2
print("使用@运算符: ")
print(mat_product2)
print("*" * 50)

# 其他线性代数运算
# 矩阵转置
mat = np.array([[1, 2], [3, 4]])
print("矩阵: ")
print(mat)
print("转置: ")
print(mat.T)
# 矩阵的迹 主对角线元素之和
print("迹: ", np.trace(mat))
# 矩阵的逆（需要方阵）
try:
    # np.linalg.inv(矩阵) = 求逆矩阵，必须是方阵、行列式不能为 0
    inv_mat = np.linalg.inv(mat)
    print("逆矩阵: ")
    print(inv_mat)
except np.linalg.LinAlgError as e:
    print("错误: ", e)
# 矩阵的行列式
# 行列式 ≠ 0 → 矩阵可逆
# 行列式 = 0 → 矩阵奇异，不可逆
# np.linalg.det()   # 行列式
# np.linalg.inv()   # 逆矩阵
# np.trace()        # 矩阵的迹（对角线和）
det = np.linalg.det(mat)
print("行列式: ", det)
print("*" * 50)


# 4.2 逻辑与比较运算
# 比较运算
# 比较运算返回布尔数组
arr1 = np.array([1, 2, 3, 4])
arr2 = np.array([4, 3, 2, 1])
print("数组1: ", arr1)
print("数组2: ", arr2)
# 逐项比较
print("等于: ", arr1 == arr2)
print("不等于: ", arr1 != arr2)
print("大于: ", arr1 > arr2)
print("大于等于: ", arr1 >= arr2)
print("小于: ", arr1 < arr2)
print("小于等于: ", arr1 <= arr2)
# 与标量比较
print("数组1大于2: ", arr1 > 2)
print("." * 50)

# 逻辑运算
# 逻辑运算（注意使用位运算符&、|、~）
arr = np.array([1, 2, 3, 4, 5])
# 找出大于2且小于5的元素
# mask 为布尔列表，根据表的值在数组中筛选
mask = (arr > 2) & (arr < 5)
print("布尔掩码: ", mask)
print("满足条件的元素: ", arr[mask])
# 找出小于3或大于4的元素
mask2 = (arr < 3) | (arr > 4)
print("另一个布尔掩码: ", mask2)
print("满足条件的元素: ", arr[mask2])
# 非运算
mask3 = ~((arr >= 3) & (arr <= 4))
print("非运算掩码: ", mask3)
print("满足条件的元素: ", arr[mask3])
print("*" * 50)


# 4.3 广播机制详解
# 4.3.1 广播规则
# 广播机制的概念
# 广播允许不同形状的数组进行算术运算
# 规则: 
# 1. 从后往前比较维度
# 2. 维度必须相等或其中一个为1
# 3. 维度数不足时在前面补1
# 示例1: 标量与数组运算
arr = np.array([1, 2, 3, 4])
scalar = 2
result = arr * scalar
print("数组: ", arr)
print("标量: ", scalar)
print("广播结果: ", result)
print("解释: 标量被广播为形状相同的数组")
print("." * 50)

# 广播规则示例
# 示例2: 不同形状数组的广播
arr1 = np.array([[1, 2, 3], [4, 5, 6]])  # 2x3
arr2 = np.array([10, 20, 30])  # 1x3（广播为2x3）
print("数组1形状: ", arr1.shape)
print("数组2形状: ", arr2.shape)
print(arr1 + arr2)
print("相加结果形状: ", (arr1 + arr2).shape)
# 示例3: 另一个广播示例
arr3 = np.array([[1], [2], [3]])  # 3x1
arr4 = np.array([10, 20, 30])  # 1x3
print("数组3形状: ", arr3.shape)
print("数组4形状: ", arr4.shape)
print(arr3 * arr4)
# [1]
# [2] x [10, 20, 30]
# [3]
# ||
# [[10 20 30]
#  [20 40 60]
#  [30 60 90]]
print("相乘结果形状: ", (arr1 * arr2).shape)
print("*" * 50)


# 广播规则验证
# 验证广播规则
def check_broadcast(arr1, arr2):
    """检查两个数组是否可以广播"""
    # 从后往前比较维度
    shape1 = arr1.shape[::-1]
    shape2 = arr2.shape[::-1]
    min_len = min(len(shape1), len(shape2))

    for i in range(min_len):
        s1 = shape1[i]
        s2 = shape2[i]

        if s1 == s2 or s1 == 1 or s2 == 1:
            continue
        return False
    return True


# 测试各种情况
# 应该就是是否满足矩阵乘法要求的数学格式
arr_a = np.array([1, 2, 3])  # 1 x 3
arr_b = np.array([[1], [2], [3]])  # 3 x 1
arr_c = np.array([1, 2])  # 1 * 2
print("arr_a和arr_b可以广播: ", check_broadcast(arr_a, arr_b))
print("arr_a和arr_c可以广播: ", check_broadcast(arr_a, arr_c))
print("arr_b和arr_c可以广播: ", check_broadcast(arr_b, arr_c))
print("*" * 50)

# 4.3.2 广播应用实例
# 数据标准化
# 使用广播进行数据标准化（(数据-均值)/标准差）

# 1. 0-1 标准化（最常用） 所有数 → 0 ~ 1 之间
# X-Xmin/Xman-Xmin
# 2. Z-Score 标准化（均值 0，方差 1）
# X-mean/std
# 3. 按列/行标准化（机器学习常用） axis=0 → 按列、axis=1 → 按行
# col_min = mat.min(axis=0)
# col_max = mat.max(axis=0)
# mat_col_norm = (mat - col_min) / (col_max - col_min)

# 机器学习 / 数据分析默认必须按列算
# 行：每一行 = 一条样本
# 列：每一列 = 一个特征/指标

# Z-Score
data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("原始数据: ")
print(data)
# 计算每列的均值和标准差
mean = np.mean(data, axis=0)  # 每列均值
std = np.std(data, axis=0)  # 每列标准差
print("每列均值: ", mean)
print("每列标准差: ", std)
# 标准化（广播应用）
standardized = (data - mean) / std
print("标准化后的数据: ")
print(standardized)
print("形状: ", standardized.shape)
print("." * 50)

# RGB 颜色调整
# 广播在图像处理中的应用
# 假设有一个256x256x3的RGB图像
# 256 * 256, 3个通道
image = np.random.randint(0, 256, size=(256, 256, 3), dtype=np.uint8)
# 创建一个调整数组（3个元素，分别对应R、G、B通道）
adjust = np.array([1.2, 1.1, 0.9])  # 调整亮度

# 应用调整（广播）
# NumPy 会自动把 adjust 扩展成
# (256, 256, 3)
# 每个像素的 R × 1.2
# 每个像素的 G × 1.1
# 每个像素的 B × 0.9
# 完全自动，不用写循环

adjusted_image = image * adjust
print("原图像形状: ", image.shape)
print("调整数组形状: ", adjust.shape)
print("调整后图像形状: ", adjusted_image.shape)
# 显示调整前后的像素值
print("原像素值: ", image[0, 0])
print("调整后像素值: ", adjusted_image[0, 0])

# 只要最后一维大小相同，就能自动匹配
# (256,256,3) × (3,) → 自动广播 → (256,256,3)
# 这就是 NumPy 处理图像最常用、最简洁、最高效的写法

# 提醒（非常重要）
# image 是 uint8（0~255 整数）乘以小数后会变成 float 类型，值可能超过 255 或低于 0
# 如果要转回正常图像，需要
# 把调整后的像素值，强行拉回合法的图片范围（0~255），并转回图像标准类型
# 第一步：np.clip (数值，最小值，最大值)
# 作用：把所有数字限制在 0 ~ 255 之间
# 第二步：astype (np.uint8)
# 作用：把浮点数 转回 图像专用的整数类型

# adjusted_image = np.clip(adjusted_image, 0, 255).astype(np.uint8)

print("." * 50)


# 4.4 通用函数（ufunc）
# 通用函数介绍
# 通用函数（ufunc）是对数组进行逐元素操作的函数
# 它们在底层使用编译的C代码执行，速度快
# 数学函数
arr = np.array([1, 2, 3, 4])
print("数组: ", arr)
print("sin: ", np.sin(arr))
print("cos: ", np.cos(arr))
print("exp: ", np.exp(arr))
print("log: ", np.log(arr))
print("sqrt: ", np.sqrt(arr))
# 聚合函数
print("求和: ", np.sum(arr))
print("求积: ", np.prod(arr))
print("最大值: ", np.max(arr))
print("最小值: ", np.min(arr))
print("平均值: ", np.mean(arr))
print("*" * 50)

# ufunc 的 reduce 方法
# reduce = 两两递归合并，多变一
# ufunc 的 reduce 方法可以沿指定轴进行聚合
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
print("二维数组: ")
print(arr_2d)
# 沿行求和（axis=1）
sum_rows = np.add.reduce(arr_2d, axis=1)
print("沿行求和: ", sum_rows)
# 沿列求和（axis=0）
sum_cols = np.add.reduce(arr_2d, axis=0)
print("沿列求和: ", sum_cols)
# 计算累积和
# accumulate 累积
# 一步步累加，保留每一步中间结果，长度和原数组一致
cumsum = np.add.accumulate(arr_2d, axis=1)
print("累积和: ")
print(cumsum)
# [[ 1  3  6]
#  [ 4  9 15]]
print("*" * 50)

# 5 随机数生成与统计函数
# 5.1 随机数生成函数
# 5.1.1 常见随机分布
# 均匀分布
# 生成均匀分布随机数
# np.random.rand(d0, d1, ..., dn) 生成[0, 1)之间的随机数
print("生成5个均匀分布随机数: ", np.random.rand(5))
print("生成3x4均匀分布随机数矩阵: ")
print(np.random.rand(3, 4))
# np.random.uniform(low, high, size) 生成[low, high)之间的随机数
print("生成[1, 10)之间的5个随机数: ", np.random.uniform(1, 10, 5))
print("." * 50)

# 正态分布
# 生成正态分布随机数
# np.random.randn(d0, d1, ..., dn) 生成标准正态分布（均值0，标准差1）
print("生成5个标准正态分布随机数: ", np.random.randn(5))
print("生成2x3标准正态分布矩阵: ")
print(np.random.randn(2, 3))
# np.random.normal(mean, std, size) 生成指定均值和标准差的正态分布
print("生成均值5，标准差2的100个随机数: ")
rand_normal = np.random.normal(5, 2, 100)
print("均值: ", np.mean(rand_normal))
print("标准差: ", np.std(rand_normal))
print("." * 50)

# 其他分布
# 生成随机整数
print("生成[0, 10)之间的5个随机整数: ", np.random.randint(0, 10, 5))
print("生成[1, 100)之间的3x4随机整数矩阵: ")
print(np.random.randint(1, 100, (3, 4)))
# 概率论里面有，自己看嘛
# 生成泊松分布
print("生成λ=5的泊松分布随机数（10个）: ", np.random.poisson(5, 10))
# 生成指数分布
print("生成λ=2的指数分布随机数（10个）: ", np.random.exponential(2, 10))
print("*" * 50)


# 5.1.2 随机种子与可重复性
# 设置随机种子
# 设置随机种子以确保结果可重现
np.random.seed(42)
# 生成随机数
rand1 = np.random.rand(5)
rand2 = np.random.randn(5)
rand3 = np.random.randint(0, 10, 5)
print("设置种子42后的随机数: ")
print("rand: ", rand1)
print("randn: ", rand2)
print("randint: ", rand3)
# 再次设置相同的种子，会得到相同的结果
np.random.seed(42)
rand1_again = np.random.rand(5)
print("再次设置种子42后的rand: ", rand1_again)

# np.array_equal
# 用来判断【两个 NumPy 数组是否完全一模一样】
# 形状相同 + 每个元素都相同 → 返回 True，否则 False。
print("与之前的rand是否相同: ", np.array_equal(rand1, rand1_again))
# 特别注意：浮点数不要直接用
# 浮点数有精度误差，比如 0.1+0.2 不是精确 0.3
# 所以浮点数比较要用:
# np.allclose(a, b)   # 允许微小误差
print("." * 50)

# RandomState 对象
# np.random.RandomState (seed) = 独立、干净、可复现的随机数生成器
# 使用RandomState对象来管理随机数生成
# ✅ 独立随机流（自己玩自己的）
# ✅ 可复现（设置种子后结果永远一样）
# ✅ 不污染全局随机状态
# ✅ 多线程、多实验安全
# 最重要的好处: 结果 100% 可复现
# 实验、机器学习、算法必须要可复现，否则别人跑不出你的结果
rng = np.random.RandomState(42)
print("使用RandomState生成的随机数: ")
print("rand: ", rng.rand(5))
print("randn: ", rng.randn(5))
print("randint: ", rng.randint(0, 10, 5))
# 不同的RandomState对象生成不同的序列
rng2 = np.random.RandomState(43)
print("另一个RandomState: ")
print("rand: ", rng2.rand(5))
print("*" * 50)

# 5.2 统计函数应用
# 5.2.1 基本统计函数
# 聚合统计函数
# 创建一个示例数组
arr = np.array([1, 3, 5, 7, 9, 2, 4, 6, 8, 10])
print("数组: ", arr)
print("元素总和: ", np.sum(arr))
print("元素乘积: ", np.prod(arr))
print("最大值: ", np.max(arr))
print("最小值: ", np.min(arr))
print("平均值: ", np.mean(arr))
print("中位数: ", np.median(arr))
print("标准差: ", np.std(arr))
print("方差: ", np.var(arr))
print("." * 50)

# 带 axis 参数的统计函数
# 创建一个二维数组
arr_2d = np.array([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
])
print("二维数组: ")
print(arr_2d)
print("沿axis=0（列）统计: ")
print("每列和: ", np.sum(arr_2d, axis=0))
print("每列均值: ", np.mean(arr_2d, axis=0))
print("每列最大值: ", np.max(arr_2d, axis=0))
print("沿axis=1（行）统计: ")
print("每行和: ", np.sum(arr_2d, axis=1))
print("每行均值: ", np.mean(arr_2d, axis=1))
print("每行最大值: ", np.max(arr_2d, axis=1))
print("*" * 50)


# 5.2.2 高级统计函数
# 百分位数和分位数
# 计算百分位数
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print("数组: ", arr)
print("第25百分位数（Q1）: ", np.percentile(arr, 25))
print("第50百分位数（Q2/中位数）: ", np.percentile(arr, 50))
print("第75百分位数（Q3）: ", np.percentile(arr, 75))
# 计算四分位数
q1, q2, q3 = np.percentile(arr, [25, 50, 75])
print(f"四分位数: Q1={q1}, Q2={q2}, Q3={q3}")
# 计算四分位距（IQR）
iqr = q3 - q1
print(f"四分位距: {iqr}")

# 百分位数：给数据 “排档位”，看百分之多少的数据在它前面
# 百分位数 Percentile
# 定义
# 一组数据从小到大排序后，P% 百分位数：有 P% 的数据 ≤ 该值，(100−P%) 的数据 ≥ 该值。
# 核心意义
# 刻画数据位置、水平层级
# 不受极端最大值 / 最小值影响，比平均值更稳健
# 用来做排名、分层、对比（如：班级成绩前 10%、收入分档）

# 例子：25 百分位数 = 3.25代表：25% 的数据 ≤ 3.25
# 一、计算公式（numpy默认插值）
# 位置公式：
# # pos = (n−1) × p/100, p位数
# Q1第25百分位
# pos = (10−1)×0.25 = 2.25
# 下标：
# 整数位：2→ 元素arr[2] = 3
# 小数位：0.25
# 下一个元素：arr[3] = 4
# Q1 = arr[2] + 0.25×(arr[3]−arr[2])
# Q1 = 3 + 0.25×(4−3) = 3.25

# 为什么 25% 分位数是 3.25，却卡着 30% 的数据？
# 百分位数不是「数个数硬切」，是「连续插值刻度」
# 人话解释
# 纯整数数据是离散的
# 百分位数是连续平滑的分界线
# 严格小于 3.25：3 个 → 30%
# 理论定义：至少 25% 数据 ≤ 该值
# 3.25 满足：有 ≥25% 的数在它左边，是标准 25% 分割线

# 一句话总结
# 离散整数数据，个数占比不会刚好卡 25%、50%
# 百分位数用插值算出一个「精准分割刻度」
# 不用纠结个数百分比不完全对齐
# 3.25 就是数学上标准的第 25 百分位数，统计、Python、考试都按这个算

# 四分位数：用三条线把数据切 4 份，看清整体分布结构
# 四分位数是三个特殊百分位数，把有序数据平均切成 4 段，每段各占 25%：
# Q1 下四分位数 = 25% 百分位数
# 前 25% 与后 75% 的分界线（低端临界值）
# Q2 中位数 = 50% 百分位数
# 数据正中间，一半大、一半小，反映整体中间水平
# Q3 上四分位数 = 75% 百分位数
# 前 75% 与后 25% 的分界线（高端临界值）
# 意义
# 直观看出数据：集中区间、偏左 / 偏右、分布疏密
# 不被极端异常值带偏，适合偏态数据

# IQR 四分位距：衡量中间一半数据的分散大小，专门用来揪异常值
# IQR=Q3−Q1
# 意义
# 代表中间 50% 数据的波动 / 离散程度
# 极强抗干扰：完全不受最大值、最小值、异常值影响
# 数据分析最核心用途：检测异常值（离群点）
# 经典异常值判定规则
# 下界：
# Q1−1.5×IQR
# 上界：
# Q3+1.5×IQR
# 超出上下界 → 判定为异常值，需要剔除 / 修正
print("." * 50)

# 加权统计
# 计算加权平均值
values = np.array([1, 2, 3, 4])
weights = np.array([0.1, 0.2, 0.3, 0.4])
# 加权和
weighted_sum = np.sum(values * weights)
# 权重和
weight_sum = np.sum(weights)
# 加权平均
weighted_mean = weighted_sum / weight_sum
print("数值: ", values)
print("权重: ", weights)
print("加权和: ", weighted_sum)
print("权重和: ", weight_sum)
print("加权平均: ", weighted_mean)
# 使用np.average计算加权平均
weighted_mean_np = np.average(values, weights=weights)
print("使用np.average: ", weighted_mean_np)
print("*" * 50)


# 5.3 数据处理函数
# 5.3.1 排序与去重
# 排序函数
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5])
print("原数组: ", arr)
# 排序（返回新数组）
sorted_arr = np.sort(arr)
print("排序后: ", sorted_arr)
# 原地排序
arr.sort()
# ✅ np.sort () — 留原数组，返回新数组
# ❌ arr.sort () — 吃原数组，无返回值
print("原地排序后: ", arr)
# 二维数组排序
arr_2d = np.array([[3, 1], [4, 6], [2, 5]])
print("二维数组: ")
print(arr_2d)
# 按行排序
sorted_2d = np.sort(arr_2d, axis=1)
print("按行排序: ")
print(sorted_2d)
# 按列排序
sorted_2d_col = np.sort(arr_2d, axis=0)
print("按列排序: ")
print(sorted_2d_col)
print("." * 50)

# argsort 函数
# argsort返回排序后的索引
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6, 5])
print("原数组: ", arr)

# np.sort → 返回排好序的值
# np.argsort → 返回值对应的原位置（索引）
# 返回的不是排序后的值，而是「排序后每个元素在原数组中的下标（索引）」
# np.sort(arr) → 得到 值：[1, 1, 2, 3, 4, 5, 5, 6, 9]
# np.argsort(arr) → 得到 索引：[1, 3, 6, 0, 2, 4, 8, 7, 5]
# 排序后的第 0 位（最小）：来自原数组下标 **1**
# 排序后的第 1 位：来自原数组下标 **3**
# 排序后的第 2 位：来自原数组下标 **6**
# ...
# 排序后的最后一位（最大）：来自原数组下标 **5**

indices = np.argsort(arr)
print("排序索引: ", indices)
print("根据索引排序: ", arr[indices])
# 找出最大的3个元素的索引
top3_indices = np.argsort(arr)[-3:]
print("最大的3个元素索引: ", top3_indices)
print("最大的3个元素: ", arr[top3_indices])
print("." * 50)

# 去重函数
# 去重函数np.unique
# 找出数组里所有不重复的元素 **，并且自动从小到大排序，返回干净的唯一值列表 **
arr = np.array([1, 2, 3, 2, 1, 4, 5, 4])
print("原数组: ", arr)
# 找出唯一值
unique_values = np.unique(arr)
print("唯一值: ", unique_values)
# 返回唯一值和出现次数
# return_counts=True 额外返回第二个数组：每个唯一值的出现次数
unique_values, counts = np.unique(arr, return_counts=True)
print("唯一值和计数: ")
# zip 遍历
# 把「唯一值」和「对应次数」一一配对，循环打印，清晰查看频次
for value, count in zip(unique_values, counts):
    print(f"{value}: {count}次")

# 保持顺序的去重（需要额外操作）
seen = set()
unique_ordered = []
for x in arr:
    if x not in seen:
        seen.add(x)
        unique_ordered.append(x)
print("保持顺序的唯一值: ", unique_ordered)
print("*" * 50)


# 5.3.2 条件筛选与聚合
# 条件筛选
# 使用where进行条件筛选
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print("原数组: ", arr)
# 找出大于5的元素
greater_5 = arr[arr > 5]
print("大于5的元素: ", greater_5)

# 使用where函数
# np.where(条件, 满足时的值, 不满足时的值)
# 相当于数组版的 if...else...，逐元素判断，返回新数组
# 只返回满足条件的索引（超级常用）
# 最常用场景：
# 找异常值
# 找满足条件的位置
# 替换特定数值

# 图像 / 数据处理最常用：替换值
# 小于0 → 变成0；大于255 → 变成255
# img = np.array([-5, 10, 260, 80])
# fixed = np.where(img < 0, 0, np.where(img > 255, 255, img))
# np.where(条件, A, B)
# → 满足条件用 A，不满足用 B
# np.where(条件)
# → 只返回满足条件的索引

indices = np.where(arr > 5)
print("大于5的元素索引: ", indices)
print("根据索引获取元素: ", arr[indices])
# 找出等于3或7的元素
indices2 = np.where((arr == 3) | (arr == 7))
print("等于3或7的元素索引: ", indices2)
print("." * 50)

# 分组聚合
# 实现简单的分组聚合
# 数据: 学生成绩
students = np.array(['Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie'])
scores = np.array([85, 92, 78, 90, 88, 76])
print("学生: ", students)
print("成绩: ", scores)
# 找出唯一学生
unique_students = np.unique(students)
print("唯一学生: ", unique_students)
# 计算每个学生的平均成绩
print("每个学生的平均成绩: ")
for student in unique_students:
    # 判断姓名是否一致，T/F
    # 第一次循环
    # mask[True False False True False False]
    mask = students == student
    # print("mask", mask)
    student_scores = scores[mask]
    avg_score = np.mean(student_scores)
    print(f"{student}: {avg_score:.1f}")
# 使用字典存储结果
result = {}
for student in unique_students:
    mask = students == student
    result[student] = np.mean(scores[mask])
print("结果字典: ", result)
print("*" * 50)


# 6 数组高级操作与性能优化
# 6.1 数组拼接与分割
# 6.1.1 数组拼接函数
# concatenate 函数
# 最基础的拼接函数
arr1 = np.array([[1, 2], [3, 4]])
arr2 = np.array([[5, 6], [7, 8]])
print("数组1: ")
print(arr1)
print("数组2: ")
print(arr2)
# 沿axis=0（垂直方向）拼接
vertical_concat = np.concatenate((arr1, arr2), axis=0)
print("沿axis=0拼接: ")
print(vertical_concat)
# 沿axis=1（水平方向）拼接
horizontal_concat = np.concatenate((arr1, arr2), axis=1)
print("沿axis=1拼接: ")
print(horizontal_concat)
print("." * 50)

# vstack 和 hstack 函数
# Vertical
# vstack（垂直堆叠）相当于axis=0的concatenate
vstack_result = np.vstack((arr1, arr2))
print("vstack结果: ")
print(vstack_result)
# Horizontal
# hstack（水平堆叠）相当于axis=1的concatenate
hstack_result = np.hstack((arr1, arr2))
print("hstack结果: ")
print(hstack_result)
# 一维数组的堆叠
arr3 = np.array([1, 2, 3])
arr4 = np.array([4, 5, 6])
print("一维数组: ")
print("arr3: ", arr3)
print("arr4: ", arr4)
print("vstack: ")
print(np.vstack((arr3, arr4)))  # 变成2x3数组
print("hstack: ")
print(np.hstack((arr3, arr4)))  # 变成1x6数组
print("." * 50)

# stack 函数
# stack函数在新的维度上堆叠
# ✔ axis=0
# 两个数组上下放 → 分成两大块
# [[[1 2]
#   [3 4]]
#
#  [[5 6]
#   [7 8]]]
# ✔ axis=1
# 按行交叉放 → 每行一对
# [[[1 2]
#   [5 6]]
#
#  [[3 4]
#   [7 8]]]
# ✔ axis=2
# 按元素逐个配对放 → 每个元素一对
# [[[1 5]
#   [2 6]]
#
#  [[3 7]
#   [4 8]]]
# 图像场景最常用
# axis=2 就是 把两个单通道图 → 合成双通道图
# 就像 R、G、B 三个通道捆绑成彩色图

print("原始数组: ")
print("arr1: ")
print(arr1)
print("arr2: ")
print(arr2)
# 在axis=0上堆叠（创建一个新的维度）
stacked_0 = np.stack((arr1, arr2), axis=0)
print("axis=0堆叠后形状: ", stacked_0.shape)
print("堆叠后数组: ")
print(stacked_0)
# 在axis=1上堆叠
stacked_1 = np.stack((arr1, arr2), axis=1)
print("axis=1堆叠后形状: ", stacked_1.shape)
print("堆叠后数组: ")
print(stacked_1)
# 在axis=2上堆叠
stacked_2 = np.stack((arr1, arr2), axis=2)
print("axis=2堆叠后形状: ", stacked_2.shape)
print("堆叠后数组: ")
print(stacked_2)
print("*" * 50)


# 6.1.2 数组分割函数
# split 函数
# 把一个数组，按指定数量 / 指定位置，切分成多个子数组
# 必须等分切割（长度要整除）
# 返回：切割后的「数组列表」
# 分割函数
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8])
print("原数组: ", arr)
# 平均分割成2份
split1, split2 = np.split(arr, 2)
print("平均分割成2份: ")
print("split1: ", split1)
print("split2: ", split2)
# 按指定位置分割
split3, split4, split5 = np.split(arr, [3, 5])  # 在索引3和5处分割
print("按位置[3,5]分割: ")
print("split3: ", split3)
print("split4: ", split4)
print("split5: ", split5)
print("." * 50)

# vsplit 和 hsplit 函数
# 垂直 = 上下方向 = 沿着行切割（拆分行）
# 水平 = 左右方向 = 沿着列切割（拆分列）
# 创建一个4x4数组
arr_2d = np.array([
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16]
])
print("4x4数组: ")
print(arr_2d)
# vsplit垂直分割（按行）
top_half, bottom_half = np.vsplit(arr_2d, 2)
print("垂直分割成2部分: ")
print("上半部分: ")
print(top_half)
print("下半部分: ")
print(bottom_half)
# hsplit水平分割（按列）
left_half, right_half = np.hsplit(arr_2d, 2)
print("水平分割成2部分: ")
print("左半部分: ")
print(left_half)
print("右半部分: ")
print(right_half)
# 分割成更多部分
part1, part2, part3 = np.hsplit(arr_2d, [1, 3])  # 在列1和3处分割
print("按列位置[1,3]分割: ")
print("part1: ")
print(part1)
print("part2: ")
print(part2)
print("part3: ")
print(part3)
print("*" * 50)


# 6.2 性能优化技巧
# 6.2.1 向量化运算优化
# 避免显式循环
# 对比循环和向量化运算的性能
# 创建两个大数组
size = 1000000
arr1 = np.random.rand(size)
arr2 = np.random.rand(size)

# 方法1: 使用向量化运算
# 不用写循环（for/while），直接对整个数组做数学运算NumPy 会自动逐元素并行计算，速度极快
# 不用循环
# 代码极短
# 运行极快（C 语言底层加速）
# 逐元素自动计算
start = time.time()
result_vectorized = arr1 * arr2 + np.sin(arr1) + np.cos(arr2)
vectorized_time = time.time() - start
# 方法2: 使用显式循环（不推荐）
result_loop = np.zeros_like(arr1)
start = time.time()
for i in range(size):
    result_loop[i] = arr1[i] * arr2[i] + np.sin(arr1[i]) + np.cos(arr2[i])
loop_time = time.time() - start
print(f"向量化运算时间: {vectorized_time:.4f}秒")
print(f"循环运算时间: {loop_time:.4f}秒")
print(f"向量化运算快{loop_time / vectorized_time:.1f}倍")
# 计算速度提升
speedup = loop_time / vectorized_time
print(f"速度提升: {speedup:.1f}倍")
print(50 * ".")


# 利用 ufunc 的向量化特性
# 使用 ufunc 进行向量化运算
arr = np.array([1, 2, 3, 4, 5])
# 同时计算多个函数
result = np.sin(arr) + np.cos(arr) + np.tan(arr) + np.exp(arr) + np.log(arr)
print("同时计算多个函数: ", result)
# 使用ufunc.reduce进行累积运算
cumulative = np.add.reduce(arr)
print("累积和: ", cumulative)
# 使用ufunc.accumulate进行累积操作
cumulative_steps = np.add.accumulate(arr)
print("累积步骤: ", cumulative_steps)
print(50 * "*")


# 6.2.2 内存优化与视图
# 内存连续存储

# 确保数组是内存连续的
# C连续（C - order） vs F连续（F - order）
# C 连续（C_CONTIGUOUS）= 行优先（默认）
# 内存里：先存完一整行，再存下一行
# F 连续（F_CONTIGUOUS）= 列优先
# C 连续 = 行优先（默认），最后一维变化最快
# F 连续 = 列优先，第一维变化最快
# .flags.c_contiguous / f_contiguous 查看状态
# 访问数据：顺连续维度遍历最快

# 内存里：先存完一整列，再存下一列
arr = np.array([[1, 2, 3], [4, 5, 6]])
print("原始数组: ")
print(arr)
print("是否C连续: ", arr.flags.c_contiguous)
print("是否F连续: ", arr.flags.f_contiguous)
# 创建一个不连续的数组（通过切片）
non_contiguous = arr[::2]
print("切片后的数组: ")
print(non_contiguous)
print("是否C连续: ", non_contiguous.flags.c_contiguous)
# 转换为连续数组
contiguous_arr = non_contiguous.copy()
print("转换为连续数组: ")
print("是否C连续: ", contiguous_arr.flags.c_contiguous)
print(50 * ".")

# 使用视图避免内存复制
# 创建一个大数组
big_arr = np.random.rand(10000, 10000)
# 方法1: 使用切片（视图）获取子数组
start = time.time()
subview = big_arr[: 1000, :1000]  # 视图，不复制数据
view_time = time.time() - start
# 方法2: 使用copy()获取子数组
start = time.time()
subcopy = big_arr[: 1000, :1000].copy()  # 复制数据
copy_time = time.time() - start
print(f"获取视图时间: {view_time:.4f}秒")
print(f"获取副本时间: {copy_time:.4f}秒")
# print(f"视图操作快{copy_time / view_time:.1f}倍")
# 验证内存使用
print(f"视图内存大小: {subview.nbytes / 1024 / 1024:.1f}MB")
print(f"副本内存大小: {subcopy.nbytes / 1024 / 1024:.1f}MB")
print("注意: 视图不占用额外内存")
print(50 * "*")


# 6.3 广播机制优化
# 合理使用广播

# ✔ 广播 = 自动扩展维度 + 向量化计算
# ✔ 无复制、无循环、极快
# ✔ NumPy 最核心、最强大、最优雅的功能
# ✔ 能广播绝对不要写 for 循环

# 广播机制优化示例
# 原始方法: 创建大数组
arr = np.random.rand(1000, 1000)
scalars = np.array([1.0, 1.1, 1.2, 1.3, 1.4])
# 方法1: 使用广播（推荐）
start = time.time()

# 1. scalars[:, np.newaxis, np.newaxis]
# 作用：给数组增加新的维度
# np.newaxis = 增加一个大小为 1 的维度
# ① 原始
# scalars.shape = (5,)
# ② 加第一个 newaxis
# scalars[:, np.newaxis].shape = (5, 1)
# ③ 加第二个 newaxis
# scalars[:, np.newaxis, np.newaxis].shape = (5, 1, 1)
# 2. 现在两边形状变成
# arr shape:          (1000, 1000)
# scalars 形状:    (5,     1,      1)
# 3. NumPy 广播机制自动做什么？
# 广播规则：维度为 1 的轴会自动扩展到匹配对方大小
# (5, 1, 1)
# → 自动扩展 →
# (5, 1000, 1000)
# 全程不复制数据，不占额外内存
# 4. 最终相乘
# arr * scalars[:, np.newaxis, np.newaxis] = (1000,1000) * (5,1,1) = (5,1000,1000)

# [1.0, 1.1, 1.2, 1.3, 1.4]
# 变为
# [
#  [1.0],
#  [1.1],
#  [1.2],
#  [1.3],
#  [1.4]
# ]
# 变为
# [
#  [[1.0]],
#  [[1.1]],
#  [[1.2]],
#  [[1.3]],
#  [[1.4]]
# ]

result_broadcast = arr * scalars[:, np.newaxis, np.newaxis]
broadcast_time = time.time() - start
# 方法2: 使用循环（不推荐）
result_loop = []
start = time.time()
for scalar in scalars:
    result_loop.append(arr * scalar)
loop_time = time.time() - start
print(f"广播方法时间: {broadcast_time:.4f}秒")
print(f"循环方法时间: {loop_time:.4f}秒")
print(f"广播方法快{loop_time / broadcast_time:.1f}倍")
# 验证结果一致性
result_stack = np.stack(result_loop, axis=0)
print(f"结果是否一致: {np.allclose(result_broadcast, result_stack)}")
print(50 * ".")

# 广播规则的实际应用
# 一个复杂的广播示例
# 假设有一个3D数组（样本数，高度，宽度）
samples = 100
height = 256
width = 256
channels = 3
# 创建数据和均值、标准差
data = np.random.rand(samples, height, width, channels)
means = np.array([0.485, 0.456, 0.406])  # 通道均值
stds = np.array([0.229, 0.224, 0.225])  # 通道标准差
# 标准化（广播应用）
start = time.time()
normalized = (data - means) / stds
broadcast_time = time.time() - start
print(f"标准化时间: {broadcast_time:.4f}秒")
print(f"广播后形状: {normalized.shape}")
# 验证广播规则
print("广播验证: ")
print(f"data形状: {data.shape}")
print(f"means形状: {means.shape}")
print(f"stds形状: {stds.shape}")
print("解释: means和stds被广播为与data相同的形状")
