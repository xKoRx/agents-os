---
type: change_log
schema_version: 1
scope: session
created: 2026-09-20
updated: 2026-09-20
area: "[[Echo]]"
project: "[[Echo Forge]]"
application:
entities:
  - "[[Echo Forge]]"
  - "[[Echo + Echo Forge — Deferred Certification Backlog]]"
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
related:
  - "[[Aranea]]"
aliases: []
confidence: verified
source_session: ZCode (daedalus, F05C-CERT-F04-02)
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-20 — Echo Forge CERT-F04-02: golden auténtico RERUN-6 capturado, verificado y persistido (`CERT_F04_02_PASS` / T2.11)

## Cambio canónico

- **Entidades actualizadas por delta, no recreadas:** `main/10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nueva sección `### Delta de golden auténtico CERT-F04-02 — 2026-09-20` con G0–G7 completos y la fricción de la sesión; entrada CERT-F04-02 del backlog marcada **EJECUTADO: `CERT_F04_02_PASS` / T2.11 satisfecho** con puntero al corpus; próxima tarea única → CERT-E04-01); `main/10-projects/Echo Forge/Echo Forge.md` (nueva entrada 2026-09-20 en `## 📆 Bitácora`); `main/10-projects/Echo/agentes/Echo Forge — F-04 Magic allocation, version seal and handoff.md` (bullet de estado: T2.11/CERT-F04-02 satisfecho con corpus y limitación PG; F-04 sigue NOT CLOSED, T2.13 pendiente). Cero cambios a contratos, templates ni a otras entidades.

## Cambio en repos externos (fuera del vault)

- **Ningún commit, push, release ni deploy.** El corpus vive en `~/aranea/work/f04-cert-f04-02/corpus` (permisos 700, destino autorizado por precedente C6; bytes privados fuera de Git y del vault, según política del corpus C6). Cero bytes privados versionados o incrustados en Markdown.
- Recursos efímeros creados y eliminados sin residuo: worktree desechable de recomputación @`25a5122` (+ symlink `sdk`), binarios temporales en `/tmp`. El worktree C13 `~/aranea/work/f04-cert-f04-01-g5/seal-fix` se usó sólo en lectura (su dirty foráneo histórico quedó intacto).

## Evidencia de la sesión

- Corpus: `CORPUS-MANIFEST.json` (inventario/lineage/provenance), 25 preimages verificados (SHA256+size == refs durables de 10 evaluaciones y de keys content-addressed), 10 evaluaciones exportadas, evidencia Temporal/release/control-plane, `VERIFICATION.md` (gates G0–G6, 10/10 criterios del mandato), `HANDOFF-E04-PACKAGE.md` (continuidad CERT-E04-01), `tools/validate.py` (validador contractual, negativos demostrados), `tools/recompute/main.go` (arnés con recetas exactas @`25a5122`). Tree digest de preimages `4a266cba45a6b07a5e9f699a9583a63e8f7b945035dbd9ee895381ca3604a36d`.
- Lecturas de producción: Temporal `sqx-prop` (lector gRPC propio en `~/aranea/work/f04-cert-f04-02/g0/`), Mongo `forge` (lector RO propio en `~/aranea/work/f04-cert-f04-02/mongo/`; el MCP aranea-mongo falló con `session not found`), MinIO presign GET (URLs desechadas, nunca persistidas), ETCD RO, SSH operator sqx-zeus (log del worker vía grep + sftp-download).
- Agent run: [[2026-09-20-zcode-glm-5.3-flash-f05c-cert-f04-02-golden-corpus-pass]].
