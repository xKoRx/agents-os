---
type: session
scope: session
created: "2026-07-09"
updated: "2026-07-09"
area: "[[Meli]]"
project: "[[Refactor Polycard]]"
application: "[[java-polycard-sdk]]"
entities:
  - "[[java-polycard-sdk]]"
  - "[[search-middleware]]"
  - "[[fury-lib-consumer-deploy]]"
related:
  - "[[2026-07-09-1817-polycard-title-fury-versioning-raw]]"
  - "[[2026-07-09-fury-versioning-contract-correction]]"
aliases: []
confidence: high
source_session: "[[2026-07-09-1817-polycard-title-fury-versioning-raw]]"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# Polycard title y versionado Fury — session summary

> [!info]+ Session summary L1
> Resumen operativo del cierre. Excluido del corpus normal de Graphify.

## Objetivo

- Llevar el título Motors a `marca modelo SHORT_VERSION/TRIM año` con guardrail de longitud.
- Alinear la operación de versiones de librería y consumidor mediante Fury.

## Contexto cargado

- [[java-polycard-sdk]], [[search-middleware]], [[fury-lib-consumer-deploy]] y memoria operativa de Polycard.

## Trabajo realizado

- Implementado fallback `SHORT_VERSION → TRIM` y guardrail inicial de 40 caracteres; si se excede, el título vuelve a `marca modelo año`.
- Search quedó configurado para activar el título compuesto en sus dos factories.
- Se dejó la versión de test `0.0.2-new-title-motors` en ambos repos y se validó localmente.
- Se corrigió la skill: declarar en Gradle no equivale a crear en Fury; librería primero, disponibilidad confirmada, consumidor después.

## Artifacts creados o modificados

- [[fury-lib-consumer-deploy]] actualizado.
- [[2026-07-09-fury-versioning-contract-correction]] creado como log auditable.
- Código y pruebas en los repositorios locales; el detalle técnico permanece en sus diffs.

## Memoria propuesta o creada

- No se creó L3 adicional: la regla operativa canónica quedó en la skill.

## Decisiones

- Umbral inicial del guardrail: 40 caracteres, pendiente de calibración visual.
- No importar una librería en el consumidor hasta verla disponible en Fury.

## Pendiente

- Validación visual del usuario en Search.
- Ajustar el umbral si las capturas reales muestran títulos de dos líneas.
