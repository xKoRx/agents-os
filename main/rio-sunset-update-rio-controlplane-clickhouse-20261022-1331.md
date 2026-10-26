---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Sunsets backends RIO]]"
  - "[[rio-controlplane-clickhouse]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# Rio sunset update — rio-controlplane-clickhouse

**Desenlace: STOPPED** — Solo redeploy; pin ya presente y efectivo en develop.

## Propósito

Registro de la corrida del 2026-10-22T13:31:42-03:00; horizonte autorizado: todos los sunsets abiertos, incluidos vencidos. America/Santiago.

## Contenido

### Sunsets mapeados

| Dependencia | Issues | Fecha local | Afectada | Objetivo Fury | Efectiva en código |
| --- | --- | --- | --- | --- | --- |
| at.yawk.lz4/lz4-java | 6619357,6619369 | 2026-11-06 | 1.10.2 | 1.11.4 | 1.11.4 |

### Scopes afectados

stage y jobs1-test.

### Cambio, PR y validación

- Ruta: Solo redeploy; pin ya presente y efectivo en develop.
- PR: No corresponde: no se modificó código.
- SHA completo: `126633f09b14643342221400a5870941a92a6fbf`.
- Validación nativa: runtimeClasspath de Gradle confirma las versiones efectivas; no se modificó código..
- Build: `0.0.2-mergetree-component-im.2` — FINISHED; gate SHA aceptado; catálogo completo 198 dependencias, cero sunsets.

### Deploy a test

No ejecutado. Falta scope exacto indicado por una persona y confirmación inmediata, después del gate de build. No hubo pipeline, deployment ni Finish en esta corrida.

### Notas y bloqueos

- Los checkouts locales con cambios ajenos se preservaron. No se creó release productiva, promoción ni merge.
- No se publicaron comentarios de GitHub ni mensajes a terceros.
- Reporte local; no se subió copia a Drive durante esta fase.

## Fuentes

- [Catálogo agregado](https://web.furycloud.io/engineering/applications/rio-controlplane-clickhouse/dependency-catalog-summary); conteos contrastados, segmentos y versiones desplegadas inspeccionados hasta completar páginas.
- Objetivos obtenidos de `issues[].upgrade_to`; los valores internos sin purl se conservaron como campo estructurado, nunca se extrajeron de `suggested`.
- Repo `melisource/fury_rio-controlplane-clickhouse` y evidencia Gradle del SHA indicado.
