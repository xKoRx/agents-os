---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[F — Decision Register]]"
  - "[[SHOT4_FIX_PACKAGE]]"
  - "[[SHOT4_FINAL_REPORT]]"
  - "[[SHOT3_ADVERSARIAL_REPORT]]"
aliases: []
tags:
  - kind/doc
  - area/echo
created: "2026-10-27"
updated: "2026-10-27"
---

# SHOT4_CORRECTION_LOG — Ingestion V2

## Propósito

Correction log del Shot 4 FINAL (C5/D4): fixes de los findings S3-A-01..06 del Shot 3, defectos nuevos descubiertos al completar el alcance J/L/F, gates re-ejecutados y SHA final integrado. Modelo: GLM-5.3-Flash Max LOCAL. Sin deploy, sin cutover, sin merge a runtime.

## Contenido

### C1. SHAs e integración (A4)

| Marca | Valor |
|---|---|
| BASE_SHA (remoto refrescado) | `d223d9f816338a831f5cf4c1acdc1c1ea9145917` (lab-v4/shot4-integration, ANCESTRY_OK) |
| Rama de trabajo | `feature/lab-v4-ingestion-v2-shot4` (nueva, worktree propio `/srv/echo-work/ingestion-v2-shot4-20261026/echo`) |
| FINAL_SHA integrado | `f93cd4f80085e328f9176c1215e42e6c8e0b2404` (ff-only push a lab-v4/shot4-integration; ls-remote verificado; 20 commits sobre d223d9f8, todos del Shot4) |
| Symphony | candidate `feature/lab-v4-ingestion-v2-shot4` @ `22f337c` (push; hija de `lab-v4/shot4-symphony@a0c68d1`; migración 017 + store + entry point `sqx/cmd/echo-ingest-v2`) |
| Build final | echo-gateway-harness `vcs.revision=f93cd4f8` `vcs.modified=false` go1.27.1 `-trimpath -buildvcs=true` (SHA256 en `harness/build_env4.sh`; identidad por buildinfo, S3-A-06) |

### C2. Findings S3-A-01..06 (criterio del paquete)

| ID | Corrección aplicada | Commit(s) |
|---|---|---|
| S3-A-01 (P2) | Routing exacto: POST sólo en `/api/v2/strategy-ingestions` (sufijos ⇒ 404 sin efectos); subtree GET de un segmento (id o by-key/{key}); regresión dedicada `TestShot4S3A01S3A02ExactRoutingAndMediaType` | `aa060160` |
| S3-A-02 (P3) | Media type parseado (`mime.ParseMediaType`) + type/subtype exacto + RECHAZO de parámetros (charset ⇒ 415; encoding identity B§3). El primer intento (sólo type/subtype) dejaba pasar charset — corregido tras la regresión propia | `aa060160`, `d5df5079` |
| S3-A-03 (P2) | `git rm` forward de `v3/core/echo-core` + gitignore (`v3/core/echo-core` y artefactos de build multi-main en raíz `/echo-core` — el mecanismo exacto se reprodujo en esta sesión) | `9fd9fccf`, `104df9a3` |
| S3-A-04 (P2) | J/L/F completados: incremento J/L `f58d0cc7` (+ follow-ups C3 abajo), incremento F `2a0ac62`+`22f337c`; gates J01–J06, L01–L04 (L05 ver abajo), F01/F03 ejecutados | ver C3 |
| S3-A-05 (P3) | Cobertura del delta publicada en [[SHOT4_FINAL_REPORT]] §R5 (per-file in-suite + drivers físicos); perfil `/tmp/cov_full2.out` espejado en evidencia | — |
| S3-A-06 (P3) | Identidad por buildinfo (`vcs.revision`+`vcs.modified`); nota de no-reproducibilidad byte-level en el reporte (sin cambio de producto) | — |

Excepciones históricas preservadas: H45 (prepare p95 ≤2s a 20k) FAIL sin re-presupuestar; QA-01 V4 85,8/85,2 FAIL adjudicación Owner; AUTH_FORGE BLOCKED_EXTERNAL (X_AUTH_ARTIFACT) — ninguna convertida en PASS.

### C3. Defectos nuevos corregidos al completar J/L/F (descubiertos por los gates propios)

| Defecto | Corrección | Commit |
|---|---|---|
| B5: el servicio de binding no propagaba el número Magic al `BindingCreateRequest` ⇒ el slot de vigencia (instancia,cuenta,magic) nunca materializaba y el ingress manejado no podía resolver el binding | Certificado resuelto contra `strategy_identity_allocation_events` (número+assigned_at con `::timestamptz`) y número propagado al slot | `2f162daa` |
| B7/B12: CLOSE-before-OPEN fallaba con error de transporte sin retención durable | Retención como pending scoped (`CLOSE_BEFORE_OPEN`) vía `persistPending`; jamás fabrica OPEN | `95792e35` |
| B7: cuarentena visible con `ON CONFLICT` sobre índice único parcial 062 no inferible ⇒ tx abortada silenciosamente | Dedupe por SELECT previo + INSERT; error de cuarentena propagado | `68b513cd`, `c57d195c` |
| B8: payload del intent de dispatch con comillas JSON violaba el dominio `v4_digest`; typed-nil `json.RawMessage` rompía el cast jsonb en la transición | Digest canónico (string desenvuelto / bytes digeridos); NULL real para provider_result; scan del payload como string | `c57d195c`, `ce80992c`, `aae5c14d` |
| B9: la re-publicación del grupo por la ruta POST daba `HISTORY_EXISTS` (el POST rechaza contenido distinto por contrato); `make_interval(secs=>$n)` sin cast fallaba en claim/backoff; grupo OPEN-sin-cierres se marcaba FAILED | N+1 por `PutHistoryV2` con CAS (ExpectedRevision/Digest del head); head ausente crea rev 1 por POST con ExistingRef; OPEN-only queda PENDING con lease liberada (reentrega al cierre); casts `::double precision` | `850a59e9`, `c1ee10ae`, `2c524839` |
| B9: journal legacy (`TradeJournalFn`) journalizaría dos veces los eventos V2 managed que comparten topic | Omisión explícita de eventos con `managed_context` en el handler legacy (ruta única MasterObservationFn) + unit test | `0f094c00` |
| Retiro de instrumentación de debug PRJDBG que quedó incluida en un commit | Limpieza + import | `3d61d62f`, `6eb0225e` |

### C4. Gates re-ejecutados en el SHA final (`f93cd4f8`, build propio `vcs.modified=false`)

| Gate | Resultado | Run | Evidencia |
|---|---|---|---|
| E01–E12 (edriver, E11 aparte) | **11/11 PASS** | `ed7ff7088cb1ae9f` | `harness/evidence/e-gates/E*_ed7ff708*.json`, `edriver-FINAL.log` |
| O01–O05 (odriver) | **5/5 PASS** | `1a3da67526d2722b` | `harness/evidence/o-gates/`, `odriver-FINAL.log` |
| J01–J06 + L01–L04 (jdriver, nuevo) | **10/10 PASS** | `bc298e9a2fbd06f7` | `harness/evidence/j-gates/`, `jdriver-FINAL.log` |
| E11 protocolo 067–086 | fresh+upgrade 20/20 APPLIED con ledger; reapply 086 ⇒ ALREADY_APPLIED; tamper bytes sin re-sellar ⇒ MIGRATION_CHECKSUM_CONFLICT pre-DDL | — | `harness/` (log de sesión) |
| E10 suites finales | contracts rc=0; sdk/postgres rc=0 (incluye `TestShot4ProjectorAndDispatch` nuevo); gateway/internal rc=0; core/functions rc=1 SOLO por `TestEconomicMinimum…Parity` — verificado FAIL idéntico en baseline `d223d9f8` (worktree temporal): histórico, superficie no tocada | — | `harness/evidence/e-gates/regression.txt`, `/tmp/s4_*_final.log` |
| F01 (fdriver/echo-ingest-v2) | POST ⇒ INGEST_ACCEPTED con receipt validado (schema/digest/producer/histories); replay post-restart idempotente (comparación semántica: jsonb normaliza orden); misma key+otro body ⇒ conflicto local; persist-before-network demostrado (manifest sin delivery de corrida fallida) | — | `sqx.handoff_manifests_v2/_deliveries_v2` en PG harness; `/tmp/f01*.log` |
| F03 | pin `shared-analytics v0.0.1-lab-v4-shot2.1` intacto (go.mod+go.sum); cold build lab-worker y sqx OK | — | — |

F02: porción funcional cubierta por E+J (DTO→HTTP→journal→historia) con fixtures etiquetados; la porción auténtica sigue BLOCKED_EXTERNAL (AUTH_FORGE) y la pata browser/UI es NO-TOUCH histórico V4 (L05: no re-ejecutado en este shot, sin regresión por diffs vacíos en front/Hasura).

### C5. Limpieza y ownership

PG del harness en 56427 (pgboot propio, PID en `harness/pgboot4.pid`); gateways/drivers propios terminados; sin killall; pgboot de otros workspaces intactos; residuo pre-existente `/tmp/w4-gomod-cold` no tocado. Evidencia final: `harness/evidence/EVIDENCE_INDEX.sha256` (327 artefactos) + `evidence/verifier/` del verificador independiente.

## Fuentes

- Mandato Owner 2026-10-26 (D4); [[F — Decision Register]] D25–D27; [[SHOT4_FIX_PACKAGE]]; [[SHOT3_ADVERSARIAL_REPORT]]; [[B — Frozen Architecture]]; [[C — Implementation Shots and Acceptance Gates]]; [[A — Source Baseline and Branch Integration]].
- Evidencia externa: `/srv/echo-work/ingestion-v2-shot4-20261026/harness/` (índice `evidence/EVIDENCE_INDEX.sha256`).
