#!/usr/bin/env node
// Gate mecanico del binding commit -> build. Decide si existe un build
// inmutable atado exactamente al commit del PR. Sale distinto de cero ante
// cualquier duda.
//
// Igual que validate-scope.mjs, no consulta Fury. Quien lo invoca obtiene
//   GET /api/proxy/versions/repositories/{repo}/versions?page=0&maxResults=<n>
// y guarda la respuesta tal cual en un archivo JSON.
//
// Uso:
//   node validate-build.mjs --sha <sha> --versions-file <ruta.json>
import { lstat, readFile } from 'node:fs/promises';
import process from 'node:process';

const shaPattern = /^[0-9a-f]{40}$/;
const MAX_VERSIONS_FILE_BYTES = 8 * 1024 * 1024;
// Estados observados: FINISHED para builds completos.
const finishedStatus = /^finished$/i;

function fail(reason) {
  console.error(`rio-sunset-update: build rechazado — ${reason}`);
  process.exitCode = 1;
}

function parseArgs(argv) {
  const allowed = new Set(['--sha', '--versions-file']);
  const out = new Map();
  for (let i = 0; i < argv.length; i += 2) {
    const key = argv[i];
    const value = argv[i + 1];
    if (!allowed.has(key)) return { error: `argumento desconocido: ${key}` };
    if (out.has(key)) return { error: `argumento repetido: ${key}` };
    if (value === undefined || value === '') return { error: `falta el valor de ${key}` };
    out.set(key, value);
  }
  if (out.size !== allowed.size) return { error: 'se requieren --sha y --versions-file' };
  return { values: out };
}

const parsed = parseArgs(process.argv.slice(2));
if (parsed.error) {
  fail(parsed.error);
} else {
  const sha = parsed.values.get('--sha');
  const versionsFile = parsed.values.get('--versions-file');

  // El SHA corto no sirve: la comparacion debe ser total o no es un binding.
  if (!shaPattern.test(sha)) {
    fail('el SHA debe ser el commit completo de 40 hexadecimales en minusculas.');
  } else {
    try {
      const info = await lstat(versionsFile);
      if (info.isSymbolicLink()) {
        const err = new Error('el archivo de versiones no puede ser un enlace');
        err.code = 'SYMLINK_REJECTED';
        throw err;
      }
      if (info.size > MAX_VERSIONS_FILE_BYTES) {
        const err = new Error('archivo de versiones demasiado grande');
        err.code = 'FILE_TOO_LARGE';
        throw err;
      }

      let payload;
      try {
        payload = JSON.parse(await readFile(versionsFile, 'utf8'));
      } catch {
        // No se reutiliza el error original: el mensaje de JSON.parse cita
        // fragmentos del contenido, que puede ser una respuesta sensible.
        const err = new Error('el archivo no contiene JSON valido');
        err.code = 'INVALID_JSON';
        throw err;
      }
      const entries = Array.isArray(payload) ? payload : payload?.versions;
      if (!Array.isArray(entries) || entries.length === 0) {
        const err = new Error('la respuesta de versiones no es una lista con elementos');
        err.code = 'INVALID_RESPONSE_SHAPE';
        throw err;
      }

      // Coincidencia por commit exacto. Nunca por branch, por string de version
      // ni por recencia: ahi es donde se despliega el artefacto equivocado.
      const matches = entries.filter((e) => e && typeof e.commit === 'string' && e.commit === sha);
      if (matches.length === 0) {
        fail('ningun build declara ese commit; no hay binding.');
      } else {
        const usable = [];
        const rejected = [];
        for (const entry of matches) {
          const reasons = [];
          if (typeof entry.status !== 'string' || !finishedStatus.test(entry.status)) {
            reasons.push(`status "${entry.status ?? 'ausente'}"`);
          }
          // disabled, igual que tags.productive mas abajo, ha llegado como string
          // en respuestas observadas: una comparacion estricta con el booleano
          // deja pasar un build deshabilitado disfrazado de "disabled": "true".
          if (entry.disabled === true || entry.disabled === 'true') reasons.push('build deshabilitado');
          const productive = entry?.tags?.productive;
          // tags.productive llega como string en la respuesta observada.
          if (productive === true || productive === 'true') reasons.push('build productivo');
          if (typeof entry.version !== 'string' || !entry.version) reasons.push('version ausente');
          if (reasons.length) rejected.push(`${entry.version ?? entry.id ?? 'sin id'}: ${reasons.join(', ')}`);
          else usable.push(entry);
        }

        if (usable.length === 0) {
          fail(`hay builds para ese commit pero ninguno es utilizable — ${rejected.join('; ')}.`);
        } else if (usable.length > 1) {
          fail(`${usable.length} builds utilizables para el mismo commit: ambiguo, resolver a mano.`);
        } else {
          const entry = usable[0];
          console.log(
            JSON.stringify({
              verdict: 'accepted',
              sha,
              version: entry.version,
              evidence: {
                status: entry.status,
                branch: entry.branch ?? null,
                productive: entry?.tags?.productive ?? null,
                disabled: entry.disabled ?? null,
              },
            }),
          );
        }
      }
    } catch (error) {
      // La causa completa va a stderr por separado: el mensaje de fail() se
      // mantiene parco a proposito, pero quien depure despues necesita el
      // .code y el mensaje propio (sin stack ni contenido de la respuesta), no solo "no se pudo validar (error)".
      console.error(`rio-sunset-update: detalle interno del gate de build — ${error?.code ?? 'SIN_CODIGO'}: ${error?.message ?? 'sin mensaje'}`);
      fail(`no se pudo validar (${error?.code ?? 'error'}).`);
    }
  }
}
