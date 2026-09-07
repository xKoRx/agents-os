---
type: methodology
status: active
area: "[[Personal]]"
sources:
  - "[[github-spec-kit-agentic-sdd|GitHub Spec Kit — Agentic SDD]]"
  - "[[kiro-specs-structured-development|Kiro Specs — Structured Development]]"
  - "[[symphony-sdd-runtime-governance|Symphony SDD Runtime Governance]]"
  - "[[symphony-sdd-manual|Symphony SDD Manual]]"
last_verified: 2026-08-08
confidence: verified
aliases:
  - SDD lifecycle
  - ciclo SDD
tags:
  - kind/methodology
  - tech/sdd
created: 2026-08-08
updated: 2026-08-08
---

# SDD — Lifecycle

## Flujo base

```text
CLASSIFY → SPECIFY → CLARIFY/REVIEW → PLAN → TASKS → ANALYZE
         → IMPLEMENT (slice) → VERIFY → CONVERGE/CLOSE
```

`CLARIFY`, `ANALYZE` y `CONVERGE` pueden ser pasos explícitos o gates dentro de
la fase vecina. Lo obligatorio es su función, no el nombre del comando.

## Fases

| Fase | Pregunta | Salida | No hace |
|---|---|---|---|
| Classify | ¿Feature, cambio, bug, RCA o trabajo trivial? | routing y alcance | mezclar todos los artefactos |
| Specify | ¿Qué comportamiento/outcome se necesita? | spec/requerimientos | decidir el diff físico final |
| Plan | ¿Cómo encaja en el sistema real? | diseño/impact map | implementar |
| Tasks | ¿Qué slices ordenados ejecutan el plan? | checklist trazable | rediseñar silenciosamente |
| Implement | ¿Cómo cumplir una task acotada? | código + evidencia local | ampliar alcance sin volver atrás |
| Verify | ¿El cambio satisface contrato, plan y gates? | reporte/veredicto | corregir en silencio como autor |

## Retornos correctivos

- Gap de outcome/aceptación → Specify.
- Gap de arquitectura, impacto o rollback → Plan.
- Gap de orden, dependencia o granularidad → Tasks.
- Defecto de implementación → Implement.
- Evidencia insuficiente → Verify/Implement según la causa.

No se modifica el artefacto downstream para esconder un error upstream.

## Brownfield

1. Consultar el catálogo de capacidades/features.
2. Inspeccionar código, tests y contratos actuales.
3. Hacer backfill de la baseline durable sólo para la capacidad que se tocará.
4. Separar delta de cambio y RCA cuando corresponda.
5. Ejecutar el ciclo para el cambio actual.

## Handoffs

Cada transición que cruce sesión o responsable declara: feature, fase origen,
fase destino, artefactos requeridos, output esperado, restricciones, evidencia
y riesgos. El handoff apunta al estado versionado; no resume todo el proyecto.

## Fuentes y provenance

- [[github-spec-kit-agentic-sdd|GitHub Spec Kit — Agentic SDD]]
- [[kiro-specs-structured-development|Kiro Specs — Structured Development]]
- [[symphony-sdd-runtime-governance|Symphony SDD Runtime Governance]]
- [[symphony-sdd-manual|Symphony SDD Manual]]

## Límites

- Los gates humanos dependen del riesgo; quick specs pueden agrupar fases para
  trabajo conocido, pero no eliminan los artefactos ni la revisión posterior.
