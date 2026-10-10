---
type: change_log
schema_version: 1
scope: session
created: "2026-10-08"
updated: "2026-10-09"
area: "[[Meli]]"
project: "[[RIO E2E local]]"
application:
entities: ["[[RIO E2E local]]"]
related: ["[[Kafka — Ambiente local con servicios reales]]"]
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-08-rio-e2e-local-created

## Cambio

- **Tipo:** created.
- **Archivos:** [[RIO E2E local]] y [[Prompt — Challenge del diseño RIO E2E local]].

## Motivo

Owner pide un proyecto AGENTS OS nuevo y prompt de challenge para mejorar el diseño antes de implementar: cinco apps (PM/front/CP Kafka/CH/Flink), native Kafka producers/consumers, sin bridge; tocar producción lo mínimo; Clean/SOLID/KISS/YAGNI; crecimiento posterior.

## Fuentes usadas

- Solicitud explícita del owner, conversación actual y propuesta LOCAL-KAFKA-1 de [[Kafka — Ambiente local con servicios reales]].
- Identidades locales de seis repos candidatos, consultadas por git read-only; el runtime inicial tendrá sólo un front. SHAs/status observados sin fetch.
- [[rio-frontend]] identifica legacy/deprecación y [[ads-signals-frontend]] como reemplazo: selección pendiente de verificar.
- Templates canónicos project/prompt/change_log materializados por el script del contrato. Bootstrap warm reutilizado, swap de entidad y dominio Meli.

## Resolución aplicada

- Nuevo proyecto raíz owner me, activo, progreso0, cinco filas de entrega con referencias/bases observadas y ramas pendientes; SPEC funcional/técnica borrador y tareas de diseño.
- Prompt autocontenido distingue requisitos del owner de hipótesis; exige evidencia/seams por app, ACK/offsets/grupos, límites conocidos, motores reales y front/browser; no autoriza implementación.
- Proyecto Kafka anterior conserva pruebas y ramas. No se hicieron cambios de código, fetch, ramas, Docker o VM. Sesión sin cierre.

## Validación

- Duplicate search por fuentes y Graphify título/alias:0 candidatos antes de crear.
- Materializer project/prompt/change_log PASS; lint strict del delta3 notas PASS,0ERROR/0WARN. Graphify título `RIO E2E local.md` y alias `rio-e2e-local` devuelven1 mismo archivo canónico después del auto-refresh; índice fuera del vault. Apertura del prompt en Codex solicitada, estado queued.
- Primera consulta sandbox Graphify no pudo escribir cache; rerun escalado autorizado actualizó el índice local. Auto-refresh reportó deuda global369ERROR/288WARN y continuó; no se modificaron notas ajenas ni skills de otras superficies. Cache fuera del vault.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin secretos; contiene referencias a repos corporativos y rutas locales, no exportar automáticamente.

## Rollback

Eliminar sólo los dos documentos recién creados y este log si el owner revoca la creación; nunca retirar evidencias/repos/recursos del proyecto Kafka anterior. Reindexar el cache derivado mediante consulta auto-refresh.
