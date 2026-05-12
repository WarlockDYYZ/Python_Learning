def knapsack_01(capacity, weights, values):
    # n 物品个数
    n = len(weights)
    # 因为根据状态转移方程，在处理第一个物品时，若物品容量大于当前体积，要赋值为上一个值dp[i - 1][j]
    # 所以多一行，保存第一次选取之前的情况
    # 多一列是状态转移方程的要求，而且会在阅读上使代码更清晰
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w = weights[i - 1]
        v = values[i - 1]

        for j in range(1, capacity + 1):
            if j < w:
                dp[i][j] = dp[i - 1][j]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - w] + v)

    print(dp[n][capacity])

V = 4
weights = [3, 4, 1]
values = [20, 30, 15]

knapsack_01(V, weights, values)
