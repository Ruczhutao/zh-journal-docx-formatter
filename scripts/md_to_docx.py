#!/usr/bin/env python3
"""Render a Markdown manuscript to DOCX using a FormatSpec."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from chinese_paper_formatter.cli import main


if __name__ == "__main__":
    raise SystemExit(main(["md-to-docx"] + sys.argv[1:]))
