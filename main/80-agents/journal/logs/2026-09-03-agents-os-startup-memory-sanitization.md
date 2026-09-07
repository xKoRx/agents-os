---
type: change_log
schema_version: 1
scope: session
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-operating-continuity]]"
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

# 2026-09-03-agents-os-startup-memory-sanitization

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated / deleted-duplicate
- **Archivo(s):** continuidad interna global y su archivo histórico; cuatro decisiones/patrones públicos de Echo Forge; cuatro memorias de dominio mal scoped; contrato, template y guías de memoria; bootstrap, Context Retrieval, Memory Distillation, constitución, mapa e índice de skills; Doctor y su ejecutable; generador de reglas de superficie; hooks local/global de Codex; cockpit de [[AGENTS OS]].

## Motivo

- El startup cargaba aproximadamente 24.492 tokens porque la memoria global contenía un ledger detallado de Echo Forge. Cuatro documentos adicionales del mismo dominio también declaraban `load_policy: always`, y la configuración global de Codex ordenaba leer `agents-os.md` ante cada mensaje.

## Fuentes usadas

- Doctor baseline; bootstrap, constitución y contrato de metadata; memoria global; metadatos de las notas Echo Forge; configuración global de Codex; generador canónico de reglas de superficie; proyecto [[AGENTS OS]].

## Resolución aplicada

- Se eliminó del hot path el ledger duplicado de Echo Forge y la memoria global quedó limitada a cinco comportamientos transferibles. Los documentos de Echo Forge usan `when_project_loaded`; Context Retrieval usa `when_entity_loaded`; memorias de dominio con scope global fueron normalizadas a project/error routing; bootstrap se ejecuta una vez por nueva sesión y nunca por mensaje. La continuidad interna usa un slot mutable por `continuity_key`: el siguiente agente actualiza el checkpoint activo en el mismo archivo; sólo un cambio material de scope crea sucesora y retira la anterior a `superseded + manual + low` de forma atómica. Doctor valida límite de 1.000 tokens, project ledgers, scopes globales, transiciones lifecycle y unicidad del checkpoint activo.

## Validación

- Doctor strict: `HIGH=0 / MEDIUM=0 / LOW=0`, startup `≈4724`; schema contract: 45 tipos, 44 templates, 5 fixtures, 0 errores; lint strict del fix: 0 errores y 0 warnings; probes de regresión de sanitización, lifecycle y regla de nueva sesión: PASS; Context Router: 14/14 operaciones, 0 misses, precision proxy 100%. Graphify reindex: bloqueado antes de indexar por 26 errores y 6 warnings fuera del fix; se conserva el índice previo.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni valores sensibles; la configuración externa se identifica por superficie, sin persistir un path de máquina.

## Rollback

- Reponer los valores `always`, la continuidad anterior y la directiva global sólo desde una copia histórica externa o una revisión manual; no se recomienda porque restaura el defecto de consumo. La información de Echo Forge permanece en sus proyectos, decisiones, patrones, known errors y memorias scoped.
