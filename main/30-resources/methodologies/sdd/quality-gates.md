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
  - SDD quality gates
  - gates SDD
tags:
  - kind/methodology
  - tech/sdd
created: 2026-08-08
updated: 2026-08-08
---

# SDD — Quality Gates

## Gate por transición

| Transición | Evidencia mínima |
|---|---|
| Classify → Specify | tipo de trabajo, owner y alcance identificados |
| Specify → Plan | outcomes/aceptación claros, contradicciones y preguntas bloqueantes resueltas |
| Plan → Tasks | impact map, riesgos, compatibilidad, rollout/rollback y comandos de validación |
| Tasks → Implement | slices pequeños, dependencias, archivos permitidos y criterio por task |
| Implement → Verify | diff acotado, checks locales registrados, desvíos visibles |
| Verify → Close | trazabilidad completa, gates ejecutados, findings resueltos/aceptados y veredicto |

## Propiedades de un gate útil

- Verificable: comando, inspección o decisión explícita.
- Proporcional: su costo responde al riesgo.
- Honesto: un failure se registra antes de corregirse.
- Trazable: conecta outcome → diseño → task → diff → evidencia.
- Independiente cuando importa: el verificador no arregla lo que audita.

## Quality loops

Antes de implementar, ejecutar consistencia entre spec, plan y tasks. Después,
comparar implementación con los tres y volver a la fase dueña de cada gap. Un
build verde es necesario pero no suficiente: faltan revisión de contrato,
comportamiento, seguridad, observabilidad y no-regresión según el dominio.

## Integridad de tests

Cambiar tests existentes puede ser legítimo cuando cambia el contrato, pero la
decisión debe ser explícita y trazable. Prohibido debilitar assertions, ocultar
tests, bajar coverage o sustituir integración real por mocks para obtener verde.
Repos de alto riesgo pueden exigir un `TEST_CHANGE_REQUEST` y separar permisos.

## Fuentes y provenance

- [[github-spec-kit-agentic-sdd|GitHub Spec Kit — Agentic SDD]]
- [[kiro-specs-structured-development|Kiro Specs — Structured Development]]
- [[symphony-sdd-runtime-governance|Symphony SDD Runtime Governance]]
- [[symphony-sdd-manual|Symphony SDD Manual]]

## Límites

- Los thresholds, comandos y severidades pertenecen a la constitution del repo.
- Un gate manual no debe presentarse como automatizado.
