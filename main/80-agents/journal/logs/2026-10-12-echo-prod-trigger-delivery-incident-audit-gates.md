---
type: change_log
schema_version: 1
scope: session
created: "2026-10-12"
updated: "2026-10-12"
area: "[[Echo]]"
project: "[[Echo]]"
application: "[[echo]]"
entities:
  - "[[Echo]]"
  - "[[30-resources/agents/skills/echo-production-operational-audit/SKILL.md|echo-production-operational-audit]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
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

# 2026-10-12 — Incidente entrega de event triggers PROD + gates G11/G12 en skill de auditoría operacional

## Contexto

Durante la migración TTP MT4→MT5 el owner editó `echo.symbol_mappings` en PROD (domingo 2026-10-11) y el topic compactado `echo.symbol-mappings.v1` nunca lo reflejó: los event triggers PROD llegaban al gateway sin header `Authorization`, el gateway (`authMiddleware` con Bearer obligatorio desde el rollout 2026-09-25) los rechazó 401 y con `num_retries=0` los eventos murieron en silencio. El bridge (mapper variante Kache-Kafka sobre el topic) siguió detransformando nombres MT4 con punto (`NAS100.`, `GER40.`, `XAUUSD.`, `USDJPY.`), los EAs terminaban `Symbol not available` → `feed_count=0` → sin instrument snapshots ni copias. Fuentes de confusión documentadas: (1) `updated_at` no se incrementa en mutaciones del backoffice (policies, symbol_mappings), por lo que los filtros por esa columna sugieren "sin cambios" falsos — la fecha real de escritura se demuestra con `xmin::text::bigint` calibrado; (2) el handler `symbol_mapping_handler.go` no publica tombstone de la key vieja cuando un UPDATE renombra `broker_symbol`, dejando llaves zombie vivas en el topic compactado (purga aplicada por owner vía INSERT con `is_active=false`); (3) el Republish Configs lee la BD directo y no prueba el delivery de triggers. Owner aplicó el fix (headers en los triggers + redeliver/republish) y quedó operativo; `feed_count` y latidos verificados en verde. Los fallos de clase pasaron invisibles a G1–G10 porque el camino E2E de trades seguía vivo en otros brokers.

## Cambios

- Skill `30-resources/agents/skills/echo-production-operational-audit/SKILL.md`: description/updated de frontmatter; Purpose ampliado; nuevos gates G11 (config-flow DB → trigger Hasura → gateway → topic compactado → cache → EA, con queries exactas de `hdb_catalog.event_log`, límite de permisos RO sobre `hdb_catalog`, y verificación de headers de webhooks contra metadata del repo) y G12 (consistencia de estado de trading: cuentas ciegas sin policies, policies hacia cuentas archivadas, cobertura `client_allowed_symbols`↔`symbol_mappings`, latidos y zombies de topic); renumeración de pasos 9–12 → 11–14; Output `GATES: G1..G12`; nuevo Hard Rule sobre `updated_at` no como prueba de recencia (usar `xmin` calibrado o evidencia funcional).
- Índice `80-agents/skills/INDEX.md`: one-liner del skill federado actualizado a G1–G12.
- Sin cambios de código ni infra: la mutación PROD (headers + redeliver + purga) la ejecutó el owner en la sesión.

## Pendientes identificados (owner)

- Backport de los headers `Authorization` a la metadata del repo `v3/hasura/` para que ningún apply futuro los deje pelados.
- Fix de producto en `symbol_mapping_handler.go`: publicar tombstone de la key vieja en UPDATE con cambio de `broker_symbol` (`event.Event.Data.Old` disponible, no usado).
- Limpieza opcional de bindings muertos: policies hacia cuentas archivadas (darwinex 265 filas/3 cuentas, ttp 21/8, orion 7/2, wsf 6/1, the5ers 5/1, ftmo 1/1; el engine las ignora por estado de cuenta).
- Cuenta Axi `3094610` ACTIVE ejecución con cero policies (o se le asignan o se archiva).
- Alerta permanente recomendada: Grafana sobre `hdb_catalog.event_log WHERE delivered=false` (requiere usuario PG con SELECT en `hdb_catalog`) y sobre cuentas ACTIVE sin latido >5 min.
