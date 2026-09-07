---
type: change_log
schema_version: 1
scope: session
created: "2026-08-11"
updated: "2026-08-11"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[Symphony]]"
related:
  - "[[echo-forge-workers-shared-access]]"
  - "[[AGENTS OS - Fase 4]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo Forge workers — macOS Keychain access

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated + conflict-resolution.
- **Archivo(s):** `80-agents/tools/echo-forge-worker-access/`, `~/bin/echo-forge-worker`, [[echo-forge-workers-shared-access]], tres runbooks/known-errors de Symphony y [[AGENTS OS - Fase 4]].

## Motivo

- El owner aclaró que la contraseña compartida de `kor` para Zeus/Hera/Kronos sigue siendo operativa y necesita acceso uniforme desde Codex, Claude Code, Cursor y Antigravity en el Mac.

## Fuentes usadas

- Instrucción directa del owner, contrato de no persistir secretos, mapeo vigente de workers y comandos existentes de SSH/SCP/sudo/setup.

## Resolución aplicada

- La primera solución Keychain local fue reemplazada por instrucción explícita del owner: un único `credentials.env` plaintext vive junto al wrapper canónico, tiene warnings/TODO, modo `0600` y exclusión de Graphify. El instalador crea un symlink local como Graphify y el wrapper ofrece `ssh`, `sudo`, `scp-to`, `scp-from` y `setup-projects` sin imprimir la clave.

## Validación

- `bash -n` verde; `credentials.env` modo `0600`; symlink local resuelve al wrapper canónico; `status` y aliases Zeus/Hera/Kronos correctos. Smoke SSH read-only previo: timeout en los tres workers desde la red actual, por lo que la conectividad end-to-end queda pendiente de LAN/VPN/ruta.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** el valor vive exclusivamente en `credentials.env` por instrucción del owner y no se repite en este log ni en los runbooks; Graphify excluye el archivo.

## Rollback

- Editar sólo `credentials.env` si cambia el valor. Eliminar el archivo o el wrapper requiere instrucción explícita; no duplicar el password en otros documentos.
