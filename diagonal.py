from random import randint


def solve(A, b, e=1e-4):
    n = len(b)
    x_pred = [0] * n
    x_cur = [0] * n

    while True:
        for i in range(n):
            x_cur[i] = (b[i]
                        - sum([A[i][j]*x_pred[j] for j in range(i)])
                        - sum([A[i][j]*x_pred[j] for j in range(i + 1, n)])) \
                / A[i][i]
        if sum([(x_cur[i] - x_pred[i]) ** 2 for i in range(n)]) <= e ** 2:
            return x_cur
        x_pred, x_cur = x_cur, x_pred


if __name__ == "__main__":
    n = 5
    A = [[randint(1, 10) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] = randint(50, 100)
    b = [randint(1, 100) for _ in range(n)]
    x = solve(A, b)
    print('x =', x)
    print('Ax =', [sum([A[i][j]*x[j] for j in range(n)]) for i in range(n)])
    print('b =', b)
