---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[Sunsets backends RIO]]"
  - "[[rio-controlplane-flink]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# Rio sunset update — rio-controlplane-flink

**Desenlace: APPLIED** — PR añade pin Guava; Jackson ya efectivo en la base.

## Propósito

Registro de la corrida del 2026-10-22T13:31:42-03:00; horizonte autorizado: todos los sunsets abiertos, incluidos vencidos. America/Santiago.

## Contenido

### Sunsets mapeados

| Dependencia | Issues | Fecha local | Afectada | Objetivo Fury | Efectiva en código |
| --- | --- | --- | --- | --- | --- |
| com.fasterxml.jackson.core/jackson-databind | 6508087,6508032,6507463 | 2026-10-31 | 2.21.5 | 2.21.7 | 2.21.7 |
| com.fasterxml.jackson.core/jackson-core | 6552766 | 2026-10-31 | 2.21.5 | 2.21.7 | 2.21.7 |
| com.google.guava/guava | 6657835 | 2026-11-11 | 33.6.0-android | 33.7.2-jre | 33.7.2-jre |

### Scopes afectados

Guava: bq-consumer-nonprod, api-nonprod, production, gcp-testing-nonsite, bq-stage-nonprod, bq-consumer-nonsite, api-nonsite. Jackson: los mismos excepto bq-consumer-nonprod y api-nonprod.

### Cambio, PR y validación

- Ruta: PR añade pin Guava; Jackson ya efectivo en la base.
- PR: https://github.com/melisource/fury_rio-controlplane-flink/pull/217
- SHA completo: `884c132609ebf5762b16a5457c7ff49d5031ea8d`.
- Validación nativa: 199 suites, 1.966 tests, cero fallas/errores/skips; build, jacocoTestReport y hooks pre-commit pasan.
- Build: `202609.24.0-feat-rio-sunset.0` — FINISHED; gate SHA aceptado; catálogo completo 339 dependencias, cero sunsets.

### Deploy a test

Rodrigo autorizó el equivalente principal de prueba y confirmó explícitamente api-nonprod. Gate de scope y build aceptados. Versión 202609.24.0-feat-rio-sunset.0, SHA 884c132609ebf5762b16a5457c7ff49d5031ea8d del PR #217.

- Pipeline [533792](https://web.furycloud.io/engineering/applications/rio-controlplane-flink/deployment-pipelines/hands-off/executions/533792): completed, completion 100, pasos deploy/wait/finish completed.
- Deployment [38932155](https://web.furycloud.io/rio-controlplane-flink/deployments/38932155): finished, active=false. Scope liberado.
- Fury ejecutó Finish automáticamente tras el minuto de espera; no hizo falta un segundo clic. Se verificó el cierre terminal de ambas entidades.
- Catálogo del artefacto: 339 dependencias, cero sunsets. Los demás scopes no fueron desplegados en esta corrida; no se afirma saneamiento completo del catálogo agregado de la app.

### Notas y bloqueos

- Los checkouts locales con cambios ajenos se preservaron. No se creó release productiva, promoción ni merge.
- No se publicaron comentarios de GitHub ni mensajes a terceros.
- Reporte local; no se subió copia a Drive durante esta fase.

## Fuentes

- [Catálogo agregado](https://web.furycloud.io/engineering/applications/rio-controlplane-flink/dependency-catalog-summary); conteos contrastados, segmentos y versiones desplegadas inspeccionados hasta completar páginas.
- Objetivos obtenidos de `issues[].upgrade_to`; los valores internos sin purl se conservaron como campo estructurado, nunca se extrajeron de `suggested`.
- Repo `melisource/fury_rio-controlplane-flink` y evidencia Gradle del SHA indicado.
