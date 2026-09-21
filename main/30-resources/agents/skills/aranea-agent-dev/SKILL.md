---
type: skill
schema_version: 1
name: aranea-agent-dev
description: Router exclusivo del dominio Aranea homelab para trabajo de desarrollo y operación del agente. Cargar para Echo, Echo Forge, Hermes, mcps, backups o red; acceso MCP sólo por aranea-mcps-expert, nunca MELI.
scope: area
created: "2026-09-12"
updated: "2026-09-20"
area: "[[Aranea]]"
entities:
  - "[[Aranea]]"
related:
  - "[[aranea-mcps-expert]]"
  - "[[Daedalus — Development Agents MCP Access & Gaps]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[hermes-agent-operator]]"
  - "[[rjara-aranea-operations-preferences]]"
  - "[[meli-agent-dev]]"
  - "[[Echo]]"
  - "[[Echo Forge]]"
aliases:
  - aranea agent dev
  - dominio aranea
  - aranea dev routing
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/area
  - area/aranea
  - action/domain-routing
  - tech/agents-os
---

# aranea-agent-dev

## Purpose

Dominio exclusivo del homelab Aranea. Fija boundary del dominio, carga preferencias scoped y enruta hacia acceso MCP y skills de dominio. Las capabilities `aranea-*` (13 registradas al 2026-09-17: SSH, PostgreSQL RO/RW, Mongo Forge RO/RW, Hasura PROD/DEV, Kafka DEV, Flink DEV, observabilidad ARGUS RO, Temporal RO, MinIO RO, etcd RO) pertenecen **exclusivamente** a este dominio; selección, estado y procedimientos en [[aranea-mcps-expert]], no duplicar el inventario aquí ni habilitar en MELI. El gateway Telegram de Hermes NO es automáticamente un MCP Telegram para coding agents.

**Trigger:** trabajo sobre hosts/servicios Aranea, Hermes Agent, Echo/Echo Forge DEV o PROD, appliance `mcps`, backups/DR, red del homelab o capability `aranea-*`. **No trigger:** MELI/corporativo (→ [[meli-agent-dev]]) ni trabajo puramente local sin infra Aranea.

## Minimal Read

1. Esta skill y boundary.
2. `../../../../80-agents/memory/public/user-preference/rjara-aranea-operations-preferences.md` — preferencias scoped Aranea.
3. **Echo o Echo Forge, cualquiera sea el tipo de tarea:** [[Echo + Echo Forge — Environment Contract]] es lectura obligatoria al inicio de la sesión o al cambiar hacia esta entidad, **antes de seleccionar ambiente, acceder a infraestructura o emitir instrucciones de despliegue**. Es contrato de contexto scoped, NO `load_policy: always` global. En warm turns de la misma entidad reutilizarlo; recuperar sólo deltas por cambio de fuente, target, ambiente o drift. No convertir una decisión TARGET en certificación física.
4. `30-resources/aranea/00-index.md` — wiki de dominio, sólo páginas necesarias.
5. [[hermes-agent-operator]] sólo cuando Hermes es **target** (gateway, systemd, perfiles, dashboard/update/recovery), no porque sea actor de una operación en otro host.
6. [[aranea-mcps-expert]] cuando se requiere acceso MCP; para coding agents Daedalus y preguntas de acceso que bloquea Echo/Forge, su matriz enlazada [[Daedalus — Development Agents MCP Access & Gaps]].

## Procedure

1. Confirmar que el target es Aranea. Si es MELI/corporativo, STOP antes de cargar documentación/conectar y swap explícito a [[meli-agent-dev]].
2. Si la entidad/tarea es Echo o Echo Forge, **MUST READ** [[Echo + Echo Forge — Environment Contract]] en cold start o entity swap, incluso para planificación, review o análisis que pueda orientar operaciones. La lectura sigue al bootstrap canónico y no lo reemplaza; no repetirla en cada turno cálido salvo invalidación. Si la nota falta, es contradictoria o no se puede recuperar, permitir lectura/trabajo local pero bloquear la mutación de infraestructura afectada hasta resolver ambiente y autoridad.
3. Cargar preferencias scoped, luego página de dominio pertinente desde índice; no escanear todo el vault.
4. Antes de cualquier operación Echo/Forge, determinar DEV/PROD, target, permisos OS/MCP, resources/queues/identidad, ownership, blast radius y estado runtime real. DEV es default para desarrollo; PROD nunca es fallback. Si una configuración DEV o una ruta de worker compartido no demuestra aislamiento, STOP de la mutación afectada. La lectura del contrato no concede permiso de ejecución.
5. Hermes como runtime/target: [[hermes-agent-operator]]. Si Hermes sólo opera `mcps`/Daedalus/otro servicio, usar skill del target y no confundir actor con target.
6. Acceso MCP: activar [[aranea-mcps-expert]], elegir ambiente PROD/DEV/runtime ANTES de capability y autoridad mínima, verificar cliente concreto Cursor/ZCode/Codex, cargar runbook de familia. Esta skill no abre MCP por su cuenta.
7. Para plugins SQX/troubleshooting Echo Forge/WFM, usar skills app-owned de `xKoRx/symphony/.agents/skills/`; delegan MCP al router aquí y no duplican tokens/endpoints. Runbooks operativos son lazy-load, no parte de lectura mínima.

## Output

```text
Dominio:            aranea
Target:             <host/servicio/app> | NO_DEMOSTRADO
Ambiente Echo/Forge:<DEV|PROD|NO_DETERMINADO|no aplica>
Contrato Echo/Forge:<leído|reutilizado|bloqueado|no aplica>
Prefs:              aranea-operations
Hermes target:       <sí → hermes-agent-operator | no>
MCP requerido:      <sí → aranea-mcps-expert + consumer real | no>
Skill de dominio:   <hermes-agent-operator | aranea-mcps-expert | app-owned | ninguna>
Dominio rechazado:  <ninguno | meli/local + motivo>
```

## Hard Rules

- Todas las `aranea-*` pasan por [[aranea-mcps-expert]] y quedan fuera de MELI/corporativo.
- Echo/Forge exige lectura scoped del contrato de ambientes en cada sesión nueva o cambio de entidad; no duplicar su topología ni cargarla globalmente para otros proyectos.
- Hermes como target usa [[hermes-agent-operator]]; no activarla sólo porque Hermes opera otro target.
- Ambiente antes que autoridad; RO PROD no se amplía ni se sustituye con DEV para obtener permiso. PROD no es fallback de DEV. `approvalPolicy=auto` no es aprobación humana.
- Un worker compartido, un clon Windows o un endpoint aparentemente DEV no implican aislamiento certificado. La ausencia de evidencia no autoriza mutación.
- No mezclar documentación/bearers/repos MELI y Aranea; hacer swap explícito de dominio.
- No copiar skills/router/runbooks federados a `80-agents/skills/` ni a repos de clientes; el vault cura y el repo owner posee su documentación específica.
