---
type: session_feedback
schema_version: 1
scope: session
created: "2026-10-24"
updated: "2026-10-24"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities: ["[[Echo Futures]]"]
related: ["[[80-agents/agents-os/agent-constitution.md|agent-constitution]]", "[[30-resources/runbooks/echo-futures-strategy-qualification-runbook.md|echo-futures-strategy-qualification-runbook]]"]
aliases: []
confidence: verified
source_session:
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
  - area/echo
---

# 2026-10-24 — ClutiFX qualification-first session feedback

## Pain Pattern Candidate

**Host no verificado al arranque.** La sesión corre EN Hefesto (hostname `hefesto`, 192.168.31.164) y el agente asumió Daedalus sin ejecutar `hostname` local: toda la sesión trabajó por SSH MCP en loopback a la misma máquina (resultado correcto, mecanismo redundante, con timeouts de 30 s y sesiones interactivas que colapsan multilínea como fricción extra). Regla candidata para el arranque: verificar identidad de host local ANTES de elegir canal de ejecución remota; si el target == host local, trabajar en local directo.

**Reportes de gates sin path de receipt.** El reporte previo del ejecutor afirmaba "S02: 0 ready / 15.256 evaluaciones" y el Owner lo citó como antecedente; el receipt físico mostraba 525.959 evaluaciones con 84% ready y 0 señales (el 15.256 era el contador de candidate warmup callbacks). Regla absorbida por el runbook (ya exigida): todo número de estado en un reporte debe citar el path del recibo que lo respalda; los resúmenes de memoria no son evidencia.

**Plantilla sellada vs. reglas resueltas por el perfil.** La spec FULL sellada trae un `rule_set` viejo que el perfil del preset no resuelve (buy window 10:00 vs 09:30; effective_at distinto); la normalización ocurre al componer el PLAN. Tres corridas fallaron por esto antes del hallazgo. Candidato: documentar en el runbook que los builders de planes deben transportar `rule_set_catalog` + `config.provider` desde un PLAN conciliado (no desde la spec plantilla), o incorporar la resolución del perfil al builder.

**Workspace híbrido vault/desarrollo en el mismo home.** El vault (`~/secondbrain/main`) y el run root (`~/echo-work`) conviven en el home de Hefesto; los builders con paths absolutos mezclan ambos mundos y ningún lado es git. Mantener la disciplina actual (entregables pesados fuera de Git, docs compactos en vault) y registrar en el runbook los paths canónicos de Hefesto para evitar rediscovery.
