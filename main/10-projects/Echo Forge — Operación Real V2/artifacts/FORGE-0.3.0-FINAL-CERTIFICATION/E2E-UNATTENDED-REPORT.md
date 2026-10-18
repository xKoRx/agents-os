# E2E-UNATTENDED-REPORT — Forge 0.3.1 · w10 · UN root FlowRun (2026-10-18)

## Veredicto

**E2E_UNATTENDED_PASS** — UN `config.json`, UN `GenericSQXWorkflow` raíz con GROUP interno `source=ranking_snapshot`, ejecutado de punta a punta sin intervención manual posterior al dispatch, estado terminal **COMPLETED** sellado en el registro durable. Cohort NUEVO del Builder (649 generadas → 22 seleccionadas; sin reutilización de snapshots/EX5/rankings anteriores).

## Identidad

- **FlowRunRef**: `79385c32-52d0-4358-95a7-090ca4bbb30f` (wave 10)
- **WorkflowID**: `sqx-main-v1-239a5b28-132b-4df4-a6e1-6fd96a4ccf9a` · **Temporal RunID**: `01a14d4b-f054-71c9-808d-077a662d3a77` (namespace `sqx-prop`, cola `sqx-main-queue`)
- **ConfigID durable**: `098d606e-15c8-4ac1-9692-0b97a34e2726` (cfgID derivado `NDX_flow_example_2_v1_w10`, libre en preflight)
- **T0**: 2026-10-18T04:36:24.77Z · **sello COMPLETED**: 07:39:27.56Z · **duración total 3h03m03s**
- Spec: SPEC_VALID `runtime.ValidateWorkflowSpec` (11 tasks raíz; deep-warnings anidada en el group). CFX del Owner byte-exactos 4/4 (SHA en SHA256SUMS.txt). Release efectiva 0.3.1 en 4/4 verificada físicamente ANTES del dispatch (gate §7 cumplido).

## Intervenciones posteriores al dispatch: CERO

Desde `screen forge-watcher-w10` (04:36:24Z) hasta el sello (07:39:27Z) la sesión sólo ejecutó LECTURAS: timeline de stages (flowkit RO), logs de workers, DescribeTaskQueue/WorkflowExecution/History (harness RO), PG/Mongo/MinIO read-only, `ps`/`journalctl`. CERO mutaciones: sin tocar CFX, config, workers, binarios, Mongo/PG escritos, artefactos, ni cancelaciones. Los helpers Go efímeros (`preflightw10`, `wfhist`, `sqlq`) son RO y se borran al cerrar. El watcher quedó corriendo en screen (higiene al cierre).

## Retries automáticos registrados (válidos por contrato, no intervención)

| # | Ventana UTC | Qué pasó | Causa | Resolución |
|---|---|---|---|---|
| 1 | 04:36:46→05:05:43 | Builder intento 1 en Hera (sqcli generando, ~1 core — fase de generación single-core, igual que w9) | **Churn de systemd en Hera 05:05:43Z**: `Stopping stager-runtime.service` mató el worker con el sqcli en vuelo (journal citado; la activación stager 0.3.1 había sido limpia a las 04:09, NO fue el stager) | Worker anterior muerto; Temporal reintenta |
| 2 | 05:09:25→05:09:27 | Intento 2 en Hera (worker nuevo 1753): sqcli exit en 2.1 s, "success markers not found" | Residuo del sqcli del intento 1 (aborto inmediato, sin log de proyecto) | Temporal reintenta |
| 3 | 05:11:27→~06:17 | Intento 3 en **Kronos**: builder completo (2m05s task datos + generación 66 min, 649 en output) | — | ÉXITO; el funnel continuó solo |

RetryPolicy del workflow: `MaximumAttempts=0` (ilimitado, 1m→30m backoff) — comportamiento contractual. No existe timeout global artificial; no se canceló nada por reloj.

## Resultado económico (viabilidad ≠ ejecución técnica)

- 649 estrategias generadas/aceptadas; 5 tipos lógicos; 22 seleccionadas (top5×tipo, 22 porque un tipo aportó 2 y otro 5); 22/22 optimizadas/WFM/robust/apply; 22/22 EX5 sin errores; 22/22 MT5 backtests ejecutados.
- **6/22 con trades MT5>0** (mejor fidelidad 67.77; 449 trades MT5), **16/22 con CERO trades MT5** = 100% de sus señales rechazadas por margen del propio EA — mismo mecanismo físico documentado en la forense 2026-10-17 (SL fijo 21 pips → lote 9.5 > margen del depósito 100k). **NO se cambió Money Management** (mandato §4): cero trades por margen NO invalida el E2E.
- Fidelidad `mt5_fidelity_shadow.v1` fórmula intacta; ranking final `score_descending` sobre 22; promoción estructural `finalist_promotion 2.0.0` STRUCTURAL_PROMOTED (decision_ref `sha256:4dc03690…`).
- Ninguna finalista demuestra rentabilidad MT5 (mt5_net de las 6 con trades es negativo) — la evaluación de calidad es trabajo del owner, no parte de este veredicto.

## PRE_ECHO

- 22 handoff manifests creados 06:50Z+ (estructurales, locales).
- **22/22 handoff_deliveries en estado `HANDOFF_CREATED`**, attempts con `last_error="echo ingest base url / bearer not configured: echo ingest ingress fail-closed: ingress_not_configured"` — **0 POSTs reales hacia Echo** (fail-closed ANTES de HTTP), 0 ingestiones, 0 deployments, 0 órdenes. Confirmado en preflight que no existe configuración de ingreso Echo para esta prueba.

## Cadena de identidad Magic (resumen)

22/22 verificaciones "Mágica efectiva MT5 == sqx.strategy_magic" en los reconciles (7 Zeus + 8 Hera + 7 Kronos), mágicas 26100091082..26100091103, MQ5 durable con `input long`. Detalle en MAGIC-NUMBER-VERIFICATION.md.

## Desviación de versión declarada

El mandato nombraba 0.3.0; la canónica resultó 0.3.1 (0.3.0 quedó publicada con stamp `vcs.modified=true` por untracked del plugin — ver RELEASE-0.3.0-MANIFEST.md). El E2E corrió sobre 0.3.1 (release limpia con el mismo fix funcional d67244b + gitignore).
