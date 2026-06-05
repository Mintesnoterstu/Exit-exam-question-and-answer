"""Set 1 exam questions 1-500 — loaded from generated JSON for maintainability."""

import json
from pathlib import Path

_DATA = Path(__file__).parent.parent / "sources" / "set1_questions.json"


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
    if not _DATA.exists():
        return ""
    items = json.loads(_DATA.read_text(encoding="utf-8"))
    items.sort(key=lambda x: x["number"])
    return "\n\n".join(_to_md(q) for q in items)


SET1_MARKDOWN = _load()
