
# Fractional Knapsack using Greedy Method

def fractional_knapsack(capacity, items):
    # Sort items by profit/weight ratio in descending order
    items.sort(key=lambda x: x[1] / x[0], reverse=True)

    total_profit = 0

    print("\nSelected Items:")

    for weight, profit in items:
        if capacity == 0:
            break

        if weight <= capacity:
            # Take the complete item
            capacity -= weight
            total_profit += profit
            print("Weight:", weight, "Profit:", profit)

        else:
            # Take the fractional part
            fraction = capacity / weight
            total_profit += profit * fraction

            print("Weight Taken:", capacity)
            print("Fraction:", round(fraction, 2))
            print("Profit:", round(profit * fraction, 2))

            capacity = 0

    print("\nMaximum Profit:", round(total_profit, 2))


# Main Program
n = int(input("Enter number of items: "))

items = []

for i in range(n):
    weight = float(input("Enter weight of item: "))
    profit = float(input("Enter profit of item: "))
    items.append((weight, profit))

capacity = float(input("Enter knapsack capacity: "))

fractional_knapsack(capacity, items)
