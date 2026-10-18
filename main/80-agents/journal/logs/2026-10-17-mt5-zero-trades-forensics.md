---
type: change_log
schema_version: 1
scope: session
created: "2026-10-17"
updated: "2026-10-17"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application:
entities:
  - "[[Echo Forge — Operación Real V2]]"
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# change_log — 2026-10-17 · MT5 Zero Trades Forensics (read-only)

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `10-projects/Echo Forge — Operación Real V2/artifacts/MT5-ZERO-TRADES-FORENSICS-20261017/ZERO-TRADES-REPORT.md` (nuevo) — veredicto `MT5_ZERO_TRADES_ROOT_CAUSE_CONFIRMED`: 16/16 `ORDER_EXECUTION_REJECTED` por margen (SL 21 pips → lote 9.5 × contract 10 × margen 4.2–5.6% > depósito 100k en todo el rango de precios 2026); 0 dependencias faltantes, 0 fallos OnInit, 0 mismatch de lógica, 1 defecto latente (MagicNumber int32 truncado); el patrón por tipo lógico es artefacto del SL del robust run; PASS técnico E2E intacto.
  - `.../MT5-ZERO-TRADES-FORENSICS-20261017/ZERO-TRADES-MATRIX.csv` (nuevo) — 16 filas con refs, SL/lote, señales vs rechazos, primera/última señal, causa y nivel.
  - `.../MT5-ZERO-TRADES-FORENSICS-20261017/POSITIVE-CONTROLS.md` (nuevo) — 4 controles (C1/C7/C13/C14) y el discriminador físico (SL→lote→margen), con la degradación transversal de los 14 (6–27% de señales ejecutadas).
  - `.../MT5-ZERO-TRADES-FORENSICS-20261017/DEPENDENCIES-AUDIT.md` (nuevo) — auditoría estática 30/30 (0 DLLs, Sq*.ex5) y física del terminal tester worker-kronos (`C:\MT5\slots\slot-1`).
  - `.../MT5-ZERO-TRADES-FORENSICS-20261017/REMEDIATION-PLAN.md` (nuevo) — R1 clamp de margen en el template MQ5, R2 MagicNumber long, R3 recomputo de fidelidad; sin implementación.
  - `10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2.md` (updated) — entrada de bitácora 2026-10-17 con hallazgos confirmados y estado de la investigación.
  - `80-agents/journal/agent-runs/2026-10-17-zcode-glm53-mt5-zero-trades-forensics.md` (nuevo).
  - `80-agents/journal/feedback/system-1/2026-10-17-mt5-forensics-session-feedback.md` (nuevo).

## Motivo

- Mandato owner ONE-SHOT: explicar con evidencia física por qué 16 estrategias de `flow_example_2` terminaron sin operaciones MT5, sin asumir defectos de estrategia ni dependencias, sin repetir el E2E.

## Fuentes usadas

- MinIO `sqx-strategies`: `durable/mt5-export/v1/8248f7fa…` (270 objetos) y `durable/trade-list/v1/8248f7fa…` (30 TradeSets SQX); artefactos `wave_9/.../09_reretester` (30 `.sqx`).
- PG/Mongo/ETCD de flota vía `fe2q` (read-only); SSH MCP worker-kronos (`mt5-kronos-admin`, read-only) para el terminal tester; CSV durable `FINALISTS-BY-LOGICAL-TYPE.csv`.

## Resolución aplicada

- Sin cambios de producto ni de flota: la investigación es read-only; las correcciones propuestas quedan en REMEDIATION-PLAN para decisión owner/manager.

## Validación

- Sanity programático: 16/16 con 0 deals y rechazos ≥95% de señales; TradeSets SQX coinciden con el CSV durable (1549/4466/3947/1633/115); `sha256:<codehash>` del path MinIO == `run_id` sellado en TradeSets; mágica truncada `durable mod 2³²` verificada en 3 HTM; indicadores Sq*.ex5 verificados por listado físico del terminal.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Borrar la carpeta `MT5-ZERO-TRADES-FORENSICS-20261017/` y revertir la entrada de bitácora; sin efectos colaterales (ningún sistema externo fue mutado).
