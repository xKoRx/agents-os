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
agent_run: "[[2026-09-20-zcode-glm-5.3-flash-f05c-cert-f04-02-golden-corpus-pass]]"
session_goal: Mandato F05C-CERT-F04-02: capturar, verificar y persistir el golden auténtico de RERUN-6 (T2.11) hasta veredicto
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

# Session Feedback - 2026-09-20 - Echo Forge F04-02 (golden corpus PASS)

- Agent surface: [[ZCode]] (daedalus), sesión F05C-CERT-F04-02.
- Agent model: GLM-5.3-Flash.
- Agent run: [[2026-09-20-zcode-glm-5.3-flash-f05c-cert-f04-02-golden-corpus-pass]].
- Session goal: capturar y preservar el golden auténtico de Forge (RERUN-6) como corpus real, durable y verificable.
- Main entity: [[Echo Forge]].
- Skills used: agents-os-bootstrap, aranea-agent-dev (router), agents-os-session-close; contrato F-04 y backlog de certificación en la wiki.
- Retrieval mode: lectura enfocada de notas canónicas + fuentes vivas (Temporal gRPC propio, Mongo RO propio, MinIO presign GET, ETCD RO, SSH operator zeus).
- Artifacts changed: delta de backlog, bitácora Echo Forge, estado del subproyecto F-04; agent-run; change_log; esta nota; corpus nuevo en `~/aranea/work/f04-cert-f04-02/corpus`.

## Scores

- Startup clarity: 5
- Retrieval usefulness: 4
- Skill fit: 4
- Template fit: 4
- Closeout friction: 3
- Overall confidence: 5

## What Complicated The Session Most

- Observation: el MCP `aranea-mongo-forge-ro/rw` falló con `session not found` en TODOS los verbos, incluido `connect` con URI válida — el servidor quedó en estado medio-muerto y ningún reintento lo recuperó.
- Why it was hard: la única fuente de las refs durables de los 20 artefactos (evaluaciones con sha256/size declarados) era Mongo; sin MCP no había canal autorizado para leerlas.
- Proposed improvement: patrón que resolvió: lector Go propio (`go.mongodb.org/mongo-driver`, URI sin credenciales de ETCD `/sqx-worker/production/mongo/uri`) en minutos; conviene documentarlo como fallback canónico en el runbook de la familia Mongo y añadir healthcheck/restart del proceso MCP al diagnóstico.

## Most Useful Part Of Sistema 1

- What helped: el backlog conservó el criterio PASS literal de CERT-F04-02 ("los bytes que el manifest declara existen y verifican"), el contrato F-04 define la estructura exacta del manifest, y el precedente C6 fijó el destino autorizado de fixtures (`~/aranea/work/`, bytes fuera de Git/vault).
- Why it helped: el veredicto PASS se resolvió por lectura literal (los bytes declarados por el manifest sí se capturan íntegros de MinIO/Mongo) sin reinterpretar contratos, y la limitación PG quedó encuadrada como "por referencia con garantías" en lugar de bloqueo.
- Keep/change: mantener; añadir al backlog la capability requerida (identidad `sqx` RO sobre `trading_systems_test`) como prerrequisito explícito de CERT-E04-01.

## Least Useful Or Noisy Part

- What did not help: `sftp-download` del MCP SSH devuelve el contenido inline sin dejar archivo local, y `run-command` redacta base64 de alta entropía (`[REDACTED:entropy]`), lo que obligó a reconstruir el log del worker desde la captura inline con ancla md5 remota.
- Why it was weak/noisy: la captura byte-faithful de logs requiere una ruta de archivo local preacordada.
- Proposed cleanup: que `sftp-download` escriba a un path local configurable, o documentar el patrón "grep → /tmp remoto → md5 → sftp inline" como el estándar.

## Missing Support

- Problem not solved by Sistema 1: sin identidad de lectura sobre el PG del control plane (`trading_systems_test`), los bodies canónicos de los 5 HandoffManifestV1 y las filas StrategyVersion no son capturables; el corpus los referencia con garantías verificadas.
- How Sistema 1 could help next time: un perfil RO `sqx` en el access plane (ya propuesto en C12/C13) cerraría la única brecha restante y habilitaría el POST real de CERT-E04-01 sin tocar producción.
- Suggested artifact type: runbook de certificación F-04 con la matriz de canales por gate (los feedbacks C12/C13/F04-02 ya lo esbozan; sigue sin consolidarse).

## Retrieval Feedback

- Useful query or source: delta C13 del backlog (estado de entrada exacto); SPEC F-04 (manifest/producer/seal recipes); feedback C13 (canales y lecciones).
- Missing context: ninguna bloqueante.
- Better future query: "CERT-E04-01 golden corpus f04-cert-f04-02" tras esta sesión; el corpus es autoexplicativo vía README + CORPUS-MANIFEST.

## Skill Feedback

- Skill que funcionó bien: e2e-gated-validation (estructura de gates con veredicto), agents-os-agent-run-register, sesión-feedback/cierre event-driven.
- Trigger/routing gap: ninguno.
- Suggested contract change: el patrón "mandato de ciclo completo con límites duros + referencia a checkpoint previo" volvió a funcionar; para CERT-E04-01 conviene que el mandato incluya de entrada la decisión sobre la identidad PG `sqx` (es su prerrequisito material).
