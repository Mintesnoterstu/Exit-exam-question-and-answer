#!/usr/bin/env python3
"""Extract Set 1 and Set 2 exam markdown from agent transcript user message."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
TRANSCRIPT = Path(
    r"C:\Users\hp\.cursor\projects\c-Users-hp-Desktop-Class-Files-4th-year-Exit-question-website-Exit-exam-question-and-answer\agent-transcripts\178266d0-54ad-4bb3-827b-861c92f4223f\178266d0-54ad-4bb3-827b-861c92f4223f.jsonl"
)
OUT = Path(__file__).parent / "sources"


def load_user_exam_text() -> str:
    for line in TRANSCRIPT.read_text(encoding="utf-8").splitlines():
        obj = json.loads(line)
        if obj.get("role") != "user":
            continue
        parts = obj.get("message", {}).get("content", [])
        for p in parts:
            if p.get("type") == "text" and "**1. Which phase of the SDLC" in p.get("text", ""):
                text = p["text"]
                # strip outer quotes if present
                if text.startswith('"') and text.endswith('"'):
                    text = text[1:-1]
                return text
    raise RuntimeError("Exam text not found in transcript")


def extract_questions_block(text: str, start_marker: str, end_marker: str | None) -> str:
    start = text.find(start_marker)
    if start < 0:
        return ""
    if end_marker:
        end = text.find(end_marker, start)
        if end < 0:
            end = len(text)
        return text[start:end]
    return text[start:]


def clean_to_questions_only(block: str) -> str:
    """Keep **N. question**, fenced code blocks, and a./b./c./d. option lines."""
    sections: list[str] = []
    current: list[str] = []
    in_code = False

    for line in block.splitlines():
        stripped = line.strip()
        if re.match(r"^\*\*\d+\.\s", stripped):
            if current:
                sections.append("\n".join(current))
            current = [stripped]
            in_code = False
            continue
        if re.match(r"^[a-d]\.\s", stripped):
            in_code = False
            current.append(stripped)
            continue
        if stripped.startswith("```"):
            in_code = not in_code
            current.append(line.rstrip())
            continue
        if in_code:
            current.append(line.rstrip())

    if current:
        sections.append("\n".join(current))
    return "\n\n".join(sections) + "\n"


def main():
    text = load_user_exam_text()

    # Set 1: from first Q1 through before Set 2 marker
    set2_start = text.find("Here is the continuation of the **500-question exit exam (Set 2)**")
    if set2_start < 0:
        set2_start = text.find("# SECTION 2: PROGRAMMING AND ALGORITHMS (125 Questions)\n\n## Theme Weight: 25% | Difficulty: Easy (19)")
        # fallback: second occurrence of section 2 with different difficulty
        idx = text.find("Difficulty: Easy (19), Medium (44), Hard (62)")
        if idx > 0:
            set2_start = text.rfind("# SECTION 2:", 0, idx)

    set1_block = text[:set2_start] if set2_start > 0 else text
    set1_q = clean_to_questions_only(set1_block)

    set2_block = text[set2_start:] if set2_start > 0 else ""
    set2_q = clean_to_questions_only(set2_block)

    OUT.mkdir(exist_ok=True)
    (OUT / "raw_set1.md").write_text(set1_q, encoding="utf-8")
    (OUT / "raw_set2.md").write_text(set2_q, encoding="utf-8")

    from build_official_banks import parse_exam_markdown

    p1 = parse_exam_markdown(set1_q)
    p2 = parse_exam_markdown(set2_q)
    print(f"Wrote raw_set1.md ({len(p1)} questions) and raw_set2.md ({len(p2)} questions)")


if __name__ == "__main__":
    main()
