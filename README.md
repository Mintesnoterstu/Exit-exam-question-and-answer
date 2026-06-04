# Ethiopian CS National Exit Exam Prep

A complete, responsive exam preparation website built with **HTML, CSS, and JavaScript only** (no backend). It includes **1,000 multiple-choice questions** aligned with the **Ministry of Education Computer Science Test Blueprint** and patterns from uploaded materials in the `matrial` folder.

## Features

- **1,000 MCQs** with correct answers, detailed explanations, and why other options are wrong
- Organized by **theme, course, chapter, difficulty** (easy/medium/hard), and **cognitive level** (Bloom: remember → create)
- **Practice mode** — instant feedback and explanations
- **Timed mock exam** — 100 questions, 120 minutes, blueprint-weighted sampling
- **Review mode** — incorrect answers, bookmarks, favorites
- **Search & filters**, **random quizzes**, **weak-area analysis**
- **Progress tracking**, **score analytics**, charts (Chart.js)
- **Dark / light mode**, mobile-responsive UI
- All progress stored in **browser localStorage**; questions in **JSON**

## Quick start

1. **Generate the question bank** (if `data/questions.json` is missing):

   ```bash
   py scripts/generate_question_bank.py
   ```

2. **Serve the site locally** (required for `fetch` to load JSON):

   ```bash
   py -m http.server 8080
   ```

3. Open [http://localhost:8080](http://localhost:8080) in your browser.

   Or use the **Live Server** extension in VS Code/Cursor.

## Project structure

```
├── index.html          # Main app shell
├── css/styles.css      # Responsive styles & themes
├── js/
│   ├── app.js          # Application logic & routing
│   ├── data-loader.js  # Loads metadata & questions
│   ├── storage.js      # localStorage progress & bookmarks
│   ├── quiz.js         # Quiz engine & UI rendering
│   └── analytics.js    # Charts & weak areas
├── data/
│   ├── metadata.json   # MoE blueprint themes & weights
│   ├── questions.json  # Full 1,000-question bank
│   └── chunks/         # Per-theme question chunks
├── scripts/
│   ├── generate_question_bank.py
│   └── bank_content.py
└── matrial/            # Your uploaded PDFs, DOCX, notes
```

## Blueprint alignment

Question counts follow **Table 6-1** of the MoE CS test blueprint (100 exam items scaled ×10):

| Theme | Exam items | Question bank |
|-------|------------|---------------|
| System Development | 27 | 270 |
| Programming and Algorithms | 25 | 250 |
| Networking and Security | 18 | 180 |
| Intelligent Systems | 6 | 60 |
| Architecture & OS | 12 | 120 |
| Compiler and Complexity | 12 | 120 |

## Regenerating questions

After adding or updating files in `matrial/`, re-run:

```bash
py scripts/generate_question_bank.py
```

The script parses sample national exam PDFs and merges course-aligned seeds from your notes.

## License

Educational use. Ministry materials remain property of their respective authors.
