---
type: feedback
scope: session
created: 2026-09-14
updated: 2026-09-14
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
entities:
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
  - "[[aranea-mcps-expert]]"
related:
  - "[[ACCESS-CERTIFICATION]]"
aliases: []
agent: ZCode
session_goal: Certificar físicamente los accesos del MCP Access Plane por ambiente, con negatives seguros y cleanup verificado.
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - area/aranea
  - tech/mcp
---

# Session Feedback - 2026-09-14 - MCP access certification

## Friction

- **Boundary viewer SSH no aplicado (HIGH):** `run-command` ejecutó un comando en el perfil `mt5-kronos` con rol `viewer`, contradiciendo la certificación 2026-09-13 ("rechazado por diseño"). El rol reportado por `list-connections` no es evidencia de enforcement; requiere inspección server-side con autoridad admin de `mcps`.
- **`export_metadata` Hasura expone credenciales (HIGH):** la capability PROD-RO entrega `database_url` con password embebido de ambos sources al cliente MCP. La frontera "RO = seguro para agentes" no se sostiene mientras el metadata incluya secretos.
- **`delete_topic` Kafka eventual y no persistente (MEDIUM):** la respuesta de éxito no garantiza eliminación. El residual del smoke 2026-09-13 acumuló 4 deletes exitosos en esta run, llegó a `partitions=[]` y reapareció con líder rotando (1→5→2→6) — sugiere re-creación por un cliente externo que aún lo referencia. Las certificaciones que usan topics efímeros necesitan post-condición de ausencia en `list_topics`, no el exit del delete.
- **`get_schema` Hasura PROD derriba el transporte (MEDIUM):** dos intentos terminaron en "Connection closed"/server desconectado; probable timeout/tamaño de introspección en proxy o backend.
- **`read-command` allowlist demasiado estricta (LOW):** rechaza compuestos (`&&`) y `docker ps --format '{{…}}'`; empuja lecturas inofensivas hacia `run-command`, justo cuando el boundary viewer está en duda.

## What worked

- Doble capa de enforcement en Postgres (validador MCP + grants reales) dió negatives limpios sin riesgo.
- El patrón mutación-DEV-con-cleanup (topic Mongo/Kafka creados y eliminados con verificación) funcionó como evidencia de autoridad sin dejar residuos una vez aplicada la post-condición.

## Suggestion

- T6 debería incluir: verificación de enforcement viewer (no sólo etiqueta de rol), redaction de credenciales en `export_metadata`, semántica delete documentada y smoke de `get_schema` con presupuesto de respuesta.
