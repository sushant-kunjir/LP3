
N = 8

board = [[0 for _ in range(N)] for _ in range(N)]

# Check whether placing a queen is safe
def is_safe(row, col):
    for i in range(row):
        # Check same column
        if board[i][col] == 1:
            return False

        # Check upper-left diagonal
        if col - (row - i) >= 0:
            if board[i][col - (row - i)] == 1:
                return False

        # Check upper-right diagonal
        if col + (row - i) < N:
            if board[i][col + (row - i)] == 1:
                return False

    return True


# Backtracking function
def solve(row):
    if row == N:
        return True

    for col in range(N):
        if is_safe(row, col):
            board[row][col] = 1

            if solve(row + 1):
                return True

            # Backtrack
            board[row][col] = 0

    return False


# Place the first queen at Row 1, Column 1
board[0][0] = 1

if solve(1):
    print("Final 8-Queens Matrix:")
    for row in board:
        print(row)
else:
    print("Solution does not exist")
