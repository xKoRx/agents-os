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
DOCUMENT_STATE = DRAFT_WAITING_FOR_TOP_EVIDENCE
PROGRAM = BTX-PERF
SHOT = S03_CONTINUATION
CANDIDATE_GLOBAL_PASS = REJECTED_BY_EXISTING_EXECUTED_RED
S03_GOD_ADJUDICATION = WAITING_FOR_TOP_EVIDENCE
S03_TEST_COVERAGE = PARTIAL
S04 = NOT_STARTED_PRESERVED
PRIMARY_SESSION = OPEN
FINAL_OWNER_ACCEPTANCE = NOT_GRANTED
```

El rechazo del candidato ya tiene fundamento en la entrada multistream ausente y las dos rutas públicas de replay CAMPAIGN rotas. El dictamen final aún requiere revisar las devoluciones despachadas; una fila pendiente no se convierte en prueba realizada por el hecho de que exista ese rechazo.

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

584a→bbb cambia README y test de ring según recibos preliminares; no convierte al binario medido 584a en un binario bbb. Cada nuevo TOP debe fijar su fuente/overlay/inputs/binarios por separado. Ningún tiempo S02 se atribuye a una compilación de S03.

### Despacho y atribución

La superficie efectiva de esta conversación expone shell local, archivos Daedalus y `collaboration.spawn_agent`; la etiqueta CLOUD del encargo no se utilizó para negar herramientas existentes. Los directorios Owner se comprobaron disponibles. Los dos despachos usaron `fork_turns=none`, modelo solicitado `gpt-6.1-sol`, sin autorizar subdelegación. El harness recibió explícitamente ese selector; la identidad real de ejecución sólo se acreditará con el recibo disponible y, si no se expone, permanece UNKNOWN. Modelo real GOD y consumo Pro no expuestos: UNKNOWN; el rol pedido no prueba el modelo servido.

| TOP | Pregunta | Límite operativo fijado por GOD | Estado |
|---|---|---|---|
| A, `/root/top_a_evidence` | Recibos/sello, biyección tipada y negativo referencial, NQZ5 preservado | 35min de tarea; comandos pequeños ≤120s; lectura forense ≤300s por spool; cero ejecución financiera nueva | DISPATCHED_WAITING |
| B, `/root/top_b_safety` | Safety/contratos compartidos y adjudicación de cinco tests rojos | 35min de tarea; ≤120s por comando y ≤12min agregados de ejecución; único ejecutor financiero | DISPATCHED_WAITING |

Son límites operativos de este despacho, no una concesión Owner de 180min/4h ni un nuevo deadline. No se reabre el ejecutor preliminar. Cada TOP tiene un artefacto distinto y una única devolución final; GOD es el escritor documental de publicación. Nada de clones completos por worker, export NT nuevo, lote13×, corridas históricas300/600/900s, perfiles o reparación de producto.

El preliminar conserva `MODEL_REPORTED=GLM-5.3-Flash`, superficie reportada ZCode, `REQUESTED_ROLE=TOP`, `REQUESTED_MODEL_COMPLIANCE=NOT_DEMONSTRATED`. El título TOP LOCAL no cambia ese recibo. Las pruebas reproducibles se evalúan por sus inputs, oráculos y resultados; no se descartan sólo por el modelo.

### Evidencia preliminar aceptada y reservas

| ID | Aporte admitido | Reserva / conclusión que no se admite |
|---|---|---|
| F-S03-01 | Bytes del bloque reportados iguales en copia/publicación anterior al commit de optimización; recibos hash/hora inconsistentes | mtime y commit no prueban la frontera del primer cambio. No aceptar PERF_TARGET_FREEZE cumplido ni atribuir falsificación intencional. Receta y frontera pendientes A |
| F-S03-02 | Dos streams físicos reales rechazados en BASIC y CAMPAIGN por `experiment`, rc2 | Defecto de implementación, no falta externa de datos; no volver a ejecutar sin duda material |
| F-S03-03 | Manifest CAMPAIGN sin Artifact; `--result` enruta antes de drenar footer lazy; ambas rutas CLI no alcanzan controlador | IDENTICAL bare sin replacement no certifica replay de campaña; fixture API no certifica CLI |
| F-S03-04 | Out-root movido rompe rutas; rc0 con FAILED/WARMUP_INCOMPLETE | Coverage de descriptor no acredita mercado consumido; precisar mapeo de estado/rc en S04 |
| F-S03-05 | Par R completo75,77s→34,01s; censuras NQU6 exceden180s | Beneficio R acotado; dos timeouts no prueban no-regresión,5h no es tiempo completo observado y omisión del pool no se convalida por R |
| F-S03-06 | Prefijo NQZ5 alcanza replacement18nov y pass-funded20nov2025, progresa hasta21nov | No completo, no footer ni checksum íntegro; conciliación contable pendiente A, nunca resume desde spool |
| F-S03-07 | 88362 records por lado,109 records con diferencias en IDs/refs; mutación de precio rechazada | Clasificación no prueba biyección ni rechazo de refs intercambiadas; no aceptar «verificación cerrada» sin A |
| F-S03-08 | Nueve regresores S02 y840 sondas findSource; estabilidad de ventanas en bordes ejercitados | No prueba universal de inmutabilidad pública, callbacks o race |
| F-S03-09 | Oráculo independiente rescata fixture legacy, sin diferencias de records | El test del producto sigue abandonando antes de comprobar; no queda reparado por un test externo |
| F-S03-10 | Recibos reportan baseline8fallos y candidato5; tres tests CLI pasan | Encabezado/resumen «reparó2» inconsistente; atribución de cinco rojos pendiente B; preexistencia no prueba seguridad |

No se repitieron F1/F2/F3 para fabricar confirmación redundante. Estos RED se aceptan como resultados atribuidos al ejecutor preliminar con localizadores y alcance descritos, no como pruebas corridas por GOD.

### Conciliación S02 frente a la evidencia real

| Afirmación anterior | Adjudicación GOD y evidencia requerida |
|---|---|
| Sello antes de cualquier cambio de rendimiento | Separar igualdad de contenido, binding del recibo y cronología. Publicación antes del commit no prueba ausencia de cambios anteriores sin commit. La hora declarada incompatible se describe como inconsistente; no inferir intención. Una rectificación posterior no acredita congelamiento anterior |
| MIN_SPEEDUP cumplido | Sólo el par R completo sustenta75,77/34,01≈2,23×; el requisito que también nombra NQU6 completo no queda cerrado por R |
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

| Gate | Estado al corte preliminar | Evidencia / límite |
|---|---|---|
| Correctness | NOT_CLOSED | Advances A–D acotados; faltan biyección, conciliación completa y ataques críticos, además de cinco rojos por adjudicar |
| Performance | FAIL en ancla NQU6 BASIC180s; resto parcial | 2,23× R; no ratio válido de timeouts ni horizonte completo; fundamento/sello insuficientemente acreditados |
| Usabilidad integrada | FAIL_EXECUTED | Multistream obligatorio no implementado; replay CLI CAMPAIGN roto por ambas rutas; portabilidad y rc incorrectos |
| Cobertura histórica de mercado | NOT_DEMONSTRATED para horizonte solicitado | Los prefijos y descriptor no demuestran trayectoria financiera continua multicontrato; NQZ5 atraviesa transición pero no termina |
| Cobertura código/tests, métrica adicional | FLOOR95_NOT_DEMONSTRATED_GLOBAL | S02 reporta58,1% selectivo y69–83% en funciones; no es cobertura global ni porcentaje de mercado |

Denominadores que S04 debe declarar sin intercambiarlos: wall end-to-end en segundos, CPU user+sys en segundos, eventos raíz leídos, pasos intrabar despachados/omitidos y records de evidencia emitidos. Una tasa records/s no se convierte en µs/root-input sin conteos de conversión demostrados para el mismo run. Speedup requiere ambos tiempos completos y mismo workload/completion; throughput integrado requiere modalidades completadas sobre wall conjunto con C financiera1.

Cobertura histórica: numerador de intervalos/observaciones efectivamente consumidos bajo obligación por stream, denominador del ReadPlan esperado para la petición sellada; informar por separado cerrado acreditado, desconocido y no requerido. No usar suma de extremos de trece archivos ni duración nominal como cobertura continua. Frontera causal y primera causa se reportan aunque no exista porcentaje defendible.

Cobertura de código: sentencias cubiertas / sentencias instrumentadas del alcance declarado, con SHA, paquetes y filtros de tests. El95% aplica al alcance de desarrollo acordado y no sustituye caminos críticos. Una ejecución con `-run` selectivo no representa todas las suites. Los comandos y denominadores exactos preservados deberán ser citados por los TOPs; no se inventa una remediación de coverage en S03.

### Paquete S04 y validación final — preparación pendiente de TOPs

Las correcciones de producto corresponden exclusivamente a S04 y deberán quedar vinculadas a la causa, owner, regresor RED, aceptación observable y dependencias. Multistream sigue obligatorio; reducir alcance no es una salida autorizada. El paquete se cerrará después de revisar las dos devoluciones. S04 no está despachado y no se certifica por anticipado una build futura.

| Prioridad / corrección | Causa y owner de producto | Cambio mínimo exigible, sin fijar implementación | RED / criterio observable | Dependencias |
|---|---|---|---|---|
| P0 C08 Aplicar el cuerpo financiero admitido | `run.go` EnqueueControl/pendingControls/Apply | Retener para aplicación el control tipado congelado al admitir; mutaciones del objeto del caller no alteran importe, contexto ni identidad aplicada | TOP B reporta cashflow admitido USD1, caller mutado USD2, Apply acredita2. Regresor y hashes pendientes revisión de artefacto final; criterio: se aplica1 con mismo digest y sin doble dinero | Ningún cambio de política económica; conservar APPLIED/REJECTED/CONFLICT/pendiente y negativa por conflicto |
| P0 C09 Frontera pública de admisiones | `run.go` Admissions y ownership de TypedPayload | Entregar vista aislada o inmutable del cuerpo/digest, sin referencias mutables hacia la autoridad interna | TOP B reporta modificación por getter corrompiendo sello; criterio: cambios en la lectura no alteran admisión almacenada, digest ni posterior aplicación | C08 debe ser probado aparte; una copia en el getter no corrige el objeto pendiente |
| P0 C10 Asequibilidad de compra inicial | `campaign.go` RunCampaign, primer débito del libro de caja | Aplicar guard de caja suficiente también a la primera compra y conservar término de negocio explícito, sin debit/activación ficticios | TOP B reporta119/120→una compra y caja−1;120/120→caja0. Criterio:119 no compra/no sobregiro,120 compra una vez; duplicados sin doble débito | Sin refund inventado ni ajuste del costo120; preservar semántica de compra≠activación |
| P1 C01 Entrada física multistream | `cmd/echo-backtest/experiment.go`, `experiment.go`, `spec.go`, adapter `internal/datasets/ntminute` | Una petición por modalidad resuelve descriptor común, catálogo/schedule y streams físicos; preparación/lectura por stream con buffers acotados y merge estable antes del dominio | F-S03-02; aceptar los dos streams reales y preservar una trayectoria continua. A→B retiene caja/estado y obligaciones de A; orden de llegada no decide dinero | Autoridades físicas/calendario existentes; no fabricar datos ni implementar mediante suma de campañas |
| P1 C02 Pool de preparación | Adapter `ntminute` y preparación integrada | Implementar capacidad admitida hasta dos workers y fallback uno por recursos, con razón registrada, cancelación/backpressure/Close correctos | Workers1/2 y entrega inversa producen mismo orden semántico; worker lento/fallido no causa deadlock ni COMPLETE parcial | C01; no convalidar ausencia por perfil R ni añadir trece procesos financieros |
| P1 C03 Replay CAMPAIGN público | CLI `experiment.go`, `reproduce.go`, `replay.go`, `resultwriter.go` | Manifest enlaza artefacto/spec; detectar y reproducir CAMPAIGN desde metadatos realmente leídos, recomponiendo controlador y comparando disposiciones/caja/residuales | F-S03-03; ambas rutas CLI alcanzan full-driver en caso con burn/recompra y replacement; corrupción material/referencial rechazada; no readmisión externa duplicada | Sello/admisiones válidos; el IDENTICAL bare sin lifecycle no sirve como aceptación |
| P1 C04 Resultado, rutas y cobertura | `experiment.go`, CLI, manifest/finalización | Resolver rutas relativas al out-root y códigos según estado; publicar frontera procesada y ReadPlan, separado del inventario | F-S03-04; mover output conserva replay; FAILED/WARMUP_INCOMPLETE no da rc0; prefijo abortado nunca se presenta como horizonte completo | C03 y contratos de integridad; datos faltantes quedan explícitos |
| P1 C05 Recibos y performance | Autor de evidencia S04, con revisión independiente | Rectificación append-only con receta hash y horas verificables; conservar contrato original y declarar falta de recibo de frontera si persiste. Verificar targets sin moverlos | F-S03-01/05; hash reproducible y trazabilidad; caso completo comparable y ancla180s bajo criterio congelado; no ratio entre censuras | Build corregida/congelada y inputs verificados. No otra optimización autorizada por este dictamen |
| P2 C06 Oráculo legacy e identidad | `native_cli_e2e_test.go` y tooling independiente de verificación | Evitar salida verde anticipada por RunID distinto; comparar contratos relevantes con correspondencia tipada justificada y negativos | F-S03-09; fixture rescatado conserva igualdad y un cambio semántico o referencial se detecta aunque RunID difiera | Mapeo auditado A; no borrado global de IDs ni adaptación al bug |
| P1 C07 Cierre de pruebas críticas/cobertura | TOP independiente de validación S04; owners afectados | Integrar regresores transportables que codifiquen invariantes y cubrir ramas críticas pendientes antes del floor | Tests rojos adjudicados por B y matriz final NOT_RUN; comando/denominador reproducible de coverage; no tests cosméticos | Repairs anteriores y final diff congelado; S03 no certifica S04 |

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

Cada NOT_RUN de A/B se agregará a esta matriz con requisito y regresor pertinente. No se exige una ejecución imposible sobre interfaz ausente ni se borra la obligación por ese motivo. El rechazo del candidato puede ser definitivo con cobertura parcial; la aceptación futura necesita las pruebas correspondientes a la build final.

### Persistencia y cierre

Documento nuevo materializado por `80-agents/skills/_shared/scripts/materialize_schema_note.py doc` según contrato vigente. BTG-PLAN, el preliminar, el informe S02 y el PERF_CONTRACT permanecen intactos. Esta versión de trabajo no es todavía el dictamen final ni un cierre del encargo.

## Fuentes

- Despacho Owner BTX-PERF-S03-GOD de2026-10-09 y adenda incorporada en [[BTX-PERF-DESIGN]].
- [[BTG-PLAN]], [[BTX-PERF-DESIGN]], [[BTX-PERF-IMPLEMENTATION]], [[BTX-PERF-S03-TOP-EVIDENCE]], con blobs fijados en este documento.
- `xKoRx/echo`, rama `codex/btx-perf-s02`, README canónico `v3/backtester/README.md`; interfaz anunciada contrastada con F-S03-02/03/04.
- Evidencia externa al vault bajo Daedalus `aranea/work/btx-perf-s03-top-20261009/`, `aranea/work/btx-perf-s02-20261009/`, `aranea/work/btx-perf-s01-e1-20261008/` y `aranea/work/btg-s06-user-oneshot-20261008/`, relativas al home autorizado Owner; no son copias dentro de Agents-OS.
