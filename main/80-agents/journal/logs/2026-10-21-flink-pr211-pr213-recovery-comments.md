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
- **Estado nuevo:** #211 @ `5a688903` y #213 @ `f681eb88`, publicados, worktrees limpios, siete hilos resueltos y todos los CI finales PASS. Verificación final posterior al bot sobre ambos SHA: cero hilos abiertos y MERGEABLE; listos para pedir review humano.

## Motivo y resolución

Se corrigieron dos variantes de recuperación: envío incierto sin job físico y DELETE aplicado con respuesta perdida. Python conserva el caché de ZIPs y libera sus extracciones tras confirmar la terminación; los fallos de borrado conservan ownership para reintento. Un comentario adicional del bot exigió separar el resultado de /run del DELETE del upload: se preservan el job sano y el error original, se retienen handles por app y se impide eliminar la app hasta completar la limpieza. La sincronización final conserva Python y aplica el contrato nuevo de uploads. El proyecto cambia porque cambiaron los SHA y la evidencia vigente.

## Validación

- Fuentes: [F1](https://github.com/melisource/fury_rio-controlplane-flink/pull/211#discussion_r4338529315), [F2](https://github.com/melisource/fury_rio-controlplane-flink/pull/211#discussion_r4338529329), [DELETE del upload](https://github.com/melisource/fury_rio-controlplane-flink/pull/211#discussion_r4339386820) y [limpieza Python](https://github.com/melisource/fury_rio-controlplane-flink/pull/213#discussion_r4338567149).
- Repo `fury_rio-controlplane-flink`: `src/local`, `src/localTest`, `local/README.md` y `local/e2e.py`; sin diff en `src/main` ni `src/test` contra `origin/develop`.
- 1937 tests productivos PASS por rama; 50 locales en #211 y 74 en #213. Hooks de seguridad, formato, Checkstyle y PMD PASS antes de cada commit, incluidos merges.
- Baseline: 3 regresiones fallan contra `6847ab66`; 6 regresiones Python fallan contra `ce8325cc`; suites corregidas PASS. Las 7 variantes de limpieza de uploads cubren éxito/rechazo/respuesta vacía, pérdida de respuesta, 404 y aislamiento entre apps.
- Reconciliación y uploads: 100% líneas/ramas. Extractor Python: 56/58 líneas y 18/18 ramas.
- E2E completo SQL/UPDATE/fallas/CRUD/JAR/UPDATE/cache hit PASS en `1178e1d6`. Probe de SQL Gateway Flink 1.20.5 real confirma el HTTP 500 con el SqlGatewayException y handle exactos tras repetir DELETE.
- Python físico PASS en `8f5af09d`: UDF, stop/start, re-provisión sin nueva descarga y volumen vacío. Smoke final integrado PASS en `f681eb88`: JAR con file sink, ambos uploads eliminados del JobManager, Python UDF, DEPROVISION, jobs terminales y volumen de extracciones vacío. No se repitió la suite física completa después del último fix; se probaron sus caminos modificados.
- `LocalFlinkJarFiles`, `LocalFlinkJobRecovery` y `LocalFlinkHttpException` tienen blobs iguales entre `5a688903` y `f681eb88`. El JAR host/runtime final coincide por SHA256 `d82b74223d3ccc59b95e32dbd767d9d6e04cda1391caf5c944f75f5d436ecd4b`.
- Cada corrida terminó con 0 contenedores/0 redes rio-*; volumen Python propio eliminado y VM encendida.
- Hilos: 0 abiertos por PR tras resolver 7, verificados después del último resultado del bot sobre ambos SHA finales; ambos MERGEABLE. CI Fury #1380 (#211) y #1379 (#213), cobertura, dependencias, estático, workflow y CodeQL PASS sobre `5a688903`/`f681eb88`; Code Reviewer NEUTRAL en ambos. La reconsulta final de comentarios y checks fue exitosa tras confirmar el usuario GlobalProtect conectado.
- Hubo rechazo intermitente por IP allowlist; se pidió verificar GlobalProtect, se recuperó acceso para publicar y resolver hilos, y volvió a bloquearse al reconsultar los reviews finales. El usuario confirmó GlobalProtect conectado y la verificación final recuperó acceso. No se cambió de VPN. Docker Bake requirió un permiso acotado para el secret de pip ya configurado; no se leyó ni registró su contenido.

## Compartibilidad

Scope local; sin secretos ni dumps. Modelo exacto no expuesto por el host, registrado como unknown en [[2026-10-21-codex-unknown-flink-recovery-comments]].

## Rollback

Conservar evidencia histórica y corregir únicamente las filas y la entrada vigente de [[CP Flink local]]. Los cambios de código están en commits separados, sin rebase, amend ni force-push.
