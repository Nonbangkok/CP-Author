#!/usr/bin/env python3
"""Verify built standard problems against the contract (run after build).

    ./run.sh verify --all [--measure]
    ./run.sh verify lp_bsa01_count_range

Every problem must satisfy:

  1. dist/<id>/ matches meta.json (config.json, the PDF, 10 testcase pairs).
  2. solution.cpp still prints every statement example (built from samples/).
  3. solution.cpp is Accepted on all 10 cases under the REAL time limit.
  4. solution.py, when present, is Accepted on all 10 cases under the judge's
     Python limit (time x4).
  5. when has_tle_subtask: slow.cpp is Accepted on every case before the last
     subtask and times out on the first case of the last subtask -- so the
     complexity the statement promises is proven by the cases, not asserted.
"""

from __future__ import annotations

import argparse
import json
import sys

import sp
from sp import HarnessError, Meta, hh

MEASURE_LIMIT_MS = 30_000


class Report:
    def __init__(self, problem_id: str) -> None:
        self.problem_id = problem_id
        self.rows: list[tuple[str, bool, str]] = []

    def record(self, name: str, ok: bool, detail: str = "") -> bool:
        self.rows.append((name, ok, detail))
        return ok

    @property
    def ok(self) -> bool:
        return all(ok for _, ok, _ in self.rows)

    def render(self) -> str:
        lines = [f"== {self.problem_id}"]
        for name, ok, detail in self.rows:
            lines.append(f"  [{'ok' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))
        return "\n".join(lines)


def check_layout(meta: Meta, report: Report) -> bool:
    input_dir, output_dir = sp.case_paths(meta)
    config_path = meta.dist_dir / "config.json"
    if not config_path.is_file():
        return report.record("built", False, "dist/<id>/ is missing — run ./run.sh build first")
    config = json.loads(config_path.read_text(encoding="utf-8"))
    mismatch = [key for key, value in (("title", meta.title), ("time_limit_ms", meta.time_limit_ms),
                                       ("memory_limit_mb", meta.memory_limit_mb), ("problem_type", "standard"))
                if config.get(key) != value]
    pdf = meta.dist_dir / f"{meta.id}.pdf"
    pairs = all((input_dir / hh.case_input_name(i)).is_file() and (output_dir / hh.case_output_name(i)).is_file()
                for i in range(1, sp.TESTCASE_COUNT + 1))
    ok = not mismatch and pdf.is_file() and pdf.read_bytes()[:4] == b"%PDF" and pairs
    detail = "" if ok else f"stale build (config differs in {mismatch or '-'}, pdf {pdf.is_file()}, testcases {pairs})"
    return report.record("dist matches meta.json", ok, detail)


def run_cases(meta: Meta, workspace, binary: str, limit_ms: int, name: str) -> tuple[int | None, str, float]:
    """Run every case; return (first failing case or None, its verdict, slowest wall ms)."""
    input_dir, output_dir = sp.case_paths(meta)
    slowest = 0.0
    for index in range(1, sp.TESTCASE_COUNT + 1):
        out = workspace / f"{name}{index:02d}.out"
        result = hh.run_program(workspace, binary, input_dir / hh.case_input_name(index), limit_ms,
                                out, workspace / f"{name}{index:02d}.err")
        slowest = max(slowest, result.wall_ms)
        if result.timed_out:
            return index, "Time Limit Exceeded", slowest
        if result.exit_code != 0:
            return index, f"Runtime Error (exit {result.exit_code})", slowest
        expected = (output_dir / hh.case_output_name(index)).read_text(encoding="utf-8")
        if not hh.outputs_match(out.read_text(encoding="utf-8", errors="replace"), expected):
            return index, "Wrong Answer", slowest
    return None, "Accepted", slowest


def check_samples(meta: Meta, report: Report) -> bool:
    workspace = meta.work_dir / "verify-sample"
    sp.compile_cpp(meta, meta.source_dir / "solution.cpp", workspace)
    number = 1
    while (meta.work_dir / f"sample{number}.in").is_file():
        out = workspace / f"sample{number}.txt"
        result = hh.run_program(workspace, sp.BINARY_NAME, meta.work_dir / f"sample{number}.in", 10_000,
                                out, workspace / f"sample{number}.err")
        expected = (meta.work_dir / f"sample{number}.out").read_text(encoding="utf-8")
        if result.exit_code != 0 or not hh.outputs_match(out.read_text(encoding="utf-8", errors="replace"), expected):
            return report.record("solution.cpp prints the statement's samples", False, f"sample {number} differs")
        number += 1
    return report.record("solution.cpp prints the statement's samples", number > 1, f"{number - 1} sample(s)")


def check_reference(meta: Meta, report: Report) -> bool:
    workspace = meta.work_dir / "verify-reference"
    sp.compile_cpp(meta, meta.source_dir / "solution.cpp", workspace)
    failure, verdict, slowest = run_cases(meta, workspace, sp.BINARY_NAME, meta.time_limit_ms, "ref")
    detail = f"slowest {slowest:.0f} ms of {meta.time_limit_ms} ms" if failure is None else f"case {failure}: {verdict}"
    return report.record("solution.cpp Accepted on all cases", failure is None, detail)


def check_python(meta: Meta, report: Report) -> bool:
    if not meta.has_python:
        return report.record("solution.py", True, "none (C++ only reference)")
    workspace = meta.work_dir / "verify-python"
    runner = sp.prepare_python(meta, meta.source_dir / "solution.py", workspace)
    limit = meta.time_limit_ms * sp.PYTHON_TIME_MULTIPLIER
    failure, verdict, slowest = run_cases(meta, workspace, runner, limit, "py")
    detail = f"slowest {slowest:.0f} ms of {limit} ms" if failure is None else f"case {failure}: {verdict}"
    return report.record("solution.py Accepted on all cases (time x4)", failure is None, detail)


def check_slow(meta: Meta, report: Report, measure: bool) -> bool:
    label = "slow.cpp passes the earlier subtasks and TLEs at the last one"
    if not meta.has_tle_subtask:
        return report.record(label, True, "skipped (no complexity subtask)")
    workspace = meta.work_dir / "verify-slow"
    sp.compile_cpp(meta, meta.source_dir / "slow.cpp", workspace)
    boundary = sum(s.cases for s in meta.subtasks[:-1])
    failure, verdict, _ = run_cases(meta, workspace, sp.BINARY_NAME, meta.time_limit_ms, "slow")
    ok = failure == boundary + 1 and verdict == "Time Limit Exceeded"
    detail = f"first failure: case {failure} ({verdict}); expected case {boundary + 1} (Time Limit Exceeded)"
    if ok and measure:
        input_dir, _ = sp.case_paths(meta)
        result = hh.run_program(workspace, sp.BINARY_NAME, input_dir / hh.case_input_name(sp.TESTCASE_COUNT),
                                MEASURE_LIMIT_MS, workspace / "measure.out", workspace / "measure.err")
        factor = "> 30 s" if result.timed_out else f"{result.wall_ms / meta.time_limit_ms:.1f}x the limit"
        detail += f"; last case takes {factor}"
    return report.record(label, ok, detail)


def verify_problem(problem_dir, measure: bool) -> Report:
    meta = sp.load_meta(problem_dir)
    report = Report(meta.id)
    if not check_layout(meta, report):
        return report
    check_samples(meta, report)
    check_reference(meta, report)
    check_python(meta, report)
    check_slow(meta, report, measure)
    return report


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Verify built standard problems.")
    parser.add_argument("problems", nargs="*")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--measure", action="store_true", help="also measure how slow slow.cpp really is")
    args = parser.parse_args(argv)
    try:
        hh.require_container()
        reports = [verify_problem(d, args.measure) for d in sp.resolve_problem_dirs([] if args.all else args.problems)]
    except HarnessError as error:
        print(f"\nVERIFY FAILED: {error}", file=sys.stderr)
        return 1
    for report in reports:
        print(report.render())
    failed = [r.problem_id for r in reports if not r.ok]
    print(f"\n{len(reports) - len(failed)}/{len(reports)} problem(s) verified" + (f"; FAILED: {', '.join(failed)}" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
