---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo Futures]]"
sprint:
start:
due:
progress: 28
repo: "xKoRx/echo"
jira:
prs:
aliases: []
tags:
  - kind/project
  - area/echo
created: "2026-10-20"
updated: "2026-10-20"
---

# Echo Futures — Optimización de Campañas

## 🎯 Objetivo

Diseñar e implementar un laboratorio reproducible para optimizar combinaciones de entrada, filtros, geometría de salida y MM, y seleccionar al menos cinco estrategias capaces de aprobar **≥25% de TODOS los challenges comprados** en el protocolo validado. El 35% del video es referencia aspiracional, no el gate obligatorio ni una garantía. El Owner acaba de fijar 1/4 como piso y prevalece sobre interpretaciones anteriores.

Una configuración que no alcanza el piso después de su búsqueda acotada y validación se descarta para challenge. No se borra código/evidencia ni se declara imposible toda su familia. Falta de datos, señales, muestra suficiente o un simulador inválido no se clasifican como fracaso económico.

Este documento es el **planificador único** de la iniciativa. Diseño, tareas, gates y despachos viven aquí. [[TRADESGERARD-CONTROL]] sigue siendo la autoridad del backtester histórico; [[Echo Futures — Runtime Pools]] sigue gobernando el runtime. No los reemplaza. La extracción del video es fuente de hipótesis, no especificación ejecutable de un optimizador.

## 📊 Estado actual

`PLAN_V1 / READY_FOR_SHOT1_WITH_LOCAL_PREFLIGHT`. Plan solicitado por el Owner; implementación nueva NO ejecutada. Sólo Shot 1 está preparado para despacho. Los demás requieren aceptación del gate anterior y autorización de su alcance. La auditoría acotada pre-research tiene resultado desconocido en esta planificación: no asumir PASS. S01 puede implementar piezas puras sin ese PASS; ninguna conclusión económica nueva se acepta hasta verificarlo.

Repositorio remoto histórico observado: `experiment/challenge-history-20261018@07cca9d399f3a4045aadb151dfcec612f192db96`. No hay inspección del working tree de Hefesto desde CLOUD. Rama runtime de referencia: `feature/ef-runtime-pools`; el planner reporta corte aceptado `b13ef43d01098de18856cce0ff95ee2761556071`. Se inspeccionaron contrato R6 y código selectivo, NO se certificó su despliegue.

La entrega histórica existente es referencia, no resultado de esta metodología: 26 configuraciones, horizonte 2023-10-02→2026-10-06, cobertura parcial declarada. El piloto antiguo `ce09ba4f/FIRST_PASS` y el log adjunto no gobiernan continuidad, selección ni aceptación de este plan.

**S01 EJECUTADO 2026-10-20 (G1 = review, sin aceptación propia):** rama `experiment/campaign-lab-s01` creada desde `20c73fd4` (descendiente verificado de `07cca9d3` vía `merge-base --is-ancestor`, auditoría acotada previa preservada; WIP previo vacío). Commit `e5af38eb` pusheado con readback (`origin == HEAD`). Entrega: kernel puro `v3/sdk/futures/riskgeometry` (SizingProfileV1/SizingInputV1/SizingProposalV1, consumidor de observaciones tipadas ATR14-Wilder/stdev20-ddof0 causal, sizing decimal exacto, ceil conservador a ticks, folding a lot_step, cap estructural explícito, rechazos nombrados sin fallback; coverage del paquete 96.7%, piso 95) y `v3/backtester/tools/tradesgerard/campaign-lab/` (catalog26 importado exacto de `challenge-first/generate.py`: 4TG+4FBC+3ORB-CH300+10MR+5ORB-NATIVE con 300/300 y 500/250 netos intactos, descriptores `SG-*` DECLARED_NOT_EXECUTED con bruto 500 USD separado del legacy, perfiles-v1, experiments-v1 DECLARATION_ONLY con `budget_semantics_ref`/`campaign_policy_ref`, validador/materializador stdlib fail-closed con digest estable ante path/host/attempt; 18 tests). Comandos probados: `validate` (VALID 26/2/1), `materialize --out $TMPDIR/...` (manifest `489a7c06…`, sin efectos económicos), `go test -cover ./v3/sdk/futures/riskgeometry/` PASS 96.7%, `python3 -m unittest test_campaign_lab` 18/18. Cero campañas ejecutadas; TGMM/Signal/Provider/ledger intactos; sin proyección de aprobaciones. **S01-R1 (corrección antes de G1, mismo día):** commit `8f2a8252` en la misma rama con push y readback. R1: validación de perfiles por valor alineada con `SizingProfileV1.Validate` y canonicalización decimal antes del digest (`"500"`≡`"500.00"`, una sola identidad); R2: contraste de instrumento canónico perfil↔recibido (`INSTRUMENT_MISMATCH`, identidad transportada desde `domain.Instrument.InstrumentID`, sin parsear símbolos); R3: conversiones enteras seguras (2^63 ticks ⇒ rechazo explícito, antes wrap→clamp a 1). Coverage Go 97,7%; Python 26/26 (18 originales preservados + 8 negativos); manifest digest estable `489a7c06…`. La auditoría pre-research existe en `20c73fd4` (AUDIT-NORMAL-20261020) y sus conclusiones/hallazgos NO se tocaron en este encargo.

Tarea puente humana: `[[Echo Futures — Optimización de Campañas]] implementar y revisar el laboratorio por shots #owner/me #type/supervision #area/echo`. Debe permanecer única en el proyecto padre; no crear otro control ni marcarla Done por el ejecutor.

## 🧱 Entrega de desarrollo

| Repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | create: `experiment/campaign-lab-s01` | corte histórico anterior, o descendiente verificado con WIP preservado | este planner §§1,3,6 | este planner §§2,4,5,7 | S01 por ejecutar; sin merge automático |
| xKoRx/echo | `feature/ef-runtime-pools` | corte reportado b13ef43d | R6 runtime | diseño runtime §§12–18 | READ_ONLY en S01–S04; integración sólo S05 autorizada |
| xKoRx/agents-os | `master` directamente | HEAD concurrente | este planner | skill de planificación | sólo documentos; sin PR/rama |

## 1. Decisiones cerradas y fuentes

| ID | status | resolution | source/evidence | phase consuming it |
|---|---|---|---|---|
| D01 | CONFIRMED | Piso obligatorio 25%; cinco estrategias como objetivo, sin prometer encontrarlas. | Owner, turno de planificación 2026-10-20 | 1–5 |
| D02 | CONFIRMED | Optimizar entradas, filtros y MM; usar ATR/stdev y lotaje para riesgo. Revalidar las 26 existentes. | Owner | 1–4 |
| D03 | CONFIRMED | Campaña continua, todas las compras y aprobaciones, cierre diario; no FIRST_PASS. | Owner e historial aprobado | 1–5 |
| D04 | CONFIRMED | Base portable al runtime; no duplicar dominio para backtest/LIVE. | Owner, Runtime Pools R6 | 1–5 |
| D05 | TECHNICAL_RESOLUTION | S01 sólo contratos, kernel de dimensionamiento y manifiesto; sin matriz histórica, nuevo MM completo ni Monte Carlo. | Riesgo/consumo de encargos anteriores; costuras verificadas | 1 |
| D06 | TECHNICAL_RESOLUTION | Nuevo perfil de geometría fija separado del TGMM histórico de objetivos netos. No cambiar su semántica. | HEAD tgmm.go, cabecera y New | 1–2 |
| D07 | TECHNICAL_RESOLUTION | Baseline nuevo: R presupuestado bruto 500 USD, ratio bruto 1:1, ATR14 Wilder M1 ×1.0; alternativa stdev de 20 cambios de cierre M1 ×1.0. | Elección explícita de diseño derivada del pedido; no regla del video ni valor optimizado | 1–3 |
| D08 | TECHNICAL_RESOLUTION | Ningún cambio silencioso de timeframe de las 26; originales conservan señal y salidas técnicas. Normalizaciones son variantes nuevas. | Fidelidad histórica y Signal account-agnostic | 1–4 |
| D09 | TECHNICAL_RESOLUTION | Política histórica y R6 de runtime tienen identidades distintas; ninguna tasa bajo una se vende como validación de la otra. | R6 vs platform_operability/TGMM | 1–5 |
| D10 | TECHNICAL_RESOLUTION | Proyección económica sólo filtra/promueve candidatos; campaña con mercado autoritativa. No rescales PnL para certificar otro MM. | Dependencia de fills, admisión, tiempos y trayectorias | 3–4 |
| D11 | TECHNICAL_RESOLUTION | GLM LOCAL, Hefesto, sin GOD/TOP ni subagentes. STOP al gate, presupuesto finito por shot. | Restricción de costo y una entrega por contexto | 1–5 |

Fuentes leídas, clase y localizador:
- **CONTRACT**: `VAULT_ROOT/10-projects/Echo Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md`, R6 §§12–18: Signal, asociación/MM versionados, analytics causal, disponibilidad, afinidad y drenaje.
- **ROADMAP/REPORT**: `VAULT_ROOT/10-projects/Echo Futures/agentes/Echo Futures — Runtime Pools.md`; no trasladar sus gates a esta rama.
- **HEAD**: `echo/v3/sdk/futures/strategies/tgmm/tgmm.go` en la rama histórica, blob `59437bb851422d26461600438319fbcb872ec679`: Manager.Evaluate, Config/New, presupuesto neto, objetivo remanente, geometría ATR inicial y recálculo posterior; ratio risk/target<1 no autorizado en ese módulo.
- **HEAD**: `echo/v3/sdk/futures/config/mm.go`, blob `c5b0fa4482b3c45b9fc3f2eabb497ea40f4d1057`: NewGerardMM, validación y composición existentes.
- **HEAD**: `echo/v3/sdk/futures/operation/mm.go` en runtime, blob `9ec1b50f1a2dcaf88ca53d010a0468672b63df7d`: triggers MM y EconomicsObservation causal; son contratos a reutilizar, no un API nuevo inventado.
- **REPORT**: `echo/v3/backtester/tools/tradesgerard/challenge-history/verification/history-execution-20261020/{MANAGER-REPORT.md,executive-26of26-economic.csv}` en `07cca9d3`.
- **SOURCE**: [[ECHO FUTURES — EXTRACCIÓN CRÍTICA DEL VIDEO KPSjqVoe_xU]] y [[VIDEO-KPSjqVoe_xU]]. Ejemplo de moneda con costos fijos, no entrada real de NQ ni trailing completamente especificado.

### Matriz requisito → evidencia → pendiente

| Requisito | Estado | Evidencia / diferencia | Trabajo |
|---|---|---|---|
| 26 entradas, campaña histórica, cierre y trazas | partial | REPORT 26/26; auditoría pre-research pendiente de adjudicar | reutilizar; no rehacer en S01 |
| Analytics → Strategy → Signal → Operation/MM/Provider | done como frontera contractual | R6 + SDK; paridad del nuevo perfil no probada | kernel común, integración S02/S05 |
| Stop ATR/stdev fijo + lotaje bruto | missing en el perfil solicitado | TGMM cambia precios para objetivos netos | módulo opt-in nuevo; no editar TGMM histórico |
| Registro versionado de candidato/experimento/promoción | missing | hay generadores específicos de lote, no asumir API universal | S01 manifiesto mínimo, sin DB/DSL |
| Barrido guiado, proyección, rechazo al 25% | missing | ninguna de las 26 acredita aún este protocolo | S03/S04 |
| Serving del nuevo perfil en runtime pools | partial | catálogo/asociaciones/MM pinning R6 existen en otro carril | adaptadores y paridad S05 |

## 2. Arquitectura objetivo y migración

Dos superficies, un dominio:

`Market/Bars → Analytics compartido → Strategy con filtros técnicos → Signal canónica → selección por asociación → Operation + MM configurado → Provider/RiskFinalizer → órdenes/fills/ledger`.

El laboratorio rodea esa cadena: `catálogo → experimento congelado → ejecución/proyección etiquetada → métricas → selección → bundle de promoción`. No se instala optimizador dentro de Core ni se importa backtester desde SDK.

**Strategy** posee patrón y condiciones de mercado. Sus filtros se evalúan causalmente en la misma oportunidad antes de emitir. No existe un segundo generador de señales en Python. No recibe saldo, fase o nombre de cuenta. El rechazo económico no resetea el episodio técnico ni reemite señales antiguas.

**Analytics** calcula una vez por key canónica (stream físico, timeframe, parámetros, precisión, calendario, versión). ATR/stdev no se recalculan en cada cuenta/MM. Snapshot portable: valor/unidad, stream, período, causal frontier y readiness; reutilizar la envoltura vigente. Missing/stale/future/wrong stream ⇒ no nueva exposición. Serialización no cambia el resultado. Prefijo/estado aislados entre runs.

**MM** congela la propuesta geométrica y su config al crear la Operation. Estado económico por cuenta/contexto/Operation, nunca global por Strategy. Conserva manejo de señales de cierre, seguridad y protección del lifecycle existente. **Pool** sólo selecciona con disponibilidad, FIFO/afinidad/claim/drain; no calcula ATR, cantidades, PnL ni target. El orquestador de investigación tampoco altera el ledger.

**Escala**: preparación compartible por cálculo, propuestas puras, manifiestos/jobs independientes y observación acotada; optimización secuencial dentro de cada trayectoria. En Hefesto iniciar jobs=1 y aumentar sólo según el gate vigente, nunca >3 en este plan. No servicios, colas remotas, dashboard, DSL, plugin framework o persistencia extra.

### Diferencia contractual crítica

El histórico usa `STRATEGIC_ENTRY_BUDGET_V1`/RiskFinalizer con pérdida por presupuesto y posibles ajustes. R6 define presupuesto completo sin inventar muerte por remanente positivo y disponibilidad económica por cuenta/asociación. **No son el mismo experimento.**

S01 registra `campaign_policy_ref` y `budget_semantics_ref`, no integra los owners de pools. S02 ejecuta nuevas geometrías con la política histórica explícita, informando ajustes y riesgo efectivo. S05 integra el conjunto coherente de cambios R6; vuelve a validar candidatos afectados. Un resultado histórico se etiqueta `HISTORICAL_POLICY_ONLY`, nunca `RUNTIME_READY`.

La portabilidad es usar el mismo kernel/perfil y fixtures desde SDK; la migración posterior transporta observaciones y configs por las asociaciones reales, no reescribe fórmulas. Una Operation abierta conserva su versión antigua. Cambios prospectivos y rollout disabled; ningún merge/deploy automático.

## 3. Objetivo, métricas y descarte

`pass_fraction = unique_passed / unique_purchased` sobre la campaña continua y todas las cuentas compradas. Pendientes permanecen en denominador; no se reclasifican como pérdidas. Compras = aprobadas + pérdidas de reglas + pérdidas de política + pendientes + otras terminaciones identificadas. Cero compras ⇒ N/A, no 0%.

`cash_cost_per_pass = (compras + renovaciones + otros cargos) / aprobaciones`. Aportes de investigación se reportan aparte; no son ingresos. PnL nominal de evaluación y caja Owner permanecen separados. Reportar tiempo por pase y fallo, P90, cohortes, sesiones elegibles/ready/con trades, frecuencia, riesgos/costos ejecutados, rachas, cierres y motivo de cada no-fill.

Estados de investigación: `DRAFT`, `IMPLEMENTATION_VALID`, `CHARACTERIZED`, `PROJECTED_ONLY`, `SCREENED`, `VALIDATION_PENDING`, `ACCEPTED_FOR_RESEARCH`, `REJECTED_CHALLENGE`, `INSUFFICIENT_EVIDENCE`, `DATA_BLOCKED`, `ENGINE_BLOCKED`, `RUNTIME_READY`.

- Resultado válido final <25% ⇒ `REJECTED_CHALLENGE` para esa versión/espacio de búsqueda. No maquillarlo quitando pendientes, cambiando reglas de prop o usando sólo cohortes favorables.
- No descartar una familia por el primer R=500 ni por cero señales. Se agota el espacio predeclarado y se conserva causa. Cambiar la hipótesis produce versión nueva, no sobrescribe el descarte.
- ≥25% es requisito necesario, no declaración de certeza. Para `ACCEPTED_FOR_RESEARCH`: integridad PASS, validación temporal sin retuning, costos/tiempos visibles, muestra y estabilidad evaluadas. No se inventa un tamaño mínimo universal como decisión del Owner: informar número de compras/resoluciones, seguimiento y variación temporal. Un cociente favorable con evidencia escasa queda candidato con incertidumbre explícita, no certificación robusta ni garantía. La suficiencia estadística se adjudica por separado del umbral numérico, sin ocultar el resultado observado.
- Informar incertidumbre por bloques y resultados por período; no exigir ni inventar un IC que mágicamente garantice 25%. No redondear 23,81 a25. 35% se conserva como benchmark aspiracional, no promesa de peor caso.
- Cinco estrategias son cinco mecanismos/candidatos diferenciados con solapamiento de señales y pérdidas estudiado; cinco tamaños de una entrada no cumplen el objetivo de diversidad.

## 4. Contratos propuestos (nuevos, no APIs existentes)

### 4.1 Núcleo portable

Proponer un paquete puro SDK `riskgeometry` (create; reutilizar un equivalente si el preflight lo encuentra). Sin import de Campaign, filesystem, reloj de pared ni red. Tipos monetarios/precio exactos del SDK; configuración decimal/racional, no floats binarios para dinero.

`SizingProfileV1`: id/version, distance_model, distance_multiplier>0, reward_multiple>0, gross_risk_budget_usd>0, instrument_ref y precision_policy. Modelos implementados en S01: `ATR_WILDER_M1_14` y `STDEV_POP_M1_DELTA_CLOSE_20`; `SIGNAL_REFERENCE` conserva geometrías existentes como descriptor, no se inventa un stop ante referencia ausente. Riesgo bruto por diferencia de precio; costos observados/proyectados en campos separados. No mezclar con `TGMM_NET_TARGET_LEGACY`.

`SizingInputV1`: perfil validado; side; instrument tick_size, point_value y lot_step enteros válidos; observación causal tipada del modelo seleccionado; decision_frontier/stream/config references; expected_closed_bar_end calculado por el calendario/owner (la observación debe corresponder a esa última barra cerrada y estar disponible antes de la fase causal de decisión); referencia de entrada válida; límite estructural de contratos si existe. No saldos ni remanente de DD en el kernel de distancia/cantidad. La autoridad Provider no se sustituye por esta función.

`SizingProposalV1`: quantity, distance_ticks, reward_ticks, planned_gross_risk, planned_gross_reward, requested_budget, budget_unused, model/config/observation refs, estado o razón de no propuesta. Costos estimados no se inventan: sólo con un modelo de costos entregado y declarado; no double-count slippage ya en fills. Diagnósticos con IDs en eventos, no labels OTel de cardinalidad ilimitada.

Fórmulas iniciales:
- ATR14: Wilder sobre TR y cierre previo; seed media de14 TR. Vista más reciente cerrada y disponible a la frontera causal; no vela en formación.
- Stdev20: población de los últimos20 cambios `C_i−C_(i−1)`, mean-centered, ddof=0, en puntos; requiere21 cierres completos. NO la desviación de20 niveles de cierre, ni volatilidad de retornos sin convertir unidades.
- `d_ticks = ceil(k × volatility_points / tick_size)`; valor cero/negativo, no disponible o de otra unidad ⇒ rechazo nombrado, sin fallback ATR↔stdev.
- `reward_ticks = max(1, ceil(reward_multiple × d_ticks))`; informar ratio efectivo por redondeo. A1:1 se cumple reward_ticks=d_ticks.
- `unit_risk = d_ticks × tick_size × point_value`.
- `q = floor(gross_budget / unit_risk)` al lot_step válido; aplicar sólo cap estructural explícito. q<1⇒`SIZE_BELOW_MIN_CONTRACT`, no cambiar stop, usar fracciones de NQ o cambiar a MNQ.
- Para stdev, reutilizar precisión/raíz del kernel existente si encaja. Alternativa exacta: menor entero de ticks que satisface la desigualdad al cuadrado; no agregar floats al dinero ni cambiar precisión global.

El resultado es propuesta, no garantía de pérdida máxima: gaps, costos y fills pueden alterar el resultado efectivo. El futuro adapter de MM ancla protección a fills autoritativos, preserva distancia congelada alineada a tick, no recomputa distancia para gastar el presupuesto sobrante ni persigue el target restante de evaluación. Fills parciales/rechazos/late fills se gestionan por Operation existente; no crear órdenes en S01.

Fixtures numéricos S01 (escenario NQ de prueba, valores del Instrument entregado): tick=.25, point_value=20, lot_step=1, presupuesto500. Volatilidad10 puntos×1→40 ticks, q2, riesgo bruto400, target bruto400, unused100. Volatilidad30→q0 y motivo explícito. Duplicar q duplica costos por contrato; un perfil de presupuesto no garantiza que se use exactamente ese importe.

### 4.2 Identidad de investigación

`CandidateSpecV1`: mecanismo, Strategy module/id/version/config digest, signal timeframe, lista ordenada de filtros tipados/configurados, geometría/salidas técnicas, MM/profile version, phase, campaign policy/ruleset. Filtros son módulos técnicos explícitos, no expresiones arbitrarias. S01 sólo conserva referencias; no implementa diez filtros.

`ExperimentSpecV1`: candidate ref, source/build, datos/calendario/roll/coverage mask, horizonte económico/prefijo, selector, compras/renovaciones/aportes, ejecución/costos, objetivos/criterios, dataset partition y espacio finito predeclarado, seed sólo para proyección. Hash semántico excluye path local/host/attempt; identidad de ejecución incluye source/binario. Canonicalizar racionales, units, orden y defaults; sin IDs de reloj o random.

`ObservationTape` futuro: oportunidad emitida, motivo de filtro, decisión/no-target, contexto de mercado, entrada/salida/fills, cantidades, costos, tiempos, account/session, refs de versión. Trade cerrado no representa oportunidades no admitidas. Contar oportunidades separadas de fills. No duplicar Signal ni meter `experiment_id` en su payload para forzar diferencias; correlation por provenance/binding exterior.

`PromotionBundle` futuro: configuración común, requirements Analytics, módulo/MM versionados, policy/ruleset compatibles, evidencias/gates, digest. No contiene rutas de Hefesto, saldos de backtest ni activaciones comerciales. Sin aprobación humana no habilita runtime.

### 4.3 Dos modalidades de gestión, no una mezcla

`NATIVE_REPLAY`: las26 tal como se ejecutaron, mismos timeframes/MM/salidas/ADD; evidencia vieja sólo se reusa con identidad compatible.

`STANDARDIZED_GEOMETRY`: mismas entradas/filtros y cierres técnicos, nuevo MM geométrico ATR/stdev+riesgo. Esas son variantes nuevas. No se fuerza 1m a entradas FBC5/15/30/60 o MR5m/H1. Las observaciones de volatilidad M1 pueden alimentar MM sin cambiar el timeframe de señal. C04/C05 con ADD se preservan como nativas; en el perfil nuevo NO_ADDS deben tener ID/version distinta y no cuentan como tres hipótesis nuevas si colapsan semánticamente al mismo candidato.

## 5. Método de búsqueda finito y barato

1. Integridad: consumir el dictamen acotado existente. Corregir defectos materiales sólo con autorización del shot; ENGINE_BLOCKED no es estrategia mala. No otra auditoría mundial por rutina.
2. Revalidar catálogo completo: importar las26 con provenance y discrepancias, jamás seleccionar sólo las que aprobaron. Caracterizar entradas/salidas y oportunidades con riesgo de referencia; mantener replay nativo y perfil nuevo separados.
3. Screening: perfil nuevo ATR14×1, 1:1, 500bruto. Variar riesgo sólo en `[250,500,750]`, dentro de lo viable. Descarta puntos geométricamente idénticos tras redondeo sin simularlos dos veces, pero conserva alias/rechazos. No es máximo global.
4. Refinamiento: por candidato prometedor, a lo sumo dos vecinos de riesgo dentro del rango declarado (midpoints entre el mejor y sus vecinos); un extremo sólo permite una ampliación previamente registrada, no bucle ilimitado.
5. Geometría: mantener el riesgo candidato; contrastar ATR×0.75 y ATR×1.5 contra ATR×1.0 O stdev20×1.0, no todo el producto cartesiano. Elegir una de esas preguntas por ronda antes de resultados.
6. Filtro: un filtro con hipótesis de fallo explícita por ronda, baseline pareado; registrar qué trades/días gana y pierde. Fijado el filtro, reconfirmar a lo sumo tres riesgos alrededor del anterior. Sin cambios simultáneos de entrada, política de cuenta y modelo de fills.
7. Congelar el candidato y validar en tiempo distinto; cada modificación tras ver confirmación invalida su carácter de confirmación y cuenta como otro intento registrado. Registrar TODOS los intentos, no sólo ganadores.

El espacio se declara antes de cada ronda y se aplica por candidato; el catálogo completo se recorre por tandas acotadas, no un shot gigante. No probar la siguiente ronda sin aceptar el gate y presupuesto.

### Proyección vs mercado

S03 podrá usar un proyector offline liviano sobre métricas/tapes, primero modelo binario diagnóstico y luego bloques de sesiones, con 10.000 trayectorias como cantidad de simulación, NO 10.000 muestras reales. Reutilizar kernels puros de reglas disponibles; lo que requiera fills intrabar no se suplanta con fórmulas paralelas. Costo variable por cantidad y eventos; modelo iid declarado, no supuesto oculto.

Rescalar PnL no valida otro stop, RR, admission, selector o duración. Reordenar retornos no representa un rollover físico. Proyección ⇒ `PROJECTED_ONLY`, útil para priorizar; aceptación exige ejecución real del motor con los inputs de ese perfil. Si no hay tape suficiente, se ejecuta la caracterización necesaria, no se fabrica. El nulo del video no exige coincidencia exacta del35% sin código/semilla/reglas completas.

### Cronología y confirmación

Toda entrega final conserva la campaña histórica única de inicio a fin, sin reset mensual/anual/roll. Separar de los ensayos por cohortes temporales, que tienen IDs y capital inicial explícitos y nunca se suman fingiendo una única trayectoria.

Partición inicial de investigación: primeras60%, siguientes20%, últimas20% de sesiones elegibles, fronteras fijadas por inventario antes de nuevos resultados, con prefijos causales. Ajuste en60; selección limitada en20; confirmación final una vez en20. Todo ese histórico ya tuvo inspección agregada: rotular `RETROSPECTIVE_TEMPORAL_CONFIRMATION`, no OOS virgen. Para confirmación por cohorte, cuentas compradas en cada tramo son denominador y carry-in se informa aparte; al final las pendientes no desaparecen. Datos no vistos/prospectivos serán la evidencia futura adicional, no se inventan hoy.

## 6. Gates, presupuesto y roadmap

| Gate | current state | phase agent responsibility | owner acceptance evidence | enables |
|---|---|---|---|---|
| G1 | delivered: S01+S01-R1 en review (`experiment/campaign-lab-s01` @ `8f2a8252`); el ejecutor NO lo acepta | kernel/manifiesto y tests; dejar review | Owner evalúa recibos S01 | S02 |
| G2 | pending | MM geométrico/analytics/config integrado y pruebas cortas | Owner acepta integridad; auditoría acotada consumida | S03 |
| G3 | pending | catálogo caracterizado y screening finito trazable | Owner acepta resultados y candidatos | S04 |
| G4 | pending | confirmación temporal y descarte/selección | Owner acepta candidatas >=25% con límites | S05 o nueva ronda versionada |
| G5 | pending | compatibilidad/runtime y suite de paridad | Owner autoriza integración; LIVE separado | migración prospectiva, no activación automática |

Ningún ejecutor acepta su gate ni inicia el siguiente. Dos reintentos correctivos por causa como máximo; después bloquear la causa, no ampliar arquitectura. Una fila con datos insuficientes no bloquea trabajo independiente válido. Cobertura del delta según piso del proyecto, sin inventar un framework para medirlo; si la herramienta vigente falla, causa explícita. Sin sesiones GOD ni subagentes.

**Presupuesto S01:** un GLM, máximo90min de sesión activa (límite operativo, no estimación), 20min acumulados de comandos de tests/build y cero campañas históricas. Si el harness no mide inferencia, no afirmar consumo exacto: usar reloj y contador de comandos. Checkpoint único antes de llegar al límite. Antes de90min entrega estado y deja de trabajar; nada de terminar una última refactorización. No tests globales con infraestructura ni espera autónoma. Recursos sólo Hefesto según gate ya medido.

## 7. Paquetes autónomos

### Paquete autónomo Fase 1 — SHOT1: contratos y kernel portable

**Misión exacta** Implementar SizingProfile/Input/Proposal, cálculo puro ATR/stdev-consumidor y manifiesto determinista de candidatos/experimentos. Importar las26 identidades de la entrega, preservando baseline. Es producto ejecutable/testeado, no sólo docs; no es aún un MM que emita órdenes.

**Precondiciones verificables** Pedido Owner de diseño+Shot1; base/working tree confirmados localmente. No requiere G0 inventado ni conclusión favorable de trading. Si auditoría pendiente afecta estos tipos concretos, registrar scope; no declarar invalidado todo por ausencia de informe.

**Lectura obligatoria** Este planner §§1–6/S01; `VAULT_ROOT/10-projects/Echo Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md` §§12–17; archivos HEAD citados; materializador/manifiesto de challenge-history y catálogo heredado sólo para importación. No historial D1–D6 ni logs FIRST_PASS.

**Decisiones cerradas** D01–D11; stop-price geometry y presupuesto bruto separados de TGMM. Valores de volatilidad vienen de snapshots tipados ya calculados; S01 NO implementa producción de ATR/stdev ni llama kernels por cuenta. Contrato exige exacta semántica de unidad/ventana y causalidad; integración owner S02.

**Implementación paso a paso** T1.1 mapear costuras y dejar bridge; T1.2 paquete puro validado; T1.3 manifiesto/catalog26 y perfiles propuestos sin ejecutar; T1.4 roundtrip/config drift/aislamiento/fixtures; T1.5 evidencia y handoff G1 review.

**Archivos esperados** create propuesto `v3/sdk/futures/riskgeometry/{profile.go,sizing.go,sizing_test.go}` y pruebas de serialización; create `v3/backtester/tools/tradesgerard/campaign-lab/{README.md,catalog-v1.json,experiments-v1.json}` + materializador mínimo stdlib/test junto al tooling existente. Config nuevos aquí son contratos de investigación, no modificar `ConfigSnapshot`/registry MM todavía. Reusar naming local si equivalente real; registrar mapeo. Máximo dos módulos nuevos (SDK kernel + herramienta de manifiesto).

**No tocar** Strategy/Signal, TGMM, Provider, ledger, platform_campaign, motor/fills, runtime branch, bridges, fuentes/datasets, calendarios, generadores anteriores y resultados. No scripts de producción ni servicios. Sin nuevo MM completo, proyector, filtro, datos o histórico.

**Spikes permitidos** Una inspección focalizada de hasta15min, incluida en los90min, para resolver unidades/precisión/normalizador y schema del catálogo. Leer los símbolos citados y sus llamadas directas. Si un equivalente no existe, crear sólo tipos/kernel definidos; contradicción de dueño ⇒ PLAN_CONFLICT, no importar pool completo.

**Tests y asserts** LONG/SHORT; ticks y lotes exactos; q0; presupuesto/units inválidos; ATR/stdev distintos sin fallback; future/stale/wrong-stream; q2×10p×20=400; redondeo cerca de tick; ratio1 mantiene distancias; monotonía en budget para geometría/caps fijos; inputs inmutables; serialización y snapshot idéntico en otro contexto; dos perfiles sin estado compartido. Manifiesto26 únicos, cambio semántico cambia digest, cambio de path/host no, unknown config fail-closed, 300/300 nativo !=500bruto experimental. Ninguna entrada de red ni campaña iniciada por materializar.

**Entregables/Gate G1** Diff pequeño, catálogo26, perfiles/contratos, tests/coverage del delta, tabla compatibilidad R6, comando local probado de validar/materializar, límites reales y ninguna cifra de aprobaciones inventada. `IMPLEMENTATION_COMPLETE/G1=review` no `RESEARCH_PASSED`.

**Handoff a Fase 2** SHA limpio o WIP explícito, contratos exactos, ejemplos serializados, fixtures y allowlist de integración pendiente. No aceptación propia.

### Paquete autónomo Fase 2 — integración de geometría y paridad local

**Misión exacta** Nuevo MM opt-in de geometría fija que usa kernel S01; conectar analytics causal a config/Operation en rama de investigación, conservar TGMM. Ensayos cortos, no26años.
**Precondiciones verificables** G1 accepted; dictamen pre-research conocido para los caminos usados.
**Lectura obligatoria** S01 y `VAULT_ROOT/10-projects/Echo Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md` §§12–17; composition/Operation/MM/analytics y runners existentes.
**Decisiones cerradas** D06–D10; NO_ADDS nuevo, salidas técnicas preservadas, presupuesto bruto no net-target.
**Implementación paso a paso** T2.1 demands/owner-volatility; T2.2 MM+pin config+fills/protection; T2.3 adapter de Campaign y ensayos causalidad/cierre.
**Archivos esperados** modify SDK config/analytics/composition y seam de runner; create mínimo módulo MM donde indique registry vigente. Conjunto exacto se sella antes del primer edit.
**No tocar** economía Provider, driver de ejecución intrabar, runtime publicado, calibración de entradas ni políticas heredadas.
**Spikes permitidos** uno para transportar observación MM por contrato existente; si exige reescribir pools, PLAN_CONFLICT.
**Tests y asserts** entrada→fill→protección→salida→ledger en ambos lados; parciales y gaps; cierre horario; dos perfiles aislados; snapshot serializado; config in-flight pin; fixture 2pases sin corte; riesgos solicitado/ejecutado/ajustado visibles.
**Entregables/Gate G2** Integración funcional y máximo6 ensayos deterministas de hasta20 sesiones válidas cada uno; no interpretar como validación histórica. Límites OHLC y política histórica explícitos.
**Handoff a Fase 3** perfiles ejecutables, tests, tiempos/memoria medidos, auditoría y comandos. Gate review.

### Paquete autónomo Fase 3 — revalidación26 y screening

**Misión exacta** Caracterizar las26 y buscar regiones de sizing con estrategia congelada; no incorporar filtros nuevos todavía.
**Precondiciones verificables** G2 accepted, integridad del motor aplicable PASS; dataset/split/espacio sellados.
**Lectura obligatoria** este planner §§3–5 y `VAULT_ROOT/10-projects/Echo Futures/agentes/Echo Futures — Optimización de Campañas.md`; recibos de S02 y catálogo.
**Decisiones cerradas** Nativo vs normalizado, tres riesgos, todas las compras; proyector no acredita passes históricos.
**Implementación paso a paso** T3.1 import/replay selectivo por identidad y caracterización; T3.2 proyección económica finita con controles; T3.3 ejecución shortlist con motor y tabla de cobertura de26. Tandas de máximo6 campañas largas por despacho, nunca más sin gate de presupuesto.
**Archivos esperados** campaign-lab materializador/runner/report; adaptar mínimo módulos puros existentes del proyector si útiles.
**No tocar** kernel financiero, prop rules, filtros/entradas, full funded ni global optimizer.
**Spikes permitidos** definir aptitud del tape para proyección; si no sirve, marcar aproximación, no inventar datos.
**Tests y asserts** 0 denominador; costos con cantidades; cero señales; corrupción ⇒FAIL; contadores de intentos; reproducción semillas; ninguna proyección entra como resultado de mercado.
**Entregables/Gate G3** todas26 clasificadas por estado real, curvas/vecinos ejecutados, costos y consumo; las no ejecutadas quedan pendientes explícitas. Cadencia por tandas registrada en mismo gate, no autoavance.
**Handoff a Fase 4** candidatos congelados y preguntas de filtros, sin borrar negativos. Gate review.

### Paquete autónomo Fase 4 — filtros y confirmación temporal

**Misión exacta** Contrastar una condición motivada por ronda, reconfirmar sizing y descartar versiones que no llegan al25% bajo protocolo suficiente.
**Precondiciones verificables** G3 accepted; candidato/filtro/fechas/contador de pruebas y presupuesto cerrado.
**Lectura obligatoria** §3/§5 y `VAULT_ROOT/10-projects/Echo Futures/agentes/Echo Futures — Optimización de Campañas.md`; evidencias de fallos S03.
**Decisiones cerradas** máximo un filtro nuevo por ronda, cinco estrategias no cinco tamaños, validación sin reoptimizar holdout.
**Implementación paso a paso** T4.1 versión del filtro en Strategy/Analytics; T4.2 comparación pareada y sizing local; T4.3 confirmación y adjudicación candidata/rechazada/insuficiente.
**Archivos esperados** módulos técnicos existentes y sus configs/tests, manifests y reportes de campaign-lab.
**No tocar** reglas económicas para fabricar25%, descartes silenciosos, nuevo engine o actividad LIVE.
**Spikes permitidos** diagnóstico acotado de rachas/causa del filtro; si no hay hipótesis, no despachar filtro.
**Tests y asserts** causalidad, filtros off=baseline, cuentas/pases/cohortes conciliados, ejemplos que el filtro elimina y conserva, sensibilidad acotada de costos/fills.
**Entregables/Gate G4** resultados candidatos y descartes con denominadores/tiempos/robustez; no promesa de encontrar cinco. Gate review.
**Handoff a Fase 5** bundles congelados; una nueva ronda require decisión registrada, no loop infinito.

### Paquete autónomo Fase 5 — adopción runtime sin duplicación

**Misión exacta** Portar integración, no fórmulas; mismo perfil/kernel por asociación con observaciones serializadas y config sellada. Validar efecto de política R6 antes de hablar de tasa runtime.
**Precondiciones verificables** G4 accepted, permiso explícito de integración al carril runtime, bases reconciliadas con su manager.
**Lectura obligatoria** `VAULT_ROOT/10-projects/Echo Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md` §§12–18; contratos y fixtures de este proyecto.
**Decisiones cerradas** Signal inmutable, dos pools/una Strategy/un cálculo, MM estado por Operation, no live automático.
**Implementación paso a paso** T5.1 registro/config transport; T5.2 parity decisiones con fixtures equivalentes; T5.3 activar perfil sólo disabled/SIM y plan de rollout Owner-gated.
**Archivos esperados** config/observations/registry runtime existentes y tests de integración; kernel compartido reutilizado.
**No tocar** IDs históricos, dinero viejo, credenciales/infra comercial ni cambios retrospectivos de operaciones.
**Spikes permitidos** compatibilidad de cambios de ramas; conflicto⇒PLAN_CONFLICT, sin cherry-picks parciales ciegos.
**Tests y asserts** config pin, stale obs, turn rotate/no replay, multiaccount aislamiento y decisiones equivalentes. Las diferencias legítimas de política se reportan como otros experimentos.
**Entregables/Gate G5** matriz de paridad source/config/input, fixtures y rollback drenado; runtime-ready sólo con aceptación, LIVE separado.
**Handoff** Owner y manager runtime; no despliegue implícito.

## ✅ Tareas

Cada fila es objetivo | símbolos | precondición | implementación | test | evidencia. No tareas en otros planners.

- [x] T1.1 Identidad/puente | HEAD/Units/catalog | pedido Owner | mapear delta y bridge | sin cambios ajenos | BASELINE.md #owner/agent
- [x] T1.2 Kernel puro | riskgeometry (create) | T1.1 | perfiles/fórmulas§4.1 | fixtures/causalidad/rounding | tests+coverage #owner/agent
- [x] T1.3 Manifiesto26 | campaign-lab (create) | T1.1 | identidad y validación§4.2 |26únicos/drift/no I/O económico | catálogo sellado #owner/agent
- [x] T1.4 Compatibilidad | tests kernel+manifest | T1.2–3 | serialización/matriz R6 | aislamiento/sin side effects | recibo #owner/agent
- [x] T1.5 Entrega | planner/artefactos | T1.4 | revisar diff/publicar evidencia | readback | G1 review #owner/agent
- [ ] T2.1 Analytics causal | owners existentes | G1 accepted | demands ATR/stdev | referencia manual/futuro | recibo #owner/agent
- [ ] T2.2 MM ópt-in | registry/Operation | T2.1 | kernel→órdenes/protección | fills/partials/close | E2E #owner/agent
- [ ] T2.3 Integración corta | runner | T2.2 | <=6 ensayos | invariancias | G2 review #owner/agent
- [ ] T3.1 Catálogo26 | tape/import | G2 accepted | caracterización | identidad completa | por fila #owner/agent
- [ ] T3.2 Proyección | tooling aislado | T3.1 | tres riesgos | nulo/costos/seed | aproximación declarada #owner/agent
- [ ] T3.3 Campaña shortlist | runner | T3.2 | tandas<=6 | oráculos | G3 review #owner/agent
- [ ] T4.1 Filtro | Strategy/Analytics | G3 accepted | uno motivado | causalidad/off | versión nueva #owner/agent
- [ ] T4.2 Región MM | runner | T4.1 |<=3 riesgos | comparabilidad | curva #owner/agent
- [ ] T4.3 Adjudicación | report/bundle | T4.2 | confirmación25% | evidencia/muestra | G4 review #owner/agent
- [ ] T5.1 Adapter runtime | config/registry | G4+permiso | wiring común | config pin | diff #owner/agent
- [ ] T5.2 Paridad | runtime harness | T5.1 | entradas equivalentes | no MM/Strategy duplicado | matriz #owner/agent
- [ ] T5.3 Rollout plan | bundle | T5.2 | disabled/SIM/rollback | drains | G5 review #owner/agent

## 8. Prompt común y despachos

### Prompt común del ejecutor

Actúa como implementador GLM-5.3-Flash Max LOCAL en Hefesto. Lee Estado actual y únicamente el paquete asignado más sus referencias. Usa el planner como autoridad; no redescubras toda la historia. Verifica HEAD/WIP y conserva trabajo ajeno. Sólo código de tu fase en rama experimental propia; Agents-OS master directo, sin ramas/PRs. No GOD/TOP/subagentes, infraestructura, LIVE ni merge automático. Semántica propuesta no implica API existente: mapea a tipos reales mediante el spike acotado. No importes backtester a SDK. Registra ejecución y límites honestos. Tests y recibos antes de gate review. No autoaceptes gate ni avances al siguiente. Dos intentos por defecto y presupuesto del shot; bloqueo puntual con WIP preservado. No cierre completo de sesión salvo instrucción explícita del Owner; deja continuidad liviana y evidencia. El prompt descargable de Shot1 es proyección de este común+S01, no otra autoridad.

**Despacho Fase 1**
FASE_ASIGNADA=1; PAQUETE_CANONICO=S01 de esta nota; GATE_REQUERIDO=pedido Owner, sin gate previo; TAREAS=T1.1–T1.5; SALIDA=kernel/manifiesto26/tests; STOP=G1 review o bloqueo; cero campañas.

**Despacho Fase 2**
FASE_ASIGNADA=2; PAQUETE_CANONICO=S02; GATE_REQUERIDO=G1 accepted; TAREAS=T2.1–T2.3; SALIDA=MM+analytics+<=6 ensayos; STOP=G2 review.

**Despacho Fase 3**
FASE_ASIGNADA=3; PAQUETE_CANONICO=S03; GATE_REQUERIDO=G2 accepted; TAREAS=T3.1–T3.3; SALIDA=caracterización26+screening por tandas autorizadas; STOP=G3 review.

**Despacho Fase 4**
FASE_ASIGNADA=4; PAQUETE_CANONICO=S04; GATE_REQUERIDO=G3 accepted; TAREAS=T4.1–T4.3; SALIDA=validación/rechazos/bundles; STOP=G4 review.

**Despacho Fase 5**
FASE_ASIGNADA=5; PAQUETE_CANONICO=S05; GATE_REQUERIDO=G4 accepted+permiso runtime; TAREAS=T5.1–T5.3; SALIDA=paridad/migración; STOP=G5 review; no LIVE.

## 9. Validación documental y límites

Template/envelope de proyecto resuelto contra `70-templates/project.md` (f9fc7ed4) y schema1. Validación estructural de secciones, tareas, gates, despachos, fórmulas y referencias; no equivale a tests de producto. El acceso CLOUD no verifica WIP ni procesos de Hefesto. No se reclama Graphify actualizado ni auditor independiente. El materializador/lint completo del vault remoto no se ejecuta mediante la API; el ejecutor hará el preflight documental mínimo sin convertirlo en reparación de Agents-OS.

El experimento antiguo de moneda permanece benchmark educativo. Ninguna implementación ni resultado nuevo se certifica en este diseño. No se cambia la extracción de video ni el control del runtime. Una decisión nueva del Owner se incorpora aquí por delta.

## 📆 Bitácora

- **2026-10-20** — PlanV1 creado por pedido Owner: piso25%, riesgo/geometría separados, 26 entradas preservadas, runtime R6 contrastado, cinco paquetes con gates. S01 acotado a contratos+kernel+manifiesto; cero pruebas económicas. Manager abierto.
- **2026-10-20 — SHOT1 ejecutado (T1.1–T1.5), STOP en G1** — Un GLM LOCAL en Hefesto, sin subagentes, cero campañas. Preflight: HEAD local `20c73fd4` confirmado como descendiente del corte verificado `07cca9d3` (preservado), WIP vacío, blobs citados por el planner verificados idénticos por `git hash-object` (tgmm `59437bb8`, config/mm `c5b0fa44`, operation/mm `9ec1b50f`). Rama propia `experiment/campaign-lab-s01` + commit `e5af38eb` pusheado y releído (`origin == HEAD`). Decisiones aplicadas: D05–D08 (kernel/manifests sin matriz histórica, geometría fija separada de TGMM, baseline bruto 500 ATR×1 1:1 con stdev como alternativa, sin cambio de timeframes). Mapeo de nombres propuestos a tipos reales: instrument → `domain.ContractSnapshot`/`InstrumentSpecFromSnapshot`, dinero → `units.Money/Price` (big.Rat, sin floats), dirección LONG/SHORT propia (domain.Side es BUY/SELL físico). Hallazgo de implementación: el ratio efectivo 4/3 no es decimal finito ⇒ se reporta como racional exacto (`"4/3"`), sin aproximación. Ramas muertas eliminadas en vez de testeadas (regla de cobertura). Tests: Go 10 funciones (fixtures planner exactos: 10p→40t/q2/400/400/100; 30p→SIZE_BELOW_MIN; monotonicidad de presupuesto; roundtrip/inmutabilidad/aislamiento; digests; causalidad stale/future/not-available/wrong-stream/wrong-model sin fallback) coverage 96.7%; Python 18 (26 únicos, familias exactas, nativas preservadas C04/C05 ADD, digest inmune a path/host/attempt y sensible a significado, fail-closed ×9, materializar determinista y sin efectos). Tarea puente `[/]`→`[r]`; pendiente Owner: aceptar G1 (revisión de recibos S01) para habilitar S02.
- **2026-10-20 — S01-R1 ejecutado, STOP** — Corrección acotada antes de G1 sobre `e5af38eb`; commit `8f2a8252` pusheado y releído. RED→GREEN documentado: R1 (8 tests negativos de perfiles: amount -500, multiplier 0/'nonsense', version 0, ids duplicados con valores distintos — antes aceptados; canonicalización `"500"`/`"500.00"` a una identidad vía vista canónica usada por materialize), R2 (`InstrumentRef` transportado verbatim en la envoltura nueva desde `domain.Instrument`; NQ/NQ propone, NQ-perfil/ES-recibido rechaza `INSTRUMENT_MISMATCH` aunque ambos sean USD y observación/stream concuerden; identidad sobrevive serialización), R3 (`ceilDiv`/`floorDiv` con guard `IsInt64`: repro 2305843009213693952 puntos → 2^63 ticks ⇒ error explícito, el código anterior envolvía a negativo y clampeaba a 1; overflow de reward y cantidad cubierto). Suites: Go PASS coverage 97,7% (piso 95), Python 26/26. `validate`/`materialize` deterministas con el catálogo existente: manifest `489a7c06…` SIN cambios (los valores shipped ya eran canónicos). Contradicción planner resuelta: fila G1 ahora `delivered: S01+S01-R1 en review`, sin aceptación del ejecutor. Alcance respetado: sólo riskgeometry/, campaign-lab/ y delta documental; TGMM/Strategy/Signal/Provider/ledger/rama runtime intactos; auditoría pre-research sin cambios.
