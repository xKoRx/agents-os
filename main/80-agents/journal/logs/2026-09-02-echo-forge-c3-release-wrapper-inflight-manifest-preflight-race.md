---
type: change_log
schema_version: 1
scope: session
created: "2026-09-02"
updated: "2026-09-02"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related: ["[[2026-09-02-release-wrapper-inflight-manifest-preflight-race]]"]
aliases: []
confidence: verified
source_session: ECHO-FORGE-C3-RELEASE-AND-CERT-RETRY-NORMAL
source_feedbacks: ["[[2026-09-02-echo-forge-c3-release-and-cert-retry-normal-session-feedback]]"]
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/echo-forge
---

# Echo Forge C3 release wrapper in-flight manifest race

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `80-agents/memory/public/known-error/symphony/2026-09-02-release-wrapper-inflight-manifest-preflight-race.md`

## Motivo

- Persistir un blocker físico repetible observado durante la publicación de 0.2.85.

## Fuentes usadas

- Fuente principal: `xKoRx/symphony` authority JSON, release output, local manifest/hashes y `deployer_screen.log`.

## Resolución aplicada

- Se creó un known error compacto y se enlazó al checkpoint, agent run y feedback de la sesión.

## Validación

- La authority inicial y target preflight fueron PASS; el release wrapper salió `1` durante el intervalo artefactos-remotos/manifest-antiguo; posterior relectura exacta fue `EXACT_MATCH`. La misión se cerró sin reanudar automáticamente.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Reversible eliminando el known error y este log si evidencia posterior demuestra que fue un caso único; no se modificaron artefactos del repo ni MinIO.
