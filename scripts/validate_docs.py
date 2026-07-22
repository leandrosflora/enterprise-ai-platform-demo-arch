#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CODE_FENCE_PATTERN = re.compile(r"```.*?```", re.DOTALL)
ADR_FILENAME_PATTERN = re.compile(r"^(?P<id>\d{3})-[a-z0-9-]+\.md$")
ADR_HEADING_PATTERN = re.compile(r"^# ADR-(?P<id>\d{3})\b", re.MULTILINE)


def local_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().split()[0].strip("<>")
    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return None
    return (source.parent / target).resolve()


def is_legacy_adr_target(target: Path) -> bool:
    legacy_dir = (ROOT / "docs/adr").resolve()
    return target == legacy_dir or legacy_dir in target.parents


def validate_adrs(errors: list[str]) -> None:
    legacy_dir = ROOT / "docs/adr"
    canonical_dir = ROOT / "docs/adrs"
    index_path = canonical_dir / "index.md"

    if legacy_dir.exists():
        errors.append("Legacy ADR directory must not exist: docs/adr")

    if not canonical_dir.exists():
        errors.append("Canonical ADR directory missing: docs/adrs")
        return

    if not index_path.exists():
        errors.append("ADR index missing: docs/adrs/index.md")
        return

    index_text = index_path.read_text(encoding="utf-8")
    seen_ids: dict[str, Path] = {}
    adr_files = sorted(path for path in canonical_dir.glob("*.md") if path.name != "index.md")

    if not adr_files:
        errors.append("No canonical ADR files found in docs/adrs")
        return

    for adr_file in adr_files:
        filename_match = ADR_FILENAME_PATTERN.match(adr_file.name)
        if not filename_match:
            errors.append(f"Invalid ADR filename: {adr_file.relative_to(ROOT)}")
            continue

        filename_id = filename_match.group("id")
        text = adr_file.read_text(encoding="utf-8")
        heading_match = ADR_HEADING_PATTERN.search(text)
        if not heading_match:
            errors.append(f"ADR heading missing or invalid: {adr_file.relative_to(ROOT)}")
            continue

        heading_id = heading_match.group("id")
        if filename_id != heading_id:
            errors.append(
                f"ADR ID mismatch: {adr_file.relative_to(ROOT)} uses {filename_id} in filename and {heading_id} in heading"
            )

        previous = seen_ids.get(filename_id)
        if previous is not None:
            errors.append(
                f"Duplicate ADR ID {filename_id}: {previous.relative_to(ROOT)} and {adr_file.relative_to(ROOT)}"
            )
        else:
            seen_ids[filename_id] = adr_file

        if f"({adr_file.name})" not in index_text:
            errors.append(f"ADR missing from index: {adr_file.relative_to(ROOT)}")

    numeric_ids = sorted(int(value) for value in seen_ids)
    if numeric_ids:
        expected_ids = list(range(1, numeric_ids[-1] + 1))
        if numeric_ids != expected_ids:
            formatted = ", ".join(f"{value:03d}" for value in numeric_ids)
            errors.append(f"ADR IDs must be contiguous from 001; found: {formatted}")


def main() -> int:
    errors: list[str] = []
    markdown_files = list(ROOT.rglob("*.md"))

    for source in markdown_files:
        if ".git" in source.parts:
            continue
        text = CODE_FENCE_PATTERN.sub("", source.read_text(encoding="utf-8"))

        for raw_target in LINK_PATTERN.findall(text):
            target = local_target(source, raw_target)
            if target is None:
                continue
            if is_legacy_adr_target(target):
                errors.append(f"Legacy ADR link: {source.relative_to(ROOT)} -> {raw_target}")
            if not target.exists():
                errors.append(f"Broken link: {source.relative_to(ROOT)} -> {raw_target}")

    required_paths = [
        ROOT / "README.md",
        ROOT / "docs/index.md",
        ROOT / "docs/adrs/index.md",
        ROOT / "docs/governance/compliance-crosswalk.md",
        ROOT / "docs/governance/model-lifecycle.md",
        ROOT / "docs/contracts/openapi.yaml",
        ROOT / "docs/contracts/async-api.yaml",
        ROOT / "docs/architecture/control-plane-data-plane.md",
        ROOT / "docs/services/model-gateway.md",
        ROOT / "samples/vertical-slice/docker-compose.yml",
        ROOT / "mkdocs.yml",
    ]
    for path in required_paths:
        if not path.exists():
            errors.append(f"Required artifact missing: {path.relative_to(ROOT)}")

    validate_adrs(errors)

    # Every service cited as a Markdown list item in domain docs must have a page.
    for domain in (ROOT / "docs/domains").glob("*.md"):
        text = domain.read_text(encoding="utf-8")
        for service in re.findall(r"^- ([A-Z][A-Za-z ]+ Service|Agent Gateway|Agent Runtime|MCP Registry)$", text, re.MULTILINE):
            slug = service.lower().replace(" ", "-")
            expected = ROOT / "docs/services" / f"{slug}.md"
            if not expected.exists():
                errors.append(f"Domain {domain.name} references missing service page {expected.name}")

    if errors:
        print("Documentation validation failed:", file=sys.stderr)
        for error in sorted(set(errors)):
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Documentation validation passed ({len(markdown_files)} Markdown files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
