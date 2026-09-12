---
type: runbook
schema_version: 1
scope: area
created: "2026-09-11"
updated: "2026-09-11"
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
application:
entities:
  - "[[Aranea]]"
  - "[[Echo Forge]]"
related:
  - "[[aranea-mcps-expert]]"
  - "[[aranea-mcp-capability-plane]]"
  - "[[aranea-ssh-mcp]]"
  - "[[aranea-mongodb-mcp]]"
aliases:
  - runbook PostgreSQL MCP Aranea
  - aranea-postgres
  - mcp postgres
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/area
  - area/aranea
  - tech/mcp
  - tech/postgresql
  - action/mcp-postgres
---

# aranea-postgres-mcp

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

Inspeccionar y, cuando esté explícitamente autorizado, mutar PostgreSQL a través del capability plane MCP de Aranea. Este runbook posee hechos operativos de PostgreSQL MCP. La selección de capability y autoridad mínima pertenece a [[aranea-mcps-expert]]. Las skills de dominio deciden cuándo PostgreSQL es la fuente correcta. El contrato detallado de acceso Echo dev vive en `xKoRx/symphony` → `docs/prd/echo-forge/POSTGRES-MCP-ACCESS.md`.

## Precondiciones

- El target es infraestructura Aranea; si es MELI/corporativo, abortar y no usar este runbook.
- `aranea-mcps-expert` ya eligió `aranea-postgres-ro` o, con mutación explícita, `aranea-postgres-rw`.
- La capability elegida aparece conectada en el cliente.
- `VAULT_ROOT` resuelve el marker `80-agents/agents-os/agents-os.md`.
- El agente no pide, imprime, copia ni persiste credenciales PostgreSQL ni valores bearer.
- PostgreSQL es el **control plane** de la Durable Foundation: estado relacional de workflow/dominio, lifecycle/control y metadata relacional durable. No sustituye evidencia/resultados de MongoDB ni artefactos de MinIO.

## Procedimiento

1. **Partir siempre en RO.** Usar `aranea-postgres-ro` para descubrir el conjunto relacional mínimo que responde la pregunta. Preferir columnas, predicados, counts y agregados acotados frente a dumps amplios. Usar `LIMIT` en exploraciones cuando no cambie la semántica pedida. Correlacionar con identificadores estables de workflow/run/strategy al cruzar planos.

| Capability | Endpoint | Authority | Scope |
|---|---|---|---|
| `aranea-postgres-ro` | `http://mcps.lab.aranea.cl:3001/mcp` | read-only | `echo-develop` |
| `aranea-postgres-rw` | `http://mcps.lab.aranea.cl:3002/mcp` | read/write | `echo-develop` |

2. **Aplicar guards de query.** Preferir `EXPLAIN` sobre `EXPLAIN ANALYZE` en diagnóstico, salvo que la ejecución real esté intencionada y sea segura. No usar `EXPLAIN ANALYZE` como dry-run de DML destructivo. Respetar los timeouts de rol/database del contrato canónico; no deshabilitarlos ni subirlos automáticamente. Si una query hace timeout, reducir scope u optimizarla antes de proponer cambios de policy. El upstream no tiene guard genérico de filas para `execute_sql`; mantener resultados exploratorios acotados cuando la semántica lo permita.
3. **No inferir éxito por `isError`.** El upstream validado puede devolver un rechazo de policy/query como texto mientras el envelope MCP reporta `isError=false`. Tratar `Error validating query`, `permission denied`, timeout textual o contenido de error equivalente como fallo.
4. **Gate de mutación.** RW no se justifica por complejidad de query. Antes de `INSERT`, `UPDATE` o `DELETE`: la mutación debe ser explícita; identificar primero filas/keys exactas con RO; mantener blast radius mínimo; no ejecutar DDL destructivo salvo pedido/autorización explícitos; registrar la mutación y la evidencia de post-check. Después de mutar, verificar la post-condición con RO cuando sea posible.
5. **Enrutar fallos sin bypass.** `401` → problema de bearer/entorno del cliente; no pedir que el usuario pegue el bearer en el chat. Permission denied en RO → boundary esperado hasta demostrar misconfiguración. Mutación requerida pero RW no disponible → detener y reportar la capability faltante. Timeout → estrechar/optimizar primero. El hecho buscado es evidencia/resultado → ir a [[aranea-mongodb-mcp]] en vez de ampliar PostgreSQL a ciegas.
6. **Reservar `psql` nativo como fallback humano.** `psql` sigue válido para un operador humano, pero no es el camino default del agente mientras existan las capabilities MCP.

## Validación

Success requiere:

```text
Capability:          aranea-postgres-ro | aranea-postgres-rw
Authority match:     PASS
Scope:               echo-develop
Query:               predicados/keys acotados
isError caveat:      contenido de error tratado como fallo
Mutation:            none | target + post-condition + RO verification
Boundary:            none | 401/permission/timeout registrado sin bypass
Secrets:             none persisted
```

Checklist:

- [ ] El target es Aranea y no MELI/corporativo.
- [ ] Se partió en RO, o RW quedó justificado por una mutación explícita.
- [ ] No se usó PostgreSQL para evidencia/resultados que pertenecen a MongoDB.
- [ ] No se interpretó `isError=false` como éxito si el contenido indica error.
- [ ] Timeouts y denegaciones se trataron como boundary, no como licencia para ampliar policy.
- [ ] No se pidieron, imprimieron ni persistieron credenciales/bearers.

Cualquier bypass del proxy, DDL no autorizado o persistencia de secreto deja la operación `ABORTED`.

## Rollback / recuperación

Abortar sin mutar cuando:

- la capability RO/RW requerida no está conectada;
- el rechazo es de policy y no hay autorización RW;
- el único workaround sería publicar backends, desactivar timeouts o pedir el bearer;
- el hecho pertenece a otro plano.

Ante fallo:

1. conservar query, predicados y el texto de error;
2. no rotar ni pedir secretos salvo evidencia de que la rotación es necesaria;
3. no degradar a `psql` agent-first si la capability canónica cubre la acción;
4. si el problema es el plano MCP mismo, handoff a [[aranea-mcp-capability-plane]].

## Evidencia

Reportar:

- capability RO o RW usada;
- database/scope;
- propósito de la query y predicados/keys relevantes;
- resultado material;
- mutación, si hubo;
- verificación de post-condición;
- timeout o boundary de policy si apareció.
