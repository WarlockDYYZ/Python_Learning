import redis


r = redis.Redis(decode_responses=True)

# Lua脚本：原子扣减库存，返回1成功/0库存不足
lua_deduct_stock = """
local stock_key = KEYS[1]
local deduct_num = tonumber(ARGV[1])

-- 获取当前库存，如果键不存在返回nil
local current_stock = redis.call('GET', stock_key)
if not current_stock then
    return -1 -- 键不存在
end

current_stock = tonumber(current_stock)
if current_stock < deduct_num then
    return 0 -- 库存不足，无法扣减
end
-- 原子化扣减库存
redis.call('DECRBY', stock_key, deduct_num)
return 1 -- 扣减成功
"""

# 注册脚本，生成SHA哈希值，后续可以通过SHA值直接调用
stock_script = r.register_script(lua_deduct_stock)

# 执行脚本：扣减ID为1001的商品的3个库存
result = stock_script(keys=["product:1001:stock"], args=[3])
if result == 1:
    print("库存扣减成功")
elif result == 0:
    print("库存不足")
else:
    print("商品不存在")