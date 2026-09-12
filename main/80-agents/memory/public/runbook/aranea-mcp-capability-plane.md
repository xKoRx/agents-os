---
type: runbook
schema_version: 1
scope: area
created: "2026-09-11"
updated: "2026-09-12"
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

Validar y diagnosticar el capability plane MCP de Aranea cuando el fallo está en discovery, configuración del cliente, environment, auth, proxy, transporte o policy, antes de culpar al backend de datos. El routing agent-facing vive en [[aranea-mcps-expert]], la arquitectura común en [[AGENT-PLATFORM - MCP Access Plane - Architecture]] y la mecánica de cada familia en [[aranea-ssh-mcp]], [[aranea-postgres-mcp]] y [[aranea-mongodb-mcp]].

## Estado normal

Un cliente Aranea correctamente iniciado debe poder descubrir las capabilities configuradas: `aranea-ssh`, `aranea-postgres-ro`, `aranea-postgres-rw`, `aranea-mongo-forge-ro` y `aranea-mongo-forge-rw`. La mera presencia de un bloque en `config.toml` no demuestra que la capability esté conectada: el proceso cliente también debe heredar las env vars requeridas y completar el handshake MCP.

Para cualquier capability nueva o reinstalada, el estado normal de deployment es el definido en [[AGENT-PLATFORM - MCP Access Plane - Architecture]]: proxy bearer publicado, backend MCP interno sin host port y credencial upstream separada del bearer del cliente.

## Procedimiento

1. **Inventariar antes de probar backend.** Listar capabilities/tools realmente expuestas por el cliente. Si una capability esperada no aparece, clasificar primero como `MCP discovery/client`.
2. **Verificar configuración sin secretos.** Confirmar URL, nombre de la env var y policy de aprobación esperada; nunca imprimir el valor bearer. Para Mongo Forge, los nombres vigentes son `ARANEA_MONGO_FORGE_MCP_RO_BEARER` y `ARANEA_MONGO_FORGE_MCP_RW_BEARER`.
3. **Verificar environment del proceso.** Comprobar sólo `SET/NOT_SET`. Una env var presente en una shell no implica que un proceso ya iniciado la haya heredado. Si se agregó después, cerrar/reabrir el cliente desde un environment correcto.
4. **Distinguir configured vs exposed.** Si el bloque MCP existe pero no hay tools, no probar Mongo/PostgreSQL por acceso directo como sustituto: aislar env/auth/handshake primero.
5. **Enrutar `401`.** Tratarlo como bearer/config del cliente o boundary del proxy autenticado. No rotar ni pedir secretos sin evidencia de necesidad.
6. **Enrutar `POLICY_DENIED` / permission denied.** Tratarlo como boundary de autoridad. En SSH viewer, `run-command` puede estar denegado por diseño; usar operator sólo cuando la operación realmente requiere ejecución/escritura. En data MCPs, respetar PROD=RO y DEV=RW según [[aranea-mcps-expert]].
7. **Enrutar `invalid request` / HTTP 400.** Un `GET /mcp` manual puede ser inválido para Streamable HTTP y no prueba caída del backend. Validar handshake/sesión/headers del protocolo o hacer una llamada MCP real antes de diagnosticar el servicio.
8. **Enrutar timeout.** Estrechar query/comando/filtro antes de ampliar policy. Delegar a runbook de familia cuando discovery/auth/transporte ya estén descartados.
9. **Disciplina de cambio.** Al agregar, reemplazar o reinstalar una capability: cargar primero [[AGENT-PLATFORM - MCP Access Plane - Architecture]], reutilizar su blueprint y actualizar [[aranea-mcps-expert]], el runbook de familia y la documentación estable de Aranea. No introducir otra topología sin evidencia material y decisión explícita. Nunca persistir bearer/password/private-key.
10. **Drift check mínimo.** No repetir la auditoría completa del host. Si se sospecha drift, comparar primero `docker ps`, redes y binds con el baseline de arquitectura; inspeccionar mounts/commands sólo si la diferencia material lo exige.

## Caso conocido — Mongo Forge 2026-09-11

`aranea-mongo-forge-ro/rw` estaban correctamente declarados en el cliente pero no aparecían en el inventario. Se comprobó que `ARANEA_MONGO_FORGE_MCP_RO_BEARER` y `ARANEA_MONGO_FORGE_MCP_RW_BEARER` estaban `NOT_SET`. Los bearer ya existían en los proxies del host `mcps`; se instalaron como archivos `0600` en `daedalus`, se cargaron persistentemente como env vars y ambas quedaron `SET`. La lección operacional es diagnosticar discovery/env antes de atribuir este síntoma a MongoDB.

## Validación

```text
Plane symptom:       missing|401|POLICY_DENIED|timeout|invalid request
Config present:      yes|no
Required env:        SET|NOT_SET (value never shown)
Capability exposed:  yes|no
Client vs backend:   distinguished
Architecture drift:  none|material
Family runbook:      loaded only after plane/auth is scoped
Bypass:              none
Secrets persisted in docs: no
```

## Rollback / recuperación

No publicar backends, no abrir nuevos puertos y no pedir secretos como workaround. Si una modificación de config/env empeora discovery, restaurar la configuración anterior y reiniciar el cliente; el backend se toca sólo con evidencia que lo incrimine.

## Evidencia

Registrar capability afectada, estado de discovery, nombres de env vars sin valores, boundary cliente/proxy/backend, drift respecto de [[AGENT-PLATFORM - MCP Access Plane - Architecture]], acción correctiva y resultado material.
