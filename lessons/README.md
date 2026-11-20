# Lessons — content for the OJ's Learn section

Source of the tracks shown at `/learn` in the grader: ordered **tracks → modules →
lessons**, each lesson a short Markdown page that ends in problems the grader
already has. The OJ imports them as one ZIP (bundle format 1).

```bash
cd lessons
./run.sh check     # validate everything, write nothing
./run.sh build     # validate, then write dist/lessons-bundle.zip
```

Plain Python 3, no Docker. Then in the OJ: **Manage › Lessons → drop
`dist/lessons-bundle.zip`**. The page runs a dry run first and shows what will be
added, changed and removed; importing is all-or-nothing. That dry run is the
final gate: it renders every lesson through the same sanitizer as problem
statements and checks every problem id exists in *that* grader.

Identity is the **slug**. Re-importing keeps learners' progress for every lesson
whose slug is still in the bundle; a lesson whose slug disappears is deleted
together with its progress (the OJ asks for confirmation when anyone completed
it). Rename a slug only if you mean "this is a different lesson".

## Layout

```
lessons/
  tracks.json                       { "tracks": ["data-structures", ...] }   order of tracks
  known-problems.txt                problem ids that exist in the grader but are not header problems
  data-structures/
    track.json                      { "slug", "title", "description"?, "modules": ["01-pair", ...] }
    01-pair/
      module.json                   { "slug", "title", "summary"?, "lessons": [ ... ] }
      operator-overloading.md
      assets/figure-1.png           only if a lesson lists it
```

A track folder's name **is** its slug. Module folders can be named anything
plain (`01-pair`); the module's slug is inside `module.json`. Array order is
display order everywhere.

A lesson entry in `module.json`:

```json
{
  "slug": "operator-overloading",
  "title": "Pair & Operator Overloading",
  "summary": "one line shown under the title",
  "minutes": 12,
  "file": "operator-overloading.md",
  "problems": [
    { "id": "hp_pair01_equal", "role": "example" },
    { "id": "hp_pair02_less", "role": "practice" },
    { "id": "hp_pair10_ordering", "role": "challenge" }
  ],
  "assets": ["figure-1.png"]
}
```

* slugs: lowercase kebab-case, at most 64 characters; lesson slugs are unique
  across the whole bundle.
* `minutes`: whole minutes, 1–180. `problems`: at most 20, each once.
* `role` is shown to learners as Example / Practice / Challenge.
* `assets`: png, jpg, jpeg, webp or gif, at most 2 MB each, stored in the
  module's `assets/` folder and referenced as `![alt](assets/figure-1.png)`.
* Unknown keys are errors, and so is any file nothing references.

## Writing a lesson

Body: GitHub-flavoured Markdown, `$…$` / `$$…$$` math (KaTeX), fenced code
with a language (`cpp`, `python`, `text`). Start with `##` headings — the page
title comes from `module.json`, and `##`/`###` headings become the "On this
page" list. Raw HTML beyond simple formatting is rejected by the sanitizer.

Directives (each line starts at column 0; a closing `:::` on its own line):

| Directive | Renders as |
|---|---|
| `:::hint [title]` … `:::` | collapsed "Hint" box |
| `:::solution [problem-id]` … `:::` | collapsed "Solution" box (open to everyone, no gate) |
| `:::note [title]` / `:::warning [title]` … `:::` | callout |
| `:::tabs` with several fenced blocks … `:::` | code tabs (one tab per block, labelled by language) |
| `:::problem <problem-id>` (one line) | a card with the learner's status and an "Open problem" link |

Every problem named by `:::problem` or `:::solution` must also be in the
lesson's `problems` list. A problem that is hidden or sits in a running contest
shows as "Problem unavailable" until it is back.

### Voice

The OJ's interface is English; **lesson text is Thai, friendly and casual** —
talk to the learner like a senior explaining at the next desk: "ลองนึกดูก่อนนะ",
"จุดที่พลาดบ่อยที่สุดคือ…", "ไม่ต้องห่วง". Keep identifiers, member names and
complexities in English/LaTeX (`mFront`, `ensureCapacity`, $O(\log n)$). KaTeX
cannot typeset Thai inside math, so never put Thai in `\text{…}` — write the
words outside the `$…$`.

Teach the idea, not the answer: show the technique on a neighbouring task, and
put problem-specific nudges in `:::hint`. A full solution to a problem in the
set belongs in `:::solution` at most, and usually not even there.

## Rules mirrored from the OJ

`build.py` repeats the OJ backend's checks (`backend/constants/lessons.ts`,
`backend/services/lessonMarkdown.ts`, `backend/services/lessonBundleReader.ts`)
so mistakes fail here, before an upload. When the OJ changes those rules,
change `build.py` in the same breath. It cannot render the Markdown, so a
sanitizer rejection still only shows up in the OJ's dry run.
