import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const directory = path.dirname(fileURLToPath(import.meta.url));
const validator = path.join(directory, 'validate-input.mjs');

function run(args) {
  return spawnSync(process.execPath, [validator, ...args], { encoding: 'utf8' });
}

assert.equal(run(['rio-controlplane-signals']).status, 0);
assert.equal(run(['rio-entity-service']).status, 0);
assert.notEqual(run([]).status, 0);
assert.notEqual(run(['rio-controlplane-signals', 'extra']).status, 0);
assert.notEqual(run(['rio-controlplane-signals-typo']).status, 0);
assert.notEqual(run(['--upload-pack=touch /tmp/pwned']).status, 0);
assert.notEqual(run(['-rio-playmaker']).status, 0);
assert.notEqual(run(['Rio-Playmaker']).status, 0);
assert.notEqual(run(['']).status, 0);
console.log('validate-input tests passed');
