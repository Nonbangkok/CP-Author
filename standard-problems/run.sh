#!/usr/bin/env bash
# Driver for the standard-problem harness (stdin/stdout practice problems for
# the Learn lessons). Same throwaway image as header-problems/ -- the judge's
# g++ 14, wkhtmltopdf and Thai fonts -- built from header-problems/Dockerfile.
#
#   ./run.sh build  [--all | <problem-id> ...]
#   ./run.sh verify [--all | <problem-id> ...] [--measure]
#   ./run.sh shell
#
# The repository root is mounted so sp.py can import the shared helpers from
# ../header-problems (harness.py, mdrender.py, statement/).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
IMAGE="${OJ_CONTENT_IMAGE:-oj-content-build}"

if [ "${OJ_CONTENT_REBUILD:-0}" = "1" ] || ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "==> building $IMAGE" >&2
  docker build -t "$IMAGE" "$REPO/header-problems" >&2
fi

if [ "$#" -eq 0 ]; then
  echo "usage: ./run.sh {build|verify|shell} [args...]" >&2
  exit 2
fi

sub="$1"; shift
case "$sub" in
  build)  cmd=(python3 build.py "$@") ;;
  verify) cmd=(python3 verify.py "$@") ;;
  shell)  cmd=(bash) ;;
  *) echo "unknown subcommand '$sub' (expected build|verify|shell)" >&2; exit 2 ;;
esac

exec docker run --rm -i \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp -e XDG_CACHE_HOME=/tmp -e XDG_RUNTIME_DIR=/tmp \
  -e PYTHONDONTWRITEBYTECODE=1 \
  -v "$REPO:/repo" \
  -w /repo/standard-problems \
  "$IMAGE" "${cmd[@]}"
