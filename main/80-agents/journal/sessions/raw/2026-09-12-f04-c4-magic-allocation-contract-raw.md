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

# 2026-09-12-f04-c4-magic-allocation-contract-raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: Cursor Grok 4.6 (TOP CONTRACT/PLANNING)
- Proyecto o entidad: [[Echo Forge — F-04 Magic allocation, version seal and handoff]]
- Objetivo de la sesión: one-shot `BOOTSTRAP → SOURCE RECOVERY → CONTRACT ANALYSIS → SPEC/TASK UPDATE → EVIDENCE → SESSION CLOSE → FEEDBACK → HANDOFF → STOP`. Sin implementar product source.

## Transcript

```
Cold start Agents OS. Entidad F-04. Inspección dirigida symphony@d645ed6, F-01@0509342, Magic V1@ea8be76.
Q1 instrument = sqx.strategies.instrument (AdoptStrategy ← WorkflowSpec).
Q2 direction = sqx.strategies.direction; mapper L/S/B y LONG/SHORT/BOTH.
Q3 AllocateMagicV1(ctx, ns, strategyRef, canonical) conservado; canonical no se parsea.
Q4 replay conflict DecodeMagicV1; migration 015 suficiente.
Requested: TaskSpec magic_number es legado; D9 corregido.
Multi-strategy soportado. E-04 T2.13 one-shot separado.
SPEC+tareas C4.1–C4.6. Padre puente [r]→[/].
```

## Evidencia externa

- FlowRun físico `eb2ebaa0-3056-445a-9d46-0953c25b2516`; release `0.2.97`; 0 allocations persistidas.
