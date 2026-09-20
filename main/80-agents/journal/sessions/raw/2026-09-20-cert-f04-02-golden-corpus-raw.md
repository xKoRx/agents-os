---
type: session_raw
schema_version: 1
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Echo]]"
project: "[[Echo Forge]]"
entities:
  - "[[Echo Forge]]"
related: []
aliases:
  - cert-f04-02 raw 2026-09-20
confidence: high
source_session:
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-raw
  - scope/session
  - area/echo
---

# 2026-09-20 — CERT-F04-02 golden corpus (raw)

Raw L0 condensado de la sesión F05C-CERT-F04-02 (transcript completo en la superficie; no se vuelcan dumps).

## Línea de tiempo material

1. Bootstrap AGENTS OS (constitución + continuidad + skills index); dominio `aranea`; entidad Echo Forge / backlog / SPEC F-04; checkpoint C13.
2. G0: probes MCP (Temporal RO perfil `aranea` sin los runs → lector gRPC propio en `~/aranea/work/f04-cert-f04-02/g0/`; ETCD 0 keys `/sqx-worker/production/echo`; MinIO 5 effective-inputs; PG RO sólo BD `echo` = `mcp_echo_prod_ro` @ 192.168.31.220; Forge PG = `trading_systems_test` @ misma instancia, user `sqx`, sin identidad autorizada); describe fresco de ambos workflows (Completed 14:23:33Z, 0 pending); resultados: campaña COMPLETED/TARGET_REACHED ×5, promotion (DecisionRef `ed703eeb…`, finalists_v2), seal (5×HANDOFF_CREATED + refs), request ev640 re-extraído.
3. MCP aranea-mongo muerto (`session not found` en todo verbo) → lector Go propio (`~/aranea/work/f04-cert-f04-02/mongo/`, URI credential-less de ETCD); 10 evaluaciones (`forge.evaluations`, `_id` == refs) con artefactos/magic/productor.
4. G1: contrato del golden desde `BuildHandoffManifest`/`HandoffManifestV1` @`25a5122` (worktree C13 sólo-lectura); inventario 25 preimages + evidencia; HTM/scores justificados como no-preimages.
5. G2: download-plan desde refs durables; 25 descargas por presign GET frescos (URLs no persistidas); SHA256+size 25/25; cross-check C13 20/20 + ancla `33937102…`; releases 0.2.103/0.2.104 descargadas (symphony+exe ×2) con `vcs.revision` 4/4 (symphony 0.2.104 `a81aa5a1…` y exe `c250d7dd…` EXACT vs C13).
6. G3: worktree desechable @`25a5122` + symlink sdk + `goldenrecompute` (recetas reales); 5/5 PASS: readbacks, logs 0-errors (`CompileLogReportsZeroErrors`), effective-inputs reproducidos byte-exacto, VersionRefs/IdempotencyKeys == Temporal, allocation_refs; worktree eliminado sin residuo (dirty foráneo del árbol C13 intacto).
7. Log del productor: grep + sftp-download de `/var/log/symphony/symphony-worker.log` en sqx-zeus (26 líneas 14:23:32Z: fetches de los 20 objetos + uploads/already-exists de effective-inputs con etags == MinIO; 1 key redactada por sanitizador MCP).
8. G4: `CORPUS-MANIFEST.json` + README + PROVENANCE + tools; permisos 700.
9. G5: `tools/validate.py` PASS; negativos (byte mutado→1; objeto ausente→1 limpio tras robustecer; identidad manipulada→detectada); recomputación re-ejecutada desde corpus final 5/5; tree digest `4a266cba…`.
10. G6 veredicto `CERT_F04_02_PASS` (10/10); G7 `HANDOFF-E04-PACKAGE.md`; G8 deltas (backlog + bitácora Echo Forge + subproyecto F-04) + agent-run + change_log + feedback + L0/L1.

## Decisiones

- PASS con manifests/versions **por referencia** (condición 4 del mandato: "capturados o referenciados bajo garantías durables verificadas"); la limitación se declara en cada superficie, sin inflar ni falsificar provenance.
- Mongo por lector propio RO (canal equivalente, identidad existente sin credenciales) tras muerte del MCP; fricción registrada en feedback, no se inventaron datos.
- Sin reproducir manifests localmente como sustituto del preimage (el body depende de `Decision.ContentDigest`/Evidence en PG); sólo se recomputaron identidades derivables de bytes (VersionRef/IdempotencyKey/allocation_ref/effective-inputs).
