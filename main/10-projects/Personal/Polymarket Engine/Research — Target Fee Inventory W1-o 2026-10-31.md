---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related: []
aliases: []
tags:
  - kind/doc
created: "2026-10-31"
updated: "2026-10-31"
---

# Research — Target Fee Inventory W1-o 2026-10-31

## Propósito

Auditar, **en lectura offline y sólo con evidencia ya capturada**, la identidad de fee del mercado objetivo `5784455` y sus dos assets: extraer del journal sellado W1-j las observaciones de fee de la condición `0x5022…cf2a62` y de ambos tokens, con su recepción real, y pasarlas por el `FeeResolverV1` existente. Es el cierre del hueco declarado en [[Research — Default Suite Isolation W1-nR 2026-10-30]]: la metadata de fee del objetivo estaba **no inspeccionada** («no inspeccionado» ≠ «ausente»). No certifica la fee de settlement, no produce rentabilidad, no abre OOS/live y no altera la regla de L.

## Contenido

### Identidad verificada contra el journal (no contra el path)

- Mercado Gamma `5784455`, slug `bra-cam-cru-2026-10-29-cam`, condición `0x502200735702dab6eacbcfbd60e109f181c25bffadfa5704d2201a8a86cf2a62`, assets `61296…6143` y `50306…9615`, kickoff `2026-10-29T22:30:00Z`.
- `confirmed = true`, `confirmed_by = [gamma_market:5784455, clob_market_details:0x5022…cf2a62]`, `mismatches = []`, `asset_binding_observed_in_journal = true`.
- El episodio es **exploratorio** W1-j (no OOS/holdout), conforme a la metadata de identidad y prereg ya autorizada; no se consultó el corpus reservado.
- Si el journal no hubiera confirmado la identidad, el extractor habría fallado cerrado sin escribir salida (comportamiento verificado en tests sintéticos).

### Journal y conteos exhaustivos (medidos)

- 9236 registros leídos = `durable_seq` 9236 (9222 data + 14 control), 11 186 396 bytes de payload; primera recepción `2026-10-29T20:21:47.072370769Z`, última `2026-10-29T22:21:25.436591589Z`.
- Superficies: `marketws` 9200 · `clobrest` 21 · `engine` (control) 14 · `gamma` 1.
- Gamma: 1 página `/markets`, 100 mercados vistos, 99 omitidos, 1 observación del target (seq 2).
- CLOB: 7 `market_details` del target (seq 4, 955, 1518, 4874, 6417, 7714, 9234) + 14 `tick_size` de los dos assets; **0** lecturas `/fee-rate`.
- Market WS: 9200 frames → `price_change` 7233 · `new_market` 1561 (**todas de otra condición**, 0 del target) · `last_trade_price` 78 (**78/78** del target, ninguno sin fee, ninguno de otro asset) · `book` 168 · `best_bid_ask` 166.
- **Errores de parseo: 0**; el parser tipado de Gamma funcionó y no hizo falta la ruta cruda de respaldo. 102 observaciones fee relevantes.

### Las tres identidades de fee, separadas

| Identidad | Fuente real (capture_seq / recepción) | Raw fee | Tipo FeeResolverV1 | Qué prueba / qué no |
|---|---|---|---|---|
| **market declared/limit** (condición) | Gamma `/markets` (2 / 20:21:49.757812419Z) + 7 CLOB `/clob-markets/{cond}` (4, 955, 1518, 4874, 6417, 7714, 9234) | `makerBaseFee=1000`, `takerBaseFee=1000`, `feesEnabled=true`; `mbf=1000`, `tbf=1000`; `fd={"e":1,"r":0.05,"to":true}`; `r={"ma":4.5,"mi":50,"moas":30}`; `mts=0.01`, `mos=5`; `gst="2026-10-29T22:30:00Z"` | **INTERVAL [0, 1000]** en las tres anclas | Prueba un cap declarado estable en 8 lecturas. No prueba la comisión que el operador cobra al liquidar; `fd`/`r` se preservan crudos sin escala, fórmula ni mapeo a settlement; `gst`/`updatedAt` no acreditan vigencia ni antigüedad de la fee |
| **asset declared/limit** (×2 assets) | heredad del cap de mercado (misma regla del reducer regimes) + tick `0.01` por lectura (seq 5, 956, 1519, 4875, 6418, 7715, 9235 y 6, 957, 1520, 4876, 6419, 7716, 9236) | `maker=1000`, `taker=1000`, `fees_enabled=true` (marcados `declared_asset_inherited`) | **INTERVAL [0, 1000]** (en K y fin: evidencia `trade_observed=0@9199` / `0@8054`) | El `base_fee` **a nivel de asset está AUSENTE**: no se capturó `/fee-rate`; ausencia, no fee 0 |
| **order/trade-informed** (×2 assets) | Market WS `last_trade_price`: asset `61296…6143` **60** trades con `fee_rate_bps="0"` (seq 3832→9199); asset `50306…9615` **18** trades con `fee_rate_bps="0"` (seq 2128→8054) | un solo lexema por asset: `"0"` | **POINT 0 bps** en K y fin (en el ancla de primera evidencia: **UNRESOLVED**, «no fee evidence») | El emisor reportó el lexema `0` para esos 78 trades; bajo el resolver, la identidad trade-observed resuelve `POINT`. No prueba la comisión aplicada a esos trades (podría ser un valor por defecto del emisor o una convención del venue), no es la fee del mercado ni un certificado de settlement, y no habilita `REAL_FEE_READY` |
| **settlement effective** | — | — | **NOT_CERTIFIED** | El resolver nunca infiere la curva de settlement (gap U-02 `base_fee`↔`feeRate`↔settlement) |

El agregado de lexemas por asset quedó explícito (`asset_id` + `count` por fila): 60 y 18, con un solo lexema distinto cada uno, sin mezcla de conteos.

Lectura de las resoluciones: `INTERVAL [0, 1000]` y `POINT 0 bps` son **outputs del `FeeResolverV1` aplicados al conjunto de evidencia del objetivo**, no parámetros. Quedan **separados** de los escenarios congelados del piloto W1-j (A = intervalo condicional `[0, 500]`, S = estrés `1000`), que este inventario no modifica ni adjudica: clasificar evidencia no ordena su aplicación ni habilita cambiar el gate de costes.

### Anclas temporales (corte por `capture_seq`)

- `as_of_first_fee_evidence`: cutoff seq 2 (20:21:49.757812419Z) — lo más temprano que el journal puede probar.
- `as_of_kickoff_K`: cutoff seq 9236 (22:21:25.436591589Z) — el estado **conocido hasta K**; **no** habilita decisiones anteriores ni fee retroactiva: una observación recibida después de una decisión previa no era elegible en esa decisión.
- `as_of_journal_end`: cutoff seq 9236 — estado capturado al cierre, nunca aplicado retroactivamente. En este episodio las dos últimas anclas coinciden porque toda la evidencia fue admitida antes de K (el último registro es 9 min anterior a K).

### Base temporal declarada

`known_at_utc` se deriva de `Envelope.ReceivedWall`: es el **reloj observado de recepción**, no una medición independiente del instante exacto de commit/admisión durable. `capture_seq` es lo que prueba orden y durabilidad, y es el corte de cada resolución. `updatedAt` (Gamma), `gst` (CLOB) y el timestamp de evento (WS, epoch ms) se preservan como campo crudo de venue: **no** prueban fee-effective-as-of, ni vigencia inicial de la fee, ni antigüedad histórica de fórmula; en `gst` el parser sólo lo tipa como timestamp y no se adjudica semántica de fee ni de calendario.

### Qué falta exactamente para la fee efectiva

1. **El mapeo de aplicación (U-02):** ninguna fuente autorizada documenta cómo `base_fee = 1000` y `fd = {e:1, r:0.05, to:true}` se convierten en la comisión efectivamente cobrada (escala, redondeo, papel de `r`/`to`). Sin ese mapeo la identidad de settlement sigue sin certificarse.
2. **Alcance del `0` trade-observado:** el inventario no puede decidir si `fee_rate_bps = "0"` es la comisión aplicada a esos trades, un valor por defecto del emisor o una convención de fee-rate del venue (documentación no disponible en el corpus autorizado).
3. **Ventana post-K:** el episodio cierra 9 minutos antes de K; nada dice sobre la fee vigente después del episodio.

**Próximo paso económico útil (no ejecutado):** con la fee efectiva aún sin certificar, el gate de costes del motor debe seguir usando el intervalo declarado `[0, 1000]` bps como cota superior y el `0` trade-observado como evidencia por trade desde su `capture_seq`, nunca como fee universal. Lo que permitiría mover `REAL_FEE_READY` es documentar el mapeo U-02 con fuente pública del venue o capturar (exploratorio) una lectura `/fee-rate` por asset y un `new_market` del target — en este episodio no hubo ninguno de los dos.

### Límites

- Una sola fuente: el episodio exploratorio W1-j. Sin request de mercado, sin captura nueva, sin proyección, sin DB mutable, sin replay de estrategia, sin P&L ni tuning.
- Ninguna fee se transfiere desde otros mercados o cohortes: la evidencia W1-e (`mbf/tbf 1000`, `fd {e:1,r:0.05,to:true}`, `tick 0.01`, `fee_observed 0`) pertenece a otros cuatro mercados con otra fecha y **no** se usa aquí en ninguna dirección.
- Un campo ausente se reporta ausente; ausencia de captura nunca se lee como fee 0.
- El `POINT 0` trade-informed y el `INTERVAL [0,1000]` declarado son identidades distintas y no se funden.
- `REAL_FEE_READY = false`. La decisión de L del Owner sigue pendiente y no bloquea este inventario.

## Fuentes

- Vault: `10-projects/Personal/Polymarket Engine/Research — Single Episode Public Pilot W1-j 2026-10-29.md` (modo identity, gate OOS id-first) y `Research — Default Suite Isolation W1-nR 2026-10-30.md` (tabla de fees: metadata del objetivo no inspeccionada).
- Metadata autorizada del lote 3: `selection-manifest-identity.json` (sha256 `b2de46c7776033002e43d179123e32681c2990041de4d2de9d5ccd6eedabd7ed`), `prepared-plan-identity.json` (sha256 `ef3a85f0279503610f165c7dda7ed3290bcee01e2298bb1f5383420d78bf1afb`), `identity-evidence.json` (sha256 `f3628a1e6a826aad3a28f326f18cab465f0c55865b7885c21ef9543c26bbd62e`).
- Código: `cmd/feeinventory/main.go` (sha256 `39305a69d334bfb3933f04b323fa5f9da540777b0ae50c0a2cb2f0545f4ef8ee`) y `cmd/feeinventory/main_test.go` (sha256 `a473635cf52bf875315d9d2c382c1ba3355233dbd967fc2a04faa5c006b3c39e`), commit local `7c9adaea59251b39ac1559db1ed63d4566996206` (rama `w0/offline-causal-replay-20261027`, sin push).
- Artefactos del shot: `inventory.json` (sha256 `06da27806d3aa72c6f1ffa89addc73457fe7f64961f7f38352566726ccbeb9ba`), `inventory.md`, `run-receipt.json`, `scout-pack.json` en `validated-baseline/w1-o-fee-inventory-20261031/`.
- Superficies reutilizadas sin duplicarlas: `internal/capture.OpenView` (vista read-only, sin recovery), `internal/protocol.ParseGammaMarkets/ParseGammaEvents/ParseClobMarketDetails/ParseClobFeeRate/ParseClobTickSize/ParseMarketWSFrame`, `internal/regimes.ResolveFee` (`fee_resolver_v1`).
