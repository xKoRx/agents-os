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

**HOLD — candidato87e33b0c no habilita campañas.** Verificación independiente LOCAL, solicitado Sol6.1 y servido UNKNOWN. Source limpio87e33b0c333a1f2f4178dfefe06126d50691c7ad, binario físico verificado89b645fcc1ea7ca7a47ed75a5a88e05d4adbbd2d9a9d6e111d39d010b8afd89b. Los probes monetarios descubrieron un supuesto no acreditado en el mínimo económico: un tick extra llamado «nearest legal protection» no existe en validateSubmit del adapter. El implementador prepara corrección aislada; cobertura autor95,833% no reemplaza este finding ni admite T1.

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
