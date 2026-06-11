from pydantic import BaseModel, ValidationError


class User(BaseModel):
    name: str
    age: int
    email: str | None = None  # 可选字段，默认为 None


# 1. 自动类型转换：字符串 "20" 会被自动转为整数 20
user = User(name="张三", age="20", email="xxx@qq.com")

# 2. 自动校验：如果传入错误类型，会抛出 ValidationError
try:
    User(name="李四", age="abc")
except ValidationError as e:
    print(e)