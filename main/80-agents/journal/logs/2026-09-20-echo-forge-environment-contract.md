---
type: change_log
schema_version: 1
scope: session
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Echo]]"
project: "[[Echo — Producto Integrado]]"
application:
entities:
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[aranea-agent-dev]]"
related:
  - "[[Echo — Live Platform V1]]"
  - "[[Echo Forge — Factory V2 Completion]]"
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

# 2026-09-20 — Echo Forge environment contract

## Cambio

- **Tipo:** created / updated.
- **Archivos:**
  - `30-resources/aranea/07-integration/Echo + Echo Forge — Environment Contract.md` — created, source canónica de separación DEV/PROD y estado TARGET vs AS-BUILT.
  - `30-resources/agents/skills/aranea-agent-dev/SKILL.md` — updated para lectura obligatoria scoped en cold start/entity swap Echo/Forge, sin modificar bootstrap global.
  - `80-agents/journal/logs/2026-09-20-echo-forge-environment-contract.md` — este registro.

## Motivo

Evitar que coding agents confundan entornos, interpreten un clon Windows o workers compartidos como DEV aislado, o recurran a PROD porque no haya infraestructura DEV física certificada. Mantener mapa factual breve en Sistema 2 y procedimiento de carga en skill federada, sin duplicar runbooks.

## Fuentes usadas

- Decisiones owner 2026-09-20: Daedalus como DEV, `192.168.31.132` como Windows DEV clonado, workers actuales compartidos, infraestructura de datos DEV/PROD existente.
- `Echo — Producto Integrado`, `Echo — Access & Physical Capability Matrix`, `Daedalus — Development Agents MCP Access & Gaps` y `aranea-ssh-mcp` para semántica de estados y acceso.
- `agent-constitution`, `agents-os-bootstrap`, `schema-contract`, template `70-templates/doc.md`.

## Resolución aplicada

- Un contrato delgado con ambientes, aislamiento, hitos y enlaces; procedimientos exactos quedan en runbooks.
- DEV default, PROD nunca fallback; mutaciones ambiguas bloqueadas.
- No se declara `dev-win`, SQX Daedalus ni Core/Gateway DEV físicamente verificados sin informe AS-BUILT de Hermes.
- Alcance de escritura únicamente `xKoRx/agents-os`. No editar `AGENTS.md` de Echo/Symphony ni actualizar datos runtime sin evidencia nueva.

## Validación

- Crear contrato y actualizar skill mediante GitHub Contents API con SHA existente.
- Verificar lectura de archivos resultantes y referencias cruzadas; no se ejecutaron smokes de infraestructura ni validador local de esquema desde el vault montado.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin passwords, tokens, claves privadas o rutas absolutas personales; IP designada no es credencial.

## Rollback

- Revertir commits del contrato y la skill mediante Git, preservando modificaciones concurrentes y verificando sus SHAs. No revertir estado de infraestructura: no se ejecutaron mutaciones de hosts.
