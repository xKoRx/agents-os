---
type: feedback
schema_version: 1
scope: session
created: "2026-09-26"
updated: "2026-09-26"
area: "[[Personal]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
  - "[[AGENTS OS]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash (account:zai-individual-coding-plan/GLM-5.3-Flash, host-reported)
agent_run: "[[2026-09-26-zcode-glm53-forge-retester-shot1]]"
session_goal: Shot 1 Ranking→Retester agrupado + intermisión owner (sync histórico flota)
source_session:
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

# Session Feedback - 2026-09-26 - forge-retester-shot1

## Context

- Agent surface: ZCode (Daedalus workspace, dominio aranea)
- Agent model: GLM-5.3-Flash
- Agent run: [[2026-09-26-zcode-glm53-forge-retester-shot1]] — sync histórico flota EQUAL + diagnóstico causal de C2 (`CanonicalSymbol("NDX")` vacío) + verificación en vivo de re-despacho wedged
- Session goal: mandato owner Shot 1 validación Ranking→Retester con `FirstRetestConfig.cfx`
- Main entity: [[Echo Forge — Operación Real V2]]
- Skills used: agents-os-bootstrap, aranea-agent-dev, technical-project-manager, sqx-instrument-sync, worker-ssh (todas por lectura directa de SKILL.md; el Skill tool no resuelve skills del vault)

## What Complicated The Session Most

- Observation: la causa raíz de C2 estaba en logs de worker de Hera del día anterior; la continuidad previa documentaba una causa incorrecta ("sin retry, GUI").
- Why it was hard: el MCP temporal-ro no puede seleccionar namespace (`sqx-prop` inalcanzable) y postgres-ro apunta a la BD de Echo, no al control-plane Forge ⇒ el estado Temporal/PG del workflow sólo fue inferible vía dispatcher + worker logs + flowkit.
- Proposed improvement: parámetro namespace por llamada en temporal-ro y un perfil forge-pg-ro documentado en [[aranea-mcps-expert]].

## Most Useful Part Of Sistema 1

- What helped: la skill app-owned `sqx-instrument-sync` (repo) ejecutó audit→sync→EQUAL de punta a punta, y `flowkit` como read surface RO del control-plane.
- Why it helped: tooling canónico versionado con contratos de exit codes en vez de improvisación; los contratos fail-closed del import (sealed manifest, put-if-absent, attribute conflict) hicieron que ambos intentos equivocados murieran sin dañar el cohort.
- Keep/change: keep; añadir al runbook del sync la nota de que "rsync no disponible en X" puede ser en realidad host key stale (el preflight oculta el error ssh real bajo `2>/dev/null`).

## Least Useful Or Noisy Part

- What did not help: `read-command` del ssh-mcp rechaza comandos read-only legítimos con mensaje engañoso ("got: safe") por parsing de tokens/quotting; `run-command` corta a los 30s (induce error en launches con sleep, aunque nohup sobrevive); el filtro de entropía redacta salidas base64 completas (transferencia binaria imposible; sftp-download corrupto para binarios).
- Why it was weak/noisy: cada uno costó llamadas redundantes y workarounds (scp por pty, binario ya presente en host).
- Proposed cleanup: mensaje de rechazo con la regla exacta; timeout configurable por llamada; sftp binario confiable.

## Missing Support

- Problem not solved by Sistema 1: no existe vía agente-safe para inspeccionar el estado de un workflow Temporal del namespace `sqx-prop` ni filas del control-plane PG de Forge.
- How Sistema 1 could help next time: lo mismo del punto 1 (namespaces en temporal-ro, perfil forge-pg-ro).
- Suggested artifact type: actualización de [[aranea-mcps-expert]] con la matriz alcance-por-namespace/BD (ya enlazada, falta el detalle sqx-prop/trading_systems).

## Skill Feedback

- Skill that worked well: sqx-instrument-sync (exit codes como contrato, verificación SHA bit-a-bit, logs rotados).
- Skill that was confusing: ninguna del vault; el grep del preflight del sync script oculta el error ssh real (mejora puntual del script, no de la skill).
- Trigger/routing gap: el owner dijo "creo que por ahí hay un script" y el script vive en `.agents/skills/` del repo owner — el bootstrap del vault no descubre skills app-owned; sólo la lectura del router aranea (hard rule §7) lo menciona.
- Suggested contract change: ninguna; funcionó el encadenamiento router → skill app-owned.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna al iniciar? sí (nota global always-load del bootstrap).
- ¿Qué valor operativo aportó? reglas transferibles (leer estado durable antes de repetir efectos laterales; verificar outcome en la capa dueña de la semántica) que evitaron re-importar y guiaron el diagnóstico por estado durable.
- ¿Dejaste algún mensaje para el próximo agente? sí — checkpoint de continuidad del proyecto actualizado (vía bitácora del proyecto + memoria del workspace ZCode).
- Utilidad del espacio privado (1-5): 4.

## Pain Pattern Candidate

- Is this likely to repeat? yes (diagnóstico de workflows Forge wedged; transferencia binaria a hosts).
- Suggested severity: medium
- Candidate owner: mantenimiento de aranea-mcps (temporal-ro namespace param; sftp binario).
- Promote to L3 memory? no (queda en feedback + bitácora del proyecto; es fricción de superficie, no regla de negocio).

## One Next Improvement

- Añadir a [[aranea-mcps-expert]] (o su matriz de acceso) la nota explícita: temporal-ro sin selector de namespace ⇒ sqx-prop no observable; postgres-ro = BD Echo ⇒ control-plane Forge sólo vía flowkit.
