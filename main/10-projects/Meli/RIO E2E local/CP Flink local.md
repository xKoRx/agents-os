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
| 2 | SQL UPDATE + CRUD HTTP de SQL + JAVA/JAR | `feature/rio-e2e-local-flink-pr2` @ `0728044c` · [#211](https://github.com/melisource/fury_rio-controlplane-flink/pull/211), base `feature/rio-e2e-local-flink-kiss` (#209) | Fix null properties pusheado; 1937 tests productivos + 20 locales y pre-commit PASS. Hilo 4276784323 resuelto; API sin hilos pendientes. Certificación física bloqueada: reinicio de colima-rio no recuperó SSH; Docker inaccesible. Descripción del PR pendiente. |
| 3 | PYTHON/ZIP | Pendiente | Pendiente |

Fuera de alcance: GCP y Playmaker; la integración Playmaker se entrega aparte, apilada como en ClickHouse.

JAR de PR 2: stub Nexus con nginx oficial y TopSpeedWindowing.jar de la imagen Flink; queries y validación de paths productivas conservadas, HTTP sólo para `nexus-local`. El SHA vigente `0728044c` conserva ConcurrentHashMap y omite entryClass/programArgs con valor null. Recuperación del 2026-10-14: `limactl stop colima-rio` terminó normalmente; el arranque no alcanzó SSH dentro de 400 s. SIGALRM no terminó el cliente, por lo que se canceló sólo ese proceso. Lima informa Running; SSH responde Connection reset by peer y el socket Docker no existe. No se pudo comprobar espacio libre, dmesg ni restos de contenedores/redes. No se ejecutaron build, tests, E2E ni teardown en esta sesión. El worktree permanece limpio y HEAD coincide con origin en `0728044c`; src/main y src/test sin diff contra ambas bases remotas. API final: 0 hilos sin resolver, CI SUCCESS (Code Reviewer NEUTRAL). Descripción del PR sin cambios. Próximo paso: recuperar acceso SSH y Docker de la VM sin recrearla ni ejecutar fsck; luego retomar certificación física. Log operativo temporal: `/private/tmp/rio-pr211-vm-recovery.log`.

## ✅ Tareas

- [ ] Fix en develop del doble dispatch de CreateAppInAWSHandler y StartAppInAWSHandler que compensa LocalFlinkEventMulticaster; entrega fuera de local. #owner/me #type/dev #area/meli
- [ ] Corregir `component_type: null` en el resultado del undeploy; entrega fuera de local. #owner/me #type/dev #area/meli

## 📆 Bitácora

- **2026-10-14:** cierre de recuperación de VM: bloqueo en SSH tras reinicio, sin corrida E2E ni cambios al repo/PR. [[2026-10-14-rio-pr211-vm-recovery-close]].

- **2026-10-14:** cierre de sesión del fix null properties en 0728044c; gates y revisión del bot PASS, E2E bloqueado por infraestructura y cleanup incompleto. [[2026-10-14-rio-pr211-null-properties-close]].

- **2026-10-14:** sesión cerrada por delta; HEAD 39937680 sobre base c0cabe72, sin delta productivo. Próximo paso: recertificar físicamente el último fix y continuar revisión humana. [[2026-10-14-rio-flink-pr211-alignment-close]] · [[2026-10-14-rio-flink-pr211-alignment-session-feedback]].

Estado y planificación vigentes en esta nota; cambios consolidados en el journal de AGENTS OS.

[[RIO E2E local]] · [[Descripción PR — rio-controlplane-flink (E2E local)]] · [[Descripción PR — rio-controlplane-flink (E2E local PR 2)]]
