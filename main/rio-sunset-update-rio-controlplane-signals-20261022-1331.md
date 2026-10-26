---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Sunsets backends RIO]]"
  - "[[rio-controlplane-signals]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# Rio sunset update — rio-controlplane-signals

**Desenlace: REDEPLOY_ONLY** — Solo redeploy; BOM/Streams 4.0.7, commons 3.0.1 y Jackson 2.21.7 ya efectivos. Los artefactos nuevos desplegados tienen estos bugs resueltos según catálogo; no se aplicaron downgrades a Streams/commons.

## Propósito

Registro de la corrida del 2026-10-22T13:31:42-03:00; horizonte autorizado: todos los sunsets abiertos, incluidos vencidos. America/Santiago.

## Contenido

### Sunsets mapeados

| Dependencia | Issues | Fecha local | Afectada | Objetivo Fury | Efectiva en código |
| --- | --- | --- | --- | --- | --- |
| com.mercadolibre.library/melistreams-commons | 830-2155958 | 2026-10-11 | 3.0.0 | 2.91.0 | 3.0.1 |
| com.mercadolibre.library/java-melitk-bom | 829-2156554 | 2026-10-11 | 4.0.6 | 4.0.7 | 4.0.7 |
| com.mercadolibre.library/java-melitk-streams | 828-2156641 | 2026-10-11 | 4.0.6 | 4.0.5 | 4.0.7 |
| com.fasterxml.jackson.core/jackson-databind | 6507463,6508087,6508032 | 2026-10-31 | 2.21.5 | 2.21.7 | 2.21.7 |
| com.fasterxml.jackson.core/jackson-core | 6552766 | 2026-10-31 | 2.21.5 | 2.21.7 | 2.21.7 |

### Scopes afectados

production-nonsite, test-nonprod y bq-stage-nonprod.

### Cambio, PR y validación

- Ruta: Solo redeploy; BOM/Streams 4.0.7, commons 3.0.1 y Jackson 2.21.7 ya efectivos. Los artefactos nuevos desplegados tienen estos bugs resueltos según catálogo; no se aplicaron downgrades a Streams/commons.
- PR: No corresponde: no se modificó código.
- SHA completo: `10a98bc09b9ad5d2ab1aa51855504a1e5efa801f`.
- Validación nativa: runtimeClasspath de Gradle confirma las versiones efectivas; no se modificó código..
- Build: `202608.21.1-develop.0` — FINISHED; gate SHA aceptado; catálogo completo 202 dependencias, cero sunsets.

### Deploy a test

Rodrigo seleccionó test-nonprod y confirmó explícitamente el deploy. Gate de scope y build aceptados. Versión 202608.21.1-develop.0, SHA 10a98bc09b9ad5d2ab1aa51855504a1e5efa801f.

- Pipeline [533791](https://web.furycloud.io/engineering/applications/rio-controlplane-signals/deployment-pipelines/hands-off/executions/533791): completed, completion 100, pasos deploy/wait/finish completed.
- Deployment [38932153](https://web.furycloud.io/rio-controlplane-signals/deployments/38932153): finished, active=false. Scope liberado.
- Fury ejecutó Finish automáticamente tras el minuto de espera; no hizo falta un segundo clic. Se verificó el cierre terminal de ambas entidades.
- Catálogo del artefacto: 202 dependencias, cero sunsets. Producción y bq-stage-nonprod conservan rollout humano pendiente; no se afirma saneamiento completo del catálogo agregado de la app.

### Notas y bloqueos

- Los checkouts locales con cambios ajenos se preservaron. No se creó release productiva, promoción ni merge.
- No se publicaron comentarios de GitHub ni mensajes a terceros.
- Reporte local; no se subió copia a Drive durante esta fase.

## Fuentes

- [Catálogo agregado](https://web.furycloud.io/engineering/applications/rio-controlplane-signals/dependency-catalog-summary); conteos contrastados, segmentos y versiones desplegadas inspeccionados hasta completar páginas.
- Objetivos obtenidos de `issues[].upgrade_to`; los valores internos sin purl se conservaron como campo estructurado, nunca se extrajeron de `suggested`.
- Repo `melisource/fury_rio-controlplane-signals` y evidencia Gradle del SHA indicado.
