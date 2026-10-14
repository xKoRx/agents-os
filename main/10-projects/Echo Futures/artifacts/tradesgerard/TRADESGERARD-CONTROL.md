---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-12"
updated: "2026-10-13"
---

# TRADESGERARD-CONTROL

## Propósito

Fuente de estado de TradesGerard. Mandato vigente 2026-10-13: **O10_INDEPENDENT_PASS_OFFLINE / T1_T2_RUNNING**. O10 corrigió el remanente de evaluación según la autoridad de consistencia y pasó verificación independiente exacta. F0×10 y F1×10 relanzadas, cuatro campañas globales; F2/F3 congelados esperan gates propios. No se lanzaron campañas O9; O8/F1 anteriores drenadas y conservadas AFFECTED. Los cuatro filtros y la ampliación acotada siguen autorizados, sin aprobación intermedia pendiente del Owner. El primer crédito histórico observado se conserva con caja neta negativa, fuera del ranking por el defecto de selección; todavía no se infiere resultado de O10. La etapa A y READY_FOR_GLM de abajo son antecedentes históricos. Aceptación final del Owner separada; manager y proyecto permanecen abiertos.

## Contenido

### Relanzamiento vigente O10

Source `76a1e69e5a0a67b94b920e2ffb983fd226eb127a`, binario `3c66a1b091fde81a7804e38eb265f16078005c1fc211db46e62f690cb04426bf`, gate independiente `verifier/independent-o10-gate.json` SHA256 `2155593e9eca093126c579bb34ab67c3b3c904b0b91da55ed3664ada93414693`. Cobertura48/50=96%, RED real-ledger anterior pasa sin cambiar test; pago/pending/daily/modo PASS,20inputs íntegros y smokes conciliados. Sólo OFFLINE_OHLC; runtime continúa funcionalmente bloqueado según [[TRADESGERARD-OPERABILITY-T0]].

Lanzamiento real: T1 F0 sesión85629, primeros K01/K02-r2300 PID/PGID3018544/3018576; T2 F1 sesión57628, primeros K01/K02-r2300 PID/PGID3018587/3018601. Manager comprobó procesos y comandos exactos. Concurrencia4 global, afinidadCPU0–5/GOMAXPROCS4. Admisión física≈9,676GB libres/RAM63,86GB/load1,54; owned≈975MB y forecast40≈1,210GB≤presupuesto1,5GiB, reserva8GiB. Progresos `implementer/evidence/T1-o10-progress.json` y `T2-o10-progress.json`; nada afectado se reutiliza. Informes [[TRADESGERARD-OPERABILITY-T1]] y [[TRADESGERARD-OPERABILITY-T2]]. [[TRADESGERARD-OPERABILITY-T3]] y [[TRADESGERARD-OPERABILITY-T4]] registran freezes y gates pendientes de SR/conjunción.

### Mandato vigente — operabilidad, campañas y filtros KISS, 2026-10-13

Dispatch LOCAL real: `/root/operability_integrator` único implementador/integrador y `/root/operability_verifier` independiente. Modelo solicitado en ambos `gpt-6.1-sol`; servido UNKNOWN. C4 preservado: source `88ed70d1ff9910bb157f1c14c0fed1d2b8e7ec49`, árbol limpio y binario `c8849bb6e5523e8625ead8282f0d97f98d8b02e14d72838e3c35de207c6bcd57` comprobados físicamente por el manager. Evidencia anterior sigue en `ARANEA_ROOT/work/tradesgerard-entry-repair-20261013`; delta nuevo en `ARANEA_ROOT/work/tradesgerard-operability-20261013`.

Alcance autorizado sin aprobaciones intermedias repetidas: T0 reconstrucción K05 y operabilidad; T1 F0×10; T2 F1-TREND×10; T3 F2-SR×10; T4 F3-TREND-SR×10. Política de mínimo económico y retiro de cuentas común, SIG-B inmutable, SMA24 H1 cerrada y extremos de60velas1m previas exactamente como el mandato. Después, ampliar los dos pares activos mejor posicionados con ambos retiros si el corpus válido lo permite; intervalo nuevo intacto sólo si existe. No optimizar parámetros vecinos ni reactivar catálogo histórico. Las restricciones históricas de ATR rígido y conservación de cuentas quedan sustituidas prospectivamente, sin relabelar todos los rechazos C4 como bugs.

Estado actual: recepción física C4 comprobada; racha12 reconstruida en [[TRADESGERARD-OPERABILITY-K05-STREAK]], sincronización master `5ef845ce923d37e7025c506f54756f659663eba2`. Sin pérdidas previas: once ganancias en cuenta1=2495,22, faltan504,78 al pase; pausa diaria875,08 y compra causal siguiente cruce; duodécima en cuenta2=260,04. Agregado2755,26 no equivale a progreso de una cuenta. Caja final4520=5000−240compras−240renovaciones; ledger global−279,46 separado. O7 y ahora O8/F1 se conservan AFFECTED por casos distintos de selección. Todavía no hay cuarenta resultados válidos de la política completa: cuatro O8 COMPLETE históricos, cuatro cancelaciones técnicas entre T1/T2 y doce no lanzadas. [[TRADESGERARD-OPERABILITY-T1]] y [[TRADESGERARD-OPERABILITY-T2]] conservan las conciliaciones e invalidaciones; O9 en corrección. El manager coordina/revisa/documenta y no escribe producto, tests ni scripts. Sólo offline: no LIVE, órdenes/compras/resets reales, deploy, servicios, ACL, merge o release productivo. No cierre/feedback del manager ni aceptación propia del gate final.

### Autoridad y límites

HOLD vigente: cuenta11 K03 funded/progreso2305,36≥2300 consumió seis cruces12nov19:18–20:38Z mientras esperaba `CompliantAt=13nov15:01:06.114649681Z`; cuatro alternativas EVAL16–19 estaban elegibles, flat y drenadas. `COMPLETED` no cedía turno. Recibo independiente `verifier/o8-K03-completed-objective-selection-HOLD.json`, SHA256 `8adeca2cfa8dd5207cf6256677773aba222cdb7f01b5e54130d98f5743e4efd1`. Parada00:22:07Z comprobada: manager envió SIGINT a supervisores propios2963227/2979615, cuyos finally drenaron cuatro hijos; todos ausentes. Corrección O9 incluye espera/selección causal y guard de modalidad, sin crédito anticipado ni pérdida artificial/plaza falsa. F0/F1 se repetirán con build común después del gate.

Primer crédito simulado observado, **AFFECTED para ranking**: O8 F0–K03–r2300/cuenta11 LIVESIM, bruto2300, split80%−50−139=neto1651, CREDITED20nov2025 15Z. Caja al crédito4011 y final3531 tras26compras/3120USD; cambio neto−1469. Cinco pases y un cobro conciliados, sin convertirlos en rentabilidad general ni resultado definitivo de la política corregida. [[TRADESGERARD-OPERABILITY-T1]] conserva recibo/hashes y calendario solicitud→aprobación→procesamiento→crédito. El dinero observado no se borra ni se fabrica; la causa de selección exige repetir la trayectoria.

### Cortes históricos O8/F1, sustituidos por el HOLD anterior

Autoridad vigente O8: source `d66bb56bccd053305c1c7dac0dc51aa292745504`, binario `a70ac11e481109b036f4a7d792c9594f8c8a73c97eb7c72cd35f2c0c025de8ce`, INDEPENDENT_PASS técnico y smoke CLI auditado por recibos separados; cobertura53/54=98,1481% del deltaO7→O8. Diario insuficiente pausa; fase insuficiente bloquea objetivo sin retiro/reset/plaza, y ambas liberan selección de alternativas. Solicitud R/T comparte primitiva TGMM con entry. Relanzamiento F0×10 real23:26Z, concurrencia2 medida; progreso `implementer/evidence/T1-o8-progress.json`, sin sobrescribir snapshotO7. Primera campaña K01–r2300 terminó23:47:54Z y está conciliada:755base,719operaciones/31días,550fallback,0Q0/UNKNOWN,15compras/13retiradas/0fallosoficiales/0pases/0cobros; caja5000→3200, costos1800, ledger−19075,18 separado. La pausa por objetivo temporal libera correctamente cuenta4 en los cruces antes bloqueados por cuenta3. K02 también conciliada:618operaciones,215fallback,29compras/26retiradas/4evaluaciones únicas aprobadas, caja1520; sus cuatro LIVESIM operaron pero quedaron inoperables por EOD antes de2300, la mejor llegó a1616,06 realizado/faltante683,94. Sesenta rechazos por cupo comercial5 comprobados con ninguna cuenta elegible en esos instantes. Ninguna de las dos configura una candidata útil en esta muestra; cero cobros, costos de compra1800/3480. Pruebas, fees condicionales y hashes en [[TRADESGERARD-OPERABILITY-T1]]. Las otras configuraciones continúan; no hay aceptación final del Owner.

Hallazgo histórico O7, corregido en O8: cuenta3 rechazó seis cruces con remanente diario/R9,60 inferior al mínimo24,98, mientras cuentas4 y5 estaban elegibles, flat y drenadas tras reset. La corrección verificada pausa/clasifica el bloqueo y libera turno causal, distinguiendo remanente diario de pase, sin retirar la cuenta ni aumentar R/T. K01 O7 conserva caja observada3200 y conciliación, pero queda AFFECTED y fuera del ranking. Parada O7 confirmada23:11Z, dos COMPLETE preservados, K03 cancelada con resultado parcial durable, siete no lanzadas y scratch0. O8 ya está congelada y ejecutando la repetición completa descrita arriba; no hay un freeze pendiente de O7.

F1 pasó gate técnico independiente OFFLINE_OHLC: source `f4643aefce49876ed40bb4fd1efefe1894cb1520`, binario `201edd9b22a08b60b9b06b6e7411449e0515eaba48b4be6571d6794c9977a4a6`, gate SHA256 `0a876028c0caf8c13a65781d3738d6c24611a76b5921503ec1a19d82a32552ac`; cobertura300/312=96,1538%. Misma economía O8 y diez inputs con delta sólo filtro/prefijo/build/identidad; seed25H1 y DST contrastados independientemente. Smoke exacto23base/14aceptados/9rechazados,14operaciones, UNKNOWN0 y caja4640 conciliada; no ranking. T2 lanzada23:58Z, jobs2, K01/K02–r2300 PID/PGID2979660/2979671; progreso `implementer/evidence/T2-f1-progress.json`,0/10completas. Cuatro campañas globales con T1jobs2, admisión medida y presupuesto preservado; F2 en desarrollo aislado. [[TRADESGERARD-OPERABILITY-T2]] contiene identidades y límites.

Dependencias runtime: la nueva política de mínimo económico en F0–F3 está funcionalmente bloqueada porque `SnapshotViews.Market()` no implementa `ExecutableQuoteSource`; los offsets de OHLC son autoridad del simulador y no sustituyen BBO observado. RED independiente de factory mostró admisión indebida de esos offsets en LIVE/EXACT_REPLAY/vacío/UNKNOWN. Integrador corregirá el guard a BACKTEST explícito en el próximo corte F2; no modifica campañas offline en curso ni inventa quote/adapter. Evidencia y límites en [[TRADESGERARD-OPERABILITY-T0-VERIFY]], recibo SHA256 `77edf7a977774df38fee65dcdb2fd5f332dcffdaa4d254bb979087d1a30b04d5`.

F1/F3 tienen además esta dependencia: la ruta runtime `ApplyTrade` no aporta autoridad suficiente para acreditar completitud de la H1 tras inicio o cambio de época. El conteo de trades y una seed de25 cierres no la sustituyen. El módulo falla cerrado con `H1_LIVE_COMPLETENESS_UNVERIFIED`; no se declara runtime operativo por compartir la matemática. El backtest OHLC usa barras horarias con cobertura de minutos fuente verificada. Negativo independiente del freeze F1 aprobado: seed válida seguida de nueva H1 sin autoridad invalida disponibilidad y ninguna snapshot anterior la restaura. Estas limitaciones no habilitan servicios ni operaciones reales, ni bloquean la investigación offline.

Lanzamiento O7 anterior, ahora AFFECTED: source `4f7594511d381483a161fc59cf0ae7ba00e2cbd1`, binario `4ea8b12f3ea0a9ab2b47f5cbb173fb71b424d70cefde004ad82f9df6948ff9ac`, gate histórico INDEPENDENT_PASS T0/I/O y cobertura299/312=95,8333%. K01 y K02 terminaron COMPLETEexit0 según harness; K03 comenzó antes de la parada y manager envióSIGINT sólo a su grupo propio2949893. El supervisor drenó y bloqueó la cola; receiptFAILED/context canceled y salida2 verificados, supervisor/child ausentes. Snapshot `implementer/evidence/T1-o7-progress-frozen.json` SHA256 `bb86933efb6036d15321e8ae13d661bcd2c524ba8c0c5ade659b0b335901524b`. [[TRADESGERARD-OPERABILITY-T1]] conserva el resultado K01 y sus causas:755cruces base idénticos,36ocupados,713entradas cerradas y6rechazos por remanente diario9,60 menor al mínimo ejecutable24,98 de los descriptores; UNKNOWN0. No retiros acreditados nuevos certificados. H1 continúa aislado del source/build de T1.

Antecedente técnico O6: **INDEPENDENT_PASS** source `74034811df66beb23f9e8bc8431fbfc7db7f00f0`, binario `dd9a528db292fdfd2646319f0115b1dfcbdd144106810278b6fd30c0b27ab214`. Gate físico, hashes de sus cinco logs y árbol limpio comprobados por manager; [[TRADESGERARD-OPERABILITY-T0-VERIFY]] conserva el dictamen y límites. Cubrió mínimo económico, retiro EOD, pausa por capacidad diaria, error ante piso obligatorio ausente, marca contable causal previa al fill, demanda/claims/cap, reconstrucción compacta y paridad de los diez inputs. Cobertura227/233=97,4249% de bloques afectados, no global. Smoke independiente23cruces/23entradas/23cierres/17fallbacks, caja4760, UNKNOWN0 y conciliación ledger/caja; diagnóstico, no ranking. El delta I/O posterior O7 ya pasó y habilitó el lanzamiento descrito arriba. En el mandato vigente sólo se ensayan solicitudes brutas2300/3000; otros targets y catálogos de las secciones siguientes son antecedentes.

### Antecedentes de autoridad e inputs

[[TRADESGERARD-MANDATE-SNAPSHOT]] autoriza desarrollo offline por TOPs, verificación independiente y correcciones. El manager coordinó, adjudicó evidencia y documentó; no escribió ni integró código, scripts de producto ni tests. Sin merge productivo, deploy, servicios, egress de trading, compras/resets reales ni reconstrucción de cuentas personales. BTG-PLAN, BTX-PERF y D1–D6 conservan sus gates históricos.

Inputs preservados: caja inicial USD 5.000, compra individual USD 120 a demanda, reinversión sólo de efectivo acreditado, una cuenta y una operación agregada ejecutando, turno persistente. Evaluación con target ordinario USD 870 netos y pausa −USD 1.000 sin reset; fallo oficial previo prevalece. NY flat/cancelado al cierre. Funded no hereda 870 ni consistencia de evaluación. Retiros brutos 2.250/2.300/2.500/3.000. Sin límite vitalicio de 41 cuentas ni horizonte fijo de dos semanas.

### Entrega aceptada técnicamente

| Entrega | Estado | Evidencia |
|---|---|---|
| Contrato, propietarios y frontera A/B | COMPLETE | [[TRADESGERARD-CONTRACT]]; SDD en el repo de desarrollo. |
| Perfil GAU50 versionado | COMPLETE_WITH_EXPLICIT_SCENARIOS | [[TRADESGERARD-PROP-PROFILE]] distingue hechos oficiales, supuestos y UNKNOWN; no certificación comercial. |
| Catálogo finito | VERIFIED_FOR_B_IMPLEMENTATION | `catalog.json` único, design-2, 53 IDs / 44 habilitados / 8 retirados / NY-OPEN inactivo. 23.040 tuplas, 7.680 incompatibles, 192 alias y 15.168 únicas compatibles; baseline 3. Toolkit integrado: 53 checks PASS y Python 119/121 = 98,347%. Ninguna variante B ejecutada. |
| Motor y composición | IMPLEMENTED_AND_VERIFIED | Cuentas preservadas, caja/cobros, relojes, turnos, reglas por fase, Strategy/MM alternativo por API, protecciones económicas y drenaje físico. |
| Salida y lote | IMPLEMENTED_AND_VERIFIED | Paridad compacta/detallada, límites, integridad y fallos durables; reanudación sólo de completos idénticos. |
| Verificación independiente §10 | PASS_MATERIAL_CONTRACT | `evidence/recheck/CANDIDATE-RECHECK.md`; pruebas propias y regresiones sobre el freeze exacto. F01/F02/F03 resueltos; ningún gap material ni defecto nuevo identificado. |
| Cobertura Go nueva ≥95% | VERIFIED | 1349/1420 = 95,000%, 20 perfiles PASS compatibles por SHA/coordenadas, 108 fuentes instrumentadas; baseline separado, sin paths excluidos. Auditor reprodujo el conteo; no se afirma que su propia selección produzca por sí sola ese 95%. |
| Manual, recetas y handoff | COMPLETE | Manual existente `v3/backtester/README.md`; `evidence/recheck/RECIPES.md`, comandos ejecutados y [[TRADESGERARD-EVIDENCE-A]]. |
| Prompt maestro GLM | PREPARED_NOT_LAUNCHED | [[TRADESGERARD-GLM-MASTER]]; lanzamiento manual del Owner. |

### Identidad exacta

Repo `xKoRx/echo`; rama `codex/tradesgerard-platform-a`; checkout relativo a ARANEA_ROOT: `work/tradesgerard-platform-a-20261012/echo`. Baseline `873f5f1c7df25086271af1de1896095f1cade2a9`. Source entregado: **`d752b3e124386330e6f8e4b270958cc2db892734`**.

Binario relativo a ARANEA_ROOT: `work/tradesgerard-platform-a-20261012/evidence/corrector/bin/echo-backtest`. SHA256 **`8abe7379483e4845f3e6f16167ac3a3d4db630d6b42b600542f4ca739fcc98ff`**; Go1.27.1 linux/amd64, VCS idéntico, modified=false. Manager corroboró HEAD limpio y hash antes/después; auditor comparó 1.359 archivos Go sin cambios durante el carril. Código local de desarrollo, sin push/merge/release productivo afirmados.

SDD `specs/FEAT-TRADESGERARD-PLATFORM-A/`. Único cambio de test heredado aprobado por TCR: literal INTRADAY_TRAILING→UNKNOWN_TRAILING en el caso de variante desconocida; asserts intactos. Tests nuevos y correcciones están identificados en los commits y manifests.

### Alcance de la evidencia y adjudicaciones

Publicación remota solicitada explícitamente por el Owner después de la entrega: rama `codex/tradesgerard-platform-a` pusheada a `git@github.com:xKoRx/echo.git` y verificada por `git ls-remote` en `d752b3e124386330e6f8e4b270958cc2db892734`. Acceso para revisión: https://github.com/xKoRx/echo/tree/codex/tradesgerard-platform-a . Push de la rama de desarrollo, sin merge ni release. Los recibos externos a Git conservan sus referencias locales.

El recheck independiente demostró compra/caja/reinversión >41, turnos sin solapamiento, pausas, calendarios y cuentas inactivas/DST, pase exacto/negativo30%, cuatro targets/cap5000/fees/latencias, terminalidad, composición/aislamiento, causalidad, disco/lote y regresiones. Smoke real NQZ5: cuatro fills, neto −109,96; BASIC/replay IDENTICAL 94.798 registros. Fixtures son prueba del motor, no rentabilidad.

El caso de piso antes de −1000 se acepta por readback físico ligado a source/binario: cuenta efectivamente seleccionada 50360→49860, pérdida diaria −500, piso50000 y fallo TRAILING_DRAWDOWN. El test que suponía account0 conserva rc1; no se declara suite PASS. Un probe adicional de parcial combinado con breach quedó NOT_DEMONSTRATED por su fixture; las capacidades materiales se demostraron mediante parciales/finality públicos, breach long/short público y contratos SDK de reducción/reservas. No se traslada un gap de A a B ni se oculta ese límite.

Los agregados históricos con timeout siguen NOT_PASS. La cobertura final sólo usa perfiles PASS compatibles; el denominador histórico1425 mezclaba versiones y fue reemplazado por recálculo auditado baseline→freeze, preservando recibo y mapa. [[TRADESGERARD-EVIDENCE-A]] conserva primeras causas, alcance y referencias físicas.

### Recursos y cierre del carril

Un escritor y un carril de build/pruebas/campaña, GOMAXPROCS=4 y Go -p1. Reserva ≥8 GiB, scratch ≤2 GiB, durable por lote/corrida ≤256 MiB, logs ≤16 MiB. Antes del último bloque CLI/replay se fijó prospectivamente presupuesto agregado de auditoría de 384 MiB; no cambió el límite del lote ni se borró historia.

Recibo final independiente: propios 113.355.152 bytes, archivo agregado 261.178.223 bytes, libres 10.214.326.272 bytes, scratch final0, logs100.820 bytes y procesos propios0. Picos observados cada0,25s: scratch133.103.985 bytes, durable113.846.479 bytes, RSS441.664 KiB; reserva mínima10.123.841.536 bytes. Son máximos muestreados. Binarios, corpus, caches y temporales históricos sin atribución permanecieron intactos; no se afirma cleanup histórico total.

Todos los TOPs terminaron sus shots; solicitado `gpt-6.1-sol`, servido UNKNOWN. Corrector y auditor liberaron explícitamente el carril. No se consumió CLOUD Pro ni se asumió disponibilidad de GLM en este harness. Agents-OS se mantuvo en master con autosync observado, sin atribuir sus commits/push al manager.

### Siguiente acción y alcance B

El Owner puede lanzar manualmente [[TRADESGERARD-GLM-MASTER]] con esta identidad y las recetas verificadas. B debe IMPLEMENTAR la Strategy TradesGerard, indicadores y todas las políticas/variantes vigentes; verificar baseline3, enumerar y ejecutar todas las combinaciones compatibles con continuidad, validar y rankear caja/cobros. No recibe reconstrucción estructural pendiente de scheduler/accounting/lifecycle/recorder.

all13 sigue NOT_READY por gaps/prefijos; nuevas ventanas requieren validación prospectiva. Los UNKNOWN comerciales siguen explícitos. READY_FOR_GLM es readiness técnico, no aceptación del Owner, autorización LIVE ni prueba de rentabilidad. No se ejecuta feedback ni cierre de sesión del manager sin petición explícita.

### Estado B — KISS-1 gobierna (GLM LOCAL, 2026-10-12)

El Owner lanzó el mandato KISS-1 (GLM-5.3-Flash, superficie LOCAL) y reemplaza la selección experimental del prompt maestro anterior: **el catálogo `catalog.json` design-2 (15.168 combinaciones) queda HISTÓRICO** — no es orden vigente de implementación; se conserva por Git/referencia con sus 53 IDs fuente y ninguna variante B del catálogo se ejecuta. La investigación vigente es la selección finita de KISS-1: 5 perfiles económicos {K01 250/250, K02 500/500, K03 500/1000÷3, K04 500/250, K05 1000/250} × {retiro2300, retiro3000} = **10 configuraciones por ventana**; iteración1 con salida fija (sin adds, sin Gerard, sin progresiones, sin BE/extensión), señal SIG-B sobre cierres 1m (estocástico lookback20, K lenta SMA3, cruce 20/80 consumido una vez), geometría TP 1×ATR / SL ρ×ATR, horario de diseño A (entradas 10:00–15:50 NY, liquidación desde 15:50, flat antes 15:55), remanente T=min(Tref, pendiente del objetivo) con R proporcional. I1 terminada el 2026-10-13: T0 COMPLETE, T1 10/10 y T1-L 4/4 conciliadas sobre NQZ5 validado (0 huecos) con **0 cobros y ninguna evaluación aprobada** — ninguna configuración recomienda campaña con este frozen; K03 menos mala (+690,14 de cuenta, no caja). Defectos B corregidos con commits `67ec0099`+`10d406b3` (binario `f00efd66…`), regresión A≡B verificada. Dictamen, higiene y pendientes I2: [[TRADESGERARD-B-RESULTADO]]. Plan, tandas y estado: [[TRADESGERARD-B-PLAN]].

### Reparación de entradas — 2026-10-13

**Estado vigente: CORRECTED_AND_VERIFIED — funcionamiento offline.** Fuente `88ed70d1ff9910bb157f1c14c0fed1d2b8e7ec49`, binario `c8849bb6e5523e8625ead8282f0d97f98d8b02e14d72838e3c35de207c6bcd57`. Las diez configuraciones K01–K05 ×2300/3000 están COMPLETE exit0 y verificadas independientemente:755 cruces por configuración, particiones, autoridad monetaria, ledger/caja y cierres sin findings. Por cada retiro, operaciones con fills0/18/7/1/6→19/24/14/34/25 (+84 agregadas). Ambos retiros se ejecutaron por separado y sólo después se comprobó su igualdad. Hay fixes reales de ciclo/rearme, finality, ATR/readiness, compra/selección y economía diaria; restricciones restantes de geometría/headroom explicadas, sin aumentar riesgo ni ATR. B preservado y observado5/5 equivalente a sus diez resultados históricos. C3 supersedido:cinco COMPLETE de referencia,un FAILED cancelado,cuatro no ejecutados. [[TRADESGERARD-ENTRY-REPAIR]] contiene causas, recibos, métricas y propuesta de selección separada NO_APLICADA. Aceptación Owner y LIVE no certificadas. Los párrafos siguientes son cortes históricos del proceso, no el estado vigente.

IN_PROGRESS bajo el mandato GOD LOCAL: [[TRADESGERARD-ENTRY-REPAIR]] es el único informe de reparación KISS-1. B físico preservado `10d406b3cddbd9c738dbc64b5db38c16ff7527b9`, binario `f00efd668eee8b121f7efb65b1b92923620e47beaac650a99491b425027486e8`. C2 congelado `63fb24996d422f3dfee28e706ad1528eb948bff8`, binario `8eff860eca8db7d2aaf84e40903b0de4e03f367aad798a79d2c371bf1ecf8f50`, supera gate independiente funcional/oráculo/cobertura sobre identidades exactas:42969 barras/755 oportunidades NY, sin divergencias de indicadores, regresiones permanentes y rearme/finality/compra acreditados. C1 recuperó K01 corto0→3 y largo0→85, pero su compra indebida al vencer pausa lo deja REFERENCE_ONLY; C2 corrige esa frontera. Diez planes finales sellados; comparación10/10 y casos largos pertinentes pendientes antes de CORRECTED_AND_VERIFIED. T1/T1-L conservan COMPLETE histórico; ENTRY-REPAIR-C01 marca afectada la explicación de frecuencia/denominadores de I1. Design-2 permanece histórico; no se activan I2 ni nuevos parámetros ni LIVE.

V-F02 confirmado después del gate acotado C2: al reanudar sesión se conserva indebidamente el turno de una cuenta posterior. Reproducción pública independiente de dos días RED y subcaso payout2300 B PASS/C2 FAIL, sin modificar asserts ni horizonte. C2 supersedido y drenado. C3 `26f3459cba47fd05f5ef9aed3d205c3c5bbad81a`, binario `92e27ef71d22bc9897af7f3c26d1fbe980f5f591b749224258747fd40c2584c9`, corrige turno y pasa los cuatro pagos/lifecycle/regresiones, gate independiente exacto y CLI singleton; manager comprobó identidad. Comparación final 3/10 COMPLETE y verificadas: K01 r2300 de0 a19 operaciones, K02 de18 a53 y K03 de7 a14, con755 cruces por configuración conciliados. K01 queda luego limitado por margen EOD15,28 inferior al mínimo19,98 del sizing vigente desde referencia previa al fill; no es un mínimo universal del exchange. Una posible política de selección por insuficiencia persistente bajo ese modelo se propone separadamente y no se aplica. K04/K05 y B observado K02 continúan; B observado K01 conserva equivalencia completa histórica y acredita719 intentos recuperados. Comparación completa pendiente. Detalle y recibos en [[TRADESGERARD-ENTRY-REPAIR]].

## Fuentes

- [[TRADESGERARD-MANDATE-SNAPSHOT]], §§10–12; [[TRADESGERARD-CONTRACT]]; [[TRADESGERARD-EVIDENCE-A]].
- `evidence/recheck/{CANDIDATE-RECHECK.md,VERIFY-END.json,FINAL-RESOURCES.json,PROCESS-CLEANUP.json,closeout-metadata.json,RECIPES.md}` relativos al workspace de la iniciativa.
- [[Echo Futures]] y `xKoRx/echo:v3/backtester/README.md`.
