---
type: agent_memory
schema_version: 1
scope: project
created: "2026-09-27"
updated: "2026-09-27"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
related:
  - "[[Echo Futures — D2-05 Instrument Session Provider]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
aliases: []
confidence: high
memory_state: active
continuity_key: "echo-futures/d2-05-submanager"
supersedes:
superseded_by:
load_policy: when_project_loaded
indexable: false
index_priority: high
tags:
  - kind/agent-memory
  - scope/project
  - agent/internal
  - area/echo
---

# Echo Futures — Continuidad D2-05 SUBMANAGER

## Continuidad

- D2-05 está cerrado por Primary Manager desde 89b4b708c56cfba137b398030a41fce4a291e3be: D2_05_MANAGER_REVIEW = CLOSED. Q6/Q7/Q10 quedan cerradas a nivel D2. No reabrir A/B/C ni el integrado salvo contradicción material nueva.
- Artefacto authority final: [[Echo Futures — D2-05 Instrument Session Provider]]. Repair final SUBMANAGER R15–R18: commit f0373c0d8c6e33c922aaaf8058fd514a7dd40eb5; pin/sweep 61baf10aa5431734f4940ea3e9603f43e76d9735.
- R15: Stage-1 OPEN admission lineariza exclusivamente en echo/provider_rules(account_id) mediante AdmissionRequest/Result; kache/admission snapshot = prefilter/read model, nunca authority.
- R16: capacity owner account-keyed mantiene firm_by_operation + live reservations; TODO Fill Echo (ENTRY/ADD/REDUCE/EXIT/safety/late) emite exposición cumulativa por Operation, soportando NET_ABS/GROSS/GROUP_WEIGHTED sin portfolio aggregate.
- R17: ProviderForceClose hace fan-out determinista sobre el AccountStrategy routing set completo; disabled/close-only identities permanecen routable mientras puedan poseer Operation viva; PG no participa.
- R18: DayBoundaryCache legacy es sólo precursor conceptual; su cache-forever + UTC-23 fallback se ADAPT/REPLACE para Futures. DayBoundary Futures es config explícita hot/readiness-safe dentro del owner account-keyed; unresolved => DENY_NEW_RISK.
- Child artifacts finales siguen válidos: D2-05A Instrument/Contract, D2-05B Session/Calendar, D2-05C Provider/Program/Rules. Checkpoints TOP antiguos que dicen D2-05 en curso son históricos y NO deben ganarle a la nota canónica [[Echo Futures]].
- Estado posterior: [[Echo Futures]] registra D2-06 Market Runtime = ACTIVE_SUBMANAGER_DISPATCH. Esa es la continuación del roadmap.

## Señales de carga

- Cargar con [[Echo Futures]] cuando aparezca D2-05, Provider/Program/RuleSet, Instrument/Contract, Session/Calendar o cuando un agente dude si D2-05 sigue abierto.
- Prioridad de autoridad: [[Echo Futures]] manager gates > integrated D2-05 authority > child A/B/C > esta continuidad > checkpoints TOP históricos.

## Próxima acción

- Continuar exclusivamente con D2-06 bajo su Primary Manager/SUBMANAGER dispatch vigente. Recuperar su mandato/carriles actuales antes de actuar.
