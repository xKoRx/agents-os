# Echo — E-10 Manager Review M6 · E-07 analytical identity repair + T05 completion

**Fecha:** 2026-09-22. **Rol:** manager técnico de Echo. **Repo:** `xKoRx/echo`. **Única branch:** `feature/e09-execution-copy-reconciliation-fidelity`. **Baseline revisado:** `6c7c253173c76cab0b1c6302fcda6dbeef9cf416`. **Master esperado:** `5dd998f16aea7b2821f460188718d7a6d279829c`.

## Decisión ejecutiva

El STOP de T05 es válido y revela un defecto material upstream: E-07 pierde información analítica que ya existe en el boundary Reference. No se re-scopa E-10 para saltarse S0, no se inventan `instrument_id`/side y no se crea calculator alternativo.

Estado: `T05_DQ_SOURCE_ACCEPTED · T05_FORWARD_BLOCKED_BY_E07_CONTRACT_DEFECT · E07_NARROW_REOPEN_AUTHORIZED · T06_T10_NOT_AUTHORIZED · POLICY_RATIFICATION_UNACCREDITED · PHYSICAL_INTEGRATION_PENDING · FINAL_CLOSED=NO`.

## Evidencia contrastada

- T05 publicó FF `a861e73b..6c7c2531` en dos commits y ocho rutas. El forward falla cerrado con `ErrForwardContractInsufficient`; no escribe 063/069 en ese path.
- S0 `contracts.NormalizedOperationV1` exige `instrument_id` no vacío y `side=LONG|SHORT`; S0 permanece READ ONLY.
- Migración 065 no persiste instrumento ni dirección en `raw_trade_events`, `trade_lifecycle` ni `trade_deals`.
- **El dato sí existe antes de E-07:** `domain.ReferenceEvent` ya porta `CanonicalSymbol` + `Side BUY|SELL`; `domain.TradeClose` también porta `CanonicalSymbol` + `Side`.
- `bridge/internal/trade_fact_emitter.go` recibe esos DTOs tipados pero `buildEnvelope` descarta ambos campos al crear `TradeFactEnvelopeV1`. Por tanto el gap no es productor/MQL ni E-10: es pérdida de información en el boundary E-07.
- `TradingFactV1` S0 no tiene esos campos y no se modificará. E-07 ya usa campos locales fuera del Fact S0 (`TradeID`, `OriginPositionID`), por lo que la corrección correcta es una extensión local E-07 pre-integración.

## Autoridad M6-A — extensión local E-07

Añadir al envelope E-07 local, fuera de `contracts.TradingFactV1`:

- `instrument_id`: **CanonicalSymbol observado** del DTO Reference; nunca broker symbol ni lookup posterior.
- `side`: mapping exacto `BUY -> LONG`, `SELL -> SHORT`; cualquier otro valor => fail-closed antes de publicar.

OPEN y CLOSE_ASSERTION de los productores Reference actuales deben portarlos. No inferirlos desde `deal_kind IN/OUT`, magic, prices, comments ni payload opaco.

El wire literal `echo-trade-fact-envelope.v1` puede mantenerse porque E-07 no está integrado/PHYSICAL y la corrección es un erratum pre-release; actualizar SPEC/fixtures. **No modificar S0**.

`FactRefForV1` mantiene su receta frozen. Los nuevos campos sí deben participar en la vista canónica/replay E-07 (o demostrar equivalencia fuerte por raw + validación); el resultado obligatorio es que una divergencia explícita instrument/side jamás converja como replay válido.

## Autoridad M6-B — persistencia 065

Antes de editar 065, NORMAL debe volver a demostrar que 065 no está aplicada en ningún entorno compartido/PROD autorizado por el Environment Contract. Si aparece aplicada: **STOP**; no editar una migración ya desplegada y escalar para una migración aditiva nueva.

Si sigue no desplegada, se autoriza corregir **065 in place** porque aún es source pre-integración, evitando una 070 artificial.

Persistir como mínimo:

- `raw_trade_events.instrument_id`, `raw_trade_events.side` write-once;
- `trade_lifecycle.instrument_id`, `trade_lifecycle.side` como pins analíticos de la operación;
- constraints `side IN ('LONG','SHORT')` y semantic-key de instrument;
- OPEN aceptado debe tener ambos; UNKNOWN/late paths no fabrican valores;
- lifecycle no puede cambiar instrument/side una vez fijados;
- DEAL/MODIFY/CLOSE reutilizan el pin del OPEN; una contradicción explícita se rechaza/cuarentena, nunca reescribe el pin.

No es obligatorio duplicar instrument/side en `trade_deals` si el ledger se une al lifecycle y la ausencia de duplicación queda demostrada. Si el store actual necesita duplicarlos para integridad transaccional, documentar y probar la necesidad antes de ampliar.

Actualizar raw write-once trigger, lifecycle guard, stores y tests de 065. Flujos legacy permanecen byte-semánticamente intactos.

## Autoridad M6-C — completar T05 sólo tras gate E-07

Tras PASS de M6-A/B:

1. Loader T05 consume instrument/side desde lifecycle, nunca raw_payload producer-specific.
2. `DeriveForwardOperations` construye `NormalizedOperationV1` sólo con campos demostrados; faltantes opcionales viajan como `missing_fields`, nunca defaults inventados.
3. `instrument_id = canonical instrument pin`; `side` ya está en vocabulario S0 LONG/SHORT.
4. Reutilizar `contracts.OperationRef`, `SealRecord`, `ValidateOperationSet`, encoder NDJSON canónico, `CanonicalWriter.Write`, `analytics/calculator.Compute` y catálogo S0. No forks.
5. Scope forward: LIVE + engine/plataforma real + `SampleTypeForward` + `SeriesRoleReference`; subject = StrategyVersion/Strategy según autoridad S0; market.instrument_id exacto; execution pin del binding; window EVENT_TIME half-open igual al ensamble. No inventar timeframe si no está demostrado.
6. Source tuple de la operation debe derivarse de identidad durable E-07 (`trade_id` + origin/binding probado) y quedar especificada antes del writer. Si no existe una única receta autoritativa sin invención, STOP en ese punto.
7. Baseline se resuelve desde 063; forward se escribe en scopes/sets nuevos 063 únicamente; replay exacto converge; conflicto sellado aborta.
8. Comparaciones usan solamente `allowed_comparisons`; PF NO_LOSSES, NULL costs y R desconocido conservan semántica fail-closed.

**No se autoriza T06** aunque T05 quede completo.

## Corrección menor DQ

En `RunDataQualityGates`, `Assembly == nil` actualmente marca `Identity=BLOCKED`. Corregir para que sea el gate de liveness/coverage el bloqueado y preservar Identity ya PASS. Es fail-closed hoy, pero la clasificación durable está equivocada. Añadir regresión.

## Gates obligatorios

- rojo→verde del loss-of-information E-07: ReferenceEvent/TradeClose con symbol+side llegan al envelope y a lifecycle;
- BUY/LONG y SELL/SHORT; valor inválido fail-closed;
- replay/digest conflict ante instrument/side divergente;
- 065 up/down/up + write-once + late/open + contradiction;
- E-07 bridge/domain/store/lifecycle suites y BWC legacy;
- E-10 DQ regressions, T04 regressions y T05 physical fixtures;
- un forward real de fixture produce OperationSet/TradeSet/MetricSet válido por S0 + writer E-05;
- writer cero veces ante gates DQ fallidos o contract gap;
- same inputs replay sin filas nuevas; nueva StrategyVersion => scope/set nuevos;
- migrations fuera de la corrección autorizada byte-intactas;
- no DEV/PROD writes, no Forge, E-11/E-12, economic commands ni activation.

Commits atómicos: E-07 contract/domain+Bridge; 065+stores; T05 completion; docs/evidence. FF-only, read-back.

## STOP conditions

STOP si: 065 ya fue aplicada en shared DEV/PROD; symbol/side no pueden demostrarse desde el DTO Reference; aparece otro campo S0 **required** no derivable sin semántica inventada; la receta de source tuple/scope requiere un default arbitrario; se requiere modificar `v3/sdk/contracts/**`; se necesita tocar 066/067 o política owner.

