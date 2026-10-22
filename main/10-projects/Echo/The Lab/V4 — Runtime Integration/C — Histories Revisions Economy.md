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
created: "2026-10-22"
updated: "2026-10-22"
---

# C — Histories Revisions Economy

## Propósito

Contrato de implementación Shot 2 para historias múltiples, revisiones reproducibles, selección continua, economía por ciclo y composición estática D11 sobre el runtime vigente. Autoridad de producto: [[F — Decision Register]] D09/D10/D11/D16–D24. La historia económica es evidencia; curvas, métricas, scores y vistas son derivados. Este documento define contratos nuevos, no declara que estén implementados ni certificados.

## Contenido

### 1. Evidencia vigente y límites

**Baseline único inspeccionado:** `xKoRx/echo`, `feature/ef-runtime-pools@2ee61791deb3139be23e1c9be3708b1d41da8d6b`, HEAD y worktree limpio comprobados localmente el 2026-10-22. Todas las referencias `Echo:path:línea` de esta sección corresponden a ese SHA. Las notas [[1 — TECHNICAL_FREEZE_PACKET]], [[THE_LAB_V4_Diseno_para_revision]] y [[SHOT4_HANDOFF]] aportan requisitos compatibles; sus implementaciones y PASS históricos no certifican esta rama. D24 excluye la integración de adapters del backtester legacy.

| Evidencia observada | Implicación para Shot 2 |
|---|---|
| `Echo:v3/sdk/contracts/strategy_history.go:1`, `:105`, `:145`: V1 presupone un trade cerrado/fila, datasets training/pre-real, sin cuenta/run/grano | Añadir DTO V2; no reinterpretar ni cambiar silenciosamente V1 |
| `Echo:v3/sdk/postgres/strategy_history_service.go:108`, `:132` y `strategy_history_repository.go:133`, `:208`: lock por versión, DELETE de importadas y head reemplazable | V2 necesita identidad por historia, cadena inmutable y CAS; no llamar `ReplaceHistory` V1 desde V2 |
| `Echo:v3/sdk/futures/domain/operation.go:149`: Operation contiene ciclo, cuenta, estrategia, contrato, MM snapshot, órdenes y provenance; no version_ref universal ni Q_i | Correlación sellada de A y certificado QI nuevos; no buscar configuración contemporánea |
| `Echo:v3/sdk/futures/operation/wire.go:71`, `:98`: facts transaccionales con owner seq, run y fill nativo; `domain/operation.go:229`: identidad fill cuenta + provider_execution_id | Consumir hechos del owner con su identidad exacta; PostgreSQL latest projection no reconstruye por sí sola el stream |
| `Echo:v3/sdk/futures/operation/engine.go:1251`, `:1275`, `:1864`: materialización antes de evaluar/aplicar decisión MM | QI_SEALED debe provenir de la decisión que establece presupuesto, antes de exposición; no de un snapshot de config |
| `Echo:v3/sdk/futures/accounting/ledger.go:111`, `:138`, `:334`, `:416`: Revision es de cuenta; lotes FIFO por contrato; costes por fill; replay mismo fill es no-op y payload distinto conflicto | Atribuir economía lógica por Operation reutilizando aritmética exacta; no asignarle el FIFO físico de cuenta |
| `Echo:v3/sdk/domain/trade_journal.go:137`, `:170`, `:298`, `:381`, `:406`: journal usa trade_id/account, risk_money de InitialRisk y tiene default/hardcode USD | Una fila no acredita automáticamente moneda observada ni presupuesto de ciclo. Journal closed net sólo con evidencia de origen; default USD conserva `CURRENCY_UNPROVEN` |
| `Echo:v3/core/internal/functions/trade_journal.go:24`, `:154`, `:254`: writer canónico journal recibe ReferenceEvent/cierre; no escribe desde LAB | Integración journal→History es lectura/proyección con outbox del servicio dueño; LAB no reescribe hechos fuente |
| `Echo:v3/sdk/contracts/wire/canonicalize.go:1`, `:24`, `hash.go:10`, `validate.go:151`: echo-wire-json.v1 y HashTagged disponibles | Usar esa implementación compartida y recetas siguientes; no JCS/RFC8785, hash por saltos de línea ni float para dinero |

### 2. Tipos comunes y autoridad de escritura

`Ref = "sha256:" + 64 hex minúscula`. `ID` es UTF-8 no vacío de ≤256 bytes, sin trim, normalización Unicode ni cambio de case; los IDs Echo que ya tengan contrato más estricto conservan ese contrato. `Dec` es string decimal canónico de `wire.CheckDecimalString`, exacto en numeric(38,18): sin exponente, ceros iniciales, trailing zeros o `-0`. `Seq` es int64 positivo (JSON entero seguro ≤2^53−1; valores mayores se rechazan). Ninguna medida es JSON number. La aritmética usa racional exacto; límites de persistencia se validan antes de commit y nunca redondean evidencia.

`TimeEvidence = {value: UTC RFC3339Nano | null, state: PROVEN|DECLARED|UNKNOWN|NOT_APPLICABLE, evidence_ref: ID|null, raw: string|null, timezone: IANA|null, precision: INSTANT|CIVIL_DAY|UNKNOWN, reason_code: string|null}`. PROVEN exige ref resoluble al artefacto/evento y valor; UNKNOWN exige value=null y motivo. Normalizar instantes a UTC `Z`, omitir fracción cero y ceros fraccionarios finales. Día civil necesita timezone y conversión explícita al instante; un cutoff de último día incluido se convierte a primer instante del día siguiente y se guarda como exclusivo. No inventar medianoche/UTC para fecha ambigua. Los campos que afecten orden/cohorte/perfil requieren instante PROVEN; DECLARED se conserva, sin afirmar causalidad demostrada.

`Money = {amount: Dec, currency: [A-Z]{3}, currency_status: OBSERVED|DECLARED|UNPROVEN, evidence_ref: ID}`. Sólo OBSERVED o declaración explícita verificable del productor habilita agregación en esa moneda; un default técnico no es declaración económica. `Provenance = {source_system, source_instance_ref, source_artifact_ref, artifact_sha256, source_schema_version, producer_algorithm_version, source_event_refs[], source_cut: {stream_ref, through_seq?, snapshot_ref?}}`. Artifact refs no llevan secretos ni rutas locales. Source cut y artefacto identifican el contenido disponible, no timestamp del polling.

| Fuente | Único writer de hechos | Writer de History/proyección |
|---|---|---|
| Forge | Su productor conserva artefactos y traduce al DTO universal | Servicio Echo autenticado, writer externo fijado a la historia; sin SQL directo de Forge |
| Runtime | Operation owner acepta fills/órdenes; accounting es autoridad económica de cuenta. Extractor puro en accounting, invocado por owner, produce atribución lógica; no otro motor | Adapter interno autorizado por servicio, consume `echo.execution.operation-facts.v2` de A |
| Master REFERENCE/journal | Ruta ReferenceEvent/cierre→TradeJournalFn→repositorio canónico | Adapter interno de journal lee evento/row snapshot después de commit; outbox/cursor durable del writer evita huecos |
| LAB | Ninguno operacional | Valida, conserva snapshots, calcula derivados y selecciones; no emite órdenes ni corrige fills/journal |

`domain.Signal` técnico, `ReferenceEvent`, `OperationID` y `trade_id` son identidades distintas. El binding sellado de A proporciona `version_ref`, `canonical_strategy_id`, versión de mapping, `account_strategy_id`, `source_operation_ref` y, cuando existe, `{reference_event_id, trade_id, opening_signal_id, operation_id, order_id, fill_identity, copy_intent_id}`. Guardar sólo enlaces demostrados; magia/símbolo/precio/hora no prueban correlación. El MASTER observado entra por ReferenceEvent→journal como historia REFERENCE; `runtime_operation_id` es nullable y sólo se llena si existe una Operation nativa acreditada. OBSERVE_MASTER no crea una Operation ficticia ni un Signal técnico para hacer analítica. El crosswalk fija `{version_ref,binding_ref,reference_cycle_id,trade_id,account_id,role}` y enlaza `runtime_operation_id` sólo con prueba explícita. Un trade master y su copia son ciclos económicos distintos; se comparan, jamás se deduplican entre sí.

### 3. HistoryInputV2 y modelo persistido

Nombre de contrato `strategy-history.v2`, contenido embebible en `strategy-ingestion.v2` de B. Cada StrategyVersion admite 0..N historias; su identidad no depende de la historia, perfil, corrida analítica, curva ni score. Namespace viene del contexto autenticado; `producer_writer` del principal autorizado, nunca de un campo libre del body. Un writer externo no puede declararse interno Echo.

| Campo HistoryInputV2 | Tipo / validación |
|---|---|
| `history_id` | ID estable elegido al crear; no se reutiliza para otro scope |
| `source_kind`, `source_instance_ref` | Enum `FORGE_SQX|FORGE_MT5|ECHO_JOURNAL|ECHO_RUNTIME|OTHER_DECLARED` e ID; preserva origen, nunca lo infiere de etapa temporal |
| `account_ref`, `account_absence_reason` | ID nullable; cuenta necesaria para LIVE Echo, ausencia explicada para datos sin cuenta. Broker no sustituye cuenta |
| `run_mode`, `run_ref`, `run_absence_reason` | `LIVE|BACKTEST|REPLAY`; run obligatorio para BACKTEST/REPLAY y cuando fuente LIVE lo identifique. LIVE sin run usa stream/instance estable, nunca ID de polling |
| `role` | `REFERENCE|EXECUTION|NATIVE`; separado de run_mode. Reference no implica live ni ejecución real |
| `mm_context_digest`, `mm_evidence_ref` | Ref nullable; ausencia explícita. Config sellada observada, nunca reejecuta otra gestión sobre la misma evidencia |
| `expected_revision`, `expected_digest` | CAS, 0/null al crear; N/digest exacto al actualizar |
| `temporal_metadata` | Cuatro TimeEvidence de §7; evidencia de versión coherente para todas las historias de ésta. Cambio corregido versiona metadata y selección, sin cambiar definición de StrategyVersion |
| `coverage` | Lista de intervalos `[from,to)` con `state COMPLETE|PARTIAL|GAP`, calendar_ref, timezone, economic_time_precision, observed_through, known_at y evidencia; contador de operaciones esperado. Sin actividad dentro de COMPLETE vale cero; GAP vale ausencia |
| `provenance`, `operations`, `retractions` | Provenance anterior; set completo de OperationInputV2; lista de cambios explícitos §5. No PUT delta |

`HistoryKey = (registry_namespace, strategy_version_ref, producer_writer, history_id)`. Guardar `history_ref = H("echo-history.v2", ns, version_ref, writer, history_id)`. `source_kind/source_instance/account/run_mode/run_ref/role/mm_context_digest` son scope sellado; cambiar cualquiera crea historia distinta (nullable MM es un valor real, no wildcard). Símbolos y contratos viven por operación; no partir historia multiinstrumento para cumplir caps. Una historia de otra cuenta/run no pisa ni agrega a la anterior. La corrección de timestamps/economía conserva scope y crea revisión.

Tablas aditivas propuestas (naming final del plan de migración en coordinación A/B): `echo.strategy_histories` con PK HistoryKey/head_revision/head_digest; `echo.strategy_history_revisions` con PK `(history_ref,revision_no)`; `echo.history_operations` con PK `(history_ref,revision_no,operation_ref)`; `echo.history_movements` con PK `(history_ref,revision_no,movement_ref)`; `echo.history_change_entries` para corrections/retractions; `echo.history_selections` + `echo.history_selection_revisions`; receipts/outbox de B. FK siempre incluye namespace o history_ref ya scoped. No segunda tabla Strategy/StrategyVersion ni cadena independiente por movimiento.

### 4. OperationInputV2, movimientos y conciliación

| Campo OperationInputV2 | Semántica exigida |
|---|---|
| `source_operation_id`, `operation_ref` | ID fuente estable; ref recalculado `H("echo-history-operation-id.v2", history_ref, source_operation_id)`. Operaciones con mismo ID de otra cuenta/run están en otra historia |
| `cycle_started_at`, `opened_at`, `closed_at` | Materialización opcional, primera exposición económica probada y terminalidad efectiva; cerrado requiere closed_at≥opened_at. `opened_at` de runtime = primer fill que adquiere exposición; materialización sin fill no inventa apertura. Master/import conserva apertura fuente probada |
| `status` | `OPEN|CLOSED|CANCELLED|CLOSED_INCOMPLETE_ECONOMICS|RECONCILIATION_REQUIRED`. Terminalidad operacional no demuestra economía completa ni drenaje físico |
| `instrument_id`, `contract_ref`, `side`, `orders_refs[]`, `fills_refs[]` | Identidad canónica y snapshot de contrato cuando fuente posee; LONG/SHORT. Ausencia se declara; jamás fabricar fill/SL/TP para CLOSED_SUMMARY |
| `granularity` | Exclusivo `CLOSED_SUMMARY|ECONOMIC_MOVEMENTS` |
| `qi` | Certificado §6 nullable; guardar también riesgos no acreditados con su tag, sin tratarlos como denominador |
| `closed_summary` | Sólo CLOSED_SUMMARY terminal: net Money obligatorio, gross/cost breakdown opcional y cost disclosure obligatorio; sin movimientos contables. Aporta net una sola vez en closed_at |
| `movements[]`, `reconciliation_summary` | ECONOMIC_MOVEMENTS: movimientos conocidos incluidos en ciclos OPEN; resumen opcional separado, jamás término adicional de suma |
| `exposure` | `{state: FLAT|OPEN|UNKNOWN, quantity?, measured_at?, evidence_ref?}`. Qty exacta/unidad cuando existe; falta de marcas → unrealized UNKNOWN, nunca cero |
| `provenance`, `correlation`, `missing_fields[]` | Evidencia/crosswalk de §2, anomalías y razones por campo |

`EconomicMovement = {source_movement_id, movement_ref, operation_ref, kind: REALIZED_PNL|COMMISSION|FEE|SWAP, amount_signed: Money, economic_at: TimeEvidence, known_at: TimeEvidence, source_event_ref, source_event_digest, causal_order?:{stream_ref,seq}, order_ref?, fill_identity?, accounting_revision_ref?, contract_snapshot_ref?, cost_model_ref?, inclusion_basis: GROSS_DELTA|SIGNED_COST}`. `movement_ref = H("echo-history-movement-id.v2", history_ref, source_operation_id, source_movement_id)`. Debe haber source_event_ref exacto y resoluble; el dinero REALIZED_PNL es bruto, y cada coste es contribución firmada. Un reembolso puede ser positivo. Un total neto que ya incluye comisiones no se combina con esos costes como movimientos. Si sólo existe neto, usar CLOSED_SUMMARY.

Runtime conserva exactamente `fill_identity = execution_account_id + ":" + provider_execution_id` del contrato actual. Su identidad durable exterior incluye source_instance/run que evitan colisiones de runs aislados; no reemplazar la clave nativa por hash de precio/hora ni añadir un ticket supuesto. `source_event_ref` runtime identifica `{source_instance, run_ref, owner_key, operation_event_seq, fact_kind, fact_digest}`; el movement fuente de un cierre parcial identifica la realización y sus lotes emparejados, no cada replay del snapshot. Seq del owner continúa entre ciclos y es watermark, no identidad de Operation. Mismo event key+digest => no-op; misma clave+payload distinto => `SOURCE_EVENT_CONFLICT` en cuarentena, sin economía nueva.

El extractor de atribución acordado con A vive junto a accounting y usa sus unidades, tick_size/tick_value/multiplicador exactos. Mantiene lotes por `operation_id+contract` y empareja sus propios fills en FIFO dentro del ciclo, con refs a fills de entrada/salida. Invocado después de aceptación física y con la misma transacción/durable fact; un fact sin Order→Operation probado se conserva como unmatched/reconciliation, no se atribuye por conveniencia. Costes vienen de evento de coste real o modelo configurado explícito versionado que también usa la cuenta; no estimación oculta de LAB. El coste positivo `feePerContract×qty` del ledger se emite una vez como contribución negativa FEE. Spread/slippage dentro del precio de fill no se descuentan otra vez.

Conciliación registra para el MISMO set de fills `{account_revision_before, account_revision_after, assigned_operation_gross, account_gross_delta, costs_assigned, account_cost_delta, attribution_method, timing_difference, status}`. Ejemplo obligatorio: A compra 1@100, B compra 1@110, B vende 1@115, valor/punto=1: atribución B=+5, FIFO físico cuenta=+15; diferencia −10 atribuida al inventario todavía abierto, no ajustada artificialmente. Al cerrar A@120: A=+20 y cuenta añade +10; totales finales lógicos/físicos=25. No sustituir una autoridad por otra.

En terminal con movimientos completos, por moneda `net = Σ REALIZED_PNL + Σ COMMISSION + Σ FEE + Σ SWAP` y gross=Σ REALIZED_PNL; conciliar exacto en transacción. Mismatch => 422 `ECONOMICS_MISMATCH`; si fuente sólo tiene economía incompleta, aceptar evidencia con status incompleto y sin resumen neto certificado. Un OPEN puede tener +40 parcial y −2 coste: curva realizada +38; sus terminal metrics no cuentan aún un trade ganador. Un CLOSED_SUMMARY de +38 no admite además esos +40/−2 como otro grano.

Journal: no hay `event_revision` universal en el DTO actual. El writer añade outbox transaccional que captura `{trade_id, account_id, event_kind OPEN|CLOSE|CORRECTION, journal_change_seq, row_snapshot_digest, version_binding_ref}`; la seq la asigna ese writer y el snapshot va íntegro. Para un backfill read-only de filas existentes, evento identifica `(trade_id,account_id,row_snapshot_digest)`, cursor/snapshot de lectura consistente y `known_at=first_observed_at`; no inventar seq histórica ni usar updated_at de baja precisión como identidad. Modificación legítima del row => nueva revisión/cambio; no muta snapshots previos. Sin neto/currency observados, preservar la fila y faltantes sin derivar neto completo a partir de valores por default.

### 5. Revisiones, hash canónico, correcciones, CAS y publicación

**Inmutabilidad estricta:** una revisión aceptada es un snapshot COMPLETO y sellado de header, cobertura, operaciones, movimientos y cambios. No se append-ean movimientos ni se actualiza una fila económica dentro de N después del commit. Un nuevo parcial/coste/terminalidad produce N+1 con set acumulado completo; el adapter puede coalescer hechos aún no aceptados, conservando watermark, sin perder eventos. Esta precisión sustituye la frase ambigua del freeze antiguo “append dentro de revisión activa”; lo compatible es reconocer movimientos oportunamente mediante nuevas revisiones. `ACTIVE/SUPERSEDED` se deriva del head (o metadata de lifecycle separada), no altera el contenido hasheado.

Recetas exactas, reutilizando `wire.Validate`, `CheckDecimalString`, `Canonicalize`, `HashTagged` del SHA inspeccionado:

1. Validar JSON UTF-8 sin BOM, claves duplicadas, null tipado inválido, numbers inseguros y límites. Campos desconocidos se retienen losslessly en artifact y hash, pero no aportan semántica económica. Verificar refs que se declaran y recalcular todas las refs/digests en Echo.
2. Normalizar sólo instantes PROVEN con regla UTC de §2. Dec debe llegar canónico: `1.0` y `-0` se rechazan, no “corrigen”. Campos opcionales ausentes y null permitidos se representan como null en la estructura económica de digest; UNKNOWN se representa explícitamente con state/reason. Los enums/IDs se comparan byte a byte.
3. Ordenar sets antes de C: operations por operation_ref UTF-8; movimientos por movement_ref; coverage por `(from,to,state,source evidence)` y rechazar intervalos contradictorios; evidence refs lexicográficos sin duplicados; retractions/corrections por `(entity_ref,change_kind)`. Arrays que representan secuencia causal conservan su orden fuente, nunca se ordenan como set.
4. `C(x)` es JSON compacto con claves de objeto por bytes UTF-8, strings mínimo escapado, arrays ya ordenados, sin NFC ni reglas RFC8785. `D(tag,x)=H(tag,string(C(x)))`; `H(tag,fields...)` es SHA256 de bytes UTF-8 del array JSON compacto `[tag, ...strings]`, prefijo sha256. La serialización la ejecuta el paquete wire, no una copia.
5. `movement_digest=D("echo-history-movement.v2", movement_body_sin_refs_autocalculadas)`; `operation_digest=D("echo-history-operation.v2", operation_header + movement_digests_ordenados)`; `content_digest=D("echo-history-content.v2", scope + temporal_metadata + coverage + provenance_fuente + operation_digests + change_entries)`. Incluir valores económicos y conocimiento, no IDs de receipt/job, wall-clock del polling, expected_revision, received_at ni publication timestamps. El source watermark cambia sólo cuando cambia la evidencia fuente; no usar contador de corrida del loader.
6. `revision_digest=H("echo-history-revision.v2", history_ref, decimal(revision_no), previous_revision_digest_o_"", content_digest)`. `revision_no=1` al crear, N+1 monotónico bajo lock. Artifact almacena bytes canónicos EXACTOS del contenido, con `artifact_sha256` SHA256 bytes descomprimidos, size y encoding; distinto de revision_digest tagged. Conservar ambos y verificar ambos al reconstruir.

Cambios posteriores son `change_entries = {entity_ref, kind CORRECTION|RETRACTION|REPRESENTATION_UPGRADE, previous_record_digest, new_record_digest|null, reason_code, source_evidence_ref, effective_at, known_at}` en N+1. Desaparición de operación/movement que estaba en N requiere RETRACTION explícita con evidencia de la autoridad original; si no, 422 `SILENT_REMOVAL`. Corrección cambia representación del MISMO hecho en el set completo; no añadir un negativo histórico junto a la versión corregida para neutralizarla. Un reverso/abono que realmente ocurrió en otro instante es un movimiento fuente nuevo. El upgrade CLOSED_SUMMARY→movements usa mismo operation_ref y change entry: N+1 incluye sólo grano movements, resumen como reconciliación, no aporte adicional. Los IDs permanecen estables y sus valores originales son recuperables en N. Post-terminal fill real conserva identidad original y activa RECONCILIATION_REQUIRED, N+1 y drain-refutation de A; no se atribuye al ciclo sucesor ni se elimina la anomalía.

Transacción del servicio:

1. Resolver receipt `(ns,writer,idempotency_key)` ANTES de CAS: mismo request_digest devuelve receipt original incluso si avanzó el head; payload distinto 409 `IDEMPOTENCY_CONFLICT`. En incertidumbre de red, GET receipt antes de reenviar.
2. Validar scope/autoridad y escribir artifact digest-addressed append-only antes de commit; store sin delete concurrente. Si falla, 503 sin receipt/head. Un artifact huérfano tras rollback es admisible; no una revisión que apunta a artifact faltante.
3. Lock por HistoryKey (advisory para creación + row lock para existente), revalidar receipt y CAS `(expected_revision,expected_digest)`. Create POST de B sólo expected=0: existente idéntico converge sin N nueva; diferente 409 `HISTORY_EXISTS`. PUT exige head exacto: stale CAS 409 `REVISION_CONFLICT` con head actual; productor relee, combina snapshot completo y usa key nueva. Un replay con receipt no depende del CAS actual. PUT con CAS correcto y content_digest igual devuelve UNCHANGED sin revisión nueva.
4. Insertar N+1/rows/change entries/receipt/outbox dirty y mover head atómicamente. Todos los history locks de un POST multihistoria se adquieren por history_ref ordenado; una invalidez revierte toda su aceptación analítica. Ninguna segunda historia queda a medias. Provisioning/readiness de B continúa independiente.
5. Worker lee manifest exacto de revisiones/selección/spec/config. Publica generación completa con puntos, operaciones consultables por revisión, métricas, coverage y estado en una transacción + CAS del vector de inputs y lease/fencing token. Si cambió head/selección/spec, el candidato se conserva como OBSOLETE o se descarta, sin mover el puntero current; reencolar head. Worker viejo no pisa N+1. Ranking/cohorte publica su vector atómicamente según D.

Un snapshot derivado fija `{history_ref,revision_no,revision_digest}` de CADA historia + selection_revision/digest + `profile_id/algorithm_version/config_digest` + ventana + knowledge mode. Nada lee “latest” durante cálculo/detalle paginado. API/UI separa `head_revision`, `displayed_revision`, `generation_ref`, `is_stale`; curva N requiere operaciones/movimientos de N. Cursor de lectura incluye generación y claves de orden; si desaparece retención (no permitido I1), error explícito, jamás salto a head. Retener revisiones, artifacts, specs/config y manifests de resultados; I1 sin GC automático. Mantenimiento sólo con writers detenidos, prueba de no referencias y autorización de su ámbito.

### 6. Q_i, moneda, costes y curvas económicas

`qi = {amount: Dec>0, currency, semantic: CYCLE_BUDGET|FIRST_ENTRY_RISK|TICKET_INITIAL_RISK|DECLARED_UNACCREDITED, method_id, method_version, sealed_at, decision_ref, operation_event_seq?, policy_digest, evidence_ref, coverage: WHOLE_CYCLE|FIRST_ENTRY|TICKET|UNKNOWN}`. Sólo `CYCLE_BUDGET + WHOLE_CYCLE + método/política/evidencia acreditados` habilita R/10k. Seal de decisión debe ser anterior o causalmente previo al primer fill; source knowledge no puede proceder de pérdida realizada/SL final. “Al abrir” significa presupuesto prospectivo del ciclo antes de asumir exposición. Puede cubrir adds planificados, no se recalcula retroactivamente al añadirlos. Breach/cambio de riesgo posterior viaja separado. QI_SEALED actual es NUEVO contrato con A; el monto de Gerard o `InitialRiskMoney` no se promueve por etiqueta sin demostrar su semántica.

Falta Q_i/método/moneda/prueba => historia aceptable con faltantes, perfiles R/10k `INSUFFICIENT_DATA` indicando operation_ref y razón. El dinero registrado puede ser evaluable de forma independiente. Riesgo cero/negativo se conserva como dato rechazado para acreditación, nunca denominador. No construir Q_i desde net loss, primer SL×qty, MM actual ni saldo posterior. Si una política single-entry prueba equivalencia, emitir el certificado con esa versión de política y su evidencia.

Cost disclosure obligatorio por operación: `{net_basis: NET_ALL_DECLARED_COSTS|GROSS_ONLY|PARTIAL_NET|UNKNOWN, commission: KNOWN_ZERO|KNOWN_NONZERO|UNKNOWN|NOT_APPLICABLE, fee:..., swap:..., other_costs:..., evidence_refs[]}`. Cero exige evidencia explícita; omisión es UNKNOWN. net final observado y declarado inclusivo de todos los costes puede tener desglose UNKNOWN: net curve READY con badge `BREAKDOWN_UNAVAILABLE`; no sumar desglose ausente ni inventar su valor. Gross sin costes acreditados conserva evidencia `GROSS_ONLY`, net curves y ranking neto `INSUFFICIENT_DATA`; no presentar gross como net. PARTIAL_NET muestra prefijo conocido, nunca métrica neta completa/score favorable. Un coste “NOT_APPLICABLE” exige razón de modelo/contrato.

Monedas diferentes nunca se suman por símbolo ni se asumen USD. `recorded_money.v1` publica series separadas por currency o una base común con FX probado y config fijada; la serie multi-money sin conversión no tiene un scalar agregado. I1 default es `NO_FX`: exigir moneda de PnL y Q_i idéntica por operación. Extensión explícita sólo mediante `fx_policy_id`, dataset_revision/digest y cada `fx_rate={base,quote,rate:Dec>0,rate_at,available_at,evidence_ref}` pinneado: convertir amount×rate en economic_at de cada movimiento; riesgo se convierte con rate de sealed_at. Sin rate causal acreditado => NOT_COMPARABLE/FX_MISSING, no spot actual, forward fill fuera de cobertura ni precio futuro. Las cuatro curvas iniciales pueden implementarse sin motor FX al declarar NO_FX. R de operaciones en distintas monedas es dimensionalmente agregable sólo si cada denominador tiene la misma moneda que SU numerador y método comparable; money total no lo es.

| Perfil | Regla económica exacta y salida |
|---|---|
| `recorded_money.v1` | `Σ d_ij` por movimiento en economic_at, o neto una vez al cierre del summary; empieza en 0 como PnL acumulado. No es saldo/equity de cuenta; depósitos/payouts/reset no son resultado de estrategia |
| `r_net_cumulative.v1` | `Σ d_ij/Q_i`; mismo denominador todo el ciclo, parciales/costes OPEN incluidos. Cierre summary aporta net/Q una vez. Etiqueta R, no USD |
| `normalized_10k_open_balance.v1` | Config inicial C0=10000 unidades virtuales, r=0.01 configurable; al abrir i sellar `B_i=r×C_realizado(t_i−)`; cada movimiento suma `B_i×d_ij/Q_i` en su tiempo económico; presupuesto es base de escala, no retiro |
| `normalized_10k_initial_balance.v1` | `B_i=r×C0` fijo en toda operación; aporta `B_i×d_ij/Q_i`; perfil distinto sin reinversión |

Presupuesto B_i y riesgo fuente Q_i son conceptos distintos. En mismo timestamp respetar orden sólo si hay secuencia causal total demostrada para esos eventos; owner seq no ordena owners/cuentas distintos. Sin ese orden, todas las aperturas del timestamp usan C(t−); luego se aplican movimientos del batch. Orden lexicográfico únicamente estabiliza salida. Una comisión del fill de apertura se aplica después del sello B de esa apertura. Operaciones concurrentes no reservan B ni tienen cap agregado; este análisis no simula margen/admisión.

Precisiones: cómputo racional exacto, resultados persistidos como `{numerator,denominator}` strings enteros canónicos cuando no hay decimal finito; además display_decimal redondeado HALF_EVEN a 12 decimales con `rounding_policy=display-half-even-12.v1`. Nunca reutilizar display para dimensionar siguiente B ni sumar curvas/score. Fact source numeric(38,18) queda intacto. `CAPITAL_EXHAUSTED` al C≤0: conservar pérdida y movimientos posteriores de operaciones YA presupuestadas; ninguna nueva apertura recibe presupuesto negativo/cero. Tramo posterior sin tamaño evaluable queda incompleto con primera operation bloqueada; no clamping a cero ni resurrección de capital por una apertura nueva.

Métricas terminales (PF/win/expectancy/SQN) reciben por ciclo completo su resultado bajo el perfil seleccionado; un parcial no es un trade. Curva realizada/DD de balance puede incluir parciales OPEN; sin marks no certificar equity DD, intrabar risk ni mark-to-market. Ventana temporal suma movimientos en `[from,to)`; métricas por cohorte declaran criterio de inclusión/terminalidad y as_of. La definición final de métricas/rankings de D debe fijar qué universo usa, sin cambiar economía ni omitir costes/operaciones faltantes.

### 7. Fechas, selección continua y ausencia de look-ahead

| Campo | Dueño semántico y uso |
|---|---|
| `construction_at` | Fecha real probada en que esa definición/version quedó construida. Única frontera PRE/POST_CONSTRUCTION D16 |
| `construction_data_cutoff` | Límite exclusivo de los datos usados para construir/seleccionar; conserva dataset/evidencia. No sustituye construction_at ni implica disponibilidad |
| `available_at` | Disponibilidad de StrategyVersion en el sistema declarado (`availability_domain_ref`); distinta de aceptación de la historia en Echo. Fecha histórica desconocida queda UNKNOWN |
| `echo_reference_started_at` | Inicio explícito acreditado de referencia Echo para versión/cuenta/contexto. No receipt ni día del primer import; tomar evento de inicio/primer OPEN aceptado acreditado y guardar esa regla/evidencia |
| `received_at`, `known_at` | Reloj servidor al aceptar revisión y conocimiento fuente por evento respectivamente; no se backdatean con tiempos económicos |

Normalmente cutoff≤construction_at≤available_at; contradicción declarada requiere evidencia/razón, no normalización automática. Echo start anterior a construcción de esa MISMA versión es `TEMPORAL_METADATA_CONFLICT`; conservar historia fuente pero bloquear clasificación compuesta hasta corregir contexto/version. Fecha de construction desconocida: no hay pre/post demostrado. Origen y run_mode nunca se derivan de período: backtest después de Echo start continúa BACKTEST.

`HistorySelectionRevision = {selection_ref, revision_no, previous_digest, context_ref, segments[], carry_policy: WHOLE_CYCLE_FROM_OPEN, knowledge_mode, created_at, digest}`. Cada segmento `{segment_id, from, to|null, history_ref, history_revision_no, revision_digest, role, mm_context_digest}` fija intervalo por APERTURA `[from,to)`. Segmentos principales sin solape; alternativas enumeradas fuera del set económico. Validar misma StrategyVersion y contexto solicitado; MM divergente queda `CONTEXT_DISCONTINUITY` visible y no entra en comparación “misma gestión”/ranking homogéneo. No elegir primera historia de una lista. Una sola candidata puede resolverse SINGLE; varias sin elección explícita => UNRESOLVED visible, sin sumarlas.

Algoritmo de vista continua:

1. Fijar vector de revisiones y metadatos. Selección típica: historia Forge elegida antes de Echo start y REFERENCE Echo desde ese instante; disponibilidad/coverage debe sostener cada segmento. No concatenar automáticamente las cuentas/copias/runs alternativos.
2. Incluir cada ciclo sólo si opened_at cae en SU segmento. Conservar todos sus movimientos hasta as_of aunque cierre después del límite de segmento (carry-out) y su cohorte de apertura original. Apertura preconstrucción sigue PRE aunque el resultado se realice POST. No trasladar PnL de fecha.
3. Si otro segmento contiene representación del MISMO ciclo/hecho, deduplicar exclusivamente por `equivalence_crosswalk={canonical_cycle_ref, exact_source_refs[], relation SAME_ECONOMIC_FACT, evidence_ref, authority_writer}` de la fuente dueña. Elegir una representación por grupo, granularidad completa priorizada mediante cambio explícito, no sumar journal summary y runtime movements. Master/copias no comparten SAME_ECONOMIC_FACT.
4. Sin crosswalk suficiente para un ciclo que cruza la frontera o podría estar duplicado, conservar alternativas y marcar `BOUNDARY_CONTINUITY_UNPROVEN`; selección no es READY continua hasta elegir exclusión explícita con coverage GAP o probar vínculo. No adivinar por instrumento/hora/precio, ni reemplazar un CLOSED_SUMMARY por fills fabricados.
5. Huecos de cobertura se propagan; no rellenar línea plana. Sumar realizaciones simultáneas de ciclos distintos es legítimo; “sin solapes” restringe selección de representaciones/fuentes de un hecho, no prohíbe exposición simultánea auténtica.

Dos modos de consulta explícitos, sin motor de selección I2:

- `RETROSPECTIVE_REVISION`: revision vector explícito + economic `as_of`; excluye movimientos de tiempo económico posterior. Corrección conocida hoy puede cambiar ayer y nuevos B; conservar resultado previo y marcar `knowledge_claim=RETROSPECTIVE_ONLY`.
- `AS_KNOWN_IN_ECHO`: además `knowledge_cutoff`; usar sólo revisión aceptada `received_at≤cutoff` y hechos con known_at probado≤cutoff, y versión disponible en ese dominio antes del corte. Una revisión nueva no se presenta como si hubiera sido conocida antes. Sin vintage/snapshot fuente que sostenga ese conocimiento => `KNOWLEDGE_UNPROVEN`; no truncar N+1 como sustituto de N archivada. NO_FX también exige disponibilidad causal de cada rate si se habilitara FX.

Estos campos preservan extensibilidad sin scheduler, Top N, rebalanceo, membresías temporales ni infraestructura I2. Las consultas retrospectivas de I1 no se venden como selección causal histórica de estrategias.

### 8. Composición estática D11 y comparación de copias

Contrato estático `StaticComposition = {composition_ref, revision_no, composition_start_at, economic_as_of, C0:Dec>0, risk_fraction:Dec en (0,1], profile_id, algorithm_version, config_digest, members[{member_ref, version_ref, mm_context_digest, selection_revision_digest|history_revision_digest, weight:Dec≥0}], snapshot_manifest}`. Miembros elegidos manualmente, pesos fijos iniciales Σw≤1; duplicar un input económico en dos miembros se rechaza `DUPLICATE_COMPONENT` salvo separación de cuentas/historias que pruebe evidencia distinta. Un peso cero no exige datos ni afecta métricas. No membresías dinámicas ni rebalanceo.

`C0_j=w_j×C0`, `cash=(1−Σw)×C0`, `C_total(t)=cash+ΣC_j(t)`. Capital separado; resultados no prestan a otro miembro. Cada miembro empieza FLAT: excluir por completo ciclos abiertos ANTES de composition_start_at, aun cuando realicen después; incluir abiertos exactamente al inicio. Recalcular cada componente con su capital asignado y presupuestos B causales desde ese inicio. Cortar gráficamente una curva de 10k anterior no cumple flat start. Las curvas normalizadas inicial/open son homogéneas lineales en C0 si r/modelo son iguales y sin redondeos intermedios, pero reusar escala sólo con manifest que pruebe mismas operaciones/fecha inicial; de lo contrario recalcular. recorded_money no se reescala como capital nuevo; R se puede comparar, no sumarse como saldo. D11 publica capital virtual bajo perfil normalizado elegido, no equity/margen/live allocation.

Coverage común requerida para miembros de peso>0. GAP/INSUFFICIENT/STALE/CAPITAL_EXHAUSTED se propagan; prefijo común válido puede mostrarse con su rango y estado incompleto. Cash residual sólo es remanente inicial, jamás sustituto de un miembro sin datos. Realizaciones OPEN se conservan al as_of junto a exposición/flotante desconocidos. Snapshot fija composición/pesos/inicios/revisiones/perfil/ventana; actualización de una historia no reescribe portfolio previo. Worker usa CAS del vector y coherencia de publicación §5.

Comparación básica I1 conserva por oportunidad/copia `{reference_event_id|copy_intent_id, reference_operation_ref, execution_operation_ref, reference_order_ref?, matched_fills[], expected_qty, matched_qty, clocks_basis, coverage}`. Enlaces exactos del runtime/journal; sin matcher probabilístico. Precio VWAP sólo sobre qty comparable y evidencia de fill: compra adverse=exec−ref, venta adverse=ref−exec; monetizar exige multiplicador/moneda/FX probados. No ejecutada/rechazada/sin correlación es categoría explícita, jamás slippage=0. Diferencia de PnL entre MMs no prueba slippage; una referencia summary permite comparar resultado con limitación, no inventar latencias/fills. Respuesta lleva expected/executed/omitted/rejected/unmatched y denominador del promedio; sin expectativas probadas, cobertura NOT_COMPARABLE.

### 9. Estados y fallos verificables

Estados separados: ingestión `INGEST_ACCEPTED`; disponibilidad de historia `ACCEPTED|QUARANTINED`; economía por perfil `READY|INSUFFICIENT_DATA|NOT_COMPARABLE|CAPITAL_EXHAUSTED`; cálculo `PENDING|RUNNING|PUBLISHED|OBSOLETE|FAILED_RETRYABLE|FAILED_PERMANENT`; exposición `FLAT|OPEN|UNKNOWN`; continuidad `RESOLVED|UNRESOLVED|GAP|CONFLICT`; readiness operacional exclusivamente B/A. Ningún estado analítico READY autoriza trading ni certifica Echo operational.

Cada resultado lleva reasons estructuradas `{code, entity_ref, field_path, evidence_ref?, missing_count, affected_interval?}`, no cero de conveniencia. UNKNOWN_CURRENCY, COSTS_UNKNOWN, QI_UNPROVEN, OPEN_EXPOSURE_UNMARKED, COVERAGE_GAP, BOUNDARY_CONTINUITY_UNPROVEN, KNOWLEDGE_UNPROVEN y CONTEXT_DISCONTINUITY se preservan hasta servicio/UI/rankings. Un profile distinto puede estar READY sobre la misma historia insuficiente para R. No omitir operaciones silenciosamente ni renormalizar pesos del ranking.

HTTP/servicio: 400 shape/JSON; 403 writer/namespace no autorizado; 404 scoped resource no visible; 409 receipt/CAS/scope/source conflict; 413 límite; 422 semántica/conservación/digest incorrecto; 503 artifact/DB transitorio. Cambios de head fallidos y validaciones no dejan revisión/receipt parcial. Retry con misma key para incertidumbre; key nueva sólo para payload nuevo, CAS nuevo o intento corregido. Límite V2: ≤128 MiB request, ≤8 historias, ≤250000 operaciones/historia, ≤1000000 movimientos/historia; rechazo explícito sin truncar ni dividir por símbolo. Medición de capacidad pendiente; multipart de UNA historia es seam posterior si la medición lo exige, no implementación especulativa.

### 10. Casos de aceptación numéricos y adversariales para Shot 2/3

Son tests especificados, **NOT_RUN en Shot 1**. Los números siguientes son fixtures deliberados para oráculos, no datos ni PASS de producción.

| ID | Entrada / acción | Oráculo exigido |
|---|---|---|
| C01 identidad | Una versión, source A cuenta X/run1 y cuenta Y/run1 o X/run2; IDs locales iguales | Historias/ref distintas y tres resultados independientes; ninguna pisa la anterior |
| C02 revisión/replay | Crear N=1, sumar parcial +40 en N+1, terminal +60/fee−2 en N+2; repetir cada receipt | N intacta; total N+2=98; replay sin revisión nueva; snapshot no contiene sólo última operación |
| C03 carrera CAS | Dos writers autorizados con expected N y payloads diferentes | Sólo uno N+1; otro 409; sin mezclar movimientos. Replay ganador después de N+2 devuelve receipt original |
| C04 grano/costes | Summary net=114; alternativa movements +120−4−2; cost evidence completa | Cada representación da 114, selección de una da 114, jamás 228. Upgrade N+1 conserva mismo operation_ref y sin doble aporte |
| C05 parcial | Q=100, OPEN realiza +40, comisión−2, remanente abierto | money=38; R=0.38; capital 10k=10038; terminal trade_count=0; flotante UNKNOWN |
| C06 Q_i ciclo | Primera entrada risk=20; certificado ciclo=100; net final=50 | R=0.5, no 2.5. Q_i ausente/tag ticket/método ausente ⇒ R/10k insuficientes; money sigue 50 si moneda/costos válidos |
| C07 causal sucesiva | Q=100 cada ciclo; +2R cierra antes de apertura del −1R | open_balance: 10000→10200→10098; initial_balance final=10100 |
| C08 concurrente/empate | Ambos abren antes de conocer +2R/−1R, o mismo timestamp sin orden causal probado | Ambos B=100 y final=10100; cambiar IDs/orden de input no cambia tamaño |
| C09 atribución | A 1@100, B 1@110, B cierra115, A cierra120, multiplier1 | B=5, A=20, suma=25; cuenta FIFO +15 luego+10; diferencia de timing visible; sin otro engine |
| C10 coste/moneda | Gross=120, comisión omitida; luego costo−6 probado. Otra fila USD sólo default técnico | Primera net insuficiente, jamás120 net. N+1=114. Default no prueba USD; no agregación certificada de esa fila |
| C11 FX | Movimiento EUR100, Q USD100, sin FX; después rate EUR→USD1.1 con tiempos/provenance | NO_FX ⇒ NOT_COMPARABLE; perfil explícito FX produce USD110 y 1.1R; rate futuro/spot actual rechazado. EUR100+USD100 sin conversión no es200USD |
| C12 períodos | construction 10:00, cutoff09:00, available11:00, Echo12:00; ciclo abre09:30 cierra12:30 net10 | Cohorte PRE, realización12:30/ECHO_PERIOD, fuente original intacta; no usar09:00 ni received para frontera |
| C13 selección/carry | Forge ciclo abre11:50 y cierra12:10; Echo start12:00. Echo contiene representación del mismo hecho | Crosswalk probado ⇒ una sola contribución; sin crosswalk ⇒ BOUNDARY_CONTINUITY_UNPROVEN; no net doble ni fills artificiales |
| C14 conocimiento | N recibida13:00 net100; N+1 recibida15:00 corrige net80 económico12:00 | Retrospectivo N+1 as_of14:00=80; AS_KNOWN_IN_ECHO cutoff14:00 usa N=100, no N+1 backdated |
| C15 D11 | C0=10000, wA=.6,wB=.4; A secuencial +2R/−1R, B −1R; r=.01; flat al inicio | A6000→6120→6058.8; B4000→3960; total10018.8. Pesos finales derivan; no rebalanceo |
| C16 flat/cash/gap | wA=.6,wB=.3,cash=.1; A tenía ciclo preinicio que cierra+100 luego; B tiene GAP | Excluir íntegro ese ciclo, cash1000 exacto; GAP no se convierte en cash/plano; agregado incompleto |
| C17 capital agotado | C0=10000, Q100, primera B100 produce−110R; otra ya presupuestada +20R, otra apertura nueva posterior | C=−1000, luego+2000=1000 para operación ya sellada; agotamiento histórico visible; apertura mientras C≤0 no recibe B, tramo completo insuficiente |
| C18 corrección/retraction | Movimiento+40 en N, corrección+30 en N+1; retractarlo N+2 con evidencia | Totales40→30→0; no +40−10+30 duplicados. Sin change_entry, SILENT_REMOVAL; N reproducible |
| C19 worker/UI | Worker N pausado; aceptar N+1; worker N publica después | No mueve current; N visible coherente/pending con opsN, después N+1 completa; cursor N no lee movimientos N+1 |
| C20 fallos/retención | Caer entre artifact y commit; caer después del commit antes respuesta; perder lease | Primer caso sin head/receipt y posible orphan; segundo GET receipt recupera efecto único; tercero fencing impide publicación vieja; ningún artifact referenciado se borra |
| C21 fill tardío/conflict | Replay fill físico mismo payload; misma clave diferente qty; fill nuevo después terminal | Replay no suma; conflicto en cuarentena; nuevo fill conserva ciclo original+RECONCILIATION_REQUIRED, no sucesor |
| C22 copias | Buy ref VWAP100, exec101 qty2 multiplier10; otra oportunidad omitida | Adverse dinero20 en matched qty2; omisión contada separada, sin slippage0 ni esperanza de qty inventada |
| C23 hash | Reordenar claves/sets, cambiar operación económica, unknown field o tiempo de polling | Primer caso mismo content_digest; cambio económico/unknown cambia digest; polling no crea revisión. Dec1.0 y−0 rechazados; Unicode distinto no converge por NFC |
| C24 alcance/request | Historia multiinstrumento132805 ops completa; 8 historias válidas y 9ª; request sobre128MiB | No partición semántica por símbolo; exceso413 y aceptación atómica sin filas parciales; benchmark real pendiente |

Superficies mínimas: DTO/validación V2 y wire existente; repositorio/servicio V2 aditivo con CAS/retención/outbox; extractor puro de attribution junto a accounting y emisor owner A; adapter journal source snapshot del writer canónico; selección temporal y manifests; worker/curves/composición estática usando los mismos snapshots. Pruebas dirigidas críticas de transacciones, replay, moneda/costes/Q_i, continuidad, D11 y generaciones; no suites/builds ni acceso a infraestructura en Shot 1.

### 11. Gates del documento

`DESIGN_CONTRACT=SPECIFIED`. `SOURCE_INSPECTION=VERIFIED_LOCAL` para SHA indicado. `IMPLEMENTATION/UNIT/INTEGRATION/CAPACITY/PHYSICAL_E2E=NOT_RUN`. Artefacto Forge auténtico, reachability y cuentas/permisos aislados pertenecen a gates externos de B; ausencia de evidencia deja `BLOCKED_EXTERNAL` cuando impida ese gate, sin sustituir por fixtures. Sin cambios de código, producto, runtime, infraestructura, campañas, órdenes, tests ni ramas; sin commits del especialista.

## Fuentes

- [[F — Decision Register]] D09/D10/D11/D16–D24; [[Echo — Producto Integrado]] — autoridad de alcance y restricciones actuales.
- [[THE_LAB_V4_Diseno_para_revision]] B.1–B.6, E.1–E.4; [[1 — TECHNICAL_FREEZE_PACKET]] §2–§4/§6 — requisitos compatibles, no baseline de código.
- [[0 — Submanager State]] y [[SHOT4_HANDOFF]] — continuidad histórica; PASS y capacidades reportadas no se trasladan a runtime vigente.
- `xKoRx/echo@2ee61791deb3139be23e1c9be3708b1d41da8d6b`, rutas y líneas enumeradas en §1; contratos nuevos de §2–§10 son decisiones de este Shot 1.
