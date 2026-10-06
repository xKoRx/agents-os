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
updated: "2026-10-06"
---

# BTG-PLAN — Gerard real, bankroll y objetivos

## Propósito

Entregar un backtester funcional de extremo a extremo con la Strategy y GerardMM canónicos de Echo Futures, medir el resultado histórico de la configuración actual y después simular compras, pérdida de cuentas, hasta cuatro retiros por cuenta y reinversión para encontrar objetivos monetarios económicamente convenientes.

Mandato Owner recibido el 2026-10-05 (America/Santiago): máximo cinco shots; el primero usa un submanager persistente con los ciclos de diagnóstico/corrección necesarios; el segundo diseña el delta; los tres restantes son implementación, adversarial LOCAL independiente y corrección/certificación. El Primary Manager mantiene la dirección; no implementa producto ni cierra su sesión sin solicitud Owner.

## Contenido

### 1. Estado y autoridad

Origen de este paquete: rama documental docs/backtester-gerard-bankroll-five-shots-20261005 de xKoRx/agents-os, commit `a16f4bb25cfb6882146f437f5913302a191313c2`. El submanager LOCAL observó su merge ya existente `d67319f0878610c786b94aa2ad31e5e4503e7efa` y master `bb9fa98be22057e8468e83f72cb53fd147accc09`. La revisión automática había rechazado mover master directamente en Primary; BTG-S01 no ejecutó ese merge ni altera master. Evidencia y deltas nuevos en rama documental separada para revisión.

PROGRAM_STATE = IN_PROGRESS
BTG_S01 = BLOCKED_EXTERNAL — ORIGINAL_BYTES_TRANSFER_POLICY; NTMINUTE_INPUT_VERIFIED; NATIVE_DRIVER_REMEDIATION_AND_CLI_PREPARATION
BTG_S02_TO_S05 = NOT_STARTED
REAL_GERARD_RUN_THIS_SESSION = NOT_RUN
CAMPAIGN_RESULTS = NOT_AVAILABLE
DESIGN_FREEZE = NOT_STARTED
PROMOTION = SOURCE_ONLY

Refs consultados directamente en GitHub el 2026-10-06 UTC:

| Repositorio / rama | HEAD |
| --- | --- |
| xKoRx/agents-os / master | 7435fa519b54c3601fb5f8e8f440cb8f54ad3d1c |
| xKoRx/echo / master | 372af59a7b83604781346613da01e3d510ea1360 |
| xKoRx/echo / feature/backtester-v1-s04-remediation | cd451972b242c8933321e03001decd4b6d778c61 |
| xKoRx/echo / feature/d6-shot1-execution-vertical | d08a30ce9815f820fda7132e20dc42cc345eb8e8 |

BT-S00–S04 son ACCEPTED_INPUT para capacidades ya certificadas; no acreditan todavía el backtest histórico Gerard solicitado. D6 es CONTINUITY_REFERENCE y no depende de esta campaña. El simulador previo Prop Economics Experiment es REFERENCE_ONLY, nunca motor alternativo.

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

### 8. Próxima acción concreta

Delta Owner 2026-10-06: [[BTG-S01-OWNER-S2-BARS-AUTHORITY]] selecciona S2 actual + GerardMM, NQ Last 1m principal y SL-first ante SL/TP en la misma vela. Alias resuelto; inspección física y seam OHLC en curso. La validación tick posterior queda limitada a cobertura físicamente recuperada; no asumir un año completo. Continúa S01, sin S02 ni optimización.

Inventario BTG-S01 ejecutado LOCAL con especialistas ONE-SHOT TOP/NORMAL. Identidad S2 resuelta por Owner; configuración restante y acceso físico siguen pendientes. Inventario actualizado [[BTG-S01-NQ-1M-DATASET]] confirma AccessDenied en la fuente Windows sin bytes recuperados. [[BTG-S01-S2-1M-FORENSICS]] delimita el prerequisito SDK OHLC, implementado y remediado en `407e03dd`, con TOP fresh review SDK PASS; [PR producto borrador](https://github.com/xKoRx/echo/pull/2) contra S04. Ningún claim de histórico; BT2-F01..F03 siguen abiertos por falta de real rerun. Evidencia y mínima acción en [[BTG-S01-REAL-GERARD-RESULT]] y [[BTG-S01-IDENTITY-CONFIG]]. Submanager conserva continuidad; REAL_SMOKE/LONGITUDINAL/RERUN siguen NOT_RUN y S02 permanece NOT_STARTED.

Delta posterior Owner: autoriza fijar reglas consistentes para el fin funcional del backtester e iterarlas después. [[BTG-S01-FUNCTIONAL-BASELINE-PROFILE]] selecciona contexto/costes/MM uniformes explícitos; config física no se presenta como recuperada. Export existente C:\Temp\history con13files/endpoints legibles en [[BTG-S01-NT-CANDLES-ACQUISITION]], originals completos aún no transferidos porpolicySFTP. NTminute reader y driver nativo avanzan, sin fake quotes, sin S02 ni aceptación.

Los siguientes prompts se generan justo a tiempo desde el resultado aceptado del shot anterior.

## Fuentes

- Owner, conversación 2026-10-05: objetivo Gerard + bankroll + cuatro retiros + reinversión + cinco shots.
- Mandato adjunto “STAGE 2 — REAL GERARD HISTORICAL BACKTEST”.
- [[Echo Futures]]: cierre Backtester V1 y continuidad Stage 2/Stage 3.
- [[Echo Futures — BT-S04 Final Remediation and Certification]].
- [[Echo Futures — D4-B3 S1 Exact Strategy]].
- [[Echo Futures — D4-B2 Q13 Gerard Hardscalping MoneyManagement]].
- [[technical-project-manager]] y [[Echo + Echo Forge — Environment Contract]].
- [[BTG-S01-SUBMANAGER-PROMPT]]: primer despacho.
