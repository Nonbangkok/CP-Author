# Curriculum plan

Owner's topic list and writing decisions (2026-11-20). Status: all three
batches written and verified (2026-11-20); waiting for the owner's review and
the production import (steps at the end of this file).

## Decisions

| Question | Decision |
|---|---|
| Practice problems | **New problems in this grader** for every lesson, 2–4 each, authored in CP-Author (statement, generator, reference solution, testcases) — no external judges. |
| Depth | **Standard, 12–20 minutes**: idea → worked example → complexity → common pitfalls → hints. Same shape as the *Data Structures (CP::)* lessons. |
| Code | **Full C++ templates** (tested reference implementations); problem-specific answers stay in `:::hint`. |
| Tracks | **By level**: Foundations → Intermediate → Advanced. *Data Structures (CP::)* stays as its own track beside them. |
| Voice | Thai, friendly and casual; UI and identifiers in English (see README.md). |

## Tracks

`P` = planned new problems (ids to be assigned when written). Problems are
standard (stdin/stdout) problems, C++ and Python allowed.

### 1. Foundations (`foundations`)

| Module | Lesson | Topic from the list | P |
|---|---|---|---|
| Getting started | C++ for Competitive Programming | programming | 3 |
| Getting started | Time & Space Complexity | time & space complexity, Big O | 2 |
| STL | Containers & Sorting (vector, pair, sort) | stl | 3 |
| STL | set, map, priority_queue, deque | stl | 3 |
| Recursion | Thinking Recursively | recursive | 3 |
| Binary search | Binary Search on an Array | bsearch on array | 3 |
| Binary search | Binary Search on the Answer | bsearch on answer | 3 |
| Techniques | Two Pointers | two pointer | 3 |
| Techniques | Sliding Window | sliding window | 3 |
| Math tools | Binary Exponentiation | binary expo | 2 |
| Math tools | Bitmasks | bitmasks | 3 |

### 2. Intermediate (`intermediate`)

| Module | Lesson | Topic from the list | P |
|---|---|---|---|
| Greedy | Greedy Choices and Exchange Arguments | greedy | 3 |
| Divide & conquer | Divide and Conquer | devide & conquer | 3 |
| Search | State Space Search (backtracking, BFS over states) | state space search | 3 |
| Dynamic programming | DP Basics (1D states) | dp | 3 |
| Dynamic programming | DP on Grids & Knapsack | dp | 3 |
| Graphs | Graphs, BFS and DFS | graph + graph algo | 3 |
| Graphs | Flood Fill on Grids | flood fill | 3 |
| Graphs | Shortest Paths (Dijkstra, Bellman–Ford, Floyd–Warshall) | graph algo | 3 |
| Trees | Tree Basics (DFS, depth, subtree size, diameter) | tree + tree algo | 3 |
| Trees | Lowest Common Ancestor (binary lifting) | tree algo | 2 |
| Stack & queue tricks | Monotonic Stack & Monotonic Queue | monotonic queue & stack | 3 |
| Sweeping | Sweep Line | sweep line | 3 |
| Strings | String Algorithms (hashing, KMP, Z) | string algorithms | 3 |

### 3. Advanced (`advanced`)

| Module | Lesson | Topic from the list | P |
|---|---|---|---|
| MST | Minimum Spanning Tree (Kruskal + DSU, Prim) | mst + mst algo | 3 |
| Range queries | Fenwick Tree | fenwick tree | 3 |
| Range queries | Segment Tree | segment tree | 3 |
| Range queries | Segment Tree with Lazy Propagation | segment tree | 2 |
| Math tools | Matrix Exponentiation | matrix expo | 2 |

Total: 29 lessons, about 82 new problems.

## Order of work

1. **Standard-problem harness** — done: `standard-problems/` next to
   `header-problems/` (pilot `lp_bsa01_count_range` for *Binary Search on an
   Array* builds, verifies and imports into the OJ): same Docker image, statement template and verify
   contract (reference AC on all cases, `slow` TLE where a complexity is
   promised), but stdin/stdout problems and an import ZIP for the OJ's batch
   upload. Lessons cannot ship before their problems exist in the grader.
2. **Batch 1 — Foundations** (11 lessons, ~31 problems), imported and reviewed
   by the owner. **Written (2026-11-20):** 11 lessons in `lessons/foundations/`,
   31 problems `lp_*` (all verified in one serial run; slow.cpp margins 3.1x–>30x),
   problems ZIP + lessons bundle accepted by the OJ importers on a scratch
   database. Waiting for the owner's review and the production import.
3. **Batch 2 — Intermediate** (13 lessons, ~38 problems). **Written (2026-11-20):** 13 lessons in
   `lessons/intermediate/` (Shortest Paths became its own module next to Graphs), 38 problems
   `lp_*` (gr, dc, ss, str, dp, dpk, gph, ff, sp, tr, lca, mono, swp). All 69 problems verified in
   one serial run (references <= 31% of the limit, slow.cpp >= 3.1x over it); the 69-problem ZIP
   (239 MiB uncompressed) and the 31-lesson bundle import cleanly with the OJ's importers.
   Reading times calibrated to ~1,125 bytes per minute (18–28 min).
4. **Batch 3 — Advanced** (5 lessons, ~13 problems). **Written (2026-11-20):** 5 lessons in
   `lessons/advanced/` (MST, Fenwick Tree, Segment Tree, Lazy Propagation, Matrix Exponentiation),
   13 problems `lp_*` (mst, fw, seg, lazy, mat). All 82 problems verified in one serial run
   (Batch 3 references <= 7% of the limit, Python <= 14% of its x4 limit, slow.cpp >= 3.0x over
   it); the 82-problem ZIP (302 MiB uncompressed, 1,804 entries) and the 36-lesson bundle import cleanly with the OJ's importers.
   Fenwick and segment trees are sized at N, Q <= 5*10^4 so Python passes with room to spare.

Each batch: problems built and verified → imported into the grader (hidden,
then published) → lessons bundle dry-run → owner review → import.

**End-to-end check (2026-11-20).** The 82-problem ZIP and the 36-lesson bundle
went through the OJ's own importers on a throwaway stack (Postgres 18 + backend
+ Vite, OJ branch `feat/lessons-phase2`): batch upload, Manage › Lessons dry run
(+36, no issues) and import, bulk publish, then every lesson opened in the
browser — KaTeX without errors, code tabs, problem cards and practice tables,
no horizontal overflow at 375 px — and the guest / learner / staff views of a
hidden problem, a contest problem and a hidden track. No content change was
needed.

## Production import (owner)

After OJ #58 and #59 are deployed and CP-Author #2 → #3 → #4 are merged, in a
checkout of `main`:

1. `cd standard-problems && ./run.sh build --all` → `dist/standard-problems.zip`
   (~124 MiB). Production Manage › Problems → Import ZIP. The 82 `lp_*`
   problems arrive hidden in the "Learn — …" collections.
2. Publish them: Hidden tab → select all → Show, until the tab reads 0.
3. `cd ../lessons && ./run.sh build` → `dist/lessons-bundle.zip`. Production
   Manage › Lessons → drop it; the dry run must show +36 added, 0 issues, four
   new tracks. Import. (Tracks are visible at once; Hide them on that page
   first if you want to read them as staff before learners do.)

