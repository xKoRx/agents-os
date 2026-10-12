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

Recibo de evidencia y handoff de la etapa A. El estado de iniciativa pertenece exclusivamente a [[TRADESGERARD-CONTROL]]. Este documento conserva identidades, alcance probado y límites; no acepta el gate del Owner. Los resultados del primer candidato no certifican las correcciones posteriores.

## Contenido

### Identidades y procedencia

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

### Corrección en curso y propuesta de cobertura

TOP coverage_prepare entregó seis archivos promovibles en `evidence/coverage-proposal/`, más `PROPOSAL.md`, `denominator-map.json` y `files-manifest.json`. Sólo lectura/análisis y gofmt; no compiló ni ejecutó. Propuestas cubren caja/crédito/cap/renovación/calendario, validadores/proyección, readback/temporales y CLI. Estimación de 65–105 hits adicionales no acredita cobertura ni garantiza 95%; había al menos 273 hits faltantes antes del nuevo delta de producto.

TOP corrector_a recibió el único carril tras cerrar la auditoría. Reprodujo F01/F02/F03 contra el binario independiente congelado (`evidence/corrector/reproduce-frozen.log`), integró los seis archivos y tests promovibles conservando asserts, y modificó sólo la ruta de outputs de fixture a t.TempDir fuera de evidencia explícita.

Reportes de avance, todavía no auditados sobre nuevo freeze: F01 pública pasa después de clasificar recuperación con costos de renovación/setup vigentes. F02 quedó reproducido antes del fix por SESSION_END no Fired con Deadline igual al frontier publicado; completar todas las fases de ese instante permite terminar las 35 sesiones. Ese resultado conserva censura: gross retirado 4500/4500/2250, dos credenciales esperando cupo; no alcanza todavía el cap 5000. Se amplía únicamente el fixture sintético de cap, conservando el resultado anterior y ventanas reales. F03, matriz restante, cobertura y nuevo commit/build todavía requieren recibo final.

Avance posterior: F03 público PASS tras permitir reservas que reducen exposición real incluso después del breach, contando reservas pendientes hasta finality; no basta etiqueta Exit. Positivos long/short parcial/total y negativos sobrecierre/reversión/expansión/binding desconocido PASS según corrector. Cuenta fallida preservada 48020/stage −1980, sin posición residual. SDK focalizado completo PASS; primer muestreo propio pico temporal 16,65 MiB/remanente cero. Selección instrumentada de 256,3 s completó casos públicos, incluido cap5000 con fixture60; un test nuevo de compra unpaid usó una hora nocturna y requiere repetir tras corregir sólo ese input. Nuevas identidades, cobertura final y verificación independiente aún pendientes. top_recheck_a preparó matriz externa y casos propios, sin ejecutar mientras fuente cambia.

### Catálogo y datos reales

Catálogo único `catalog.json`: SHA256 `e367741ad47975e4a8b1aff3172bc10e659ed52cb9993f8db81507ceb588abd4`. Design-2 conserva 53 IDs; raw 23040, incompatibles 7680, alias 192 y únicas compatibles 15168. Auditoría/reparación: 59 checks PASS; cobertura del generador 119/121 = 98,3471%, distinta de cobertura Go/branches. Toolkit integrado ejecuta 53 checks canónicos, excluyendo seis comparaciones históricas, con `--catalog`/`--source` explícitos y sin catálogo editable duplicado.

Corpus legible relativo a Aranea: `work/btx-perf-last-20261010/integrator/package/corpus`. all13 sigue NOT_READY por gaps/prefijos; no se repite para fingir cobertura. Datos originales del otro workspace inaccesibles; permisos intactos.

Ventana NQZ5 validada: trading 2025-10-28T14:00Z→15:00Z, lectura requerida desde 2025-10-13T17:52Z. Catálogo COMPLETE: 15008/15008 minutos abiertos requeridos, 60/60 trading, unknown0. Smoke del autor: qty30 rechazada por cap, cero fills, caja4880/HORIZON_CENSORED; prueba pipeline/rechazo. **Smoke independiente:** riesgo100/TP50, cuatro fills/una operación, COMPLETE/conciliado, saldo49890,04; gross−100/costos9,96/neto−109,96. Evidencia operativa, ninguna inferencia de rentabilidad. Artefactos en `evidence/verifier/physical/real-risk100/`; configs del autor en `evidence/integrator/smoke/{runspec,profile,source,plan,basic-request,validation}.json`.

Hashes: NQZ5.nt `700579b3b3c78e58ccceb39bd79e8d11aa3efab3e8457d92bee1833ef2686406`; NQH6.nt `31546615336370083b02ad7878cbd86a362d7bf3967b9a984478735b7598d643`; NQU6.nt `d4cbbdcdbe7bcb2932f1fbfb1418e8f12a52ef3305df29d5619a19cef6112be3`.

### Recursos y handoff

Límites: reserva libre ≥8 GiB, scratch propio ≤2 GiB, durable ≤256 MiB, logs ≤16 MiB, GOMAXPROCS=4 y un carril de build/prueba/campaña. Autor: libres 11.251.548.160 bytes, durable 44.975.061 bytes, logs 99.855 bytes. Auditor: libres aproximadamente 11,02 GB, durable 38.825.944 bytes; RSS observado máximo 324.156 KiB incluyendo compilación. Sin muestreo continuo del pico temporal. Temporales históricos de timeout no totalmente atribuidos; no se borraron a ciegas ni se afirma cleanup total. Las nuevas ejecuciones usan scratch propio manifestado.

Manual único: `v3/backtester/README.md`. Superficies públicas: RunPlatformCampaign, ComposePlatformSpec, CompositionFactories, CLI platform-prepare/platform-batch. Reejecutar campaña detallada exige PlatformCampaignRequest completo y fábricas; un RunSpec desnudo de reproduce no reconstruye controles de admisión/cobro. Recetas finales se verificarán tras el nuevo freeze; no se inventan flags.

`spec.ExecutionModel`, market_data_mode y OHLC_CAUSAL_PATH_V2 con prioridades/slippage/fees/offsets están sellados por `fidelity.execution_model_digest`. `ModelIdentity` es etiqueta libre no vacía; no sustituye al modelo económico. Distinguir modelo causal, composition_id y agente solicitado/servido.

[[TRADESGERARD-GLM-MASTER]] encarga implementar todas las familias y variantes de B, luego baseline y producto cartesiano compatible completo con continuidad, validación y ranking. B no absorbe capacidades estructurales de A pendientes. Readiness técnico no certificaría términos comerciales UNKNOWN, LIVE ni rentabilidad. Código permanece en desarrollo local, sin push/merge/release afirmados.

## Fuentes

- [[TRADESGERARD-MANDATE-SNAPSHOT]], §§10–12; [[TRADESGERARD-CONTRACT]]; [[TRADESGERARD-PROP-PROFILE]].
- Recibos físicos del integrador, auditor, corrector y propuestas de cobertura bajo el workspace Aranea.
- `xKoRx/echo:specs/FEAT-TRADESGERARD-PLATFORM-A/`; matriz independiente y manual público.
