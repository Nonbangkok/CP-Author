#!/usr/bin/env python3
"""Validate the lessons and pack them into dist/lessons-bundle.zip (bundle format 1).

The OJ imports the ZIP at Manage > Lessons (dry run first). Its importer is the
real gate -- it renders every lesson through the statement sanitizer and checks
that each problem exists in *that* grader -- but this script catches everything
it can earlier, with the same rules, so a PR fails before anyone uploads it:

  * layout: tracks.json -> <track>/track.json -> <track>/<module>/module.json -> lesson .md + assets/
  * strict JSON shapes, slugs, limits (mirror of OJ backend/constants/lessons.ts)
  * lesson directives (mirror of OJ backend/services/lessonMarkdown.ts)
  * every problem named by :::problem / :::solution is listed in the lesson's "problems"
  * every listed problem exists: a folder in ../header-problems/problems/ or
    ../standard-problems/problems/, or an id in known-problems.txt
  * images: declared, png/jpg/jpeg/webp/gif, content matches the extension
  * no stray files

Keep the mirrored rules in sync with the OJ backend when those change.

Usage: python3 build.py [--check]     (--check validates without writing the ZIP)
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIST = HERE / "dist"
HEADER_PROBLEMS = HERE.parent / "header-problems" / "problems"
STANDARD_PROBLEMS = HERE.parent / "standard-problems" / "problems"
KNOWN_PROBLEMS = HERE / "known-problems.txt"

# -- mirrored from OJ backend/constants/lessons.ts -----------------------------
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SLUG_MAX = 64
DIR_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
LESSON_FILE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,100}\.md$")
PROBLEM_ID = re.compile(r"^[A-Za-z0-9_-]{1,50}$")
ASSET_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
ROLES = {"example", "practice", "challenge"}
ASSET_TYPES = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp", "gif": "image/gif"}
MAX_TITLE, MAX_SUMMARY, MAX_MINUTES = 200, 500, 180
MAX_TRACKS, MAX_MODULES, MAX_LESSONS_PER_MODULE, MAX_LESSONS = 20, 30, 40, 500
MAX_PROBLEMS, MAX_ASSETS = 20, 30
MAX_JSON, MAX_MARKDOWN, MAX_ASSET = 256 * 1024, 200 * 1024, 2 * 1024 * 1024
MAX_BUNDLE = 25 * 1024 * 1024

# -- mirrored from OJ backend/services/lessonMarkdown.ts -----------------------
OPEN_DIRECTIVE = re.compile(r"^:::(hint|solution|note|warning|tabs|problem)(?:[ \t]+(.*?))?[ \t]*$")
CLOSE_DIRECTIVE = re.compile(r"^:::[ \t]*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
MAX_DIRECTIVE_DEPTH, MAX_DIRECTIVE_TITLE = 3, 120

errors: list[str] = []


def fail(path: Path | str, message: str) -> None:
    rel = path.relative_to(HERE) if isinstance(path, Path) else path
    errors.append(f"{rel}: {message}")


def read_json(path: Path) -> dict | None:
    if not path.is_file():
        fail(path, "file is missing")
        return None
    if path.stat().st_size > MAX_JSON:
        fail(path, f"is larger than {MAX_JSON} bytes")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(path, f"is not valid JSON ({exc})")
        return None
    if not isinstance(data, dict):
        fail(path, "must be a JSON object")
        return None
    return data


def check_keys(path: Path, data: dict, required: set[str], optional: set[str] = frozenset(), where: str = "") -> bool:
    ok = True
    for key in sorted(required - data.keys()):
        fail(path, f"{where}missing \"{key}\"")
        ok = False
    for key in sorted(data.keys() - required - optional):
        fail(path, f"{where}unknown key \"{key}\"")
        ok = False
    return ok


def check_slug(path: Path, value: object, where: str) -> bool:
    if not isinstance(value, str) or len(value) > SLUG_MAX or not SLUG.match(value):
        fail(path, f"{where}slug {value!r} must be lowercase kebab-case, at most {SLUG_MAX} characters")
        return False
    return True


def check_text(path: Path, value: object, where: str, limit: int, required: bool) -> None:
    if value is None and not required:
        return
    if not isinstance(value, str) or (required and not value.strip()) or len(value.strip()) > limit:
        fail(path, f"{where} must be {'non-empty ' if required else ''}text of at most {limit} characters")


def directive_refs(path: Path, source: str) -> list[str]:
    """Validate directives the way the OJ preprocessor does; return problem ids they name."""
    refs: list[str] = []
    stack: list[tuple[str, int]] = []
    fence: str | None = None
    for number, line in enumerate(source.split("\n"), start=1):
        line = line.rstrip("\r")
        fence_match = FENCE.match(line)
        if fence is not None:
            if fence_match and fence_match.group(1)[0] == fence[0] and len(fence_match.group(1)) >= len(fence) \
                    and line.strip() == fence_match.group(1):
                fence = None
            continue
        if fence_match:
            fence = fence_match.group(1)
            continue
        if not line.startswith(":::"):
            if line.lstrip().startswith(":::"):
                fail(path, f"line {number}: a directive must start at the beginning of a line")
            continue
        if CLOSE_DIRECTIVE.match(line):
            if not stack:
                fail(path, f"line {number}: ::: closes nothing")
            else:
                stack.pop()
            continue
        match = OPEN_DIRECTIVE.match(line)
        if not match:
            fail(path, f"line {number}: unknown directive {line.strip()[:40]!r}")
            continue
        kind, argument = match.group(1), (match.group(2) or "").strip()
        if kind in ("problem", "solution") and argument:
            if not PROBLEM_ID.match(argument):
                fail(path, f"line {number}: {argument!r} is not a valid problem id")
            else:
                refs.append(argument)
        if kind == "problem":
            if not argument:
                fail(path, f"line {number}: :::problem needs a problem id")
            continue
        if kind == "tabs" and argument:
            fail(path, f"line {number}: :::tabs takes no argument")
        if kind in ("hint", "note", "warning") and len(argument) > MAX_DIRECTIVE_TITLE:
            fail(path, f"line {number}: directive title is longer than {MAX_DIRECTIVE_TITLE} characters")
        if len(stack) >= MAX_DIRECTIVE_DEPTH:
            fail(path, f"line {number}: directives nest deeper than {MAX_DIRECTIVE_DEPTH}")
        stack.append((kind, number))
    if fence is not None:
        fail(path, "a fenced code block is not closed")
    for kind, number in stack:
        fail(path, f"line {number}: :::{kind} is not closed")
    return refs


def sniff_image(data: bytes) -> str | None:
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    return None


def known_problem_ids() -> set[str]:
    ids: set[str] = set()
    for folder in (HEADER_PROBLEMS, STANDARD_PROBLEMS):
        if folder.is_dir():
            ids |= {p.name for p in folder.iterdir() if (p / "meta.json").is_file()}
    if KNOWN_PROBLEMS.is_file():
        for line in KNOWN_PROBLEMS.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                ids.add(line)
    return ids


def source_commit() -> str | None:
    try:
        out = subprocess.run(["git", "rev-parse", "--short=12", "HEAD"], cwd=HERE, capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    commit = out.stdout.strip()
    return commit if re.fullmatch(r"[0-9a-f]{7,64}", commit) else None


def build(check_only: bool) -> int:
    used: set[Path] = set()
    problems = known_problem_ids()
    index = read_json(HERE / "tracks.json")
    if index is None:
        return report()
    used.add(HERE / "tracks.json")
    check_keys(HERE / "tracks.json", index, {"tracks"})
    tracks = index.get("tracks")
    if not isinstance(tracks, list) or not tracks or len(tracks) > MAX_TRACKS or len(set(tracks)) != len(tracks):
        fail(HERE / "tracks.json", f'"tracks" must list 1..{MAX_TRACKS} distinct track folders')
        return report()

    lesson_slugs: dict[str, str] = {}
    lesson_count = 0
    entries: list[tuple[str, Path]] = []
    for track_dir in tracks:
        if not isinstance(track_dir, str) or not DIR_NAME.match(track_dir):
            fail(HERE / "tracks.json", f"{track_dir!r} is not a plain folder name")
            continue
        track_path = HERE / track_dir / "track.json"
        track = read_json(track_path)
        if track is None:
            continue
        used.add(track_path)
        entries.append((f"{track_dir}/track.json", track_path))
        check_keys(track_path, track, {"slug", "title", "modules"}, {"description"})
        if check_slug(track_path, track.get("slug"), "") and track["slug"] != track_dir:
            fail(track_path, f"slug {track['slug']!r} must equal its folder name {track_dir!r}")
        check_text(track_path, track.get("title"), "title", MAX_TITLE, True)
        check_text(track_path, track.get("description"), "description", MAX_SUMMARY, False)
        modules = track.get("modules")
        if not isinstance(modules, list) or not modules or len(modules) > MAX_MODULES or len(set(map(str, modules))) != len(modules):
            fail(track_path, f'"modules" must list 1..{MAX_MODULES} distinct module folders')
            continue
        module_slugs: set[str] = set()
        for module_dir in modules:
            if not isinstance(module_dir, str) or not DIR_NAME.match(module_dir):
                fail(track_path, f"{module_dir!r} is not a plain folder name")
                continue
            base = HERE / track_dir / module_dir
            module_path = base / "module.json"
            module = read_json(module_path)
            if module is None:
                continue
            used.add(module_path)
            entries.append((f"{track_dir}/{module_dir}/module.json", module_path))
            check_keys(module_path, module, {"slug", "title", "lessons"}, {"summary"})
            if check_slug(module_path, module.get("slug"), "module "):
                if module["slug"] in module_slugs:
                    fail(module_path, f"module slug {module['slug']!r} is used twice in this track")
                module_slugs.add(module["slug"])
            check_text(module_path, module.get("title"), "title", MAX_TITLE, True)
            check_text(module_path, module.get("summary"), "summary", MAX_SUMMARY, False)
            lessons = module.get("lessons")
            if not isinstance(lessons, list) or not lessons or len(lessons) > MAX_LESSONS_PER_MODULE:
                fail(module_path, f'"lessons" must list 1..{MAX_LESSONS_PER_MODULE} lessons')
                continue
            for position, lesson in enumerate(lessons, start=1):
                where = f"lessons[{position - 1}] "
                if not isinstance(lesson, dict):
                    fail(module_path, f"{where}must be an object")
                    continue
                lesson_count += 1
                check_keys(module_path, lesson, {"slug", "title", "minutes", "file", "problems"}, {"summary", "assets"}, where)
                slug_ok = check_slug(module_path, lesson.get("slug"), where)
                check_text(module_path, lesson.get("title"), f"{where}title", MAX_TITLE, True)
                check_text(module_path, lesson.get("summary"), f"{where}summary", MAX_SUMMARY, False)
                minutes = lesson.get("minutes")
                if not isinstance(minutes, int) or isinstance(minutes, bool) or not 1 <= minutes <= MAX_MINUTES:
                    fail(module_path, f"{where}minutes must be a whole number from 1 to {MAX_MINUTES}")
                file_name = lesson.get("file")
                if not isinstance(file_name, str) or not LESSON_FILE.match(file_name):
                    fail(module_path, f"{where}file must be a .md file next to module.json")
                    continue
                lesson_path = base / file_name
                if slug_ok:
                    first = lesson_slugs.get(lesson["slug"])
                    if first:
                        fail(lesson_path, f"lesson slug {lesson['slug']!r} is already used by {first}")
                    lesson_slugs[lesson["slug"]] = str(lesson_path.relative_to(HERE))

                listed: list[str] = []
                plist = lesson.get("problems")
                if not isinstance(plist, list) or len(plist) > MAX_PROBLEMS:
                    fail(module_path, f"{where}problems must be a list of at most {MAX_PROBLEMS}")
                    plist = []
                for item in plist:
                    if not isinstance(item, dict) or set(item) != {"id", "role"} \
                            or not isinstance(item.get("id"), str) or not PROBLEM_ID.match(item["id"]) \
                            or item.get("role") not in ROLES:
                        fail(module_path, f"{where}problem {item!r} must be {{\"id\", \"role\": example|practice|challenge}}")
                        continue
                    listed.append(item["id"])
                if len(set(listed)) != len(listed):
                    fail(module_path, f"{where}a problem may appear once per lesson")
                for pid in listed:
                    if pid not in problems:
                        fail(module_path, f"{where}problem {pid!r} is not in header-problems/, standard-problems/ or known-problems.txt")

                assets = lesson.get("assets", [])
                if not isinstance(assets, list) or len(assets) > MAX_ASSETS or len(set(map(str, assets))) != len(assets):
                    fail(module_path, f"{where}assets must be at most {MAX_ASSETS} distinct names")
                    assets = []
                asset_names: set[str] = set()
                for name in assets:
                    asset_path = base / "assets" / str(name)
                    if not isinstance(name, str) or not ASSET_NAME.match(name):
                        fail(module_path, f"{where}asset name {name!r} is not allowed")
                        continue
                    expected = ASSET_TYPES.get(name.rsplit(".", 1)[-1].lower())
                    if not expected:
                        fail(asset_path, "only .png, .jpg, .jpeg, .webp and .gif images are allowed")
                    elif not asset_path.is_file():
                        fail(asset_path, "file is missing")
                    elif asset_path.stat().st_size > MAX_ASSET:
                        fail(asset_path, f"is larger than {MAX_ASSET} bytes")
                    elif sniff_image(asset_path.read_bytes()) != expected:
                        fail(asset_path, f"content is not a {expected} image")
                    else:
                        used.add(asset_path)
                        asset_names.add(name)
                        entries.append((f"{track_dir}/{module_dir}/assets/{name}", asset_path))

                if not lesson_path.is_file():
                    fail(lesson_path, "file is missing")
                    continue
                used.add(lesson_path)
                entries.append((f"{track_dir}/{module_dir}/{file_name}", lesson_path))
                raw = lesson_path.read_bytes()
                if len(raw) > MAX_MARKDOWN:
                    fail(lesson_path, f"is larger than {MAX_MARKDOWN} bytes")
                    continue
                try:
                    source = raw.decode("utf-8")
                except UnicodeDecodeError:
                    fail(lesson_path, "is not valid UTF-8")
                    continue
                if "\0" in source:
                    fail(lesson_path, "contains a null byte")
                refs = directive_refs(lesson_path, source)
                unlisted = sorted(set(refs) - set(listed))
                if unlisted:
                    fail(lesson_path, f"problem {', '.join(unlisted)} is used in the lesson but missing from its \"problems\" list")
                for match in re.finditer(r"\]\(assets/([^)\s]+)\)", source):
                    if match.group(1) not in asset_names:
                        fail(lesson_path, f"image assets/{match.group(1)} is not declared in \"assets\"")

    if lesson_count > MAX_LESSONS:
        fail(HERE / "tracks.json", f"{lesson_count} lessons; the limit is {MAX_LESSONS}")

    if not errors:
        content_dirs = [HERE / t for t in tracks if isinstance(t, str)]
        for folder in content_dirs:
            for path in sorted(folder.rglob("*")):
                if path.is_file() and path.name != ".DS_Store" and path not in used:
                    fail(path, "file is not referenced by tracks.json, track.json or module.json")

    if errors or check_only:
        return report(lesson_count)

    DIST.mkdir(exist_ok=True)
    bundle = DIST / "lessons-bundle.zip"
    manifest = {"format": 1, "tracks": tracks}
    commit = source_commit()
    if commit:
        manifest["sourceCommit"] = commit
    with zipfile.ZipFile(bundle, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        for name, path in entries:
            archive.write(path, name)
    if bundle.stat().st_size > MAX_BUNDLE:
        fail(bundle, f"is larger than the {MAX_BUNDLE} byte upload limit")
        return report(lesson_count)
    print(f"wrote {bundle.relative_to(HERE)} ({bundle.stat().st_size} bytes, {lesson_count} lessons"
          f"{', source ' + commit if commit else ''})")
    return 0


def report(lesson_count: int = 0) -> int:
    if errors:
        print(f"{len(errors)} problem(s):", file=sys.stderr)
        for line in errors:
            print(f"  {line}", file=sys.stderr)
        return 1
    print(f"ok: {lesson_count} lessons")
    return 0


if __name__ == "__main__":
    sys.exit(build(check_only="--check" in sys.argv[1:]))
