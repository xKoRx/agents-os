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
  - "[[aranea-postgres-mcp]]"
aliases:
  - runbook MongoDB MCP Aranea
  - aranea-mongo
  - mcp mongo
  - aranea-mongo-forge
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
  - tech/mongodb
  - action/mcp-mongo
---

# aranea-mongodb-mcp

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

Inspeccionar y, cuando esté explícitamente autorizado, mutar MongoDB a través del capability plane MCP de Aranea. Este runbook posee hechos operativos de MongoDB MCP. La selección de capability y autoridad mínima pertenece a [[aranea-mcps-expert]]. Las skills de dominio deciden cuándo MongoDB es la fuente correcta.

## Precondiciones

- El target es infraestructura Aranea; si es MELI/corporativo, abortar y no usar este runbook.
- `aranea-mcps-expert` ya eligió `aranea-mongo-forge-ro` o, con mutación explícita, `aranea-mongo-forge-rw`.
- La capability elegida aparece conectada en el cliente.
- `VAULT_ROOT` resuelve el marker `80-agents/agents-os/agents-os.md`.
- El agente no pide, imprime, copia ni persiste credenciales MongoDB ni valores bearer.
- MongoDB es el **evidence/result plane** de la Durable Foundation: salidas de ejecución y evidencia como matrices/runs WFM, evidencia de export/import y otros documentos Forge/SQX. No usar PostgreSQL como sustituto de este plano.
- Baseline validado: MongoDB MCP Server `2.1.1`.

## Procedimiento

1. **Usar la conexión preconfigurada.** El server está preconfigurado para el path Forge. Usar `connectionId = "preconfigured"`. No llamar la tool MCP `connect` para abrir una URI MongoDB arbitraria salvo que el usuario pida explícitamente otra conexión y autorice ese scope. Aunque `connect` sea visible incluso en RO, eso no convierte conexiones arbitrarias en autoridad normal de troubleshooting.

| Capability | Endpoint | Authority | Scope |
|---|---|---|---|
| `aranea-mongo-forge-ro` | `http://mcps.lab.aranea.cl:3003/mcp` | read-only | MongoDB `forge` |
| `aranea-mongo-forge-rw` | `http://mcps.lab.aranea.cl:3004/mcp` | read/write | MongoDB `forge` |

2. **Partir en RO.** `aranea-mongo-forge-ro` es el default. Su superficie validada excluye mutadores: `insert-many`, `update-many`, `delete-many`, `create-collection`, `create-index`, `drop-collection`, `drop-database`, `drop-index`, `rename-collection`. Usar RO para discovery, `find`, `count`, inspección de schema/índices, aggregations acotadas y correlación de evidencia.
3. **Acotar lecturas.** Usar filtros y projections targeted; fijar `limit` en `find` cuando no se requiera el set completo; acotar aggregations con stages selectivos y `$limit` cuando sea semánticamente válido; preferir `count` si sólo se necesita cardinalidad; no exportar ni devolver result sets grandes sin necesidad clara; correlacionar por identificadores de workflow/wave/run/strategy en vez de recorrer colecciones a lo ancho. Colecciones WFM habituales: `wfm_matrices`, `wfm_runs`, `export_runs`. Tratar esos nombres como detalle del evidence plane, no como permiso para dumpear colecciones enteras.
4. **Gate de mutación RW.** `aranea-mongo-forge-rw` expone los mutadores anteriores además de lecturas. Usarlo sólo cuando el troubleshooting/remediación necesite realmente una mutación. Antes de update/delete/drop/rename: identificar documentos/colección exactos con RO; registrar identificadores estables y cardinalidad esperada; mantener blast radius mínimo; ejecutar sólo la mutación autorizada; verificar la post-condición con RO; borrar cualquier documento/colección temporal creado sólo para validar. `drop-database`, `drop-collection`, operaciones destructivas de índices y `delete-many` amplios nunca quedan implícitos en un permiso genérico de troubleshooting.
5. **No endurecer autorización del server Mongo como parte del diagnóstico.** En desarrollo, `security.authorization` está deliberadamente desactivada mientras Forge sigue activo. No habilitarla como parte de troubleshooting: los workers Symphony/SQX dependen de esa postura de desarrollo y cambiarla es una migración de hardening productiva aparte. Los endpoints MCP siguen protegidos por bearer y separados en RO/RW.
6. **Enrutar fallos sin bypass.** `401` → problema de bearer/config del cliente; no pedir que el usuario pegue el bearer. `invalid request` en smoke HTTP manual → verificar handshake/session headers y `Accept` antes de culpar a MongoDB. Tool mutadora ausente en RO → boundary esperado; pasar a RW sólo si la mutación es explícitamente requerida. Evidencia ausente en Mongo → decidir si es resultado descartado/faltante legítimo, import/export incompleto o identificador incorrecto antes de mutar. Necesidad de estado relacional/control → ir a [[aranea-postgres-mcp]] en vez de buscar en Mongo a ciegas.
7. **Reservar `mongosh` nativo como fallback humano.** `mongosh` sigue válido para un operador humano, pero no es el camino default del agente mientras existan `aranea-mongo-forge-ro/rw`. No reemplazar un diagnóstico MCP por acceso directo de red sólo porque sea más fácil.
8. **Smoke de transporte sólo si el plano MCP es el sospechoso.** Path externo esperado: `/mcp` a través del proxy autenticado. En un smoke HTTP manual: un request sin auth debe devolver `401`; `initialize` debe devolver `200` y un `mcp-session-id`; los clientes deben enviar `Accept: application/json, text/event-stream`; usar la sesión emitida en llamadas posteriores; el backend desplegado está configurado para respuestas JSON HTTP para mantener el smoke finito. No exponer puertos de contenedor backend para saltarse problemas de proxy/cliente. Si el problema es el plano MCP mismo, handoff a [[aranea-mcp-capability-plane]].

## Validación

Success requiere:

```text
Capability:          aranea-mongo-forge-ro | aranea-mongo-forge-rw
connectionId:        preconfigured
Authority match:     PASS
Scope:               forge + collections/identificadores acotados
Mutation:            none | target + cardinality + post-condition + RO verification
Boundary:            none | 401/RO-missing-mutator/transport registrado sin bypass
Secrets:             none persisted
Authorization:       security.authorization no alterada
```

Checklist:

- [ ] El target es Aranea y no MELI/corporativo.
- [ ] Se usó `connectionId="preconfigured"` salvo otra conexión explícitamente autorizada.
- [ ] Se partió en RO, o RW quedó justificado por una mutación explícita.
- [ ] No se usó MongoDB para estado relacional/control que pertenece a PostgreSQL.
- [ ] No se habilitó `security.authorization` como workaround.
- [ ] No se pidieron, imprimieron ni persistieron credenciales/bearers.

Cualquier URI arbitraria no autorizada, drop amplio o persistencia de secreto deja la operación `ABORTED`.

## Rollback / recuperación

Abortar sin mutar cuando:

- la capability RO/RW requerida no está conectada;
- la tool mutadora falta en RO y no hay autorización RW;
- el único workaround sería publicar backends, llamar `connect` a una URI arbitraria o pedir el bearer;
- el hecho pertenece a otro plano.

Ante fallo:

1. conservar `connectionId`, colección, filtros e identificadores;
2. no rotar ni pedir secretos salvo evidencia de que la rotación es necesaria;
3. no degradar a `mongosh` agent-first si la capability canónica cubre la acción;
4. revertir documentos/colecciones temporales creados sólo para validar;
5. si el problema es el plano MCP mismo, handoff a [[aranea-mcp-capability-plane]].

## Evidencia

Reportar:

- capability RO o RW usada;
- `connectionId` usado (`preconfigured` esperado);
- database/collections inspeccionadas;
- filtros/identificadores usados;
- resultado material;
- mutación, si hubo;
- verificación de post-condición;
- boundary de policy/transporte si apareció.
