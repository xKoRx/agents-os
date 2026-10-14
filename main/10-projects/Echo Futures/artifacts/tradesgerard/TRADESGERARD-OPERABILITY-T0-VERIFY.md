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
updated: "2026-10-14"
---

# TRADESGERARD-OPERABILITY-T0-VERIFY

## Dictamen vigente

**O10/F0–F3: HOLD económico común por autoridad MM stale tras financiación/reselección. O11 está en corrección, todavía sin gate integrado independiente.** Resultados observados, incluido crédito simulado K03, se conservan AFFECTED y fuera del ranking vigente. Código y pruebas anteriores no se borran; ver el counterexample exacto y sus hashes al final. Verificador LOCAL: Sol6.1 solicitado, servido UNKNOWN.

### Antecedente inicial de recepción y mínimo (superado por cortes posteriores)

**HOLD inicial — candidatos87e33b0c y cb9cc0cd no habilitaban campañas.** Verificación independiente LOCAL, solicitado Sol6.1 y servido UNKNOWN. Source limpio87e33b0c333a1f2f4178dfefe06126d50691c7ad, binario físico verificado89b645fcc1ea7ca7a47ed75a5a88e05d4adbbd2d9a9d6e111d39d010b8afd89b. Los probes monetarios descubrieron un supuesto no acreditado en el mínimo económico: un tick extra llamado «nearest legal protection» no existe en validateSubmit del adapter. El implementador prepara corrección aislada; cobertura autor95,833% no reemplaza este finding ni admite T1.

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

## O7: gate de productor durable y habilitación técnica de T1

Source `4f7594511d381483a161fc59cf0ae7ba00e2cbd1`, árbol limpio, binario SHA256 `4ea8b12f3ea0a9ab2b47f5cbb173fb71b424d70cefde004ad82f9df6948ff9ac`. Recibo independiente `work/tradesgerard-operability-20261013/verifier/independent-o7-gate.json`, SHA256 `6a47a4fad3b5bc7cab8082f879ae180a6d596e98beb160ba41b4c5b4592d236b`, INDEPENDENT_PASS técnico exacto. Este gate permite ejecutar T1 diez inputs O7 congelados; sus resultados todavía no existen como evidencia auditada de ventana completa.

Delta O6→O7 limitado a I/O de platform_search.go, tests y documentación. Se transfieren money/SDK/native mark/lifecycle por identidad de bytes, preservando el recibo O6 y el E2E12 O4 explícitamente. Nueva ejecución independiente PASS4,138s compara una campaña directa/plaincompact y batch gzip en dos directorios: payload expandido byte idéntico, gzip determinista, digest sobre bytes durables después de Close, resume COMPLETE no ejecuta de nuevo. Segundo miembro gzip con digest recalculado se rechaza pese coincidencia de hash. Cancel/FAILED, bounds físicos/lógicos y legacy plain se verifican con los negativos de contrato afectados; no se borran fallos históricos ni se cambian aserciones de C4.

Receipt versiona event_encoding NDJSON_GZIP_V1 y event_file economic.ndjson.gz para policy nueva. Decoder independiente streaming exige un único miembro, CRC/footer válido, ausencia de trailing data, física<=16MiB y expansión<=256MiB; NDJSON y sizing anchor/delta se validan antes del análisis, sin cargar toda traza en RAM. Claves sizing removidas se reconstruyen, campos desconocidos/huérfanos no se convierten en cero. Suite propia de decoder verifica truncación, doble miembro, magic/path, límites y encoding/delta inválidos.

Smoke real CLI O7 COMPLETE,34.708 bytes gzip, digest físico `ec08cca7eed3c98e57662e9a6b43244481408dcf5f0467e1ae0ce87ffd4be54b`. Auditor independiente streaming:23 cruces originales con K/ATR exactos,23 entradas/23 cierres/17 fallback, caja4760, cero oportunidades UNKNOWN, balances por cuenta y caja conciliados. Los23 primeros callbacks MM_FILL contrastan marca actual−15×q y neto de liquidación desde gross/costos realizados/pendientes; no depende sólo del resumen del implementador.

Paridad diez inputs C4 PASS_TEN salvo políticas, metadata y source/bin versionados. Coverage recalculado independiente299/312=95,8333%, unión conservadora de blocks Go que intersectan el delta, sin reinterpretarlo como coverage histórico global o AST exacto de nuevos statements. Perfiles y logs físicos PASS corresponden a SDK byte compatible y affected O7 exacto. Se preservan bin/build/input de cada corte HOLD/PASS y los recibos incompletos no cuentan como pérdida de trading.

Pendiente fuera de este gate: resultados completos T1 y filtros F1/F2/F3; reglas runtime de broker/adapter real y slippage real no certificados. No hay órdenes reales, servicio iniciado ni aceptación final del proyecto.


### O7 — bloqueo efectivo por remanente diario: AFFECTED

La primera campaña F0-K01-r2300 produjo seis Q0 entre 23-oct 18:51 y19:46Z porque la cuenta3 conservaba turno ELIGIBLE con beneficio diario pendiente9.60 y rho1: R/T9.60/9.60 no cubría el mínimo ejecutable24.98 del descriptor C4. No era ruina EOD ni agotamiento de pérdida diaria. Las cuentas4/5 estaban ELIGIBLE desde14Z, flat y drenadas, sin operaciones/cargos intervenidos; sus últimas holguras permanentes verificadas eran105.12 y1355.02. Por tanto una cuenta bloqueada por el objetivo diario impidió usar alternativas existentes. No corresponde retirar cuentas ni aumentarR/T ni consumir de nuevo los cruces.

Evidencia física compacta: `work/tradesgerard-operability-20261013/verifier/turn-block-daily-remainder-T1-first.json`, SHA256 `93432c641f2eefb550fcb2d9e49b093df12245e2b51480e46588b91d87ab5bf0`. Incluye los seis cruces, autoridad monetaria y estados de cuentas4/5. El Manager adjudicó el hallazgo y ordenó drenar sólo campañas/harness propios: K01/K02 COMPLETE se conservan AFFECTED, K03 parcial diagnóstico. Se requiere repetir F0 después de corrección y nuevo gate exacto; el anterior INDEPENDENT_PASS técnico O7 no certifica esta selección económica.

RED independiente sobre O7: `objective_turn_adversarial_test.go`, overlay `objective-turn-overlay.json`, log `o7-objective-turn-RED.log`; exit1, FAIL0.854s: `selectedfx-acct-1 firstELIGIBLE`. Fixture monetaria explícita: ajuste de balance860.40 y autoridad diaria860.40, seguida de compra previa de sucesora, selección original y comprobación de turno. Es prueba del seam de selección fuera del ranking; la campaña proporciona la atribución mediante fills reales. El assert exige sucesora existente y conserva ledger/piso/caja/plaza. El lease quedó liberado tras drain para O8. Pendientes: GREEN mismo assert, rho4 conR38.40 viable, remanente de pase diminuto sin falsa recuperación diaria/retirada y sin bloquear alternativas.


### O8 — INDEPENDENT_PASS técnico exacto

Fuente `d66bb56bccd053305c1c7dac0dc51aa292745504`, árbol limpio; binario `echo-backtest-o8` SHA256 `a70ac11e481109b036f4a7d792c9594f8c8a73c97eb7c72cd35f2c0c025de8ce`, comprobados físicamente. Los diez inputs mantienen perfil/economía/corpus/horizonte C4 fuera de identidades y políticas explícitas: PASS_TEN. La extracción compartida RequestedObjectiveBudget conserva entry/selector en un mismo owner.

RED byte-identical selector pasa GREEN3.702s, con negativos independientes: diario9.60/rho1 cede turno a sucesora; diario9.60/rho4 conserva R38.40 viable; igualdad24.98 preservada; pase9.60 sin recuperación diaria falsa, retirada/plaza ni mutación económica y sin bloquear alternativas. SDK adversarial PASS0.015s. Pipeline físico mínimo12LONG/SHORT PASS4.356s: riesgo insuficiente sin fill, mínimos24.98/25.28 y500 con fill/protección y economía conservada. Seis negativos lifecycle/cap/claims/DayFloor PASS1.915s. Cobertura independiente de bloques Go de delta O7→O8:53/54=98.1481%, con denominador conservador explícito; el metadato de fuente inicialmente repetía O7, corregido y leído de vuelta antes del gate.

Intentos de harness conservados, no PASS: duplicación de tests promovidos; dos errores del consumidor viejo de sizing compacto (mapa delta era booleano); dos regex amplias incluyeron tests históricos ajenos y fueron canceladas únicamente por sus PIDs propios, exit143, con scratch propio drenado. Los asserts monetarios no se debilitaron; el consumidor ahora reconstruye anchors/deltas/removals antes de comprobarlos. El gate JSON `work/tradesgerard-operability-20261013/verifier/independent-o8-gate.json` identifica hashes/logs/inputs exactos. Este INDEPENDENT_PASS permite repetir y auditar T1; no certifica resultados todavía no ejecutados ni recupera O7 AFFECTED. Gzip/receipt/sizing y comparador semántico se reutilizan sólo donde el delta no altera sus propietarios.


Smoke CLI O8 productor→gzip sellado→auditor streaming independiente: PASS, artefacto `independent-o8-smoke-gate.json` SHA256 `90957558490a53b02e8b8ddfc357722a6b5cd052ae9c8935adef4476f3ef89e8`. Gate JSON previo se conserva sin reescribir.23 cruces base/K/ATR emparejados con oráculo C4 (error float ATR≤7.11e−15),23 operaciones,46fills,17fallback,0Q0,0UNKNOWN y0 snapshots económicos ausentes.23 primeras publicaciones MM_FILL acreditan mark actual:OpenMark−15/Net−24.98 porq1. Todas operaciones flat/terminal. Ledger cuentas−994.88/+295.34 reconciliado con balances49005.12/50295.34; caja5000−2×120=4760. ReceiptCOMPLETE/hash/CRC/trailing y inputs exactos verificados. Derivados `campaigns-O8-smoke.json` SHAc50820d184df0ff77645e2e4a1c30ae5c99a7e8b49fd3b2e0f8ae83ff4a2b858 y `o8-smoke-receipt-verified.json` SHA9771834e49686f4377b994d80dc76b37efdc6176bdab73b47f95363d9abcabbb. Alcance primer día NY, no campaña completa T1.


### F1 — gate independiente OFFLINE/OHLC

Fuente `f4643aefce49876ed40bb4fd1efefe1894cb1520` limpia, binario SHA256 `201edd9b22a08b60b9b06b6e7411449e0515eaba48b4be6571d6794c9977a4a6`: INDEPENDENT_PASS técnico sólo F1-TREND en corpus OHLC. `independent-f1-gate.json` SHA256 `0a876028c0caf8c13a65781d3738d6c24611a76b5921503ec1a19d82a32552ac`. Diez inputs emparejados exactamente O8 fuera de filtro/prefijo/build/identidades; propietarios monetarios byte-identical O8.25 H1 cerradas completas contrastadas directamente contra NQZ5 físico, mismo contrato/epoch0/asof original; prefijo sólo H1, no altera warmup1m. SDK TG entero PASS0.139s, negativos independientes seed→H1runtime desconocida→bloqueo, snapshot OHLC antiguo no elimina frontera, F0 independiente de H1, F2/F3/UNKNOWN rechazados y DST31Oct/3Nov conNY−04/−05 yUTC14/15 PASS0.007s. Cobertura conservadora300/312=96.1538%, baseline534ca1c7 corresponde cherry-pick O8 con dinero idéntico.

Smoke CLI freeze exacto COMPLETE auditado por lector streaming estricto y decoder sizing:23cruces base emparejados K/ATR/H1/SMA,14filtrados+9rechazos direccionales,14operaciones cerradas/primeras publicaciones MM_FILL con mark actual,0UNKNOWN/ausencias económicas. Caja4640 y ledger reconciliados; no representa T2 completo. Dataset descriptor y SHA físico NT se distinguen, ambos conservados en `f1-prefix-independent.json`. La comparación de755 witnesses durante campañas completas comprobará también ambos lados del DST; no se inventa evidencia de productor aún no ejecutado.

Límite funcional explícito: F1/F3 no pueden operar sobre fuente runtimeTRADE sin autoridad verificable de completitud H1. TradeCount yFeed.AsOf no acreditan cobertura; una semilla no autoriza SMA estancada después de una H1 no verificable. El filtro bloquea con `H1_LIVE_COMPLETENESS_UNVERIFIED`; esto es bloqueo funcional de esa ruta, no sólo una etiqueta de 'no validado'. Research OHLC con60refs sí soportado. No LIVE/órdenes reales iniciadas. F2/F3 todavía no implementadas en este freeze y su configuración se rechaza, sin aliases silenciosos.


### Dependencias runtime comunes y factory-mode RED

Inventario `runtime-operability-dependencies-and-mode-RED.json` SHA256 `77edf7a977774df38fee65dcdb2fd5f332dcffdaa4d254bb979087d1a30b04d5`. RuntimeCompose aliasa SnapshotViews; Market devuelve readModelMarket conMark/Ready, sinExecutableQuoteSource. Por tanto la ruta observada EconomicMinimumV2 de TODOS F0–F3 está funcionalmente bloqueada para entradasruntime actuales por falta de BBO/freshness ejecutable; F1/F3 además carecen de autoridad de completitud H1. No se limita la dependencia pendiente aH1.

En fuenteF1 `config.NewTGMM` ignorabaRunMode y podía aceptar offsetsOHLC modelados también enLIVE/EXACT_REPLAY/vacío/UNKNOWN, evitando la exigencia deBBOobservado. RED independiente sobre fuentequietaf464: cuatro subcasos fallan por aceptación indebida, exit1/0.014s; BACKTEST positivo y ausencia de interfaz observada realSnapshotViews comprobados. Manager adjudicó guardallowBACKTEST explícito para el próximo freezeF2, sin fabricarBBO ni ampliaradapter. El gate OFFLINE/OHLC F1 permanece válido; no certificó ni autorizó runtimeLIVE.

Otros requisitos precisos: metadataNQ/qmín/tick/pointvalue y protecciónSLTP tienen seams offlineLONG/SHORT/grid/fill→protección verificados, pero legalidad y aceptaciónadapter/broker reales pendientes. Ledger/Provider/EOD/DayFloor obligatorio/claims/reservas/selección causal fueron verificados offline; su publicaciónserving y autoridadaccountreal no probadas, sin afirmar ausencia donde no hayevidencia. Fee2.49/slip1/spread2/min24.98 pertenecen al modelo fijo concreto, no se trasladan como mínimo universal aNQreal. Costos/fills/repricing offline conservan entradarealizada y salidapendiente una vez; fees/slippage/structuralspread reales pendientes. Cierre lógico/liberación de plaza es DESIGN_SCENARIO, sin cancelación de suscripción/compra/retiroreal ejecutados.


### O9 — HOLD autoritativo por objetivo efectivo de evaluación

Fuente `cf855c7a3cffd276d5bf24458417a4dd7940863b`, binario `3ed52db8d418f7ff23b8074c932d75b59c1aeee8a1ad22093ca8edeaba4dee4f`: no gatePASS. Primer intento de consistencia se clasifica HARNESS_AUTHORITY_ERROR: el override BestDay enlastRev fue ignorado por platformBestDay que lee ledgerclosed/current; ese log NO demuestra bug.

Prueba posterior AUTORITATIVA de Ledger real: q1 BUY100→SELL160.25 net1200.02 y día siguiente BUY100→SELL190.25 net1800.02, fee2.49 porlado, precios tickgrid y dos folds reales. En tercer día balance53000.04/StagePnL3000.04/BestDayclosed1800.02/currentday0 fueron afirmados correctamente. Regla actual de perfil Consistency30% exige total suficiente según EvaluateConsistencyShared; ratio cercano60% no habilita pase. O9objectiveCapacity, sin considerar esa autoridad, devuelve COMPLETED/remaining−0.04/Rref500/Tref500. REDexit1 FAIL5.508s. Funded completed-yield promovido unchanged síGREEN; no sustituye este negativo.

Dictamen `independent-o9-HOLD.json` conserva identidad/hashes y límites. Manager/integrador recibieron prueba yleaseGo drenado. Corrección debe usar primitiva compartida Provider de objetivo efectivo/consistencia con max(closed,current) y mismoowner enMM/selector, incluyendo igualdadreal del comparador share>=threshold comoBREACHED; no copiar fórmula paralela ni declarar igualdad de6000.0666 aprobada. Fixtures nunca entran al ranking. O8/F1 mantienen resultadosAFFECTED porCOMPLETEDselection; crédito observado1651 conservado/reconciliado comoAFFECTED, sin afirmar resultado corregido.


### O10 — INDEPENDENT_PASS offline F0/F1

Fuente `76a1e69e5a0a67b94b920e2ffb983fd226eb127a` limpia y binario `3c66a1b091fde81a7804e38eb265f16078005c1fc211db46e62f690cb04426bf` verificados físicamente. Dictamen durable `verifier/independent-o10-gate.json`, SHA256 `2155593e9eca093126c579bb34ab67c3b3c904b0b91da55ed3664ada93414693`: INDEPENDENT_PASS para OFFLINE_OHLC_F0_F1; no certifica resultados de campañas aún no auditados. Los20inputs conservan hashes y paridad normativa O9 salvo campaign_id/build.

RED autoritativo de consistencia y funded completed-yield pasan unchanged5.223s. Factory RunMode BACKTEST único y ausenciaBBO runtime pasan0.012s. Calendario real de solicitud→aprobación→procesado→crédito, pendingpreservado, crédito neto1651 sólo en fecha y pausa diaria antes del cruce con owner rolloverdisabled pasan11.376s. Primer intento de pago usó perfil fixture2250 frenteMM2300: HARNESS_PROFILE_MISMATCH (neto1611 correcto para ese perfil), no defecto producto; fixture independiente recompone autoridad y afirma coincidencia previa gross2300/net1651. Coverage delta independiente conservadora48/50=96%, denominador bloques instrumentados intersectando líneas modificadas, sin archivos modificados sin perfil.

Ambos smokes COMPLETE durables verifican request/identity/result/eventdigests y gzip estricto sellado. Auditor streaming independiente: F0 23cruces/23operaciones/17fallbacks/caja4760; F1 23base/14filtrados/14operaciones/9rechazosdirección/caja4640. Cero UNKNOWN; K/ATR y SMA causal contra oráculo, marca actual al fill, ledger y caja reconciliados. Fixtures no entran al ranking. Manager e integrador recibieron gate y lease drenado; F0/F1 relanzadas con supervisión. Persisten bloqueos funcionales runtime comunes BBO y F1/F3 completitud H1; ninguna operación real autorizada.


### F2/F3 — gates independientes offline

F2 fuente `a9c4505914e897bd3587e3158a3ff9f205dd4948`, binario `4fe35ce7d3e868c34cd48fa808bf7a007fee412bf1bec288350a83d96d71c785`: `verifier/independent-f2-gate.json` SHA256 `8350ac5f9095de2b22d37bad996cb8c8d61ef837ae0a88a4bcd00d35a7fa7a59` INDEPENDENT_PASS. Diez inputs conservan economía/horizonteO10 salvo filtro/model_identity/CID/build. Oráculo variable17historias/136fronteras LONG/SHORT, extrema propia/futura excluida y zonas inclusivas PASS0.422s; seisregresiones dirigidas calendario/DST/gaps/autoridad/readiness PASS0.053s. Delta104/104; provenance exactsource/blobs/log precommit en `implementer/evidence/f2-profile-provenance.json`. Dos errores iniciales de SessionWindow/decimal fueron fixture, no producto.

F3 fuente `466e4f17b5b311adc74302417307452bc462d54a`, binario `281a76e9ab84111749fd248b8eb10f435ef90990e0e83ce0286f51499ac4ac60`: `verifier/independent-f3-gate.json` SHA256 `1922ab03e9ac2513ce345229cba7735292efe809a61b92fe1cd2c3f67e4008e3` INDEPENDENT_PASS. DiezprefijosH1 idénticosF1O10/dinero común. Tabla independiente144casos pendiente positiva/negativa/igual, zonasLONG/SHORT y faltaH1/ATR prueba conjunción exacta PASS0.323s; delta23/23.

Smokes físicos F2/F3:23base cada uno,0aceptados/operaciones/cuentas, caja5000. Testigos contrastanK/ATR/extremos60previos conoráculo; F3 ademásSMA/conjunción. Receipt/request/identity/result/eventdigests/gzip selladoCOMPLETE verificados. Evento CAMPAIGN_OPEN no es compra. Ceroactividad primerdía no representa conteo total ni candidata. Gates habilitan campañas offline con presupuesto/plazas globales; no certifican40resultados antes de auditoría. RuntimeF0–F3 mantiene bloqueo BBO; F1/F3H1 y F2/F3completitud1mTRADE sin autoridad suficiente en ruta observada.


### O10 — counterexample real posterior: HOLD de autoridad al reseleccionar cuenta financiada

Los gates técnicos anteriores se preservan como pruebas realizadas; quedan superados para continuidad económica por evidencia real de K04r2300. Dictamen `verifier/independent-o10-authority-HOLD.json` SHA256 `9d40ba525c03a51c51ab172ab4e571effbe1af8a800ea307cc9b8a99465aca36`. Prueba `o10-K04-stale-funded-authority-finding.json` SHA256 `5d6dda573a84bf7832cc55738f4c81853938974ca68a997264788d9908a15e88`: source76a1/bin3c66/resultadocfddab1 inmutables.

Cuenta2 recibió RESET_ADJUSTMENT−3005.92 a24Oct14:18:30.535714286Z y ACCOUNT_CONTEXT_TRANSITION a14:18:30.535714287Z. ECONOMICSrev27403 acredita /livesim/balance50000/stageNet0/day0. FUNDING_CONTROL_APPLIED14:21:30.535714285 confirma instalación. Al cruce16:06, selector la entrega ELIGIBLE/LIVESIM/flat/claims0, pero MM consume rev27398 anterior23Oct22Z, EVALUATION/balance53005.92/progreso3005.92 y rechazaTG_OBJECTIVE_ALREADY_MET. No es control futuro1ns ni race legítima: la autoridad nueva antecede casi1h47m al cruce. Ventanas físicas13eventos de cruce y7de funding conservadas.

Manager adjudicó HOLD común F0/F1/F2/F3 y drenaje de propios procesos; no pérdida de trading por fallos técnicos. Tabla cincofilas congelada `final-comparison-five-o10-AFFECTED.json`, SHA256 `547e28dc21893e5bbe085e205c34450df47e13e689af52c1c3560fff741d459f`. Crédito K03 observado2300bruto/1651neto acreditado20Nov, caja final3531/netcampaña−1469, ledger/caja/calendario conciliados se preservan como AFFECTED, no ranking válido. Recibo exacto `o10-K03-payment-selector-proof.json` SHA256 `15597f6546b4ac593ecb5ccc0b6fcb4e2cdeb6f5d63553017801ac8e1e6fee05`; sus seis antiguos cruces bloqueados ahora materializan cuentas16/17.

Probe independiente determinista preparado y promovido byteidéntico: `inactive_funding_authority_adversarial_test.go` SHA256 `be7a7e11002d5eb646d439f43d855793fd07c18717cd5a8b8d670456a84b18b6`. Cuatro días con fills ledger reales750.02/día, financiación inactiva mediante controles, reselección y MM materialization real deben consumir LIVESIM50000/stage0/revisiónúltima. No modifica caches/OwnerState para fabricar stale. Aún NO ejecutado: admisión Go bloqueada por reserva de disco y presupuesto agregado; no reclamar RED ni GREEN. Fuente correctora intacta mientras se resuelve recurso.


### O11 — reproducción autoritativa RED/GREEN aún sin gate integrado

Probe de financiación inactiva SHAbe7a7e11 promovido sin cambios: RED5.306s contra base466 y GREEN6.007s tras delta upstream. En RED, latestrev10230/contextLIVESIM/balance50000 frente MM EVALUATION/balance52250.06/rev8298; Views tiene balance/revactual pero phaseEVALUATION. Los dos seams son identidad instalada después de proyección y falta de entrega AccountEconomicsUpdate a Owner.DeliveredEconomics. GREEN conserva assertions completas y entrega normal, sin prioridadSDKhack ni cambiar políticas económicas. Recepción sparse/imports fallida fue HARNESS, no REDproducto.

Débito real adicional: tras timer de nuevo día efectivamente procesado, Delivered50000 afirmado antes de PAYOUT_DEBIT−100; fuente real commitrev2770/balance49900 vsOwnerrev2764/balance50000 fue RED7.977s. Corrección entrega snapshot completo después de riskprojection. Ensayo posterior con dinero ya correcto49900 comparó latest de markflat un minuto después (rev2770) con revision exacta del débito (rev2768), sólo versión/AsOf distintos: frontera de fixture en corrección, no obligación de publicar todosmarksflat ni debilitar asserts monetarios. Igualdad completa se verifica en la causa exacta; autoridad a ENTRY se audita aparte.

Auditor independiente reconstruido desde fills/fees una vez +cashflow/context/day: detecta sólo el contraejemplo1/649 enK04 y0mismatches en719K01,647K03,59F2K02. RawcompactECONOMICS es lowerbound de revisión porque omite eventosordinarios; primer prototipo se conserva HARNESS_INCOMPLETE_ECONOMICS, sin atribuir falsosbugs. Actualmoney/context/day/best efectivo se concilian; faltan floors absolutas publicadas porENTRY para comparación independiente, por lo que se solicitó anchor mínimo MATERIALIZED versionado/account/context/day/currentrevision/DayFloor/EODFloor y regla diaria requerida, sin nuevoSDK ni trazas por evento. Revisión equivalente por markflat no se confunde con autoridad posterior a débito/funding/día/floor. Próximo gate exige freeze/build/inputs y recheck exactos.


## O11 — dictamen independiente exacto (2026-10-14)

Fuente `5de33134311f3a23a306d12d1c8fabbf5222c502`, árbol limpio `1f5ade0301125728bbfcc368cdce858956a5f371`, binario SHA256 `734c923804fff719b1037953a387b715cc57e41f988775970b48038cea1b55a7`. Gate durable `verifier/independent-o11-gate.json`, SHA256 `ecb199bad5e32eefcfa87fa7cf73e72ed10451aedf0a106f2b8447d002dddd87`: **INDEPENDENT_PASS**, alcance OHLC offline F0–F3.

Recheck independiente de 29 nombres exactos: exit0,13.183s, fuente limpia antes/después. Incluye reproducción byte-identical be7a, débito real a frontera causal con autoridad completa, fault técnico de watermark inconsistente conservando débito único, negativos de handover/cuenta/revisión/recorder, objetivos completados, mínimos físicos y pisos. Cobertura nueva conservadora frente466e4f17:36/37=97.2973%, sin excluir bloque no cubierto. Cuarenta inputs concuerdan normativamente con sus anteriores; únicamente campaña/build cambian.

Los cuatro smokes reales quedaron COMPLETE y drenados; recibos, digest y gzip estricto comprobados por auditor streaming. F0:23 operaciones,caja4760; F1:14,caja4640; F2/F3:0,caja5000. Cruces y filtros coinciden con oráculos. Autoridad de entrada reconstruida sin mismatches;37/37 anclas verifican fase/día/pisos/headroom. Dos headers distintos por marca flat inicial mantienen equivalencia económica explícita; no se extiende esa equivalencia a cashflow/contexto/día/pisos. Referencias propias: `o11-inputs-independent.json`, `o11-independent-critical-receipt.json`, `o11-smoke-entry-anchor-independent.json`.

Limitación de recursos separada: el recheck no capturó cache absoluto previo; delta UNKNOWN, no se afirma cumplimiento medido del cap180MiB. Readback físico y admisión de nuevas campañas se realizan aparte; ningún Go futuro está autorizado por este gate. Todas las políticas V2 siguen funcionalmente bloqueadas en runtime actual por autoridad BBO ejecutable ausente; H1/continuidad de barras añade dependencias de filtros. No se emitieron órdenes reales. El gate habilita ejecución offline técnica, no acepta resultados económicos todavía no corridos ni rehabilita campañas AFFECTED.
