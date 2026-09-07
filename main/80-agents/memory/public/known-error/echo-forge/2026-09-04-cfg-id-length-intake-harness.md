---
type: known_error
schema_version: 1
scope: project
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application:
entities:
  - "[[Echo Forge]]"
related: []
aliases: []
confidence: verified
source_session: "[[2026-09-04-echo-forge-c3-final-recert-summary]]"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - project/echo-forge
---

# 2026-09-04-cfg-id-length-intake-harness

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- La primera intake física no alcanzó persistencia durable y el watcher terminó con `pq: value too long for type character varying(100)` al generar `cfg_id` desde nombres largos de strategy/wave.

## Causa

- El harness de certificación construyó una identidad derivada mayor a la longitud contractual de la columna; no fue un defecto del flujo Campaign ni produjo una Campaign/FlowRun durable.

## Impacto

- Retrasó la intake y dejó evidencia operacional del intento fallido; no contaminó la identidad histórica, no requirió mutación de source y no bloqueó la certificación después de corregir el shape efímero.

## Detección

- Log del watcher y ausencia de filas durables; la autoridad de release, source y CFX permaneció intacta.

## Mitigación

- Usar nombres cortos y únicos en el config efímero (`c3p092-248f450f`), conservar `config_source_wave` ausente y repetir sólo la intake válida autorizada; no modificar el producto ni reusar identidades.

## Evidencia

- Config válida SHA256 `329b4a2298105c3b9dd84988d6ede76b03ffb4da7c88ed51b24242eeaf941565`; Campaign durable posterior `a9e73e66-5062-44d7-b665-22740383c676` y conteos post-redelivery `campaign=1,wave=1,flow=1,promotion=1,stop=1`.
