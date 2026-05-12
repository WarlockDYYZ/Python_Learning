def knapsack_02(capacity, weights, values):
    n = len(weights)
    # 一维 DP 数组，dp[j] 表示容量为 j 时的最大价值
    dp = [0] * (capacity + 1)

    for i in range(n):
        w = weights[i]
        v = values[i]
        # ⚠️ 核心：必须逆序遍历！防止当前物品被重复使用
        for j in range(capacity, w - 1, -1):
            dp[j] = max(dp[j], dp[j - w] + v)

    return dp[capacity]

V = 4
weights = [3, 4, 1]
values = [20, 30, 15]

print(f"优化后背包能装下的最大价值为: {knapsack_02(V, weights, values)}")