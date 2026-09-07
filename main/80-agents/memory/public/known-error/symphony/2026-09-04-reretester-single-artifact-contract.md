---
type: known_error
schema_version: 1
scope: project
created: "2026-09-03"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-09-04-final-reretester-empty-fanin-rca]]"
  - "[[2026-09-04-echo-forge-c3-lean-0289-blocked-reretester]]"
  - "[[2026-08-31-forge-campaign-stop-policy-v1-contract]]"
  - "[[2026-09-04-echo-forge-final-reretester-empty-output-fix]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-C3-FINAL-RERETESTER-SINGLE-ARTIFACT-RCA-V1-TOP
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - project/echo-forge
---

# 2026-09-04-reretester-single-artifact-contract

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- El Generic child de una Campaign muere en `05_reretester` con `error en final reretester task 05_reretester: final reretester strategy <StrategyRef>: final reretester activity must return exactly one key and one StrategyArtifact`.
- CERT-A 0.2.89: Campaign `WAVE_FLOW_RUN_FAILED`, FlowRun `FAILED`, finalists=0, promotion decisions=0, stop evaluations=0, pese a que otras strategies del mismo hop sí produjeron `.sqx`.

## Causa

- PRIMARY: `CONSUMER_CARDINALITY_ASSUMPTION_BUG`. `validateFinalReretesterFanoutOutput` exige exactamente 1 key y 1 `StrategyArtifact` por activity; el productor `sqx-final-reretester.v1` puede completar success con 0+0 vía `CompleteEmpty`.
- En CERT-A la activity de `225e111a-fe51-45c5-979c-d3ad6376ca65` (Hera) devolvió Keys=0 / StrategyArtifacts=0 con exit=0; las otras dos activities devolvieron 1+1 y persistieron objetos MinIO. El consumer abortó todo el child.
- Autoridad de “exactly one”: consumer del fan-out en `sqx/workflows/generic_workflow.go`, no el productor durable.

## Impacto

- Un empty legítimo en una sola estrategia del cohort mata la wave y la Campaign. Artefactos produced hermanos quedan huérfanos respecto de ranking/promotion.
- C3 no puede avanzar a CERT-B ni a un checkpoint MT5 certificable.

## Detección

- Temporal ns `sqx-prop`, child `sqx-main-v1-82543151-dc53-46fd-9c5b-51188f232713` event Fail 212 nombra `225e111a-fe51-45c5-979c-d3ad6376ca65`.
- PostgreSQL: 2 evidencias final-reretester + 1 CompleteEmpty; `flow_run_strategies` todas `PRODUCED`.
- MinIO bucket `sqx-strategies`, prefijo `05_reretester/` de esa wave: exactamente 2 objetos (`final-6c07035f-….sqx`, `final-4dd7fd71-….sqx`).

## Mitigación

- No reintentar CERT-A ni CERT-B sobre las mismas identidades. No mutar PG/Mongo/MinIO.
- Fix NORMAL: tratar empty per-strategy como drop; merge solo 1+1 válidos; fallar malformados y errores reales de activity. Recertificar con identidad nueva tras release patch.

## Evidencia

- Source `a846adca3896cf578cf27eb854d9ea9bb725997d` / release `0.2.89` / SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`.
- Decisión: [[2026-09-04-final-reretester-empty-fanin-rca]].

## Resolución

- Implementado en `xKoRx/symphony` commit `32d0740ccb0fe6ee04e016eef874790bc8684efc`: el consumer clasifica `0+0` como empty válido, omite ese StrategyRef y conserva sólo outputs producidos `1+1`.
- La cardinalidad parcial, `>1`, errores reales de activity y todas las validaciones de identidad, evaluación, decisión y carriers continúan fallando; el merge acepta outputs producidos vacíos sin placeholders y conserva orden determinista.
- C3 permanece `BLOCKED / CLOSED`; este cambio de source aún requiere una release nueva y recertificación física con identidades nuevas.
- **Actualización 2026-09-04 (release 0.2.90, CERT-A `baeb747d-1cb9-4cbc-8903-58d91f64c720`):** la pipeline 0.2.90 atravesó el final reretester sin la violación (`project@sqx-final-reretester.v1` COMPLETED con 1 input → 1 producido y continuidad downstream completa hasta MT5). El tramo producido del fix quedó demostrado físicamente; el branch `CompleteEmpty` no surgió en esta corrida y su cobertura sigue siendo unitaria. CERT-A terminó `BLOCKED / CLOSED` por un defecto independiente ([[2026-09-04-mt5-terminal-build-unsupported]]); la resolución plena de este known-error queda atada a la primera CERT-A que alcance strong PASS.
- **Re-test 2026-09-05 (HEAD `3b0737c1efe153f1f72eec40465fd1aa883887d0`, 6 commits posteriores al fix):** el fix y sus tests siguen intactos — mixed-empty retorna 2 survivors de 3, all-empty retorna `0/0` sin cardinality failure, partial cardinality y regresiones siguen fallando, y el producer zero-output sigue PASS. Un re-despacho del mission original fue detenido por el gate de baseline (ver [[2026-09-05-echo-forge-reretester-fix-retest]]); sin mutación de source.
