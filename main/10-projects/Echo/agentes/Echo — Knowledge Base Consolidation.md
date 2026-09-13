---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo — Producto Integrado]]"
sprint:
start: 2026-09-12
due:
progress: 0
repo: xKoRx/echo
jira:
prs:
aliases:
  - Echo Knowledge Base Consolidation
  - KBC
tags:
  - kind/project
  - area/echo
  - agent/owner
created: 2026-09-12
updated: 2026-09-12
cssclasses:
  - wide
---

# Echo — Knowledge Base Consolidation

> [!info]+ Echo — Knowledge Base Consolidation
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo — Producto Integrado]] · **Repos (INPUTS READ ONLY):** `xKoRx/echo`, `xKoRx/symphony`
> Campaña documental transversal: cartografía funcional de Echo y Echo Forge, frontera de integración, wiki canónica en `30-resources/`, archivo de docs superseded, AGENTS.md como routers y auditoría de context budget de Agents-OS. No toca source, tests ni config operacional.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre humano tiene la tarea puente `#type/supervision`.

## 🎯 Objetivo

Dejar Echo y Echo Forge documentados según su realidad implementada actual, la integración Forge→Echo documentada desde ambos lados, la documentación durable migrada a Agents-OS (`30-resources/`), lo viejo superseded/archived, los AGENTS.md reducidos a routers efectivos, y el retrieval de Agents-OS sin duplicación/staleness — todo verificado contra source real antes de publicación canonical.

## 📊 Estado actual

- **CORRECCIÓN CICLO 1 EN CURSO** — G ciclo 1: PARTIAL (48 PASS / 3 FAIL / 4 UNKNOWN, verificación de primera mano; vault HEAD real `ca473eeb`, drift +21). FAILs: F-1 Temporal SDK en `sqx/go.mod:24` = **v1.35.0** (no v1.44.1, que es el go.mod root legacy); F-2 topics = **17** (`v3/sdk/domain/snapshots.go` L254-270, artifact 02 decía 18 listando 17); F-3 **13** filas Echo en Arquitectura de producto (no 11). Todos los claims críticos de la tarea PASS. Plan: re-run focalizado forge cartographer (corrige artifact 03) → echo cartographer (corrige artifact 02) → documentarian (aplica F-1/F-2/F-3 al draft 06) → verifier ciclo 2.
- **FASE G ciclo 1 COMPLETE** — verdicto y evidencia en `artifacts/09-verification.md`. Unknowns documentados sin inventar: cobertura de deudas/hitos pre-supersede, exactitud GUIA_WORKER_TEMPORAL_MT5, inbound links exactos (grep sin Graphify), G7 observability (unknown por diseño).
- Fase E COMPLETE (vault `a87aa62`): 27 CANONICAL / 3 MERGE / 5+3 SUPERSEDED / ARCHIVE resto / 0 DELETE. ⚠️ Flag seguridad al owner: `30-resources/APIs.md` con credenciales vivas en texto plano — sin tocar, decisión del humano.
- Fase D COMPLETE: frontera rota en producción (pin SDK única frontera real; G1–G7 en `artifacts/04-echo-forge-boundary.md`).
- Fase C COMPLETE: Forge @ `9fad768c` — GenericSQXWorkflow + ForgeCampaignWorkflow (Temporal SDK); magic V1 cableado; PG/Mongo/MinIO/etcd.
- Fase B COMPLETE: Echo @ `f7ddea18` — **Flink StateFun, NO Temporal**; E-02 implementado (PHYSICAL_PARTIAL); receptor E-04 completo, Spec-Active.
- Fase A COMPLETE: subdominio `30-resources/applications/echo/` + `00-index.md` (`artifacts/01-knowledge-architecture.md`).
- Riesgos registrados en artifact: vault HEAD real `09746b3` (sync commits ajenos, reconcilia fase H); movimiento ~17 páginas exige actualizar índice raíz en el mismo cambio; symphony dirty → sólo lectura; skills INDEX declara 3 app-owned vs 21 reales en symphony (fases I/J); Graphify CLI no disponible (inventario por búsqueda enfocada).
- `MAX_ACTIVE_SUBAGENTS = 1` — ejecución estrictamente secuencial. El planner (esta nota) es single-writer del parent orchestrator.
- Artefacts de especialistas: `10-projects/Echo/agentes/kb-consolidation/artifacts/` (READ MANY / WRITE ONE por especialista; `filesystem_enforcement: PROMPT_ONLY`).

## 🧱 Baseline (2026-09-12)

| Repositorio | Branch | HEAD baseline | Nota |
|---|---|---|---|
| Vault Agents-OS | `master` | `9a5299f1ec9dd950cd86480d5448e76870e8bd12` | working tree clean |
| `~/go/src/github.com/xKoRx/echo` | `feature/e02-control-safety-journal-recovery` | `f7ddea18cab51db72c9765aa74381328134d7ce7` | `origin/master` = `a99f9a63`; clean |
| `~/go/src/github.com/xKoRx/symphony` | `feature/f04-magic-version-handoff` | `9fad768ccd1f9d25ebb535a2d26edb3d74556c10` | `origin/master` = `0b9742b0`; **working tree dirty → NO tocar** |

Reglas de repos: INPUTS READ ONLY. Sin reset/clean/stash/rebase/checkout destructivo. Los repos avanzan en paralelo por otros agentes; antes de publicación canonical se reconcilia `documented_baseline..current_HEAD` y sólo se revalida lo DOCUMENTATION_RELEVANT/UNKNOWN.

## ✅ Tareas

> [!example]- Fuente de tareas — pipeline secuencial
> - [x] A — knowledge-architect: topología documental → artifact `01-knowledge-architecture.md` #owner/agent #area/echo
> - [x] B — echo-functional-cartographer: cartografía Echo @ baseline → `02-echo-cartography.md` #owner/agent #area/echo
> - [x] C — forge-functional-cartographer: cartografía Forge @ baseline → `03-forge-cartography.md` #owner/agent #area/echo
> - [x] D — echo-forge-integration-cartographer: frontera contractual/implementada → `04-echo-forge-boundary.md` #owner/agent #area/echo
> - [x] E — legacy-doc-curator: clasificación CANONICAL/MERGE/SUPERSEDED/ARCHIVE/DELETE + manifest → `05-legacy-doc-audit.md` #owner/agent #area/echo
> - [x] F — llm-wiki-documentarian: propuesta wiki canónica → `06-wiki-draft-plan.md` #owner/agent #area/echo
> - [/] G — documentation-verifier (MAX): refutación adversarial; máx 2 ciclos globales de corrección → `09-verification.md` #owner/agent #area/echo
> - [ ] H — vault-publisher-reconciler (MAX): reconciliación baseline→HEAD + publication manifest → `10-publication-plan.md` #owner/agent #area/echo
> - [ ] P — Parent ejecuta publicación canonical en `30-resources/` (sólo con verification PASS) #owner/agent #area/echo
> - [ ] I — agents-md-gardener: AGENTS.md Echo + Forge minimalistas → `07-agents-md-plan.md`; luego documentation-verifier scope AGENTS.md; parent aplica #owner/agent #area/echo
> - [ ] J — context-budget-auditor: duplicación, staleness, leakage MELI/ARANEA/DEFAULT → `08-context-budget.md` #owner/agent #area/echo
> - [ ] K — Agents-OS hygiene pass acotado (KISS) desde findings J; conformance check conceptual (no inventar PASS; NOT_VERIFIABLE si no demostrable) #owner/agent #area/echo
> - [ ] L — Informe final + cierre de sesión con feedback (Agents-OS session-close) #owner/agent #area/echo

## 📆 Bitácora

- **2026-09-12** — Interrupción infra: primer lanzamiento de forge-functional-cartographer (KBC-C) falló con "user concurrency limit exceeded" antes de iniciar. Verificado: sin hijos activos. Reintento único de la misma task en curso.
- **2026-09-12** — Campaña iniciada (NEW). Bootstrap Agents-OS ejecutado; dominio aranea, entity Echo. Baselines capturados (tabla 🧱). Proyecto creado como planner único; artifacts en `agentes/kb-consolidation/artifacts/`. Tarea puente creada en [[Echo — Producto Integrado]]. Fase A lanzada.
