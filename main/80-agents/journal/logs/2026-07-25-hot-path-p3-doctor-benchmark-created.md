---
type: change_log
scope: session
created: "2026-07-25"
updated: "2026-07-25"
area: "[[Personal]]"
project: "[[AGENTS OS - Hot Path y Cierre Silencioso]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-doctor]]"
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
  - area/personal
  - project/agents-os
  - change/created
---

# Hot Path Iteration — P3 Doctor + Benchmark creados

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `80-agents/skills/agents-os-doctor/SKILL.md` — skill nueva, lint y
    auto-repair del AGENTS OS installation.
  - `80-agents/skills/agents-os-doctor/BENCHMARK.md` — gate E2E reproducible
    con 5 escenarios y criterios de aprobación.

## Motivo

- Sin un doctor, los hallazgos del brief (paths rotos, `always` mal usado,
  startup duplicado) se redescubren cada vez que alguien los pisa.
- Sin un gate E2E, no hay forma de saber si Hot Path realmente reduce tokens
  sin perder calidad de decisión. El gate convierte la métrica relevante
  ("reducir tokens sin perder una fuente que cambie la decisión") en algo
  medible y comparable.

## Fuentes usadas

- Brief de ChatGPT `agents-os-hot-path-brief.md` (sección "Iteración
  recomendada" ítem 4: doctor + benchmark).
- Hallazgos concretos encontrados durante P0/P1/P2:
  - Path integrity (drift `/Users/rjara` vs `/Users/rodrigojara`).
  - `load_policy` closed club (memoria Symphony marcada `always`).
  - Startup duplication (procedimientos duplicados en `agents-os.md`).
  - Refs rotas en `agents-os-skill-authoring`.
  - `session-close` marcado `always` en la guía aunque requiere trigger.
- `80-agents/skills/_shared/skill-contract.md` y `metadata-schema.md` como
  autoridades que el doctor valida.

## Resolución aplicada

- **Skill `agents-os-doctor`:** 11 checks categorizados, severidad HIGH/
  MEDIUM/LOW, output estructurado, política read-only por defecto (aplica
  fixes solo tras aprobación explícita). Un `change_log` consolidado por
  fix-set aprobado.
- **Benchmark E2E:** 5 escenarios (cold start / warm turn / swap entity /
  Graphify degradado / 4 tipos de cierre) con targets blandos y un criterio
  de aprobación compuesto. Registro de corridas en `journal/logs/`.
- **Integración con el routing:** `agents-os-bootstrap` ya enruta a
  `agents-os-doctor` desde su tabla lazy.

## Validación

- Skill creada desde template `templates/skill.md` (cumple el contrato).
- Frontmatter: `type: skill`, `name`, `description` accionables, tags
  correctos, `load_policy: manual` (lazy-load).
- `BENCHMARK.md` tiene frontmatter `type: benchmark` y vincula al proyecto
  controlador.
- Ambos archivos usan rutas relativas correctas (`../_shared/`).

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin secretos ni identidad.

## Pendiente

- Forward-test real del gate con agente fresco (primera corrida formal).
- Registrar la primera corrida en `journal/logs/` cuando se ejecute.
- Considerar mover el gate al proyecto `[[AGENTS OS - Beta y Hardening]]`
  como su benchmark oficial de beta.

## Rollback

- Borrar la carpeta `80-agents/skills/agents-os-doctor/` y quitar la entrada
  de routing del `agents-os-bootstrap/SKILL.md`. Sin dependencias cruzadas.
