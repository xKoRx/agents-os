---
type: change_log
schema_version: 1
scope: session
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Personal]]"
project: "[[Multimodal Knowledge Engine]]"
application:
entities:
  - "[[Multimodal Knowledge Engine]]"
related:
  - "[[M0 Execution]]"
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

# 2026-09-20 — MKE live readiness sprint (LIVE_READY_WITH_LIMITATIONS)

## Cambios

- Entidad `[[M0 Execution]]`: nuevo estado actual (LIVE_READY_WITH_LIMITATIONS), tarea del agente LIVE READINESS SPRINT con 5 sub-tareas WP cerradas, bitácora nueva. La tarea puente humana NO se tocó.
- Repo `xKoRx/multimodal-knowledge-engine`, rama `fix/m0-live-readiness` (desde `b48822d`, HEAD `2867a31`, pusheada a origin):
  - `0743adf` WP-01: `mke windows` (policy `m0-windows-baseline-v1`) + E2E gate test de trazabilidad planificador→publicación.
  - `fd99a00` WP-02: contratos live E2E (kind:event, contradicciones honestas, procedures).
  - `0d63a09` WP-04: preflight HTTP GLM simulado (matriz consolidada).
  - `6786f3c` WP-05: runbook `docs/runbooks/m0-live-certification.md`.
  - `2867a31` WP-03: holdout independiente (fixture 8s, golden congelado 6 elems `64446e4e…`, script 11 entries, A 6/6).
- README: command surface con `plan`/`windows`, timeline de veredictos fechados y separados (sintética NO_GO → recovery PASS → física BLOCKED → holdout → live readiness), sección live readiness con limitación explícita del holdout recorded-provider.
- Evidencia durable: `~/mke/evidence/live-readiness/` (holdout-golden.jsonl, holdout-quality.json, holdout-selection.json, holdout-authoring.md).

## Decisiones

- NO se cambió el detector de candidatos de conflicto: el falso-positivo aparente del par EXCEPTION_TO fue verificado como decisión adjudicada del recovery (test unitario lo fija: el hint nunca se suprime; es hint, jamás relación). Los tests E2E nuevos fijan la semántica honesta publicada.
- Prompts de inferencia intactos (`mke.recon03.v1`/`mke.ground03.v1`/`mke.consolid03.v1`): tocar el texto invalidaría todas las identidades de replay y los benchmarks de recovery; los contratos se probaron por el lado engine.
- `artifacts/` sigue gitignoreado; el golden congelado del holdout se preservó como copia verificada en `testdata/holdout/golden/` (mismo content hash `64446e4e…`).

## Pendientes

- Certificación física M0 (G0/G1): requiere video autorizado + credenciales GLM (`MKE_GLM_API_KEY`); el runbook deja la ejecución lista.
- Llamada GLM live: no ejecutada en este sprint; los contratos live del prompt quedan por validar con el modelo real en la certificación.
