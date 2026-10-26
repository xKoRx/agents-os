import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const directory = path.dirname(fileURLToPath(import.meta.url));
const validator = path.join(directory, 'validate-input.mjs');

function run(args) {
  return spawnSync(process.execPath, [validator, ...args], { encoding: 'utf8' });
}

// Cualquier nombre con forma de slug se acepta: la existencia se verifica
// contra Fury en la primera fase de red, no aca.
assert.equal(run(['rio-controlplane-signals']).status, 0);
assert.equal(run(['rio-entity-service']).status, 0);
assert.equal(run(['ads-signals-collector-api']).status, 0, 'cualquier app del ecosistema');
assert.equal(run(['rio-sdk-events']).status, 0, 'incluidas las librerias');
assert.notEqual(run([]).status, 0);
assert.notEqual(run(['rio-controlplane-signals', 'extra']).status, 0);
assert.notEqual(run(['--upload-pack=touch /tmp/pwned']).status, 0);
assert.notEqual(run(['-rio-playmaker']).status, 0);
assert.notEqual(run(['Rio-Playmaker']).status, 0);
assert.notEqual(run(['']).status, 0);

// Forma invalida: mayusculas, guion inicial, vacio, caracteres raros.
assert.notEqual(run(['rio_controlplane_signals']).status, 0, 'guion bajo no es slug');
assert.notEqual(run(['rio--doble']).status, 0, 'doble guion no es slug');
assert.notEqual(run(['rio-controlplane-']).status, 0, 'guion final no es slug');

// Modo de intento de migracion: unica bandera admitida, literal.
const conFlag = run(['rio-controlplane-clickhouse', '--attempt-migration']);
assert.equal(conFlag.status, 0, 'el proyecto con la bandera debe aceptarse');
assert.match(conFlag.stdout, /--attempt-migration/, 'la salida debe declarar el modo');
assert.equal(run(['--attempt-migration', 'rio-controlplane-clickhouse']).status, 0, 'el orden no importa');

// Sin la bandera, la salida no debe mencionar el modo.
assert.doesNotMatch(run(['rio-playmaker']).stdout, /attempt-migration/);

// Variantes, abreviaturas y banderas ajenas: rechazadas.
assert.notEqual(run(['rio-playmaker', '--attempt-migration=si']).status, 0);
assert.notEqual(run(['rio-playmaker', '--attempt_migration']).status, 0);
assert.notEqual(run(['rio-playmaker', '--migration']).status, 0);
assert.notEqual(run(['rio-playmaker', '--force']).status, 0);
assert.notEqual(run(['rio-playmaker', '-i']).status, 0);
// Bandera repetida y dos proyectos: rechazados.
assert.notEqual(run(['rio-playmaker', '--attempt-migration', '--attempt-migration']).status, 0);
assert.notEqual(run(['rio-playmaker', 'rio-materializer', '--attempt-migration']).status, 0);
// La bandera sola, sin proyecto: rechazada.
assert.notEqual(run(['--attempt-migration']).status, 0);

console.log('validate-input tests passed');
