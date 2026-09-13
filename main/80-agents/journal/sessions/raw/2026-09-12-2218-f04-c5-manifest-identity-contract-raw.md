---
type: raw_session
schema_version: 1
scope: session
created: "2026-09-12"
updated: "2026-09-12"
area: "[[Echo]]"
project: "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
related:
  - "[[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]"
aliases: []
confidence: verified
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-raw.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-09-12-2218-f04-c5-manifest-identity-contract-raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: Cursor Grok 4.6 (TOP CONTRACT/PLANNING)
- Proyecto o entidad: [[Echo Forge — F-04 Magic allocation, version seal and handoff]]
- Objetivo de la sesión: one-shot `BOOTSTRAP → AUTHORITY RECOVERY → DIRECTED SOURCE REVIEW → ECHO S0 CONTRACT REVIEW → CONTRACT DECISION → SPEC/TASK UPDATE → SESSION CLOSE → FEEDBACK → HANDOFF → STOP`. Sin implementar product source.

## Transcript

```
Pedido: ECHO FORGE F-04 — TOP CONTRACT SESSION. MANIFEST IDENTITY MUST NOT PARSE F-01 CANONICALSTRATEGYID.

Bootstrap Agents OS (cold): constitución, perfil, continuidad, skills index, aranea-agent-dev, agent-project-workflow, sdd-workflow.

Authority recovery: proyecto F-04, SPEC F-04, padre Factory V2. C4.1–C4.6 CLOSED @ bba833d. Residual flaggeado: forge_seal_handoff strategyIdentityFromCanonicalID. T2.11–T2.13 OPEN.

Directed source @ symphony-f04-c4 = bba833d7b57c767d6ce5ebfeae7a7b71b5785782:
- forge_seal_handoff.go:391 llama strategyIdentityFromCanonicalID
- helper parsea CanonicalStrategyID con Split("_") vía ParseMagicV1AllocationIdentity + parts[2] timeframe
- BOTH no mapea a wire; LONG/SHORT sí; no hay OperationSide: LONG incondicional
- RequestedInstrument/Timeframe vienen de WorkflowSpec; observed se toma del parse
- AdoptStrategy persiste instrument/direction/timeframe; C4 SELECT ya lee instrument/direction; timeframe es columna brownfield
- StrategyIdentityView sigue Ref+CanonicalStrategyID (no extender)

Echo S0 @ 91671f6f:
- OperationSide = LONG|SHORT only
- Validate: unknown direction → INVALID_INPUT; timeframe required non-empty; G11/G12 requested==observed==strategy identity (igualdad exacta, no EqualFold)
- CanonicalStrategyID es opaco UTF-8 ≤1024

Decision: C5 nuevo bloque (no reabrir C4). MIGRATION NONE. BOTH fail closed at handoff, no S0 change, no silent LONG/SHORT map. No STOP S0_DIRECTION_MODEL_GAP porque el producto no exige emitir BOTH (C4 + receta PHYSICAL dirección única).
```

## Evidencia externa

- Symphony worktree `symphony-f04-c4` HEAD `bba833d7b57c767d6ce5ebfeae7a7b71b5785782`
- Echo pin `91671f6f46ffa889a79aed0979cb3b4e5821ed33` vía `git show`
- SPEC/proyecto F-04 y padre Factory V2 actualizados in-place
