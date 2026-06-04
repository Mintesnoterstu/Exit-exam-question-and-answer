const PREFIX = "exitExamPrep_";

export const Storage = {
  get(key, fallback = null) {
    try {
      const raw = localStorage.getItem(PREFIX + key);
      return raw ? JSON.parse(raw) : fallback;
    } catch {
      return fallback;
    }
  },

  set(key, value) {
    localStorage.setItem(PREFIX + key, JSON.stringify(value));
  },

  getProgress() {
    return (
      this.get("progress", {
        answered: 0,
        correct: 0,
        byCourse: {},
        byDifficulty: { easy: { t: 0, c: 0 }, medium: { t: 0, c: 0 }, hard: { t: 0, c: 0 } },
        history: [],
        wrongIds: [],
        seenIds: [],
      }) || {
        answered: 0,
        correct: 0,
        byCourse: {},
        byDifficulty: { easy: { t: 0, c: 0 }, medium: { t: 0, c: 0 }, hard: { t: 0, c: 0 } },
        history: [],
        wrongIds: [],
        seenIds: [],
      }
    );
  },

  saveProgress(progress) {
    this.set("progress", progress);
  },

  getBookmarks() {
    return this.get("bookmarks", []);
  },

  setBookmarks(ids) {
    this.set("bookmarks", ids);
  },

  getFavorites() {
    return this.get("favorites", []);
  },

  setFavorites(ids) {
    this.set("favorites", ids);
  },

  getTheme() {
    return this.get("theme", "light");
  },

  setTheme(theme) {
    this.set("theme", theme);
  },

  recordAnswer(question, isCorrect) {
    const p = this.getProgress();
    p.answered += 1;
    if (isCorrect) p.correct += 1;

    const cid = question.courseId;
    if (!p.byCourse[cid]) p.byCourse[cid] = { total: 0, correct: 0 };
    p.byCourse[cid].total += 1;
    if (isCorrect) p.byCourse[cid].correct += 1;

    const d = question.difficulty || "medium";
    if (!p.byDifficulty[d]) p.byDifficulty[d] = { t: 0, c: 0 };
    p.byDifficulty[d].t += 1;
    if (isCorrect) p.byDifficulty[d].c += 1;

    if (!p.seenIds.includes(question.id)) p.seenIds.push(question.id);
    if (!isCorrect && !p.wrongIds.includes(question.id)) p.wrongIds.push(question.id);
    if (isCorrect) p.wrongIds = p.wrongIds.filter((id) => id !== question.id);

    p.history.push({
      id: question.id,
      correct: isCorrect,
      courseId: cid,
      at: Date.now(),
    });
    if (p.history.length > 200) p.history = p.history.slice(-200);

    this.saveProgress(p);
    return p;
  },

  toggleList(key, id) {
    const list = this.get(key, []);
    const idx = list.indexOf(id);
    if (idx >= 0) {
      list.splice(idx, 1);
    } else {
      list.push(id);
    }
    this.set(key, list);
    return list;
  },
};
