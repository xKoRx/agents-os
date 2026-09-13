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

- **FASE H EN CURSO** — vault-publisher-reconciler (MAX) para publication manifest. **Fase G ciclo 2: PASS con unknowns documentados** (`artifacts/09-verification.md`): F-1/F-2/F-3 re-verificados PASS contra source, sin contradicciones nuevas, los 4 UNKNOWNs persisten declarados. Gate: procede con 4 condiciones — (1) revalidar volátiles contra HEAD al publicar (vault drift ca473eeb→82852b3, nada tocó `30-resources/applications/`), (2) supersedes sólo tras cobertura de los 32 deudas/hitos, (3) índice raíz + MOVEs + log en un cambio atómico, (4) unknowns G7/supersede declarados en las páginas.
- Correcciones ciclo 1 aplicadas y verificadas: `03-forge-cartography.md` (Temporal v1.35.0), `02-echo-cartography.md` (17 topics), `06-wiki-draft-plan.md` (3 fixes, L106/L202/L409).
- Fase E COMPLETE (vault `a87aa62`): 27 CANONICAL / 3 MERGE / 5+3 SUPERSEDED / ARCHIVE resto / 0 DELETE. ⚠️ Flag seguridad al owner: `30-resources/APIs.md` con credenciales vivas en texto plano — sin tocar, decisión del humano.
- Fase D COMPLETE: frontera rota en producción (pin SDK única frontera real; G1–G7 en `artifacts/04-echo-forge-boundary.md`).
- Fase C COMPLETE: Forge @ `9fad768c` — GenericSQXWorkflow + ForgeCampaignWorkflow (**Temporal SDK v1.35.0**); magic V1 cableado; PG/Mongo/MinIO/etcd.
- Fase B COMPLETE: Echo @ `f7ddea18` — **Flink StateFun, NO Temporal**; 17 topics Kafka; E-02 implementado (PHYSICAL_PARTIAL); receptor E-04 completo, Spec-Active.
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
