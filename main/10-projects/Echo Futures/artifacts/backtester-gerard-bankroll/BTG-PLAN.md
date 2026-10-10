---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTX-PERF-DESIGN]]"
  - "[[BTX-PERF-IMPLEMENTATION]]"
  - "[[BTX-PERF-ADVERSARIAL]]"
  - "[[BTX-PERF-FINAL]]"
  - "[[BTX-PERF-S03-TOP-A-EVIDENCE]]"
  - "[[BTX-PERF-S03-TOP-B-EVIDENCE]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-05"
updated: "2026-10-10"
---

# BTG-PLAN — Estado vigente y continuidad del backtester

## Propósito

Control único de BTX-PERF. Owner exige una trayectoria financiera integrada por modalidad sobre todo el histórico disponible, rendimiento utilizable para iterar, Strategy/MM compartidos sustituibles, replay oficial y explicación de actividad. Primary dirige y revisa evidencia: no desarrolla ni acepta producto por Owner.

La historia completa anterior queda preservada en el mismo path en Git `e0be1e552b51cf005ee10e0fa67295bbf78e9476`. Esta edición incorpora una NUEVA autorización expresa Owner de un último shot y corrige dos hechos: la fuente S04 ya está publicada y los TOPs directos del Owner son GLM, mientras los TOPs de GOD son Sol6.1. No reescribe informes, RED ni recibos históricos. C01–C12 y matrices pendientes conservan autoridad a través de [[BTX-PERF-ADVERSARIAL]]; los límites de [[BTX-PERF-FINAL]] no se convierten en aceptación.

## Contenido

### Estado vigente — autorización terminal Owner, 2026-10-10

```text
PROGRAM = BTX-PERF
PRIMARY_SESSION = OPEN_UNTIL_EXPLICIT_OWNER_CLOSE
S01_TECHNICAL_DESIGN = ACCEPTED_WITH_EXPLICIT_PERF_EXCEPTION
E1 = PARTIAL_WITH_EVIDENCE
S02 = PARTIAL_IMPLEMENTATION_WITH_MATERIAL_GAPS
S03 = ACCEPTED_BOUNDED_RED_REJECTION_AND_HANDOFF
S04 = PARTIAL_DELIVERY_WITH_USEFUL_BOUNDED_FUNCTIONAL_EVIDENCE
PROGRAM_OPERATIONAL_OBJECTIVE = NOT_DELIVERED_IN_FULL
S04_SOURCE_REMOTE_RESOLUTION = VERIFIED_ed31156fe251a053241044f7659c078424667348
LAST_SHOT = EXPLICITLY_AUTHORIZED_BY_OWNER
LAST_SHOT_ID = BTX-PERF-LAST
LAST_SHOT_DISPATCH = GOD_COORDINATOR_PROMPT_ISSUED
LAST_SHOT_EXECUTION = NOT_STARTED_BY_THIS_PRIMARY
LAST_SHOT_GOD_PRODUCT_CODE = FORBIDDEN
OWNER_DIRECT_TOP_MODEL = GLM-5.3-Flash
GOD_DISPATCHED_TOP_MODEL_REQUESTED = GPT-6.1_Sol
FINAL_OWNER_ACCEPTANCE = NOT_GRANTED
READY_FOR_OWNER_ACCEPTANCE = NO
PHYSICAL_RUNTIME_READINESS = NOT_DEMONSTRATED_OUT_OF_SCOPE
PROMOTION = NO_MERGE_NO_DEPLOY_NO_LIVE_AUTHORIZATION
```

Owner pide evaluar el producto y dar «un last shot para GOD con sus TOPs», terminar el backtester dentro del día disponible y aclarar las pocas compras/días de actividad. Es una excepción explícita al máximo anterior, no un quinto shot rutinario ni aceptación de los anteriores. No hay nuevas extensiones automáticas. GOD coordina y adjudica, TOPs desarrollan/ejecutan; no otro GOD arquitecto entre etapas ni una cadena de prompts de investigación.

La aclaración de modelo prevalece para interpretar las sesiones directas del Owner: GLM-5.3-Flash es su TOP válido. Se retira la objeción por esa elección; las reservas de correctness/evidencia son independientes. Para los trabajadores de GOD el selector solicitado sigue siendo Sol6.1, sin sustitución silenciosa. Registrar identidad servida sólo cuando exista recibo, sin convertir UNKNOWN en acusación o garantía.

### Día disponible y límite global

Recepción temporal observada por herramienta: `2026-10-10T10:09:16-03:00`, America/Santiago. «Un día» se interpreta en el mandato de transporte como máximo24h desde ese corte, hasta `2026-10-11T10:09:16-03:00`; es una interpretación explícita del presupuesto Owner, no una estimación de duración ni una promesa de entrega asíncrona. El ejecutor registra inicio/remanente reales y no reinicia el reloj por worker. Un nuevo corte sólo puede proceder de Owner. La ventana histórica9oct00:00 sigue vencida; ya no se usa para bloquear la autorización nueva.

### Publicación S04 resuelta y alcance de esta revisión

GET autenticado de `xKoRx/echo/refs/heads/codex/btx-perf-s04` devuelve `ed31156fe251a053241044f7659c078424667348`. Compare desde `bbbcc1d5dc0ed18badae46b4eba1a17822632b60` confirma9commits. La explicación Owner de push a un origin local intermedio es consistente con la publicación ahora accesible; no se inspeccionó la configuración física de remotes desde Primary. No volver a pedir el push ni conservar el404 como bloqueo vigente.

Primary revisó source puntual en ed31156f: adapter ntminute y pool/cursor/tests, compose/openDatasetCursor/composeStreams, experiment_catalog, E2E multistream del CLI y biblioteca, functional_profile, composición compartida y S2. Leyó el diff del último commit. No compiló, ejecutó tests/backtests, perfiló ni inspeccionó los artefactos locales completos de S04. Los hallazgos siguientes son de lectura/razonamiento sobre source, no falsificadores ya corridos por este Primary.

Identidades útiles: S04 corridas `0a6a0763` abreviado/bin `f80d8974157452f0e7ac0d757b8815a37d0a259e222d132a69321a196010f69e`; HEAD ed31156f/bin reportado `068a854802c29a6dcb69b949d8c70882101452fc1fa2db0939d6cae60216edd6`. Resolver SHA completo de0a6a en el DAG antes de atribuir pruebas. No transferir la revisión independiente de0a6a al último cambio sólo por un replay del autor.

### Qué significa la corrida entregada

BASIC y CAMPAIGN S04 reportan trading `2025-10-27T17:52Z` a `2025-11-27T18:00Z`, con warmup desde13oct. No son tres años. BASIC saldo70307,92USD/neto−29692,08,3214366records/wall1025,53s. CAMPAIGN6compras/5burns/1cobro neto1500/caja5780,3127905records/wall668,92s; `5000−6×120+1500=5780`.

Compras de cuentas no son señales, entradas, operaciones ni fills. Una cuenta puede operar múltiples veces antes de quemarse/retiro; seis compras no permiten estimar la frecuencia diaria. Los millones de records tampoco son millones de trades. Falta extraer actividad diaria de los outputs para responder la pregunta Owner, sin inventar conteos.

NQH6 declara consumo0 y sin obligación en esa ventana, porque los datos/selección corresponden a diciembre. Ese0no es por sí solo un bug; sí demuestra que esas corridas no ejercitaron una transición financiera real a NQH6. Las corridas sirven como evidencia funcional acotada de pérdidas/lifecycle/cobro/replay, no como entrega multianual. Tener un descriptor con dos contratos no prueba usar ambos.

S2 source:5m BAR_CLOSE, H4/SMA50, BB20/2poblacional, setup pullback y un ciclo técnico por excursión; rearme por basis/tendencia, sin apertura en la vela de rearme. No hay garantía implementada de una entrada diaria. Esto no exonera días vacíos: diagnosticar oportunidades/causas y detectar señales válidas perdidas, no forzar trades o modificar reglas para alcanzar un conteo.

### Nuevos riesgos materiales localizados para el LAST SHOT

| ID | Fuente / mecanismo estático | Verificación y reparación exigibles |
|---|---|---|
| L1 | ntminute.Source.Open asigna partes a2workers; pumpPart retiene worker hastaEOF con canal256; refill espera el stream siguiente del heap. Con3+streams largos, dos workers pueden quedar en canales llenos mientras el consumidor espera una parte todavía no asignada. | Negativo3y13streams, orden temporal adverso al orden de IDs, >256filas, workers1/2 y cancelación. Corregir starvation manteniendo orden causal; no declarar deadlock ejecutado aquí. |
| L2 | WaitGroup de Open no se espera en Close; cancelar no confirma salida antes de cerrar parts. failed y heads cerrado pueden quedar simultáneamente seleccionables tras error. | Race/Close bajo backpressure y error junto aEOF/buffer; primera causa no se pierde ni se finge fin limpio. |
| L3 | experiment_catalog ordena catálogo y fija primero inicial; omite cambios anteriores aTradeStart, PrepareAt=EffectiveAt, intervalos estáticos y calendario mensual basado enWeeklyBase. openDatasetCursor usa intersección global, no ReadPlan por obligación. composeStreams anticipa demanda de todos los slots. | Probar horizonte intermedio,3expiries, warmup real, overrides y retirado con obligaciones. Reconciliar selección/prefijos/ReadPlan efectivo; no afirmar que toda observación estática ya sea bug financiero. |
| L4 | E2E TestS04ExperimentMultistreamTwoStreamsBasic comenta que no llega a diciembre; test de replay multistream de ed31156f exige schedule vacío y fuente futura fuera de horizonte. | E2E público que atraviese una frontera con ambos lados consumidos y operación/estado válidos; caso real de rollover. Los tests anteriores no acreditan esa capacidad. |
| L5 | Falta desglose diario; S2 no tiene cadencia diaria contractual y compras no cuantifican operaciones. | Embudo diario desde datos/readiness/setup/señal hasta admisión/orden/fill, causas y días sin entrada. Oráculo independiente de reglas compartidas; no tuningROI ni cuota artificial de trades. |

Estos puntos alimentan tareas ejecutables, no otro ciclo de diseño. Una prueba que refute un riesgo se conserva y acota; un defecto confirmado se corrige dentro del mismo encargo. No ejecutar primero todo el histórico para descubrir un bloqueo que un fixture de segundos puede demostrar.

### Mandato terminal y organización

Un GOD en superficie con delegación/Daedalus efectivos dirige como máximo3TOPs de trabajo disjunto (integración/fuentes, actividad-datos-Strategy, rendimiento) y1TOP verificador independiente. Es máximo, no mínimo ceremonial. Un único integrador de producto; GOD no escribe código/tests/scripts ni integra parches. Workers ONE-SHOT con devolución/cierre únicos, sin reactivarlos una vez cerrados. Comunicación intermedia para corregir RED dentro del mismo encargo es válida; no se entrega una build distinta de la que firma el verificador.

Prioridades: negativos baratos pool/rollover y actividad existente → catálogo completo/gaps y reparación funcional → mejoras de coste sustentadas en carga ACTIVA → freeze final → BASIC/CAMPAIGN integrales y replay independiente → publicación verificable y reporte de operaciones/días. No repetir investigación de C08–C10 reparados; conservar regresores y completar las matrices pendientes de S03/C01–C12, incluido provider final/ALL-SKIP y cobertura del delta.

Esta autorización permite reparaciones/optimizaciones acotadas necesarias para el objetivo, no otro motor o plataforma. Targets históricos se conservan (BASIC3600s/CAMPAIGN3900s multianual; NQU6BASIC180s/CAMPAIGN220s; MIN_SPEEDUP1,5× y RSS512MiB), con sus fallos/fundamento objetado explícitos. Sólo comparaciones limpias y semánticamente compatibles; no retarget ni usar un mes como tres años. No medir mientras builds/tests/coverage/replays propios compiten. No escalera de reruns300/600/900. Reserva para finalización/replay dentro del corte global.

La trayectoria completa usa todos los años disponibles y su catálogo verificado, no campañas por contrato sumadas. Datos genuinamente ausentes no se fabrican ni se saltan con estado arbitrario; identificar/recuperar desde autoridades autorizadas la frontera faltante, conservar requisito incumplido si no puede resolverse. Nunca COMPLETE por descriptor, rc0, replays de un aborto o conciliación aislada.

### Invariantes de producto y entrega

BASIC100000 continuo sin lifecycle; CAMPAIGN5000/120 ON_DEMAND, una cuenta operando,4COBROS efectivos por cuenta y reinversión cobrada, pérdidas nominales sin redebito. Strategy/MM compartidos y sustituibles; sin ifGerard, SL/TP/sizing/adds/señales/fees alterados para velocidad oROI. Mantener protección/callbacks/reservas/claims/finality, dinero exacto, todas las revisiones y propiedad del sink, cuerpos admitidos/aplicados coherentes y getters aislados. IDs/ref mappings uno-a-uno por generación; no hashes/digests borrados.

Build única al final: source/bin/corpus/config/Strategy/MM y outputs con hashes; cambio posterior invalida cobertura del delta hasta revalidación. Reporte diario conciliado, resultados por cuenta, rollover realmente ejecutado, límites y tiempos con denominadores, commands completos sin elipsis/CWD ambiguo. Publicación de producto verificada en GitHub real, no sólo origin local. Agents-OS master solamente, un escritor/readback preservando concurrentes. Sin merge/deploy/órdenes/broker/cuentas/ETCD/PROD/ACL desde este encargo. Readiness física sigue separada.

### Prompt exacto y próxima devolución

Library `/BTX-PERF-LAST-GOD-TOPS-PROMPT.md`, `library_file_id=libfile_4359e47e47108191ae5ae0c83ad73644`, backing `file_000000004e28820e82a6a9ff70a46ed4`;29661bytes,SHA256 `92ae19f23dcfa097a84aeee9e31b0b87d6b1a7257320c1fa2155c988e84251e9`. Transporte ONE-SHOT GOD, no ejecución iniciada por Primary. Salida esperada `BTX-PERF-LAST-FINAL.md` en este directorio canónico, con paquete externo y todos los gates/evidencias de la build final. No precrear ese dictamen ni dar aceptación por Owner.

S04/contrato/informes siguen intactos. Registro de esta autorización y rectificaciones en el change_log consolidado [[2026-10-09-btx-perf-s02-owner-amendment]], con historia anterior preservada por Git. Primary sigue abierto; no feedback/cierre Primary implícitos.

## Fuentes

- Mensaje Owner10oct2026: asignación GLM/Sol, push real de S04, pregunta sobre frecuencia y autorización expresa de un LAST SHOT dentro del día disponible.
- Mandato original BTX-PERF, especialmente trayectoria única y todas las oportunidades admisibles; la nueva autorización altera número de encargos/plazo, no permite aceptar producto incompleto.
- [[BTX-PERF-DESIGN]], [[BTX-PERF-ADVERSARIAL]], [[BTX-PERF-FINAL]], originales inalterados.
- Echo ed31156fe251a053241044f7659c078424667348: paths/funciones citados en esta nota y en el prompt; compare autenticado bbbcc1d5→ed31156f:9commits. Revisión de source, no ejecución Primary.
- Control/journal anteriores completos en e0be1e552b51cf005ee10e0fa67295bbf78e9476. Los404/422 anteriores son históricos, la publicación actual ya está verificada.
