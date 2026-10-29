---
type: session
schema_version: 1
status: closed
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
created: "2026-10-29"
updated: "2026-10-29"
source_session: sess_no-legible-desde-superficie-w1j
surface: "[[ZCode]]"
model: "account:zai-individual-coding-plan/GLM-5.3-Flash"
host: sqx-ulab-hefesto-0
related:
  - "[[Research — Single Episode Public Pilot W1-j 2026-10-29]]"
  - "[[Plan — Executable Single Episode Pilot W1-j 2026-10-29]]"
  - "[[2026-10-29-polymarket-w1j-single-episode-feedback]]"
  - "[[2026-10-29-zcode-glm-5.3-flash-polymarket-w1j-single-episode]]"
  - "[[2026-10-29-polymarket-engine-entity-updated]]"
aliases: []
tags:
  - kind/session
  - topic/research-ops
---

# 2026-10-29-polymarket-w1j-single-episode-summary

## Resultado

- **Desenlace terminal del shot: `NO_ELIGIBLES_EN_LOTE`** — captura `NOT_RUN` con causa, análisis `NOT_RUN`, harness del piloto materializado, probado y commiteado. Bootstrap real de Agents-OS ejecutado (constitución, memoria interna global, índice de skills, perfil `rjara-agent-profile`, continuidad de la entidad, prereg v2 y Plan v3).
- Supervisor `pilot-supervisor` (7 archivos `cmd/researchpilot/`, exactamente la allowlist del shot) implementado sobre el Engine real como único productor de journal: `prepare` (discovery acotado con presupuesto durable + manifiesto compatible + plan), `run` (deadlines absolutos V3, pasos seriales con recibo, exclusión fail-closed de escritores, pausa 02:00–08:00 GMT-3, stop-line 8 GB), `analyze` (round trip virtual H=300 s, escenarios 500/1000 bps, taxonomía de 7 estados, sin claims). Gate de source real: suite propia PASS (9/9 casos + negativos económicos sobre `poc-sports`/`economics`/`books`/`regimes` reales con fixture sintético) y `TestMain` produjo `offline-preflight.json` (9 casos + SHA de los 7 fuentes) e `inputs.json` (12 inputs) sólo tras el PASS completo.
- Descubrimiento REAL 2026-10-29T19:28:48Z: 1 GET (1/3), HTTP 200, 100/100 candidatos inspeccionados (presupuesto total del shot), 0 sellados, **0 elegibles** — todos moneyline con kickoff parseable pero «kickoff closer than the 30m preparation margin». Causa raíz declarada sin atenuación: `ascending=true` gastó el presupuesto en los kickoffs más antiguos (pasados, aún activos); el prereg v2 §3 había fijado `ascending=false` para lotes futuros poblados. Página cruda journalizada durable-antes-de-decidir en `OUT/episode`. `run` selló el recibo terminal (exit 0); el primer `run` falló exit 1 por un bug propio de orden (corregido con tests verdes y rebuild antes del segundo, registrado como hecho).
- Commit local `a20e61777b3db57ecea7ade14f9f0d3fc2acfe1f` «Add bounded public episode research supervisor and pilot» (+3554, 7 archivos, sobre `62a819dc09fb715247973451895106f5c9b7cc6d`), árbol limpio, sin push. Sin órdenes, sin auth, sin live, OOS `3901955/3901953` jamás consultados, WS jamás abierto, 12 inputs intactos, workspace 3,03 GB ≪ stop-line 8 GB.

## Limitaciones

- `journal verify` del episodio NOT_RUN (hook denegó la forma manual del engine; el verify vive dentro del motor de pasos de `run`, que no arrancó pasos para un lote vacío). SHA del binario `pilot-supervisor` post-rebuild sin medir (`sha256sum` denegado; `execution-identity.json` preserva el previo al rebuild). gofmt y formas `diff` denegadas por el perfil; el formateo quedó verificado por compilación limpia. El `NO_ELIGIBLES` describe ESTE lote acotado, no el universo (contraste W1-d pasada 8: 100/100 elegibles con `ascending=false`).
- Sin captura no hay análisis económico ni P&L; `REAL_FEE_READY=false` intacto; nada de esto reabre el freeze de producto ni habilita live; Owner sólo cuenta/elegibilidad/fondos/riesgo/activación real.

## Próximo paso

- Decisión de Metis/lanzador (una pieza): nuevo presupuesto de descubrimiento con `ascending=false` (corrección mínima en `discovery.go` + rerun de tests + rebuild) y re-despacho de [[Plan — Executable Single Episode Pilot W1-j 2026-10-29]]; sin proceso esperando, sin captura automática diferida.
