import pandas as pd


class DataPreprocessor:
    def __init__(self, min_gmv=0, fill_orders=0):
        self.min_gmv = min_gmv
        self.fill_orders = fill_orders
        self.report = {}

    def _drop_dup(self, df):
        n0 = len(df)
        # 显式指定 subset 参数
        df = df.drop_duplicates(subset=["day", "channel"])
        self.report["去重删除"] = n0 - len(df)
        return df

    def _fix_type(self, df):
        df["day"] = pd.to_datetime(df["day"], errors="coerce", format="%Y-%m-%d")
        df["gmv"] = pd.to_numeric(df["gmv"], errors="coerce")
        return df

    def _fill_na(self, df):
        n = int(df["orders"].isna().sum())
        df["orders"] = pd.to_numeric(df["orders"], errors="coerce")
        df["orders"] = df["orders"].fillna(self.fill_orders).astype("Int64")
        self.report["订单缺失填充"] = n
        return df

    def _filter_gmv(self, df):
        n = int(df["orders"].isna().sum())
        df["orders"] = pd.to_numeric(df["orders"], errors="coerce")
        # 支持 NaN 的 Int64 类型
        df["orders"] = df["orders"].fillna(self.fill_orders).astype("Int64")
        self.report["订单缺失填充"] = n;
        return df

    def _clip(self, df):
        n0 = len(df)
        df = df[(df["gmv"] >= self.min_gmv) & (df["gmv"].notna())]
        self.report["GMV异常过滤"] = n0 - len(df)
        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        for step in (self._fix_type, self._drop_dup, self._fill_na, self._filter_gmv):
            n_before = len(df)
            df = step(df)
            print(f"{step.__name__:>12}  {n_before:>8} -> {len(df)}  {self.report}")
        df["day"] = pd.to_datetime(df["day"]).dt.strftime("%Y-%m-%d")
        self.report["最终行数"] = len(df)
        return df.reset_index(drop=True)
