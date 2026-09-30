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
- D26 permanece sin cambios y con decisión de alternativa pendiente; se documentan opciones por systemId y scope de compatibilidad, sin afirmar inventario de datos ni permisos disponibles para todos los usuarios.
- Descripción local reescrita con evidencia actual y bloqueantes visibles; no se alteraron la descripción ni los comentarios remotos.

## Validación

- Regresión: 4.097 tests, cero fallas/errores, dos skips; 97,16% de cobertura. Los 51 selectores pasaron.
- Gate MySQL falló por orden de migraciones previo; cleanup propio verificado. Corrección de seis archivos staged, sin commit/push; conflictos contra develop pendientes.
- Sin Zord por instrucción del owner; sin smoke ni mutaciones remotas.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** sin secretos ni payloads reales.

## Rollback

- Restaurar sólo los ajustes de contrato y estado de esta fecha; conservar la bitácora histórica de las decisiones previas.
