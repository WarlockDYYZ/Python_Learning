import pandas as pd
from app.db_storage import db_cursor


class QueryService:
    def query(self, start=None, end=None, channels=None, limit=None):
        sql, params = "SELECT day, channel, gmv, orders FROM sales WHERE 1=1", []
        if start:   sql += " AND day >= ?"; params.append(start)
        if end:     sql += " AND day <= ?"; params.append(end)
        if channels:
            sql += " AND channel IN (%s)" % ",".join("?" * len(channels))
            params += list(channels)
        sql += " ORDER BY day, channel"
        if limit:   sql += " LIMIT ?"; params.append(int(limit))
        with db_cursor() as cur:
            rows = cur.execute(sql, params).fetchall()
        return pd.DataFrame([dict(r) for r in rows])

    def summarize(self, start=None, end=None):
        df = self.query(start, end)
        if df.empty:
            return {"total_gmv": 0.0, "total_orders": 0, "channels": []}
        g = df.groupby("channel", as_index=False).agg(
            gmv=("gmv", "sum"), orders=("orders", "sum"))
        return {"total_gmv": round(float(df.gmv.sum()), 2),
                "total_orders": int(df.orders.sum()),
                "by_channel": g.to_dict("records")}