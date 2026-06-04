import { Storage } from "./storage.js";
import { getCourseMap } from "./data-loader.js";

export class QuizSession {
  constructor(questions, options = {}) {
    this.questions = questions;
    this.index = 0;
    this.answers = {};
    this.mode = options.mode || "practice";
    this.showFeedback = options.showFeedback !== false;
    this.onComplete = options.onComplete || (() => {});
    this.timerSeconds = options.timerSeconds || 0;
    this.startTime = Date.now();
    this.timerId = null;
    this.remaining = this.timerSeconds;
  }

  get current() {
    return this.questions[this.index];
  }

  get total() {
    return this.questions.length;
  }

  get progress() {
    return ((this.index + 1) / this.total) * 100;
  }

  answer(letter) {
    const q = this.current;
    this.answers[q.id] = letter;
    if (this.mode === "practice" && this.showFeedback) return { done: false, feedback: true };
    if (this.index < this.total - 1) {
      this.index += 1;
      return { done: false };
    }
    return { done: true };
  }

  next() {
    if (this.index < this.total - 1) {
      this.index += 1;
      return true;
    }
    return false;
  }

  prev() {
    if (this.index > 0) {
      this.index -= 1;
      return true;
    }
    return false;
  }

  score() {
    let correct = 0;
    this.questions.forEach((q) => {
      if (this.answers[q.id] === q.correct) correct += 1;
    });
    return { correct, total: this.total, percent: Math.round((correct / this.total) * 100) };
  }

  finish() {
    const s = this.score();
    this.questions.forEach((q) => {
      const ok = this.answers[q.id] === q.correct;
      if (this.answers[q.id]) Storage.recordAnswer(q, ok);
    });
    Storage.set("lastSession", {
      mode: this.mode,
      score: s,
      at: Date.now(),
      answers: this.answers,
    });
    this.onComplete(s, this.answers);
    return s;
  }

  startTimer(onTick) {
    if (!this.timerSeconds) return;
    this.timerId = setInterval(() => {
      this.remaining -= 1;
      onTick(this.remaining);
      if (this.remaining <= 0) {
        clearInterval(this.timerId);
        this.finish();
      }
    }, 1000);
  }

  stopTimer() {
    if (this.timerId) clearInterval(this.timerId);
  }
}

export function renderQuizUI(container, session, handlers) {
  const courseMap = getCourseMap();
  const q = session.current;
  if (!q) return;

  const course = courseMap[q.courseId]?.name || q.courseId;
  const answered = session.answers[q.id];
  const showResult = session.mode === "practice" && answered && session.showFeedback;

  container.innerHTML = `
    <div class="card quiz-card">
      <div class="quiz-header">
        <div class="quiz-meta">
          <span class="tag">${course}</span>
          <span class="tag">${q.chapter}</span>
          <span class="tag ${q.difficulty}">${q.difficulty}</span>
          <span class="tag">${q.cognitive}</span>
        </div>
        ${session.timerSeconds ? `<span class="timer" id="quiz-timer">${formatTime(session.remaining)}</span>` : ""}
        <div class="icon-actions">
          <button type="button" data-action="bookmark" title="Bookmark">${handlers.isBookmarked(q.id) ? "🔖" : "📑"}</button>
          <button type="button" data-action="favorite" title="Favorite">${handlers.isFavorite(q.id) ? "⭐" : "☆"}</button>
        </div>
      </div>
      <p class="question-text">${escapeHtml(q.question)}</p>
      <div class="options" role="group" aria-label="Answer options">
        ${["A", "B", "C", "D"]
          .map((letter) => {
            let cls = "option-btn";
            if (answered === letter) cls += " selected";
            if (showResult) {
              if (letter === q.correct) cls += " correct";
              else if (answered === letter) cls += " incorrect";
            }
            return `<button type="button" class="${cls}" data-option="${letter}" ${showResult ? "disabled" : ""}>
              <strong>${letter}.</strong> ${escapeHtml(q.options[letter])}
            </button>`;
          })
          .join("")}
      </div>
      ${showResult ? renderExplanation(q) : ""}
      <div class="quiz-actions">
        <div class="progress-bar"><div class="progress-fill" style="width:${session.progress}%"></div></div>
        <span>${session.index + 1} / ${session.total}</span>
        ${session.index > 0 ? '<button type="button" class="btn btn-secondary" data-action="prev">Previous</button>' : ""}
        ${
          showResult || (session.mode === "mock" && answered)
            ? `<button type="button" class="btn btn-primary" data-action="next">${session.index < session.total - 1 ? "Next" : "Finish"}</button>`
            : ""
        }
        ${session.mode === "mock" ? '<button type="button" class="btn btn-danger" data-action="submit">Submit Exam</button>' : ""}
      </div>
    </div>
  `;

  container.querySelectorAll("[data-option]").forEach((btn) => {
    btn.addEventListener("click", () => handlers.onSelect(btn.dataset.option));
  });
  container.querySelectorAll("[data-action]").forEach((btn) => {
    btn.addEventListener("click", () => handlers.onAction(btn.dataset.action));
  });
}

function renderExplanation(q) {
  const inc = q.explanation?.incorrect || {};
  const wrongHtml = Object.entries(inc)
    .map(([k, v]) => `<li><strong>${k}:</strong> ${escapeHtml(v)}</li>`)
    .join("");
  return `
    <div class="explanation">
      <h4>✓ Correct: ${q.correct}</h4>
      <p>${escapeHtml(q.explanation?.correct || "")}</p>
      ${wrongHtml ? `<h4>Why other options are wrong</h4><ul>${wrongHtml}</ul>` : ""}
      ${q.explanation?.commonMistake ? `<div class="mistake"><strong>Common mistake:</strong> ${escapeHtml(q.explanation.commonMistake)}</div>` : ""}
    </div>
  `;
}

function escapeHtml(s) {
  const d = document.createElement("div");
  d.textContent = s;
  return d.innerHTML;
}

function formatTime(sec) {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

export { formatTime, escapeHtml };
