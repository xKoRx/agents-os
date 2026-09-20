---
type: feedback
schema_version: 1
scope: session
created: 2026-09-20
updated: 2026-09-20
area: "[[Echo]]"
project: "[[Echo Forge]]"
entities:
  - "[[Echo Forge]]"
  - "[[Aranea]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-09-20-zcode-glm-5.3-flash-f05c-cert-f04-01-c13-recovery-certified]]"
session_goal: Mandato F05C-CERT-F04-01-C13: release 0.2.104 del fix aprobado, recuperación natural de RERUN-6 y veredicto de CERT-F04-01
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agents-os
  - agent/system1
---

# Session Feedback - 2026-09-20 - Echo Forge C13 (recuperación y certificación PASS)

- Agent surface: [[ZCode]] (daedalus), sesión F05C-CERT-F04-01-C13.
- Agent model: GLM-5.3-Flash.
- Agent run: [[2026-09-20-zcode-glm-5.3-flash-f05c-cert-f04-01-c13-recovery-certified]].
- Session goal: publicar el fix aprobado del defecto #6, recuperar RERUN-6 sin reiniciarla y completar CERT-F04-01 con la evidencia recuperada.
- Main entity: [[Echo Forge]].
- Skills used: agents-os-bootstrap, aranea-agent-dev (router), agents-os-agent-run-register, agents-os-session-feedback, agents-os-session-close; lectura del backlog de certificación y del contrato F-04 en la wiki.
- Retrieval mode: lectura enfocada de notas canónicas + fuentes vivas (Temporal gRPC `/tmp/thist`, Mongo RO, MinIO presign+curl, ETCD RO, SSH operator).
- Artifacts changed: delta de backlog y bitácora de Echo Forge; agent-run; change_log; esta nota; FF `codex/f05-release-prep`→`25a5122` y release `0.2.104` publicada/desplegada; workdir de ensayo `g1-stage/`.

## Scores

Use 1-5, where 1 is poor and 5 is excellent.

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 4
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 5

## What Complicated The Session Most

- Observation: la lectura del estado de retry de Temporal fue ambigua con las herramientas existentes: el historial de eventos no exponía los intentos fallidos de la actividad (0 eventos ActivityTaskFailed visibles por paging) mientras el describe reportaba attempt=16; el perfil del MCP temporal apunta a otro namespace y las páginas grandes de historial revientan el límite gRPC de 4 MB.
- Why it was hard: dos lecturas del mismo plano daban respuestas distintas y el estado real vivía en el estado mutable del pending activity, no en eventos.
- Proposed improvement: extender el scratch `/tmp/thist` con un modo `pending` canónico (DescribeWorkflowExecution completo: attempt, next_attempt_schedule, last_failure, last_worker) y documentarlo como la lectura fresca estándar del runbook; evitar dumps de historial sin límite de page size.
- Observation (fricción menor): el SSH operator de Windows (mt5-kronos-operator) ejecuta cmd/PowerShell sin sesión interactiva y el shell local (zsh) expande `$` de los scripts PowerShell embebidos, rompiendo dos invocaciones.
- Why it was hard: los errores llegan como parse errors de PowerShell sin pista de la causa real (expansión local).
- Proposed improvement: en el runbook windows-operator, documentar el patrón "sin variables `$`" o preferir `sftp-download` del evidence JSON + lectura local (fue lo que resolvió limpio).

## Most Useful Part Of Sistema 1

- What helped: el backlog de certificación conservó el criterio PASS literal de CERT-F04-01 y la distinción con el criterio "release cohesiva" de CERT-F05-01, y la nota de entidad conservó las lecciones por defecto; el feedback de C12 documentó que el MCP temporal no apunta a `sqx-prop` y que la vía autorizada es `/tmp/thist`.
- Why it helped: el veredicto G5 se pudo resolver por lectura literal sin reinterpretar la SPEC, y la infraestructura de diagnóstico estuvo operativa en minutos.
- Keep/change: mantener; añadir al runbook del MCP temporal el namespace por perfil y al runbook de certificación F-04 la matriz de canales mínimos por gate (el patrón MinIO presign+curl+SHA local para artefactos grandes funcionó perfecto y vale generalizarlo).

## Least Useful Or Noisy Part

- What did not help: los logs de telemetría OTEL de `release-authority`/deployer (endpoint de trazas caído) ensucian toda la salida del pipeline de release con errores de shutdown que no afectan el resultado.
- Why it was weak/noisy: obliga a filtrar manualmente para ver el JSON de autoridad real.
- Proposed cleanup: silenciar o degradar a debug el export OTEL cuando el endpoint no está alcanzable, o separar stderr de stdout en el runner.

## Missing Support

- Problem not solved by Sistema 1: sin lectura directa del PG del flujo (registry), el estado `HANDOFF_CREATED ×5` de las filas de delivery se atestó por el payload físico de cierre de la actividad + semántica de la máquina de estados + ETCD 0 keys, no por lectura de filas.
- How Sistema 1 could help next time: un perfil RO de lectura del PG del flujo (o capability MCP de lectura flowkit) cerraría la única brecha de evidencia directa restante; ya propuesto en el feedback de C12, sigue vigente.
- Suggested artifact type: runbook de certificación F-04 consolidado con la matriz de canales por gate (los deltas ya lo esbozan; falta consolidarlo).

## Retrieval Feedback

- Useful query or source: criterios PASS en el backlog; contrato F-04 §11 y failure matrix; feedback de C12 (thist, ssh-mcp).
- Missing context: ninguna bloqueante; la ubicación del fixture 6182 (`f04-cert-f04-01-c6/artifact/`) y de `mt5-export.htm` (commit `b5c71d5`) hubo que buscarlas por filesystem/historia git.
- Duplicate/noisy result: n/a.
- Better future query: "CERT-F04-02 golden auténtico preimages c71687ca" tras esta sesión.

## Skill Feedback

- Skill que funcionó bien: e2e-gated-validation (vocabulario de gates), agents-os-agent-run-register y el par feedback/cierre.
- Skill que fue confusa: ninguna grave.
- Trigger/routing gap: ninguno; el router aranea cargó bien.
- Suggested contract change: el patrón que volvió a funcionar fue "mandato con ciclo completo autorizado + límites duros" (continuidad de evidencia sin STOPs intermedios); conviene mantenerlo para los siguientes gates de la cadena (CERT-F04-02 y siguientes).
