#!/usr/bin/env python3
import json
import re
from pathlib import Path

TRANSCRIPT = Path(
    r"C:\Users\hp\.cursor\projects\c-Users-hp-Desktop-Class-Files-4th-year-Exit-question-website-Exit-exam-question-and-answer\agent-transcripts\178266d0-54ad-4bb3-827b-861c92f4223f\178266d0-54ad-4bb3-827b-861c92f4223f.jsonl"
)


def load_text() -> str:
    for line in TRANSCRIPT.read_text(encoding="utf-8").splitlines():
        obj = json.loads(line)
        if obj.get("role") != "user":
            continue
        for part in obj.get("message", {}).get("content", []):
            t = part.get("text", "")
            if "**1. Which phase of the SDLC" in t:
                return t
    raise RuntimeError("not found")


def code_questions(chunk: str) -> dict[int, str]:
    blocks = re.findall(r"\*\*(\d+)\.[^*]*\*\*(.*?)(?=\n[a-d]\.\s)", chunk, re.S)
    out = {}
    for num, body in blocks:
        if "```" in body:
            code = re.search(r"```(?:\w+)?\n(.*?)```", body, re.S)
            if code:
                out[int(num)] = code.group(1).strip()
    return out


def main():
    text = load_text()
    set2_start = text.find("Here is the continuation of the **500-question exit exam (Set 2)**")
    s1 = code_questions(text[:set2_start])
    s2 = code_questions(text[set2_start:])
    print("Set1 code questions:", sorted(s1))
    print("Set2 code questions:", sorted(s2))
    print("Set2-only:", sorted(set(s2) - set(s1)))


if __name__ == "__main__":
    main()
