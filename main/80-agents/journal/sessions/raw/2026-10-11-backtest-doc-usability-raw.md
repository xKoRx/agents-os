---
type: raw_session
schema_version: 1
scope: session
created: "2026-10-11"
updated: "2026-10-11"
area: "[[Personal]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
related:
  - "[[BTX-PERF-LAST-FINAL]]"
aliases: []
confidence: verified
source_session: sess_2299342a-86fe-4ca6-9ad2-b9979bff02e9 (ZCode)
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-raw.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-10-11-backtest-doc-usability-raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: ZCode / account:zai-individual-coding-plan/GLM-5.3-Flash, LOCAL TOP Owner, fresh-context ONE-SHOT.
- Proyecto o entidad: [[Echo Futures]] — prueba de usabilidad del manual `v3/backtester/README.md @ c75023c8` contra el paquete `btx-perf-last-20261010`.
- Objetivo de la sesión: instalar el paquete y ejecutar BASIC+CAMPAIGN NQZ5 + replays usando exclusivamente el manual; calificar la documentación /10.

## Transcript

```
[Bootstrap] agents-os.md + SKILL.md bootstrap; constitución, perfil rjara, nota interna global, INDEX de skills. Entidad: Echo Futures (manual backtester).

[Manual] URL anónima 404 → gh api autenticado OK. README 43.332 bytes, SHA256 0ae8eedd…, commit c75023c8 (2026-10-11T05:19:50Z). Leído completo (542 líneas). Guardado en ~/aranea/work/bt-doc-usability-20261011/.

[§2.1] Requisitos OK: Linux x86_64; gh/tar/sha256sum/python3; gh auth xKoRx; 16G libres; sin instalación previa en ~/echo-backtest-873.
[§2.1] mkdir BT_HOME + download + package. OK.
[§2.2] gh release download 5 assets (rc0, ~60s, 1.327.842.399 bytes). FINAL-ASSET-SHA256SUMS 3/3 OK. tar -xzf ×3 (rc0). SHA256SUMS 3494/3494 OK. Hash binario 0320b80e… OK. find = 3495 archivos físicos (diferencia = SHA256SUMS mismo).
[§2.3] test bin/echo-backtest + 2 requests + descriptor corpus OK; mkdir -p runs replay reports logs. PACKAGE-IDENTITY.json: source 873f5f1c, bin 0320b80e, go1.27.1.

[§3.1] BASIC NQZ5 → runs/basic-NQZ5-01: rc0, 858s. assert execution_state==COMPLETE OK; terminal_reason None; artifact basic/bt-b8a466…/result.json.gz. Emite catalog-validation.json, daily-report.json (92 filas), phase-wall.json, experiment-manifest.json.
[§3.2] CAMPAIGN NQZ5 → runs/campaign-NQZ5-01: rc0, 604s. COMPLETE/HORIZON_REACHED. campaign-result.json: caja 5000→4400, compras 5, cobros 0, 4 BURNED_RISK_BREACH + 1 ACTIVE_AT_HORIZON (saldo 98000.12).
[§3.3] reproduce BASIC (1185s, rc0): verdict IDENTICAL, identical true. reproduce CAMPAIGN (988s, rc0): verdict IDENTICAL, identical true.

[§4.1] Reportes diarios consultados: BASIC 39 ops con fills / 22 días entrada / 24 elegibles; CAMPAIGN 15 / 6 / 24.
[Artefacto] result.json.gz BASIC: summary.economics balance 70307.92, realized_net −29692.08 (gross −25230, costos 4462.08). CAMPAIGN: balance 98000.12; neto 5 cuentas = −10.576,28. Todo coincide con §4.3.
[§8 spot-check] bin/echo-backtest --help NO lista experiment/campaign — síntoma documentado verificado.

[Entrega] BACKTEST-DOC-USABILITY-REPORT.md: EJECUTABLE_SOLO_CON_DOC, nota 9/10 (2+2+2+1+2), 5 problemas menores documentados. Copia en vault artifacts/backtester-gerard-bankroll/. 0 procesos backtest pendientes.

[Cierre] feedback + L0 + change_log materializados (materialize_schema_note.py; tipos feedback/raw_session/change_log); commit master + readback.
```

## Evidencia externa

- Manual bajo prueba: `~/aranea/work/bt-doc-usability-20261011/README-manual-under-test.md`.
- Informe de entrega: `10-projects/Echo Futures/artifacts/backtester-gerard-bankroll/BACKTEST-DOC-USABILITY-REPORT.md`.
- Salidas del operador: `~/echo-backtest-873/package/{runs,replay,logs}` (runs/basic-NQZ5-01, runs/campaign-NQZ5-01, replay/*, logs/*).
