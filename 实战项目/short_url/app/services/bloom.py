import mmh3


class BloomFilter:
    """简易布隆过滤器实现"""
    def __init__(self, bit_size: int = 1 << 24, hash_count: int = 5):
        """
                :param bit_size: 位数组大小
                :param hash_count: 哈希函数个数
        """
        self.bit_size = bit_size
        self.hash_count = hash_count
        self.bit_array = bytearray(bit_size // 8 + 1)

    def _get_positions(self, item: str) -> list[int]:
        """使用 MurmurHash3 计算多个位位置"""
        positions = []
        for i in range(self.hash_count):
            # 使用不同的 seed 模拟多个哈希函数
            hash_val = mmh3.hash(item, seed=i, signed=False)
            positions.append(hash_val % self.bit_size)
        return positions

    def add(self, item: str):
        """将元素加入布隆过滤器"""
        for pos in self._get_positions(item):
            byte_idx = pos // 8
            bit_idx = pos % 8
            self.bit_array[byte_idx] |= (1 << bit_idx)

    def might_contain(self, item: str) -> bool:
        """
        判断元素是否可能存在
        返回 False 一定不存在，返回 True 可能存在
        """
        for pos in self._get_positions(item):
            byte_idx = pos // 8
            bit_idx = pos % 8
            if not (self.bit_array[byte_idx] & (1 << bit_idx)):
                return False
        return True