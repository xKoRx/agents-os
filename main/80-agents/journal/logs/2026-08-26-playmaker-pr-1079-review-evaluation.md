---
type: change_log
schema_version: 1
scope: session
created: "2026-08-26"
updated: "2026-08-27"
area: "[[Meli]]"
project: "[[Playmaker — Doble dispatch al avanzar batches]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Playmaker — Doble dispatch al avanzar batches]]"
related:
  - "[[Auditoría independiente — Informe del doble dispatch]]"
  - "[[Descripción PR — rio-playmaker — Hotfix doble dispatch]]"
  - "[[RIO]]"
aliases:
  - Change log evaluación review PR 1079
confidence: verified
source_session:
source_feedbacks: []
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/meli
  - app/rio-playmaker
---

# 2026-08-26-playmaker-pr-1079-review-evaluation

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `updated` — `10-projects/Meli/Playmaker — Doble dispatch al avanzar batches/Playmaker — Doble dispatch al avanzar batches.md`
- **Detalle:** se agregó la sección `## 🔬 Revisión del PR #1079 — evaluación de los comentarios y guía de resolución`, insertada entre la revisión CP/KVS y las secciones forenses numeradas 1–14. La decisión del owner cierra el alcance operacional: QKVS compartido probado en `test2` y `bq-consumer-test-nonprod`; no se toca `stage`/`staging-nonprod`; contention reintenta por deadline y outage KVS hace fallback al comportamiento pre-hotfix con métrica. No-Op/log-and-skip/SecureRandom no son fixes adecuados por defecto.

## Motivo

El PR #1079 recibió *request changes* con once comentarios. La nota del proyecto no tenía dónde registrar qué de esa revisión resiste verificación independiente ni en qué orden atacarla, y esa evaluación es estado del proyecto, no historia de sesión.

## Verificación

Cada comentario se contrastó contra el diff de `origin/feature/serialize-batch-completed-listener@1eb04d0c` y sus consumidores. C1/H1/M3/M4 aplican; C2/M1 se observan con métricas; H2 queda validado para el rollout elegido por prueba de QKVS compartido; L1–L3 son menores. No-Op, log-and-skip y SecureRandom no se adoptan sin evidencia adicional.

## Implementación posterior

- Se creó un worktree aislado en `/tmp/rio-playmaker-pr1079-fix`, sin modificar el checkout activo del usuario.
- El lease queda en 7 s. El retry conserva backoff con jitter para contención sana y propaga un deadline monotónico desde el primer conflicto; al agotarse los retries agenda exactamente un probe no anterior a `primer conflicto + TTL + 100 ms`.
- `ErrorCode.CONFLICT.getCode()` identifica contención. Las demás `KvsClientException` y una excepción no tipada que salga del `save` de QKVS señalan indisponibilidad y ejecutan el comportamiento previo sin mutex; el mismo fallback se aplica si el scheduler no puede dejar programado el retry.
- Se agregaron cuatro métricas sin dimensiones dinámicas: acquired, contended, fallback con razón finita y hold-duration. No incluyen execution, batch, deployment, key, owner ni mensajes.
- La materialización parcial ahora envía sólo los componentes faltantes. Se simplificó `LockHandle` a `key` y `owner`.
- Se añadieron pruebas de carrera sobre `BatchAdvanceLockImpl` usando un fake create-only de KVS, más pruebas del fallback, probe final y materialización parcial.

La batería dirigida y `./gradlew test --no-daemon` terminaron sin fallas. Se creó y pusheó el commit `b20aa2474` (`fix: harden batch advance serialization`) a `origin/feature/serialize-batch-completed-listener`; tras un rechazo inicial de allowlist, el reintento quedó sincronizado. Queda observar p99/p99.9 de `hold_duration_ms` y declarar el cambio de segmento en la descripción del PR.

## Deltas que no se derivan del texto del review

- El horizonte actual de reintentos termina antes del TTL y no se corrige sólo por configuración. Con full jitter, incluso una suma máxima mayor que el TTL no garantiza liveness; se requiere un probe posterior al TTL basado en deadline monotónico.
- `actionsFramework.enabled: false` no acredita por sí solo que los containers del mutex nuevo falten. Antes de rollout se debe validar en Fury el container, segmento, permiso y operación create-only de cada scope.
- El envío al control plane ocurre fuera de la transacción de dispatch (`AFTER_COMMIT` + `@Async`), así que el riesgo de expiración del TTL es de cola de latencia de DB y tamaño de batch, y es medible.
- `checkPrerequisites` tiene un solo llamador de producción y `DeploymentTimeoutJob` sólo actúa sobre deployments en `REQUESTED`/`STARTED`: un batch nunca despachado no tiene deployment, así que el stall es permanente.
- El lock gobierna también `propagateFailure` y `checkGroupCompletion`, no sólo el dispatch, así que perder un evento tiene más radio de impacto del descrito.
- `ThreadLocalRandom` no es un problema de seguridad para un jitter de backoff; sólo se cambiaría ante evidencia de un gate aplicable.

## Discrepancia registrada

El review pide consolidar `BatchAdvanceLock` sobre una versión generalizada de `DataProductActionLock` dentro de este PR. La evaluación sostiene que eso **no** debe bloquear el merge: los dos bugs concretos que el review atribuye a la duplicación se arreglan directamente, y generalizar obliga a reimplementar el lock de acciones que ya está en producción dentro de un hotfix P1. Queda como deuda separada.
