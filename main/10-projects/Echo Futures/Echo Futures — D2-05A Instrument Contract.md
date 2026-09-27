---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D1 Analysis Pack]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
  - "[[CONTRACT + SESSION SEMANTICS — AUTHORITATIVE EVIDENCE]]"
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

# Echo Futures — D2-05A Instrument / Contract / Mapping

> [!info]+ TOP A result
> D2-05A — Instrument / Contract / Mapping. Diseño técnico V1 del modelo `Instrument`, `Contract`, external identifiers, mapping canónico→físico hot y rollover manual. Input de diseño para la integración D2-05 del SUBMANAGER; no cierra D2-05 ni D2. Autoridades derivadas: [[Echo Futures]] (D2-01/02/03 OWNER_CLOSED), [[Echo Futures — D2-04 Operation Order Fill Position]] (CLOSED R1–R14), [[Echo Futures — D1 Analysis Pack]] (Front E) y [[CONTRACT + SESSION SEMANTICS — AUTHORITATIVE EVIDENCE]]. Baseline física verificada: `xKoRx/echo origin/master = 372af59a7b83604781346613da01e3d510ea1360` (fetch re-verificado, sin delta). No implementa código productivo.

> [!warning]+ SUBMANAGER REPAIR A-R1 — 2026-09-26
> Repair dirigido por el SUBMANAGER sobre el artefacto aceptado-en-dirección; registra dos defectos corregidos sobre la misma base de diseño (nada de lo aceptado se reabrió):
> - **A-R1 — Mapping no representaba "context X":** `InstrumentMapping` pasaba de unicidad `(instrument_id, context)` a identidad `(mapping_context, binding_id, instrument_id)` — ahora conviven varios bindings de market-data y varios execution bindings, cada uno con su Contract corriente propio (§3, §5, casos A-R1-1/2/3).
> - **A-R2 — Seam compartido A↔B↔C sin cerrar:** `exchange` y `product_group` migran a Instrument como única autoridad canónica de grouping (Contract pierde su campo `exchange` propio y lo hereda vía `instrument_id`); B resuelve CalendarResolver con `(calendar_ref, exchange, product_group)` y C evalúa reglas/caps con `(instrument_id, exchange, product_group)` — decisión congelada aquí, no diferida al SUBMANAGER (§2.1, §2.2, §10, caso A-R1-4).
> - Congeladas además las dos resoluciones explícitas: current-Contract selection ≠ vendor external-identifier selection (§4, §5).
> Sin cambios en: pin de Operation, rollover semántico, mono-contract, fail-closed, sin lifecycle timestamps, `version` sigue siendo metadato de config (no revision framework).

## 1. Verdict

```text
D2-05A STATUS: READY_FOR_SUBMANAGER_REREVIEW (post repair A-R1)
```

El modelo V1 separa exactamente dos capas de identidad: **Instrument** es la identidad económica/canónica (NQ, ES, CL) que Strategy/Signal/AccountStrategy conocen; **Contract** es el contrato listado expiry-specific tradable (NQZ6) que Operation pinnnea al materializarse y que las Orders/Fills/Position físicas referencian. Los símbolos de vendors/plataformas (CME display code, ProjectX `contractId`/`symbolId`, NinjaTrader instrument string, feed symbol) son **external identifiers** con provenance por fuente, jamás identidad Echo (C-E08). El mapping `Instrument → Contract` es config hot con identidad por **binding concreto** (`(mapping_context, binding_id, instrument_id)`): varios bindings de feed y varios bindings de ejecución pueden coexistir, cada uno con su Contract corriente y rolando en momentos distintos, sin tocar a Strategy; cada Operation lo resuelve **una sola vez**, dentro de `echo/operation` en la materialización (guard D2-01/D2-04), y el resultado vive embebido en el snapshot de la Operation. Rollover es owner-manual y estrictamente prospectivo.

No se crean: ContractVersion, InstrumentRevision, rollover engine, symbol ontology, vendor subclasses, metadata framework, scheduler de rollover. La evidencia no los sustenta y D2-01 prohíbe el framework de versiones.

## 2. Modelo mínimo

### 2.1 Instrument (identidad económica/canónica)

| Campo | Clase | Nota |
|---|---|---|
| `instrument_id` | **AUTHORITY** | Identidad canónica Echo, owner-controlled (ej. `NQ`). Es el único identificador de instrumento que Strategy/Signal/AccountStrategy conocen. No es un símbolo de venue. |
| `quote_currency` | **CONFIG** (inicializada de spec venue/exchange) | Denominación del precio (NQ → `USD`). Base del modelo de unidades; no se duplica en Contract. |
| `calendar_ref` | **CONFIG** (nullable) | Referencia nominal a la autoridad Session/Calendar de D2-05B (ej. `CME-GLOBEX-EQINDEX`). Es un puntero, no una definición: Instrument/Contract **no embuten** sesiones, horas ni holidays. |
| `exchange` | **AUTHORITY (config-of-record)** | Exchange de listado del producto económico (ej. `CME`). Única copia en el modelo (repair A-R1: migrada desde Contract); dimensión de reglas de C y parte de la identidad calendario de B. |
| `product_group` | **AUTHORITY (config-of-record)** | Único agrupador canónico del modelo (ej. `NQ` para la familia NQ/MNQ, `ES` para ES/MES, `CL`). owner-curated y estable. Es la llave de grouping que B usa para overrides de calendario por grupo (S-E05) y C para permitted-instruments/caps. |

Sin taxonomía ornamental: no `asset_class`, no `display_name`, no segundo eje de grouping. **Full-vs-micro no es un campo de dominio V1** (repair A-R2): NQ y MNQ comparten `product_group`; cuando una regla de C necesite distinguir tamaño, se expresa en la config del RuleSet (sets de instrumentos explícitos o cantidades scopeadas al grupo), porque no existe evidencia de una taxonomía universal de size-class — agregar ese eje sería el taxonomy framework que se quiere evitar. Si un requirement real multi-provider lo demuestra, `product_group` admite extensión de valores sin cambio de identidad. Instrument no tiene lifecycle runtime: es config referencial con tombstone.

### 2.2 Contract (tradable expiry-specific)

| Campo | Clase | Nota |
|---|---|---|
| `contract_id` | **AUTHORITY** | Identidad canónica Echo del contrato listado, única por instrumento (ej. `NQZ6`). Es identidad interna Echo, **no** un ID universal (C-E08: el mismo código es display en otros sistemas). |
| `instrument_id` | AUTHORITY (FK) | Root económico. |
| `contract_year`, `contract_month` | AUTHORITY | Identidad de expiración explícita (ej. 2026-12), no parseada del display code. |
| `display_code` | CONFIG | Código humano default (derivado de root+month; letra CME como convención de display, no identidad). |
| `tick_size` | **CONFIG-of-record** (evidencia venue/exchange) | Fluctuación mínima de precio (NQ 0.25). Echo es autoridad de la spec económica que usa; el venue es autoridad de lo que ejecuta. |
| `point_value` | **CONFIG-of-record** | Valor monetario de 1.0 punto de precio por contrato en `quote_currency` (NQ $20; evidencia C-E06: contract unit $20 × Nasdaq-100). |
| `tick_value` | **DERIVED** | `tick_size × point_value` (NQ $5). Se deriva para eliminar la clase de inconsistencia de dos números configurables que pueden discrepar; ProjectX `tickSize`/`tickValue` sirven de cross-check (mismatch ⇒ telemetría, §8). |
| `qty_min`, `qty_step` | CONFIG | Mínimo e incremento de quantity en contratos enteros (cohorte V1: 1/1; ProjectX `size` integer, evidencia D1). |
| `active` | CONFIG (operacional) | Elegible para nuevos mappings (análogo operativo de ProjectX `activeContract`, C-E07). Tombstone = delete. |

Repair A-R1: Contract ya no porta campo `exchange` propio — el exchange de listado se hereda de su Instrument vía `instrument_id` (§2.1), única autoridad, cero duplicación contradictoria. `calendar_ref`/`product_group` tampoco se duplican en Contract: todo atributo de grouping vive en Instrument.

**Lifecycle timestamps NO autoritativos en V1.** La evidencia lo dice explícitamente: ProjectX no expone `expirationAt`/`lastTradeAt` estructurados y Front E dejó la autoridad de esos timestamps como unknown no bloqueante (C-E07, unknown §22.1). V1 no inventa `first_trade_date`/`last_trade_date`; expiración se gestiona por rollover manual + rechazo del venue (§6). `DEFERRED_DEBT`: el backtester futuro necesitará resolución histórica por fecha — se abre cuando exista el requisito real, sin cambiar identidad.

## 3. Identidades y cardinalidades

```text
Instrument 1 ──▶ 0..N Contract          (expiry-specific; identity = contract_id)
Contract 1 ──▶ 0..N ExternalIdentifier  (identity = (source, context); §4)
Instrument 1 ──▶ 0..N Mapping           (identity = (mapping_context, binding_id, instrument_id); §5)
Operation ──▶ exactamente 1 contract_id (pinned al materializar; D2-01/D2-04)
Order/Fill/Position ──▶ contract_id heredado del pin de la Operation (D2-04 §2.2/§2.3/§2.4)
```

- Una Operation es mono-contract: todo su ciclo (adds incluidos) ocurre sobre su Contract pinneado. Prohibido un ADD sobre otro contrato dentro de la misma Operation: la exposición lógica (Σ fills firmados, D2-04 I4) sólo es coherente en unidades del contrato pinneado.
- Position física queda `(account_id, contract_id)` — exactamente el shape congelado en D2-04 R8; este TOP no cambia nada ahí.
- Strategy/Signal referencian sólo `instrument_id` (D2-03: agnósticas del `contract_id` físico).

## 4. External identifiers

Modelo KISS: una sola entidad de binding con namespace explícito, sin entidad distinta por vendor y sin subclasses de Contract.

```text
ContractIdentifier {
  contract_id          // FK
  source               // namespace del adapter/fuente config: "projectx", "databento", "ninjatrader", "cqg", ...
  context              // MARKET_DATA | EXECUTION
  external_id          // string literal del venue/vendor (ej. "CON.F.US.ENQ.H25", "NQ 12-26")
}
```

- **Identidad/cardinalidad:** única por `(contract_id, source, context)`; la dirección inversa `(source, context, external_id) → contract_id` debe ser única — la resolvibilidad así lo exige y se valida al escribir config (fail-closed en gateway, no en runtime).
- `source` es la clave de configuración de un adapter/fuente declarada (mismo namespace que usarán los adapters futures de D6); **no** es `Provider` (§10, seam C). Dos hubs/gateways del mismo family con IDs distintos = dos `source`.
- Los identifiers no participan del mapping Instrument→Contract (§5); se resuelven en un segundo paso, local al adapter/source que los consume. Un Contract sin identifier para el `(source, context)` requerido = fail-closed (§8).
- Provenance/layer preservada (C-E08, capas §11 de Front E): ningún `external_id` se promue a `contract_id`, y `symbolId` de ProjectX no se asume family ID (claim rechazado en Front E).
- **Dos resoluciones distintas, jamás fusionadas (repair A-R1):** (1) *current-Contract selection* — qué contrato listado está corriente para un binding (§5); (2) *vendor external-identifier selection* — qué string literal usa un source concreto para ese Contract. El mismo Contract resuelto por dos bindings distintos puede —y va a— tener identifiers distintos por source (ej. ProjectX `CON.F.US.ENQ.H25` vs NinjaTrader `NQ 12-26` para el mismo `NQH7`); no se duplica el Contract ni se colapsan las capas.

## 5. Mapping canónico → físico (hot)

```text
InstrumentMapping {
  instrument_id        // FK
  mapping_context      // MARKET_DATA | EXECUTION (propósito de resolución)
  binding_id           // identidad concreta del binding/contexto (owner-curated, estable)
  contract_id          // FK al Contract corriente para ese binding
  updated_at, version  // metadatos de config, no framework de versiones
}
```

- **Identidad/cardinalidad (repair A-R1):** una fila corriente por `(mapping_context, binding_id, instrument_id)`. `binding_id` es la identidad concreta del contexto de uso — p.ej. `databento-main`, `databento-backup` en `MARKET_DATA`; `projectx-topstep`, `nt-kronos` en `EXECUTION`. Su namespace vive dentro del `mapping_context` (nunca colisionan porque la resolución siempre lleva ambos). Varios bindings de feed y varios execution bindings coexisten para el mismo instrumento, cada uno con su Contract corriente propio y rolando en momentos distintos — el requisito owner "mapping separado para reference feed y execution venue cuando sea necesario" queda cubierto a nivel de binding, no de propósito genérico.
- **Ownership del binding:** el mapping posee sólo la fila `(context, binding_id, instrument) → contract`. La definición de qué es un binding (su adapter/fuente, credenciales, config de transporte) pertenece a su consumidor: los bindings `MARKET_DATA` a la config del runtime de mercado (autoridad feed, D2 market), los `EXECUTION` a la config de la Account/adapter (D2-04 + binding C). Una Account de ejecución referencia exactamente un `execution_binding_id` en su config. `binding_id` desconocido o fila ausente = fail-closed (§8); sin default cross-binding ni fallback al valor de otro binding.
- **Momento de resolución (congelado, D2-01/D2-03/D2-04):** `echo/operation` resuelve `instrument_id + execution_binding_id (de la Account) → contract_id` **exactamente una vez**, durante las guards de materialización (§3.1 D2-04), y lo pinnnea en la Operation; el snapshot embebido (D2-04 §2.1) lleva las specs del Contract (`tick_size`, `point_value`/`tick_value`, `qty_min/step`). El par `MARKET_DATA` lo resuelve el runtime de mercado (feed/StrategyEngine) con el binding de feed que esté resolviendo, al suscribir/etiquetar streams — mismo mecanismo, otro consumidor, otro momento.
- **Cadena completa por lado:** market runtime: `Instrument + market-data binding → current Contract`, y si el feed necesita símbolo vendor: `Contract + source → external identifier (MARKET_DATA)`. Materialización: `Instrument + Account execution binding → current Contract` (pin + specs), y después `Contract + source (del adapter) → external identifier (EXECUTION)`. Current-Contract selection y vendor identifier selection son **dos resoluciones distintas y secuenciales** (§4) — la segunda la ejecuta el consumidor que conoce su `source`, nunca el mapping.
- No hay resolución perezosa ni re-resolución: después de CREATED, ningún path del aggregate consulta el mapping (el pin y las specs viven en el estado del aggregate). El hot path no hace I/O remoto: resolución desde kache (§8), patrón D2-04 §8.6.
- Strategy permanece agnóstica: emite `instrument_id` en Signal; el `execution_binding_id` de la Account (config owner, territorio Account/transport — D2-04/D2-05C) determina qué fila de mapping aplica y qué `source` resuelve el external_id. Dos cuentas con bindings distintos pueden pinnear Contracts distintos para el mismo instrumento si la config owner así lo exige; Position queda neta por `(account_id, contract_id)` (D2-04 R8), por lo que no hay mezcla posible.

## 6. Rollover manual (semántica congelada)

Owner manual V1; hot update via config (§8); **nunca** retroactivo. Congelado exacto:

1. **Resolución en creación:** toda Operation nueva resuelve el mapping corriente **de su execution binding** al materializarse y pinnnea el resultado. Caso A: `NQ→NQZ6` vigente para el binding de la cuenta; Operation A creada (pin `NQZ6`); owner cambia `NQ→NQH7` para ese binding; Operation B nueva resuelve `NQH7`; A sigue `NQZ6` en todo su ciclo.
2. **OPEN/gestión sobre Operation viva tras rollover:** adds/reduces/exits de A van al contrato pinneado (`NQZ6`), aunque el mapping corriente sea `NQH7` (regla mono-contract §3). Cambiar el mapping jamás retargetea A (D2-01).
3. **REDUCE/CLOSE sobre contrato viejo (Caso H):** las Orders de cierre usan `NQZ6` + su external identifier corriente. Si el venue lo rechaza (ej. contrato expirado/inactivo) la Order queda `REJECTED` (D2-04 §3.2), fail-visible; MM decide (retry no repara expiración; escalación a safety plane/procedimiento operacional owner). **No silent remap, no auto-migración, no synthetic order sobre el contrato nuevo** — espejo del patrón LEAN documentado (C-E05: liquidate(old) + order(new) es acción explícita, no efecto del mapping).
4. **Mapping inexistente/eliminado con Operation viva:** la Operation existente no se ve afectada (nada la re-resuelve). Las materializaciones nuevas cuya fila `(context, binding, instrument)` falte fallan la guard con telemetría `CONTRACT_RESOLUTION_FAILED` — no se crea Operation (misma semántica de guard que `SIGNAL_EXPIRED` en D2-04 §3.1); una cuenta sobre otro binding con fila vigente sigue materializando normalmente. Fail-closed, sin fallback silencioso al contrato anterior ni al valor de otro binding.
5. **Rollover de exposición = procedimiento operacional owner:** cerrar A (MM/CLOSE o flatten del safety plane) y abrir sobre el contrato nuevo. Echo no automatiza ni sugiere; sin scheduler, sin trigger calendario (fuera de V1 por decisión owner).
6. **Raza en el borde del rollover:** una Signal materializada un instante antes/después de la propagación del hot update resuelve viejo o nuevo según lo que el kache del state owner tenga en ese momento — determinístico por construcción (el estado que resuelve es el mismo estado commiteado con la Operation) y suficiente; la telemetría de config-change da la trazabilidad.

## 7. Unidades (pips eliminado del camino nuevo)

- **Canon V1 para MM:** `price` (decimal, `quote_currency`); deltas de precio en **ticks** (`Δticks` integer) o precio absoluto; `tick_size` (Contract); `point_value`/`tick_value` derivado (Contract); `quantity` en **contratos** enteros con `qty_min`/`qty_step` (Contract).
- P&L/exposición monetaria por Operation = `Σ fills firmados` (contracts) × `Δpuntos` × `point_value`, en `quote_currency` — derivable de Fills + specs del snapshot; sin pips en ningún punto del dominio nuevo (constraint V1 del proyecto; D2-03 ya excluye pips de Strategy levels).
- **Qué es canonical y qué viene del venue:** las specs económicas que Echo usa (`tick_size`, `point_value`, qty rules) son config-of-record Echo inicializada de evidencia exchange/venue (CME/ProjectX); el venue es autoridad de lo que efectivamente ejecuta. InstrumentSnapshot (venue-observado) queda como observación runtime, **no** como fuente de specs — y su `TickValue` actual es "en la moneda de la cuenta" (source d319d0a3), dependiente de la cuenta, por lo que es materialmente inadecuado como spec de Contract.
- **Seam declarado (no diseñado aquí):** cuenta en moneda ≠ `quote_currency` (ej. cuenta EUR operando NQ) exige conversión FX para riesgo monetario en MM. No se inventa un FX engine para identidad/lifecycle; el seam queda registrado para el diseño de MoneyManagement (bloqueante de sizing fixed-risk, no de este modelo).
- `PipSizeCanonical` (`v3/sdk/mm/pip_size.go`, 3d4f34e1) y `StopLossOffsetPips` (ExecutionPolicy) permanecen confinados al path legacy Reference; el dominio nuevo jamás los invoca. La limpieza pips legacy conserva su deuda candidata pendiente de ratificación owner (ID/alcance), fuera de este TOP.

## 8. Persistencia / hot config

- **Source of truth:** PostgreSQL (tablas config owner-editadas vía Hasura/front, patrón `symbol_mappings` actual): instruments, contracts, contract_identifiers, instrument_mappings (nombres ilustrativos, no congelados). Validación de unicidad inversa de identifiers al escribir (§4).
- **Distribución hot:** handlers de Gateway (event triggers Hasura → Kafka) sobre topics compactados, patrón exacto de `SymbolMappingHandler` (a9364d4a): INSERT/UPDATE → value; DELETE o `active=false` → **tombstone** (value nil). Consumo por **kache** en Core (REUSE; se agregan caches instrument/contract/mapping junto a account_configs/strategy_configs) y por caches locales donde un consumidor lo necesite (adapters). Un topic de la familia config con record types por entidad, o topics hermanos — decisión física de implementación, no semántica nueva.
- **Startup readiness:** kache global init + readiness gate; cualquier resolución con cache no-listo es idéntica a resolución faltante ⇒ fail-closed (§6.4) + telemetría. Disposición D1 ya registrada: aceptable hoy, medir startup antes de escalar.
- **Deletes/tombstones:** borrar un Contract con mappings colgantes deja mappings resolvibles-a-nada ⇒ guard fail-closed (CONTRACT_RESOLUTION_FAILED), no borrado en cascada silencioso; el owner remueve mappings como paso del procedimiento. Operations vivas jamás se tocan (§6.4).
- **Fail-closed summary:** instrument desconocido / `binding_id` desconocido para el consumidor / fila de mapping ausente para el `(mapping_context, binding_id, instrument_id)` pedido / contract inexistente o inactivo / external identifier ausente para el `(source, context)` del adapter ⇒ sin materialización + telemetría; nunca fallback al valor anterior, a otro binding ni a otro identifier.
- **Cross-check de specs:** cuando el adapter exponga specs del venue (ej. ProjectX `tickSize`/`tickValue`), se comparan contra config al conectar y se emite métrica/warning en mismatch; Echo config sigue siendo la autoridad económica (mismatch fail-visible, no auto-corrección).

## 9. Disposición física Echo V3 (baseline 372af59a, sin delta)

| Pieza V3 | Disposición | Evidencia (repo/path, blob) |
|---|---|---|
| `InstrumentSnapshot` | REUSE (path legacy) / **no** es fuente de specs del nuevo dominio | `v3/sdk/domain/snapshots.go` d319d0a3 — mezcla quotes hot + specs broker y `TickValue` en moneda de cuenta; sin expiry/currency/session (gap D1). El nuevo Contract config-of-record lo reemplaza como autoridad económica. |
| `MMEngineFn` resolución implícita `broker:canonical` | ADAPT (ya dispuesto D2-04) → resolución explícita en `echo/operation` | `v3/core/internal/functions/mm_engine.go` e725ceb0 (línea ~285: `instKey = executionBroker + ":" + canonicalSymbol`) — hoy la "resolución física" es una convención de key; el modelo la hace explícita y pinneada. |
| `InstSnapshotFn` (KVS broker:symbol) | REUSE (legacy) | `v3/core/internal/functions/inst_snapshot.go` 89d59129. |
| `SymbolMappingHandler` (Hasura→Kafka compactado→tombstone) | **REUSE/EXTEND** (patrón para los nuevos handlers config) | `v3/gateway/internal/symbol_mapping_handler.go` a9364d4a — upsert/tombstone nil, key compuesta; el mapping futures agrega bindings/contexts y entidades, la mecánica no cambia. |
| `SymbolMappingMessage` + topic `echo.symbol-mappings.v1` | REUSE patrón; tabla/mapping `broker:symbol` queda legacy | `v3/sdk/domain/symbol_mapping_message.go` 7b699901. Unificación futura con Forex/CFD = `DT-EF-CROSS-MARKET-INSTRUMENT-02`. |
| Bridge `mapper.go` / `symbol_mapping_cache.go` (detransform edge) | REUSE legacy / no es el mecanismo futures | `v3/bridge/internal/mapper.go` 76a1b1de; `symbol_mapping_cache.go` 6dfb5203 — los adapters futures resuelven identifiers server-side; unificación = deuda cross-market. |
| kache (`account_configs`/`strategy_configs`) | **REUSE/EXTEND** | `v3/sdk/kache/account_configs.go` 2991979b (+ `strategy_configs.go`) — agregar caches instrument/contract/mapping con el mismo mecanismo de topics compactados. |
| `ExecutionPolicy` (offsets en pips) | ADAPT (dispuesto D2-04); unidades pips = legacy-only | `v3/sdk/domain/execution_policy.go` 295f7ea2. |
| `ClientConfig.AllowedSymbols` / `TradingWhitelist` | REUSE concepto — whitelist por **símbolo canónico** (instrument), agnóstica del contrato físico | `v3/sdk/domain/client_config.go` (+ handshake_client_config.go, transform vía mapper) — la asignación de feed/whitelist por cuenta sigue siendo canonical; el physical lo resuelve el mapping/adapters. |
| `PipSizeCanonical` | REUSE confinado a legacy | `v3/sdk/mm/pip_size.go` 3d4f34e1 — autoridad pips del path Reference; el dominio nuevo no la llama. |

Refactors bloqueantes nuevos: **ninguno** más allá del registro D1 §6 ("Instrument/Contract + hot mapping semantics", ya declarado blocking design item). Sin reescritura de Core (Q1 owner-accepted).

## 10. Seams obligatorios hacia D2-05B / D2-05C

**Hacia B (Session/Calendar):**
- **Seam congelado (repair A-R2):** las llaves canónicas que B recibe viven todas en Instrument — `calendar_ref` (nominal, apunta a la autoridad calendario de B), `exchange` y `product_group`. El CalendarResolver de B keyea por `(calendar_ref, exchange, product_group)` y aplica sus overrides específicos por grupo usando `product_group` como única llave de grouping (S-E05: schedules varían por product group; NQ y MNQ comparten grupo y calendario). **Prohibido** embutir sesiones, horas, breaks, holidays o trade-date en Instrument/Contract.
- `product_group` es owner-curated en Instrument y estable; B no define grupos propios ni duplica la llave en su modelo (una sola autoridad, cero contradicción Instrument↔Contract — Contract no porta ninguno de estos atributos).
- La autoridad de lifecycle timestamps (`expirationAt`/`lastTradeAt`) sigue UNKNOWN por diseño (C-E07/§22.1): B ni market-data deben inferirla desde el mapping; si aparece un requisito real (backtest histórico), se abre como deuda explícita con fuente elegida, sin mutar identidad.
- Trade-date/session semantics nunca entran al pin de Contract: el pin es identidad, no temporalidad.

**Hacia C (Provider/Program/Rules):**
- `source` de `ContractIdentifier` es namespace de **transporte/adapter**, no identidad de negocio de Provider; C no debe convertir Provider/ProviderProgram en namespace de identifiers físicos (el error de mezclar platform/API entitlement ya fue corregido en Front C/D).
- **Llaves de reglas congeladas (repair A-R2):** permitted-instruments/exchanges y caps se evalúan sobre `(instrument_id, exchange, product_group)` — las tres llaves viven en Instrument, única autoridad. `product_group` (ej. familia NQ = {NQ, MNQ}) es la llave de agregación de caps; cuando una regla necesite distinguir full-vs-micro, se expresa en la config del RuleSet (sets explícitos de instrumentos o cantidades scopeadas), no como nuevo eje de dominio (§2.1). C no crea agrupadores propios paralelos.
- El execution binding concreto (qué venue/hub usa una Account — su `execution_binding_id`, y por tanto qué fila de mapping y qué `source` resuelven sus identifiers) es territorio Account/transport (D2-04 adapter + binding C); el mapping canónico no lo embute y un `binding_id` nunca se deriva de la identidad de Provider.
- C debe respetar: hot updates de reglas/provider jamás mutan el pin de Contract ni el snapshot de Operation (D2-01), igual que MM state.

## 11. Casos de validación

**Caso A — rollover manual (NQZ6 → NQH7):** mapping `(EXECUTION, projectx-topstep, NQ)→NQZ6` vigente para el binding de la cuenta; OPEN aceptado → `echo/operation` resuelve `NQZ6` (context EXECUTION, binding de la Account), pinnnea + embebe specs (tick 0.25, point $20, qty 1/1) → Operation A CREATED. Owner actualiza la fila del binding a `NQ→NQH7` vía config → tombstone/upsert → Kafka compactado → kache. Nueva OPEN → Operation B con pin `NQH7`. A sigue `NQZ6`: sus adds, reduces y fills usan `NQZ6` y sus specs embebidas; la posición física de A vive en `(account, NQZ6)` y la de B en `(account, NQH7)` — Positions neta separadas por contract (D2-04 R8). Ningún retarget, ninguna migración.

**Caso B — feed y ejecución con identifiers distintos, Strategy agnóstica:** Strategy S1 opera `NQ` y emite Signal `{instrument_id: NQ, ...}`. El runtime de mercado resuelve su binding de feed `(MARKET_DATA, databento-main, NQ) → NQZ6` → identifier `(databento, MARKET_DATA)` → subscripción al feed X. En paralelo, la Account de Topstep resuelve su execution binding `(EXECUTION, projectx-topstep, NQ)` → identifier `(projectx, EXECUTION) = CON.F.US.ENQ.H25` (Y) para sus Orders. Signal no contiene X ni Y ni `contract_id` (D2-03); el pin de A/B es el mismo `contract_id` Echo (`NQZ6`) — X e Y son capas de identifier distintas sobre el mismo contrato listado. Si el owner rola el feed un día antes que la ejecución, las filas de mapping de cada binding divergen sin tocar a las Operations vivas.

**Caso H — Operation vieja con contrato viejo:** A (pin `NQZ6`) activa cuando el owner rola a `NQH7`. MM emite CLOSE sobre A → Order con `contract_id=NQZ6` + identifier `(projectx, EXECUTION)` de `NQZ6` → venue ejecuta (cierre normal) o rechaza (contrato ya no operable) → `REJECTED` fail-visible, sin remap: no existe path de código que sustituya el contrato de una Order viva o del pin de A. Si el mapping `NQ→…` se elimina por completo, A sigue cerrando sobre `NQZ6`; nuevas materializaciones cuya fila falte fallan `CONTRACT_RESOLUTION_FAILED` (sin Operation). La migración de exposición es siempre decisión owner explícita (cerrar A + abrir nueva).

### Casos de validación — repair A-R1

**Caso A-R1-1 — dos market-data bindings:** filas `(MARKET_DATA, databento-main, NQ) → NQH7` y `(MARKET_DATA, feed-b, NQ) → NQZ6` conviven. El runtime de feed A suscribe/etiqueta H7; el feed B sigue Z6. Strategy S1 emite `instrument_id=NQ` idéntico para ambas; ninguna Signal cambia y ninguna Operation se ve afectada (el pin es de ejecución). Cada feed aplica su propio hot rollover cuando el owner actualice su fila.

**Caso A-R1-2 — dos execution bindings:** Account 1 tiene `execution_binding_id=X`, Account 2 `execution_binding_id=Y`; filas `(EXECUTION, X, NQ) → NQH7` y `(EXECUTION, Y, NQ) → NQZ6`. El OPEN de S1 se materializa en la cuenta 1 con pin `NQH7` y en la cuenta 2 con pin `NQZ6` — mismas Signals, contracts físicos distintos si la config owner lo exige. No se asume que los venues rolan simultáneamente: cada binding rollea cuando su fila se actualiza. Las Positions quedan netas por `(account, contract)` y no interactúan.

**Caso A-R1-3 — mismo Contract, identifiers distintos:** ambos bindings resuelven `NQH7` como Echo Contract (una sola entidad Contract, sin duplicar). Identifiers: `(NQH7, projectx, EXECUTION) = CON.F.US.ENQ.H25` (Y1) y `(NQH7, ninjatrader, EXECUTION) = "NQ 12-26"` (Y2). La current-Contract selection fue una; la vendor identifier selection son dos, locales a cada adapter (§4). Cambiar Y1 no toca a Y2 ni al Contract.

**Caso A-R1-4 — calendar/provider seam:** `NQ` entrega a B/C sus atributos canónicos: `instrument_id=NQ`, `exchange=CME`, `product_group=NQ` (familia NQ/MNQ), `calendar_ref=CME-GLOBEX-EQINDEX`. Con eso B resuelve CalendarResolver (calendario + overrides por grupo) y C evalúa permitted-instruments (por instrument/exchange), caps por grupo (por `product_group`) y distinciones full-vs-micro vía config del RuleSet sobre el mismo conjunto de llaves — sin nuevos agrupadores ni duplicación en Contract.

## 12. Riesgos / unknowns

- **R-A — Divergencia entre bindings (post repair A-R1):** con mappings por binding, feeds y cuentas pueden quedar conscientemente en contratos distintos; en rollover, un binding actualizado y otro no produce la divergencia que la config declara. Es capacidad pedida por el owner y ahora representada nativamente, pero exige disciplina operacional: el runbook de rollover actualiza todas las filas de los bindings que deban moverse juntos, y la telemetría de mapping-change (por binding) hace visible cualquier divergencia residual.
- **R-G — Curación de `product_group`:** los valores son owner-curated; grupos ad-hoc o inconsistentes degradan las llaves de B (overrides por grupo) y C (caps por grupo) sin error runtime. Mitigación: convención de nombrado (default = instrument_id del flagship de la familia, ej. `NQ`, `ES`) y validación en el plano config (B/C rechazan en arranque un grupo sin instrumentos o duplicado semánticamente); sin segundo eje de grouping.
- **R-B — Conversión de moneda para MM:** riesgo monetario de cuentas no-USD sobre contracts USD exige una política FX en MoneyManagement; seam declarado (§7), no diseñado aquí. Bloqueante de sizing fixed-risk, no de identidad/mapping.
- **R-C — Ventana de propagación hot:** entre la edición del owner y la convergencia del kache, materializaciones nuevas resuelven el valor anterior; determinístico y acotado por la latencia del topic compactado (patrón ya operativo para symbol mappings). Sin acción.
- **R-D — Spec drift venue vs config:** si un venue reporta specs distintas (tick/value), Echo no autocorrige; la métrica de mismatch es la señal. Inconsistencia no detectada en boot dependería de la cobertura del cross-check por adapter (capacidad por transporte, D6).
- **R-E — Resolución histórica por fecha (backtest):** sin lifecycle timestamps, el futuro backtester no puede resolver "¿qué contrato era corriente el día D?" desde config sola. Deuda explícita (§2.2), se abre con el módulo de backtesting.
- **R-F — Identifiers duplicados en venue:** la unicidad inversa se valida en el plano config; un venue que recicle IDs entre contratos se detecta en validación, no en runtime.

## 13. Decisiones owner

```text
OWNER DECISIONS REQUIRED: NONE
```

Todo el diseño vive dentro de decisiones ya congeladas: D2-01 (pin + no retarget; sin framework de versiones), D2-03 (Strategy/Signal agnósticas del `contract_id`), D2-04 (materialización/guards, snapshot embebido, Position por `(account, contract)`) y los requisitos owner del proyecto (mapping hot manual, sin rollover automático, unidades sin pips). Ratificaciones técnicas ordinarias para el manager/submanager en integración: nombres físicos de tablas/topics de config, la forma del topic (uno con record types vs familia de topics) y la convención de nombrado de `binding_id`/`product_group` (§12 R-G) — ninguna cambia semántica.

## 14. Evidencia

- Vault: [[Echo Futures]] (requisitos owner §Símbolos canónicos; D2-01/02/03 OWNER_CLOSED; D2-04 CLOSED), [[Echo Futures — D1 Analysis Pack]] (Q1 matrix, Front E synthesis §5A, refactor register §6), [[CONTRACT + SESSION SEMANTICS — AUTHORITATIVE EVIDENCE]] (C-E01..C-E08, capas de identifiers §11, specs monetarias §10, unknowns §22).
- Repo físico (verificado vía working tree @ 372af59a; blobs `git rev-parse 372af59a:<path>`; fetch re-verificado `origin/master = 372af59a…`): paths y blobs en §9.
- Los drafts previos D2-05A/B/C y D2-05 integrado eran self-authored por el SUBMANAGER y fueron invalidados (bloque NON-AUTHORITATIVE en cada archivo); este artefacto se derivó exclusivamente de las autoridades congeladas + source físico y **reemplaza** el contenido invalidado de este archivo.
