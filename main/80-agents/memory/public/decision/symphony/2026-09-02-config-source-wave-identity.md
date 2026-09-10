---
type: decision
schema_version: 1
scope: project
created: "2026-09-02"
updated: "2026-09-02"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related:
  - "[[symphony-config-source-wave-legacy-cfg]]"
aliases: []
confidence: verified
source_session: "ECHO-FORGE-CONFIG-SOURCE-WAVE-PROVENANCE-FIX-NORMAL"
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# Config identity must use the effective source wave

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- La qualification C3 bajo runtime `48997d773e91dec9b8fe57fbd1650e8d8beb8b57` evidenció que la lectura de `.cfx` usaba la wave completa, mientras `dbRegister` derivaba `cfgID` y `config_minio_key` desde el primer token de `st.Config.Wave`.

## Decisión

- En `sqx/activities/worker/steps/steps.go`, `dbRegister.Execute` usa `sourceWave := runtime.EffectiveConfigSourceWave(st.Config)` como única autoridad para `cfgID` y `configMinioKey`; `getStoragePrefix` y los outputs siguen usando `st.Config.Wave` como execution namespace.

## Rationale

- La separación evita reutilizar identities históricas truncadas y mantiene Campaign child con config read/identity en `base.Wave` y outputs en su wave de ejecución.

## Consecuencias

- Commit `bac1d6ef93cd4714c1af4f2e44516bea44642e80` fue validado y publicado en `origin/master`; el fix requiere la release física siguiente `0.2.86`.

## Alternativas descartadas

- No se cambia watcher, materializer Campaign, `prepareGenericRequest`, `SaveConfig` ni se agrega fallback histórico; si la source exacta no existe, la descarga falla.
