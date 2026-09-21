---
type: change_log
schema_version: 1
scope: session
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Echo]]"
project: "[[Echo — Producto Integrado]]"
application:
entities:
  - "[[Echo]]"
  - "[[Echo Forge]]"
  - "[[Aranea]]"
related:
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[Echo + Echo Forge — Deferred Certification Backlog]]"
  - "[[PostgreSQL FK KEY SHARE exige UPDATE en tablas write-once]]"
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

# 2026-09-21-echo-forge-dev-ingest-close

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `30-resources/aranea/07-integration/Echo + Echo Forge — Environment Contract.md` (§5.4 + reconciliación §7)
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md`
  - `10-projects/Echo/agentes/Echo — Live Platform V1.md`
  - `10-projects/Echo/agentes/Echo — E-04 Forge Ingestion E1.md`
  - `10-projects/Echo/agentes/Echo Forge — Factory V2 Completion.md`
  - `10-projects/Echo/Echo — Producto Integrado.md`
  - `80-agents/memory/public/known-errors/postgres-fk-key-share-requires-update.md`
  - `80-agents/journal/agent-runs/2026-09-21-cursor-grok-echo-forge-dev-ingest-close.md`
  - este change_log
- **Fuera del vault:** release Daedalus `/home/kor/opt/echo-dev/releases/2360369c3ba406a8bf575f2169993028978f48da`; evidencia `~/aranea/work/echo-dev-ingest-close-20260921/`

## Motivo

- El recovery anterior dejó source y schema listos pero Gateway en `5dd998f1` (503). Esta sesión cierra deploy + ingestión física DEV.

## Fuentes usadas

- Environment Contract §5.1–5.3; FINDINGS 2026-09-21 recovery; worktrees `2360369c` / `a2321cc`; systemd --user; PG `echo-develop`; HTTPIngress Symphony.

## Resolución aplicada

- Publicar Gateway `2360369c` (SHA256 `ef56fff6…`); restart exclusivo `echo-gateway-dev`; GRANT UPDATE a `echo_user` sobre tablas E-04 para FK KEY SHARE; smoke HTTPIngress 201 INGESTED + replay 200 + conflicto 409.
- CERT-E04-01 / CERT-F04-03 no marcados PASS (golden `trading_systems_test` sigue GOLDEN_AUTHORITY_BLOCKED).

## Validación

- `current` → `2360369c…`; PID Gateway 2521367; Core 2479388 intacto; `/health` 200; journal `forge_ingest_misconfigured=false`; PG `promotion_records` `338bd937-…` status INGESTED.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- `ln -sfn releases/5dd998f16aea7b2821f460188718d7a6d279829c /home/kor/opt/echo-dev/current` + `systemctl --user restart echo-gateway-dev`. No revertir GRANT ni DROP de tablas E-04. Fila smoke DEV write-once permanece.
