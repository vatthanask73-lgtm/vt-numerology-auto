const test = require('node:test');
const assert = require('node:assert/strict');
const numerology = require('../src');

test('calculateLifePath reduces birth dates correctly', () => {
  assert.equal(numerology.calculateLifePath('1990-08-15'), 6);
  assert.equal(numerology.calculateLifePath('11/11/1991'), 6);
});

test('calculateExpressionNumber reduces full names', () => {
  assert.equal(numerology.calculateExpressionNumber('Alice'), 3);
  assert.equal(numerology.calculateExpressionNumber('John'), 2);
});

test('compatibility is symmetric and same-date returns 100', () => {
  assert.equal(numerology.calculateCompatibility('1990-08-15', '1990-08-15'), 100);
});
