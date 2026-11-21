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
(`oj-content-build`: the judge's g++ 14 and wkhtmltopdf 0.12.6) and imports
that harness's judge-faithful runner (`timeout -k 2s`, exit 124 = TLE) and
output comparison, so both problem kinds are judged the same way.

Import `dist/standard-problems.zip` in the OJ at **Manage › Problems → Batch
upload**. Problems arrive hidden; publish them, then import the lessons bundle
that links them (the lessons dry run refuses ids the grader does not have).

## A problem

`problems/<id>/`, id = `lp_<topic><nn>_<name>` (e.g. `lp_bsa01_count_range`):

| file | |
|---|---|
| `meta.json` | title (English), author, categories, difficulty, collection, limits, `has_tle_subtask`, subtasks, `pdf_probe`, `lesson` (slug of the lesson that uses it) |
| `statement.html` | Nonbangkok's red-gate-v1 format (below), first line `<h1><title></h1>` |
| `samples/1.in`, `2.in`, … | the statement's examples; outputs come from solution.cpp |
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

## Statement template — Nonbangkok's red-gate-v1

Statements use the author's own template, exactly as the original Red Gate
statement is written (`task-pdf-writer/demo/red-gate/content.mjs`): **HTML with
`$...$` / `$$...$$` LaTeX**, rendered by real KaTeX inside the red-gate-v1 page
(`template/red-gate-v1/`, copied unchanged from the OJ's
`backend/authoring/templates/red-gate-v1`) with the avatar header
"Nonbangkok / Author : Kittitouch Thipmontha / <task code> / Thai (THA)", and
printed by wkhtmltopdf with the original renderer's arguments. Sarabun and
Inconsolata are registered as fonts for the render, like the original's
Docker image, so the PDF carries real text.

`statement.html`, in this order:

```html
<h1>Count in Range</h1>                       <!-- must equal meta.json's title -->
<p>…story / task, <b>bold</b> for the key facts, $N$ for math…</p>

<h2>Input :</h2>
<p class="input-spec">บรรทัดแรก : …<br>บรรทัดที่สอง : …</p>

<h2>Output :</h2>
<p>มีทั้งหมด $Q$ บรรทัด โดย<br>บรรทัดที่ $j$ …</p>

{{examples}}                                  <!-- generated from samples/*.in -->

<h2>คำอธิบายตัวอย่างที่ 1</h2>
<p>…</p>

<div class="forced-page-break"></div>        <!-- optional, where it helps the split -->

<h2>Constraints :</h2>
<ul><li>$1 \leq N \leq 10^5$</li></ul>

{{subtasks}}                                  <!-- generated from meta.json -->

{{limits}}                                    <!-- generated, Python limits included -->

{{> author}}                                  <!-- template/author.html: Author : + Contacts : -->
```

* `{{examples}}` writes `<h2>Examples :</h2>` and one `ตัวอย่างที่ N` sample
  table per `samples/N.in`, in the template's own markup; the **output column
  is produced by running solution.cpp**, so a sample can never be wrong.
* Classes from the template: `input-spec`, `geometry-data`, `sample-table`,
  `forced-page-break`. No scripts, styles or event handlers.
* KaTeX runs in strict mode: an unknown command or bad formula fails the
  build with KaTeX's message, and a stray `$` left in the PDF fails it too.
* Never put Thai inside math; write the words outside the `$...$`.

## Verification contract (`./run.sh verify`)

1. `dist/<id>/` matches meta.json (config, PDF, 10 testcase pairs).
2. `solution.cpp` still prints every example (outputs were built from it).
3. `solution.cpp` is Accepted on all 10 cases under the real time limit
   (the build also warns when it uses more than half of it).
4. `solution.py`, when present, is Accepted under the judge's Python limit
   (time ×4) — proof the problem is fair in Python.
5. With `has_tle_subtask`: `slow.cpp` is Accepted on every case before the
   last subtask and times out on the first case of the last one, so the
   complexity the statement promises is proven by the cases.
