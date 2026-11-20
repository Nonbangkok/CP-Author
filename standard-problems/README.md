# Standard problems — practice problems for the Learn lessons

Ordinary stdin/stdout problems (C++ and Python) behind the lessons planned in
[../lessons/CURRICULUM.md](../lessons/CURRICULUM.md). Each one is source here;
the harness turns it into a batch-upload ZIP for the OJ.

```bash
cd standard-problems
./run.sh build  --all                          # or: ./run.sh build lp_bsa01_count_range
./run.sh verify --all                          # the contract below; exit 0 = all good
./run.sh verify lp_bsa01_count_range --measure # also: how far over the limit slow.cpp is
```

It runs in the same throwaway Docker image as `header-problems/`
(`oj-content-build`: the judge's g++ 14, wkhtmltopdf, Thai fonts) and imports
that harness's generic parts — the judge-faithful runner (`timeout -k 2s`,
exit 124 = TLE), the output comparison, the PDF text probes and the math
renderer — so both problem kinds are judged and rendered the same way.

Import `dist/standard-problems.zip` in the OJ at **Manage › Problems → Batch
upload**. Problems arrive hidden; publish them, then import the lessons bundle
that links them (the lessons dry run refuses ids the grader does not have).

## A problem

`problems/<id>/`, id = `lp_<topic><nn>_<name>` (e.g. `lp_bsa01_count_range`):

| file | |
|---|---|
| `meta.json` | title (English), author, categories, difficulty, collection, limits, `has_tle_subtask`, subtasks, `pdf_probe`, `lesson` (slug of the lesson that uses it) |
| `statement.md` | house template, first line `# <title>` |
| `gen.py` | `python3 gen.py <dir>` writes `input01.txt` … `input10.txt`, **deterministic**, smallest first |
| `solution.cpp` | reference — every expected output is produced by running it |
| `slow.cpp` | naive version; required exactly when `has_tle_subtask` |
| `solution.py` | optional Python reference |

`meta.json` example:

```json
{
  "id": "lp_bsa01_count_range",
  "title": "Count in Range",
  "author": "Nonbangkok",
  "categories": ["Binary Search"],
  "difficulty": 1100,
  "collection": "Learn — Foundations",
  "lesson": "binary-search-array",
  "time_limit_ms": 1000,
  "memory_limit_mb": 256,
  "has_tle_subtask": true,
  "subtasks": [
    { "cases": 3, "percent": 30, "note": "$N, Q \\leq 1{,}000$" },
    { "cases": 2, "percent": 20, "note": "$N, Q \\leq 5{,}000$" },
    { "cases": 5, "percent": 50, "note": "$N, Q \\leq 40{,}000$" }
  ],
  "pdf_probe": "นับจำนวนสมาชิกที่มีค่าอยู่ในช่วง"
}
```

Ten cases always. The judge stops at the first failing case and scores the
passed prefix, so subtasks are listed smallest first and each subtask's
`percent` must equal its share of the cases (3 cases = 30%).

## Statement template

Same house style as the header problems ("Red Gate"), minus the
header-only sections:

1. `# <title>` (checked against meta.json, then rendered from it), then one or
   two narrative paragraphs.
2. `## คำอธิบาย :` — the task.
3. `## Input :` / `## Output :` — "บรรทัดแรก : …<br>" lines, variables as `$math$`.
4. `## Examples :` with `### ตัวอย่างที่ 1` and a ```` ```sample-input ```` /
   ```` ```sample-output ```` pair (more pairs allowed; every one is checked
   against solution.cpp), then `## คำอธิบายตัวอย่างที่ 1`.
5. `## Constraints :` — one `*` bullet per bound, as LaTeX.
6. `{{subtasks}}`, `{{limits}}` (generated; the Python limits are printed
   too), `{{> author}}` last.

Write bounds and complexities as LaTeX — the build extracts the rendered math
back out of the PDF, like the Thai probe. `<b>…</b>` for emphasis.

## Verification contract (`./run.sh verify`)

1. `dist/<id>/` matches meta.json (config, PDF, 10 testcase pairs).
2. `solution.cpp` prints every statement sample exactly.
3. `solution.cpp` is Accepted on all 10 cases under the real time limit
   (the build also warns when it uses more than half of it).
4. `solution.py`, when present, is Accepted under the judge's Python limit
   (time ×4) — proof the problem is fair in Python.
5. With `has_tle_subtask`: `slow.cpp` is Accepted on every case before the
   last subtask and times out on the first case of the last one, so the
   complexity the statement promises is proven by the cases.
