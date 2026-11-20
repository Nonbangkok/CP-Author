# Python reference for lp_tr02_longest_trail (must pass under the judge's x4
# time). Independent of the two-pass reference: a tree DP. down[v] = longest
# trail going down from v; the longest trail turns at some vertex and is the sum
# of its two longest "child + edge" branches. Children are handled before their
# parent by walking a BFS order backwards (no recursion).
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    adj = [[] for _ in range(n + 1)]
    pos = 1
    for _ in range(n - 1):
        u, v, w = int(data[pos]), int(data[pos + 1]), int(data[pos + 2])
        pos += 3
        adj[u].append((v, w))
        adj[v].append((u, w))
    parent = [0] * (n + 1)
    up_w = [0] * (n + 1)
    parent[1] = -1
    order = [1]
    for u in order:
        pu = parent[u]
        for v, w in adj[u]:
            if v != pu:
                parent[v] = u
                up_w[v] = w
                order.append(v)
    best1 = [0] * (n + 1)  # longest branch down from v
    best2 = [0] * (n + 1)  # second longest, from a different child
    answer = 0
    for i in range(n - 1, -1, -1):
        v = order[i]
        b1 = best1[v]
        if b1 + best2[v] > answer:
            answer = b1 + best2[v]
        p = parent[v]
        if p > 0:
            cand = b1 + up_w[v]
            if cand > best1[p]:
                best2[p] = best1[p]
                best1[p] = cand
            elif cand > best2[p]:
                best2[p] = cand
    print(answer)


main()
