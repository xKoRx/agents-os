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

#### D09 · P2 · Horizonte y episodios de Sports atraviesan observaciones inválidas

En `Sports.Detect`, un asset no usable se omite sin terminar historia ni pending. Al recuperar datos, el contador puede comparar contra historia anterior al gap. En `resolvePending`, comprobar `bid>=breakeven` antes de `now-signal>=window` permite contar como revertida una señal cuyo primer BID favorable llegó fuera del horizonte [C12]. La combinación no necesita un fallo de economía: basta una señal con breakeven ya calculado y un frame posterior tardío. Es un defecto de atribución temporal frente a M1.6/9 y al `window_ms` del experimento, no evidencia de alpha. Corrección S6; H05. La igualdad exacta al límite requiere la convención de intervalo preregistrada; el contraejemplo estrictamente posterior falla bajo cualquiera de las convenciones razonables.

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

Decision(F) = Strategy(prefijo_de_deliveries_completas, F, inputs_por_fase_pineados)

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

### 9. SPEC correctiva mínima — HCA-1: frontera de entrega causal

**Unidad de entrega:** una corrección integrada HCA-1 del camino histórico de observación/entrega. No construir otra arquitectura, Strategy API, base de datos analítica, simulador o replay paralelo. Reutilizar Capture, reducers propietarios, Frames, runtime, Economics V2 y Simulator. Las seis partes siguientes son dependencias de esa corrección, no proyectos independientes. La implementación puede rechazar de manera explícita capacidades cuyo contrato/datos no alcanza; no tiene que fabricar metadatos, resolver el feed remoto ni habilitar A.

**Invariante común:** todo input efectivo de una decisión tiene bytes recuperables, identidad y disponibilidad autorizada al corte; todo estado inelegible llega con motivo; cambiar un sufijo futuro no cambia el prefijo. Un dato posterior sólo puede cambiar el estado posterior y una anotación de auditoría versionada. El certificado debe declarar modalidad/observador/calidad/latencias y fase exacta certificada.

#### S1. Contrato de importación histórica y procedencia

- **Contratos/owner:** M1.3/5/6; `internal/histimport`, `internal/replay` manifests y composición CLI; usar Capture sin reescribir journals.
- **Actual/evidencia física:** D04/C01; Event no conserva witness, usa epoch constante, sort por tipo antes de sequence y pierde independencia BBO. D08/C13 admite disponibilidad futura.
- **Requerido:** formato histórico v2 con referencia durable al source original, `observer_id`, `source_witness`, `source_boot/connection/epoch` cuando existan, sequence local y ordinal del registro/elemento, raw E/R/unidades/precisión, publicación opcional con estado conocido/desconocido, hash de archivo/fila o locator verificable. Campos ausentes = unknown, nunca rellenarlos con una identidad real inventada. Mantener dos hechos separados: recepción histórica y fecha de importación. Una sidecar de provenance hash-pineada puede evitar cambiar el envelope Capture, siempre que cada record resuelva inequívocamente su fuente.
- **Orden:** preservar orden probado del flujo seleccionado; con receive timestamps iguales usar sequence/ordinal local antes de cualquier criterio convencional. Si recepción y sequence se contradicen, registrar anomalía/clock uncertainty y rechazar certificación estricta hasta política; nunca escoger en silencio. No comparar sequence entre witnesses. Un dataset multi-witness sin observador/order policy aprobado se admite sólo como diagnóstico `PROVENANCE_INSUFFICIENT`, sin Strategy causal. Conservar `best_bid_ask` como observación de BBO, no update de depth.
- **Versionado/compatibilidad:** journals v1 siguen legibles y sus bytes/digests originales se conservan. Manifest `historical_temporal_contract=v2` pinea import/provenance/clock/order/cuts; manifests sin él son `LEGACY_CAUSALITY_UNVERIFIED`. Un binding nuevo puede recuperar provenance desde original hash-verificado, pero crea manifest/run nuevos, no altera capture_seq antiguo ni inventa pérdidas. Modalidad ausente → B estricta bloqueada cuando no cumpla; A no se activa por inferencia.
- **Positivos:** flujo de un witness con timestamps empatados conserva delta-antes-de-base; lectura en archivos distintos con identidad inequívoca entrega mismo journal lógico; evento late conserva E y R diferentes; BBA se conserva como evidencia.
- **Negativos:** dos payloads distintos con misma identidad; merge de clocks no calibrados; missing receive/domain; cambio de orden de archivo con colisión; source posterior presentado como histórico. Todos rechazan/censuran sin falso PASS.
- **Gate/evidencia nueva:** H01/H03/H10; manifest v2 + tabla canonical de registros admitidos/rechazados y hashes de fixture. No se requiere recodificar todo raw v1 ni descargar datos.

#### S2. Regimes y metadata conocidos al corte

- **Contratos/owner:** M1.3/4/6/10; `internal/regimes`, `internal/persist` migraciones forward-only; `internal/external` para sus tiempos; wiring histimport/experiment.
- **Actual/evidencia física:** D01/D06/D08; C04/C05/C07/C13 y test `TestFutureTickRevisionIsVisibleDuringDrain` ejecutado PASS.
- **Requerido:** lectura histórica explícita por `(asset/entity, cut_seq, virtual_time, temporal_policy)` o equivalente mediante store aislado limitado estrictamente al prefijo. Reutilizar el reducer de Regimes sobre el journal; nunca consumir el `engine.db` final de otra run como estado causal. Tick, min-size, flags/suspect, fee observations, reglas y resolución deben resolver la revisión conocida en C. Un lector current sólo es válido si su store probado no contiene hechos posteriores a C. Registrar esa frontera en el frame. `Qualities` debe declarar scope terminal, y su reconstrucción debe usar el mismo camino temporal; no presentar transiciones contaminadas como historial.
- **Transiciones:** idempotencia por identidad del hecho ya procesado. A→A idéntico consecutivo puede compartir contenido; A→B→A debe tener una nueva transición/revisión temporal que active A. No borrar tablas/migraciones antiguas: agregar historial de transiciones versionado que pueda referenciar contenido deduplicado, o una tabla v2 equivalente. Rebuild desde journal en DB scratch; si raw necesario falta, `NOT_REPRODUCIBLE`, no completar desde el último contenido de SQLite.
- **Metadata:** verificar K y publicación al proyectar, con clock inyectado en admission; no reemplazar disponibilidad desconocida por reference time. Conservar target/reference futuro de forecasts si ya publicado, sin volverlo hecho realizado. Revisiones legítimas tienen version/source key explícitos; conflicto del mismo identificador inmutable sigue fallando. Config `kickoff_ms` debe vincularse a evidencia admitida o supuesto de A; sin ella B no habilita señales pre-match. Bootstrap se valida como §7.
- **Fee:** limitar evidencia al corte y a su alcance. No modificar fórmulas V2 ni `FeeResolver` para inferir tarifa universal del trade; el consumidor impide que una POINT scoped a otro trade se presente como fee certificada del candidato. Puede devolver `UNRESOLVED` aunque exista una cifra observada posterior o ajena.
- **Compatibilidad/versionado:** mantener lectura histórica v1 para diagnóstico con etiqueta legacy. Nueva versión del projector/manifests/refs; migración nueva con checksum y rebuild reproducible. No modificar una revisión inmutable v1 ni sus referencias. Una DB ya drenada más allá de C no puede servir como bypass del nuevo gate.
- **Positivos:** tick conocido antes de C válido; mismo tick reobservado idempotente; retorno A→B→A produce A en el tercer corte; prueba obtenida después que demuestra disponibilidad antigua se admite con ambos tiempos.
- **Negativos:** tick futuro no vuelve usable el book anterior; suspect futuro no contamina corte viejo; fee posterior no cambia sus métricas; metadata corregida posteriormente no reemplaza inputs pasados; raw faltante no se reconstruye desde latest.
- **Gate/evidencia nueva:** H01/H04/H07; trazas por corte de transition ID, known_at, fuente y valor. Actualizar el test que actualmente prescribe look-ahead y mostrar rojo contra baseline, verde contra cambio.

#### S3. Una semántica de Books y una elegibilidad por uso

- **Contratos/owner:** M1.5/8, M2-S06/07/09; `internal/books` posee niveles/calidad; `internal/marketview` queda como adaptación/serialización del snapshot común; `internal/strategy` aplica requisitos antes de Detect/Evaluate; composición no redefine calidad.
- **Actual/evidencia física:** D02/D03; C02/C03/C06/C07/C11/C14. No corregir size como si fuera aditivo: el set/delete ya es correcto y debe permanecer.
- **Requerido:** compartir el paso de aplicación de eventos de Books entre inspección, frames y replay; puede extraerse una función pura interna al owner existente. marketview no debe mantener reglas divergentes de nivel, régimen, gap o frescura. Enrutar todos los controles relevantes por la misma frontera, con fan-out scoped a los assets/epochs afectados; falta de scope → invalidación conservadora explícita. Invalidar al cambiar autor/epoch; nuevo flujo sin base sigue `SYNCING`. No aceptar autor distinto con mismo número, ni volver a epoch revocado, ni sanar gap con snapshot del mismo epoch. El replay no solicita red: espera evidencia capturada o queda bloqueado.
- **Orden/calidad:** evaluar timestamp regresivo en deltas y snapshots antes de mutar; high-water mark no se rebaja por dato rechazado. Para fixture, cualquier regresión dispara `SUSPECT`; tolerancia real requiere política identificada. Un snapshot válido posterior puede rebasar hacia adelante un nuevo epoch autorizado; no reescribe estados previos. Parse/schema/ID conflict de un flujo activo deja motivo y degradación, no simple drop que mantiene usable. Verificar freshness desde observación/check y metadata requerida; no confundir latest change con liveness ni igualdad interna de timestamps con continuidad L2.
- **Elegibilidad:** cumplir DataRequirements existentes; separar `data_diagnostic`, `signal_eligible`, `fill_eligible` y `economics_certified` como facts/version de frame/política, sin otra Strategy API. Defaults M1 fail-closed. BBO descriptivo puede exponerse en diagnóstico sin fee ni L2, pero A4 no autoriza automáticamente nuevas oportunidades. Un consumidor no puede habilitar fills sólo por ver BBO válido. Si falta dato para comprobar un requirement, la instancia espera y queda razón durable.
- **Compatibilidad/versionado:** no cambiar vocabulario ni significado de estados M1; nuevos facts de elegibilidad son aditivos/versionados. Journals antiguos se reproyectan en nueva run; no sobrescribir sus frames o certificados. Snapshots tardíos del archive sólo pueden iniciar un epoch de reconstrucción explícito si la política lo permite, sin fingir reconnect original.
- **Positivos:** snapshot replace; size 10→7 resulta 7; cero elimina; aislamiento A/B; recuperación con snapshot autor/nuevo epoch permitidos; BBO corroborado permanece describible si L2 falla.
- **Negativos:** sin tick no `OBSERVED_USABLE`; gap no llega a Detect ejecutable; late delta no altera book usable; old epoch no vuelve; datos stale no pasan; BBO exacto con size incorrecto no produce fill.
- **Gate/evidencia nueva:** H02/H03/H05; transcript de transiciones con seq/event/knowledge/detected times y comparación Books↔Frames. Preservar suites set/delete ya verdes.

#### S4. Frames completos y tiempo de decisión estable al prefijo

- **Contratos/owner:** M1.5/6, FBL-008; `internal/frames` y composición `cmd/engine/screen.go`, `internal/experiment`; mismo runtime.
- **Actual/evidencia física:** D07/D08; C06/C07/C08/C13. Barreras existentes son reutilizables.
- **Requerido:** no admitir un corte hasta terminar todos los destinos de un capture record (incluidos control/metadata). Procesar transiciones ≤C aunque no cambien un book; owners silenciosos dan snapshot de su último estado con watermark probado. Un asset descubierto después de T no entra en F_T salvo universo ex ante explícitamente declarado que sólo lo incluya como identidad conocida, sin datos futuros. Declarar causales tanto la selección como los triggers.
- **Cortes/reloj:** fijar política de cuts por tiempos o prefijos completos antes de evaluar; distinta concurrencia de procesamiento no puede cambiarla. Preservar grid antiguo sólo como legacy/retrospectivo. Timer permite evaluar T sin inventar eventos; no usar el reloj actual como fallback cuando el histórico carece de tiempos. No avanzar el reloj desde un evento todavía no admitido completamente. Metadata/control solos deben poder invalidar antes del siguiente callback.
- **Dependencias:** vector completo por uso: refs por asset a estado/quality/epoch, régimen correspondiente, universo/reglas/relaciones/config/clock policy y bootstrap/external facts. Hash más locator resoluble o snapshot embebido con hash. Un slot no usado se registra `NOT_REQUIRED` y motivo/consumer profile; no etiquetar un hash de book como régimen. Incluir min/max knowledge bound usado, corte y versión temporal. Para Evaluate/fills, pinear inputs adicionales efectivos o devolver fase `NOT_REPRODUCIBLE`/bloqueada; nunca llenar con latest.
- **Compatibilidad/versionado:** DeliveryFrame v2 o metadata versionada equivalente, reader v1 sigue mostrando evidencia sin promoción causal. Mantener formato de Strategy y métodos; la adaptación entrega sólo campos permitidos y extensiones serializadas del frame. No editar decisiones/frames viejos ni reutilizar run IDs para corregirlos.
- **Positivos:** registro multiasset completo a ambos owners; snapshots de owners sin mutaciones correctos; metadata anterior a corte disponible; SCREEN y SHADOW con misma lista de cortes ven el mismo input.
- **Negativos:** corte solicitado entre destinos devuelve espera/ineligible, nunca C incompleto; sufijo cambia longitud total pero no decisiones prefijo; refs >C/unknown/hash incorrecto bloquean; un clock sin dominio no habilita B.
- **Gate/evidencia nueva:** H01/H06/H07/H08/H10; frames canónicos serializados, dependencias resueltas y tabla de admisión temporal por callback.

#### S5. Prueba de replay que cubre estado y dependencias reales

- **Contratos/owner:** M1.6, G-07/G-07b; `internal/replay`, `internal/experiment`, evidencia de certificación scoped. No nuevo replay paralelo.
- **Actual/evidencia física:** D05/D07; C09/C10/C16. Los mismos tests de seis paquetes pasan con los huecos descritos.
- **Requerido:** el replay de observación ejecuta los reducers usados por la entrega causal. Hash canónico de niveles/size/side, quality+reasons, epoch/autor, regime transitions y refs, tiempos relevantes, controles, frames y outputs de cada fase certificada. El batch schedule realmente gobierna avance/drenaje; no sólo un contador auxiliar. Comparar prefijos, no sólo final. Digests de identidad de dataset, estado y decisión deben ser distintos y tener alcance declarado.
- **Resolución:** comprobar integridad del VerifyReport y cada dependency hash contra bytes pineados; refs faltantes/mismatch y resultado de delivery ausente son `NOT_REPRODUCIBLE`/`INCOMPLETE`. Seleccionar `(run_id, instance_id, ordinal, phase)` completo; otra run con ordinal igual no puede sobrescribir una observación. Sin frames requeridos = `NO_DELIVERIES/INCOMPLETE`, no certificado positivo. Read-only estricto sobre fuentes. Si una fase de cuenta/risk/simulación carece de inputs recuperables, fail-closed de esa fase; la aceptación mínima de señales no exige inventar un replay económico completo.
- **Compatibilidad/versionado:** digest v2 y certificado `HCA1_CAUSAL_SIGNALS` con scope inequívoco, separado de M4/legacy y de los outputs A. Mantener hashes v1 como referencias históricas, sin compararlos como si tuvieran el mismo dominio. Capturas válidas pueden reutilizarse; evidencia insuficiente conserva ese estado.
- **Positivos:** schedules `{1}`, `{32}`, `{7,3,1}` con misma historia lógica/cortes producen mismos estados y decisiones; reinicio desde prefijo probado reproduce; aislar dos runs con ordinal 1.
- **Negativos:** mutar sólo size manteniendo BBO/calidad cambia estado hash; mutar tick/fee/reason detecta diferencia; hash no vacío inventado no resuelve; dependencia faltante bloquea; doble ejecución de frames contaminados no pasa gate causal.
- **Gate/evidencia nueva:** H07/H09/H10; manifests, fixtures SHA-256, estados/decisiones esperados versus actuales por corte y pruebas de mutación. No usar igualdad con los antiguos cuatro digests de calidad como oracle de niveles.

#### S6. Censura y horizonte de medición sin alterar economía

- **Contratos/owner:** M1.6/9; `internal/experiment` scorecards y `internal/strategy/pocs/sports` para historia/pending. Usar Feedback/observación existentes; no agregar estimando ni Strategy API nuevos.
- **Actual/evidencia física:** D09/C12; estados omitidos conservan historial y primera cotización favorable fuera de horizonte puede contarse como reversión. Describe cuenta discrepancias agregadas sin explicar cada intervalo temporal [C01: `describe.go:85–140`].
- **Requerido:** censura con `(asset, epoch, interval_start/end, reason, source_ref, detected_at, evidence_acquired_at, cut_seq, policy_version)`. Distinguir invalidación que el sistema sabía en T de hallazgo ex post. Excluir del resultado certificado con denominador/motivo, sin editar la decisión original. Para continuidad desconocida, no unir historia pre-gap y post-gap como referencia continua. Pendings que cruzan gap requerido quedan censurados; nuevo warm-up es explícito. Antes de contar una reversión comprobar pertenencia al horizonte; límite exacto definido por protocolo, primera observación estrictamente posterior nunca demuestra reversión dentro de él.
- **Compatibilidad/versionado:** scorecard/projection v2 en nueva run; parámetros congelados originales no se sobrescriben. Si se necesitan reglas de censura no aprobadas, guardar bruto y censurado y dejar outcome `INCONCLUSIVE`; no escoger la máscara que produce alpha.
- **Positivos:** reversión observada dentro de ventana cuenta; señal madura fuera sin reversión cuenta según protocolo; diagnóstico BBO puede continuar sin fee; snapshot revela discrepancia con detected_at correcto.
- **Negativos:** bid favorable sólo después de ventana no cuenta; silencio/gap no se interpreta como no-reversión observada; coincidencia del snapshot final no levanta fill eligibility de todo el intervalo; fee unresolved no se vuelve 0.
- **Gate/evidencia nueva:** H05/H08/H11; registro de censuras y denominadores, sin PnL como oracle arquitectónico.

### 10. Experimento determinista y gates de aceptación

**Todos los gates Hxx están `NOT_RUN` en esta auditoría.** Se especifican para el coding agent; no se confunden con las suites baseline ejecutadas. La prueba central usa datos sintéticos pequeños; no carga ni ejecuta OOS. Un fixture de prueba con Strategy neutral implementando la interfaz vigente es suficiente; no crear una estrategia productiva alternativa.

#### 10.1 Fixture HCA-1

Reloj UTC sintético de un solo día, precios/tamaños decimales exactos; assets A y B; IDs/condition/protocol válidos según fixtures existentes. Dos datasets B separados: observador W1 y observador W2. Ambos tienen su propia sequence/boot/epoch; no concatenarlos como un flujo global. Declarar procesamiento cero como supuesto del fixture, timestamps sin incertidumbre sólo por construcción sintética. W1 autor de A en epoch e1; B tiene owner propio. Kickoff v1=12:30, tick 0.01 y mapping se publican/conocen a las 11:58. Fee permanece unresolved salvo subcaso explícito de evidencia temporal, sin certificar economía.

Pinear en el probe `MaxBookAge=5 min`, `MaxMetadataAge=1 h`, `MinAssets=1` y observación inicial de ambos assets; son parámetros del fixture, no umbrales recomendados para producción. Así el corte 12:03 no falla por antigüedad antes de ejercer la causalidad. Agregar variante que excede esos límites y debe quedar inelegible. Los subcasos de gaps y epochs comprueban cada motivo aunque otros requisitos también fallen.

Para demostrar D06 sin confundir contenido y valor, el tick de M0 se observa en una revisión propia `RegimeContent{TickSizeRaw:"0.01"}` equivalente a un `tick_size_change` anterior a S0; mapping/reglas van en sus fuentes separadas. T1 y T2 usan el mismo namespace/asset y la misma estructura de contenido con valores `"0.001"` y `"0.01"`. No comparar un content inicial rico de CLOB contra un content tick-only: dos estructuras distintas no ejercen el dedup A→B→A señalado.

| ID | Event time / hecho | Knowledge W1 | Knowledge W2 | Estado/expectativa |
|---|---|---|---|---|
| M0 | 11:58 metadata v1, tick 0.01, reglas/identidad válidas | 11:58 | 11:58 | Bootstrap anterior probado; subcaso sin M0 debe permanecer inelegible |
| S0 | 11:59 snapshot A: bids 0.40×10 y 0.39×5; asks 0.42×10 y 0.50×8. B: 0.55×6 / 0.57×6 | 11:59 | 11:59 | Bases por asset; B no cambia por deltas de A |
| U1 | 11:59:20 ask A 0.42 size=7 | 11:59:20 | 11:59:20 | Debe quedar 7, nunca 17; repetir asignación no suma |
| Z1 | 11:59:30 bid A 0.39 size=0 | 11:59:30 | 11:59:30 | Nivel ausente, no cero contabilizado como liquidez |
| L | 12:00 ask A 0.42 size=0 | **12:08** | **12:00:01** | Evento tardío para W1; W2 ve BBO diferente. A las 12:03 W1 aún tiene ask 0.42; W2 ask 0.50 |
| U2 | 12:01 bid A 0.40 size=9 | 12:01 | 12:01 | High-water venue posterior a L. W1 no puede aplicar L tardío sobre estado más nuevo sin marcar anomalía |
| CUT | Decisión 12:03 | 12:03 | 12:03 | Probe devuelve `WIDE` si ask>0.45 y datos elegibles. W1=`NO_SIGNAL`; W2=`WIDE`. Diferencia válida entre observadores |
| G0 | 12:03:30 falta delta ask 0.50: 8→2; ausencia en el flujo observado | desconocido hasta comprobación | desconocido hasta comprobación | Ground truth sólo en oracle, nunca como input de Strategy. El sistema no puede conocer mágicamente la pérdida |
| T1 | 12:04 tick 0.01→0.001 | 12:04 | 12:04 | No cambia frames de 12:03; invalida constraints/candidatos desde ahora |
| C1 | 12:04:10 control `evidence_gap`, epoch e1 revocado | 12:04:10 | 12:04:10 | Invalidación conocida y durable. Libro puede conservarse para diagnóstico, no para fill |
| R0 | 12:05 snapshot completo: bid 0.40×9; ask 0.50×2, nueva base e2 autorizada | 12:05 | 12:05 | Detecta discrepancia con la reconstrucción anterior; repara hacia adelante. Registra intervalo incierto y detected_at=12:05 |
| M1 | 12:06 publicación de schedule corregido kickoff=12:20, que declara referirse al mismo partido | 12:06 | 12:06 | Lo declarado sobre el pasado no cambia K. F12:03 conserva v1; F12:06 usa v2 |
| T2 | 12:07 tick 0.001→0.01 | 12:07 | 12:07 | Debe activar nueva transición A→B→A; nuevo snapshot necesario según política de calidad |
| R1 | 12:07:30 snapshot actual completo e2 | 12:07:30 | 12:07:30 | Recupera constraints/base; fija watermark source mayor que L |
| L-arrival | Llegada W1 del evento L de venue 12:00 | 12:08 | ya recibido | No reescribe CUT. W1 lo conserva raw y marca/registra regresión; no vuelve atrás el libro usable |
| R2 | 12:09 snapshot actual e3 tras resincronización autorizada | 12:09 | 12:09 | Recuperación forward; historial/censuras anteriores conservados |

Cortes explícitos mínimos: 11:59, 11:59:20, 11:59:30, 12:01, **12:03**, 12:04, 12:04:10, 12:05, 12:06, 12:07, 12:07:30, 12:08, 12:09. Usar timers explícitos para cortes sin record exactamente en ese tiempo; no inferir cortes desde el tamaño final del dataset. La rama Sports usa sus `ref_frames=10` con diez observaciones válidas de warm-up anteriores al CUT y el mismo cutoff; esos warm-ups son sintéticos y no alteran los parámetros de la cohorte existente.

Subcasos deterministas del mismo bundle:

1. **No tick conocido:** quitar M0.tick y conservar T1 futuro. La baseline marca usable en marketview y en el primer tramo de Qualities; el contrato corregido impide oportunidad en 12:03. Este test debe fallar en baseline aunque el resultado terminal ya sea SUSPECT.
2. **Empate real local:** antes de la primera base de un asset C, mismo `received_us`, delta sequence=10 seguido de book sequence=11. Delta ignorado por no base; snapshot queda intacto. El sort por tipo de baseline lo invierte y cambia el nivel. Agregar variante mismo key/diferente payload → conflicto declarado, no orden de archivo accidental.
3. **Fan-out:** un único record actualiza A y B; solicitar corte después de intentar entregar sólo A. C no se publica completo hasta B o el frame es inelegible. Repetir con schedules que fuerzan el borde del batch.
4. **Epoch/autor:** después de C1, snapshot del mismo e1 no recupera; después de e2, delta o snapshot de e1 no reviven. Autor distinto con mismo epoch tampoco pasa. Un snapshot válido e3 sí recupera hacia adelante.
5. **Hidden gap:** omitir G0 sin C1/T1 en una variante. El sistema puede mantener calidad best-effort hasta R0, pero no puede certificar continuidad absoluta ni afirmar que sabía la ausencia antes de R0. La censura ex post debe preservar CUT y su decision hash original.
6. **Metadata categorías 2/3:** dos certificados obtenidos después: uno demuestra publicación y valor de M0 antes del CUT; otro sólo ofrece el valor revisado M1. El primero puede acreditar retrospectivamente un input viejo con prueba; el segundo no entra en CUT. Cambiar bytes de M1 no afecta prefijo. Un External con `AvailableAt>T` y capture seq bajo C tampoco entra.
7. **Fee posterior:** incorporar una observación de fee después del CUT y otra revisión de régimen aplicable; ni la fee efectiva del candidato anterior ni su etiqueta de evidencia cambia. Trade fee 0 scoped nunca se transforma en tarifa universal. No evaluar rentabilidad.
8. **BBO versus L2:** discrepancia sólo de size en nivel profundo con BBO idéntico y testigo BBA disponible. Mantener diagnóstico BBO, bloquear fill L2 insuficientemente soportado. Mutación size 10→100 con mismo BBO/calidad debe alterar state digest.
9. **Horizonte:** señal sintética con breakeven válido; primera cotización favorable en `signal_time+window_ms+1` → nunca `reverted`. Variante favorable dentro de ventana sí; gap que cruza la ventana → censurado, no no-revert observado.
10. **Reinicio y replay:** partir después de U2, reconstruir/reanudar con misma política y cortes; añadir sufijo T1/M1/L; comparar decisiones del prefijo. Ejecución SCREEN/SHADOW del probe con mismos cuts debe coincidir en Detect/Evaluate no económico; fills/ledger sólo existen en SHADOW y se comparan dentro de su fase.

No todos los subcasos deben fallar en baseline: set/delete ya funcionan. **El suite debe fallar antes de la corrección** al menos por futuro tick, gap omitido, tie rank, A→B→A, fan-out parcial, publicación futura y digest insensible a tamaños. El agente debe registrar resultados rojos reales de esos asserts contra baseline, sin escribir al checkout canónico de captura. El caso L por sí solo no demuestra look-ahead en el importer receive-time actual; la mutación que ordena venue-time en B debe ser rechazada por H01. Esa precisión evita fabricar una regresión inexistente.

#### 10.2 Gates y evidencia esperada

| Gate | PASS verificable | Negativo obligatorio / FAIL |
|---|---|---|
| H01 — Causalidad de prefijo | Para cada frame/dependencia: K≤T y seq≤C; decisiones prefijo idénticas al cambiar sufijo futuro bajo mismos cuts/protocolo | T1/M1/L conocidos después de T cambian una decisión vieja, o K desconocido se convierte en fecha inventada |
| H02 — Elegibilidad común | Books, SCREEN y SHADOW dan mismos estados/reasons; requirements se cumplen antes de callbacks ejecutables | Sin tick, metadata requerida, base o freshness aparece oportunidad atribuida elegible |
| H03 — Provenance/orden/epoch | Witness y clock domain resolubles, orden local conservado, set/delete correcto, late events/autor/epoch conflict degradan | Rank por tipo invierte sequence, collectors mezclados sin prueba, old epoch rehabilitado |
| H04 — Revisiones históricas | A→B→A produce tres transiciones; lectura por corte correcta también para suspect, metadata y fees; bootstrap probado | Latest atraviesa C; dedup borra vuelta a A; evidencia post hoc se confunde con publicación |
| H05 — Calidad y censura | Motivo/intervalo/fuente/detected_at recuperables; recovery sólo forward; BBO y L2 separados; horizonte respetado | Fill L2 sólo por BBO coincidente; hidden gap «conocido» antes de detectar; reversión fuera de ventana; salto de historia sobre gap |
| H06 — Corte atómico | Todos los destinos de cada record ≤C aplicados o frame ineligible; clocks/metadata/control incluidos | A actualizado y B viejo bajo el mismo C; clock adelantado por record aún parcial |
| H07 — Inputs resolubles | Refs/snapshots correctos por asset/fase, hash↔bytes y known-at; error explícito ante dato faltante | Hash inventado no vacío produce RESOLVED; régimen=hash de book; fase incompleta recibe PASS |
| H08 — Paridad consumidores | Mismos cuts/policy/dataset/input inicial ⇒ mismos inputs elegibles y señales SCREEN/SHADOW/REPLAY, con diferencias de ejecución declaradas | Igualdad aparente por cero oportunidades o comparación entre grids distintos |
| H09 — Determinismo significativo | Tres schedules ejercen realmente reducers/frames; reinicio y cold rebuild reproducen todos los hashes esperados por corte | Cambiar nivel, tick, quality reason o output relevante no cambia digest; otra run pisa ordinal |
| H10 — Compatibilidad y fallo cerrado | v1 legible no promovido; v2 completo pasa; zero-delivery/unknown clock/refs corruptos fallan; raw source sin cambios | Reescritura del journal anterior; v1 recibe certificado v2 por herencia; orden ambiguo oculto |
| H11 — Cohorte real limitada | Se ejecuta sólo ventana exploratoria permitida, reporta discordancias por evento/intervalo y los mismos gates, sin alpha como oracle | OOS leído, fee cero inferida, censura sin provenance, concordancia 0/628 declarada sin recalcular |

Cada gate deja artefacto pequeño en `testdata/historical-causality/evidence/`: ID/version, fixture hash, build/config, command, expected/actual, status, mode/observer, cuts hash, timestamp y refs al transcript por corte. El nombre y formato concretos se integran con el harness existente. No dejar suites que sólo afirman PASS ni tests que comparan el resultado consigo mismo; usar oracles numéricos y metamorfismos negativos del fixture. Resultado objetivo del correctivo mínimo: `HCA1_CAUSAL_SIGNALS_PASS` para fixture B; **no** `BACKTEST_PASS`, economía, alpha o live. H11 puede quedar `NOT_RUN/UNVERIFIED` si no hay datos admisibles; eso no se presenta como PASS del dataset.

#### 10.3 Aceptación sobre cohorte existente, cuando el agente tenga los datos

Usar exclusivamente los cuatro mercados exploratorios registrados: SD 3901945, NYM 3901951, TOR 3901947, SF 3901949; ventana `[2026-09-01T21:10Z, 22:40Z)`, cutoff y warm-up declarados. No leer payloads del OOS ATL/SEA 22:45Z. Los raw horarios pueden contener otros mercados: primero construir allowlist por condition/asset desde el manifest autorizado y aplicar predicados antes de materializar filas. Si no puede garantizarse el aislamiento, H11 queda `UNVERIFIED`; no abrir OOS para mejorar calidad.

1. Read-only de originales y hashes contra manifest; registrar entradas SHA256SUMS stale conocidas y resolverlas por manifest/archivo existente, sin «arreglar» el original ni afirmar integridad total con paths inexistentes. Scratch externo al dataset fuente; `dataset.Guard` activo. Sin descargas, infraestructura o cambios a Sports Week bajo este mandato.
2. Recuperar provenance witness/sequence/E/R real; si el NDJSON v1 la perdió, producir un binding derivado desde raw verificado. Seleccionar observador B y reportar qué proporción puede adjudicarse; cuando el merge original impida reconstruir esa perspectiva, bloquear B en esos intervalos, no elegir el witness conveniente.
3. Comparar reconstrucción engine versus oracle exacto independiente del test usando set/delete por asset, en cortes idénticos y sin gates que cambien inadvertidamente la serie comparada. Separar precio BBO, tamaño del top, todos los niveles y continuidad. El forense cuenta matches en extremos; reportar también observaciones `best_bid_ask` y sus discrepancias exactas. No usar 0/628 como umbral mágico para otro orden, ventana o denominador; reproducir ese número requiere exactamente su ámbito. Excluir OOS incluso si el antiguo script leía horas completas.
4. Reejecutar H01 cambiando sólo el sufijo de datos/revisiones de la cohorte y H08/H09 con cuts pineados. `cuts=30` previo no especifica por sí solo sus instantes: recuperar la lista efectiva y etiquetarla legacy; una nueva lista ex ante es nueva revisión de experimento, no sustitución silenciosa. Mantener `window_ms=300000`, `ref_frames=10`, `widen_min_bps=50` para checks de compatibilidad; nunca optimizarlos buscando señales.
5. Incorporar incidente 22:30–22:40, fronteras de hora y gaps como evidencia con disponibilidad/detección separadas. Audit mask posterior puede censurar métricas certificadas; no borrar inputs o decisiones del replay original. Mantener hipótesis estadística y OOS sin ejecutar.
6. Entregar counts de eventos/intervalos admitidos, censurados por razón, desconocidos y comparados; hashes de decisiones prefijo y divergencias. Si tick/kickoff históricamente observable no puede acreditarse, resultado `B_BLOCKED_METADATA`, aunque BBO descriptivo sea consistente. Fee unresolved no impide el diagnóstico, pero economía sigue no certificada.

### 11. Mandato ONE-SHOT para coding agent

> Implementa **HCA-1 — frontera causal del histórico** en `xKoRx/polymarket-engine` usando §§9–10 de esta auditoría como SPEC correctiva y M1 congelado como autoridad. El objetivo es demostrar con fixtures que ninguna decisión certificada usa conocimiento posterior, que un gap/estado inválido no se vuelve elegible por otro consumidor y que replay compara estados y dependencias efectivos. No investigar alpha ni rediseñar el engine.
>
> Arranca con bootstrap Agents-OS; lee el MVP, esta auditoría, continuidad y los contratos de los paquetes a tocar. Verifica HEAD vigente frente a baseline auditada `09e8c7610f29a35f8080122b7cb4219b9866ebd7` / código `66486ac99a4606d5dc2b44757ac0722a6baa5415`. Si avanzó, revisa el delta y revalida cada finding antes de corregirlo; no reviertas trabajo concurrente ni asumas que un hallazgo sigue abierto.
>
> Trabaja en checkout/worktree aislado, rama `codex/historical-causality-hca1` si no hay rama indicada por el owner. Mantén los datasets fuente read-only y usa scratch; no toques Sports Week ni infraestructura. Implementa S1–S6 como un correctivo integrado: provenance/policy temporal versionada, Regimes limitado al corte y transiciones recurrentes, semántica de Books compartida para Frames, controles de continuidad y eligibility, cortes completos/inputs resueltos, replay significativo y censura/horizonte. Preserva Economy V2 y la API Strategy existente. Puedes bloquear una fase no certificable con motivo explícito; no añadir otra arquitectura para hacerla pasar.
>
> Primero materializa el fixture de §10 y guarda la evidencia roja real contra la baseline para D01–D09 aplicables; preserva los controles positivos set/delete. Corrige las aserciones que actualmente prescriben look-ahead, mostrando la cláusula M1 que reemplaza su expectativa. Implementa por ownership; migraciones sólo nuevas/forward-only y reconstrucción scratch desde raw, sin modificar checksums de migraciones viejas. Certificados/digests nuevos tienen versión; no reselles un journal viejo como causal sin demostrar sus datos faltantes.
>
> No habilites modalidad A ni el perfil de oportunidades BBO relajado sin decisión registrada del owner (OD-H1/OD-H2). Mientras falte esa decisión, completa la corrección de B bajo M1 y devuelve bloqueos de metadata/calidad donde corresponda. No hace falta esa aprobación para quitar lecturas latest, propagar gaps, corregir A→B→A, cerrar fan-out, hacer cumplir publicación o reparar el verificador. No congeles fee cero, no cambies reglas económicas y no cambies el estimando de reversión.
>
> Ejecuta H01–H10 con oracles y los tres schedules; prueba reinicio, sufijo futuro, missing refs y compatibilidad v1. Después corre tests pertinentes con race, build/vet y regresiones de integración existentes. Coverage se mide según política vigente sobre cambios, pero ningún porcentaje reemplaza gates. Enlaza cada finding a su regresión y al artefacto de prueba. No uses resultados de alpha ni igualdad con el digest legacy como aceptación.
>
> Ejecuta H11 sólo si los datos exploratorios y su provenance están disponibles de forma aislada; no descargues datos ni solicites accesos para encubrir un `UNVERIFIED`. Ausencia de datos deja H11 pendiente explícito, no bloquea la prueba sintética ni habilita `BACKTEST_PASS`. No abrir OOS, enviar mensajes a terceros, comprar servicios, modificar infra, activar live, tocar Sports Week o publicar un cambio de modelo.
>
> Entrega un único diff revisable, comandos/results, matriz Hxx, manifest/versiones/migraciones, compatibilidad y limitaciones. Commit local del correctivo cuando esté verificado; publicación/merge del código requieren mandato de implementación/publicación aplicable del owner, no se deducen de esta auditoría documental. Actualiza sólo continuidad necesaria en Agents-OS. Si algún gate causal obligatorio falla, resultado `HCA1_NOT_ACCEPTED`; si todos H01–H10 pasan, `HCA1_CAUSAL_SIGNALS_PASS` limitado a B y al fixture, con H11 y economía separados. `LIVE_DISABLED` siempre.

### 12. Decisiones que requieren aprobación del owner

Estas decisiones **no se cierran** aquí y no son excusa para dejar sin corregir defectos M1. No se solicita acceso ni aprobación durante esta auditoría: la propuesta queda concreta para revisión posterior.

| ID | Alternativas y consecuencias | Propuesta fundada / estado |
|---|---|---|
| OD-H1 — Modalidad de investigación | B conserva observabilidad de un sistema definido y puede quedar bloqueada por provenance; A permite describir mercado idealizado con otra interpretación del tiempo; mezclarlas impide interpretar resultados | Mantener B como certificado causal por defecto y A opt-in con manifest/certificado independiente. Habilitar A requiere addendum explícito a M1.5, no cambiar el freeze ni ordenar venue-time automáticamente. **PENDING_OWNER** |
| OD-H2 — BBO descriptivo y señales sin L2 completo | Default M1 mantiene `SYNCING` sin constraints; perfil BBO admite fenómeno descriptivo sin certificar fills/economía, y eventualmente señales con requirements reducidos explícitos | Autorizar primero diagnóstico BBO separado; si se desea usarlo como señal PE-005-R1 sin tick/L2, congelar un perfil preciso y su certificado. No degradar significado de `OBSERVED_USABLE`. **PENDING_OWNER** para ampliación |
| OD-H3 — Prueba retrospectiva y selección | Exigir observador exacto maximiza auditabilidad y reduce muestra; admitir observabilidad históricamente demostrada después puede rescatar datos sin look-ahead; asumirla sólo produce A | Admitir categoría 2 con prueba separada de valor/disponibilidad y revisar cohort selection/censura. El tick/kickoff concreto sigue sin acreditación nueva en este shot. **PENDING_OWNER** para protocolo experimental, no permiso para backfill arbitrario |
| OD-H4 — Política de cortes, gaps y recuperación del archivo | Grid retrospectivo conserva comparabilidad legacy; grid/timers ex ante permite prefijo invariante. Censura más estricta reduce muestra; recovery por snapshot requiere epoch de reconstrucción distinguible del transporte | Pinear cortes/ventana/censura y reglas de recuperación antes de nueva corrida; conservar outputs anteriores. No cambiar `cuts=30`, horizonte o sample protocol sin revisión explícita. **PENDING_OWNER** |
| OD-H5 — Economía/estimando | Fee desconocida mantiene fenómeno descriptivo; fee 0 universal sin evidencia o redefinir `reverted` como spread bruto cambiaría el modelo | **No aprobar en este shot.** Economía V2/REAL_FEE_READY y OOS permanecen como estaban. Cualquier nuevo estimando o hipótesis de fee va a revisión separada; 256 trades no son autorización |

Propiedades `UNVERIFIED` al cierre: integridad byte-a-byte y métricas forenses de la cohorte en esta sesión; continuidad L2 entre observaciones; completitud/intra-ms del venue; sincronía entre collectors; timestamps históricos de persistencia; disponibilidad original de tick/kickoff/reglas/fees; comportamiento del binario en infraestructura; fills reales/queue, costes netos y OOS. Cada una tiene límite/gate en §§6–10; ninguna se convierte en una garantía por determinismo local o certificado M4.

```text
ASTRA_HISTORICAL_CAUSALITY_AUDIT
baseline: master/origin/master/origin/main 09e8c7610f29a35f8080122b7cb4219b9866ebd7; code 66486ac99a4606d5dc2b44757ac0722a6baa5415
m1_compatibility: PARTIAL_IMPLEMENTATION; M1 causal invariants remain appropriate; no freeze modified
causal_backtest_currently_valid: NOT_CERTIFIABLE_END_TO_END; no BACKTEST_PASS
critical_defects: D01-D08; D09 additional temporal measurement defect
contract_ambiguities: A1,A3,A5,A6; provenance, retrospective evidence, recovery/censoring, cut policy
m1_changes_required: A2/A4 only if idealized mode or relaxed BBO signal eligibility is authorized
unverified_properties: original-data revalidation, continuous L2, cross-clock order, historical metadata availability, economic execution, OOS
minimal_corrective_spec: HCA-1 / S1-S6; reuse Capture/Books/Regimes/Frames/Strategy/Replay/Simulator
acceptance_gates: H01-H10 synthetic mandatory; H11 cohort scoped; all new gates NOT_RUN here
owner_decisions: OD-H1..OD-H5 pending; no model decision closed
implementation_mandate: section 11; B fail-closed; no A/fee-zero/OOS/live activation
```

## Fuentes

Autoridad documental: [[Polymarket Engine — MVP]] §§M1.3–M1.10, M1.15, FBL-004/008/012, ASTRA-2, ASTRA-3, M2-S05…S10/S13; [[Research — Technical Platform Map M0]] y [[Polymarket — Technical Platform Map — synced 2026-09-17]], partes 03/05/07/10; [[2026-09-21-historical-research-m0]], [[2026-09-21-historical-backtest-readiness]], [[Polymarket Engine — Continuidad Five-POC 2026-09-20]] §§15–16; addendum y forense enlazados arriba. Los informes previos se conservan como historia; esta auditoría no modifica M1.

Todas las referencias Cxx siguientes corresponden a archivos leídos físicamente de `xKoRx/polymarket-engine` en **09e8c7610f29a35f8080122b7cb4219b9866ebd7**. Rangos de línea identifican evidencia, no cambios propuestos.

| ID | Archivo y líneas de evidencia |
|---|---|
| C01 | `internal/histimport/import.go:28–56,132–175,214–217,235–291,302–342`; `internal/histimport/describe.go:85–140`; import schema, reloj, epoch, tipos, sort y discrepancias agregadas |
| C02 | `internal/books/reducer.go:43–48,256–273,330–469,474–498`; `internal/books/books.go:6–29`; replace/upsert, quality, gap, author y epoch |
| C03 | `internal/marketview/projection.go:37–75,80–109,133–223,231–282`; proyección compartida sin régimen/control, deltas y provenance de depth |
| C04 | `internal/histimport/quality.go:13–42,66–74`; `internal/histimport/anchor_test.go:92–150`; `cmd/engine/historical.go:46–59`; consumidor terminal y test de look-ahead |
| C05 | `internal/regimes/service.go:30–120`; `internal/regimes/reducer.go:502–520,646–711,764–777`; `migrations/0021_regime_revisions.sql:8–27`; latest, known_at, dedup histórico y suspect |
| C06 | `cmd/engine/screen.go:198–241,262–365,379–425,510–516`; Books→owners→marketview, filtros y batches |
| C07 | `internal/experiment/experiment.go:225–245,267–305,366–438,822–831,863–903`; SHADOW, cortes, fee latest y fills |
| C08 | `internal/frames/frames.go:68–99`; `internal/frames/dispatcher.go:374–401,429–445,498–557,585–601`; `internal/frames/receive_clock.go:10–40`; `internal/frames/dispatcher_fanout_test.go:13–46` |
| C09 | `internal/replay/replay.go:123–175,179–210,222–279,299–375`; `internal/replay/manifest.go:33–50,81–105`; digest, schedule, resolución y cutoff |
| C10 | `internal/experiment/strategy_replay.go:63–111,113–216`; lectura de frames, aislamiento de observaciones y comparación de outputs |
| C11 | `internal/strategy/api.go:35–52,84–96`; `internal/strategy/runtime.go:149–184,297–357`; requisitos declarados y callbacks |
| C12 | `internal/strategy/pocs/sports/sports.go:120–173,203–204,220–282,291–313,317–352,447–480`; kickoff, historia, reversión, calidad y fee |
| C13 | `internal/external/external.go:44–73,78–116,135–171,175–209`; publicación, known_at y filtro por seq |
| C14 | `internal/strategy/pocs/pocdata/pocdata.go:119–125`; `internal/simulator/simulator.go:91–105,128–188,193–246`; `internal/regimes/feeresolver.go:199–257`; profundidad, llegada, gross y fee de trade |
| C15 | `internal/capture/envelope.go:193–227`; `internal/capture/capture.go:396–455`; `internal/capture/writer.go:193–204`; frontera durable y tiempos |
| C16 | `testdata/research-master/certificate.json:1–18,242–260,524–544,636`; certificado existente; suites vigentes inspeccionadas bajo los seis paquetes del comando de §1 |
| F01 | Workspace forense registrado en [[Research — Historical L2 Forensic Validation 2026-09-21]], `hist-l2-forensic-20260922/scripts/recon.py` funciones `recon/analyze/apply_price_change`, `bba_check.py`, `cut_states.py`; código leído, datos y cifras no reejecutados |
