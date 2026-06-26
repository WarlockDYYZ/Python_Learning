# app/core/security.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.db import AsyncSessionLocal

# 子依赖：提取请求头中的Bearer Token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",  # 登录接口地址，用于获取Token
    scheme_name="JWT",
    auto_error=True
)

# 子依赖：解析并校验Token，获取用户信息
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="身份校验失败：无效的用户凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 解码JWT令牌，获取用户ID
        payload = jwt.decode(token, "SECRET_KEY", algorithms=["HS256"])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # 复用数据库会话，查询用户详情
    db = AsyncSessionLocal()
    user = await db.execute(select(User).where(User.id == user_id))
    user = user.scalar_one_or_none()
    await db.close()

    if user is None:
        raise credentials_exception
    return user

# 父依赖：校验用户管理员权限
async def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足：该接口仅允许管理员用户访问"
        )
    return current_user