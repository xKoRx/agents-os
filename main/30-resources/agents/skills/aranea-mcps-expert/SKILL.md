---
type: skill
schema_version: 1
name: aranea-mcps-expert
description: Selecciona y gobierna el uso de las capabilities MCP del homelab Aranea. Cargar antes de usar cualquier MCP aranea-* para elegir capability, autoridad mínima y runbook correcto; nunca aplica a MELI ni a sistemas corporativos.
scope: area
created: "2026-09-11"
updated: "2026-09-11"
area: "[[Aranea]]"
entities:
  - "[[Aranea]]"
related:
  - "[[aranea-ssh-mcp]]"
  - "[[aranea-postgres-mcp]]"
  - "[[aranea-mongodb-mcp]]"
  - "[[aranea-mcp-capability-plane]]"
aliases:
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

Seleccionar **cómo acceder** a infraestructura y datos de Aranea mediante su capability plane MCP sin repartir credenciales finales ni elevar autoridad innecesariamente.

Activar antes de usar cualquier capability `aranea-*`, o cuando una skill de dominio determine que necesita acceso MCP a un host, PostgreSQL o MongoDB de Aranea.

No activar para trabajo local que no requiere MCP. **MUST NOT activate for Mercado Libre / MELI infrastructure, databases, repositories, hosts, credentials or corporate systems.**

Esta skill no vive en `80-agents/skills/`; ese catálogo es sólo core AGENTS OS. Los procedimientos mecánicos están en los runbooks enlazados.

## Minimal Read

Read only:

1. Esta skill para seleccionar capability y autoridad.
2. Después, sólo el runbook de la familia seleccionada:
   - [[aranea-ssh-mcp]]
   - [[aranea-postgres-mcp]]
   - [[aranea-mongodb-mcp]]
3. [[aranea-mcp-capability-plane]] sólo si el problema es el capability plane MCP mismo.

No cargar los tres runbooks por defecto.

## Procedure

### 1. Confirmar boundary Aranea

Si el target es MELI/corporativo, detener esta skill y usar la autoridad/herramientas corporativas correspondientes. No extrapolar endpoints, perfiles, policies ni secretos de Aranea.

### 2. Clasificar el recurso

| Necesidad | Capability default | Authority |
|---|---|---|
| runtime, logs, archivos u operación remota en workers Aranea | `aranea-ssh` | perfil viewer; operator sólo si la tarea exige mutación |
| PostgreSQL `echo-develop` | `aranea-postgres-ro` | read-only |
| mutación explícita en PostgreSQL `echo-develop` | `aranea-postgres-rw` | read/write |
| MongoDB `forge` evidence/result plane | `aranea-mongo-forge-ro` | read-only |
| mutación explícita en MongoDB `forge` | `aranea-mongo-forge-rw` | read/write |

Endpoints y detalles operativos viven en los runbooks; no inferirlos de memoria si el runbook está disponible.

### 3. Elegir autoridad mínima

Default: viewer/RO.

Cambiar a operator/RW sólo si la tarea requiere realmente una mutación. Complejidad, comodidad, volumen de resultados o una policy incómoda no justifican elevar autoridad.

### 4. Cargar el runbook de la familia

- host/runtime → [[aranea-ssh-mcp]]
- PostgreSQL → [[aranea-postgres-mcp]]
- MongoDB → [[aranea-mongodb-mcp]]

La skill de dominio decide **qué plano posee el hecho**; esta skill decide **cómo acceder**. No redefinir ownership de dominio aquí.

### 5. Acotar y ejecutar

Antes de invocar el MCP, fijar el target mínimo: perfil/host, database/schema/table o database/collection/identificador.

Ejecutar sólo la operación necesaria para responder la pregunta actual. Si aparece necesidad de otro backend/host, exigir una pregunta concreta derivada de la evidencia previa.

### 6. Gate de mutación

Antes de una mutación:

1. demostrar el target con viewer/RO cuando sea posible;
2. fijar cardinalidad/blast radius;
3. declarar post-condición esperada;
4. usar la capability writable más estrecha;
5. verificar después con viewer/RO cuando sea posible.

### 7. Tratar boundaries como evidencia

- `401` → diagnosticar auth/config del cliente; no pedir el bearer al usuario.
- `POLICY_DENIED` / permission denied → revisar el boundary del runbook; no crear bypass automático.
- timeout → reducir scope/optimizar antes de ampliar policy.

## Output

```text
Capability: <aranea-*>
Authority: <viewer|operator|RO|RW>
Target: <host/profile/database/collection/schema>
Operation: <acción ejecutada>
Evidence: <resultado material>
Mutation: <none | target + post-condition + verification>
Boundary: <none | policy/error relevante>
```

## Hard Rules

- Esta skill es **Aranea-only**; nunca usarla para MELI o sistemas corporativos.
- Antes de usar `aranea-*`, cargar esta skill y el runbook de la familia seleccionada.
- Default viewer/RO; no elevar por comodidad.
- Nunca pedir, imprimir, copiar, persistir ni registrar bearer tokens, passwords o private keys.
- No saltar el proxy MCP ni usar acceso directo agent-first cuando existe capability canónica que cubre la acción.
- No cambiar ACLs/privilegios, publicar backends internos ni crear side channels como workaround automático.
- Que una tool exista no amplía la autoridad declarada por el runbook; por ejemplo, MongoDB `connect` no autoriza URIs arbitrarias.
- Skills consumidoras deben referenciar esta skill en vez de duplicar endpoints, permisos o semántica MCP.
- No copiar esta skill a `80-agents/skills/` ni duplicar los runbooks fuera de `80-agents/memory/public/runbook/`.
