#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CODE_FENCE_PATTERN = re.compile(r"```.*?```", re.DOTALL)


def local_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().split()[0].strip("<>")
    if not target or target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return None
    return (source.parent / target).resolve()


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
            if not target.exists():
                errors.append(f"Broken link: {source.relative_to(ROOT)} -> {raw_target}")

    required_paths = [
        ROOT / "README.md",
        ROOT / "docs/index.md",
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
