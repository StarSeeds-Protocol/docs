#!/usr/bin/env python3
"""Double-check the content of the built PDF against the Markdown sources.

Extracts the text of every heading and paragraph from the Markdown sources
and verifies each one appears in the text extracted from the PDF. Fails with
a non-zero exit code (listing the missing content) if anything is absent.

Usage:
    python3 scripts/check_pdf.py [--pdf build/docs.pdf]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from pypdf import PdfReader

REPO_ROOT = Path(__file__).resolve().parent.parent

# Reuse the same source discovery as the build so both stay in sync.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_pdf import collect_sources  # noqa: E402


def normalize(text: str) -> str:
    """Collapse whitespace so line wrapping in the PDF doesn't cause misses."""
    return re.sub(r"\s+", " ", text).strip().lower()


def markdown_fragments(path: Path) -> list[str]:
    """Extract checkable plain-text fragments from a Markdown file."""
    fragments: list[str] = []
    text = path.read_text(encoding="utf-8")
    # Drop fenced code blocks: PDF text extraction of code is unreliable.
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block:
            continue
        # Strip common Markdown syntax down to plain text.
        block = re.sub(r"^#{1,6}\s*", "", block, flags=re.MULTILINE)  # headings
        block = re.sub(r"^\s*[-*+]\s+", "", block, flags=re.MULTILINE)  # bullets
        block = re.sub(r"^\s*\d+\.\s+", "", block, flags=re.MULTILINE)  # numbered
        block = re.sub(r"^\s*>\s?", "", block, flags=re.MULTILINE)  # blockquotes
        block = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", block)  # images
        block = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", block)  # links
        block = re.sub(r"[*_`]{1,3}", "", block)  # emphasis / inline code
        block = re.sub(r"^\s*\|.*\|\s*$", "", block, flags=re.MULTILINE)  # tables
        block = re.sub(r"^[-=\s|:]+$", "", block, flags=re.MULTILINE)  # rules
        fragment = normalize(block)
        if fragment:
            fragments.append(fragment)
    return fragments


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pdf",
        type=Path,
        default=REPO_ROOT / "build" / "docs.pdf",
        help="Path of the PDF to check (default: build/docs.pdf)",
    )
    args = parser.parse_args()

    if not args.pdf.is_file():
        print(f"error: {args.pdf} not found; run scripts/build_pdf.py first", file=sys.stderr)
        return 1

    reader = PdfReader(str(args.pdf))
    pdf_text = normalize(" ".join(page.extract_text() or "" for page in reader.pages))
    if not pdf_text:
        print("error: no text could be extracted from the PDF", file=sys.stderr)
        return 1

    missing: list[tuple[Path, str]] = []
    checked = 0
    for source in collect_sources(REPO_ROOT):
        for fragment in markdown_fragments(source):
            checked += 1
            if fragment not in pdf_text:
                missing.append((source, fragment))

    print(f"Checked {checked} content fragment(s) across {len(reader.pages)} PDF page(s).")
    if missing:
        print(f"\nFAIL: {len(missing)} fragment(s) missing from the PDF:", file=sys.stderr)
        for source, fragment in missing:
            preview = fragment if len(fragment) <= 100 else fragment[:97] + "..."
            print(f"  - [{source.relative_to(REPO_ROOT)}] {preview}", file=sys.stderr)
        return 1

    print("OK: all Markdown content is present in the PDF.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
