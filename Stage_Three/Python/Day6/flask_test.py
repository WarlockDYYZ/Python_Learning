import requests

# 目标URL
url = "http://127.0.0.1:5000/users"

# 要发送的JSON数据
data = {"username": "zhangsan"}

# 发送POST请求
response = requests.post(url, json=data)

# 打印返回的状态码和数据
print("状态码:", response.status_code)
print("返回数据:", response.json())
