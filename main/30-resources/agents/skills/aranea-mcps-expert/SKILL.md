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
  - "[[aranea-hasura-mcp]]"
  - "[[aranea-mcp-capability-plane]]"
aliases:
  - aranea-mcps-expert
  - aranea mcp
  - mcp access plane
  - usar mcp
  - mcp ssh
  - mcp postgres
  - mcp mongo
  - mcp hasura
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

Activar antes de usar cualquier capability `aranea-*`, o cuando una skill de dominio determine que necesita acceso MCP a un host, PostgreSQL, MongoDB o Hasura de Aranea. No activar para trabajo local que no requiere MCP. **MUST NOT activate for Mercado Libre / MELI infrastructure, databases, repositories, hosts, credentials or corporate systems.**

## Canonical Authority

Esta skill es el router agent-facing. Los procedimientos mecánicos viven exclusivamente en `VAULT_ROOT/80-agents/memory/public/runbook/`:

- `80-agents/memory/public/runbook/aranea-ssh-mcp.md` → [[aranea-ssh-mcp]]
- `80-agents/memory/public/runbook/aranea-postgres-mcp.md` → [[aranea-postgres-mcp]]
- `80-agents/memory/public/runbook/aranea-mongodb-mcp.md` → [[aranea-mongodb-mcp]]
- `80-agents/memory/public/runbook/aranea-hasura-mcp.md` → [[aranea-hasura-mcp]]
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

| Sistema / necesidad | Ambiente | Capability | Authority |
|---|---|---|---|
| Echo PostgreSQL consulta productiva | PROD | `aranea-postgres-ro` | read-only |
| Echo PostgreSQL lectura o mutación de desarrollo | DEV | `aranea-postgres-rw` | read/write; puede usarse para lecturas DEV sin mutar |
| Echo Forge MongoDB consulta productiva | PROD | `aranea-mongo-forge-ro` | read-only |
| Echo Forge MongoDB lectura o mutación de desarrollo | DEV | `aranea-mongo-forge-rw` | read/write; puede usarse para lecturas DEV sin mutar |
| Hasura inspección administrativa productiva | PROD | `aranea-hasura-prod-ro` | read-only estricto; exactamente 4 tools Hasura server-side |
| Hasura administración de desarrollo | DEV | `aranea-hasura-dev-admin` | admin Hasura; mutaciones sólo con scope/post-condición explícitos |
| runtime/logs/archivos workers | según perfil | `aranea-ssh` | viewer para evidencia; operator cuando la operación necesita escritura/ejecución |

**Invariante:** elegir ambiente antes que autoridad. No cambiar de ambiente para conseguir más permisos ni usar una capability DEV para verificar estado PROD.

### 3. Elegir autoridad mínima dentro del ambiente correcto

En SSH, viewer es default para evidencia y operator sólo si la operación exige mutación/ejecución. En data MCPs no inventar capabilities nuevas como workaround. En Hasura, PROD y DEV son contratos distintos: PROD es inspección estricta; DEV puede administrar metadata/DDL cuando la tarea lo requiere.

Para Hasura PROD, la superficie certificada es exclusivamente:

```text
export_metadata
get_inconsistent_metadata
get_schema
get_version
```

`run_sql`, `reload_metadata` y mutadores de metadata no existen en la capability PROD. No ampliar esta superficie para resolver una tarea puntual.

### 4. Cargar el runbook de la familia

- host/runtime → [[aranea-ssh-mcp]]
- PostgreSQL → [[aranea-postgres-mcp]]
- MongoDB → [[aranea-mongodb-mcp]]
- Hasura → [[aranea-hasura-mcp]]

Si se está incorporando una familia nueva, la arquitectura común se toma de [[AGENT-PLATFORM - MCP Access Plane - Architecture]] y sólo se documenta aparte lo específico del servicio.

### 5. Acotar y ejecutar

Fijar host/perfil o database/schema/table/collection/metadata object. Ejecutar sólo la operación necesaria. Para mutaciones, identificar primero el target en el mismo ambiente, fijar blast radius, declarar post-condición, ejecutar y verificar en ese mismo ambiente.

### 6. Tratar boundaries como evidencia

- capability ausente del inventario → revisar discovery/config/env del cliente antes de culpar al backend;
- `401` → diagnosticar bearer/config del cliente sin pedir ni imprimir el secreto upstream;
- `POLICY_DENIED` / permission denied → revisar el boundary del runbook, no crear bypass;
- timeout → reducir scope/optimizar antes de ampliar policy;
- una capability configurada pero sin tools expuestas no prueba fallo del servicio destino: primero aislar cliente/auth/handshake;
- en Hasura, `tools/list` server-side es evidencia de autoridad: no asumir que `--read-only` o el nombre del container hacen segura una capability PROD;
- `mcp_auth` visible en un cliente no cuenta como tool Hasura mientras no aparezca en `tools/list` server-side del backend.

## Output

```text
Environment: <PROD|DEV|runtime>
Capability: <aranea-*>
Authority: <viewer|operator|RO|RW|admin>
Target: <host/profile/database/collection/schema/metadata-object>
Operation: <acción ejecutada>
Evidence: <resultado material>
Mutation: <none | target + post-condition + same-environment verification>
Boundary: <none | policy/error relevante>
```

## Hard Rules

- Esta skill es **Aranea-only**; nunca usarla para MELI o sistemas corporativos.
- Elegir ambiente antes que capability/autoridad.
- PROD de datos/control plane es RO; DEV puede tener mayor autoridad sólo dentro de su capability explícita.
- Toda capability nueva debe respetar [[AGENT-PLATFORM - MCP Access Plane - Architecture]]: proxy bearer separado, backend interno sin host port, secretos upstream separados y pinning reproducible, salvo excepción explícitamente aprobada.
- `mcps` es appliance de servicios MCP Docker/Portainer, no workstation/jump host: no instalar clientes ad-hoc para administrar servicios destino.
- Nunca pedir, imprimir, copiar a documentación ni registrar bearer tokens, passwords, admin secrets o private keys.
- No saltar el proxy MCP ni usar acceso directo agent-first cuando existe capability canónica que cubre la acción.
- No cambiar ACLs/privilegios, publicar backends internos ni crear side channels como workaround automático.
- Hasura PROD no expone SQL ni mutación de metadata; cualquier tarea que los requiera debe detenerse o moverse al ambiente/flujo correcto, no ampliar la capability dinámicamente.
- Skills consumidoras deben referenciar esta skill en vez de duplicar endpoints, permisos o semántica MCP.
- No copiar esta skill a `80-agents/skills/` ni duplicar los runbooks fuera de `80-agents/memory/public/runbook/`.
