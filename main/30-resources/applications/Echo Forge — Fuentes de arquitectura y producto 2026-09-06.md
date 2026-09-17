---
type: source
schema_version: 1
status: active
area: "[[Echo]]"
source_url: "https://github.com/xKoRx/symphony/tree/a10c26c887e4d203b403d2557e292ed773830b0e/sqx"
repo: "xKoRx/symphony"
path: "sqx/"
author: "xKoRx"
captured: "2026-09-06"
aliases: []
tags: ["kind/source", "area/echo"]
created: "2026-09-06"
updated: "2026-09-06"
---

# Echo Forge — Fuentes de arquitectura y producto 2026-09-06

## Referencia

- **Origen resoluble:** `xKoRx/symphony`, `sqx/`, master `a10c26c887e4d203b403d2557e292ed773830b0e` (2026-09-06). [Commit](https://github.com/xKoRx/symphony/commit/a10c26c887e4d203b403d2557e292ed773830b0e).
- **Fecha de captura/verificación:** 2026-09-06; HEAD y master remoto coinciden. Dirty ajeno de config/manifest/fixtures/specs preservado y excluido de autoridad release.
- **Locators detallados:** ledger F01–F10/D01–D04/P01–P04 de [[Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026]].
- **Dependencias:** SDK `xKoRx/sdk@c85594440f6755443ceb97ec4e333cd0ddb5b0ed`, Stager `xKoRx/stager@083dff2806cdc133a43a48ff461bca242d3129d1`; workspace [[echo-go-workspace]].

## Alcance

Generic/Campaign, PG identity/control/Decision migrations, Mongo evidence, MinIO contracts, Apply/Final Reretester/WFM bindings, MT5 parser/normalize/reconcile/scoring, slot allocator/lifecycle, Promotion/Result V1 y SPEC ingestion. Rutas auxiliares api-core/api-persist/mde inspeccionadas de forma acotada: no se encontró Finalist Ingestion allí. Sus commits y alcance están en el master.

## Notas de provenance

- [[2026-09-06-echo-forge-mt5-execution-model-v2]], [[2026-09-06-echo-forge-mt5-global-physical-ownership-v2]] y [[2026-09-06-echo-forge-finalist-model-v2]] son autoridad de intent frozen; NORMAL A está implementado, B/Finalist V2 pendientes al corte.
- [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]] conserva acta de release 0.2.96 y Campaign `0ac51a05-7bd8-49a8-a130-4c4e205d7084`, así como baseline/next exact vigente. El master preserva FlowRunRefs de dos FULL y diferencia certificación reportada de nueva ejecución.
- Evidencia física primaria conservada en repo: `specs/FEAT-SQX-MT5-PIPELINE-ARTIFACTS/evidence/owner-run/` (summary compile/backtest, HTM/tester settings). No se copió el dump al vault.
- Documentación primaria auxiliar: [Temporal activity failures/timeouts](https://github.com/temporalio/documentation/blob/main/docs/encyclopedia/detecting-activity-failures.mdx). SDK Temporal del módulo SQX `v1.35.0`; el pin `v1.44.1` citado en TOP es otra referencia de auditoría y no debe declararse runtime actual.
- Test focal de Forge/domain/report/scoring PASS cached; ningún backtest ni query a producción nuevo.

## Lifecycle

Snapshot de fuentes fechado, no nuevo cierre de proyecto. V1 permanece histórico/certificado en su alcance; contratos supersedidos y BWC están descritos en el master. No reescribe Decisions ni autoriza un tercer FULL.

## Revalidación de seam posterior al snapshot — 2026-09-06

Consumidor: [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]], ledger de source/superficies en §10. S Symphony HEAD/master `db8a022703082fd7ee9d1e15243c5d1b2feaf578`; SDK externo HEAD/master `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`. B1A/B1B/B2 presentes en commits185825c/ef65dd1/db8a022; Finalist C1/C2 aún pendientes según decision.go/promotionFinalists. Pin **declarado** sqx/go.mod sigue v1.35.0; go.work incorpora root cuyo require1.44.1 lleva la resolución local a v1.44.1 (`GOPROXY=off GOSUMDB=off go list -m -mod=readonly`). Esto corrige la inferencia de que el pin del módulo aislado basta para identificar todo build/runtime. Binario desplegado no verificado aquí. Las afirmaciones previas a10c26c permanecen históricas.
