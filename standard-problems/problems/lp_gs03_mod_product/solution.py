# Python reference for lp_gs03_mod_product (must pass under the judge's x4 time).
import sys

MOD = 10**9 + 7


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    total, product = 0, 1
    for token in data[1:1 + n]:
        x = int(token) % MOD
        total = (total + x) % MOD
        product = product * x % MOD
    print(total)
    print(product)


main()
