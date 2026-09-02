import hashlib
from app.config import settings


ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(ALPHABET)

def encode_base62(num: int) -> str:
    """将十进制数转换为 Base62 字符串"""
    if num == 0:
        return ALPHABET[0]
    result = []

    while num > 0:
        num, remainder = divmod(num, BASE)
        result.append(ALPHABET[remainder])

    return "".join(reversed(result))

def decode_base62(s: str) -> int:
    """将 Base62 字符串转换为十进制数"""
    char_to_index = {c: i for i, c in enumerate(ALPHABET)}
    num = 0
    
    for char in s:
        num = num * BASE + char_to_index[char]

    return num

def generate_short_code(url: str, salt: str = "") -> str:
    """
    方案二：MD5 哈希截断生成短码
    注意：此方案存在碰撞风险，需数据库唯一约束兜底
    """
    raw = f"{url}{salt or settings.SECRET_KEY}"
    md5_hash = hashlib.md5(raw.encode("utf-8")).hexdigest()
    # 取前 8 位十六进制，转为十进制后 Base62 编码
    num = int(md5_hash[:8], 16)

    return encode_base62(num)