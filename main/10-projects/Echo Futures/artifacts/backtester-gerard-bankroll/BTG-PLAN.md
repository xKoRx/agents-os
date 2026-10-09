---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTX-PERF-DESIGN]]"
  - "[[BTX-PERF-IMPLEMENTATION]]"
  - "[[BTG-S05-REMEDIATION-AND-RESULTS]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-05"
updated: "2026-10-09"
---

# BTG-PLAN — Estado vigente y continuidad del backtester

## Propósito

Control operativo único de BTX-PERF para [[Echo Futures]]: cuatro shots, una trayectoria financiera integrada por modalidad, dominio runtime compartido y módulos sustituibles. Correctness, performance, usabilidad integrada y cobertura son obligaciones separadas. No optimizar ROI ni certificar rentabilidad o readiness física. Primary coordina, no implementa ni acepta el producto.

Esta edición adjudica la entrega S02 aportada por Owner. El control anterior íntegro queda preservado en Git `534daa16b9e043192250b8def8adee2fca6bd800`, mismo path; el informe del autor y el bloque PERF_CONTRACT NO se modifican. Los estados del autor se distinguen de la adjudicación Primary. Las reglas técnicas completas de [[BTX-PERF-DESIGN]] y su adenda Owner siguen vigentes; no se retiran requisitos por esta compactación.

## Contenido

### Estado vigente — adjudicación Primary de S02, 2026-10-09

```text
PROGRAM = BTX-PERF
PRIMARY_SESSION = OPEN_UNTIL_EXPLICIT_OWNER_CLOSE
S01_TECHNICAL_DESIGN = ACCEPTED_FOR_IMPLEMENTATION_WITH_EXPLICIT_PERF_EXCEPTION
E1 = PARTIAL_WITH_EVIDENCE
S02_OWNER_AUTHORIZATION = AUTHORIZED_REPAIR_AND_INTEGRATION
S02_DELIVERY = RECEIVED
S02_AUTHOR_STATUS = READY_FOR_S03_REVIEW_WITH_PERF_HORIZON_BLOCK
S02_PRIMARY_ADJUDICATION = PARTIAL_IMPLEMENTATION_WITH_MATERIAL_GAPS
S02_COMPLETE_IMPLEMENTATION_ACCEPTED = NO
PERF_TARGET_FREEZE = REQUIRED_BEFORE_OPTIMIZATIONS
PERF_CONTRACT_SEAL = REPORTED_BY_AUTHOR_NOT_INDEPENDENTLY_RECONSTRUCTED
PERF_CONTRACT_SUFFICIENT_JUSTIFICATION = NOT_ACCEPTED_BY_PRIMARY
FINAL_OWNER_ACCEPTANCE = NOT_GRANTED
CURRENT_ACTION = BOUNDED_INDEPENDENT_FALSIFICATION_WITHIN_S03
S03 = NOT_EXECUTED_BY_PRIMARY_PROMPT_READY
S04 = PRESERVED_CORRECTION_AND_FINAL_VALIDATION_NOT_STARTED
PRODUCT_CHANGES_TESTS_PROFILES_RUNS_BY_PRIMARY = NONE
PHYSICAL_RUNTIME_READINESS = NOT_DEMONSTRATED_OUT_OF_SCOPE
PROMOTION = NOT_ACCEPTED_NO_MERGE_OR_DEPLOY
```

Primary leyó el informe publicado, los deltas Git y source puntual de los owners necesarios para contrastar el handoff. No ejecutó tests, descargó perfiles ni inspeccionó los bytes de los recibos locales. Los dos incumplimientos de interfaz están confirmados por source; los tiempos, replay y RED/GREEN permanecen evidencia REPORTADA hasta verificación independiente. No presentar esta revisión de manager como S03 ejecutado.

### Adjudicación por hallazgo

| ID | Hallazgo y alcance de evidencia | Decisión |
|---|---|---|
| M1 | `v3/backtester/cmd/echo-backtest/experiment.go`, cmdExperiment, exige exactamente un stream y usa Streams[0]. Source en bbbcc1d5. | Usabilidad multicontrato FAIL por carencia de implementación, no bloqueo externo de datos. La nueva entrada no cumple todavía el experimento integrado solicitado. |
| M2 | En ese archivo, CAMPAIGN no rellena ExperimentManifest.Artifact; `cmd/echo-backtest/reproduce.go` exige Artifact no vacío para --experiment. | El replay público de CAMPAIGN por el manifest que genera la propia entrada está roto por contrato de source. Exigir prueba ejecutada independiente corta. El PASS de ReproduceCampaign vía fixtureFactory no cubre esa ruta. |
| M3 | PERF_CONTRACT publicado fija NQU6 BASIC<=180s; el mismo informe reporta timeout del candidato a900s. MIN_SPEEDUP se exige sobre R y NQU6 completo, pero sólo R tiene pareja COMPLETE. | Ancla NQU6 BASIC FAIL según evidencia del autor, pendiente contrastar los recibos exactos; no NOT_VERIFIED sin más. MIN_SPEEDUP global NOT_DEMONSTRATED, prefijo R 2,23x REPORTADO. Horizonte todos los años y CAMPAIGN no heredan ese resultado. |
| M4 | El contrato extrapola45,2us/root-input de un prefijo con warmup y presupone tasa uniforme. Luego el informe la considera refutada. Ambos timeouts a600s se usan para afirmar ausencia de regresión. | Sello previo no valida fundamento. No aceptar el contrato como evidencia suficiente de la precondición Owner ni aceptar no-regresión de dos tiempos censurados. Proyección5h no equivale a corrida5h ni a coste inevitable demostrado. |
| M5 | `compareLegacyCLIArtifacts` hace Logf+return cuando difieren RunID, antes de comprobar ExecutionState, InputSHA256 y hashes. | Ese verde no acredita el comparador histórico entre builds. Drift legítimo se adjudica con oráculo tipado; un replay con la misma build no lo reemplaza. No declarar fraude ni asumir defectos económicos sin prueba. |
| M6 | NQZ5 real no alcanzó la transición del20nov2025; el informe sitúa el spool parcial en21oct. Test de campaña usa fxCorpus/fxSpec y factory de fixture. Funciones nuevas críticas69–83% y58,1% agregado selectivo, ocho fallos reportados preexistentes. | Correctness histórica y floor95% no cerrados. Un fixture es evidencia útil, no NQZ5 histórico. Preexistente describe origen, no aceptación; clasificar impacto de los ocho fallos y denominadores, no llenar coverage cosmético. |
| M7 | El autor declara omitido el pool de preparación por no dominar R; la comparación de32 archivos no cambia el adapter ntminute. `RecentShared` comparte el almacenamiento del ring;109 diferencias de IDs reportadas sin mapa inspeccionado por Primary. | No acreditar paralelismo implementado. Ownership público y mapeo uno-a-uno/referencias son objetivos del verificador, no bugs ejecutados por el manager. |

Fuentes de M1/M2/M5/M7: source `xKoRx/echo` en `bbbcc1d5dc0ed18badae46b4eba1a17822632b60`, archivos indicados y `v3/sdk/futures/bars/ring.go`. Fuente de métricas/omisiones: [[BTX-PERF-IMPLEMENTATION]] en Agents-OS `534daa16b9e043192250b8def8adee2fca6bd800`, blob `cec0feaede7e52cdd9b742c0ebfd63179c158207`. Fixture leído: `v3/backtester/btx_s02_campaign_replay_test.go`.

Gates del objetivo completo: correctness NOT_DEMONSTRATED con defectos públicos materiales; performance FAIL en el ancla NQU6 reportada y NOT_DEMONSTRATED en horizontes/ratios restantes; usabilidad integrada FAIL_SOURCE_CONFIRMED; cobertura total NOT_DEMONSTRATED. No READY_FOR_OWNER_ACCEPTANCE. Un resultado útil parcial no consume ni aprueba por sí solo S03/S04.

### Trabajo útil conservado y builds exactas

El source contiene repairs de batch/retenido y payloads de admisión, replay de controlador por API y optimizaciones por perfiles. El autor reporta RED minimo rev5→7, GREEN y ratio R BASIC75,77s→34,01s, CPU141,79s→48,69s, RSS60,4→54,5MiB,88362records/6fills y dinero igual. Es avance reutilizable; no prueba universal ni dato físico reejecutado por Primary. El porcentaje de allocations y atribución CPU se conservan como reportados en el informe, sin recomponerlos desde memoria.

| Identidad | Valor |
|---|---|
| Baseline source/documentación | `50250a2b0df6106943108bf6bfe57552409f3d13` |
| Código histórico | `d1b1446d401f88cfa42dee2eb959120305f5a372` |
| Control corregido | `d609ca241eed63b1b4413af5bae5b849d334ead0` |
| Binario control reportado | `0db2feae6237ebc20ba8ce16bcc9f50fee0e6809c3677585b403a3d708c490ee` |
| Candidato medido | `584a3cd91d8ecf2d8f292547a35f8e9963e2270d` |
| Binario candidato reportado | `e5d4860b4e70f5f5833ebf374b08fb771a4551bc6d58996fa42305e1049bd141` |
| HEAD remoto observado codex/btx-perf-s02 | `bbbcc1d5dc0ed18badae46b4eba1a17822632b60` |
| Diferencia584a→bbb | Sólo README y prueba btx_s02_ring_shared_test.go; no transferir identidad de binario por inferencia |
| Sello PERF_CONTRACT reportado | `ff320f01e9954eefaf84de5380b78e8b99e334d42ac10bf50f018d34ae89079d` |
| Binario E1 | `66657a99384ff6e622da15cd6953ea34621edc35100b536f118d1ff3918a89fb` |
| Registro E1 | `52d17ce92321fe0673eeaf1ed59d7e8753d47af7`, no contiene cápsula completa |

Evidencia local: workspaces `aranea/work/btx-perf-s02-20261009/`, `aranea/work/btx-perf-s01-e1-20261008/` y `aranea/work/btg-s06-user-oneshot-20261008/`, relativos al home autorizado en Daedalus. El prompt de transporte conserva los localizadores absolutos Owner; no son montajes acreditados en CLOUD. Consumir cápsula/recibos existentes y verificar hashes, no reconstruirla, reexportar NinjaTrader, clonar por worker o ampliar ACL. GitHub permite lectura/escritura documental demostrada; eso no concede ejecución física de Daedalus a Primary.

### Autoridad Owner que sigue vigente

Adenda9oct2026: un integrador TOP LOCAL S02 fresh-context ONE-SHOT. Secuencia autorizada: captura CPU focalizada de R sellado, timeout120s y una corrección mecánica instrumental máxima → repairs de correctness/interfaz/replay → control corregido sin optimizaciones → contrato numérico sustentado y sellado → optimizaciones. Sin fundamento suficiente para el contrato completo, entregar repairs verificados y bloqueo sin optimizaciones, no mover objetivos después del resultado. La adjudicación actual no modifica retrospectivamente ese permiso ni el bloque histórico del autor.

BASIC100000 continuo sin lifecycle prop; CAMPAIGN caja5000, compra ON_DEMAND120, una cuenta operando, máximo cuatro COBROS efectivos y reinversión. Pérdida nominal no debita caja otra vez. Strategy/MM compartidos sustituibles; S2/GerardMM son configuración de prueba. Sin if Gerard, cambio de SL/TP/sizing/adds/señales, recorder descartable ni dinero flotante para acelerar.

Preparación/lectura por stream con buffers acotados y merge estable antes del dominio; dependencias de Strategy/MM/riesgo/cuenta/caja preservadas. Diseño C financiera1, pool hasta2 sujeto a recursos, chunks256records/1MiB serializado sin confundir esa cota con RSS. No sumar campañas/contratos reiniciados ni otro motor de indicadores. Rollover prospectivo por autoridades declaradas, warmup por requisitos, obligaciones del retirado conservadas; selección futura no equivale a deuda corriente. No copiar año/mes inicial ni usar siempre catalog[0]. No inventar fechas/feriados/precios/fills o continuidad sobre gaps.

Historial: conservar TODAS las revisiones comprometidas SetAccountContext(k)→CloseStage(k+1)→OpenStage(k+2), autoridad final coherente y release únicamente de evidencia poseída del ledger/generación correctos con guard de autoridad corriente. Prohibidos LatestRevision como descarte, guard<= e ignorar errores. Cuerpo tipado/digest sellado al admitir, incluso REJECTED/CONFLICT/pendiente o Apply fallido; idempotencia/conflictos preservados. Replay recompone CAMPAIGN y no readmite externamente sus controles regenerados. Original esperaba ACCOUNT_REPLACEMENT, reproducción produjo OPERATION_APPLY.

Equivalencia entre builds/horizontes admite sólo diferencias tipadas justificadas y mapeos IDs uno-a-uno con referencias; no supresión genérica de IDs/hashes/timestamps/kinds. No comparar campaña vieja abortada como denominador. Separar PASS latched, solicitud/admisión/aplicación FUNDED, funded activo y cobros; no inferir0pases. Cuarto solicitado no es cuarto cobrado; residual forfeited no es caja; compra aplicada no es activación ni refund implícito.

### Reloj, independencia y próximos shots

Ventana histórica `2026-10-09T00:00:00-03:00` EXPIRED; T0 histórico180min UNKNOWN; continuación S02 fue autorizada sin presupuesto total nuevo. No reiniciar180min ni aprobar4h o ventanas dedicadas por sugerencia de un worker. Límites reales del harness se registran como tales. Procesos propios terminan en la sesión.

| Shot | Responsabilidad | Estado y evidencia |
|---|---|---|
| S01 | Arquitecto GOD CLOUD distinto del manager; probe TOP LOCAL E1 | Diseño aceptado con excepción, E1 parcial; diseño materializado en8942ee2f y registro E1 en52d17ce9 |
| S02 | Integrador TOP LOCAL ONE-SHOT | Entregado; Primary lo adjudica parcial con M1–M7, no implementación completa |
| S03 | GOD CLOUD independiente del arquitecto/autor, con TOP independiente que escribe/ejecuta falsificadores | Sin ejecutar aquí. Primer trabajo preparado: TOP LOCAL falsifica M1/M2 y verifica oráculos/recibos; GOD independiente adjudica dentro del mismo shot. No reemplazar su dictamen por este control |
| S04 | TOP fresco y comprobación independiente acotada | Correcciones/validación final conservadas; sin garantía inventada de que alcanzará para cumplir todo |

Primero pruebas cortas sobre rechazo multistream y replay por manifest propio. Si confirman RED estructural, no gastar horas en reruns completos300/600/900s o auditoría general de capacidad ausente. Completar falsificadores cortos que cambien repairs S04; devolver RED temprano y declarar el resto NOT_RUN. No convertir S03 en implementación, nueva investigación, quinto shot o reactivación de S02 cerrado. La verificación aún no realizada sigue obligatoria; RED temprano no equivale a S03 totalmente completado.

### Despacho y persistencia

Único siguiente prompt de transporte: Library `/BTX-PERF-S03-TOP-LOCAL-VERIFICATION-PROMPT.md`, `library_file_id=libfile_4bcf419d25f88191a9bc1dd65d1123f2`, backing `file_00000000a780820ea975f22bd8fbc57a`;15929bytes, SHA256 `8fb80bf567395943ce0bd4209c23408fb362585d1e3487ac3c65af780c556141`. Es ejecución técnica dentro de S03, no un shot nuevo, worker ya iniciado ni dictamen independiente GOD ya devuelto. Sin herramienta de despacho directo, Owner transporta el prompt.

TOP conserva producto/originales y escribe sólo pruebas independientes en verificación aislada y evidencia. Entrega propuesta `BTX-PERF-S03-TOP-EVIDENCE.md`; `BTX-PERF-ADVERSARIAL.md` sigue reservado al dictamen independiente de S03. No más controles paralelos. Workers dejan agent-run/feedback y cierran su propia sesión; no Primary. Ningún PASS por source review, rc0, aborto idéntico o conciliación aislada.

Agents-OS sólo master, un escritor por delta, blob SHA/readback y preservación de cambios concurrentes. Sin ramas/PRs/worktrees documentales. Registro consolidado en [[2026-10-09-btx-perf-s02-owner-amendment]] mediante adición de esta adjudicación, sin reescribir la adenda anterior. No código de producto/tests/scripts, merge/deploy, broker/cuentas/órdenes, PROD/ETCD, permisos, feedback o cierre de Primary en esta revisión. Modelos/tokens/cuotas no expuestos UNKNOWN; no contar despachos planeados.

## Baseline histórico BTG-S05 — referencia preservada

Owner cerró BTG8oct2026 como PASS_BOUNDED_OFFLINE_SOFTWARE,16findings S04 e invarianciaIDs sobre d1b. Reejecución final terminada; no volver a pedirla como pendiente. WarmupNQZ3=2023-10-15T22:00Z, trading=2023-10-29T22:00Z, fin exclusivo2023-11-23T03:29Z, V2/CONFIGURED. BinarioS05 `520d5343a1171796b67daa43875ac71ebeb9ce2c5ad39f84737c7adba44a84f1`. BASIC116fills/neto−43405.84/saldo56594.16; CAMPAIGN22fills/neto−6151.60/caja4640/3compras/2reemplazos/0cobros. First/replay826.715/911.089s BASIC y751.442/721.335s CAMPAIGN, bajo concurrencia.

[[BTG-S05-REMEDIATION-AND-RESULTS]] conserva evidencia y release `btg-s05-id-invariance-d1b1446d`; paquete112640203bytes SHA256 `e95b178e61240ca39200f8da6be23c9c62554b2661b9821d7fe1f249062fa907`. No transferir resultados, coverage o provenance al candidato. Plazo BTG7oct/cierre8oct incumplido, no retrofechar. Cobertura multianual y readiness física nunca aprobadas; D6 separado en otra build, nuevo riesgo físico no habilitado.

## Fuentes

- Mandato BTX-PERF y adenda Owner9oct2026 de esta sesión, que preservan cuatro shots, independencia y aceptación final humana.
- [[BTX-PERF-DESIGN]], [[BTX-PERF-IMPLEMENTATION]] y control previo en534daa16, mismo path.
- Source Echo bbbcc1d5: cmd/experiment.go, cmd/reproduce.go, cmd/native_cli_e2e_test.go, btx_s02_campaign_replay_test.go y sdk/futures/bars/ring.go; compare5025→bbb y584a→bbb consultados autenticadamente.
- E1 registro52d17ce9 y [[BTG-S05-REMEDIATION-AND-RESULTS]] sólo en sus ámbitos probados.
