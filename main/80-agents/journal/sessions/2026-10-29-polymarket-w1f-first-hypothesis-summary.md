---
type: session
schema_version: 1
scope: session
created: "2026-10-29"
updated: "2026-10-29"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine]]"
related:
  - "[[Research — First Hypothesis W1-f 2026-10-29]]"
  - "[[Preregistration — First Hypothesis W1-f 2026-10-29]]"
  - "[[Research — Prospective Metadata Quality W1-e 2026-10-28]]"
aliases:
  - "W1-f first hypothesis session"
confidence: high
source_session: sess_4d2d4204-b8bd-4a0f-9ea9-5218ad3d6c24
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# 2026-10-29-polymarket-w1f-first-hypothesis-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- W1-f (mandato one-shot del lanzador, ejecutor GLM-5.3-Flash Max vía ZCode CLI en `sqx-ulab-hefesto-0`): terminar UNA primera hipótesis objetiva preregistrada y evaluable con el Engine, con diagnóstico reproducible de si los datos autorizados (capture-v6) alcanzan. Sin búsqueda de rentabilidad ni optimización.

## Contexto cargado

- Bootstrap Agents-OS (constitución, perfil global vía directorio resuelto, nota interna global, índice de skills, registro de dominio: DEFAULT sin router). Entidad [[Polymarket Engine]].
- Continuidad Five-POC §§1–18 (W0…W1-e, bullets 1–17), informes W1-e y W1-d, 6 manifests v6 (sólo metadata), `inputs.json` (12 SHAs), y código real del engine (`regimes`, `books`, `replay`, `experiment`, `cmd/engine`) en HEAD `7d519eb712a6a4ec9f369c92d9ee2c735454678b`, rama `w0/offline-causal-replay-20261027`, árbol limpio.

## Trabajo realizado

- Inventario conceptual y admisibilidad por contratos: 5 candidatas económicas/observacionales existentes (PE-002/005-R1/001/030/004) descartadas con razón contractiva; ELEGIDA la falsación del gate de calidad prospectiva W1-e como primera hipótesis (única compatible con contratos y datos; candidata económica condicional documentada con gates).
- Preregistro W1-F-H1 congelado ANTES de medir: MD canónico + JSON de máquina en OUT (SHA `9c56acfa…`), con predicciones P1–P7, criterios de falsación y regla de veredicto; el harness falla cerrado si el prereg falta (orden prereg→medición test-enforced).
- Harness en los 2 archivos autorizados (tests del paquete `internal/experiment`, sin tocar producción): sintético con oráculos independientes de expectativas a mano (futuro/postcut, empate wall+seq, stale, fail-closed, fee honesty) y de integración que consume capture-v6 por APIs read-only existentes y escribe evidencia/manifests sólo en OUT.
- 4 corridas reales del trial (bug ordinario de ruta → bug de determinismo propio → 2 defectos menores de evidencia → corrida autoritativa): resultado final `NO_FALSATION_FIRED_IN_RUN` en ambas pasadas, P4 determinismo OK, suite completa del paquete PASS, BUILD exit 0.
- Commit local `853c0e46c9be2de4e84201e240e9cf8366b1036e` «Preregister and exercise first offline Polymarket hypothesis» (sólo los 2 archivos propios; sin push).

## Artifacts creados o modificados

- Repo: `internal/experiment/w1f_hypothesis_test.go` (SHA `ec901049…`), `internal/experiment/w1f_hypothesis_integration_test.go` (SHA `18d6fdb9…`); commit `853c0e4`.
- OUT `validated-baseline/w1-f-first-hypothesis-20261029/`: `w1f-preregistration-h1.json`, `W1-F-MANIFEST.json` (recibo con hashes), 8 evidence JSON (`w1f-gate-evidence-*.json`, runs 14:39/14:40/14:42/14:45 preservados), 12 derived manifests (`w1f-derived-manifest-*.json`), binario `engine` (SHA `3d8b83f5…`, reproducible).
- Vault: preregistro MD, informe [[Research — First Hypothesis W1-f 2026-10-29]], esta sesión, feedback, agent_run, change_log y bloque W1-f en la continuidad canónica.

## Memoria propuesta o creada

- Ninguna promovida; lecciones de fricción registradas en feedback (hooks de inventario, naming con run-id para no sobrescribir).

## Decisiones

- Elección de hipótesis técnica de disponibilidad sobre candidata económica (fee sin certificar, ventana de 5 min, sin hecho de cambio de tick): registrada en el preregistro con descartes.
- Veredicto congelado aplicado: `DATA_SUFFICIENT_FOR_GATE_AVAILABILITY_TRIAL`; ramas stale/tick-change a nivel libro INCONCLUSIVE (déficit estructural cuantificado: lag máximo 47 s ≪ TTL 900 s; 0 cambios de lexema); economía NO afirmada.

## Pendiente

- Para cualquier hipótesis económica futura (candidata condicional S02-style): fee certificada (mapeo documental base_fee↔feeRate o trades convergentes), hecho real de cambio de tick con libro posterior, ventanas > TTL con re-polls, ≥100 frames elegibles por ventana preregistrada — diseño de adquisición, no ejecutado aquí.
- Decisión lanzador/Owner sobre la ventana prospectiva que ejerza cambio/stable/stale.
