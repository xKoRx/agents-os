---
type: feedback
schema_version: 1
scope: session
created: 2026-10-31
updated: 2026-10-31
area: "[[Echo]]"
project: "[[Echo Futures — Runtime Pools]]"
entities:
  - "[[Echo Futures — Runtime Pools]]"
related:
  - "[[Echo Futures — Runtime Pools]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: minimax/MiniMax-M3.1-Flash
agent_run: "[[2026-10-31-zcode-minimax-m3.1-flash-echo-b2-acceptance]]"
session_goal: EF-SUN-01 — map the exact promotion criteria and corpus/indicator parameters of the B2 native rebuild path.
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - agent/system1
---

# Session Feedback - 2026-10-31 - code-scout EF-SUN-01-REPO-B

## Context

- **request / revisiones:** `EF-SUN-01-REPO-B` (code-scout). Repo `xKoRx/echo`, worktree `/home/kor/aranea/work/echo-p0-final-integration-20261031`, HEAD `bf7420d2c5656c09830f427d710142fea6b60735`, `git status --porcelain` vacío. Pregunta única: criterios exactos de promoción y parámetros de corpus/indicadores del rebuild B2, para poder decidir si el bloqueo es "sólo falta DATA fresca".
- **ruta de recuperación:** skill `agents-os-code-scout` + `_shared/scout-contract.md` leídos primero; luego los archivos dirigidos (`sdk/futures/strategy/{rebuild,engine,strategy,readiness}.go`, `sdk/futures/strategies/s2/{s2,indicators,warmup_requirements,warmup_diagnostic}.go`, `sdk/futures/analytics/{native_rebuild,s2/indicators}.go`, `sdk/futures/bars/{native_rebuild,native_bar}.go`, `sdk/futures/market/{rebuild_state,rebuild,cursor,freshness}.go`, `core/functions/{futures_rebuild,futures_strategy_engine,futures_analytics_observations,futures_market_stream}.go`, `core/internal/futuresruntime/runtime.go`) + `specs/EF-FEED-RECOVERY/{B2-CONTRACT,B2-VERIFICATION,VERIFICATION}.md`. Sin code-graph ⇒ búsqueda dirigida, degradación declarada.
- **rangos realmente leídos:** los citados, con `file:line` por hecho.
- **utilidad observada:** `COMPLETE` — entregó las cuatro condiciones simultáneas de promoción (receipts + cursor de la época siguiente + gap cerrado + frescura), el gate de cobertura 51/20, los parámetros S2 (SMA 50 ⇒ 51 cierres H4, BB 20 con desviación 2.0 poblacional), el corte causal **inclusivo** (`!CloseBoundary.After(entryOpen)`) y el guard literal de warmup sin señal/ciclo.
- **gaps / truncado / degradación / relecturas:** sin truncado ni permiso denegado. Gaps declarados: el texto fuente D4-B1 §7.3 no está en el repo; `RecoverySummary.Summary()` omite `OldTicksRecovered` y ningún writer no-test lo asigna; los `FreshnessBounds` reales del runtime no son trazables desde el repo. Causa: `none` en retrieval.
- **decisión de mantenimiento:** `NO_FINDING` para la skill. Se **escalaron** tres hallazgos de producto al principal (drift de la cabecera de `s2.go:11-12`, `OldTicksRecovered` sin escritor, promoción silenciosa por falta de frescura) — son del repo, no de la skill, y no se corrigieron unilateralmente.
- **hallazgo del scout que cambió el veredicto del principal:** la promoción no exige "bundle reciente en wall-clock"; la frescura se evalúa al promover sobre evidencia viva. Por eso un rebuild con receipts completos pero sin DATA queda PENDING indefinidamente — y, por simetría, un rebuild sin receipts NO es "sólo falta DATA3".

## Scores

- Startup clarity: 5
- Retrieval usefulness: 5
- Skill fit: 5
- Template fit: 4
- Closeout friction: 5
- Overall confidence: 5

## What Complicated The Session Most

- **Observation:** el contrato escrito ("promoción exige 51/20 elegibles, kernels causales, cobertura y frescura") no separa *qué bloquea antes* de *qué bloquea por mercado*.
- **Why it was hard:** sin el desglose de `tryPromoteRebuild` el lector puede clasificar erróneamente un rechazo determinista como espera de mercado.
- **Proposed improvement:** ninguno en la skill; el scout ya lo desglosó por condición.

## Missing Support

- **Problem not solved by Sistema 1:** ninguno material.
- **How Sistema 1 could help next time:** el contrato de retorno con literales y `file:line` fue suficiente.

## Skill Feedback

- **Skill that worked well:** `agents-os-code-scout`.
- **Skill that was confusing:** ninguno.
- **Trigger/routing gap:** ninguno.
- **Suggested contract change:** ninguno.

## One Next Improvement

- Pedir siempre, en este tipo de despacho de contratos de promoción, el desglose de las condiciones **simultáneas** con su literal de código; fue lo que permitió separar "bloqueo de producto" de "condición de mercado" en este shot.
