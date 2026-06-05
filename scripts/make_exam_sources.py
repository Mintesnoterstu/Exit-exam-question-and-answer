#!/usr/bin/env python3
"""Assemble set1_exam.md and set2_exam.md from section modules."""
from pathlib import Path

SOURCES = Path(__file__).parent / "sources"
SOURCES.mkdir(exist_ok=True)

def main():
    from exam_sections import set1_sections, set2_sections

    set1_md = "\n\n".join(set1_sections())
    set2_md = "\n\n".join(set2_sections())

    (SOURCES / "set1_exam.md").write_text(set1_md, encoding="utf-8")
    (SOURCES / "set2_exam.md").write_text(set2_md, encoding="utf-8")
    print(f"Wrote set1_exam.md ({set1_md.count('**')} questions approx)")
    print(f"Wrote set2_exam.md ({set2_md.count('**')} questions approx)")

if __name__ == "__main__":
    main()
