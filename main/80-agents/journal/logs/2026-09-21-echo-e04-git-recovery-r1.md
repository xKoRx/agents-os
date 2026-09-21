---
type: change_log
schema_version: 1
scope: session
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Personal]]"
project: "[[Echo — Producto Integrado]]"
application:
entities:
  - "[[Echo]]"
  - "[[Aranea]]"
related:
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[Echo + Echo Forge — Deferred Certification Backlog]]"
  - "[[Echo — E-04 Forge Ingestion E1]]"
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

# 2026-09-21 — E-04 git recovery R1 (publicación de commits certificados; fix seguridad ETCD; renumeración 064→068)

## Cambios

- **`xKoRx/echo` — branch `feature/e04-dev-ingest-recovery` publicada:** FF `2360369c..4aad647b` a origin, read-back verificado; `origin/master` intacto `5dd998f1`. Commits nuevos de esta sesión: `988e0ae6` (fix seguridad: dump mirror ETCD development→production de v1 exige aprobación explícita/endpoints explícitos/unlock production; `DeleteVar` con guarda de tests en v1/v2) y `4aad647b` (rename puro `064_strategy_version_forge_platform` → `068_`; colisión con `064_reference_enrollment_binding` de E-06 resuelta contra el DAG completo; 065/066/067 ocupados por E-07/08/09).
- **Documentación (delta, sin duplicar certs):** [[Echo + Echo Forge — Deferred Certification Backlog]] delta `E04_RECOVERY_PUBLISHED` 2026-09-21T13:0xZ; [[Echo — E-04 Forge Ingestion E1]] (bullet de estado, tabla de entrega `4aad647b PUBLICADA`, bitácora); [[Echo — Producto Integrado]] (estado: publicación + siguiente carril E-08 C3; bitácora); [[Echo + Echo Forge — Environment Contract]] (§5.6 nueva; §7 filas de publicación y migraciones reconciliadas).

## Motivo

- Misión ECHO MANAGER RECOVERY R1: los commits E-04 desplegados y certificados (`2498042f`, `3d260e81`) existían sólo localmente en Daedalus; la misión ordena recuperarlos, verificarlos y publicar la feature branch de forma segura sin re-certificar ni tocar runtime.
- Hallazgo material de seguridad durante §5: `v1/sdk/etcd/example_test.go:TestEtcdDumpUtility` escribía `/sqx-flowkit/production/` del clúster real desde `go test` ordinario (helper `put()` interno salta el guard de `SetVar`); corregido de forma mínima con regresiones herméticas, sin re-ejecutar la ruta contra el clúster compartido.

## No cambió

- Runtime DEV: Gateway PID 2543059 (binario `3d260e81`), Core PID 2479388 (`5dd998f1`) — sin restart. PROD, workers SQX/MT5, screen `deployer`: intactos. CERT-E04-01/CERT-F04-03: PASS previos no re-ejecutados ni duplicados. E-09 (`0798ce4a`): intacto. `origin/master`: intacto.

## Pendientes (owner)

- Restaurar `/echo/production/postgres/password` desde historial ETCD (sigue en seed de prueba).
- Verificar integridad `/sqx-flowkit/production/` (105 keys espejan development; condición: `mod_revision` > 2026-09-21T12:20Z ⇒ contaminación de la corrida de este día ⇒ reconciliar y evaluar impacto en workers flowkit).
- Retirar credenciales versionadas del repo (`scratch_query_test.go`).
- Deuda estructural: `echo-develop` sin tabla de control de migraciones (aplicación manual); 061 parcial (`strategy_definitions.id` `varchar(64)`).
