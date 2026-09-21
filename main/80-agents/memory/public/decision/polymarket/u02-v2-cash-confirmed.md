---
type: decision
schema_version: 1
scope: project
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[2026-09-21-u02-protocol-authority]]"
  - "[[2026-09-21-u02-v2-authority-register]]"
aliases:
  - U-02 V2_CASH_CONFIRMED
  - TAKER_PROCEEDS no aceptado
  - U-02 protocol authority
confidence: verified
source_session:
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - kind/adr
  - scope/project
  - area/personal
  - project/polymarket-engine
---

# U-02 — V2_CASH_CONFIRMED (autoridad vigente)

## Contexto

- El parche `d5ce263` (`fix/u02-buy-shares-accounting`) modeló BUY taker fees como recorte de shares (`TAKER_PROCEEDS`), tomando como autoridad el `CalculatorHelper` de `ctf-exchange` V1 archivado.
- La auditoría P0 del 2026-09-21 contrastó contrato V2, docs oficiales y liquidaciones públicas de PE-001 y weather. Informe: `polymarket-engine-datasets/u02-protocol-authority-20260921/REPORT.md`. Change log de auditoría: [[2026-09-21-u02-protocol-authority]].
- Esta nota es la autoridad vigente de unidad de fee para los mercados verificados. No sustituye al padre ni a la continuidad Five-POC; el consolidator debe promover el estado sin reabrir el dictamen.

## Decisión

- Dictamen vigente: **`V2_CASH_CONFIRMED`** para los mercados verificados (PE-001 sports binary CTF Exchange V2; weather NegRisk CTF Exchange V2). BUY cobra fee extra en collateral pUSD y entrega shares completas. SELL recorta collateral.
- `d5ce263` queda **`PATCH_NOT_ACCEPTED_FOR_V2`**: no es el venue vivo; no mergear, no integrar, no usar como baseline de research real. La rama `fix/u02-buy-shares-accounting` y el pin v08 se conservan intactos como histórico.
- `USDC_CASH` (default sintético vacío + `SYNTHETIC_FIXTURE`) coincide en **unidad** con V2. Eso no certifica la fee efectiva.
- **`REAL_FEE_READY=false`**. `fd` no prueba `takerFeeAmount`. El redondeo on-chain observado es 5 dp USDC; el engine usa `TRUNCATE_6DP`. El operador aporta la fee; el contrato sólo valida tope.
- Baseline de integración sigue `feature/five-poc-integration@85e27ff`. v07 (`c38f6c4`) y v08 (`d5ce263` pineado, HEAD U-02 `d62768a`) no se alteran. Sin implementación, refactor, recertificación M4, merge, push, live, órdenes, wallet ni signing.

## Rationale

- Fuente primaria on-chain: PE-001 BUY `0x35f204735b3d0854dc3da5a77a0ff4251cf41ad19a88f4dc569a9b83b7c2de61` en `0xE111180000d2663C0091e4f400237545B87B996B` (180.340000 shares + 2.239820 pUSD fee). Weather BUY `0x5a2269f1f9a9325b7874630b3346040ddd7fef18899cca5c22ee3f38685c5fc8` en `0xe2222d279d744050d28e00520010520000310F59` (483.900000 shares + 0.047040 pUSD fee).
- `Trading.sol` V2: BUY transfiere tokens completos y cobra collateral; `Fees.sol` valida fee vs cashValue en collateral. V1 `calculateFee` BUY sobre token proceeds queda archivado.
- Help Center Maker Rebates (shares on BUY) es lenguaje V1; el FAQ de upgrade + docs `place-orders` (fees on top) coinciden con V2.

## Consecuencias

- Research sobre mercados verificados debe tratar BUY como cash-additive (`USDC_CASH` / V2), nunca como recorte de shares.
- El consolidator no debe reescribir el dictamen ni aceptar `d5ce263` como corrección de venue. Relabel de comentarios/`TAKER_PROCEEDS` queda planificado y no ejecutado.
- Cualquier POC (incluido S02 Sports Reversion) puede citar esta decisión; economía real sigue no certificada.

## Alternativas descartadas

- `V1_SHARES_CONFIRMED`: contradice txs y contrato V2.
- `MIXED_BY_MARKET`: PE-001 y weather usan el mismo mecanismo de unidad (exchanges V2 distintos, misma cobranza en pUSD).
- `PROTOCOL_UNRESOLVED`: la evidencia de liquidación basta para la unidad; no basta para `REAL_FEE_READY`.
- Integrar `d5ce263` “por si acaso”: falsearía cash y payout de canastas 2×BUY en V2.
