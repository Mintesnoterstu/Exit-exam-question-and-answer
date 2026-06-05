#!/usr/bin/env python3
"""
Build Set 1 and Set 2 (500 each) using:
1. Official separate answer keys
2. User-provided question text from raw_set1_sec*.md / raw_set2_sec*.md
3. Legacy question bank as fallback, with option remapping when answer keys differ
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from answer_keys import SET1_ANSWERS, SET2_ANSWERS
from build_official_banks import (
    build_explanation,
    lookup_meta,
    parse_exam_markdown,
)

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
SOURCES = Path(__file__).parent / "sources"


def load_parsed(prefix: str) -> dict[int, dict]:
    out: dict[int, dict] = {}
    for path in sorted(SOURCES.glob(f"{prefix}_sec*.md")):
        out.update(parse_exam_markdown(path.read_text(encoding="utf-8")))
    p = SOURCES / f"{prefix}.md"
    if p.exists():
        out.update(parse_exam_markdown(p.read_text(encoding="utf-8")))
    return out


def load_legacy() -> list[dict]:
    p = DATA / "questions.json"
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8")).get("questions", [])[:500]


def remap_options(opts: dict[str, str], old_correct: str, new_correct: str) -> dict[str, str]:
    old_correct = old_correct.upper()
    new_correct = new_correct.upper()
    if old_correct == new_correct:
        return dict(opts)
    result = dict(opts)
    result[old_correct], result[new_correct] = result[new_correct], result[old_correct]
    return result


def build_set(bank_id: str, answers: dict[int, str], user_parsed: dict[int, dict], legacy: list[dict]) -> list[dict]:
    questions = []
    for num in range(1, 501):
        official = answers[num].upper()
        pdata = user_parsed.get(num)

        if pdata:
            question = pdata["question"]
            opts_lower = pdata["options"]
            opts = {k.upper(): v for k, v in opts_lower.items()}
            correct = official
        elif num <= len(legacy):
            leg = legacy[num - 1]
            question = leg["question"]
            opts = {k.upper(): v for k, v in leg["options"].items()}
            old_c = leg["correct"].upper()
            opts = remap_options(opts, old_c, official)
            correct = official
        else:
            theme_id, course_id, difficulty, chapter = lookup_meta(num, bank_id)
            question = f"[{chapter}] Select the best answer for official exit exam item #{num}."
            opts = {L: f"Option {L} — {chapter}" for L in "ABCD"}
            opts[official] = f"Correct answer for item #{num} per official key."
            correct = official

        theme_id, course_id, difficulty, chapter = lookup_meta(num, bank_id)
        exp = build_explanation(
            num, question, correct.lower(), {k.lower(): v for k, v in opts.items()}, course_id,
            pdata.get("code") if pdata else None,
        )

        item = {
            "id": f"{bank_id.upper()}-Q{num:03d}",
            "bankId": bank_id,
            "number": num,
            "courseId": course_id,
            "themeId": theme_id,
            "chapter": chapter,
            "difficulty": difficulty,
            "cognitive": "understand" if difficulty == "easy" else "apply" if difficulty == "medium" else "analyze",
            "question": question,
            "options": opts,
            "correct": correct,
            "explanation": exp,
        }
        if pdata and pdata.get("code"):
            item["code"] = pdata["code"]
        questions.append(item)
    return questions


def main():
    user1 = load_parsed("raw_set1")
    user2 = load_parsed("raw_set2")
    legacy = load_legacy()

    bank1 = build_set("set1", SET1_ANSWERS, user1, legacy)
    bank2 = build_set("set2", SET2_ANSWERS, {**user1, **user2}, legacy)

    (DATA / "questions-set1.json").write_text(json.dumps({
        "bankId": "set1",
        "title": "Official Exit Exam Bank — Set 1 (500 Questions)",
        "description": "MoE blueprint weights. Official answer key Set 1. User-provided stems where uploaded.",
        "count": 500,
        "questions": bank1,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    (DATA / "questions-set2.json").write_text(json.dumps({
        "bankId": "set2",
        "title": "Official Exit Exam Bank — Set 2 (500 Questions)",
        "description": "Alternate exam. Official answer key Set 2 — kept separate from Set 1.",
        "count": 500,
        "questions": bank2,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    version = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    (DATA / "questions-index.json").write_text(json.dumps({
        "version": version,
        "banks": [
            {"id": "set1", "file": "questions-set1.json", "title": "Question Bank Set 1", "count": 500},
            {"id": "set2", "file": "questions-set2.json", "title": "Question Bank Set 2", "count": 500},
        ],
        "total": 1000,
    }, indent=2), encoding="utf-8")
    print(f"Data version: {version}")

    print(f"User text Set1: {len(user1)}, Set2 extra: {len(user2)}")
    print("Built questions-set1.json and questions-set2.json (500 each)")


if __name__ == "__main__":
    main()
