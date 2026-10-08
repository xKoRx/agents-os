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
created: "2026-10-05"
updated: "2026-10-08"
---

# BTG-PLAN — Gerard real, bankroll y objetivos

## Propósito

Entregar un backtester funcional de extremo a extremo con la Strategy y GerardMM canónicos de Echo Futures, medir el resultado histórico de la configuración actual y después simular compras, pérdida de cuentas, hasta cuatro retiros por cuenta y reinversión para encontrar objetivos monetarios económicamente convenientes.

Mandato Owner recibido el 2026-10-05 (America/Santiago): máximo cinco shots; el primero usa un submanager persistente con los ciclos de diagnóstico/corrección necesarios; el segundo diseña el delta; los tres restantes son implementación, adversarial LOCAL independiente y corrección/certificación. El Primary Manager mantiene la dirección; no implementa producto ni cierra su sesión sin solicitud Owner.

## Contenido

### 1. Estado y autoridad

Este plan y los artefactos activos del programa viven en Agents-OS `master`; las ramas documentales históricas no son autoridad vigente. Cambios del control se publican por delta en `master`, con readback y preservación de cambios concurrentes.

PROGRAM_STATE = READY_FOR_PRIMARY_FINAL_REVIEW
BTG_S01 = BOUNDED_REAL_RUN_COMPLETE; FULL_COVERAGE_AND_OWNER_ACCEPTANCE_OPEN
BTG_S02 = DESIGN_PRESERVED_IN_BTG-S02-DESIGN
BTG_S03 = HISTORICAL_CANDIDATE_AUDITED_BY_S04; FINDINGS_REMEDIATED_BY_S05
BTG_S04 = READY_FOR_PRIMARY_REVIEW_WITH_FINDINGS
BTG_S05 = READY_FOR_PRIMARY_FINAL_REVIEW; SOFTWARE_INDEPENDENT_REVIEW_PASS; OWNER_ACCEPTANCE_PENDING
CAMPAIGN_RESULTS = FRESH_1AB_BASIC_AND_CAMPAIGN_COMPLETE; REPLAYS_EXACT; FINANCIAL_READBACK_PASS
DESIGN_FREEZE = S02_ARTIFACT_PRESERVED; SOURCE_1AB_FROZEN
PROMOTION = NOT_ACCEPTED


Corte vigente 2026-10-08: [[BTG-S05-REMEDIATION-AND-RESULTS]] contiene una matriz final de16 findings FIXED_WITH_REGRESSION_AND_RERUN, fuente1ab9a7b5 y ACK integral G. BASIC/CAMPAIGN y ambos replays completos, financieros conciliados; caja4640/3compras/2reemplazos/0cobros. INDEPENDENT_SOFTWARE_REVIEW=PASS; PRIMARY_FINAL_REVIEW=PENDING; GATE_ACCEPTED=false. Próxima acción única: Primary revisa el informe/bundle final y presenta aceptación al Owner. PROMOTION=NOT_ACCEPTED; no cierre Root/Primary ni certificación/acción física. Los estados y refs de cortes previos son históricos y no autoridad actual.

Refs históricas consultadas directamente en GitHub el 2026-10-06 UTC:

| Repositorio / rama | HEAD |
| --- | --- |
| xKoRx/agents-os / master | 7435fa519b54c3601fb5f8e8f440cb8f54ad3d1c |
| xKoRx/echo / master | 372af59a7b83604781346613da01e3d510ea1360 |
| xKoRx/echo / feature/backtester-v1-s04-remediation | cd451972b242c8933321e03001decd4b6d778c61 |
| xKoRx/echo / feature/d6-shot1-execution-vertical | d08a30ce9815f820fda7132e20dc42cc345eb8e8 |

Los artefactos previos son evidencia histórica, no certificación automática del candidato actual. El informe S04 reporta 16 findings materiales aún abiertos en S05; D6 es una referencia física separada y su certificado no se transfiere entre SHA. El simulador Prop Economics Experiment es REFERENCE_ONLY, nunca motor alternativo.

Este mandato amplía Stage 2 + Stage 3 en un único programa de cinco shots. Conserva la dependencia: primero demostrar el trading histórico real; después diseñar y construir campaña/optimización. Sustituye la antigua instrucción de dejar Stage 3 para un futuro mandato separado. No cambia contratos BT-S01/D4/D5/D6.

### 2. Requisitos Owner y decisiones pendientes

| Punto | Estado | Regla |
| --- | --- | --- |
| Strategy + MM | OWNER_REQUIRED | Usar identidad, source y configuración canónicos; baseline tal como están. |
| Bankroll inicial | UNIT_UNCONFIRMED | Owner escribió 5k. Hipótesis para explicar la aritmética: USD 5.000. |
| Costo medio de adquisición | UNIT_UNCONFIRMED | Owner escribió 120k y unas 41 cuentas. Hipótesis compatible: USD 120 por compra; también CLP 5.000.000 / CLP 120.000 sería compatible. Resolver antes de resultados económicos. |
| Capacidad inicial | ILLUSTRATIVE | 5.000 / 120 permite 41 compras y deja 80, sólo sin otros cargos ni reinversión; no es un máximo de cuentas de la campaña. |
| Reinversión | OWNER_REQUIRED | Retiros netos efectivamente cobrados aumentan la caja disponible. PnL de cuenta o cobros pendientes se muestran aparte. |
| Retiros por cuenta | OWNER_REQUIRED | Máximo cuatro. Propuesta operacional: retirar la cuenta de nuevas operaciones al completar cuatro retiros y clasificarla como salida exitosa. Precisar cierre/settlement/residual en Shot 2. |
| Concurrencia base | PRESERVE_PRIOR_OWNER_CONSTRAINT | Una cuenta operando a la vez, según instrucción Owner previa del 2026-09-29, salvo autoridad posterior. Las 41 compras posibles no significan 41 cuentas simultáneas. |
| Programa/prop y reglas | SOURCE_RESOLUTION_REQUIRED | Recuperar plan correspondiente y reglas completas vigentes; E2T de D6 no se impone automáticamente a la campaña. |
| Optimización | OWNER_REQUIRED | Buscar objetivos monetarios que maximicen ganancias de campaña; preservar señal técnica y comparar siempre contra baseline. |
| Otros parámetros económicos | DESIGN_REQUIRED | Fees, activación/renovación/reset, reparto, elegibilidad, límites de retiro, espera de cobro, política de compra y horizontes. No asumir gratis o instantáneo. |

Observación documental: S1_NY_ORB_30M_V1 está especificada para NQ y utiliza GerardMM, pero las fuentes leídas no establecen de forma suficiente que sea la identidad exacta solicitada como “Strategy Gerard”. Recuperar configuración/decisión vigente antes de asignarle ese alias. GerardMM tiene configuración Owner de EVALUATION días 1–2: SL USD 2.000 / TP USD 1.500. Las autoridades D4 dejan días posteriores y FUNDED dependientes de filas explícitas; la instalación actual debe inspeccionarse antes de afirmar que siguen faltando. Los seeds de scaling de research no son defaults autorizados.

No se solicita al Owner reconstruir datos/configuración que un agente LOCAL puede recuperar. Si tras inventario queda una decisión de producto genuinamente ausente, se presenta la pregunta concreta con la evidencia.

### 3. Los cinco shots

| Shot | Responsable / superficie | Resultado exigido |
| --- | --- | --- |
| BTG-S01 — Usar y reparar lo existente | TOP / LOCAL / SUBMANAGER persistente; delega especialistas ONE-SHOT NORMAL/TOP y CLOUD para razonamiento útil | Identidad/config exactas; dataset real; smoke y corrida longitudinal; first divergence → fix en superficie correcta → regresión → mismo histórico; baseline reproducible, métricas y gaps delimitados. |
| BTG-S02 — Diseño del delta económico | GOD o TOP / CLOUD / architect ONE-SHOT sobre evidencia S01 | SPEC acotada de campaña, lifecycle de hasta cuatro retiros, caja/reinversión, reglas/configuración faltantes, conjunto pequeño de objetivos, criterio de selección y validación temporal. |
| BTG-S03 — Implementación | TOP / LOCAL / implementation lead ONE-SHOT con especialistas acotados cuando convenga | Campaign runner y evaluación de objetivos sobre el mismo engine, exports/resultados utilizables, tests críticos y comandos reproducibles. |
| BTG-S04 — Adversarial independiente | TOP / LOCAL / verifier ONE-SHOT, contexto nuevo | Crear y ejecutar E2E/falsificación propios contra el commit exacto; evidencia reproducible de cada finding; no corregir producto mientras audita. |
| BTG-S05 — Corrección y certificación | TOP / LOCAL / remediation lead ONE-SHOT | Cerrar findings aceptados, conservar regresiones útiles, repetir baseline/campañas/comparación completa en commit final y entregar resultados para aceptación Owner. |

S01 es una sola etapa del presupuesto. El submanager conserva continuidad y repite delegaciones cuando la evidencia lo exige; no necesita un nuevo shot numerado ni autorización por cada error ordinario. Sus especialistas siguen siendo ONE-SHOT. S02 no comienza antes del gate técnico de S01. S05 absorbe correcciones ordinarias; no se planifica S06 ni se rebaja un gate para aparentar el cumplimiento del límite.

### 4. Gate S01

Debe existir una corrida longitudinal auténtica y reproducible con Strategy y GerardMM reales, dominio compartido, operaciones/fills/accounting y lifecycle demostrados. El primer slice debe tener warm-up suficiente y un caso histórico capaz de ejercitar la funcionalidad. Una ventana sin señales es un resultado legítimo, pero por sí sola no demuestra toda la cadena.

Conservar datos originales, provenance, manifest/digests, contratos físicos, calendario y rollover cuando corresponda. BBO real si lo requiere la fidelidad; con TRADE-only, usar sólo un modo explícito soportado y limitar sus claims. El stock físico y cobertura del histórico se verifican LOCAL; la existencia de un feed D6 no los demuestra.

Verificar errores solucionables hasta cierre con regresión y rerun real. Si el engine alcanza un límite de configuración no definida por producto, registrar ese límite sin inventar valores; el gate y alcance demostrado quedan explícitos. Una demostración acotada a evaluación no se reporta como funded/campaña completa.

La salida incluye un inventario de lo que falta para S02. Rentabilidad negativa no invalida un backtest correcto ni autoriza modificar la Strategy.

### 5. Campaña cronológica mínima

La campaña posee compras, fees, presupuesto, decisiones de asignación de cuentas y solicitudes/cobros de retiros. Cada cuenta opera con el Backtest Engine y el dominio ya certificados. Las transiciones y movimientos económicos de la cuenta deben regresar por los seams canónicos para que balances, drawdown, Provider y GerardMM vean sus efectos.

Propuesta de política base para fijar en S02: una cuenta en trading; comprar reemplazo al siguiente momento elegible si la caja permite todos los cargos exigibles, operar según etapas y reglas, cerrar por breach o retiro exitoso tras el cuarto payout. Las cuentas nuevas arrancan en la fecha causal de compra, con warm-up técnico permitido pero sin generar beneficios antes de existir. Las pendientes de cobro no habilitan reinversión anticipada.

Las pérdidas del saldo virtual queman la cuenta según su RuleSet; no se restan de nuevo del bankroll personal. El costo de compra y otros fees ya están cargados a caja. Retiros deben debitar la cuenta y abonar caja una sola vez en los momentos correspondientes.

Reconciliación del escenario sin aportes externos:

Bankroll final = bankroll inicial + retiros netos cobrados - compras - fees adicionales.

Profit neto de campaña = bankroll final - bankroll inicial.

El cierre de horizonte mantiene separados: cuentas fallidas; cuentas retiradas exitosamente; cuentas aún activas; etapas pasadas; retiros 0/1/2/3/4; cobros pendientes; balance/PnL no retirado. No inventar payout final ni convertir en pérdidas los desenlaces aún no observados. Caja insuficiente con cobros futuros pendientes no equivale automáticamente a ruina definitiva.

### 6. Búsqueda del sweet spot

Primero conservar baseline con su configuración y resultados exactos. S02 definirá un barrido pequeño de los objetivos económicos materiales, como objetivo monetario GerardMM por stage y umbral de retiro si aplica. El SL/capacidad actuales permanecen en el baseline; ampliar su búsqueda requiere explicitarlo como decisión de diseño. No optimizar simultáneamente todas las dimensiones por defecto.

Cada candidato debe volver a ejecutar la trayectoria de Strategy/MM/Provider y la campaña. Cambiar un objetivo puede cambiar tamaños, adds, stops, duración y capacidad; no alcanza con multiplicar el PnL de una lista vieja de trades.

Comparación a horizonte, histórico, costos y reglas comunes. Seleccionar candidatos con un tramo previo y evaluar en tramo posterior reservado; ninguna decisión puede usar datos futuros. Si faltan datos para una prueba fuera de muestra significativa, el resultado se etiqueta exploratorio. Mostrar sensibilidad de vecinos y, si la cobertura lo permite, varias fechas de inicio; cada escenario tiene su bankroll independiente y sus resultados no se suman como cuentas independientes.

Criterio principal propuesto: crecimiento neto de caja realizada de la campaña en el horizonte fijado. Mostrar junto al ganador consumo de cuentas, drawdown de caja, tiempo a primer retiro, agotamiento de capital y estabilidad por tramo. Empates favorecen configuración más simple y menor consumo de capital. No prometer rentabilidad ni un óptimo universal.

### 7. Adversarial y gate final

Ataques mínimos materiales: reinversión de PnL no cobrado; quinto retiro; doble payout/fee; compra sin fondos o antes de tiempo; cuenta nueva reutilizando el pasado; transición de etapa con contexto incompleto; retiro que modifica drawdown/buffer; pérdida virtual descontada dos veces; omisión de costos; fin de histórico con cuentas/cobros abiertos; contaminación entre candidatos; selección usando el tramo reservado.

Gate final: mismo comando/configuración/dataset produce el mismo resultado económico; caja conciliada evento a evento; todos los outcomes de cuenta tienen causa/fecha; baseline intacto y comparación de objetivos con holdout identificable; todos los findings materiales del programa cerrados con pruebas. La aceptación final del producto sigue con Owner.

Entregables: comando reproducible, configuración/manifest del escenario, tabla de cuentas y eventos económicos, curva temporal de bankroll, informe baseline versus objetivos y resultados completos exportables. No agregar UI, optimizador genérico, framework multi-prop o Monte Carlo para cumplir este alcance.

### 8. Despacho inicial del programa (histórico)

El plan inicial habilitó S01 para inventario, baseline histórico real y brechas. El baseline acotado existe; la cobertura integral y aceptación Owner siguen abiertas. El estado vigente y siguiente paso después de la revisión S04 están en §11.

### 9. Delta Owner 2026-10-06 — BTG-S03 (vigente)

BTG_S03 = S03_CORRECTED_CANDIDATE_FOR_PRIMARY_REVIEW (2026-10-07, devolución correctiva completada: R1–R5 cerrados con pruebas, [[BTG-S03-REMEDIATION]]; candidato previo del 2026-10-06 queda supersedido por esta devolución). (2026-10-06): implementación y corridas reales en [[BTG-S03-IMPLEMENTATION]] (producto codex/btg-s03-implementation @ c1c0e7d4; BASIC real byte-idéntico al golden S01 + reproduce IDENTICAL; CAMPAIGN real 3 compras/2 burns/0 cobros, caja 5000→4640 conciliada y replay byte-idéntico; sustitución Strategy/MM por seams probada). Siguiente paso único: S04 adversarial LOCAL independiente.

Mandato Owner registrado en [[BTG-S03-OWNER-MANDATE-20261006]]. Prioridad vigente: «No quiero una estrategia ganadora: quiero que el motor ejecute la estrategia como en real. Strategy y MM deben poder cambiar sin modificar el motor. KISS/YAGNI. No perder tiempo mejorando ROI». Objetivo S03 = engine correctness con Strategy/MM intercambiables sobre los mismos seams del runtime, ambos modos BASIC/CAMPAIGN ejecutados de verdad y candidato CANDIDATE_READY_FOR_PRIMARY_REVIEW para S04. ROI/rentabilidad queda fuera de alcance: F3 deja de exigir búsqueda de rentabilidad (configuración sigue, optimización NO); T30/holdout/ranking = SUPERSEDED_BY_OWNER_SCOPE (no PASS); T38 acotada a prueba focalizada de propagación de configuración. Resultado económico negativo es aceptable si la ejecución es correcta. Fecha límite Owner: 2026-10-07 America/Santiago; sin S06 ni nueva fase de diseño. Limpieza administrativa asociada: rama codex/btg-s02-design-cloud-20261006 retirada tras recuperar su feedback original a master.

### 10. Delta BTG-S04 GOD LOCAL — 2026-10-07 (vigente)

BTG_S04 = READY_FOR_PRIMARY_REVIEW_WITH_FINDINGS; informe único [[BTG-S04-GOD-ADVERSARIAL]]. Auditado correctivo codex/btg-s03-remediation@1bf45050780554c1135edc619bf01a8a4b04ba08, HEAD local/remoto confirmado. S04 ejecutó falsificadores nuevos, comparación real acotada con owners runtime, perfiles activos y determinismo de1/2/4procesos; tests preservados en commit local independiente d5b16049bbee7295063e88d8d8f7fa0a4bbe34fe. Candidato preservado, ningún cambio productivo ni LIVE/D6.

DOMAIN_PARITY = NOT_DEMONSTRATED completo / PASS_BOUND primer circuito NO_ADDS y CONFIGURED; protección tras ADD = FAIL. SIMEXECUTION_CORRECTNESS y OPTIMIZATION_EQUIVALENCE = FAIL. CAMPAIGN_ACCOUNTING y MODULE_SUBSTITUTION = FAIL parcial; cash ledger probado sin doble débito, contexto5m/H4 continuo, pero términos de segunda cuenta, checkpoint ON_DEMAND y agregados defectuosos. PERFORMANCE = MEASURED_WITH_FINDINGS (copia histórica dominante/retención); INDEPENDENT_RUN_CONCURRENCY = PASS_BOUND con beneficio1.84x/2.35x en2/4procesos y artifacts idénticos por RunID. MIXED = REQUIREMENT_NOT_IMPLEMENTED; DATA_COVERAGE = PARTIAL; PHYSICAL_RUNTIME_READINESS = NOT_DEMONSTRATED.

Dieciséis findings: protección insuficiente de7contratos con stops5/2; scheduler V2 consume futuro; skip pierde consumidor flat; clock/mark atrasados en fill; extremos revisitados; fases Open/Close invertidas; venue sella fills antes de drain; composición runtime y requirements sustitutos incompletos; términos heredados, reemplazo demorado23h50 y agregados vacíos; copia O(historial)/retención; MIXED y provenance. Las afirmaciones de cierre R1–R5 de sección9 son claims del implementador, no gates aceptados; esta evidencia supersede cualquier inferencia de aceptación. R1 rings reconstruidos es párrafo obsoleto, continuidad observable sí pasó en una stream.

BTG_S05 = REQUIRED_REPAIRS_AND_RERUNS. Único siguiente paso: reparar seguridad/protección, causalidad/venue y skip probado; factories/requirements y campaña; O(1) latestRevision/retención conforme consumidores; delta MIXED y provenance. Rerun falsificadores, ampliar paridad pendiente y después BASIC USD100000 continuo y CAMPAIGN caja USD5000/compra USD120/una cuenta/hasta4cobros efectivos, sin tuning ROI ni recorte de warmup/horizonte. No S06 ni aceptación por auditor. Corridas reales existentes readback verificadas, no fresh rerun S04: CAMPAIGN Oct29T22→Nov2T22Z son96h/4sesiones, no3días; V1 economía/records iguales con bytes distintos. Trece archivos no prueban3años continuos; gaps y límites D6 quedan explícitos en informe.

Cierre propio del auditor y tres workers completado con registro/feedback por delta. Primary y programa permanecen abiertos; ventana Owner sigue2026-10-07 America/Santiago, sin ocultar pendientes para cumplirla.

### 11. Delta Owner vigente BTG-S05 — 2026-10-07

`BTG_S05 = IN_PROGRESS`; `PRODUCT_NOT_CERTIFIED`; matriz S04-01…16 abierta hasta que el fix SHA, regresión, rerun independiente y rerun real aplicable tengan evidencia. El informe único [[BTG-S05-REMEDIATION-AND-RESULTS]] conserva la evidencia aislada de RED, límites, decisiones S05-DEC-01/02, delegaciones y orden de integración.

La reproducción inicial preservó S04 tests en el padre exacto del SHA auditado; los cuatro grupos aislados de red devolvieron el RED esperado. No se declara BASIC/CAMPAIGN final, no se acredita MIXED ni cobertura integral, y PHYSICAL_RUNTIME_READINESS queda NOT_DEMONSTRATED.

Siguiente acción: completar protección, luego causalidad/venue, skip, composición/campaña, costo/retención, MIXED/provenance, integración, corridas finales y revisión independiente fresca. No S06, no aceptación del propio worker, no despliegue.

### 12. Delta BTG-S05 — 2026-10-08, readback 00:48 Santiago

`BTG_S05 = IN_PROGRESS`; `PRODUCT_NOT_CERTIFIED`; el plazo Owner venció y el mandato continúa dentro de S05, sin recorte ni S06. Fresh G acepta C86fabc/Df285 sólo en los wrappers y ataques del snapshot compuesto `18d1d35c…f038b` (33 PASS nominales, exit0); la RED previa queda como historia de iteraciones rechazadas. El snapshot no revisó DEC13/14 posterior ni el producto final.

C/D registran focal10 PASS en ADD adverso/pyramiding, ForceClose y recuperación offline parcial; strict-revalidation S2 pasa siete casos y negativos, security público pasa tres probes. El check stale público previo pasa, pero la comparación diferencial sigue pendiente. Un negativo público separado (`public-reconciliation-negative-01.jsonl`, exit1), ejecutado con `testsupport.NewSession`, `sim.Adapter` real y sólo override del reporte, pasa wrong-account pero falla missing-position (net5/snapshot vacío) y stale-position (una hora), ambos con `ReadyNewRisk=true`; D tiene autorizado un fix acotado, aún OPEN/material y bloqueante del freeze. ForceClose coincide en comandos/estado/fills/cero hechos pendientes; `EvaluatedAt` se compara por mismo instante tipado con negativos. DEC13 aprueba mantener held sólo para new-risk ENTRY/ADD y dejar protección/EXIT inmediatos según Role; los Sends internos de Invoke se encolan antes de egress, sin hop VENUE artificial ni Apply síncrono de ACK/finality. Sigue pendiente el interleaving de dos comandos y un Send posterior. DEC14 libera hechos/fills auténticos recuperados y drena consecuencias antes de consultar venue y producir un único reporte actual; IDs evitan doble aplicación, sin nuevos journals/polling. Readiness es BACKTEST soportado, anchor `FIRST_ACCEPTED_ORDER` sólo con aceptación real y `OpenOrders` como set tipado ya vinculado. API `ExecutionReconciliation` sólo está en compilación; recorrido offline final pendiente. Las ampliaciones de C/D aún esperan revisión independiente G.

E mantiene 800/836 líneas añadidas (95.69%), CLI 239/261 (91.57%) aparte. NQZ3 DERIVED está verificado y hay descriptor preparado, aún no sellado. No se ejecutaron benchmarks ni corridas BASIC/CAMPAIGN; specs, SHA/build/binario y outputs finales siguen sin asignar. La matriz 16 findings permanece abierta. D6 canónico sigue `ENVIRONMENTAL_BLOCKED` en `d08a30ce`; el readback read-only actual comparó cero paths en común entre cuatro archivos tocados por D6 y 72 cambios del S05 working tree respecto de base S04. Esa comparación por nombre no reemplaza análisis semántico ni transfiere la certificación.

Próximo paso: cerrar la obligación Invoke→Send y el recorrido offline, revalidar con falsificadores y fresh G, congelar candidato limpio y sólo entonces autorizar benchmark/corridas en outputs únicos con inputs sellados. Ver [[BTG-S05-REMEDIATION-AND-RESULTS]] §12 y la cápsula externa `work/btg-s05-20261007/evidence/cost-modes/preparation-capsule-20261008.md`.

## Fuentes

- Owner, conversación 2026-10-05: objetivo Gerard + bankroll + cuatro retiros + reinversión + cinco shots.
- Mandato adjunto “STAGE 2 — REAL GERARD HISTORICAL BACKTEST”.
- [[Echo Futures]]: cierre Backtester V1 y continuidad Stage 2/Stage 3.
- [[Echo Futures — BT-S04 Final Remediation and Certification]].
- [[Echo Futures — D4-B3 S1 Exact Strategy]].
- [[Echo Futures — D4-B2 Q13 Gerard Hardscalping MoneyManagement]].
- [[technical-project-manager]] y [[Echo + Echo Forge — Environment Contract]].
- [[BTG-S01-SUBMANAGER-PROMPT]]: primer despacho.

### Corte vigente — BTG-S05 freeze4152 — 2026-10-08

`BTG_S05=IN_PROGRESS`; `PRODUCT_NOT_CERTIFIED`; 16 findings pendientes de aceptación final. Candidato4152ca7dd096851a29cb034c3a20bf4951e2e8aa limpio, build externo test/CLI embeddedVCS exacto/modified=false PASS. C25 autor119/119top326nominalPASS y cobertura global2426/2536=95,66246% no sustituyen revisión G `REVIEW_RUNNING`; V1 final: future-prefix y las cuatro variantes stop/take-profit LONG/SHORT PASS, todos exit0 sobre binario97f37249 congelado. Performance120 y BASIC/CAMPAIGN reales NOT_RUN. D6d08a30ce/doc38a4b196 sigue ENVIRONMENTAL_BLOCKED/no transferible; PositionSeal completo requerido, Ninja actual no lo acredita y new-risk sigue fail-closed. Luna NORMAL indisponible tras dos rechazos harness; escritor TOP Sol exclusivo con modelo ejecutado/costoUNKNOWN.

Próximo paso: cerrar el gate G del freeze4152 y adjudicar residuales (V1 ya completo), luego performance120 y corridas reales/provenance/replay completos. La evidencia final verificada permite clasificar las filas FIXED_WITH_REGRESSION_AND_RERUN o DISPROVED_WITH_EVIDENCE y preparar READY_FOR_PRIMARY_FINAL_REVIEW; aceptación Owner posterior y separada. El estado actual sigue sin READY. No READY ni cierre root/Primary. Estado detallado y refresh D6transitivo en [[BTG-S05-REMEDIATION-AND-RESULTS]], corte vigente; historial anterior conservado.
