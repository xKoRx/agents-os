---
type: known_error
schema_version: 1
scope: project
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-09-04-echo-forge-c3-lean-0290-blocked-mt5-build]]"
  - "[[2026-09-04-echo-forge-mt5-report-6140-compatible-allowlist]]"
  - "[[2026-09-04-echo-forge-mt5-report-6180-compatible-allowlist]]"
  - "[[2026-09-03-orphan-mt5-after-cancel]]"
  - "[[2026-09-02-echo-forge-c3-mt5-fidelity-period-mismatch]]"
aliases:
  - MT5 build 6140 no soportado
  - MT5_TERMINAL_BUILD_UNSUPPORTED
confidence: verified
source_session: ECHO-FORGE-RELEASE-0.2.90-AND-C3-LEAN-RECERT-NORMAL
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - project/echo-forge
---

# 2026-09-04-mt5-terminal-build-unsupported

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- `mt5_reconcile_v1` falla cerrado con `mt5 report: build not supported: build=6140` (`contract_error`, `retryable: false`); el Generic muere en `09_mt5_backtest` tras un backtest físicamente exitoso.

## Causa

- El terminal MT5 físico de `worker-kronos` (`192.168.31.128`, `C:\MT5\test\terminal64.exe`) es build `5.0.0.6140` (mtime 2026-09-02 19:18 local Windows, auto-update de MetaTrader). El parser congelado de reportes fija `SupportedBuild = 6090` (`sqx/adapters/mt5/report/types.go`, SPEC-PARSER §4) y rechaza cualquier otro build por diseño fail-closed.

## Impacto

- Ningún backtest MT5 que complete puede reconciliarse: `Score` `mt5_fidelity_shadow.v1` no obtiene `MT5_NATIVE` ⇒ ningún promoted finalist con score `COMPUTED` ⇒ C3 no puede alcanzar strong PASS en esta flota. No es regresión de 0.2.90: el contrato del producto operó correctamente.

## Detección

- CERT-A 0.2.90 CampaignRef `baeb747d-1cb9-4cbc-8903-58d91f64c720`: el history muestra `ActivityTaskFailed` ev=210 y `WorkflowExecutionFailed` ev=220 con identity `972535@sqx-ulab-kron-0@`; el `MT5BacktestArtifactWorkflow` hijo completó `status success` segundos antes. El smoke de cancelación 0.2.88 nunca ejercitó reconcile de éxito (cancela antes), por eso el drift pasó inadvertido.

## Mitigación

- RCA TOP 2026-09-04 ([[2026-09-04-echo-forge-mt5-report-6140-compatible-allowlist]]): 6140 es `COMPATIBLE_WITH_MT5_REPORT_V1`. Desbloqueo correcto = allow-list explícita `{6090, 6140}` en `mt5-report.v1` + fixture físico 6140 + tests, luego recert C3 con identidad nueva. No pinnear/downgradear el terminal (OPTION A descartada). No `build >= N`.
- **IMPLEMENTADO 2026-09-04** (misión `ECHO-FORGE-MT5-REPORT-CERTIFIED-BUILD-ALLOWLIST-6140-FIX-NORMAL`): commit `9641c9f11b2a321041f61ea6b8d93ef199d5a38e` — `isSupportedBuild{6090,6140}`, fixture `FIX-B6140-75`. El patrón se repitió: Live Update llevó el terminal a `5.0.0.6180`; recert Finalist Factory V1 release `0.2.95` falló cerrado pre-Campaign (`MT5_RUNTIME_BUILD_NOT_CERTIFIED`). TOP 2026-09-04 ([[2026-09-04-echo-forge-mt5-report-6180-compatible-allowlist]]) clasificó 6180 como `SUPPORTED_FORMAT_UNCERTIFIED_BUILD` / `COMPATIBLE_WITH_MT5_REPORT_V1`. Source vigente sigue `{6090,6140}` hasta el NORMAL de allow-list. No pinnear el terminal. NEXT EXACT: `ECHO-FORGE-MT5-BUILD-6180-ALLOWLIST-V1-NORMAL`.

## Evidencia

- Terminal: `Get-Item C:\MT5\test\terminal64.exe` → `FileVersion 5.0.0.6140`, `LastWriteTime 2026-09-02 07:18:53 PM`. Sin huérfanos tras el fallo (`terminal64=0`, `metatester64=0`). FlowRun `67d81075-ef71-4f40-82cb-10dd2201fd9a` FAILED; campaña FAILED / `WAVE_FLOW_RUN_FAILED`, `waves=1`, `finalists=0`.
- HTM durable CERT-A: bucket `sqx-strategies`, key `durable/mt5-export/v1/67d81075-ef71-4f40-82cb-10dd2201fd9a/75ed071a-7096-445b-9d0e-93aa117f8497/sha256:0b74ba3d8dc3e508f1d2202677194aa681140bd445d63273a2820f0093e45148/09_mt5_backtest/final-75ed071a-7096-445b-9d0e-93aa117f8497.htm`, size 173030, SHA-256 `efbd37e417b287b262a1b27d6764ad4e001ca01b402d5c5faef63f9df4ef49f8`. Child `mt5-backtest-forge-campaign-baeb747d-1cb9-4cbc-8903-58d91f64c720-wave-000001-94b3c83566ef947b` RunID `01a06ae7-4911-71c9-bd2d-54211dc7b7b0` status Completed success. StrategyRef `75ed071a-7096-445b-9d0e-93aa117f8497`.
