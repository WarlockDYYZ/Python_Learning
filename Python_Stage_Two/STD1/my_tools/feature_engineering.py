import pandas as pd


class FeatureEngineer:
    """特征工程类"""

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def create_time_features(self, date_col: str) -> pd.DataFrame:
        """创建时间特征"""

        '''
            self.df[date_col] 必须是 datetime65 时间类型
            dt 只能用在 datetime 类型上
            .dt.year 最终得到的 year 是整数（int）
            
            .dt 是 pandas 专门给【时间类型】提供的属性工具
            只有列是 datetime64 才能用 .dt
                .dt.year 年
                .dt.month 月
                .dt.day 日
                .dt.hour 时
                .dt.weekday 星期
        '''
        self.df['year'] = self.df[date_col].dt.year
        self.df['month'] = self.df[date_col].dt.month
        self.df['day'] = self.df[date_col].dt.day
        self.df['weekday'] = self.df[date_col].dt.weekday

        return self.df

    def calculate_rfm_features(self, customer_id: str, revenue_col: str, date_col: str) -> pd.DataFrame:
        """计算RFM指标"""

        # 计算最近购买时间
        max_date = self.df[date_col].max()  # 获取日期列的最大值(最晚的日期)

        rfm_df = self.df.groupby(customer_id).agg({  # 根据 customer_id 分组(每个用户算一行) 聚合
            date_col: lambda x: (max_date - x.max()).days,  # Recency   # 每组(每个用户)最后一次购买距今的天数，只要日(整数)
            customer_id: 'count',  # Frequency  计数(有多少天订单)
            revenue_col: 'sum'  # Monetary  求和(消费了多少钱)
        }).rename(columns={
            date_col: 'recency',
            customer_id: 'frequency',
            revenue_col: 'monetary'
        })

        return rfm_df
