import { Storage } from "./storage.js";
import { getCourseMap } from "./data-loader.js";

const charts = {};

export function renderAnalytics() {
  const progress = Storage.getProgress();
  renderScoreChart(progress);
  renderCourseChart(progress);
  renderDifficultyChart(progress);
}

function chartOptions() {
  const dark = document.documentElement.dataset.theme === "dark";
  return {
    responsive: true,
    maintainAspectRatio: true,
    aspectRatio: window.innerWidth < 480 ? 1.2 : 2,
    plugins: { legend: { labels: { color: dark ? "#e8edf5" : "#1a2234" } } },
    scales: {
      x: { ticks: { color: dark ? "#94a3b8" : "#5c6b82" }, grid: { color: dark ? "#334155" : "#e2e8f0" } },
      y: { ticks: { color: dark ? "#94a3b8" : "#5c6b82" }, grid: { color: dark ? "#334155" : "#e2e8f0" } },
    },
  };
}

function destroyChart(id) {
  if (charts[id]) {
    charts[id].destroy();
    delete charts[id];
  }
}

function renderScoreChart(progress) {
  const el = document.getElementById("score-chart");
  if (!el || typeof Chart === "undefined") return;
  destroyChart("score");

  const sessions = progress.history.filter((_, i) => i % 5 === 4).slice(-12);
  const labels = sessions.map((_, i) => `S${i + 1}`);
  const data = [];
  let run = 0;
  let runT = 0;
  progress.history.forEach((h) => {
    runT += 1;
    if (h.correct) run += 1;
  });
  for (let i = 0; i < Math.min(12, progress.history.length); i++) {
    const slice = progress.history.slice(0, i + 1);
    const c = slice.filter((x) => x.correct).length;
    data.push(slice.length ? Math.round((c / slice.length) * 100) : 0);
  }

  charts.score = new Chart(el, {
    type: "line",
    data: {
      labels: labels.length ? labels : ["Start"],
      datasets: [
        {
          label: "Accuracy %",
          data: data.length ? data : [0],
          borderColor: "#2563eb",
          backgroundColor: "rgba(37,99,235,0.15)",
          fill: true,
          tension: 0.35,
        },
      ],
    },
    options: chartOptions(),
  });
}

function renderCourseChart(progress) {
  const el = document.getElementById("course-chart");
  if (!el || typeof Chart === "undefined") return;
  destroyChart("course");

  const courseMap = getCourseMap();
  const entries = Object.entries(progress.byCourse || {});
  const labels = entries.map(([id]) => courseMap[id]?.name?.slice(0, 18) || id);
  const data = entries.map(([, v]) => (v.total ? Math.round((v.correct / v.total) * 100) : 0));

  charts.course = new Chart(el, {
    type: "bar",
    data: {
      labels: labels.length ? labels : ["No data yet"],
      datasets: [{ label: "% Correct", data: data.length ? data : [0], backgroundColor: "#7c3aed" }],
    },
    options: { ...chartOptions(), indexAxis: labels.length > 8 ? "y" : "x" },
  });
}

function renderDifficultyChart(progress) {
  const el = document.getElementById("difficulty-chart");
  if (!el || typeof Chart === "undefined") return;
  destroyChart("difficulty");

  const bd = progress.byDifficulty || {};
  charts.difficulty = new Chart(el, {
    type: "doughnut",
    data: {
      labels: ["Easy", "Medium", "Hard"],
      datasets: [
        {
          data: ["easy", "medium", "hard"].map((d) => bd[d]?.t || 0),
          backgroundColor: ["#059669", "#d97706", "#dc2626"],
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      aspectRatio: window.innerWidth < 480 ? 1.1 : 1.8,
      plugins: { legend: { position: "bottom", labels: { boxWidth: 12, font: { size: 11 } } } },
    },
  });
}

export function renderDashboardCharts(progress, totalQuestions) {
  const el = document.getElementById("progress-chart");
  if (!el || typeof Chart === "undefined") return;
  destroyChart("progress");

  const seen = progress.seenIds?.length || 0;
  charts.progress = new Chart(el, {
    type: "doughnut",
    data: {
      labels: ["Attempted", "Remaining"],
      datasets: [{ data: [seen, Math.max(0, totalQuestions - seen)], backgroundColor: ["#2563eb", "#e2e8f0"] }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      aspectRatio: window.innerWidth < 480 ? 1.1 : 1.5,
      plugins: { legend: { position: "bottom", labels: { boxWidth: 12, font: { size: 11 } } } },
    },
  });
}

export function getWeakAreas(progress, limit = 8) {
  const counts = {};
  progress.wrongIds?.forEach((id) => {
    const parts = id;
    counts[parts] = (counts[parts] || 0) + 1;
  });

  const byCourse = {};
  progress.history
    .filter((h) => !h.correct)
    .forEach((h) => {
      byCourse[h.courseId] = (byCourse[h.courseId] || 0) + 1;
    });

  return Object.entries(byCourse)
    .sort((a, b) => b[1] - a[1])
    .slice(0, limit)
    .map(([courseId, count]) => ({ courseId, count }));
}

export function refreshChartsOnTheme() {
  renderAnalytics();
}
