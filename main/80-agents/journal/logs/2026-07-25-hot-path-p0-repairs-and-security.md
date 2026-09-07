---
type: change_log
schema_version: 1
scope: session
created: "2026-07-25"
updated: "2026-08-11"
area: "[[Personal]]"
project: "[[AGENTS OS - Hot Path y Cierre Silencioso]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-skill-authoring]]"
  - "[[agent-constitution]]"
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
  - area/personal
  - project/agents-os
  - change/updated
  - change/security
---

# Hot Path Iteration — P0 reparación y seguridad

## Cambio

- **Tipo:** updated + security + created
- **Archivo(s):**
  - CREADO `10-projects/AGENTS OS/agentes/AGENTS OS - Hot Path Iteration.md`
    (proyecto de agente controlador de la iteración)
  - CREADO `00-inbox/AGENTS OS Hot Path/agents-os-hot-path-brief.md`
    (brief original de ChatGPT movido desde el root del vault)
  - EDITADO `10-projects/AGENTS OS/AGENTS OS.md`
    (siembra de tarea puente hacia el nuevo proyecto de agente)
  - EDITADO `80-agents/memory/internal/agent-memory/2026-07-22-symphony-kronos-instrument-sync-gap.md`
    (redacción de credencial + `load_policy: always` → `when_project_loaded`)
  - EDITADO `80-agents/skills/agents-os-skill-authoring/SKILL.md`
    (corrección de referencias relativas rotas)
  - EDITADO `10-projects/AGENTS OS/chatgpt-pack/PROJECT-STATE.md`
    (path legado de constitución → path canónico)

## Motivo

- Diagnóstico y propuesta de iteración "Hot Path" surgidos de ChatGPT contra
  el `ITERATION-PROMPT.md`. Sin un proyecto controlador, los cambios iban a
  quedar huérfanos en el vault. Esta iteración reforma contratos vivos y
  requiere control versionado y aprobación humana por fase.
- Hallazgo P0 de seguridad: una memoria interna de dominio (Symphony) marcada
  - [REDACTED] Credencial retirada del historial; la fuente original debe rotarse fuera del vault.
  texto plano. Violaba el mandamiento 13 de la constitución y se cargaba en
  toda sesión del vault, no solo las de Symphony.

## Fuentes usadas

- Brief de ChatGPT preservado en `00-inbox/AGENTS OS Hot Path/agents-os-hot-path-brief.md`.
- Auditoría local contra archivos vivos del vault (verificación uno a uno de
  los 4 hallazgos P0 declarados por ChatGPT).
- `80-agents/agents-os/agent-constitution.md` mandamiento 13 (fronteras duras:
  no secretos ni credenciales en el vault).
- Modelo de ownership de proyectos: `90-system/convenciones.md` y
  `80-agents/skills/agents-os-agent-project-workflow/SKILL.md`.

## Resolución aplicada

- **Proyecto controlador creado** con `owner: agent` y `parent: [[AGENTS OS]]`
  según el modelo de ownership. Tarea puente humana sembrada en el proyecto
  padre con `#owner/me #type/supervision #area/personal`.
- **Brief preservado** en `00-inbox/` del proyecto (no en el root del vault)
  para que no contamine retrieval pero quede a mano del agente.
- **Credencial redactada** sin reproducirla en ningún artefacto. La línea que
  la contenía ahora apunta al log y a la decisión de consultar fuera del vault.
- **`load_policy` bajado** de `always` a `when_project_loaded` para que la
  memoria de Symphony solo cargue cuando el proyecto Symphony esté activo.
- **Referencias relativas arregladas** en `agents-os-skill-authoring/SKILL.md`:
  `_shared/` → `../_shared/` y `../../templates/` → `../../../templates/`.
  Validé posteriormente que las otras 20 skills usan correctamente `../_shared/`
  y `../../templates/`; esta era la única con profundidad incorrecta.
- **Path de constitución** en `chatgpt-pack/PROJECT-STATE.md` línea 243:
  `memory/public/constitution/agent-constitution.md` → `agents-os/agent-constitution.md`.
- **Sub-hallazgo `.graphifyignore` ya resuelto** — las exclusiones de
  `outputs/agents-os-chatgpt/` ya estaban en `.graphifyignore` líneas 52-53.
- **Drift de `user_rule` de Cursor NO corregido** — apunta a
  `/Users/rodrigojara/...` pero el vault está en `/Users/rjara/...`. No es
  editable desde el vault; queda como tarea puente humana (#waiting).

## Validación

- `cat` sobre la credencial: la línea que la contenía ya no la tiene.
- `grep` sobre referencias de password y hosts en la memoria afectada:
  cero hits.
- Verificación de paths relativos contra las 20 skills: 20/20 OK después del
  fix de `skill-authoring`.
- Estructura del proyecto de agente cumple el modelo de ownership: tiene
  `owner: agent`, `parent`, carpeta `agentes/` bajo iniciativa padre, tarea
  puente sembrada en el padre.

## Compartibilidad

- **Scope:** local — todos los cambios son específicos del vault personal.
- **Redacción revisada:** no contiene secretos ni credenciales. La credencial
  redactada no se reproduce en ninguna parte del log ni de las notas.

## Pendiente (P1-P3)

- **P1 Hot Path** — bloqueado esperando OK del owner: unificar bootstrap
  canónico, arranque incremental, enrutar memoria interna por metadata,
  corregir Context Router, refactor mandamiento 16.
- **P2 Silent Close** — bloqueado esperando OK del owner: cierre por delta,
  feedback event-driven, reporte default 1-2 líneas, sacar session-close de
  always-load.
- **P3 Doctor + Benchmark** — bloqueado esperando OK del owner: skill
  `agents-os-doctor` + gate E2E.

## Rollback

- Revertir el diff de los 5 archivos editados (restaurar la credencial en la
  memoria Symphony, devolver `load_policy: always`, deshacer el fix de refs,
  restaurar el path legado de constitución, borrar la tarea puente).
- Eliminar el proyecto `AGENTS OS - Hot Path Iteration.md` y el brief movido
  a `00-inbox/`. No hay dependencias cruzadas que se rompan al borrar.
