
# 0/1 Knapsack using Dynamic Programming

def knapsack(W, wt, profit, n):

    # Create DP table
    dp = [[0 for x in range(W + 1)]
          for x in range(n + 1)]

    # Build the DP table
    for i in range(1, n + 1):
        for w in range(1, W + 1):

            if wt[i - 1] <= w:
                dp[i][w] = max(
                    profit[i - 1] + dp[i - 1][w - wt[i - 1]],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][W]


# Main Program
n = int(input("Enter number of items: "))

wt = []
profit = []

for i in range(n):
    w = int(input("Enter weight of item: "))
    p = int(input("Enter profit of item: "))

    wt.append(w)
    profit.append(p)

W = int(input("Enter knapsack capacity: "))

result = knapsack(W, wt, profit, n)

print("\nMaximum Profit:", result)
