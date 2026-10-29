---
type: session
schema_version: 1
scope: session
created: "2026-10-29"
updated: "2026-10-29"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine]]"
related:
  - "[[Research — Causal Metadata Renewal W1-i 2026-10-29]]"
  - "[[Plan — Single Episode Pilot v3 W1-i 2026-10-29]]"
aliases: []
confidence: high
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# 2026-10-29-polymarket-w1i-causal-renewal-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Mandato W1-i (one-shot GLM-5.3-Flash Max, offline): implementar la **opción B adjudicada por Metis** (prereg PE-005-R1 v2 §4) — renovación causal de evidencia para metadata idéntica — más la receta temporal serial V3 con deadlines absolutos; pruebas y commit LOCAL; sin captura, sin live, sin cambio de estrategia, sin adquisición. Excepción técnica acotada al freeze del checkout de investigación.

## Contexto cargado

- Bootstrap AgentsOS (constitución + perfil + continuidad global + índice de skills); HEAD `853c0e4` y rama `w0/offline-causal-replay-20261027` verificados; fixture W1-h untracked leída; prereg v2 §4 y Plan v2 W1-h; fuente real `regimes/{reducer,service,prospect}`, `capture`, `persist`, `cmd/engine/{record,clob_observe}`.

## Trabajo realizado

- **Segmento 1 (historia):** política pura `EvaluateRenewedConstraint`; cuarentena AsOf con doble cota real; 15 tests; bloqueador preciso de `migrations/0025` declarado; sin lock nuevo; fixture W1-h intacta.
- **Segmento 2 (misma sesión, continúa):** el lanzador desbloqueó el perfil para `migrations/` (lectura de 0020–0024+embed, escritura de 0025) — el ledger quedó **CONECTADO de verdad**: migración creada desde los esquemas reales (no desde propuestas); `upsertRegimeRevision` registra la observación inmutable en las 3 ramas con provenance real y contadores `ObservationsNew`/`RenewalsNew`; idempotencia `UNIQUE(entity_id, capture_seq, source_ref) DO NOTHING`; `AssetConstraintAsOf` consume el ledger vía la política probada con **chequeo de completitud** (ledger parcial ⇒ ruta legacy fail-closed); `Inspect` expone `observations`; test nativo de ruta REAL (`TestW1IRenewalLedgerNativeThroughService`: T16 invariante antes/después de drenar T20, T20 known con su seq, ledger T0+T20, first_seen T0, re-drain idempotente, restart/rebuild deterministas); fixture W1-h actualizada SÓLO en la expectativa de frescura (renovación re-ancla; historia declarada en el archivo).
- **Regresión:** regimes/books/replay/capture/cmd-engine PASS; `internal/experiment` rojo en UNA sonda (`TestW1FCaptureV6GateAvailabilityTrial` P5): su premisa es la semántica retraída (ancla init + consulta a seq=frontier, donde la renovación final está legítimamente admitida). El engine es correcto; `regime_digest` invariante. La corrección de 2 líneas está en `internal/experiment/w1f_hypothesis_integration_test.go` — FUERA de la allowlist, denegada por el hook (1 sonda). **Impedimento real ⇒ delta SIN commit** (regla: suite roja no se sella); árbol @ `9e2c6b7` + 4 modificados + migración nueva, todo hasheado. 12 inputs: 7/12 re-verificados (4 `.seg` + `engine.db` denegados al hash por el perfil; récords vigentes).

## Artifacts creados o modificados

- Repo (SIN commit, árbol @ `9e2c6b7` + delta): `migrations/0025_regime_observations.sql` (nuevo, sha `89bdbab9…`), `internal/regimes/{reducer.go, service.go, w1i_renewal_integration_test.go}` modificados, `internal/experiment/w1h_acquisition_recipe_test.go` modificada (frescura). Segmento 1 ya commiteado: `9e2c6b7dd26e70a53b05499a2d682ef33f1dac27`.
- OUT: `validated-baseline/w1-i-causal-renewal-20261029/` (`evidence-manifest.json`, `test-receipt.md` del segmento 1, binario `engine` reconstruido sobre código wired).
- Vault: INFORME + PLAN V3 actualizados (segmento 2), summary/feedback/agent_run (esta edición), change_log (sección ampliada), continuidad (bullet (21) actualizado).

## Memoria propuesta o creada

- Ninguna en memoria interna global (sin delta transferible nuevo; las lecciones de fricción van al feedback).

## Decisiones

- Rechazar la elusión con `observed_at`/`last_observed_at` mutables (veredictos falsos en cortes retroactivos T0/T10/T20→T16) ⇒ migración 0025 como único camino válido; precisarla como bloqueador y seguir con lo entregable.
- No reescribir la fixture W1-h: sin cambio de semántica enviada, sus expectativas siguen válidas; preservar v1 byte-idéntica.
- Receta V3: 6×13,5 min + observes de 1 min = 88 min < 90 con margen 2 min; tramo+observe < TTL.

## Pendiente

- **Un desbloqueo exacto:** permitir la edición de `internal/experiment/w1f_hypothesis_integration_test.go` (sondas P5 en `a.FirstSeq` — comentario y corrección ya redactados en el informe, §0) o aplicarla el lanzador; luego re-corrida de los 6 paquetes (se espera 6/6) y commit 'Renew causal prospective metadata observations for research' con el subset completo.
- Lock de data-dir: bloqueo separado (sin patrón compatible en repo), sin cambios.
- Los 4 segmentos `.seg` + `engine.db` de capture-v6 quedaron sin re-hash este segmento (perfil deniega); sus hashes de récord W1-h siguen vigentes.
