---
type: agent_memory
schema_version: 1
scope: project
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-09-04-echo-forge-mt5-report-6180-compatible-allowlist]]"
  - "[[2026-09-04-echo-forge-mt5-report-6140-compatible-allowlist]]"
  - "[[2026-09-04-mt5-terminal-build-unsupported]]"
  - "[[2026-09-04-zcode-glm-5-3-flash-echo-forge-mt5-6180-allowlist]]"
aliases: []
confidence: high
memory_state: active
continuity_key: echo-forge/mt5-build-cert-and-finalist-factory-recert
load_policy: when_echo_forge_loaded
indexable: false
index_priority: never
tags:
  - kind/agent-memory
  - scope/project
  - project/echo-forge
---

# Continuidad — MT5 6180 certificado en source; Finalist Factory espera release 0.2.96

## Continuidad

- HEAD / origin/master: `3b0737c1efe153f1f72eec40465fd1aa883887d0` (`feat(mt5): certify report build 6180`), hijo de baseline `0f18ef0440e104c6a38ba4cc259f674cfad3c390`. SDK: `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`. Release desplegada sigue `0.2.95`; `0.2.96` NO creada (misión lo prohíbe). Dirty foráneo preservado sin stagear.
- MT5_REPORT_V1_BUILD_6180: `CERTIFIED / CLOSED`. Allow-list source en `sqx/adapters/mt5/report/types.go` `isSupportedBuild` = `{6090,6140,6180}` (la misión decía `parse.go`; la autoridad real es `types.go`). `ParserVersion` intacto `mt5-report.v1`; sin branch por build.
- Fixture físico durable en git: `specs/FEAT-SQX-MT5-RECONCILIATION-SCORING/fixtures/XAUUSD_H1_build6180_20260504_20260605.htm` = `FIX-B6180-75`, SHA-256 `6c9e975fff5b9821257d250a9877bcba87f5adce69f14d3bc396821056076485`, 28572 bytes, UTF-16LE+BOM, `Darwinex-Demo (Build 6180)`, periodo `H1 (2026.05.04 - 2026.06.05)`, zero-trade (`mmLots=0.0`), ticks `11288069`, bars `550`. Provenance WORKER-KRONOS FileVersion `5.0.0.6180`, smoke `ParserCert6180\tester.ini`, sesión TOP `ECHO-FORGE-MT5-BUILD-6180-PARSER-CERTIFICATION-TOP`.
- Gates ejecutados: `go test`, `go test -race`, `go vet` en `./sqx/adapters/mt5/report/...` y `go test ./sqx/adapters/mt5/...` completo (mt5, binding, normalization, report, scoring) — todos PASS. B1–B12 PASS; 7/7 crosschecks; 6179/6181/6200 fail-closed con build observado en `ErrBuildNotSupported`; corpus SHA integrity PASS; ≤6 archivos.
- Residual no bloqueante: hint stale `allow-list: 6090, 6140` en `parse.go:158` (`StructureUnknownError` fila build ausente; path de error distinto, cosmético) — candidata a higiene futura, NO urgente. Margin Level 6140 `414.35%` INVALID sigue deuda congelada; 6180 ZT es `MISSING NOT_REPORTED`. El 6180 ZT no ejercita filas Orders/Deals operacionales (headers idénticos).

## Señales de carga

- Política congelada vigente: Live Update ON; fail-closed unknown; certificar build por build explícito; sin rangos; sin pin.
- Graphify de symphony sigue stale; no reparar. Autoridad: SPEC-PARSER / CORPUS / `types.go` (los tres actualizados en `3b0737c`).

## Próxima acción

- NEXT EXACT: `ECHO-FORGE-RELEASE-0.2.96-AND-FINALIST-FACTORY-V1-FINAL-PHYSICAL-RECERT-NORMAL` — crear release `0.2.96` desde master (contiene la autoridad 6180) y ejecutar la recert física final acotada de dos olas del Finalist Factory V1. No reutilizar identidades de Campaign previas.
