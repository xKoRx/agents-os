---
type: change_log
schema_version: 1
scope: session
created: "2026-08-24"
updated: "2026-08-24"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[Crear Context]]"
related:
  - "[[agents-os-entity-lifecycle]]"
  - "[[agents-os-agent-project-workflow]]"
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
---

# 2026-08-24-development-project-spec-branch-contract

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):** `70-templates/project.md`; `80-agents/skills/agents-os-entity-lifecycle/SKILL.md`; `80-agents/skills/agents-os-agent-project-workflow/SKILL.md`; `10-projects/Meli/Crear Context/Crear Context.md`; `10-projects/Meli/Crear Context/SPEC Funcional — Context IO.md`; `10-projects/Meli/Crear Context/SPEC Tecnica — Context IO.md`.

## Motivo

- Los proyectos de desarrollo no tenían un lugar estándar ni un gate durable para relacionar SPEC funcional, SPEC técnica y las branches/bases de cada repo afectado.

## Fuentes usadas

- Pedido explícito del owner del vault.
- Estructura vigente de `70-templates/project.md`, contrato de creación en `agents-os-entity-lifecycle` y protocolo de ejecución en `agents-os-agent-project-workflow`.

## Resolución aplicada

- El template de proyecto incorpora una sección `## 🧱 Entrega de desarrollo` con una fila por repo/branch y columnas para base, SPEC funcional, SPEC técnica y estado.
- `agents-os-entity-lifecycle` clasifica los proyectos de desarrollo al crearlos y exige completar la sección antes de implementar; los proyectos no técnicos conservan la sección con un `No aplica` justificado.
- `agents-os-agent-project-workflow` usa esa sección como gate durable al iniciar o retomar una ejecución de código.
- `Crear Context` adopta la sección y apunta a las SPECs canónicas del repo `rio-playmaker` mediante repo + path relativo.
- Los mirrors funcional y técnico del vault quedan `archived` porque estaban desalineados y competían con `.sdd/features/new-component-context/`; se preservan sólo como trazabilidad histórica.

## Validación

- Schema contract PASS: 45 tipos, 44 templates canónicos, 5 fixtures, 0 errores.
- Lint estricto de las seis notas canónicas modificadas PASS: 0 errores, 0 warnings. El template se validó mediante el schema contract porque sus placeholders de fecha no son valores materializados.
- Doctor: HIGH=0, MEDIUM=2, LOW=0; los dos MEDIUM son deuda ajena a este cambio (`signals-spec-authoring` ausente del índice y startup estimado sobre el soft target).
- Graphify update bloqueado por 10 errores y 1 warning en notas ajenas a este cambio; los paths modificados por esta entrega pasan lint estricto y no agregan findings.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir este change log junto con la nueva sección del template y las reglas agregadas a ambas skills; retirar la sección de `Crear Context` solo si se reemplaza por otra fuente canónica equivalente.
