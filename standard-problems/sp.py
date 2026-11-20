"""Shared code for the standard-problem harness (stdin/stdout problems).

Standard problems are the practice problems behind the Learn lessons
(lessons/CURRICULUM.md). They reuse the header-problem toolchain where it is
generic -- the same Docker image (g++ 14 like the judge, wkhtmltopdf, Thai
fonts), the judge-faithful runner and output comparison in
../header-problems/harness.py, and the server-side math renderer in
../header-problems/mdrender.py -- and add what differs: a single-source C++
reference, an optional Python reference, no grader/starter file sets, and a
statement template without the header-only sections.

A problem lives in problems/<id>/:

    meta.json       limits, categories, difficulty, subtasks, Thai PDF probe
    statement.md    the house template (see README.md), first line "# <title>"
    gen.py          writes input01.txt .. input10.txt into the directory it is given
    solution.cpp    reference; produces every expected output
    slow.cpp        naive version, required when has_tle_subtask (must TLE exactly
                    at the last subtask, proving the promised complexity)
    solution.py     optional Python reference: must be Accepted under the
                    judge's Python multipliers (time x4)
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HEADER_DIR = ROOT.parent / "header-problems"
sys.path.insert(0, str(HEADER_DIR))

import harness as hh  # noqa: E402  (the header harness: runner, comparison, PDF probes)
import mdrender  # noqa: E402

PROBLEMS_DIR = ROOT / "problems"
DIST_DIR = ROOT / "dist"
WORK_DIR = DIST_DIR / ".work"
SHARED_STATEMENT_DIR = hh.STATEMENT_DIR  # style.css and the author partial are shared
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
    "คำอธิบาย :",
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

    for required in ("statement.md", "gen.py", "solution.cpp"):
        _require((problem_dir / required).is_file(), f"{pid}: {required} is missing")
    _require((problem_dir / "slow.cpp").is_file() == has_tle,
             f"{pid}: slow.cpp must exist exactly when has_tle_subtask is true")
    allowed = {"meta.json", "statement.md", "gen.py", "solution.cpp", "slow.cpp", "solution.py"}
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


# --- statement -------------------------------------------------------------


def limits_section(meta: Meta) -> str:
    def seconds(ms: int) -> str:
        value = f"{ms / 1000:g}"
        return f"{value} second" + ("" if value == "1" else "s")

    return "\n".join([
        "## Limits :",
        "",
        f"* Time limit: {seconds(meta.time_limit_ms)} (Python: {seconds(meta.time_limit_ms * PYTHON_TIME_MULTIPLIER)})",
        f"* Memory limit: {meta.memory_limit_mb} MB (Python: {meta.memory_limit_mb * PYTHON_MEMORY_MULTIPLIER} MB)",
    ])


def assemble_statement_markdown(meta: Meta) -> str:
    text = (meta.source_dir / "statement.md").read_text(encoding="utf-8")
    text = hh._split_title(meta, text)  # checks "# <title>" against meta.json, then drops it
    _require("{{> author}}" in text, f"{meta.id}: statement.md must end with the shared partial {{{{> author}}}}")
    text = text.replace("{{> author}}", (SHARED_STATEMENT_DIR / "author.md").read_text(encoding="utf-8").strip())
    for placeholder, section in (("{{subtasks}}", hh.subtask_section(meta)), ("{{limits}}", limits_section(meta))):
        _require(placeholder in text, f"{meta.id}: statement.md must place the generated section with {placeholder}")
        text = text.replace(placeholder, section)
    text = text.replace("{{id}}", meta.id).replace("{{title}}", meta.title)
    scan = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    _require("{{" not in scan and "}}" not in scan, f"{meta.id}: statement.md still contains an unexpanded placeholder")
    headings = {line[3:].strip() for line in scan.splitlines() if line.startswith("## ")}
    missing = [section for section in REQUIRED_SECTIONS if section not in headings]
    _require(not missing, f"{meta.id}: statement.md is missing the section(s): {', '.join(missing)}")
    return text


def statement_html(meta: Meta, markdown: str) -> str:
    style = (SHARED_STATEMENT_DIR / "style.css").read_text(encoding="utf-8")
    difficulty = "ไม่จัดระดับ" if meta.difficulty is None else str(meta.difficulty)
    try:
        body = mdrender.render_markdown(markdown)
    except mdrender.MathError as error:
        raise HarnessError(f"{meta.id}: statement math does not render: {error}") from error
    return (
        "<!DOCTYPE html>\n<html lang=\"th\">\n<head>\n<meta charset=\"utf-8\">\n"
        f"<title>{meta.id}</title>\n<style>\n{style}\n</style>\n</head>\n<body>\n"
        f"<h1>{meta.title}</h1>\n"
        f"<p class=\"meta\"><span>รหัสข้อ: <code>{meta.id}</code></span>"
        f"<span>ภาษา: C++, Python</span><span>ระดับความยาก: {difficulty}</span></p>\n"
        f"{body}\n</body>\n</html>\n"
    )


def render_pdf(meta: Meta, html_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "wkhtmltopdf", "--encoding", "UTF-8", "--page-size", "A4", "--print-media-type",
        "--margin-top", "18mm", "--margin-bottom", "18mm", "--margin-left", "16mm", "--margin-right", "16mm",
        "--footer-right", "[page]/[topage]", "--footer-font-size", "8",
        "--disable-local-file-access", "--load-error-handling", "abort", "--quiet",
        str(html_path), str(pdf_path),
    ]
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if completed.returncode != 0 or not pdf_path.is_file() or pdf_path.read_bytes()[:4] != b"%PDF":
        raise HarnessError(f"{meta.id}: wkhtmltopdf failed (exit {completed.returncode}): "
                           f"{(completed.stderr or completed.stdout).strip()[:800]}")


def assert_statement_survived(meta: Meta, pdf_path: Path, markdown: str) -> tuple[str, str]:
    """The Thai and the math must come back out of the finished PDF."""
    extracted = hh.extract_pdf_text(meta, pdf_path, meta.work_dir)
    haystack = hh.thai_comparison_key(extracted)
    base = sum(1 for ch in extracted if hh.THAI_BASE_RANGE[0] <= ord(ch) < hh.THAI_BASE_RANGE[1])
    _require(base >= 150, f"{meta.id}: only {base} Thai characters came back out of the PDF (missing Thai font?)")
    for probe in [meta.pdf_probe, *REQUIRED_SECTIONS]:
        _require(hh.thai_comparison_key(probe) in haystack,
                 f"{meta.id}: \"{probe}\" is NOT in the rendered PDF (missing glyphs or section)")
    return meta.pdf_probe, hh.assert_math_survived(meta, extracted, markdown)


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
