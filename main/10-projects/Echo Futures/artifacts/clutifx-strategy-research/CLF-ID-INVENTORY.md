# CLF-ID-INVENTORY — Inventario por ID (mandato Owner 2026-10-24)

Estados: NOT_STARTED · CODED_UNVERIFIED · TESTED · E2E_VERIFIED · BLOCKED_DATA · BLOCKED_SPEC · INVALID · HIST_COMPLETE

> Provenance: reconciliado físicamente contra `~/go/src/github.com/xKoRx/echo-clf` (rama `experiment/clutifx-s01`, commit P2 `f165ef08`) y el catálogo v1.0 de esta carpeta (5 documentos + manifest local). No existe ningún `HIST_COMPLETE` Clutifx: la primera parrilla histórica arranca sólo tras Gate A (mandato §3).

## Capa compartida

| Componente | Estado | Evidencia |
|---|---|---|
| Detectores (16 APIs: RangeChain, Pendiente/Reiniciado, DOL, Bias×4 motores, TurtleSoup×4 modos, Po3, FailureSwing, InsideCandle, RedFlags×3 modos, KeyHours×3 anclas, Exits, Compositor M1→HTF) | **TESTED** | commit `f165ef08`; suite verde 95,4%; arnés anti-lookahead (prefijos densos DST± + grid 2 semanas + canario de reloj); fixtures LONG/SHORT espejo; NOT_READY/errores con causa nombrada |
| Serialización de estado para el contrato Strategy (Encode/DecodeState) | CODED_UNVERIFIED | `snapshot.go` en progreso por P3a (sin commit al corte) |

## Estrategias (IDs del catálogo)

| ID | Estado | Notas |
|---|---|---|
| CLF-STR-002 rango pendiente→DOL | **E2E_VERIFIED** | smoke NQZ6 10 sesiones COMPLETE+reconciled: 11 señales (8 OPEN 5L/3S + 3 CLOSE_ALL), compra real 120 USD, cadena 28-sep reconciliada punta a punta, replay determinista PASS (identidad 75b631b0…); DEV 444 sesiones EN CURSO |
| CLF-STR-006 failure swing | **E2E_VERIFIED** (0 señales en smoke, no-bug) | cadena verificada (1.401 callbacks, warmup ready, gates activos); frecuencia baja ⇒ sonda DEV 444 sesiones EN CURSO (mandato §3) |
| CLF-STR-001 London ideal | NOT_STARTED | P3b EN CURSO (worker): hipótesis versionada FX→NQ |
| CLF-STR-003 NY continuación | NOT_STARTED | P3b EN CURSO |
| CLF-STR-004 NY reversal | NOT_STARTED | P3b EN CURSO |
| CLF-STR-005 refinado multi-TF | NOT_STARTED | P3b EN CURSO; overlay del padre, jamás familia independiente |
| CLF-STR-009 reentrada/rearme | NOT_STARTED | P3b EN CURSO; versión técnica documentada |
| CLF-STR-007 SMT | **BLOCKED_DATA** | sin ES/YM/DXY sincronizado en Hefesto (verificado físicamente 2026-10-23); specs+fixtures de contrato se conservan; PROHIBIDO sustituto NQ |
| CLF-STR-008 noticias | **BLOCKED_DATA** | sin calendario económico con timestamp; PROHIBIDO inferir desde velas |

## Variantes (34 IDs / 35 sets)

| Grupo | Estado |
|---|---|
| C02, C06 (controles implementables ya) | ligados al estado de STR-002/006 (CODED_UNVERIFIED → TESTED cuando P3a cierre) |
| C01, C03, C04 (sesión), C05 (refinado) | NOT_STARTED (P3b) |
| C07 (rearme) | NOT_STARTED (P3b) |
| C08 (contrato SMT/noticias) | BLOCKED_DATA |
| S01–S21 (sustituciones; S12≡C05 equivalencia declarada) | NOT_STARTED tras controles; un eje por vez |
| T01–T04 (interacciones) | NOT_STARTED tras componentes; T05 BLOCKED_DATA |

## Cadena Gate A pendiente por control factible (mandato §3)

fixtures ± → MTF causal → warmup/dedupe/expiry/DST → fail-closed gaps/rollover → **E2E motor real** (señal→MM→Provider→orden→fill→salida→ledger) → replay determinista → **smoke NQZ6 10 sesiones** → (si 0 señales: 60–90 sesiones contiguas de frecuencia) → **congelar versión** (IDs+hashes+specs).

## Corrección de autoridad aplicada

Baseline vigente R03 `ae1b09bc` (89/89) = autoridad READ-ONLY para comparar; no se reejecuta. Trabajo Clutifx en `experiment/clutifx-s01` con linaje desde `ae1b09bc`; sin merges; sin tocar `experiment/campaign-lab-s04`.
