---
type: session-raw
schema_version: 1
created: "2026-09-17"
area: "[[Echo]]"
project: "[[Echo — E-06 Reference Enrollment and Binding]]"
related:
  - "[[Echo — Live Platform V1]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-raw
  - scope/session
---

# 2026-09-17 — E-06 NORMAL WP-A Persistencia (raw)

- Mandato Manager one-shot: NORMAL WP-A exclusivamente (T01–T03), branch `feature/e06-reference-enrollment-binding` @ `acf996ad`, base `5dd998f1`, push FF sin merge. Bootstrap cold-start completo (constitución + perfil + continuidad + INDEX + router `aranea-agent-dev`); entidad E-06 resuelta por búsqueda enfocada.
- Baseline verificado pre-write: worktree dedicado `/tmp/echo-e06-reference-enrollment` (branch correcta @ `acf996ad` == origin, worktree limpio, merge-base == `origin/master` == `5dd998f1`); drift material: ninguno.
- T01: `064_reference_enrollment_binding.{up,down}` — 3 tablas §16, FK compuesta a `uq_strategy_versions_identity_tuple` (061) + FK accounts, CHECKs, 3 UNIQUE parciales (CANONICAL OPEN-admitting / collector claim / overlap vivo), triggers lifecycle §6 (INSERT siempre PREPARED, write-once, transiciones enumeradas, auditoría AFTER SECURITY DEFINER con GUCs `echo.e6.actor/reason`, watermark `GREATEST(proof,barrier)` en trigger, recovery reabre `accepts_opens_to`), vista sin proof crudo, revokes patrón 061/063, widen `active_positions.strategy_id`→text con recreación de `v_trade_stream` (057), down fail-closed umbral exacto 50. Recetas SQL `fn_e6_hash_tagged` con `to_json` ≡ `wire.appendJSONString` (S0) — golden cruzado SQL==Go.
- T02: `reference_binding_store.go` — InsertPrepared (validación S0, map_revision leído del mapping con pin exacto, replay §14 por PK+digest sellado, clasificación UNIQUE/FK por constraint), Ack idempotente, MarkObserving (exige ACK, sella watermark/claim), Recover/Drain/Suspend/Close/AdvanceReadback; transacciones ReadCommitted con GUCs de auditoría.
- T03: tests Go 13/13 — golden §5.1/§13, dominios, replay/conflicto, ACK-gate, watermark exacto e inmutable (incl. recovery), auditoría append-only, unicidad con evidencia UNIQUE SQL directa (UPDATE con claim → `uq_e6_collector_claim`; INSERT cross-namespace mismo magic → `uq_e6_overlap_live`; segundo CANONICAL → `uq_e6_canonical_open_admitting`), FK Version ausente, binding_ref recomputado server-side.
- PG REAL: sin psql/docker/sudo en la máquina → PG 17.11 descartable armado en `/tmp/e06-pg17` (server binarios Zonky Maven 17.11; cliente `postgresql-client-17` PGDG .deb extraído con `dpkg -x` + `libpq5` de Ubuntu vía `apt-get download`; socket unix local, trust, puerto 5499). Harness `run.sh` PASS completo (secuencia en bitácora E-06). `-race` PASS; vet OK; build sdk/gateway/bridge OK.
- Defectos corregidos en iteración: auditoría bloqueada por su propio deny-INSERT (trigger movido a UPDATE/DELETE/TRUNCATE + REVOKE); precedencia de errores same-state (watermark específico antes del genérico); Recover no reabría `accepts_opens_to` (defecto real del store); 6 literales hex de 63; fila >50 antes del widen; pin vs overlap en test (segundo namespace).
- Colateral documentado en `TEST_CHANGE_REQUEST.md` (TC-06-1 identityBWCDB TRUNCATE vs FK 064; TC-06-2 harnesses identity_bwc/analytics_a0 aplican 064 sin 061, repro incluido) — sin editar archivos ajenos.
- Commit `429e5c03`, push FF verificado. Agents OS: nota E-06 (estado/tabla/tareas/bitácora), change_log, agent_run, L0. Feedback separado. Cierre solicitado explícitamente por el owner ("cierra sesión"); sin L1 (la bitácora ya navega).
