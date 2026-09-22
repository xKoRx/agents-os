---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
related:
  - "[[Polymarket Engine — MVP]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
  - "[[Research — Historical L2 Forensic Validation 2026-09-21]]"
  - "[[Research — Historical Data Acquisition ADDENDUM 2026-09-21]]"
aliases:
  - ASTRA_HISTORICAL_CAUSALITY_AUDIT
tags:
  - kind/doc
  - project/polymarket-engine
  - topic/causality
created: "2026-09-22"
updated: "2026-09-22"
---

# Polymarket Engine — Historical Causality Architecture Audit

## Propósito

Auditoría adversarial ONE-SHOT de documentación y código del backtest histórico. Responder si una estrategia sólo puede consumir información disponible y estados admisibles en su instante de decisión. Entrega documental del 2026-09-22; no modifica contratos congelados, código, economía V2, infraestructura, Sports Week ni OOS. La SPEC de §9 es propuesta correctiva; las decisiones de modelo de §12 permanecen pendientes del owner.

## Contenido

### 1. Resumen ejecutivo

**Dictamen: el engine actual NO permite certificar un backtest histórico causal de extremo a extremo. M1 sí exige las propiedades principales; la implementación las cumple parcialmente y tiene desviaciones demostrables.** No hace falta reemplazar el monolito, el simulador ni la Strategy API. Hace falta cerrar el camino de entrega `journal prefix → reducers → frame → elegibilidad → decisión`, con dependencias temporales verificables y sin lectores de estado final.

La baseline leída físicamente es `xKoRx/polymarket-engine master@09e8c7610f29a35f8080122b7cb4219b9866ebd7`; `git ls-remote` confirmó ese mismo SHA en `origin/master` y `origin/main`. El commit de código es `66486ac99a4606d5dc2b44757ac0722a6baa5415`; el siguiente commit contiene recertificación. Checkout limpio al comenzar. No se hizo fetch, checkout, patch ni push del engine.

Hallazgos prioritarios:

1. **D01 — Regímenes finales consultados durante reconstrucción pasada.** `Qualities` es terminal, no un stream de frames; su look-ahead interno está demostrado y hasta exigido por un test. SHADOW sí consulta el mismo servicio latest al resolver fee para un candidato histórico.
2. **D02/D03 — La calidad que ve Strategy no es la calidad de Books.** SCREEN y SHADOW usan `marketview`, promueven snapshots sin régimen/tick, omiten controles de gap y carecen de fencing suficiente. Los deltas temporalmente regresivos no disparan el control que sí se aplica a snapshots.
3. **D04/D07 — La importación y los cortes pierden garantías de procedencia y orden.** Se fusionan witnesses en conexión/epoch sintéticos; el orden por tipo puede contradecir la secuencia de un mismo recolector; se puede cortar en medio del fan-out de un record multiasset.
4. **D05/D07 — La evidencia de replay es más débil que su descripción.** El digest de observación no contiene niveles ni regímenes; el vector de frame llama `regime` a la revisión de un solo `marketview`; resolver un hash no vacío no comprueba sus bytes.
5. **D06/D08 — Historia de revisiones y metadata incompletas.** A→B→A deja B como estado vigente; las observaciones externas se filtran por secuencia, sin hacer cumplir publicación/disponibilidad, y el kickoff de Sports se acepta como parámetro sin provenance temporal.

**Lo que sí se confirmó:** `book` reemplaza niveles; `price_change.size` se asigna de forma absoluta y cero elimina, con mapas por asset, tanto en Books como en marketview. No hay evidencia de que el engine use el algoritmo aditivo defectuoso del certificado externo. Capture separa recepción/fuente y publica su frontera durable después de fsync; Frames tiene barreras FIFO y espera persistencia antes de entregar. Esas piezas se reutilizan.

Ejecutado en esta auditoría, con red de dependencias deshabilitada: `GOPROXY=off GOSUMDB=off go test -count=1 ./internal/histimport ./internal/books ./internal/marketview ./internal/regimes ./internal/frames ./internal/replay` → **6/6 paquetes PASS**, Go 1.27.1. No se ejecutaron nuevas regresiones, backtests de alpha, ni recertificación M4. PASS de los tests existentes no resuelve sus omisiones ni convierte un comportamiento incorrecto codificado por un test en contrato válido.

**Alcance físico del histórico:** existen localmente los directorios del dataset y los scripts forenses; se inspeccionaron `recon.py`, `bba_check.py` y `cut_states.py` como código, sin ejecutarlos ni leer eventos/raw/OOS. Los hashes y métricas de 0/628, 514/516, ~92% y 674 s siguen siendo **resultados reportados, no revalidados por esta auditoría**. No se alegan datasets inexistentes; se preserva la frontera entre lectura de código y revalidación de datos.

### 2. Veredicto de compatibilidad temporal y autoridades

M1.3 establece `observed_at`, `source_at?` y `effective_from` sólo cuando lo establece la fuente; ausencia significa conocido desde observación. M1.5 ordena reproducir recepción, prohíbe inventar orden global y exige constraints para `OBSERVED_USABLE`. M1.6 exige reconstrucción por `capture_seq`, inputs recuperables por fase, censura declarada y nunca rellenar conocimiento pasado con metadata posterior. FBL-004 y FBL-008 fueron integrados en ASTRA-2; ASTRA-3 congeló esas obligaciones. M2-S05…S10/S13 las vuelve pruebas y entregables. **La lectura as-of no es un cambio de modelo respecto de M1; es cumplimiento pendiente.**

La prohibición M1 de reordenar por timestamp de fuente es correcta para replay del sistema. Una reconstrucción idealizada del mercado necesita un perfil contrafactual explícito, hoy no especificado para importaciones multi-witness. La adquisición/backfill L2 y Parquet estaban diferidos: su ausencia original no es un defecto M1. Una vez añadido `histimport`, no puede heredar automáticamente el certificado causal de un journal nativo.

| Materia | Diseño congelado | Implementación observada | Informe previo / reconciliación de las tres versiones |
|---|---|---|---|
| Deltas | M1.5: absoluto, cero elimina | Books y marketview lo cumplen [C02/C03] | Forense refuta el modelo aditivo del certificado externo; no es una corrección pendiente de semántica size del engine |
| Orden | M1.5: recepción para nuestro estado; no orden global | Import ordena receive/type/sequence y elimina witness [C01] | Forense pide venue-time para «replay físico»; eso sólo puede ser modalidad A, no reproducción del conocimiento del recolector B |
| Tick conocido | M1.3/6: revisión disponible al corte | `Qualities` consulta latest [C04/C05] | Readiness reconoce look-ahead pero llama as-of «quality-model change»; esa clasificación contradice M1 y se corrige aquí |
| Elegibilidad SCREEN | M1.5 y M2-S06/07: book+constraints+mapping+freshness | marketview sólo valida base/cruce/regresión parcial [C03/C06] | Readiness reconoce bypass, pero 30/30 deliveries y cero oportunidades no acreditan elegibilidad causal |
| Replay | G-07: igualdad de reducers/frames/oportunidades y dependencia completa | Digest sólo asset+quality; régimen vacío [C09] | Igualdad 4/4 reportada prueba igualdad de ese digest, no igualdad L2 ni causalidad |
| L2 | M1.5: coincidencia no prueba ausencia de gaps | Snapshot reemplaza, no deja certificado de continuidad del intervalo | Forense llama «cada snapshot certifica la reconstrucción previa»: lectura admisible = concordancia en el extremo observado; no certificación de todo el camino |
| Fee | FBL-012/M1.10: fee del trade no es tarifa universal | Resolver conserva observación, pero consumidor SHADOW usa latest para otro candidato [C05/C07/C14] | Las 256 filas con bps=0 no habilitan fee cero para backtesting ni certificación económica |

M4 `testdata/research-master/certificate.json` declara no-live y pin `66486ac`, con 27 PASS y 5 gates live diferidos. Se leyó su alcance; no se revoca ni edita el artefacto en este shot. **No se ratifica como prueba de causalidad histórica, L2 completo, observabilidad multi-witness o economía real.** D05 identifica además insuficiencia concreta de la prueba G-07 respecto de su cláusula congelada; no es sólo una capacidad nueva fuera del alcance.

### 3. Defectos de implementación demostrados

Las trazas siguientes son deducciones directas de rutas leídas; sólo los tests expresamente indicados se ejecutaron. No se presentan fixtures nuevos como tests ya corridos. P1 denota bloqueo de una certificación causal; no afirma impacto financiero live.

#### D01 · P1 · Lecturas latest del régimen aplicadas a un pasado

**Ruta A:** `histimport.Import` drena Regimes después de admitir todos los eventos; `Qualities` crea Books sobre ese store completo; `AssetConstraintOK(asset)` no recibe corte y `Service.Constraint` selecciona `ORDER BY revision DESC LIMIT 1` junto al flag suspect actual [C01/C04/C05]. Un book seq=1 sin tick se considera usable gracias al tick seq=2 antes de que Books procese seq=2. `TestFutureTickRevisionIsVisibleDuringDrain` exige exactamente `SYNCING→OBSERVED_USABLE→SUSPECT→OBSERVED_USABLE`; pasó en la suite ejecutada [C04].

**Límite del hallazgo A:** `Qualities` devuelve un mapa terminal, usado por `engine historical import`; no emite DeliveryFrames. SCREEN/SHADOW hacen un drenaje similar para descubrir assets, pero sus frames se forman por marketview. Por tanto, «Qualities filtra directamente un tick futuro a un frame» **no está demostrado y no es la ruta real encontrada**. Su diagnóstico temporal interno y cualquier reutilización como elegibilidad son incorrectos.

**Ruta B que sí cruza el corte:** `RunShadow → fillCandidate → shadowFeeResolver → Service.AssetConstraint` lee el store final sin `CutSeq` ni `VirtualTime` [C07]. Una fee observada después de C puede cambiar `FeeInconclusiveFills` y la evidencia económica de un candidato anterior. `FillAt` mantiene notional bruto e ignora el argumento fee: no atribuir a esta ruta un cambio de importe neto que no ejecuta [C14]. Las transiciones suspect de régimen también requieren as-of; filtrar sólo la revisión dejando `e.suspect` actual seguiría contaminando el pasado.

**Clasificación:** `IMPLEMENTATION_DEFECT` frente a M1.3/6/10. Corrección S2; gates H01/H04/H07.

#### D02 · P1 · SCREEN/SHADOW eluden constraints y requisitos de datos

`openScreenPipeline` drena Books con constraints, pero sólo toma `Assets()` y crea proyecciones marketview nuevas. `RunShadow` hace lo mismo. Un snapshot no cruzado recibe `OBSERVED_USABLE` en marketview sin consultar tick, mapping, régimen, continuidad certificada ni edad [C03/C06/C07]. Esto puede ocurrir cuando Books informa `SYNCING`. `DataRequirements` declara `MaxBookAge`, `MaxMetadataAge` y `MinAssets`, pero `Runtime.DeliverFrame/runJob` invoca Detect sin validarlos [C11]. `Sports.Detect` confía en la etiqueta de calidad y en el kickoff de config [C12].

Caso negativo: snapshot y widening sintético, sin tick y con suficiente historia, pueden llegar como señal a Sports; la tarifa unresolved detiene Evaluate, no revierte la señal contada. No se afirma que ocurrió en la cohorte de cero oportunidades. `DepthFresh` sólo compara el timestamp codificado con `LastSourceMs`; ambos se escriben desde el mismo estado, por lo que no demuestra edad, continuidad ni profundidad correcta [C03/C14].

**Clasificación:** `IMPLEMENTATION_DEFECT`, no diferencia deliberada de modo, porque los dos caminos usan la etiqueta congelada de elegibilidad. Una observación descriptiva de BBO puede ser útil sin fee; necesita un resultado explícitamente descriptivo y sus propios requisitos, no ampliar silenciosamente `OBSERVED_USABLE`. S3, H02/H05/H08.

#### D03 · P1 · Gaps, fencing y regresiones no se propagan uniformemente

SCREEN y SHADOW cargan sólo `marketws` + `record_kind=data`; `evidence_gap` vive como control de Capture y queda descartado. `marketview.RecordFacts` no tiene control, autor de conexión ni boot; ningún gap llega al estado que Strategy ve [C06/C07/C03]. Books sí revoca epochs ante `evidence_gap`, por lo que las rutas divergen [C02].

Además, ambos reducers comprueban regresión de source time en `book`, pero no antes de aplicar `price_change`. Books ni siquiera avanza `LastSourceMs` al aplicar ese delta; marketview lo reemplaza, incluso hacia atrás. Traza: snapshot venue=12:02, delta venue=12:00 recibido=12:08 que deja book no cruzado → nivel sobrescrito sin `SUSPECT` por regresión. No es necesariamente look-ahead a las 12:03; es un estado inválido usado desde las 12:08.

Fencing incompleto: Books guarda `EpochAuthor`, pero `deltaAppliable` sólo compara número de epoch; marketview no conoce conexión. Un snapshot puede cambiar epoch a uno anterior si pasa el control de tiempo. Books, tras `EpochRevoked`, acepta snapshot del mismo epoch y lo rehabilita, aunque M1 exige epoch nuevo después de gap. Un delta del nuevo epoch sin base se ignora sin degradar necesariamente la calidad del book viejo. `marketview` puede seguir mutando niveles en `SUSPECT`; Books limita deltas a usable/syncing. Las pruebas actuales de handover y gap no cubren retorno a epoch viejo ni snapshot recuperador del mismo epoch [C02/C03].

**Clasificación:** `IMPLEMENTATION_DEFECT` M1.5/M2-S06. No implica que se puedan detectar todos los deltas perdidos del proveedor. S3/S4; H03/H05/H06.

#### D04 · P1 · Importación pierde identidad de recolector y desempata contra su orden

`Event` conserva `ReceivedUs`, `TimestampMs` y `Sequence`, pero no `source_witness`, boot, conexión, ordinal raw, publicación ni fuente/hash del registro original. Cada admisión usa `connectionID=histimport`, `epoch=1`; sequence sólo sirve para ordenar y no se serializa en el payload generado [C01]. El journal da durabilidad a la representación importada, no recupera la procedencia descartada.

`prepare` compara `(ReceivedUs, rank(EventType), Sequence, AssetID+AssetHex)`. A mismo receive time, un delta seq=10 anterior al primer snapshot seq=11 se reordena después del snapshot y pasa a aplicarse sobre una base que no existía cuando llegó. Incluso dentro de un solo recolector contradice M1.5. Dos deltas distintos con la misma clave completa conservan orden de entrada por `SliceStable`; invertir archivos puede invertir el estado. No hay política de conflicto para esa colisión. `best_bid_ask` tampoco es un tipo importable, aunque el parser/Books conozca esa observación; la corroboración forense independiente no entra por este adapter.

**Clasificación:** orden/fencing perdidos = `IMPLEMENTATION_DEFECT` del adapter existente. Definir observador, reloj y política multi-witness = `CONTRACT_AMBIGUITY` histórica; no defecto por haber diferido backfill en M1. S1; H01/H03/H10.

#### D05 · P1 · Replay puede pasar sin comparar el estado que afirma certificar

`RunObservation` crea Books con constraints nil. `replayRegimesReducer.drain` cuenta registros, no ejecuta Regimes; `digest()` retorna string vacío. `digestObservation` sólo hashea lista de asset IDs y etiquetas de calidad: no niveles, tick, timestamps, revisiones ni bytes del stream. Cambiar size=10 a size=100 con misma calidad deja el digest igual. `replayBooksReader.batchFn` está almacenado pero no se usa para leer Books; variar schedule no varía su batch real [C09].

`RunDelivery` acepta refs con hash no vacío sin resolver contenido/localizador; `clock` y slots reservados tienen excepciones. Un hash ficticio de régimen no vacío puede ser `RESOLVED`. No comprueba presencia de resultado completo por delivery. El replay de Strategy reejecuta frames ya entregados dos veces, lo cual comprueba repetición sobre esos inputs, no causalidad de su creación. Indexa observaciones por ordinal sin aislar run/instance, lee hasta frontier actual y devuelve `Deterministic=true` si no encuentra frames [C10]. Una run nueva sin frames no demuestra reproducción exitosa. Los controles de integridad deben revisar `VerifyReport.IntegrityFailures()`, no sólo error de llamada; `BuildManifest` sí hace esa distinción [C09/C10].

**Clasificación:** `IMPLEMENTATION_DEFECT` contra M1.6/G-07/G-07b. Los digests históricos quedan como evidencia limitada preservada, no se recalculan para aparentar continuidad. S5; H07/H09/H10.

#### D06 · P1 · Repetición válida de un régimen se elimina como duplicado

`upsertRegimeRevision` busca el hash en **toda** la historia. Si lo vio alguna vez, sólo actualiza `last_observed_at`, sin mover el estado actual; `UNIQUE(entity_id,content_hash)` lo refuerza [C05]. Para tick 0.01 → 0.001 → 0.01, el tercero no crea revisión y el servicio mantiene 0.001. Un reingreso del mismo hecho puede ser idempotente, pero observar nuevamente un contenido después de otro contenido es una transición nueva. También afecta reglas de reconstrucción as-of y reinicios.

**Clasificación:** `IMPLEMENTATION_DEFECT` M1.3/4/M2-S05. S2; H04. Recuperar la transición perdida requiere reconstruir desde raw; migrar sólo filas existentes no basta.

#### D07 · P1 · Corte incompleto, vector falso y política de muestreo retrospectiva

`buildRevisionVector` selecciona la primera revisión de owner y la guarda bajo `regime`. En las rutas inspeccionadas esa revisión pertenece a marketview y su hash es de niveles. No representa tick/min-size/fee ni a los demás assets; faltan dependencias M1.6 requeridas o una declaración explícita de no uso [C08]. Las barreras pueden ser correctas para owners registrados y aun así el frame no ser un estado completo del engine.

`loadJournal` expande un record en N routings por asset; `routeNext(n)` y SHADOW cortan por número de routings. Si el límite cae después del primer asset de un record seq=C, el frame se construye con C aunque al otro asset todavía le falta su parte del mismo record. M1/FBL-008 prohíbe omisiones ≤C. El test existente de fan-out valida dos llamadas seguidas, no una barrera entre ellas.

SCREEN calcula batch a partir de `len(routed)/cuts`; SHADOW fija el número de frames con `Seed%1000+3`. Añadir un sufijo cambia los instantes de frames del prefijo; los cortes SCREEN=30 y SHADOW=920 de los informes no son el mismo experimento de señales. Asimismo, los owners provienen de `Assets()` del dataset completo; declarar ese universo ex ante puede ser válido, pero descubrirlo del futuro y llamarlo universo point-in-time no lo es [C06/C07].

**Clasificación:** vector y fan-out = `IMPLEMENTATION_DEFECT`; grid/selección global = `CONTRACT_AMBIGUITY` si son muestreo retrospectivo declarado, defecto si se certifican como decisión online causal. S4/S5; H06/H07/H08/H10.

#### D08 · P1 · Disponibilidad de metadata no se impone en la frontera genérica

`external.Admit` usa `time.Now`, rechaza reference time futuro, pero no compara `AvailableAt` con now; si falta disponibilidad la sustituye por reference time. `Project` sólo filtra `CaptureSeq<=C`, y no entrega `AvailableAt` a Strategy [C13]. Un hecho con reference time antiguo y publicación futura puede admitirse ahora y proyectarse sin esa barrera. Un forecast conocido hoy para mañana demuestra además que reference time futuro no es por sí mismo look-ahead: se debe diferenciar tiempo objetivo y publicación.

Sports acepta `kickoff_ms` fijo sin registro de quién lo conoció ni cuándo; la puerta pre-match usa directamente ese valor. Un schedule revisado después podría alterar señales antiguas si el operador lo pasa como parámetro histórico. No se demuestra que el kickoff concreto de la cohorte haya cambiado: su disponibilidad histórica sigue `UNVERIFIED` [C12]. La protección particular de un consumidor externo no sustituye un contrato genérico y Sports no pasa por ese consumidor.

**Clasificación:** publicación futura no filtrada = `IMPLEMENTATION_DEFECT`; admisión de metadata histórica corregida/parametrizada = `CONTRACT_AMBIGUITY`. S1/S2/S4; H01/H04/H10.

### 4. Ambigüedades y cambios M1 necesarios

| ID | Clasificación | Decisión o precisión necesaria | Propuesta acotada |
|---|---|---|---|
| A1 | `CONTRACT_AMBIGUITY` | Quién observa el archivo histórico: recolector original, agregador o consumidor del archive | Declarar `observer_id`, clock domain y evidencia de recepción/publicación por fuente. El primer timestamp de cualquier witness no es disponibilidad de todos |
| A2 | `M1_CHANGE_REQUIRED` si se habilita A | M1.5/M2-S06 prohíben ordenar venue-time; el objetivo descriptivo idealizado lo puede necesitar | Addendum opt-in de reconstrucción idealizada como contrafactual M1.6, con certificado distinto. Mantener B fail-closed por defecto. No modificar M1 congelado en este shot |
| A3 | `CONTRACT_AMBIGUITY` | Evidencia retrospectiva de valor versus disponibilidad histórica | Separar `valid/event time`, `knowledge time`, `evidence_acquired_at` y estado de prueba. No fabricar un tick_size_change anterior |
| A4 | `M1_CHANGE_REQUIRED` si se amplía elegibilidad | BBO útil sin L2/tick íntegros no tiene etiqueta independiente en M1.5 | Extensión aditiva de perfil BBO descriptivo, sin reusar `OBSERVED_USABLE` y sin fills. Requiere aprobación sólo para nuevas oportunidades que hoy M1 rechaza; medir spreads con `describe` ya está permitido |
| A5 | `CONTRACT_AMBIGUITY` | Umbrales de freshness/regresión, empate intra-ms, censura post hoc y snapshots de recovery del archivo | Política preregistrada, scoped al experimento; unknown no hereda precisión ni SLA. No se fijan tolerancias productivas universales |
| A6 | `CONTRACT_AMBIGUITY` | Grid `cuts=30` define cantidad, no instantes causales ni paridad con SHADOW | Persistir lista/política de cortes estable al prefijo; recalificar corridas anteriores como muestreo retrospectivo cuando corresponda |

`TIME_TO_VALIDATED_HYPOTHESIS` exige fallar con un motivo accionable y un nivel de evidencia: fenómeno medible aunque economía no lo esté; reproducibilidad por corte; una sola corrección de calidad para todos los consumidores; denominadores/censuras recuperables; resultados `INCONCLUSIVE` ante dato/modelo insuficiente. No exige feeds perfectos, reconstruir queue ni calibrar maker en esta corrección. Arreglar D01–D08 no depende de aprobar fee cero, comprar datos o reabrir OOS.

### 5. Matriz M1 y causalidad por componente

| Contrato | Diseño M1 | Implementación | Evidencia | Clasificación |
|---|---|---|---|---|
| Capture durable-before-publish | fsync antes de frontier; source y receive distintos | Se cumple en la mecánica inspeccionada; no existe timestamp de persistencia por record | M1.6; C15 | `M1_COMPLIANT` para durabilidad local; latencia histórica fsync `UNVERIFIED` |
| Histórico/witness | Sin secuencia remota global; bootstrap no inventado | Conexión/epoch únicos y pérdida de sequence/witness | M1.3/5; C01 | `IMPLEMENTATION_DEFECT` D04; extensión multi-witness `CONTRACT_AMBIGUITY` |
| Books: snapshot/delta/asset | Replace, set-size, cero delete, asset aislado | Equivalentes semánticos del forense; snapshots actuales reemplazan | M1.5; C02/C03; F01 | `M1_COMPLIANT` en operaciones de nivel |
| Books: continuidad/orden | Gap→epoch nuevo; no regresión silenciosa | Controles omitidos en delivery; old epoch/late delta insuficientemente cercados | M1.5/G-05; C02/C03/C06/C07 | `IMPLEMENTATION_DEFECT` D03 |
| Regimes por corte | Known-at, revisiones e invalidación | API latest, suspect mutable actual, A→B→A pierde transición | M1.3/4/6; C04/C05 | `IMPLEMENTATION_DEFECT` D01/D06 |
| Frames | Barrera por record completo; dependencias completas | Barreras locales presentes; fan-out divisible y vector con hash de un book bajo regime | FBL-008; M1.6; C08/C06 | `IMPLEMENTATION_DEFECT` D07 |
| SCREEN | Misma Strategy y requisitos de calidad | marketview ignora régimen; runtime no hace cumplir edades | M1.5/8; C03/C06/C11/C12 | `IMPLEMENTATION_DEFECT` D02 |
| SHADOW | Mismos inputs elegibles + ejecución sintética separada | Comparte marketview, hereda bypass/gaps, fee latest; grid distinto | M1.8/9/10; C07 | `IMPLEMENTATION_DEFECT` D01/D02/D03; grid A6 |
| Replay de observación | Mismos reducers y estados completos | Calidad-only digest; Regimes no ejecutado | M1.6/G-07; C09 | `IMPLEMENTATION_DEFECT` D05 |
| Replay de decisiones | Inputs por fase resolubles; outputs completos | Comprobación superficial de refs y reejecución de frames dados | FBL-004; C09/C10 | `IMPLEMENTATION_DEFECT` D05/D07 |
| Metadata externa | Disponible al corte, versiones conocidas | seq sí; AvailableAt no; config kickoff sin provenance | M1.3/6; C12/C13 | `IMPLEMENTATION_DEFECT` D08; admisión retrospectiva A3 |
| Economics | No fee universal de trade; costes con régimen aplicable | Fórmulas no auditadas ni modificadas; consumer lee fee latest | M1.10/FBL-012; C05/C07/C14 | `IMPLEMENTATION_DEFECT` temporal; corrección económica V2 fuera de alcance |
| Simulator | Depth al tiempo de llegada; queue/touch no prueban fill | Recibe book del caller; FillAt no selecciona estado temporal; SHADOW pasa book del frame y delays cero | M1.9; C07/C14 | `UNVERIFIED` ejecución histórica con latencia; modelo cero-latencia sólo supuesto explícito |
| BBO/L2 histórico | Best-effort no lossless | Sin cadena de certificación fina por intervalo | M1.5; F01 | `UNVERIFIED`; perfil descriptivo A4 |
| Backfill/Parquet | Adapter/optimización diferidos, contrato estable | Import agregado después de M4 | M1.15/M2-S06/S08 | Ausencia inicial `M1_COMPLIANT`; modalidad A `M1_CHANGE_REQUIRED` |
| Live/maker/OOS | Gates separados | No ejecutados en este shot | M1.15; mandato | `UNVERIFIED`; no habilitados |

### 6. Contrato formal: event time y knowledge time

Para cada hecho `f`, conservar `E(f)` (tiempo atribuido por la fuente), `R_s(f)` (recepción en el observador s), `P(f)` (publicación cuando importa), `I(f)` (admisión/importación actual), `A(f)` (momento de adquirir evidencia para auditoría), fuente/clock domain/precisión y referencias raw. No son intercambiables. `K_m,s(f)` es el primer instante en que el observador de la modalidad m puede usar el hecho bajo su protocolo. Si se dispone de límites de incertidumbre, usar intervalos; una comparación no demostrable no pasa la elegibilidad requerida.

Para un frame F en corte C y tiempo T:

```text
visible(f,F) = f pertenece al manifest y a la procedencia autorizada
               AND f fue admitido en el prefijo completo <= C
               AND K_mode,observer(f) <= T es demostrable según la política
               AND la revisión no fue reemplazada antes de C

Decision(F) = Strategy(prefixo_de_deliveries_completas, F, inputs_por_fase_pineados)

prefix_noninterference:
  con protocolo, cortes, seed, build y estado inicial idénticos,
  agregar/modificar hechos cuyo K > T no cambia frames/decisiones <= T.
```

La vigencia E/valid-time anterior **no elimina** la condición K≤T. Para observaciones de estado, el valor consultado debe ser el último admisible en esa frontera, no necesariamente el de mayor event time global. Una anomalía de orden puede bloquear esa proyección; no se corrige reordenando decisiones.

| Reloj/secuencia real | Existe | Garantía y límite |
|---|---|---|
| Timestamp venue | `TimestampMs` y payload raw; SourceTime en envelope | Precisión declarada ms para estos eventos; no orden intra-ms ni sincronía con otros relojes. Payload conserva lexema; `SourceTimeRaw` en Capture contiene instante normalizado, no siempre el lexema original |
| Recepción del archivo | `ReceivedUs` → FakeClock → `ReceivedWall` | µs de representación, no exactitud física. Mezclar relojes sin witness es ambiguo |
| Monotónico local | `ReceivedMonoOffsetNs`, boot | Nativo sólo comparable dentro del boot. En histimport se sintetiza por diferencias de ReceivedUs; no mide latencia física histórica |
| Sequence recolector | `Event.Sequence` antes de Import | Local al recolector; se pierde en payload generado. No convertir diferencia de números en conteo de pérdidas global |
| Secuencia journal | `CaptureSeq`; frontier `DurableSeq` | Orden total local de admisión; durable_seq avanza post-fsync. No es orden del exchange ni mismo espacio que sequence recolector |
| Persistencia | Ack/frontera/locators | No `persisted_at` histórico por evento. No se puede reproducir latencia de commit original ni decir que recepción=fsync |
| Frames/decisiones | CutSeq, ordinal, VirtualTime, RequestedAt/CompletedAt; records runtime | ReceiveClock avanza con records routed; no es reloj venue. Ordinal es por run; cutoff solo no garantiza inputs correctos. Timestamp de runtime grabado hoy no representa la hora histórica de decisión |
| Metadata | Regimes known_at/observed_at, CaptureRef; External AvailableAt/KnownAt | Parte de la evidencia existe, los lectores no la limitan correctamente. Kickoff parametrizado carece de estas garantías |

**Modalidad B — perspectiva causal del sistema/recolector.** Es la correspondiente al objetivo de PE-005-R1 de detectar una señal pre-match que un sistema podía observar y luego evaluar ejecución. Usar una fuente/witness seleccionado, recepción y publicación probadas, más latencias explícitas. Para el recolector directo, P puede ser una restricción de precedencia sin un reloj comparable; no calcular `max` de relojes incompatibles. Para un consumidor del archive, la hora de publicación del archivo sí importa. Cuando los tiempos están en un dominio calibrado, `K_B=max(recepción, publicación aplicable)+pipeline_delay_model`. La fecha en que hoy se descargó el archivo no es por defecto K de un recolector histórico; tampoco se puede fingir que un consumidor del archive lo vio antes de publicarse.

B se selecciona por defecto para certificar señal causal, **pero queda bloqueada donde falte evidencia requerida**. No requiere que todos los experimentos usen la latencia del recolector original: un contrafactual puede usar otra latencia explícita con su propio manifest. El perfil mínimo de B puede modelar disponibilidad a recepción con procesamiento cero declarado y conservar la durabilidad actual; no puede llamarse replay exacto de la latencia histórica del engine.

**Modalidad A — reconstrucción idealizada del mercado.** Puede servir para estudiar si existió ensanchamiento/reversión bajo observabilidad ideal. Orden por E con política de empate, cobertura y latencia modelada; `K_A` es disponibilidad **asumida**, por ejemplo E+latencia declarada, nunca un timestamp observado inventado. Debe rechazarse un supuesto imposible de disponibilidad anterior a existencia/publicación del hecho. El resultado es `IDEALIZED_MARKET_RECONSTRUCTION`/contrafactual, no `COLLECTOR_CAUSAL_PASS`. No es el certificado de ejecución de PE-005-R1; puede ser su estudio descriptivo precursor. Implementación de A deshabilitada hasta la decisión §12; no cambiar el orden de B para hacer calzar snapshots.

**Caso obligatorio 12:00 / 12:08 / 12:03:**

| Pregunta | B, recepción real 12:08 | A, observabilidad ideal declarada |
|---|---|---|
| ¿Integra el libro reconstruido? | Puede integrar una proyección desde 12:08 si sigue siendo orden/epoch admisible; si es stale frente a la base actual, se conserva raw y bloquea/diagnostica, no sobrescribe sin control | Puede integrar el libro event-time de 12:00 si provenance/orden/calidad lo permiten |
| ¿Lo usa Strategy a las 12:03? | No; K_B=12:08 o después | Sólo si K_A≤12:03 por supuesto explícito. No acredita conocimiento del recolector |
| ¿Reescribe una decisión de 12:03? | Nunca | Nunca en la misma run. Una revisión de datos produce otra run derivada |
| ¿Puede reparar una vista histórica? | Sí, como revisión de auditoría/reconstrucción separada; no como input retroactivo de esa decisión | Sí en una nueva versión de dataset/run, con lineage y diferencia respecto del resultado anterior |

Dos recolectores con orden distinto producen dos perspectivas B potencialmente distintas. No exigir igualdad entre ellas. Exigir igualdad de cada perspectiva bajo distintos schedules de cómputo que conservan su orden lógico. Un merge autorizado debe tener un observador agregador y reglas verificables; no elegir `min(received)` entre witnesses retrospectivamente. Empates del mismo flujo respetan ordinal/sequence local; empates cross-source sin orden probado se censuran si afectan el resultado o se declaran orden convencional en A. El hash como desempate puede hacer la ejecución determinista, pero no demuestra causalidad remota.

### 7. Admisión de datos retrospectivos y bootstrap

| Categoría | Admisión a decisión B | Uso en auditoría/A | Evidencia requerida |
|---|---|---|---|
| 1. Hecho existente y conocido históricamente | Sí desde su K probado, con revision/valid interval y prefix constraint | Sí | Captura anterior, publicación archivada auténtica o registro de observabilidad aplicable al observador; bytes y fuente |
| 2. Hecho existente cuya veracidad se certifica después | Sí únicamente si además se demuestra que ese valor era accesible al observador en T; adquirir la prueba después no es look-ahead por sí mismo | Puede validar un valor/intervalo pasado, conservando A(f) posterior; si disponibilidad no probada, sólo auditoría/A con supuesto | Prueba de valor y prueba de disponibilidad separadas; cobertura de revisiones; no inferir continuidad perfecta de ausencia de eventos en archivo incompleto |
| 3. Hecho/revisión que no existía en T | No antes de publicación/recepción de esa revisión | Etiqueta de resultado o corrección posterior; no predictor pasado | Append de revisión, supersedes, tiempos de publicación/conocimiento y alcance temporal |

Reglas por campo:

- **Tick inicial:** `old_tick_size` de un cambio posterior evidencia el valor inmediatamente anterior a ese cambio. Extenderlo hasta el inicio de la ventana exige continuidad de cambios o fuente adicional que establezca ese intervalo. El scan de 367 horas y cero cambios intermedios es evidencia reportada, pero un archive con gaps no vuelve infalible la inferencia. Puede certificar retrospectivamente un tick viejo si la cadena lo demuestra; para B, probar además que era observable históricamente. Registrar una ancla de bootstrap con `evidence_acquired_at` posterior y fundamento; no falsificar un evento WS anterior. El `new_tick_size` posterior jamás se aplica a frames viejos.
- **Kickoff:** separar schedule publicado, revisiones del schedule y hora efectiva de comienzo. Una consulta actual a CLOB/MLB corrobora un valor; no demuestra por sí sola qué schedule se conocía al decidir. Una captura obtenida hoy que preserve un documento publicado antes puede servir categoría 2. En B usar la revisión de schedule conocida entonces; en A puede fijarse un anchor retrospectivo con disclosure. No seleccionar sólo mercados cuyo schedule terminó cumpliéndose sin declararlo.
- **Rules, mapping, membership y universo:** publicar versiones por source/known time. La verdad final de reglas o relaciones no rellena lo desconocido en T. Un universo exploratorio seleccionado ex post puede medir una cohorte declarada, pero no certifica discovery ni representatividad histórica; contabilizar disponibilidad/selección y no usar winners como filtro oculto.
- **Fees:** conservar alcance de la observación (trade, rol, asset, período y unidades). Las 256 operaciones con `fee_rate_bps=0` no autorizan fee cero del siguiente trade, ni identifican necesariamente importe efectivo sin mapping contractual. No implementar ni aprobar esa extrapolación. La economía V2 permanece intacta y no certificada.
- **Resolución:** payoff/resolved/finality se conocen cuando llegan sus observaciones. Pueden ser labels posteriores para evaluación con horizonte y censura definidos, nunca features anteriores. Revisiones o disputes no reescriben decisiones.
- **Bootstrap histórico:** reconstruir prefijo anterior o usar checkpoint probado con frontera, dependencias y máximo K; Strategy empieza después del warm-up declarado. No cargar todas las revisiones de `engine.db` como si existieran al inicio. Un checkpoint con fact posterior al primer corte falla, aunque su effective_from sea antiguo.
- **Selección y censura retrospectivas:** la auditoría puede descubrir después que un intervalo era malo. Guardar decisiones originales, resultado bruto, resultado censurado, causa/intervalo/fuente/`detected_at`/`evidence_acquired_at`, protocolo y denominadores. La censura no puede transformarse retroactivamente en lo que la estrategia supuestamente sabía. Reglas elegidas después de mirar alpha requieren nueva revisión del experimento, no PASS del original.

### 8. Gates BBO/L2 y alcance del backtest

Un snapshot posterior tiene dos usos distintos: **(a)** reemplaza/repara el estado hacia adelante desde su disponibilidad cuando autor/epoch/base son admisibles; **(b)** sirve de referencia posterior para comparar el extremo del intervalo anterior. No reconstruye deltas perdidos ni prueba cada estado intermedio. Dos deltas ausentes compensatorios pueden dejar el mismo snapshot final y haber alterado el BBO durante el intervalo. La cifra ~92% de extremos con profundidad idéntica no es «92% del tiempo L2 lossless».

| Nivel de uso | Gate mínimo | Resultado si falta |
|---|---|---|
| Diagnóstico de datos | Identidad, unidades, tiempos raw y procedencia; anomalías conservadas | Quarantine/UNVERIFIED, nunca valor cero sustituto |
| Spread BBO descriptivo | BBO no cruzado/no vacío, as-of bajo modalidad explícita, frescura y soporte de BBO; referencias de corroboración con su instante de detección | `BBO_UNVERIFIED` o intervalo censurado; fee no necesaria |
| Señal causal BBO | Gate anterior + K≤T de todo input, schedule/reglas/universo requeridos, prefijo de historia válido, protocolo/cortes preregistrados | `SIGNAL_INELIGIBLE` con motivo. Default M1 conserva tick/constraints; perfil más débil requiere A4 |
| Reversión observable | Señal admisible + observaciones posteriores dentro de horizonte exacto, sin gap incompatible; denominador censurado | `REVERSION_UNOBSERVABLE`; no reemplazar por la primera cotización posterior a un gap |
| Ejecución hipotética | Candidato/modelo explícitos, tick/min-size/reglas y latencia/política de fill declarados | `EXECUTION_UNCERTIFIED`; puede continuar descripción |
| Fills L2 | Estado observado en el instante simulado de llegada, continuidad suficiente para el perfil, tamaños/asset/side/epoch/truncation válidos y ledger aislado | No fill base certificado. Snapshot-only puede permitir evaluación puntual bajo supuesto; touch es sólo upper bound declarado |
| Economía neta | Fill admitido + fee/costes aplicables, versión V2 y unidades verificadas | `ECONOMICS_UNCERTIFIED`, jamás fee cero implícita |
| OOS/hipótesis validada | Protocolo/split sellados y gates previos, ejecución autorizada aparte | `NOT_RUN`; OOS permanece cerrado |

BBO independientemente corroborado puede seguir siendo útil aunque tamaños L2 no lo sean; no elevarlo a continuidad total ni descartar automáticamente todo BBO por drift de profundidad. Una observación `best_bid_ask` prueba precios en su instante y bajo su procedencia, no tamaños ni FIFO. Su acuerdo agregado no es una máscara por intervalo ya implementada en el engine.

En `SYNCING` o `SUSPECT`, conservar raw/diagnóstico; bloquear oportunidades ejecutables y fills. La historia/pending de la estrategia no debe puentear un intervalo inválido como si fuera continuo: cerrar/censurar el episodio o esperar nuevo warm-up según protocolo. `Sports.Detect` hoy hace `continue` y conserva historia; ese detalle requiere H05. Además `resolvePending` compara breakeven antes de comprobar expiración: un BID favorable que aparece por primera vez después de `window_ms` puede contarse como reversión [C12]. El gate H05 debe impedir esa falsa atribución; se corrige el orden de checks y la censura, sin cambiar umbrales ni modelo económico.

Por tanto, **un intervalo con tamaños aparentemente correctos pero continuidad insuficiente no admite fills certificados**. Puede alimentar un escenario explícitamente acotado/UNCALIBRATED sólo si la política aprobada lo permite; la corrección mínima puede bloquearlo. No existe prueba absoluta de ausencia de pérdidas usando sólo este feed; el certificado debe decir «causal bajo observabilidad y calidad declaradas», nunca «mercado completo conocido».

`Sports.Detect` ya separa ensanchamientos de fee; `Evaluate` devuelve `FEE_UNRESOLVED`. Eso es útil y no debe endurecerse hasta exigir fee para medir spreads. Su métrica `reverted` actual depende del breakeven calculado en Evaluate; sin fee no puede presentarse como reversión económica. Si se desea una reversión puramente de spread, definirla como estimando descriptivo separado y someterlo al owner, no reinterpretar el contador existente.

## Fuentes

Autoridad documental: [[Polymarket Engine — MVP]] §§M1.3–M1.10, M1.15, FBL-004/008/012, ASTRA-2, ASTRA-3, M2-S05…S10/S13; [[Research — Technical Platform Map M0]] y [[Polymarket — Technical Platform Map — synced 2026-09-17]], partes 03/05/07/10; [[2026-09-21-historical-research-m0]], [[2026-09-21-historical-backtest-readiness]], [[Polymarket Engine — Continuidad Five-POC 2026-09-20]] §§15–16; addendum y forense enlazados arriba. Los informes previos se conservan como historia; esta auditoría no modifica M1.

Todas las referencias Cxx siguientes corresponden a archivos leídos físicamente de `xKoRx/polymarket-engine` en **09e8c7610f29a35f8080122b7cb4219b9866ebd7**. Rangos de línea identifican evidencia, no cambios propuestos.

| ID | Archivo y líneas de evidencia |
|---|---|
| C01 | `internal/histimport/import.go:28–56,132–175,214–217,235–291,302–342`; import schema, reloj, epoch, tipos y sort |
| C02 | `internal/books/reducer.go:43–48,256–273,330–469,474–498`; `internal/books/books.go:6–29`; replace/upsert, quality, gap, author y epoch |
| C03 | `internal/marketview/projection.go:37–75,80–109,133–223,231–282`; proyección compartida sin régimen/control, deltas y provenance de depth |
| C04 | `internal/histimport/quality.go:13–42,66–74`; `internal/histimport/anchor_test.go:92–150`; `cmd/engine/historical.go:46–59`; consumidor terminal y test de look-ahead |
| C05 | `internal/regimes/service.go:30–120`; `internal/regimes/reducer.go:502–520,646–711,764–777`; `migrations/0021_regime_revisions.sql:8–27`; latest, known_at, dedup histórico y suspect |
| C06 | `cmd/engine/screen.go:198–241,262–365,379–425,510–516`; Books→owners→marketview, filtros y batches |
| C07 | `internal/experiment/experiment.go:225–245,267–305,366–438,822–831,863–903`; SHADOW, cortes, fee latest y fills |
| C08 | `internal/frames/frames.go:68–99`; `internal/frames/dispatcher.go:374–401,429–445,498–557,585–601`; `internal/frames/receive_clock.go:10–40`; `internal/frames/dispatcher_fanout_test.go:13–46` |
| C09 | `internal/replay/replay.go:123–175,179–210,222–279,299–375`; `internal/replay/manifest.go:33–50,81–105`; digest, schedule, resolución y cutoff |
| C10 | `internal/experiment/strategy_replay.go:63–111,113–223`; lectura de frames, aislamiento de observaciones y comparación de outputs |
| C11 | `internal/strategy/api.go:35–52,84–96`; `internal/strategy/runtime.go:149–184,297–357`; requisitos declarados y callbacks |
| C12 | `internal/strategy/pocs/sports/sports.go:120–173,203–204,220–282,291–313,317–352,447–480`; kickoff, historia, reversión, calidad y fee |
| C13 | `internal/external/external.go:44–73,78–116,135–171,175–209`; publicación, known_at y filtro por seq |
| C14 | `internal/strategy/pocs/pocdata/pocdata.go:119–125`; `internal/simulator/simulator.go:91–105,128–188,193–246`; `internal/regimes/feeresolver.go:199–257`; profundidad, llegada, gross y fee de trade |
| C15 | `internal/capture/envelope.go:193–227`; `internal/capture/capture.go:396–455`; `internal/capture/writer.go:193–204`; frontera durable y tiempos |
| C16 | `testdata/research-master/certificate.json:1–18,242–260,524–544,636`; certificado existente; suites vigentes inspeccionadas bajo los seis paquetes del comando de §1 |
| F01 | Workspace forense registrado en [[Research — Historical L2 Forensic Validation 2026-09-21]], `hist-l2-forensic-20260922/scripts/recon.py` funciones `recon/analyze/apply_price_change`, `bba_check.py`, `cut_states.py`; código leído, datos y cifras no reejecutados |
