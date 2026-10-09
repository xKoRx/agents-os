---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[BTG-PLAN]]"
  - "[[BTX-PERF-DESIGN]]"
  - "[[BTX-PERF-IMPLEMENTATION]]"
  - "[[BTX-PERF-S03-TOP-EVIDENCE]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-09"
updated: "2026-10-09"
---

# BTX-PERF-S03-TOP-A-EVIDENCE

## Propósito

TOP A LOCAL, fresh-context ONE-SHOT independiente, limitado a evidencia estática, parsing y comparadores; no autor de S01/S02/preliminar. Entrega para adjudicación GOD, no aceptación de producto: `READY_FOR_GOD_REVIEW_WITH_EXPLICIT_GAPS`. Los originales y el checkout Echo permanecieron intactos; no ejecuté motor financiero, backtest, replay, perfil, benchmark, F1/F2/F3 ni instalación. TOP B fue el único ejecutor financiero autorizado. No commit/push manual. El vault tiene sync automático activo; la ausencia de commit manual no equivale a no-publicación. GOD debe leer los bytes/hashes finales y adjudicar el corte correspondiente.

`REQUESTED_ROLE=TOP`; `REQUESTED_MODEL=GPT-6.1 Sol`; `EXECUTED_MODEL_EXACT=UNKNOWN`, porque este contexto del harness no expone identificador exacto ejecutado ni recibo de selección. La autodescripción general GPT-6 no acredita GPT-6.1 Sol. `REQUESTED_MODEL_COMPLIANCE=NOT_DEMONSTRATED`; superficie observada `Codex` LOCAL. Tokens, costo y consumo de pool `UNKNOWN`; no uso de CLOUD Pro observado ni delta confirmado. Preliminar se conserva como `MODEL_REPORTED=GLM-5.3-Flash`, solicitado TOP y cumplimiento `NOT_DEMONSTRATED`; no lo rebautizo ni descarto sus recibos por modelo.

## Contenido

### Autoridad, alcance y cortes

Mandato TOP A del GOD recibido en esta tarea prevalece sobre mapping de modelos/three-shot histórico de technical-project-manager: cuatro shots, TOP solicitado GPT-6.1 Sol, GOD coordina sin programar. Cargados agents-os.md, bootstrap mínimo, constitución/perfil/continuidad global/INDEX, technical-project-manager y skills de agent-run, feedback y cierre. Control autorizado `BTG-PLAN` en commit `9561c60d1de2d59d1fe9ac393aaa6d37fa8ad17a`, blob comprobado `de3753b81564eb62f64a8b5eb18f198a6a81fd27`; preludio `88e92e98de735dec8a0fa5832babf418c57c340c`, preliminar blob `cf21581c5cee5d90035e602456619e1eda2e7c0d`. Diseño: adenda Owner leída primero, estados históricos subordinados. Informe S02 es objeto de auditoría; preliminar es input aceptado acotado con reservas, nunca certificación universal. No se reabrió D1–D6 ni historia total.

Host efectivo `daedalus`, acceso local directo a las raíces autorizadas; SSH no necesario. Nuevo workspace sin colisión: home autorizado + `aranea/work/btx-perf-s03-top-a-20261009/`. Tooling propio sólo ahí, ningún overlay de producto nuevo, clon ni exportación. `input-cuts.json` conserva path físico operativo, bytes, mtime_ns, SHA256 completo y momento UTC de cada lectura; las rutas canónicas del vault aquí son relativas. `identity-cut.json` conserva HEAD, branch, dirty, DAG y stamps reales. Vault observado master, avanzando por sync; no traté los commits de sync como escritura mía manual.

Baseline `50250a2b0df6106943108bf6bfe57552409f3d13`; histórico `d1b1446d401f88cfa42dee2eb959120305f5a372` sólo referencia de mandato, no revalidado integralmente. Echo observado HEAD `bbbcc1d5dc0ed18badae46b4eba1a17822632b60`, dirty vacío. Delta `584a→bbb` comprobado: README + test ring, 95 inserciones/3 borrados; no atribuir binario medido de584a a bbb. Stamps Go confirman revisions y `vcs.modified=false` para cada binario abajo.

| Identidad | Commit completo | SHA256 binario completo |
|---|---|---|
| Control medido | d609ca241eed63b1b4413af5bae5b849d334ead0 | 0db2feae6237ebc20ba8ce16bcc9f50fee0e6809c3677585b403a3d708c490ee |
| Candidato medido R/NQZ5 | 584a3cd91d8ecf2d8f292547a35f8e9963e2270d | e5d4860b4e70f5f5833ebf374b08fb771a4551bc6d58996fa42305e1049bd141 |
| Binario preliminar distinto, sólo inspeccionado | bbbcc1d5dc0ed18badae46b4eba1a17822632b60 | c9ac66caf363e1eda662c15d07b7c6cdb2fa11e773c30243d23e4aed7edc13b8 |

### A — receta de sello y cronología

Oráculo propio `receipts.py`, función block: buscar bytes `## PERF_CONTRACT`, después primer ` ```text ` sin espacios añadidos y cerrar en los siguientes tres backticks inclusive. No conversión de encoding, CRLF, espacios ni saltos de línea. Algoritmo SHA256; original preservado. Resultado `seal.json`:

| Alcance exacto | Bytes | SHA256 |
|---|---:|---|
| Documento entero `btx-perf-s02-20261009/measure/perf-contract-frozen.md` | 13977 | 2ee87f94414e3b48d7a48d8c4915c4ed994cf864e5b74702654d3e98569417f7 |
| Bloque fences inclusive, sin LF final, frozen y publicado iguales | 3651 | 7e71aed95548905ded11e898df04aa02fd0c54a2d4d0d8d690f743d0cd9ba984 |
| Bloque fences inclusive con un LF final | 3652 | cfa81c17c7acea7dd78aa80b58e32984230a5e81c65a74009e4d1123d35e08d2 |

Recibo publicado `ff320f01e9954eefaf84de5380b78e8b99e334d42ac10bf50f018d34ae89079d` no corresponde a estas recetas ni a las variantes ya inspeccionadas en `logs/seal-verification.txt` preliminar. `measure/perf-contract-seal.sha256` sí coincide exactamente con DOCUMENTO ENTERO; no prueba el alcance declarado de bloque. `PUBLISHED_BLOCK_RECEIPT_NOT_REPRODUCIBLE`, sin nuevo sello ni corrección del original.

Fecha declarada del bloque: `SEALED_2026-10-09T13:20-03:00`. mtime/birth local observado: `2026-10-09T10:16:59-03:00`; esto es metadata de filesystem, no recibo independiente de inicio de cambios. Source DAG: control commit10:12:06, primer commit de optimización10:28:47. El recibo preliminar documenta sync b1c31734 a10:17:03 y publicación byte-idéntica anterior a13:20; se conserva como `EXISTING_PUBLICATION_RECEIPT`, no fecha real inferida de sellado. El bloque declara una hora posterior a bytes ya publicados: inconsistencia temporal demostrada por esos recibos; no inferencia de intención ni fraude.

Busqué frontera en archivos measure/seal existentes, inputs/seal.json, logs seleccionados y reflog acotado del checkout: ninguno preserva un árbol/hash/recibo antes del PRIMER CAMBIO de rendimiento. Publicación/mtime anterior al primer COMMIT no prueba anterior al primer CAMBIO. `PERF_TARGET_FREEZE_BEFORE_FIRST_PERFORMANCE_CHANGE=NOT_DEMONSTRATED`, corrigiendo el alcance del preliminar que daba el orden por cerrado. Reflog registra commits, no cada edición. No retrofechar un eventual repair de evidencia S04; preservar bytes/targets y declarar fecha actual del nuevo recibo si Owner lo autoriza.

### A — tiempos, poblaciones y censuras

Único par COMPLETE comparable inspeccionado: R BASIC, 88.362 records de evidencia por extremo, 1.674.851 root inputs por extremo, trade_start19jul2026 22:01Z/end23:00Z, warmup05jul22:01Z. Recibos `/usr/bin/time -v`: control75,77s user128,24/sys13,55/maxRSS61840KiB; candidato34,01s user45,80/sys2,89/maxRSS55788KiB; rc0 ambos. Speedup75,77/34,01=2,22787415466× exclusivamente R. Tasas derivadas: control45,2399µs/root-input versus candidato20,3063µs/root-input; usando records de evidencia son857,495µs/record versus384,893µs/record. Los denominadores NO se intercambian; root inputs incluyen la expansión causal y warmup, records son evidencia emitida. RSS60,3906/54,4805MiB del proceso, sin garantía histórica/global.

rc124 comprobados en archivos measure: ctrl-NQU6full, opt-NQU6full, opt-NQZ5, opt-NQZ5R, probe-NQZ5R/R2. Se reutiliza ancla NQU6 BASIC180s FAIL ya demostrada por censuras/progreso en preliminar; no se repitieron300/600/900s. Dos corridas censuradas no dan cociente válido ni prueban no-regresión. Las cifras S02301.911@21jul/49.359@21oct/4,9ms quedan sin binding a un intento conservado; la nueva lectura NQZ5 contradice el límite21oct. El tiempo600s de NQZ5 es límite REPORTED del intento censurado, no wall completo certificado (stderr/stdout vacíos, rc124 sí existe). Si se usa600 como denominador nominal:2.764.371/600=4607,285records de evidencia/s, 0,21705ms/record; no tasa de root inputs ni coste homogéneo del warmup. Proyección5h sigue proyección, no duración inevitable. Los otros conteos de intentos NQU6/NQZ5R permanecen evidencia preliminar acotada; no recontados por rutina.

Pool de preparación ausente/declarado en S02: R no convalida su suficiencia para el horizonte completo ni el requisito de preparar por stream. Workers efectivo1 no prueba posibilidad/admisión2. Distinguir restricciones de recursos y obligación arquitectónica; `PREPARATION_POOL_FULL_HORIZON=NOT_DEMONSTRATED`. Objetivos publicados permanecen congelados, no aceptados retrospectivamente por esta auditoría.

### B — biyección referencial del par real R

Oráculo independiente `compare_r.py`, Python stdlib, sin llamar `CompareRecords` ni código producto. Reutiliza clasificación previa de109/39paths; nuevo trabajo verifica mapa y falsificación referencial. Mapas separados por namespace y generación fija observada `btg-functional/BTG_FUNCTIONAL_NQ_EVAL_V1/1`: R no contiene reemplazo ni context-transition. Cuenta/contexto/estrategia/contrato se comparan exactos, jamás se eliminan. No normalización global de IDs/hashes/timestamps.

Mapas fijados por declaraciones tipadas del trace alineado: SIGNAL; admisión provider; OPERATION_SNAPSHOT; ORDER_SNAPSHOT; COMMAND; ORDER_OBSERVATION; FILL; ORDER_ACTION_OBSERVATION. Dos diccionarios por namespace impiden fusión y reasignación; una segunda declaración incompatible rechaza. Cada aparición se contrasta contra ese mapa fijo, incluyendo snapshot orders, fill/command/provider ref, coordinate.owner_ref y owner_key sólo cuando identifican orden. Gramáticas explícitas: `sim-order:<order>`, `sim-exec:<order>:<ordinal>`, `FILL:<provider_execution>`, solicitud `adm:<cuenta>:<account_strategy>:<cycle>:<signal>`. `payload.detail` NO ignorado: debe ser exactamente `stage-1 admission request ` concatenado con request_id, y ese request termina en la señal mapeada; cuerpo/causa conservados. Toda otra hoja distinta rechaza, incluso precio, fecha, kind y hash no clasificado.

Resultados:88.362/88.362 records;109records distintos; primera divergencia cruda `seq85915 payload.signal_id`, cero divergencias de la comparación tipada acotada. Mapas:run1/señal1/solicitud1/operación1/órdenes9/provider_order_ref9/provider_execution_id6/command_id3/action_id3. `r-oracle.json` conserva todas las parejas completas, generación y hashes. Gráfico independiente por cada extremo:1operación,9órdenes,45referencias tipadas; ninguna fusión/reasignación/huérfano de órdenes/operaciones/cuentas; snapshots asignan misma cuenta/estrategia/ciclo; definiciones preceden comandos, observaciones/fills y acciones. root_input_ordinal no decrece; step_seq estrictamente aumenta; tiempos y fases iguales entre extremos. Una causa económica FILL precede a la fila FILL de publicación dentro del mismo root: no inventar la regla de que toda referencia debe aparecer después de su fila de evidencia. Su correlación se verifica por provider_execution mapeada; la secuencia causal real permanece intacta.

Negativo independiente, sin ejecutar motor: COPIA en memoria del candidato; en primer FILL seq85929 sustituir sólo order_id por otra de las9órdenes existentes, conservar operation_id, precio, qty, ejecución, cuentas y todo el dinero. Mapa fijado antes de mutación; rechaza `reference seq=85929 path=.payload.fill.order_id`. El negativo de precio del preliminar no fue repetido ni usado como sustituto. Asset `DISPOSABLE_REPRODUCER` para el delta mutado en memoria, no artefacto histórico falso ni nueva exportación.

### B — contratos de header/footer/integridad separados

`gzip.decompress` verifica CRC/cierre de ambos R. Recomputación independiente SHA256 con encuadre por record de8bytes longitud big-endian + bytes JSON EXACTOS, y logical seal header||records_sha256||footer con sólo logical_sha256 vaciado: ambos coinciden con sellos propios. Control records `68c8db54f4ecef039e1c99a67595e9c176ca79c7c99dcd4f0bf5b1754ddc4fdf`, logical `8c91b4e0bacc0433dab911de18354b504ec3f48f2d0e1bbf884ecc53ccdff8d4`; candidato records `588c8d9843e9a3dcff0d5ac102712c8d983d35c200fb4057f339eba1af36c63e`, logical `cd3c9a01f23e933102e6f521150cfdc5d624d839662e554a4b269747bbfad0c6`. No se comparan hashes cross-build como si debieran ser iguales.

Inputs son iguales quitando EXCLUSIVAMENTE BuildIdentity; resolved_spec idéntico; input_sha/run_id cambian de acuerdo con su identidad de build. El oráculo recomputa además el digest SHA256 de los bytes exactos inputs del footer y verifica run_id=bt-<input_sha256>: controlf03be4183ea74abd583cdbdba630381b9c273ec7eb28bb08ac3d2b16e98ac74a/candidato78e17fe0a9797c3d34ddf9eee3bbbb1849125646c323c3fd92d3253927b86daf. Dataset/config/execution model/schedule/context/time bounds permanecen exactos. Footer summary COMPLETE, first_error null, último cursor1.674.851, economics98.020,18/-1.935/44,82/net−1.979,82/6fills/1operación idénticos, residuales idénticos: día/stage abiertos y3timers pendientes explícitos. Controls/control_admissions nulos y control_dispositions ausente en ambos R: igualdad de ausencia, no evidencia de todos los contratos de admisión. Ledger/risk digests iguales, input_sequence digest igual llevado `93b75e765c2b2a72833e1becfb672ab4286e1a015abbc7b0e03cd0edc443bfd8`, NO recomputado desde inputs externos en esta auditoría.

Provider state digest DIFERENTE:control `ff27d84fba6a6febaceebfff0d981b73f3e9278a475ef4a366da7bf821a18993`, candidato `f644d2db0bb28d1eb3f895162ffa9feb02a4e9bb3d2d684920b27231c0187c51`. Sin preimagen final recuperada, no normalizar ni afirmar que todo el estado del proveedor es equivalente. `PROVIDER_FINAL_STATE_EQUIVALENCE=NOT_DEMONSTRATED`; la biyección de la traza real y dinero no cierra ese contrato. Tampoco acredita automáticamente el fixture ALL/SKIP, otros builds, múltiples generaciones ni programa entero. S04 requiere preservar/exportar preimagen tipada final o replay comparable autorizado que permita su mapa exacto.

### C — NQZ5 forense, identidad y frontera íntegra

Input `inputs/campaign-NQZ5-optimized.json` declara candidato584a/bin e5d4860b y descriptor autorizado NQZ5, warmup13oct17:52Z/trade27oct17:52Z/horizonte27nov18:00Z. Spool existente: `out-opt-NQZ5/bt-c-e4cc8f263b77628887517f57542c5a69c9a06d84cedaec92c4462fd623e41348/attempt-dm0ct6ccs13a-bec43c43f142/result.json.gz`,90225184bytes,SHA256 `2acbfe38122f18a65b9a5d7d7e7848563ccc83d04c990d3f3ebe804d5304f180`; rc `measure/opt-NQZ5.rc=NQZ5_RC=124`. Run header coincide con directorio/attempt; binding al bin es input preservado y stamps/hash, no footer final ausente. Estado `CENSORED_PREFIX_FORENSIC`, jamás COMPLETE.

`prefix.py` descomprime con zlib gzip de manera incremental y JSONDecoder recupera sólo objetos completos. Primer intento propio de parser se interrumpió tras~270s por copias repetidas del buffer; se corrigió sólo tooling propio a cursor incremental y finalizó lectura en~24s. No motor ni spool editado; tiempo agregado de lectura del spool aproximadamente294s, dentro del límite300s. El recibo final devuelve2.764.371objetos, `gzip_eof=false`,92bytes de objeto siguiente incompleto. Conteo preliminar2.764.372 incluye una frontera adicional que NO es objeto JSON completo bajo este oráculo; corregir denominador. Último completo seq2.764.371,root3.578.967,step2.845.190,ts `2025-11-21T21:01:45.257142857Z`. No footer, CRC final, resumen, dispositions, admissions finales ni publicación completa; no resume desde spool.

### C — reconciliación tipada, cuentas y revisiones

Eventos íntegros y ventanas en `nqz5-events.json` y `nqz5-windows.json`; asserts sin producto en `check_prefix.py`, resultados `nqz5-oracle.json`. Generación1 `btg-NQZ5-20251027-acct-1` termina evidencia económica rev70629/saldo98000,9; reemplazo seq2009468 a18nov08:06Z nombra cuenta anterior1 y nueva2, contexto nuevo2-ctx/EVALUATION, nominal100000. Cuenta2 primer ECONOMICS seq2009469 revision3/saldo100000. No continuidad de revision70629 a3 cruzando ledger: mapas por cuenta/generación. ECONOMICS recuperados completos:80768 =70627cuenta1(rev3..70629)+10141cuenta2(rev3..10143), cero gaps/duplicados internos en esos rangos. Inicialización1/2 no publicada en este formato; no declarar que este spool captura absolutamente cada revisión del lifetime antes de su primer3.

| Paso cuenta2 | Record seq | Revisión/cadena exacta |
|---|---:|---|
| Último fill que alcanza target | 2342370 | rev4868, saldo103010,56, stage_net3010,56, día1510,2 |
| PASS latched lógico | 2342381 | MODELED_EVALUATION_PASS, AWAITING_NEXT_CONTEXT,2traded_days; aún EVALUATION |
| Reset económico | 2342382/2342383 | rev4869, CASHFLOW reset−3010,56; saldo100000; excluido de performance, stage PnL3010,56 conservado |
| SetAccountContext | 2342385 | rev4870, CONTEXT:acct-2-ctx |
| CloseStage | 2342386 | rev4871, STAGE_CLOSE:EVALUATION |
| OpenStage | 2342387 | rev4872, STAGE_OPEN:FUNDED; stage PnL0, día1510,2 conservado |
| Publicación typed transition | 2342388 | control pass-funded-2, START_NEW_STAGE/CONTINUE_CURRENT_DAY/REPLACE_EXPLICIT_RISK_SEED |
| Pausa posterior | 2546048/2546049 | rev7621, CONTEXT:acct-2-ctx, stage FUNDED preservado, binding.enabled=false, saldo101500,18 |

Batch4870→4871→4872 íntegro y ordenado bajo mismo root3.172.021 a20nov `01:55:16.19631902Z`; no se descartan intermedias. CONTINUE_CURRENT_DAY exige conservar cuenta-día19nov y no un OpenAccountDay adicional aquí; PRESERVE_STAGE/CONTINUE_CURRENT_DAY de pausa sólo compromete SetAccountContext7621. Las revisiones posteriores de día quedan dentro de la secuencia de revision sin gaps observada; no inventar una transición START_NEW_CONTEXT_DAY inexistente. Context_id se mantiene al cambiar stage, por eso se verifica digest con ambos campos.

Hash independiente del JSON ordenado `{context_id,stage_id}`: EVALUATION `409766e3f6fb4995fbeaed7bf9c0876266b6756b65b9402950b7a9701018ae45` corresponde a expected_context_digest del reset y transición; FUNDED `c7ec59251a19b4ac003721e9fa52a4f09c188bb99c0cc9385167702b4c922687` corresponde a expected_context_digest de pausa. Esto corrobora autoridad lógica FUNDED instalada posteriormente, además de next_context y stage economics. Funded instala términosversion2 sin target/min-days, selectoresMM FUNDED INITIAL, floor98000 y binding enabled=true; pausa posteriormente lo deshabilita, no cambia a EVALUATION aunque binding.phase histórico permanezca EVALUATION. No usar ese campo solo como autoridad económica.

Solicitud FUNDED: inferida del control tipado aplicado y flujo source `campaign.applyAccountPolicy`; no recibo standalone anterior. Admisión aceptada: inferida por haber sido aplicado, pero sello de cuerpo/digest en admission antes de aplicación `NOT_AVAILABLE` porque vive en footer.inputs.ControlAdmissions ausente. Aplicación FUNDED: ECONOMICS+typed transition observados. Estado lógico FUNDED posterior: expected-context digest de pausa + next_context lo corroboran. Publicación/autoridad final durable/historial release runtime: `NOT_DEMONSTRATED` a nivel final; fuente preserva guard `revision == ledger.seq`, batch contiguo y rechazo swapped/reentrant, pero spool no es checkpoint durable.

Cobros: el único ACCOUNT_CASHFLOW del prefijo es RESET_ADJUSTMENT, no PAYOUT_DEBIT. Pausa21nov00:00 corresponde por source a requestPayout tras saldo101500,18: solicitud/inferencia, NO cobro efectivo. No se recupera debit ni resume en el prefijo completo; no convertir saldo residual1500,18 a caja cobrada, ni fourth requested a fourth collected. Campaign footer/cash ledger final ausente: collected amount/cash/purchases final `NOT_CERTIFIED`. Ausencia de error textual no es oráculo suficiente; la evidencia positiva es cadena tipada, continuidad de revisiones y progreso completo posterior, con límites anteriores explícitos.

### Resultado, obligaciones conservadas y activos

| Pregunta | Resultado acotado | Gate pendiente |
|---|---|---|
| A sello | Recetas reproducidas; publicado no reproducible; antes-primer-cambio NOT_DEMONSTRATED | Owner/GOD adjudica freeze; repair actual sin retrofecha |
| B R | Biyección/traza/negativo/integridad PASS acotado | Provider preimagen final, input-sequence externo; ALL/SKIP separado |
| C NQZ5 | PREFIX_TYPED_CHAIN_CORROBORATED; contigüidad4870–4872 y FUNDED posterior | Footer/admisiones/dispositions/Close/autoridad/publicación/cobros finales y horizonte S04 |
| Performance |2,2279× sólo R; ancla NQU6 BASIC180s FAIL reutilizada | Horizons/ratios comparables y pool; no aceptación retrospectiva |

| NOT_RUN requisito | Motivo | Oráculo requerido | Gate |
|---|---|---|---|
| NQZ5 horizonte completo/replay campaña | Prohibido nuevo backtest; spool truncado no resume | Nueva corrida desde input autorizado, driver campaña completo y seal/caja/revisiones | S04 correctness+histórico |
| State provider cross-build final | Preimagen no está conservada en R | Comparación tipada de preimagen/mapping refs sin descartar hash | S04 equivalencia |
| Recomputar input_sequence desde feed | No nuevo replay ni export; igualdad sellada no recomputación | Encuadre exacto de inputs consumidos en ejecución autorizada | S04 integridad |
| Freeze antes primer cambio | No recibo fronterizo encontrado | Snapshot/tree/receipt independiente anterior a edición inicial | Owner/GOD freeze |
| Pool/horizonte full/comparación no-regresión | R y timeouts insuficientes; no perfiles/corridas largas | Workload COMPLETE comparable + workers/resources efectivos | S04 performance |
| ALL/SKIP y adversarios safety restantes | Par distinto/función de TOP B; no ampliación rutinaria | Primera divergencia tipada con causa/refs y assertions de dominio | S03 TOP B/S04 |

Assets: `compare_r.py` y sus mapas/grafo/negativo = HARNESS_TOOLKIT_CANDIDATE, reutilizable como comparador entre builds con extensión explícita de generación/definiciones, no promoción automática. `prefix.py` = HARNESS_TOOLKIT_CANDIDATE, recuperación read-only de JSON gzip truncado con frontera íntegra y EOF explícito. `check_prefix.py` = E2E_CANDIDATE para invariant batch/contexto/cashflow de este prefijo real, fixture fechado/hashes específicos requieren dueño antes de promoción. `receipts.py`/`identity-cut.json`/`input-cuts.json`/`seal.json` = HARNESS_TOOLKIT_CANDIDATE de corte reproducible, sin reseal implícito. `inspect_r.py`, r-inspection/r-diffs y mutación sólo en memoria = DISPOSABLE_REPRODUCER de clasificación/negativo acotado; no duplicar en vault. PERMANENT_REGRESSION promovidos=NONE (S04/Owner decide dueño).

`REUSABLE_BEHAVIOR_CANDIDATES`: (1) separar integridad del artefacto, biyección de traza y estado final; un mapa correcto no legitima normalizar un digest opaco. (2) recuperar sólo JSON completo y declarar siguiente parcial; contar tokens record_seq sobre gzip truncado sobrecuenta frontera. (3) cursor incremental para spool evita quadratic buffer copying y respeta ventana forense. Clase propuesta tooling/test_harness, capturada en feedback, ninguna skill pública editada.

### Reproducción real y cierre

Comandos ejecutados (desde home autorizado; scripts y receipts están bajo raíz externa indicada):

```sh
timeout 120s python3 aranea/work/btx-perf-s03-top-a-20261009/receipts.py
timeout 120s python3 aranea/work/btx-perf-s03-top-a-20261009/compare_r.py
timeout 300s python3 aranea/work/btx-perf-s03-top-a-20261009/prefix.py
timeout 120s python3 aranea/work/btx-perf-s03-top-a-20261009/check_prefix.py
go version -m aranea/work/btx-perf-s02-20261009/bin/echo-backtest-control
go version -m aranea/work/btx-perf-s02-20261009/bin/echo-backtest-optimized
go version -m aranea/work/btx-perf-s03-top-20261009/bin/echo-backtest-s03
```

Scripts guardan outputs exactos bajo su propia raíz; `receipts.py` inspecciona originales sin escribirlos. Pasar scripts relativos funciona desde home autorizado; no son instrucciones de backtest. Primer comparador rechazó namespace action_id no clasificado seq86033; se añadió declaración ORDER_ACTION_OBSERVATION con referencia a COMMAND y el run final pasa; no relajar campos. Primera versión de parser cancelada por costo de copia; versión final recuperó frontera y rc0. Todos los procesos propios cerrados; no procesos financieros propios. Sesión worker cerrada por mandato; continuidad durable en este documento, agent-run y feedback; ningún L0/L1 ni memoria global modificada. Owner/Primary siguen abiertos, no se cerraron chats ajenos. Sin commit/push manual, LIVE/broker/ETCD/PROD, permisos o aceptación final.

## Fuentes

[[BTG-PLAN]], [[BTX-PERF-DESIGN]], [[BTX-PERF-IMPLEMENTATION]], [[BTX-PERF-S03-TOP-EVIDENCE]]; paquete externo `aranea/work/btx-perf-s03-top-a-20261009/` con SHA256MANIFEST final y cuts por input. Source puntual `xKoRx/echo` HEADbbbcc1d5: `v3/backtester/README.md`, `resultwriter.go`, `result.go`, `controls.go`, `identity.go`, `run.go`, `driver.go`, `campaign.go`, `sdk/futures/accounting/ledger.go`. Originales S02 y preliminar local permanecen raíces autorizadas. Agent-run `80-agents/journal/agent-runs/2026-10-09-codex-unknown-btx-perf-s03-top-a.md`; feedback `80-agents/journal/feedback/system-1/2026-10-09-btx-perf-s03-top-a-session-feedback.md`; change_log único `80-agents/journal/logs/2026-10-09-btx-perf-s03-top-a-change-log.md`.

### SHA256 completos de entradas y artefactos leídos

La tabla selecciona bindings relevantes; `input-cuts.json` conserva todos los cortes, incluyendo measure y autoridades.

| Archivo operativo relativo a home autorizado | Bytes | SHA256 |
|---|---:|---|
| aranea/work/btx-perf-s02-20261009/inputs/basic-NQU6-R-control.json | 1039 | 337b60aa9588c40b9ef388a4e84983357e393a7cb5531c64358e3c96e92c54c1 |
| aranea/work/btx-perf-s02-20261009/inputs/basic-NQU6-R-optimized.json | 1039 | 287b38fe1082e50281c3f8f32270cd720da0ce6f39e780296685a8526e968f67 |
| aranea/work/btx-perf-s02-20261009/inputs/campaign-NQZ5-optimized.json | 1348 | 89f5f1ece421ecfbabafcf0dfd5347c47197ac8ebe8ecd37698cc2bdd6110b36 |
| aranea/work/btx-perf-s02-20261009/out-control-R/bt-f03be4183ea74abd583cdbdba630381b9c273ec7eb28bb08ac3d2b16e98ac74a/result.json.gz | 4411269 | 8f429779fbf0ef7caf790094cf0234d53aede6d39bfca753efb8bd7629c3c519 |
| aranea/work/btx-perf-s02-20261009/out-opt-R/bt-78e17fe0a9797c3d34ddf9eee3bbbb1849125646c323c3fd92d3253927b86daf/result.json.gz | 7064679 | 8d6c572cd711f12feace50c1fb5c51c97fb14a0541c4903e57cfb0e9f4ead533 |
| aranea/work/btx-perf-s02-20261009/out-opt-NQZ5/bt-c-e4cc8f263b77628887517f57542c5a69c9a06d84cedaec92c4462fd623e41348/attempt-dm0ct6ccs13a-bec43c43f142/result.json.gz | 90225184 | 2acbfe38122f18a65b9a5d7d7e7848563ccc83d04c990d3f3ebe804d5304f180 |
| aranea/work/btg-s06-user-oneshot-20261008/inputs/nt/NQZ5/nt-source.json | 803 | 11e9b5fb69a220d973fcd3bd14edcce282eca24af786496223149cb563209ed8 |
| aranea/work/btg-s06-user-oneshot-20261008/inputs/nt/NQU6/nt-source.json | 803 | b21238f4dabfea566d4a73f46c7544cd4acf3701d206ceb0a7f29904408de13e |
| aranea/work/btg-s01-20261006/reports/real-gap-forensics/derived-nt-weekly-v1/NQ 09-26.Last.txt | 4946161 | d4cbbdcdbe7bcb2932f1fbfb1418e8f12a52ef3305df29d5619a19cef6112be3 |
| aranea/work/btg-s06-user-oneshot-20261008/inputs/nt/NQZ5/nt-source.json | 803 | 11e9b5fb69a220d973fcd3bd14edcce282eca24af786496223149cb563209ed8 |
| aranea/work/btg-s01-20261006/reports/real-gap-forensics/derived-nt-weekly-v1/NQ 12-25.Last.txt | 4748275 | 700579b3b3c78e58ccceb39bd79e8d11aa3efab3e8457d92bee1833ef2686406 |
| aranea/work/btx-perf-s02-20261009/prepared-control/runspec.json | 13360 | 83e3a03e972c591778c0957eb2938ac6f1d2b31774edd84017e6bacec3c2c7ac |
| aranea/work/btx-perf-s02-20261009/prepared-control/manifest.json | 108474 | 98a455fa28dff8c66ac125b431accb8534e6a1ab63eb0c33720d8b4df41a3f02 |
| aranea/work/btx-perf-s02-20261009/prepared-optimized/runspec.json | 13360 | fba05b791c61e6e9605356f59ebf14aed2817665f50dc43cf8382b9490155de4 |
| aranea/work/btx-perf-s02-20261009/prepared-optimized/manifest.json | 108474 | 98a455fa28dff8c66ac125b431accb8534e6a1ab63eb0c33720d8b4df41a3f02 |
