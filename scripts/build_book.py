#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK_DIR = ROOT / "docs" / "book"
OUTPUT_DIR = ROOT / "build" / "book"
OUTPUT_PATH = OUTPUT_DIR / "enterprise-ai-platform-book.md"

FRONT_MATTER = "index.md"
CHAPTERS = [
    "01-why-ai-platform.md",
    "02-capability-map.md",
    "03-operating-model.md",
    "04-agent-lifecycle.md",
    "05-case-study-document-agent.md",
    "06-decision-guides.md",
    "07-adoption-roadmap.md",
    "08-production-checklists.md",
    "glossary.md",
]
SUMMARY = [
    "1. Por que uma AI Platform?",
    "2. Capability Map",
    "3. Operating Model",
    "4. Ciclo de vida de agentes",
    "5. Estudo de caso: agente documental com RAG",
    "6. Decision Guides",
    "7. Modelo de maturidade e roadmap de adoção",
    "8. Checklists de produção",
    "9. Glossário",
]

LOCAL_MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\((?!https?://|mailto:|#)([^)]+\.md(?:#[^)]+)?)\)")


def git_revision() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def book_files() -> list[str]:
    return [FRONT_MATTER, *CHAPTERS]


def validate() -> list[str]:
    errors: list[str] = []
    for chapter in book_files():
        path = BOOK_DIR / chapter
        if not path.exists():
            errors.append(f"Missing book chapter: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if not text.startswith("# "):
            errors.append(f"Chapter must start with H1: {path.relative_to(ROOT)}")
        if len(text.split()) < 80:
            errors.append(f"Chapter is unexpectedly short: {path.relative_to(ROOT)}")
    if len(SUMMARY) != len(CHAPTERS):
        errors.append("Summary and chapter manifest must contain the same number of items")
    return errors


def web_link(source: Path, label: str, raw_target: str) -> str:
    target, separator, fragment = raw_target.partition("#")
    resolved = (source.parent / target).resolve()
    try:
        relative = resolved.relative_to(ROOT / "docs")
    except ValueError:
        try:
            relative = resolved.relative_to(ROOT)
            url = f"https://github.com/leandrosflora/enterprise-ai-platform-demo-arch/blob/main/{relative.as_posix()}"
        except ValueError:
            return f"[{label}]({raw_target})"
    else:
        clean = relative.with_suffix("").as_posix()
        url = f"https://leandrosflora.github.io/enterprise-ai-platform-demo-arch/{clean}/"
    if separator and fragment:
        url = f"{url}#{fragment}"
    return f"[{label}]({url})"


def normalize_links(source: Path, text: str) -> str:
    return LOCAL_MARKDOWN_LINK.sub(
        lambda match: web_link(source, match.group(1), match.group(2)),
        text,
    )


def as_front_matter(path: Path) -> str:
    text = normalize_links(path, path.read_text(encoding="utf-8").strip())
    return text.replace(
        "# Enterprise AI Platform Book",
        '<h1 class="unnumbered">Como ler este livro</h1>',
        1,
    )


def build() -> None:
    generated_at = datetime.now(UTC).strftime("%Y-%m-%d")
    revision = git_revision()
    parts = [
        "---",
        'lang: "pt-BR"',
        'pagetitle: "Enterprise AI Platform Book"',
        "---",
        "",
        '<div class="title-page">',
        "",
        "<h1>Enterprise AI Platform Book</h1>",
        "",
        "Estratégia, arquitetura, governança e operação",
        "",
        "Leandro Silva Flora",
        "",
        f"Revisão `{revision}` - {generated_at}",
        "",
        "Arquitetura de referência acompanhada por contratos, policies e vertical slice executável.",
        "",
        "</div>",
        "",
        '<h1 class="unnumbered">Sumário</h1>',
        "",
        '<div class="book-summary">',
        "",
        *SUMMARY,
        "",
        "</div>",
        "",
        '<div class="page-break"></div>',
        "",
        as_front_matter(BOOK_DIR / FRONT_MATTER),
        "",
        '<div class="page-break"></div>',
        "",
    ]

    for index, chapter in enumerate(CHAPTERS):
        path = BOOK_DIR / chapter
        text = normalize_links(path, path.read_text(encoding="utf-8").strip())
        parts.append(text)
        if index < len(CHAPTERS) - 1:
            parts.extend(["", '<div class="page-break"></div>', ""])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"Book manuscript generated: {OUTPUT_PATH.relative_to(ROOT)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate or build the consolidated AI Platform book")
    parser.add_argument("--check", action="store_true", help="Validate the chapter manifest without writing output")
    args = parser.parse_args()

    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    if args.check:
        print(f"Book manifest validation passed ({len(book_files())} files)")
        return 0

    build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
