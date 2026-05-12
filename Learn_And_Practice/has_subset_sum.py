def has_subset_sum(nums, target=10000):
    # possible_sums 存储所有可能凑出的和
    possible_sums = {0}  # 初始状态：和为 0 总是可以凑出来的（什么都不选）

    for num in nums:
        # 这一步很关键：我们需要基于“上一轮”的结果来计算，所以不能直接修改正在遍历的集合
        # 我们复制一份当前的 possible_sums 用于本次迭代的新增计算
        new_sums = set()

        for current_sum in possible_sums:
            new_sum = current_sum + num

            if new_sum == target:
                return True  # 找到了！

            if new_sum < target:  # 优化：如果超过了目标值，就不需要存了（假设都是正数）
                new_sums.add(new_sum)

        # 将新产生的和加入到总集合中
        possible_sums.update(new_sums)

    return False


# 测试
nums_list = [2000, 3000, 4000, 5000]
# 2000 + 3000 + 5000 = 10000，应该返回 True
print(f"是否存在任意数量数字之和为 10000: {has_subset_sum(nums_list)}")