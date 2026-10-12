---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[TRADESGERARD-CONTROL]]"
  - "[[TRADESGERARD-CONTRACT]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-12"
updated: "2026-10-12"
---

# TRADESGERARD-EVIDENCE-A

## Propósito

Recibo de evidencia y handoff de la etapa A. El estado de iniciativa pertenece exclusivamente a [[TRADESGERARD-CONTROL]]. Entrega actual: d752b3e1, con dictamen independiente PASS del contrato material de §10. Este documento conserva identidades, alcance probado y límites; no acepta el gate del Owner. Los resultados del primer candidato no certifican por sí solos las correcciones posteriores.

## Contenido

### Identidades y procedencia

Actualización posterior a la entrega, por petición explícita del Owner: push exitoso a `git@github.com:xKoRx/echo.git`, rama `codex/tradesgerard-platform-a`; `git ls-remote` corroboró `d752b3e124386330e6f8e4b270958cc2db892734`. El source auditado está disponible remotamente para revisión. No se modificó el freeze ni se hizo merge/release. Evidencia externa/corpus/binarios permanecen locales; no se afirma que el push los incluya.

Repo: `xKoRx/echo`. Baseline inspeccionado: `873f5f1c7df25086271af1de1896095f1cade2a9`, rama histórica `codex/btx-perf-last`. Desarrollo: rama `codex/tradesgerard-platform-a`, checkout relativo al workspace Aranea `work/tradesgerard-platform-a-20261012/echo`. SDD: `specs/FEAT-TRADESGERARD-PLATFORM-A/`.

Primer candidato auditado: commit `06ab6b12d2e4701d21ee8506238a481c5c47af5e`, árbol limpio corroborado antes y después de la auditoría. Binario relativo a Aranea `work/tradesgerard-platform-a-20261012/evidence/integrator/bin/echo-backtest`, SHA256 `7afb11bc32b5d5e3a0330589aa9f0b75310eb2c11193d64204fb5a7ee56951ba`. Go1.27.1 linux/amd64, VCS revision idéntica, modified=false. Manager corroboró HEAD/status/SHA256/`go version -m`; no ejecutó campañas.

El binario histórico tiene SHA256 `49957b660e0a248cd03fc9f321461b8f8ae190856f1bd7740950807c475b64af` y source embebido `48647d1ff9860bd4e1fff47e5fca7c9be273fb74`, distinto del baseline 873. Manual baseline leído: blob `b66dacec9a0f6e0bc99ac13bde3a8e53cdb036e3`. Ni la build histórica ni el blob anterior citado por el mandato se atribuyen al source encontrado.

Modelo solicitado de cada TOP: `gpt-6.1-sol`; servido UNKNOWN. No se usó CLOUD Pro ni se lanzó GLM. En las referencias siguientes, `evidence/` se resuelve como `work/tradesgerard-platform-a-20261012/evidence/` desde Aranea. Informes y logs pesados permanecen fuera del vault.

### Primer shot de implementación

Recibos cerrados: `evidence/integrator/{CANDIDATE-REPORT.md,commands-executed.md,changed-files.txt,coverage-delta-audit.json,coverage_delta.py,resource-receipt.json,closeout-metadata.json}`. El delta reutiliza provider, operación/MM, accounting, ejecución causal y replay; añade registro preservado de cuentas, relojes de todas las cuentas, campaña/caja, reglas por fase, composición pública alternativa, salida compacta y lote.

Pruebas focalizadas del autor incluyeron registro/relojes pausados, ReplaceAccount, perfil/ladder/DST/feriados, piso Live intraday, reglas selladas por fase, nueva Strategy/MM pública con add/BE y proyección económica, paridad compacta/detallada, lote/resume y fallos. `lifecycle-final-dll-test.log` registra 23 sesiones sintéticas: dos evaluaciones pasan con 3090,24 netos y seis días; llegan a LiveSim; retiro 2250 acredita 1611; tres cuentas preservadas y una ejecutando, funded 50325,2 sin falso DAILY_LOSS/TRAILING. Son pruebas de motor, no rentabilidad.

Defectos corregidos antes del freeze: fase desactualizada en liveConfig tras cambiar binding; baseline diario/piso al iniciar funded; retiro computado como pérdida diaria; min-days nil en compra nueva; churn de cancelación del exit del fixture y promedio residual FIFO. Los logs fallidos y primeras causas se conservan. Manager señaló dos riesgos adicionales que el autor corrigió: readback fallido debe degradar COMPLETE a FAILED con causa durable; temporales JSON exclusivos y cleanup sólo del archivo propio.

Única modificación aprobada de test heredado: TCR en el SDD permite sustituir `INTRADAY_TRAILING` por `UNKNOWN_TRAILING` en `TestEvaluateEconomicRisk_StaticLockNeverRatchets`, manteniendo aserciones. El primer literal pasó a ser una variante soportada; no podía seguir representando una variante desconocida. Provider completo y proof MM pasaron tras aplicarlo.

Baseline/actual con idéntica selección causal heredada y `-p1`: PASS 0,080 s / 0,087 s. SDK focalizado del baseline también PASS. Suites amplias backtester/cmd agotaron 180 s: **NOT_PASS**. La primera medición multipaquete con paralelismo por defecto no es comparación válida del carril serial.

Recibo de cobertura del primer candidato: **1081/1425 = 75,85965%**, por debajo de 95%, actualmente bajo revisión metodológica. El método pretendía incluir todos los bloques nuevos y bloques mixtos completos que intersectan líneas añadidas, frente al baseline histórico. Incluía hits instrumentados de suites con timeout, sin convertirlas en testPASS. Durante la corrección se detectó que la unión mezcló coordenadas de proof.go de distintas versiones: perfil antiguo 137 statements/89 bloques frente a final 154/97, con unión de 210 statements. El recibo original se conserva, pero no acredita una medida exacta. Se exige recalcular desde baseline873→fuente actual y perfiles compatibles por contenido, con mapa de discrepancias y denominador completo; nunca excluir paths para lograr 95%.

### Auditoría independiente del primer candidato

TOP verifier_a cerró su shot y liberó el carril sin modificar el producto ni dejar procesos propios. Recibos: `evidence/verifier/{CANDIDATE-AUDIT.md,COMMANDS.md,AUDIT-METADATA.json}`; matriz de 15 grupos en `preparation/ADVERSARIAL-MATRIX.md`. Casos propios bajo `physical/adversarial_test.go`, compilados mediante overlay que sólo añade un test nuevo. SHA256 del test source: `bade4120b0632604dde117e709bbcb233cf02672b5088933bdf46768d36a1b34`; binario `physical/verifier.test`: `9ff1a0203e031d19430fac0356dd5e0e2de68d7b4b953d4d625462ec5bae5f99`. Ese binario enlaza bibliotecas de 06ab y debe recompilarse para verificar un nuevo freeze. La auditoría no midió cobertura Go nueva.

| Caso físico propio | Resultado y alcance |
|---|---|
| Pase/consistencia | 3×870+390 = 3000, best-day 870, pase en cuatro días; 16 fills / ocho ciclos en la misma cuenta. 900×3+300 no pasa por igualdad de 30%. Pérdida intermedia −200 preservada y recuperación hasta 3000. |
| Pausa | −1000 y luego +870 conservan cuenta, saldo 49870, stage −130 y caja 4880, sin breach. Riesgo 25 insuficiente para un contrato: rechazo sin fill. |
| Cobros | Flujo público propio 2250→1611; pendientes al horizonte no son caja. Cap hipotético 2250: pending a 12 sesiones, crédito/TRANSITION_PENDING a 19, sin cobro posterior. Cap 5000 no demostrado en ese freeze por F02. |
| Parciales y fills tardíos | Entrada parcial 1+1 en la misma orden, add rechazado, cancel pendiente y fill tardío. Cancel 14:03Z, salida 1 a 14:04, add tardío 1 a 14:10, cierre residual 1 a 14:11; flat/COMPLETE. |
| Precios económicos | Antes del add: SL125,75/TP163,25; después: SL138,25/TP157; BE posterior observado. TP es precio económico con salida a mercado al dispararse, no orden LIMIT resting. |
| Paridad | Resultado tipado completo de campaña detallada/compacta idéntico; digest `7fe719fd042d2fc55b639086d528455a1438c412ad63378f9e7ecba02cc0120a`. |
| Disco y lote | SIGTERM a 2 s: rc2, receipt FAILED/context canceled, failurecount1, resultado preservado, cero directorios scratch. Deadline API y escritor ENOSPC fallan; temp/sentinel ajeno preservado. Resume exacto skipped1; trace alterado rechazado; campaña cambiada reejecutada; fallidos visibles. |
| Regresión | BASIC detallado/reproduce IDENTICAL, 94.798 registros. SDK focalizado provider/operation/accounting/proof fixture PASS. |

**F01 confirmado:** renovación hipotética 4800/día, compra 120 y renovación 4800 dejan caja 80; única cuenta RENEWAL_UNPAID, sin pagos pendientes. Devuelve COMPLETE/conciliado pero HORIZON_CENSORED y RuinAt cero, sin cuenta utilizable. `TestVerifierPublicRenewalUnpaidTrueRuin`; artefactos `physical/renewal-public-ruin-result.json`, `ruin-writer.log`. La existencia de una cuenta irrecuperable no debe impedir ruina ni compra admisible; se debe evaluar recuperabilidad y acciones legales, sin reset ni capital externo.

**F02 confirmado:** campaña propia de 35 sesiones falla ANALYTICS_SOURCE_FAILED en 2026-10-05T14:01Z después de dos créditos y cuatro cuentas: intervalo 14:00–14:01Z no cabe en región 1m. Mismo source/calendario/fábricas sin campaña, target elevado para evitar pase, completa 35 sesiones/12460 registros/140 fills. Evidencia `own-lifecycle-result.json`, `isolated-adversarial.log`, `long-without-campaign-result.json`, `long-cap-late.log`. Tests `TestVerifierOwnLifecyclePayoutAndFiniteCap` y `TestVerifierSameLongSourceWithoutCampaign`.

**F03 confirmado en alcance acotado:** MM propio sin SL logra entrada admitida/1 fill; gap deja equity 48020 y DAILY_LOSS; DRAIN_NOT_CONVERGENT impide flatten y deja posición +1/cuenta ELIGIBLE. MM del autor con SL sobre el mismo mercado evita el fallo. Evidencia `rulefail-result.json`, `lifecycle-adversarial.log`, `rulefail-author-mm-result.json`; tests `TestVerifierPublicFailureAndWriterDrain` y `TestVerifierRuleFailUsingAuthorMMIndependentMarket`. La API no había impuesto SL como precondición; debe cerrar exposición admitida sin inventar fills ni aceptar expansión/reversión.

Filas todavía incompletas: compra/fondos/cupos extremos y reinversión más allá de 41 compras; aislamiento mutable entre MM y matriz física de no solapamiento; relojes de cuentas inactivas/DST; cuatro targets, funded por encima de 870 y cap completo 5000; baja caja con cuenta utilizable/pago pendiente; causalidad cierre/intrabar representada; pico temporal continuo y fallos posteriores de write/readback; invalidación por build/perfil/ventana; regresiones relevantes restantes; cobertura ≥95%.

### Candidato corregido y recheck independiente

Freeze actual: `d752b3e124386330e6f8e4b270958cc2db892734`, árbol limpio. Binario `evidence/corrector/bin/echo-backtest`, SHA256 `8abe7379483e4845f3e6f16167ac3a3d4db630d6b42b600542f4ca739fcc98ff`; Go1.27.1 linux/amd64, VCS d752b3e1, modified=false. Manager corroboró estos datos y el diff de tests heredados: sólo el literal autorizado por TCR, sin cambiar asserts. Corrector terminó su shot y liberó procesos y carril; recheck_a recibió RELEASE_VERIFY y recompiló su propio arnés contra el nuevo freeze.

Recibos del autor: `evidence/corrector/{CANDIDATE-REPORT.md,MATRIX-A.md,FIX-ADJUDICATION.md,freeze-metadata.json,public-cli-validation.json,final-profile-manifest.json,coverage-delta-current.json,denominator-history-map.json,resource-receipt.json,old-temporary-attribution.json,commands-executed.md,final-files-manifest.json,artifact-manifest.json,closeout-metadata.json,lane-release.json}`. Son pruebas del autor; el dictamen independiente final se registra en la sección siguiente.

| Corrección o prueba | Evidencia del autor sobre d752b3e1 |
|---|---|
| F01 | Recuperabilidad según costos efectivos y acciones legales; cuenta impaga irrecuperable no bloquea compra admisible. Ruina pública y compra con 120 PASS, historia y cupos preservados. |
| F02 | AdvanceUntil completa todas las fases del mismo instante antes de publicar frontera. Prueba con/sin campaña de 35 sesiones completa. Fixture de 60 sesiones llega a tres cuentas LiveSim con gross5000 y TRANSITION_PENDING: nueve cuentas, doce pagos, caja17825; campaña global censurada por otras cuentas pendientes. |
| F03 | Admisión y revalidación permiten reducción demostrada contando claims ejecutables pendientes; Exit por sí solo no autoriza expansión, reversión ni sobrecierre. Long/short parcial/total y negativos PASS. Gap original conserva fallo 48020/stage−1980 y queda flat. |
| Reinversión y aislamiento | 71 cuentas preservadas, 70 falladas, tres créditos, caja41, sin solapamiento y cada cuenta flat. El fixture recupera precio antes del fill causal de cierre: FIFO reconstruye saldo50000/stage0 con latch DAILY_LOSS conservado; el assert anterior48020 era un oráculo incorrecto y su fallo permanece registrado. |
| Cuatro targets | 2250/2300/2500/3000 acreditan respectivamente1611/1651/1811/2211. Funded opera1305 diarios sin heredar870. Estos casos usan cap de un pago; cap5000 tiene prueba separada. |
| MM alternativo | Parcial real1+1 de una orden en instantes distintos, rechazo sin add, fill tardío tras cancel y cierre residual. SL125,75/TP163,25→SL138,25/TP157 tras add y BE observado. TP económico dispara salida Market; no se exige resting LIMIT. |
| Fallos físicos | RLIMIT_FSIZE8KiB/EFBIG, RLIMIT_NOFILE/EMFILE y tamper inotify durante publicación conservan primera causa FAILED y cleanup; límites restaurados. No equivalen por sí solos a pruebas económicas E2E. |

coverage_prepare y coverage_finish aportaron propuestas externas sólo leídas/formateadas; el corrector las integró y ejecutó. Sus estimaciones previas de hits no cuentan como cobertura. El denominador final baseline873→d752 incluye todos los archivos Go ejecutables nuevos y los bloques mixtos completos que intersectan líneas nuevas, sin exclusiones.

Cobertura final del autor: **1349/1420 = 95,000%**, exactamente el umbral ceil(0,95×1420)=1349. Veinte perfiles PASS,108 fuentes instrumentadas con SHA y coordenadas compatibles. La procedencia de mediciones previas al commit limpio se conserva y se mapea por contenido al freeze; no se reescribe como ejecución sobre commit limpio. Perfiles FAIL/timeout no aportan hits al gate. El mapa frente al histórico1425 explica proof210→154 (−56), driver14→23 (+9), campaign371→394 (+23), reducción provider0→16 (+16), reservation0→3 (+3), total1420; no se congeló un denominador contaminado.

Recheck_a reprodujo independientemente 1349/1420 desde SHA/coordenadas de los 20 perfiles, sin paths faltantes ni conflictos y con 108 fuentes instrumentadas. El toolkit Python integrado también fue ejecutado sobre su contenido actual: 53/53 checks PASS y 119/121 sentencias = 98,347%, mediante trace/AST; métrica separada de Go. No se atribuye el recibo histórico al contenido cambiado: esta cifra tiene una nueva ejecución propia, manifests de comandos y summary en `evidence/recheck/`. La selección propia del auditor no se presenta como una nueva unión física del 95%; el dictamen de cobertura es una auditoría independiente de contenido, denominador, coordenadas y perfiles PASS del autor.

Regresiones focalizadas completas SDK provider/operation/accounting/domain/config/proof PASS. Selección causal/full-driver/campaign/replay/cashflow/siblingless PASS20,110s; grupo público extendido PASS139,995s; propietarios/propuestas PASS88,925s; independientes promovidos PASS193,975s; CLI final PASS7,600s. El agregado plataforma agotó420s, sin assert previo, tres segundos después de comenzar el siguiente caso público de caja: **NOT_PASS**, log/stack conservados y perfil excluido. Grupos separados cubren sus casos; no se afirma que el agregado pasó. Los timeouts históricos180s conservan su condición.

CLI física exacta en `evidence/corrector/physical/cli-real/`: source/profile/runspec/basic-request/plan JSON. Campaña real riesgo100/TP50 COMPLETE/conciliada/HORIZON_CENSORED, caja4880, cuatro fills/una operación, saldo49890,04; gross−100/costos9,96/neto−109,96/unrealized0. Resume exacto expected1/pending0/completed0/skipped1/failed0. BASIC y reproduce **IDENTICAL,94798 registros**, runID `bt-0ff7a6d2c4a5044de133aceac5a929eaecafe8186253965d9ad8bff0406734f5`. SIGTERM tras2s: CLIrc2, receiptFAILED/context canceled/attempt1/failurecount1, resultado preservado y cero attemptdirs. El wrapper valida ese rc esperado y puede devolver0; no se confunden ambos códigos. Comandos exactos/config hashes están en commands-executed.md y public-cli-validation.json. Estos resultados no demuestran rentabilidad.

Recursos del corrector: muestreo cada0,25s, pico TMPDIR observado41121025bytes, RSS377248KiB, pico durable de replay63730033bytes; todos los attemptdirs propios durante publicación7838077bytes (incluye BASIC, no sólo plataforma). TMPDIR y attemptdirs propios finales cero; logs75211bytes; libres finales10487418880bytes. No se afirma máximo instantáneo entre muestras. Primer sampler falló por carrera al desaparecer un temporal Go: descartado y repetido. lane-release registra cero procesos propios y source limpio. Temporales históricos no tienen atribución suficiente por prefijo/fecha/usuario: ninguno eliminado, sin borrar caches compartidas ni afirmar cleanup histórico total.

### Dictamen independiente final sobre d752b3e1

TOP recheck_a terminó su shot y liberó el carril: **PASS del contrato material de §10**, sin defecto nuevo ni gap material identificado. Manager leyó/adjudicó el informe y corroboró de nuevo HEAD limpio y hash del CLI/catálogo. Recibos en `evidence/recheck/`: `CANDIDATE-RECHECK.md`, `COMMANDS.json`, `COMMANDS.md`, `RECIPES.md`, `VERIFY-START.json`, `VERIFY-END.json`, `FINAL-RESOURCES.json`, `PROCESS-CLEANUP.json`, `closeout-metadata.json` y `FINAL-FILES-MANIFEST.json`. VERIFY-END compara 1.359 archivos Go antes/después sin cambios. Modelo solicitado gpt-6.1-sol, servido UNKNOWN. Verificación tras RELEASE_VERIFY: 2.221,28 s; preparación anterior no medida de forma fiable.

| Contrato material | Prueba independiente final |
|---|---|
| Caja, compra, turnos y terminalidad | Fronteras 119,99/120, ruina real por renovación impaga, caja baja con cuenta utilizable/pago pendiente, campaña pública de 120 sesiones con más de 41 compras y ledger racional independiente. Exposición y cantidades ejecutables físicas sin solapamiento, señales distintas y fuente monótona. |
| Pausa, pase y riesgo | Pase 3×870+390, igualdad30% negativa y pérdida intermedia −200; pausa −1000 seguida de +870 sin reset. Fallo por piso antes de −1000 demostrado por readback adjudicado descrito debajo. |
| Calendarios y funded | Campaña de 60 sesiones observa MM aislado, EOD16CT/reset17CT inactivos y cambio DST de noviembre, piso preservado y funded >870. DST de primavera/calendario hábil tiene prueba owner separada. |
| Cuatro cobros y cap | Cuatro campañas propias de 80 sesiones: 2250/2300/2500/3000→primer crédito1611/1651/1811/2211, split exacto y fee139 no repetido; cap5000 y TRANSITION_PENDING, sin crédito fuera del horizonte. |
| Composición y causalidad | Strategy/MM propios, parciales físicos1+1, add rechazado, cancel pendiente/fill tardío, SL/TP económicos y BE. Breach sin SL long/short drena, etiquetas Exit inseguras rechazadas; reservas SDK cuentan hasta finality. Regresiones diferencian cierre/intrabar y extremos pasados; OHLC es modelo declarado. |
| Disco, integridad y lote | Paridad tipada compacta/detallada; tamper inotify posterior a escritura degrada a FAILED; EFBIG/EMFILE/ENOSPC/deadline y sentinels preservados. Mutar build/config/perfil/datahash/ventana exige nuevo intento; sólo identidad íntegra completa omite ejecución. |
| Regresiones y CLI reales | SDK focalizado completo, legacy causal/campaign/full-driver replay/reconstrucción, CLI y almacenamiento PASS. Runtime público factories/bounded/substitution PASS, sin servicios; runtime no cambió desde baseline. Smoke real cuatro fills/neto−109,96, exact resume skipped1; BASIC/reproduce IDENTICAL94.798. |

Cancelación propia tras 2 s: CLI real rc2, wrapper rc0 porque valida ese fallo esperado; attempt1 FAILED/context canceled. Reinicio rc0 en 39,42 s: COMPLETE/attempt2, conserva first_cause=context canceled y failure_count1. `real-restart.log` no emitió stdout; recursos, código de salida y lectura del receipt demuestran el resultado. No se confundió silencio con proceso activo ni se elevó timeout.

Adjudicaciones conservadas: `floor-v4-adjudicated.json` liga resultado/hashes a la cuenta efectivamente seleccionada `/account/2`, día `ad-20261001`: 50360→49860, PnL diario−500, piso50000, TRAILING_DRAWDOWN/FAILED_RULE e historia sin reset. El assert original suponía account0 y queda rc1; no se declara suite PASS. Días anteriores de otra cuenta se excluyeron al filtrar evidencia contemporánea. Un probe adicional que combinaba entrada parcial y salida parcial tras breach queda **NOT_DEMONSTRATED por fixture**; las capacidades requeridas tienen evidencia complementaria pública de parciales/finality, breach long/short y contratos SDK de reducción/reservas. No se afirma que esa combinación pasó ni se oculta un defecto de producto establecido. Otros errores de harness —provenance sin reglas recompiladas, cronología imposible y fase consultada en Economics.StageID— quedan registrados. La fase para MM en MATERIALIZED se obtiene de `operation.MMInput.RuleSet.Phase`.

Recibo final independiente: durable propio113.355.152 bytes, agregado de iniciativa261.178.223 bytes, libres10.214.326.272 bytes, scratch0, logs100.820 bytes y procesos propios0. Picos muestreados a0,25s: scratch133.103.985 bytes, durable113.846.479 bytes, RSS441.664 KiB; reserva mínima10.123.841.536 bytes. Sin violaciones de límites. El presupuesto agregado384 MiB fue prospectivo antes del último bloque CLI/replay; por corrida/lote y auditor propio se mantuvo256 MiB. Sin borrar binarios, corpus, caches ni historia/temporales ajenos. Son medidas del corte de recibo, no máximo instantáneo ni afirmación de limpieza histórica total.

Recetas: `evidence/recheck/RECIPES.md` ofrece equivalentes de argv físicos para prepare/batch/resume, BASIC/reproduce y toolkit; `COMMANDS.json` conserva argv realmente ejecutados. Resolver ARANEA_ROOT/VAULT_ROOT desde el workspace. El manager normalizó sólo esas variables documentales tras el cierre del worker: hash anterior18f670ee19959f92eb4d73ed3ac69c27438f3e5351008f907dfb00982842e187, actuald530dbff0570a0b2a83edea54faa6c5546b39e79ff301f604324e5d93ba794de; entrada del manifest actualizada. Ningún producto/test/argv histórico cambió. Las versiones ejecutadas del arnés se conservan en HARNESS-v2/v3, snapshots/v4_new_test.go y binarios; la corrección posterior no ejecutada del oráculo no sustituye esa procedencia.

### Catálogo y datos reales

Catálogo único `catalog.json`: SHA256 `e367741ad47975e4a8b1aff3172bc10e659ed52cb9993f8db81507ceb588abd4`. Design-2 conserva 53 IDs; raw 23040, incompatibles 7680, alias 192 y únicas compatibles 15168. Auditoría/reparación: 59 checks PASS; cobertura del generador 119/121 = 98,3471%, distinta de cobertura Go/branches. Toolkit integrado ejecuta 53 checks canónicos, excluyendo seis comparaciones históricas, con `--catalog`/`--source` explícitos y sin catálogo editable duplicado.

Corpus legible relativo a Aranea: `work/btx-perf-last-20261010/integrator/package/corpus`. all13 sigue NOT_READY por gaps/prefijos; no se repite para fingir cobertura. Datos originales del otro workspace inaccesibles; permisos intactos.

Ventana NQZ5 validada: trading 2025-10-28T14:00Z→15:00Z, lectura requerida desde 2025-10-13T17:52Z. Catálogo COMPLETE: 15008/15008 minutos abiertos requeridos, 60/60 trading, unknown0. Smoke del autor: qty30 rechazada por cap, cero fills, caja4880/HORIZON_CENSORED; prueba pipeline/rechazo. **Smoke independiente:** riesgo100/TP50, cuatro fills/una operación, COMPLETE/conciliado, saldo49890,04; gross−100/costos9,96/neto−109,96. Evidencia operativa, ninguna inferencia de rentabilidad. Artefactos en `evidence/verifier/physical/real-risk100/`; configs del autor en `evidence/integrator/smoke/{runspec,profile,source,plan,basic-request,validation}.json`.

Hashes: NQZ5.nt `700579b3b3c78e58ccceb39bd79e8d11aa3efab3e8457d92bee1833ef2686406`; NQH6.nt `31546615336370083b02ad7878cbd86a362d7bf3967b9a984478735b7598d643`; NQU6.nt `d4cbbdcdbe7bcb2932f1fbfb1418e8f12a52ef3305df29d5619a19cef6112be3`.

### Recursos y handoff

Límites: reserva libre ≥8 GiB, scratch propio ≤2 GiB, durable por lote/corrida ≤256 MiB, archivo agregado de auditoría ≤384 MiB, logs ≤16 MiB, GOMAXPROCS=4 y un carril de build/prueba/campaña. Recibos históricos de 06ab: autor con 11.251.548.160 bytes libres, 44.975.061 bytes durables y 99.855 bytes de logs; auditor con aproximadamente 11,02 GB libres, 38.825.944 bytes durables y RSS observado máximo 324.156 KiB incluyendo compilación. Esas corridas no tuvieron muestreo continuo del pico temporal y no se atribuyen al nuevo freeze. Temporales históricos de timeout no totalmente atribuidos; no se borraron a ciegas ni se afirma cleanup total. Los recursos de d752 se detallan en su sección de corrección y en el recibo independiente final.

Manual único: `v3/backtester/README.md`, leído en el freeze. Superficies públicas: RunPlatformCampaign, ComposePlatformSpec, CompositionFactories, CLI platform-prepare/platform-batch. Reejecutar campaña detallada exige PlatformCampaignRequest completo y fábricas; un RunSpec desnudo de reproduce no reconstruye controles de admisión/cobro. Recetas finales existentes, leídas y verificadas en `evidence/recheck/RECIPES.md`; no se inventan flags. La sección del manual fue escrita como candidato de desarrollo antes del recheck; el dictamen técnico posterior pertenece al control/evidencia, sin modificar el source congelado.

`spec.ExecutionModel`, market_data_mode y OHLC_CAUSAL_PATH_V2 con prioridades/slippage/fees/offsets están sellados por `fidelity.execution_model_digest`. `ModelIdentity` es etiqueta libre no vacía; no sustituye al modelo económico. Distinguir modelo causal, composition_id y agente solicitado/servido.

[[TRADESGERARD-GLM-MASTER]] encarga implementar todas las familias y variantes de B, luego baseline y producto cartesiano compatible completo con continuidad, validación y ranking. B no absorbe capacidades estructurales de A pendientes. Readiness técnico no certificaría términos comerciales UNKNOWN, LIVE ni rentabilidad. Código permanece en desarrollo local, sin push/merge/release afirmados.

## Fuentes

- [[TRADESGERARD-MANDATE-SNAPSHOT]], §§10–12; [[TRADESGERARD-CONTRACT]]; [[TRADESGERARD-PROP-PROFILE]].
- Recibos físicos del integrador, auditor, corrector y propuestas de cobertura bajo el workspace Aranea.
- `xKoRx/echo:specs/FEAT-TRADESGERARD-PLATFORM-A/`; matriz independiente y manual público.
