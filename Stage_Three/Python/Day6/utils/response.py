from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any, Optional


def success_response(
        code: int = 200,
        message: str = "操作成功",
        data: Optional[Any] = None,
        http_status: int = 200  # 新增 HTTP 状态码参数
) -> JSONResponse:
    """
    通用成功响应工具，返回固定格式的JSON响应
    :param code: 业务状态码，默认200
    :param message: 业务操作提示信息
    :param data: 响应业务数据，支持Pydantic模型、ORM对象、字典、列表等
    :param http_status: 真实的HTTP状态码，默认200（用于与业务状态码解耦）
    :return: 标准化JSON响应
    """
    response_content = {
        "code": code,
        "message": message,
        "data": data if data is not None else {}
    }
    # jsonable_encoder自动序列化Pydantic、SQLAlchemy ORM等对象为JSON兼容格式
    serialized_content = jsonable_encoder(response_content)

    return JSONResponse(content=serialized_content, status_code=http_status)


def fail_response(
        code: int = 400,
        message: str = "操作失败",
        data: Optional[Any] = None
) -> JSONResponse:
    """
    通用失败响应工具，格式与成功响应完全一致
    :param code: 错误业务状态码，默认400
    :param message: 错误提示信息
    :param data: 错误附加数据（如参数校验错误详情）
    :return: 标准化JSON响应
    """
    response_content = {
        "code": code,
        "message": message,
        "data": data if data is not None else {}
    }
    serialized_content = jsonable_encoder(response_content)

    return JSONResponse(content=serialized_content, status_code=code)