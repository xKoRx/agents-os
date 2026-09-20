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
  - cert-f04-01 c13 2026-09-20
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

# 2026-09-20 — CERT-F04-01 C13: recuperación de RERUN-6 y certificación PASS

## Objetivo

Mandato maestro F05C-CERT-F04-01-C13: publicar el fix aprobado del defecto #6 (`25a5122…`), recuperar de forma segura la ejecución existente RERUN-6 (evitando repetir los cinco backtests físicos) y completar CERT-F04-01 si la evidencia y la SPEC lo permitían.

## Ejecución (resumen)

- G0 inventario vivo: RERUN-6 viva en retry benigno del seal (attempt 16, backoff máx 30 m); miembro `7508a66c…` en estado C (versión+manifest+delivery `UNAVAILABLE`), miembros 2–5 vírgenes por el loop fail-fast; ETCD echo 0 keys; `MT5_PROCS=0`.
- G1 ensayo realista (corrigió la brecha de C12): actividad real + máquina de estados real + `FailClosedIngress` real de producción sobre los 5 miembros auténticos y 20 artefactos SHA256-verificados; ancla byte-exacto (effective-inputs regenerado == objeto real `33937102…`); 5/5 `HANDOFF_CREATED`/0 POST/sin duplicación; suites y gate 6182 PASS, fallos idénticos al baseline.
- G2/G3: release `0.2.104` publicada (FF `2993da0→25a5122`, authority CONSISTENT, 6/6 SHA == manifest, `vcs.revision=25a5122`) y rollout Stager 4/4 certificado (Windows `exe_sha256 c250d7dd…` EXACT).
- G4 recuperación natural: el attempt 17 (14:23:32Z) fue atendido por los workers `0.2.104`; seal 5/5 `HANDOFF_CREATED` + `ingested=false` con VersionRefs/IdempotencyKeys reales; campaña `f50e5cdb…` `COMPLETED/TARGET_REACHED` con 5 finalistas; Running=0; write-once intacto; 0 POST.
- G5–G7: `CERT_F04_01_PASS` por lectura literal de los 4 criterios (con atribución por etapa: productoras `2993da0`, seal/delivery `25a5122`); seguridad PASS; `RERUN-7 NOT_REQUIRED` (cero campañas nuevas).

## Veredicto

**CERT-F04-01 = PHYSICALLY CERTIFIED (PASS)**; `RERUN6_RECOVERED`; `RERUN7_NOT_REQUIRED`. `HANDOFF_CREATED ×5` es el terminal contractual con Echo sin configurar (INGESTED pertenece a CERT-E04-01/CERT-F04-03). Se evitó un séptimo ciclo físico completo (~3.5 h). Ver delta completo en [[Echo + Echo Forge — Deferred Certification Backlog]] y change log `2026-09-20-echo-forge-cert-f04-01-c13-recovery-certified`.

## Estado final y próximo paso

Flota 4/4 en `0.2.104`/`25a5122`; allocations `26090011001–018` write-once intactas; ambos workflows de RERUN-6 terminales. Próximo gate del orden frozen: **CERT-F04-02 (golden auténtico / T2.11)**, desbloqueado con los preimages SHA-anclados del FlowRun `c71687ca…`.
