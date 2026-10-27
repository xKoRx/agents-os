---
type: change_log
schema_version: 1
scope: session
created: "2026-10-26"
updated: "2026-10-26"
area: "[[Trading]]"
project: "[[Estrategias IMOX — Forex y CFD con Echo Forge]]"
application:
entities: ["[[Estrategias IMOX — Forex y CFD con Echo Forge]]"]
related: ["[[IMOX — Registro de campañas]]", "[[30-resources/agents/skills/sqx144-campaign-design/SKILL.md]]"]
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

# 2026-10-26-imox-sqb-catalog-contract

## Cambio

- **Tipo:** updated
- **Archivo(s):** proyecto IMOX y `IMOX — Registro de campañas.md`, commits `8b5b65bd` y `cb93ae92`.

## Motivo

- El owner requiere preservar y documentar todos los presets `.sqb` de familias/grupos/configs para que no se pierdan al crear múltiples Builders genéticos calibrados.

## Fuentes usadas

- Instrucción expresa del owner; documentación IMOX Building Blocks Skill y procedimiento `sqx144-campaign-design`.

## Resolución aplicada

- Contrato canónico de catálogo maestro SQX 144, identidad y revisiones de cada `.sqb`, SHA256 y referencias privadas, vinculación al Builder CFX, políticas de importación/review y relación con matriz/campañas. No se generó ningún preset ni se almacenaron los bytes privados.

## Validación

- Actualizaciones con optimistic concurrency por SHA de GitHub. No se ejecutó el validador local del vault; el próximo agente con checkout puede hacer lint dirigido.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** solo especificación de metadatos; sin contenidos privados, archivos `.sqb` reales ni secretos

## Rollback

- Revertir commits `8b5b65bd` y `cb93ae92`, sin afectar el resto del proyecto.
