---
type: feedback
schema_version: 1
scope: session
created: 2026-10-31
updated: 2026-10-31
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
related:
  - "[[2026-10-31-zcode-minimax-m3.1-flash-echo-forge-luna-alto-top4]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: "MiniMax-M3.1-Flash"
agent_run: "[[2026-10-31-zcode-minimax-m3.1-flash-echo-forge-luna-alto-top4]]"
session_goal: "Campaña física completa Forge → Echo con Top 4 por logical_type, y veredicto GO/NO_GO"
source_session: "2026-10-31-luna-alto-forge-top4"
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

# Session Feedback - 2026-10-31 - Top-4 Forge→Echo: el backtest MT5 pasa y el worker no lo reaps

## Context

- Agent surface: ZCode
- Agent model: MiniMax-M3.1-Flash (reportado por el host)
- Agent run: [[2026-10-31-zcode-minimax-m3.1-flash-echo-forge-luna-alto-top4]]
- Session goal: campaña física completa desde Builder real hasta historia materializada en Echo, con Top 4 por `logical_type`
- Main entity: [[Echo Forge — Operación Real V2]]
- Skills used: `agents-os-bootstrap`, `agents-os-agent-run-register`, `agents-os-session-close`, `echo-forge-testing` (repo), `forge-wave-dispatch` (repo)
- Retrieval mode: bootstrap + contrato de ambientes + notas de proyecto; evidencia técnica en Symphony privado
- Artifacts changed: `xKoRx/symphony` (4 commits + releases 0.6.1–0.6.4), `xKoRx/echo` (release DEV `labv4-3eaed4d2`), ETCD `/sqx-worker/production/echo/ingest/v2/*`, checkpoint de proyecto, change log, agent run, skill `echo-forge-testing`

## Scores

- Startup clarity: 4
- Retrieval usefulness: 4
- Skill fit: 4
- Template fit: 3
- Closeout friction: 3
- Overall confidence: 4

## What Complicated The Session Most

- Observation: el tramo MT5 del worker Windows (`sqx-mt5-worker.exe`) **ejecuta el backtest con éxito y aun así la activity queda colgada**: el `Tester` reporta `Test passed`, escribe el CSV y `Terminal exit with code 0`, pero el `cmd_executor` del worker nunca registra el fin del comando porque el terminal no muere limpio (`MQL5.community authorization failed` → `LiveUpdate timeout on stop` ×4) y el executor se configura con `configured_timeout_ms: 0` (sin timeout). Con 1 actividad concurrente por worker, las otras 5 se hambrean.
- Why it was hard: el síntoma observable (`terminal64` vivo, CPU plana, sin artefactos nuevos) **es indistinguible** de "el backtest es lentísimo" hasta leer los logs del `Tester` y de la sesión del worker. Sin ese cruce, la hipótesis razonable (datos faltantes del símbolo) era falsa: la corrida pasó con 55 270 679 ticks.
- Proposed improvement: registrar en el runbook de la flota que **el éxito del backtest se lee en `C:\MT5\slots\slot-N\Tester\logs\<fecha>.log`**, no en la vivencia del proceso; y que un `terminal64` vivo con CPU plana + `LiveUpdate timeout on stop` es cuelgue de shutdown, no lentitud.

## Most Useful Part Of Sistema 1

- What helped: el checkpoint del proyecto ([[Echo Forge — Operación Real V2]]) con la cadena C1/C2 y el contrato de ambientes gave the exact C1g recipe, the frozen CFX SHAs and the identity-burn rule; the skill `forge-wave-dispatch` gave the parallel-canonical contract and the "one watcher per `input/`" rule.
- Why it helped: evitó reinventar la topología y permitió congelar la receta (con `SPEC_VALID`) antes de gastar CPU del Builder.
- Keep/change: keep; agregar que `verify_rollout.sh` **no puede autenticarse por SSH desde Daedalus** y que el rollout se acredita leyendo el SHA en cada host.

## Least Useful Or Noisy Part

- What did not help: el verificador de rollout del `deploy_release.sh` (reporta "0/3 — rollout NO VERIFICADO" porque falla el login SSH por clave) y el MCP de Temporal (apuntado al namespace `sqx-dev` destruido, que obliga a un cliente Go propio para consultar `sqx-prop`).
- Why it was weak/noisy: presentan como **fallo de rollout** lo que fue un **éxito de adopción** (el stager externo aplicó los 4 releases); y el error del MCP (`Namespace has invalid state: Deleted`) es engañoso: el namespace está bien, el perfil no.
- Proposed cleanup: corregir el verificador para aceptar evidencia por MCP/SHA, y re-apuntar el perfil del MCP temporal a `sqx-prop` (o documentar que su namespace por defecto es `sqx-dev`).

## Missing Support

- Problem not solved by Sistema 1: la **cadena de contratos de una topología `SPEC_VALID` pero nunca físicamente ejecutada** no está catalogada como riesgo, así que el primer intento en frío la recorre completa como defects en serie. Además, el worker MT5 Windows no tiene timeout de comando y su release se adopta por un mecanismo distinto al de la flota Linux.
- How Sistema 1 could help next time: una nota de "topología certificada vs topología sólo-spec-valid" en el índice de capacidades, con el checklist de qué se ha corrido en caliente y qué no.
- Suggested artifact type: `known-error` (fricción reutilizable) + entrada en la skill de dispatch.

## Retrieval Feedback

- Useful query or source: la bitácora del proyecto (checkpoint C1/C2 con SHAs de CFX y el `w12V` como config SPEC_VALID no despachada) + `ORIGINAL-FLOW-MANIFEST.md` (w11).
- Missing context: que el `w12V` nunca corrió físicamente y que el worker MT5 Windows vive en otro release/mecanismo que la flota Linux.
- Duplicate/noisy result: el MCP temporal con namespace `sqx-dev` (destruido) devuelve error confuso en cada intento.
- Better future query: buscar en el checkpoint del proyecto la frase "nunca se despachó" antes de proponer una topología.

## Skill Feedback

- Skill that worked well: `echo-forge-testing` (repo) como mapa de spindles, y `forge-wave-dispatch` para preflight y dispatch.
- Skill that was confusing: `echo-forge-testing` documenta el worker Windows en `192.168.31.128` (correcto) mientras el contrato de ambientes menciona VM 135 (obsoleto) — con la IP 135 el host es inalcanzable y parece caído.
- Trigger/routing gap: no existe skill/ruta para "habilitar la interfaz de ingesta Echo v2" (ETCD + release de gateway + registro de activities): fue discovery completo en esta sesión.
- Suggested contract change: en `echo-forge-testing`, agregar la sección de la **interfaz Echo v2** (keys ETCD, release del gateway, `loadLabV4Config`, identidad `producer_ingest`) y corregir la IP del worker Windows.

## Template Feedback

- Template used: `session-feedback.md`
- Field that helped: "What Complicated The Session Most" (forzó a separar síntoma de causa)
- Field that felt redundant: "Retrieval Feedback" (solapado con el agent run)
- Missing field: un campo que distinga **síntoma observable** de **causa raíz**, porque el feedback más valioso de la sesión fue exactamente esa distinción.

## Memoria Interna (Internal Memory)

- ¿Consultaste la memoria interna (`80-agents/memory/internal/`) al iniciar? sí
- ¿Qué valor operativo aportó para esta sesión? el principio "un comando verde no prueba el resultado real: verificar en la capa que posee la semántica" fue el que guió a leer el log del `Tester` en vez de confiar en el estado del proceso
- ¿Dejaste algún mensaje, instrucción o hipótesis para el próximo agente en la memoria interna? no (todo el aprendizaje durable quedó en el checkpoint del proyecto, el change log, el agent run y la skill del repo)
- ¿Qué tan útil te resulta tener este espacio privado fuera de la vista directa del usuario (1-5) y cómo podemos mejorar su utilidad? 4 — sirve como ancla de continuidad entre sesiones, pero conviene que el próximo agente lo lea al retomar una campaña con deadlines largos

## Pain Pattern Candidate

- Is this likely to repeat? yes
- Suggested severity: high
- Candidate owner: equipo Echo Forge (producto) para el timeout del `cmd_executor` del worker MT5; dueño de la plataforma para el verificador de rollout y el namespace del MCP temporal
- Promote to L3 memory? defer — el aprendizaje ya quedó en la skill del repo y en el checkpoint del proyecto; falta que el fix de producto lo cierre

## One Next Improvement

- Registrar en el runbook de la flota la lectura de dos fuentes para diagnosticar un backtest MT5: el log del `Tester` (¿pasó?) y el log de sesión del worker (¿el executor cerró?), y tratar `terminal64` con CPU plana + `LiveUpdate timeout on stop` como cuelgue de shutdown con timeout efectivo ausente.
