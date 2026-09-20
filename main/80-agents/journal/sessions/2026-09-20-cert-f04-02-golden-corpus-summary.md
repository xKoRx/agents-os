---
type: session_summary
schema_version: 1
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Echo]]"
project: "[[Echo Forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo + Echo Forge — Deferred Certification Backlog]]"
  - "[[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]"
related:
  - "[[Echo — E-04 Forge Ingestion E1]]"
aliases:
  - cert-f04-02 golden corpus 2026-09-20
confidence: verified
source_session:
share_scope: local
load_policy: manual
indexable: true
index_priority: low
tags:
  - kind/session-summary
  - scope/session
  - area/echo
  - project/echo-forge
---

# 2026-09-20 — CERT-F04-02: golden auténtico de RERUN-6 capturado, verificado y persistido

## Objetivo

Mandato maestro F05C-CERT-F04-02: capturar y preservar el golden auténtico de Forge producido por la campaña física RERUN-6 (todos los bytes, identidades, evaluaciones, versiones y manifests necesarios para reproducir y verificar el handoff), ejecutando los gates hasta PASS o bloqueo causal; sin campañas, backtests, releases ni POST a Echo.

## Ejecución (resumen)

- G0 autoridad fresca: workflows RERUN-6 terminales (Completed 14:23:33Z, 0 pending), campaña `COMPLETED/TARGET_REACHED ×5`, DecisionRef `ed703eeb…` desde el resultado durable de promotion, ETCD echo 0 keys, 10 evaluaciones Mongo con refs durables, 5 effective-inputs MinIO con atribución por etapa (1×0.2.103, 4×0.2.104).
- G1 inventario desde el contrato (`BuildHandoffManifest`/`HandoffManifestV1` @`25a5122`); HTM/scores/snapshots omitidos del corpus autocontenido porque el contrato demuestra que no son preimages del manifest (refs registradas).
- G2 25/25 preimages byte-exactos (SHA256+size == refs durables; cross-check C13 20/20 + ancla `33937102…`); releases verificadas 4/4 con `vcs.revision` (`0.2.104` symphony `a81aa5a1…` y exe `c250d7dd…` EXACT vs C13).
- G3 recomputación con el código real @`25a5122` (worktree desechable, sin residuo): readbacks SQX/MQ5 == magic, logs 0-errors con el gate real, effective-inputs reproducidos byte-exacto, **VersionRefs e IdempotencyKeys recomputados == outputs físicos del seal**; producer `echo-forge-handoff` demostrado por log físico del worker (14:23:32Z) + Temporal.
- G4/G5 corpus durable `~/aranea/work/f04-cert-f04-02/corpus` (manifest machine-readable, validador contractual PASS con 3 negativos, recomputación re-ejecutada 5/5). Limitación declarada: bodies de manifests/versions write-once en PG `trading_systems_test` sin canal autorizado → por referencia con garantías verificadas y capability requerida registrada.
- G7 paquete de continuidad CERT-E04-01 (`HANDOFF-E04-PACKAGE.md`): fixture vs POST real, canales autorizados, dependencias.

## Veredicto

**CERT_F04_02_PASS** (10/10 criterios del mandato; criterios del backlog satisfechos literalmente). T2.11 satisfecho; T2.12 conserva CERT-F04-01 PASS; T2.13 OPEN. HANDOFF_CREATED ≠ INGESTED: CERT-E04-01 y CERT-F04-03 siguen pendientes del join real con Echo. Ver delta completo en [[Echo + Echo Forge — Deferred Certification Backlog]], change log `2026-09-20-echo-forge-cert-f04-02-golden-corpus-pass` y `VERIFICATION.md` del corpus.

## Estado final y próximo paso

Corpus persistido y validado (tree digest `4a266cba…`); sin efectos laterales físicos (0 campañas/backtests/POST/releases; write-once intacto). Próximo gate único: **CERT-E04-01 (Echo cross-lane golden / T21)** — su prerrequisito material es resolver la identidad de lectura `sqx` sobre `trading_systems_test` para obtener los bodies canónicos de los manifests (o autorización owner equivalente) y contar con el runtime Echo E-04 desplegado.
