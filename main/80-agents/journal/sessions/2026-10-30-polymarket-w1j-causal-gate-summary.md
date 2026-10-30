---
type: session
schema_version: 1
scope: session
status: closed
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities: []
created: "2026-10-30"
updated: "2026-10-30"
source_session: sess_no-legible-desde-superficie-w1k-recovery
surface: "[[ZCode]]"
model: "account:zai-individual-coding-plan/GLM-5.3-Flash"
host: sqx-ulab-hefesto-0
related:
  - "[[Research — W1-j Causal Gate Diagnosis 2026-10-30]]"
  - "[[Research — Single Episode Public Pilot W1-j 2026-10-29]]"
  - "[[2026-10-30-polymarket-w1j-causal-gate-feedback]]"
  - "[[2026-10-30-zcode-glm-5.3-flash-polymarket-w1j-causal-gate]]"
  - "[[2026-10-29-polymarket-engine-entity-updated]]"
aliases: []
confidence: high
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
  - topic/research-ops
---

# 2026-10-30-polymarket-w1j-causal-gate-summary

## Objetivo

- Recuperación W1-k (misma superficie×modelo, offline, host Hefesto): completar lo que el cierre previo de la sesión W1-k dejó pendiente — ejecutar el test del contraejemplo del gate congelado con el Engine real, dejar el test validado commiteado localmente, producir el extractor verificado de un único input sellado, y cerrar en Agents-OS con informe nuevo, errata de comisiones al informe W1-j, continuidad, change_log, feedback y agent_run.

## Contexto cargado

- Bootstrap AGENTS OS ya cargado en esta sesión (warm turn): constitución, continuidad global, índice de skills, router DEFAULT, skills session-close/session-feedback/agent-run-register.
- Delta de cierre: informe W1-j y sus 3 registros journal del 2026-10-29, change_log canónico [[2026-10-29-polymarket-engine-entity-updated]], continuidad Five-POC §18 (bullets 24–30), artefacto de revisión sellado `analysis-revision-w1j-ep-20261029T2230-identity.json` (SHA `93e7fe79…`) leído íntegro, y fuentes del Engine congeladas (`sports.go`, `economics.go`, `scheduled.go`, `feeresolver.go`, `schedule.go`, `api.go`, pocdata, persist, replay, researchpilot).

## Trabajo realizado

- **Test del contraejemplo (ejecutado y PASS):** `TestW1kSyntheticCounterexample` en `internal/strategy/pocs/sports/w1k_synthetic_counterexample_test.go` — contraejemplo de caída de dos lados con ask bajo `L` ACCEPTA el gate congelado (A +1375 bps, S +250 bps) y el control bid-led con ask pegado RECHAZA (`REVERT_INSUFFICIENT_AFTER_COSTS`) en ambos escenarios. Formas exactas del perfil: test-only PASS 0.005s; suite completa del paquete PASS 0.014s; build exit 0; `gofmt -w`/`-l` limpio. Commit local **`c0c35e7`** «test: verify frozen widening counterexample» (sólo el test), sin push.
- **Diagnóstico causal:** el gate v0.1 NO es no-positivo por construcción; las 36 decisiones del episodio fueron negativas por la forma del libro (ask de entrada sobre `L` en 36/36; gross mark-to-`L` negativo 36/36; `B* > L` 36/36). Dedup `(asset, signal_seq)`: 72 filas = 36 señales únicas × 2 escenarios; 3 ráfagas × 6 frames × 2 activos; cobertura/identidad verificadas sin agregación.
- **Extractor de recuperación:** `recovery-v2/verified_extractor.py` escrito e inspeccionado (único input = JSON sellado; imports de la lista permitida; sin SQLite/red/subprocess/eval; salidas sólo en recovery-v2; profundidad de entrada vs salida distinguida — la salida no consta en la fuente). **Su ejecución quedó NOT_RUN:** `/usr/bin/python3 <ruta absoluta>` denegado 3× por el guard de la superficie; el artefacto previo `episode-diagnostics.json` (`a966b1ff…`) se conserva como no acreditado (sin corrida) y no se reescribió su historia.
- **Cierre Agents-OS:** informe nuevo [[Research — W1-j Causal Gate Diagnosis 2026-10-30]], errata de comisiones añadida como sección nueva al informe W1-j (historia íntegra preservada), bullet (31) W1-k y "Siguiente paso" actualizado en la continuidad (historia preservada como cita HISTORIA), sección nueva en [[2026-10-29-polymarket-engine-entity-updated]], feedback y agent_run nuevos del 2026-10-30. El materializador canónico quedó en deadlock documentado (hook exige ruta absoluta; el script exige relativa) — notas nuevas creadas con Write replicando el frontmatter canónico de las notas materializadas del 2026-10-29; intentos registrados sin variantes.

## Artifacts creados o modificados

- Vault: las 5 notas listadas arriba (1 doc nuevo, summary/feedback/agent_run nuevos, errata en el informe W1-j, bullet+siguiente-paso en la continuidad, sección en el change_log).
- Repo externo: commit local `c0c35e7` (1 archivo de test; sin push; nada de producción tocado).
- Workspace (fuera del vault): `validated-baseline/w1-j-single-episode-pilot-20261029-lot3/analysis-revision-w1j-20261029/w1k-causal-gate-diagnosis-20261030/` — `extract_episode_diagnostics.py` (borrador v1, sha `3f36014b…`), `episode-diagnostics.json` (`a966b1ff…`, NO acreditado), `ERRATA-fees-w1k-20261030.md` (`a7665be1…`), `recovery-v2/verified_extractor.py` (ejecución NOT_RUN).

## Memoria propuesta o creada

- Ninguna memoria interna nueva: el delta es estado de proyecto (continuidad + journal), no comportamiento transferible.

## Decisiones

- **El ensayo v0.1 se mantiene INCONCLUSIVE de un mercado** (sin inconsistencia demostrada del harness; réplica 72/72). Propuesta de revisión económica especificada sin implementar: condición de nivel `bestAsk < L·(1−margen)` con margen preregistrado, evidencia requerida = enmienda de prereg + re-procesamiento offline de episodios sellados; sin captura autorizada.
- El test del contraejemplo se conserva commiteado como activo de verificación del paquete (útil y validado), no como cambio de producto.

## Pendiente

- Ejecución del extractor de recuperación (requiere que el lanzador registre la forma exacta del script, patrón W1-b/W1-j: preflight de fuente por SHA) y cotejo formal contra el borrador no acreditado.
- Decisión Metis/Owner sobre la revisión económica especificada (sin código ni captura hasta entonces).
