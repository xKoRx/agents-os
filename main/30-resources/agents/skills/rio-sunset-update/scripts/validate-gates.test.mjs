import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const directory = path.dirname(fileURLToPath(import.meta.url));
const scopeGate = path.join(directory, 'validate-scope.mjs');
const buildGate = path.join(directory, 'validate-build.mjs');
const work = mkdtempSync(path.join(tmpdir(), 'rio-sunset-gates-'));

const run = (script, args) => spawnSync(process.execPath, [script, ...args], { encoding: 'utf8' });
const fixture = (name, data) => {
  const file = path.join(work, name);
  writeFileSync(file, JSON.stringify(data));
  return file;
};

// ---------------------------------------------------------------------------
// validate-scope.mjs
// Fixture calcada en la respuesta real de rio-controlplane-clickhouse.
// Lo esencial: "prod" llega con productive=false, y "stage"/"test-events"
// muestran que ni criticality ni el nombre alcanzan por separado.
// ---------------------------------------------------------------------------
const scopes = fixture('scopes.json', [
  { name: 'test', application: 'rio-controlplane-clickhouse', productive: false, criticality: 'test' },
  { name: 'jobs1-test', application: 'rio-controlplane-clickhouse', productive: false, criticality: 'test' },
  { name: 'stage', application: 'rio-controlplane-clickhouse', productive: false, criticality: 'test' },
  { name: 'bq-stage-nonprod', application: 'rio-controlplane-clickhouse', productive: false, criticality: 'test' },
  { name: 'prod', application: 'rio-controlplane-clickhouse', productive: false, criticality: 'low' },
  { name: 'test-events', application: 'rio-controlplane-clickhouse', productive: false, criticality: 'low' },
  { name: 'consumer-prod', application: 'rio-controlplane-clickhouse', productive: true, criticality: 'medium' },
  { name: 'sin-criticality', application: 'rio-controlplane-clickhouse', productive: false },
  { name: 'ajeno', application: 'otra-aplicacion', productive: false, criticality: 'test' },
  { name: 'duplicado', application: 'rio-controlplane-clickhouse', productive: false, criticality: 'test' },
  { name: 'duplicado', application: 'rio-controlplane-clickhouse', productive: false, criticality: 'test' },
]);

const scopeArgs = (scope, file = scopes) => [
  '--project', 'rio-controlplane-clickhouse', '--scope', scope, '--scopes-file', file,
];

// Acepta: criticality test, no productivo, sin marcador de stage.
assert.equal(run(scopeGate, scopeArgs('test')).status, 0, 'test debe aceptarse');
assert.equal(run(scopeGate, scopeArgs('jobs1-test')).status, 0, 'jobs1-test debe aceptarse');

// El caso que motivo este gate: productive=false NO autoriza.
const prod = run(scopeGate, scopeArgs('prod'));
assert.notEqual(prod.status, 0, 'prod NUNCA debe aceptarse');
assert.match(prod.stderr, /criticality es "low"/);

// stage no cuenta como test, aunque criticality diga test.
assert.notEqual(run(scopeGate, scopeArgs('stage')).status, 0, 'stage debe rechazarse');
assert.notEqual(run(scopeGate, scopeArgs('bq-stage-nonprod')).status, 0, 'bq-stage-nonprod debe rechazarse');

// Nombre con "test" pero productivo en la UI: lo frena criticality.
assert.notEqual(run(scopeGate, scopeArgs('test-events')).status, 0, 'test-events debe rechazarse');

// productive=true niega.
assert.notEqual(run(scopeGate, scopeArgs('consumer-prod')).status, 0, 'consumer-prod debe rechazarse');

// Datos faltantes, ambiguos, ajenos o inexistentes: siempre cerrado.
assert.notEqual(run(scopeGate, scopeArgs('sin-criticality')).status, 0);
assert.notEqual(run(scopeGate, scopeArgs('ajeno')).status, 0);
assert.notEqual(run(scopeGate, scopeArgs('duplicado')).status, 0);
assert.notEqual(run(scopeGate, scopeArgs('no-existe')).status, 0);

// Proyecto fuera de la allowlist.
assert.notEqual(
  run(scopeGate, ['--project', 'proyecto-ajeno', '--scope', 'test', '--scopes-file', scopes]).status, 0,
);

// Argumentos: nada de extras, repetidos, faltantes o inyeccion por opcion.
assert.notEqual(run(scopeGate, []).status, 0);
assert.notEqual(run(scopeGate, [...scopeArgs('test'), '--extra', 'x']).status, 0);
assert.notEqual(run(scopeGate, ['--project', 'rio-playmaker', '--scope', '--upload-pack=x', '--scopes-file', scopes]).status, 0);
assert.notEqual(run(scopeGate, ['--scope', 'test', '--scopes-file', scopes]).status, 0);

// Payload corrupto o vacio.
assert.notEqual(run(scopeGate, scopeArgs('test', fixture('vacio.json', []))).status, 0);
assert.notEqual(run(scopeGate, scopeArgs('test', fixture('objeto.json', { nope: true }))).status, 0);

// ---------------------------------------------------------------------------
// Casos reales medidos el 2026-09-16 sobre los 11 proyectos de la allowlist.
// Cada fila viene de la respuesta de /fury_read/.../scopes, no es inventada.
// ---------------------------------------------------------------------------
const reales = fixture('reales.json', [
  // rio-controlplane-fury: criticality "test" CONVIVE con productive true.
  // Sin la negacion por productive, estos dos se aceptarian.
  { name: 'prod-default-test--tp', application: 'rio-controlplane-fury', productive: true, criticality: 'test' },
  { name: 'prod-test--tp-nonprod', application: 'rio-controlplane-fury', productive: true, criticality: 'test' },
  { name: 'orchestrator-web-nonprod', application: 'rio-controlplane-fury', productive: false, criticality: 'test' },
  { name: 'stage-nonprod', application: 'rio-controlplane-fury', productive: false, criticality: 'test' },
  // rio-controlplane-flink: "staging" no es "stage"; tambien aparece "develop".
  { name: 'staging-nonprod', application: 'rio-controlplane-flink', productive: false, criticality: 'test' },
  { name: 'staging-consumer-nonprod-nonprod', application: 'rio-controlplane-flink', productive: false, criticality: 'test' },
  { name: 'develop', application: 'rio-controlplane-flink', productive: false, criticality: 'test' },
  { name: 'jobs-test-nonprod', application: 'rio-controlplane-flink', productive: false, criticality: 'test' },
  { name: 'consumer-stage', application: 'rio-controlplane-flink', productive: true, criticality: 'high' },
  // rio-materializer: "dev" suelto y varios stage con prefijo.
  { name: 'dev', application: 'rio-materializer', productive: false, criticality: 'test' },
  { name: 'api-stage', application: 'rio-materializer', productive: false, criticality: 'test' },
  { name: 'stream-production', application: 'rio-materializer', productive: false, criticality: 'low' },
  { name: 'work-queues-test', application: 'rio-materializer', productive: false, criticality: 'test' },
  // rio-entity-service y rio-playmaker.
  { name: 'prod-nonsite', application: 'rio-entity-service', productive: false, criticality: 'low' },
  { name: 'test-columnupdates-nonprod-nonprod', application: 'rio-entity-service', productive: false, criticality: 'test' },
  { name: 'bq-consumer-production', application: 'rio-playmaker', productive: true, criticality: 'medium' },
  { name: 'test4-nonprod', application: 'rio-playmaker', productive: false, criticality: 'test' },
]);

const real = (project, scope) => run(scopeGate, ['--project', project, '--scope', scope, '--scopes-file', reales]);

// Aceptados: criticality test, no productivo, sin marcador de entorno no-test.
for (const [project, scope] of [
  ['rio-controlplane-fury', 'orchestrator-web-nonprod'],
  ['rio-controlplane-flink', 'jobs-test-nonprod'],
  ['rio-materializer', 'work-queues-test'],
  ['rio-entity-service', 'test-columnupdates-nonprod-nonprod'],
  ['rio-playmaker', 'test4-nonprod'],
]) {
  assert.equal(real(project, scope).status, 0, `${scope} debe aceptarse`);
}

// criticality "test" + productive true. El caso que prueba que la negacion por
// productive es imprescindible, no redundante.
for (const scope of ['prod-default-test--tp', 'prod-test--tp-nonprod']) {
  const r = real('rio-controlplane-fury', scope);
  assert.notEqual(r.status, 0, `${scope} NUNCA debe aceptarse`);
  assert.match(r.stderr, /productive es true/);
}

// stage y staging, con y sin prefijo. "staging" no lo cubria el patron inicial.
assert.notEqual(real('rio-controlplane-fury', 'stage-nonprod').status, 0);
assert.notEqual(real('rio-controlplane-flink', 'staging-nonprod').status, 0);
assert.notEqual(real('rio-controlplane-flink', 'staging-consumer-nonprod-nonprod').status, 0);
assert.notEqual(real('rio-materializer', 'api-stage').status, 0);

// dev y develop tampoco cuentan como test.
assert.notEqual(real('rio-controlplane-flink', 'develop').status, 0);
assert.notEqual(real('rio-materializer', 'dev').status, 0);

// Nombres productivos frenados por criticality.
assert.notEqual(real('rio-materializer', 'stream-production').status, 0);
assert.notEqual(real('rio-entity-service', 'prod-nonsite').status, 0);
assert.notEqual(real('rio-playmaker', 'bq-consumer-production').status, 0);
assert.notEqual(real('rio-controlplane-flink', 'consumer-stage').status, 0);

// ---------------------------------------------------------------------------
// validate-build.mjs
// ---------------------------------------------------------------------------
const good = '329fe7be905215f52f9f307113f0759db1799954';
const other = 'a'.repeat(40);
const versions = fixture('versions.json', [
  { version: '202609.16.1-sb4', branch: 'feature/x', commit: good, status: 'FINISHED', disabled: false, tags: { productive: 'false' } },
  { version: '202609.16.0-prod', branch: 'master', commit: other, status: 'FINISHED', disabled: false, tags: { productive: 'true' } },
  { version: '202609.15.0-run', branch: 'feature/y', commit: 'b'.repeat(40), status: 'RUNNING', disabled: false, tags: { productive: 'false' } },
  { version: '202609.14.0-off', branch: 'feature/z', commit: 'c'.repeat(40), status: 'FINISHED', disabled: true, tags: { productive: 'false' } },
]);

const buildArgs = (sha, file = versions) => ['--sha', sha, '--versions-file', file];

assert.equal(run(buildGate, buildArgs(good)).status, 0, 'commit exacto y build sano debe aceptarse');

// SHA corto no es binding.
assert.notEqual(run(buildGate, buildArgs(good.slice(0, 12))).status, 0);
// Sin build para ese commit.
assert.notEqual(run(buildGate, buildArgs('d'.repeat(40))).status, 0);
// Build productivo, no finalizado o deshabilitado.
assert.notEqual(run(buildGate, buildArgs(other)).status, 0, 'build productivo debe rechazarse');
assert.notEqual(run(buildGate, buildArgs('b'.repeat(40))).status, 0, 'build no finalizado debe rechazarse');
assert.notEqual(run(buildGate, buildArgs('c'.repeat(40))).status, 0, 'build deshabilitado debe rechazarse');

// Dos builds utilizables para el mismo commit: ambiguo.
const ambiguous = fixture('ambiguo.json', [
  { version: 'v1', commit: good, status: 'FINISHED', disabled: false, tags: { productive: 'false' } },
  { version: 'v2', commit: good, status: 'FINISHED', disabled: false, tags: { productive: 'false' } },
]);
assert.notEqual(run(buildGate, buildArgs(good, ambiguous)).status, 0);

// Argumentos.
assert.notEqual(run(buildGate, []).status, 0);
assert.notEqual(run(buildGate, [...buildArgs(good), '--extra', 'x']).status, 0);
assert.notEqual(run(buildGate, buildArgs(good, fixture('vacio2.json', []))).status, 0);

console.log('validate-scope and validate-build tests passed');
