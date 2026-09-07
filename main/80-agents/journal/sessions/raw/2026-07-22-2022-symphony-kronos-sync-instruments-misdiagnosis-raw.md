---
type: raw_session
scope: session
created: "2026-07-22"
updated: "2026-07-22"
area: "[[Symphony Portal]]"
project: "[[Symphony]]"
application: "[[StrategyQuant X]]"
entities:
  - "[[Symphony]]"
  - "[[StrategyQuant X]]"
related:
  - "[[sqx-instrument-sync]]"
  - "[[symphony-worker-bootstrap]]"
aliases:
  - Kronos vuelve a fallar 2026-07-22 tarde
  - Misdiagnóstico run_id en lugar de sync instrumentos
confidence: verified
source_session: "f0a8c3b2-7e91-4f4d-9c2b-1d6e3a5f8b04"
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
  - app/strategyquant-x
  - area/symphony-portal
  - project/symphony
---

# Symphony Kronos — segunda investigación: misdiagnóstico run_id, causa real era sync de instrumentos

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: Claude Code (GLM-5.2).
- Proyecto o entidad: [[Symphony]] / [[StrategyQuant X]] / [[sqx-instrument-sync]].
- Objetivo de la sesión: entender por qué Kronos seguía fallando dos wfs
  concretos tras los fixes de la sesión anterior (permisos JAR + cache
  compiled). Los wfs:
  - `sqx-main-00_configs-v1-NDX-H1-L-1784764719`
  - `sqx-main-00_configs-v1-NDX-H1-L-1784762810`
- Resultado real: la hipótesis diagnóstica del agente (asimetría de
  `run_id` en `databank_metadata`) **fue rebutida por el usuario**. La
  causa raíz verdadera, descubierta vía la UI de SQX en Kronos, era
  **dependencias de proyecto no resueltas por falta del instrumento
  `XAUUSD_darwinex` en Kronos**, ausente respecto de Zeus y Hera.
  La herramienta de sincronización de `user/data` actual (skill
  `sqx-instrument-sync`) no lo detectó porque solo verifica hash maestro
  de `History/`.

## Transcript

```
Pegar aquí la sesión completa cuando se exporte.
```

## Hallazgos correctos (rescatables)

- Confirmación operativa: Kronos está en 0.1.130, WorkingDirectory
  correcto, usuario `kor`, servicio activo. No es problema de
  despliegue.
- Confirmación vía Temporal de que ambas waves mueren en la actividad
  `classify_and_rank` (evento 17→19) con `ErrMetadataMissing` non
  retryable.
- Análisis detallado de `databank_metadata` mostró que los 380 docs de
  `wave_key=test` tienen `run_id` por actividad, no por wf, y que los
  traceIDs de los wfs afectados no aparecen.
- Identificación de las brechas reales de la skill `sqx-instrument-sync`
  (ver L3 known-error generado).
- Generación de un prompt maestro robusto para reescribir la skill +
  script con verificación bit-a-bit sobre TODO `user/data`, no solo
  `History/`.

## Error de diagnóstico (lo que el usuario corrigió)

El agente concluyó que la causa era el BUG-001 del backlog (`run_id`
asimetría writer/reader en `SaveStrategyMetadataBatch`). El usuario lo
refutó: "nah wn tay puro dando jugo... no tiene nada que ver la wea que
dices... el problema está en que el proyecto tiene dependencias no
resueltas, que es específicamente instrumentos no creados a diferencia
de los otros dos workers... lo acabo de ver en la UI, es por
XAUUSD_darwinex".

Lección: cuando hay un síntoma de `metadata missing` que aparece
**solo en un worker**, antes de ir a la asimetría de run_id hay que
verificar (a) si el builder realmente escribió algo (logs de SQX) y
(b) si las dependencias de instrumentos del proyecto están resueltas
en el worker. La raíz operativa (datos) suele estar antes que la raíz
de código.
