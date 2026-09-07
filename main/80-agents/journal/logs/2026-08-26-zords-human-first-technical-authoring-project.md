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
  - "[[2026-08-26-human-first-technical-writing]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-08-26-zords-human-first-framing-session-feedback]]"
  - "[[2026-08-26-zords-human-first-reindex-gate-graphify-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Creación y Fase 0 del proyecto Zords — Human-First Technical Authoring

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `10-projects/Meli/Zords — Human-First Technical Authoring/Zords — Human-First Technical Authoring.md`

## Motivo

- Crear una fuente durable y ejecutable para integrar `human-first-technical-writing` en Zords como capacidad transversal de autoría documental, con PR descriptions como primera recipe y no como techo del producto.

## Fuentes usadas

- Visión y decisiones entregadas por el usuario durante la sesión.
- `80-agents/skills/human-first-technical-writing/SKILL.md`.
- Inspección read-only del baseline de `local-agents-pipeline-cli` y de la relación Grimoire/SDD/Zords.

## Resolución aplicada

- Se documentaron tesis cognitiva, alcance, arquitectura, contratos, jerarquía de fuentes, modelo Terra, almacenamiento, seguridad, requisitos, decisiones, tareas, cinco paquetes autónomos, gates, evals, rollout y rollback.
- Se fijó `gpt-5.6-terra + high` como baseline reproducible y `xhigh` como perfil opt-in sujeto a evaluación comparativa.
- Se mantuvo a Grimoire como productor de specs y a Zords como consumidor read-only para authoring.
- Se creó `feature/zords-technical-authoring` desde `master@ac48d123` y se ejecutó F0: contratos documentales compilables, `task` con default legacy `review`, `reasoning_effort` validado y propagado al adapter Codex mediante `model_reasoning_effort`.
- Se dejó G0 en `review`; T0.1 (issue tracker) permanece pendiente porque esta sesión no tiene conector de issue tracking habilitado.

## Validación

- `validate_plan.py`: 5 fases, 5 gates, 5 dispatches, 2 referencias portables, 0 errores y 0 warnings.
- `validate_schema_contract.py`: contrato global version 1, 0 errores.
- Scan de placeholders y paths locales: sin hallazgos en la nota del proyecto.
- `lint.py --strict` sobre proyecto, change log y feedback: 0 errores y 0 warnings. `graphify-obsidian update` quedó bloqueado antes de indexar por 12 errores y 6 warnings globales ajenos a estos artefactos; ver [[2026-08-26-zords-human-first-reindex-gate-graphify-feedback]].
- Repo F0: `npm test -- --runInBand` con 433 tests passing, `npm run build` OK y `npm run lint` sin errores; permanecen 11 warnings preexistentes en `tests/add.spec.ts` y `tests/cli.spec.ts`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit de F0 y restaurar el estado de la nota si la iniciativa se descarta; la branch es local y no se publicó.
