/**
 * URS external-evidence gate.
 * This gate deliberately refuses to certify external production/market readiness
 * unless independently verifiable evidence is supplied in the repository.
 */
import fs from 'node:fs';
import assert from 'node:assert/strict';

const requiredEvidence = [
  'docs/EXTERNAL_VERIFICATION.md',
  'docs/SECURITY_AUDIT.md',
  'docs/PRODUCTION_READINESS.md'
];

for (const file of requiredEvidence) {
  assert.ok(fs.existsSync(file), `${file} is required for external certification`);
}

const text = requiredEvidence
  .map(file => fs.readFileSync(file, 'utf8'))
  .join('\n');

assert.match(text, /independent|third-party|external/i);
assert.match(text, /audit|review/i);
assert.match(text, /reproducib|evidence/i);

console.log('URS EXTERNAL GATE: PASS');
console.log('External certification evidence is present for human review.');
