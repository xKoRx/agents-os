---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTX-PERF-DESIGN]]"
  - "[[BTX-PERF-IMPLEMENTATION]]"
  - "[[BTX-PERF-S03-TOP-EVIDENCE]]"
  - "[[BTG-S05-REMEDIATION-AND-RESULTS]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-05"
updated: "2026-10-09"
---

# BTG-PLAN — Estado vigente y continuidad del backtester

## Propósito

Control único de BTX-PERF para [[Echo Futures]]: cuatro shots, una trayectoria financiera integrada por modalidad, dominio runtime compartido y módulos sustituibles. Correctness, performance, usabilidad integrada y cobertura histórica son obligaciones separadas; cobertura de tests es otra medida, no el porcentaje de mercado procesado. Primary coordina, no implementa ni acepta producto.

Esta edición recibe la falsificación preliminar S03 aportada por Owner y prepara GOD independiente dirigiendo TOPs. El control anterior íntegro se preserva en Git `88e92e98de735dec8a0fa5832babf418c57c340c`, mismo path. No se modifican informe S02, PERF_CONTRACT, informe preliminar, RED o recibos originales. La arquitectura de [[BTX-PERF-DESIGN]] y la adenda Owner siguen vigentes; esta recepción no crea otro shot ni reduce requisitos.

## Contenido

### Estado vigente — recepción del subartefacto S03

```text
PROGRAM = BTX-PERF
PRIMARY_SESSION = OPEN_UNTIL_EXPLICIT_OWNER_CLOSE
S01_TECHNICAL_DESIGN = ACCEPTED_FOR_IMPLEMENTATION_WITH_EXPLICIT_PERF_EXCEPTION
E1 = PARTIAL_WITH_EVIDENCE
S02_PRIMARY_ADJUDICATION = PARTIAL_IMPLEMENTATION_WITH_MATERIAL_GAPS
S02_COMPLETE_IMPLEMENTATION_ACCEPTED = NO
S03_PRELIMINARY_EVIDENCE = RECEIVED_ACCEPTED_INPUT_BOUNDED_WITH_QUALIFICATIONS
S03_PRELIMINARY_EXECUTION = REPORTED_EXECUTED_RED_WITH_LOCAL_RECEIPTS
S03_GOD_ADJUDICATION = NOT_YET_DELIVERED
S03_EXECUTED_TEST_COVERAGE = PARTIAL_NOT_RUN_ITEMS_EXIST
CURRENT_ACTION = OWNER_RUN_FRESH_GOD_CLOUD_S03_COORDINATOR_PROMPT
NEW_TOP_DISPATCHES_FROM_THIS_PRIMARY_TURN = NONE
S04 = PRESERVED_CORRECTION_AND_FINAL_VALIDATION_NOT_STARTED
PERF_TARGET_FREEZE = REQUIRED_BEFORE_FIRST_OPTIMIZATION_CHANGE
PERF_CONTRACT_SUFFICIENT_JUSTIFICATION = NOT_ACCEPTED_BY_PRIMARY
FINAL_OWNER_ACCEPTANCE = NOT_GRANTED
PRODUCT_CODE_TESTS_PROFILES_BACKTESTS_BY_PRIMARY = NONE
PHYSICAL_RUNTIME_READINESS = NOT_DEMONSTRATED_OUT_OF_SCOPE
PROMOTION = NOT_ACCEPTED_NO_MERGE_OR_DEPLOY
```

Owner solicita revisar esta entrega y, si sirve, entregar el prompt GOD de S03 comandando TOPs; reitera que GOD no desarrolla. Primary acepta el documento como evidencia preliminar útil, con reservas explícitas, suficiente para dirigir el dictamen independiente y las pruebas pendientes. No es aceptación indiscriminada de sus conclusiones ni S03 completo. Primary leyó informe y control remotos, no ejecutó pruebas ni inspeccionó bytes de los spools locales.

### Evidencia recibida y rectificaciones al corte anterior

Informe `BTX-PERF-S03-TOP-EVIDENCE.md`, leído en Agents-OS `88e92e98de735dec8a0fa5832babf418c57c340c`, blob Git `cf21581c5cee5d90035e602456619e1eda2e7c0d`. El handoff menciona sync32d8d6d0 y SHA256 abreviado51f2a1d2; no confundirlos con el blob Git ni inventar el SHA256 completo. Paquete local referenciado: `aranea/work/btx-perf-s03-top-20261009/`, relativo al home autorizado de Daedalus, con RECEIPTS/SHASUMS/logs/overlay/inputs/outputs/binario. Cero procesos propios y checkout limpio son reportes del ejecutor, no sondeos realizados por Primary.

| Aspecto | Estado útil recibido / adjudicación de recepción |
|---|---|
| Multistream | F-S03-02 reporta RED ejecutado con dos streams físicos reales en ambas modalidades. Confirma la carencia M1; no falta externa de datos. |
| Replay CAMPAIGN | F-S03-03 reporta manifest sin Artifact y enrutado --result que lee footer lazy antes del drain. Ambas rutas CLI no alcanzan el controlador; IDENTICAL bare sin reemplazos no acredita campaña. M2 ampliado. |
| Portabilidad/estado | F-S03-04 reporta rutas absolutas rotas al mover out-root y rc0 con FAILED/WARMUP_INCOMPLETE. Coverage del descriptor no equivale a cobertura procesada. |
| Rendimiento | Recibos R respaldan el par75,77s→34,01s; no extrapolar2,23x a CAMPAIGN o multianual. Ancla NQU6 BASIC180s FAIL según censuras verificadas por el ejecutor. Otros ratios/horizontes no demostrados; dos timeouts no demuestran no-regresión. |
| NQZ5 | Rectificación M6: el informe preliminar encuentra reemplazo18nov y pass-funded20nov2025 a01:55Z en spool del candidato, sin error de release observado y con progreso posterior hasta21nov. Ya no afirmar que toda evidencia quedó en21oct. Prefijo censurado/truncado: falta reconciliación tipada, integridad final y horizonte completo; no PASS completo. |
| IDs |88362records por artefacto,109records diferentes sólo en hojas IDs/refs y mutación material de fill_price rechazada según prueba independiente. Clasificación útil, pero aún falta mapa uno-a-uno con referencias preservadas y falsificación del mapa; no declarar equivalencia completa por nombre de campo. |
| Ring/índice |840sondas de paridad findSource y estabilidad de ventanas en los bordes ejercitados; no defecto encontrado en ese alcance. No prueba universal de inmutabilidad pública o race. |
| Legacy |El oráculo independiente rescata el fixture entre builds; el Logf+return del test de producto sigue siendo una debilidad, no queda reparado por una prueba externa. |
| Cinco rojos vivos |Detalle/handoff:8fallos baseline,5candidato,3reparados. Encabezado y resumen del propio informe todavía dicen2: reconciliar por recibos y nombres. Preexistente no significa aceptado; contrastar expectativas con autoridad vigente, no forzar asserts obsoletos. |

### Reservas que GOD debe resolver sin repetir el trabajo completo

**Modelo del ejecutor preliminar:** el documento declara GLM-5.3-Flash sobre ZCode aunque se titula TOP LOCAL. `MODEL_REPORTED=GLM-5.3-Flash`; cumplimiento del TOP Sol solicitado `NOT_DEMONSTRATED`. Primary no inspeccionó autoridad del harness. No rebautizarlo Sol ni descartar evidencia reproducible sólo por el modelo. Los próximos TOPs deben corresponder al modelo solicitado o exponer UNKNOWN/discrepancia, nunca sustituirse silenciosamente ni poner a GOD a codear.

**Sello:** el informe reporta bloque idéntico en copia/publicación anteriores al commit de optimización, pero hash publicadoff320f01 y hora13:20 inconsistentes con sus recibos. Preservar ambos originales, fijar receta de hash/alcance y separar contenido, recibo, cronología y fundamento. Antes del primer commit no prueba por sí solo antes del primer cambio de rendimiento; mtime aislado tampoco basta. No inferir intención o fraude. Una corrección posterior del recibo no puede retrofechar ni mover objetivos.

**NQZ5:** recuperar registros completos de un spool gzip truncado permite análisis forense del prefijo, no acredita checksum/footer/Close completos ni permite resume no certificado. Aprovechar el spool significa analizar evidencia ya existente; una nueva ejecución final parte de entradas autorizadas cuando S04 esté listo. Separar PASS latched, solicitud/admisión/aplicación FUNDED, funded activo y cobros; ausencia de error textual sola no certifica captura de todas las revisiones.

**Cobertura y proyecciones:** no confundir cobertura de código con histórico solicitado/procesado. La medición selectiva58,1% no acredita una medición global ni por sí sola fija el resultado de todas las suites; floor95 sigue no demostrado con denominador conforme y caminos críticos pendientes. Cifras de progreso corregidas no demuestran5h inevitables. Distinguir records de evidencia, inputs raíz, pasos activos/omitidos y minutos causales al calcular tasas.

### S03 restante — dirección GOD, ejecución TOP

GOD CLOUD independiente del diseñador S01/autor S02: coordina ataques, revisa evidencia y escribe únicamente dictamen/documentación. Cero código de producto, tests, scripts, comparadores, instrumentación o integración. TOPs GPT-6.1 Sol LOCAL fresh-context ONE-SHOT independientes: escriben/ejecutan falsificadores en overlays separados, sin corregir producto. Si no hay despacho directo acreditado, GOD entrega un paquete de prompts mediante Owner; no finge subagentes, runner o trabajo asíncrono.

Uno o como máximo dos TOPs nuevos según separación útil, sin árbol de submanagers: evidencia/identidad/NQZ5 y safety/contratos pendientes. Reutilizar RED F1–F3, recibos y corpus por hash; no repetirlos salvo duda material. No nuevas corridas históricas300/600/900s, lote13x, benchmarks completos ni perfiles exploratorios. Un proceso financiero a la vez, tareas ligeras disjuntas sólo sin contaminar mediciones. No editar el árbol bajo prueba ni regenerar cápsulas.

Preguntas restantes: biyección referencial entre builds y negativos del propio comparador; reconciliación contable de la transición NQZ5 preservada; cinco tests rojos versus autoridad vigente; LONG/SHORT, adds/protección, parciales/duplicados, cancel/ACK/finality/claims, timers y callbacks, writer/Close fallidos, referencias prestadas, admisiones y sustitución pública Strategy/MM. Rollover por API disponible puede probarse sin fingir que el CLI multicontrato existe. Workers/capacidades ausentes se registran como no implementados y oráculos S04, no se construyen dentro de S03.

El dictamen RED puede cerrar el rechazo del candidato sin fingir cobertura exhaustiva: mantener cada NOT_RUN y el gate futuro afectado. No cerrar requisitos por haber alcanzado un límite de lectura/ejecución. S04 recibe findings adjudicados con causa, owner, regresor y aceptación observable; ninguna garantía de que todo quedará resuelto ni reducción de alcance multistream sin Owner.

### Builds, autoridades y restricciones vigentes

Echo HEAD remoto confirmado en este turno: `bbbcc1d5dc0ed18badae46b4eba1a17822632b60`, rama `codex/btx-perf-s02`. Baseline50250a2b0df6106943108bf6bfe57552409f3d13, código históricod1b1446d401f88cfa42dee2eb959120305f5a372; control corregidod609ca241eed63b1b4413af5bae5b849d334ead0/binario0db2feae6237ebc20ba8ce16bcc9f50fee0e6809c3677585b403a3d708c490ee; candidato medido584a3cd91d8ecf2d8f292547a35f8e9963e2270d/binarioe5d4860b4e70f5f5833ebf374b08fb771a4551bc6d58996fa42305e1049bd141. Binario preliminar propio c9ac66ca abreviado, resolver completo en SHASUMS. No atribuir binarias entre SHAs.

Workspaces E1/S02/evaluación anterior permanecen los ya autorizados bajo home Daedalus: `aranea/work/btx-perf-s01-e1-20261008/`, `aranea/work/btx-perf-s02-20261009/`, `aranea/work/btg-s06-user-oneshot-20261008/`. El prompt conserva los localizadores exactos Owner. No son montajes acreditados en CLOUD. GitHub lectura/escritura documental está demostrada; eso no concede ejecución física a Primary.

S01 y adenda: repairs/integración permitidos antes de contrato numérico, optimizaciones sólo tras control corregido y objetivos sustentados/sellados antes del primer cambio de rendimiento. Mantener contrato original, sin mover objetivos para aprobar. La evidencia preliminar no convalida retrospectivamente una proyección insuficiente.

BASIC100000 continuo sin lifecycle prop; CAMPAIGN caja5000, compra ON_DEMAND120, una cuenta operando, máximo4cobros efectivos y reinversión. Pérdida nominal no vuelve a debitar caja. Mismos Strategy/MM sustituibles; sin ROI tuning, if Gerard, floats, cambios de SL/TP/sizing/adds/señales/fees ni recorder descartable.

Preparación/lectura por stream, buffers acotados, merge estable antes del dominio; dependencia financiera preservada. Diseño C financiera1, pool hasta2 sujeto a recursos, chunks256records/1MiB serializado sin fingir RSS. No otro motor de indicadores, campañas reiniciadas sumadas ni fechas/calendario/precios/fills inventados. Rollover prospectivo conserva obligaciones del retirado y year/month propios; warmup por requisitos y gaps requeridos explícitos. Selección futura no es por sí sola deuda corriente.

Conservar todas las revisiones SetAccountContext(k), CloseStage(k+1), OpenStage(k+2), proyección final coherente y release sólo de evidencia poseída del ledger/generación correctos con guard de igualdad. No LatestRevision como descarte, guard<= ni error ignorado. Cuerpo tipado y digest en admisión para APPLIED/REJECTED/CONFLICT/pendiente; replay CAMPAIGN con controlador completo, sin readmisión externa duplicada. IDs uno-a-uno y referencias intactas; cuarto solicitado no es cuarto cobrado, residual no es caja, compra no es activación/refund.

Ventana histórica `2026-10-09T00:00:00-03:00` EXPIRED. No nuevos180min,4h o ventana dedicada aprobada por un worker. Límites del harness no son presupuesto Owner. Cero procesos propios después del cierre. Sin D6, LIVE, broker, cuentas, órdenes, ETCD/PROD, permisos, merge o deploy. Readiness física fuera de alcance.

### Cuatro shots y despacho actual

| Shot | Estado vigente |
|---|---|
| S01 | Diseño aceptado con excepción explícita de performance; E1 parcial preservado |
| S02 | Implementación entregada y adjudicada parcial con carencias materiales |
| S03 | Falsificación preliminar recibida con reservas; siguiente GOD independiente coordina TOPs y entrega dictamen, todavía no ejecutado desde este despacho |
| S04 | Correcciones y validación final conservadas; no iniciado ni aceptado |

Prompt final de transporte: Library `/BTX-PERF-S03-GOD-COORDINATOR-PROMPT.md`, `library_file_id=libfile_284cf4a81af08191b3746389ab3e2d63`, backing `file_0000000079c0820eb6c5bc9cedbc1834`,24611bytes,SHA256 `8b7f409feefaa1903b1d0dbfee80ef57f03239e737b5ab90566c6d5769c150ce`. Es mandato de coordinación, no dictamen ya escrito ni worker ya iniciado. Sustituye el siguiente-paso del prompt preliminar ya ejecutado; no lo vuelve a despachar.

Salida GOD: `BTX-PERF-ADVERSARIAL.md` con registro de evidencia, matriz requisito/finding/oráculo, cuatro gates, cobertura de tests separada y paquete acotado S04. GOD devuelve delta al Primary; no acepta ni despliega. Workers cierran sólo sus sesiones, con agent-run/feedback reales. GOD cierra sólo su encargo cuando entregue dictamen; Primary permanece abierto hasta pedido explícito.

Persistencia Agents-OS exclusivamente master, un escritor por delta, protección por blob/readback, sin ramas/PRs/tags/worktrees documentales. Nuevas notas por contrato/materializador; esta edición modifica nota existente. Registro consolidado en [[2026-10-09-btx-perf-s02-owner-amendment]]. No feedback/cierre Primary ni código de producto en este turno. Consumos no expuestos UNKNOWN.

## Baseline histórico BTG-S05

Preservado íntegro en el control anterior `88e92e98de735dec8a0fa5832babf418c57c340c` y [[BTG-S05-REMEDIATION-AND-RESULTS]]. PASS_BOUNDED_OFFLINE_SOFTWARE d1b y reejecución final ya terminada: no volver a pedirla como pendiente. No transferir SHAs, cifras, cobertura, aceptación o readiness física a BTX-PERF. El incumplimiento temporal previo y D6 en otra build permanecen explícitos en esas autoridades; no se retrofechan ni reabren.

## Fuentes

- Mandato BTX-PERF y adenda Owner de esta sesión; pedido actual de revisión y GOD S03 comandando TOPs sin desarrollar.
- [[BTX-PERF-DESIGN]], [[BTX-PERF-IMPLEMENTATION]], [[BTX-PERF-S03-TOP-EVIDENCE]] leído en88e92e98/blobcf21581c.
- Control anterior completo en88e92e98, mismo path; HEAD Echo consultado autenticadamente enbbbcc1d5.
- E1 y S05 únicamente en su alcance; recibos locales del preliminar no reejecutados por Primary.
