# Python reference for lp_stl05_nearest_van (must pass under the judge's x4 time).
# Python has no ordered multiset, so this one reads every command first,
# compresses the spots and keeps a count per spot in a Fenwick tree:
# predecessor / successor are "the k-th smallest" for the right k.
import sys
from bisect import bisect_right


def main() -> None:
    data = sys.stdin.buffer.read().split()
    q = int(data[0])
    types = data[1:1 + 2 * q:2]
    xs = list(map(int, data[2:2 + 2 * q:2]))
    spots = sorted({x for t, x in zip(types, xs) if t != b"3"})
    index = {p: i + 1 for i, p in enumerate(spots)}
    m = len(spots)
    tree = [0] * (m + 1)
    top = 1
    while top * 2 <= m:
        top *= 2
    total = 0
    out = []

    def kth(k: int) -> int:  # 1-based position of the k-th smallest spot on the road
        pos, step = 0, top
        while step:
            nxt = pos + step
            if nxt <= m and tree[nxt] < k:
                pos = nxt
                k -= tree[nxt]
            step >>= 1
        return pos + 1

    for t, x in zip(types, xs):
        if t == b"1" or t == b"2":
            delta = 1 if t == b"1" else -1
            total += delta
            i = index[x]
            while i <= m:
                tree[i] += delta
                i += i & -i
        elif total == 0:
            out.append(-1)
        else:
            i = bisect_right(spots, x)  # spots[0:i] are <= x
            c = 0
            while i:
                c += tree[i]
                i -= i & -i
            best = -1
            if c < total:
                best = spots[kth(c + 1) - 1]  # smallest spot > x
            if c > 0:
                below = spots[kth(c) - 1]  # largest spot <= x
                if best == -1 or x - below <= best - x:
                    best = below
            out.append(best)
    sys.stdout.write("".join(f"{v}\n" for v in out))


main()
