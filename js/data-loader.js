let metadata = null;
let questions = [];
let bankIndex = null;
let activeBankId = "set1";

const BANK_STORAGE_KEY = "activeQuestionBank";

export async function loadData(bankId = null) {
  const cacheBust = Date.now();
  const [metaRes, indexRes] = await Promise.all([
    fetch(`./data/metadata.json?v=${cacheBust}`),
    fetch(`./data/questions-index.json?v=${cacheBust}`),
  ]);
  if (!metaRes.ok || !indexRes.ok) throw new Error("Failed to load exam metadata");

  metadata = await metaRes.json();
  bankIndex = await indexRes.json();

  const saved = localStorage.getItem(BANK_STORAGE_KEY);
  activeBankId = bankId || saved || bankIndex.banks[0]?.id || "set1";

  const bank = bankIndex.banks.find((b) => b.id === activeBankId) || bankIndex.banks[0];
  const dataVersion = bankIndex.version || cacheBust;
  const qRes = await fetch(`./data/${bank.file}?v=${dataVersion}`);
  if (!qRes.ok) throw new Error(`Failed to load ${bank.file}`);

  const qData = await qRes.json();
  questions = qData.questions || [];
  localStorage.setItem(BANK_STORAGE_KEY, activeBankId);
  return { metadata, questions, bankId: activeBankId, bank };
}

export async function switchBank(bankId) {
  if (bankId === activeBankId) return { metadata, questions, bankId: activeBankId };
  return loadData(bankId);
}

export function getActiveBankId() {
  return activeBankId;
}

export function getBankIndex() {
  return bankIndex;
}

export function getMetadata() {
  return metadata;
}

export function getAllQuestions() {
  return questions;
}

export function getCourseMap() {
  const map = {};
  metadata?.themes?.forEach((theme) => {
    theme.courses.forEach((c) => {
      map[c.id] = { ...c, themeId: theme.id, themeName: theme.name };
    });
  });
  return map;
}

export function filterQuestions(filters = {}) {
  let list = [...questions];
  const { course, difficulty, cognitive, theme, search, excludeIds = [] } = filters;

  if (course) list = list.filter((q) => q.courseId === course);
  if (theme) list = list.filter((q) => q.themeId === theme);
  if (difficulty) list = list.filter((q) => q.difficulty === difficulty);
  if (cognitive) list = list.filter((q) => q.cognitive === cognitive);
  if (excludeIds.length) list = list.filter((q) => !excludeIds.includes(q.id));
  if (search) {
    const s = search.toLowerCase();
    list = list.filter(
      (q) =>
        q.question.toLowerCase().includes(s) ||
        q.chapter.toLowerCase().includes(s) ||
        Object.values(q.options).some((o) => o.toLowerCase().includes(s))
    );
  }
  return list;
}

export function shuffle(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/** Sample mock exam: 100 questions weighted by blueprint course targets */
export function sampleMockExam() {
  const targets = {};
  metadata.themes.forEach((t) =>
    t.courses.forEach((c) => {
      targets[c.id] = c.items;
    })
  );

  const picked = [];
  for (const [courseId, count] of Object.entries(targets)) {
    const pool = shuffle(questions.filter((q) => q.courseId === courseId));
    picked.push(...pool.slice(0, count));
  }

  let result = picked;
  if (result.length < 100) {
    const extra = shuffle(questions.filter((q) => !result.find((r) => r.id === q.id)));
    result = [...result, ...extra.slice(0, 100 - result.length)];
  }
  return shuffle(result).slice(0, 100);
}

export function sampleRandom(n = 20, filters = {}) {
  return shuffle(filterQuestions(filters)).slice(0, n);
}

export function getQuestionById(id) {
  return questions.find((q) => q.id === id);
}
