---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures — Execution Client y Feed Batching]]"
  - "[[EXECUTION-FEED-BATCHING-DESIGN]]"
  - "[[EXECUTION-FEED-BATCHING-VERIFICATION]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# EXECUTION-FEED-BATCHING-S02-DICTAMEN

## Propósito

Dictamen consolidado del verificador adversarial independiente (FEFB Shot 2 de 3). Sesión ONE-SHOT, contexto fresco, sin subagentes; superficie LOCAL; modelo efectivo GLM-5.3-Flash (reasoning Max autorizado). Reconstructor de AC01–AC16 y atacante de los 7 ejes del despacho sobre el delta completo `112ccccd..960bf60a` (96 archivos, +21292/−294), no sólo MR1c2. Autorización: G1 = accepted (decisión Primary Manager GPT-6, 2026-10-22, persistida en el planner); S1 cerrado para este corte. Producto READ-ONLY: únicos archivos nuevos = reproductores de auditoría en copia aislada. Sin fixes, sin merge, sin deploy; S3 no iniciado.

- AUDITED_SHA: `960bf60ae0832570ca3b97aba0e7badea486bb00` (`origin/feature/ef-runtime-pools`, HEAD=origin verificado; worktree aislado limpio).
- BASE ORIGINAL: `112ccccdbbf32bc3ca486fd04a28ab0afa0451a4` (checkout aislado propio para comparación por causa).
- Veredicto: **REQUIERE_CORRECCION** — 2 DEFECTO_CONFIRMADO (P1, causa raíz común del ACK acumulativo cliente/feed), 1 GAP_DE_VERIFICACION, 3 OBSERVACION_NO_BLOQUEANTE. El resto del alcance: CONFORME_EN_ALCANCE con evidencia ejecutada en esta sesión.
- G2: **review** (la auditoría se completó; la adjudicación de findings y scope de S3 es del Primary Manager).
- Evidencia durable: `/home/kor/aranea/work/fefb-s02-audit-20261022/evidence/` (worktrees `echo`/`base`, sweeps, logs dotnet, sonda STAMPED, cobertura, hashes de reproductores).

## Método

Checkout aislado del candidato y de la base (worktrees detached, jamás sobre el workspace del implementador). Suite completa candidato vs base comparada por nombre y causa; suites dotnet del motor puro ejecutadas con SDK 8.0.426 user-local (las pruebas Go NO se aceptan como acreditación del comportamiento C#); reproductores NUEVOS atacando los bordes que las suites del implementador no ejercitan; cadena de configuración atacada con handlers reales (RequestReplyHandler con checkpoint cerrado) desde JSON de envelope, nunca por inyección de fixtures; capacidad del camino STAMPED medida con productor open-loop, estado maduro, ráfagas, 2× y stall-recovery con llegadas continuas; race funcional separado de las mediciones de capacidad; cobertura reproducida con el método W4 del implementador sobre perfiles frescos sin cambiar denominadores.

## Hallazgos (consolidados por causa raíz)

| ID | Clase | Severidad | Requisito | Archivo/símbolo | Esperado | Observado |
|---|---|---|---|---|---|---|
| FEFB-S2-01 | DEFECTO_CONFIRMADO | P1 | Diseño §5: publicación parcial o ACK perdido produce reentrega, no omisión; ACK sólo tras publicación durable de TODOS los grupos | `v3/futures-bridge/adapters/ntfeed/relay_batch.go` — `runConnWorker`/`processJob` | Un frame con publish fallido no puede quedar cubierto por un ack posterior | El FIFO drena el frame siguiente tras un fallo: frame seq=2 publica y emite `feed_ack{up_to_seq:2}`; el cliente retira por prefijo (`Acknowledge`, `SeqLast <= cursor`) el frame seq=1 NUNCA publicado ni retransmitido → pérdida silenciosa |
| FEFB-S2-02 | DEFECTO_CONFIRMADO | P1 | C4/§5; pin de la propia matriz (FeedV1ContractTests.cs:486-489): el ack de negociación NO lleva componente de cursor | `negotiateHello` (relay_batch.go:431) + `FeedV1Engine.OnFeedAck` (EchoFeedV1.cs:1677) + `FeedWriterLoop` (retransmit gated en StateActive) | Los pendientes durables retransmiten byte-idénticos tras la negociación; el ack de negociación no retira nada | El hello reabre la sesión con seq sobre el durable floor (espacio compartido); el relay responde `up_to_seq=<helloSeq>`; el cliente retira TODOS los pendientes (`pendingAfterNegotiationAck=0`) antes de la retransmisión one-shot → pérdida en toda reconexión con lotes un-acked |
| FEFB-S2-03 | GAP_DE_VERIFICACION | media | AC13; matriz: registro de una ejecución con condiciones declaradas | `fefb_w4_capacity_campaign_test.go`; condición de entorno | PASS AC13 reproducible en condiciones declaradas | El PASS de MR1c2 (edad max 11,14s) requiere host silencioso: bajo contención de CPU moderada la misma campaña en el MISMO SHA falla (edad max 36,5s > 30s; backlog no recuperado in-run; processed==ingress y errors=0 intactos) y la corrida de cobertura del propio implementador registra su FAIL (923,5s). `TestBridgeRunsSessionsAndShutsDownCleanly` flakea igual y pasa solo. Condición NO declarada; no es defecto de producto demostrado |
| FEFB-S2-04 | OBSERVACION_NO_BLOQUEANTE | baja | §4/§7 hot change rechazado con causa; docstring applyBarsOrigin: "rejection counters persist" | `analytics/bars_origin.go` + gate `handleCanonicalEventBatch` | Rechazo visible y autoridad intacta (cumplido); recovery tras revertir config | La declaración rechazada + su C2 gated viajan agrupados en UNA request: el gate aborta la request entera → la declaración y el contador nunca cometen (contador duradero 0 pese al log) y la request reintenta por siempre (head-of-line). Revertir el relay NO drena los forwards envenenados del mailbox: recuperación manual sin procedimiento documentado. En V1 el hot-change está fuera del camino normal |
| FEFB-S2-05 | OBSERVACION_NO_BLOQUEANTE | baja | Re-ejecutabilidad de la matriz de contrato C# | `tests/FeedV1ContractTests.cs` Main (raíz fija `/tmp/feedv1-contract`) | La matriz re-ejecuta limpia | La 2ª corrida sin limpiar la raíz fija falla 10 asserts por estado residual durable (identidad+outbox de corridas previas). Con raíz limpia: 96/96 |
| FEFB-S2-06 | OBSERVACION_NO_BLOQUEANTE | baja | D5/D7 una sola autoridad por stream | `handleCandidate` (singleton lane) vs gate batch | Legacy auténtico por shape (diseño) | El gate NOTE-8 aplica sólo a batch-kind: singletons legacy sobre stream perfilado no se gatean (analytics protege por config en ambos sentidos, verificado). D5 es disciplina de config sin enforcement del relay; declarar en runbook que el perfil no autoriza productores singleton mixtos en el mismo stream |

### Reproductores (durables, con hash en evidence/REPRODUCER_HASHES.txt)

- `fefb_s2_audit_repro_test.go::TestS2Audit_X3_FalseCumulativeAckAfterFailedPublish` — Go, ROJO sobre 960bf60a: "acks=[{UpToSeq:2 ...}] batchesPublished=1". Clase: PERMANENT_REGRESSION.
- `S2AuditRepro.cs::X1_NegotiationAckRetiresPendingBeforeRetransmit` — C# (motor puro linkeado), ROJO: pendientes retirados por el ack de negociación. `X2` — faceta cliente del S2-01 (retired=2 con seq1 nunca publicado). Clase: PERMANENT_REGRESSION.
- `fefb_s2_stamped_audit_test.go::TestS2Audit_StampedLaneFirstBatchGateAndHotChange` — Go, verde con la observación S2-04 documentada en el propio test. Clase: PERMANENT_REGRESSION.
- `TestS2Audit_StampedCapacityProbe` — sonda STAMPED 300s sobre handlers reales. Clase: E2E_CANDIDATE (AC13 stampado).
- Colector ordenado `BarsOriginUpdate`+C2 (`s2CollectForwardsOrdered`) — el colector de la campaña W4 descarta las declaraciones head-of-frame. Clase: HARNESS_TOOLKIT_CANDIDATE.
- Corridas sweep/coverage de la sesión. Clase: DISPOSABLE_REPRODUCER.

## Verificación por eje (ejecutada, no heredada)

- **Eje 1 CONFIG/ORIGEN — CONFORME.** Cadena perfil C3 (etcd `futures-bridge/nt-feed/feed-profile`, parseFeedProfileSection fail-closed en startup) → relay (stamp per-batch SOLO desde cfg.Feed aplicada; sin perfil = UNSTAMPED) → market_stream (declaración HEAD-OF-FRAME antes de los eventos; evidence durable `futures_ms_bars_origin`; unstamped-con-evidence falla visible SIN commits — snapshot byte-idéntico verificado; reentrega reconverge) → analytics (aplicación idempotente; gate declarada≠aplicada; autoridad durable `futures_ma_bars_origin`). Stamp desde el PRIMER batch, demora/retry (reintentos del runtime sobre datos durables en Kafka, nada convertido a decisión), restore (evidence sobrevive round-trip del checkpoint) y hot-change rechazado: verificados con handlers reales desde JSON de envelope (test determinista S2 + suites MR1c2 verdes en el sweep). etcd-caído en startup: las claves requeridas (auth-token/instruments) matan el proceso antes de poder degradar a legacy accidental.
- **Eje 2 BATCH/PERSISTENCIA — CONFORME.** AC07 splits 1/2/50/1001 sobre RequestReplyHandler real y AC08 (veneno a mitad, restore, 2 keys intercaladas) verdes en el sweep; memo del shell keyed por identidad de storage (sin reuse cross-request; el fallo olvida su entrada); ninguna caché cruza owners (analytics sin memo).
- **Eje 3 CLIENTE/OUTBOX/ACK — REQUIERE_CORRECCION (S2-01/S2-02).** Motor C# ejecutado REAL (EchoFeedV1RepairTests 94 asserts verde; matriz 96 asserts verde con raíz limpia); identidad durable, ACK perdido, crash alrededor de ack/compaction, saturación→progreso cubiertos por S1..S8; los DOS defectos son los bordes que esas suites no componen (ack acumulativo × frame fallido posterior; ack de negociación × pendientes).
- **Eje 4 BARRAS/TICKS/CONTINUIDAD — CONFORME.** Ingestión nativa y autoridad por config, no por llegada (suites MR1/MR1c/MR1c2 verdes en sweep); D3 (barras jamás muestreadas) fail-closed en ingress Go + guard C#; LAST por clase con C6 (QUOTE no borra TRADE, ventanas event-time, late etiquetado) en la matriz C#; multi-TF sin consumidores (suite MR1); historia sin consumidores + gaps + readiness (MR1 F2); supresión de agregación TRADE bajo NATIVE observada en contenido durante la sonda ("trade aggregation suppressed on native-authority builder").
- **Eje 5 EXECUTION CLIENT/BRIDGE — CONFORME.** M2/fencing pinneados sha256 byte-identidad (verdes en sweep); Bridge sin decisiones económicas ni sampling (revisión de source: transporte/stamp/routing/ack únicamente); comandos, cuentas y resultados preservados (lanes M2 intactas); MT4/MT5 y legacy NT compatibles (legacy_feed_compat verde, legacy byte-exacto pinneado); una sola definición de instalación (runbook guard verde; EchoFeedAddOn = legacy opcional); un engine por proceso con N bindings (matriz F4).
- **Eje 6 CAPACIDAD CAMINO STAMPED — CONFORME EN LAB con ventana reducida.** La campaña MR1c2 ejercitó UNSTAMPED (PROVENANCE); esta auditoría ejercitó el STAMPED end-to-end sobre handlers reales: maduración 1,13 MiB (0,7s) + 300s con 1× capturada + ráfagas 256 + 2× headroom + stall de consumidor con llegadas continuas → ingress==processed 23.552, errors=0, gateFailures=0, autoridad NATIVE intacta, identidad/contenido verificados (no sólo ingress==processed). Límites declarados: ventana 300s vs AC13 1800s; checkpoints de runtime aislado NOT_RUN (físico vigente CERT-NT-01). Artefacto: evidence/e6-capacity/stamped_probe_300s.log.
- **Eje 7 REGRESIONES/COBERTURA — CONFORME.** Sweep completo candidato vs base: los 5 fallos heredados fallan con MISMAS causas (mismo archivo:línea y mensaje) → cero regresiones nuevas reales; los 2 fallos adicionales del candidato existen sólo bajo contención de CPU y pasan solos (ver S2-03). Cobertura reproducida con el método W4 sobre perfiles frescos: universo NUEVO **631/653 = 96,63%** (≥95%, reproducción EXACTA del claim) y delta completo **1181/1247 = 94,71%** (mismo denominador 1247 del implementador; MERGE MAX explica +3 statements). Sin cambios de denominador ni asserts debilitados. Race funcional en curso al cierre (resultado en evidence/e7-regressions/race_s2.log).

## Limitaciones físicas (sin cambio)

Compile NT con assemblies reales, runtime StateFun aislado/checkpoints, Kafka broker real, instalación física del AddOn, ACK extremo-a-extremo con broker: NOT_DEMONSTRATED/NOT_RUN → gates de CERT-NT-01. No se convirtieron en requisitos de desarrollo nuevos ni se usaron mocks como prueba física.

## Paquete de reparación recomendado para S3 (adjudicación del Manager)

1. S2-01: detener el drenaje del FIFO de la conexión al fallar un publish hasta reintentar el frame fallido (o acks no acumulativos); reproductor rojo X3 como oráculo permanente.
2. S2-02: ack de negociación sin componente de cursor (UpToSeq=-1, cumple el pin de la matriz) o campo separado de versión aplicada; y en el cliente no aplicar cursor de acks con ConfigVersion antes de la primera retransmisión (defensa en ambos lados).
3. S2-03: declarar la condición host-dedicado de AC13 en la matriz y re-ejecutar AC13 en host dedicado para el cierre de S3; endurecer opcionalmente la medición de edad contra scheduling.
4. S2-04: documentar recuperación del wedge hot-change en el runbook; persistir el rechazo fuera de la request que puede abortar; corregir docstring.
5. S2-05: directorio temporal único por corrida en la matriz C#.
6. S2-06: una línea de runbook (perfil no autoriza mezcla singleton/batch del mismo stream).

## Registro de la sesión

Modelo efectivo: GLM-5.3-Flash (surface ZCode, LOCAL). G2 = review entregado al Primary Manager; nunca auto-aceptado. Sin fixes de producto, sin merge, sin deploy, sin iniciar S3.
