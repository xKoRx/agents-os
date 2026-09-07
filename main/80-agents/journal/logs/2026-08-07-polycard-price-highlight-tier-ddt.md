---
type: change_log
scope: session
created: 2026-08-07
updated: 2026-08-07
area: "[[Meli]]"
project: "[[Destaque de Precio Search — Java Polycard SDK]]"
application: "[[java-polycard-sdk]]"
entities:
  - "[[Destaque de Precio Search — Java Polycard SDK]]"
related:
  - "[[Cierre VIS]]"
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
  - area/meli
  - app/java-polycard-sdk
  - feature/destaques-de-precio
---

# DDT de PRICE_HIGHLIGHT_TIER agregado en Java Polycard SDK

## Cambio

- Se agregó un registry DDT opt-in para Price V1.
- Se agregó un mock MLA con `LOW`, `VERY_LOW` y `NORMAL`.
- Se agregó un escenario Android V1.
- Price V2 queda fuera de esta validación y no recibe cambios.

## Validación

- JSON, referencias de mocks y aliases de registry validados estáticamente.
- La ejecución Gradle/DDT no se completó: Gradle 7.6 no puede cargar el plugin i18n compilado con class-file major version 65.

## Pendiente

- Ejecutar DDT Studio y la suite de integración en un entorno Gradle/JDK compatible.
- Adjuntar capturas DDT Studio y de Android al PR.
