from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr, ValidationError
import uvicorn


# 初始化FastAPI应用，配置标题、版本等信息
app = FastAPI(title="FastAPI接口Demo", version="1.0.0")


# GET 接口传参
from fastapi import Path, Query
# 查询参数：用Query()添加校验规则
@app.get("/get/user/list")
def get_user_list(
        page: int = Query(default=1, description="页码，从1开始", ge=1),
        size: int = Query(default=10, description="每页数量，1-100之间", ge=1, le=100),
        keyword: str = Query(default="", description="搜索关键词，最大长度50", max_length=50)
):
    return {
        "code": 200,
        "msg": "success",
        "data": {"page": page, "size": size, "keyword": keyword}
    }

# 路径参数：用Path()添加校验规则
@app.get("/get/user/{user_id}")
def get_user(
        user_id: int = Path(description="用户ID，必须大于0", gt=0, examples=[1001])
):
    return {"code": 200, "msg": "success", "data": {"user_id": user_id}}


# POST 接口传参
from fastapi import Form, File, UploadFile
from pydantic import BaseModel, EmailStr

# 1. 定义JSON请求体模型，继承BaseModel
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(description="用户名，2-20位字符串", min_length=2, max_length=20)
    password: str = Field(description="密码，6-16位字符串", min_length=6, max_length=16)
    email: EmailStr = Field(description="邮箱地址，自动校验格式")
    age: Optional[int] = Field(default=None, description="年龄，0-120之间", ge=0, le=120)

# 2. POST接口JSON传参：直接使用BaseModel子类作为参数
@app.post("/post/user/json")
def create_user(user: UserCreate):
    # user是UserCreate的实例，自动校验参数，转字典用 V2 定义的函数 .model_dump()
    return {
        "code": 200,
        "msg": "success",
        "data": user.model_dump()
    }

# 3. POST接口表单传参：用Form()接收参数
@app.post("/post/user/form")
def create_user_by_form(
        username: str = Form(description="用户名"),
        password: str = Form(description="密码"),
        email: EmailStr = Form(description="邮箱")
):
    return {
        "code": 200,
        "msg": "success",
        "data": {"username": username, "email": email}
    }

# 4. POST接口文件上传：用UploadFile接收文件
@app.post("/post/file/upload")
def upload_file(file: UploadFile = File(description="上传的文件对象")):
    # 读取文件内容，保存到本地
    content = file.file.read()
    with open(f"./uploads/{file.filename}", "wb") as f:
        f.write(content)
    return {
        "code": 200,
        "msg": "文件上传成功",
        "data": {"filename": file.filename}
    }


# 参数校验
# 路径参数校验
@app.get("/get/user2/{user_id}")
def get_user(
        user_id: int = Path(
            description="用户ID，必须大于0、小于10000",
            gt=0,
            lt=10000,
            examples=[1001]
        )
):
    return {"code": 200, "msg": "success", "data": {"user_id": user_id}}

# Header / Cookie 校验
from fastapi import Header, Cookie
@app.get("/get/user3/token")
def get_user_by_token(
        token: str = Header(description="用户登录Token，放在请求头中"),
        version: str = Header(default="1.0.0", description="接口版本号"),
        session_id: Optional[str] = Cookie(default=None, description="用户会话ID")
):
    return {
        "code": 200,
        "msg": "success",
        "data": {"token": token, "version": version, "session_id": session_id}
    }


# Header and Cookie
from fastapi import Header, Cookie
@app.get("/get/user4/token")
def get_user_by_token(
    token: str = Header(description="用户登录Token，放在请求头中"),
    version: str = Header(default="1.0.0", description="接口版本号"),
    session_id: Optional[str] = Cookie(default=None, description="用户会话ID")
):
    return {
        "code": 200,
        "msg": "success",
        "data": {"token": token, "version": version, "session_id": session_id}
    }


# 手动抛出异常
from fastapi import HTTPException, status
@app.get("/get/user5/{user_id}")
def get_user(user_id: int = Path(gt=0)):
    if user_id > 1000:
        # 手动抛出404异常，detail为错误描述
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return {"code": 200, "msg": "success", "data": {"user_id": user_id}}

# 自定义全局异常处理器
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
# 1. 处理参数校验异常
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": 400,
            "msg": "参数校验失败",
            "data": exc.errors()
        }
    )

# 2. 处理HTTP异常（如404、405）
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "msg": exc.detail,
            "data": {}
        }
    )

# 3. 处理服务器内部异常
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 500,
            "msg": "服务器内部异常",
            "data": str(exc)
        }
    )

# 统一入口：启动ASGI服务器
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)