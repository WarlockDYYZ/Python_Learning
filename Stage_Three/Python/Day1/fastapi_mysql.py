from fastapi import FastAPI, Depends, HTTPException
import aiomysql
from aiomysql import DictCursor
from contextlib import asynccontextmanager


# 数据库配置
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_USER = "root"        # 改为你的MySQL用户名
DB_PWD = "123456"       # 改为你的MySQL密码
DB_NAME = "test_db"
DB_CHARSET = "utf8mb4"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动：创建连接池
    try:
        print("🚀 正在创建数据库连接池...")
        app.state.pool = await aiomysql.create_pool(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PWD,
            db=DB_NAME,
            charset=DB_CHARSET,
            autocommit=True,
            maxsize=20,
            minsize=5,
            pool_recycle=3600
        )
        print("✅ 数据库连接池创建成功！")
    except Exception as e:
        print(f"❌ 数据库连接池创建失败: {e}")
        raise

    yield

    # 应用关闭：销毁连接池
    if hasattr(app.state, 'pool') and app.state.pool is not None:
        print("🛑 正在安全关闭数据库连接池...")
        app.state.pool.close()
        await app.state.pool.wait_closed()
        print("✅ 数据库连接池已彻底释放。")


app = FastAPI(lifespan=lifespan)


# ========== 重点修改：标准异步依赖项（替代原 get_db） ==========
async def get_db_cursor():
    """
    FastAPI 标准异步依赖：自动获取连接、游标，请求结束自动归还连接
    返回字典格式游标 DictCursor
    """
    pool = app.state.pool
    try:
        async with pool.acquire() as conn:
            async with conn.cursor(DictCursor) as cur:
                yield cur
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"数据库操作异常: {str(e)}")


# ========== 测试接口示例 ==========
@app.get("/list-income")
async def get_income_data(cur = Depends(get_db_cursor)):
    """查询 income_data 表数据"""
    await cur.execute("SELECT * FROM income_data;")
    data = await cur.fetchall()
    return {"code": 200, "data": data}


@app.get("/db-version")
async def get_mysql_version(cur = Depends(get_db_cursor)):
    """测试数据库连通性"""
    await cur.execute("SELECT VERSION() as version;")
    res = await cur.fetchone()
    return res


# 启动入口
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)