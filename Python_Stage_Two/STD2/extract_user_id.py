from abc import ABC, abstractmethod


# 抽象类 + 抽象方法
# 抽象父类：数据提取器（统一接口规范）
class DataExtractor(ABC):
    @abstractmethod
    def extract_user_id(self):
        """抽取用户ID，子类必须实现"""
        pass


class JsonExtractor(DataExtractor):
    def __init__(self, json_data):
        self.json_data = json_data

    def extract_user_id(self):
        return self.json_data["user_id"]


class DatabaseExtractor(DataExtractor):
    def __init__(self, query_result):
        self.query_result = query_result

    def extract_user_id(self):
        return self.query_result["user_id"]


class CsvExtractor(DataExtractor):
    def __init__(self, csv_data):
        self.csv_data = csv_data

    def extract_user_id(self):
        return self.csv_data[0]["user_id"]


# 统一处理函数
def process_data(extractor: DataExtractor):
    return extractor.extract_user_id()


# 多态使用
json_data = {"user_id": 12345, "name": "Alice"}
db_result = {"user_id": 67890, "email": "bob@example.com"}
csv_data = [{"user_id": 54321, "age": 30}]
json_extractor = JsonExtractor(json_data)
db_extractor = DatabaseExtractor(db_result)
csv_extractor = CsvExtractor(csv_data)
print(process_data(json_extractor))  # 输出：12345
print(process_data(db_extractor))  # 输出：67890
print(process_data(csv_extractor))  # 输出：54321
