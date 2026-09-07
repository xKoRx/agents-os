---
type: session
scope: session
created: "2026-07-09"
updated: "2026-07-09"
area: "[[Meli]]"
project:
application: "[[java-polycard-sdk]]"
entities:
  - "[[java-polycard-sdk]]"
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

# Polycard — new title motors (single layout)

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- En `feature/new-title-motors`: sacar el subtítulo del layout single de motors y componer el título como `brand model short_version year` cuando un predicado esté en `true`.

## Contexto cargado

- Repo `/Users/rjara/fuentes/java-polycard-sdk`. AGENTS OS se cargó recién al cierre (no al inicio) — ver feedback.

## Trabajo realizado

- `TitleDecorator` + `TitleDecoratorBuilder`: predicado nuevo `shortVersionInTitlePredicate` (default `false`) con `withShortVersionInTitle()`. Con motors + predicado true arma `brand model short_version year` usando **solo** `AttributeUtils.Motors.getShortVersion()` (`SHORT_VERSION`); si no está, omite versión — **nunca** cae a `TRIM/VERS` (el usuario lo exigió explícitamente).
- Saqué `PredefinedPolycardComponent.SUBTITLE` de `SingleNativeAndroidLayoutOrder` y `SingleNativeIosLayoutOrder`.
- Tests: 2 casos nuevos en `TitleDecoratorTest`, ajuste de conteo (57→56) en tests de layout, y `CardLayoutCoverageTest` (SUBTITLE ya no requerido; se preservó requisito de LABELS renombrando helper a `isLabelsRequired`). Version bump + CHANGELOG.
- Diagnóstico del "solo veo marca modelo año": los ítems no traen `SHORT_VERSION`. Ver [[2026-07-09-polycard-short-version-title-data-dependency]].

## Artifacts creados o modificados

- Código en repo (sin commit). Artefactos AGENTS OS: este summary, L0 raw, continuity interna, learning L3, feedback.

## Memoria propuesta o creada

- Learning L3: [[2026-07-09-polycard-short-version-title-data-dependency]].
- Continuity interna: `2026-07-09-polycard-new-title-motors-continuity`.

## Decisiones

- Predicado dedicado (no reusar `versionInTitlePredicate`) porque el formato reordena y usa versión corta.
- Sin fallback a TRIM: versión corta = `SHORT_VERSION` y nada más.

## Pendiente

- Commit del cambio.
- Agregar `SHORT_VERSION` a mocks de motors + escenario de integración con `withShortVersionInTitle()` (hoy solo 1 de 7 mocks lo trae).
- Confirmar quién puebla `SHORT_VERSION` en el input (API Decoradora) para prod.
