---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-16"
updated: "2026-10-16"
area: "[[Aranea]]"
project: "[[Echo Futures]]"
application:
entities: []
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM 5.3 (account:zai-individual-coding-plan/GLM-5.3-Flash, host-reported)
model_source: host
task_type: implementation
task_complexity: high
outcome: success
verification: passed
evaluator: agent
user_rework: unknown
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — TradesGerard presupuesto de entrada + matriz O11-40 (2026-10-16)

## Tarea

Mandato Owner one-shot: corregir el criterio de muerte de cuenta (presupuesto
de entrada R_ref, no el mínimo físico ~24,98), impedir que el MM recorte el
riesgo al remanente, definir 40 configuraciones en master y reejecutar las 40
campañas nuevas terminadas y explicadas.

## Ejecución

- Regla `STRATEGIC_ENTRY_BUDGET_V1` implementada en el flujo común de retiro
  (margen permanente < R_ref ⇒ `LOST_ENTRY_BUDGET_BY_POLICY`; igualdad
  sobrevive; M_físico queda como admisión de cantidad) + tgmm sin recorte de
  headroom (declina `TG_ENTRY_BUDGET_EXCEEDS_HEADROOM`; el shrink histórico
  queda sólo para configs legacy) + pausa diaria
  `DAILY_CAPACITY_BELOW_ENTRY_BUDGET` + pago acreditado jamás reabre cuenta
  terminal. Emparejamiento exacto política-de-campaña ↔
  `tg_mm.entry_budget_policy` validado antes del motor.
- Matriz versionada en master ANTES del lote: `matrix/manifest.json` +
  40 presets + generador/validador/lot-runner/agregador. Master: `13066432`
  (regla), `95e9d105` (fix técnico: traza comprimida 256MiB para toda
  política declarada — F0/K05 abortaba por 'compact output byte limit' con el
  camino raw de 16MiB), `d74b6525` (docs + RESULTS-20261016.csv).
- Lote: binario congelado `bce583e7d88f59af…` sobre `95e9d105` árbol
  limpio, 40 planes validados (cruces completos, R/T/rho exactos, política en
  los 40, sin residuos S2). Las corridas previas (`a4af2554…`, 5 filas
  13\*\+7\*) se descartaron y TODO el lote se reejecutó bajo el corte final.
  Secuencia mandato: F1/K05/2300 → 7 K05 → 32 restantes; concurrencia ≤6
  procesos, 1 preparación TG por clave, `tg_kernel_feeds_runtime=0`.

## Verificación

- 40/40 COMPLETE intento 1, reconciled=true, 0 breaches oficiales, 404
  cuentas `LOST_ENTRY_BUDGET_BY_POLICY` con evidencia + sucesora, 9 cobros
  netos (5×1651 + 4×2211), 9.916 entradas. Ranking: F2-SR/K02/3000 +1851,
  F1/K04/3000 +171, peores F0/K05 −4920 (caja 80).
- Tests nuevos verdes (límites R−0,01/=/+0,01 en 5 perfiles, no-shrink,
  pausa diaria, pending sin resurrección, emparejamiento, cadena preset en 40
  filas, paridad de traza). Suite completa: mismos 7 fallos preexistentes que
  en base `0c4aae55` (contrastado con stash en base), cero nuevos.
- Fila 1 reproducida idéntica bajo el binario final (caja 4251, 15 perdidas,
  1651 neto) — determinismo del motor confirmado.

## Rework y prevención de causa

- Rework interno: primer diseño estampaba economía del preset sobre el spec;
  el test de divergencia existente lo rechazó — la materialización por fila
  vive en el materializador del manifiesto, el preset sólo conserva políticas
  y verifica (CheckRequest). Lección: el contrato existente (rechazo de
  divergencia) manda sobre la conveniencia del estampado.
- Causa-preventiva registrada: los umbrales gated por literal de versión de
  política (V2) deben expresarse como "política declarada" — un tiers de
  storage por versión exacta excluye silenciosamente a la versión nueva.
