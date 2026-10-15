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
progress: 66
repo:
jira:
prs: ["https://github.com/melisource/fury_rio-controlplane-flink/pull/209", "https://github.com/melisource/fury_rio-controlplane-flink/pull/211"]
aliases: []
tags:
  - kind/project
  - area/meli
  - project/cp-flink-local
created: "2026-10-13"
updated: "2026-10-14"
---

# CP Flink local

## 🎯 Objetivo

CP Flink levantable en local con los flujos que soporta develop, sin Playmaker.

## 📊 Estado actual

| PR | Alcance | Rama / PR | Estado |
|---|---|---|---|
| 1 | SQL PROVISION, DEPROVISION, acciones start/stop y estado en runtime | `feature/rio-e2e-local-flink-kiss` · [#209](https://github.com/melisource/fury_rio-controlplane-flink/pull/209), base `develop` | Abierto, no draft; comentarios corregidos/respondidos; 32 tests y E2E de dos jobs PASS |
| 2 | SQL UPDATE + CRUD HTTP de SQL + JAVA/JAR | `feature/rio-e2e-local-flink-pr2` @ `0728044c` · [#211](https://github.com/melisource/fury_rio-controlplane-flink/pull/211), base `feature/rio-e2e-local-flink-kiss` (#209) | Listo para review: 0728044c, E2E físico PASS, 0 hilos, CI verde, descripción final |
| 3 | PYTHON/ZIP | `feature/rio-e2e-local-flink-pr3` @ `0728044c`, base `feature/rio-e2e-local-flink-pr2`; sin push ni PR | STOP en spike REST: imagen 1.20.5 + PyFlink construida mediante BuildKit secret; history/inspect en 0. Upload del jar OK, run PythonDriver HTTP 400: falta ejecutable `python` pese a `-pyexec python3`. Sin cambios Java, gates ni E2E; worktree limpio y cleanup completo. |

Fuera de alcance: GCP y Playmaker; la integración Playmaker se entrega aparte, apilada como en ClickHouse.

JAR de PR 2: stub Nexus con nginx oficial y TopSpeedWindowing.jar de la imagen Flink; queries y validación de paths productivas conservadas, HTTP sólo para `nexus-local`. El SHA vigente `0728044c` conserva ConcurrentHashMap y omite entryClass/programArgs con valor null. Certificación completa: 1937 tests productivos, 20 locales y pre-commit PASS; E2E físico completo PASS en una corrida, con cache hit de JAR sin descarga nueva desde Nexus y SQL retenido después de DEPROVISION. Cleanup verificado: 0 contenedores y 0 redes `rio-*`; VM recreada y sana, encendida. Worktree limpio y HEAD igual a origin; src/main y src/test sin diff contra origin/develop y la base. Descripción final en inglés publicada y verificada contra [[Descripción PR — rio-controlplane-flink (E2E local PR 2)]].

## ✅ Tareas

- [ ] Fix en develop del doble dispatch de CreateAppInAWSHandler y StartAppInAWSHandler que compensa LocalFlinkEventMulticaster; entrega fuera de local. #owner/me #type/dev #area/meli
- [ ] Corregir `component_type: null` en el resultado del undeploy; entrega fuera de local. #owner/me #type/dev #area/meli

## 📆 Bitácora

- **2026-10-14:** precondiciones PR 3 PASS con mirror Fury vía GlobalProtect; imagen `rio-kiss-flink-runtime:pr3-spike` construida (Flink 1.20.5). No hay wheel binario arm64 de apache-flink==1.20.5 en la prueba; instalación con toolchain completada. Conteos de furycloud: history 0, inspect 0. Spike curl: upload OK; PythonDriver con `-py ... -pyexec python3` devuelve HTTP 400, `Cannot run program "python": error=2, No such file or directory`; sin job id. STOP solicitado antes de Java. Alternativa propuesta, no implementada: alias python → python3 en la imagen y repetir spike. Parche secret conservado temporalmente como `rio-pr3-spike-secret-image.patch`; evidencia en `rio-pr3-spike-build-secret.log`, `rio-pr3-spike-upload.json` y `rio-pr3-spike-run.json`. Recursos del spike eliminados; 0 contenedores, 0 redes rio-*, contexto activo colima; worktree limpio en 0728044c, src/main y src/test sin diff contra base ni origin/develop. [[2026-10-14-rio-pr3-python-driver-spike-close]].

- **2026-10-14:** PR 3 iniciado desde 0728044c. Docker de colima-rio accesible y vacío; contexto activo colima. Build de imagen Flink 1.20.5 + apache-flink==1.20.5 terminó con código 1 tras errores DNS de pip; curl a PyPI también agotó resolución en 20 s. STOP antes del spike REST, sin job id ni cambios Java. Único cambio temporal del Dockerfile restaurado y contenedor del build eliminado; worktree limpio, sin delta productivo contra base ni origin/develop. Evidencia temporal: rio-pr3-spike-build.log y rio-pr3-spike-image.patch en el directorio temporal del sistema. Próximo paso: recuperar resolución/acceso a PyPI y repetir construcción y spike antes de implementar. [[2026-10-14-rio-pr3-spike-change-log]].

- **2026-10-14:** descripción final en inglés del PR #211 publicada y verificada contra [[Descripción PR — rio-controlplane-flink (E2E local PR 2)]]; rama `feature/rio-e2e-local-flink-pr2` @ `0728044c`, base `feature/rio-e2e-local-flink-kiss` @ `c0cabe72`. E2E físico y gates PASS, cleanup completo, 0 hilos y CI verde. La VM se recreó y quedó sana; los antecedentes de recuperación quedan en las entradas históricas de esta bitácora.

- **2026-10-14:** cierre de recuperación de VM: bloqueo en SSH tras reinicio, sin corrida E2E ni cambios al repo/PR. [[2026-10-14-rio-pr211-vm-recovery-close]].

- **2026-10-14:** cierre de sesión del fix null properties en 0728044c; gates y revisión del bot PASS, E2E bloqueado por infraestructura y cleanup incompleto. [[2026-10-14-rio-pr211-null-properties-close]].

- **2026-10-14:** sesión cerrada por delta; HEAD 39937680 sobre base c0cabe72, sin delta productivo. Próximo paso: recertificar físicamente el último fix y continuar revisión humana. [[2026-10-14-rio-flink-pr211-alignment-close]] · [[2026-10-14-rio-flink-pr211-alignment-session-feedback]].

Estado y planificación vigentes en esta nota; cambios consolidados en el journal de AGENTS OS.

[[RIO E2E local]] · [[Descripción PR — rio-controlplane-flink (E2E local)]] · [[Descripción PR — rio-controlplane-flink (E2E local PR 2)]]
