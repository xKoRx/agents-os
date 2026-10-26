---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Sunsets backends RIO]]"
  - "[[rio-controlplane-fury]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# Rio sunset update — rio-controlplane-fury

**Desenlace: STOPPED** — Solo redeploy; constrain LZ4 1.11.4 ya presente y efectivo en develop.

## Propósito

Registro de la corrida del 2026-10-22T13:31:42-03:00; horizonte autorizado: todos los sunsets abiertos, incluidos vencidos. America/Santiago.

## Contenido

### Sunsets mapeados

| Dependencia | Issues | Fecha local | Afectada | Objetivo Fury | Efectiva en código |
| --- | --- | --- | --- | --- | --- |
| at.yawk.lz4/lz4-java | 6619368,6619356 | 2026-11-06 | 1.10.1 | 1.11.4 | 1.11.4 |

### Scopes afectados

prober-nonprod, inbound-direct-nonprod, stage-nonprod, pusher-sink-test-nonprod, pusher-sink-stage-nonprod y bq-stage-nonprod.

### Cambio, PR y validación

- Ruta: Solo redeploy; constrain LZ4 1.11.4 ya presente y efectivo en develop.
- PR: No corresponde: no se modificó código.
- SHA completo: `b0fb7af1cfb4e49f2ab187915e113e78b8650cf0`.
- Validación nativa: runtimeClasspath de Gradle confirma las versiones efectivas; no se modificó código..
- Build: `202610.5.0-logs-tag.0` — FINISHED; gate SHA aceptado; catálogo completo de 167 dependencias, cero sunsets.

### Deploy a test

No ejecutado. Falta scope exacto indicado por una persona y confirmación inmediata, después del gate de build. No hubo pipeline, deployment ni Finish en esta corrida.

### Notas y bloqueos

- Los checkouts locales con cambios ajenos se preservaron. No se creó release productiva, promoción ni merge.
- No se publicaron comentarios de GitHub ni mensajes a terceros.
- Reporte local; no se subió copia a Drive durante esta fase.

## Fuentes

- [Catálogo agregado](https://web.furycloud.io/engineering/applications/rio-controlplane-fury/dependency-catalog-summary); conteos contrastados, segmentos y versiones desplegadas inspeccionados hasta completar páginas.
- Objetivos obtenidos de `issues[].upgrade_to`; los valores internos sin purl se conservaron como campo estructurado, nunca se extrajeron de `suggested`.
- Repo `melisource/fury_rio-controlplane-fury` y evidencia Gradle del SHA indicado.
