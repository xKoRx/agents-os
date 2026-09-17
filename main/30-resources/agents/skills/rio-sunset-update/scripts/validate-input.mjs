#!/usr/bin/env node
import { lstat, readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import process from 'node:process';

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const projectsPath = path.join(scriptDirectory, '..', 'references', 'projects.json');
const slugPattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

function fail(message) {
  console.error(`rio-sunset-update: ${message}`);
  process.exitCode = 1;
}

const args = process.argv.slice(2);
if (args.length !== 1) {
  fail('se requiere exactamente un argumento: <nombre_del_proyecto>.');
} else {
  const project = args[0];
  // El valor se emite como argumento de git/gh/fury, así que la forma del slug se
  // exige aquí y no sólo en la allowlist: projects.json es un archivo editable.
  if (!slugPattern.test(project)) {
    fail('el proyecto debe ser un slug en minúsculas sin caracteres especiales.');
  } else {
    try {
      if ((await lstat(projectsPath)).isSymbolicLink()) {
        throw new Error('el registro de proyectos no puede ser un enlace simbólico');
      }
      const registry = JSON.parse(await readFile(projectsPath, 'utf8'));
      if (registry.schemaVersion !== '1.0' || !Array.isArray(registry.projects)) {
        throw new Error('registro de proyectos inválido');
      }
      const allowed = registry.projects.some(
        (entry) => entry && typeof entry.name === 'string' && slugPattern.test(entry.name) && entry.name === project,
      );
      if (!allowed) {
        fail('el proyecto debe coincidir literalmente con un elemento de la allowlist.');
      } else {
        console.log(project);
      }
    } catch (error) {
      fail(`no se pudo validar el registro de proyectos (${error?.code ?? 'error'}).`);
    }
  }
}
