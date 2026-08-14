from enum import Enum


class ErrorCode(Enum):
    # 通用/数据校验错误 (400)
    DATA_INVALID = (400, 40001, "数据格式非法")

    # 权限相关错误 (403)
    PERMISSION_DENIED = (403, 40301, "权限不足")

    # 系统/ETL任务错误 (500)
    ETL_TASK_FAILED = (500, 50001, "ETL任务执行失败")
    INTERNAL_SERVER_ERROR = (500, 50000, "服务器内部错误")

    def __init__(self, http_status: int, code: int, message: str):
        self.http_status = http_status  # HTTP 状态码
        self.code = code  # 业务错误码
        self.message = message  # 默认错误描述


class BusinessException(Exception):
    """业务异常基类"""
    def __init__(self, error_code: ErrorCode, detail: str = None):
        self.http_status = error_code.http_status
        self.code = error_code.code
        self.message = error_code.message
        self.detail = detail
        super().__init__(self.message)

class PermissionDeniedException(BusinessException):
    """权限不足异常"""
    def __init__(self, detail: str = None):
        super().__init__(ErrorCode.PERMISSION_DENIED, detail)

class DataInvalidException(BusinessException):
    """数据校验失败异常"""
    def __init__(self, detail: str = None):
        super().__init__(ErrorCode.DATA_INVALID, detail)

class ETLTaskException(BusinessException):
    """ETL任务执行异常"""
    def __init__(self, detail: str = None):
        super().__init__(ErrorCode.ETL_TASK_FAILED, detail)