import sqlite3, logging
from contextlib import contextmanager
from app.config import DB_PATH

logger = logging.getLogger(__name__)


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 查询结果可按列名取值
    return conn


@contextmanager
def db_cursor(commit=False):
    conn = get_conn()
    try:
        cur = conn.cursor()
        yield cur
        conn.commit() if commit else None
    finally:
        conn.close()


def init_db():
    with db_cursor(commit=True) as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sales(
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                day     TEXT NOT NULL,
                channel TEXT NOT NULL,
                gmv     REAL NOT NULL,
                orders  INTEGER,
                UNIQUE(day, channel)
            )""")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_day ON sales(day)")
    logger.info("数据库初始化完成: %s", DB_PATH)


def fetch_source():
    """模拟从接口/爬虫获取一批原始数据。真实实现用 requests.get。"""
    import random, datetime as dt
    rng = random.Random(42)
    rows = []
    for i in range(30):
        day = (dt.date(2026, 9, 1) + dt.timedelta(days=i)).isoformat()
        for ch in ["抖音", "淘宝", "微信"]:
            rows.append((day, ch, round(rng.uniform(800, 2000), 2),
                         rng.randint(10, 120)))
    return rows


def save_records(rows):
    """幂等写入：重复 (day, channel) 自动覆盖，避免主键冲突报错。"""
    with db_cursor(commit=True) as cur:
        cur.executemany(
            "INSERT OR REPLACE INTO sales(day, channel, gmv, orders) VALUES(?,?,?,?)",
            rows)
    logger.info("写入/更新 %d 条记录", len(rows))
    return len(rows)