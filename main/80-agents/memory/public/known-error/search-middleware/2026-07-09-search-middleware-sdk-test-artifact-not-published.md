---
type: known_error
scope: integration
created: 2026-07-09
updated: 2026-07-09
area: "[[Meli]]"
project: "[[Single View Layout — Migración al Polycard SDK]]"
application: "[[search-middleware]]"
entities:
  - "[[search-middleware]]"
  - "[[java-polycard-sdk]]"
related: []
aliases:
  - missing test SDK artifact
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: medium
tags:
  - kind/known-error
  - app/search-middleware
  - integration/maven
  - error/sdk-artifact-missing
---

# Search Middleware no puede resolver SDK de prueba no publicada

## Síntoma

`./gradlew compileJava` falla resolviendo los módulos `com.mercadolibre.polycard:*:0.0.1-new-title-motors` desde Fury Maven.

## Causa

La versión está declarada en Search y existe en el checkout local de `java-polycard-sdk`, pero el build remoto de Fury no terminó publicando los módulos; la versión quedó en `ERROR`.

## Impacto

No se puede distinguir un error de código Java de un error de resolución de dependencias ejecutando el build normal.

## Mitigación validada

- Publicar la SDK con `./gradlew publishToMavenLocal` desde `java-polycard-sdk`.
- Usar `mavenLocal()` como fallback local antes de Fury durante desarrollo.
- Verificar después la publicación remota antes de retirar el fallback o depender de CI.

## Evidencia

- Search compiló y pasó tests focales con Maven local.
- Fury reportó `0.0.1-new-title-motors` en estado `ERROR`.
