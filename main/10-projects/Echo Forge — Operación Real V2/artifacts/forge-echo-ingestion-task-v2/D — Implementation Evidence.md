---
type: doc
schema_version: 1
status: active
area: '[[Echo]]'
related:
- '[[10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2|Echo Forge — Operación Real V2]]'
- '[[Echo — Producto Integrado]]'
aliases: []
tags:
- kind/doc
- area/echo
created: '2026-10-27'
updated: '2026-10-27'
---

# D — Implementation Evidence

## Propósito

Evidencia del Shot 2 (GLM-5.3-Flash Max LOCAL/ZCode, ONE-SHOT 2026-10-27) del programa `forge-echo-ingestion-task-v2`. Estado de entrega: **`FORGE_ECHO_TASK_IMPLEMENTED_LOCAL_CANDIDATE`** — candidato integrado para adjudicación del Primary Manager y QA Shot 3. No certificación independiente ni FULL_CERTIFIED. Ejecutor ≠ QA.

## SHAs y ramas (REMOTE_VERIFIED)

| Repositorio | Rama | SHA | Notas |
|---|---|---|---|
| xKoRx/symphony | `feature/forge-echo-ingestion-task-v2` | `07c9142` (full: ver push) | 1 commit Shot 2 sobre base `lab-v4/shot4-symphony@22f337ca` (ancestry directo) |
| xKoRx/echo | `feature/forge-task-contract-v2` | `2c66e940` | 3 commits sobre `lab-v4/shot4-integration@f93cd4f8` (`5bd93fe8` contracts+EC, `b4d4c8f1` fixes, `2c66e940` gofmt) |
| xKoRx/echo (tag) | `v3/sdk/contracts/v0.0.1-forge-ingestion-task.1` | commit `2c66e940`, subtree `0c727f10` | Versión de prueba inmutable (addendum §2); go.sum del módulo en el repo |
| xKoRx/sdk | checkout dedicado del programa | `c7f11496b6f681687c9e1e41a773a13295640351` | replace `../../sdk` del symphony worktree apunta aquí (fijado, no desconocido) |

Pin Symphony: `sqx/go.mod` require `v0.0.1-forge-ingestion-task.1` + `exclude v0.0.1-lab-v4-shot2.1` (MVS elegía el tag viejo por orden léxico; shared-analytics lo requiere).

## Qué quedó implementado (por frente B)

- **Contrato B§3**: `core/runtime/echo_ingestion_task.go` (config tipada, enums congelados, límites con tech ceilings, matriz B§3.2, campos de productor físico rechazados) + TaskSpec/TaskSource aditivos + validación en `validateTask`/`validateCohortWaves` (carve-out output_cohort).
- **Fuente exacta B§4**: `core/forge/echo_ingestion.go` resolver (4 modos; StageExecution COMPLETED + membership sellada; hijos por binding o `EvidenceChildrenReader` acotado expected+1; cero=ausente, >1=ambiguo; jamás latest; snapshot `EchoIngestionSourceSnapshotV1` write-once como Evaluation Foundation + work-item refs pequeños).
- **Definición B§5**: `adapters/sqx-definition` + helper exportado `magicreadback.ExtractStrategyPortfolioXML` (ZIP entrada única/límite/CRC, jamás fallback; plain-XML = documento entero); manifest `sqx-strategyfile.v1` de contracts.
- **Mapping B§6**: `core/forge/echo_ingestion_map.go` — envelope compartido, SourceEvidenceV2 tipado, CLOSED_SUMMARY net único, PARTIAL_NET + UNKNOWN (CommSwap combinado jamás comisión/swap KNOWN), currency DECLARED obligatoria con TradeSets, histories=[] sólo IF_AVAILABLE/NONE, CURRENCY_EVIDENCE_MISSING/HISTORY_REQUIRED antes de POST; CANONICAL_HISTORY_V2 por decoder shared; MT5_TRADESET_V1 rechazado (D14).
- **Entrega B§9**: `http_ingress_v2_native` Prepare/DeliverPrepared/Recover (BeginAttempt atómico pre-POST; receipt por `DecodeIngestionReceiptV2`+`ValidateNativeIngestionReceiptV2` compartidos en POST y GET; 401/403 conservan UNKNOWN; jamás INGESTED ciego); migración **018** aditiva (scope/destino/bytes canónicos/attempt counters/`echo_source_bindings_v1` insert-once ⇒ SOURCE_BINDING_CONFLICT); store PG nativo.
- **Workflow/wiring B§8**: case en Generic y Group (carriers intactos; FAIL_AFTER_BATCH tras el reporte), activities resolve/batch/finalize, children readers Mongo acotados con `result_key` conservado en `tradeListScope` (omitempty), worker `data_only` (cola propia explícita, bifurca antes de SQX) + registro en physical.
- **Echo addendum**: SourceEvidenceV2 completa; receipt compartido en contracts con scope/`reason_codes` + validator nativo; 0-historias REGISTER_ONLY; EC-01..EC-08 (decoder estricto, EC-02 headDigest+conteos reales en unchanged, EC-03 metadata versional preservada — destapó que `buildJournalHistory` infería `available_at` de actividad y el POST del projector pisaba metadata: corregido UNKNOWN/NOT_DECLARED_BY_JOURNAL).

## Gates (estado honesto)

| Gate | Estado | Evidencia |
|---|---|---|
| A — Functional Contract | **PARCIAL** | Build `./...` rc=0 (go1.27.1; `tools/` redeclare pre-existente fuera del gate). Tests rc=0: runtime (matriz B§3.2, rename O02, UNSUPPORTED_*), sqx-definition (O20), forge, domain, echo-handoff, magic-readback (gate fixture auténtico FAIL idéntico al baseline), metadata-mongo, trade-list. **NOT_RUN**: O01/O03–O19/O21–O24 como E2E integrado. `workflows/` tests fallan IDÉNTICOS en baseline `22f337ca` (worktree limpio verificado) — ambiental, no regresión. |
| B — Echo Ingestion E2E | **NOT_RUN** | Requiere harness integrado (Gateway+PG+artifact store+receipt/readback). La suite completa `sdk/postgres` de Echo sí corre rc=0 sobre PG aislada propia (56438, pipeline rebase.sh replicado). |
| C — The Lab E2E | **NOT_RUN** | Depende de B. |
| D — Authentic Forge Source | **NOT_RUN** | Sin intento de lectura real en esta sesión (tiempo del shot consumido en A); canales MCP aranea RO disponibles para el intento. |
| E — Release/Deploy | **NOT_AUTHORIZED** | Igual que el diseño. |

## Bloqueos y pendientes para el manager (adjudicación → Shot 3)

1. Harness E2E integrado: rehehydrator del snapshot en Ingest (el workflow porta refs; el batch debe cargar el snapshot por ref — hook `IngestEchoBatchRequest.Snapshot` presente, carga por sink pendiente de cablear en el wiring), Gateway real, Temporal real (O18), Lab (O22/O23).
2. Cobertura ≥95% con denominador por paquete nuevo (owner preference) — no medida en este shot.
3. Goldens cruzados del corpus compartido (addendum §2.5) — corpus base presente en contracts; entradas nuevas de source_evidence pending.
4. `validateTradeListTask`/tramo Overview stage=Folder (G7/A5): corrección local sólo si el tramo se usa; no tocado.
5. D: intentar fuente auténtica read-only (durable Evidence PG/Mongo/MinIO reales) antes de declarar BLOCKED_EXTERNAL.

## Recursos y cleanup

- PG harness propia del programa: `/home/kor/aranea/work/forge-echo-task-v2-20261027/harness2/` puerto 56438 (pgboot-bin+dbexec+pre_001+applybase del pipeline probado lab-v4-shot4-20261023; `w.Start()` sin flota). Queda arriba para Shot 3 (PID en `harness2/pgboot.log`).
- Incidente reportable: el pgdata template compartido del workspace viejo (`lab-v4-shot4-20261021/pgdata`, DB `echo_labv4_s4`) fue dropped/parcialmente repoblado por error de DataPath al inicio de la sesión (base desechable de workspace cerrado; reconstruible con el mismo pipeline). No afecta flota ni bases compartidas productivas.
- Worktree sdk dedicado: `/home/kor/aranea/work/forge-echo-task-v2-20261027/sdk` @ c7f11496 (symlink `../../sdk` del worktree symphony).
- Sin PROD, flota, trading, ETCD real, campañas ni migraciones compartidas.

## Entrada Shot 3 (QA adversarial)

QA GLM-5.3-Flash Max LOCAL fresco, sin autoría. SHAs: symphony `feature/forge-echo-ingestion-task-v2@07c9142`, echo `feature/forge-task-contract-v2@2c66e940`, contracts tag `v0.0.1-forge-ingestion-task.1` (subtree 0c727f10), sdk `c7f11496`. Oráculos vinculantes: B§14 O01–O24 + addendum §10. Baselines de atribución: los fallos de `workflows/` y del gate `SQX_AUTHENTIC_FIXTURE` son pre-existentes en `22f337ca` (verificados en worktree limpio); no adjudicarlos al delta sin repro contrario.

## Fuentes

- [[SHOT2 — Local Implementation Mandate]], [[B — Frozen Design]], [[C — Four Shot Delivery Plan]], [[A — Source Authority Report]], [[../Echo/Ingestion V2 — Operational Integration/Forge Task — Contract Addendum|Forge Task — Contract Addendum]].
- Evidencia runtime local: `/home/kor/aranea/work/forge-echo-task-v2-20261027/` (worktrees echo/symphony/sdk + harness2).
