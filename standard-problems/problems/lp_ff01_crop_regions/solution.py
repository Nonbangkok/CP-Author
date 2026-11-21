# Python reference for lp_ff01_crop_regions (must pass under the judge's x4 time).
# The grid is padded with a border of '#' (never a crop) and flattened, so the
# four neighbours of cell i are i-1, i+1, i-W, i+W with no bounds checks.
import sys


def main() -> None:
    data = sys.stdin.buffer.read().split()
    r, c = int(data[0]), int(data[1])
    w = c + 2
    g = bytearray(b"#" * (w * (r + 2)))
    for i in range(r):
        start = (i + 1) * w + 1
        g[start:start + c] = data[2 + i]
    seen = bytearray(len(g))
    regions = 0
    largest = 0
    for i in range(r):
        base = (i + 1) * w + 1
        for s in range(base, base + c):
            if seen[s]:
                continue
            regions += 1
            crop = g[s]
            seen[s] = 1
            queue = [s]
            for cur in queue:
                for nxt in (cur - 1, cur + 1, cur - w, cur + w):
                    if g[nxt] == crop and not seen[nxt]:
                        seen[nxt] = 1
                        queue.append(nxt)
            if len(queue) > largest:
                largest = len(queue)
    print(regions, largest)


main()
