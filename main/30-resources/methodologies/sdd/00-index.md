---
type: index
status: active
icon: 📐
slug: sdd-methodology-index
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-08-08
updated: 2026-08-08
reviewed: 2026-08-08
aliases:
  - SDD index
  - Spec-Driven Development index
  - índice SDD
cssclasses:
  - wide
---

# 📐 Spec-Driven Development — Índice

> [!info] Dominio metodológico reusable
> Selecciona primero una página; no cargues el dominio completo. Las specs de
> features reales viven en `<repo>/specs/`, no acá.

## 📊 De un vistazo

- **Páginas:** 6 de metodología + 5 de provenance
- **Última ingesta:** 2026-08-08
- **Última verificación:** 2026-08-08
- **Confianza:** verified
- **Estado:** active

## 📂 Catálogo

| Página | Una línea | Meta |
|---|---|---|
| [[overview|SDD — Overview]] | Cuándo aplicar SDD, núcleo portable y adaptación por riesgo. | verified · 4 fuentes activas |
| [[lifecycle|SDD — Lifecycle]] | Flujo intent/spec → plan → tasks → implement → verify, con retorno al artefacto dueño del gap. | verified · lifecycle |
| [[artifact-model|SDD — Artifact Model]] | Autoridad y límites de constitution, catálogo, spec, plan, tasks, changes/RCA y verification. | verified · artifacts |
| [[quality-gates|SDD — Quality Gates]] | Gates de entrada/salida, trazabilidad, verificación y evidencia honesta. | verified · quality |
| [[roles|SDD — Roles]] | Responsabilidades Coordinator/Implementor/Verifier sin atarlas a una herramienta. | high · governance |
| [[anti-patterns|SDD — Anti-patterns]] | Fallas recurrentes: phase mixing, docs duplicadas, big-bang backfill y test masking. | verified · risks |

## 🔎 Provenance

| Fuente | Estado | Uso |
|---|---|---|
| [[github-spec-kit-agentic-sdd|GitHub Spec Kit — Agentic SDD]] | active | Flujo portable, constitution, clarify/analyze/converge. |
| [[kiro-specs-structured-development|Kiro Specs — Structured Development]] | active | Variante requirements/design/tasks/execution y quick specs. |
| [[symphony-sdd-runtime-governance|Symphony SDD Runtime Governance]] | active | Taxonomía durable/delta/RCA, permisos y verificación real. |
| [[symphony-sdd-manual|Symphony SDD Manual]] | active | Handoffs, brownfield JIT, atomic slices y anti-test-masking. |
| [[symphony-sdd-adoption-plan|Symphony SDD Adoption Plan]] | superseded | Evidencia histórica; no representa el runtime vigente. |

## 🚨 Salud

- **Contradicción resuelta:** el plan histórico de adopción afirma que Fase 0
  no se ejecutó, pero el repo ya contiene constitution, reglas, skills y specs.
  Se conserva como `superseded`; para estado actual manda runtime governance.
- **Specs concretas duplicadas:** 0.
- **Capturas crudas indexadas:** 0.

## 🔗 Links

- [[30-resources/00-RESOURCE-WIKI|Reglas de la Resource Wiki]]
- [[30-resources/methodologies/00-index|Índice de metodologías]]
- `log.md` — bitácora de ingest/query/lint
