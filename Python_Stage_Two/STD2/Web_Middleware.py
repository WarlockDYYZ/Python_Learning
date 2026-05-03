class Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 预处理请求
        print("中间件预处理请求")
        response = self.get_response(request)
        # 后处理响应
        print("中间件后处理响应")
        return response


class AuthenticationMiddleware(Middleware):
    def __call__(self, request):
        print("认证中间件：验证用户身份")
        return super().__call__(request)


class LoggingMiddleware(Middleware):
    def __call__(self, request):
        print("日志中间件：记录请求信息")
        return super().__call__(request)


# 中间件链
def get_response(request):
    print("视图函数处理请求")
    return "响应内容"


# 构建中间件链
middleware_chain = AuthenticationMiddleware(
    LoggingMiddleware(
        Middleware(get_response)
    )
)
# 调用中间件链
middleware_chain("请求对象")
