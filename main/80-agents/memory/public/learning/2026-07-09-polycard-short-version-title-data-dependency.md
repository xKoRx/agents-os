---
type: learning
scope: application
created: "2026-07-09"
updated: "2026-07-09"
area: "[[Meli]]"
project:
application: "[[java-polycard-sdk]]"
entities:
  - "[[java-polycard-sdk]]"
related: []
aliases: []
confidence: verified
source_session: "[[2026-07-09-polycard-new-title-motors-summary]]"
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/learning
  - area/meli
  - app/java-polycard-sdk
---

# Polycard: el título/subtítulo de motors depende del atributo SHORT_VERSION, ausente en casi todos los mocks de test

## Aprendizaje

- La "versión corta" de motors en la SDK sale **exclusivamente** del atributo con id `SHORT_VERSION` (`AttributeUtils.Motors.getShortVersion`, key única `SHORT_VERSION`, sin alias ni derivación en `data-fetcher`). La versión **larga** es `TRIM`/`VERS` (`getVersion`) — son atributos distintos.
- Los mocks de test de esta SDK están incompletos: de 7 ítems de motors (los que tienen `VEHICLE_YEAR`), **solo 1** (`raw_MLB3516992949_motors.json`, Ford Ka → "Se") trae `SHORT_VERSION`. En prod, en cambio, viene poblado en todos.
- Consecuencia práctica: cualquier feature que muestre `short_version` (título compuesto `brand model short_version year`, o el subtítulo) se ve vacío/incompleto en test aunque el código sea correcto. No confundir con bug. El `SubtitleDecorator` sí cae a `TRIM` como fallback; el título compuesto de `feature/new-title-motors` NO (por decisión de Rodrigo).

## Aplicabilidad

- **Cuándo cargarlo:** al tocar título/subtítulo/atributos de motors (Cars & Vans) en java-polycard-sdk, o al ver "marca modelo año" sin versión en test.
- **Cuándo no cargarlo:** trabajo no-motors o fuera de la SDK de polycard.

## Entidades relacionadas

- [[java-polycard-sdk]]

## Evidencia

- Fuente: [[2026-07-09-polycard-new-title-motors-summary]] — grep de todo el repo: única key `SHORT_VERSION` en `AttributeUtils.java:184`; 1/7 mocks de motors la incluyen.
