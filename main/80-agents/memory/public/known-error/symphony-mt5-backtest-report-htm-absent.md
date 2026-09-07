---
type: known_error
schema_version: 1
scope: application
created: "2026-08-14"
updated: "2026-08-14"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[symphony]]"
entities:
  - "[[Symphony]]"
  - "[[Echo Forge]]"
related:
  - "[[symphony-mt5-compile-ex5-absent]]"
  - "[[stager-g3-lifecycle-accepted-e2e-is-next]]"
  - "[[symphony-deploy-release-go-stager-cutover-gap]]"
aliases:
  - report_not_found
  - reporte .htm ausente o vacío
  - tester csv sin htm
confidence: verified
source_session: 11f6babe-3522-40c1-bb09-f29b5012c34d
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - area/echo
  - tech/mt5
  - project/echo-forge
---

# symphony-mt5-backtest-report-htm-absent

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Child `mt5-backtest-*` COMPLETED con `status=failed`, `error_code=report_not_found`, `error_message=reporte .htm ausente o vacío`.
- Tester log: `Test passed` + `automatic testing finished`; evidencia incluye `.tester.ini`, `.tester.log`, `.csv` del EA, no `.htm`.

## Causa

- MT5 portable sí escribe el `.htm` con `Report=` relativo anidado. El Strategy Tester bajo `NT AUTHORITY\SYSTEM` (`StagerRuntime` LocalSystem, sesión 0) completa `Test passed` y **no materializa HTML**. El mismo INI y el mismo `os/exec`+pipes como `kor` sí dejan `.htm` ~28KB.
- `ArtifactRunner` exige `reportBase + ".htm"`; si SYSTEM no lo escribe, Symphony clasifica `report_not_found`.

## Impacto

- E2E Stager (Started + Tester passed) no se bloquea. El artifact de backtest Symphony no sube reporte HTML/métricas parseadas.

## Detección

- Result JSON `operation=backtest` + `report_not_found` con `evidence` sin `.htm`.
- Owner de `sqx-mt5-worker.exe` = `SYSTEM` y `StagerRuntime.StartName=LocalSystem`.
- Tester log UTF-16 con `Test passed` y `automatic testing finished`.

## Mitigación

- Correr `StagerRuntime` / `sqx-mt5-worker` como `kor` (`install-stager.ps1 -ServiceUser kor -ServicePassword …`; `SeServiceLogonRight`). No reabrir Stager F3/G3 por el path `Report=`.

## Evidencia

- 2026-08-14 Kronos Windows `192.168.31.128`: SYSTEM schtasks → HTML ausente; `kor` cmd/`os/exec` pipes → HTML 28332–28388. Servicio dejado en `StartName=.\kor`.
