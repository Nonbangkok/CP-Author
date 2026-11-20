"""Shared code for the standard-problem harness (stdin/stdout problems).

Standard problems are the practice problems behind the Learn lessons
(lessons/CURRICULUM.md). They reuse the header-problem toolchain where it is
generic -- the same Docker image (g++ 14 like the judge, wkhtmltopdf) and the
judge-faithful runner and output comparison in ../header-problems/harness.py --
and render statements with Nonbangkok's own red-gate-v1 template (the Red Gate
layout, KaTeX, Sarabun), as the original task-pdf-writer renderer does.

A problem lives in problems/<id>/:

    meta.json       limits, categories, difficulty, subtasks, Thai PDF probe
    statement.html  Nonbangkok's red-gate-v1 format (HTML + $LaTeX$, see README.md),
                    first line "<h1><title></h1>"
    samples/        1.in, 2.in, ...: the statement's examples (outputs come from solution.cpp)
    gen.py          writes input01.txt .. input10.txt into the directory it is given
    solution.cpp    reference; produces every expected output
    slow.cpp        naive version, required when has_tle_subtask (must TLE exactly
                    at the last subtask, proving the promised complexity)
    solution.py     optional Python reference: must be Accepted under the
                    judge's Python multipliers (time x4)
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HEADER_DIR = ROOT.parent / "header-problems"
sys.path.insert(0, str(HEADER_DIR))

import harness as hh  # noqa: E402  (the header harness: runner, comparison, PDF probes)

PROBLEMS_DIR = ROOT / "problems"
DIST_DIR = ROOT / "dist"
WORK_DIR = DIST_DIR / ".work"
ZIP_NAME = "standard-problems.zip"

HarnessError = hh.HarnessError
TESTCASE_COUNT = hh.TESTCASE_COUNT
BINARY_NAME = hh.BINARY_NAME

# lp_<topic><nn>_<name>, e.g. lp_bsa01_count_range ("lesson problem").
PROBLEM_ID_PATTERN = re.compile(r"^lp_[a-z]+[0-9]{2}_[a-z0-9_]+$")

# Mirrors backend/constants/index.ts LANGUAGE_LIMITS.
PYTHON_TIME_MULTIPLIER = 4
PYTHON_MEMORY_MULTIPLIER = 2

REQUIRED_SECTIONS = [
    "Input :",
    "Output :",
    "Examples :",
    "Constraints :",
    "Subtasks :",
    "Limits :",
    "Author :",
    "Contacts :",
]

META_KEYS = {
    "id", "title", "author", "categories", "difficulty", "collection", "time_limit_ms",
    "memory_limit_mb", "has_tle_subtask", "subtasks", "pdf_probe", "lesson",
}
OPTIONAL_META_KEYS = {"collection", "lesson", "difficulty"}


@dataclass(frozen=True)
class Meta:
    id: str
    title: str
    author: str
    categories: list[str]
    difficulty: int | None
    collection: str | None
    time_limit_ms: int
    memory_limit_mb: int
    has_tle_subtask: bool
    subtasks: list[hh.Subtask]
    pdf_probe: str
    lesson: str | None
    source_dir: Path

    @property
    def dist_dir(self) -> Path:
        return DIST_DIR / self.id

    @property
    def work_dir(self) -> Path:
        return WORK_DIR / self.id

    @property
    def has_python(self) -> bool:
        return (self.source_dir / "solution.py").is_file()


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise HarnessError(message)


def load_meta(problem_dir: Path) -> Meta:
    pid = problem_dir.name
    path = problem_dir / "meta.json"
    _require(path.is_file(), f"{pid}: meta.json is missing")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise HarnessError(f"{pid}: meta.json is not valid JSON: {error}") from error
    _require(isinstance(raw, dict), f"{pid}: meta.json must be an object")
    missing = sorted(META_KEYS - OPTIONAL_META_KEYS - raw.keys())
    unknown = sorted(raw.keys() - META_KEYS)
    _require(not missing, f"{pid}: meta.json is missing {', '.join(missing)}")
    _require(not unknown, f"{pid}: meta.json has unknown key(s) {', '.join(unknown)}")

    _require(raw["id"] == pid, f"{pid}: meta.json id {raw['id']!r} must equal the folder name")
    _require(bool(PROBLEM_ID_PATTERN.match(pid)) and len(pid) <= hh.MAX_PROBLEM_ID_LENGTH,
             f"{pid}: problem ids look like lp_<topic><nn>_<name> (lowercase), at most {hh.MAX_PROBLEM_ID_LENGTH} chars")
    title = raw["title"]
    _require(isinstance(title, str) and title.strip() == title and 0 < len(title) <= hh.MAX_TITLE_LENGTH
             and title.isascii(), f"{pid}: title must be non-empty English text without surrounding spaces")
    _require(isinstance(raw["author"], str) and raw["author"].strip() != "", f"{pid}: author is required")

    categories = raw["categories"]
    _require(isinstance(categories, list) and all(c in hh.PROBLEM_CATEGORIES for c in categories)
             and len(set(categories)) == len(categories),
             f"{pid}: categories must be distinct values from {hh.PROBLEM_CATEGORIES}")
    difficulty = raw.get("difficulty")
    _require(difficulty is None or (isinstance(difficulty, int) and hh.DIFFICULTY_MIN <= difficulty <= hh.DIFFICULTY_MAX
                                    and difficulty % hh.DIFFICULTY_STEP == 0),
             f"{pid}: difficulty must be {hh.DIFFICULTY_MIN}-{hh.DIFFICULTY_MAX} in steps of {hh.DIFFICULTY_STEP}")
    collection = raw.get("collection")
    _require(collection is None or (isinstance(collection, str) and collection.strip()),
             f"{pid}: collection must be a name or omitted")

    time_limit = raw["time_limit_ms"]
    memory_limit = raw["memory_limit_mb"]
    _require(isinstance(time_limit, int) and time_limit >= hh.MIN_TIME_LIMIT_MS, f"{pid}: time_limit_ms is too small")
    _require(isinstance(memory_limit, int) and memory_limit >= hh.MIN_MEMORY_LIMIT_MB, f"{pid}: memory_limit_mb is too small")

    has_tle = raw["has_tle_subtask"]
    _require(isinstance(has_tle, bool), f"{pid}: has_tle_subtask must be true or false")
    subtasks_raw = raw["subtasks"]
    _require(isinstance(subtasks_raw, list) and len(subtasks_raw) >= (2 if has_tle else 1),
             f"{pid}: subtasks must be a list (at least two when has_tle_subtask)")
    subtasks: list[hh.Subtask] = []
    for entry in subtasks_raw:
        _require(isinstance(entry, dict) and set(entry) == {"cases", "percent", "note"}
                 and isinstance(entry["cases"], int) and entry["cases"] >= 1
                 and isinstance(entry["percent"], int) and entry["percent"] >= 1
                 and isinstance(entry["note"], str) and entry["note"].strip(),
                 f"{pid}: every subtask is {{cases >= 1, percent >= 1, note}}")
        subtasks.append(hh.Subtask(cases=entry["cases"], percent=entry["percent"], note=entry["note"]))
    _require(sum(s.cases for s in subtasks) == TESTCASE_COUNT, f"{pid}: subtask cases must add up to {TESTCASE_COUNT}")
    _require(sum(s.percent for s in subtasks) == 100, f"{pid}: subtask percents must add up to 100")
    # The judge stops at the first failed case and scores the passed prefix, so
    # each subtask's percent must equal its share of the cases.
    for number, s in enumerate(subtasks, start=1):
        _require(round(s.cases * 100 / TESTCASE_COUNT) == s.percent,
                 f"{pid}: subtask {number} has {s.cases} cases, so it is worth {s.cases * 100 // TESTCASE_COUNT}%, not {s.percent}%")

    probe = raw["pdf_probe"]
    _require(isinstance(probe, str) and len(probe) >= 8 and any("ก" <= ch <= "ฮ" for ch in probe),
             f"{pid}: pdf_probe must be a Thai phrase from the statement (8+ characters)")
    lesson = raw.get("lesson")
    _require(lesson is None or (isinstance(lesson, str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", lesson)),
             f"{pid}: lesson must be the slug of the lesson that uses the problem")

    for required in ("statement.html", "gen.py", "solution.cpp"):
        _require((problem_dir / required).is_file(), f"{pid}: {required} is missing")
    _require((problem_dir / "slow.cpp").is_file() == has_tle,
             f"{pid}: slow.cpp must exist exactly when has_tle_subtask is true")
    allowed = {"meta.json", "statement.html", "samples", "gen.py", "solution.cpp", "slow.cpp", "solution.py"}
    extra = sorted(p.name for p in problem_dir.iterdir() if p.name not in allowed and p.name != "__pycache__")
    _require(not extra, f"{pid}: unexpected file(s) {', '.join(extra)}")

    return Meta(
        id=pid, title=title, author=raw["author"], categories=categories, difficulty=difficulty,
        collection=collection, time_limit_ms=time_limit, memory_limit_mb=memory_limit,
        has_tle_subtask=has_tle, subtasks=subtasks, pdf_probe=probe, lesson=lesson, source_dir=problem_dir,
    )


def resolve_problem_dirs(selectors: list[str]) -> list[Path]:
    if not PROBLEMS_DIR.is_dir():
        raise HarnessError("problems/ does not exist")
    every = sorted(p for p in PROBLEMS_DIR.iterdir() if p.is_dir() and not p.name.startswith(("_", ".")))
    if not selectors:
        if not every:
            raise HarnessError("problems/ has no problem yet")
        return every
    chosen = []
    for selector in selectors:
        path = PROBLEMS_DIR / selector
        _require(path.is_dir(), f"no problem {selector!r} under problems/")
        chosen.append(path)
    return chosen


# --- statement (Nonbangkok's red-gate-v1 template) ---------------------------
#
# Statements are written the way the original Red Gate statement is
# (task-pdf-writer demo/red-gate/content.mjs): plain HTML with $...$ / $$...$$
# LaTeX, rendered by real KaTeX inside the red-gate-v1 page shell
# (template/red-gate-v1, copied unchanged from the OJ's
# backend/authoring/templates/red-gate-v1) with the author header and avatar,
# then printed by wkhtmltopdf with the same arguments as the original
# renderer (demo/red-gate/dockerPdf.mjs). Generated parts -- the examples
# (outputs produced by solution.cpp), subtasks, limits and author block --
# come from placeholders so they can never drift from meta.json or the code.

TEMPLATE_ROOT = ROOT / "template"
TEMPLATE_DIR = TEMPLATE_ROOT / "red-gate-v1"
AVATAR = TEMPLATE_ROOT / "avatar.png"
RENDER_ERROR_MARKER = "PDF_RENDER_ERROR"
REQUIRED_PLACEHOLDERS = ("{{examples}}", "{{subtasks}}", "{{limits}}", "{{> author}}")
SAMPLE_PADDING = "&#x20;           "  # the template's trailing line inside each sample <pre>


def escape_html(value: str) -> str:
    return (value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&#039;"))


def sample_inputs(meta: Meta) -> list[Path]:
    folder = meta.source_dir / "samples"
    inputs = sorted(folder.glob("*.in")) if folder.is_dir() else []
    _require(inputs, f"{meta.id}: samples/ needs at least one <n>.in file")
    names = [p.stem for p in inputs]
    _require(names == [str(i) for i in range(1, len(inputs) + 1)], f"{meta.id}: samples must be named 1.in, 2.in, ...")
    return inputs


def examples_html(samples: list[tuple[str, str]]) -> str:
    parts = ["<h2>Examples :</h2>"]
    for number, (sample_in, sample_out) in enumerate(samples, start=1):
        cells = []
        for text in (sample_in, sample_out):
            body = escape_html(text.rstrip("\n"))
            cells.append(f"<td><pre>\n{body}\n{SAMPLE_PADDING}\n</pre></td>")
        parts.append(f"<h3>ตัวอย่างที่ {number}</h3>\n<table class=\"sample-table\"><thead><tr><th>ข้อมูลนำเข้า</th>"
                     f"<th>ข้อมูลส่งออก</th></tr></thead><tbody><tr>{''.join(cells)}</tr></tbody></table>")
    return "\n\n".join(parts)


def subtasks_html(meta: Meta) -> str:
    items = "".join(f"<li>({s.percent} points) {s.note}</li>" for s in meta.subtasks)
    return f"<h2>Subtasks :</h2>\n<ol>{items}</ol>"


def limits_html(meta: Meta) -> str:
    def seconds(ms: int) -> str:
        value = f"{ms / 1000:g}"
        return f"{value} second" + ("" if value == "1" else "s")

    return ("<h2>Limits :</h2>\n<ul>"
            f"<li>Time limit: {seconds(meta.time_limit_ms)} (Python: {seconds(meta.time_limit_ms * PYTHON_TIME_MULTIPLIER)})</li>"
            f"<li>Memory limit: {meta.memory_limit_mb} MB (Python: {meta.memory_limit_mb * PYTHON_MEMORY_MULTIPLIER} MB)</li></ul>")


def assemble_statement(meta: Meta, samples: list[tuple[str, str]]) -> str:
    """statement.html with the generated parts filled in."""
    path = meta.source_dir / "statement.html"
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    first = text.lstrip().split("\n", 1)[0].strip()
    _require(first == f"<h1>{escape_html(meta.title)}</h1>",
             f"{meta.id}: statement.html must start with <h1>{meta.title}</h1> (the title in meta.json)")
    for placeholder in REQUIRED_PLACEHOLDERS:
        _require(text.count(placeholder) == 1, f"{meta.id}: statement.html must contain {placeholder} exactly once")
    text = (text.replace("{{examples}}", examples_html(samples))
                .replace("{{subtasks}}", subtasks_html(meta))
                .replace("{{limits}}", limits_html(meta))
                .replace("{{> author}}", (TEMPLATE_ROOT / "author.html").read_text(encoding="utf-8").strip()))
    scan = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    _require("{{" not in scan and "}}" not in scan, f"{meta.id}: statement.html still contains an unexpanded placeholder")
    _require(not re.search(r"<script|<style|\son[a-z]+\s*=|javascript:", scan, flags=re.IGNORECASE),
             f"{meta.id}: statement.html may not contain scripts, styles or event handlers")
    headings = {re.sub(r"<[^>]+>", "", h).strip() for h in re.findall(r"<h2>(.*?)</h2>", scan, flags=re.DOTALL)}
    missing = [section for section in REQUIRED_SECTIONS if section not in headings]
    _require(not missing, f"{meta.id}: statement.html is missing the section(s): {', '.join(missing)}")
    return text


def _file_url(path: Path) -> str:
    return "file://" + str(path.resolve()).replace(" ", "%20")


def statement_html(meta: Meta, body: str) -> str:
    """The red-gate-v1 page, as the OJ's backend/authoring/pdfTemplate.ts builds it."""
    document = json.loads((TEMPLATE_ROOT / "document.json").read_text(encoding="utf-8"))
    base = _file_url(TEMPLATE_DIR)
    css = (TEMPLATE_DIR / "layout.css").read_text(encoding="utf-8")

    def font(name: str, file: str, weight: int) -> str:
        return (f"@font-face{{font-family:'{name}';src:local('{name}'),url('{base}/fonts/{file}') format('truetype');"
                f"font-weight:{weight};font-style:normal;font-display:block;}}")

    return f"""<!doctype html>
<html lang="th"><head><meta charset="utf-8"><title>{escape_html(meta.title)}</title>
<link rel="stylesheet" href="{base}/vendor/katex.css"><style>
{font('Sarabun', 'Sarabun-Regular.ttf', 400)}
{font('Sarabun', 'Sarabun-Medium.ttf', 500)}
{font('Sarabun', 'Sarabun-Bold.ttf', 700)}
@font-face{{font-family:'RedGatePreviewInconsolata';src:url('{base}/fonts/Inconsolata-VariableFont_wdth,wght.ttf') format('truetype');font-weight:100 900;font-style:normal;font-display:block}}
{css}
</style></head><body><main class="document">
<header class="document-header"><div class="header-logo"><img src="{_file_url(AVATAR)}" alt=""></div>
<div class="header-title"><div><span class="aka-name">{escape_html(document['akaName'])}</span><br><span class="author-name">Author : {escape_html(document['realName'])}</span></div></div>
<div class="header-meta"><div>{escape_html(meta.id)}</div><div>{escape_html(document['language'])} ({escape_html(document['countryCode'])})</div></div><div style="clear:both"></div><hr></header>
<article id="statement" class="statement">{body}</article></main>
<script src="{base}/vendor/bundle.js"></script><script>
function failPdfRender(error) {{
  var marker = document.createElement('p');
  marker.textContent = '{RENDER_ERROR_MARKER}: ' + String(error);
  document.getElementById('statement').appendChild(marker);
}}
window.onerror = function (message) {{ failPdfRender(message); return true; }};
try {{
  var renderMathInElement=require('katex/dist/contrib/auto-render');
  renderMathInElement(document.getElementById('statement'),{{
    delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'\\\\[',right:'\\\\]',display:true}},{{left:'$',right:'$',display:false}},{{left:'\\\\(',right:'\\\\)',display:false}}],
    trust:false,strict:'error',throwOnError:true,maxExpand:1000,maxSize:100,
    errorCallback:function (message,error) {{ throw error || new Error(message); }}
  }});
}} catch (error) {{ failPdfRender(error); }}
window.setTimeout(function () {{ window.status='ready-to-print'; }}, 1500);
</script></body></html>
"""


def render_pdf(meta: Meta, html_path: Path, pdf_path: Path) -> None:
    """wkhtmltopdf with the original renderer's arguments (demo/red-gate/dockerPdf.mjs)."""
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    # The original renderer installs Sarabun and Inconsolata as system fonts
    # (demo/red-gate/Dockerfile), so the template's local('Sarabun') resolves to
    # a real font and the PDF carries extractable text. Do the same without
    # changing the image: a fontconfig file that adds the template's fonts/.
    fonts_conf = meta.work_dir / "fonts.conf"
    hh.write_text(fonts_conf, (
        '<?xml version="1.0"?>\n<!DOCTYPE fontconfig SYSTEM "fonts.dtd">\n<fontconfig>\n'
        '  <include ignore_missing="yes">/etc/fonts/fonts.conf</include>\n'
        f'  <dir>{TEMPLATE_DIR / "fonts"}</dir>\n'
        f'  <cachedir>{meta.work_dir / "fontconfig-cache"}</cachedir>\n'
        '</fontconfig>\n'
    ))
    env = {**os.environ, "FONTCONFIG_FILE": str(fonts_conf)}
    command = [
        "wkhtmltopdf", "--enable-local-file-access", "--page-size", "A4",
        "--margin-left", "0.75in", "--margin-right", "0.75in", "--margin-top", "0.62in", "--margin-bottom", "1in",
        "--print-media-type", "--window-status", "ready-to-print", "--encoding", "UTF-8", "--quiet",
        str(html_path), str(pdf_path),
    ]
    try:
        completed = subprocess.run(command, capture_output=True, text=True, check=False, timeout=90, env=env)
    except subprocess.TimeoutExpired as error:
        raise HarnessError(f"{meta.id}: wkhtmltopdf did not finish within 90 s") from error
    if completed.returncode != 0 or not pdf_path.is_file() or pdf_path.read_bytes()[:4] != b"%PDF":
        raise HarnessError(f"{meta.id}: wkhtmltopdf failed (exit {completed.returncode}): "
                           f"{(completed.stderr or completed.stdout).strip()[:800]}")


def assert_statement_survived(meta: Meta, pdf_path: Path) -> str:
    """Read the PDF's text back: math rendered, Thai present, every section there."""
    # -raw keeps the content-stream order: with KaTeX boxes between the words,
    # the default layout mode reorders Thai text across lines.
    text_path = meta.work_dir / "statement.txt"
    completed = subprocess.run(["pdftotext", "-raw", "-enc", "UTF-8", str(pdf_path), str(text_path)],
                               capture_output=True, text=True, check=False)
    _require(completed.returncode == 0 and text_path.is_file(), f"{meta.id}: pdftotext failed: {completed.stderr[:300]}")
    extracted = text_path.read_text(encoding="utf-8", errors="replace")
    marker = extracted.find(RENDER_ERROR_MARKER)
    _require(marker < 0, f"{meta.id}: KaTeX could not render the statement: {extracted[marker:marker + 300].strip()}")
    _require("$" not in extracted, f"{meta.id}: the PDF still shows a literal $ — some math was not rendered "
             "(unbalanced $ or math inside an element KaTeX skips)")
    haystack = hh.thai_comparison_key(extracted)
    base = sum(1 for ch in extracted if hh.THAI_BASE_RANGE[0] <= ord(ch) < hh.THAI_BASE_RANGE[1])
    _require(base >= 150, f"{meta.id}: only {base} Thai characters came back out of the PDF (missing Thai font?)")
    for probe in [meta.pdf_probe, *REQUIRED_SECTIONS, meta.title]:
        _require(hh.thai_comparison_key(probe) in haystack,
                 f"{meta.id}: \"{probe}\" is NOT in the rendered PDF (missing glyphs or section)")
    return meta.pdf_probe


# --- compile & run ---------------------------------------------------------


def compile_cpp(meta: Meta, source: Path, workspace: Path, binary: str = BINARY_NAME) -> None:
    """Compile one source exactly like the judge compiles a C++ submission."""
    hh.reset_dir(workspace)
    hh.write_text(workspace / "main.cpp", source.read_text(encoding="utf-8"))
    completed = subprocess.run(["g++", *hh.CPP_COMPILE_FLAGS, "main.cpp", "-o", binary],
                               cwd=workspace, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        raise HarnessError(f"{meta.id}: {source.name} does not compile:\n{(completed.stderr or '')[:2000]}")


def prepare_python(meta: Meta, source: Path, workspace: Path) -> str:
    """Copy the Python reference and syntax-check it like the judge does; return the runner name."""
    hh.reset_dir(workspace)
    hh.write_text(workspace / "main.py", source.read_text(encoding="utf-8"))
    completed = subprocess.run([sys.executable, "-m", "py_compile", "main.py"],
                               cwd=workspace, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        raise HarnessError(f"{meta.id}: {source.name} has a syntax error:\n{(completed.stderr or '')[:1200]}")
    runner = workspace / "run_python"
    hh.write_text(runner, f"#!/bin/sh\nexec {sys.executable} main.py\n")
    runner.chmod(0o755)
    return "run_python"


def case_paths(meta: Meta) -> tuple[Path, Path]:
    return meta.dist_dir / "testcases" / "input", meta.dist_dir / "testcases" / "output"
