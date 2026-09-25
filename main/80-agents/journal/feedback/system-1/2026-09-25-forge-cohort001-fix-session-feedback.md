---
type: feedback
schema_version: 1
scope: session
created: 2026-09-25
updated: 2026-09-25
area: "[[Personal]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
  - "[[AGENTS OS]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash (account:zai-start-plan/GLM-5.3-Flash, host-reported)
agent_run: "[[2026-09-25-zcode-glm53-forge-cohort001-fix]]"
session_goal: CORRECCIÓN DE MANDATO Cohort 001 Zeus/Retester + resolución BR_G* + import
source_session: sess_bd5bee74-db1b-44ad-90ba-a47831746fcc
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/agentsos
  - agent/system1
---

# Session Feedback - 2026-09-25 - forge-cohort001-fix

## Context

- Agent surface: ZCode (Daedalus workspace, dominio aranea)
- Agent model: GLM-5.3-Flash
- Agent run: import 727 estrategias vía watcher candidate-local en Zeus + fix de producto rama `fix/watcher-import-intake-deadline`
- Session goal: mandato owner — reconstruir Cohort 001, resolver BR_G\*, congelar, importar, continuar C1/C2
- Main entity: [[Echo Forge — Operación Real V2]]
- Skills used: agents-os-bootstrap, aranea-agent-dev, aranea-mcp-plane-operator (lectura directa de SKILL.md/runbooks; el Skill tool no resuelve skills del vault — ver [[zcode-skill-tool-vault-skills]])

## Fricciones operativas (nuevas, con evidencia)

- **ssh-mcp pool saturado al iniciar** (`Server is at its session limit (64)` persistente): la remediación canónica del runbook (`docker restart ssh-mcp` vía `mcps-ops` desde Hermes) funcionó; restauró servicio en <1 min. El pool vuelve a saturarse entre sesiones — candidato a root-cause (sesiones huérfanas de clientes que no cierran).
- **MCP HTTP sessions expiran a mitad de operación** (MinIO MCP devolvió 404 tras ~30 min de sesión): los scripts que reutilizan `Mcp-Session-Id` deben re-inicializar ante 404; detectado y compensado en esta sesión.
- **`pkill/pgrep -f <patrón>` dentro de run-command del ssh-mcp se auto-matchea el wrapper bash** (su cmdline contiene el patrón): mató mi propio comando (`killed by SIGSIGTERM`) y reporta PIDs falsos. Regla operativa nueva: envolver el patrón (`pgrep -f 'bin/nombre'` desde script file, no inline) o filtrar por uid/ejecutable.
- **El watchdog de auto-upgrade del watcher (main.go) mata a los 10s todo binario no bajo `/opt/symphony/current`** aunque ENV=production venga del login shell: operativo candidate-local imposible sin knob; fix propuesto en rama (hard rule: defaults de flota intactos).
- **El deadline fijo de 2 min del import_intake no escala a cohorts de cientos de .sqx** (publish secuencial ~6/s; el orden no-compounding hace que los reintentos vuelvan a exceder): fix propuesto por env knob.
- **Contratos write-once (sealed manifest + frozen membership) sin vía de limpieza de control-plane:** un error de naming en un intento envenena la identidad del FlowRun de forma irrecuperable para el agente (no hay write-path a PG `sqx.control`); la única salida fue una wave nueva (`wave1b`). Sugerencia de producto: comando owner-side de purga de FlowRun/participations para cleanup operacional (o etiqueta de descarte del intento).

## Lo que funcionó bien

- ssh-mcp con `run-command` + scripts por base64 in-host cubrió todo el flujo Zeus sin SSH directo (echo-dev operator + ACL `--x` en /home/kor alcanza para lectura de databanks y ejecución de binarios de flota).
- La reconciliación del sealed manifest contra el freeze local (727/727 SHA) dio verificación de lineage barata y fuerte sin acceso a PG.
- El mecanismo candidate-local (watch_dir en home de echo-dev, sin tocar ETCD/ETCD production keys ni la flota) mantuvo el blast radius mínimo a pesar de los 3 intentos fallidos.
