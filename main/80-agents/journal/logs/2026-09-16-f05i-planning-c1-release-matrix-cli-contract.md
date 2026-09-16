---
type: change_log
schema_version: 1
scope: session
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Echo]]"
project: "[[Echo Forge — F-05-I Cohesive release and read surfaces]]"
application:
entities:
  - "[[Echo Forge — F-05-I Cohesive release and read surfaces]]"
  - "[[Echo Forge]]"
related:
  - "[[Echo Forge — F-05-I Release Matrix and Read Surface Contract]]"
  - "[[Echo Forge — Factory V2 Completion]]"
  - "[[Echo + Echo Forge — Deferred Certification Backlog]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-16 F-05-I Planning C1 — corrección contractual Release Matrix + CLI

%% Corrección contractual dentro de F-05-I (no nueva fase). Resuelve C1.1–C1.6 para desbloquear F05I-T1 y F05I-T5. Validación CONTRACT REVIEW, no BUILD PASS. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `30-resources/applications/echo/Echo Forge — F-05-I Release Matrix and Read Surface Contract.md` — §Release matrix contract reescrita (ubicación C1.1, carga portable C1.2, dimensiones/estados C1.3/C1.4, autoridades C1.5, contenido de verdad inicial congelado, guard tests con allowlist histórica), §Exit codes ampliada con mapping ErrorKind→exit, nueva §Grafo mínimo de inicialización por subcomando (C1.6), comandos `release-matrix` y handoff F-05-C actualizados a la ruta embebida, evidencia Planning C1 agregada, invariantes/STOP ampliados, baseline anotado con HEAD `3da8b47` verificado 2026-09-16.
  - `10-projects/Echo/agentes/Echo Forge — F-05-I Cohesive release and read surfaces.md` — tarjetas F05I-T1 y F05I-T5 con contrato corregido (allowed files, tipos, validaciones, tests, stops), tablero T2/T3/T4 `[r]→[x]` por aprobación manager SOURCE REVIEW APPROVED (físico NOT RUN; F-05-I abierta), estado actual + entrega de desarrollo actualizados, decisiones ampliadas, bitácora con la sesión, progress 57→64.

## Razón

El plan original dejaba seis defectos materiales: (1) `deploy/release-matrix.json` vive dentro del WatchRoot del deployer-watcher y del staging de `deploy_release.sh`; (2) T5 cargaba la matriz por ruta relativa al checkout, imposible en binario instalado; (3) un estado `deployed` escalar no representa flota heterogénea ni incertidumbre; (4) la prohibición absoluta de física DONE borraba certificaciones históricas verdaderas (F-03 PHYSICAL PASS, B1A/B1B/B2 CLOSED); (5) fuentes de infraestructura tratadas como autoridades equivalentes; (6) `sqx-flowkit` bootea DI completo (etcd/telemetry/MinIO/Postgres/Temporal) antes de despachar el subcomando.

## Decisiones

- Ruta canónica `sqx/core/releasematrix/release-matrix.json`; `deploy/` prohibido para artefactos declarativos (evidencia: `deployer/cmd/deployer-watcher/main.go` WatchRoot `./deploy`, `source-fsnotify` WalkDir recursivo, `pathing-staticlayout.ComputeKey`, `deploy_release.sh` staging `deploy/<version>/`).
- Carga portable: `//go:embed` + API `Embedded/LoadEmbedded/Parse/Load/Validate`; override `--matrix` con error tipado exit 2; default relativo-repo eliminado.
- `deployed` con `deploy_targets[]` (release/release_present OBSERVED|NOT_OBSERVED/process RUNNING|NOT_OBSERVED + evidencia + as_of); sin inferencia publicación⇒deploy ni archivos⇒proceso.
- Semántica DONE/OPEN/DEFERRED/NOT_APPLICABLE; DONE físico/cross-lane exige `certification_record`/`cross_lane_receipt` + `as_of` y alcance de época; guard con allowlist histórica `{b1a-mt5-ownership, b1b-mt5-wallclock, b2-cancel-recovery, f03-sqx-long-running}`; certificación no comprobable queda pendiente de verificación.
- `evidence_kind` enum por dimensión (git/tests/release_manifest/deployment_proof/runtime_observation/certification_record/cross_lane_receipt/none); RELEASED≠DEPLOYED; SOURCE VERIFIED≠PHYSICALLY CERTIFIED; `persistence_authority` nombra storage concreto sin intercambiabilidad.
- CLI: dispatch-first; `release-matrix` cero DI; inspect PG-only; `run get` añade Mongo (`sharedmongo.New` + `NewRankingSnapshotStore` como port read); push-output intacto; único delta documentado: falla etcd pre-dispatch pasa de exit 1 a exit 10 `config_error`; `internal/di` intocado.

## Verificación

- HEAD symphony `3da8b470239a15f62d87f16559feada409e2d611` verificado sin cambios (branch `codex/f05-release-prep`); dirty preexistente `specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json` preservado.
- Cero cambios source en symphony (READ ONLY); sin migraciones; sin contratos frozen alterados; MCPs de infraestructura no usados.
- No se declararon certificaciones físicas nuevas; la aprobación manager T2–T4 se registra como SOURCE REVIEW con tests locales PASS reportados por el agente, físico NOT RUN.
- Validación de la sesión: CONTRACT REVIEW (comparación SPEC previa/posterior, coherencia T1/T5, rutas, autorizaciones); no se afirma que ningún diseño compile.

## NO_RUN

- Graphify: NOT_RUN (no disponible en la sesión; Markdown canónico es la fuente).
- agent_run: no registrado — la sesión no generó ni evaluó código; es corrección contractual documental (scope del registro: coding/debug/review/testing material).
