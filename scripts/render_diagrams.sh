#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mapfile -d '' diagrams < <(find "$ROOT/docs" -name '*.puml' -print0 | sort -z)

if (( ${#diagrams[@]} == 0 )); then
  echo "No PlantUML diagrams found" >&2
  exit 1
fi

if command -v plantuml >/dev/null 2>&1; then
  plantuml -checkonly "${diagrams[@]}"
  exit 0
fi

if command -v docker >/dev/null 2>&1; then
  relative=()
  for diagram in "${diagrams[@]}"; do
    relative+=("${diagram#"$ROOT/"}")
  done
  docker run --rm -v "$ROOT:/work" -w /work plantuml/plantuml:1.2026.4 -checkonly "${relative[@]}"
  exit 0
fi

echo "PlantUML or Docker is required" >&2
exit 1
