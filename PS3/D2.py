import pandas as pd


class DataPreprocessor:
    def __init__(self, min_gmv=0, fill_orders=0):
        self.min_gmv = min_gmv
        self.fill_orders = fill_orders
        self.report = {}

    def _drop_dup(self, df):
        n0 = len(df);
        df = df.drop_duplicates(["day", "channel"])
        self.report["去重删除"] = n0 - len(df);
        return df

    def _fix_type(self, df):
        df["day"] = pd.to_datetime(df["day"], errors="coerce")
        df["gmv"] = pd.to_numeric(df["gmv"], errors="coerce")
        return df

    def _fill_na(self, df):
        n = int(df["orders"].isna().sum())
        df["orders"] = df["orders"].fillna(self.fill_orders).astype(int)
        self.report["订单缺失填充"] = n;
        return df

    def _clip(self, df):
        n0 = len(df);
        df = df[df["gmv"] >= self.min_gmv]
        self.report["GMV异常过滤"] = n0 - len(df);
        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        for step in (self._drop_dup, self._fix_type, self._fill_na, self._clip):
            df = step(df)
        df["day"] = pd.to_datetime(df["day"]).dt.strftime("%Y-%m-%d")
        self.report["最终行数"] = len(df)
        return df.reset_index(drop=True)