---
type: session
schema_version: 1
scope: session
created: "2026-09-25"
updated: "2026-09-25"
area: "[[Echo]]"
project: "[[Echo — Producto Integrado]]"
application:
entities:
  - "[[Echo]]"
  - "[[Aranea]]"
  - "[[Echo — Producto Integrado]]"
related:
  - "[[Echo — Production Operational Audit 2026-09-21]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[Echo — Producto Integrado]]"
aliases:
  - echo prod rollout 25-sep
confidence: high
source_session: sess_19545c7e-b154-48a1-b34b-aead5a24fa60
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-09-25 — Rollout Echo DEV→PROD (D1+D3 @ 372af59a)

- **Objetivo:** ejecutar el paso a producción de Echo autorizado por el owner ("haz el paso a prod completo"), punto por punto.
- **Veredicto:** `PROD_ROLLOUT_PARTIAL_EXECUTED` — todo lo alcanzable con capabilities vigentes quedó **ejecutado y verificado en PROD en vivo**; el deploy físico de binarios/front y la metadata Hasura quedan empaquetados con runbook exacto, bloqueados sólo por acceso owner (operator en `.71` y admin secret Hasura PROD).
- **Ejecutado en PROD (en vivo, mercado abierto, sin incidentes):** (1) **BD** `echo` @ .220: migraciones 061–065 verbatim de master + suplementos certificados (CHECK plataforma MetaTrader5/4; GRANT UPDATE identity tables por FK KEY SHARE) — postcheck PASS, backup previo 157.310 filas/67 tablas; (2) **ETCD production:** 4 tokens auth Gateway + CORS (mod_rev 59077–59081, aditivo); (3) **builds** limpios `372af59a` de core/functions/gateway/lab-worker + front dist sin secretos. Salud post: lab 3 min, account_sync segundos, gateway 200, trade_journal intacto.
- **Hallazgo crítico de diseño:** `v3/hasura/` del repo NO contiene event_triggers ⇒ un `hasura metadata apply` directo desde el repo borraría los 6 triggers de config-propagación y rompería el canal de configuración a terminales. El paquete trae `merge_metadata.py` (merge aditivo export vivo + delta repo, triggers intactos) + apply vía HTTP replace_metadata.
- **Artefactos:** workspace `~/aranea/work/echo-prod-rollout-20260925/` (db/, release/ con RUNBOOK-DEPLOY.md y hasura/RUNBOOK-HASURA.md, tool/, etc/); agent-run `2026-09-25-zcode-glm-prod-rollout`; feedback `2026-09-25-echo-prod-rollout-session-feedback`.
- **Próximo paso:** owner ejecuta ventana (≈25 min) con RUNBOOK-DEPLOY.md + RUNBOOK-HASURA.md; luego post-verificación G1–G10 + 72 h y deuda (merge `4aad647b`, AUD-10 GDAXI, WSFMARKETS, alertas).
