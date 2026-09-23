---
type: change_log
schema_version: 1
scope: session
created: "2026-09-23"
updated: "2026-09-23"
area: "[[Meli]]"
project: "[[SIG-616 — Autorización de operaciones por equipo]]"
application: "[[rio-playmaker]]"
entities:
  - "[[SIG-616 — Autorización de operaciones por equipo]]"
related:
  - "[[SPEC técnica — Slice 4 — Relaciones y pipelines]]"
  - "[[Descripción PR — rio-playmaker — Slice 4]]"
  - "[[SPEC técnica — Slice 5 — Actions restantes]]"
  - "[[Descripción PR — rio-playmaker — Slice 5]]"
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

# 2026-09-23-sig-616-autorizacion-entity-updated

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/SIG-616 — Autorización de operaciones por equipo.md`
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/SPEC técnica — Slice 4 — Relaciones y pipelines.md`
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/Descripción PR — rio-playmaker — Slice 4.md`
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/SPEC técnica — Slice 5 — Actions restantes.md`
  - `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/Descripción PR — rio-playmaker — Slice 5.md`

## Motivo

- Slice 3 fue mergeado y su rama eliminada; Slice 4 cambió de base efectiva a `develop`, recibió la
  regularización config-backed y el cascade trasladado, y obtuvo nueva evidencia de tests, coverage,
  CI y versiones de prueba. Esa información cambia el estado vigente del proyecto.
- F5 requería incorporar la corrección F4 `e75ca90d9` y actualizar su evidencia y base efectiva.
- El comentario humano de PR #1182 detectó tipos Flink inválidos y cobertura GCP faltante; el usuario pidió familias abstractas y configuración YAML sin ampliar los casos de uso.

## Fuentes usadas

- Git remoto y API de GitHub para PR #1178/#1181.
- F3 en `develop@19d70a6cf`, tip posterior observado `origin/develop@9a559dfb3`, F4 inicial
  `d792b902b` y corrección publicada `e75ca90d9`.
- Resultados locales de Gradle, contrato ejecutable, JaCoCo y Fury CLI.
- Rama publicada `feature/operation-authorization-by-team-f5@dfc26fda7`, PR #1182 y resultados locales de 24 selectores, dos checks L0/LOCAL_STACK y `./gradlew check`.
- Tipos admitidos por Control Plane en `develop` consultados desde GitHub; F5 corregida y publicada como `a89fcffcb`, PR #1182 con base F4 `e75ca90d9` y `MERGEABLE`.

## Resolución aplicada

- Se reemplazó el estado obsoleto de Slice 3/4 por los hashes y gates actuales, se eliminó la falsa
  regla same-DP del alcance vigente y se documentaron las ramas/versiones no productivas sin
  declarar deploy ni smoke manual.
- El comentario de compatibilidad de #1181 se clasificó como regresión real; el estado canónico
  refleja el bypass histórico restaurado, la evidencia con configuración real y las versiones
  test3 nuevas que incorporan `e75ca90d9`.
- Se registró el merge de F4 en F5, la matriz combinada, el diff F4→F5 acotado a nueve archivos, la base y descripción actualizadas de PR #1182 y el smoke aún pendiente.
- Se agregaron `component-families` y `family-permissions` a YAML: `flink-sql` agrupa `flink-sql`/`gcp-flink-sql`; `flink-job` agrupa `aws-flink-job`/`gcp-flink-job`. Las reglas F2–F4 siguen exactas o wildcard como antes. Eliminar un permiso familiar apaga el guard adicional de la Action para sus miembros sin alterar el caso de uso.

## Validación

- Se verificaron HEAD/base remotos, mergeability, checks verdes, coverage diferencial/global,
  ausencia de conflictos y derivación de ambas ramas mock desde `d792b902b`.
- Para F5 se verificaron contratos del repositorio, 24 selectores focalizados, dos checks locales con cleanup, suite completa de 4.077 tests (0 fallas, 2 skips), HEAD/base remotos y `MERGEABLE`; la CI remota continúa en curso.
- La corrección F5 pasó los contratos, 25 selectores, ambos checks locales con cleanup y `./gradlew check` con 4.086 tests (0 fallas, 0 errores, 2 skips). El nuevo HEAD remoto y la base F4 se verificaron; el smoke Tiger/ACME no productivo sigue pendiente.
- JaCoCo local pasó y reportó 31/31 líneas cubiertas en `ConfiguredActionPermissionProvider`; este dato no sustituye el check remoto de cobertura abortado.
- [CI #5490](https://rp-ci-java.furycloud.io/job/rio-playmaker/5490/) falló antes del checkout de la aplicación: Git no confió en el certificado al obtener `fury_rp-ci-pipelines.git`. Los checks de cobertura y dependencias fueron abortados por ese fallo; la solicitud GitHub de reejecución devolvió 404. La descripción del PR se actualizó con esta limitación.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sí; sin tokens, payloads ni secretos.

## Rollback

- Restaurar las notas afectadas desde el historial del vault si la evidencia remota fuese invalidada; el merge y el PR se gestionan en GitHub.
