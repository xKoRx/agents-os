---
type: session_feedback
schema_version: 1
scope: system-1
created: "2026-09-24"
updated: "2026-09-24"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[aranea-agent-dev]]"
aliases: []
confidence: verified
share_scope: local
load_policy: manual
indexable: true
index_priority: low
proposed_artifact_class: pattern
tags:
  - kind/session-feedback
  - scope/system-1
  - area/echo
---

# 2026-09-24 — feedback sesión corrección de modelo de ambientes Forge

## Observación

Tres sesiones de prework (2026-09-24) se ejecutaron y bloquearon contra una premisa de ambiente falsa ("Forge necesita runtime/SQX DEV en Daedalus"), derivada legítimamente del texto entonces vigente del Environment Contract ("el ambiente predeterminado para desarrollo y pruebas es DEV", aplicado sin distinguir productos) y de la fila §2 "SQX DEV → Daedalus". La corrección del owner (un solo ambiente operacional para Forge) llegó después de que el costo ya se pagó: instalación SQX en Daedalus, siembra/retiro de license.db, smoke con repro de licencia, y una 3.ª sesión de cierre sobre un gate que dejó de existir.

## Causa estructural

El contrato mezclaba bajo un solo modelo DEV/PROD a dos productos con modelos distintos, y ninguna regla obligaba a validar la **premisa de ambiente** con el owner antes de embarcarse en adquisiciones físicas (instalaciones, licencias, hosts). El bloqueo por "autoridad" se trató como blocker externo cuando en realidad era una contradicción conceptual no escalada.

## Propuesta (proposed_artifact_class: pattern)

Patrón "premisa de ambiente antes de adquisición": antes de ejecutar un prework que exija **adquirir o construir infraestructura nueva** (licencia, instalación, VM, worker), verificar con el owner que la premisa de ambiente del contrato vigente aplica al producto en cuestión — una línea de confirmación habría evitado tres sesiones. La corrección ya materializada (§0 del contrato + router) reduce la recurrencia para Echo/Forge; el patrón es generalizable a otros productos con modelos de ambiente heterogéneos.

## Evidencia

- Bitácora 1.ª–3.ª sesión en `10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2.md` (nota de premisa corregida incluida).
- §0 y banners `SUPERSEDED_BY_OWNER_ENVIRONMENT_CORRECTION` en `30-resources/aranea/07-integration/Echo + Echo Forge — Environment Contract.md`.
- Run register: `80-agents/journal/agent-runs/2026-09-24-zcode-glm53-forge-env-model-correction.md`.
