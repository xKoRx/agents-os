---
type: feedback
scope: session
created: 2026-07-31
updated: 2026-07-31
area: "[[Echo]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
entities:
  - "[[Echo Forge - Cierre de Etapa 4]]"
  - "[[EchoForgeTradeListExporter]]"
related:
  - "[[2026-07-29-sqx-trade-list-exporter-source-order-count-zero]]"
  - "[[2026-07-31-echo-forge-wrong-rca-from-auditor-feedback]]"
aliases:
  - ef-g28-reflection-contract-feedback
  - unfalsified-rca-pattern
agent: cursor
session_goal: auditar el flujo Echo Forge, reevaluar los bugs abiertos y diseñar la solución definitiva
source_session: cursor-2026-07-31-echo-forge-reflection-contract-rca
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - project/echo-forge
  - agent/system1
---

# Session Feedback - 2026-07-31 - echo-forge-reflection-contract

## Context

- Agent: Cursor. Goal: evaluar la auditoría del flujo Echo Forge, reevaluar los
  GAPs de `G6_HANDOFF.md` §10 y diseñar la solución definitiva.
- Main entity: [[Echo Forge - Cierre de Etapa 4]]
- Skills used: agents-os-bootstrap, agents-os-session-close, worker-ssh,
  graphify (query).
- Resultado: causa raíz aislada (contrato de reflexión SQX Build 142) + 3 bugs
  nuevos tipificados. Es la **segunda RCA consecutiva** que invalida a la
  anterior sobre el mismo síntoma.

## What Complicated The Session Most

- Observation: la auditoría entregada culpaba al `result_key`
  (`Main: XAUUSD_darwinex/D1`) por ser "incoherente" con la estrategia NDX. Era
  falso en los dos sentidos: el `.sqx` **sí** contiene ese result key, y el
  `result_key` **no** es lo que produce `source_order_count=0`.
- Why it was hard: el síntoma es real y el razonamiento era internamente
  consistente. Solo se cae al abrir el artefacto físico (`unzip` del `.sqx`) y
  al contrastar el SDK real con `javap`. Ninguna de las dos cosas se había hecho
  nunca en 3 releases.
- Proposed improvement: para bugs de integración externa, **el primer paso debe
  ser inspeccionar el artefacto y el contrato reales**, no razonar sobre el
  código propio. Dos comandos (`unzip -l`, `javap -constants`) cerraron lo que
  cinco sesiones de lectura de código no cerraron.

## Most Useful Part Of Sistema 1

- What helped: el known-error previo estaba indexado y con la RCA anterior ya
  marcada como corregida; eso hizo obvio que el síntoma sobrevivía al fix y que
  la hipótesis debía descartarse, no refinarse.
- Keep/change: keep el patrón "reescribir la causa raíz en el mismo
  known-error". Añadir: registrar explícitamente **qué evidencia falsaría** la
  causa propuesta.

## Pain Pattern Candidate

**RCA no falsada cerrada como `resolved` por tests unitarios verdes.** EF-G26 y
EF-G27 se marcaron `resolved` con `go build`/`go test` OK mientras el síntoma
seguía vivo en producción. El resultado fueron 10 releases (0.2.8 → 0.2.17)
atacando capas distintas del mismo síntoma. Agravante detectado: el código citaba
como autoridad un dump `javap` que **jamás contuvo los valores citados** (se
capturó sin `-constants`), y ese comentario falso sobrevivió a G0, G2, G3, G4,
G5 y G6. Regla propuesta: un GAP se cierra falsando el síntoma con evidencia de
runtime, y toda constante de un SDK externo debe venir de un dump versionado y
verificado, nunca de un literal comentado.
