---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[F — Decision Register]]"
  - "[[Echo — Producto Integrado]]"
aliases: []
tags:
  - kind/doc
  - area/echo
created: "2026-10-22"
updated: "2026-10-22"
---

# E — Rankings Shared Go Parity

## Propósito

Fijar el contrato implementable de los rankings D19/D20 sobre el runtime Echo autorizado: una sola implementación Go consumida por Forge y Echo, perfiles económicos explícitos, cohorte inmutable y publicación completa. Es diseño Shot 1, no implementación ni certificación. Autoridad producto: [[F — Decision Register]] D09/D10/D19/D20/D24. Curvas y métricas fuente: [[D — Curves Metrics Workers]]. Selección/revisión histórica: [[C — Histories Revisions Economy]].

## Contenido

### 1. Baseline observado y límites de paridad

Inspección local de 2026-10-22: `xKoRx/symphony@daded14cbe0bc85f6fafda8d079e94036f715b47` y `xKoRx/echo@2ee61791deb3139be23e1c9be3708b1d41da8d6b` (`feature/ef-runtime-pools`), ambos sin cambios de worktree. No se usaron ramas históricas como baseline. No se ejecutaron tests, builds, suites, infraestructura, migraciones ni publicación de módulos.

| Evidencia observada, repo + archivo:líneas | Consecuencia contractual |
|---|---|
| Symphony `sqx/core/domain/ranking_snapshot_per_type.go:14-20,155-177` | `weighted_combination_minmax.v1`, implementación `1.0.0`, pesos enteros positivos normalizados por su suma; configuración y parámetros tienen digest. |
| Symphony `sqx/core/domain/ranking_snapshot_per_type.go:296-319,322-371` | Extremos sólo sobre candidatos elegibles completos; min=max da **1**; BENEFIT `(x-min)/(max-min)`, COST `(max-x)/(max-min)`; contribución `normalized * float64(weight) / float64(total)`; score 0..1 DESC; igualdad exacta desempata `StrategyRef` ASC y rank ordinal 1..N. |
| Symphony `sqx/core/domain/ranking_snapshot_per_type.go:447-503` | Métricas ausentes, INVALID, null o no finitas excluyen al candidato entero; malformed/source/catalog contradictorios son conflicto fatal. `drawdown<=0` excluye si se selecciona ese coste. No redistribuye pesos por candidato. |
| Symphony `sqx/core/domain/ranking_snapshot_per_type.go:181-218,240-292,506-520,634-655` | Partición PER_LOGICAL_TYPE; identidad por evidencia/ref; validación exige componentes en orden de código y cohorte elegible completa. El builder itera `config.Metrics` en su orden original, aunque Validate ordena sólo una copia para params digest. El adaptador nuevo valida orden canónico antes del kernel; no asume que el código observado lo ordena. |
| Symphony `sqx/core/evaluation/catalog_core.go:3-17,21-34,41-48` | RetDD/PF/Sharpe/SQN son **SQX_NATIVE**; el catálogo describe ratios/Sharpe anualizado pero no prueba calendario, rf, sampleSD ni definición de SQN equivalente a LAB. No se puede afirmar paridad económica copiando sus números. |
| Symphony `sqx/core/evaluation/risk_adjusted_delta.go:23-34,46-110`; `comparison.go:175-226` | Comparador baseline→optimized de seis métricas, no ranking absoluto. Fórmula y guards se detallan abajo. |
| Symphony `sqx/go.mod:1-5,16-18` y `go.mod:141-143`; Echo `v3/sdk/go.mod:1-6`, `v3/lab-worker/go.mod:1-11` | Forge SQX Go 1.24 y dependencias SDK/root con replace locales; Echo SDK/worker Go 1.25.5. Importar SQX desde Echo arrastra autoridad y dependencias de producto; reutilizar esos replace no publica un módulo. |
| Echo `v3/sdk/lab/formulas/formulas.go:9-15,46-84`; `v3/sdk/lab/metrics/metrics.go:12-28,77-87,265-268` | Baseline contiene fallback R monetario→pips→journal y subscores mínimos; eso no implementa los rankings aquí definidos ni demuestra Q de ciclo D10. El contrato nuevo consume evidencia D, nunca ese fallback como sustituto de Q. |

**Paridad que se exige:** mismos raw values binary64, métricas/direcciones/pesos y orden, misma cohorte elegible → mismos componentes, score, orden y rank que el builder Forge válido en el SHA observado. `CreatedAt`, envelopes Forge y nuevas identidades LAB quedan fuera de igualdad porque pertenecen al adaptador. La diferencia económica es explícita: `sqx_native.v1` conserva evidencia nativa; `rank_economics.v1` usa fórmulas D abajo. Nunca mezclar ambas políticas en la misma cohorte ni declarar equivalencia por compartir nombres.

### 2. Una implementación y publicación concreta

**Destino nuevo de Shot 2:** repo `xKoRx/echo`, directorio `v3/sdk/analytics`, módulo independiente `github.com/xKoRx/echo/v3/sdk/analytics`, `go 1.24.0`. Paquetes públicos `ranking` (kernel y presets) y `metricinput` (DTOs/políticas/validación); sólo biblioteca estándar. Fingerprint/canonicalización quedan en los adaptadores y reutilizan `github.com/xKoRx/echo/v3/sdk/contracts/wire`, fuera del módulo puro; no se crea otro paquete de hash. Este submódulo no importa Echo SDK/contracts, Symphony, DB, ETCD, Temporal, OTel ni un `internal` de aplicación. No contiene historia, provisioning, órdenes ni dinero de cuenta. Los adaptadores de ambos productos manejan persistencia/telemetría fuera del kernel. Forge ya consume un submódulo de contratos Echo sin importar el runtime (`sqx/go.mod:16`); no crea una dependencia circular.

`ranking.MinMaxV1(config Config, candidates []Candidate) (Result, error)` es el único kernel de score, identificado por `weighted_combination_minmax.v1/1.0.0`. DTOs puros: `MetricSpec{Code string, Direction BENEFIT|COST, Weight uint32}`, `Candidate{StrategyRef string, MetricSnapshotRef string, Values []MetricInput}`, `MetricInput{Code string, Status enum, CalcDecimal string, Reason string}`; resultado `Candidates[]{eligible,reasons}`, `Extrema[]{code,min,max}`, `Entries[]{StrategyRef,metric_snapshot_ref,rank,score,components[]{code,normalized,weight,contribution}}`. `score`/componentes son binary64 finitos; el adaptador serializa con formato round-trip, nunca el número de display. Entradas inválidas devuelven error tipado; insuficiencia económica devuelve exclusión explicada.

La implementación Forge existente se refactoriza a llamada al kernel compartido, conservando el envelope `ranking-snapshot-per-logical-type.v1`, inspección de `SQX_NATIVE`, evidencia builder/import/retester, digests y TopN. Se elimina la fórmula duplicada de `ranking_snapshot_per_type.go`; su wrapper sigue siendo dueño del contrato Forge. Echo crea su adaptador en `v3/sdk/lab/ranking`, invocado por el worker derivado. Ningún adaptador vuelve a calcular min/max ni score. `risk_adjusted_delta.go` sigue como comparador independiente; no se convierte en otro kernel absoluto.

**Pin diseñado, todavía no publicado:** versión de prueba `v0.0.1-lab-v4-shot2.1`, tag de submódulo `v3/sdk/analytics/v0.0.1-lab-v4-shot2.1`, únicamente después de materializar y verificar el módulo en la rama autorizada. Consumidores `Echo v3/sdk/go.mod` y `Symphony sqx/go.mod` requieren exactamente `github.com/xKoRx/echo/v3/sdk/analytics v0.0.1-lab-v4-shot2.1` y el mismo `go.sum h1`; el manifest de build guarda commit completo al que resuelve el tag, zip checksum y Go toolchain. No se inventa aquí un SHA futuro ni se dice que el tag existe. Una corrección usa `.2`, nunca mueve el tag. No release productiva limpia desde feature.

Gate de distribución Shot 2: descarga del mismo tag desde caché vacía, `GOWORK=off`, sin `replace` de **analytics**, sin vendor divergente y sin rutas relativas para este import. Verificar dependencia efectiva con `go list -m -json` y checksum en ambos consumidores; demás replaces preexistentes del repo se registran por separado, sin atribuirles paridad del módulo. CI compila el módulo aislado con Go 1.24 y ambos consumidores con su toolchain. Si la versión no es accesible, `BLOCKED_EXTERNAL_MODULE_PUBLICATION`; nunca sustituirla por copia o por un local replace como evidencia de distribución. Publicar el tag y cambiar go.mod es trabajo futuro Shot 2, no efectuado por este documento.

### 3. Presets sellados y frontera numérica

| Ranking ID / nombre | Engine | Métricas en orden canónico del kernel y pesos enteros | Pesos efectivos |
|---|---|---|---|
| `edge_duo.v1` / Edge Dúo | `weighted_combination_minmax.v1/1.0.0` | `profit_factor:1`, `ret_dd:1`, ambas BENEFIT | PF=.5, RetDD=.5 |
| `forge_quality_four.v1` / Forge Calidad 4 | Igual | `profit_factor:4`, `ret_dd:5`, `sharpe_ratio:4`, `sqn_score:3`, todas BENEFIT | PF=.25, RetDD=.3125, Sharpe=.25, SQN=.1875 |

Pesos efectivos derivan de enteros 1:1 y 5:4:4:3; no se guardan decimales redondeados como autoridad. Catálogo de presets estático, rechazando ID/versión desconocidos. Cambiar fórmula, pesos, muestra, perfil, ventana o política económica crea nuevo preset/config digest; nunca reinterpreta un snapshot persistido. No hay plugins arbitrarios, scheduler, rebalance ni membresía I2. Registrar un preset recorre las historias elegibles usando el worker derivado existente, con control de generación abajo.

Evidencia fuente exacta y derivados `derived-fixed24-half-even.v1` según C/D; métricas conservan su expresión y `calc_decimal` HALF_EVEN a 24 posiciones; `display_decimal` a 12 posiciones es sólo presentación. El ranker convierte **una sola vez** `calc_decimal` a IEEE754 binary64 nearest-even mediante `strconv.ParseFloat(...,64)`, valida finitud, guarda string original y bits hex en `MetricInputSnapshot`. Cero negativo se canoniza a +0 antes del kernel. No usa display ni vuelve a derivar economía con floats. Presets sellan `numeric_policy=calc_he24_to_binary64.v1`; eso hace reproducible la frontera y permite golden parity contra Forge con los mismos bits. Ningún segundo motor decimal de scoring.

Se preservan el orden de operaciones `(normalized * weight) / total`, comparación exacta `min==max` e igualdad exacta de score para ties. No epsilon, bucket ni redondeo para desempatar. Las métricas deben estar en código ASC sin duplicados; `StrategyRef` UUID canónico no nulo (Echo strategy UUID enlazado al Forge canonical StrategyRef), un solo candidato por StrategyRef. Versiones paralelas de una estrategia se separan por `selection_revision`/cohorte; no inventar UUID por concatenación. Si falta correlación canonical, candidato `NOT_COMPARABLE/STRATEGY_REF_UNRESOLVED`.

### 4. Perfil económico y muestra acordados con D

`rank_economics.v1` fija por defecto `input_curve_profile_id=normalized_10k_open_balance.v1`, `initial_capital=10000`, `risk_fraction=.01`, config/risk-method digest sellado y sizing causal D09/D10. Cada moneda fuente sólo produce R cuando PnL y Q están en la misma moneda y el presupuesto total de ciclo está probado al abrir. El resultado 10k se expresa en `VIRTUAL_CAPITAL_UNIT`, sin atribuirle USD ni hacer FX. Otras monedas fuente pueden entrar tras ese ratio probado; `recorded_money.v1` exigiría una única moneda ISO y una nueva configuración de ranking. No mezclar perfiles/capital/risk_fraction/Q_method/cost policy en una cohorte.

Ventana explícita `[window_from,window_to)`, `as_of>=window_to`, `knowledge_cutoff`, `history_selection_revision` y warmup causal desde el origen del perfil. Default operativo de consulta: últimos 365 días UTC completos hasta `00:00:00Z` del día actual conocido; todo el rango va persistido, no se recalcula al leer. Ventanas personalizadas deben ser días UTC completos; ventana corta es válida pero puede quedar insuficiente. No usar fecha de import como construction date ni completar cobertura desconocida.

`utc_day_365.v1`: todos los días civiles UTC (incluye fin de semana), bins completos de 24h, anualización `A=365`, rf anual=0 y rf diario=0, sin estimar festivos/sesiones. Cada bin incluye estado COMPLETE/GAP/OUTSIDE_COVERAGE; COMPLETE sin movimiento da retorno 0, GAP da insuficiencia, OUTSIDE no se convierte en cero. Calendario y cobertura tienen digest. No anualización por número de trades, 252 implícito ni forward-fill de MTM.

Frecuencia de cálculo es por evento: cambio de selección/revisión de historia, input económico, cobertura, configuración o catálogo de preset marca cohorte DIRTY; el paso de medianoche crea una nueva ventana default. Debounce técnico máximo 60s, sin alterar el corte sellado. Esto es actualización de derivados, no selección/rotación de cartera. UI muestra generación, freshness y motivo, sin SLO físico demostrado.

| Métrica de `rank_economics.v1` | Fórmula, universo y unidad | Estado de borde |
|---|---|---|
| RetDD `ret_dd` | `net_change / max_drawdown_absolute_window_local`, ambos del perfil 10k en ventana FLOW_WINDOW; PnL realizado incluye parciales/abiertos y carry-in; DD arranca en valor inmediatamente previo a from, sin máximo anterior arrastrado; ratio sin unidad | DD=0 → UNDEFINED/ZERO_DRAWDOWN, incluso 0/0; DD nunca negativo; no infinito/cap arbitrario. |
| PF `profit_factor` | `sum(max(z_i,0))/abs(sum(min(z_i,0)))`; `z_i` es **resultado total del ciclo en el perfil** y no cada fill, parcial o R sin escalar | Sin pérdidas → UNDEFINED/NO_LOSSES (también si sólo ganancias); todos cero → UNDEFINED/NO_LOSSES con zero_count explícito; sólo pérdidas con denominador>0 → DEFINED 0. |
| SQN `sqn_score` | `sqrt(n) * mean(z) / sampleSD(z)`; sampleSD denominador n−1, sin cap de n, ratio sin unidad | n<2 → INSUFFICIENT_DATA; sigma=0 → UNDEFINED/ZERO_VARIANCE. No usar SQN sobre R si el perfil sellado es 10k. |
| Sharpe `sharpe_ratio` | Retorno simple realizado diario `y_d=q24((B_end_d−B_start_d)/B_start_d)`, `sqrt(365)*mean(y_d−0)/sampleSD(y_d)`; balance realizado con warmup; sin retornos log ni equity MTM | n_daily<2, gap o B_start<=0/CAPITAL_EXHAUSTED → INSUFFICIENT_DATA con motivo; sigma=0 → UNDEFINED/ZERO_VARIANCE. |

PF y SQN usan **WHOLE_CYCLE_TERMINAL_IN_WINDOW**: todos los ciclos terminales CLOSED cuyo `closed_at` está en `[from,to)`, incluyendo carry-in con su resultado completo, incluso movimientos anteriores a from. OPEN/PARTIALLY_CLOSED no son una observación terminal; sus realizaciones sí pueden contribuir al FLOW_WINDOW de RetDD/Sharpe. `CLOSED_SUMMARY` puede aportar un resultado terminal completo probado, sin inventar fills; falta de movimientos/fechas necesarios para la serie diaria deja Sharpe insuficiente. Manifest de métricas publica `n_closed`, `n_daily`, `n_carry_in_closed`, `n_open`, `n_partial`, `flow_movement_count` y motivos de faltantes. Es una diferencia de universos declarada, no una reconciliación falsa de sumas PF vs ventana.

Ambos presets fijan `sample_policy_id=ranking_sample_30x30.v1`: al menos **30 ciclos terminales evaluables y 30 bins diarios completos**, aunque Edge no consuma Sharpe. Fórmula definida con n≥2 no implica elegibilidad estadística de ranking. Sample no es confidence score ni garantía predictiva. La cohorte elegible de cada preset además exige todas sus métricas obligatorias DEFINED; Edge puede admitir sigma=0 en una métrica que no utiliza, pero no un GAP de cobertura. Historia sin observaciones se publica NO_OBSERVATIONS, sin score/rank; con muestra insuficiente, INSUFFICIENT_DATA; incompatibilidad económica, NOT_COMPARABLE; denominador inválido, UNDEFINED. Nunca cero imputado, exclusión de ciclos con Q desconocido para fingir completitud ni reducción del mínimo después del cálculo.

Costos: `z_i` y cada delta son netos de comisiones, swaps, fees y demás componentes conocidos, aplicados exactamente una vez según C/D. Costos cero requieren `KNOWN_ZERO`; desconocidos/mixtos → INSUFFICIENT_DATA/COSTS_UNKNOWN en todo el perfil afectado. No descontar de nuevo costos ya incluidos en `profit_net`; spread/slippage registrados por ejecución/precio no reciben estimación adicional. Cost model/basis y treatment digest integran comparability key.

### 5. Extremos, missing y determinismo

Sin winsorizar, clipping de percentiles ni eliminar outliers finitos válidos: contribuyen a los extremos y pueden comprimir a los demás. UI expone min/max y flags informativos. Antes del kernel se excluye candidato con required metric no DEFINED, no finita o fuera de rango numérico seguro `abs(x)>1e150`, motivo `SCORE_NUMERIC_RANGE`; ese guard de adaptación es **nuevo**, no se atribuye al baseline Forge. Protege resta/división binary64 y multiplicación por pesos pequeños de estos presets. En el wrapper legacy Forge se mantiene su política histórica; raw fixture paritario está dentro del dominio seguro. Overflow de pesos o salida no finita/inválida → falla de generación, sin publicar score parcial. Pesos de presets son los enteros exactos arriba.

Cada candidato excluido permanece en membership con estado/motivo y `score=null,rank=null`; nunca aporta min/max. Decodificación externa UTF-8 estricta con wire.Validate, sin unknown fields ni duplicate keys; números de score nunca aceptados como evidencia económica del productor. Config inválida, duplicado de identidad, métricas duplicadas, payload digest contradictorio o JSON malformado → `CONTRACT_CONFLICT` non-retryable de toda la generación. Missing económico válido → exclusión, no falla técnica. Cero elegibles produce snapshot completo `NO_ELIGIBLE_CANDIDATES` con entries vacías y motivos completos. Un único elegible o columna constante: normalized=1; si todas constantes, score=1 para todos; eso expresa igualdad dentro de esa cohorte, no calidad máxima universal.

### 6. Cohorte, identidad y publicación atómica

`RankingContext` sellado: `{namespace/tenant, evaluation_mode, input_curve_profile_id, input_curve_config_digest, metric_policy_id, numeric_policy_id, sample_policy_id, calendar_digest, cost_basis_digest, q_method_digest, window_from, window_to, knowledge_cutoff, as_of, partition_kind, partition_key, ranking_preset_id, engine_id, engine_version, module_commit}`. `partition_kind=GLOBAL_COMPATIBLE` para screener LAB y `PER_LOGICAL_TYPE` para wrapper Forge; clasificación entra mediante snapshot ref y nunca se infiere del folder. No comparar ranks entre particiones ni entre distintos contexts.

El contexto común fija semántica comparable, no exige el mismo run físico ni la misma revisión de selección/configuración entre estrategias distintas. Esas identidades particulares viajan en cada membership row y se validan contra su manifest de entrada. `evaluation_mode` fija la modalidad y política de comparación; no mezcla LIVE/BACKTEST/REPLAY silenciosamente.

Congelar membership completo antes de calcular. Cada fila ordenada por StrategyRef contiene `{strategy_ref,strategy_version_ref,run_id,config_revision,history_selection_revision,history_input_digest,curve_snapshot_ref,metric_snapshot_ref,eligibility,reasons}`; fuente de historia y revisiones son refs inmutables de C, nunca latest leídos durante el loop. `membership_digest=D("lab-ranking-membership.v1", rows)` incluye elegibles y excluidos; `eligible_digest=D("lab-ranking-eligible.v1", eligible_rows)` incluye sólo los elegibles y sus inputs; `context_digest=D("lab-ranking-context.v1", RankingContext)` incluye campos sellados; `ranking_snapshot_ref=H("lab-ranking-snapshot.v1", context_digest, membership_digest, eligible_digest)`. `D(tag,x)=wire.Digest(tag,x)` y `H=wire.HashTagged` de C, mediante el adaptador; se reutiliza `echo-wire-json.v1` observado en Echo `v3/sdk/contracts/wire/hash.go:10-37` y `canonicalize.go:1-14,26-34`. Claves por bytes UTF-8, arrays de sets previamente ordenados, timestamps UTC RFC3339Nano, calc strings canónicas, scores como strings round-trip y bits. No nueva serialización de hash ni una copia de wire. `created_at` se excluye de identidad y payload semántico; `payload_digest=D("lab-ranking-payload.v1", body)` sí incluye extrema/componentes/entries/motivos y excluye su propio digest/ref autocalculados. Este envelope LAB no promete igualdad de digests con Forge: Forge usa `HashIdentity(namespace + newline + joined parts)` (`persistence_identity.go:95-103`).

Estados: `DIRTY → BUILDING → VALIDATED → PUBLISHED`, o `BUILDING/VALIDATED → SUPERSEDED|FAILED`. Worker único lógico por context key; lease/retry físico no cambia identidad. En una transacción PostgreSQL de proyección escribe header inmutable, membership, extrema y todas las entries/components, valida conteos/digests/ranks y cambia CAS el pointer `published_snapshot_ref` sólo si la revisión fuente/generation token sigue vigente. Header/filas son autoridad del derivado, nunca autoridad de Operation/History. Si revisión fuente cambió, SUPERSEDED y rebuild completo; jamás parchea sólo la fila que disparó el evento. No mezcla miembros N con scores N+1.

Inserción write-once idempotente por snapshot_ref: mismo payload_digest → replay OK sin duplicar; digest distinto → CONTRACT_CONFLICT. Falla antes de commit no cambia pointer; fallo de respuesta después de commit se resuelve leyendo snapshot/pointer antes de retry. CAS vigente fallido expuesto por servicio → 412 PRECONDITION_FAILED y nueva lectura del vector antes de otra generación; nunca 409 de idempotencia. Error transitorio DB → retry con el mismo input congelado; lease vencida no autoriza otro payload para el mismo ref. Min/max pueden cambiar por alta/baja/exclusión/actualización de una sola estrategia: invalidar **todos** los scores de la partición afectada. Otra partición no se recalcula salvo que comparta la cohorte.

Read API/Hasura sólo expone generaciones publicadas con permisos de rol, joins por snapshot_ref y generation token. Respuesta screener incluye ranking_context, cohort counts, extrema, score y rank; paginación/sorting usa `score DESC NULLS LAST, StrategyRef ASC`, sin recalcular por página/TopN/filtros cosméticos. Un filtro que define universo exige nueva cohort/query context; un filtro de visualización no re-normaliza. TopN es proyección posterior sobre entries completas, no input del kernel. Cambiar curva visible no cambia ranking context; UI conserva `ranking_input_curve_profile_id` visible y distinto de `selected_display_curve_profile_id`.

### 7. `risk_adjusted_delta.v1`: comparador separado

Para cada métrica baseline b y optimized o, `signal=(o−b)/(|o|+|b|)`; si ambos cero signal=0; invertir signo para lower; clamp [−1,1]. Pesos RetDD=.25, PF=.20, Sharpe=.20, SQN=.15, DD(lower)=.15, net_profit=.05; score `50+50*Σ(weight*signal)`, rango 0..100 y 50 neutral. Código observado retorna not_comparable si falta cualquiera; el comentario sobre partial no produce score parcial real (`risk_adjusted_delta.go:62-98`).

Guards observados comparan strategy/stage/pnl_basis/sample/currency/período sólo si ambos strings no vacíos (`comparison.go:202-226`); no acreditan calendario, costs, rf, numeric finiteness ni ausencia de metadata desconocida. LAB no invoca ese comparator para llenar scores absolutos. Si se expone comparativa futura, `lab_pair_comparability.v1` exige metadata completa e idéntica de ambos lados, mismas definiciones y valores DEFINED/finite, preservando el resultado nativo por separado; rechazo adicional se versiona en policy y nunca se presenta como comportamiento observado del comparator Forge. No hay feature de comparativa nueva implementada en este shot.

### 8. Golden fixtures y oráculos independientes — diseño, NOT_RUN

Golden inputs se guardarán en el módulo compartido `testdata/ranking/*.json`, con `source_sha`, config canónica, métricas originales/calc24/bits, candidatos excluidos, context y expected output. A/B/C/D abajo son aliases sólo de lectura; fixture usa UUID canónicos ordenados `00000000-0000-4000-8000-000000000001` a `...0004`. Todos declaran sample/cobertura suficientes salvo el caso de borde explícito. Estos números son fixtures sintéticos de diseño, nunca datos productivos ni UI.

| Fixture / raw inputs (RetDD, PF, Sharpe, SQN) | Expected independiente |
|---|---|
| G01 A=(1,1,0,0), B=(2,3,1,1), C=(3,2,2,2) | Extrema RetDD=[1,3], PF=[1,3], Sharpe/SQN=[0,2]. Edge: B=.75 rank1, C=.75 rank2, A=0 rank3. Quality4: C=.875 rank1, B=.625 rank2, A=0 rank3. Componentes B: PF=.25, RetDD=.15625, Sharpe=.125, SQN=.09375; sum=.625. |
| G02 dos candidatos todos (2,2,2,2); y subcaso singleton | Cada columna normalized=1; Edge/Quality score=1, empate StrategyRef ASC, ranks 1 y 2; singleton rank1 score1. No usar .5. |
| G03 G01 + D=(101,101,100,100), sólo Edge | Recalcular TODOS: A=0, B=.015, C=.015, D=1; orden D,B,C,A. Publicar sólo D dejando .75 anteriores es FAIL. |
| G04 G01, C carece SQN, B PF UNDEFINED/NO_LOSSES | Quality sólo A elegible → score1 rank1; B y C score/rank null, razones. Edge C es elegible si PF/RetDD y cobertura/muestra OK; SQN ausente no cambia pesos de Edge. |
| G05 required PF null/NaN/Inf o n_closed=29/n_daily=29 | Null/undefined o muestra excluye; NaN/Inf no se serializa como número JSON, error/exclusión en adapter según status; jamás score0 favorable ni compensar pesos. Todos excluidos → entries=[] y NO_ELIGIBLE_CANDIDATES. |
| G06 genérica kernel BENEFIT x=1..3, COST DD=2..6, pesos1:1, A=(1,2), B=(3,6) | Cada score=.5, orden A,B por StrategyRef; comprueba signo COST separado de presets. |
| G07 economía 30 días completos, 30 ciclos secuenciales, deltas de perfil (+200,−100) repetidos15, C0=10000, cada delta en un día UTC | net_change=1500, DD local=100, RetDD=15, PF=2, n_closed=n_daily=30, SQN=sqrt(29)/3. Sharpe exacto: sqrt365·mean(y)/sampleSD(y), y_(2j)=q24(200/(10000+100j)), y_(2j+1)=q24(−100/(10200+100j)), j=0..14. Daily balances fuente y returns son fixture explícito; no inferir que se aplicó sizing causal desde estos deltas sintéticos. |
| G08 carry-in: ciclo abre antes de from, realiza +200 antes y −100 dentro; cierra dentro; otro OPEN realiza +30 dentro | Terminal PF/SQN recibe ciclo completo z=+100, FLOW_WINDOW recibe −70; open no agrega observación terminal. Manifest carry_in_closed=1/open=1. Con esa única observación ambas políticas ranking son insuficientes aunque su flujo exista. |
| G09 comparator baseline todas métricas=1, optimized todas higher=2 y DD=.5 | Signals higher=1/3; DD lower=1/3; score=200/3≈66.6666666666667. Identidad→50; falta una métrica→not_comparable/score null. No utilizar 66.66 como ranking absoluto. |
| G10 inputs permutados, replay, cambio fuente durante BUILDING | Permutar candidatos no cambia snapshot semántico; replay mismo input digest no duplica; source revision nueva bloquea CAS antigua; lector ve cohorte completa previa o nueva, nunca mezcla. |

Oráculos exigidos en Shot 2/3: (1) ejecutar builder Forge del **SHA fijado** desde arnés local aislado con fixtures nativas válidas y comparar raw scores/component bits/ranks contra módulo distribuido usando mismos binary64; no usa DB/SQX físico. (2) calculadora independiente Python stdlib `fractions.Fraction` para G01–G06 y SQN de G07; no importa/copia el kernel Go ni expected outputs de éste. Para valores racionales que son binarios exactos en G01/G02 comparar bits; para .015 reportar racional y round-trip binary64 esperado. (3) `decimal.Decimal` con precisión80 y sqrt independiente para G07/G09 y comprobación calc_HE24, con reporte de tolerancia de conversión binary64 <=1ULP; rankings G01–G06 siguen exigiendo outputs exactos del contrato. (4) integration test de publicación transaccional con falla inyectada después de mitad de entries y carrera de revisión; read side sólo acepta pointer PUBLISHED y mismos conteos/digests. (5) Go module cold-cache build/pin y prueba de import graph sin dependencias de producto.

La golden suite verifica Forge y shared **antes de eliminar la fórmula duplicada**, guardando outputs SHA-pinned como artefacto de verificación fuera del vault; luego deja fixtures/replay en la suite permanente compartida. No dejar dos implementaciones productivas como fallback. Gate crítico incluye denominadores/missing, tie, min=max, outlier que mueve el resto, costs/Q, coverage, distribución de módulo y atomicidad; coverage mínimo95% en el código nuevo, sin tests vacíos ni infra real. Estados actuales de todos los gates anteriores: **NOT_RUN**. No hay PASS de paridad, build, distribución ni aceptación física en Shot 1.

## Fuentes

- [[F — Decision Register]] — D19/D20 y D24, autoridad producto y baseline.
- [[Echo — Producto Integrado]] — ownership integrado y evolución analítica.
- [[D — Curves Metrics Workers]] — matemática/economía y perfil fuente acordados; E gobierna normalización/score y publicación de ranking.
- [[C — Histories Revisions Economy]] — inputs históricos y selección temporal inmutable.
- [[THE_LAB_V4_Diseno_para_revision]], [[1 — TECHNICAL_FREEZE_PACKET]], [[SHOT4_HANDOFF]] — requisitos compatibles e historia, nunca segundo baseline de código.
- `xKoRx/symphony@daded14cbe0bc85f6fafda8d079e94036f715b47` y `xKoRx/echo@2ee61791deb3139be23e1c9be3708b1d41da8d6b` — archivos/líneas enumerados en §1 y §7.
