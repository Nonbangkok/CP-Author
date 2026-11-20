# Python reference for lp_rec01_subset_sum: build every subset sum (2^N of them)
# by doubling the list once per coin, then count the ones equal to S.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, s = int(data[0]), int(data[1])
    sums = [0]
    for x in map(int, data[2:2 + n]):
        sums += [t + x for t in sums]
    print(sums.count(s))


main()
