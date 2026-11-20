# Python reference for lp_ss01_three_buttons: BFS with a list as the queue.
import sys


def main() -> None:
    L, S, T = map(int, sys.stdin.buffer.read().split())
    dist = [-1] * (L + 1)
    dist[S] = 0
    queue = [S]
    head = 0
    while head < len(queue):
        x = queue[head]
        head += 1
        if x == T:
            break
        d = dist[x] + 1
        for y in (2 * x, x - 1, int(str(x)[::-1])):
            if 1 <= y <= L and dist[y] < 0:
                dist[y] = d
                queue.append(y)
    print(dist[T])


main()
