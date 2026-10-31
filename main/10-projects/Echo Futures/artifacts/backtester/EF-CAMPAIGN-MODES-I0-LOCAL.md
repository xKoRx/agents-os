---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[EF-CAMPAIGN-MODES-DESIGN]]"
  - "[[Echo Futures — Optimización de Campañas]]"
  - "[[EF-CAMPAIGN-MODES-GO-S04-RETURN]]"
  - "[[EF-S04-INTEGRATION-RECONCILIATION]]"
aliases:
  - "Echo Futures — Mandatos Go-only C06"
  - "Echo Futures — Cierre final y último contrato"
tags:
  - kind/doc
created: "2026-10-28"
updated: "2026-10-30"
---

# EF-CAMPAIGN-MODES-I0-LOCAL

## Propósito

**MANDATO VIGENTE: EF-CAMPAIGNS-FINAL — 30-10-2026 (America/Santiago).** Una única sesión coordinadora LOCAL nueva debe completar la entrega Go C06, migrar el catálogo entero, ejecutar y comparar el último contrato físico NQ y entregar al siguiente agente el histórico completo listo para ejecutar. **GLM-5.3-Flash coordina; TODO el código, pruebas, harnesses y correcciones los implementan subagentes MiniMax M3.1 Flash.** No se despacha otra revisión general antes de avanzar ni otro ciclo S03/S04 por rutina.

El diseño C06 [[EF-CAMPAIGN-MODES-DESIGN]] sigue siendo la arquitectura. Este documento es su mandato final de entrega y precisa las pruebas de determinismo y el alcance autorizado por el Owner, no otro diseño/motor. El planner único es [[Echo Futures — Optimización de Campañas]]. Este path histórico se conserva para no romper routing; los prompts de tres shots que lo ocupaban quedan supersedidos como instrucciones activas, con su texto y los retornos íntegros preservados en Git (corte anterior `bb51f2ecd228047abd31c63edf94c11517d65e8e`). No reactivar el I0 Python ni fusionar su rama.

**Visión del Owner:** cientos de estrategias y MM concretos, reutilizados mediante factories compartidas por runtime y backtester; tres tipos de Campaign reutilizables, no una implementación por estrategia; mismos hechos ordenados y mismo estado deben producir exactamente la misma operación; investigación histórica posterior sin volver a desarrollar el sistema. Primera candidata real objetivo domingo **1 de noviembre de 2026**. La fecha expresa prioridad, no certificación automática, promesa de rentabilidad ni autorización de órdenes reales.

## 1. Baseline y memoria mínima que evita repetir el trabajo

| Elemento | Estado de entrada |
|---|---|
| Repositorio producto | `xKoRx/echo` |
| Rama de trabajo | `feature/ef-campaigns-go` |
| HEAD verificado para este despacho | `a22970c85d139c81c919aafac69f4bf6ceaf5dcd` |
| Master observado | `2baf319ddcba622d9557bc9f23a13787b44c58a7`; sin merge C06 |
| SHA revisado en S03/S03R1 | `062b6df77845d2042e398bb6174700e80bb58b60` |
| Build S04 reportado | SHA256 `9769039d69d26ddb54b953ad2a9eb289a6ac9d6c7f5bd9faf1392bac5c939c35` |
| C06 actual | PARTIAL según retorno S04; no acabado ni LIVE-ready |
| Catálogo de referencia | 26 nativas +63 SG =89 configuraciones ejecutables; +15 aliases =104 filas; no son104 estrategias |
| Materialización general reportada | 27 V2_ADMITTED (26 TGMM+1 RGMM), 62 BLOCKED por fuente sellada de AccountPolicy RG,15 aliases; LEGACY_PATH_PRESERVED es dimensión adicional, no otras26 |
| Ejecuciones económicas C06 reportadas | 0 históricas; las pruebas mecánicas de candidatas NO ejecutan sus señales reales |
| Candidata priorizada | `LAB-SG-FBC-CH300-15M-R500`; comparación `LAB-SG-MR-09-R750`, prioridad de revalidación, no ganadora impuesta |
| Restricción LIVE | RGMM es HISTORICAL_POLICY_ONLY; no eliminar guardas para decir listo |

Estos datos de ejecución son reportados por los workers anteriores. El manager CLOUD comprobó las refs/retornos/source focal, no ejecutó sus suites. El coordinador nuevo verifica hashes y recupera evidencia local antes de reutilizarla. Si cambió HEAD, reconciliar el delta y fijar base efectiva sin pisar WIP. No volver a implementar lo que ya está ni basarse en la rama Python.

### 1.1 Qué ya existe y se reutiliza

Go implementa CHALLENGE/FUNDED/SIMULATION, inventario/rotación, composición simultánea, wiring TGMM/RG por catálogos sellados, heterogeneidad de perfiles/RuleSets/MM, FUNDED multi-asociación, CloseSafety, eventos/proyección, reversos y CLI lab. S04 reporta correcciones de routing de la segunda Strategy y del RuleSet del seed, activación aplicada/compliance separados y admisión física en puertas legacy. Revalidar los seams críticos con fixtures/outputs, no rediseñar por sospecha general.

Factories y owners SDK: `NewSealedMoneyManagerCatalog`, `WireSealedMoneyManagers`, `SealedAccountPolicy`, Strategy/Operation/Provider/accounting, claims/fencing/drain. Backtester añade adaptadores de fuente/reloj/venue y Campaign comercial; no debe duplicar señales, sizing, reglas de riesgo o lógica de operaciones.

### 1.2 Problemas conocidos que esta sesión debe resolver

1. **Migración parcial de configuración:** faltan62 SG en el builder general. R01/R03 ya declaran AccountPolicy por identidad; recuperar planes+receipts, verificar contenido/hashes y materializar un manifest derivado completo. El Owner autoriza esta recuperación de hechos existentes para la migración: NO pedirle transcribir62 políticas ni inventar defaults870/1000 para todas. Conflicto entre fuentes => identidad concreta bloqueada, no paralizar las demás.
2. **Sustitución de Strategy en la prueba:** `campaign_v2_candidate_test.go::candidateMechanicalFixture` devuelve `platformproof.NYStrategy`; prueba un MM/lifecycle, no FBC/MR. Las validaciones de catálogo y último contrato deben usar módulos y parámetros reales sin overrides. Fixtures de señales sólo para unitarios adversariales, rotulados aparte.
3. **Pérdida de CloseSafety al derivar:** `campaign_v2_candidate.go` documenta que el calendario sellado queda sólo como provenance y no viaja al request v2; horizonte NO reemplaza calendario de sesiones/horas/exclusiones. Conservar los controles y datos efectivos en la migración; si el perfil nuevo cambia semántica, versionarlo y no afirmar SAME_SEMANTICS.
4. **REFUND sin productor de lifecycle:** no basta enum/proyector. Implementar aplicación determinista de una devolución comercial explícitamente declarada/confirmada mediante el control/evento del owner existente: causa, importe, moneda, adquisición, idempotencia, autorización/provenance y caja. NO inventar una regla de reembolso automático por fallo/fin de horizonte. Una devolución no declarada nunca ocurre; el test usa instrucción de devolución rotulada y demuestra el productor real.
5. **Calidad pendiente:** coverage reportado79,6% diff-aware vs piso95%; race no ejecutado por host; corpus decía15 PASS+5 FAIL de21, falta clasificar una fila. Reconciliar resultados completos por ID (PASS/FAIL/ERROR/SKIP/NOT_RUN suman total), TCR y positivos nuevos. Ningún FAIL se vuelve PASS por renombrar la expectativa sin autoridad.
6. **Fuente legacy no universal:** S04-F01 cambió intérprete de `STRATEGIC_ENTRY_BUDGET_V1` entre el linaje y master. Congelar baseline efectivo por familia/configuración y demostrar igualdad o divergencia, no renombrar V1→Unclipped ni confundir constantes iguales con conducta igual.
7. **Runtime serving:** integrar lo que falte para ejecutar módulos/configuraciones mediante las costuras runtime reales y probarlas en entorno sin egress económico. `HISTORICAL_POLICY_ONLY` indica capacidad/autoridad pendiente; implementar y certificar el servicio correspondiente en coordinación con Runtime Pools, no borrar la guarda o sustituir MM. La habilitación productiva requiere GO Owner y no ocurre aquí.
8. **Fragilidad de agentes:** muchos workers GLM murieron por cuota/red; se llegó a declarar review GOD cuando corría GLM. La selección real MiniMax se valida antes del trabajo. WIP/harness de workers muertos se recupera, no se descarta ni se declara completado por existir archivos.

## 2. Autoridad y alcance de esta última sesión

**Autorizado ahora:** completar implementación/refactor mínimo C06 y su wiring runtime compartido; recuperar y sellar configuraciones ya existentes; tests/adversarial/replay; ejecutar cada configuración admitida en el último contrato físico NQ (~2–3 meses) tras sus gates; baseline antiguo comparable limitado a esa misma ventana; corregir divergencias y validar reglas de señales/cierres; publicar candidato y paquete para histórico posterior. El diseño no vuelve al Owner para elegir helpers ni recuperar valores ya sellados.

**Fuera de alcance:** ejecutar el histórico multianual completo, optimizar/buscar parámetros o nuevas estrategias, ampliar el universo cartesiano, migrar ramas ajenas no aceptadas, reescribir historia/evidencia, gastos/compras, trade LIVE, deploy productivo, cambiar reglas de prop, inicializar otro repo/vault, merge a master sin autorización específica vigente. Preparar la integración y reproducibilidad del candidato en esta misma sesión; no entregar otro prompt de desarrollo al Owner por un fix ordinario.

**G0–G5 siguen vigentes.** El mandato autoriza G2/G4 en la ventana sellada a quienes satisfagan prerequisitos; no autoriza fingirlos. G5 se deja como cola elegible, **no se ejecuta**. D05 funded-only se recupera de autoridad y no se salta; su ausencia no bloquea CHALLENGE ni el soporte funcional del tipo FUNDED. El umbral1/3 no es sinónimo de G4: preservar ambos requisitos sin mezclarlos. Rendimiento económico malo no es bug de software ni motivo para forzar señales.

La arquitectura objetivo sigue KISS/SOLID: un módulo por Strategy/MM como hoy, tipos/configuraciones Campaign reutilizables, un owner comercial y mismo motor SDK, sin DSL, otra plataforma de agentes, otro supervisor económico o segunda contabilidad.

## 3. Contrato de agentes — obligatorio antes de modificar código

- **Coordinador: GLM-5.3-Flash LOCAL, función submanager de entrega.** Puede leer/razonar, planificar, despachar, revisar diffs/receipts, resolver decisiones técnicas ordinarias, ejecutar comandos de integración ya existentes y mantener documentación. **No implementa producto, harnesses ni tests**, ni siquiera un arreglo de una línea: toda escritura de código la hace MiniMax.
- **Todos los workers de implementación, pruebas, migración y verificación: MiniMax M3.1 Flash**, con ID real resuelto del provider del host (p. ej. etiqueta esperada `MiniMax-M3.1-Flash`, no inventarla si difiere). No usar GLM, Luna o Sol como fallback silencioso; la instrucción Owner actual reemplaza el reparto anterior.
- Antes de trabajo: una tarea read-only mínima a un worker MiniMax y un recibo de finalización. Verificar provider/modelo efectivo en metadata del harness, no en lo que el modelo dice ser. No modificar el default del coordinador ni mostrar/copiar claves. Usar ZCode/cliente/provider existente y autorizado, no construir una plataforma para delegar.
- Si el mecanismo principal de subagentes está agotado, usar otro mecanismo LOCAL YA INSTALADO y autorizado que ejecute MiniMax (CLI/workflow existente), con ID/receipt y workspace separado. No repetir indefinidamente errores `exceed quota`. Si MiniMax no puede ejecutar por ninguna ruta existente: `BLOCKED_PROVIDER` con prueba y acción mínima Owner; no empezar a implementar con GLM.
- Un coordinador, una cola finita de tareas, un integrador de commits. Workers sin subdelegación recursiva ni autoridad de negocio; scope/Allowed Files/No tocar/expected tests/SHA/result claros. Context scout y code scout, si el bootstrap los requiere, también MiniMax y con sus skills, no otro manager.
- Paralelismo por archivos/owners disjuntos; worktree/TMPDIR/outputs únicos. Ningún `pkill` por patrón amplio ni background sin handle/timeout/exit receipt. Subagentes pueden correr en paralelo; motores de backtest respetan el techo global vigente (hasta6 incluidos baseline/oráculos) y RAM/PSI/swap medidos. La capacidad de modelos y la de motores son cuotas distintas.
- Un MiniMax fresco que no escribió los cambios críticos verifica corpus y paridad, idealmente uno por frente. Eso aporta independencia de autor/contexto/corpus y modelo respecto a la implementación GLM previa; no afirmar independencia de modelo entre implementador MiniMax y revisor MiniMax, ni llamarlo GOD si no lo es.

## 4. Datos y universo: cerrar antes de repartir motores

### 4.1 Universo exhaustivo sin expansión especulativa

Congelar un manifiesto de TODAS las Strategy/variante/MM/config existentes y aceptadas en el alcance del repo/catálogo del proyecto. Referencia inicial S04:89 ejecutables y15 aliases. Censar también módulos/configuraciones oficiales registrados en runtime/backtester que no aparezcan en esa tabla; ninguna exclusión silenciosa. Si hay deltas reales, nombrarlos y justificar procedencia; no importar por rutina toda la rama ClutiFX no aceptada ni crear combinaciones nuevas. Cientos de tipos futuros son capacidad de extensión, no una orden de correr un producto cartesiano hoy.

Una fila tiene identidad de señal, variante, MM/config/policy, etapa/perfil/RuleSet, dataset/corte, hashes source/target, compatibilidad runtime, materialización, ejecución y clasificación. Aliases apuntan a su canónico sólo con equivalencia demostrada. Un status MIGRATED requiere request nuevo válido y prueba ejecutable del camino real, no sólo un string de catálogo.

### 4.2 Último contrato y horizonte

Elegir antes del ranking el contrato físico trimestral NQ más reciente con cobertura efectiva suficiente: objetivo2–3 meses, mínimo vigente45 sesiones elegibles más warmup causal. Preferir el más reciente si cumple; de lo contrario usar el inmediatamente anterior suficiente y declarar fallback con fechas/datos exactos. NO asumir ticker por la fecha actual, no concatenar vencimientos para fabricar un trimestre ni escoger el periodo que dé más beneficio.

Sellar `WINDOW_MANIFEST`: contract_id, inicio/fin exclusivos, sesiones de mercado/exclusiones, source/data hashes, granularidad, zona/calendario/roll, warmup y prioridad de orden causal; evidenciar gaps. Trailing warmup anterior al corte puede leerse, nunca atribuir sus trades/KPI al periodo. Rollover G3 sólo canarios acotados autorizados, no histórico multianual encubierto.

Los presets pueden apuntar a HIST2023–2026. Crear identidad DERIVED_LAST_CONTRACT explícita para limitar ventana y reproducir estado comparable, sin editar el original ni usar1050 días por accidente. Ajustar sólo ventana/corpus/warmup y los IDs derivados necesarios; conservar señal, MM, stops, fees, calendario CloseSafety y reglas. Si se exige estado continuo de una campaña que empezó antes, ambas versiones reciben el mismo snapshot/checkpoint inicial verificable. Filtrar trades de un histórico sin reproducir su estado NO es comparación válida. Si falta snapshot, hacer old/new desde el mismo inicio declarado y nombrarlo como nueva comparación, no afirmar que es el recorte exacto de R03.

### 4.3 Prerequisitos y presupuesto

G0→G1→G2A/B/C→G3→G4 por identidad. Ejecutar primero smoke/actividad/ciclo y luego el trimestre según el runbook; G2C requiere un round-trip real conciliado en la ventana, no orden rechazada. Corregir un adaptador defectuoso si el gate no puede aceptar una identidad válida; NO fabricar receipts, reclasificar datos para saltarlo ni heredar el pase de otra variante. Reutilizar receipts vigentes y bit-idénticos después de verificar compatibilidad de build/semántica.

Este encargo autoriza el lote finito de último contrato del universo congelado; no pedir otra autorización genérica para correrlo. El número de intentos, coste/perfil y criterio de cohorte se recuperan de las fuentes. Decisiones realmente ausentes se registran por fila y sólo se escalan si cambian economía; el coordinador sigue con lo independiente. No terminar llamando a todo el lote BLOCKED_D01/D02 sin haber resuelto la ventana Owner y los datos existentes.

## 5. Paridad determinista — definición verificable de EXACTAMENTE IGUAL

No confundir el mismo paquete importado con la misma ejecución. Entregar tres pruebas separadas; ninguna reemplaza a las otras.

### P0 — determinismo nuevo→nuevo

Repetir la misma identidad semántica al menos dos veces, con procesos/attempts separados, mismos inputs y estado. Comparar toda la traza canónica de decisiones y negocio; invariancia ante orden irrelevante de mapas/despacho de jobs. Los IDs técnicos de proceso/attempt y metadata no determinista de observabilidad pueden diferir; el esquema de normalización es explícito, mínimo y probado, nunca elimina tiempos de negocio, orden causal, señales, precios o dinero.

### P1 — campaña anterior→campaña nueva, último contrato

Baseline por identidad = implementación/policy que realmente produjo su referencia sellada, no elegir automáticamente master actual ni un SHA por conveniencia. Master2baf y linajeS04 pueden interpretar V1 distinto: recuperar manifest/receipt/commit efectivos. Comparar dos binarios Go aislados con mismos módulos/config/policies/reglas/fees/slippage/calendario/cierre, corpus, market model, warmup y estado inicial. Un camino legacy monocuenta y un modelo OHLC nuevo de multi-asociación pueden representar experimentos distintos; usar el contrato legacy equivalente para el test de compatibilidad, no forzar resultados de modelos incompatibles.

Comparación por `SignalID`/identidad causal y operación: evaluaciones, señales, filtros/faltantes, decisiones de MM/AccountPolicy/Provider, órdenes/cancelaciones/rechazos, fills/timestamp/precio/cantidad/costes, stops/targets, cierres/PnL nominal, estados de cuenta, compras/pases/activaciones/retiros/caja. En variantes misma semántica: igualdad exacta de campos económicos y causalidad, no sólo mismo PnL agregado ni tolerancia elegida después.

Toda divergencia conserva primer evento distinto, estado previo, expected/actual y causa. Corregir adaptador nuevo si es regresión. Si el viejo violaba fuente/contrato, NO reproducir el bug: prueba contra la fuente, fixture rojo→verde, cambio versionado/identidad nueva y adjudicación explícita. Mientras se afirme compatibilidad, ese caso NO cuenta `LEGACY_PARITY_EXACT`; clasificarlo separadamente como cambio deliberado demostrado y no esconderlo con hash/tolerancia/renombre. Prohibido alterar estrategias para empatar ganancias o cambiar V1 a Unclipped sin identidad.

### P2 — runtime→backtest, replay exacto de operación

Usar los owners/adaptadores runtime reales en entorno no económico y el backtester con las MISMAS entradas canónicas: config/build/policies, snapshots de Strategy/MM/Operation/Provider/cuentas, mercado ordenado, readiness de indicadores, reloj/temporizadores, comandos/eventos de control, ACK/rechazos/fills/cancelaciones, fees y orden de aplicación. Capturar una traza/event tape reutilizable y reproducirla sin segunda lógica de negocio. Comparar intenciones y decisiones ANTES de aplicar las respuestas externas grabadas; después aplicar esos mismos hechos y comparar estado/PnL/cierre. Reinyectar el resultado final o forzar fills para ocultar decisiones diferentes NO es paridad.

Una operación capturada en runtime debe dar EXACTAMENTE la misma secuencia y resultado al replay con sus hechos observados. IDs de negocio y referencias causales se preservan o usan mapeo canónico biyectivo predefinido; no ignorar diferencias de orden/riesgo/qty/precio/SL/TP/PnL/time. Semillas aleatorias, versiones, tiempo monotónico/lógico y serialización deben estar fijados cuando afecten decisiones. Usar aritmética exacta y redondeo contractual común.

**Límite que no se puede falsear:** un backtest OHLC con fills simulados no predice los fills reales del broker a partir de velas. Para reproducir una operación runtime exacta se necesitan sus eventos/fills y estado. Si faltan, `MISSING_REPLAY_INPUT`, no PARITY_PASS por aproximación. Separar `DECISION_REPLAY_EXACT`, `FACT_REPLAY_EXACT` y `SIMULATED_EXECUTION_MODEL`; las dos primeras son el requisito de equivalencia y la tercera es el modelo de investigación, no promesa de precio real.

Recuperar grabaciones existentes autorizadas; si aún no hay operaciones LIVE, probar el mismo entrypoint runtime con hechos/ACK/fills de una sesión SIM/integración aislada, sin egress económico, y registrar `SOURCE=RUNTIME_SIM` (no atribuir LIVE observado). Esto prueba la capacidad de replay; una captura real posterior se podrá consumir sin nuevo desarrollo. No desbloquear guardas productivas para conseguir esa captura. P2 tiene pruebas de ejecución real de componentes, no dos llamadas a `riskgeommm.New` con el mismo input ni un stub de Strategy.

## 6. Estrategias reales y conformidad de reglas

Usar siempre el módulo Strategy real y MM real del catálogo por las factories de producción en las validaciones G1/G2/G4 y P1/P2. Retirar del camino de certificación cualquier override `platformproof`, señales pregrabadas en lugar de evaluar la Strategy o mocks de Provider/MM. Conservar esos fixtures sólo como pruebas técnicas negativas, sin contarlos como ejecución de FBC/MR/ORB.

Además de comparar resultados, comprobar teoría/configuración→predicado→decisión con trazas: mercado→barras→indicadores/readiness→detección→filtros→señal→sesión→cuenta/MM→Provider→orden→fill→protección→cierre. Muestreo predeclarado por límites/ramas, no por ganancia: entradas y NO entradas, long/short, cruce de sesión, warmup, stop/target y rollover. Revisar todos los eventos mediante invariantes y conservar ejemplos positivos/contraejemplos por familia/configuración. El oráculo no copia los expected del autor ni el mismo helper que se evalúa.

Cero señales/entradas/round-trips no termina como `COMPLETE0` sin explicación. Distinguir bug de readiness/filtro/sesión/MM de una Strategy válida pero rara; no fabricar operación ni relajar filtro para aprobar. Una Strategy perdedora puede ser técnicamente correcta; se etiqueta económicamente y no recibe elegibilidad para histórico que no ganó. Cada fila se evalúa o conserva un bloqueo real con primer eslabón y causa; no excluir62 perfiles para declarar 27/27 terminado.

## 7. Plan único de cierre por frentes MiniMax

El coordinador mantiene este plan/cola y acepta entregas por evidencia, no sólo commits. Son olas dentro de esta sesión, no nuevos shots que el Owner deba despachar.

| Frente | Trabajo y dependencias | Salida/prueba |
|---|---|---|
| A — inventario/datos/config | Lectura C06/retornos, provider preflight, catálogo entero, policies selladas faltantes, WINDOW_MANIFEST, baseline efectivo por identidad | Censo sin delta inexplicado; cada campo source→target con hash; ninguna policy inventada |
| B — implementación/migración | Resolver gaps C06/refund/CloseSafety/migrador genérico; consumos CLI; preservar99% reutilizable, evitar loaders por candidata; puede avanzar junto A con contratos sellados | Requests v2 para cada canónico, no prototipos específicos FBC/MR; pruebas por tipo/cuenta/composición |
| C — runtime/paridad | En coordinación con Runtime Pools, conectar capacidades SDK/runtime requeridas, snapshots/event tape/adaptador replay, P0/P2 | Runtime y backtest mismo owner real; no guarda borrada para ocultar capacidad ausente |
| D — corpus/compatibilidad | Baseline Go + nuevo, mapeos canónicos, P1 último contrato, reglas señales/cierres y per-op first divergence; después de A/B | Matriz comparada fila a fila, con análisis de divergencias verificable |
| E — adversarial/quality | MiniMax fresco no autor; repetir harnesses reales, fallos/refunds/caja/sesión/idempotencia; coverage y race en entorno autorizado | Evidencia independiente de autor, regresiones y exacto recuento del corpus |
| F — lote final/handoff | Tras freeze del código, ejecutar/reutilizar último contrato por todos los elegibles; resumen económico, paquete histórico y candidata | FINAL_SHA + manifests + gates + comandos reales sin programar nada después |

Un worker independiente revisa fixes de otro; los conflictos los resuelve otro worker MiniMax, no el coordinador editando a escondidas. Antes de correr el lote costoso integrar y hacer canario corto con un caso de cada costura crítica; luego congelar build. Si se corrige código tras el lote, invalidar/repetir sólo filas y gates afectados con prueba de impacto; no reutilizar evidencia de otro SHA sin compatibilidad demostrada ni reiniciar todo el histórico por rutina.

### 7.1 Cerrar C06 sin inventar economía

CHALLENGE/FUNDED/SIMULATION, rotación N, varias asociaciones/props y caixa4000 siguen el diseño. `AccountSlots` inventario concurrente y reemplazos, no límite de compras de por vida. MM por etapa/config explícitos; FUNDED aislada no demuestra compra financiada. Producir eventos para devoluciones explícitas confirmadas conserva cohorte y no autoriza refunds automáticos. Comparación legacy puede usar5000/ResearchCash sólo como identidad histórica; nunca llamar a eso SIMULATION4000 ni forzar ese cambio para que coincida el replay.

La migración es genérica por registros sellados. La candidata no debe estar hardcodeada en funciones de negocio, rutas absolutas del host ni selección fija del motor. References/rankings pueden vivir en configuración/manifests. Artefactos que falten se recuperan por rutas declaradas y checksums, no tests `Skip` que luego se cuentan PASS en el gate obligatorio.

### 7.2 Quality gates de esta sesión

Usar perfiles Go válidos, coverage de desarrollo nuevo según policy >=95% con denominador statement/diff explícito y caminos críticos completos; no promedios por función. Tests críticos con missing source fallan como gate, no SKIP silencioso. Normalizar/actualizar TCR sólo con autoridad semántica, preservando corpus previo y pruebas positivas que ahora deben pasar. 15+5 no suma21: publicar el inventario con todos los estados.

`-race` debe ejecutarse en toolchain/host efímero o existente compatible y autorizado por las policies del repositorio, sin mutar infra productiva ni instalar globalmente por iniciativa. Si falta autorización/capacidad real, se registra un bloqueo preciso y no `PASS`. No prohibir el trabajo técnico normal en un entorno de build ya aprobado para perpetuar un bloqueo de gcc. Clasificar deuda baseline por causa, aislar todos los fallos nuevos; mismos nombres de fallos no bastan.

Prueba Go-only completa prepare/admit/run/report/resume/reproduce/export del binario final, sin intérprete Python en el camino oficial. Un directorio que contiene scripts viejos en worktree baseline no es permiso de ejecutarlos en producto ni de reintroducir wrappers. Cancelación y presión de memoria se prueban, incluyendo K>1 simultáneo, sin loops descontrolados ni OOM.

## 8. Candidata, domingo y siguiente agente

Prioridad de validación: `LAB-SG-FBC-CH300-15M-R500`; contraste `LAB-SG-MR-09-R750`. Los números viejos (26→9, coste/pase666,67 frente a13→5,936) son descriptivos históricos, no se transfieren al corte nuevo ni prueban retiros. El último periodo y las reglas reales pueden cambiar la selección; no tunear ni escoger ventana retrospectivamente para favorecerla.

La entrega deja la candidata operativa en backtest nuevo con módulo real y la integración runtime correspondiente implementada/probada en entorno no económico. Para RGMM, completar el trabajo compartido de serving que falte con el owner Runtime Pools, reusar sus contratos y verificación de readiness; no aparcar automáticamente todo como "es HISTORICAL_ONLY" ni eliminar la guarda. No certificar LIVE sin el gate específico y GO Owner. Si hay writer/mandato runtime concurrente, coordinar la frontera y trabajar sólo en cambios propios compatibles.

**Domingo1/11/2026 es objetivo Owner, no permiso implícito para operar.** No cambiar caps/riesgo/SL para encajar una certificación y conservar la etiqueta de la estrategia vieja. No afirmar que terminar C06 implica que la cuenta/bridge/entitlement/feed ya son aptos; comprobar estado vigente del frente FIRST_LIVE_TRADE, sin competir con su manager. Preparar todo lo desarrollable y el paquete exacto para certificar esa identidad; bloqueo externo auténtico debe tener comprobante y acción mínima, no frase genérica.

El próximo agente ejecuta histórico completo, NO continúa desarrollando esta capacidad. Debe recibir binario/FINAL_SHA, catálogos/requests v2 completos, provenances, datasets/recursos/gates, resultados último contrato y lista EXACTA de IDs elegibles/inelegibles. Si cambia corpus de trimestre a historia, cada dataset tiene su hash/manifiesto y compatibilidad explícita, no hashes falsamente iguales. El script/comando de histórico se entrega validado/dry-run, sin lanzar el motor multianual aquí.

## 9. Artefactos de salida y criterios de cierre

Guardar evidencia de código/datasets fuera del vault en el workspace autorizado; el vault conserva refs/hashes y decisión. El manifest de evidencias puede agrupar nombres (no crear un documento por tarea). Mínimos derivados legibles por máquina:

- `catalog-status`: universo/aliases y por ID source/policies/request digest, runtime-binding, migración y estados. Contadores deduplicados; aclarar que dos candidatas de ruta separada pueden solaparse con las62 del censo.
- `window-and-baselines`: datos exactos, warmup/cutoff, baseline SHA/binary/config por fila, semántica antigua/nueva y razones.
- `parity-report`: P0/P1/P2 por identidad/operación, campos comparados, mapeo IDs, first divergence o hash de traza exacto; evidencia runtime SIM/LIVE explícita.
- `last-contract-results`: funnel, fills/cierres/PnL/costos, compras/pases/pérdidas/pendientes y recibos G0–G4/clasificación, no sólo ranking.
- `full-history-handoff`: build/dataset/queue/resources/commands validados; ELIGIBLE/BLOCKED/EXCLUDED_BY_ALIAS y causa. G5_READY no G5_EXECUTED.
- `candidate-runtime-handoff`: identidad exacta, señales/MM/risks/configs/serving, pruebas y límites; READY_FOR_CERTIFICATION no LIVE_EXECUTED.

Retorno canónico final NUEVO materializado por skill: `main/10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-FINAL-RETURN.md`. Enlazar los artefactos, no inventar sandbox links. Actualizar sólo este planner y los artefactos propios/SDD existentes; el reporte previo S04 permanece inmutable.

Estados separados: `DELIVERY=READY_FOR_OWNER_REVIEW|PARTIAL|BLOCKED`, `CATALOG_MIGRATION`, `P0_DETERMINISM`, `P1_LEGACY_PARITY`, `P2_RUNTIME_REPLAY`, `LAST_CONTRACT_VALIDATION`, `FULL_HISTORY_HANDOFF`, `CANDIDATE_RUNTIME_CERTIFICATION`, `MERGE`, `DEPLOY`, `LIVE`.

**READY exige**: todo el catálogo aceptado materializado sin omitidos; casos reales probados y todas las filas con evaluación/clasificación justificada en el periodo; paridad exacta en dominios de igualdad sin divergencias inexplicadas; cero fallos técnicos materiales del scope; C06 y Go-only completos; quality gates; comandos/manifests listos para histórico. Un resultado económico perdedor/rare honestamente clasificado no obliga a cambiar Strategy ni convierte en listo para G5. Bloqueos por missing config recuperable o capacidad no implementada son PARTIAL, no cierre pleno. Las diferencias intencionadas documentadas no se presentan como igualdad exacta. G5/LIVE siguen sin ejecutar.

No devolver otro prompt de implementación para un fix ordinario ni cerrar al terminar sólo W1. Corregir/retestear dentro de esta sesión hasta completar el backlog finito. Si una dependencia externa real impide el resultado, conservar entregables y nombrar la mínima intervención necesaria; no prometer terminar después ni inventar PASS por la fecha del domingo.

## 10. Arranque, permisos de persistencia y cierre

Orden de primera acción: bootstrap vigente + router/skills/scouts exigidos → leer este paquete y estado vigente → verificar modelos parent/worker MiniMax con una tarea real → reconciliar HEAD/WIP → sellar inventario/ventana/plan de owners → implementar y probar por las olas. Recuperar artefactos `c06-s02`, `c06-s03`, `c06-s03r1`, `c06-s04` por el workspace del host; no asumir que cambiar cuenta transportó sus archivos. Rutas absolutas antiguas son localizadores, nunca contrato portable.

GLM mantiene contexto limpio con retornos cortos por worker y manifests, sin volcar dumps/historial completo. Si un worker muere, inspeccionar su status/WIP/hashes antes de retomar por MiniMax; no dar su trabajo por integrado. Una prueba de capacidad fallida no dispara cuatro reintentos idénticos. Avisar inmediatamente bloqueos externos; seguir trabajo independiente en vez de detener toda la entrega.

Agents-OS master directo, HEAD reconciliado, sin ramas/PR/force; un writer documental principal, change_log y readback remoto. No convertir vault sin .git en repo nuevo: usar mecanismo de publicación vigente, sincronizar sólo deltas propios y preservar cambios concurrentes. Materializador/schema de notas para retornos nuevos. Journal privado según policy; no forzar publicación de memoria privada ni secretos. Registrar modelo/provider real por child y consumo sólo confirmado.

Echo: cambios en la rama de trabajo reconciliada, commits verificables y candidato final; no nuevo branch de producto por cada corrección salvo worktrees internos coordinados. Integración técnica y plan de merge listos, no autopromoción a master/release/producción sin autorización específica. No redistribuir credenciales ni alterar cuentas/infra LIVE para probar.

Los workers cargan `agents-os-agent-run-register` cuando aplica, `agents-os-session-feedback` y `agents-os-session-close`, y cierran sólo su encargo. Este mandato autoriza el cierre de la sesión local final cuando entregue su resultado verificable, no cerrar automáticamente al manager coordinador de la conversación ni el programa Echo Futures.

## Fuentes

Instrucción Owner30-10-2026: última iteración, GLM coordinador + implementadores MiniMax, todas las estrategias, determinismo runtime/backtest, comparación último contrato2–3 meses y handoff de histórico para otro agente; domingo1-11 prioridad real. Arquitectura [[EF-CAMPAIGN-MODES-DESIGN]] C06; contratos Runtime Pools/R6, retester y qualification runbook; retornos GO-S02/S03/S03R1/S04; source Echo en HEADa22970c8. Los hechos nuevos y resultados de esta sesión aún NO han sido ejecutados por el manager CLOUD.
