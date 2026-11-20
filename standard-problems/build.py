#!/usr/bin/env python3
"""Build standard problems into the OJ batch-upload layout.

    ./run.sh build --all
    ./run.sh build lp_bsa01_count_range [...]

For each problem: render statement.md to <id>.pdf (and prove the Thai and the
math survived into the PDF's text), run gen.py for the 10 inputs, compile
solution.cpp with the judge's flags and RUN it to produce every expected
output (outputs are never written by hand), then write dist/<id>/ and
rewrite dist/standard-problems.zip from everything in dist/.

Import layout (backend/services/batchUploadService.ts):

    <id>/config.json          problem_type "standard"
    <id>/<id>.pdf
    <id>/testcases/input/inputNN.txt
    <id>/testcases/output/outputNN.txt
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import zipfile

import sp
from sp import HarnessError, Meta, hh

REFERENCE_TIMEOUT_MS_MIN = 20_000
REFERENCE_TIME_WARN_FRACTION = 0.5


def generate_inputs(meta: Meta) -> None:
    input_dir, _ = sp.case_paths(meta)
    hh.reset_dir(input_dir)
    completed = subprocess.run([sys.executable, "gen.py", str(input_dir.resolve())], cwd=meta.source_dir,
                               capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        raise HarnessError(f"{meta.id}: gen.py failed (exit {completed.returncode}): "
                           f"{(completed.stderr or completed.stdout).strip()[:800]}")
    expected = {hh.case_input_name(i) for i in range(1, sp.TESTCASE_COUNT + 1)}
    found = {p.name for p in input_dir.iterdir()}
    if found != expected:
        raise HarnessError(f"{meta.id}: gen.py must write exactly input01.txt..input{sp.TESTCASE_COUNT:02d}.txt "
                           f"(missing {sorted(expected - found)}, extra {sorted(found - expected)})")


def build_outputs(meta: Meta) -> list[dict]:
    input_dir, output_dir = sp.case_paths(meta)
    workspace = meta.work_dir / "reference"
    sp.compile_cpp(meta, meta.source_dir / "solution.cpp", workspace)
    hh.reset_dir(output_dir)
    timeout_ms = max(meta.time_limit_ms * 10, REFERENCE_TIMEOUT_MS_MIN)
    measurements = []
    for index in range(1, sp.TESTCASE_COUNT + 1):
        input_path = input_dir / hh.case_input_name(index)
        output_path = output_dir / hh.case_output_name(index)
        result = hh.run_program(workspace, sp.BINARY_NAME, input_path, timeout_ms, output_path,
                                workspace / f"stderr{index:02d}.txt")
        if result.timed_out:
            raise HarnessError(f"{meta.id}: the reference timed out on case {index} after {timeout_ms} ms")
        if result.exit_code != 0:
            stderr = result.stderr_path.read_text(encoding="utf-8", errors="replace").strip()
            raise HarnessError(f"{meta.id}: the reference exited {result.exit_code} on case {index}: {stderr[:600]}")
        if output_path.stat().st_size == 0:
            raise HarnessError(f"{meta.id}: the reference produced no output on case {index}")
        measurements.append({
            "case": index, "wall_ms": round(result.wall_ms, 1), "max_rss_mb": round(result.max_rss_mb, 1),
            "input_bytes": input_path.stat().st_size, "output_bytes": output_path.stat().st_size,
        })
    return measurements


def write_config(meta: Meta) -> None:
    config = {
        "id": meta.id,
        "title": meta.title,
        "author": meta.author,
        "time_limit_ms": meta.time_limit_ms,
        "memory_limit_mb": meta.memory_limit_mb,
        "categories": meta.categories,
        "difficulty": meta.difficulty,
        "collection": meta.collection,
        "problem_type": "standard",
    }
    hh.write_text(meta.dist_dir / "config.json", json.dumps(config, ensure_ascii=False, indent=2) + "\n")


def build_problem(problem_dir) -> dict:
    meta = sp.load_meta(problem_dir)
    print(f"==> {meta.id}")
    started = time.monotonic()
    hh.reset_dir(meta.work_dir)
    hh.reset_dir(meta.dist_dir)

    markdown = sp.assemble_statement_markdown(meta)
    samples_in = sp.mdrender.extract_fenced(markdown, "sample-input")
    samples_out = sp.mdrender.extract_fenced(markdown, "sample-output")
    if not samples_in or len(samples_in) != len(samples_out):
        raise HarnessError(f"{meta.id}: statement.md needs matching ```sample-input / ```sample-output pairs "
                           f"(found {len(samples_in)} and {len(samples_out)})")
    for number, (sample_in, sample_out) in enumerate(zip(samples_in, samples_out), start=1):
        hh.write_text(meta.work_dir / f"sample{number}.in", sample_in.rstrip("\n") + "\n")
        hh.write_text(meta.work_dir / f"sample{number}.out", sample_out.rstrip("\n") + "\n")

    html_path = meta.work_dir / "statement.html"
    hh.write_text(html_path, sp.statement_html(meta, markdown))
    pdf_path = meta.dist_dir / f"{meta.id}.pdf"
    sp.render_pdf(meta, html_path, pdf_path)
    thai_probe, math_probe = sp.assert_statement_survived(meta, pdf_path, markdown)
    print(f"    statement.pdf  {hh.human_bytes(pdf_path.stat().st_size)}  "
          f"(Thai \"{thai_probe}\" and math \"{math_probe}\" found in the PDF text)")

    generate_inputs(meta)
    measurements = build_outputs(meta)
    write_config(meta)

    slowest = max(measurements, key=lambda entry: entry["wall_ms"])
    testcase_bytes = sum(entry["input_bytes"] + entry["output_bytes"] for entry in measurements)
    summary = {"id": meta.id, "built_in_s": round(time.monotonic() - started, 1), "cases": measurements}
    hh.write_text(meta.work_dir / "build.json", json.dumps(summary, indent=2) + "\n")
    print(f"    testcases      {sp.TESTCASE_COUNT} cases, {hh.human_bytes(testcase_bytes)}")
    print(f"    reference      slowest case {slowest['case']}: {slowest['wall_ms']:.0f} ms of {meta.time_limit_ms} ms, "
          f"peak {max(e['max_rss_mb'] for e in measurements):.0f} MB of {meta.memory_limit_mb} MB")
    if slowest["wall_ms"] > meta.time_limit_ms * REFERENCE_TIME_WARN_FRACTION:
        print("    WARNING: the reference uses more than half the time limit on this machine")
    if testcase_bytes > hh.TESTCASE_BYTES_BUDGET:
        print(f"    WARNING: {hh.human_bytes(testcase_bytes)} of testcases exceeds the per-problem budget")
    return summary


def write_zip() -> None:
    archive = sp.DIST_DIR / sp.ZIP_NAME
    built = sorted(p for p in sp.DIST_DIR.iterdir()
                   if p.is_dir() and not p.name.startswith(".") and (p / "config.json").is_file())
    if not built:
        raise HarnessError("nothing to zip: dist/ has no built problem")
    archive.unlink(missing_ok=True)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for problem in built:
            for path in sorted(problem.rglob("*")):
                if path.is_file():
                    zip_file.write(path, path.relative_to(sp.DIST_DIR).as_posix())
    print(f"==> dist/{sp.ZIP_NAME}  {hh.human_bytes(archive.stat().st_size)}  "
          f"({len(built)} problem(s): {', '.join(p.name for p in built)})")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Build standard problems into the batch-upload layout.")
    parser.add_argument("problems", nargs="*")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args(argv)
    try:
        hh.require_container()
        sp.DIST_DIR.mkdir(parents=True, exist_ok=True)
        sp.WORK_DIR.mkdir(parents=True, exist_ok=True)
        for problem_dir in sp.resolve_problem_dirs([] if args.all else args.problems):
            build_problem(problem_dir)
        write_zip()
    except HarnessError as error:
        print(f"\nBUILD FAILED: {error}", file=sys.stderr)
        return 1
    print("\nbuild ok")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
