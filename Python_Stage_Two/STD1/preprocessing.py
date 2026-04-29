import pandas as pd


class DataPreprocessor:
    """数据预处理类"""

    '''
        类似其他语言的 “构造函数”，是类的初始化方法
        当你创建这个类的对象时，它会自动第一个运行
        
        self = 创建出来的 “对象自己”
        可以理解成：这个类内部的 “专属变量容器”
        所有存在 self.xxx 里的东西，整个类里的所有函数都能用
        
        调用流程：
        传进去：my_data
        ↓
        __init__ 收到：df = my_data
        ↓
        存起来：self.df = my_data
        ↓
        类里面所有函数都能用：self.df
    '''

    def __init__(self, df: pd.DataFrame):
        self.df = df

    '''
        self 必须写在第一个参数,代表当前对象自己,用来访问 self.df（存在类里的数据）
        columns: list 传入要填充空值的列（类型为列表）
        fill_value: any = 0 用什么值去填充空值，默认是 0（不传就自动用 0），可以填：None / '未知' / 平均数（mean） 等

        -> pd.DataFrame 返回值类型提示，表示这个函数最后返回处理好的表格
    '''
    def fill_missing(self, columns: list, fill_value: any = 0) -> pd.DataFrame:
        """填充缺失值"""
        self.df[columns] = self.df[columns].fillna(fill_value)

        return self.df

    '''
        对指定的数值列，用 Z‑score 算法剔除极端异常值（离群点）
        比如：订单金额突然出现 999999、年龄写 200 这种离谱数据，都会被删掉
        
        column: str：要剔除异常值的列名（如 'order_amount'）
        threshold: int = 3：Z 分数阈值，默认 3（统计学标准）
        -> pd.DataFrame：返回处理后的表格
    '''
    def remove_outliers(self, column: str, threshold: int = 3) -> pd.DataFrame:
        """使用Z-score法去除异常值"""
        from scipy.stats import zscore  # 导入工具
        z_scores = zscore(self.df[column])  # 计算Z‑score
        self.df = self.df[(z_scores < threshold)]   # 筛选正常数据（核心）
        # (z_scores < threshold) 返回 布尔 Series (bool Series)，方括号内的代码本身具有完整的语义，可以不加括号；加括号是一个好习惯，在复杂逻辑条件时阅读起来更清晰

        return self.df

    '''
        date_columns: list：必须传一个列表，里面是要转成日期的列名
    '''
    def convert_dates(self, date_columns: list) -> pd.DataFrame:
        """转换日期格式"""
        # 要转换的日期是一个列表，包含多列，使用循环每次处理一列，使用 .to_datetime()
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col])

        return self.df
