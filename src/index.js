const LETTER_VALUES = {
  A: 1, B: 2, C: 3, D: 4, E: 5, F: 6,
  G: 7, H: 8, I: 9, J: 1, K: 2, L: 3,
  M: 4, N: 5, O: 6, P: 7, Q: 8, R: 9,
  S: 1, T: 2, U: 3, V: 4, W: 5, X: 6,
  Y: 7, Z: 8,
};

const MASTER_NUMBERS = new Set([11, 22, 33]);
const VOWELS = new Set(['A', 'E', 'I', 'O', 'U', 'Y']);

function reduceNumber(value, { keepMasterNumbers = false } = {}) {
  let total = Math.abs(Number(value) || 0);
  while (total > 9 && (!keepMasterNumbers || !MASTER_NUMBERS.has(total))) {
    total = String(total)
      .split('')
      .reduce((sum, digit) => sum + Number(digit), 0);
  }
  return total;
}

function parseDate(value) {
  if (value instanceof Date && !Number.isNaN(value.getTime())) return value;
  if (typeof value === 'string') {
    const trimmed = value.trim();
    if (!trimmed) throw new Error('Date string cannot be blank');

    const isoMatch = trimmed.match(/^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$/);
    if (isoMatch) {
      const [, year, month, day] = isoMatch;
      const date = new Date(Date.UTC(Number(year), Number(month) - 1, Number(day)));
      if (!Number.isNaN(date.getTime())) return date;
    }

    const slashMatch = trimmed.match(/^(\d{1,2})[/-](\d{1,2})[/-](\d{4})$/);
    if (slashMatch) {
      const [, first, second, year] = slashMatch;
      const firstValue = Number(first);
      const secondValue = Number(second);
      const isDayFirst = firstValue > 12 || (secondValue <= 12 && firstValue > secondValue);
      const day = isDayFirst ? firstValue : secondValue;
      const month = isDayFirst ? secondValue : firstValue;
      const date = new Date(Date.UTC(Number(year), month - 1, day));
      if (!Number.isNaN(date.getTime())) return date;
    }

    const digits = trimmed.replace(/\D/g, '');
    if (digits.length === 8) {
      const year = digits.slice(0, 4);
      const month = digits.slice(4, 6);
      const day = digits.slice(6, 8);
      const date = new Date(Date.UTC(Number(year), Number(month) - 1, Number(day)));
      if (!Number.isNaN(date.getTime())) return date;
    }
  }
  throw new TypeError(`Unsupported date value: ${String(value)}`);
}

function calculateLifePath(dateValue) {
  const date = parseDate(dateValue);
  const raw = `${date.getUTCFullYear()}${String(date.getUTCMonth() + 1).padStart(2, '0')}${String(date.getUTCDate()).padStart(2, '0')}`;
  const total = Array.from(raw).reduce((sum, ch) => sum + Number(ch), 0);
  return reduceNumber(total, { keepMasterNumbers: false });
}

function lettersToDigits(name, selector, { keepMasterNumbers = false } = {}) {
  const letters = Array.from(String(name || '').toUpperCase()).filter((ch) => /[A-Z]/.test(ch));
  if (!letters.length) throw new Error('Name does not contain letters');
  const filtered = selector === 'vowels'
    ? letters.filter((ch) => VOWELS.has(ch))
    : selector === 'consonants'
      ? letters.filter((ch) => !VOWELS.has(ch))
      : letters;
  if (!filtered.length) throw new Error('Selector produced no letters');
  const total = filtered.reduce((sum, ch) => sum + (LETTER_VALUES[ch] || 0), 0);
  return reduceNumber(total, { keepMasterNumbers });
}

function calculateExpressionNumber(name, { keepMasterNumbers = false } = {}) {
  const letters = Array.from(String(name || '').toUpperCase()).filter((ch) => /[A-Z]/.test(ch));
  if (!letters.length) throw new Error('Name does not contain letters');
  const total = letters.reduce((sum, ch) => sum + (LETTER_VALUES[ch] || 0), 0);
  return reduceNumber(total, { keepMasterNumbers });
}

function calculateNameNumber(name, options) {
  return calculateExpressionNumber(name, options);
}

function calculateSoulNumber(name, options) {
  return lettersToDigits(name, 'vowels', options);
}

function calculatePersonalityNumber(name, options) {
  return lettersToDigits(name, 'consonants', options);
}

function calculateCompatibility(left, right) {
  const leftPath = calculateLifePath(left);
  const rightPath = calculateLifePath(right);
  const delta = Math.abs(leftPath - rightPath);
  const score = 100 - Math.min(delta * 10, 90);
  return Math.max(0, score);
}

function calculateReport(name, birthDate) {
  return {
    life_path: calculateLifePath(birthDate),
    expression_number: calculateExpressionNumber(name),
    soul_number: calculateSoulNumber(name),
    personality_number: calculatePersonalityNumber(name),
  };
}

module.exports = {
  MASTER_NUMBERS,
  reduceNumber,
  calculateLifePath,
  calculateExpressionNumber,
  calculateNameNumber,
  calculateSoulNumber,
  calculatePersonalityNumber,
  calculateCompatibility,
  calculateReport,
};

module.exports.default = module.exports;
