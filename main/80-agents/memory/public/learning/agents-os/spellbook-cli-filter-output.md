---
type: learning
schema_version: 1
scope: "project"
created: "2026-09-30"
updated: "2026-09-30"
area: "[[Meli]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[2026-09-30-playmaker-context-flows-session-feedback]]"
aliases:
  - "Filtrar JSON de Spellbook"
  - "Spellbook metadata de proyecto en respuestas CLI"
confidence: "high"
source_session: "01a0f2b3-8e01-7130-8ef6-ac26a639e079"
load_policy: "manual"
indexable: true
index_priority: high
tags:
  - "kind/learning"
  - "scope/project"
  - "project/agents-os"
  - "tech/spellbook"
---

# Spellbook CLI — filtrar salidas antes de mostrarlas

## Aprendizaje

Las respuestas de la CLI de Spellbook pueden incluir metadata del proyecto ajena al contenido solicitado. Capturar y parsear el JSON antes de mostrarlo; emitir sólo los campos necesarios, como `id`, `specNumber`, `title`, `type`, `status` o el cuerpo de la SPEC. No imprimir ni guardar el payload completo en notas de sesión o memoria.

## Aplicabilidad

- **Cuándo cargarlo:** al leer, crear, editar o verificar specs por CLI de Spellbook; criterio para scripts de orquestación y manejo de errores.
- **Cuándo no cargarlo:** edición local sin respuestas de Spellbook. No implica una falla de autenticación ni una política de renderizado.

## Entidades relacionadas

- [[AGENTS OS]]; procedimiento mecánico: [runbook de acceso](../../../../skills/signals-func-spec-authoring/references/spellbook-access-runbook.md).

## Evidencia

- Fuente: [[2026-09-30-playmaker-context-flows-session-feedback]] — la sesión observó metadata ajena a la SPEC en una respuesta completa; las lecturas siguientes emitieron sólo contenido y campos seleccionados.
