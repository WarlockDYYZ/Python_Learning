# 练习1 变量操作综合练习
# 1. 定义变量保存个人信息
name = "Lxf"
age = 27
height = 1.68 ** 2
weight = 65
# 2. 计算BMI（身体质量指数）
# BMI = 体重(kg) / 身高(m)²
bmi = weight / height
# 3. 输出个人信息和BMI
print("=" * 50)
print("个人信息与健康指标")
print("=" * 50)
print(f"姓名：{name}")
print(f"年龄：{age}岁")
print(f"身高：{height}厘米")
print(f"体重：{weight}公斤")
print(f"BMI：{bmi:.2f}")

# 4. 根据BMI判断健康状况
if bmi < 18.5:
    health_status = "体重过轻"
elif bmi < 24:
    health_status = "正常范围"
elif bmi < 28:
    health_status = "超重"
else:
    health_status = "肥胖"
print(f"健康状况：{health_status}")
print("=" * 50)

# 练习2 温度转换程序
# 设计一个温度转换程序，支持：
# 1. 华氏度转摄氏度：C = (F - 32) * 5/9
# 2. 摄氏度转华氏度：F = C * 9/5 + 32
# 获取用户选择
print("温度转换程序")
print("1. 华氏度转摄氏度")
print("2. 摄氏度转华氏度")
choice = int(input("请选择转换类型（1或2）:"))

if choice == 1:
    # 华氏度转摄氏度
    fahrenheit = float(input("请输入华氏温度:"))
    celsius = (fahrenheit - 32) * 5 / 9
    print(f"{fahrenheit}°F = {celsius:.2f}°C")
elif choice == 2:
    # 摄氏度转华氏度
    celsius = float(input("请输入摄氏温度:"))
    fahrenheit = celsius * 9 / 5 + 32
    print(f"{celsius}°C = {fahrenheit:.2f}°F")
else:
    print("错误：请选择1或2")

# 练习3 模拟超市购物结算：
# 1. 输入商品价格和数量
# 2. 计算总价（价格 × 数量）
# 3. 若总价超过100元，打95折
# 4. 若总价超过200元，打9折
# 5. 输出结算信息

price = float(input("请输入商品单价（元）："))
quantity = int(input("请输入购买数量："))
# 计算总价
total = price * quantity

# 计算折扣
if total >= 200:
    discount = 0.9  # 9折
elif total >= 100:
    discount = 0.95  # 95折
else:
    discount = 1.0  # 无折扣

# 计算实付金额
actual_payment = total * discount

print("n购物结算单")
print("-" * 40)
print(f"商品单价：{price}元")
print(f"购买数量：{quantity}件")
print(f"商品总价：{total}元")
print(f"折扣：{discount:.0%}")
print(f"实付金额：{actual_payment:.2f}元")
print("-" * 40)
