---
type: project
schema_version: 1
owner: me
root: false
status: active
priority: P2
area: "[[Meli]]"
parent: "[[RIO E2E local]]"
sprint:
start: "2026-10-13"
due:
progress: 90
repo:
jira:
prs: ["https://github.com/melisource/fury_rio-controlplane-flink/pull/209", "https://github.com/melisource/fury_rio-controlplane-flink/pull/211", "https://github.com/melisource/fury_rio-controlplane-flink/pull/213"]
aliases: []
tags:
  - kind/project
  - area/meli
  - project/cp-flink-local
created: "2026-10-13"
updated: "2026-10-21"
---

# CP Flink local

## 🎯 Objetivo

CP Flink levantable en local con los flujos que soporta develop, sin Playmaker.

## 📊 Estado actual

**Actualización 2026-10-22:** los tres PRs de esta serie están mergeados según el owner; GitHub confirma #211 squash `74cc6f96` y #213 squash `920a7075`. La tabla inferior conserva la evidencia previa al merge. Ya no quedan review/retarget pendientes de la serie; la próxima entrega es integración con Playmaker sobre develop fresco. #214 también está mergeado. El transporte local de deployments y resultados existe; actions standalone entra por HTTP directo y falta completar su consumo Kafka para integrarlo con PM. No se repitió E2E en esta retoma.

| PR | Alcance | Rama / PR | Estado |
|---|---|---|---|
| 1 | SQL PROVISION, DEPROVISION, acciones start/stop y estado en runtime | `feature/rio-e2e-local-flink-kiss` @ `05d46cfd` · [#209](https://github.com/melisource/fury_rio-controlplane-flink/pull/209), base `develop` | Mergeado a `develop` el 2026-10-19 como squash `0b60e64b` (un solo padre); aprobado, CI verde |
| 2 | SQL UPDATE + CRUD HTTP de SQL + JAVA/JAR | `feature/rio-e2e-local-flink-pr2` @ `5a688903` · [#211](https://github.com/melisource/fury_rio-controlplane-flink/pull/211), base `develop` | F1/F2 corregidos en `1178e1d6`: ausencia 404 acotada de jobs inciertos y cierre idempotente con error de sesión ausente e identidad exacta. Comentario nuevo del bot corregido en `5a688903`: DELETE de upload no cancela un job sano ni reemplaza el error de /run; handles retenidos por app para reintento y borrado final. 1937 productivos + 50 locales y hooks PASS; reconciliación y uploads 100% líneas/ramas. E2E completo PASS en `1178e1d6`, cleanup 0/0 y probe SQL Gateway real PASS; smoke integrado JAR/Python PASS en `f681eb88`, helpers compartidos iguales a #211 y cleanup 0/0. Tres hilos resueltos; CodeQL PASS en el SHA nuevo, CI Fury #1380, cobertura, dependencias, estático y CodeQL PASS en `5a688903`; Code Reviewer NEUTRAL. Verificación final posterior al bot: cero hilos abiertos, MERGEABLE y listo para pedir review humano |
| 3 | PYTHON/ZIP | `feature/rio-e2e-local-flink-pr3` @ `f681eb88` · [#213](https://github.com/melisource/fury_rio-controlplane-flink/pull/213), base #211 | Limpieza inmediata de extracciones inválidas y liberación de válidas tras terminación confirmada; retención ante lanzamiento/cancelación inciertos y reintento ante fallo de disco, incluidos inválidos (`2b5ff6ae`, `8f5af09d`). Merge final de #211 `f681eb88`, con resolución conservadora del launcher y README. 1937 productivos + 74 locales y hooks PASS; extractor 96,55% líneas/100% ramas. E2E Python físico en `8f5af09d` PASS (UDF, stop/start, cache hit, volumen vacío y cleanup 0/0); smoke integrado JAR/Python PASS en `f681eb88`, helpers compartidos iguales a #211 y cleanup 0/0. Cuatro hilos resueltos; CI Fury #1379, cobertura, dependencias, estático y CodeQL PASS en `f681eb88`; Code Reviewer NEUTRAL. Verificación final posterior al bot: cero hilos abiertos, MERGEABLE y listo para pedir review humano |

Fuera de alcance: GCP y Playmaker; la integración Playmaker se entrega aparte, apilada como en ClickHouse.

JAR de PR 2: stub Nexus con nginx oficial y TopSpeedWindowing.jar de la imagen Flink; queries y validación de paths productivas conservadas, HTTP sólo para `nexus-local`. El SHA `0728044c` conserva ConcurrentHashMap y omite entryClass/programArgs con valor null. Certificación registrada el 2026-10-14: 1937 tests productivos, 20 locales y pre-commit PASS; E2E físico completo PASS en una corrida, con cache hit de JAR sin descarga nueva desde Nexus y SQL retenido después de DEPROVISION. En esa corrida se verificó cleanup con 0 contenedores y 0 redes `rio-*`, VM sana y encendida, worktree limpio y src/main/src/test sin diff contra develop y la base `c0cabe72`. Descripción en inglés publicada y verificada contra [[Descripción PR — rio-controlplane-flink (E2E local PR 2)]]. El traspaso del 2026-10-19 añadió sólo el seguimiento opcional; no modificó la rama de PR 2 ni repitió esa certificación.

### ▶ Próxima sesión: E2E con Playmaker + CP Flink

- **Objetivo:** integrar Playmaker con el CP Flink en el E2E local y validar todos los flujos de la serie (SQL, SQL UPDATE, SQL CRUD, JAVA/JAR, PYTHON/ZIP, stop/start, runtime status, fallas) end-to-end vía Playmaker, como un PR propio en `fury_rio-playmaker`.
- **Patrón a seguir:** la integración ClickHouse, ya mergeada: PM [#1286](https://github.com/melisource/fury_rio-playmaker/pull/1286) (Kafka) y [#1288](https://github.com/melisource/fury_rio-playmaker/pull/1288) (ClickHouse, `feature/rio-e2e-local-clickhouse-kiss`, worktree `rio-playmaker-rio-e2e-clickhouse`). Hub de integración: Playmaker `local/RIO_E2E.md`, que hoy registra a Flink como gap.
- **Base CP Flink:** `feature/rio-e2e-local-flink-pr3` @ `f681eb88` contiene la serie completa; si #211/#213 se mergean antes, usar `develop`. Validación standalone vigente: prompt de QA de la sesión 2026-10-20 (no persistido).
- **Contrato Flink que Playmaker consume:** `describeApp` = salud (FAILED gana: un PROVISION con FAILED+RUNNING falla); `describeForDeletion` = actividad (stop/update/delete); `create()` idempotente; resultados en `rio-deployment-result-local` y `rio-action-result-local`; runtime en `rio-component-runtime-status-local` (POLL cada 60 s).
- **Riesgos conocidos:** undeploy = develop-gap en Playmaker (`already_terminal`/`terminal_component_run`), no se toca; PRs abiertos de otra sesión que cambian estados: CP Flink [#214](https://github.com/melisource/fury_rio-controlplane-flink/pull/214) (gate de última acción) y PM [#1318](https://github.com/melisource/fury_rio-playmaker/pull/1318) (SIG-650, FAILED sobre servicios terminados). Regla dura: sólo implementación local, sin lógica de negocio.
- **Comportamientos de develop que el E2E con Playmaker va a observar (QA 2026-10-21, no son bugs de la serie):** (1) un PROVISION repetido sobre una app RUNNING redepliega: `CheckToCreateAppInAWSHandler` la deriva a STOP_TO_UPDATE → update → start, igual que KDA, y reemplaza los job IDs sin duplicarlos; (2) `PublishStateChangeCommand` publica RUNNING→READY como `FAILED` hacia Playmaker, de modo que un stop legítimo visto por el POLL de 60 s sin pasar por STOPPING llega como FAILED; es el falso FAILED que aborda CP Flink #214.
- **Pendientes de esta serie:** ninguno de merge/review; continuar integración Playmaker desde `develop` que incluya #213 y #214.
- **Plan vigente de la integración (2026-10-22):** [[RIO E2E local — Integración Flink Playmaker]]. Reemplaza este brief como autoridad de diseño, fases y gates.

## ✅ Tareas

- [x] En PR 2 (#211), conservar el handle de la sesión de reemplazo si fallan el DELETE anterior y el de compensación; reintentar el cierre y ampliar `retainsOriginalStateWhenReplacementSessionCleanupAlsoFails` para demostrar la recuperación. [Seguimiento](https://github.com/melisource/fury_rio-controlplane-flink/pull/211#issuecomment-6276874011) · [sugerencia de Karla](https://github.com/melisource/fury_rio-controlplane-flink/pull/209#discussion_r4318564696). #owner/me #type/dev #area/meli
- [ ] Fix en develop del doble dispatch de CreateAppInAWSHandler y StartAppInAWSHandler que compensa LocalFlinkEventMulticaster; entrega fuera de local. #owner/me #type/dev #area/meli
- [ ] Corregir `component_type: null` en el resultado del undeploy; entrega fuera de local. #owner/me #type/dev #area/meli

## 📆 Bitácora

- **2026-10-21 — revalidación F1/F2 y limpieza Python:** fixes publicados en `1178e1d6`, `5a688903` (#211), `2b5ff6ae`, `8f5af09d` y merge `f681eb88` (#213). Incluye el comentario nuevo del bot sobre DELETE de uploads: conserva el job sano y el error original, retiene handles y reintenta por dueño. 1937 productivos por rama, 50/74 locales y hooks PASS; E2E completo #211 en `1178e1d6` y Python en `8f5af09d` PASS, ambos con cleanup 0/0. Siete hilos corregidos/resueltos. Acceso GlobalProtect recuperado; smoke final integrado PASS en `f681eb88`, cleanup 0/0; todos los CI/checks finales PASS (Code Reviewer NEUTRAL); verificación final posterior al bot completada: cero hilos abiertos y ambos MERGEABLE, listos para pedir review humano. [[2026-10-21-flink-pr211-pr213-recovery-comments]].

- **2026-10-21 — PR 3:** merge conservador de #211 vigente y tres comentarios de #213 aplicados/publicados en `438d2b9b`. UPDATE Python ya no reutiliza módulos ni archivos requeridos de un ZIP anterior; nombres seguros y extensión nula cubiertos. 1937 productivos + 53 locales y hooks PASS, extractor 100% líneas/ramas; E2E físico completo PASS sobre el JAR publicado, tres extracciones Python distintas con permisos 755, cleanup 0 contenedores/0 redes rio-* y volumen propio eliminado. Checks CI/CodeQL/cobertura/dependencias/análisis estático/workflow PASS. [[2026-10-21-flink-pr213-review-comments]].

- **2026-10-21:** comentarios de #211 atendidos en `48de148b` (UPDATE) y `44adcafd` (JAR/properties), publicados en la rama del PR. 1937 tests productivos + 33 locales y hooks staged PASS; cinco nuevas regresiones fallan sobre el código previo. Tres hilos humanos respondidos y resueltos. E2E físico completo PASS y cleanup 0/0 en `44adcafd`. Dos bordes posteriores del bot corregidos en `febd460f` (rechazo JAR 4xx) y `6847ab66` (DELETE con sesiones pendientes): 1937 productivos + 36 locales y hooks staged PASS; cinco hilos respondidos/resueltos. Recertificación física completa PASS en `6847ab66` (incluye SQL, UPDATE, CRUD, JAVA/JAR y cache hit), cleanup 0/0, CI y CodeQL PASS, Code Reviewer NEUTRAL sin nuevos hilos. Worktree limpio, sin diff en src/main/src/test contra origin/develop. PR 3 conserva su base anterior `91cdd5f8`; no se sincronizó en este trabajo. [[2026-10-21-flink-pr211-review-comments]].

- **2026-10-20:** descripciones de #211 (`feature/rio-e2e-local-flink-pr2` @ `91cdd5f8`, base `develop`) y #213 (`feature/rio-e2e-local-flink-pr3` @ `e7e12bff`, base #211) reescritas como serie alineada con #209 y publicadas en GitHub: [[Descripción PR — rio-controlplane-flink (E2E local PR 2)]] · [[Descripción PR — rio-controlplane-flink (E2E local PR 3)]].
- **2026-10-20:** #209 entró como squash, así que #211 quedó con conflictos en 9 archivos y sin los últimos 5 commits de PR 1. Se mergeó `feature/rio-e2e-local-flink-kiss` en PR 2 (`9d3253ac`) y luego `develop` (`67081cde`). En la resolución: la ejecución SQL delega en `LocalFlinkSqlOperations`; `update()` registra el reemplazo sin pasar por el `create()` idempotente de PR 1 y valida con la vista de actividad; cancelación y reemplazo de sesión pasan a `LocalFlinkJobLauncher` por PMD GodClass. Mejora de Karla en `03e681b7`: el handle de la sesión de reemplazo se conserva y el siguiente stop reintenta cerrarlo. El caso FAILED+RUNNING de `local/e2e.py`, roto también en develop, ahora lee desde el offset actual (`91cdd5f8`). PR 3 re-sincronizado (`c6fd48cf`, `e7e12bff`), con la extracción ZIP en `LocalFlinkPythonArchive`. E2E físico PASS en ambas ramas. Seguimiento respondido en [#211](https://github.com/melisource/fury_rio-controlplane-flink/pull/211#issuecomment-6305674796). Pendiente: pedir review de #211.

- **2026-10-19:** #209 recuperado con commit vacío `05d46cfd`; Fury #1356 y CodeQL PASS, sin cambios de archivos en el relanzamiento. Descripción existente modificada en GitHub y [[Descripción PR — rio-controlplane-flink (E2E local)]]. La mejora opcional de Karla quedó pendiente en #211 y fue [respondida con la referencia cruzada](https://github.com/melisource/fury_rio-controlplane-flink/pull/209#discussion_r4318662950). Próximo: implementarla y validarla en PR 2. [[2026-10-19-codex-unknown-flink-pr209-fury-ci]] · [[2026-10-19-flink-pr209-fury-ci-session-feedback]].

- **2026-10-15:** PR 3 implementado en `feature/rio-e2e-local-flink-pr3` @ aaec54bd (3 commits, +310/−29 vs PR 2, sin src/main/src/test): PyFlink 1.20.5 vía secret BuildKit, symlink `python → python3` (resuelve cliente y worker Beam), stub ZIP con layout KDA, extracción con protección zip-slip al volumen `python-apps`, PythonDriver por REST. Gates y E2E físico completo PASS; PR draft #213 abierto contra #211.
- **2026-10-14:** precondiciones PR 3 PASS con mirror Fury vía GlobalProtect; imagen `rio-kiss-flink-runtime:pr3-spike` construida (Flink 1.20.5). No hay wheel binario arm64 de apache-flink==1.20.5 en la prueba; instalación con toolchain completada. Conteos de furycloud: history 0, inspect 0. Spike curl: upload OK; PythonDriver con `-py ... -pyexec python3` devuelve HTTP 400, `Cannot run program "python": error=2, No such file or directory`; sin job id. STOP solicitado antes de Java. Alternativa propuesta, no implementada: alias python → python3 en la imagen y repetir spike. Parche secret conservado temporalmente como `rio-pr3-spike-secret-image.patch`; evidencia en `rio-pr3-spike-build-secret.log`, `rio-pr3-spike-upload.json` y `rio-pr3-spike-run.json`. Recursos del spike eliminados; 0 contenedores, 0 redes rio-*, contexto activo colima; worktree limpio en 0728044c, src/main y src/test sin diff contra base ni origin/develop. [[2026-10-14-rio-pr3-python-driver-spike-close]].

- **2026-10-14:** PR 3 iniciado desde 0728044c. Docker de colima-rio accesible y vacío; contexto activo colima. Build de imagen Flink 1.20.5 + apache-flink==1.20.5 terminó con código 1 tras errores DNS de pip; curl a PyPI también agotó resolución en 20 s. STOP antes del spike REST, sin job id ni cambios Java. Único cambio temporal del Dockerfile restaurado y contenedor del build eliminado; worktree limpio, sin delta productivo contra base ni origin/develop. Evidencia temporal: rio-pr3-spike-build.log y rio-pr3-spike-image.patch en el directorio temporal del sistema. Próximo paso: recuperar resolución/acceso a PyPI y repetir construcción y spike antes de implementar. [[2026-10-14-rio-pr3-spike-change-log]].

- **2026-10-14:** descripción final en inglés del PR #211 publicada y verificada contra [[Descripción PR — rio-controlplane-flink (E2E local PR 2)]]; rama `feature/rio-e2e-local-flink-pr2` @ `0728044c`, base `feature/rio-e2e-local-flink-kiss` @ `c0cabe72`. E2E físico y gates PASS, cleanup completo, 0 hilos y CI verde. La VM se recreó y quedó sana; los antecedentes de recuperación quedan en las entradas históricas de esta bitácora.

- **2026-10-14:** cierre de recuperación de VM: bloqueo en SSH tras reinicio, sin corrida E2E ni cambios al repo/PR. [[2026-10-14-rio-pr211-vm-recovery-close]].

- **2026-10-14:** cierre de sesión del fix null properties en 0728044c; gates y revisión del bot PASS, E2E bloqueado por infraestructura y cleanup incompleto. [[2026-10-14-rio-pr211-null-properties-close]].

- **2026-10-14:** sesión cerrada por delta; HEAD 39937680 sobre base c0cabe72, sin delta productivo. Próximo paso: recertificar físicamente el último fix y continuar revisión humana. [[2026-10-14-rio-flink-pr211-alignment-close]] · [[2026-10-14-rio-flink-pr211-alignment-session-feedback]].

Estado y planificación vigentes en esta nota; cambios consolidados en el journal de AGENTS OS.

[[RIO E2E local]] · [[Descripción PR — rio-controlplane-flink (E2E local)]] · [[Descripción PR — rio-controlplane-flink (E2E local PR 2)]]
