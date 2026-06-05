#!/usr/bin/env python3
"""
Parse user exam markdown files into set1_questions.json and set2_questions.json.

Place raw exam text in:
  scripts/sources/raw_set1.md  (questions 1-500, first bank)
  scripts/sources/raw_set2.md  (questions 136-500 revised, second bank)

Run: py scripts/parse_user_exam_to_json.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
SOURCES = ROOT / "sources"


def parse_md(text: str) -> list[dict]:
    text = re.sub(r"```[\s\S]*?```", "", text)
    blocks = re.split(r"\n(?=\*\*\d+\.\s)", text)
    out = []
    for block in blocks:
        m = re.match(r"\*\*(\d+)\.\s*(.+?)(?=\n[a-d]\.\s)", block, re.S)
        if not m:
            continue
        num = int(m.group(1))
        question = re.sub(r"\s+", " ", m.group(2).strip())
        opts = {}
        for letter in "abcd":
            om = re.search(rf"^{letter}\.\s*(.+)$", block, re.M)
            if om:
                opts[letter] = om.group(1).strip()
        if len(opts) == 4:
            out.append({"number": num, "question": question, "options": opts})
    out.sort(key=lambda x: x["number"])
    return out


def main():
    SOURCES.mkdir(exist_ok=True)
    raw1 = SOURCES / "raw_set1.md"
    raw2 = SOURCES / "raw_set2.md"

    if raw1.exists():
        q1 = parse_md(raw1.read_text(encoding="utf-8"))
        (SOURCES / "set1_questions.json").write_text(json.dumps(q1, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Set1: {len(q1)} questions -> set1_questions.json")
    else:
        print(f"Missing {raw1}")

    if raw2.exists():
        q2 = parse_md(raw2.read_text(encoding="utf-8"))
        (SOURCES / "set2_questions.json").write_text(json.dumps(q2, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Set2: {len(q2)} questions -> set2_questions.json")
    else:
        print(f"Missing {raw2} (Set 2 will reuse Set 1 text for Q1-135)")


if __name__ == "__main__":
    main()
