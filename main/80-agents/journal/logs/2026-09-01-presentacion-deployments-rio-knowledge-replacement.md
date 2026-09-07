---
type: change_log
schema_version: 1
scope: session
created: "2026-09-01"
updated: "2026-09-01"
area: "[[Meli]]"
project: "[[Presentación deployments en RIO]]"
application:
entities:
  - "[[RIO]]"
related:
  - "[[ads-signals-knowledge-library]]"
  - "[[Deployments en RIO — flujo completo]]"
  - "[[Revisión de ads-signals-knowledge-library]]"
aliases:
  - change log presentación deployments RIO
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

# 2026-09-01-presentacion-deployments-rio-knowledge-replacement

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated + conflict-resolution
- **Archivo(s):**
  - `10-projects/Meli/Presentación deployments en RIO/` — proyecto y dos documentos técnicos.
  - `30-resources/knowledges/` — nueva resource/source, lifecycle de la anterior, índice y log.
  - [[RIO]], [[Signals Knowledge Harness]] y [[Onboarding Signals]] — referencias y hechos vigentes reconciliados.

## Motivo

- Preparar la presentación del 2026-09-02 con una explicación verificable del deployment flow y reemplazar la knowledge anterior por `ads-signals-knowledge-library` sin perder provenance histórica.

## Fuentes usadas

- `ads-signals-knowledge-library@c2e83fdbd`: superficie completa de 148 archivos inventariada y validada; lectura profunda de startup, todas las capas `docs/00`–`docs/10`, scripts y templates relevantes al flujo y gobierno.
- `origin/master` de Playmaker, SDK Events, Materializer, Kafka, Flink, ClickHouse, Fury, Signals y Observability; SHAs exactos en [[Deployments en RIO — flujo completo]].
- Contratos y procedimientos del vault: `human-first-technical-writing`, `agents-os-resource-wiki`, schema contract y templates materializados.

## Resolución aplicada

- [[ads-signals-knowledge-library]] pasa a ser el único knowledge bundle activo y supersede a [[signals-knowledge]]. El código del servicio dueño prevalece sobre la librería para comportamiento vigente.
- Se separó una guía corta, ordenada por preguntas del lector, de la auditoría forense de frescura e integridad.
- La auditoría reproduce 17 errores del validador y documenta drift material en Signals, Fury, Observability y Playmaker.
- Los principales riesgos quedan modelados como boundaries causales: evento post-commit en memoria, ACK antes del trabajo y terminal local antes del resultado. Fury se documenta como referencia interna de desired/observed state durable y publicación reintentable.
- No se modificó código de RIO ni el repo externo. Los worktrees y sus `graphify-out/` no trackeados se preservaron.

## Validación

- `validate_schema_contract.py --type project|doc|resource|source|change_log`: 0 errores para las clases tocadas.
- `ruby scripts/validate_library.rb`: falla reproducible con 17 errores; se registra como estado de la fuente, no como fallo de los documentos creados.
- `graphify-obsidian update`: bloqueado antes de indexar por 25 errores y 6 warnings preexistentes fuera de los archivos tocados; no se corrigió deuda ajena.
- Lint manual del dominio `knowledges`: una sola fila vigente, provenance resoluble, source lifecycle cruzado, índice y log actualizados.
- Tests de `human-first-technical-writing`: scan test pasa por el orden `modelo → flujo → datos → mensajes → CP → riesgos → diseño`; backtracking test mantiene cada término junto a su definición o tabla; mental-model test permite reconstruir owner, correlación y ventana de pérdida sin abrir el código.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Restaurar las referencias vigentes a `signals-knowledge`, retirar las tres notas nuevas y revertir los cambios de lifecycle/índice/log si el equipo determina que la nueva librería no reemplaza la anterior. No borrar los registros históricos.
