import pymysql
from dbutils.pooled_db import PooledDB


# 创建连接池（针对批量导入优化）
pool = PooledDB(
    creator=pymysql,
    maxconnections=20,
    mincached=5,
    maxcached=10,
    host='localhost',
    user='root',
    password='your_password',
    database='sales_db',
    charset='utf8mb4',
    # 增大包大小，支持批量数据
    options={'max_allowed_packet': 1024 * 1024 * 100}  # 100MB
)


def import_sales_data(csv_file):
    """批量导入销售数据"""
    conn = pool.connection()
    cursor = conn.cursor()

    try:
        # 1. 先删除索引（提高插入性能）
        cursor.execute("ALTER TABLE sales DROP INDEX idx_user_id")
        cursor.execute("ALTER TABLE sales DROP INDEX idx_product_id")
        cursor.execute("ALTER TABLE sales DROP INDEX idx_time")

        # 2. 使用LOAD DATA INFILE（最快方式）
        sql = """
           LOAD DATA INFILE %s
           INTO TABLE sales
           FIELDS TERMINATED BY ','
           ENCLOSED BY '"'
           LINES TERMINATED BY 'n'
           IGNORE 1 ROWS
           (order_id, user_id, product_id, amount, order_time)
       """
        cursor.execute(sql, (csv_file,))
        conn.commit()

        # 3. 重新创建索引
        cursor.execute("CREATE INDEX idx_user_id ON sales(user_id)")
        cursor.execute("CREATE INDEX idx_product_id ON sales(product_id)")
        cursor.execute("CREATE INDEX idx_time ON sales(order_time)")
        conn.commit()

        print("数据导入完成，共导入", cursor.rowcount, "条记录")

    except Exception as e:
        conn.rollback()
        print(f"数据导入失败: {e}")

    finally:
        cursor.close()
        conn.close()
# 使用示例
import_sales_data('sales_data.csv')


# 批量查询
def query_top_spenders():
    """查询消费金额最高的前100名用户"""
    conn = pool.connection()
    cursor = conn.cursor()

    try:
        # 执行查询（使用索引优化）
        sql = """
           SELECT
               u.user_id,
               u.name,
               SUM(s.amount) AS total_spent,
               COUNT(s.order_id) AS order_count
           FROM sales s
           JOIN users u ON s.user_id = u.user_id
           WHERE
               s.order_time BETWEEN '2023-01-01' AND '2023-06-30'
               AND s.amount > 1000
           GROUP BY s.user_id
           ORDER BY total_spent DESC
           LIMIT 100
       """

        # 使用EXPLAIN分析执行计划
        cursor.execute("EXPLAIN " + sql)
        explain_result = cursor.fetchall()
        print("执行计划分析:")
        for row in explain_result:
            print(row)

        # 执行实际查询
        cursor.execute(sql)
        results = cursor.fetchall()

        print(""
              "\n前100名高消费用户:")
        for i, (user_id, name, total_spent, order_count) in enumerate(results, 1):
            print(f"{i:3d}. 用户ID: {user_id:6d}, 姓名: {name:10s}, "
                  f"总消费: {total_spent:8.2f}, 订单数: {order_count:3d}")

    except Exception as e:
        print(f"查询失败: {e}")

    finally:
        cursor.close()
        conn.close()
# 执行查询
query_top_spenders()