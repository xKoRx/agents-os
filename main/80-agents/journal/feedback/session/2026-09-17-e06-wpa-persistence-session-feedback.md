# Session feedback — 2026-09-17 — E-06 WP-A (fricción PG descartable)

## Fricción real (recurrente, no resuelta en Sistema 1)

Cada fase Echo (E-03/E-04/E-05, ahora E-06) necesita "PostgreSQL 17.x descartable" para sus gates PG REAL, y la máquina de desarrollo no tiene psql ni servidor PG, docker está inactivo y sudo está bloqueado (`no new privileges`). La solución se re-descubre por fase: esta sesión quedó operativa en ~10 minutos con la receta: server = binarios Zonky (`io.zonky.test.postgres:embedded-postgres-binaries-linux-amd64:17.11.0` de Maven Central, trae `initdb`/`pg_ctl`/`postgres` pero **no** `psql`) + cliente = `postgresql-client-17` de apt.postgresql.org descargado como .deb y extraído con `dpkg -x` + `apt-get download libpq5` (sin root); cluster efímero con socket unix local y trust. EDB binaries devuelve 403 por curl.

## Sugerencia

Promover la receta a **runbook** (Sistema 1, dominio Aranea/Echo dev): "PG 17.x descartable sin root ni docker". Las bitácoras de fase la mencionan de pasada pero no hay fuente canónica del procedimiento; E-06 lo documentó en la bitácora del proyecto y el L0 de la sesión.

## Segunda fricción menor

Los harnesses SQL por fase (`identity_bwc`, `analytics_a0`) iteral las migraciones aplicando todo menos su exclusiva: cada migración nueva de otra fase rompe su rebuild (documentado con repro en `TEST_CHANGE_REQUEST.md` TC-06-2). Sugerencia estructural: que el bucle salte migraciones `> <última de la fase>` por defecto.
