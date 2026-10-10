---
type: source
schema_version: 1
status: active
area: "[[Meli]]"
source_url:
repo: melisource/fury_rio-controlplane-clickhouse
path: local/VALIDATION.md
author:
published:
captured: "2026-10-08"
license:
checksum: bd34ef5164668d46a7e1b43ebbb4e465eaa0db5a2a420d61abe70fbdf59ff4b8
supersedes:
superseded_by:
aliases: []
tags:
  - kind/source
created: "2026-10-08"
updated: "2026-10-08"
related: ["[[rio-controlplane-clickhouse]]"]
---

# Source — ClickHouse — Pruebas físicas locales 2026-10-08

## Referencia

- Repo: `melisource/fury_rio-controlplane-clickhouse`, `develop @ c8b20b6531a73348314587fc14f43e0ad8ce76ae` con cambios locales sin commit; reporte `local/VALIDATION.md`, runner `local/clickhouse_e2e.py` y ayuda `local/colima_forward.py`.
- Motor ejecutado: Docker `clickhouse/clickhouse-server:25.8`, versión SQL `25.8.33.6`; JVM Corretto 25.0.4. Jar SHA-256: `ddfc7632c2b6113eb73c8ee05e986255b8dde57d7ffb1c27fe9d729cc7d53f4e`.

## Alcance y resultados

- `test bootJar jacocoTestReport`: 2340 tests en 357 clases, cero fallos, errores u omitidos. La suite Gradle sigue usando mocks; se reporta separada de la suite física.
- `python3 local/clickhouse_e2e.py`: 14 escenarios PASS contra CP HTTP y servidor físico, 66,404 segundos, exit 0. Se esperan resultados terminales correlacionados y se contrastan efectos SQL.
- Cubiertos: autenticación, permisos fuera de usernames exactos rechazados, MergeTree con campos tipados/Nullable/DateTime64/índice, usuarios y grants con escritura/lectura reales, reentrega idempotente, list/describe, updates preservando filas, ingestión por MV, stop/start y runtime status, conflicto de propietario, Context ausente, tipo inválido, deprovision y liberación de ownership para otro producto.
- Cleanup físico: cero tablas en `rio_local_e2e`, cero usuarios de fixtures y cero recursos detached. MySQL preexistente preservado. CP PID 7323 en loopback 8080 y ClickHouse saludable quedaron ejecutándose; existe forward loopback de Colima para 8123/9000.

## Defectos y cambios contrastados

- El cliente on-premise enviaba `format=JSONEachRow`; el motor lo rechazó con UNKNOWN_SETTING antes del primer provision (deployment `ea481cde-ae0f-4951-ab40-7b2e0c2cfa14`). Se corrigió a `default_format=JSONEachRow`; dos regresiones HTTP fueron RED antes del cambio y GREEN después. Fuente primaria: [HTTP interface](https://clickhouse.com/docs/concepts/features/interfaces/http).
- El generador no garantizaba dígitos; un update falló con `crud_user password must contain at least 1 digit` (deployment `78da3cbe-684c-41ed-bf54-196ca9feb368`). Ahora garantiza dígito/símbolo en posiciones distintas. Dos regresiones deterministas RED→GREEN; líneas/ramas del generador 100%.
- El ownership local era no-op; un update de otro producto se completó indebidamente en la prueba. Se implementó registro atómico por instancia sólo en local; tres regresiones RED→GREEN. Las 15 líneas ejecutables nuevas y sus ramas están cubiertas; el camino KVS desplegado conserva comportamiento.
- READMEs/fixtures completos con Context y warehouse existente; acción list-tables mantiene su contrato camelCase. Se agregaron grants locales exactos para usuarios propios y lecturas de metadatos necesarias; se revocan grants temporales al terminar. Compose selecciona línea 25.8.
- Colima estaba saludable pero sus forwards SSH morían con exit 137; el fallback local usa Colima/socat ya instalados, sin reiniciar la VM ni MySQL. La revisión automática rechazó grants globales; se resolvió usando permisos por nombres exactos, sin autorización global ni bloqueo final.

## Notas de provenance

- PASS corresponde al standalone local probado. Kafka de ingestión, transporte Playmaker/Kafka, ClickHouse Cloud y destinos S3/Iceberg no se ejecutaron. KMS/estado son adapters locales; el ownership se pierde al reiniciar el CP.
- No se declara que los 2340 tests usen motor real: los 14 escenarios adicionales sí lo hacen. No hubo commit, push ni PR. No se guardan secretos ni logs pesados en el vault.
- El MCP AppSec no estuvo disponible; no se agregaron dependencias y el cambio de protocolo/grants/fixtures se revisó manualmente junto con regresiones/cobertura.
- Evidencia de corridas fallidas conservada por separado en el entorno temporal; cada rerun usó IDs/recursos nuevos. Esta captura sustituye el estado anterior de DDL no ejecutado sin borrar las fuentes históricas.
