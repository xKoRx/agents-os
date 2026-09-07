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

# Zords Human First — boundary mínimo de authoring

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `10-projects/Meli/Zords — Human-First Technical Authoring/Zords — Human-First Technical Authoring.md`

## Motivo

- El owner priorizó explícitamente no alterar funcionalidades actuales en su primer feature sobre un repo todavía desconocido y eligió stdout por sobre persistencia local.
- El plan anterior mezclaba authoring con contratos globales de Zord y daba demasiado protagonismo a SDD.

## Fuentes usadas

- Decisiones directas del owner en esta sesión.
- HEAD y LOCAL_CHANGE de `local-agents-pipeline-cli`: package description, `ZordMeta`, loader, runner, orchestrator, provider Codex y diff WIP.
- `80-agents/skills/human-first-technical-writing/SKILL.md` y contrato de implementation planning.

## Resolución aplicada

- Se reemplazó el segundo task type global por un subcomando hermano `zord author` y módulos nuevos aislados.
- Se fijó stdout-only para documentos, stderr para diagnósticos, cero persistence/publication y SDD como source explícito genérico sin conocimiento del core.
- Se reabrió G0 para podar hunk-by-hunk el WIP invasivo; `task: document`, `Document*` globales y cambios al loader legacy quedaron reemplazados.
- Se redujo el roadmap de cinco a cuatro fases con no-touch list, seams permitidos, contracts, tareas y rollback consistentes.
- Se cerró el contrato CLI: `--initiative` y `--source <label>=<path>` existen sólo bajo `zord author`; initiative nunca descubre archivos, los labels sólo aportan semántica y los comandos legacy deben rechazar esas options.

## Validación

- `validate_plan.py`: 4 fases, 4 gates, 4 dispatches, 2 referencias portables, 0 errores y 0 warnings después del cierre del contrato CLI.
- `lint.py --strict` sobre el proyecto: 0 errores y 0 warnings.
- Scan dirigido: sin paths locales ni referencias al store `.sdd/zords`; las menciones de `task/document` sólo documentan explícitamente su rechazo.
- `graphify-obsidian update` intentado y bloqueado por la misma deuda global ajena ya registrada: 12 errores y 6 warnings en Signals/Symphony; el proyecto y este log pasan lint estricto, pero el índice permanece stale.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Restaurar la versión previa de la nota desde historial si el equipo decide conscientemente ampliar `ZordMeta` y el runtime de review; no se modificó código del repo en esta actualización.
