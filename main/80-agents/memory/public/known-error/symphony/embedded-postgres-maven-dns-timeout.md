---
type: known_error
schema_version: 1
scope: application
created: "2026-08-23"
updated: "2026-08-30"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[echo-forge]]"
entities:
  - "[[Symphony]]"
related:
  - "[[2026-08-23-durable-strategy-identity-v2-storage-support]]"
  - "[[2026-08-23-durable-strategy-identity-v2-cutover]]"
aliases:
  - embedded-postgres maven timeout
  - zonky maven dns
  - TEST_POSTGRES_DSN missing
confidence: verified
source_session: DURABLE-STRATEGY-IDENTITY-V2-CUTOVER-NORMAL
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - app/echo-forge
  - tech/symphony
  - tech/postgres
---

# embedded-postgres-maven-dns-timeout

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- `go test ./sqx/adapters/registry-postgres/...` cuelga minutos sin output y no llega a ejecutar tests de integración.
- `curl https://repo1.maven.org/maven2/` falla con `Resolving timed out after 10005 milliseconds`.

## Causa

- `fergusstrange/embedded-postgres` descarga binarios desde Maven Central. En este host la resolución DNS de `repo1.maven.org` no completa.
- No hay Postgres local (`postgres`/`psql` ausentes), Docker no está disponible, `TEST_POSTGRES_DSN` no está seteado, y el cache `/tmp/sqx-pg-bin` está vacío.

## Impacto

- Los tests de integración Postgres (incluido el cutover de `AdoptStrategy()` a identity v2) no se certifican en este host. Compilación y vet sí pasan.

## Detección

- El harness ya soporta `TEST_POSTGRES_DSN` en `postgrestest.OpenDB`. Si está vacío, arranca embedded-postgres y bloquea en Maven.

## Mitigación

- Exportar `TEST_POSTGRES_DSN` a un Postgres efímero/local ya existente. No instalar Docker/Postgres ni parchear producción para Maven.
- No tratar datos v1 de test como compatibilidad productiva.
- **Validada 2026-08-29 (sin Postgres local ni Docker disponibles):** pre-poblar el cache de binarios de `fergusstrange/embedded-postgres` — resolver `repo1.maven.org` vía DoH por 443 (`cloudflare-dns.com/dns-query`, el resolver LAN falla selectivamente para ese host y el UDP/53 saliente está bloqueado aunque ICMP/TCP operan), descargar con `curl --resolve repo1.maven.org:443:<IP>` el jar `io/zonky/test/postgres/embedded-postgres-binaries-darwin-arm64v8/<ver>/...jar` verificando su `.sha256`, extraer el `*.txz` interno (cualquier nombre; la librería toma el primero que termine en `.txz`) y dejarlo en `$TMPDIR/sqx-embedded-postgres-cache/embedded-postgres-binaries-darwin-arm64v8-<ver>.txz`. Tres quirks que hicieron fallar el primer intento: `os.TempDir()` de Go es `$TMPDIR` de macOS (`/var/folders/...`), no `/tmp`; para darwin/arm64 con PG ≥14.2 la librería reescribe la arquitectura a `arm64v8` (no existe artefacto `darwin-arm64`); la versión default de la librería v1.30.0 es `16.4.0`. Con el cache presente `ep.Start()` salta la red por completo.
- **Validada 2026-08-30 (`OpenDB`/`newControlPlane` sigue bloqueando con cache pre-poblado):** el cache pre-poblado sólo cubre `OpenIsolatedDB` (`$TMPDIR/sqx-embedded-postgres-cache`); `OpenDB` usa cache **per-PID** (`$TMPDIR/sqx-embedded-postgres-<pid>`) que nunca existe de antemano ⇒ reintenta Maven y muere con `unable to connect to https://repo1.maven.org/maven2` ("failed to start ephemeral PostgreSQL"). Workaround: levantar PG manual desde el `.txz` cacheado (`tar xJf` ⇒ binarios mínimos con sólo `initdb`/`pg_ctl`/`postgres`, SIN `psql` ni `createdb` ⇒ apuntar el DSN a la DB default `postgres`; no importa el nombre porque los tests usan la DB que el DSN indica), `initdb -U postgres` + `pg_ctl -o "-p <puerto>" start`, exportar `TEST_POSTGRES_DSN` (gana sobre el ephemeral en `OpenDB`) y crear **DB VIRGEN por cada invocación de `go test`**: los fixtures usan claves deterministas que persisten y contaminan conteos/uniques entre corridas (p.ej. conteos esperados 1 vs acumulados, `idx_strategies_unique_key_v0` duplicate). Con DB virgen, la suite completa produce el mismo set de fallos que el baseline en worktree hermano ⇒ comparación de causalidad fiable. Al cierre: `pg_ctl stop` + eliminar scratch (sin procesos/sockets colgando).

## Evidencia

- Sesiones DURABLE-STRATEGY-IDENTITY-V2-STORAGE-SUPPORT-NORMAL y DURABLE-STRATEGY-IDENTITY-V2-CUTOVER-NORMAL: mismo síntoma Maven; compile/vet/domain PASS.
- Sesión DURABLE-ARTIFACT-VERIFIED-READS-APPLY-PG-TARGETED-CLOSURE-NORMAL (2026-08-29): el bloqueo reapareció porque `/tmp` fue limpiado (cache ausente) y el DNS LAN no resuelve `repo1.maven.org`; con la mitigación de cache pre-poblado, Migration 008 y StageProducerOutput PASS en embedded PostgreSQL real (9.15s / 8.60s).
- Sesión DURABLE-PROJECT-STAGES-RECOVERY-SLICE2-EMPTY-RACE-CORRECTION-NORMAL (2026-08-30): los tests de `newControlPlane` fallaban a los 30s con el cache pre-poblado presente (per-PID cache + Maven); con PG manual + `TEST_POSTGRES_DSN` + DB virgen por invocación, los 6 tests nuevos de la correction PASS y la comparación full-suite diff-vs-baseline (worktree hermano) dio delta vacío.
