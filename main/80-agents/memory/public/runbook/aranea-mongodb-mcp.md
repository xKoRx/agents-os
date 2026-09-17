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

## Propósito

Operar MongoDB de Echo Forge mediante dos capabilities separadas por ambiente. La selección de ambiente/capability pertenece a [[aranea-mcps-expert]]; este runbook posee la mecánica y los hechos operativos de MongoDB MCP.

## Contrato de ambientes

| Capability | Endpoint | Ambiente | Authority |
|---|---|---|---|
| `aranea-mongo-forge-ro` | `http://mcps.lab.aranea.cl:3003/mcp` | PROD | read-only |
| `aranea-mongo-forge-rw` | `http://mcps.lab.aranea.cl:3004/mcp` | DEV | read/write |

El nombre exacto de las databases productiva/development no se infiere aquí si la capability no lo expone; usar el target preconfigurado y observarlo en runtime. Una lectura DEV usa `aranea-mongo-forge-rw` sin necesidad de mutar. No usar PROD RO para verificar una mutación DEV.

## Precondiciones

- El target es Aranea, no MELI/corporativo.
- Elegir ambiente antes de capability: PROD→RO, DEV→RW.
- Usar la conexión preconfigurada del servidor (`connectionId="preconfigured"` cuando la tool lo requiera); no abrir URIs arbitrarias con `connect` como workaround.
- No pedir, imprimir ni persistir credenciales/bearers.
- MongoDB es el evidence/result plane de Echo Forge; PostgreSQL sigue siendo el control plane relacional.
- Baseline de servidor documentado: MongoDB MCP Server `2.1.1`.

## Procedimiento

1. **Fijar ambiente.** Evidencia productiva → `aranea-mongo-forge-ro`. Lectura o mutación de desarrollo → `aranea-mongo-forge-rw`.
2. **Acotar lecturas.** Usar filtros/projections targeted, `limit` cuando corresponda, `count` para cardinalidad y aggregations acotadas. Correlacionar por identificadores estables de workflow/wave/run/strategy.
3. **Gate de mutación DEV.** Identificar documentos/colección exactos en DEV, fijar cardinalidad/blast radius y post-condición, ejecutar sólo la mutación requerida y verificar nuevamente en DEV. Para probes de acceso, usar documento/colección temporal identificable y eliminarlo al terminar.
4. **Boundary PROD.** La ausencia de mutadores en `aranea-mongo-forge-ro` es comportamiento esperado. No intentar writes en PROD para demostrar que son rechazados cuando la superficie/metadata ya acredita read-only.
5. **Autorización interna Mongo.** Si el endpoint DEV apunta a una instancia donde `security.authorization` está desactivada por diseño operacional, no habilitarla durante troubleshooting MCP. El control agent-facing sigue estando en bearer + separación RO/RW del plano MCP. No extrapolar esta condición a PROD sin evidencia runtime.
6. **Discovery antes de backend.** Si `aranea-mongo-forge-ro/rw` están declarados en el cliente pero no aparecen tools, no culpar a MongoDB: verificar primero env vars, reinicio del proceso cliente y handshake/auth del MCP.
7. **Enrutar fallos.** `401` → bearer/config cliente; capability ausente → [[aranea-mcp-capability-plane]]; mutador ausente en PROD RO → boundary esperado; error de transporte/`invalid request` → revisar protocolo/sesión antes de MongoDB; evidencia relacional/control → [[aranea-postgres-mcp]].
8. **Fallback humano.** `mongosh` puede usarse por un operador humano, pero no sustituye el MCP agent-first cuando la capability canónica cubre la acción.

## Discovery y secrets

En clientes Codex/CLI, las capabilities usan las variables `ARANEA_MONGO_FORGE_MCP_RO_BEARER` y `ARANEA_MONGO_FORGE_MCP_RW_BEARER`. Los nombres son documentación; los valores nunca se registran.

En `daedalus`, los archivos de secret del cliente están bajo `~/.config/aranea/secrets/ARANEA_MONGO_FORGE_MCP_RO_BEARER` y `~/.config/aranea/secrets/ARANEA_MONGO_FORGE_MCP_RW_BEARER`, con permisos `0600`; la shell los carga como variables de ambiente. Un proceso Codex ya iniciado no absorbe variables agregadas después: reiniciar/reabrir el cliente desde un environment que las haya cargado.

En host `mcps`, los bearer del proxy Mongo viven bajo `/opt/mcp/mongo-forge/runtime/proxy-secrets/`; documentar paths, jamás contenido. Los proxies observados son `mongo-forge-auth-ro` y `mongo-forge-auth-rw`.

**Estado 2026-09-11:** se confirmó que la ausencia inicial de tools Mongo en el cliente coincidía con ambas env vars `NOT_SET`; luego quedaron `SET` y persistidas en `daedalus`. La certificación funcional end-to-end posterior al restart del cliente queda pendiente de evidencia en esta fuente y no debe inventarse como PASS.

## Validación

```text
Environment:          PROD | DEV
Capability:           aranea-mongo-forge-ro | aranea-mongo-forge-rw
connectionId:         preconfigured (si aplica)
Authority match:      PASS
Target observed:      <database/collection runtime>
Mutation:             none | DEV target + cardinality + post-condition + DEV verification
Secrets exposed:      no
Discovery/auth:       PASS before backend diagnosis
```

## Rollback / recuperación

Si una capability desaparece del inventario, no publicar backends ni pedir bearer al usuario. Verificar config/env/restart/handshake y escalar a [[aranea-mcp-capability-plane]]. Si una mutación DEV deja un probe temporal, eliminarlo y comprobar ausencia. No cambiar autorización Mongo ni ACLs como bypass automático.

## Evidencia

Reportar ambiente, capability, `connectionId` si aplica, database/collections observadas, filtros/identificadores, resultado material, mutación/post-check y boundary de discovery/auth/policy si apareció.
