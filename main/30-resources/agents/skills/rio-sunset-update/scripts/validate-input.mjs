#!/usr/bin/env node
// Gate de forma de la invocacion. No consulta la red y no lee ningun registro:
// valida unicamente que haya exactamente un proyecto, que su nombre tenga forma
// de slug, y que la unica bandera admitida sea la literal.
//
// Deliberadamente NO valida que el proyecto exista: eso se verifica contra Fury
// en la primera fase de red (ver references/workflow.md, "Validar el proyecto
// contra Fury"). Este gate existe para fallar cerrado sin red, en cualquier
// cliente: sin argumento no hay proyecto sobre el que actuar, asi que un agente
// que llegue a esta skill por iniciativa propia no puede hacer nada.
//
// Uso:
//   node validate-input.mjs <project_name> [--attempt-migration]
import process from 'node:process';

// Unica bandera admitida. Literal, sin abreviaturas ni variantes.
const MIGRATION_FLAG = '--attempt-migration';
// El nombre viaja a lineas de comando (git, fury), asi que se exige forma de
// slug aqui y no solo mas adelante.
const slugPattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

function fail(message) {
  console.error(`rio-sunset-update: ${message}`);
  process.exitCode = 1;
}

const args = process.argv.slice(2);
const flags = args.filter((a) => a.startsWith('-'));
const positional = args.filter((a) => !a.startsWith('-'));
const unknownFlag = flags.find((f) => f !== MIGRATION_FLAG);

if (positional.length !== 1) {
  fail('se requiere exactamente un proyecto: <project_name>.');
} else if (unknownFlag) {
  fail(`bandera desconocida: se admite solo ${MIGRATION_FLAG}.`);
} else if (flags.length > 1) {
  fail('bandera repetida.');
} else if (!slugPattern.test(positional[0])) {
  fail('el nombre del proyecto debe ser un slug en minusculas, sin caracteres especiales.');
} else {
  const project = positional[0];
  const migrationMode = flags.length === 1;
  console.log(migrationMode ? `${project} ${MIGRATION_FLAG}` : project);
}
