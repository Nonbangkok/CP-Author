#!/usr/bin/env bash
# Lessons for the OJ's Learn section (bundle format 1). Plain Python 3, no Docker.
#
#   ./run.sh check    validate everything, write nothing
#   ./run.sh build    validate, then write dist/lessons-bundle.zip
#
# Import the ZIP in the OJ at Manage > Lessons: the dry run there is the final
# gate (it renders every lesson and checks the problems exist in that grader).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
case "${1:-}" in
  check) exec python3 "$HERE/build.py" --check ;;
  build) exec python3 "$HERE/build.py" ;;
  *) echo "usage: ./run.sh {check|build}" >&2; exit 2 ;;
esac
