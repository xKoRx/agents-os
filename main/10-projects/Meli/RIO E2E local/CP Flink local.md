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
| 2 | SQL UPDATE + CRUD HTTP de SQL + JAVA/JAR | `feature/rio-e2e-local-flink-pr2` @ `39937680` · [#211](https://github.com/melisource/fury_rio-controlplane-flink/pull/211), base `feature/rio-e2e-local-flink-kiss` @ `c0cabe72` (#209) | Publicado; 1937 tests productivos + 19 locales y hooks PASS. Tres hilos respondidos/resueltos. E2E completo PASS en 278b4a1a; último fix de adjuntos 39937680 pendiente de recertificación física tras agotar tres iteraciones. |
| 3 | PYTHON/ZIP | Pendiente | Pendiente |

Fuera de alcance: GCP y Playmaker; la integración Playmaker se entrega aparte, apilada como en ClickHouse.

JAR de PR 2: stub Nexus con nginx oficial y TopSpeedWindowing.jar de la imagen Flink; queries y validación de paths productivas conservadas, HTTP sólo para `nexus-local`. En 278b4a1a pasaron PROVISION/RUNNING, stop/start, UPDATE con nuevo job/file-sink y DEPROVISION con nueva descarga posterior del artefacto. El fix 39937680 elimina también adjuntos reemplazados sin referencias y tiene regresiones SQL/JAR locales verdes. Las tres iteraciones físicas terminaron con cleanup vacío; no queda ningún contenedor ni red rio-*. El último fix no se volvió a ejecutar físicamente por el límite de esta sesión.

## ✅ Tareas

- [ ] Fix en develop del doble dispatch de CreateAppInAWSHandler y StartAppInAWSHandler que compensa LocalFlinkEventMulticaster; entrega fuera de local. #owner/me #type/dev #area/meli
- [ ] Corregir `component_type: null` en el resultado del undeploy; entrega fuera de local. #owner/me #type/dev #area/meli

## 📆 Bitácora

- **2026-10-14:** sesión cerrada por delta; HEAD 39937680 sobre base c0cabe72, sin delta productivo. Próximo paso: recertificar físicamente el último fix y continuar revisión humana. [[2026-10-14-rio-flink-pr211-alignment-close]] · [[2026-10-14-rio-flink-pr211-alignment-session-feedback]].

Estado y planificación vigentes en esta nota; cambios consolidados en el journal de AGENTS OS.

[[RIO E2E local]] · [[Descripción PR — rio-controlplane-flink (E2E local)]] · [[Descripción PR — rio-controlplane-flink (E2E local PR 2)]]
