---
type: session
scope: session
created: "2026-07-14"
updated: "2026-07-14"
area: "[[Meli]]"
project: "[[Título Compuesto Motors — Short Version y Dedup]]"
application: "[[java-polycard-sdk]]"
entities:
  - "[[java-polycard-sdk]]"
  - "[[search-api-go]]"
related: []
aliases: []
confidence: high
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
  - area/meli
  - app/java-polycard-sdk
---

# Polycard título motors — dedup + prep de PR (L1)

> [!info]+ Session summary L1
> Continuación de [[2026-07-09-polycard-new-title-motors-summary]]. Detalle vivo en la nota de proyecto [[Título Compuesto Motors — Short Version y Dedup]] (planificador) y en la memoria interna de continuidad.

## Objetivo

- Resolver la repetición de palabras del título compuesto de motors de forma escalable y preparar el PR del SDK.

## Trabajo realizado

- **Dedup v2:** `TitleTokenDeduplicator.mergeModelAndVersion` (subsunción de tokens bidireccional) integrado en `TitleDecorator`. Corrige `Nx`/`Nx300h`, `Clc`/`Clc200` (token de modelo prefijo del de short version).
- **Detección escalable:** barrido BQ sobre `LK_CATALOG_PRODUCTS_CARS_AND_VANS` (12.910 combos, ~4,25% con repetición). Reveló 2 falsos positivos corregidos (trims de 1 letra `L/S/M`; letra de modelo superseded solo si sigue dígito). `MotorsTitleDedupInvariantTest` + CSV real como gate escalable.
- **Caché search:** confirmado por código que la short_version runtime la sirve [[search-api-go]] desde Redis (no queriable por valor); se descartó investigar la caché → BQ cubre el universo.
- **Prep PR:** `descripcion_pr.md` reescrito acotado al impacto real. Prompt maestro entregado para delegar 2 ajustes: (1) NO remover `SUBTITLE` de los `SingleNative*LayoutOrder` (mantenerlo, suprimir solo para motors a nivel decorator); (2) evaluar abstraer la composición del título (cross-vertical) a helper/util con KISS/YAGNI.
- Versión de test `0.0.5-new-title-motors`. `:decorator:test` completo verde, 0 borrados.

## Incidente y corrección

- Correr `:decorator:test` con `--tests` filtrado disparó `cleanTestFiles` y borró 283 ejemplos versionados ajenos. Restaurados. Regla registrada: [[feedback-no-collateral-file-deletion]] equivalente en memoria interna; correr suite COMPLETA o restaurar.

## Decisiones

- Dedup por subsunción de tokens (no `contains` crudo); reglas de 1 letra guiadas por datos reales.
- Validación escalable = invariante sobre corpus real, no salida esperada por caso.
- Componentes compartidos (Subtitle) se suprimen por vertical a nivel decorator, no se remueven del layout.

## Pendiente

- Aplicar prompt maestro (ajustes de alcance) → PR del SDK.
- Bloque B (consumo en search) y decisión de mesa C1 (fallback sin short_version).
