from random import choices, randint
from math import e


# Function to visualize the board
def print_board(queens):
    n = len(queens)
    for r in range(n):
        for c in range(n):
            if queens[c] == r:
                print('Q', end= ' ')
            else:
                print('*', end=' ')
        print()
    print()


# Calculate number of attacked queens by checking duplicates
def calc_score(queens, n):
    # a) row
    row_duplicates = 0
    found = set()
    for row in queens:
        if row in found:
            row_duplicates += 1
        else:
            found.add(row)

    # b) diagonals
    diag_duplicates = 0
    found = set()
    diag1 = [queens[col] + col for col in range(n)]
    for i in diag1:
        if i in found:
            diag_duplicates += 1
        else:
            found.add(i)
    found = set()
    diag2 = [queens[col] - col for col in range(n)]
    for i in diag2:
        if i in found:
            diag_duplicates += 1
        else:
            found.add(i)

    return row_duplicates + diag_duplicates

# Returns the list of queen coordinates, None if fails after a max number of iterations (worst case)
def solve_queens(n):
    # Generate random row numbers for each queen in each column
    queens = [randint(0, n-1) for _ in range(n)]

    # Calculate initial score
    min_score = calc_score(queens, n)

    # Initialize constants
    TEMP = 1000
    MAX_ITERS = 10000  # To escape infinite loop if stuck in local optima

    # Loop counters
    i = 0  # Counter for total number of iterations
    iters = 0  # Incremented if no updates to min_score, reset to 0 otherwise

    while min_score > 0:
        # Return None if exceeded MAX_ITERS
        if iters > MAX_ITERS:
            return None

        # Pick random queen from a column
        rand_col = randint(0, n-1)
        # queens_cpy = queens.copy()
        row_cpy = queens[rand_col]

        # Move queen randomly up or down by a random value (move to random row)
        rand_position = randint(0, n-1)
        while (rand_position == queens[rand_col]):
            rand_position = randint(0, n-1)
        queens[rand_col] = rand_position

        score = calc_score(queens, n)

        # Accept move if score < min_score
        if score < min_score:
            min_score = score
            iters = 0
        else:
            # Accept move with some probability dependent on time and difference between scores
            diff = score - min_score
            t = TEMP / float(i + 1)
            p = e ** (-1 * diff / t)

            if choices([True, False], weights=(p, 1-p))[0]:
                min_score = score
                iters = 0
            else:
                # Revert move
                queens[rand_col] = row_cpy
                iters += 1
        i += 1

    return queens


import time
import matplotlib.pyplot as plt

# Running time for solve_queens (averaged over 10 runs from n = 4 to 50)
time_list = []
AVG = 1
for k in range(AVG):
    for i in range(4, 51):
        start_time = time.time()
        solve_queens(i)
        end_time = time.time() - start_time
        if len(time_list) <= i - 4:
            time_list.append(end_time)
        else:
            time_list[i-4] += end_time

time_list = list(map(lambda x: x / AVG, time_list))
x = [i for i in range(4, 51)]

plt.xlabel("N")
plt.ylabel("Running time of solve_queens (seconds)")
plt.plot(x, time_list)
plt.show()


# Running time for calc_score
# time_list = []
# x = [i for i in range(4, 10000)]
# for i in range(4, 10000):
#     queens = [j for j in range(i)]
#     start_time = time.time()
#     calc_score(queens, i)
#     end_time = time.time() - start_time
#     time_list.append(end_time)

# plt.xlabel("N")
# plt.ylabel("Running time of calc_score (seconds)")
# plt.plot(x, time_list)
# plt.show()


# Failure rate (0% so far)
# fail_count = 0
# for i in range(10):
#     for i in range(4, 51):
#         res = solve_queens(i)
#         if res is None:
#             fail_count += 1

# print('number of fails =', fail_count)
# print('total runs =', 460)
# print('failure rate =', fail_count*100/460)

# print(solve_queens(50))