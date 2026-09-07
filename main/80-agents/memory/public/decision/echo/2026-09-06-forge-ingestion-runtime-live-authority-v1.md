---
type: decision
schema_version: 1
scope: "project"
created: "2026-09-06"
updated: "2026-09-06"
area: "[[Echo]]"
project: "[[Echo - Discovery y Estado]]"
application: "[[echo-core]]"
entities: ["[[echo-core]]", "[[echo-forge]]"]
related: ["[[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]"]
aliases: []
confidence: "high"
source_session: "ECHO-FORGE-TO-ECHO-BOUNDARY-AND-LIVE-AUTHORITY-V1-TOP"
load_policy: "when_project_loaded"
indexable: true
index_priority: high
tags: ["kind/decision", "scope/project", "area/echo"]
---

# Forge ingestion and live authority — Contract disposition V1

## Contexto

[[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] es la autoridad única. Source Echo e25165ba (master remoto04c16bd) y Symphony db8a022; runtime físico actual U. Las decisiones owner previas permanecen D según el ledger.

## Decisión

**PROPOSED / READY TO FREEZE, NOT OWNER-FROZEN.** Recomendaciones: seal executable/inputs posterior a compile, Gateway ingest individual, versión/promoción inmutables, OPEN pin, enrollment físico, raw antes de routing y command/policy snapshot. Contratos exactos sólo en el Resource; este registro no ratifica nuevas D.

## Rationale

GeneratedStrategy no es identidad semántica cross-generación. Promoción, paquete ejecutable y runtime tienen vidas distintas; current pointer y magic no prueban qué ejecutó un trade. Las refs/proofs eliminan el redescubrimiento sin nuevo servicio/framework.

## Consecuencias

- O1: ratificar observation fact y una enrollment canónica por versión. O2: magic canónico vs override, catálogo CC y allocation-before-Apply. O3: no same-account overlap V1 mientras existan posiciones/pending antiguos.
- NEXT EXACT boundary: ratificación O1–O3 → `ECHO-FORGE-LIVE-IDENTITY-WIRE-V1-NORMAL`. Factory actual C1, con B1A/B1B/B2 source presentes y sin nueva cert física.
- No implementación/migraciones/trading. Slices/proofs viven en el Resource y no se duplican aquí.

## Alternativas descartadas

CLOSE por current_version, magic como Strategy, membership desde ranking, ingestion como activation, tabla/proceso por concepto y recompute histórico desde policy mutable. Challenges CH1–CH10 explícitos; no cambio silencioso de freeze.
