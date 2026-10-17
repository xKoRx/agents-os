---
type: session_feedback
schema_version: 1
created: "2026-10-17"
updated: "2026-10-17"
area: "[[Aranea]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
  - "[[aranea-agent-dev]]"
related:
  - "[[forge-wave-dispatch]]"
  - "[[2026-10-16-forge-fast-e2e-budget-control-feedback]]"
severity: high
category: process
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-feedback
  - scope/session
---

# Feedback — E2E flujo único: presupuesto T+40 era insuficiente por diseño, alias canónico nuevo por dataset, y reset≠completar

**Qué pasó (2026-10-16/17, FLOW_EXAMPLE_2):** tres lecciones de una misma cadena. (1) La cancelación por tiempo T+40 de la sesión anterior fue **incorrecta**: el workflow estaba sano; el funnel completo (builder→…→MT5→fidelity→promoción) midió **2h09m30s** en la corrida limpia w9 y el intento w8 demoró >3h con export de overview lento — ningún presupuesto de 30-60 min era realista para la cadena completa con estos CFX. (2) El dataset del Owner (`USATECHIDXUSD_dukascopy_UTC02`) no estaba en la tabla explícita de aliases de `CanonicalSymbol` y la fidelidad falló no-retryable DESPUÉS de 3h de pipeline (MT5 30/30) — el defecto se detectó al final de la cadena. (3) Un reset Temporal re-ejecutó el tramo final con el fix, pero `flow_run_seal` rechazó FAILED→COMPLETED: **un FlowRun sellado FAILED es terminal y ningún reset lo completa**.

**Por qué importa:** (1) los presupuestos por reloj para campañas de cadena completa impulsan cancelaciones de trabajo sano — el costo real debe medirse y declararse, no estimarse agresivo; (2) un dataset nuevo cruza la frontera de fidelidad al FINAL del pipeline: quemar 3h por un alias de una línea es el peor punto de fallo posible; (3) el "continuar" post-fix requiere identidad de wave nueva, no reset.

**Lección accionable (incorporada a [[forge-wave-dispatch]]):** (1) preflight de dataset: si el dataset/símbolo no está en `canonical_scope.go`, añadir el alias exacto (+ fila negativa de variante) y release ANTES de despachar; (2) presupuesto: declarar duración medida por etapa y NO cancelar trabajo sano por reloj — el owner revocó explícitamente los timeouts de campaña; (3) ante fallo sellado FAILED + fix: re-despacho con wave nueva (identidad limpia), jamás reset esperando COMPLETED; (4) diagnóstico de sqcli "colgado": el export del overview es single-thread — verificar progreso real con el log `overview_databank_*.log` (`processed N/M`) antes de intervenir.
