---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Sunsets backends RIO]]"
  - "[[rio-controlplane-kafka]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# Rio sunset update — rio-controlplane-kafka

**Desenlace: STOPPED** — Solo redeploy; pins ya merged en develop (#84). Checkout original sucio preservado.

## Propósito

Registro de la corrida del 2026-10-22T13:31:42-03:00; horizonte autorizado: todos los sunsets abiertos, incluidos vencidos. America/Santiago.

## Contenido

### Sunsets mapeados

| Dependencia | Issues | Fecha local | Afectada | Objetivo Fury | Efectiva en código |
| --- | --- | --- | --- | --- | --- |
| com.fasterxml.jackson.core/jackson-databind | 6507463,6508032,6508087 | 2026-10-31 | 2.21.5 | 2.21.7 | 2.21.7 |
| com.fasterxml.jackson.core/jackson-core | 6552766 | 2026-10-31 | 2.21.5 | 2.21.7 | 2.21.7 |
| at.yawk.lz4/lz4-java | 6619368,6619356 | 2026-11-06 | 1.10.1 | 1.11.4 | 1.11.4 |

### Scopes afectados

test-nonprod, gcp-nonprod, aws-nonprod, rio-consumer-nonsite, production, gcp-nonsite, test, bq-stage-nonprod, bq-kafka-materialize-test-nonprod y alpha-consumer-nonprod.

### Cambio, PR y validación

- Ruta: Solo redeploy; pins ya merged en develop (#84). Checkout original sucio preservado.
- PR: No corresponde: no se modificó código.
- SHA completo: `f4b5701e1ad338512578a39c16df955e3fb15d21`.
- Validación nativa: runtimeClasspath de Gradle confirma las versiones efectivas; no se modificó código..
- Build: `202609.22.1-rc1.0` — FINISHED; gate SHA aceptado; catálogo completo 197 dependencias, cero sunsets.

### Deploy a test

No ejecutado. Falta scope exacto indicado por una persona y confirmación inmediata, después del gate de build. No hubo pipeline, deployment ni Finish en esta corrida.

### Notas y bloqueos

- Los checkouts locales con cambios ajenos se preservaron. No se creó release productiva, promoción ni merge.
- No se publicaron comentarios de GitHub ni mensajes a terceros.
- Reporte local; no se subió copia a Drive durante esta fase.

## Fuentes

- [Catálogo agregado](https://web.furycloud.io/engineering/applications/rio-controlplane-kafka/dependency-catalog-summary); conteos contrastados, segmentos y versiones desplegadas inspeccionados hasta completar páginas.
- Objetivos obtenidos de `issues[].upgrade_to`; los valores internos sin purl se conservaron como campo estructurado, nunca se extrajeron de `suggested`.
- Repo `melisource/fury_rio-controlplane-kafka` y evidencia Gradle del SHA indicado.
