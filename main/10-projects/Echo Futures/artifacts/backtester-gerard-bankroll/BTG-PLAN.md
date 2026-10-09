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
  - "[[BTX-PERF-S03-TOP-A-EVIDENCE]]"
  - "[[BTX-PERF-S03-TOP-B-EVIDENCE]]"
  - "[[BTG-S05-REMEDIATION-AND-RESULTS]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-05"
updated: "2026-10-09"
---

# BTG-PLAN — Estado vigente y continuidad del backtester

## Propósito

Control único de BTX-PERF para [[Echo Futures]]: cuatro shots, una trayectoria financiera integrada por modalidad, dominio runtime compartido y módulos sustituibles. Correctness, performance, usabilidad integrada y cobertura histórica son obligaciones separadas; cobertura de tests no es porcentaje de mercado procesado. Primary dirige y adjudica evidencia, no desarrolla ni acepta producto por Owner.

Esta edición recibe el dictamen final acotado S03 aportado por Owner y dirige las correcciones S04 ya previstas. El control anterior íntegro queda en Git `cf7183c2398658b5f95eced76a7b3e379b7f1b29`, mismo path. No se modifican informes S02/S03, PERF_CONTRACT, RED ni recibos originales. El mandato Owner de cuatro shots, su adenda y [[BTX-PERF-DESIGN]] siguen vigentes; no se crea investigación, quinto shot ni reducción de alcance.

## Contenido

### Estado vigente — recepción Primary del dictamen S03 y despacho S04

```text
PROGRAM = BTX-PERF
PRIMARY_SESSION = OPEN_UNTIL_EXPLICIT_OWNER_CLOSE
S01_TECHNICAL_DESIGN = ACCEPTED_FOR_IMPLEMENTATION_WITH_EXPLICIT_PERF_EXCEPTION
E1 = PARTIAL_WITH_EVIDENCE
S02_PRIMARY_ADJUDICATION = PARTIAL_IMPLEMENTATION_WITH_MATERIAL_GAPS
S02_COMPLETE_IMPLEMENTATION_ACCEPTED = NO
S03_GOD_ADJUDICATION = RECEIVED_ACCEPTED_AS_BOUNDED_RED_REJECTION_AND_S04_HANDOFF
S03_VERDICT = RED_REJECT_CANDIDATE
S03_DOCUMENT_COMPLETENESS = COMPLETE_FOR_BOUNDED_REJECTION_AND_HANDOFF
S03_TEST_COVERAGE = PARTIAL_WITH_EXPLICIT_NOT_RUN
S03_WORKER_CLOSEOUTS = REPORTED_CLOSED_ZERO_OWN_PROCESSES
S04_SCOPE = C01_C12_CORRECTIONS_AND_FINAL_VALIDATION_UNDER_EXISTING_OWNER_PROGRAM
S04_DISPATCH = PROMPT_ISSUED_SINGLE_TOP_LOCAL_INTEGRATOR
S04_EXECUTION = NOT_OBSERVED_BY_PRIMARY
S04_INDEPENDENT_VERIFICATION = REQUIRED_WITHIN_S04_NOT_YET_EXECUTED
CURRENT_ACTION = OWNER_RUN_FRESH_TOP_LOCAL_S04_PROMPT
FINAL_OWNER_ACCEPTANCE = NOT_GRANTED
PRODUCT_CODE_TESTS_PROFILES_BACKTESTS_BY_PRIMARY = NONE
PHYSICAL_RUNTIME_READINESS = NOT_DEMONSTRATED_OUT_OF_SCOPE
PROMOTION = NOT_ACCEPTED_NO_MERGE_OR_DEPLOY
```

Primary acepta el dictamen como evidencia suficiente para rechazar el candidato y dirigir C01–C12, no como aceptación de producto ni certificación exhaustiva. Se leyó íntegro el dictamen por rangos y se contrastaron directamente los findings monetarios con el artefacto TOP B; se confirmaron HEADs y control por GitHub autenticado. Primary no reejecutó pruebas, leyó los spools físicos ni inspeccionó los bytes de los paquetes locales. Sus PASS/RED se atribuyen a los ejecutores y a la adjudicación S03, no a ejecución propia del manager.

### Autoridades exactas recibidas

Publicación S03: Agents-OS master `cf7183c2398658b5f95eced76a7b3e379b7f1b29`. Dictamen `10-projects/Echo Futures/artifacts/backtester-gerard-bankroll/BTX-PERF-ADVERSARIAL.md`, blob Git `45fa5af308a9999f24c1028684b3eceadf448c95`. Es la entrada detallada para S04, incluidas matrices C01–C12 y dos matrices NOT_RUN; no se reconstruyen conversaciones.

TOP A: [[BTX-PERF-S03-TOP-A-EVIDENCE]], blob `4f97884c0a8b0d26e8d75197f22dd5e35a04a3e9`; TOP B: [[BTX-PERF-S03-TOP-B-EVIDENCE]], blob `058b63623a4bd7b2c833831ccf6360c9b5a6dc5c`. Preliminar: blob `cf21581c5cee5d90035e602456619e1eda2e7c0d`. Informe S02 blob `cec0feaede7e52cdd9b742c0ebfd63179c158207` sigue AUDIT_TARGET; su autocalificación no prevalece sobre S03. Diseño blob `1cedf2e4c66886079a04d18dd60216b423316b42` conserva aceptación técnica con adenda.

La sesión GOD reporta haber dirigido dos TOPs mediante herramientas reales y sin código propio. Selector solicitado gpt-6.1-sol, modelo servido exacto UNKNOWN; no afirmar Sol servido sin recibo. Preliminar conserva GLM-5.3-Flash/ZCode reportado y no se renombra. Cierres/procesos0 son evidencia reportada por ejecutores; este Primary no los sondeó. GitHub tiene lectura/escritura documental demostrada; acceso físico de otra sesión no se atribuye a esta por compartir etiqueta CLOUD.

### Adjudicación recibida: defectos y avances separados

| Ámbito | Decisión Primary basada en S03 |
|---|---|
| B-02 / C08, crítico | Admitir+1USD y aplicar+2 tras mutación del objeto caller es defecto vigente ejecutado. Pending conserva objeto mutable distinto del sello; el fix del getter por sí solo no basta. Se acepta el RED monetario y el de ExpectedContextDigest. No se atribuye origen a la optimización sin evidencia. |
| B-01 / C09 | Admissions expone referencias profundas mutables que permiten corromper ContextID/digest internos. Defecto ejecutado de frontera pública, distinto de la cola C08. |
| B-03 / C10 | Primer débito con119/costo120 lleva caja−1; control120 deja0. Defecto ejecutado en fixture válido9min. Es boundary de prueba, no alteración del perfil5000/120 ni afirmación de sobregiro observado en esa configuración. |
| C01–C04 | Multistream obligatorio sigue ausente; replay CAMPAIGN roto por Artifact faltante y enrutado antes de drenar footer; rutas absolutas y rc0/FAILED incumplen interfaz. RED preliminares aceptados en S03, no volver a investigarlos ni convertirlos en falta externa de datos. |
| Equivalencia R | TOP A demostró biyección por namespace y una generación,45referencias y negativo referencial a seq85929 sobre88362records/109diferencias. PASS_BOUNDED_SINGLE_GENERATION. Provider final con digest distinto sin preimagen sigue NOT_DEMONSTRATED; no transferir R a ALL/SKIP o generaciones múltiples. |
| NQZ5 | Prefijo real reconciliado:2764371objetos completos, replacement18nov y batch4870/4871/4872→FUNDED20nov2025, autoridad posterior coherente. Un objeto siguiente parcial no cuenta. Gzip sin EOF/footer: no COMPLETE, cobros/caja final no certificados ni resume desde spool. |
| Sello y performance | Receta hash resuelta, recibo publicado inconsistente y hora incompatible; freeze antes del primer CAMBIO de optimización NOT_DEMONSTRATED. No inferir secuencia opuesta ni intención. Par R2,2279× es run-only con preparación previa separada; ancla NQU6 BASIC180s FAIL en S02, horizontes/ratios restantes no demostrados. |
| Cinco rojos históricos | Tres expectativas supersedidas (dos ON_DEMAND y MIXED), un fallo de harness ADD (SL cancela antes de elegibilidad) y StructuralReference NO_RESUELTO. Los tres CLI tests reparados son distintos. Mantener negativos válidos y no modificar negocio para satisfacer asserts obsoletos. |
| Safety y coverage | PASS acotados de protección/Record/Close/Strategy/rollover se conservan con sus fronteras. Pendientes provider,ALL/SKIP,callbacks,MM custom,lifecycle completo,race,input-sequence y cobertura no desaparecen.58,1% selectivo no certifica cobertura global. |

### Paquete S04: prioridad y límites

C08/C09/C10 primero: aplicar el cuerpo congelado, aislar la vista pública y comprobar fondos iniciales. Mantener las pruebas monetarias originales como controles RED y los nuevos regresores GREEN con dinero exacto. Antes de cargas largas deben pasar las fronteras monetarias e integridad afectadas.

C01/C02: implementar entrada física multistream, catálogo/schedule/ReadPlan, capacidad hasta2workers con fallback1, buffers acotados y merge estable antes del único estado financiero. No basta quitar un guard, seguir Streams[0], usar catálogo sólo en memoria o sumar campañas. Ausencia de pool no queda exenta por el perfil R. C03/C04: ambas rutas CLI reproducen el controlador completo, artefactos reubicables, estados/rc y cobertura consumida distintos del inventario.

C06/C11/C12: restaurar comparadores con oráculos referenciales, cerrar preimagen provider y ALL/SKIP, corregir únicamente expectativas ya adjudicadas y mantener negativos. C07: integrar regresores y ejecutar matrices pendientes sobre la build exacta; cobertura de desarrollo95 con denominador y caminos críticos, separada del histórico. C05: rectificar recibos por adición trazable, medir y contrastar targets intactos; no otro programa de optimización autorizado por el dictamen ni retarget retrospectivo.

La rectificación posterior no puede fabricar evidencia pre-cambio. SHA256 documento congelado: `2ee87f94414e3b48d7a48d8c4915c4ed994cf864e5b74702654d3e98569417f7`; bloque3651bytes con fences sin LF: `7e71aed95548905ded11e898df04aa02fd0c54a2d4d0d8d690f743d0cd9ba984`; con LF3652bytes: `cfa81c17c7acea7dd78aa80b58e32984230a5e81c65a74009e4d1123d35e08d2`. Conservar originales y el recibo históricoff320f01 objetado; no sobrescribir ni retrofechar.

S04 no promete que los targets se alcanzarán. Si faltan requisitos, evidencia, datos o performance, devolver entrega parcial precisa; no listo para uso completo, aceptación implícita o un quinto shot automático. La medición final usa build/inputs/semántica/completion comparables; dos timeouts no prueban ratio ni no-regresión. Preparación,run,outputs/Close,replay y comparación llevan tiempos propios y total sólo cuando esté medido.

### Builds y ejecución física

HEAD Echo confirmado nuevamente: `bbbcc1d5dc0ed18badae46b4eba1a17822632b60`, rama `codex/btx-perf-s02`. ControlS02 `d609ca241eed63b1b4413af5bae5b849d334ead0`, binario `0db2feae6237ebc20ba8ce16bcc9f50fee0e6809c3677585b403a3d708c490ee`; candidato medido `584a3cd91d8ecf2d8f292547a35f8e9963e2270d`, binario `e5d4860b4e70f5f5833ebf374b08fb771a4551bc6d58996fa42305e1049bd141`. Baseline anterior50250a2b0df6106943108bf6bfe57552409f3d13 y código históricod1b1446d401f88cfa42dee2eb959120305f5a372. Cada nueva build lleva identidad propia; d609 no es referencia correcta en toda frontera recién descubierta.

Paquetes existentes en Daedalus, relativos al home autorizado: `aranea/work/btx-perf-s03-top-a-20261009/`, `aranea/work/btx-perf-s03-top-b-20261009/`, `aranea/work/btx-perf-s03-top-20261009/`, S02/E1/evaluación previa ya referidos en el dictamen. Prompt privado conserva localizadores exactos Owner. Consumir bytes por manifiestos, no regenerar cápsulas/export NT, clonar por worker ni ampliar permisos. Las rutas locales no son montajes acreditados en este Primary.

Integrador TOP LOCAL fresh-context ONE-SHOT, con el acceso ya usado en Daedalus, un solo owner de producto. TOP independiente nuevo verifica dentro del mismo S04, separado de autoría y ligado a SHA final. GOD sólo coordina/adjudica y escribe documentación. Subagente sólo mediante herramienta real; si falta, el integrador entrega mandato resuelto para transporte Owner y deja verificación/aceptación pendientes. No fingir worker ni reutilizar su certificado después de cambios no revalidados; no reactivar especialistas cerrados.

### Invariantes y gates de entrada a S04

BASIC100000 continuo sin lifecycle; CAMPAIGN5000/120, una activa, cuatro COBROS efectivos por cuenta, reinversión sólo de cobrados y pérdida nominal sin redebito. Strategy/MM sustituibles por composición compartida, sin ifGerard,ROI tuning,cambio SL/TP/sizing/adds/señales/fees, dinero flotante o recorder descartado. Warmup por requisitos, año/mes físico propio, rollover prospectivo y obligaciones retiradas preservadas; gaps requeridos desconocidos dejan frontera explícita, no precios/fills/feriados inventados.

Capturar todas las revisiones comprometidas y liberar sólo evidencia poseída del ledger/generación correctos, guard de igualdad vigente. Cuerpo/digest al admitir y al aplicar coinciden para todas las disposiciones; vistas públicas no mutan autoridad. Replay CAMPAIGN no readmite externamente controles regenerados. IDs por biyección y referencias; no borrar hashes/digests opacos, IDs, timestamps o kinds para declarar equivalencia.

| Gate del objetivo completo al recibir S03 | Estado |
|---|---|
| Correctness | FAIL_EXECUTED según S03, incluidos B-01/B-02/B-03 |
| Performance | FAIL ancla NQU6 BASIC180s de S02; resto NOT_DEMONSTRATED/R acotado run-only |
| Usabilidad integrada | FAIL_EXECUTED |
| Cobertura histórica solicitada | NOT_DEMONSTRATED |
| Cobertura de código adicional | FLOOR95_NOT_DEMONSTRATED_GLOBAL |

No se concede READY_FOR_OWNER_ACCEPTANCE con un requisito obligatorio abierto. La build final requiere BASIC y CAMPAIGN integrados, replay oficial fresco, casos reales nuevos y regresiones aplicables, matrices críticas y revisión independiente. Un run limitado por datos no se convierte en horizonte completo por haber tocado los cuatro años en fragmentos. PHYSICAL_RUNTIME_READINESS fuera de alcance; D6/broker/cuentas/LIVE/ETCD/PROD/permisos/merge/deploy no autorizados.

Ventana histórica2026-10-09T00:00:00-03:00 EXPIRED; no180min/4h ni ventana dedicada nueva. Límites operativos del harness se registran como tales, no como concesión Owner. Cero procesos propios pendientes tras devolución. No repetir la escalera300/600/900s para demostrar un fallo ya conocido; corridas finales sólo cuando dependencias y recursos estén listos, sin promesa de trabajo asíncrono.

### Registro de cuatro shots y transporte final

| Shot | Estado actual |
|---|---|
| S01 | Diseño aceptado con excepción explícita; E1 parcial preservado |
| S02 | Entregado y rechazado como implementación completa; avance útil conservado |
| S03 | Dictamen GOD recibido y aceptado para rechazo acotado/remediación; pruebas ejecutadas parciales, workers cerrados reportados |
| S04 | Prompt de correcciones emitido para TOP LOCAL; ejecución todavía no observada; verificación independiente interna requerida |

Prompt final de transporte: Library `/BTX-PERF-S04-TOP-LOCAL-CORRECTIONS-PROMPT.md`, `library_file_id=libfile_edf3923ed4108191b0025f99527f968f`, backing `file_00000000eb7c820eab2ef260ef05956f`,26787bytes,SHA256 `cdb3fdb8ad128d6280c0f05fd131ed10225978da73fc6fd69cb9eca9d49d441d`. Artefacto guardado y destino verificado; emitir un prompt no demuestra que el integrador comenzó. No volver a despachar los prompts S03 ya devueltos.

Salida esperada `BTX-PERF-FINAL.md` en este mismo directorio, con C01–C12, build/inputs/comandos/mediciones/resultados/coverage y comprobación independiente. README del repo es manual único; evidencia pesada fuera del vault, portable por rutas relativas y hashes. Integrador/verificador dejan feedback y cierre propios conforme al mandato; no Primary. Modelo servido/tokens/consumo no expuestos UNKNOWN, sin contar un despacho planeado.

### Persistencia y registro

Este cambio modifica únicamente control existente con protección por blob, sobre master. Registro consolidado en [[2026-10-09-btx-perf-s02-owner-amendment]] mediante adición de la recepción S03/despacho S04. No modifica dictamen/autores/contrato histórico, no crea otra nota de control ni ejecuta producto/materializador/lint global. Nuevas notas del worker seguirán su contrato documental vigente. Readback acredita publicación remota, no sincronización física Daedalus ni ejecución S04.

## Baseline histórico BTG-S05

Preservado en controles anteriores y [[BTG-S05-REMEDIATION-AND-RESULTS]]. PASS_BOUNDED_OFFLINE_SOFTWARE sobre d1b y reejecución terminada no se transfieren a BTX-PERF. No volver a pedir la reejecución anterior como pendiente, reabrir D1–D6, retrofechar incumplimientos o usar PnL/tiempos viejos como resultados nuevos.

## Fuentes

- Mandato Owner BTX-PERF de cuatro shots y adenda de aceptación técnica S01/autorización acotada S02; handoff actual S03 RED/READY_FOR_PRIMARY_REVIEW.
- [[BTX-PERF-ADVERSARIAL]] en cf7183c2398658b5f95eced76a7b3e379b7f1b29, blob45fa5af308a9999f24c1028684b3eceadf448c95; C01–C12 y matrices de validación son autoridad de correcciones.
- [[BTX-PERF-S03-TOP-B-EVIDENCE]] leído directamente en sus findings monetarios; [[BTX-PERF-S03-TOP-A-EVIDENCE]] mediante adjudicación y referencias explícitas del GOD, sin lectura física propia.
- [[BTX-PERF-DESIGN]], [[BTX-PERF-IMPLEMENTATION]], control anterior íntegro en cf7183c2 y HEAD Echo bbbcc1d5 consultados en sus ámbitos.
