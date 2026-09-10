---
type: decision
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
  - "[[2026-09-04-mt5-terminal-build-unsupported]]"
aliases:
  - EXPLICIT_CERTIFIED_BUILD_ALLOWLIST
  - MT5 report 6140 compatible con mt5-report.v1
confidence: verified
source_session: ECHO-FORGE-MT5-REPORT-BUILD-COMPATIBILITY-AND-ALLOWLIST-RCA-V1-TOP
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-09-04-echo-forge-mt5-report-6140-compatible-allowlist

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- CERT-A 0.2.90 (`CampaignRef` `baeb747d-1cb9-4cbc-8903-58d91f64c720`, `FlowRunRef` `67d81075-ef71-4f40-82cb-10dd2201fd9a`) falló en `mt5_reconcile_v1` con `mt5 report: build not supported: build=6140` tras un `MT5BacktestArtifactWorkflow` COMPLETED success. El parser v1 fija `SupportedBuild = 6090`.
- RCA TOP sobre baseline `32d0740ccb0fe6ee04e016eef874790bc8684efc` comparó el HTM físico 6140 contra el contrato `mt5-report.v1` y el corpus 6090 (4 fixtures). C3 permanece `BLOCKED / CLOSED`. Esta sesión no implementó source.

## Decisión

- **BUILD_6140_COMPATIBILITY = COMPATIBLE_WITH_MT5_REPORT_V1.** Clasificación primaria: `SUPPORTED_FORMAT_UNCERTIFIED_BUILD`. `parser_version` permanece `mt5-report.v1`.
- **Autoridad de builds:** allow-list explícita de builds certificados, no un único `SupportedBuild` exacto ni un rango abierto. Conceptual: `SupportedBuilds = {6090, 6140}` con helper `isSupportedBuild(build int)` (switch KISS). Build desconocido sigue `ErrBuildNotSupported`. Sin `build >= N`, sin `accept any`, sin warn-and-continue.
- **Ambiente / auto-update:** OPTION B. Permitir updates de MT5; el parser permanece fail-closed hasta certificar el build. No pinnear el terminal ni deshabilitar auto-update como requisito de producto. Un probe operacional de `FileVersion` vs allow-list es higiene de certificación, no un pin.
- **Margin Level `414.35%`:** primera instancia poblada del corpus (6090 tenía el label vacío → `MISSING NOT_REPORTED`). El parser v1 vigente lo tipa `INVALID`/`pattern_mismatch` y **no** falla `Parse()`. No reinterpretar en el fix mínimo; no es drift estructural ni nueva `parser_version`.

## Rationale

- Encoding, 2 tablas, headings, headers Orders/Deals (11 y 13 columnas), labels Settings/Results, gramáticas Period/Volume/Price/Deals y los 7 crosschecks son los de `mt5-report.v1`. `Build 6140` aparece una sola vez, en la fila `Darwinex-Demo (Build 6140)`.
- Ignorando únicamente el gate `build != 6090`, `Parse()` retorna nil; `Normalize()` produce `TradeSet COMPLETE` (43 trades). El único campo contractual no-OBSERVED nuevo es `margin_level` INVALID, ya contemplado por `parseMarginLevel`.
- Un único `SupportedBuild` exacto es lo que bloqueó C3 frente a un formato ya soportado. Un mínimo/máximo abierto violaría fail-closed.

## Consecuencias

- NEXT EXACT: `ECHO-FORGE-MT5-REPORT-CERTIFIED-BUILD-ALLOWLIST-6140-FIX-NORMAL` (allow-list + fixture/golden 6140 + tests; sin workflow/Campaign/scoring). Después, recert C3 con identidad CERT-A nueva. No reutilizar `baeb747d…`.
- Replay Temporal: el gate vive en la activity `mt5_reconcile_v1`; ampliar la allow-list no cambia decisiones de workflow ni requiere `GetVersion`. Histories FAILED existentes no se reescriben.
- C3 no se reabre en esta sesión.

## Alternativas descartadas

- Pin/downgrade del terminal a 6090 (OPTION A): innecesario dado compatibilidad demostrada; reduce disponibilidad y no escala a builds futuros.
- `build >= 6090` o accept-any: viola fail-closed.
- Nueva `parser_version` por Margin Level poblado: el status INVALID ya es el contrato v1 para gramática no-plain de ese campo; no hay branch por build ni fallback.
- Certificar 6140 con una Campaign completa: un HTM físico durable (este) basta para PARSER BUILD CERTIFICATION, separado de FULL C3.
