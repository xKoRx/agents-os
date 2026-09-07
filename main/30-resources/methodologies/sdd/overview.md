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
  - SDD overview
  - Spec-Driven Development
tags:
  - kind/methodology
  - tech/sdd
created: 2026-08-08
updated: 2026-08-08
---

# SDD — Overview

## Propósito

Spec-Driven Development convierte la intención y las decisiones en artefactos
versionados antes de ejecutar cambios. Su objetivo no es producir más
documentación, sino reducir improvisación, pérdida de contexto y validación
oportunista en trabajo que cruza fases o sesiones.

## Núcleo portable

Las implementaciones difieren en nombres, pero convergen en este flujo:

```text
intent/requirements → spec → design/plan → tasks → implementation → verification
```

- La spec describe outcomes, alcance, restricciones y aceptación.
- El plan decide impacto técnico, riesgos, rollout y rollback.
- Las tareas convierten el plan en slices pequeños y verificables.
- La implementación respeta el contrato y registra evidencia.
- La verificación compara comportamiento, artefactos y cambio real.

## Cuándo usarlo

Aplicar el ciclo completo cuando haya cambios de contrato, más de un componente,
riesgo operativo, incertidumbre significativa, trabajo brownfield o handoffs.
Para cambios triviales y bien entendidos, usar una versión liviana explícita;
el threshold exacto pertenece al repositorio, no a esta metodología global.

## Principios

1. El artefacto dueño de una decisión manda sobre el chat.
2. Cada fase tiene una pregunta y permisos distintos.
3. Un gap vuelve a la fase que lo originó; no se parchea aguas abajo.
4. La evidencia de verificación forma parte del entregable.
5. La metodología es reusable; las specs concretas viven con el código/proyecto.
6. Brownfield se documenta just-in-time, no con un big bang preventivo.

## Fuentes y provenance

- [[github-spec-kit-agentic-sdd|GitHub Spec Kit — Agentic SDD]]
- [[kiro-specs-structured-development|Kiro Specs — Structured Development]]
- [[symphony-sdd-runtime-governance|Symphony SDD Runtime Governance]]
- [[symphony-sdd-manual|Symphony SDD Manual]]

## Límites

- SDD no garantiza una spec correcta; exige revisión y evidencia.
- No vuelve inmutable cada detalle: las decisiones cambian mediante lifecycle.
- No impone una herramienta, un set de comandos ni nombres universales.
- No sustituye discovery de código, tests, observabilidad ni criterio humano.
