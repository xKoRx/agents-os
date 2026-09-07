---
type: known_error
schema_version: 1
scope: application
created: "2026-09-02"
updated: "2026-09-02"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities:
  - "[[Symphony]]"
  - "[[sqx-watcher]]"
related: []
aliases: []
confidence: high
source_session: "ECHO-FORGE-CONFIG-SOURCE-WAVE-PROVENANCE-FIX-NORMAL"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - project/echo-forge
---

# symphony-config-source-wave-legacy-cfg

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Una qualification con `request_id` y `wave` nuevos crea su registro durable correcto, pero actividades posteriores registran/usan el `cfg_id` legacy `XAUUSD_example_flow_23_v1_wc3` y `config_minio_key` bajo `wave_c3/...`.
- La fila legacy queda con `request_id`/`wave` de la ejecución nueva mientras conserva la clave MinIO histórica, rompiendo la correspondencia entre fuente declarada y objeto físico.

## Causa

- El camino legacy de resolución de configuración deriva/reutiliza el `cfg_id` truncado en lugar de transportar una fuente inmutable separada (`config_source_wave`) para la ola de ejecución.

## Impacto

- La salida de la qualification no es elegible para promoción ni para certificación física: no se puede demostrar que cada artefacto provenga exclusivamente de la ola nueva.
- No debe repararse con UPDATE/fixture/overwrite en producción; una decisión de promoción no vacía bajo esta procedencia sería inválida para C3.

## Detección

- Consultar PostgreSQL por `config_id`, `config_json.request_id`, `config_json.wave`, `wave_config.wave_key` y `minio_key`; corroborar con logs `sqx_db_register_config_use` y `flow_run_ref`.
- En la ejecución `forge-c3-supply-v2-20260902T2215Z-59EC5E`, el `flow_run_ref` nuevo fue `d7693ebe-4ea8-4c10-a65e-c45d676ac788`; la fila nueva usó `bb242481-d755-43a1-8425-61cce5ce03eb`, mientras la actividad observó `69b44c2c-adcf-4bb0-be6e-c8997ccda3cc` y `wave_c3/...`.

## Mitigación

- Cerrar `C3` como `BLOCKED / CLOSED` con `CONFIG_SOURCE_WAVE_PROVENANCE_VIOLATION`; no iniciar Campaign ni aceptar `NONEMPTY_PROMOTION_SUPPLY` hasta corregir el transporte de fuente y publicar/converger una nueva release.
- Repetir desde watcher con RequestIDs frescos y verificar que ningún `cfg_id`/clave legacy llegue a una ola nueva.

## Corrección source

- El defecto quedó corregido en `sqx/activities/worker/steps/steps.go`: `dbRegister.Execute` deriva `cfgID` y `config_minio_key` desde `runtime.EffectiveConfigSourceWave(st.Config)` sin split, prefijo ni fallback histórico.
- Commit `bac1d6ef93cd4714c1af4f2e44516bea44642e80` está publicado en `origin/master`; targeted tests, race, vet y diff check PASS. La release requerida es `0.2.86`.
- El FlowRun `d7693ebe-4ea8-4c10-a65e-c45d676ac788` queda `INVALID_FOR_SUPPLY_CERTIFICATION`; no se modifica ni se reutiliza como evidencia.

## Evidencia

- [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]] — checkpoint de sesión C3 del 2026-09-02.
- Repositorio `xKoRx/symphony`, runtime `48997d773e91dec9b8fe57fbd1650e8d8beb8b57`, release física `0.2.85`; evidencia read-only de PostgreSQL y logs del worker.
