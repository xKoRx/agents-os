---
type: change_log
schema_version: 1
scope: session
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-09-04-forge-campaign-v2-stop-policy-schema-mismatch]]"
  - "[[2026-09-04-codex-unknown-echo-forge-release-0293-physical-cert]]"
aliases: []
confidence: verified
source_session: "ECHO-FORGE-RELEASE-0.2.93-AND-FINALIST-FACTORY-V1-PHYSICAL-CERT-NORMAL"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-04-echo-forge-release-0293-physical-cert

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `sqx/activities/watcher/intake.go` observado; sin modificación.
  - Release/deploy 0.2.93 y configuración física efímera.
  - [[2026-09-04-forge-campaign-v2-stop-policy-schema-mismatch]]

## Motivo

- La certificación exigía `sqx-forge-campaign.v2` con replenishment cap; el source exacto lo acepta al validar pero no puede resolverlo como StopPolicy.

## Fuentes usadas

- Source authority, SDK authority, release manifest/binaries, migration 013, fleet 4/4, MT5 6140, watcher logs y decisiones/checkpoints previos de Echo Forge.

## Resolución aplicada

- Se clasificó **A. PRODUCT DEFECT**, se detuvo el watcher y se preservó evidencia. No se hizo patch, no se inició Campaign, no se mutó DB/Mongo/MinIO manualmente y no se ejecutó replay/redelivery.

## Validación

- Gates 0–5 PASS; Gate 6 bloqueado en `resolve ForgeCampaign` con `contract_conflict`. Campaign identity/waves/supply/results: no materializados.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Reversible: resolver el contrato en source, publicar release posterior y repetir la certificación con una identidad nueva; no reabrir la evidencia de esta sesión.
