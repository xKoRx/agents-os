---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D1 Analysis Pack]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
aliases:
  - Echo Futures D2-05A
  - EF Instrument Contract Mapping
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-26"
updated: "2026-09-26"
---

# Echo Futures — D2-05A Instrument Contract

> [!info]+ TOP A result
> D2-05A — Instrument / Contract / Mapping. Design input for D2-05 integration. Echo baseline verified at 372af59a7b83604781346613da01e3d510ea1360 with no delta. No product code was changed.

## 1. Verdict

TOP_A_RESULT = READY_FOR_INTEGRATION.

V1 must separate economic identity from physical tradable identity. Strategy and Signal reference Instrument. A new Operation resolves the execution-context Instrument → Contract mapping exactly once at materialization and pins contract_id. Market-data and execution contexts may roll independently. External vendor/platform symbols are identifiers of a Contract, never Echo identity.

No automatic rollover, rollover engine, symbol ontology or lifecycle timestamp framework is required.

## 2. Minimal model

### Instrument

Instrument is the canonical economic identity used by Strategy.

Minimum fields:

- instrument_id: stable internal identity.
- canonical_symbol: owner-facing canonical root such as NQ, ES or CL; unique in the Echo catalog.
- currency: economic/quote denomination needed by sizing and P&L semantics.
- exchange_session_id: binding to the exchange/session authority resolved by D2-05B.

Asset class and generic market-family taxonomy are omitted in V1. Futures is the only implemented market and the exchange-session binding already supplies the operational classification actually needed.

### Contract

Contract is an expiry-specific physical tradable owned by one Instrument.

Minimum fields:

- contract_id: stable internal identity.
- instrument_id: owning Instrument.
- contract_code: canonical/display contract code such as NQZ6.
- contract_month: year-month identity; exact expiration/last-trade timestamps are not invented until an authoritative source is required.
- tick_size: minimum quoted price increment.
- tick_value: monetary value of one tick for one contract in contract currency.
- contract_multiplier: exchange/economic multiplier when available; it is retained explicitly and is not treated as a universal derivation rule for tick_value.
- quantity_min: minimum executable contract quantity.
- quantity_step: executable quantity increment.
- currency: settlement/P&L denomination for this Contract.
- operational_state: ENABLED or DISABLED for new-risk resolution. This is Echo catalog state, not a claim about exchange lifecycle timestamps.

DISABLED blocks resolution for new risk. It does not rewrite or retarget an existing Operation. A REDUCE/CLOSE for an existing Operation still addresses its pinned Contract; the venue/adapter can reject it and that rejection remains visible.

## 3. External identifiers

Use one bounded ContractExternalIdentifier model rather than one entity per vendor.

Identity:

    contract_id
    identifier_namespace
    purpose
    binding_context_id

Fields:

- contract_id: Echo physical identity.
- identifier_namespace: protocol/platform namespace such as CME, DATABENTO, PROJECTX or NINJATRADER.
- purpose: MARKET_DATA, EXECUTION or PLATFORM_DISPLAY.
- binding_context_id: optional stable market-data source or execution binding when the same namespace can differ by connection/account family.
- external_identifier: vendor/platform value such as a ProjectX contractId or NinjaTrader instrument string.

Provider business identity is not part of this key. Provider and transport are separate concerns; an execution Account reaches the identifier through its execution binding.

ContractExternalIdentifier records for old contracts must remain resolvable after rollover while any historical/live Operation can still reference those contracts.

## 4. Instrument → Contract mapping

Use a single hot InstrumentContractMapping with a bounded context dimension:

    instrument_id
    mapping_purpose = MARKET_DATA | EXECUTION
    context_id
    -> contract_id

For MARKET_DATA, context_id identifies the feed/data-source binding. For EXECUTION, context_id identifies the execution binding used by the Account. No implicit fallback from one context to another is permitted.

This separates two different questions:

1. Which physical Contract is current for NQ in this context?
2. Which native identifier does this adapter/feed use for that Contract?

The first is InstrumentContractMapping. The second is ContractExternalIdentifier.

Example:

    Instrument NQ
      market-data / databento-main -> Contract NQZ6
      execution / projectx-sim    -> Contract NQZ6

    Contract NQZ6
      DATABENTO/MARKET_DATA -> native feed identifier X
      PROJECTX/EXECUTION    -> contractId ABC
      NINJATRADER/PLATFORM  -> NQ 12-26

Strategy never receives X, ABC or NQ 12-26.

## 5. Resolution and manual rollover semantics

For Signal OPEN on an AccountStrategy:

1. Provider/account admission eligibility is evaluated before materialization by D2-05C.
2. Core resolves the Account execution_binding_id.
3. ContractResolver reads the current EXECUTION InstrumentContractMapping for Signal.instrument_id + execution binding.
4. Resolution fails closed if mapping, Contract, required economic specs or execution identifier capability is unavailable.
5. Operation is materialized according to D2-04 with instrument_id, pinned contract_id and embedded effective Contract specs required by MM.
6. All Orders of that Operation inherit the pinned contract_id.

Manual rollover is one hot mapping change by the owner. A mapping update is prospective only.

    NQ -> NQZ6
    create Operation A => A.contract_id = NQZ6

    owner hot update
    NQ -> NQH7

    Operation A remains NQZ6
    next Operation B => B.contract_id = NQH7

No migration, auto-close, synthetic replacement or automatic rollover occurs.

When Signal OPEN arrives while an Operation is already non-terminal, D2-04 sends it to the existing Operation/MM. It therefore continues under the existing pinned Contract; a mapping update does not turn an ADD into the new Contract.

REDUCE/CLOSE/CLOSE_ALL for an existing Operation never re-resolve Instrument → current Contract. They use Operation.contract_id.

If a venue no longer allows closing the old Contract, the adapter reports the real rejection/error. Echo does not silently map the action to the new Contract.

## 6. Units

Pips are not part of the canonical domain.

Definitions:

- price: decimal native quote price.
- point: price-unit delta in the instrument quote convention; it is not a universal monetary unit.
- tick: one tick_size increment.
- contract quantity: number of physical contracts, normalized to quantity_min/quantity_step.
- tick_value: monetary value of one tick per contract in Contract.currency.
- contract_multiplier: economic multiplier/equivalent supplied by Contract metadata.
- currency: explicit denomination of monetary values.

For linear futures sizing, MM can use price distance → ticks via tick_size and then tick_value × quantity. V1 does not require MM to infer tick_value from multiplier. If Contract.currency differs from Account.currency and no explicit conversion authority exists, sizing that requires conversion fails visible; no implicit 1:1 conversion is allowed.

D2-04 Operation snapshot keeps the effective tick_size, tick_value, contract_multiplier and quantity_step it needs. A later catalog edit therefore cannot silently change the economics of a live Operation.

## 7. Persistence and hot configuration

PostgreSQL remains source of truth for Instrument, Contract, ContractExternalIdentifier and InstrumentContractMapping. Hasura/Gateway remain control plane. Hot distribution uses compacted Kafka configuration streams keyed by the stable internal identity/context, following the existing Echo config pattern.

Core owns an in-memory ContractResolver cache that loads compacted state from the beginning and then consumes hot updates. Market-data runtime and execution adapters consume only the catalog slices they need.

The current Bridge ConfigCache pattern is reusable: complete initial load from a compacted topic, ready barrier, atomic upsert/tombstone and live updates. Exact topic/table names are implementation detail, not domain.

Critical fail-closed behavior:

- missing current mapping => no new Operation;
- disabled/malformed Contract => no new Operation;
- missing required native identifier => no new physical submission;
- stale old Contract on an existing Operation => keep the pin and surface adapter failure; never remap.

## 8. Echo V3 physical map

| Current piece | Classification | Why |
| --- | --- | --- |
| v3/sdk/domain/snapshots.go · InstrumentSnapshot · blob d319d0a3587a3d5ec56ed68911cd60d86b096da8 | ADAPT + REPLACE SHAPE | Reuse tick/spec vocabulary and live snapshot ingress idea, but current identity Broker + CanonicalSymbol mixes economic Instrument, broker symbol and physical tradable; it has no expiry Contract. Dynamic quote state also belongs to D2-06, not Contract identity. |
| v3/core/internal/functions/mm_engine.go · MMEngineFn · blob e725ceb0bd056f3312365b96fbd93e6f52fdde5f | REUSE PRIMITIVES / ADAPT INPUT | Existing sizing already consumes tick size/value/contract size. Replace pip/lot assumptions with pinned Contract units; MM remains economic authority. |
| v3/gateway/internal/symbol_mapping_handler.go · SymbolMappingHandler · blob a9364d4a8e40a13bb4562b2870784545293a39c5 | REUSE PATTERN / REPLACE SEMANTICS | Hasura → Gateway → compacted Kafka + tombstones is the right hot-config pattern. broker:symbol → canonical_symbol is not the Futures domain model. |
| v3/bridge/internal/config_cache.go · ConfigCache · blob 1f46133344022b1193e15d0566c2f76e4354ff44 | REUSE | Complete compacted-topic bootstrap, ready barrier and hot update behavior fit Contract/identifier caches. |
| v3/sdk/domain/client_config.go · ClientConfig trading whitelist · blob 587eb5c4db63b101c9f6b672230a4a7769d4e02a | ADAPT | Account-level symbol allow/deny is a useful edge guard, but provider permitted-instrument authority belongs to D2-05C and should use instrument_id, not vendor symbols. |
| Legacy broker symbol mapping persisted in Echo | DEFERRED_DEBT | Keep Forex/CFD compatibility until DT-EF-CROSS-MARKET-INSTRUMENT-02. Do not force expiry semantics onto non-futures. |

## 9. Invariants

- Instrument is canonical economic identity; Contract is physical expiry identity.
- External vendor IDs are mappings, never Echo identity.
- Strategy/Signal never depend on physical vendor symbols.
- Operation pins contract_id exactly once when materialized.
- Mapping hot updates affect only future Operations.
- Every Order/Fill of an Operation carries that Operation's contract_id.
- REDUCE/CLOSE never resolve through current Instrument mapping.
- No automatic rollover exists in V1.
- No universal pips unit exists in the new domain.

## 10. Risks / non-blocking unknowns

- Exact exchange expiration/last-trade timestamp authority remains intentionally absent until needed; contract_month + owner mapping is sufficient for V1 manual rollover.
- ProjectX/other venue behavior when a pinned old contract becomes inactive remains a transport edge. The architectural behavior is already determined: fail visible, no remap.
- Contract catalog correctness is safety-critical. Implementation must validate required specs and may compare venue-reported metadata, but must not silently switch authority at runtime.
- Cross-currency MM is not designed here. V1 can operate exact-currency accounts; mismatches must fail visible until a conversion authority exists.

OWNER_DECISIONS_REQUIRED = NONE.
