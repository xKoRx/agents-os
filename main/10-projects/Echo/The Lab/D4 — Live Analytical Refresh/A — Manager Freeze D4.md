---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[A — Product Contract — The Lab]]"
  - "[[D — Revised Roadmap]]"
  - "[[F — Decision Register]]"
  - "[[A — Technical SPEC D3]]"
  - "[[G — Correction Record D3 (Shot 3)]]"
tags:
  - kind/doc
  - area/echo
  - the-lab
  - d4
created: "2026-09-25"
updated: "2026-09-25"
---

# A — Manager Freeze D4 — Live Analytical Refresh

## Estado

`D4_MANAGER_FREEZE = CLOSED`.

Baseline remoto Echo verificado:

`xKoRx/echo master@372af59a7b83604781346613da01e3d510ea1360`

Manager SDD branch creada desde ese SHA, sin product code:

`feature/d4-live-analytical-refresh@8c4a52266bbd615990fec4f2f5b8dbfc727b9b16`

Artefactos SDD frozen en Echo:

- `specs/FEAT-THELAB-D4-LIVE-ANALYTICAL-REFRESH/SPEC.md`
- `specs/FEAT-THELAB-D4-LIVE-ANALYTICAL-REFRESH/changes/CHANGE-001-entrypoint-metadata-reproducibility.md`
- `specs/FEAT-THELAB-D4-LIVE-ANALYTICAL-REFRESH/PLAN.md`
- `specs/FEAT-THELAB-D4-LIVE-ANALYTICAL-REFRESH/TASKS.md`

## Hito funcional del día

Cambio de canonical history por la autoridad D1 debe converger automáticamente a curvas/puntos/métricas actuales y a la experiencia The Lab sin ejecutar manualmente `lab-worker recalculate-curves`.

```text
history replace
→ durable currentness becomes DIRTY
→ existing lab-worker discovers it
→ existing LabCurveService recalculates
→ atomic publish
→ Hasura
→ existing The Lab UI shows current result
```

D4 actual NO ingiere `trade_journal`; la fila D4 REAL/journal del roadmap 22–23 Sep queda desplazada al próximo hito por mandato owner del 25-09. Forge sigue independiente.

## Findings PRE reconciliados en source exacto

### D4-PRE-01 — CONFIRMED

`StrategyHistoryHandler` existe, pero `v3/gateway/internal/server.go` no lo monta en el branch `pgClient != nil`; los tests D1 construyen un `http.NewServeMux` privado y registran PUT/GET manualmente. El 404 físico D3 es coherente con source.

Corrección frozen: montar el handler/service existente en `NewServer` y agregar regression sobre el assembly real.

### D4-PRE-02 — CONFIRMED

La metadata V3 contiene múltiples bloques explícitos `role: admin` en tables/functions. D3 DEV requirió evitarlos para aplicar en Hasura v2.38.

Corrección frozen: remover todos los permisos explícitos del role admin en metadata V3, preservando roles no-admin. Admin-secret permanece implícito. Gate: apply completo DEV sin filtros.

### LOW aceptado

`--triggered-by` acepta valores que violan el CHECK de `lab_job_runs`. D4 lo corrige fail-fast porque toca ese mismo path.

### LOW diferidos

- formato ticks Y;
- `aria-label` de unidad.

No bloquean D4.

## Decisiones manager congeladas

- No recálculo síncrono dentro del PUT.
- No goroutine fire-and-forget del Gateway.
- No nueva cola, dirty table/flag, CDC, Kafka, Temporal, Flink ni microservicio.
- DIRTY se deriva de PostgreSQL: para cada default curve spec requerida, missing o `lab_curves.history_digest != strategy_history_state.history_digest`.
- CURRENT cuando todas las default specs existen y matchan el head; estado READY/INSUFFICIENT/ERROR es independiente de currentness.
- D4 V1 refresca `curve.DefaultRegistry().DefaultSpecs`. Si discovery de implementación demuestra custom-config curves activas, STOP y vuelve al manager.
- `lab-worker` obtiene modo persistente de scan periódico, no-overlap. Cadencia DEV frozen: 5 segundos después de cada scan completo.
- Failure por StrategyVersion no bloquea las demás; dirty persiste por derivación y el siguiente scan reintenta.
- Restart no pierde trabajo: startup reescanea estado durable.
- A→B→C puede coalescer a C.
- Concurrencia replacement/recalc reutiliza el advisory transaction lock D1/D3 existente.
- Publicación atómica D3 no cambia.
- Observabilidad reutiliza `lab_job_runs`, job `recalculate_lab_curves_v3`, `triggered_by=SCHEDULED`, agregando digests/resultados suficientes sin schema nuevo.
- DEV usa una instancia gestionada del worker en el patrón existente `systemd --user`.
- No journal ingestion, no Forge, no front feature work, no algoritmos, no migrations, no PROD.

## Fit del día

`THREE_SHOT_FIT = YES`.

Razón: el slice reusa D1/D3 y no requiere modelo nuevo, schema nuevo ni engine nuevo. Shot 1 cruza Gateway + worker + PostgreSQL + metadata/runtime, por lo que corresponde TOP. Shot 2 TOP fresh adversarial. Shot 3 TOP sólo para findings aceptados.

## Physical reality pendiente

Esta sesión manager no tuvo un canal SSH/Aranea ejecutable disponible para reprobar Daedalus hoy. Se conserva como dependency la certificación física D3 y el Environment Contract, pero D4 no reclama `DEV_PHYSICAL=PASS` antes del candidate.

## Certification posture al freeze

```text
SOURCE          = PENDING
REMOTE_BASELINE = PASS
MAIN            = PENDING
DEV_PHYSICAL    = PENDING
AUTHENTIC_DATA  = PENDING
PROD            = PENDING
```

## Próximo exacto

Ejecutar Shot 1 TOP desde `feature/d4-live-analytical-refresh@8c4a52266bbd615990fec4f2f5b8dbfc727b9b16`, producir candidate exacto y máximo `SHOT1_CANDIDATE_PASS`. No cerrar sesión global.
