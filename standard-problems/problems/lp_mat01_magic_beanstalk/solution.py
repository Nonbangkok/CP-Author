# Python reference for lp_mat01_magic_beanstalk (independent of solution.cpp):
# raise the 3x3 step matrix by squaring, but apply it to the state vector
# (f_n, f_{n-1}, 1) from the right-most bit -- valid because powers of one
# matrix commute.
import sys

MOD = 10**9 + 7


def mat_mul(x, y):
    return [[sum(x[i][k] * y[k][j] for k in range(3)) % MOD for j in range(3)] for i in range(3)]


def main() -> None:
    a, b, c, f0, f1, n = map(int, sys.stdin.buffer.read().split()[:6])
    if n == 0:
        print(f0 % MOD)
        return
    m = [[a % MOD, b % MOD, c % MOD], [1, 0, 0], [0, 0, 1]]
    v = [f1 % MOD, f0 % MOD, 1]
    e = n - 1
    while e:
        if e & 1:
            v = [sum(m[i][k] * v[k] for k in range(3)) % MOD for i in range(3)]
        m = mat_mul(m, m)
        e >>= 1
    print(v[0])


main()
