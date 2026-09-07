---
type: change_log
schema_version: 1
scope: session
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-09-04-campaign-generic-mt5-backtest-cap]]"
aliases: []
confidence: verified
source_session: "ECHO-FORGE-CAMPAIGN-GENERIC-MT5-BACKTEST-HARD-CAP-V1-NORMAL"
source_feedbacks:
  - "[[2026-09-04-echo-forge-campaign-generic-mt5-backtest-hard-cap-session-feedback]]"
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-04 Echo Forge Campaign Generic MT5 Backtest Hard Cap

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated / deleted / conflict-resolution
- **Archivo(s):**
  - `sqx/workflows/generic_workflow.go`
  - `sqx/workflows/mt5_backtesting_integration_test.go`

## Motivo

- Cerrar el error conocido `CAMPAIGN_GENERIC_MT5_BACKTEST_CAP_NOT_ENFORCED` detectado durante la certificación física de release 0.2.94, manteniendo fuera de alcance Replenishment, BuilderSupplyBatch, schemas, migraciones y release/deploy.

## Fuentes usadas

- Baseline confirmado y preservado: HEAD/origin/master `9ef5549da3308b286ecff52f2d825af8024c27fe` antes del cambio; SDK en `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`; evidencia física Wave2 g000002 como suministro genuinamente nuevo.

## Resolución aplicada

- Se añadió la autoridad única cuatro y el preflight en `executeMT5ArtifactTask`, después de conocer el plan exacto de backtest y antes de `startMT5ArtifactChildren`; sólo activa con `ForgeCampaignWave` tipado y nunca trunca ni selecciona los primeros cuatro.

## Validación

- H1-H12 dirigidos PASS: H4 observó exactamente cuatro children; H5 y H6 observaron cero; H7 probó compile cinco con un fallo y cuatro backtests; H8 dejó compile intacto y bloqueó cinco backtests; cero-supply, determinismo y lifecycle de cancelación permanecen sin regresión.
- `go test -race -count=1 ./sqx/workflows -run 'TestMT5BacktestingIntegration_CampaignHardCap'` PASS y `go vet ./sqx/workflows/...` PASS. La suite completa de workflows conserva fallos baseline por fixtures sin `flow_run_start`; `go test ./sqx/...` además encontró `sqx/tools` con múltiples `main` y quedó interrumpida tras más de diez minutos en `registry-postgres`.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit `0f18ef0` sólo mediante un commit posterior revisado; no se revirtieron cambios foráneos del working tree y no se creó 0.2.95.
