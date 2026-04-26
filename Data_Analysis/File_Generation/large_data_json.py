import json
import random

file_path = "../Data_File/large_data.json"
# 生成 30000 行数据（足够测试 chunksize=10000）
with open(file_path, "w", encoding="utf-8") as f:
    for i in range(30000):  # 3万行，分3块读取
        data = {
            "id": i + 1,
            "name": random.choice(["Alice", "Bob", "Charlie", "David", "Ella"]),
            "age": random.randint(18, 60),
            "city": random.choice(["Beijing", "Shanghai", "Guangzhou", "Shenzhen"]),
            "score": round(random.uniform(60, 100), 2)
        }
        # 每行一个JSON → 满足 lines=True
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

print("✅ large_data.json 生成完成！共 30000 行")