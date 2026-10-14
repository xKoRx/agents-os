---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[TRADESGERARD-CONTROL]]"
  - "[[TRADESGERARD-ENTRY-REPAIR]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-13"
updated: "2026-10-13"
---

# TRADESGERARD-OPERABILITY-T0

## Propósito

Recibir C4 y verificar el cambio prospectivo de operabilidad del mandato GOD LOCAL del Owner, PROMPT_VERSION1, 2026-10-13. T0 es técnico; no acredita rentabilidad. Estado vigente **O9_CONSISTENCY_HOLD / COMMON_POLICY_CORRECTION**: el segundo test con ledger autoritativo confirmó el bloqueo erróneo al alcanzar3000 sin cumplir consistencia. El primer intento permanece HARNESS_AUTHORITY_ERROR y no sustenta la atribución. No se lanzaron campañas O9; integrador corrige la autoridad compartida mientras F2 avanza aislado. Campañas O8/F1 drenadas; sus resultados se preservan AFFECTED fuera del ranking. Sus PASS técnicos conservan el alcance probado y no sustituyen la nueva verificación.

## Contenido

### O10 congelado — remanente efectivo compartido, gate pendiente

Source `76a1e69e5a0a67b94b920e2ffb983fd226eb127a`, árbol `aebf5e8724147b343e525e2594fbed7f42fafff4`, checkout limpio comprobado por manager. Binario `implementer/bin/echo-backtest-o10` SHA256 físico `3c66a1b091fde81a7804e38eb265f16078005c1fc211db46e62f690cb04426bf`. Manifiesto `implementer/evidence/o10-freeze-manifest.json` SHA256 físico `f8168673e089d8ed9be9a9535ba46209a54c073aec33fbe5ddc5a36490c1cb6c`, veinte inputs F0/F1. Helper de provider deriva el objetivo efectivo con su comparador de consistencia estricto y grid USD0,01 del perfil; MM y selección comparten ese remanente. Usa max(mejor día cerrado, día actual); mantiene target nominal si no hay regla de consistencia. No modifica lifecycle ni costos ni acredita pagos.

Integrador reporta GREEN del fixture real3,601s, SDK/provider/TGMM/config y críticos PASS, cobertura delta48/50=96%. Estos son resultados del autor; verificación independiente exacta todavía pendiente. Reserva física del manifiesto9.818.783.744B, presupuesto agregado nuevo1.610.612.736B incluyendo evidencia afectada; admisión se medirá de nuevo antes de lanzar. Cuarenta trayectorias siguen pendientes de validación económica final.

### O9 congelado — HOLD confirmado por consistencia autoritativa

Recibo independiente durable `verifier/independent-o9-HOLD.json`, SHA256 `83503df1c9e6d1dda555f6f97a2679156ba45415f5c9b9d76ecd1152bfda723d`, identifica source/binario/fixture/logs y separa expresamente el primer error de harness. Manager comprobó físicamente su hash. Lease O9 liberado; próximo corte común O10 en implementación, sin campañas lanzadas todavía.

Segundo intento con autoridad real confirmado por el verificador: `TestVerifierRealLedgerConsistencyPreventsFalseCompletedObjective`, exit1/FAIL5,508s. Dos días con fills q1 BUY100→SELL160,25 y BUY100→SELL190,25, comisión2,49 por lado, producen ledger Balance53000,04/StagePnL3000,04/BestDay cerrado1800,02/currentday0; las precondiciones autoritativas pasan. `objectiveCapacity` devuelve incorrectamente COMPLETED/remaining−0,04/Rref500. Evidencia `verifier/evaluation_consistency_adversarial_test.go` y `verifier/o9-consistency-real-RED.log`. Este segundo caso demuestra el defecto y justifica HOLD O9 antes de ejecutar campañas. Manager autoriza corrección compartida desde la regla del provider, sin fórmula paralela ni pase artificial. La comparación real `EvaluateConsistencyShared` rechaza share≥threshold: igualdad no aprueba; el remanente deberá respetar esa frontera y la unidad monetaria realizable. El fixture anterior permanece separado como error de harness.

El primer intento `TestVerifierEvaluationConsistencyPreventsFalseCompletedObjective`, log `verifier/o9-completed-objective-independent.log`, FAIL1,870s, fue corregido de atribución por el verificador: el fixture modificaba BestDay en lastRev, pero `accountEconomicsFromRevision/platformBestDay` lo sustituye desde ledger closed/current, donde todavía era0. Se conserva como HARNESS_AUTHORITY_ERROR, no como RED de producto. Manager había atribuido prematuramente el log; se corrigió también en chat. El verificador prepara el caso con dos días de operaciones reales de fixture en ledger antes de emitir dictamen. Sólo si ese caso demuestra el defecto se corregirá el objetivo efectivo compartido, sin forzar aprobación. O9 permanece quieto; los smokes siguientes no habilitan campañas. SR avanza en un checkout separado.

Continuación del Owner recibida; ambos TOP retomaron ejecución. Source `cf855c7a3cffd276d5bf24458417a4dd7940863b`, árbol `1bf69f984eb4ea5b7ef948b1e2aa733fde923d5d`, checkout `implementer/echo-t0-corrected` limpio comprobado. Binario `implementer/bin/echo-backtest-o9` SHA256 `3ed52db8d418f7ff23b8074c932d75b59c1aeee8a1ad22093ca8edeaba4dee4f`; manifiesto `implementer/evidence/o9-freeze-manifest.json` SHA256 `30ef1d3b9eef0539db0dd9d30f9184b833577d400854340a06ee682e96cceffa`, veinte inputs F0/F1 bajo una política común. O9 añade espera `OBJECTIVE_MET_WAITING_TRANSITION`, pausa diaria ante objetivo completado y guard que restringe offsets OHLC modelados a BACKTEST explícito. Conserva las fechas de elegibilidad y pago.

El integrador entrega smokes exactos reconciliados: F0 23cruces/23aceptados/23operaciones/17fallback/caja4760; F1 23cruces/14aceptados/9rechazados/14operaciones/10fallback/caja4640. Recibo `implementer/evidence/o9-frozen-smoke-receipt.json`. Son diagnósticos de una sesión, no filas económicas finales. Gate independiente O9 aún pendiente; no se han relanzado las veinte campañas por estos smokes solamente. Cobertura del autor19/19 bloques afectados pendiente de recálculo independiente.

### HOLD posterior — objetivo alcanzado y espera de cumplimiento

K03 O8 cuenta11 LIVESIM alcanzó2305,36USD realizados, superior al objetivo2300, pero siguió ELIGIBLE y consumió seis cruces12nov19:18–20:38Z con `OBJECTIVE_ALREADY_MET` y ningún fill. Cuatro cuentas EVALUATION16–19 estaban elegibles desde15Z, flat y drenadas; cuenta16 tenía saldo51640,26/progreso1640,26/headroom1975,16. La cuenta financiada debía esperar `CompliantAt=2025-11-13T15:01:06.114649681Z`, los dos días hábiles del perfil, y ceder turno mientras tanto. No faltaban ganancias ni se debe inventar un nuevo requisito de días operados.

La causa compartida: `RequestedObjectiveBudget` devuelve Rref/Tref cuando remaining≤0 y la clasificación COMPLETED no libera selección antes del MM. El pago posterior1651 está conciliado y se conserva como observado; la trayectoria no es un resultado definitivo del experimento corregido. Dictamen independiente `verifier/o8-K03-completed-objective-selection-HOLD.json`, SHA256 `8adeca2cfa8dd5207cf6256677773aba222cdb7f01b5e54130d98f5743e4efd1`.

Adjudicación: pausa/espera de objetivo completado con reevaluación desde autoridad y selección causal de alternativa; no retiro EOD, ni liberación de plaza comercial falsa, ni crédito anticipado, ni reset de saldo/piso. Verificación independiente RED/GREEN debe cubrir el caso positivo de payout diferido, la alternativa elegible, y la tabla diario/evaluación/funded con objetivo real y consistencia. El mismo build O9 podrá ejecutar F0/F1; sus veinte configuraciones se repetirán antes de ranking. SR/F2 y F3 siguen dentro del mandato.

Parada verificada00:22:07Z: manager identificó los supervisores propios2963227/2979615 y envió un SIGINT a cada uno. Sus bloques finally drenaron los cuatro hijos, preservaron recibos parciales y salieronexit130; procesos ya ausentes. T1 O8 conserva cuatro COMPLETE, dos CANCELLED_DRAINEDexit2 y cuatro no lanzadas; T2 F1 conserva dos CANCELLED_DRAINEDexit2 y ocho no lanzadas. Cancelaciones técnicas, no pérdidas de trading. Scratch propio0B. Invalidación `implementer/evidence/o8-f1-objective-completed-invalidation.json` SHA256 `bc1a8402277dceccbe615a5fab3c00bdd3e55e98a44cf714c27cbb44e2c0c29f`; snapshots `T1-o8-progress-AFFECTED-frozen.json` SHA256 `12da33ea86df017ee576c1e5a0612db4e6a7151ce478e5f8809f5d608765a9a8` y `T2-f1-progress-AFFECTED-frozen.json` SHA256 `6a0ff6e04155c9194a1b631eeaa9da76de8386c5653e6363c9586e8f1b6d827a` en el mismo directorio. Presupuesto nuevo debe incluir toda esta evidencia retenida.

### O8 — bloqueo de capacidad del objetivo, gate técnico histórico

Freeze físico comprobado por manager: source `d66bb56bccd053305c1c7dac0dc51aa292745504`, checkout causal limpio, binario `implementer/bin/echo-backtest-o8` SHA256 `a70ac11e481109b036f4a7d792c9594f8c8a73c97eb7c72cd35f2c0c025de8ce`; manifiesto `implementer/evidence/o8-freeze-manifest.json` con diez inputs. O8 reutiliza `TGMM.RequestedObjectiveBudget` tanto en entry del MM como en selección: misma autoridad para solicitud económica antes de headroom, sin fórmulas paralelas en driver. Añade pausa temporal por remanente diario insuficiente y bloqueo de objetivo de fase reevaluable por autoridad; conserva saldo, piso, plaza e historial. Un remanente de pase no recupera capacidad ficticia por reset diario.

Verificador ejecutó el mismo RED O7 sobre O8 y negativos, PASS3,702s: diario9,60 libera turno, rho4/T9,60/R38,40 permanece operable, igualdad24,98 permanece admisible y pase9,60 no se retira ni se trata como pausa diaria, pero deja operar la sucesora. Recheck SDK PASS0,015s, E2E físico12LONG/SHORT PASS4,356s, lifecycle seis nombres exactos PASS1,915s, paridad diez inputs PASS_TEN y binario coincidente. Cobertura recalculada independientemente53/54=98,1481% de bloques afectados O7→O8; no coverage global. Errores de overlay/decoder de pruebas y dos selecciones regex demasiado amplias canceladas quedaron como HARNESS_ERROR/CANCELLED, sin reclasificarlos como fallos de producto o PASS ni modificar aserciones monetarias.

Gate exacto `verifier/independent-o8-gate.json`, SHA256 `0afa455654df3a7362dc1c6e0c8a24a4e871af3e3490f24a71a348ed6f376de0`, **INDEPENDENT_PASS técnico**. Manager corroboró source limpio, árbol `0083e0d0d9854779c240971d17749593755413a8`, binario y hashes de los cinco logs/recibos incluidos. El gate permite ejecutar/auditar T1; no constituye resultado económico ni aceptación final del Owner. Smoke CLI real O8 COMPLETE y auditoría streaming independiente solicitada como recibo adicional. O7 I/O y su codec se conservan por identidad de caminos; sus resultados económicos afectados no se reutilizan.

Smoke CLI O8 posteriormente auditado streaming PASS en recibo separado `verifier/independent-o8-smoke-gate.json` SHA256 `90957558490a53b02e8b8ddfc357722a6b5cd052ae9c8935adef4476f3ef89e8`, sin sobrescribir gate anterior. Una sesión:23cruces base,23operaciones/46fills,17fallback,0Q0,UNKNOWN0 y0campos económicos ausentes. Comparación K exacta, error máximo ATR7,1e−15 frente oráculo float;23/23primeros fills con marca contemporánea OpenMark−15/net−24,98. PnL de cuentas−994,88/+295,34, saldos49005,12/50295,34; caja4760 por dos compras120, conciliación y residual0flat/terminal. Diagnóstico técnico, no fila del ranking ni prueba de toda la ventana.

### Dependencia runtime y guard de modalidad

Dependencia runtime comprobada después del gate offline F1: `SnapshotViews.Market()` devuelve `readModelMarket`, que implementa Mark/Ready pero no `operation.ExecutableQuoteSource`. La nueva política de mínimo con quote observado exige esa autoridad en `execution_minimum.go`; por tanto F0–F3 con esa política están funcionalmente bloqueados en la ruta runtime actual. F1/F3 requieren además la autoridad de completitud H1 documentada en [[TRADESGERARD-OPERABILITY-T2]]. Los campos de piso diario/EOD/claims, costos, metadata y protección tienen seams offline verificados; no se inventa que falten todos, pero tampoco se certifica autoridad del adapter real por tests offline.

Finding independiente adicional: `config.NewTGMM` en sourceF1 `f4643aef` ignora RunMode y admite offsets OHLC modelados incluso con LIVE, EXACT_REPLAY, vacío o UNKNOWN. Probe de construcción de configuración, sin servicios ni órdenes, produjo RED exacto en esos cuatro negativos; el positivo BACKTEST y la ausencia de quote-source en SnapshotViews quedaron comprobados. Evidencia `verifier/runtime-operability-dependencies-and-mode-RED.json`, SHA256 `77edf7a977774df38fee65dcdb2fd5f332dcffdaa4d254bb979087d1a30b04d5`.

Adjudicación manager ejecutada en candidato O9: restringir offsets OHLC modelados a BACKTEST explícito, con mismo RED/GREEN independiente y prueba de semántica BACKTEST conservada. No fabricar BBO, no cambiar matching ni abrir un adapter nuevo. Las campañas O8/F1 se drenaron por el defecto económico de selección descrito arriba; el guard de modalidad por sí solo no invalida el camino offline. No se declara la política lista para operar con broker.

### Recepción y dispatch

C4 source `88ed70d1ff9910bb157f1c14c0fed1d2b8e7ec49`, árbol limpio comprobado con Git; SHA256 físico del binario `c8849bb6e5523e8625ead8282f0d97f98d8b02e14d72838e3c35de207c6bcd57`. Checkout relativo a ARANEA_ROOT: `work/tradesgerard-entry-repair-20261013/implementer/echo-c4`. La evidencia final C4 acredita diez campañas completas; bitácoras anteriores no se convierten en pendientes actuales. C4 y sus resultados se preservan.

TOP LOCAL implementador único `/root/operability_integrator`; TOP LOCAL verificador `/root/operability_verifier`. Modelo solicitado `gpt-6.1-sol`, servido UNKNOWN. Dispatch real mediante subagentes de esta sesión, sin nuevo manager ni dependencia GLM. El integrador recibió el delta de mínimo económico y retiro EOD; el verificador recibió primero la reconstrucción por operación de la racha K05, seguida de falsación independiente exacta. Sus entregas aún no constituyen gate aprobado.

Nueva evidencia relativa a ARANEA_ROOT: `work/tradesgerard-operability-20261013/{implementer,verifier}`. CONTROL pertenece al manager; cada worker conserva un informe propio. Escrituras canónicas por materializador y sincronización separada de su mera existencia local.

### Hallazgo K05 entregado

[[TRADESGERARD-OPERABILITY-K05-STREAK]] reconstruye doce operaciones desde C4 físico: sin pérdidas previas; once ganancias cuenta1=2495,22 y faltante504,78, una ganancia cuenta2=260,04. La racha agregada2755,26 cruza dos cuentas de evaluación; no existe pase/pago omitido en ese corte. El cambio proviene de pausa diaria y compra causal siguiente cruce. Caja4520 y neto de ledger−279,46 conciliados por separado. Readback manager y sync remoto `5ef845ce923d37e7025c506f54756f659663eba2`; la barrera TP económica postfill no retenida queda como límite de evidencia, sin inferirla del neto.

### Recursos y fronteras vigentes

Lectura física inicial del manager:13.190.447.104 bytes libres y aproximadamente62.612MiB de memoria available. Son observaciones puntuales. Se mantienen reserva disco≥8GiB, scratch agregado≤2GiB, lote≤256MiB y traza/log≤16MiB. Presupuesto agregado nuevo, dependencias, perfil, inputs y request real se fijan en el recibo del integrador antes de ejecutar; no se hereda un presupuesto por cambiar carpeta.

Sólo trabajo offline aislado. Ningún resultado económico nuevo todavía. No LIVE, cambios de servicios/permisos, operaciones reales ni promoción productiva. Aceptación final del Owner separada; el mandato permite continuar automáticamente entre las tandas acotadas después de su verificación técnica.

### Finding independiente en desarrollo — cap residual

El verificador identificó en `xKoRx/echo:v3/backtester/platform_campaign.go`, working tree T0, que `maybeRequest` todavía recorta `PayoutTarget` al remanente del cap. Ejemplos:3000→2000 después de un pago3000, o2300→400 después de4600. El mandato nuevo exige conservar el objetivo2300/3000 y no presentar un cobro menor como logro. Manager adjudicó corrección acotada del contrato nuevo, preservando C4; reproducer determinista independiente y corrección/gate pendientes. No es una pérdida de trading ni un resultado de las cuarenta campañas.

### Candidato T0 y HOLD del mínimo ejecutable

Candidato congelado `87e33b0c333a1f2f4178dfefe06126d50691c7ad`, limpio comprobado por manager. Cobertura de desarrollo `CONSERVATIVE_DIFF_BLOCKS_V1`:115/120=95,8333%, bloques Go completos que intersectan líneas productivas añadidas/reemplazadas; no cobertura AST ni global. Primer overlay independiente SDK PASS, pero no habilita T1 por sí solo.

Manager cuestionó que `MinimumExecutableRisk` añadiera un tick a los costos prefill y retirara una cuenta con margen15,28 al calcular19,98. Verificador inspeccionó el adapter: no acredita una distancia mínima de un tick desde mark. Ejemplo algebraico por falsar causalmente: fill LONG100,25, stop100, costos pendientes9,98 produce pérdida proyectada14,98≤15,28. Integrador reconoce que el tick adicional era un supuesto suyo, no restricción probada; se conserva el candidato y sus resultados como diagnóstico, sin campañas T1. Prueba Venue/Provider/reservas/fill/protección real y corrección acotada pendientes; no se modifica el simulador para sostener el supuesto. El mínimo definitivo deberá derivarse del contrato ejecutable y sus costos, sin hardcode ni afirmación de legalidad de broker.

### Adjudicación física del mínimo — V-MIN

Pruebas independientes conservadas sobre87e33b0c: Venue12casos LONG/SHORT×offset0/1×precio posterior sin cambio/favorable/adverso, PASS0,007s; ProviderRisk+Ledger20casos, PASS0,639s. Con spread cero y slippage1tick por lado, salida estática neta−14,98; con offsets bid1/ask1 del descriptor C4,−24,98. No son garantías frente a movimiento/slippage. Con C4 y margen15,28, la equity tras entrada cae a47997,79 frente piso48000: breach antes de protección. Con19,98, entrada todavía válida pero salida estática deja47995 y breach. Igualdad24,98 termina exactamente en48000 y activa regla de piso hit-inclusive;25,28 deja48000,30. La igualdad de presupuesto admite riesgo de fallo al stop; no se la transforma automáticamente en cuenta permanentemente perdida si la orden y una oportunidad causal son válidas.

Se rechaza el fundamento anterior tick-extra como mínimo legal demostrado. Integrador corrige desde el descriptor/costos estructurales, sin alterar el matching C4 ni endurecer el adapter. `implementer/echo-t0-corrected`, rama `codex/tradesgerard-operability-correction-20261013`, nace del candidato87; anterior quieto. El presupuesto nuevo único incluye ambos checkouts. Los probes Provider/Ledger no incluyen por sí solos Operation admission; la verificación final exigirá ese seam real además de los casos unitarios.

La prueba independiente de retiro/demanda finalmente PASS0,949s tras usar `nextNYOpen` real; fallos previos eran fixtures fuera de sesión y quedan registrados, no bugs de producto. Claims y matriz cap4casos PASS. Evidencia relativa a nuevo root: `verifier/{venue-minimum-87e33b0c-attempt2.log,provider-minimum-87e33b0c.log,backtester-demand-87e33b0c-attempt6.log}`. Gate T1 continúa HOLD hasta freeze corregido y recheck exacto.

### Freeze V2 y finding de valoración stale en callback

Source corregido `cb9cc0cd997e78bbf7f777a5291482b6c9870bfd`, árbol limpio comprobado; binario `implementer/bin/echo-backtest-c2` SHA256 `34a300eecabf3baa55519fc6322cb1b524161c2c9471a8602742231c7e407a45`, hash físico leído. Políticas `ECONOMIC_MINIMUM_V2` y `ECONOMIC_MINIMUM_RETIRE_V2`; perfil comercial y horizon C4 preservados. Delta cobertura177/181=97,790055% bloques completos; SDK, money/policy/NT físico, Core typed LIVE/BACKTEST offline y vet del autor PASS. No certificación de LIVE ni gate independiente final.

E2E independiente V2: seis negativos LONG/SHORT con R14,98/15,28/19,98 no generan fills. Al investigar positivos cercanos al mínimo, el verificador halló un defecto monetario: primer fill LONG14:01:06.666 a100,75 con cursor actual100,25, pero MM_FILL recibe equity50377,51 y Cycle.open_mark380/net_liquidation370,02 desde mark anterior119,75/cierre120. MM considera TP25,28 logrado y la salida siguiente a100 realiza−19,98. No se acepta como cierre inmediato legítimo; el supuesto de marca contemporánea está contradicho. Evidencia `verifier/e2e-cb9cc0cd/long-R25.28-trace.ndjson.gz` y resultado propio. Caso de fixture, no PnL del ranking; aún no se extrapola a todas las campañas C4.

Manager adjudicó HOLD y corrección upstream acotada de valoración/autoridad antes de callback, con reproducción de atribución y RED/GREEN en el mismo assert. No guard compensatorio TG, no alterar retrospectivamente fills/precios ni simulador para fabricar resultado. Original cb9 debe permanecer quieto; integrador único y verificador independientes continúan. T1 todavía no lanzada.

### Atribución de la valoración stale a C4

Verificador ejecutó el mismo assert monetario sobre C4 `88ed70d1`, con política nueva OFF, TGMM real resuelto por su factory y presupuesto500 que permite cantidad ATR. RED exit1 en2,027s para LONG y SHORT: OpenMark380/net370,02 publicados frente a OpenMark−15/net−24,98 exigidos por la cotización causal. `verifier/fill-authority-C4-red-attempt2.log` y resultados/traces correspondientes conservados. Primer intento usó un constructor legacy y no abrió operaciones; se conserva como error propio de harness, no evidencia del defecto.

La raíz preexistente omite marcar ledger en `processNativeStep`/`markNative` cuando está flat con entrada working antes del matching. Integrador corrige sólo la autoridad upstream incluyendo obligaciones pendientes; debe conservar guards de cuenta/contrato y ausencia de efectos cuando no hay inventario ni orden. Los resultados C4 se conservan como observados; la propiedad general de valoración contemporánea tras fill tiene un contraejemplo. Esto no demuestra que todas sus755oportunidades o todos sus netos estén errados. F0 nuevo incluirá este fix además de políticas mínima/retirada; no se atribuirá toda diferencia a una única causa ni se inventará PnL contrafactual.

### Candidato C3 — regresión ALL/skip pendiente

Source local `0db7e3656ee7e3404da6c55a96cad5a4710b9201`, árbol limpio comprobado, binario `implementer/bin/echo-backtest-c3` SHA256 físico `6ed1590041ef96fa00ccd60aecc4d40454d3df30e5a06592a0cb7536e17ef660`. El mismo reproductor monetario pasa tras el parche; críticos nuevos4,224s, SDK/config y paridad Core LIVE/BACKTEST offline PASS. Guard contable incluye inventario, órdenes working y claims físicos del mismo contrato aún no liberados. No se ha emitido gate independiente ni manifiesto final admisible.

Suite afectada exit1 en98,240s: `TestBTGS05_RealPendingReservationsAndProtectionALLSkip` y `TestBTGS05_NativeFixturePartialDuplicateDelayedFinalityALLSkip` divergen en record25.signal_id entre ALL/skip. Evidencia `implementer/evidence/c3-final-policy.log`. Candidato **HOLD**; no se debilita el assert ni se atribuye una causa todavía. Integrador investiga primera divergencia causal antes de repetir la suite; verificador informado. Las40campañas siguen sin ejecutar.

Presupuesto nuevo agregado mantiene1.610.612.736bytes, separado de evidencia C4 existente770.330.496bytes. Reasignación interna prospectiva para conservar builds y resultados: durable1.476.395.008bytes y scratch134.217.728bytes. Se mantienen scratch global≤2GiB, lote≤256MiB, traza/log≤16MiB y reserva física≥8GiB; se exige pronóstico completo de40configuraciones y derivados antes del lanzamiento. Checkout87 detenido puede reutilizarse para el delta de filtros sólo preservando commit/binario/inputs/evidencia y comprobando ausencia de escritores; no reinicia presupuesto ni permite borrar historia.

### Adjudicación ALL/skip y nuevo finding temporal V-DAY

Los mismos dos asserts ALL/skip fallan idénticamente en cb9 en0,159s y en C4 en0,177s. Verificador identificó una referencia `OPERATION_APPLY` de `SIGNAL_DELIVERY.signal_id` comparada como literal aunque un SIGNAL previo ya establece la biyección: RunID difiere legítimamente por modo, mientras eval_seq,signal_seq,trigger ytimestamp coinciden. Se conserva el fallo histórico; no se adjudica como regresión monetaria de C3. Overlay externo independiente comprobará relaciones referenciales tipadas previamente definidas y todas las aserciones semánticas; no se cambian ni debilitan los tests históricos. C3 manifiesto ya disponible, cobertura nueva185/188=98,4043%, con los fallos heredados de la suite explícitos.

Smoke C3 físico CLI COMPLETE/reconciled:6operaciones con entrada,12fills,6fallbacks,23materializaciones; caja4880 y traza265678bytes. Diagnóstico de una sesión, no ranking. Manager detectó17rechazos posteriores con neto diario−994,88; verificador e integrador confirmaron políticaV2 activa, margen diario5,12<24,98 y margen EOD1005,12. Sin exposición ni órdenes, la cuenta permanecía ELIGIBLE y consumía cruces16:12–19:40Z. Finding **V-DAY: política temporal incompleta**, no ruina EOD ni ausencia de señales. Se corrige pausa por capacidad diaria insuficiente tras drenaje, con recuperación en próximo día sin regenerar piso y selección/demanda causal de otra cuenta. Candidato0db/bin6ed y smoke se preservan; T1 sigue pendiente de freeze corregido y gate independiente exacto.

### O6 verificado y delta de salida acotado

Source O6 `74034811df66beb23f9e8bc8431fbfc7db7f00f0`, árbol `65aa13fa6f128840eb37534f3b67b88368f40dfd`, limpio; binario `implementer/bin/echo-backtest-o6` SHA256 `dd9a528db292fdfd2646319f0115b1dfcbdd144106810278b6fd30c0b27ab214`, lectura física manager. Gate independiente `verifier/independent-o6-gate.json` SHA256 `65c90be21776fed3543277b66e0f6d08b39fb1a53c331dc67ea69c953e6cf14c`: **INDEPENDENT_PASS**. Sus cinco logs coinciden físicamente con hashes del recibo. Platform2,353s, SDK0,008s, same-assert de marca monetaria GREEN, tee detailed→expandedcompact LONG/SHORT1,428s y ALL/skip con negativos de identidad0,215s PASS. Cobertura independiente227/233=97,4248927%, bloques completos que intersectan líneas nuevas/reemplazadas; diez inputs preservan perfil, datos y horizonte C4 fuera de cambios autorizados explícitos.

Smoke independiente de ese binario:23cruces,23entradas,23cierres,17fallbacks, UNKNOWN0, ledger/caja conciliados y caja4760. Cuenta1 pausada por capacidad diaria insuficiente, preserva saldo49005,12 y EOD; cuenta2 compra causal y saldo50295,34. No retiros acreditados en este diagnóstico y no reemplaza las diez campañas completas F0. Frente a C3 smoke, se eliminó el bloqueo de17rechazos diarios repetidos; frente a C4 completa la comparación sigue pendiente y estará afectada también por el fix de marca, no sólo por mínimo/retiro.

O6 reduce repetición de sizing mediante schema explícito `MM_SIZING_ANCHOR_DELTA_V1`, anchor de materialización, deltas y remociones reconstructibles. Consumidor independiente rechaza versión desconocida, delta huérfano y remoción inexistente. Traza smoke561518bytes frente624912O4, pero extrapolar máxima actividad755 daría18,43MB y supera16MiB. Manager autoriza delta mínimo de gzip streaming lossless con stdlib/ruta I/O existente, receipt encoding/path versionado y hash de bytes durables después de Flush/Close; C4 plain compatible. Cap físico16MiB y lectura descomprimida acotada≤256MiB, sin carga completa a RAM. Recheck incluirá paridad, integridad/resume, error/cancelación y pronóstico agregado. No framework nuevo ni poda de dinero/finality para cumplir disco. O6 se conserva; lease liberado después de drenar Go independiente, siguiente freeze de salida separado antes de T1.

### Preparación causal de filtros e intervalo adicional

El inventario físico independiente encontró13contratos NQZ3→NQZ6, aproximadamente1,2millones de minutos entre2023-10-01 y2026-10-06. Presencia de corpus no acredita uno o tres años válidos. NQZ5 permite prefijo H1 más largo del mismo archivo; la hora2025-10-13T17:00–18:00Z tiene59minutos y no se fabrica su cierre. El oráculo conserva las25últimas H1 completas válidas y excluye explícitamente esa hora; K/ATR1m mantienen el calentamiento C4 original. La adopción en el módulo compartido sigue pendiente de implementación y verificación. Oráculo diagnóstico:755cruces base,331aprobados F1,65F2,16F3 y cero cruces con H1 no disponible usando el prefijo largo; son controles de señal, no resultados de campaña ni garantía de fills.

Antes del ranking se reservó un intervalo adicional por fecha/cobertura, sin mirar PnL: NQZ6, warmup2026-09-21T00:00Z, trade_start2026-09-22T14:00Z, end_exclusive2026-10-02T21:00Z. Fuente SHA256 `2176dce88405aee7fe5383cf1244330ad83fe0b0f1105abe9c7b198a30555141`; conteo físico semanal13680minutos,2220de prefijo y11460de trading, sin huecos en ese intervalo. No se ha demostrado que nunca fuera usado en todo el proyecto: clasificación **exploratorio adicional**, no holdout intacto certificado. Recibo `verifier/prospective-additional-interval.json` conserva el criterio y un intervalo previo rechazado por112minutos faltantes; no relleno de precios ni nueva descarga. Su ejecución depende del ranking acotado y la validación del descriptor/calendario.

### Tandas autorizadas por ejecutar

T0 políticas y racha → T1 F0×10 → T2 F1×10 → T3 F2×10 → T4 F3×10 → clasificación de40configuraciones y ampliación disponible de hasta cuatro configuraciones activas. Hallazgos materiales se corrigen y las trayectorias afectadas se repiten. No hay garantía de cobro; cobro acreditado y caja neta se informan por separado.

Regla operativa del ranking declarada antes de completarlo: ordenar configuraciones con al menos una operación real por caja neta, luego neto acreditado, evaluaciones aprobadas e ID estable; tomar los primeros dos pares únicos(filtro,perfil económico) y mantener ambos retiros en la ampliación, máximo cuatro configuraciones. No repetir variantes inactivas por ganar un empate vacío ni sumar los pares de retiro como mercados independientes. El primer resultado parcial F0–K01–r2300 no modifica esta regla.

## Fuentes

- Mandato Owner TRADESGERARD — GOD LOCAL: OPERABILIDAD, CAMPAÑAS Y FILTROS KISS, PROMPT_VERSION1,2026-10-13.
- [[TRADESGERARD-ENTRY-REPAIR]], [[TRADESGERARD-CONTROL]], [[TRADESGERARD-B-PLAN]], [[TRADESGERARD-PROP-PROFILE]].
- Recepción física manager: Git HEAD/status, sha256sum, df y free; dispatch local y acuse del integrador en la sesión activa.
