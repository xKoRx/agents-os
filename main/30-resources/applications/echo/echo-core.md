---
type: application
schema_version: 1
status: active
area: "[[Echo]]"
lang: Go
github: "https://github.com/xKoRx/echo"
path: "xKoRx/echo (árbol activo v3/)"
last_verified: "2026-09-12"
confidence: verified
aliases:
  - Echo Core
  - echo-core
  - xKoRx/echo
tags:
  - application
  - kind/application
created: 2026-07-03
updated: 2026-09-13
---

# Echo Core

%% Naming: echo-core es el link canónico de la aplicación; aliases puede incluir repo, nombre viejo o sistema externo; tags/slugs no reemplazan links. %%

> [!info]+ Echo Core
> **Rol:** plataforma de ejecución y registro de trading (runtime v3) · **Área:** [[Echo]] · **Lang:** Go (+ EAs MQL, front Vue)
> **Repo:** `xKoRx/echo` · **Baseline citado:** `xKoRx/echo@f7ddea18` (branch `feature/e02-control-safety-journal-recovery`; master `a99f9a63`)

## 🎯 Responsabilidad (estable)

- Ejecutar el ciclo de trading de extremo a extremo: EAs MT4/MT5 → Echo Bridge (Windows, named pipes) → Kafka → Core (Flink StateFun: StrategyConfig → ExecutionPlanner → MMEngine → TradeJournal) → Kafka `echo.core-commands.v1` → Bridge → EA de ejecución. El Gateway queda FUERA del hot path de trading (webhooks, control, automation, boundary Forge).
- Mantener el diario de operaciones durable (Trade Journal en PostgreSQL, esquema `echo`) con cuarentena determinística de payloads en conflicto y CLI de recuperación sin Kafka (`v3/tools/journalctl`).
- Ser el RECEPTOR de la frontera Forge→Echo: expone `POST/GET /api/v1/forge/promotions` para ingestión de `HandoffManifestV1`; la ingesta produce sólo receipt `INGESTED` y nunca activación (ver [[echo-forge-integration-boundary]]).
- Poseer la identidad canónica compartida: contratos frozen en `v3/sdk/contracts` (identidad ≤1024 bytes, HandoffManifestV1, receipt único INGESTED); Echo nunca asigna ni recicla magic (ownership Forge).

## 🔌 Contratos e interacciones (semi-estable)

- **Expone:** Gateway HTTP (puerto 8082): `/health`, auth hook Hasura, webhooks de config (account-config, symbol-mapping, automation-profiles, execution-policy), `POST /api/v1/close-positions`, `POST /api/v1/admin/republish`, boundary Forge (`POST /api/v1/forge/promotions` + 2 GET de reconciliación).
- **Consume/produce:** 17 topics Kafka canónicos declarados en `xKoRx/echo: v3/sdk/domain/snapshots.go` + topic por cuenta `echo.commands.<account>.v1`; productor durable `PublishSync` para facts de trading.
- **Persistencia:** PostgreSQL único esquema de app `echo` (migraciones 001..062: núcleo, identidad BWC 061, cuarentena 062); etcd para config por servicio+env; Hasura como único GraphQL del front.
- **Forge:** receptor del boundary — detalles, matriz de errores y gaps en [[echo-forge-integration-boundary]]; contrato vigente en [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] y contratos F-0x.
- **Observabilidad:** OpenTelemetry OTLP (logs/metrics/traces) con semconv por servicio.

## 🧩 Implementación (volátil · last_verified: 2026-09-12)

- **Stack:** Go v3 (Core/Gateway/Bridge/SDK/lab-worker/toolkit), Flink StateFun vía HTTP (la orquestación NO es Temporal: cero dependencias `go.temporal`), PostgreSQL, Kafka (Sarama), etcd, Hasura, front Vue 3 + Vite, EAs MQL MT4/MT5 + DLLs.
- **Auth por 4 actores (E-02, BRANCH-ONLY en `f7ddea18`, no en master `a99f9a63`):** `front_read`, `config_operator`, `control_operator`, `service_hasura_webhook`; tokens por env/etcd, fail-closed, 401 vs 403, hook Hasura emite sólo roles `readonly`/`config_operator`; front con session tokens por actor, sin admin secret en bundle.
- **Resilience:** productor síncrono durable Bridge→Kafka; cuarentena de journal (`echo.journal_quarantine`, razones POISON_PAYLOAD/CLOSE_WITHOUT_OPEN/conflictos) con ACK a Flink; `journalctl` (`quarantine list/show/resolve/discard`, `replay-facts` PG→PG garantizado sin Kafka por `deps_guard_test.go`); replay idempotente de ingestión Forge (200 exact-replay / 409 conflictos).
- **Legacy conviviente:** binario `v3/core/cmd/echo-functions` DEPRECATED; topics `echo.account-snapshots.v1`/`echo.instrument-snapshots.v1` DEPRECATED; módulos v1/v2 aún en `go.work` (el activo es v3).

## 🚨 Estado y gaps conocidos (volátil · last_verified: 2026-09-12)

- E-02 está en el branch como código + tests CONTRACT PASS pero PHYSICAL_PARTIAL: compose Flink/PG/Kafka/Hasura real no ejecutado (T14/T15); el branch no está mergeado a master.
- Receptor Forge E-01/E-04: integrado en master, E-04 INTEGRATED pero FINAL CLOSED = NO (T21/AC-37 CROSS_LANE GOLDEN pending, `FORGE_GOLDEN_FIXTURE_PENDING`).
- Sin backend de artefactos en V1: producción usa `unavailableArtifactSource` (503 fail-closed) → ningún primer accept end-to-end posible hoy (gap G3 del boundary).
- Post-INGESTED no hay consumidores: cero provisioning/activación/capital/Kafka (impuesto por tests de non-effects y REVOKE en DB); E-06+ es frontera futura.
- La wiki no decide producto: estos gaps se documentan, no se resuelven aquí.

## 📌 Provenance

- **Repo:** `xKoRx/echo` (path: `v3/`; README, `v3/docs/ARCHITECTURE|DATA_MODEL|FLOWS|OBSERVABILITY|TROUBLESHOOTING.md`, `docs/adr/`, `specs/SPECS.md` como índice de estado por feature).
- **Sources:** [[Echo — Fuentes de implementación 2026-09-12 (f7ddea18)]] · [[Echo — Fuentes de arquitectura y producto 2026-09-06]] (provenance histórica master 04c16bd).
- `last_verified: 2026-09-12` · `confidence: verified` (contraste directo contra `f7ddea18`, artifact 02).

## 🔗 Links

- [[echo-core-changelog|Bitácora de Cambios (Changelog)]] · [[echo-forge]] (fábrica cuantitativa upstream) · [[echo-forge-integration-boundary]] (frontera) · [[Echo]] (área madre)
- Índice del subdominio: [[30-resources/applications/echo/00-index|Echo — Índice]]
