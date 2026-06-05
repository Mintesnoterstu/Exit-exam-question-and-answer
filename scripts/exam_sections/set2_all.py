"""Set 2 exam questions — Q1-135 share text with Set 1; Q136-500 from set2 JSON."""

import json
from pathlib import Path

_SET1 = Path(__file__).parent.parent / "sources" / "set1_questions.json"
_SET2 = Path(__file__).parent.parent / "sources" / "set2_questions.json"


def _to_md(q: dict) -> str:
    n = q["number"]
    return (
        f"**{n}. {q['question']}**\n"
        f"a. {q['options']['a']}\n"
        f"b. {q['options']['b']}\n"
        f"c. {q['options']['c']}\n"
        f"d. {q['options']['d']}"
    )


def _load() -> str:
    merged: dict[int, dict] = {}
    if _SET1.exists():
        for q in json.loads(_SET1.read_text(encoding="utf-8")):
            if q["number"] <= 135:
                merged[q["number"]] = q
    if _SET2.exists():
        for q in json.loads(_SET2.read_text(encoding="utf-8")):
            merged[q["number"]] = q
    if not merged:
        return ""
    parts = [_to_md(merged[n]) for n in sorted(merged)]
    return "\n\n".join(parts)


SET2_MARKDOWN = _load()
