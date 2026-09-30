---
type: change_log
schema_version: 1
scope: session
created: "2026-09-30"
updated: "2026-09-30"
area: "[[Meli]]"
project: "[[SIG-616 — Autorización de operaciones por equipo]]"
application: "[[rio-playmaker]]"
entities: []
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# SIG-616 F4 — Limpieza autorizada de relaciones cross-DP históricas

## Cambio

- **Tipo:** updated.
- **Archivo(s):** [[SIG-616 — Autorización de operaciones por equipo]], [[SPEC técnica — Slice 4 — Relaciones y pipelines]] y [[Descripción PR — rio-playmaker — Slice 4]].

## Motivo

- El owner autorizó corregir el delete que bloqueaba relaciones cross-DP históricas y pidió alternativas al ownership obligatorio sin regularización masiva.

## Fuentes usadas

- Instrucción directa del owner, comentarios del PR 1181 y código de su branch en HEAD 1c9f1aba7.
- Pruebas unit con el autorizador real, HTTP/H2, regresión completa, checks locales y estado remoto del PR.

## Resolución aplicada

- D25 y la SPEC distinguen create/update same-DP de delete histórico con guards de ambos owners persistidos.
- D26 permanece sin cambios productivos y el owner ratificó su excepción de compatibilidad, aceptando expresamente que Tiger-only no prueba permiso de borrado. No se adoptan los respaldos alternativos ni se exige backfill masivo.
- Descripción local y remota alineadas con la decisión final, publicadas sobre `99c51fe8b`. Respuestas verificadas y todos los hilos resueltos; aprobación humana pendiente.
- Merge de `develop@0c9e9e3ee` sin reescribir historia. Runner MySQL aplica la migración CHECK antes del DROP histórico; runner Kafka detecta Jetty/Tomcat. No se cambió SQL ni se desactivaron constraints o tests. OpenAPI sincronizado con anotaciones de catálogo/importación.

## Validación

- Regresión final: 4.129 tests, cero fallas/errores, 2 skips; 97,19% de cobertura. Los 53 selectores y tres checks L0/LOCAL_STACK pasaron, con cleanup certificado.
- Publicación verificada en `99c51fe8bd3da2e73ede96ae717a1ab1fae723c7`; dependencies FAIL; los demás checks publicados pasaron; PR MERGEABLE / BLOCKED / REVIEW_REQUIRED.
- Sin Zord por instrucción del owner; sin smoke remoto, merge del PR ni deploy. Los fallos iniciales del runner se resolvieron antes de publicar.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin secretos ni payloads reales.

## Rollback

- Restaurar sólo los ajustes de contrato y estado de esta fecha; conservar la bitácora histórica de las decisiones previas.
