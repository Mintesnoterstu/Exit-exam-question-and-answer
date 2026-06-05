#!/usr/bin/env python3
"""
Build two separate 500-question banks from official exam source files + answer keys.
Source format: **N. Question text** then a./b./c./d. options (markdown).

Run: py scripts/build_official_banks.py
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from answer_keys import SET1_ANSWERS, SET2_ANSWERS

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SOURCES = Path(__file__).parent / "sources"

THEME_RANGES = [
    (1, 135, "system-development", "System Development"),
    (136, 260, "programming-algorithms", "Programming and Algorithms"),
    (261, 350, "networking-security", "Computer Networking and Security"),
    (351, 380, "intelligent-systems", "Intelligent Systems"),
    (381, 440, "architecture-os", "Computer Architecture and OS"),
    (441, 500, "compiler-complexity", "Compiler and Complexity"),
]

DIFFICULTY_SET1 = {
    "system-development": [(1, 27, "easy"), (28, 95, "medium"), (96, 135, "hard")],
    "programming-algorithms": [(136, 160, "easy"), (161, 223, "medium"), (224, 260, "hard")],
    "networking-security": [(261, 278, "easy"), (279, 323, "medium"), (324, 350, "hard")],
    "intelligent-systems": [(351, 356, "easy"), (357, 371, "medium"), (372, 380, "hard")],
    "architecture-os": [(381, 392, "easy"), (393, 422, "medium"), (423, 440, "hard")],
    "compiler-complexity": [(441, 452, "easy"), (453, 482, "medium"), (483, 500, "hard")],
}

DIFFICULTY_SET2 = {
    "system-development": [(1, 27, "easy"), (28, 95, "medium"), (96, 135, "hard")],
    "programming-algorithms": [(136, 154, "easy"), (155, 198, "medium"), (199, 260, "hard")],
    "networking-security": [(261, 274, "easy"), (275, 309, "medium"), (310, 354, "hard")],
    "intelligent-systems": [(355, 359, "easy"), (360, 369, "medium"), (370, 384, "hard")],
    "architecture-os": [(385, 393, "easy"), (394, 414, "medium"), (415, 444, "hard")],
    "compiler-complexity": [(445, 453, "easy"), (454, 474, "medium"), (475, 500, "hard")],
}

COURSE_BY_NUM = [
    (1, 27, "software-engineering", "Software Engineering"),
    (28, 54, "web-programming", "Web Programming"),
    (55, 90, "database-fundamentals", "Database Fundamentals"),
    (91, 135, "advanced-database", "Advanced Database"),
    (136, 160, "computer-programming", "Computer Programming"),
    (161, 185, "oop", "Object Oriented Programming"),
    (186, 210, "design-analysis-algorithms", "Design and Analysis of Algorithms"),
    (211, 260, "data-structures-algorithms", "Data Structures and Algorithms"),
    (261, 290, "data-communication-networking", "Data Communication and Networking"),
    (291, 320, "computer-security", "Computer Security"),
    (321, 350, "network-system-admin", "Network and System Administration"),
    (351, 380, "artificial-intelligence", "Artificial Intelligence"),
    (381, 410, "operating-system", "Operating System"),
    (411, 440, "computer-organization", "Computer Organization and Architecture"),
    (441, 470, "automata-complexity", "Automata and Complexity Theory"),
    (471, 500, "compiler-design", "Compiler Design"),
]

EXPLANATIONS = {
    "analysis": "The Analysis phase of the SDLC gathers and documents user requirements before design begins — a core software engineering concept from your course materials.",
    "single responsibility": "The Single Responsibility Principle (SRP) states a software component should have only one reason to change — one job, one responsibility. This is the first SOLID principle taught in software engineering.",
    "scrum": "Scrum is an Agile framework with sprints, daily stand-ups, and iterative delivery — unlike sequential models such as Waterfall.",
    "html": "HTML (Hyper Text Markup Language) is the standard markup language for structuring web content, as covered in web programming materials.",
    "select": "The SQL SELECT statement retrieves rows from database tables; INSERT adds rows, UPDATE modifies them, and DELETE removes them.",
    "css": "CSS (Cascading Style Sheets) controls presentation, layout, and styling of HTML documents — it does not add interactivity (JavaScript) or structure content (HTML).",
    "get": "HTTP GET requests retrieve representations of resources from a server and should be safe and idempotent in RESTful design.",
    "acid": "ACID stands for Atomicity, Consistency, Isolation, and Durability — the four properties that guarantee reliable database transactions.",
    "mongodb": "MongoDB is a document-oriented NoSQL database; MySQL, PostgreSQL, and Oracle are relational SQL databases.",
    "primary key": "A primary key uniquely identifies each row in a relational table and enforces entity integrity in database design.",
    "foreign key": "A foreign key references the primary key of another table, establishing referential integrity between relations.",
    "normal form": "Normalization removes redundancy and update anomalies. 3NF eliminates transitive dependencies; BCNF strengthens 3NF when the key alone determines all attributes.",
    "inner join": "INNER JOIN returns only rows with matching values in both tables; LEFT JOIN keeps all rows from the left table plus matches from the right.",
    "tcp": "TCP is connection-oriented, provides reliable delivery with acknowledgments, and uses the three-way handshake (SYN, SYN-ACK, ACK).",
    "udp": "UDP is connectionless and faster but does not guarantee delivery — suitable for streaming and DNS where speed matters more than reliability.",
    "dijkstra": "Dijkstra's algorithm finds shortest paths from a single source in graphs with non-negative edge weights, typically O(E log V) with a binary heap.",
    "stack": "A stack follows LIFO (Last In, First Out) — push/pop at one end. Used for recursion, undo operations, and DFS.",
    "queue": "A queue follows FIFO (First In, First Out) — enqueue at rear, dequeue at front. Used for BFS and scheduling.",
    "polymorphism": "Polymorphism allows one interface with multiple implementations — compile-time (overloading) and runtime (overriding) in OOP.",
    "halting": "The halting problem asks whether a program will halt on a given input. It is undecidable — no general algorithm can solve it for all programs.",
    "finite automaton": "Finite automata recognize regular languages — the lowest level in the Chomsky hierarchy, used in lexical analysis.",
    "pushdown": "Pushdown automata have a stack and recognize context-free languages — used in syntax analysis of programming languages.",
    "machine learning": "Machine learning is a subset of AI where systems learn patterns from data rather than being explicitly programmed for every rule.",
    "overfitting": "Overfitting means the model memorizes training data but fails on unseen data — regularization and cross-validation help prevent it.",
    "paging": "Paging divides physical memory into fixed-size frames and logical memory into pages, enabling virtual memory and reducing external fragmentation.",
    "deadlock": "Deadlock requires mutual exclusion, hold-and-wait, no preemption, and circular wait. Prevention breaks one of these conditions.",
    "default": "This answer aligns with the Ethiopian MoE CS exit exam blueprint and standard references in your course materials (software engineering, databases, networking, OS, AI, compilers).",
}


def parse_exam_markdown(text: str) -> dict[int, dict]:
    """Parse **N. question** blocks with a./b./c./d. options."""
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = text.replace("\r\n", "\n")
    blocks = re.split(r"\n(?=\*\*\d+\.\s)", text)
    out: dict[int, dict] = {}

    for block in blocks:
        m = re.match(r"\*\*(\d+)\.\s*(.+?)(?=\n[a-d]\.\s)", block, re.S)
        if not m:
            continue
        num = int(m.group(1))
        question = re.sub(r"\s+", " ", m.group(2).strip())
        question = question.rstrip("*").strip()
        opts = {}
        for letter in "abcd":
            om = re.search(rf"^{letter}\.\s*(.+)$", block, re.M)
            if om:
                opts[letter] = om.group(1).strip()
        if len(opts) == 4:
            out[num] = {"question": question, "options": opts}
    return out


def lookup_meta(num: int, bank: str) -> tuple[str, str, str, str]:
    theme_id, theme_name = "system-development", "System Development"
    for lo, hi, tid, tname in THEME_RANGES:
        if lo <= num <= hi:
            theme_id, theme_name = tid, tname
            break
    course_id, course_name = "software-engineering", "Software Engineering"
    for lo, hi, cid, cname in COURSE_BY_NUM:
        if lo <= num <= hi:
            course_id, course_name = cid, cname
            break
    diff_map = DIFFICULTY_SET1 if bank == "set1" else DIFFICULTY_SET2
    difficulty = "medium"
    for tid, ranges in diff_map.items():
        for lo, hi, d in ranges:
            if lo <= num <= hi:
                difficulty = d
                break
    chapter = f"{theme_name} · Q{num}"
    return theme_id, course_id, difficulty, chapter


def build_explanation(num: int, question: str, correct: str, options: dict[str, str]) -> dict:
    qlow = question.lower()
    correct_text = options.get(correct, "")
    key = "default"
    for kw, exp in EXPLANATIONS.items():
        if kw in qlow or kw in correct_text.lower():
            key = kw
            break
    correct_exp = EXPLANATIONS.get(key, EXPLANATIONS["default"])
    correct_exp += f" Option {correct.upper()} ({correct_text}) is correct per the official answer key for this item."

    incorrect = {}
    for letter, text in options.items():
        if letter != correct:
            incorrect[letter.upper()] = (
                f"Option {letter.upper()} ({text}) does not match the definition or scenario required by the question stem."
            )

    mistake = "Students often confuse similar terms or pick a partially correct statement that fails the precise requirement of MoE-style items."
    if "normal form" in qlow or "normalization" in qlow:
        mistake = "Confusing 1NF, 2NF, and 3NF partial vs transitive dependencies is a common exit exam trap."
    elif "tcp" in qlow or "udp" in qlow:
        mistake = "Mixing connection-oriented TCP with connectionless UDP characteristics is frequently tested."
    elif "complexity" in qlow or "o(" in qlow:
        mistake = "Confusing average-case and worst-case complexity leads to wrong algorithm choices."

    return {"correct": correct_exp, "incorrect": incorrect, "commonMistake": mistake}


def build_bank(bank_id: str, answers: dict[int, str], parsed: dict[int, dict], fallback: dict[int, dict] | None = None) -> list[dict]:
    questions = []
    for num in range(1, 501):
        ans = answers.get(num)
        if not ans:
            raise ValueError(f"{bank_id}: missing answer for question {num}")
        pdata = parsed.get(num) or (fallback or {}).get(num)
        if not pdata:
            raise ValueError(f"{bank_id}: missing question text for {num}")

        theme_id, course_id, difficulty, chapter = lookup_meta(num, bank_id)
        correct_upper = ans.upper()
        options_upper = {k.upper(): v for k, v in pdata["options"].items()}

        questions.append({
            "id": f"{bank_id.upper()}-Q{num:03d}",
            "bankId": bank_id,
            "number": num,
            "courseId": course_id,
            "themeId": theme_id,
            "chapter": chapter,
            "difficulty": difficulty,
            "cognitive": "understand" if difficulty == "easy" else "apply" if difficulty == "medium" else "analyze",
            "question": pdata["question"],
            "options": options_upper,
            "correct": correct_upper,
            "explanation": build_explanation(num, pdata["question"], ans, pdata["options"]),
        })
    return questions


def main():
    SOURCES.mkdir(exist_ok=True)
    set1_path = SOURCES / "set1_exam.md"
    set2_path = SOURCES / "set2_exam.md"

    if not set1_path.exists():
        raise FileNotFoundError(f"Missing {set1_path}. Add the Set 1 exam markdown source.")

    set1_text = set1_path.read_text(encoding="utf-8")
    set1_parsed = parse_exam_markdown(set1_text)

    set2_parsed: dict[int, dict] = {}
    if set2_path.exists():
        set2_parsed = parse_exam_markdown(set2_path.read_text(encoding="utf-8"))

    # Set 2 questions 1-135 reuse Set 1 text when not in set2 file
    set2_full = {**set1_parsed, **set2_parsed}

    bank1 = build_bank("set1", SET1_ANSWERS, set1_parsed)
    bank2 = build_bank("set2", SET2_ANSWERS, set2_full, fallback=set1_parsed)

    out1 = DATA / "questions-set1.json"
    out2 = DATA / "questions-set2.json"
    out1.write_text(json.dumps({
        "bankId": "set1",
        "title": "Official Exit Exam Bank — Set 1 (500 Questions)",
        "description": "Full-length bank with blueprint weights: Easy 20%, Medium 50%, Hard 30%",
        "count": len(bank1),
        "questions": bank1,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    out2.write_text(json.dumps({
        "bankId": "set2",
        "title": "Official Exit Exam Bank — Set 2 (500 Questions)",
        "description": "Alternate bank with harder distribution — answers kept separate from Set 1",
        "count": len(bank2),
        "questions": bank2,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    # Combined index for backward compatibility
    (DATA / "questions-index.json").write_text(json.dumps({
        "banks": [
            {"id": "set1", "file": "questions-set1.json", "count": 500},
            {"id": "set2", "file": "questions-set2.json", "count": 500},
        ],
        "total": 1000,
    }, indent=2), encoding="utf-8")

    print(f"Set 1: {len(bank1)} questions -> {out1}")
    print(f"Set 2: {len(bank2)} questions -> {out2}")
    print(f"Parsed Set1 text: {len(set1_parsed)} blocks, Set2 unique: {len(set2_parsed)} blocks")


if __name__ == "__main__":
    main()
