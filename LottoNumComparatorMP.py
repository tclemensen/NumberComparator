# This program is intended to try to determine whether it is a higher chance of winning the lotto by using the
# same set of numbers for each draw, or if it is better to use a randomly generated set of numbers.
# By default, this will use all your CPU cores/threads to make the calculation as quick as possible.
# If you require something else you can change the number of threads in the code.

# Note: The code is set up to run 1000000 iterations per core/thread, which can take a while if you have
# a slow computer. The number of iterations can be changed in the code.

# Note: I have already run this code with 10 billion simulated games, the results were as follows:

# Total numbers of wins for random game: 924
# Total numbers of wins for static game: 1843

# This indicates that your chances of winning will be slightly higher (about twice) if you play with a
# static set of numbers vs choosing a random set for every game. However, the chances of winning Lotto are
# still incredibly low. This simulation won in about 0.00003% of the games played, clearly demonstrating how
# unlikely it is to win the jackpot, regardless of your strategy.

# Yes I am aware that I am mixing camelCase and the more pythonic snake_case.
# I learned to code with C# and camelCase, so it is a habit. Fix it yourself if this bothers you

# Feel free to use this code. It is provided "As Is", with no restrictions of any kind.
# Use at your own risk and responsibility.

import random
import multiprocessing
import numpy

# Static numbers - You can use these or put in your own set of 7 numbers.
staticNumbers = [4, 6, 12, 19, 22, 27, 31]

threads = (
    multiprocessing.cpu_count()
)  # Number of threads. This defaults to the number of cores/threads you have.
iterations = (
    threads * 1000000
)  # Number of iterations. This defaults to one million iterations per core/thread.

print("Running a total of ", iterations, " iterations")


# First Random Number Generator
def rndNums(size, min_value, max_value):
    array = []
    while len(array) < size:
        new_element = random.randint(min_value, max_value)
        if new_element not in array:
            array.append(new_element)
    array.sort()
    return array


# Second Random Number Generator. I thought it would be a good idea to get the random numbers from separate sources
# I don't know if it matters, but here it is.
def rndNums2(size, min_value, max_value):
    array = []
    array = numpy.sort(numpy.random.randint(min_value, max_value + 1, size))
    return array


# Checking to see if the arrays are identical
def areArraysIdentical(array1, array2):
    if len(array1) != len(array2):
        return False
    for i in range(len(array1)):
        if array1[i] != array2[i]:
            return False
    return True


# Function to generate and compare and count draws
def compare_lotto_numbers(seed, x_total, y_total, result_queue):
    x = 0
    y = 0

    for _ in range(seed):
        lottoNumbersDraw = rndNums(7, 1, 34)
        lottoNumbersPlay = rndNums2(7, 1, 34)

        rndResult = areArraysIdentical(lottoNumbersDraw, lottoNumbersPlay)
        if rndResult:
            x += 1
            print("Random Win With ", lottoNumbersDraw)

        staticResult = areArraysIdentical(lottoNumbersDraw, staticNumbers)
        if staticResult:
            y += 1
            print("Static Win With ", lottoNumbersDraw)

    result_queue.put((x, y))


if __name__ == "__main__":
    try:
        num_simulations = iterations
        num_processes = threads

        with multiprocessing.Manager() as manager:
            x_total = manager.Value("i", 0)
            y_total = manager.Value("i", 0)
            result_queue = manager.Queue()

            with multiprocessing.Pool(num_processes) as pool:
                seeds = [num_simulations // num_processes] * num_processes
                pool.starmap(
                    compare_lotto_numbers,
                    zip(
                        seeds,
                        [x_total] * num_processes,
                        [y_total] * num_processes,
                        [result_queue] * num_processes,
                    ),
                )

            while not result_queue.empty():
                x, y = result_queue.get()
                x_total.value += x
                y_total.value += y

            print("Total numbers of wins for random game:", x_total.value)
            print("Total numbers of wins for static game:", y_total.value)

    except KeyboardInterrupt:
        pass
