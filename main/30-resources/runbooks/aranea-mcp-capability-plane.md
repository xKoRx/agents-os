---
type: runbook
schema_version: 1
scope: area
created: "2026-09-11"
updated: "2026-09-13"
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
application:
entities:
  - "[[Aranea]]"
related:
  - "[[AGENT-PLATFORM - MCP Access Plane - Architecture]]"
  - "[[aranea-mcps-expert]]"
  - "[[aranea-ssh-mcp]]"
  - "[[aranea-postgres-mcp]]"
  - "[[aranea-mongodb-mcp]]"
  - "[[aranea-hasura-mcp]]"
  - "[[aranea-kafka-mcp]]"
aliases:
  - runbook capability plane MCP Aranea
  - aranea mcp plane
  - troubleshooting MCP Aranea
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
  - action/mcp-plane
---

# aranea-mcp-capability-plane

## Propósito

Validar y diagnosticar el capability plane MCP de Aranea cuando el fallo está en discovery, configuración del cliente, environment, auth, proxy, transporte o policy, antes de culpar al backend de datos/servicio. El routing agent-facing vive en [[aranea-mcps-expert]], la arquitectura común en [[AGENT-PLATFORM - MCP Access Plane - Architecture]] y la mecánica de cada familia en sus runbooks.

## Estado normal

Capabilities actualmente certificadas/esperadas por familia:

```text
aranea-ssh
aranea-postgres-ro
aranea-postgres-rw
aranea-mongo-forge-ro
aranea-mongo-forge-rw
aranea-hasura-prod-ro
aranea-hasura-dev-admin
aranea-kafka-dev-admin
```

Endpoints certificados adicionales:

```text
Hasura PROD RO   http://mcps.lab.aranea.cl:3005/mcp
Hasura DEV admin http://mcps.lab.aranea.cl:3006/mcp
Kafka DEV admin  http://mcps.lab.aranea.cl:3007/mcp
```

La mera presencia de un bloque en config no demuestra que la capability esté conectada: el proceso cliente también debe heredar las env vars requeridas y completar handshake MCP.

Para cualquier capability nueva o reinstalada, el deployment normal es el definido en [[AGENT-PLATFORM - MCP Access Plane - Architecture]]: proxy bearer publicado, backend MCP interno sin host port y credencial upstream separada del bearer del cliente cuando el servicio destino la requiera.

## Procedimiento

1. **Inventariar antes de probar backend.** Listar capabilities/tools realmente expuestas por el cliente. Si una capability esperada no aparece, clasificar primero como `MCP discovery/client`.
2. **Verificar configuración sin secretos.** Confirmar URL, nombre de env var y policy esperada; nunca imprimir el bearer.
3. **Verificar environment del proceso.** Comprobar sólo `SET/NOT_SET`. Una env presente en una shell no implica que un proceso ya iniciado la haya heredado.
4. **Distinguir configured vs exposed.** Si el bloque MCP existe pero no hay tools, no saltar al servicio destino por acceso directo como sustituto: aislar env/auth/handshake primero.
5. **Enrutar `401`.** Tratarlo como bearer/config del cliente o boundary del proxy autenticado. No rotar ni pedir secretos upstream sin evidencia.
6. **Enrutar policy/permission denied.** Respetar autoridad de [[aranea-mcps-expert]] y runbook de familia; no crear bypass.
7. **Enrutar `invalid request` / HTTP 400/406.** Un `GET /mcp` manual puede ser inválido para Streamable HTTP y no prueba caída del backend. Validar `initialize`, sesión y headers o hacer llamada MCP real.
8. **Enrutar timeout.** Estrechar query/comando/filtro antes de ampliar policy.
9. **Disciplina de cambio.** Al agregar/reemplazar/reinstalar capability: cargar [[AGENT-PLATFORM - MCP Access Plane - Architecture]], reutilizar blueprint y actualizar skill + runbook de familia. No introducir otra topología sin evidencia material.
10. **Drift check mínimo.** No repetir auditoría completa. Comparar primero containers/red/binds; inspeccionar mounts/commands sólo si el drift material lo exige.
11. **Hasura authority check.** Para Hasura, `tools/list` server-side forma parte de la certificación de autoridad. No aceptar `--read-only`, nombre del container o README como prueba suficiente de PROD RO.
12. **Kafka authority check.** Para Kafka DEV, `tools/list` debe exponer la superficie administrativa certificada y `alter_configs` debe conservar semántica incremental. Si una config no objetivo cambia, detener mutaciones y tratar la capability como fuera de contrato.
13. **Distinguir tool backend vs helper cliente.** Una entrada como `mcp_auth` reportada por Cursor no amplía el authority boundary si no aparece en `tools/list` server-side del MCP correspondiente.

## Casos conocidos

### Mongo Forge — 2026-09-11

Capabilities declaradas pero ausentes del inventario resultaron ser env vars bearer `NOT_SET` en Daedalus. Lección: diagnosticar discovery/env antes de culpar a MongoDB.

### Hasura DEV — 2026-09-12

`aranea-hasura-dev-admin` fue certificado por capas:

```text
unauthenticated :3006/mcp -> 401
authenticated initialize -> 200 + session id
tools/list -> 9 tools admin
Daedalus -> endpoint -> 200
Cursor -> get_version/get_inconsistent_metadata -> PASS
```

El Hasura admin secret nunca fue entregado al cliente; queda server-side en `mcps`.

### Hasura PROD RO — 2026-09-12

El upstream `--read-only` conservaba `reload_metadata` y `run_sql`, por lo que no se aceptó como boundary suficiente. Se construyó una variante strict-RO que elimina ambas tools y mantiene `--read-only` para no registrar mutadores de metadata.

Certificación:

```text
unauthenticated :3005/mcp -> 401
authenticated initialize -> 200 + session id
tools/list server-side -> exactamente 4 tools
  export_metadata
  get_inconsistent_metadata
  get_schema
  get_version
backend host port -> none
Cursor -> get_version/get_inconsistent_metadata -> PASS
metadata -> consistent
```

Cursor además mostró `mcp_auth`, pero esa entrada no apareció en `tools/list` server-side y no se considera tool Hasura ni ampliación del authority boundary.

### Kafka DEV admin — 2026-09-13

`aranea-kafka-dev-admin` quedó certificado por capas:

```text
unauthenticated :3007/mcp -> 401
authenticated tools/list -> exactamente 19 tools
backend host port -> none
Cursor -> describe_cluster/list_topics -> PASS
cluster_id -> Eiuq4GsaTXOUPif-rLU-6Q
brokers -> 6
topics baseline -> 117
```

Golden admin smoke sobre recursos `mcp-cert-*`:

```text
create topic -> PASS
alter retention.ms incremental -> PASS / configs ajenas intactas
increase partitions -> PASS
produce + consume marker -> PASS
consumer group describe/offsets/reset -> PASS
delete temp topic -> PASS
```

El backend upstream fue patchado para usar `incremental_alter_configs`; el `alter_configs` legacy podía revertir a defaults propiedades no incluidas. Ver [[aranea-kafka-mcp]] para la autoridad técnica y referencias oficiales.

Daedalus carga `ARANEA_KAFKA_MCP_DEV_ADMIN_BEARER` mediante el mismo chain KDE usado por el resto de capabilities (`~/.config/plasma-workspace/env/aranea-mcp.sh` → `~/.config/mcp/aranea-env.sh`). Un proceso Cursor ya iniciado no absorbe automáticamente una variable agregada a mitad de sesión.

## Validación

```text
Plane symptom:       missing|401|POLICY_DENIED|timeout|invalid request
Config present:      yes|no
Required env:        SET|NOT_SET (value never shown)
Capability exposed:  yes|no
Client vs backend:   distinguished
Architecture drift:  none|material
Tool surface:        expected exact set|unexpected
Family runbook:      loaded only after plane/auth is scoped
Bypass:              none
Secrets persisted in docs: no
```

## Rollback / recuperación

No publicar backends, no abrir nuevos puertos y no pedir secretos como workaround. Si una modificación de config/env empeora discovery, restaurar configuración anterior y reiniciar cliente; tocar backend sólo con evidencia que lo incrimine.

Para Hasura PROD, si un upgrade vuelve a exponer `run_sql`, `reload_metadata` o cualquier mutador, considerar la capability fuera de contrato y restaurar el artefacto strict-RO certificado antes de continuar.

Para Kafka DEV, si un rebuild cambia versiones pinneadas, pierde el patch incremental o `tools/list` deja de coincidir con la superficie certificada, restaurar `local/kafka-mcp:2.0.0-0b3bf47-inc1-fm3.0.1` y no ejecutar mutaciones hasta recertificar.

## Evidencia

Registrar capability afectada, estado de discovery, nombres de env vars sin valores, boundary cliente/proxy/backend, tool surface server-side cuando aplique, drift respecto de arquitectura, acción correctiva y resultado material.
