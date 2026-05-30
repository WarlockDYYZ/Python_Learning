from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import bcrypt
import pymysql
from dbutils.pooled_db import PooledDB
import time


app = FastAPI()

# 数据库连接池（针对认证优化）
pool = PooledDB(
    creator=pymysql,
    maxconnections=30,
    mincached=10,
    maxcached=15,
    blocking=True,
    host='localhost',
    user='root',
    password='your_password',
    database='auth_db',
    charset='utf8mb4'
)


class LoginRequest(BaseModel):
    username: str
    password: str


@app.post('/login')
async def login(req: LoginRequest):
    """用户登录接口"""
    conn = pool.connection()
    cursor = None
    try:
        # 1. 登录验证：只读事务，使用一致性快照（在MySQL中，普通SELECT默认就是一致性非锁定读取）
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        # 用户名唯一索引用于快速查询
        sql_select = "SELECT id, username, password_hash FROM users WHERE username = %s"
        cursor.execute(sql_select, (req.username,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="用户名或密码错误")

        # 2. 密码存储：使用加密算法（如 bcrypt），不存储明文。进行密码比对
        # bcrypt.checkpw 需要传入 bytes 类型
        if not bcrypt.checkpw(req.password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            raise HTTPException(status_code=401, detail="用户名或密码错误")

        # 提交只读事务（实际上对于纯SELECT，commit主要用于释放一致性快照的视图）
        conn.commit()

        # 3. 登录日志：独立事务，保证不影响登录验证
        # 开启一个新的事务来记录日志
        log_conn = pool.connection()
        log_cursor = None
        try:
            log_cursor = log_conn.cursor()
            # 假设登录日志表有 user_id + 时间范围索引
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
            sql_insert_log = "INSERT INTO login_logs (user_id, login_time) VALUES (%s, %s)"
            log_cursor.execute(sql_insert_log, (user['id'], current_time))
            log_conn.commit()  # 提交独立的登录日志事务
        except Exception as e:
            # 即使日志记录失败，也不应该影响用户的正常登录体验，因此这里只做异常捕获和回滚
            log_conn.rollback()
            print(f"登录日志记录失败: {e}")
        finally:
            if log_cursor:
                log_cursor.close()
            log_conn.close()

        return {"code": 0, "message": "登录成功", "user_id": user['id']}

    except HTTPException:
        # 重新抛出业务异常（如密码错误、用户不存在）
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        conn.close()