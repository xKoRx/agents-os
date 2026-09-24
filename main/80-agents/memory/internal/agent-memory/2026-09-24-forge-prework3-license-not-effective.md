---
type: agent_memory
schema_version: 1
scope: domain
created: 2026-09-24
updated: 2026-09-24
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
related:
  - "[[Echo + Echo Forge — Environment Contract]]"
aliases: []
confidence: verified
memory_state: active
continuity_key: echo/forge-v2-prework-license
load_policy: manual
indexable: true
index_priority: low
trigger: cuando alguien proponga SQX/licencia/worker DEV en Daedalus para Forge, o se reinterprete ENV=production de Forge como defecto
tags:
  - agent/internal
  - kind/agent-memory
  - area/echo
  - project/echoforge
---

# Forge V2 — modelo de ambientes corregido; licencia Daedalus SUPERSEDED (2026-09-24)

## Estado durable

- **El blocker de licencia SQX en Daedalus quedó `SUPERSEDED_BY_OWNER_ENVIRONMENT_CORRECTION`.** El owner corrigió el modelo conceptual: Echo Forge tiene UN solo ambiente operacional (production; flota SQX Zeus/Hera/Kronos + worker Windows Kronos) y sus pruebas físicas se ejecutan allí. No hay requisito de SQX/licencia/worker DEV en Daedalus ni de `dev-win`; Campaign 001 no se bloquea por eso. Canon: [[Echo + Echo Forge — Environment Contract]] §0.
- `ENV=production` de Forge es el ambiente canónico, no fallback/leak/defecto. "Forge production" NO autoriza dinero real (gates owner independientes). Aislamiento de candidatos = cola/prefijo/instancia candidate-local (patrón G7), flota activa intacta.
- Contexto histórico (ya sin efecto operativo): `sqcli` en Daedalus con copia flota rechazaba en línea (`License is not valid for this computer`, HWID `C487C9A88600`); la copia stale (`license=D0C25B`, SHA256 `a25ce029…`) fue retirada con backup en `~/aranea/work/forge-prework3-20260924/`. NO restaurarla. Lección técnica que sobrevive: la identidad de licencia SQX es 100% local (`internal/license.db`); una activación hecha fuera del host no cambia el comportamiento de `sqcli` sin el registro local.
- Runtime candidato DEV del prework (`/sqx-{worker,watcher}/forgev2dev/`, cola `sqx-forgev2-dev-v1`, binarios `7af048f0…`/`b2e9c227…` en `~/aranea/work/forge-prework2-20260924/bin/`): queda como artefacto de investigación bajo premisa corregida, no como requisito de Campaign 001.

## Próximo paso exacto

- Shot 1 de Fase 1 de [[Echo Forge — Operación Real V2]] (milestone único C0+C1+C2) sobre el ambiente operacional Forge canónico; no avanzar C3. C0 incluye revalidar el runtime desplegado (RC 0.2.106 @ `d07cc69` vs baseline `d9032ff8`). No reabrir prework: `PREWORK_REQUIRES_RUNTIME_REVALIDATION` quedó absorbido por C0.
