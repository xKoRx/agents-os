---
type: change_log
schema_version: 1
scope: session
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
  - "[[POC-S03 — Sports Combinatorial]]"
  - "[[POC-S04 — Weather]]"
related:
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
  - "[[Polymarket Engine — Five-POC Guía Operativa 2026-09-20]]"
  - "[[2026-09-21-polymarket-final-readiness]]"
aliases:
  - "U-02 V1/V2 protocol authority 2026-09-21"
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
  - area/personal
  - project/polymarket-engine
---

# 2026-09-21-u02-protocol-authority

## Cambio

- **Tipo:** updated (notas existentes) + created (este change log y el informe fuera del vault). Sin parche de código, sin merge, sin push.
- **Archivo(s):**
  - `main/10-projects/Personal/Polymarket Engine/Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (§6, §11)
  - `main/10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md` (bitácora)
  - `main/10-projects/Personal/Polymarket Engine/POC-S03 — Sports Combinatorial.md`
  - `main/30-resources/polymarket/00-index.md`
  - `main/30-resources/polymarket/log.md`
  - `main/30-resources/polymarket/Polymarket Engine — Five-POC Guía Operativa 2026-09-20.md`
  - evidencia fuera del vault: `polymarket-engine-datasets/u02-protocol-authority-20260921/REPORT.md`

## Motivo

Mandato owner P0 U-02: dictaminar si `TAKER_PROCEEDS` en `d5ce263` corresponde al venue aplicable de PE-001 y la familia objetivo. No implementar otro parche ni integrar código hasta el dictamen.

## Fuentes usadas

- Worktree integración `feature/five-poc-integration@85e27ff` limpio; worktree U-02 `fix/u02-buy-shares-accounting@d62768a` (código `d5ce263`, pin v08). v07/v08 no reescritos.
- `github.com/Polymarket/ctf-exchange-v2` `Trading.sol` / `Fees.sol`; `github.com/Polymarket/ctf-exchange` archivado `CalculatorHelper.sol`.
- Docs oficiales: Exchange Upgrade 28-04-2026, `docs.polymarket.com/resources/contracts`, `docs.polymarket.com/trading/fees`, `docs.polymarket.com/trading/place-orders`. Help Center Maker Rebates (dateModified 2026-07-21).
- Gamma/CLOB read-only: PE-001 `4358151`/`4778073`; weather NYC `1046925` / condition `0x5427a918…`.
- Liquidación pública Polygon: PE-001 BUY `0x35f204735b3d0854dc3da5a77a0ff4251cf41ad19a88f4dc569a9b83b7c2de61` → CTF Exchange V2; weather BUY `0x5a2269f1f9a9325b7874630b3346040ddd7fef18899cca5c22ee3f38685c5fc8` → Neg Risk CTF Exchange V2. Sin órdenes propias, sin wallet, sin signing.

## Resolución aplicada

Dictamen **`V2_CASH_CONFIRMED`**. El venue vivo cobra BUY fee en collateral (pUSD) y entrega tokens completos. `TAKER_PROCEEDS` modela V1 archivado (fee sobre token proceeds), no el exchange aplicable. `USDC_CASH` coincide en unidad con V2. `REAL_FEE_READY` permanece **false**. Código U-02 no mergeado; integración intacta @ `85e27ff`. Plan de corrección preparado, no ejecutado.

## Validación

- PE-001 `createdAt` 2026-09-08, `negRisk=false`, `feesEnabled=true`, `feeType=sports_fees_v3`, `fd {rate:0.05,exponent:1,takerOnly:true}`.
- Tx PE-001: `to=0xE111180000d2663C0091e4f400237545B87B996B`, `matchOrders`, taker envía 85.196220 pUSD = notional 82.956400 + fee 2.239820; ERC1155 Liberty 180.340000 (completo); `FeeCharged` 2.239820 pUSD; `OrderFilled` side=BUY fee en collateral.
- Tx weather: `to=0xe2222d279d744050d28e00520010520000310F59`, mismas semántica BUY (shares completas + fee pUSD).
- Graphify `NOT_RUN` (binario ausente en PATH; retrieval degradado a búsqueda enfocada).
- Lint de schema del change log: materializado por contrato.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin wallet, secretos ni órdenes; hashes de tx y direcciones de contrato públicos

## Rollback

Revertir los markdown del vault; el informe `u02-protocol-authority-20260921/` es apéndice fuera de Agents-OS y no reescribe rs-v03, pe001-reality-check, hardening-20260921, research-v07 ni research-v08.
