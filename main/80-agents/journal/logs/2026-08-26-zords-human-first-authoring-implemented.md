---
type: change_log
schema_version: 1
scope: session
created: "2026-08-26"
updated: "2026-08-26"
area: "[[Meli]]"
project: "[[Zords — Human-First Technical Authoring]]"
application:
entities:
  - "[[Zords — Human-First Technical Authoring]]"
  - "[[human-first-technical-writing]]"
related:
  - "[[2026-08-26-zords-human-first-technical-authoring-project]]"
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

# Implementación de Zords Human-First Technical Authoring

## Cambio

- **Tipo:** implemented
- **Archivo(s):** branch `feature/zords-technical-authoring` del repo `local-agents-pipeline-cli`; proyecto canónico de Zords actualizado.

## Motivo

- Agregar documentación técnica Human First como capacidad de authoring opt-in para humanos y agentes, sin cambiar el pipeline existente de code review.

## Resolución aplicada

- Se agregó `zord author document` y `zord author pr-description` con sources etiquetados, templates explícitos, stdin opcional, Git read-only y Markdown únicamente por stdout.
- Se agregó el writer bundled `human-first-technical-writing` con Codex `gpt-5.6-terra`, reasoning effort `high`, límites de input, rechazo de paths inseguros y delimitación de fuentes no confiables.
- El adapter Codex sólo agrega `model_reasoning_effort` cuando una invocación lo solicita; los callers legacy conservan su argv.
- No se modificaron `zordLoader`, runner, orchestrator, synthesis, contracts de review, SDD, filesystem output, publicación de PR ni persistencia de documentos.

## Validación

- `npm test -- --runInBand`: 458 tests passing; cobertura global 95.26% statements y 95.35% lines.
- `npm run build`, `npm run dist`, `git diff --check` y smoke de `zord --help`, `zord author --help`, `zord author document --help` pasan.
- `npm run lint -- --no-warn-ignored` queda sin errores; permanecen 11 warnings preexistentes en `tests/add.spec.ts` y `tests/cli.spec.ts`.
- `zord list` mantiene sólo reviewers y no descubre el writer bundled.

## Rollback

- G0–G2 quedan en `review` para aceptación humana; dogfood del PR y apertura de PR siguen pendientes.
- Rollback: retirar el registro CLI, `src/authoring/`, `src/commands/author.ts`, `zords/writers/` y el campo opcional de reasoning effort; los comandos legacy no requieren migración.
