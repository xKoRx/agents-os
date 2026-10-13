---
type: change_log
schema_version: 1
scope: session
created: "2026-10-13"
updated: "2026-10-13"
area: "[[Echo]]"
project: "[[Echo]]"
application: "[[echo]]"
entities:
  - "[[Echo]]"
  - "[[30-resources/agents/skills/echo-production-operational-audit/SKILL.md|echo-production-operational-audit]]"
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-13 — Auditoría operacional PROD post-migración MT5 y post-fix de triggers

## Contexto

Owner solicita auditoría tras la ventana 2026-10-11/12 (incidente event triggers sin header `Authorization` arreglado por owner; migración TTP MT4→MT5 con archive de cuentas MT4) reportando "muy pocas operaciones abiertas". Primera auditoría que ejercita los gates G11/G12 incorporados el 12-oct. Capabilities completas (SSH + PG RO + Hasura RO + ETCD RO + observabilidad RO). Veredicto `OPERATIONAL_DEGRADED`.

## Cambios

- Creado [[Echo — Production Operational Audit 2026-10-13]] con gates G1–G12 completos y regresión contra la auditoría 04-oct (`OPERATIONAL_PASS`).
- Actualizada la bitácora "Estado y realidad" de [[Echo — Producto Integrado]] con el resultado del día.
- Skill `echo-production-operational-audit` sin cambios: los gates G11/G12 del 12-oct fueron suficientes para detectar y acotar la degradación del día (hallazgo en G7, no en la cadena config-flow).

## Evidencia clave

- Fixes del 12-oct verificados en verde: gateway publicó 72 ClientConfigs/48 h con última ola post-fix a las 23:21 UTC del 12-oct vía trigger `accounts_config`; flota 17/17 (3 MT4 + 14 MT5) con latido de segundos y terminales conectadas; bridge ERROR 0/3 h; 0 FAILED/72 h.
- "Pocas operaciones" explicado por config vigente: 10 posiciones en 6 cuentas de 4 señales copiables del master; `magic_260104001` con 0 policies (`NO_EXECUTION_POLICIES` demostrado en logs + DB) y GDAXI `magic_251002035` con sus 2 policies hacia cuentas ARCHIVED (0 legs EXECUTION GDAXI/DAX en toda la historia).
- Hallazgo nuevo AUD-24 (P1): TTP G5 MT5 `504079710` no journaliza — 3 tickets vivos (`18893127`/`18894146`/`18898488`) con cero filas en `trade_journal` por account_id y por ticket global; riesgo activo al próximo cierre del master NDX (posiciones quedarían sólo con TP/SL estático de broker).
- Hallazgo AUD-25 (P2): repo `v3/hasura/metadata/` sigue sin declarar event_triggers ni el header `Authorization` reparado — un apply directo reproduciría el incidente del 12-oct.
- Carry-overs verificados: AUD-14 (2 legs reliquia jun-04, ahora en cuentas `[MIGRATED MT5]` archivadas), AUD-17 (4109 sigue cerrado), AUD-19 (masters INACTIVE con legs REF, benigno).
