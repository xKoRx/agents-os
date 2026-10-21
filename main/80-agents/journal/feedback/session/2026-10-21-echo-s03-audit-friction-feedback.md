---
type: feedback
schema_version: 1
scope: session
created: 2026-10-21
updated: 2026-10-21
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Echo Futures — Optimización de Campañas]]"
related:
  - "[[2026-10-21-zcode-glm53-flash-echo-s03-audit]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: "account:zai-individual-coding-plan/GLM-5.3-Flash"
agent_run: "[[2026-10-21-zcode-glm53-flash-echo-s03-audit]]"
session_goal: "S03 auditoría adversarial de la entrega S02 congelada de Echo Futures (campaign-lab)"
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

# Session Feedback - 2026-10-21 - auditoría S03 Echo Futures: ubicación de repo no canónica, evidencia S02 fragmentada y publicación Agents-OS arrastra un shot de retraso

## Context

- Agent surface: ZCode (Hefesto, local).
- Agent model: `account:zai-individual-coding-plan/GLM-5.3-Flash`.
- Agent run: [[2026-10-21-zcode-glm53-flash-echo-s03-audit]].
- Session goal: auditar adversarialmente la entrega S02 congelada `00347f4f` y publicar `audit/s03`.
- Main entity: [[Echo Futures — Optimización de Campañas]].
- Skills used: agents-os-bootstrap, agents-os-agent-run-register, agents-os-session-feedback, agents-os-session-close; router aranea + contrato de entorno Echo.
- Retrieval mode: bootstrap canónico + lectura dirigida por el despacho (sin Graphify por camino crítico de código).
- Artifacts changed: planner (rectificación 4 shots), `audit/s03` en rama `audit/campaign-lab-s03`, agent_run, esta nota, change_log.

## Observaciones (fricción real de ESTA sesión; la fragmentación y los excesos de presupuesto son estado del proceso, no culpa del implementador)

- **La ubicación canónica del checkout de `xKoRx/echo` en Hefesto no es resoluble desde el vault.** El planner, el contrato de entorno (apunta a `/home/kor/opt/echo-dev/`, layout de release) y los recibos (sólo `/home/kor/echo-work/tmp-s02/…`) no nombran el repo real (`/home/kor/go/src/github.com/xKoRx/echo`); un auditor nuevo lo encuentra por `find` de varios minutos. La constitución ya manda registrar `repo + path relativo` desde la entidad (regla 11): falta la fila concreta en la entidad Echo Futures o en el contrato de entorno.
- **La evidencia de S02 quedó repartida en ≥3 superficies**: cierre dentro del repo (`CLOSURE-S02-VERIFY.md`), declaración `trials-s02-v1.json`, recibos pesados fuera del repo (`~/echo-work/tmp-s02/trials-r1/`) y bitácora del planner. La auditoría pudo conciliar todo y los números coincidieron, pero el comparador de conciliación fue ad-hoc del verificador (hallazgo S03-F4): la normalización de identidad debería ser un subcomando del repo para que el recorrido sea reproducible sin re-ingeniería.
- **Los presupuestos de shot se exceden cuando el despacho crece a mitad de camino** (S02-R1 cerró ~195/150 min tras añadir la garantía UNAVAILABLE antes del sellado, autorizado por el Owner). Para que el presupuesto siga siendo una restricción real y auditable, una ampliación a mitad de shot debería re-basar el despacho explícitamente (tope nuevo + hora) en vez de acumularse sobre el original.
- **La publicación de Agents-OS a GitHub arrastra desde el cierre anterior.** Esta superficie sí tiene vía de escritura verificada (git+SSH a github.com funcionando para `xKoRx/echo`), y el vault local no es repo git: el estado más nuevo vive en el vault y el remoto está atrasado al menos un shot. Riesgo real: un agente que arranque desde GitHub hereda gates superseded. Se corrige en el cierre de esta sesión aplicando el delta local sobre un clon fresco y empujando `master` con readback.
- **Nada que achacar al implementador:** las ampliaciones de alcance fueron decisiones del Manager/Owner y el material de S02 permitió auditar sin reparaciones previas; el dictamen desfavorable (cobertura) ya estaba declarado honestamente en el cierre S02.

## Lección accionable

- Registrar el path del repo por entidad/host en la fuente scoped (contrato de entorno o entidad) la primera vez que se toca; el costo de no hacerlo lo paga cada shot siguiente.
- Los comparadores de conciliación usados para aceptar evidencia deben vivir en el repo del experimento, no en el historial del agente.
- PUBLICACION_PENDIENTE debe tratarse como tarea con dueño y shot límite, no como nota de cierre: en la sesión siguiente con vía de escritura, publicar ANTES de empezar el trabajo nuevo.
