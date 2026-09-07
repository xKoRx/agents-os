---
type: methodology
status: active
area: "[[Personal]]"
sources:
  - "[[symphony-sdd-runtime-governance|Symphony SDD Runtime Governance]]"
  - "[[symphony-sdd-manual|Symphony SDD Manual]]"
  - "[[github-spec-kit-agentic-sdd|GitHub Spec Kit — Agentic SDD]]"
last_verified: 2026-08-08
confidence: high
aliases:
  - SDD roles
  - Coordinator Implementor Verifier
tags:
  - kind/methodology
  - tech/sdd
created: 2026-08-08
updated: 2026-08-08
---

# SDD — Roles

## Responsabilidades

| Rol lógico | Es dueño de | Límite principal |
|---|---|---|
| Coordinator | clasificación, spec, plan, tasks y decisiones bloqueantes | no mezcla planificación con implementación |
| Implementor | una o más tasks acotadas y su evidencia local | no amplía alcance ni debilita gates |
| Verifier | auditoría contra artefactos y realidad | no corrige el código que está calificando |
| Owner/humano | intención, trade-offs materiales y aceptación final | no delega decisiones de negocio implícitamente |

Son responsabilidades, no una obligación de usar tres productos o modelos. Una
persona puede desempeñar más de un rol en cambios simples; en trabajo no trivial
conviene reset de contexto o actor independiente para Verify.

## Permisos

- Coordinator lee el repo y escribe artefactos de definición/planificación.
- Implementor escribe sólo el alcance de las tasks aprobadas.
- Verifier ejecuta checks y escribe evidencia/veredicto.
- Cambios al contrato vuelven al Coordinator antes de continuar.

## Handoffs

El handoff transmite phase, artefactos, output, restricciones y riesgos. No debe
inyectar una interpretación paralela a lo que dicen los archivos canónicos.

## Fuentes y provenance

- [[symphony-sdd-runtime-governance|Symphony SDD Runtime Governance]]
- [[symphony-sdd-manual|Symphony SDD Manual]]
- [[github-spec-kit-agentic-sdd|GitHub Spec Kit — Agentic SDD]]

## Límites

- La separación rígida de escritura usada por Symphony es una política local
  para un sistema productivo; otros repos pueden aplicar controles más livianos.
- Independencia no significa desconocimiento: Verify necesita leer todo el
  contexto canónico y el diff.
