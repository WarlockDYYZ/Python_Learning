import requests

# get + headers(请求头)
# url = "http://127.0.0.1:5000/get/user/token"
# headers = {
#     "Token": "abc123",
#     "Version": "2.0.0"
# }
#
# response = requests.get(url, headers=headers)
# print(response.json())

# post data
# url = "http://127.0.0.1:5000/post/user/form"
# # 将数据放到 data 参数中
# form_data = {
#     "username": "张三",
#     "age": 25,
#     "email": "zhangsan@example.com"
# }
#
# response = requests.post(url, data=form_data)
# print(response.json())

# post json
# url = "http://127.0.0.1:5000/post/user/json"
# # 将数据放到 data 参数中
# json_data = {
#     "username": "李四",
#     "age": 25,
#     "email": "lisi@example.com"
# }
# # response = requests.post(url, data=json_data)  # 传入非 json 格式数据，返回 400
# response = requests.post(url, json=json_data)
# print(response.json())

# 上传文件
# url = "http://127.0.0.1:5000/post/file/upload"
# # 使用 with 语句自动管理文件资源，避免内存泄漏
# with open('Cyber Notebook.txt', 'rb') as f:
#     # 构造 files 字典，键 'file' 必须与后端 <input name="file"> 一致
#     files = {'file': f}
#     # 可同时上传文件和其他表单参数（如描述信息），可以结合 data 参数一起使用，data 怎么传上面有
#     response = requests.post(url, files=files)
#
# print(response.json())

# 手动校验
# url = "http://127.0.0.1:5000/post/user/validate"
# # 将数据放到 data 参数中
# json_data = {
#     "username": "wangwu",
#     "password": "123456",
#     "email": "wangwu@example.com"
# }
# # response = requests.post(url, data=json_data)  # 传入非 json 格式数据，返回 400
# response = requests.post(url, json=json_data)
# print(response.json())

# marshmallow 校验
# url = "http://127.0.0.1:5000/post/user/schema"
# # 将数据放到 data 参数中
# json_data = {
#     "username": "赵六",
#     "password": "asdfgh",
#     "email": "zhaoliu@example.com",
#     "age": 25
# }
# # response = requests.post(url, data=json_data)  # 传入非 json 格式数据，返回 400
# response = requests.post(url, json=json_data)
# print(response.json())

# 手动抛出异常
url = "http://127.0.0.1:5000/get/user/abort/10000"

response = requests.get(url)
print(response.json())
