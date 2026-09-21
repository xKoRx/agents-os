**Decisión: `GO_RESEARCH`.** PE-001 tiene un par real identificable y el fail-closed del engine se sostuvo (0 `ACCEPT`). La implicación contractual no está demostrada y U-02 no está cerrado: no hay validación económica ni permiso live.

Informe durable: `~/go/src/github.com/xKoRx/polymarket-engine-datasets/pe001-reality-check-20260921/REPORT.md`. Código de producción intacto. `LIVE_DISABLED`. Sesión Agents-OS abierta.

## 1. Checkout y certificación

Worktree de integración `feature/five-poc-integration` en `85e27ff85d466c6522455f1426f6e0c8e23fe157`, limpio. `56e8fac` es ancestro; `c38f6c4` es el pin de evidencia/M4; `c38f6c4..85e27ff` es sólo `certificate-v07.json`. El remoto sigue en `25f578a`; HEAD local no está publicado. RS v0.3 no se tocó. M4 no se recertificó (no hubo código nuevo).

## 2. Par contractual

Identidad admisible, **implicación no demostrada**:

| | Moneyline | Spread ATL −1.5 |
|---|---|---|
| Evento | WNBA `986912` Atlanta Dream vs New York Liberty, `gameId` `13002544`, kickoff `2026-09-22T00:00:00Z` | mismo evento y `gameStartTime` |
| Market | `4358151` | `4778073` |
| Condition | `0x05877726250f4903cbe937cd159419b2be8a9a604f36ae38c062b10b090d4f68` | `0x7a95a6f7dfaae94f0292d96064ff8a0fa94c0940ebee0f6fa0b6ba85915736fb` |
| YES / NO | `69509824…76083` / `11014429…793111` | `40059528…16569` / `55586564…74006` |
| Texto | ganador **con OT**; postpone abierto; cancel 50-50; **sin empate** | ATL por ≥2, si no NYL; **empate → NYL**; postpone abierto; cancel 50-50; **OT no declarado** |
| Fuente | `wnba.com/scores` | `wnba.com/` |
| SHA reglas | `4998c255…b3241` | `3f4ad514…eb9c` |
| Consulta | Gamma HTTP 200, `2026-09-21T12:51:20Z` | misma captura |

`Cover(ATL,−1.5) ⇒ Win(ATL)` valdría si ambas patas liquidan el mismo marcador final. El texto no lo prueba: el spread no declara OT y sí declara empate, contra el axioma basketball v1. Basket PE-001 = YES(ML)+NO(SP): ≥2 → 1, por 1 → 2, derrota → 1, cancel 50-50, postpone no terminal. `proof_status` honesto = `HYPOTHESIS`.

Descartados (no se inventó par sintético): MLB 494880 (no basketball; empate distinto), series NBA sin games, Euroleague/ACB/Greek sin spread, WNBA ya cerrados, FIBA pasado.

Gamma avisó `deprecation: true` y `sunset` 2026-05-01 (ya vencido); el endpoint aún respondió.

## 3. U-02 y economics

Parámetros observados el 2026-09-21 ~12:48–12:51Z: docs Sports `0.05·p·(1−p)` con redondeo 5 dp; Gamma `sports_fees_v3` rate 0.05 exp 1 takerOnly; CLOB `fd {r:0.05,e:1,to:true}` en ambas patas. `/fee-rate` sigue `{base_fee:1000}` (legado, no es la fórmula sports). Factory del engine: sólo `SYNTHETIC_FIXTURE`, `TRUNCATE_6DP`. **`REAL_FEE_READY=NO`.** U-02 reducido, no cerrado. No hay rentabilidad declarable.

REST taker, no midpoint, q=20: ML YES VWAP **0.56** (62 al best), SP NO VWAP **0.48** (921 al best), suma **1.04**, coste **20.80**. Peor payoff si la implicación valiera: 20. Gross **−0.80**. Fee sintética ≈ **0.496**. Worst net ≈ **−1.296**. Canasta secuencial: profundidad puntual sí cubre q=20; no hay atomicidad. Lock de capital no acotado si hay postpone.

## 4. Dataset

Bundle `polymarket-engine-datasets/pe001-reality-check-20260921/` (rs-v03 intacto). Catalog scans `a8a742cf…` / `31d3e11c…`, fingerprint `9d498011d8dc…`. WS `12:53:26Z`–`12:54:12Z`, admitted 177 / refused 0, durable_seq **184**, ambas patas `OBSERVED_USABLE`. Journal captura: research_evidence OK. Replay digest `0829265feb0b4136…` idéntico en schedules `1` y `32,7,1`, `not_reproducible=0`.

SHADOW escribió RUNTIME después: cutoff 2162. El journal de captura pura es 184. Próxima vez: congelar **antes** de shadow. `engine replay` no tiene `--json`.

## 5. Experimento

**H1** (única, pre-registrada): con reglas verbatim, este par no produce `ACCEPT`. Falsación: cualquier `ACCEPT` sin `RELATION_UNVERIFIED` / `RULES_CONTRADICT` / `TERMINAL_STATE_INCOMPLETE`.

**H1 no falsificada.** SCREEN 5/5 `REJECT` `RULES_CONTRADICT`. SHADOW honest: 54 evals, 54 semantic_reject, 0 ACCEPT, 0 fills, outcome `INCONCLUSIVE`, `engine_sha` `85e27ff`. Ceros y rechazos registrados. Skew WS 834 ms > 250 ms.

Diagnóstico (no es H1; COMPARE `identical=false`): forzar OT/no-tie contra el texto → 52 economic_reject + 1 economic_unknown, 0 ACCEPT. Coherente con VWAP 1.04>1. No certifica reglas.

## 6. Auditoría adversarial

La relación escrita no garantiza el payoff. El alcance OT no está emparejado. El libro es pre-partido y corto; skew supera el umbral. Fees observadas, no certificadas. El lock puede extenderse con postpone. Identidad y books son reales; fee y el diagnóstico OT no. Sin retrospectiva de resultado (el partido no se había jugado). Journal post-shadow contaminado: declarado.

## 7. Decisión y mandato mínimo

**`GO_RESEARCH`**: hay evidencia real nueva y el pipeline funcionó en contratos vivos. No es `NO_GO` (no se demostró imposibilidad). No es `ITERATE` de código. No es `REAL_DATA_READY`. `GO_RESEARCH` no autoriza live.

Siguiente mandato mínimo, no un rediseño:

1. Par basketball con el **mismo OT escrito en ambas patas** y sin payout de empate vivo, **o** dictamen del owner de que la cláusula de empate WNBA es boilerplate inerte.
2. Captura WS read-only, journal congelado **antes** de SHADOW; medir la fracción de frames con skew ≤ 250 ms.
3. Reusar SCREEN → REPLAY → SHADOW → COMPARE. Sin órdenes. Sin recertificar M4 salvo código nuevo.

Review humana `c915c11..85e27ff` y publicación del engine siguen abiertas; no se autoaceptaron. Graphify `NOT_RUN` (binario ausente). Notas actualizadas: POC-S03, continuidad §9, bitácora del padre, guía S03, índice/log, change log `[[2026-09-21-pe001-reality-check]]`.s