---
type: change_log
schema_version: 1
scope: session
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Meli]]"
project: "[[Playmaker — Doble dispatch al avanzar batches]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Playmaker — Doble dispatch al avanzar batches]]"
  - "[[rio-playmaker]]"
related:
  - "[[Playmaker — java-toolkit-kvs 0.6.1 es incompatible con json-jackson 4]]"
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

# Change Log — Playmaker KVS/Jackson y release 0.0.13

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated + created
- **Archivo(s):**
  - `10-projects/Meli/Playmaker — Doble dispatch al avanzar batches/Playmaker — Doble dispatch al avanzar batches.md`
  - `80-agents/memory/public/known-error/playmaker-java-toolkit-kvs-0-6-1-json-jackson-4-linkage.md`

## Motivo

- Persistir el estado final de la corrección que desbloqueó el arranque y dejar recuperable la incompatibilidad binaria para diagnósticos futuros.

## Fuentes usadas

- Logs del deployment `0.0.12-listener-lock`, diff y pruebas del commit `b4fa880a2`, resolución Gradle y estado terminal de Fury para `0.0.13-listener-lock`.

## Resolución aplicada

- Se actualizó el estado canónico del proyecto y se creó un known error acotado con síntoma, causa, detección y mitigación verificadas.

## Validación

- Suite completa, bootJar, test dirigido, diff check, sincronía remota y versión Fury `FINISHED`; las cinco notas del cierre pasaron lint estricto con `0 ERROR / 0 WARN`. `graphify-obsidian update` quedó bloqueado antes de indexar por 19 findings globales ajenos a este delta, por lo que Markdown permanece como fuente de verdad y el índice queda pendiente de higiene.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Eliminar el known error y revertir únicamente el delta de estado/bitácora del proyecto mediante este log; no afecta el commit ni la versión Fury ya publicados.
