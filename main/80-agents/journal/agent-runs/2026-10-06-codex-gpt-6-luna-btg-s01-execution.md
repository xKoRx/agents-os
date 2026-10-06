---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-06"
updated: "2026-10-06"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
related:
  - "[[BTG-S01 Real History Execution]]"
  - "[[BTG-PLAN]]"
aliases: []
agent_surface: "[[Codex]]"
agent_model: "GPT-6 Luna"
model_source: user
task_type: ops
task_complexity: medium
outcome: blocked
verification: partial
evaluator: agent
user_rework: unknown
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — BTG-S01 Real History Execution

## Trabajo

- **Objetivo:** intentar el primer smoke histórico real autorizado y dejarlo listo para continuar sin inventar datos.
- **Alcance atribuible a esta combinación superficie×modelo:** inspección de acceso local/MCP, build offline del CLI y preparación documental/command templates; no se tocaron fuentes del candidato.
- **Artefactos afectados:** [[BTG-S01 Real History Execution]]; paquete de evidencia local `xKoRx/echo:reports/real-history-execution/`.

## Evidencia

- **Validaciones ejecutadas:** candidato `fb210ac4afeab2315aaa3c424f287c2d9db5a7b3` limpio; build de `echo-backtest` con workspace explícito y `GOPROXY=off`, `GOSUMDB=off`, `GOFLAGS=-mod=readonly` (exit 0); `--help` confirmó las tres rutas nativas; SHA256 del binario `5a20ed5c34fa6bfb0e898aa1e39021bd2dcf1865a8fc93ef394964d538c2e945`.
- **Resultado observable:** el binario local quedó listo. El acceso al directorio NT del usuario de sistema `hermes-ops` fue denegado para `kor`; perfiles SSH disponibles no incluyen Daedalus/Hermes. Se preparó un destino vacío de propiedad `kor` en el workspace BTG-S01 para transferir los originales.
- **Limitaciones de la evidencia:** no se leyeron ni hashearon originales; no hay manifest real, corrida histórica, PnL, throughput real ni reproducción fresca. Perfiles fuente y horizonte quedan pendientes de lectura, no de autoridad adicional.

## Evaluación

%% Scores opcionales 1–5: agregar al frontmatter sólo cuando exista evidencia suficiente. Si son autoevaluados, conservar evaluator: agent. %%

- **Correctness:**
- **Autonomy:**
- **Efficiency:**
- **Tool use:**
- **Overall:**

## Resultado

- **Outcome:** bloqueado por el acceso POSIX al origen; build y command discovery parciales aprobados.
- **Rework posterior:** desconocido.
- **Aprendizaje para comparar herramientas:** el CLI y el build local son suficientes para continuar cuando el Owner copie el corpus; el ambiente no ofrece un perfil remoto documentado para leer directamente como `kor` el home privado de `hermes-ops`.
