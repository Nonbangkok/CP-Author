# Python reference for lp_mono03_stable_stretch (must pass under the judge's x4 time).
# Same idea as solution.cpp (two monotonic deques), written differently: the
# left end jumps straight past the index that has to leave, instead of moving
# one step at a time.
import sys
from collections import deque


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n, d = int(data[0]), int(data[1])
    a = list(map(int, data[2:2 + n]))
    mx = deque()
    mn = deque()
    l = 0
    best, start = 0, 0
    for r in range(n):
        v = a[r]
        while mx and a[mx[-1]] <= v:
            mx.pop()
        mx.append(r)
        while mn and a[mn[-1]] >= v:
            mn.pop()
        mn.append(r)
        while a[mx[0]] - a[mn[0]] > d:
            # the older of the two fronts must leave; the window starts just after it
            if mx[0] < mn[0]:
                l = mx.popleft() + 1
            else:
                l = mn.popleft() + 1
        if r - l + 1 > best:
            best = r - l + 1
            start = l
    print(best, start + 1)


main()
