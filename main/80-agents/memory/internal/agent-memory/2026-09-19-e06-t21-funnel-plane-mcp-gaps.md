---
type: feedback
schema_version: 1
scope: session
created: "2026-09-19"
updated: "2026-09-19"
area: "[[Echo]]"
project: "[[Echo — E-06 Reference Enrollment and Binding]]"
entities:
  - "[[Echo — E-06 Reference Enrollment and Binding]]"
  - "[[Echo Forge]]"
  - "[[AGENTS OS]]"
related:
  - "[[aranea-mcps-expert]]"
  - "[[Daedalus — Development Agents MCP Access & Gaps]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash (zai-individual-coding-plan/GLM-5.3-Flash)
agent_run: "[[2026-09-19-zcode-glm-echo-e06-t21-g0-pass-g1-stop]]"
session_goal: Mandato maestro E-06/T21 (R3 G0 → Forge seal → E-04 → §22); terminó T21_BLOCKED con G0 PASS y G1 STOP material
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - area/echo
  - agent/system1
---

# Session Feedback - 2026-09-19 - e06-t21-funnel-plane-mcp-gaps

## Context

- Agent surface: ZCode
- Agent model: GLM-5.3-Flash
- Agent run: 2026-09-19-zcode-glm-echo-e06-t21-g0-pass-g1-stop
- Session goal: ejecutar T21 (G0 identidad R3, G1 sellado forge_seal_handoff, G2 ingestion E-04, G3/G4 físico §22)
- Main entity: [[Echo — E-06 Reference Enrollment and Binding]]
- Skills used: agents-os-bootstrap, aranea-agent-dev (router), agents-os-session-close, agents-os-session-feedback
- Retrieval mode: Graphify no requerido; entidad + memorias + VERIFICATION repo
- Artifacts changed: entidad E-06, VERIFICATION/TASKS echo `b66dc5ff`, agent_run, change_log, memoria auto

## Scores

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 5
- Template fit: 5
- Closeout friction: 5
- Overall confidence: 5

## What Complicated The Session Most

- Observation: los tres canones de lectura del plano del funnel fallaron esta sesión y es el tercer mandato consecutivo con el mismo patrón: Temporal RO MCP lista 0 workflows (apunta a namespace distinto de `sqx-prop`), Mongo forge RO caído (`-32003 session not found`), MCP postgres bound a DB `echo` sin cross-database hacia `trading_systems_test`. Además el SSH MCP redacta bulk binario/base64 por entropía (imposible transferir el MQ5 por ese canal) y `sftp-download` devuelve el contenido inline, no a disco.
- Why it was hard: sin esas lecturas el veredicto G1 habría dependido sólo de los resúmenes de sesiones anteriores; el mandato exige estado durable vigente, no heredado.
- Proposed improvement: (1) repuntar el namespace del perfil `aranea` del Temporal RO MCP a `sqx-prop` (o exponer namespace por parámetro); (2) revisar el transporte SSH MCP para permitir base64 de artefactos grandes bajo comando explícito (hoy cualquier bulk de alta entropía se redacta); (3) reconectar Mongo forge RO.

## Most Useful Part Of Sistema 1

- What helped: la memoria auto de la 7ª sesión (rutas zeus/Windows, sellos, deploy `Snippets.jar`) + el bullet de entidad; el runbook/patrón de perfiles SSH (`mt5-kronos-operator` para lectura, viewer rechaza read-command).
- Why it helped: G0 se re-verificó completo sin re-derivar nada.
- Keep/change: keep.

## Least Useful Or Noisy Part

- What did not help: `/opt/symphony/current/bin/symphony --help` en zeus arrancó el worker legacy 0.2.40 completo (loop de mantenimiento con SKIP idempotente; sin efecto durable pero ruidoso y con riesgo de confusión de estado).
- Why it was weak/noisy: binario legacy sin CLI de ayuda segura.
- Proposed cleanup: documentar en el runbook aranea-ssh que ese binario no admite `--help` (lección ya anotada en memoria auto).

## Missing Support

- Problem not solved by Sistema 1: no había ruta documentada para leer el control plane del funnel (decisions/versions/handoffs) desde el agente — la resolví construyendo `sqx-flowkit` scratch (read-only) contra etcd/PG del lab.
- How Sistema 1 could help next time: runbook corto en el wiki aranea: «lectura durable del plano Forge» con el comando exacto (`go build -o /tmp/sqx-flowkit ./sqx/cmd/sqx-flowkit` en un worktree symphony; `ENV=production /tmp/sqx-flowkit strategy get <StrategyRef>`; etcd 192.168.31.250-254:2379; PG `trading_systems_test`@192.168.31.220 user `sqx`).
- Suggested artifact type: runbook (federado aranea) o sección en [[aranea-mcps-expert]]/[[Daedalus — Development Agents MCP Access & Gaps]]; hoy el detalle vivo está en la memoria auto `echo-e06-t21-cert-state` y en el agent_run.
