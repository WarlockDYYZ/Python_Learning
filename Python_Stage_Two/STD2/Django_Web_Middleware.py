class Middleware:
    def __init__(self, get_response):
        # 把下一层，绑定到当前中间件实例身上存着
        # 后面 __call__ 里要用
        self.get_response = get_response

    def __call__(self, request):
        print("基础中间件预处理")
        response = self.get_response(request)
        print("基础中间件后处理")
        return response


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("认证预处理")
        response = self.get_response(request)
        print("认证后处理")
        return response


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("日志预处理")
        response = self.get_response(request)
        print("日志后处理")
        return response


def view(request):
    print("视图处理")
    return "ok"


# 正确链：互相包装，不继承
chain = AuthMiddleware(
           LogMiddleware(
               Middleware(view)
           )
         )

chain("request")