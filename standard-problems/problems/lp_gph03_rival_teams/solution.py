# Python reference for lp_gph03_rival_teams (must pass under the judge's x4 time).
# Independent of solution.cpp: one pass of union-find with parity. parity[x]
# is x's team relative to its parent; a rivalry inside one set whose ends have
# the same parity closes an odd cycle -- that is the answer.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, m = int(data[0]), int(data[1])
    parent = list(range(n + 1))
    parity = [0] * (n + 1)

    def find(x: int) -> tuple[int, int]:
        path = []
        while parent[x] != x:
            path.append(x)
            x = parent[x]
        root = x
        # compress: walk back from the node nearest the root
        acc = 0
        for y in reversed(path):
            acc ^= parity[y]
            parity[y] = acc
            parent[y] = root
        return root, (parity[path[0]] if path else 0)

    for i in range(m):
        u, v = int(data[2 + 2 * i]), int(data[3 + 2 * i])
        ru, pu = find(u)
        rv, pv = find(v)
        if ru == rv:
            if pu == pv:
                print(i + 1)
                return
        else:
            parent[ru] = rv
            parity[ru] = pu ^ pv ^ 1
    print(-1)


main()
