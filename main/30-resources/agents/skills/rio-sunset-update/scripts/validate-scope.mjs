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
import process from 'node:process';

const slugPattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
// Un scope puede llamarse casi cualquier cosa, pero no aceptamos formas que
// luego viajarian a una linea de comando.
const scopePattern = /^[A-Za-z0-9][A-Za-z0-9._-]*$/;
// Entornos que NO son de prueba, detectados como segmento del nombre. Se usan
// SOLO para negar: negar por nombre es conservador, autorizar por nombre es lo
// que resulto peligroso.
//
// Medido sobre los proyectos RIO: "stage" y "staging" conviven
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
      {
        const info = await lstat(scopesFile);
        if (info.isSymbolicLink()) {
          const err = new Error('el archivo de scopes no puede ser un enlace');
          err.code = 'SYMLINK_REJECTED';
          throw err;
        }
        if (info.size > MAX_SCOPES_FILE_BYTES) {
          const err = new Error('archivo de scopes demasiado grande');
          err.code = 'FILE_TOO_LARGE';
          throw err;
        }

        let payload;
        try {
          payload = JSON.parse(await readFile(scopesFile, 'utf8'));
        } catch {
          // No se reutiliza el error original: el mensaje de JSON.parse cita
          // fragmentos del contenido, que puede ser una respuesta sensible.
          const err = new Error('el archivo no contiene JSON valido');
          err.code = 'INVALID_JSON';
          throw err;
        }
        const entries = Array.isArray(payload) ? payload : payload?.scopes;
        if (!Array.isArray(entries) || entries.length === 0) {
          const err = new Error('la respuesta de scopes no es una lista con elementos');
          err.code = 'INVALID_RESPONSE_SHAPE';
          throw err;
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
          //    Obligatoria: sin application no hay prueba de pertenencia, y un
          //    payload malformado o de otro proyecto no puede autorizar el deploy.
          if (typeof entry.application !== 'string' || !entry.application) {
            reasons.push('application ausente o no es texto: no se puede probar la pertenencia al proyecto');
          } else if (entry.application !== project) {
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
          //    El campo ha llegado como string en respuestas observadas: una
          //    comparacion estricta con el booleano deja pasar "productive": "true".
          if (entry.productive === true || entry.productive === 'true') {
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
      // La causa completa va a stderr por separado: el mensaje de fail() se
      // mantiene parco a proposito, pero quien depure despues necesita el
      // .code y el mensaje propio (sin stack ni contenido de la respuesta), no solo "no se pudo validar (error)".
      console.error(`rio-sunset-update: detalle interno del gate de scope — ${error?.code ?? 'SIN_CODIGO'}: ${error?.message ?? 'sin mensaje'}`);
      fail(`no se pudo validar (${error?.code ?? 'error'}).`);
    }
  }
}
