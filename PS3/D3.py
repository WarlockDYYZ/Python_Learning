import math
import pandas as pd
from app.db_storage import db_cursor


class QueryService:
    def query(self, start=None, end=None, channels=None, limit=None):
        sql, params = "SELECT day, channel, gmv, orders FROM sales WHERE 1=1", []

        if start is not None:
            sql += " AND day >= ?"
            params.append(start)
        if end is not None:
            sql += " AND day <= ?"
            params.append(end)

        if channels:
            sql += " AND channel IN (%s)" % ",".join("?" * len(channels))
            params += list(channels)

        sql += " ORDER BY day, channel"

        if limit is not None:
            sql += " LIMIT ?"
            params.append(int(limit))

        with db_cursor() as cur:
            rows = cur.execute(sql, params).fetchall()
        return pd.DataFrame([dict(r) for r in rows])

    def summarize(self, start=None, end=None):
        df = self.query(start, end)

        if df.empty:
            return {"total_gmv": 0.0, "total_orders": 0, "by_channel": []}

        total_gmv = df["gmv"].sum()
        total_orders = df["orders"].sum()

        safe_total_gmv = 0.0 if pd.isna(total_gmv) else round(float(total_gmv), 2)
        safe_total_orders = 0 if pd.isna(total_orders) else int(total_orders)

        g = df.groupby("channel", as_index=False).agg(
            gmv=("gmv", "sum"), orders=("orders", "sum")
        )

        return {
            "total_gmv": safe_total_gmv,
            "total_orders": safe_total_orders,
            "by_channel": g.to_dict("records")
        }