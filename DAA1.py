
# Fibonacci Series with Step Count

n = int(input("Enter the number of terms: "))

a = 0
b = 1
steps = 0

print("Fibonacci Series:")

for i in range(n):
    print(a, end=" ")

    c = a + b
    a = b
    b = c

    steps += 1

print("\nStep Count:", steps)
