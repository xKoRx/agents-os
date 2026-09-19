---
type: change_log
schema_version: 1
scope: session
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Echo]]"
project: "[[Echo — E-05 Analytics Convergence A0]]"
application:
entities:
  - "[[Echo]]"
related:
  - "[[Echo — Live Platform V1]]"
  - "[[Echo — E-02 Control Safety, Auth and Journal Recovery]]"
  - "[[Echo — E-03 Identity BWC]]"
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

# 2026-09-16-e05-shared-dev-rollout-pass

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambios

- [[Echo — E-05 Analytics Convergence A0]]: estado operacional `SHARED DEV ROLLOUT BLOCKED — PREDECESSOR_MIGRATION_MISSING` reemplazado en `## 📊 Estado actual` por `SHARED DEV ROLLOUT PASS` (primera entrada); nueva entrada en `## 📆 Bitácora`; fila de `## 🧱 Entrega de desarrollo` actualizada con `SHARED DEV 063 APPLIED / VERIFIED · SHARED DEV HASURA APPLIED / CONSISTENT · SHARED DEV GRAPHQL READ PASS` y la deuda separada `E-03/061 SHARED DEV NOT_APPLIED`. **`CLOSED — SOFTWARE / INTEGRATED` no cambia**; PROD = NOT DEPLOYED; E-03 no cambia a OPEN y 061 no se atribuye a E-05.

## Verificación

- Enmienda Manager aplicada: 061 no es precondición física de 063 (E-05 additive, sin FK hacia identity, refs S0 en JSON); `062 presente / 061 ausente / 063 aplicada` no se clasifica como migration drift de E-05; NO se ejecutó 061 ni se normalizó el orden histórico.
- Baseline Git PASS: `origin/master` == `master` == `5dd998f16aea7b2821f460188718d7a6d279829c` (fetch previo). Checkout principal permaneció en `feature/e02-control-safety-journal-recovery` `92d0ec2e` con árbol limpio toda la sesión; artefactos leídos vía `git show master:` sin checkout; worktrees E-03 (`echo-verify-e03-*`) intactos; **0 source commits**.
- Artefactos certificados: `063_analytics_convergence_a0.up.sql` sha256 `77dfec65695998316e3cbcddccd8b99c2ef05eddd1d552ed59367ee717156713` y `canonical_analytics.yaml` sha256 `690bb149242cef9118ad8cb7a7e8d9bfa48679204ec1ab14a362618a05001376` @ master `5dd998f1`, idénticos a la evidencia de la sesión bloqueada previa.
- Preflight físico re-confirmado en `echo-develop` (PG 17.6 @ `192.168.31.220`, `mcp_echo_dev_rw`, no recovery): 061 ausente en todos los schemas (7 objetos firma + backups, 0), 062 íntegra (`journal_quarantine` 12 columnas, PK+CHECK, 3 índices, 0 rows), 063/E-05 sin drift (0 objetos), Hasura DEV v2.38.0 consistente y sin tracking E-05.
- **Apply 063** transaccional (BEGIN/COMMIT explícitos, equivalente `psql -1`): vía `run_sql` del Hasura DEV admin ejecutando exactamente el artefacto de master y ningún otro objeto. Justificación material: `mcp_echo_dev_rw` no tiene CREATE en schema `echo` (`has_schema_privilege` = false) y `echo_user` sí (owner de `journal_quarantine`/`trade_journal`/`canonical_trades` y de los objetos nuevos); no se usó ningún runner que pudiese arrastrar 061.
- **Postcondition PostgreSQL PASS** por introspección vía `aranea-postgres-rw`: `echo.canonical_scopes` / `canonical_trade_sets` / `canonical_metric_sets` / `v_canonical_trade_sets` / `v_canonical_metric_sets` con columnas exactas al artefacto; `fn_canonical_a0_write_once`; 3 triggers write-once `BEFORE DELETE OR UPDATE OR TRUNCATE`; PKs, CHECKs y `idx_canonical_*_scope`; FKs exactamente 2 y ambas internas E-05 (`canonical_trade_sets.scope_digest` y `canonical_metric_sets.scope_digest` → `canonical_scopes`); **cero FK hacia objetos 061** (061 no existe en ningún schema); owner `echo_user`; revokes del artefacto aplicados (guard omitió rol inexistente `mcp_echo_dev_ro`; DML de `mcp_echo_dev_rw` proviene de default-ACLs preexistentes, roles sin alterar); 0 rows en las 3 tablas; sin pruebas destructivas TRUNCATE. Estado final: **061 NOT_APPLIED · 062 APPLIED · 063 APPLIED** (válido y autorizado).
- **Apply Hasura** (`canonical_analytics.yaml`): `apply_metadata` del backend pinneado `9ba59f2` verificado en source = `V2ReplaceMetadata` completo fail-closed (`allow_inconsistent` default false). El export JSON (70,953B) excedía el presupuesto de render del cliente (50,000B) y `format: yaml` no compacta en el build desplegado ⇒ export/merge/apply máquina-a-máquina vía JSON-RPC directo a `mcps.lab.aranea.cl:3006/mcp` con el bearer de capability local; merge con aserciones (sólo +2 entradas E-05 sobre 75 tablas, entradas preexistentes byte-estables). Post: `get_inconsistent_metadata` limpio; re-export semánticamente igual al intento; vistas trackeadas con rol `readonly` SELECT-only, columnas exactas al yaml, sin `payload_ndjson`, sin mutators, sin relaciones. `reload_metadata` sólo diagnóstico.
- **GraphQL physical smoke PASS** contra SHARED DEV real con rol `readonly` (curl dentro del contenedor `hasura-graphql` vía profile `docker-echo-dev-operator`; admin secret expandido sólo dentro del contenedor, jamás impreso): naming DEV `echo_<tabla>`; `SELECT {echo_v_canonical_trade_sets, echo_v_canonical_metric_sets}` → arrays vacíos (PASS sin sets, sin datos sintéticos); mutación → `no mutations exist`; `payload_ndjson` → field not found. Lectura física de las vistas por PG: 0 filas.
- No-effects demostrados: PROD PG/Hasura/observability sin ninguna conexión (`-ro` nunca invocados); 061 untouched (post-check 0); 062 untouched (12 cols / 0 rows post-check); 0 Kafka produces; 0 commands; 0 acciones de broker; 0 capital; 0 backfill; 0 cron nuevo; 0 dual-run permanente; writer y `lab-canonical-a0` no lanzados; Hasura PROD untouched; 0 source commits. Sesión SSH cerrada; temporales con credenciales (`/tmp/e05-hasura-apply`) eliminados.

## Runtime (explícito)

- **DEV_ROLLOUT_PASS. Master `5dd998f16aea7b2821f460188718d7a6d279829c`. Target `echo-develop` (DEV PG 17.6 @ `192.168.31.220`) + Hasura SHARED DEV v2.38.0 (`echo_test` → `echo-develop`).** 061/E-03 SHARED DEV = NOT_APPLIED (deuda separada, NO blocker E-05); 062 APPLIED íntegra; 063 APPLIED / VERIFIED; Hasura APPLIED / CONSISTENT; GraphQL readonly = PASS con superficie sin mutations; PROD = NOT DEPLOYED y untouched; no-effects 0. Agents OS actualizado (proyecto E-05 + este change log). Siguiente gate: **MANAGER → OPEN E-06**.
