#!/usr/bin/env python3
"""Build a single PDF from the Markdown documentation in this repository.

Collects README.md plus every Markdown file under docs/ (if present),
converts them to HTML, and renders the result to build/docs.pdf.

Usage:
    python3 scripts/build_pdf.py [--output build/docs.pdf]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import markdown
from weasyprint import HTML

REPO_ROOT = Path(__file__).resolve().parent.parent

CSS = """
@page {
    size: A4;
    margin: 2.2cm 1.8cm;
    @bottom-center {
        content: counter(page) " / " counter(pages);
        font-size: 9pt;
        color: #666;
    }
}
body {
    font-family: sans-serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #222;
}
h1, h2, h3, h4 { color: #111; page-break-after: avoid; }
h1 { border-bottom: 2px solid #444; padding-bottom: 4px; }
pre, code {
    font-family: monospace;
    background: #f4f4f4;
    border-radius: 3px;
}
pre { padding: 8px; white-space: pre-wrap; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #999; padding: 4px 8px; text-align: left; }
blockquote { border-left: 3px solid #bbb; margin-left: 0; padding-left: 12px; color: #555; }
section.doc-file { page-break-before: always; }
section.doc-file:first-of-type { page-break-before: avoid; }
"""


def collect_sources(root: Path) -> list[Path]:
    """Return Markdown files to include, in a stable, predictable order."""
    sources: list[Path] = []
    readme = root / "README.md"
    if readme.is_file():
        sources.append(readme)
    docs_dir = root / "docs"
    if docs_dir.is_dir():
        sources.extend(sorted(docs_dir.rglob("*.md")))
    # Any other top-level Markdown files, excluding the README already added.
    for path in sorted(root.glob("*.md")):
        if path not in sources:
            sources.append(path)
    return sources


def render_html(sources: list[Path]) -> str:
    md = markdown.Markdown(extensions=["extra", "toc", "sane_lists"])
    sections = []
    for path in sources:
        body = md.reset().convert(path.read_text(encoding="utf-8"))
        rel = path.relative_to(REPO_ROOT)
        sections.append(f'<section class="doc-file" data-source="{rel}">{body}</section>')
    joined = "\n".join(sections)
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<style>{CSS}</style></head><body>{joined}</body></html>"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "build" / "docs.pdf",
        help="Path of the PDF to write (default: build/docs.pdf)",
    )
    args = parser.parse_args()

    sources = collect_sources(REPO_ROOT)
    if not sources:
        print("error: no Markdown sources found to build", file=sys.stderr)
        return 1

    print("Building PDF from:")
    for path in sources:
        print(f"  - {path.relative_to(REPO_ROOT)}")

    html = render_html(sources)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html, base_url=str(REPO_ROOT)).write_pdf(str(args.output))
    size = args.output.stat().st_size
    print(f"Wrote {args.output.relative_to(REPO_ROOT)} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
