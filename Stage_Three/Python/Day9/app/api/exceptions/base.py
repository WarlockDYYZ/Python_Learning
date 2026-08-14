# app/exceptions/base.py
class BusinessException(Exception):
    """业务异常基类，所有自定义业务异常均继承该类"""
    def __init__(self, code: int, message: str, detail: str = None):
        self.code = code
        self.message = message
        self.detail = detail
        super().__init__(self.message)

class PermissionDeniedException(BusinessException):
    """权限不足异常"""
    def __init__(self, message: str = "权限不足", detail: str = None):
        super().__init__(code=403, message=message, detail=detail)

class DataInvalidException(BusinessException):
    """数据校验失败异常"""
    def __init__(self, message: str = "数据格式非法", detail: str = None):
        super().__init__(code=400, message=message, detail=detail)

class ETLTaskException(BusinessException):
    """ETL任务执行异常"""
    def __init__(self, message: str = "ETL任务执行失败", detail: str = None):
        super().__init__(code=500, message=message, detail=detail)