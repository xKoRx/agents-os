---
type: skill
schema_version: 1
name: aranea-mcps-expert
description: Selecciona y gobierna el uso de las capabilities MCP del homelab Aranea. Cargar antes de usar cualquier MCP aranea-* para elegir ambiente, capability, autoridad y runbook correctos; nunca aplica a MELI ni a sistemas corporativos.
scope: area
created: "2026-09-11"
updated: "2026-09-12"
area: "[[Aranea]]"
entities:
  - "[[Aranea]]"
related:
  - "[[AGENT-PLATFORM - MCP Access Plane - Architecture]]"
  - "[[aranea-ssh-mcp]]"
  - "[[aranea-postgres-mcp]]"
  - "[[aranea-mongodb-mcp]]"
  - "[[aranea-mcp-capability-plane]]"
aliases:
  - aranea-mcps-expert
  - aranea mcp
  - mcp access plane
  - usar mcp
  - mcp ssh
  - mcp postgres
  - mcp mongo
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/area
  - area/aranea
  - tech/mcp
  - action/mcp-routing
---

# aranea-mcps-expert

## Purpose

Seleccionar cómo acceder a infraestructura y datos de Aranea mediante su capability plane MCP sin repartir credenciales finales ni mezclar ambientes.

Activar antes de usar cualquier capability `aranea-*`, o cuando una skill de dominio determine que necesita acceso MCP a un host, PostgreSQL o MongoDB de Aranea. No activar para trabajo local que no requiere MCP. **MUST NOT activate for Mercado Libre / MELI infrastructure, databases, repositories, hosts, credentials or corporate systems.**

## Canonical Authority

Esta skill es el router agent-facing. Los procedimientos mecánicos viven exclusivamente en `VAULT_ROOT/80-agents/memory/public/runbook/`:

- `80-agents/memory/public/runbook/aranea-ssh-mcp.md` → [[aranea-ssh-mcp]]
- `80-agents/memory/public/runbook/aranea-postgres-mcp.md` → [[aranea-postgres-mcp]]
- `80-agents/memory/public/runbook/aranea-mongodb-mcp.md` → [[aranea-mongodb-mcp]]
- `80-agents/memory/public/runbook/aranea-mcp-capability-plane.md` → [[aranea-mcp-capability-plane]]

La arquitectura/deployment común para **agregar o reemplazar capabilities** vive en [[AGENT-PLATFORM - MCP Access Plane - Architecture]]. No redescubrirla desde cero salvo evidencia material de drift.

No copiar procedimientos desde esos runbooks a esta skill.

## Minimal Read

1. Leer esta skill para elegir ambiente y capability.
2. Si la tarea **agrega, reemplaza o reinstala** una capability MCP, cargar obligatoriamente [[AGENT-PLATFORM - MCP Access Plane - Architecture]].
3. Cargar sólo el runbook de la familia elegida.
4. Cargar [[aranea-mcp-capability-plane]] sólo cuando el problema sea discovery/auth/transporte/policy del plano MCP mismo.

## Procedure

### 1. Confirmar boundary Aranea

Si el target es MELI/corporativo, detener esta skill y usar las autoridades corporativas correspondientes.

### 2. Elegir primero el ambiente

Para data MCPs el ambiente determina la capability; RO y RW no son dos niveles intercambiables sobre el mismo ambiente.

| Sistema / necesidad | Ambiente | Capability | Authority |
|---|---|---|---|
| Echo PostgreSQL consulta productiva | PROD | `aranea-postgres-ro` | read-only |
| Echo PostgreSQL lectura o mutación de desarrollo | DEV | `aranea-postgres-rw` | read/write; puede usarse para lecturas DEV sin mutar |
| Echo Forge MongoDB consulta productiva | PROD | `aranea-mongo-forge-ro` | read-only |
| Echo Forge MongoDB lectura o mutación de desarrollo | DEV | `aranea-mongo-forge-rw` | read/write; puede usarse para lecturas DEV sin mutar |
| runtime/logs/archivos workers | según perfil | `aranea-ssh` | viewer para evidencia; operator cuando la operación necesita escritura/ejecución |

**Invariante:** no usar PROD RO para verificar una mutación DEV y no cambiar de ambiente para conseguir más o menos autoridad.

### 3. Elegir autoridad mínima dentro del ambiente correcto

En SSH, viewer es default para evidencia y operator sólo si la operación exige mutación/ejecución. En data MCPs no existe una capability DEV RO separada: una lectura DEV usa el endpoint RW sin convertir la lectura en mutación.

### 4. Cargar el runbook de la familia

- host/runtime → [[aranea-ssh-mcp]]
- PostgreSQL → [[aranea-postgres-mcp]]
- MongoDB → [[aranea-mongodb-mcp]]

Si se está incorporando una familia nueva, la arquitectura común se toma de [[AGENT-PLATFORM - MCP Access Plane - Architecture]] y sólo se documenta aparte lo específico del servicio.

### 5. Acotar y ejecutar

Fijar host/perfil o database/schema/table/collection/identificador. Ejecutar sólo la operación necesaria. Para mutaciones, identificar primero el target en el mismo ambiente, fijar blast radius, declarar post-condición, ejecutar y verificar en ese mismo ambiente.

### 6. Tratar boundaries como evidencia

- capability ausente del inventario → revisar discovery/config/env del cliente antes de culpar al backend;
- `401` → diagnosticar bearer/config del cliente sin pedir ni imprimir el secreto;
- `POLICY_DENIED` / permission denied → revisar el boundary del runbook, no crear bypass;
- timeout → reducir scope/optimizar antes de ampliar policy;
- una capability configurada pero sin tools expuestas no prueba fallo de PostgreSQL/MongoDB: primero aislar cliente/auth/handshake.

## Output

```text
Environment: <PROD|DEV|runtime>
Capability: <aranea-*>
Authority: <viewer|operator|RO|RW>
Target: <host/profile/database/collection/schema>
Operation: <acción ejecutada>
Evidence: <resultado material>
Mutation: <none | target + post-condition + same-environment verification>
Boundary: <none | policy/error relevante>
```

## Hard Rules

- Esta skill es **Aranea-only**; nunca usarla para MELI o sistemas corporativos.
- Elegir ambiente antes que capability/autoridad.
- PROD de datos es RO; DEV de datos es RW. No inventar sandbox, profiles dinámicos ni nuevos ambientes como workaround.
- Toda capability nueva debe respetar [[AGENT-PLATFORM - MCP Access Plane - Architecture]]: proxy bearer separado, backend interno sin host port, secretos upstream separados y pinning reproducible, salvo excepción explícitamente aprobada.
- `SUPERUSER`, `CREATEDB` y `CREATEROLE` no son requisitos del PostgreSQL MCP DEV salvo que un contrato explícito distinto los exija; su ausencia no es blocker por defecto.
- Nunca pedir, imprimir, copiar, persistir ni registrar bearer tokens, passwords o private keys.
- No saltar el proxy MCP ni usar acceso directo agent-first cuando existe capability canónica que cubre la acción.
- No cambiar ACLs/privilegios, publicar backends internos ni crear side channels como workaround automático.
- Skills consumidoras deben referenciar esta skill en vez de duplicar endpoints, permisos o semántica MCP.
- No copiar esta skill a `80-agents/skills/` ni duplicar los runbooks fuera de `80-agents/memory/public/runbook/`.
