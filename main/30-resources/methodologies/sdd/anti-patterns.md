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
  - SDD anti-patterns
  - anti-patrones SDD
tags:
  - kind/methodology
  - tech/sdd
created: 2026-08-08
updated: 2026-08-08
---

# SDD — Anti-patterns

## Fallas recurrentes

| Anti-patrón | Síntoma | Corrección |
|---|---|---|
| Code-first con spec retroactiva | la spec justifica el diff ya hecho | volver a outcomes y aceptación antes del plan |
| Phase mixing | SPEC enumera archivos/SQL/tasks finales | mover cada decisión al artefacto dueño |
| Plan sólo en chat | otro agente no puede retomar | persistir diseño y tasks versionadas |
| Spec monolítica | mezcla baseline, bug, RCA y rollout | separar capability, change y RCA |
| Catálogo ornamental | estado no coincide con repo | actualizar lifecycle en cada hito real |
| Big-bang brownfield | meses de docs sin cambio entregado | backfill just-in-time por capacidad tocada |
| Task gigante | una task exige recordar toda la conversación | cortar en slices verticales con gate propio |
| Implementor rediseña | aparecen decisiones sin actualizar plan/spec | detener y volver a la fase dueña |
| Verifier que corrige | el reporte nunca puede fallar | separar auditoría de reparación |
| Test masking | skips, assertions débiles, coverage menor | registrar cambio de contrato y auditar tests |
| Docs duplicadas por herramienta | cada IDE tiene su propia verdad | canon agnóstico + adapters/pointers mínimos |
| SDD para todo | cambios triviales pagan ritual completo | definir fast path proporcional y explícito |
| Threshold global inventado | una cifra local se vuelve dogma | mantener umbrales en la constitution del repo |

## Señal de drift

Si el artefacto describe una fase futura mientras el runtime ya cambió, marcar
la fuente como superseded o actualizarla. No sintetizar ambos estados como si
fueran compatibles.

## Fuentes y provenance

- [[github-spec-kit-agentic-sdd|GitHub Spec Kit — Agentic SDD]]
- [[kiro-specs-structured-development|Kiro Specs — Structured Development]]
- [[symphony-sdd-runtime-governance|Symphony SDD Runtime Governance]]
- [[symphony-sdd-manual|Symphony SDD Manual]]

## Límites

- Un anti-patrón describe un riesgo; no autoriza enforcement que el repo no haya
  adoptado.
