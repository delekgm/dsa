def staircase(n, memo = None):
    if n == 0:
        return 1
    if n < 0:
        return 0

    if memo == None:
        memo = {}

    if n in memo:
        return memo[n]

    memo[n] = staircase(n - 1, memo) + staircase(n - 2, memo)
    return memo[n]

print(staircase(100))

def staircase_dp(n):
    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(1, n + 1):
        if i - 1 >= 0:
            dp[i] += dp[i - 1]
        if i - 2 >= 0:
            dp[i] += dp[i - 2]

    return dp[n]

print(staircase_dp(100))