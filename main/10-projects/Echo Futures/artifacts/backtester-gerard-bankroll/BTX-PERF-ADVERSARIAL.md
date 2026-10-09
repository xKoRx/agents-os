---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
  - "[[BTX-PERF-DESIGN]]"
  - "[[BTX-PERF-IMPLEMENTATION]]"
  - "[[BTX-PERF-S03-TOP-EVIDENCE]]"
  - "[[BTX-PERF-S03-TOP-A-EVIDENCE]]"
  - "[[BTX-PERF-S03-TOP-B-EVIDENCE]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-09"
updated: "2026-10-09"
---

# BTX-PERF-ADVERSARIAL

## Propósito

Dictamen independiente del encargo BTX-PERF-S03 iniciado, dirigido por GOD y sustentado en falsificación preliminar y dos TOPs independientes. No reinicia S01/E1/S02, no ejecuta S04 y no concede aceptación de producto. Primary conserva BTG-PLAN y Owner conserva la autoridad de producto. GOD escribe documentación y adjudica evidencia; no escribe ni modifica código, tests, fixtures ejecutables, extractores, comparadores o instrumentación, ni compila o ejecuta backtests.

## Contenido

### Estado del dictamen

```text
DOCUMENT_STATE = FINAL_BOUNDED_ADJUDICATION
PROGRAM = BTX-PERF
SHOT = S03_CONTINUATION
CANDIDATE_GLOBAL_PASS = REJECTED_BY_EXISTING_EXECUTED_RED
S03_GOD_ADJUDICATION = READY_FOR_PRIMARY_REVIEW
S03_VERDICT = RED_REJECT_CANDIDATE
S03_DOCUMENT_COMPLETENESS = COMPLETE_FOR_BOUNDED_REJECTION_AND_S04_HANDOFF
S03_TEST_COVERAGE = PARTIAL_WITH_EXPLICIT_NOT_RUN
S04 = NOT_STARTED_PRESERVED
PRIMARY_SESSION = OPEN
FINAL_OWNER_ACCEPTANCE = NOT_GRANTED
```

**Dictamen RED:** rechazar este candidato. A los RED integrados del preliminar se agregan tres defectos confirmados por TOP B: aplicación de dinero distinto del cuerpo admitido, corrupción del sello desde un getter público y sobregiro en la compra inicial. La evidencia favorable de la traza R y del prefijo NQZ5 se conserva con sus límites. Los dos TOPs entregaron y cerraron; el dictamen queda completo para este rechazo acotado y el paquete S04, mientras la cobertura ejecutada sigue parcial. `READY_FOR_PRIMARY_REVIEW` significa dictamen disponible, nunca producto aceptado.

### Autoridad, cortes e identidades

Orden de autoridad: mandato Owner BTX-PERF y adenda de aceptación S01/autorización S02, despacho Owner de esta continuación, control vigente BTG-PLAN y diseño aceptado bajo la adenda. Las afirmaciones S02, su PERF_CONTRACT y el README son objeto de contraste. Los estados históricos del diseño no revocan la aceptación posterior ni habilitan un nuevo probe.

Lectura local de Agents-OS sobre `master` en `9561c60d1de2d59d1fe9ac393aaa6d37fa8ad17a`; `ls-remote origin refs/heads/master` devolvió el mismo corte. Control también leído por conector GitHub autenticado. La lectura del Primary del preliminar en `88e92e98de735dec8a0fa5832babf418c57c340c` se conserva como procedencia documental, no como inspección física de sus spools.

| Artefacto | Blob Git leído | Tratamiento |
|---|---|---|
| BTG-PLAN.md | `de3753b81564eb62f64a8b5eb18f198a6a81fd27` | Autoridad de control; no editado por GOD |
| BTX-PERF-DESIGN.md | `1cedf2e4c66886079a04d18dd60216b423316b42` | ACCEPTED_INPUT técnico con adenda delante de estados históricos |
| BTX-PERF-IMPLEMENTATION.md | `cec0feaede7e52cdd9b742c0ebfd63179c158207` | AUDIT_TARGET; preservado sin correcciones retrospectivas |
| BTX-PERF-S03-TOP-EVIDENCE.md | `cf21581c5cee5d90035e602456619e1eda2e7c0d` | ACCEPTED_INPUT_BOUNDED_WITH_QUALIFICATIONS |

El sync abreviado `32d8d6d0` y SHA256 abreviado `51f2a1d2…` del handoff preliminar son localizadores reportados distintos del blob Git. No se expanden por conjetura.

| Identidad de producto | Valor y alcance |
|---|---|
| Baseline de lectura/documentación | `50250a2b0df6106943108bf6bfe57552409f3d13` |
| Código histórico | `d1b1446d401f88cfa42dee2eb959120305f5a372` |
| Control corregido | `d609ca241eed63b1b4413af5bae5b849d334ead0` |
| Binario control SHA256 | `0db2feae6237ebc20ba8ce16bcc9f50fee0e6809c3677585b403a3d708c490ee` |
| Candidato medido | `584a3cd91d8ecf2d8f292547a35f8e9963e2270d` |
| Binario medido SHA256 | `e5d4860b4e70f5f5833ebf374b08fb771a4551bc6d58996fa42305e1049bd141` |
| HEAD de verificación preliminar | `bbbcc1d5dc0ed18badae46b4eba1a17822632b60` |
| Binario preliminar SHA256 completo, verificado por TOP B | `c9ac66caf363e1eda662c15d07b7c6cdb2fa11e773c30243d23e4aed7edc13b8` |
| Archive source TOP B SHA256 | `5f45a04dfccac63f8178e1f7dbec41d6bc5d0c738880eda2148650bc99441d25` |
| Binario final de tests TOP B SHA256 | `45ba14ba265290fa3fb164ccfe4d79bedb77620c09ddc1a2e66e95ae1d6c5671` |

584a→bbb cambia README y test de ring según recibos preliminares; no convierte al binario medido 584a en un binario bbb. Cada nuevo TOP debe fijar su fuente/overlay/inputs/binarios por separado. Ningún tiempo S02 se atribuye a una compilación de S03.

### Despacho y atribución

La superficie efectiva de esta conversación expone shell local, archivos Daedalus y `collaboration.spawn_agent`; la etiqueta CLOUD del encargo no se utilizó para negar herramientas existentes. Los directorios Owner se comprobaron disponibles. Los dos despachos usaron `fork_turns=none`, modelo solicitado `gpt-6.1-sol`, sin autorizar subdelegación. El harness recibió explícitamente ese selector; la identidad real de ejecución sólo se acreditará con el recibo disponible y, si no se expone, permanece UNKNOWN. Modelo real GOD y consumo Pro no expuestos: UNKNOWN; el rol pedido no prueba el modelo servido.

| TOP | Pregunta | Límite operativo fijado por GOD | Estado |
|---|---|---|---|
| A, `/root/top_a_evidence` | Recibos/sello, biyección tipada y negativo referencial, NQZ5 preservado | 35min de tarea; comandos pequeños ≤120s; lectura forense ≤300s por spool; cero ejecución financiera nueva | RETURNED_CLOSED; evidencia aceptada con límites explícitos |
| B, `/root/top_b_safety` | Safety/contratos compartidos y adjudicación de cinco tests rojos | 35min de tarea; ≤120s por comando y ≤12min agregados de ejecución; único ejecutor financiero | RETURNED_CLOSED; evidencia aceptada con límites explícitos |

Son límites operativos de este despacho, no una concesión Owner de 180min/4h ni un nuevo deadline. No se reabre el ejecutor preliminar. Cada TOP tiene un artefacto distinto y una única devolución final; GOD es el escritor documental de publicación. Nada de clones completos por worker, export NT nuevo, lote13×, corridas históricas300/600/900s, perfiles o reparación de producto.

El preliminar conserva `MODEL_REPORTED=GLM-5.3-Flash`, superficie reportada ZCode, `REQUESTED_ROLE=TOP`, `REQUESTED_MODEL_COMPLIANCE=NOT_DEMONSTRATED`. El título TOP LOCAL no cambia ese recibo. Las pruebas reproducibles se evalúan por sus inputs, oráculos y resultados; no se descartan sólo por el modelo.

### Evidencia preliminar aceptada y reservas

| ID | Aporte admitido | Reserva / conclusión que no se admite |
|---|---|---|
| F-S03-01 | Bytes del bloque iguales en copia/publicación anterior al commit de optimización; recibos hash/hora inconsistentes | A resolvió receta; freeze anterior al primer cambio sigue NOT_DEMONSTRATED. No atribuir intención |
| F-S03-02 | Dos streams físicos reales rechazados en BASIC y CAMPAIGN por `experiment`, rc2 | Defecto de implementación, no falta externa de datos; no volver a ejecutar sin duda material |
| F-S03-03 | Manifest CAMPAIGN sin Artifact; `--result` enruta antes de drenar footer lazy; ambas rutas CLI no alcanzan controlador | IDENTICAL bare sin replacement no certifica replay de campaña; fixture API no certifica CLI |
| F-S03-04 | Out-root movido rompe rutas; rc0 con FAILED/WARMUP_INCOMPLETE | Coverage de descriptor no acredita mercado consumido; precisar mapeo de estado/rc en S04 |
| F-S03-05 | Par R completo75,77s→34,01s; censuras NQU6 exceden180s | Beneficio R acotado; dos timeouts no prueban no-regresión,5h no es tiempo completo observado y omisión del pool no se convalida por R |
| F-S03-06 | Prefijo NQZ5 alcanza replacement18nov y pass-funded20nov2025, progresa hasta21nov | A concilió batch/cuenta/generación; no completo, no footer/checksum ni cobros finales, nunca resume desde spool |
| F-S03-07 | 88362 records por lado,109 records con diferencias en IDs/refs; mutación de precio rechazada | A añade biyección de R y negativo referencial; estado final provider todavía no demostrado |
| F-S03-08 | Nueve regresores S02 y840 sondas findSource; estabilidad de ventanas en bordes ejercitados | No prueba universal de inmutabilidad pública, callbacks o race |
| F-S03-09 | Oráculo independiente rescata fixture legacy, sin diferencias de records | El test del producto sigue abandonando antes de comprobar; no queda reparado por un test externo |
| F-S03-10 | Recibos reportan baseline8fallos y candidato5; tres tests CLI pasan | Encabezado/resumen «reparó2» inconsistente; B adjudicó3expectativas supersedidas,1fallo de harness y1no resuelto; preexistencia no prueba seguridad |

No se repitieron F1/F2/F3 para fabricar confirmación redundante. Estos RED se aceptan como resultados atribuidos al ejecutor preliminar con localizadores y alcance descritos, no como pruebas corridas por GOD.

### TOP A — sello, equivalencia y NQZ5 adjudicados

Leído íntegro [[BTX-PERF-S03-TOP-A-EVIDENCE]] y su delta final, blob `4f97884c0a8b0d26e8d75197f22dd5e35a04a3e9`, SHA256 `13508e92ddcb64f6f745deab2daf96405348f8f1dbc77b6a40c072f061e7e5c3`. Paquete externo `aranea/work/btx-perf-s03-top-a-20261009/`; SHA256MANIFEST.txt `0d8d97322435eac763802018e6fcee501813a343f06895f5bf21c85e7567f345`. GOD revisó `seal.json`, `r-oracle.json` y `nqz5-oracle.json` además del documento; TOP A ejecutó los parsers/oráculos propios. No hubo motor financiero nuevo ni reconstrucción de cápsulas. Inputs, spools y binarios completos están ligados por `input-cuts.json`/`identity-cut.json` y tabla final del artefacto A. El borrador previo leído por GOD tenía otro blob: no se confunde con esta devolución final.

**Sello:** SHA256 del documento entero `measure/perf-contract-frozen.md`,13977bytes, es `2ee87f94414e3b48d7a48d8c4915c4ed994cf864e5b74702654d3e98569417f7`. Para el bloque: localizar `## PERF_CONTRACT`, primer fence de apertura text posterior y fence de cierre inclusive, sin LF final,3651bytes; SHA256 `7e71aed95548905ded11e898df04aa02fd0c54a2d4d0d8d690f743d0cd9ba984`, igual entre frozen y publicado. Agregar exactamente un LF produce3652bytes y `cfa81c17c7acea7dd78aa80b58e32984230a5e81c65a74009e4d1123d35e08d2`. `measure/perf-contract-seal.sha256` corresponde al documento entero; el hash publicado `ff320f01e9954eefaf84de5380b78e8b99e334d42ac10bf50f018d34ae89079d` no coincide con esos alcances. Se acepta `PUBLISHED_BLOCK_RECEIPT_NOT_REPRODUCIBLE`.

La hora declarada13:20−03 contradice publicación previa; mtime/birth10:16:59−03 y commits control10:12:06/optimización10:28:47 son hechos distintos. A buscó en recibos/logs/reflog acotado y no encontró snapshot/árbol anterior al primer cambio de rendimiento. Adjudicación: `PERF_TARGET_FREEZE_BEFORE_FIRST_PERFORMANCE_CHANGE=NOT_DEMONSTRATED`. Se rechaza la conclusión preliminar de congelamiento cumplido por mtime+DAG. No afirmar que el cambio ocurrió antes: la falta de recibo no prueba la secuencia opuesta. Corrección posterior sólo acredita sus bytes y su fecha, sin retrofecha ni movimiento de objetivos.

**Par R:** el comparador independiente de A usa mapa por namespace y generación observada `btg-functional/BTG_FUNCTIONAL_NQ_EVAL_V1/1`.88362records por extremo,109diferentes; primer delta crudo seq85915/signal_id. Mapa bijectivo de1run/1señal/1solicitud/1operación/9órdenes/9provider_order_ref/6ejecuciones/3command_id/3action_id; gráfico de45referencias sin fusiones, huérfanos ni reasignaciones bajo esa generación. Cuenta/contexto/contrato/estrategia y hojas monetarias/temporales se comparan exactos. `detail` se valida por gramática de admisión+request_id, cuya señal está mapeada; no se ignora la cadena completa. Definiciones, raíz/step/fase y referencias se contrastan sin imponer un orden de publicación de FILL que no sea el causal del motor.

Negativo del propio mapa: fijado el mapa, reasignar sólo `fill.order_id` del primer FILL a otra orden existente conservando dinero y las restantes referencias; rechazo en seq85929. Se acepta `R_TYPED_TRACE_EQUIVALENCE=PASS_BOUNDED_SINGLE_GENERATION`, no una propiedad universal ni igualdad de toda la build.

Integridad distinta de equivalencia: A recomputó CRC/EOF gzip y records/logical SHA según encuadre de8bytes big-endian + JSON exacto; también el SHA de inputs exactos del footer y el RunID derivado. Ambos artefactos R son válidos en esos contratos. Summary/economics COMPLETE, residuales, ledger/risk e input-sequence sellado coinciden; input-sequence se cotejó, no se recomputó desde feed externo. Admisiones/dispositions no presentes en R: igualdad de ausencia no prueba su contrato. Digest provider difiere: control `ff27d84fba6a6febaceebfff0d981b73f3e9278a475ef4a366da7bf821a18993`, candidato `f644d2db0bb28d1eb3f895162ffa9feb02a4e9bb3d2d684920b27231c0187c51`. Sin preimagen tipada final, `PROVIDER_FINAL_STATE_EQUIVALENCE=NOT_DEMONSTRATED`; no eliminar ese hash ni asumir cascada de IDs. Se conserva un gap de evidencia, no un defecto monetario demostrado.

**NQZ5:** input `campaign-NQZ5-optimized.json` SHA256 `89f5f1ece421ecfbabafcf0dfd5347c47197ac8ebe8ecd37698cc2bdd6110b36`, build584a/bin e5d4860b completo fijado arriba; run `bt-c-e4cc8f263b77628887517f57542c5a69c9a06d84cedaec92c4462fd623e41348`, attempt `attempt-dm0ct6ccs13a-bec43c43f142`, rc124. Spool90225184bytes SHA256 `2acbfe38122f18a65b9a5d7d7e7848563ccc83d04c990d3f3ebe804d5304f180`. Oráculo recupera **2764371 objetos completos**, gzip EOF=false y92bytes del siguiente objeto parcial. Rectifica2764372 del preliminar; no contar un objeto incompleto como record válido. Último completo21nov2025 `21:01:45.257142857Z`, root3578967/step2845190; horizonte solicitado27nov18:00Z. Recuperación forense no valida CRC/footer/Close ni permite resume.

| Secuencia NQZ5 comprobada | Evidencia tipada / alcance |
|---|---|
| Reemplazo18nov08:06Z | seq2009468 cuenta1→cuenta2; nominal100000. Primera economics cuenta2 seq2009469/rev3. Se separan generaciones; rev70629 de cuenta1 no se compara con rev3 de cuenta2 como si fuera un hueco |
| Contigüidad de prefijo |80768ECONOMICS:70627 de cuenta1/rev3..70629 y10141 de cuenta2/rev3..10143, sin gaps internos. Inicialización rev1/2 no publicada en ese formato, por lo que no se certifica todo el lifetime |
| PASS latched | seq2342381 MODELED_EVALUATION_PASS/AWAITING_NEXT_CONTEXT; aún EVALUATION |
| Reset aplicado | seq2342382/83,rev4869,−3010,56 de RESET_ADJUSTMENT; balance100000, PnL de evaluación conservado. No es cobro |
| Batch20nov01:55:16.19631902Z | seq2342385/86/87,rev4870 SetAccountContext,4871 CloseStage EVALUATION,4872 OpenStage FUNDED, mismo root3172021; conserva todas las revisiones de ese batch |
| Transición aplicada | seq2342388 pass-funded-2,START_NEW_STAGE/CONTINUE_CURRENT_DAY/REPLACE_EXPLICIT_RISK_SEED; nuevo stage PnL0, día conserva1510,2. No hay OpenAccountDay adicional exigible por CONTINUE_CURRENT_DAY |
| FUNDED posterior | Pausa seq2546048/49,rev7621, stage FUNDED; digest expected-context `c7ec59251a19b4ac003721e9fa52a4f09c188bb99c0cc9385167702b4c922687` recomputado, frente a EVALUATION `409766e3f6fb4995fbeaed7bf9c0876266b6756b65b9402950b7a9701018ae45` |
| Solicitud, admisión y cobros | Solicitud FUNDED inferida desde control aplicado/source; recibo standalone de solicitud y sello de admisión previo no disponibles. Pausa21nov se vincula por source a requestPayout; único ACCOUNT_CASHFLOW recuperado es RESET, no PAYOUT_DEBIT. Cobros/caja final/admisiones/dispositions no certificados sin footer |

Se acepta `NQZ5_PREFIX_TYPED_CHAIN_CORROBORATED`, favorable al repair A y más fuerte que ausencia de error textual. Se rechazan tanto «no alcanzó la transición» como «NQZ5 completo PASS». Publicación lógica FUNDED está corroborada por transición+autoridad posterior; publicación final durable, release completo y cierre íntegro siguen NOT_DEMONSTRATED.

### TOP B — findings adjudicados y evidencia aceptada

Leído íntegro [[BTX-PERF-S03-TOP-B-EVIDENCE]], blob `058b63623a4bd7b2c833831ccf6360c9b5a6dc5c`, SHA256 `7b295e43b5d7866c24d23c6196c0a762d6f36b3127f34bef7452ffccb3378aed`. Paquete externo `aranea/work/btx-perf-s03-top-b-20261009/`; SHASUMS.txt SHA256 `430ee4e2117eff2fa063b268fc930674e44cc9ac4f000c15409476c7a4df1072`. GOD leyó COMMANDS.md, IDENTITY.json y `logs/final-sealed-own.log`; no reejecutó pruebas ni atribuye a su lectura la ejecución del TOP. Source original limpio reportado por TOP; modelos real/consumo UNKNOWN. El artefacto enumera fixtures sintéticos y hashes completos, sin corpus NT nuevo.

| Finding / requisito | Evidencia y primera divergencia | Oráculo / adjudicación |
|---|---|---|
| B-02, CRITICAL — aplicar exactamente el cuerpo admitido | `TestTOPBCashflowUsesFrozenMoney`: admitido USD1 con digest `sha256:4c472c69516c48a53e191ad5987ce4ef052052bfc6a6377daaa866f761e5ec6b`; caller cambia a2; Apply acredita2 y APPLIED usa `sha256:db86e30d877183a5b6f826101209ae06fb72e0c385477f4f8f434baeac342a24`. Otra prueba cambia ExpectedContextDigest tras admisión y causa fallo que el cuerpo congelado no habría causado | DEFECTO_VIGENTE, EXECUTED_RED. Adenda exige payload sellado y dinero exacto. `EnqueueControl` conserva `c` original en pendingControls; C08 obligatorio. No se ha demostrado si fue introducido por optimización o heredado, y eso no altera el rechazo |
| B-01, MAJOR — lectura pública observacional | `TestTOPBAdmissionsReadIsolation`: mutar ContextID a través de `Admissions()` cambia el payload interno; digest original `sha256:c64c6cc65135d1036458e8090e53d380c5152641c00c5ca431f28c74f7533a4d`, cuerpo posterior `sha256:cbaad4812b5ec11d1798f8af930e1e0e658b1603fdbdfb73709fd046696c89af` | DEFECTO_VIGENTE, EXECUTED_RED. Copia superficial del slice no conserva ownership profundo; C09 distinto de C08. El mutador es una prueba adversarial de frontera pública, no una propuesta de uso normal |
| B-03, MAJOR — fondos suficientes antes de compra | `TestTOPBInitialCash119120`: fixture final válido9min, sin trading;119→compra1→−1 USD, HORIZON_REACHED, FailureCode vacío. Control120→compra1→0 USD | DEFECTO_VIGENTE, EXECUTED_RED. C10. Boundary adversarial autorizado no cambia el perfil CAMPAIGN de5000; no extrapolar sobregiro a esa entrada sin prueba. Primer fixture entries0 con error Strategy fue descartado y preservado, no fundamenta el finding |
| Captura/Record y ownership | Cuatro subcasos independientes: fallo Record retiene5 revisiones; borrowed retiene5; owned captura2/libera hasta quedar1; reemplazo artificial del ledger devuelve LEDGER_OWNERSHIP_CHANGED y retiene5 del dueño anterior | PASS_BOUNDED. Prueba guard y conservación del owner capturado; reemplazo a nil no certifica transición real a ledger sucesor ni todas las revisiones día/contexto/stage |
| Close fallido | `TestTOPBRecorderCloseFailure`: Finish devuelve error aunque el Result diagnóstico tenga COMPLETE | PASS_BOUNDED del canal de error; rechazar ese resultado sigue obligatorio. No adjudicar defecto nuevo sólo por el campo sin considerar err. F-S03-04 sí es un RED distinto de salida CLI |
| Protection/finality | Ocho tests Gerard, LONG/SHORT y adverse/pyramid, parciales, ACK/claims, late ADD y cancel de riesgo pendiente, más dos fixtures nativos ALL/SKIP | PASS_BOUNDED a fixtures citados; no broker, no sustitución universal de MM ni equivalencia general ALL/SKIP |
| Lifecycle | FourthRequestPending, ReplacementRestoresEvaluationTerms y oráculo nuevo3burns/4compras/caja4520 PASS | Cuarta solicitud pendiente no cobrada; términos restaurados en reemplazo; dinero de ese fixture conciliado. Cuarto cobro efectivo/residual y reinversión larga quedan NOT_RUN |
| Sustitución/lecturas | Strategy pública stateful:6 callbacks, Encode/Decode consistente y mutación BarRange recibida no cambia lectura siguiente ni historia; requisitos públicosH4 PASS | PASS_BOUNDED; no certifica MM custom stateful/events/timers ni todas las referencias públicas. No contradice B-01 en otra frontera |
| Rollover | API conserva prefijos separados y exige precio propio para orden del retirado | PASS_BOUNDED del núcleo; combinación posición+orden+claim, readiness y entrada multistream integrada siguen pendientes |

La ejecución final propia devuelve rc1 de forma esperada: contiene cuatro tests de defecto rojo para tres causas adjudicadas, además del comparador StructuralReference todavía rojo/no resuelto. No se describe como «todas las pruebas PASS». Los regresores previos reutilizados y las pruebas nuevas permanecen distinguibles en el artefacto B.

### Adjudicación de los cinco rojos históricos

| Test original, sin editar | Clasificación final S03 | Motivo y obligación S04 |
|---|---|---|
| `TestBTGS03_CampaignCashBurnReplacementAndContinuity` | EXPECTATIVA_SUPERSEDIDA | Cuatro quemadas seguidas de una quinta cuenta activa al horizonte son compatibles con recompra ON_DEMAND. El límite de cobros no es un máximo de compras. Ajustar expectativa de fixture sin desactivar recompra |
| `TestBTGS04CampaignBurnCashLedger` | EXPECTATIVA_SUPERSEDIDA | Tres burns requieren cuarta compra cuando hay fondos:4×120→caja4520; exigir3compras/caja4640 omite la sucesora activa. Oráculo independiente B lo demuestra |
| `TestBTGS03_V2IntrabarAddsAdverseAndProtection` | FALLO_HARNESS | Se envía ADD a22:11:06.666…, SL llena a22:11:10 y cancela el ADD pendiente. Dos fills no demuestran «add ausente»; forzar un tercero aquí puede crear exposición huérfana. Fixture adicional debe garantizar paso elegible posterior sin stop anterior |
| `TestBTGS04_MixedMinuteCapabilityBoundary` | EXPECTATIVA_SUPERSEDIDA | API acepta MIXED_MINUTE con modelo explícito y el input sin modelo falla por `ohlc_model`; assertion antigua esperaba modo no soportado. Conservar negativos de modelo/autoridad sin equiparar soporte API con CLI multistream |
| `TestBTGS04_StructuralReferenceSkipFirstDivergence` | NO_RESUELTO | Al mapear provider_order_ref según orden ya bijectada, primera divergencia pasa a cause_ref FILL:sim-exec:ord…:1.74records/rev36 iguales y snapshots semejantes no bastan. Completar mapa referencial ALL/SKIP y negativos en S04; no declarar un bug monetario ni un PASS por inferencia |

Ninguna clasificación borra el rojo original. S04 conserva una prueba que codifique el requisito vigente y trace la sustitución de expectativas obsoletas. El mapa TOP A del par real R es otro experimento y no cierra el quinto test.

### Conciliación S02 frente a la evidencia real

| Afirmación anterior | Adjudicación GOD y evidencia requerida |
|---|---|
| Sello antes de cualquier cambio de rendimiento | Separar igualdad de contenido, binding del recibo y cronología. Publicación antes del commit no prueba ausencia de cambios anteriores sin commit. La hora declarada incompatible se describe como inconsistente; no inferir intención. Una rectificación posterior no acredita congelamiento anterior |
| MIN_SPEEDUP cumplido | Sólo el par R completo sustenta75,77/34,01≈2,23×; se cronometra `run --spec` con preparación separada ya hecha, no prepare+run+replay+comparación. El requisito que también nombra NQU6 completo no queda cerrado por R |
| Ancla NQU6 «no verificada» | FAIL para candidato BASIC frente a180s: las censuras preservadas exceden ese umbral sin completion. No se necesita otra medición para repetir la desigualdad |
| «No regresión» porque ambos exceden timeout | Rechazado como inferencia: dos tiempos censurados no establecen ratio ni equivalencia de duración |
|301911 records hasta21jul en900s; NQZ5 sólo21oct | Cifras sin correspondencia con spools preservados según preliminar; TOP A fija frontera y población. No mezclar records de evidencia, inputs raíz y pasos intrabar |
| Proyección5h = coste necesario | No admitido. Una proyección depende de mezcla de actividad, warmup, exposure y denominador; no es duración completa observada ni inevitabilidad demostrada |
|109 diferencias prueban equivalencia total | La clasificación se conserva; biyección/referencias/negativo propio y header/footer son obligaciones adicionales. El alcance del mapa R no se transfiere a ALL/SKIP ni múltiples generaciones |
| Repair NQZ5 sólo probado sintéticamente | El prefijo real preservado contiene replacement18nov y pass-funded20nov2025; su reconciliación amplía evidencia favorable. No significa salida íntegra ni horizonte completo |
| Ocho fallos idénticos en todos los extremos | Baseline8, candidato5 y tres PASS de clase CLI según detalle: `TestFreshProcessDeterminism`, `TestLargeCorpusStreamingMetrics`, `TestBT_S04_StandaloneReproduceClosedSpec`. «Reparó2» del encabezado/resumen preliminar no concuerda con su propio detalle |
| Pool no requerido porque no domina R | No aceptado como exención. El diseño aceptado exige capacidad de preparación/lectura por stream hasta2 con fallback1 por recursos. Workers∈{1,2} permite ejecutar1; no convierte ausencia de capacidad/concurrencia en implementación del pool |
| TOP preliminar es el Sol solicitado | No demostrado: declara GLM-5.3-Flash/ZCode. Conservar procedencia y auditar evidencia; no renombrar modelo ni invalidar hechos reproducibles sólo por etiqueta |

La corrección documental de estas afirmaciones vive aquí, no reemplaza los originales. E1 permanece PARTIAL_WITH_EVIDENCE y S02 PARTIAL_IMPLEMENTATION_WITH_MATERIAL_GAPS; nada de esta conciliación reinicia esos shots.

### Cuatro gates y cobertura de código separada

| Gate | Estado final adjudicado | Evidencia / límite |
|---|---|---|
| Correctness | FAIL_EXECUTED | B-01/B-02/B-03 vigentes, incluido dinero aplicado distinto del admitido. Biyección R y NQZ5 favorecen alcance acotado; provider/ALL-SKIP y ataques pendientes impiden cierre |
| Performance | FAIL en ancla NQU6 BASIC180s; resto parcial | 2,23× R; no ratio válido de timeouts ni horizonte completo; fundamento/sello insuficientemente acreditados |
| Usabilidad integrada | FAIL_EXECUTED | Multistream obligatorio no implementado; replay CLI CAMPAIGN roto por ambas rutas; portabilidad y rc incorrectos |
| Cobertura histórica de mercado | NOT_DEMONSTRATED para horizonte solicitado | Los prefijos y descriptor no demuestran trayectoria financiera continua multicontrato; NQZ5 atraviesa transición pero no termina |
| Cobertura código/tests, métrica adicional | FLOOR95_NOT_DEMONSTRATED_GLOBAL | S02 reporta58,1% selectivo y69–83% en funciones; no es cobertura global ni porcentaje de mercado |

Denominadores que S04 debe declarar sin intercambiarlos: wall end-to-end en segundos, CPU user+sys en segundos, eventos raíz leídos, pasos intrabar despachados/omitidos y records de evidencia emitidos. Una tasa records/s no se convierte en µs/root-input sin conteos de conversión demostrados para el mismo run. Speedup requiere ambos tiempos completos y mismo workload/completion; throughput integrado requiere modalidades completadas sobre wall conjunto con C financiera1.

Cobertura histórica: numerador de intervalos/observaciones efectivamente consumidos bajo obligación por stream, denominador del ReadPlan esperado para la petición sellada; informar por separado cerrado acreditado, desconocido y no requerido. No usar suma de extremos de trece archivos ni duración nominal como cobertura continua. Frontera causal y primera causa se reportan aunque no exista porcentaje defendible.

Cobertura de código: sentencias cubiertas / sentencias instrumentadas del alcance declarado, con SHA, paquetes y filtros de tests. El95% aplica al alcance de desarrollo acordado y no sustituye caminos críticos. Una ejecución con `-run` selectivo no representa todas las suites. El58,1% se mantiene REPORTED_SELECTIVE por S02: en esta revisión no se recuperó su comando exacto/profile con lista de sentencias, ni se volvió a medir. Es insuficiente para certificar floor global. Los comandos focalizados ejecutados por B sí están preservados en COMMANDS.md; no se inventa una remediación de coverage en S03.

### Paquete cerrado de correcciones S04

Las correcciones siguientes corresponden exclusivamente a S04, vinculadas a causa, owner, regresor RED, aceptación observable y dependencias. Multistream sigue obligatorio; reducir alcance no es una salida autorizada. El paquete cierra la adjudicación S03 tras ambas devoluciones. S04 no está despachado y no se certifica por anticipado una build futura ni se promete que ese shot resolverá todo.

| Prioridad / corrección | Causa y owner de producto | Cambio mínimo exigible, sin fijar implementación | RED / criterio observable | Dependencias |
|---|---|---|---|---|
| P0 C08 Aplicar el cuerpo financiero admitido | `run.go` EnqueueControl/pendingControls/Apply | Retener para aplicación el control tipado congelado al admitir; mutaciones del objeto del caller no alteran importe, contexto ni identidad aplicada | B-02: `TestTOPBCashflowUsesFrozenMoney` y `TestTOPBPendingControlUsesAdmittedBody`; criterio: aplica1 con mismo digest, tiempo/orden sellados y sin doble dinero | Ningún cambio de política económica; conservar APPLIED/REJECTED/CONFLICT/pendiente y negativa por conflicto |
| P0 C09 Frontera pública de admisiones | `run.go` Admissions y ownership de TypedPayload | Entregar vista aislada o inmutable del cuerpo/digest, sin referencias mutables hacia la autoridad interna | B-01: `TestTOPBAdmissionsReadIsolation`; mutar lectura no altera admisión almacenada, digest ni posterior aplicación; extender cashflow/maps/getter post-Finish | C08 debe ser probado aparte; una copia en el getter no corrige el objeto pendiente |
| P0 C10 Asequibilidad de compra inicial | `campaign.go` RunCampaign, primer débito del libro de caja | Aplicar guard de caja suficiente también a la primera compra y conservar término de negocio explícito, sin debit/activación ficticios | B-03: `TestTOPBInitialCash119120` versión válida9min;119 no compra/no sobregiro,120 compra una vez; duplicados sin doble débito | Sin refund inventado ni ajuste del costo120; preservar semántica de compra≠activación |
| P1 C01 Entrada física multistream | `cmd/echo-backtest/experiment.go`, `experiment.go`, `spec.go`, adapter `internal/datasets/ntminute` | Una petición por modalidad resuelve descriptor común, catálogo/schedule y streams físicos; preparación/lectura por stream con buffers acotados y merge estable antes del dominio | F-S03-02; aceptar los dos streams reales y preservar una trayectoria continua. A→B retiene caja/estado y obligaciones de A; orden de llegada no decide dinero | Autoridades físicas/calendario existentes; no fabricar datos ni implementar mediante suma de campañas |
| P1 C02 Pool de preparación | Adapter `ntminute` y preparación integrada | Implementar capacidad admitida hasta dos workers y fallback uno por recursos, con razón registrada, cancelación/backpressure/Close correctos | Workers1/2 y entrega inversa producen mismo orden semántico; worker lento/fallido no causa deadlock ni COMPLETE parcial | C01; no convalidar ausencia por perfil R ni añadir trece procesos financieros |
| P1 C03 Replay CAMPAIGN público | CLI `experiment.go`, `reproduce.go`, `replay.go`, `resultwriter.go` | Manifest enlaza artefacto/spec; detectar y reproducir CAMPAIGN desde metadatos realmente leídos, recomponiendo controlador y comparando disposiciones/caja/residuales | F-S03-03; ambas rutas CLI alcanzan full-driver en caso con burn/recompra y replacement; corrupción material/referencial rechazada; no readmisión externa duplicada | Sello/admisiones válidos; el IDENTICAL bare sin lifecycle no sirve como aceptación |
| P1 C04 Resultado, rutas y cobertura | `experiment.go`, CLI, manifest/finalización | Resolver rutas relativas al out-root y códigos según estado; publicar frontera procesada y ReadPlan, separado del inventario | F-S03-04; mover output conserva replay; FAILED/WARMUP_INCOMPLETE no da rc0; prefijo abortado nunca se presenta como horizonte completo | C03 y contratos de integridad; datos faltantes quedan explícitos |
| P1 C05 Recibos y performance | Autor de evidencia S04, con revisión independiente | Rectificación append-only con receta hash y horas verificables; conservar contrato original y declarar falta de recibo de frontera si persiste. Verificar targets sin moverlos | F-S03-01/05; hash reproducible y trazabilidad; caso completo comparable y ancla180s bajo criterio congelado; no ratio entre censuras | Build corregida/congelada y inputs verificados. No otra optimización autorizada por este dictamen |
| P2 C06 Oráculo legacy e identidad | `native_cli_e2e_test.go` y tooling independiente de verificación | Evitar salida verde anticipada por RunID distinto; comparar contratos relevantes con correspondencia tipada justificada y negativos | F-S03-09; fixture rescatado conserva igualdad y un cambio semántico o referencial se detecta aunque RunID difiera | Mapeo auditado A; no borrado global de IDs ni adaptación al bug |
| P1 C07 Cierre de pruebas críticas/cobertura | TOP independiente de validación S04; owners afectados | Integrar regresores transportables que codifiquen invariantes y cubrir ramas críticas pendientes antes del floor | Tests rojos adjudicados por B y matriz final NOT_RUN; comando/denominador reproducible de coverage; no tests cosméticos | Repairs anteriores y final diff congelado; S03 no certifica S04 |
| P1 C11 Equivalencia final y StructuralReference | Owners de estado provider, evidencia y harness ALL/SKIP | Exponer/recuperar preimagen tipada final y completar mapa por namespace/generación/causa para ese par; adjudicar diferencias antes de cambiar producto | `compare_r.py` conserva negativo seq85929; `TestTOPBStructuralReferencesBijection` sigue RED en cause_ref. Precio, swap de refs, colisión/huérfano deben ser rechazados; estado final no se aprueba por hash ignorado | C06; registrar gap como evidencia pendiente, no bug financiero ya probado |
| P2 C12 Expectativas de fixtures históricos | Owners de tests de campaña/V2/MIXED | Corregir únicamente expectativas adjudicadas y crear casos que alcancen ADD posterior elegible; mantener originales/recibos en historia | Tabla de cinco rojos: ON_DEMAND3burns/4compras4520, pending ADD cancelado por SL, MIXED sin modelo falla; todos con oráculos causales | No alterar política/código para satisfacer expectativas supersedidas; StructuralReference se resuelve mediante C11 |

Los propietarios son áreas de código, no autorización a este GOD o a los TOPs S03 para editarlas. La elección local de implementación permanece con el integrador S04 dentro de los contratos congelados; Primary recibe el paquete para dirigir ese shot.

### Matriz de validación final posterior a las correcciones

| Prueba aún no acreditada de la futura build | Motivo para no ejecutarla ahora | Oráculo y gate |
|---|---|---|
| BASIC y CAMPAIGN integrados multicontrato por CLI | Entrada física rechazada; falta implementación C01/C02 | Trayectoria única, readiness/gaps explícitos, identidad de expiries, obligaciones retiradas y caja continua; correctness/usabilidad/histórico |
| Workers1/2, entrega inversa, empates, lento/falla/cancelación/buffers llenos | Pool ausente; no construirlo dentro de S03 | Merge estable, sin adelanto de HLCV, no deadlock, no COMPLETE parcial, recursos cerrados; correctness/usabilidad/performance |
| Replay público CAMPAIGN con lifecycle y ambos enrutados | C03 pendiente y candidato ya RED | Controlador idéntico, dinero/disposiciones/residual íntegros, negativos materiales/referenciales, rutas movidas; correctness/usabilidad |
| NQZ5 completo con cierre/integridad/replay | Spools censurados, sin checkpoint restaurable; nueva corrida larga prohibida en S03 | Desde inputs autorizados en build corregida: revisiones/cuenta/generación reconciliadas, footer/checksum/Close válidos y replay completo; correctness/histórico |
| Anclas NQU6 y horizonte completo/ratios/RSS/throughput | Candidato no satisface ancla y superficies necesarias ausentes; no medir otra vez para confirmar180s | Protocolo comparable con bin/input/completion iguales; wall/CPU/RSS y denominadores explícitos; performance |
| Cobertura histórica total | No ReadPlan integrado consumido de extremo a extremo; descriptor no es ejecución | Expected/observed/closed/unknown/not-required por stream/obligación; primera frontera desconocida falla explícita; histórico |
| Suite global y floor95 de desarrollo | S03 sólo pruebas focalizadas; resultados previos selectivos | Todas las suites afectadas con clasificación de rojos, caminos críticos y denominador explícito; cobertura código separada |

Cada NOT_RUN adicional de A/B se conserva en la matriz específica siguiente. No se exige una ejecución imposible sobre interfaz ausente ni se borra la obligación por ese motivo. El rechazo del candidato es definitivo para este corte con cobertura parcial; la aceptación futura necesita las pruebas correspondientes a la build final.

| Obligación focal pendiente | Por qué la evidencia actual no basta | Oráculo posterior / dependencia / gate |
|---|---|---|
| Timer intrabar→callback→orden y rearme | Test de timer/control PASS no cubre orden nueva desde callback ni fill retrospectivo adversarial | LONG/SHORT y ALL/SKIP: submit después de causa, drain completo, fill sólo en observación posterior elegible; C07/correctness |
| Batch día/contexto/stage con sucesor real y reentrancia | S02 y NQZ5 cubren casos concretos; B usa reemplazo a nil para guard, no swap completo de generación | Todas las revisiones comprometidas capturadas; vistas finales coherentes; no liberación prestada/cruzada; igualdad corriente intacta, también fallos primer/intermedio/último Record y Close; C07/correctness |
| Sello en todas las disposiciones y post-Finish | R no tiene controles; tests previos de duplicate/reject/pending no prueban ownership profundo; B-01/B-02 son RED | APPLIED/REJECTED/CONFLICT/pendiente con cuerpo/digest original recuperable y dinero una vez; mutaciones de caller/getter/nested maps no alteran autoridad; C08/C09/correctness+replay |
| Cuarto cobro efectivo, residual y reinversión larga | FourthRequestPending pasa, pero no prueba cuarto cobro/retirada/residual; NQZ5 no conserva footer de caja | Caja=inicial−compras aplicadas+cobros netos aplicados; residual separado y no reinvertible, compra≠activación; mantener costo/fees/reglas; C07/C10/correctness |
| MM y Strategy custom con events/timers y estado | Strategy de B verifica6 callbacks y lectura, no conjunto events/timers de MM ni continuidad bajo rollover/replacement | Módulos públicos sin ifGerard, callbacks/estado preservados, lecturas observacionales; C07/correctness |
| Rollover completo posición+orden+claim/readiness | Núcleo preserva orden retirada y prefijos, pero combinación completa y merge CLI ausentes | Identidad/year/month propia, obligación retirada resuelta con su precio, candidato no elegible antes de readiness, caja/Strategy continuas; C01/C07/correctness+histórico |
| Provider final y ALL/SKIP | Digest opaco distinto y cause_ref todavía no mapeada; mapas R de una generación no cubren estos pares | Preimagen final tipada, biyección por generación y referencias, colisión/swap huérfano rechazados conservando dinero; C11/correctness |
| Input-sequence de R reconstruida desde feed | Coincidencia del digest sellado no es recomputación externa; SHA de inputs de footer sí verificado | Encuadre real de inputs consumidos, dato/fase/orden concordantes y mismo digest; C07/integridad |
| Race y alcance global de tests | `-race` sólo reportado por S02; no ejecutado por nuevos TOPs. Coverage selectivo no global | Ejecutar sobre build final congelada y owners afectados; zero races observadas no prueba universal de thread safety; C07/cobertura código |

Las tareas analíticas no resueltas se entregan a la validación independiente de S04, sin reabrir TOP A/B ni crear un tercer especialista S03. No se convierte la ausencia de recibo pre-cambio en una reparación histórica posible: si no aparece evidencia anterior auténtica, ese límite de F-S03-01 permanece para Primary/Owner.

### Denominadores, comandos y reutilización verificable

Recibos R originales `logs/run-control-R.stderr.log` y `logs/run-opt-R.stderr.log` cronometran `echo-backtest-control run --spec prepared-control/runspec.json ...` y `echo-backtest-optimized run --spec prepared-optimized/runspec.json ...`, con descriptor NQU6 común y outputs separados. GOD leyó las líneas `Command being timed`, user/sys/wall/maxRSS y TOP A liga los archivos completos por hash. Preparación separada, replay y comparación no están dentro de esos tiempos. Cierre/escritura realizados dentro del proceso run pertenecen a ese tiempo; no se conoce un total end-to-end de verificación por sumar duraciones no conservadas.

| Magnitud R | Control | Candidato | Alcance |
|---|---:|---:|---|
| Wall del proceso run |75,77s|34,01s| Ratio2,22787415466×, R únicamente |
| CPU user+sys |128,24+13,55=141,79s|45,80+2,89=48,69s| CPU no wall |
| maxRSS |61840KiB=60,3906MiB|55788KiB=54,4805MiB| Proceso medido, no histórico completo |
| Root inputs |1674851|1674851|45,2399 frente a20,3063µs/root-input; no sustituir por records |
| Records emitidos |88362|88362|857,495 frente a384,893µs/record; población distinta |

Comandos de verificación **ejecutados por TOP A**, CWD home autorizado; scripts y hashes viven en su paquete. Se conservan para reproducción, no se ejecutaron por GOD:

```sh
timeout 120s python3 aranea/work/btx-perf-s03-top-a-20261009/receipts.py
timeout 120s python3 aranea/work/btx-perf-s03-top-a-20261009/compare_r.py
timeout 300s python3 aranea/work/btx-perf-s03-top-a-20261009/prefix.py
timeout 120s python3 aranea/work/btx-perf-s03-top-a-20261009/check_prefix.py
```

TOP B ejecutó desde su `overlay/v3`, entre otros comandos literales conservados en COMMANDS.md:

```sh
timeout 120s go test ./backtester -run '^(TestBTGS03_CampaignCashBurnReplacementAndContinuity|TestBTGS03_V2IntrabarAddsAdverseAndProtection|TestBTGS04CampaignBurnCashLedger|TestBTGS04_MixedMinuteCapabilityBoundary|TestBTGS04_StructuralReferenceSkipFirstDivergence)$' -count=1 -v
timeout 120s ../../bin/backtester.test -test.run '^TestTOPB' -test.v
```

La segunda línea usa el localizador relativo equivalente al binario absoluto de COMMANDS.md; CWD y bin SHA45ba14ba completo fijado en identidades. Logs `five-reds.log` y `final-sealed-own.log` rc1 esperado; no se confunde fallo de aserción con rechazo del harness. El bin Gerard retenido fue compilado después del `go test` y no se le atribuye falsamente la ejecución de ese comando.

Para coverage final **NOT_RUN en S03**, receta de S04 desde el checkout corregido/congelado `v3`, con `S04_OUT` fuera del árbol y procesos financieros seriales:

```sh
go test -count=1 -covermode=atomic -coverprofile="$S04_OUT/backtester-futures.cover" ./backtester/... ./sdk/futures/...
go tool cover -func="$S04_OUT/backtester-futures.cover"
```

La lista explícita define el alcance de esa medición, no «todo Echo». S04 debe conservar stdout/rc/profile, lista de paquetes/sentencias instrumentadas y subconjunto nuevo/modificado contra control/candidato, además de cobertura de caminos críticos. Si quedan owners modificados fuera de esa lista se incluyen de forma explícita antes de medir; no se ocultan ni se promedia un paquete para dar floor global. Cualquier fail/skip/timeout permanece reportado. Estos comandos son criterio futuro, no autorización de ejecución desde esta sesión ni nueva evidencia verde.

Assets a conservar por el integrador S04: B propone regresores permanentes para getters/controles congelados/dinero119–120/Record/Close; E2E candidates para ON_DEMAND y Strategy stateful. A aporta `compare_r.py` y recuperación forense como HARNESS_TOOLKIT_CANDIDATE, y `check_prefix.py` como E2E_CANDIDATE fechado. Diagnóstico ADD y mutaciones en memoria son DISPOSABLE_REPRODUCER; el comparador ALL/SKIP parcial no debe promoverse como correcto antes de C11. No integración mecánica por GOD ni promoción automática al producto.

### Delta adjudicado para Primary

Actualizar BTG-PLAN mediante su único owner: S03 dictamen entregado RED/READY_FOR_PRIMARY_REVIEW, cobertura ejecutada parcial explícita. Aceptar B-01/B-02/B-03 como defectos vigentes, conservar F-S03-02/03/04 y ancla BASIC180s FAIL. Rectificar sello a freeze-pre-cambio NOT_DEMONSTRATED, R a run-only2,2279×, NQZ5 a prefijo reconciliado2764371objetos completos y cinco rojos a3supersedidos/1harness/1no resuelto. Preservar provider/input-sequence/ALL-SKIP y matriz causal/lifecycle/rollover/race/coverage pendientes. S04 recibe C01–C12, sin despacho por GOD ni aceptación adelantada. Primary permanece abierto y FINAL_OWNER_ACCEPTANCE=NOT_GRANTED.

### Persistencia y cierre

Documento nuevo materializado por `80-agents/skills/_shared/scripts/materialize_schema_note.py doc` según contrato vigente. BTG-PLAN, el preliminar, el informe S02 y el PERF_CONTRACT permanecen intactos. Sus blobs se comprobaron nuevamente sin delta. Se cierra únicamente este encargo S03: ambos TOPs devueltos/cerrados, cero procesos propios pendientes reportados, ningún código o test escrito por GOD y ninguna ejecución S04. Primary sigue abierto; registros/feedback por delta separados y sin L0 inventado. La sincronización automática publicó versiones de trabajo explícitamente DRAFT; el corte final/readback determina el dictamen entregado.

## Fuentes

- Despacho Owner BTX-PERF-S03-GOD de2026-10-09 y adenda incorporada en [[BTX-PERF-DESIGN]].
- [[BTG-PLAN]], [[BTX-PERF-DESIGN]], [[BTX-PERF-IMPLEMENTATION]], [[BTX-PERF-S03-TOP-EVIDENCE]], con blobs fijados en este documento.
- `xKoRx/echo`, rama `codex/btx-perf-s02`, README canónico `v3/backtester/README.md`; interfaz anunciada contrastada con F-S03-02/03/04.
- Evidencia externa al vault bajo Daedalus `aranea/work/btx-perf-s03-top-20261009/`, `aranea/work/btx-perf-s02-20261009/`, `aranea/work/btx-perf-s01-e1-20261008/` y `aranea/work/btg-s06-user-oneshot-20261008/`, relativas al home autorizado Owner; no son copias dentro de Agents-OS.
