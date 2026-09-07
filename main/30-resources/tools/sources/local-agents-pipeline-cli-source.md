---
type: source
schema_version: 1
status: active
area: "[[Personal]]"
source_url: https://github.com/melisource/fury_local-agents-pipeline-cli
repo: local-agents-pipeline-cli
path: .
author: Mercado Libre / melisource
published:
captured: "2026-08-26"
license: UNLICENSED
checksum:
supersedes:
superseded_by:
aliases:
  - local-agents-pipeline-cli repo
  - fuente local-agents-pipeline-cli
tags:
  - kind/source
created: "2026-08-26"
updated: "2026-08-26"
---

# local-agents-pipeline-cli-source

## Referencia

- **Origen resoluble:** repo `local-agents-pipeline-cli`, path `.`, relativo a [[Fuentes — Workspace de repositorios]] (`~/fuentes`); remoto upstream: `https://github.com/melisource/fury_local-agents-pipeline-cli`.
- **Fecha de captura:** 2026-08-26; checkout en `master`, commit `ac48d12`, alineado con `origin/master` al momento de la investigación.

## Alcance

- Código TypeScript de la CLI `zord`, prompts bundled en `zords/agents/`, configuración repo en `.zords/config.json`, tests Jest y documentación operativa en `README.md`.
- La evidencia usada para la página canónica cubre README, package manifest, configuración, todos los módulos bajo `src/`, todos los Zords bundled, tests, estado Git, tags/branches y ejecución local de build/lint/tests/smoke.

## Notas de provenance

- La revisión local ejecutó `npm ci --ignore-scripts`, `npm run build`, `npm run lint`, `npm test`, `node lib/cli.js list` y `node lib/cli.js assemble --dry-run`.
- Resultado observable: build OK; lint con 0 errores y 11 warnings en tests; 27 suites y 426 tests OK; cobertura Jest 96.58% statements, 88.17% branches, 91.10% functions y 96.72% lines.
- El smoke test mostró 8 Zords bundled disponibles, 7 habilitados para `manual` y asignaciones actuales según `.zords/config.json`: Codex para cinco Zords y Copilot para dos.
- La ejecución local usó Node `v26.7.0`, fuera del rango de engines declarado; sirve como evidencia de funcionamiento en este host, no como certificación de compatibilidad soportada.
- Hay warnings de npm sobre `always-auth` y dependencias transitivas deprecated (`inflight`, `glob`) durante la instalación; no se convierten aquí en vulnerabilidades sin un audit/versionado específico.

## Lifecycle

- **Supersedes:** —
- **Superseded by:** —
