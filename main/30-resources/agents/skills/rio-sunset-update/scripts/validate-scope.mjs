#!/usr/bin/env node
// Gate mecanico del scope de deploy. Decide una sola cosa: si el scope
// indicado puede recibir un deploy de prueba. Sale distinto de cero ante
// cualquier duda.
//
// El script no consulta Fury: un proceso Node no tiene la sesion autenticada.
// Quien lo invoca debe obtener la respuesta de
//   GET /api/proxy/fury_read/applications/{app}/scopes?show_new_criticality=true
// y guardarla tal cual en un archivo JSON. El valor de este gate es que la
// REGLA queda en codigo auditable y falla cerrada, en lugar de vivir en prosa
// que un agente puede no leer.
//
// Uso:
//   node validate-scope.mjs --project <proyecto> --scope <scope> --scopes-file <ruta.json>
import { lstat, readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import process from 'node:process';

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const projectsPath = path.join(scriptDirectory, '..', 'references', 'projects.json');
const slugPattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
// Un scope puede llamarse casi cualquier cosa, pero no aceptamos formas que
// luego viajarian a una linea de comando.
const scopePattern = /^[A-Za-z0-9][A-Za-z0-9._-]*$/;
// Entornos que NO son de prueba, detectados como segmento del nombre. Se usan
// SOLO para negar: negar por nombre es conservador, autorizar por nombre es lo
// que resulto peligroso.
//
// Medido sobre los 11 proyectos de la allowlist: "stage" y "staging" conviven
// ("stage", "api-stage", "bq-stage-nonprod", "staging-nonprod",
// "staging-consumer-nonprod-nonprod"), y "dev"/"develop" aparecen con
// criticality test. Todos llegan como criticality "test", asi que ese campo no
// puede distinguirlos: hay que nombrarlos.
const nonTestEnvironments = ['stage', 'staging', 'dev', 'develop'];
const nonTestMarker = new RegExp(`(^|[-_.])(${nonTestEnvironments.join('|')})($|[-_.])`, 'i');
const MAX_SCOPES_FILE_BYTES = 4 * 1024 * 1024;

function fail(reason) {
  console.error(`rio-sunset-update: scope rechazado — ${reason}`);
  process.exitCode = 1;
}

function parseArgs(argv) {
  const allowed = new Set(['--project', '--scope', '--scopes-file']);
  const out = new Map();
  for (let i = 0; i < argv.length; i += 2) {
    const key = argv[i];
    const value = argv[i + 1];
    if (!allowed.has(key)) return { error: `argumento desconocido: ${key}` };
    if (out.has(key)) return { error: `argumento repetido: ${key}` };
    if (value === undefined || value === '') return { error: `falta el valor de ${key}` };
    out.set(key, value);
  }
  if (out.size !== allowed.size) return { error: 'se requieren --project, --scope y --scopes-file' };
  return { values: out };
}

const parsed = parseArgs(process.argv.slice(2));
if (parsed.error) {
  fail(parsed.error);
} else {
  const project = parsed.values.get('--project');
  const scope = parsed.values.get('--scope');
  const scopesFile = parsed.values.get('--scopes-file');

  if (!slugPattern.test(project)) {
    fail('el proyecto debe ser un slug en minusculas.');
  } else if (!scopePattern.test(scope)) {
    fail('el nombre del scope tiene caracteres no admitidos.');
  } else {
    try {
      // 1. El proyecto debe pertenecer a la allowlist, misma fuente unica que el gate de entrada.
      if ((await lstat(projectsPath)).isSymbolicLink()) throw new Error('registro de proyectos enlazado');
      const registry = JSON.parse(await readFile(projectsPath, 'utf8'));
      if (registry.schemaVersion !== '1.0' || !Array.isArray(registry.projects)) {
        throw new Error('registro de proyectos invalido');
      }
      const known = registry.projects.some((entry) => entry && entry.name === project);
      if (!known) {
        fail('el proyecto no pertenece a la allowlist.');
      } else {
        const info = await lstat(scopesFile);
        if (info.isSymbolicLink()) throw new Error('el archivo de scopes no puede ser un enlace');
        if (info.size > MAX_SCOPES_FILE_BYTES) throw new Error('archivo de scopes demasiado grande');

        const payload = JSON.parse(await readFile(scopesFile, 'utf8'));
        const entries = Array.isArray(payload) ? payload : payload?.scopes;
        if (!Array.isArray(entries) || entries.length === 0) {
          throw new Error('la respuesta de scopes no es una lista con elementos');
        }

        // 2. Exactamente una coincidencia literal por nombre.
        const matches = entries.filter((e) => e && typeof e.name === 'string' && e.name === scope);
        if (matches.length === 0) {
          fail(`el scope "${scope}" no existe en la respuesta de scopes de ${project}.`);
        } else if (matches.length > 1) {
          fail(`el scope "${scope}" aparece ${matches.length} veces: ambiguo.`);
        } else {
          const entry = matches[0];
          const reasons = [];

          // 3. Pertenencia a la aplicacion, cuando el payload la declara.
          if (typeof entry.application === 'string' && entry.application !== project) {
            reasons.push(`pertenece a ${entry.application}, no a ${project}`);
          }

          // 4. criticality === "test" es la UNICA senal que autoriza.
          if (typeof entry.criticality !== 'string') {
            reasons.push('criticality ausente o no es texto');
          } else if (entry.criticality !== 'test') {
            reasons.push(`criticality es "${entry.criticality}", no "test"`);
          }

          // 5. productive sirve solo para NEGAR. Nunca para autorizar: se observo
          //    productive=false en scopes productivos, incluido uno llamado "prod".
          if (entry.productive === true) {
            reasons.push('productive es true');
          }

          // 6. El nombre solo niega. stage/staging/dev/develop no cuentan como test.
          const marker = scope.match(nonTestMarker);
          if (marker) {
            reasons.push(`el nombre contiene "${marker[2].toLowerCase()}", que no cuenta como entorno de test`);
          }

          if (reasons.length) {
            fail(`${reasons.join('; ')}.`);
          } else {
            console.log(
              JSON.stringify({
                verdict: 'accepted',
                project,
                scope,
                evidence: {
                  criticality: entry.criticality,
                  productive: entry.productive ?? null,
                  application: entry.application ?? null,
                  type: entry.type ?? null,
                },
              }),
            );
          }
        }
      }
    } catch (error) {
      // Sin detalles del sistema de archivos ni del contenido en el mensaje.
      fail(`no se pudo validar (${error?.code ?? 'error'}).`);
    }
  }
}
