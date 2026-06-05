import {
  loadData,
  switchBank,
  getActiveBankId,
  getBankIndex,
  getMetadata,
  getAllQuestions,
  filterQuestions,
  sampleMockExam,
  sampleRandom,
  getCourseMap,
  getQuestionById,
} from "./data-loader.js";
import { Storage } from "./storage.js";
import { QuizSession, renderQuizUI } from "./quiz.js";
import { renderAnalytics, renderDashboardCharts, getWeakAreas, refreshChartsOnTheme } from "./analytics.js";

let activeSession = null;
let courseMap = {};

function setMobileViewportHeight() {
  const vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty("--vh", `${vh}px`);
}

async function init() {
  setMobileViewportHeight();
  window.addEventListener("resize", setMobileViewportHeight);
  window.addEventListener("orientationchange", () => setTimeout(setMobileViewportHeight, 100));

  try {
    await loadData();
    courseMap = getCourseMap();
    applyTheme(Storage.getTheme());
    bindNavigation();
    bindMobileNav();
    bindThemeToggle();
    renderDashboard();
    buildFilterUI();
    bindPractice();
    bindMock();
    bindReview();
    bindBrowse();
    bindQuickActions();
    bindBankSwitcher();
    document.getElementById("app-loader").classList.add("hidden");
  } catch (err) {
    document.querySelector(".loader-card p").textContent =
      "Could not load data. Serve via a local server (e.g. Live Server) or run: py -m http.server";
    console.error(err);
  }
}

function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  document.querySelector(".theme-icon").textContent = theme === "dark" ? "☀️" : "🌙";
}

function bindThemeToggle() {
  document.getElementById("theme-toggle").addEventListener("click", () => {
    const next = Storage.getTheme() === "dark" ? "light" : "dark";
    Storage.setTheme(next);
    applyTheme(next);
    renderDashboard();
    renderAnalytics();
  });
}

function bindNavigation() {
  document.querySelectorAll(".nav-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      closeMobileMenu();
      showView(btn.dataset.view);
    });
  });
}

function bindMobileNav() {
  document.querySelectorAll(".bottom-nav-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const view = btn.dataset.view;
      if (view === "more") {
        openMobileMenu();
        return;
      }
      closeMobileMenu();
      showView(view);
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  });

  document.getElementById("menu-toggle")?.addEventListener("click", () => {
    const menu = document.getElementById("mobile-menu");
    if (menu?.hidden) openMobileMenu();
    else closeMobileMenu();
  });

  document.querySelectorAll("[data-close-menu]").forEach((el) => {
    el.addEventListener("click", closeMobileMenu);
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeMobileMenu();
  });
}

function openMobileMenu() {
  const menu = document.getElementById("mobile-menu");
  const toggle = document.getElementById("menu-toggle");
  if (!menu) return;
  menu.hidden = false;
  document.body.classList.add("menu-open");
  toggle?.setAttribute("aria-expanded", "true");
}

function closeMobileMenu() {
  const menu = document.getElementById("mobile-menu");
  const toggle = document.getElementById("menu-toggle");
  if (!menu) return;
  menu.hidden = true;
  document.body.classList.remove("menu-open");
  toggle?.setAttribute("aria-expanded", "false");
}

function showView(name) {
  document.querySelectorAll(".nav-btn").forEach((b) => b.classList.toggle("active", b.dataset.view === name));
  document.querySelectorAll(".bottom-nav-btn").forEach((b) => {
    const v = b.dataset.view;
    if (v === "more") {
      b.classList.toggle("active", name === "analytics" || name === "browse");
    } else {
      b.classList.toggle("active", v === name);
    }
  });
  document.querySelectorAll(".view").forEach((v) => v.classList.toggle("active", v.id === `view-${name}`));
  if (name === "analytics") renderAnalytics();
  if (name === "review") renderReview("wrong");
  if (name === "dashboard") renderDashboard();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function bindBankSwitcher() {
  const select = document.getElementById("bank-select");
  if (!select) return;
  select.value = getActiveBankId();
  select.addEventListener("change", async () => {
    const loader = document.getElementById("app-loader");
    loader?.classList.remove("hidden");
    try {
      await switchBank(select.value);
      courseMap = getCourseMap();
      activeSession = null;
      buildFilterUI();
      refreshBrowseCourseFilter();
      document.getElementById("filter-course-options")?.dispatchEvent(new Event("change", { bubbles: true }));
      renderDashboard();
      bindPractice();
      document.getElementById("quiz-container")?.classList.add("hidden");
      document.getElementById("practice-empty")?.classList.remove("hidden");
      document.getElementById("mock-quiz")?.classList.add("hidden");
    } finally {
      loader?.classList.add("hidden");
    }
  });
}

function renderDashboard() {
  const meta = getMetadata();
  const questions = getAllQuestions();
  const progress = Storage.getProgress();
  const pct = progress.answered ? Math.round((progress.correct / progress.answered) * 100) : 0;
  const bank = getBankIndex()?.banks?.find((b) => b.id === getActiveBankId());
  const bankLabel = bank?.title || getActiveBankId();

  document.getElementById("dashboard-stats").innerHTML = `
    <div class="stat-pill"><strong>${bankLabel}</strong><span>Active bank</span></div>
    <div class="stat-pill"><strong>${questions.length}</strong><span>Questions</span></div>
    <div class="stat-pill"><strong>${progress.answered}</strong><span>Answered</span></div>
    <div class="stat-pill"><strong>${pct}%</strong><span>Accuracy</span></div>
    <div class="stat-pill"><strong>${Storage.getBookmarks().length}</strong><span>Bookmarks</span></div>
  `;

  const themeBars = document.getElementById("theme-bars");
  themeBars.innerHTML = meta.themes
    .map(
      (t) => `
    <div class="bar-row">
      <div class="bar-label"><span>${t.name}</span><span>${t.weight}% · ${t.questionTarget} Q</span></div>
      <div class="bar-track"><div class="bar-fill" style="width:${t.weight}%"></div></div>
    </div>`
    )
    .join("");

  renderDashboardCharts(progress, questions.length);

  const weak = getWeakAreas(progress);
  const weakEl = document.getElementById("weak-areas");
  if (!weak.length) {
    weakEl.innerHTML = '<span class="muted">Answer questions to see weak areas here.</span>';
  } else {
    weakEl.innerHTML = weak
      .map((w) => `<span class="weak-chip">${courseMap[w.courseId]?.name || w.courseId} (${w.count} wrong)</span>`)
      .join("");
  }
}

function renderCourseCheckboxes(containerId, inputName) {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = Object.entries(courseMap)
    .map(
      ([id, c]) => `
    <label class="course-chip-check">
      <input type="checkbox" name="${inputName}" value="${id}" />
      <span>${c.name}</span>
    </label>`
    )
    .join("");
}

function getSelectedCourses(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return [];
  return [...container.querySelectorAll('input[type="checkbox"]:checked')].map((cb) => cb.value);
}

function bindCourseMultiActions() {
  document.querySelectorAll("[data-course-action]").forEach((btn) => {
    if (btn.dataset.bound) return;
    btn.dataset.bound = "1";
    btn.addEventListener("click", () => {
      const targetId = btn.dataset.target;
      const container = document.getElementById(targetId);
      if (!container) return;
      const checked = btn.dataset.courseAction === "all";
      container.querySelectorAll('input[type="checkbox"]').forEach((cb) => {
        cb.checked = checked;
      });
      container.dispatchEvent(new Event("change", { bubbles: true }));
    });
  });
}

function buildFilterUI() {
  const el = document.getElementById("practice-filters");

  el.innerHTML = `
    <h3>Practice Filters</h3>
    <div class="filter-grid">
      <div class="filter-span-full course-multi-filter">
        <div class="course-multi-header">
          <label>Courses <span class="course-multi-hint">(select one or more, or leave empty for all)</span></label>
          <div class="course-multi-actions">
            <button type="button" class="course-multi-btn" data-course-action="all" data-target="pf-course-options">All</button>
            <button type="button" class="course-multi-btn" data-course-action="none" data-target="pf-course-options">Clear</button>
          </div>
        </div>
        <div id="pf-course-options" class="course-multi-options" role="group" aria-label="Filter by course"></div>
      </div>
      <div><label>Difficulty</label><select id="pf-difficulty"><option value="">All</option><option value="easy">Easy</option><option value="medium">Medium</option><option value="hard">Hard</option></select></div>
      <div><label>Cognitive</label><select id="pf-cognitive"><option value="">All</option><option value="remember">Remember</option><option value="understand">Understand</option><option value="apply">Apply</option><option value="analyze">Analyze</option><option value="evaluate">Evaluate</option><option value="create">Create</option></select></div>
      <div><label>Count</label><select id="pf-count"><option value="10">10</option><option value="20" selected>20</option><option value="50">50</option></select></div>
    </div>
    <button class="btn btn-primary" id="start-practice-filtered">Start Session</button>
  `;

  renderCourseCheckboxes("pf-course-options", "pf-course");
  bindCourseMultiActions();
  document.getElementById("start-practice-filtered").addEventListener("click", startPracticeFromFilters);
}

function getPracticeFilters() {
  return {
    courses: getSelectedCourses("pf-course-options"),
    difficulty: document.getElementById("pf-difficulty")?.value || "",
    cognitive: document.getElementById("pf-cognitive")?.value || "",
  };
}

function bindPractice() {
  const btn = document.getElementById("start-practice");
  if (!btn || btn.dataset.bound) return;
  btn.dataset.bound = "1";
  btn.addEventListener("click", startPracticeFromFilters);
}

function startPracticeFromFilters() {
  const filters = getPracticeFilters();
  const count = parseInt(document.getElementById("pf-count")?.value || "20", 10);
  const qs = sampleRandom(count, filters);
  if (!qs.length) {
    alert("No questions match your filters.");
    return;
  }
  startQuiz(qs, { mode: "practice", showFeedback: true }, "quiz-container", "practice-empty");
  showView("practice");
}

function bindMock() {
  document.getElementById("start-mock").addEventListener("click", () => {
    const qs = sampleMockExam();
    document.querySelector(".mock-intro").classList.add("hidden");
    const container = document.getElementById("mock-quiz");
    container.classList.remove("hidden");
    startQuiz(qs, { mode: "mock", showFeedback: false, timerSeconds: 120 * 60 }, "mock-quiz", null);
    showView("mock");
  });
}

function startQuiz(questions, options, containerId, emptyId) {
  if (activeSession) activeSession.stopTimer();

  activeSession = new QuizSession(questions, {
    ...options,
    onComplete: (score) => showResults(containerId, score, options.mode),
  });

  if (emptyId) {
    document.getElementById(emptyId)?.classList.add("hidden");
    document.getElementById(containerId)?.classList.remove("hidden");
  }

  const container = document.getElementById(containerId);
  const handlers = makeHandlers(container, options);

  const render = () => renderQuizUI(container, activeSession, handlers);
  render();

  if (options.timerSeconds) {
    activeSession.startTimer((remaining) => {
      const t = document.getElementById("quiz-timer");
      if (t) {
        t.textContent = formatTimer(remaining);
        if (remaining < 600) t.classList.add("warning");
      }
    });
  }
}

function makeHandlers(container, options) {
  return {
    isBookmarked: (id) => Storage.getBookmarks().includes(id),
    isFavorite: (id) => Storage.getFavorites().includes(id),
    onSelect: (letter) => {
      activeSession.answers[activeSession.current.id] = letter;
      if (options.mode === "practice") {
        Storage.recordAnswer(activeSession.current, letter === activeSession.current.correct);
      }
      renderQuizUI(container, activeSession, makeHandlers(container, options));
    },
    onAction: (action) => {
      const q = activeSession.current;
      if (action === "bookmark") {
        Storage.toggleList("bookmarks", q.id);
        renderQuizUI(container, activeSession, makeHandlers(container, options));
      }
      if (action === "favorite") {
        Storage.toggleList("favorites", q.id);
        renderQuizUI(container, activeSession, makeHandlers(container, options));
      }
      if (action === "next") {
        if (activeSession.index < activeSession.total - 1) activeSession.next();
        else activeSession.finish();
        renderQuizUI(container, activeSession, makeHandlers(container, options));
      }
      if (action === "prev") {
        activeSession.prev();
        renderQuizUI(container, activeSession, makeHandlers(container, options));
      }
      if (action === "submit") {
        if (confirm("Submit mock exam now?")) activeSession.finish();
      }
    },
  };
}

function showResults(containerId, score, mode) {
  activeSession?.stopTimer();
  const el = document.getElementById(containerId);
  el.innerHTML = `
    <div class="card results-panel animate-in">
      <h2>${mode === "mock" ? "Mock Exam Complete" : "Session Complete"}</h2>
      <p class="results-score">${score.percent}%</p>
      <p>${score.correct} correct out of ${score.total}</p>
      <button class="btn btn-primary" onclick="location.reload()">Back to Dashboard</button>
    </div>
  `;
  renderDashboard();
}

function formatTimer(sec) {
  const m = Math.floor(sec / 60);
  const s = sec % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

function bindReview() {
  document.querySelectorAll("[data-review]").forEach((tab) => {
    tab.addEventListener("click", () => {
      document.querySelectorAll("[data-review]").forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
      renderReview(tab.dataset.review);
    });
  });
}

function renderReview(type) {
  const list = document.getElementById("review-list");
  let ids = [];
  if (type === "wrong") ids = Storage.getProgress().wrongIds || [];
  if (type === "bookmarks") ids = Storage.getBookmarks();
  if (type === "favorites") ids = Storage.getFavorites();

  if (!ids.length) {
    list.innerHTML = '<p class="muted">Nothing to review in this category yet.</p>';
    return;
  }

  list.innerHTML = ids
    .slice(0, 50)
    .map((id) => {
      const q = getQuestionById(id);
      if (!q) return "";
      return `<div class="review-item">
        <strong>${courseMap[q.courseId]?.name || q.courseId}</strong>
        <p>${q.question.slice(0, 120)}…</p>
        <button class="btn btn-secondary btn-review-one" data-id="${q.id}">Practice this</button>
      </div>`;
    })
    .join("");

  list.querySelectorAll(".btn-review-one").forEach((btn) => {
    btn.addEventListener("click", () => {
      const q = getQuestionById(btn.dataset.id);
      if (q) {
        showView("practice");
        startQuiz([q], { mode: "practice", showFeedback: true }, "quiz-container", "practice-empty");
      }
    });
  });
}

function refreshBrowseCourseFilter() {
  renderCourseCheckboxes("filter-course-options", "browse-course");
  bindCourseMultiActions();
}

function bindBrowse() {
  refreshBrowseCourseFilter();

  const run = () => {
    const qs = filterQuestions({
      courses: getSelectedCourses("filter-course-options"),
      difficulty: document.getElementById("filter-difficulty").value,
      cognitive: document.getElementById("filter-cognitive").value,
      search: document.getElementById("search-input").value,
    }).slice(0, 40);

    document.getElementById("browse-results").innerHTML =
      qs.length === 0
        ? '<p class="muted">No matches.</p>'
        : qs
            .map(
              (q) => `
        <div class="browse-item">
          <div class="quiz-meta">
            <span class="tag">${courseMap[q.courseId]?.name || q.courseId}</span>
            <span class="tag ${q.difficulty}">${q.difficulty}</span>
          </div>
          <p>${q.question.slice(0, 200)}${q.question.length > 200 ? "…" : ""}</p>
          <button class="btn btn-ghost btn-browse-start" data-id="${q.id}">Practice</button>
        </div>`
            )
            .join("");

    document.querySelectorAll(".btn-browse-start").forEach((btn) => {
      btn.addEventListener("click", () => {
        const q = getQuestionById(btn.dataset.id);
        if (q) {
          showView("practice");
          startQuiz([q], { mode: "practice", showFeedback: true }, "quiz-container", "practice-empty");
        }
      });
    });
  };

  ["search-input", "filter-difficulty", "filter-cognitive"].forEach((id) => {
    document.getElementById(id).addEventListener("input", run);
    document.getElementById(id).addEventListener("change", run);
  });
  document.getElementById("filter-course-options")?.addEventListener("change", run);
  run();
}

function bindQuickActions() {
  document.querySelectorAll("[data-quick]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const action = btn.dataset.quick;
      if (action === "practice") {
        showView("practice");
        startPracticeFromFilters();
      }
      if (action === "mock") {
        showView("mock");
        document.getElementById("start-mock").click();
      }
      if (action === "random") {
        const qs = sampleRandom(20, {});
        showView("practice");
        startQuiz(qs, { mode: "practice", showFeedback: true }, "quiz-container", "practice-empty");
      }
    });
  });
}

init();
