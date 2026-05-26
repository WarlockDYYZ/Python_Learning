from contextlib import contextmanager
import sqlite3


@contextmanager
def get_db_transaction(db_path):
    """自定义数据库事务上下文管理器"""
    conn = None
    try:
        # 1. 建立连接（修路）
        conn = sqlite3.connect(db_path)
        print("数据库连接已建立")

        # 2. 开启事务并交出游标（发车）
        yield conn.cursor()

        # 3. 如果 with 块内没有报错，自动提交事务
        conn.commit()
        print("事务已提交")

    except Exception as e:
        # 4. 如果 with 块内报错，自动回滚事务
        if conn:
            conn.rollback()
            print(f"发生错误，事务已回滚: {e}")
        raise
    finally:
        # 5. 无论成功失败，最后一定关闭连接（拆路）
        if conn:
            conn.close()
            print("数据库连接已关闭")


def create_account_table(db_path):
    """创建 account 数据表"""
    # 连接到数据库（如果 bank.db 不存在会自动创建）
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # 编写创建表的 SQL 语句
        sql = '''
        CREATE TABLE IF NOT EXISTS account (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 用户ID，主键且自动递增(1, 2, 3...)
            balance REAL NOT NULL                       -- 账户余额，不能为空
        )
        '''

        # 执行 SQL 语句
        cursor.execute(sql)

        # 提交事务，保存更改
        conn.commit()
        print("表格 'account' 创建或检查完毕！")

    except Exception as e:
        print(f"创建表格失败: {e}")
        conn.rollback()  # 发生错误则回滚
    finally:
        # 关闭游标和数据库连接
        cursor.close()
        conn.close()


def show_all_tables(db_path):
    """查看 bank.db 中的所有用户表"""
    try:
        # 使用只读方式连接数据库，防止误操作修改数据
        conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)

        # 使用 with 语句自动管理游标的开启与关闭
        with conn:
            cursor = conn.cursor()
            # 从 sqlite_master 系统表中筛选出类型为 'table' 的记录
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = cursor.fetchall()

            print(f"\n数据库 '{db_path}' 中包含以下表格：")
            if tables:
                for table in tables:
                    print(f"- {table[0]}")
            else:
                print("(该数据库中没有找到任何用户表)")

    except Exception as e:
        print(f"查看表格失败: {e}")
    finally:
        # 无论成功或发生异常，最后一定关闭数据库连接
        if conn:
            conn.close()


def show_account_data(db_path):
    """查看 account 表里的所有数据内容"""
    try:
        # 依然建议使用只读模式连接，保证数据安全
        conn = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)
        # mode = ro： "Read-Only"（只读）这次连接打开文件后，只能读取数据，绝对不允许进行任何写入、修改或删除操作
        # uri=True：这是一个开关。传入的第一个参数不仅仅是一个普通的文件名，而是一个标准的 URI（统一资源标识符）。
        # 只有打开了这个开关，SQLite 才会去解析问号后面的 mode=ro 等高级参数。
        cursor = conn.cursor()

        # 使用 SELECT * 查询表中所有的行和列
        cursor.execute("SELECT * FROM account;")
        rows = cursor.fetchall()  # fetchall() 会提取出查询到的所有数据

        print(f"\n表格 'account' 中的数据内容如下：")
        if rows:
            # 获取表的列名（方便打印表头）
            column_names = [description[0] for description in cursor.description]
            print(f"{' | '.join(column_names)}")
            print("-" * 50)

            # 遍历并打印每一行的数据
            for row in rows:
                # 将元组中的每个元素转为字符串并用空格隔开
                print(" | ".join(str(item) for item in row))
        else:
            print("(account 表中目前没有任何数据)")

    except Exception as e:
        print(f"查看数据失败: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    db_file = 'bank.db'

    # 第一步：确保 account 表存在
    create_account_table(db_file)

    # 第二步：为了演示转账，如果表里没有数据，先插入两条初始账户数据（各给1000元）
    init_conn = sqlite3.connect(db_file)
    init_cursor = init_conn.cursor()
    init_cursor.execute("SELECT COUNT(*) FROM account")
    if init_cursor.fetchone()[0] == 0:
        # 插入 user_id 为 1 和 2 的初始账户
        init_cursor.execute("INSERT INTO account (balance) VALUES (1000), (1000)")
        init_conn.commit()
        print("已为 user_id 1 和 2 初始化初始余额 1000\n")
    init_cursor.close()
    init_conn.close()

    # 第三步：执行转账操作并查看结果
    try:
        with get_db_transaction(db_file) as cursor:
            # 扣款
            cursor.execute("UPDATE account SET balance = balance - 100 WHERE user_id = 1")
            # 加款
            cursor.execute("UPDATE account SET balance = balance + 100 WHERE user_id = 2")
            # 退出缩进后，自动提交并断开连接
            print("\n--- 转账事务完成，开始查看数据库状态 ---")

            # 查看所有表
            show_all_tables(db_file)
            # 查看 account 表的具体数据
            show_account_data(db_file)
    except Exception as e:
        print(f"转账整体失败: {e}")