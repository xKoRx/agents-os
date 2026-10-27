---
type: session
schema_version: 1
scope: session
created: "2026-10-27"
updated: "2026-10-27"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
entities: []
related: []
aliases: []
confidence: high
source_session: ZCode CLI 2026-10-26/27 (mandato ONE-SHOT owner: certificación replay-based E2E)
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---
## Objetivo

ONE-SHOT owner: recuperar el último flow completo real de Echo Forge (Temporal+MinIO), replicarlo con `dynamic-groups.v1`, cerrar los gaps de integración imprescindibles y ejecutar la certificación física completa con Top X por logical_type.

## Trabajo realizado

- **Veredictos: `INTEGRATION_COMPLETE` + `FULL_MULTITASK_FLOW_BLOCKED`.** Paquete `cert-replay/` completo (entregables A–J + evidencia + originales) en rama local `codex/forge-cert-replay-oneshot` (worktree `~/aranea/work/forge-cert-replay-20261026`); base = candidato shot4-cont `417c3819` preservado.
- FASE A: último flow completo = **w11 `561267ed`** (COMPLETED 2h05m49s, 105/105 children, 0 fallos, 317/317 stages durables, `sqx-prop`, release 0.3.2); w9/w10 excluidos con motivo.
- FASE B: paquete original congelado byte-exacto (config PG `7307aee6`, 4 CFX con SHA256, manifest 973 objetos).
- FASE C/D/E: 3 fixes con oráculos — FIX-1 Apply↔SelectedPeriod `18f6777` (gap `wfm.selected_period_index` jamás inyectado; opt-in `resolve_selected_period` + resolver 2.6 sobre payload CELL + readback físico verificado + `evaluation-period.v1` + carrier sellado), FIX-2 MetricSet del productor→ledger `be2167a` (ranking sobre el Retester daba EVIDENCE_MISSING), FIX-3 select_robust sella `EvaluationPeriodRef` `40a878b` (tramo G-03 pendiente del shot4-cont). Legacy sin opt-in byte-exacto; paridad de fallos ambientales con candidato puro.
- FASE F: `certification/config.json` w12 **SPEC_VALID** (target group por logical_type top_n=1, ranking por métricas del `group-retester`, bindings en apply/final-reretester/mt5-final, cutover declarativo).
- FASE G/H: **BLOCKED con bloqueo exacto** — worker-kronos (192.168.31.135) inalcanzable (22/3389/5985 cerrados desde Daedalus y Kronos; `aranea-ssh`/`aranea-mongo` MCPs expirados todo el cierre); SQX Daedalus Build 142 sin licencia; flota cambió a identidad `sqx-ulab-*`; NO se despachó flujo condenado a parcial; cero FlowRun nuevos.
- Oráculo físico §5.3 sobre w11: **35/35 scores recomputados == snapshot `sha256:0356f6b7`, orden descendente EXACTO** (`evidence/w11-ranking-oracle.txt`).
- Cierre: proyecto actualizado, agent run registrado, change_log, feedback (gateway MCPs), memoria ZCode.

## Pendiente

1. Re-inicializar gateway `aranea-*` MCPs y revalidar flota `sqx-ulab-*` (layout cambió).
2. Review owner de los 3 fixes + push de la rama.
3. Rollout candidate-local (worker Linux `sqx-dev` + mt5-worker Windows slots propios + watcher prefijo ETCD propio) → despachar w12 → verificación por etapa según `PHYSICAL-FLOW-EXECUTION.md` §4.
4. Gate B (cobertura ≥95% delta) y Gate C (verificación física exporter Java V2) heredados, no bloqueantes para la integración.
