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
  - "[[BTG-S05-REMEDIATION-AND-RESULTS]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-05"
updated: "2026-10-10"
---

# BTG-PLAN — Estado vigente y continuidad del backtester

## Propósito

Control único de BTX-PERF para [[Echo Futures]]. El programa Owner consta de cuatro shots y exige una trayectoria histórica integrada por modalidad sobre todos los años disponibles, dominio runtime compartido, Strategy/MM sustituibles, replay oficial y rendimiento comparable. Primary dirige y adjudica evidencia; no desarrolla ni acepta el producto por Owner. Cobertura de código, cobertura histórica, corrección funcional y rendimiento son obligaciones distintas.

Esta edición recibe la entrega S04 y conserva su avance sin adoptar los PASS globales que no están sustentados. El control anterior completo permanece en Git `6e2b25c3637403e52cbbc9039b1240dae495c65b`, mismo path. No se modifican informes S02/S03/S04, diseño, PERF_CONTRACT, RED ni recibos. La aceptación técnica S01 y su adenda no redujeron el horizonte a octubre–noviembre de 2025. No se crea un quinto shot, otra investigación o reapertura automática de especialistas cerrados.

## Contenido

### Estado vigente — recepción y adjudicación documental Primary de S04

```text
PROGRAM = BTX-PERF
PRIMARY_SESSION = OPEN_UNTIL_EXPLICIT_OWNER_CLOSE
S01_TECHNICAL_DESIGN = ACCEPTED_FOR_IMPLEMENTATION_WITH_EXPLICIT_PERF_EXCEPTION
E1 = PARTIAL_WITH_EVIDENCE
S02_PRIMARY_ADJUDICATION = PARTIAL_IMPLEMENTATION_WITH_MATERIAL_GAPS
S03_GOD_ADJUDICATION = ACCEPTED_BOUNDED_RED_REJECTION_AND_S04_HANDOFF
S03_TEST_COVERAGE = PARTIAL_WITH_EXPLICIT_NOT_RUN
S04_DELIVERY = RECEIVED
S04_EXECUTION = REPORTED_EXECUTED_BY_INTEGRATOR_AND_VERIFIER
S04_PRIMARY_ADJUDICATION = PARTIAL_DELIVERY_WITH_USEFUL_BOUNDED_FUNCTIONAL_EVIDENCE
C01_C12_GLOBAL_CLOSURE = NOT_ACCEPTED_AS_COMPLETE
PROGRAM_OPERATIONAL_OBJECTIVE = NOT_DELIVERED_IN_FULL
S04_INDEPENDENT_REVIEW = REPORTED_PASS_WITH_FINDINGS_ON_0a6a0763
S04_FINAL_HEAD_INDEPENDENT_REVIEW = NOT_DEMONSTRATED_FOR_ed31156f
S04_SOURCE_REMOTE_RESOLUTION = FAILED_FOR_REPORTED_BRANCH_AND_ABBREVIATED_COMMITS
CURRENT_ACTION = OWNER_REVIEW_OF_PARTIAL_DELIVERY_AND_UNSATISFIED_OBLIGATIONS
NEW_WORKER_DISPATCH = NONE
FIFTH_SHOT = NOT_AUTHORIZED_NOT_DISPATCHED
READY_FOR_OWNER_ACCEPTANCE = NO
FINAL_OWNER_ACCEPTANCE = NOT_GRANTED
PRODUCT_CODE_TESTS_PROFILES_BACKTESTS_BY_PRIMARY = NONE
PHYSICAL_RUNTIME_READINESS = NOT_DEMONSTRATED_OUT_OF_SCOPE
PROMOTION = NOT_ACCEPTED_NO_MERGE_OR_DEPLOY
```

Primary leyó el informe canónico completo por rangos, su transcripción Owner y el control vigente. La devolución del verificador se leyó como cita incluida por el integrador en ese informe; no como inspección independiente de los logs originales de Daedalus. Se acepta como evidencia reportada y atribuida, suficiente para conservar los avances y detectar límites de la entrega. No se reejecutaron tests/backtests ni se inspeccionó el source S04: la resolución remota de sus refs falló. Este corte no descubre un defecto nuevo del producto por ejecución ni afirma que sigan abiertos los tres RED monetarios pese a sus GREEN reportados.

### Fuente recibida, disponibilidad y cortes

| Entrada | Identidad y alcance comprobado en esta recepción |
|---|---|
| Agents-OS master leído | `6e2b25c3637403e52cbbc9039b1240dae495c65b` |
| Informe S04 | `10-projects/Echo Futures/artifacts/backtester-gerard-bankroll/BTX-PERF-FINAL.md`, blob Git `9b68ea4eb3627d020cef97b79c1fe21681537181`, 20735 bytes según metadata. Publicación documental verificada |
| Dictamen S03 vigente | [[BTX-PERF-ADVERSARIAL]], blob `45fa5af308a9999f24c1028684b3eceadf448c95`; C01–C12 y matrices NOT_RUN no quedan sustituidos por etiquetas VERIFIED del autor |
| Fuente de corridas finales reportada | `0a6a0763`; binario SHA256 `f80d8974157452f0e7ac0d757b8815a37d0a259e222d132a69321a196010f69e` |
| HEAD final reportado | `ed31156f`; binario SHA256 `068a854802c29a6dcb69b949d8c70882101452fc1fa2db0939d6cae60216edd6`; movió un validador de producto a biblioteca después del freeze, no sólo documentación/tests |
| Publicación de producto | GET `xKoRx/echo/git/ref/heads/codex/btx-perf-s04` devolvió404. Consultas de commits `ed31156f` y `0a6a0763` devolvieron422/No commit found. GET de `codex/btx-perf-s02` sí devolvió `bbbcc1d5dc0ed18badae46b4eba1a17822632b60` |
| Alcance del fallo de acceso | No se pudo resolver la publicación S04 mediante esta conexión. No prueba inexistencia del trabajo local, eliminación de la rama o falta general de permisos GitHub. No se inventan SHAs completos desde abreviaturas ni se atribuye source review S04 a Primary |
| Paquetes locales reportados | `aranea/work/btx-perf-s04-20261009/` y `aranea/work/btx-perf-s04-verify/`, relativos al home autorizado de Daedalus; no montados ni inspeccionados por este Primary |

El informe conserva una inconsistencia menor de inventario: dice ocho commits y enumera nueve, concordantes con los nueve del handoff. Sin DAG remoto S04 recuperado no se adjudica el conteo real. Publicar documentación en Agents-OS no publica automáticamente código, binarios ni paquetes de evidencia de Echo. No se solicita una exportación nueva de NinjaTrader ni se amplían conexiones/permisos desde este corte.

### Avance funcional conservado — evidencia reportada, no certificado universal

C08/C09/C10 reportan RED baseline→GREEN y comprobación independiente en `0a6a0763`: aplicar el cuerpo financiero congelado, aislar profundamente Admissions y proteger la compra inicial119/120. Se conservan esos resultados; no se desechan por el modelo declarado ni se transforman en prueba de todas las disposiciones o del HEAD posterior.

Se reportan CLI con descriptor multistream, pool hasta2, replay de CAMPAIGN por ambas rutas, rutas relativas, rc por estado, oráculos ALL/SKIP/legacy y expectativas históricas corregidas. El verificador citado reporta suites propias, negativos y replays de sus copias. Estos son avances frente a S03, pero su alcance exacto y sus omisiones siguen determinando qué requisitos cierran.

| Resultado de la ventana ejecutada | BASIC | CAMPAIGN |
|---|---|---|
| Build de corridas reportada | `0a6a0763` / bin `f80d8974…` | Misma build |
| Warmup / trading / fin exclusivo | 2025-10-13T17:52Z / 2025-10-27T17:52Z / 2025-11-27T18:00Z | Mismos límites |
| Modalidad/modelo | Nominal100000 sin lifecycle; OHLC_CAUSAL_PATH_V2, CONFIGURED | Caja5000, compra120 ON_DEMAND, una activa, máximo4cobros efectivos; mismo modelo |
| Estado reportado | COMPLETE, rc0 | COMPLETE, HORIZON_REACHED, rc0 |
| Records de evidencia | 3214366 | 3127905 |
| Economía reportada | Saldo70307,92USD, neto−29692,08, costos4462,08 | 6compras,5burns/reemplazos,1cobro neto1500, caja5780; cuenta activa101500,12 |
| Wall / CPU / RSS | 1025,53s / 1453,90s / 108,36MiB | 668,92s / 964,45s / 109,57MiB |
| Replay reportado | IDENTICAL por manifest; verificador repite en copia | IDENTICAL por manifest y result; verificador repite en copia |

La caja reportada concilia exactamente `5000−6×120+1500=5780`. Es resultado del perfil FUNCTIONAL_ASSUMPTIONS del experimento, no acreditación de reglas de una prop ni rentabilidad futura. No se conserva sólo una conciliación como sustituto de causalidad, integridad o replay.

### Límites materiales y rectificaciones del resumen de S04

**D-S04-01 — horizonte y rollover.** La entrega llama «solicitada» a su ventana octubre–noviembre2025. El mandato del programa exige todos los años disponibles y no consta autorización Owner que lo reduzca. El propio informe publica45488records de mercado NQZ5 consumidos y NQH6 con `obligated=null, consumed=0`; reconoce que no hubo rollover real en las corridas finales. Aceptar un descriptor de dos streams es avance de interfaz, no prueba de una trayectoria financiera que atravesó ambos. El E2E sintético/API de rollover reportado conserva su valor, sin sustituir la validación real de continuidad solicitada. El objetivo multianual no se intentó en esta entrega; no se presenta como bloqueado por datos mediante una corrida integral que no existe.

**D-S04-02 — performance y denominador.** Los1025,53/668,92s corresponden a esa ventana corta. Compararlos con3600/3900s fijados para el horizonte completo no acredita MAX_WALL_PER_MODE. Las observaciones RSS también son acotadas a los procesos medidos. NQU6 completo reporta1741,82s frente a180s: incumple ese umbral en la ejecución observada, pero tuvo contención del propio ancla/coverage/replay/verificador. No es una medición limpia C=1 ni permite adjudicar cuánto tardaría aislado; tampoco autoriza convertirlo en PASS. Se conserva FAIL de la observación, ancla S02 ya fallida y aceptación de performance no demostrada. No hay par comparable control/candidato S04: MIN_SPEEDUP sigue NOT_DEMONSTRATED. El2,2279× de S02 es run-only de R, no un ratio de todo el programa. No se programan otra escalera de timeouts o benchmarks por rutina.

**D-S04-03 — identidad final e independencia.** El verificador citado selló `0a6a0763`/`f80d8974`; excluye explícitamente artefactos posteriores a su corte, incluidos replay/coverage de `ed31156f`. Su PASS no se transfiere al HEAD final después de mover código de validación. El replay IDENTICAL posterior, declarado por el integrador, es evidencia focal favorable; no demuestra por sí solo negativos del validador, todos los callers ni validación independiente del delta. No se exige repetir indiscriminadamente todo: falta una cadena verificable de diff/identidades y comprobación independiente del impacto final.

**D-S04-04 — C11 no equivale a campo presente.** El verificador citado declara que provider_final_state está presente/tipado y comparadores GREEN, pero reconoce no haber comparado su equivalencia semántica contra el control porque no hay par S04. C11 exigía esa comparación y sus negativos. Exponer la preimagen no demuestra equivalencia del estado final. ALL/SKIP tiene GREEN reportado; no se le transfiere un PASS de provider no ejecutado. C11 permanece parcialmente demostrado, no cerrado íntegramente.

**D-S04-05 — cobertura y matriz crítica.** El informe final reporta76,4% en el alcance instrumentado y porcentajes parciales en funciones del delta: ReproduceCampaign64,8%, ApplyResolvedCatalog60%, ValidateSealedMultistream84%, frozenDeclaredControls36,4%, además de rangos79–100% en otras áreas. El promedio global heredado no determina por sí solo el porcentaje del delta. Tampoco una selección de funciones llamadas «núcleo» prueba el floor95: falta numerador/denominador reproducible del desarrollo acordado y trazabilidad de las obligaciones críticas pendientes. La afirmación de cumplir95 en el núcleo no se acepta a partir de rangos con valores inferiores y sin agregado conforme. Una rama declarada inalcanzable no se excluye silenciosamente ni obtiene un test cosmético. Cobertura funcional de CLI por E2E es distinta de cobertura instrumentada. C07 no queda completamente cerrado por «suite verde» sin mapear los NOT_RUN de S03;41paquetesOK y2fallos ambientales reportados tampoco son una suite global sin fallos. Se conserva la clasificación ambiental atribuida al ejecutor sin ampliar permisos/infra.

**D-S04-06 — modelos y consistencia de reporte.** Handoff y sección de límites declaran GLM-5.3-Flash para integrador/verificador; tabla de identidades también conserva UNKNOWN. Registrar `S04_MODEL_REPORTED=GLM-5.3-Flash`, selector solicitado Sol no acreditado y recibo servido exacto no inspeccionado por Primary. No renombrar esas sesiones como Sol ni atribuir automáticamente sus defectos al modelo. Es una discrepancia repetida de asignación/procedencia, no motivo para borrar evidencia reproducible.

**D-S04-07 — entrega reproducible.** El documento publicado es accesible; las refs de producto no se resolvieron. La receta --result contiene RunID con elipsis y la ubicación BIN requiere resolver el CWD real. Esas líneas no son un paquete portable enteramente copiable. No inventar rutas/SHA ni confundir entrega documental con entrega íntegra del producto. Los originales y worktrees locales reportados deben conservarse; no se ejecuta publicación/push de producto, ni se modifica un archivo ajeno para simular entrega, desde esta recepción.

### Gates del objetivo completo tras S04

| Gate / obligación | Adjudicación Primary | Alcance favorable conservado |
|---|---|---|
| Correctness del objetivo completo y HEAD final | NOT_DEMONSTRATED | GREEN monetarios y replay en ventana/build de corridas reportados; provider final, delta posterior y matriz crítica no cerrados |
| Performance | NOT_ACCEPTED: anclas con FAIL observado; condiciones limpias/ratios/horizonte completo NOT_DEMONSTRATED | Tiempos completos de ventana corta y R anterior; no trasladar límites entre horizontes |
| Usabilidad integrada de todo el catálogo/horizonte | NOT_DEMONSTRATED en alcance integral | CLI/pool/replay/portabilidad reportados sobre fixtures y ventana; segundo stream real no consumido |
| Cobertura histórica solicitada | NOT_DEMONSTRATED / objetivo completo no entregado | Ventana octubre–noviembre2025 reportada COMPLETE; no rollover final real ni todos los años |
| Cobertura95 del alcance de desarrollo | NOT_DEMONSTRATED |76,4% global reportado y métricas por función; no agregado del delta con contrato satisfecho |
| Publicación/identidad reproducible de producto | NOT_DEMONSTRATED en esta conexión | Informe canónico publicado; source/binarios S04 locales reportados |

No se rechaza por completo el trabajo ni se inventa un bug nuevo desde ausencia de prueba; se rechaza la promoción de resultados acotados a «C01–C12 íntegro» y «sólo falta performance». Los cuatro shots han sido devueltos, pero el objetivo operativo sigue sin entregarse completo. Agotar la secuencia no concede aceptación. No se solicita al Owner aceptar un resultado que el manager declare listo cuando hay obligaciones conocidas abiertas.

### Continuidad, autoridad y límites que sobreviven

El programa no se reinicia. No quinto shot automático, nuevo prompt de investigación, worker en background ni regreso a las sesiones cerradas. Esta recepción sólo adjudica/documenta. La falta de fuente final/evidencia y los requisitos pendientes quedan explícitos para una decisión posterior Owner; no se transforma esa decisión en otro presupuesto o autorización tácita. Primary permanece abierto hasta cierre explícito.

Siguen vigentes los contratos completos de [[BTX-PERF-DESIGN]], la adenda Owner y C01–C12/matrices finales de [[BTX-PERF-ADVERSARIAL]]: BASIC100000 sin lifecycle, CAMPAIGN5000/120/una activa/cuatro COBROS por cuenta, reinversión sólo de cobrados, pérdida nominal sin redebito; módulos compartidos sustituibles; todas las revisiones comprometidas y guard corriente; controles tipados congelados al admitir/aplicar y vistas aisladas; replay completo con identidad/referencias; preparación hasta2workers con fallback1, buffers acotados y merge causal; warmup/schedule prospectivos, obligaciones del retirado y gaps explícitos. Nada de ROI tuning, ifGerard, floats, cambios SL/TP/sizing/adds/señales/fees, recorder descartado, calendarios/precios/fills inventados o suma de campañas reiniciadas.

C05 conserva rectificación append-only y el contrato original. Recibo históricoff320f01 objetado y freeze antes del primer cambio siguen NOT_DEMONSTRATED; una rectificación posterior no puede acreditar retrospectivamente la secuencia. Targets no movidos para aceptar resultados parciales.

Ventana histórica `2026-10-09T00:00:00-03:00` EXPIRED; no180min/4h ni ventana dedicada nueva. Cero procesos propios al cierre es reporte de ejecutores, no sondeo de este Primary. D6/PHYSICAL_RUNTIME_READINESS siguen separados: no LIVE, broker/cuentas, órdenes, PROD/ETCD, permisos, merge, despliegue ni promoción. GitHub lectura/escritura documental se usa sobre master únicamente, con protección por blob y preservación de cambios concurrentes.

### Registro de cuatro shots

| Shot | Estado de su entrega |
|---|---|
| S01 | Diseño aceptado con excepción explícita; E1 PARTIAL_WITH_EVIDENCE preservado |
| S02 | Entregado, parcial con carencias; source publicado hasta bbbcc1d5 |
| S03 | Dictamen RED acotado aceptado para rechazo/remediación; pruebas NOT_RUN preservadas |
| S04 | Entregado y recibido como avance funcional acotado con obligaciones abiertas; fuente remota no resuelta, HEAD final no certificado por el verificador citado |

Los prompts previos son transporte histórico, no despachos activos. Su registro íntegro y baselines BTG-S05 permanecen en la versión anterior de este control y los logs. No se reabre d1b, su reejecución final ni los16hallazgos S04 históricos. Registro consolidado de esta recepción: [[2026-10-09-btx-perf-s02-owner-amendment]], adición fechada10oct2026. No feedback/cierre de Primary ni modificaciones de producto.

## Fuentes

- Mandato Owner BTX-PERF de cuatro shots, especialmente horizonte íntegro, gates separados y aceptación final humana; adenda S01/S02 y despacho S04 ya emitido.
- Handoff S04 recibido del Owner y [[BTX-PERF-FINAL]], blob `9b68ea4eb3627d020cef97b79c1fe21681537181` en Agents-OS `6e2b25c3637403e52cbbc9039b1240dae495c65b`; sus resultados/verificador son reportes atribuidos, no ejecutados aquí.
- [[BTX-PERF-ADVERSARIAL]], [[BTX-PERF-DESIGN]], [[BTX-PERF-IMPLEMENTATION]] y evidencias A/B dentro de sus autoridades y cortes; no modificados.
- Control previo completo en `6e2b25c3637403e52cbbc9039b1240dae495c65b`, blob `a1b215b7bc40f62f891f17bac23fc3ae352e61a3`; los límites de acceso S04 se basan en respuestas404/422 actuales y lectura positiva de S02 en la misma conexión.
