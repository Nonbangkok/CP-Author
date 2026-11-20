# Python reference for lp_ss03_spin_tiles: one backwards BFS from the solved
# board over 9-character strings, then a dict lookup per query.
import sys
from operator import itemgetter

BLOCKS = [(0, 1, 4, 3), (1, 2, 5, 4), (3, 4, 7, 6), (4, 5, 8, 7)]


def undo_getter(block):
    """new[i] = old[src[i]] for one counter-clockwise turn of the block."""
    a, b, c, d = block
    src = list(range(9))
    src[a], src[b], src[c], src[d] = b, c, d, a
    return itemgetter(*src)


def main() -> None:
    data = sys.stdin.buffer.read().split()
    getters = [undo_getter(b) for b in BLOCKS]
    goal = "123456789"
    dist = {goal: 0}
    queue = [goal]
    head = 0
    join = "".join
    while head < len(queue):
        state = queue[head]
        head += 1
        d = dist[state] + 1
        for get in getters:
            nxt = join(get(state))
            if nxt not in dist:
                dist[nxt] = d
                queue.append(nxt)
    q = int(data[0])
    out = []
    for i in range(q):
        key = b"".join(data[1 + 9 * i: 10 + 9 * i]).decode()
        out.append(dist[key])
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
