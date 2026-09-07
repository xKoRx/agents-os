---
type: decision
schema_version: 1
scope: project
created: 2026-08-10
updated: 2026-08-10
area: "[[Personal]]"
project: "[[AGENTS OS - Fase 3]]"
entities:
  - "[[AGENTS OS]]"
  - "[[AGENTS OS - Fase 3]]"
related:
  - "[[schema-contract]]"
  - "[[Economía de Tokens]]"
  - "[[token-economy-indexing-architecture]]"
aliases:
  - AGENTS OS executable schema contract versioning
  - Contrato ejecutable y versionado de AGENTS OS
confidence: verified
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/agents-os
  - tech/agents-os
---

# AGENTS OS — Contrato Ejecutable y Versionado

## Contexto

Los sets exactos de tipos, campos, lifecycle y templates estaban repartidos
entre guías Markdown y constantes del lint. Fase 3 requiere una autoridad
machine-readable sin dejar de usar Markdown como fuente de verdad.

## Decisión

- El bloque JSON estricto de `schema-contract.md` es la autoridad ejecutable
  única para S1/S2; las otras notas explican semántica sin copiar sets.
- `schema_version` es entero. La versión actual es `1`; notas sin versión son
  legacy read-only y versiones desconocidas se rechazan.
- Cambios incompatibles usan nueva versión y migrador explícito; no hay
  retrofit masivo por inferencia.
- Cada tipo creable tiene un template canónico. Derivados y fragmentos sólo
  existen mediante exención justificada en el contrato.
- F1 valida contrato/templates con un auditor propio. F2 debe hacer que el
  lint preventivo consuma el mismo bloque y elimine sus constantes duplicadas.
- Toda creación canónica pasa por un materializador local fail-closed; las
  skills creadoras son entrypoints auditados del contrato.
- El fail-closed de creación se aplica al envelope común y al tipo/template
  solicitado. El auditor global de los 42 templates queda reservado para
  cambios del contrato, Doctor y release; drift no relacionado no puede
  bloquear artefactos de cierre sanos.

## Rationale

JSON puede parsearse con Python stdlib, mantiene el contrato dentro de una
nota auditable y permite probar mapping, versiones y cobertura sin introducir
otra autoridad o dependencia runtime.

La resolución es un filtro programático local de costo LLM cero. El cuerpo
completo del contrato se carga sólo al mantener el schema, nunca como parte del
hot path. Esto preserva [[Economía de Tokens]]: metadata barata antes de cuerpo.

## Consecuencias

- Templates y notas nuevas usan la versión actual.
- Una nota legacy se migra al modificarla, no por un barrido ciego.
- Lifecycle/create falla cerrado ante tipo desconocido, exento o mapping roto.
- Un template roto bloquea su propio tipo, no tipos sanos del otro sistema;
  la regresión scoped/global se prueba con fixture aislada.
- Hasta F2, el lint legacy conserva constantes sólo para mantener el baseline;
  esa duplicación está acotada y no define nuevas reglas.

## Alternativas descartadas

- YAML/JSON externo: separaría la autoridad del Markdown canónico.
- Mantener tablas y constantes sincronizadas manualmente: perpetúa drift.
- Versionar sólo templates: no identifica el contrato de notas live.
- Agregar `schema_version` a todo el corpus ahora: mezcla F1 con el retrofit F6.
