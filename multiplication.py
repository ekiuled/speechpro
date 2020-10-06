from concurrent.futures import ProcessPoolExecutor
import numpy
from random import randint
import itertools as it
from timeit import timeit


def sum_pair(a, b, i):
    """Summation wrapper."""

    return i, a + b


def mul(a, b, i):
    """Multiplication wrapper."""

    return i, a * b


def mul_sum_row(A, x, i):
    """Calculate element-wise multiplication concurrently.
    Add all values concurrently with divide & conquer scheme."""

    n = len(x)
    row = [None] * n
    with ProcessPoolExecutor() as executor:
        for j, r_j in executor.map(mul, A[i], x, range(n)):
            row[j] = r_j
    step = 1
    while step < n:
        with ProcessPoolExecutor() as executor:
            for j, r_j in executor.map(sum_pair, row[::step], row[step::step], range(0, n, step)):
                row[j] = r_j
        step *= 2

    return i, sum([A[i][j]*x[j] for j in range(len(x))])


def multiply(A, x):
    """Compute each dimension concurrently."""

    n = len(x)
    y = [None] * n
    with ProcessPoolExecutor() as executor:
        for i, y_i in executor.map(mul_sum_row, it.repeat(A), it.repeat(x), range(n)):
            y[i] = y_i
    return y


if __name__ == "__main__":
    n = 30
    A = [[randint(1, 100) for _ in range(n)] for _ in range(n)]
    x = [randint(1, 100) for _ in range(n)]
    print(multiply(A, x))
    print(numpy.dot(A, x))
    print(timeit('multiply(A, x)', setup='from __main__ import multiply, A, x', number=10) / 10)
    print(timeit('numpy.dot(A, x)', setup='from __main__ import numpy, A, x', number=10) / 10)
