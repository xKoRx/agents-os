---
type: known_error
schema_version: 1
scope: project
created: "2026-08-28"
updated: "2026-08-28"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[xKoRx/symphony]]"
related:
  - "[[2026-08-28-durable-artifact-verified-reads-apply-correction]]"
aliases: []
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-APPLY-CORRECTION-NORMAL
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - scope/project
---

# 2026-08-28-embedded-postgres-shm-init-failure

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Las suites PostgreSQL que usan `postgrestest.OpenIsolatedDB` fallaban durante `initdb` con `could not create shared memory segment: No space left on device`.

## Causa

- Host Darwin 25.5.0 x86_64; `/dev/shm` no existe como mount; `/private/tmp` tenía 38 GiB libres e inodos disponibles; `kern.sysv.shmmni=32` y `ipcs -m` mostró exactamente 32 segmentos SysV más 256 sets de semáforos.
- Los 32 masters eran instancias `sqx-embedded-postgres-*` del usuario de la sesión, con `PPID=1`, puertos loopback y antigüedad de hasta cuatro días; no había runner Go activo ni PostgreSQL no-harness.
- `postgrestest.OpenDB` inicia el embedded PostgreSQL compartido sin registrar `ep.Stop` en `t.Cleanup`, por lo que runners terminados dejan procesos y recursos IPC huérfanos.

## Impacto

- El límite de 32 segmentos impedía crear otra instancia y bloqueaba declarar PASS de las integraciones PostgreSQL aunque el código compilara.

## Detección

- La evidencia mínima fue `uname -a`, `df -h`, `df -i`, `mount`, `sysctl kern.sysv`, `ipcs -a`, `ps auxww | grep -i postgres` y búsqueda de `OpenDB`/`OpenIsolatedDB` en el harness.

## Mitigación

- Se detuvieron graciosamente sólo los 32 masters identificados con `runtime/bin/pg_ctl -D ... -m fast -w`; luego se eliminaron 41 directorios temporales por-PID con el patrón inequívoco `sqx-embedded-postgres-*`; el cache compartido se dejó intacto.
- Verificación posterior: 0 masters/procesos PostgreSQL embedded, 0 segmentos SysV y 0 sets de semáforos; migrations y StageProducerOutput pasaron en PostgreSQL real embedded.

## Evidencia

- `go test ./sqx/adapters/registry-postgres/migrations -count=1` PASS; `go test ./sqx/adapters/registry-postgres -count=1` y el comando combinado ejecutaron PostgreSQL sin SHM failure, pero conservaron fallos baseline de Strategy Identity/origin membership fuera de Apply.
- No modificar el código de persistencia para ocultar el fallo ni reportar PASS inventado; el cleanup sólo afectó procesos temporales del harness claramente huérfanos.
