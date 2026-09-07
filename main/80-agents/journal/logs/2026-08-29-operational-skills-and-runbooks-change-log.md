---
type: change_log
schema_version: 1
scope: session
created: "2026-08-29"
updated: "2026-08-29"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Echo Forge]]"
related:
  - "[[2026-08-29-durable-artifact-verified-reads-final-e2e-normal]]"
  - "[[e2e-gated-validation]]"
aliases: []
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-FINAL-E2E-NORMAL
source_feedbacks:
  - "[[2026-08-29-symphony-worker-observability-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-29-operational-skills-and-runbooks-change-log

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `80-agents/skills/e2e-gated-validation/SKILL.md` (nueva, orquestadora)
  - `80-agents/skills/release-certification/SKILL.md` (nueva)
  - `80-agents/skills/deployment-proof/SKILL.md` (nueva)
  - `80-agents/skills/readonly-production-probe/SKILL.md` (nueva)
  - `80-agents/skills/distributed-incident-triage/SKILL.md` (nueva)
  - `80-agents/skills/evidence-channel-discovery/SKILL.md` (nueva)
  - `80-agents/skills/write-once-conflict-triage/SKILL.md` (nueva)
  - `80-agents/memory/public/runbook/symphony/symphony-release-certification.md` (nuevo)
  - `80-agents/memory/public/runbook/symphony/symphony-worker-runtime-proof.md` (nuevo, incluye matriz de canales verificada)
  - `80-agents/memory/public/runbook/symphony/symphony-prod-probe.md` (nuevo)
  - `80-agents/memory/public/runbook/symphony/echo-forge-golden-e2e.md` (nuevo)
  - `80-agents/memory/public/runbook/symphony/echo-forge-cross-system-triage.md` (nuevo)
  - `80-agents/skills/INDEX.md` (7 filas agregadas al catálogo core + fecha)

## Motivo

- Capitalizar el aprendizaje operacional de la sesión `DURABLE-ARTIFACT-VERIFIED-READS-FINAL-E2E-NORMAL` (2026-08-29) como método reusable: separar comportamiento genérico (skills, transferibles a Echo/Echo Forge/Agents OS/MELI) de especificidad de sistema (runbooks de Symphony), reduciendo tokens y exploración en futuras sesiones por agentes nuevos.

## Fuentes usadas

- Sesión del 2026-08-29: gates ejecutados, patrón de probe, matriz de canales verificada, triage del defecto [[2026-08-29-durable-verified-reads-exporter-double-execution]]; feedback [[2026-08-29-symphony-worker-observability-session-feedback]]; propuesta de arquitectura skill/runbook/memory aprobada por el owner.

## Resolución aplicada

- Skills materializadas con el contrato canónico (`materialize_schema_note.py`, template skill/runbook) y redactadas agnósticas al sistema; los datos operacionales (endpoints, colas, scripts, comandos exactos, gotchas de build) viven sólo en los runbooks; INDEX.md registra las 7 con descripción y uso. Frontera aplicada: SKILL=cómo razonar/ejecutar una clase de tarea; RUNBOOK=cómo se hace en este sistema; MEMORY=hechos del sistema.

## Validación

- 12 notas creadas vía script (schema contract OK en dry-run y escritura); skills con description de routing, load_policy manual, related a sus runbooks; runbooks con comandos probados en la sesión del 2026-08-29.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos (paths de workspace referidos como `~/go/src/github.com/xKoRx/...`; sin credenciales)

## Rollback

- Borrar las 12 notas y revertir las 8 filas/fecha de `INDEX.md`; sin impacto en notas canónicas previas.
