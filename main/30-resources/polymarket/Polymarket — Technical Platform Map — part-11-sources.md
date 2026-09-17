## 26. SOURCE REGISTRY — IDs persistentes, URLs oficiales y verificación diferenciada

**Timestamp de registro:** 2026-09-17 02:34:53 UTC. `GET confirmado` significa que durante las pasadas de esta investigación se obtuvo una representación HTTP legible de esa URL; `indexado` significa que el URL se recuperó del índice oficial S01 pero no quedó registrado un GET individual de su cuerpo; `raw NO parseado` impide atribuirle conteos de operaciones o cobertura plena. En GitHub, el SHA de la revisión fijada S34–S34d se corroboró por `fetch_commit` con API oficial; algunos paths también por `fetch` individual, otros únicamente dentro de la diff. Este registro deliberadamente **NO falsifica** el control de 67 URL independientes; RG-06 permanece abierto. Links sin sufijo `.md` son forma canónica navegable publicada en el índice S01, con contenido Markdown equivalente indexado.

| ID | Título | URL oficial durable | Tipo | Retrieval / verificación | Secciones respaldadas |
|---|---|---|---|---|---|
| S01 | Documentation Index / llms.txt | `https://docs.polymarket.com/llms.txt` | índice oficial | GET confirmado; 2026-09-17 02:34:53 UTC | corpus, inventario specs y alcance |
| S02 | API: Getting Started | `https://docs.polymarket.com/getting-started/api` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | hosts y overview |
| S03 | Wallets and Authentication | `https://docs.polymarket.com/trading/wallets-auth` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | wallet L1/L2, flujo credenciales |
| S04 | Markets & Events | `https://docs.polymarket.com/concepts/markets-events` | concepto oficial | indexado; 2026-09-17 02:34:53 UTC | Event/Market/identity |
| S05 | Positions & Tokens | `https://docs.polymarket.com/concepts/positions-tokens` | concepto oficial | indexado; 2026-09-17 02:34:53 UTC | condition, ERC1155, redeem |
| S05a | Manage Positions | `https://docs.polymarket.com/trading/positions/manage` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | split/merge/redeem |
| S05c | Combinatorial Positions | `https://docs.polymarket.com/trading/positions/combinatorial` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | legs/combinatorial module |
| S06 | Market Details | `https://docs.polymarket.com/market-data/market-details` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | market IDs/status/tokens |
| S07 | Prices and Order Books | `https://docs.polymarket.com/market-data/prices-order-books` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | book/prices/history |
| S07a | Prices & Orderbook | `https://docs.polymarket.com/concepts/prices-orderbook` | concepto oficial | indexado; 2026-09-17 02:34:53 UTC | precio UI/book semantics |
| S08 | Real-Time Data | `https://docs.polymarket.com/market-data/realtime-data` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | Market WS/recovery/features |
| S09 | Real-Time Order Updates | `https://docs.polymarket.com/trading/realtime-order-updates` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | User WS order/trade |
| S10 | Sports WebSocket / Real-Time Data | `https://docs.polymarket.com/api-reference/wss/sports` | referencia oficial | GET confirmado; schema de mensaje contrastado S47; 2026-09-17 02:34:53 UTC | sports endpoint y stream; fuente auxiliar S47 |
| S11 | Real-Time Data | `https://docs.polymarket.com/market-data/realtime-data` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | RTDS topic/filter/heartbeat |
| S12 | Chainlink TWAP Prices | `https://docs.polymarket.com/market-data/chainlink-twap` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | Chainlink/TWAP source |
| S13 | Wallets and Authentication / Relayer | `https://docs.polymarket.com/trading/wallets-auth` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | account/wallet relayer; complementar S42 |
| S14 | Session Keys | `https://docs.polymarket.com/trading/session-keys` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | session signer scope/revoke |
| S15 | Place Orders | `https://docs.polymarket.com/trading/place-orders` | guía oficial | GET en investigación previa; indexado; 2026-09-17 02:34:53 UTC | EIP712, DTO, submit, precision/rounding/GTD |
| S16 | Manage Orders | `https://docs.polymarket.com/trading/manage-orders` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | order/trade/cancel; contradicción batch |
| S16a | Get trades — CLOB | `https://docs.polymarket.com/api-reference/trade/get-trades` | REST referencia oficial | GET confirmado; 2026-09-17 02:34:53 UTC | wire {data,count,next_cursor,limit} |
| S17 | Matching Engine Restarts | `https://docs.polymarket.com/trading/matching-engine` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | 425/503/post-only restart |
| S18 | Error Codes | `https://docs.polymarket.com/resources/error-codes` | referencia oficial | indexado; 2026-09-17 02:34:53 UTC | HTTP/model, orderbook-history |
| S19 | Rate Limits | `https://docs.polymarket.com/api-reference/rate-limits` | referencia oficial | GET confirmado en auditoría; 2026-09-17 02:34:53 UTC | IP limits, throttle |
| S20 | CLOB Trading Rate Limits | `https://docs.polymarket.com/api-reference/trading-rate-limits` | referencia oficial | GET confirmado; 2026-09-17 02:34:53 UTC | signer token buckets, tiers, headers |
| S20c | Polymarket Rust CLOB client v2 | `https://github.com/Polymarket/rs-clob-client-v2` | repo oficial | repo en organización verificado; versión exacta no verificada; 2026-09-17 02:34:53 UTC | Rust, balance/update; version/SDK |
| S21 | Fees | `https://docs.polymarket.com/trading/fees` | guía oficial | GET confirmado en auditoría; 2026-09-17 02:34:53 UTC | fee formula/rounding/mínimo/category |
| S22 | Taker Rebate Program | `https://docs.polymarket.com/programs/taker-rebates` | programa oficial | GET confirmado en auditoría; 2026-09-17 02:34:53 UTC | 7 tier/threshold/weights/payout |
| S23 | Maker Rebates Program | `https://docs.polymarket.com/programs/maker-rebates` | programa oficial | indexado; 2026-09-17 02:34:53 UTC | pool category/maker payout |
| S24 | Liquidity Rewards | `https://docs.polymarket.com/programs/liquidity-rewards` | programa oficial | indexado; 2026-09-17 02:34:53 UTC | scoring/current config |
| S25 | Contracts | `https://docs.polymarket.com/resources/contracts` | registry oficial | indexado; direcciones contrastadas TS env; 2026-09-17 02:34:53 UTC | direcciones polygon/audits/proxies |
| S26 | Negative Risk Markets | `https://docs.polymarket.com/concepts/negative-risk` | concepto oficial | indexado; 2026-09-17 02:34:53 UTC | NegRisk/augmented/Other/legacy conversion |
| S27 | Resolution | `https://docs.polymarket.com/concepts/resolution` | concepto oficial | indexado; 2026-09-17 02:34:53 UTC | UMA/Oracle/redeem/liveness |
| S28 | Combo Requesters | `https://docs.polymarket.com/trading/combos/requesters` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | RFQ requester, thresholds/IDs |
| S28a | Combos for Builders | `https://docs.polymarket.com/trading/combos/builders` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | builder gateway |
| S28b | Collateral Return | `https://docs.polymarket.com/trading/combos/collateral-return` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | combo collateral return |
| S29 | How Combos Work | `https://docs.polymarket.com/trading/combos/overview` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | RFQ and combinatorial definitions |
| S30 | Data API v2 release — Predictions Changelog | `https://docs.polymarket.com/changelog/predictions` | changelog oficial | GET confirmado; 2026-09-17 02:34:53 UTC | v1 frozen, D2 cursor/wrapper/host |
| S31 | Public Analytics | `https://docs.polymarket.com/market-data/public-analytics` | guía oficial | indexado; 2026-09-17 02:34:53 UTC | trades/price history/analytics |
| S32 | Predictions Changelog | `https://docs.polymarket.com/changelog/predictions` | changelog oficial | GET confirmado; 2026-09-17 02:34:53 UTC | todos hitos 2026/contradicciones |
| S32a | Migrating to CLOB V2 | `https://docs.polymarket.com/v2-migration` | migration guide oficial | GET confirmado por búsqueda; 2026-09-17 02:34:53 UTC | v1/v2 orders/SDK migration |
| S33 | SDK Changelog | `https://docs.polymarket.com/changelog/sdks` | changelog oficial | GET confirmado; 2026-09-17 02:34:53 UTC | SDK versions/data wrappers/migrations |
| S34 | ts-sdk environments.ts — commit pinned | `https://github.com/Polymarket/ts-sdk/blob/983a10a7579c95043d4099f60873ff7ea817e5a0/packages/client/src/environments.ts` | SDK oficial, permalink SHA | commit y path GET confirmados; 2026-09-17 02:34:53 UTC | host, chain, addresses |
| S34a | ts-sdk approvals.ts — commit pinned | `https://github.com/Polymarket/ts-sdk/blob/983a10a7579c95043d4099f60873ff7ea817e5a0/packages/client/src/actions/approvals.ts` | SDK oficial, permalink SHA | path GET confirmado; 2026-09-17 02:34:53 UTC | ERC20/1155 approval workflows |
| S34b | ts-sdk positions.ts — commit pinned | `https://github.com/Polymarket/ts-sdk/blob/983a10a7579c95043d4099f60873ff7ea817e5a0/packages/client/src/actions/positions.ts` | SDK oficial, permalink SHA | path GET confirmado; 2026-09-17 02:34:53 UTC | CTF vs Router v2 split/merge/redeem |
| S34c | ts-sdk auth.ts — commit pinned | `https://github.com/Polymarket/ts-sdk/blob/983a10a7579c95043d4099f60873ff7ea817e5a0/packages/client/src/actions/auth.ts` | SDK oficial, permalink SHA | path GET confirmado; 2026-09-17 02:34:53 UTC | exact API credential CRUD/headers |
| S34d | ts-sdk typed-data tests — commit pinned | `https://github.com/Polymarket/ts-sdk/blob/983a10a7579c95043d4099f60873ff7ea817e5a0/packages/client/src/actions/orders/typed-data.test.ts` | SDK oficial, permalink SHA | path en diff de commit; independiente GET no confirmado; 2026-09-17 02:34:53 UTC | deposit signed typed data/domain |
| S34e | ts-sdk orders post.ts pinned | `https://github.com/Polymarket/ts-sdk/blob/983a10a7579c95043d4099f60873ff7ea817e5a0/packages/client/src/actions/orders/post.ts` | SDK oficial commit pinned | raw HTTP 200; 2026-09-17 14:48 UTC | deferExec=false and signed order request serializer |
| S34f | ts-sdk Data resolutions.ts pinned | `https://github.com/Polymarket/ts-sdk/blob/983a10a7579c95043d4099f60873ff7ea817e5a0/packages/bindings/src/data/resolutions.ts` | SDK oficial commit pinned | GitHub fetch_file path y SHA comprobado 2026-09-17 14:48 UTC | wire-to-SDK status/enum/sentinel/epoch conversions |
| S35 | Builder Fees | `https://docs.polymarket.com/programs/builders/fees` | programa oficial | indexado; 2026-09-17 02:34:53 UTC | attribution/additional maker/taker builder fees |
| S36 | Official Python unified SDK | `https://github.com/Polymarket/py-sdk` | repo oficial | repo en organización confirmado; 2026-09-17 02:34:53 UTC | unified python sdk |
| S36a | Legacy Python CLOB client | `https://github.com/Polymarket/py-clob-client` | repo oficial, legacy | repo en organización confirmado; 2026-09-17 02:34:53 UTC | legacy notifications/examples, NO protocolo v2 |
| S36b | Previous TypeScript CLOB V2 client | `https://github.com/Polymarket/clob-client-v2` | repo oficial | repo en organización confirmado; 2026-09-17 02:34:53 UTC | former sdk and migration boundary |
| S36c | Previous Python CLOB V2 client | `https://github.com/Polymarket/py-clob-client-v2` | repo oficial | repo en organización confirmado; 2026-09-17 02:34:53 UTC | former sdk and migration boundary |
| S37 | SDK Migration to Unified SDK | `https://docs.polymarket.com/getting-started/migrate-from-previous-sdks` | guía oficial | GET confirmado; 2026-09-17 02:34:53 UTC | unified, old SDK replacement |
| S38 | Geographic Restrictions | `https://docs.polymarket.com/api-reference/geoblock` | referencia oficial | GET por search verificado; 2026-09-17 02:34:53 UTC | compliance; GET polymarket.com/api/geoblock |
| S39 | Gamma OpenAPI YAML | `https://docs.polymarket.com/api-spec/gamma-openapi.yaml` | OpenAPI oficial | URL en S01; raw NO parseado; 2026-09-17 02:34:53 UTC | Gamma path matrix; RG-01 |
| S40 | CLOB OpenAPI YAML | `https://docs.polymarket.com/api-spec/clob-openapi.yaml` | OpenAPI oficial | HTTP 200 raw parsed 2026-09-17 14:48 UTC; 216099 bytes; SHA256 `d993169c2fd17cbc75304c9cd7bc3b6a351fa21f98cbd12dcd4c5dbbca2fedb8` | CLOB REST; RG-01 |
| S40a | Get fee rate | `https://docs.polymarket.com/api-reference/market-data/get-fee-rate` | REST referencia oficial | GET en auditoría previa; 2026-09-17 02:34:53 UTC | fee base bps by token |
| S40b | Get CLOB market info | `https://docs.polymarket.com/api-reference/markets/get-clob-market-info` | REST referencia oficial | GET confirmado en auditoría; 2026-09-17 02:34:53 UTC | market trading flags/fee curve/taker delay contradiction |
| S41 | Data API v2 OpenAPI | `https://data-api.polymarket.com/v2/openapi.json` | OpenAPI oficial | HTTP 200 raw parsed 2026-09-17 14:48 UTC; 144258 bytes; SHA256 `877b955a83df48e862631773a179f446acd0b112d2d0884922af49e83cdf1ff1` | D2 endpoints/wire/RG-01,RG-04 |
| S41a | Legacy Data API OpenAPI YAML | `https://docs.polymarket.com/api-spec/data-openapi.yaml` | OpenAPI oficial | URL en S01; raw NO parseado; 2026-09-17 02:34:53 UTC | Data v1/out-of-scope except migration |
| S42 | Relayer OpenAPI YAML | `https://docs.polymarket.com/api-spec/relayer-openapi.yaml` | OpenAPI oficial | URL en S01; raw NO parseado; 2026-09-17 02:34:53 UTC | relayer methods/transactions |
| S43 | Combo RFQ OpenAPI YAML | `https://docs.polymarket.com/api-spec/combos-rfq-openapi.yaml` | OpenAPI oficial | URL en S01; raw NO parseado; 2026-09-17 02:34:53 UTC | RFQ REST/maker vs requester |
| S44 | Bridge OpenAPI YAML | `https://docs.polymarket.com/api-spec/bridge-openapi.yaml` | OpenAPI oficial | URL en S01; raw NO parseado; 2026-09-17 02:34:53 UTC | funding/withdrawal only |
| S45 | Market AsyncAPI JSON | `https://docs.polymarket.com/asyncapi.json` | AsyncAPI 3.0.0 v1.0.0 | GET JSON confirmado; enumerado; 2026-09-17 02:34:53 UTC | market channel/11 ops/messages |
| S46 | User AsyncAPI JSON | `https://docs.polymarket.com/asyncapi-user.json` | AsyncAPI 3.0.0 v1.0.0 | GET JSON confirmado; enumerado; 2026-09-17 02:34:53 UTC | user channel/6 ops/messages |
| S47 | Sports AsyncAPI JSON | `https://docs.polymarket.com/asyncapi-sports.json` | AsyncAPI 3.0.0 v1.0.0 | GET JSON en auditoría previa; 2026-09-17 02:34:53 UTC | sports channel/3 ops/messages |
| S48 | RFQ AsyncAPI JSON | `https://docs.polymarket.com/asyncapi-rfq.json` | AsyncAPI oficial | HTTP 200 raw parsed 2026-09-17 14:48 UTC; 35338 bytes; SHA256 `6f4d9a814f457a4aa81b7eb7759e6b277491a9131edb35aab6e6b9d45236523b` | RFQ WS; RG-02 |
| S49 | connect-wss legacy/subset AsyncAPI | `https://docs.polymarket.com/developers/open-api/connect-wss.json` | AsyncAPI oficial listado | indexado; variante parcial observada; 2026-09-17 02:34:53 UTC | documentary mismatch vs market asyncapi |
