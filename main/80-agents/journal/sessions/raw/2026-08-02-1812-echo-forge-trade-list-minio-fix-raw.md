---
type: session_raw
scope: project
created: 2026-08-02
updated: 2026-08-02
project: "[[Echo Forge - Trade List Export Contrato Remoto]]"
entities:
  - "[[Echo Forge]]"
source_session: cursor-6ded3437-echo-forge-trade-list-close-2026-08-02
indexable: false
index_priority: low
tags:
  - kind/session-raw
  - project/echo-forge
---

# Raw — Echo Forge trade_list MinIO fix

- Corrección falso negativo `agents-os.md`: path canónico `VAULT_ROOT/80-agents/agents-os/agents-os.md` (`/Users/rjara/...`), no `rodrigojara` ni sin subdir.
- RCA cluster: plugin Java OK en `___FULL/`; fallas en publish MinIO.
- Bug 1: Stat 404 → transient (clasificador). Fix → worker `0.2.29`.
- Bug 2: Put manifest `Content-Type` en UserMetadata. Fix → worker `0.2.30`.
- Ver [[2026-08-02-echo-forge-trade-list-minio-stat-put-fix]].
