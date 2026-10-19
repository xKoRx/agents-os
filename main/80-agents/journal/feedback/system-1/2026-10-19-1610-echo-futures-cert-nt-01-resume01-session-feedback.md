---
type: feedback
schema_version: 1
scope: session
created: 2026-10-19
updated: 2026-10-19
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[Echo Futures — Runtime Pools]]"
related:
  - "[[aranea-mcps-expert]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run:
session_goal: RESUME-01 de CERT-NT-01 (reanudación bloqueada por P1 productivo)
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

# 2026-10-19-1610-echo-futures-cert-nt-01-resume01-session-feedback

## Observación

- **MCP aranea sin conectar en la sesión:** ssh/flink/kafka/etcd no vinieron registrados como tools; el helper HTTP crudo sobre `~/.zcode/cli/config.json` (extendí `mcp_ssh_call.sh` a `mcp_call.sh <server> <tool> <args>`) fue la vía operativa para SSH/Kafka/Flink REST. Coste: re-initialize por llamada (~1.3 s) y cada tool call funciona, pero el workflow no descubre los tools sin el truco.
- **`profile` opcional con default a otro host:** `sftp-download` sin `profile` golpeó `sqx-zeus` en silencio ("No such file") cuando apuntaba a `docker-echo-dev-operator` (.75). Casi-miss de blast radius; el `profile` debe ir SIEMPRE dentro de los args JSON.
- **Timeout efectivo de Bash ~30 s en llamadas MCP lentas:** `docker logs` completos sobre logs gigantes cuelgan la llamada aunque se pida timeout mayor; acotar siempre con `--tail`/`--since` o extraer a archivo en el host remoto y leer por rangos (`sed -n`).
- **PowerShell 5 en dev-win:** sin `&&`, `$` y `$_` se pierden por el transporte en comandos largos; `Get-WinEvent` funcionó donde `Get-EventLog` con scriptblock falló; comandos cortos y partidos en varias llamadas.

## Pain Pattern Candidate

- Registro lazy de estados en StateFun: un typename inválido sólo explota con el PRIMER mensaje real (estado latente durante horas con feed congelado). El harness Go no valida la gramática del runtime Java (`<namespace>/<name>`); validación de typenames en test = gap estructural del pipeline de pruebas del release.
