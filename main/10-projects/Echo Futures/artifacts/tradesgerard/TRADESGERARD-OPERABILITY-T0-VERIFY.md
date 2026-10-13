---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[TRADESGERARD-OPERABILITY-T0]]"
  - "[[TRADESGERARD-OPERABILITY-K05-STREAK]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-13"
updated: "2026-10-13"
---

# TRADESGERARD-OPERABILITY-T0-VERIFY

## Dictamen vigente

**HOLD vigente — candidatos87e33b0c y cb9cc0cd no habilitan campañas.** Verificación independiente LOCAL, solicitado Sol6.1 y servido UNKNOWN. Source limpio87e33b0c333a1f2f4178dfefe06126d50691c7ad, binario físico verificado89b645fcc1ea7ca7a47ed75a5a88e05d4adbbd2d9a9d6e111d39d010b8afd89b. Los probes monetarios descubrieron un supuesto no acreditado en el mínimo económico: un tick extra llamado «nearest legal protection» no existe en validateSubmit del adapter. El implementador prepara corrección aislada; cobertura autor95,833% no reemplaza este finding ni admite T1.

## Hallazgos y evidencia física

V-OP-01, contrato nuevo de cap: la ruta heredada maybeRequest recortaba el retiro solicitado2300/3000 a su remanente cap. El mandato vigente lo prohíbe. Se corrigió opt-in en87: TRANSITION_PENDING y cap_blocked_residual, sin solicitud menor. Oráculo independiente cuatro casos PASS: remaining2000 para target3000 y remaining400 para target2300 no solicitan; remaining3000/2300 exactos sí solicitan el total. C4 sin política nueva conserva su contrato histórico; no se recategoriza como bug retrospectivo.

V-OP-02, mínimo económico: MinimumExecutableRisk87 calculaba q_min×(tickValue+2fees+2slippageTicks×tickValue),19,98 para el descriptor C4. El oráculo aritmético PASS27 combinaciones sólo acredita esa fórmula, **no acredita que sea el mínimo del adapter**. Validación STOP_MARKET exige precio positivo y forma de comando; no impone una distancia mínima de un tick contra el mark. No se añadió una restricción al simulador para sostener el resultado.

Probe Venue causal real, doce casos LONG/SHORT×offset0/1×observación posterior igual/favorable/adversa: usa slip1 y tick0,25. Entrada/stop/exit ocurren en cursores distintos; no hay fill retroactivo. En C4 offsets1 por lado, mark100: LONG entry100,50 y protección100,25 aceptada; posterior mark100 liquida99,50; neto−24,98 incluyendo fees4,98. SHORT es espejo. Con offsets0 declarados: entry100,25/stop100/exit99,75, neto−14,98. C4 con un tick posterior favorable produce−19,98 y adverso−29,98. La proyección de SL desde su precio de orden no garantiza el precio físico: spread/slippage/cursores y gaps permanecen causales.

Probe Ledger→Run.projectEconomics→ProviderRisk real, veinte casos cinco márgenes×offset0/1×LONG/SHORT. Los precios ya confirmados en Venue son inputs de fixture; no se presenta esto como certificación de admisión Operation/egress. Conserva el piso48000 y debita fees por fill una vez. Sin spread, margen15,28 deja48000,30 tras liquidación y no infringe. Con descriptor C4 offsets1, margen15,28 cae a equity47997,79 después de la entrada y falla EOD antes de colocar protección; margen19,98 conserva entry headroom2,49 pero la liquidación deja47995 y falla. Margen24,98 llega exactamente48000: Provider aplica<= y declara breach;25,28 deja48000,30 sin breach. La igualdad del techo presupuestario no evita la igualdad prohibida del piso oficial.

La evidencia permite concluir que15,28 no restaura operabilidad bajo el descriptor C4 exacto. No autoriza copiar24,98 como constante ni retirar por spread actual transitorio: la corrección debe derivar metadata/costos/estructura declarada y distinguir prefilling, fills ya realizados y proyección postfill, sin descontar la entrada dos veces. La legalidad de broker no está certificada. R es techo esperado modelado, no garantía frente a gaps/slippage.

## Probes críticos ya ejecutados

- SDK independiente,27 mínimos de costo aritméticos y8 postfill shifts LONG/SHORT: PASS0,009s, SL proyectado<=R, TP proyectado>=T y presupuestos no aumentados. Primer resultado positivo no se convierte en gate del mínimo real.
- Retirement/demand: PASS0,949s una vez que la fixture avanza por autoridad nextNYOpen hasta la sesión válida. Preserva ledger/piso/caja, no sintetiza pérdida, compra una única sucesora por demanda y caja80 con sucesora viable continúa; retiro no renueva. Claim ejecutable tardío bloquea reemplazo y cap residual/equality cuatro casos PASS.
- Venue causal del mínimo: PASS0,007s doce casos, autoritativo para los precios modelados descritos arriba.
- Provider/Ledger mínimo: PASS0,639s veinte casos, autoritativo para floors/fees/headroom y breach modelados descritos arriba.

Intentos propios preservados: attempt1 de retirement no compiló por comparación de Money no comparable; se corrigió sólo la fixture. Attempt2 usó selector demasiado amplio y se detuvo sólo el proceso propio identificado tras coincidir con tests históricos; CANCELLED_SCOPE_SELECTOR, nunca cobertura/gate. Attempts3–5 fallaban una expectativa de compra en la sesión nocturna inicial de la fixture; motivo físico SESSION_ENTRY_WINDOW, quiescent=true, caja/cupo/horizonte válidos. Attempt6 usa nextNYOpen real y pasa. Venue attempt1 tenía nombre de helper errado; attempt2 pasa. No se atribuyen esos errores de harness a pérdidas económicas ni defectos de producto.

## Oráculos y corpus preparados

Inventario físico una vez:13 contratos NQZ3–NQZ6,2023-10-01→2026-10-06. Esto no prueba un año usable; all13 histórico sigue NOT_READY. Request C4 real: warmup2025-10-13T17:51Z, trade_start2025-10-14T13:30Z, end2025-11-25T23Z;42.969 barras y755 cruces mantienen identidad.

Oráculo H1 solamente con prefijo más largo del mismo NQZ5 y K/ATR originales C4: últimos25 cierres H1 completos, excluye13oct17–18 con59 minutos (falta17:51), mantiene historia como SDK Ring y registra discontinuidad; no fabrica cierre. F1 requiere sólo25 cierres válidos, no25 horas consecutivas. Diagnóstico755base/331F1/65F2/16F3, cero señales H1 unready. No es conteo final de campañas ni ranking; descriptores y source del filtro integrado deben cotejarse después. Oráculo alternativo C4 prefijo corto registra23 señales sin readiness H1. F0 nunca depende de H1.

Intervalo adicional reservado antes de ranking nuevo: NQZ6 warmup2026-09-21T00Z, trade_start2026-09-22T14Z, end2026-10-02T21Z;13.680 minutos esperados=2.220 prefijo+11.460 trading, cero huecos semanales. Candidato temporal inicial tenía112 minutos ausentes y fue rechazado exclusivamente por cobertura, sin PnL. T1/C4/T1-L son conocidos y no son nuevo holdout. No se ha probado que toda investigación histórica jamás haya usado NQZ6: intervalo adicional exploratorio, no certificado intacto. No se descargan datos ni se rellenan precios.

## Reproducción y siguiente gate

Todos los archivos siguientes son relativos a ARANEA_ROOT bajo `work/tradesgerard-operability-20261013/verifier/`; scripts/probes son toolkit/regresiones candidatas o fixtures diagnósticos, nunca estrategias del ranking. Las pruebas usan overlays y no modifican source producto. Commands se reconstruyen con checkout congelado, GOMAXPROCS4, módulo SDK/backtester y selector exacto propio; el overlay JSON conserva rutas locales resueltas sólo en workspace externo.

Corrección siguiente: source/build nuevo y descriptor coherente, paridad shared runtime/offline de seams modificados, tests RED/GREEN si se demuestra defecto y comportamientos nuevos, smoke real, censo completo de oportunidades, safety negativos, cobertura nueva>=95 con denominador/procedencia exacta. Sólo después habrá un gate independiente PASS y habilitación de T1. Los resultados candidatos87 quedan conservados y no entrarán a la comparación económica final.

## Artefactos y hashes

- `sdk-adversarial-87e33b0c.log`, SHA256 `66385e82527aacfb978b6393c0c18f00a852b9de31c62559a1fefa2b56c007fb`.
- `backtester-demand-87e33b0c-attempt6.log`, SHA256 `b9185ef89d44a2826ab615518a4c72ccf3793b5387ce534745401141d5f94583`.
- `backtester-adversarial-87e33b0c-attempt3.log`, SHA256 `cc78d3ff6388ec156af3ca7e6b141a1e2ffcf598408657789797ce0790255941`.
- `venue-minimum-87e33b0c-attempt2.log`, SHA256 `ed77e6b85cb59934aa883cd86227c8c05e493050eadd91b9d5b46c681fb3cd87`.
- `provider-minimum-87e33b0c.log`, SHA256 `bdeeba5f0c5646d0f4d872b7535095e47f46bd68e42d880afc131b263014bc65`.
- `filter-oracle-long-h1-prefix.json.gz`, SHA256 `40cae17e715ad791a8d469df9d514585406d4c4dd387069ab5ac293702d44a32`.
- `prospective-additional-interval.json`, SHA256 `66254848c8b0b9deb69876e069f91c7abe291d0410e088d7de55d088494d9ede`.

Recibo independiente durable `work/tradesgerard-operability-20261013/verifier/independent-t0-hold-87e33b0c.json`: source/tree/bin metadata leídos físicamente, procesos propios drenados, derivados propios861.451 bytes al cierre de este corte.

## Recheck C2 y RED causal compartido

C2 congelado `cb9cc0cd997e78bbf7f777a5291482b6c9870bfd`, árbol limpio, binario SHA256 `34a300eecabf3baa55519fc6322cb1b524161c2c9471a8602742231c7e407a45` leído físicamente con vcs.modified=false. Mínimo V2 deriva2fees+2slip+spread estructural declarado, separa cotización corriente y retiro permanente, elimina el tick mínimo inventado y errores de overflow. El gate continúa HOLD por un segundo finding probado en el callback monetario.

V-FILL-MARK: antes de un primer fill, el optimizador native OHLC conservaba la marca de ledger anterior porque aún estaba flat, aunque existía una orden working y un cursor nuevo. En la fixture LONG actual, primer fill100,75 a14:01:06,666Z; cotización causal mark100,25, exit-side100. Gross de posición esperado−15 y Cycle.net_liquidation esperado−24,98. Se publicaban gross380 y net370,02 por usar marca anterior119,75. TG con T25,28 interpreta objetivo alcanzado y cierra a siguiente cursor100 realizando−19,98, sin protección. SHORT demuestra el mismo defecto espejo. No es lookahead de un precio futuro; es valoración de exposición nueva con una marca previa superada por el cursor causal.

Regresión independiente real `fill_mark_authority_regression_test.go`, SHA256 `dd2477a48d226134057a2b7762ce5fc26bb67093fc98c263d410a8401e8d3261`, compara Cycle.OpenMark y NetLiquidation con cotización disponible, fill real, metadata y costos pendientes. Política nueva OFF; R/T500 compatible con sizing C4, resolución real TGMM por fábrica pública. Misma prueba da RED C4 exacto88ed70d1 (exit1,2,027s) y C2 exactocb9 (exit1,2,051s), LONG/SHORT. Primera versión del harness llamó NewGerardMM legacy y no entró: ese intento se conserva como error propio de constructor, nunca como RED productivo. La regresión corregida usa ResolveMoneyManager y no cambia assert entre fuentes.

La propiedad causal C4 queda AFFECTED por el defecto demostrado. No se extrapola desde estas cintas sintéticas que cada operación o campaña histórica C4 haya sufrido el caso ni que755 identidades cambien. Caja/ledger observados siguen siendo evidencia histórica de sus builds; la corrección upstream afectará las campañas nuevas y obliga identidad nueva. No se modifica matching del simulador ni se oculta el error con un guard en TG.

Near-boundary E2E público ejecutó seis negativos R14,98/15,28/19,98 LONG/SHORT: cero fills, cero protección, sin retirar cuenta EOD viable por presupuesto pequeño. Positivos R24,98/25,28 detectaron la falsa salida inicial anterior; el segundo ciclo sí operó protegido. R500 deja una posición protegida al horizonte de la fixture REPORT_RESIDUALS, que no exige terminalidad: esa expectativa propia se corrigió explícitamente. Los inputs de ranking mantienen su EndPolicy. Se probará el mismo near-boundary E2E y ambos asserts monetarios sobre el corte causal corregido; no se suman probes aislados para declarar FULL E2E.

Evidencia relativa a ARANEA_ROOT: `work/tradesgerard-operability-20261013/verifier/fill-authority-C4-red/`, `fill-authority-cb9-red/`, logs `fill-authority-C4-red-attempt2.log` y `fill-authority-cb9-red.log`, más `e2e-cb9cc0cd/*-trace.ndjson.gz` y resultados por caso. Fixtures fuera del ranking; procesos propios drenados antes de la nueva corrección aislada.

## Corte causal C3 y operabilidad temporal O4

C3 `0db7e3656ee7e3404da6c55a96cad5a4710b9201` corrige publicación de marca antes del fill con inventario, órdenes working o claims ejecutables no liberados del mismo contrato. Provider/ledger/venue son propietarios por cuenta: composeAccount crea OwnerState(accountID) y selección preservada los restaura juntos; no se mezclan claims de todas las cuentas. Negativos de contrato ajeno/released y cancelación permanecen. El siguiente corte O4 `2ec0a8caecc22d3bd92d032ebc4f9e96b53618fc`, binario `6760db167a96f3cf0f8a266879366d9d621d5a6ce59b429fc1057dba44d85a5f`, agrega pausa temporal cuando la capacidad diaria es inferior al mínimo, preservando EOD.

ALL/skip histórico fallaba igual en C4, C2 y C3 por referencias derivadas de RunID tratadas literalmente en el comparador. Dumps demuestran misma primera señal eval_seq2/signal_seq0/trigger/time, RunID distinto por descriptor ALL/SKIP. Comparación independiente mantiene las aserciones completas de dinero/órdenes/causas y sólo normaliza referencias previamente vinculadas por SIGNAL/orden: SIGNAL_DELIVERY.signal_id/operation_id, MM_EVALUATION tipado.signal_id y causa duplicate:FILL:sim-exec:<orden>:<secuencia>, conservando secuencia literal. Dos casos PASS0,239s; originales no modificados y FAIL heredado conservado, no presentado como suite histórica PASS. Negativo de identidad ejecutado durante cambio de source se conserva SUPERSEDED y se repetirá congelado.

V-DAY demostrado físicamente en smoke C3 con policy V2: caja4880, cuenta ELIGIBLE, neto día−994,88, margen EOD1005,12 y capacidad interna5,12 frente mínimo24,98. Diecisiete rechazos Q0 entre16:12 y19:40Z bloquearon la siguiente cuenta aunque quedaba EOD suficiente. O4 introduce PAUSED_TEMPORARY_CAPACITY flat/drained hasta siguiente NY; no retiro, regeneración de piso ni compra sin demanda. Probe independiente O4 demuestra pausa, preservación de ledger/caja/piso, siguiente compra por un cruce causal y continuidad con caja80 y otra cuenta operable.

E2E independiente O4 compartido Operation/admission/fill/protection pasa12 casos LONG/SHORT con R14,98/15,28/19,98 negativos sin fill y R24,98/25,28/500 positivos con fallback/protección. R/T no aumentan; q real y salidas tick válidas se contrastan con economía pendiente. Fixtures REPORT_RESIDUALS R500 conservan exposición protegida al horizonte, sin afirmar terminalidad. Resultado inicial PASS4,349s y repetición para conservación durable de12 trazas/resultados; sólo necesaria para producir esa evidencia, no benchmark.

O4 continúa INDEPENDENT_HOLD: V-DAY-FLOOR, con activeRuleSet.DailyLoss obligatorio y risk.DayFloor ausente, lifecycle acepta silenciosamente el límite interno como única capacidad. Negativo independiente RED; Provider calcula siempre DayFloor cuando DailyLoss está instalado, por lo que no es ausencia legítima bajo este perfil activo. Requiere error técnico sin retiro/pérdida/pausa ficticia. Parent autoriza corrección O5 acotada y nuevo freeze, sin repetir pruebas de seams cuyo hash no cambie.

Evidencia durable propia: `c3-all-skip-first-difference.json` SHA256 `9ed258f6c39522688500992573fb262a5fd6944daf7222e56af48720c318d015`; `c3-temporary-daily-capacity-finding.json` SHA256 `4485b0a8c64e430efd2883c8422b675d16abf6e93062b5cf576bff8b210912fb`; `independent-o4-partial-gate.json` SHA256 `429012eaee49f63e4f81084ee94ef529faaef33818f70b7aa1eb9e6def66baa9`; `o4-independent-platform.log`, `o4-independent-e2e-durable.log` y `e2e-o4/`. Todos relativos al verifier workspace previo. Go propios drenados; no T1 ejecutada ni gate final admitido por este corte.

## O6: gate técnico independiente PASS exacto

Source `74034811df66beb23f9e8bc8431fbfc7db7f00f0`, árbol limpio leído después de pruebas bajo lease quieto; binario `dd9a528db292fdfd2646319f0115b1dfcbdd144106810278b6fd30c0b27ab214`. Recibo `work/tradesgerard-operability-20261013/verifier/independent-o6-gate.json`, SHA256 `65c90be21776fed3543277b66e0f6d08b39fb1a53c331dc67ea69c953e6cf14c`, status INDEPENDENT_PASS limitado a T0 técnico. No certifica aún T1 ni40 resultados económicos.

Pruebas propias exactas: lifecycle2,353s PASS incluye mandatoryDayFloor RED→GREEN, pausa temporal5,12, sucesor causal, caja80+cuenta viable, cap residual4casos y claims, y negativo dinámico cuenta preservada/contrato ajeno/released. SDK V2 PASS0,008s, marca causal primera ejecución fill GREEN con mismo archivo/asserts SHA `dd2477a48d226134057a2b7762ce5fc26bb67093fc98c263d410a8401e8d3261`. Comparación ALL/skip semántica y negativos de falsificación PASS0,215s. Intento de overlay monetario agregó función ya promovida y falló por duplicación de nombre; se conserva como error propio de harness, luego se ejecuta el archivo promovido byte idéntico, sin cambiar aserciones.

Compaction sizing conserva todos los callbacks monetarios/fills y tiene encoding explícito MM_SIZING_ANCHOR_DELTA_V1. Tee independiente real LONG/SHORT captura payload detailed antes del productor y reconstruye compacto, comparando todos los campos, incluidos R/T/q/SL/TP/costos/economía y keys removidas. PASS1,428s. Primer intento no implementaba Close del recorder y se preserva como error propio corregido. Decoder independiente rechaza encoding desconocido, delta huérfano y eliminación de key ausente; no supone cero para campos ausentes. Snapshot terminal/Close drenan mapa propio del productor.

Ten inputs F0 emparejados con C4 físicamente PASS_TEN, salvo source/bin/model/policies/metadata mínimos explícitos. Unión independiente coverage coincide227/233=97,4249%, blocks Go completos que intersectan líneas modificadas, incluyendo statements antiguos en blocks mixtos: denominador conservador, no se presenta como conteo AST exacto de nuevos statements. Perfil SDK C3 compatible porque bytes SDK no cambian C3→O6; perfil affected O6 posee PASS físico. Fallos históricos ALL/skip originales quedan separados, no maquillados como suite histórica PASS.

Smoke CLI O6 auditado streaming contra oráculo:23 cruces originales/K/ATR exactos,23 entradas,23 operaciones cerradas,17 fallback, cero oportunidades UNKNOWN, caja4760 y ledger/caja reconciliados. Reutilización E2E12 O4 se declara por hashes iguales de SDK y matching/mark causal, con guard nuevo de lifecycle exacto y tee monetario O6 repetidos; fixture R500 REPORT_RESIDUALS no se convierte en promesa de terminalidad ni ejecución broker.

Manager autorizó, dentro del mandato offline del Owner, el delta O7 de gzip streaming lossless para mantener límite físico16MiB ante ventana completa. O6 bin/source/inputs/gate permanecen preservados; source lease liberado después de drenar pruebas. T1 debe esperar gate I/O del nuevo freeze si utiliza gzip. No se descartan eventos de dinero ni se acepta por este PASS ninguna operación real.
