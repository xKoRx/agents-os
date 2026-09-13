---
type: source
schema_version: 1
status: active
area: "[[Echo]]"
source_url: "https://github.com/xKoRx/echo/tree/04c16bd2bd7b69725560873950a5d6b067fd3a4f/v3"
repo: "xKoRx/echo"
path: "v3/"
author: "xKoRx"
captured: "2026-09-06"
aliases: []
tags: ["kind/source", "area/echo"]
created: "2026-09-06"
updated: "2026-09-06"
---

# Echo — Fuentes de arquitectura y producto 2026-09-06

## Referencia

- **Origen resoluble:** `xKoRx/echo`, `v3/`, master `04c16bd2bd7b69725560873950a5d6b067fd3a4f` (2026-08-24). [Commit](https://github.com/xKoRx/echo/commit/04c16bd2bd7b69725560873950a5d6b067fd3a4f).
- **Fecha de captura/verificación:** 2026-09-06; consulta master remoto, clone aislado y source inspection. Checkout habitual `e25165ba2e57a86b7cdcbd78d44406f66fc9ba23` sólo difiere en sintaxis del readiness check.
- **Locators detallados:** ledger E01–E19 de [[Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026]]. Workspace: [[echo-go-workspace]].

## Alcance

Contratos SDK, migrations 001/034/038–060 seleccionadas, journal/planner/MM/Bridge/EA MT5, Lab Clean, jobs SQL portfolio/health/account, Gateway, Hasura, frontend y configuración StateFun productiva del repo. Tests focales SDK Lab/domain/MM PASS. Sin queries a producción ni cert física nueva.

## Notas de provenance

- Source implementado y documentación de intención separados. Los paths del ledger fijan símbolos y migraciones; no se almacenan repos, secrets ni dumps en el vault.
- [[Echo - Auditoria POC e Identidad Forge-Echo 2026-08-23]] conserva decisiones owner del 24-08 (magic/canonical, Reference/mirrors permanentes, 3–6m, Forex/MT5-first) y hallazgos históricos sujetos a revalidación.
- [[Echo - Cierre del Lab y Limpieza del Journal]] y [[Echo - Reporte de Estado Lab y Journal 2026-08-21]] conservan evidencia reportada de producción de agosto. Sus cifras no se elevan a inventario vivo de septiembre.
- Documentación externa primaria consultada para la semántica del reloj: [MQL5 local/server time](https://www.mql5.com/en/book/common/timing/timing_local_server), [TimeGMT](https://www.mql5.com/en/docs/dateandtime/timegmt). No prueba wiring local ni calidad de timestamps existentes.

## Lifecycle

Snapshot de fuentes fechado. No reemplaza el código ni los contratos owner; la síntesis canónica está en el master Resource enlazado. Una auditoría posterior contrasta nuevos commits y evidencia física sin borrar este baseline.

## Revalidación de seam posterior al snapshot — 2026-09-06

Consumidor: [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]], ledger de source/superficies en §10. S Echo local limpio e25165ba y master remoto04c16bd reconfirmados por git. Source inspeccionado en e25165ba; objeto remoto ausente y gh sin auth impidieron una nueva comparación readiness-only (la previa permanece evidencia fechada). SSH a core rechazado por autenticación; runtime actual U, P de revisión independiente no rejuvenecida. Nuevas lecturas: ReferenceEvent/TradeClose/TradeMapper, raw_trade_events029, Gateway, planner/MM/close_handler, policy/definition schema; ningún query de performance/DB.
