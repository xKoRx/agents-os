---
type: change_log
schema_version: 1
scope: session
created: "2026-10-21"
updated: "2026-10-21"
area: "[[Meli]]"
project: "[[CP Flink local]]"
application: "[[rio-controlplane-flink]]"
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

# Comentarios de recuperación — PR 211 y 213

## Cambio

- **Tipo:** updated.
- **Archivo:** `10-projects/Meli/RIO E2E local/CP Flink local.md`.
- **Estado anterior:** #211 @ `6847ab66` y #213 @ `438d2b9b`, certificados antes de los nuevos comentarios.
- **Estado nuevo:** fixes publicados en #211 @ `1178e1d6` y #213 @ `2b5ff6ae`; validación física nueva pendiente de completar.

## Motivo y resolución

Se abordaron dos variantes de recuperación no cubiertas: envío incierto sin job físico y DELETE aplicado con respuesta perdida. En Python se separó el caché de ZIPs de las extracciones por ejecución, que se liberan tras confirmar la terminación. El proyecto se actualiza porque cambiaron los SHA y la evidencia vigente, no por actividad administrativa.

## Validación

- Hilos [F1](https://github.com/melisource/fury_rio-controlplane-flink/pull/211#discussion_r4338529315), [F2](https://github.com/melisource/fury_rio-controlplane-flink/pull/211#discussion_r4338529329) y [limpieza Python](https://github.com/melisource/fury_rio-controlplane-flink/pull/213#discussion_r4338567149).
- Repo `fury_rio-controlplane-flink`: `src/local`, `src/localTest`, `local/README.md` y `local/e2e.py`; sin cambios en `src/main` ni `src/test` contra `origin/develop`.
- 1937 tests productivos PASS por rama; 43 locales en #211 y 67 en #213. Hooks de seguridad, formato, Checkstyle y PMD PASS antes de cada commit.
- Baseline: 3 regresiones fallan contra `6847ab66`; 6 regresiones Python fallan contra `ce8325cc`. Las suites corregidas pasan.
- Reconciliación: 100% líneas/ramas. Extractor Python: 56/58 líneas y 18/18 ramas.
- E2E físico #211 completo PASS en `1178e1d6`; JAR host y runtime iguales por SHA256; teardown 0 contenedores/0 redes rio-*. Python físico #213 en curso. CI Fury de #211 iniciado; CodeQL PASS. GitHub empezó a rechazar por IP allowlist durante la validación; se pidió verificar GlobalProtect.
- Ajuste adicional local `8f5af09d` conserva el ownership de una extracción inválida si falla su borrado y reintenta antes de otro start. 67 tests locales y hooks PASS; push pendiente de recuperar acceso.
- Probe contra SQL Gateway Flink 1.20.5 real confirma HTTP 500 con el SqlGatewayException y handle exactos tras repetir DELETE.

## Compartibilidad

Scope local; sin secretos ni dumps.

## Rollback

Para corregir el estado del proyecto, conservar la evidencia histórica y editar únicamente las filas y la entrada vigente.
