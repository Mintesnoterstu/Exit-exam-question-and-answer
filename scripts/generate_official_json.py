#!/usr/bin/env python3
"""Generate set1_questions.json and set2_questions.json from official_q_banks module."""
import json
from pathlib import Path

from official_q_banks import SET1_QUESTIONS, SET2_QUESTIONS

SOURCES = Path(__file__).parent / "sources"
SOURCES.mkdir(exist_ok=True)

(SOURCES / "set1_questions.json").write_text(
    json.dumps(SET1_QUESTIONS, ensure_ascii=False, indent=2), encoding="utf-8"
)
(SOURCES / "set2_questions.json").write_text(
    json.dumps(SET2_QUESTIONS, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"Set1: {len(SET1_QUESTIONS)} questions")
print(f"Set2: {len(SET2_QUESTIONS)} questions")
