---
type: feedback
schema_version: 1
scope: session
created: "2026-10-18"
updated: "2026-10-18"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Aranea]]"
related:
  - "[[aranea-ssh-mcp]]"
  - "[[Echo Forge — Operación Real V2]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM 5.3 Flash (account:zai-individual-coding-plan/GLM-5.3-Flash)
agent_run: "[[2026-10-18-zcode-glm53-overview-cpu-parallelism-s02]]"
session_goal: S02 paralelismo CPU Echo Forge (CustomAnalysis multicore con paridad exacta)
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

# Session Feedback - 2026-10-18 - aranea-ssh transport + benchmarking sqcli

## Context

- Agent surface: [[ZCode]] · Agent model: GLM 5.3 Flash · Agent run: [[2026-10-18-zcode-glm53-overview-cpu-parallelism-s02]]
- Main entity: [[Echo Forge — Operación Real V2]] · Skills: aranea-agent-dev (router), agents-os-session-close.
- Artifacts changed: rama `perf/overview-s02` (symphony), artifacts vault S02, copia candidate-local Kronos restaurada.

## What Complicated The Session Most

- Observation: el transporte `aranea-ssh` (MCP) redacta contenido de alta entropía (base64/binario → `[REDACTED:entropy]`), corta heredocs multilínea (timeout/indent corrupt), limita sftp-download a 1 MB y devuelve binarios inline inservibles; además `read-command` rechazó `md5sum` (allowlist) y el límite de 30 s por tool-call mató compiles/largos a mitad.
- Why it was hard: transferir el exporter (87 KB) y scripts entre Daedalus↔Kronos exigió 3 vías alternativas antes de una estable.
- Proposed improvement: runbook en [[aranea-ssh-mcp]]: "para archivos >10 KB usar http.server efímero en Daedalus + curl en el host + verificación SHA256; scripts pequeños por sftp-upload; nunca heredocs remotos".

## Most Useful Part Of Sistema 1

- What helped: el artefacto S01 (`artifacts/ECHO-FORGE-OVERVIEW-PERF-S01/`) reutilizables casi completos (mecanismo de deploy snippet+manifiesto+jar, protocolo de corpus pristine+SHA, parity2.py, entorno candidate-local en Kronos).
- Keep: evidencia previa como infraestructura de la siguiente sesión — se pagó sola en minutos.

## Least Useful Or Noisy Part

- What did not help: `read-command` false-negativo sobre comandos de sólo lectura (`md5sum`) obliga a usar `run-command` (superficie aprobatoria más amplia) para operaciones inofensivas.
- Proposed cleanup: ampliar allowlist de `read-command` a checksums (`md5sum`, `sha256sum`, `stat`, `wc`).

## Missing Support

- Problem not solved by Sistema 1: no existía registro del bug del lock single-instance SQX observado en vivo (sqcli huérfano → boots posteriores se rechazan en silencio con exit 0 y logs "another instance") ni del pgid-reuse al muestrear /proc.
- Suggested artifact type: L3 known-error/learning (creada en memoria interna esta sesión).

## Retrieval Feedback

- Useful: memory index ZCode (S01 + SQX144 CPU) resolvieron el arranque sin re-derivar nada.
- Better future query: "mecanismo deploy snippet jar Forge" → ahora también cubierto por S02 artifacts.

## Pain Pattern Candidate

- Is this likely to repeat? yes (todo benchmark/bench remoto contra hosts Aranea).
- Suggested severity: medium.
- Promote to L3 memory? yes (hecho: checkpoint interno + gotchas en artifacts S02).

## One Next Improvement

- Añadir al runbook de [[aranea-ssh-mcp]] la receta de transferencia de archivos (http.server + curl + SHA) y la advertencia del lock single-instance para cualquier secuencia de runs sqcli.
