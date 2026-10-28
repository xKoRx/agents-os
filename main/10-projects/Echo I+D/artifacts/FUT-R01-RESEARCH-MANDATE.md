---
type: prompt
schema_version: 1
status: active
area: "[[Trading]]"
target: "IA investigadora Cloud; roles A, B, C e integrador"
prompt_version: 2
inputs:
  - "Autoridades vigentes y decisiones Owner de FUT-R01"
  - "Cobertura NQ y baseline de código/recibos existentes"
  - "Fuentes primarias y reglas oficiales actuales de props"
outputs:
  - "Fichas de Strategy: setup, filtro, RR u objetivo y riesgo técnico"
  - "Mapa de familias, redundancias y brechas NQ"
  - "Comparación de MM por prop/etapa y economía de caja"
  - "Primer experimento recomendado y alternativa"
project: "[[Echo I+D — Futures]]"
aliases:
  - "FUT-R01 — Prompt maestro de investigación"
related:
  - "[[Echo — I+D de Estrategias]]"
  - "[[Echo I+D — Cobertura Futures]]"
  - "[[Echo I+D — Mapa de capacidades]]"
tags:
  - kind/prompt
  - area/trading
  - project/echo-rnd
created: "2026-10-27"
updated: "2026-10-28"
---

# FUT-R01 — Setups, filtros, riesgo/objetivo y cobertura

## Propósito

Investigar estrategias algorítmicas objetivas basadas en indicadores, partiendo de lo que Echo ya tiene. La ficha aceptada por el Owner tiene **setup, filtro y RR u objetivo–riesgo técnico**. **Strategy es una entidad; MM asociado a prop/etapa es otra.** Esta versión sustituye la descomposición extensa propuesta en v1 por decisión Owner del 2026-10-28.

**Estado: PREPARADO, sin Deep Research completo despachado.** Es un encargo de FUT-R01, no otro programa, skill, manager ni diseño de runtime. La evidencia y los gates mantienen sus autoridades existentes.

## Contrato de entrada

### Autoridad

Gestión: `xKoRx/agents-os`, branch `master`, vault `main/`. En sesión nueva, bootstrap desde `main/AGENTS.md` y `main/80-agents/agents-os/agents-os.md`; en sesión caliente, sólo deltas necesarios. Cargar `echo-futures-research-manager`.

Leer [[Echo I+D — Futures]], [[Echo I+D — Cobertura Futures]], [[Echo — I+D de Estrategias]], [[Echo I+D — Mapa de capacidades]] y [[30-resources/runbooks/echo-rnd-cycle-runbook]]. Para cualificación, conservar [[30-resources/agents/skills/echo-retester-master/SKILL]] y [[30-resources/runbooks/echo-futures-strategy-qualification-runbook]].

Si falta acceso, indicar la entrada exacta y trabajar sólo la parte independiente con fuentes disponibles. No fingir lectura, acceso al host ni pruebas. Los workers retornan al manager y no escriben simultáneamente en el vault.

### Decisiones y límites vigentes

- Capital inicial **USD 4.000 exclusivamente Futures**. Forex tiene **aproximadamente USD 2.000 separados**. No hay más aportes previstos. USD 5.000 está superseded; capital disponible no autoriza consumirlo completo ni comprar cuentas.
- Meta al 31-12-2026: cinco estrategias challenge y cinco funded produciendo retiros, al menos dos props simultáneas, operación fiable y escalable. Superposición 5+5 pendiente; fechas/metas no rebajan validaciones.
- Embudo ideal confirmado en su sentido general: pase 1/3, cobro en 1/3–1/2 de funded activadas y aspiración de al menos una cuenta que cobre por diez compradas. Son objetivos, no probabilidades estimadas ni garantías. Precisar horizonte, resets y activaciones cuando afecten la comparación.
- Primer retiro objetivo **USD 3.000**, con split 90% u 80%. Falta aclarar importe previo/posterior al split y verificar programa. No asumir que cualquier prop permite ese primer payout.
- NQ exclusivo. No abrir MNQ, otros instrumentos, datos intermarket ni microestructura sin el alcance y datos necesarios. El preflight histórico 1m no certifica capacidad física actual.
- Preferir props compatibles con automatización, idealmente sin consistencia; no hay proveedor/programa aprobado. Earn2Trade/GAU50 es histórico, nunca prueba de cuentas reales.
- Reutilizar TG/FBC/ORB/MR. ClutiFX queda histórico y no se reabre. Owner disponible ampliamente; eso no prueba throughput ni capacidad libre de Hefesto.
- Cloud investiga; Daedalus procesa fuentes locales cuando haga falta; Hefesto implementa/valida sólo mediante mandato técnico autorizado.

### Baseline reutilizable

La matriz enlaza código `xKoRx/echo@ae1b09bc10370806f7648f076c5fa0825c9efa4e` y recibos R03. FBC es dirección de primera vela cerrada; ORB es ruptura de rango; MR08 es recuperación local condicionada a tendencia H1; MR10 existía y ya está incorporada a cobertura. TG/filtros, timeframes y MM no se cuentan automáticamente como mecanismos independientes.

R03 conserva evidencia histórica simulada, aceptación REVIEW y confirmación temporal retrospectiva; no demuestra retiros ni OOS virgen. Consultar identidades/recibos concretos, completar brechas y evitar reruns de campañas válidas.

## Contrato de salida

| Entregable | Salida exigida |
|---|---|
| Fichas simples | Identidad y versión como encabezado; tres bloques: setup, filtro y objetivo–riesgo/RR. Referenciar evidencia y MM por separado. |
| Cobertura | Qué regla pertenece a qué mecanismo, posibles duplicidades, datos faltantes y brecha que merece estudiar. |
| Indicadores y métricas | Pocas opciones por función, justificación, regla de combinación y cómo demostrar aporte incremental. |
| Economía | Programas comparables por prop/etapa, costes, DD, restricciones, primer cobro y continuidad con bankroll USD 4.000. |
| Decisión | Un experimento recomendado y una alternativa, con refutador, coste, dependencia y autorización requerida. |

**Contrato ONE-SHOT:** pregunta = elegir siguiente investigación útil; autoridad = documentos anteriores; entradas = decisiones y baseline; entregables = tabla anterior; presupuesto propuesto = una entrega por módulo, una revisión y una corrección enfocada, sin gasto ni campañas; refutador = falta de aporte incremental, duplicidad, incompatibilidad o evidencia insuficiente; parada = decisión preparada o dependencia indispensable identificada; retorno = manager Futures/Owner.

Puede usar una IA secuencial o workers A/B/C acotados. No decidir por votación de modelos ni generar bibliografía sin impacto. Para props: criba inicial de hasta cuatro proveedores y dos programas concretos por proveedor; justificar cualquier ampliación. No es presupuesto de compra.

## Prompt

Investiga el módulo asignado. Usa reglas deterministas: indicadores, parámetros, timeframe y comparaciones explícitas. Nada de lectura subjetiva del gráfico.

### A — Ficha simple, indicadores y métricas

**La ficha Strategy es ésta:**

| Bloque | Qué especificar |
|---|---|
| Setup | Regla exacta de entrada long/short por indicadores/precio; incluye el evento o cruce que dispara la entrada y sus parámetros/timeframe. |
| Filtro | Regla booleana opcional que permite/bloquea el setup. Puede ser ninguno. |
| Objetivo y riesgo / RR | SL/TP o distancia de riesgo más RR, en ATR o unidades explícitas de precio del instrumento. Definir lo necesario para reproducirlos. |

La identidad/versionado acompaña la ficha. **MM permanece separado** y determina sizing/riesgo monetario y controles según prop/etapa y contratos vigentes. No trasladar a la ficha de Strategy la arquitectura de cuenta, ejecución, cartera o validación; esas evidencias se referencian desde sus superficies existentes. No modificar contratos ni diseñar otro framework.

1. Describir estrategias existentes con esta ficha. Cuando el objetivo/stop efectivo dependa del MM, declararlo y enlazarlo; no inventar una regla de Strategy ni reinterpretar resultados.
2. Investigar indicadores por función: dirección/tendencia, extensión/reversión, rango/ruptura y volatilidad para normalizar distancias. Para cada opción: qué mide, en qué setup podría servir, limitación y prueba de aporte. No existe selección aceptada de “mejores indicadores” por popularidad.
3. Combinar con hipótesis: baseline → añadir filtro → comparar → quitarlo para comprobar aporte. Registrar combinaciones probadas, coste en señales y estabilidad. No acumular filtros correlacionados sin evidencia incremental.
4. Comparar objetivos/riesgos y RR como experimentos identificados. Diferenciar RR planeado y payoff realizado; cambiar salida puede cambiar duración y secuencia. No multiplicar una curva histórica para simular otro RR.
5. Proponer métricas concretas que cambien decisiones: frecuencia/inactividad, distribución neta, drawdown/duración, sensibilidad, estabilidad temporal y economía de cuenta. Definir fórmula, denominador y datos necesarios. No convertir una métrica aislada en nuevo gate.

### B — Familias y cobertura NQ

1. Mapear las fichas TG/FBC/ORB/MR01–MR10 a la matriz existente. Separar mecanismo de indicador, horario, filtro, timeframe, RR y MM. Señalar duplicidad demostrada o sólo sospechada.
2. Investigar prioritariamente persistencia/continuación, reversión, rupturas fallidas y transiciones de sesión que puedan estudiarse con capacidades existentes. Una celda vacía no obliga a abrirla. Datos/eventos/flow/intermarket adicionales requieren evidencia y alcance.
3. Para cada hipótesis recomendada: mecanismo o regularidad empírica; fuente primaria; regla investigable; datos/ejecución necesarios; control; resultado que la refutaría; coste; contribución respecto a lo existente.
4. No declarar una familia superior para props sin economía y trayectoria compatibles. Un paper de otro activo/periodo no demuestra ventaja NQ. Conservar descartes de versión/perfil y no reabrir ClutiFX.
5. Proponer pocas preguntas; devolver un primer candidato y una alternativa de mecanismo distinto cuando exista justificación.

### C — MM por prop/etapa, caja y cartera

1. Identificar cada perfil por Provider/Program/tamaño/fase/plataforma/RuleSet/fecha. Fuentes oficiales actuales: automatización/API/origen de órdenes, transición a live, DD intradía/EOD, consistencia, noticias/horarios, contratos, costes, activación, payout, copy/multicuentas y elegibilidad pendiente. No mezclar fases ni programas.
2. Comparar la misma señal congelada con MM/perfiles distintos, conservando identidades. Riesgo técnico en ATR/precio no fija por sí solo dólares ni contratos. No ajustar señal para compensar MM sin nueva hipótesis.
3. Medir compra → pase → activación → cobro efectivo → repetición/supervivencia, con cohortes, horizonte y pendientes. Las tasas objetivo no se usan como estimaciones. Verificar la factibilidad del primer payout USD 3.000 y aclarar bruto/neto.
4. Ledger: USD 4.000 iniciales + cobros recibidos − costes externos − distribuciones Owner. Incluir compras/resets/renovación/activación/operación sin descontar dos veces costes ya incluidos en PnL. Funded nominal y beneficio no cobrado no son bankroll. No usar los USD 2.000 Forex como respaldo.
5. Preparar alternativas de reserva, pérdida máxima, desembolsos por etapas y parada para decisión Owner. No fijar porcentajes arbitrarios ni autorizar gasto. Evaluar caja hasta primer cobro y financiación del siguiente lote; “1 de 10” no asegura autosostenimiento.
6. Medir diversidad cuando existan datos: PnL normalizado alineado, solapamiento, pérdidas/drawdowns simultáneos, dirección/sesión/régimen y periodos sin trades. Dos props no hacen independientes señales NQ replicadas. No ejecutar simulaciones en este encargo.

### Integración y evidencia

Separar hechos, inferencias, propuestas y decisiones Owner. Reutilizar resultados válidos, registrar selección previa y citar URLs/secciones/fechas; declarar lectura sólo de abstract cuando corresponda. Mantener evidencia contraria. No inventar probabilidades, accesos, throughput o resultados.

Conservar G0–G5 exactamente en retester/runbook: trade propio reconciliado G2C y trimestre propio requerido G4 antes del histórico; rareza/funded/research no crean excepciones. G4 es filtro de cómputo, no prueba estadística ni payout. No llamar OOS virgen a datos que influyeron en selección ni resolver fills intrabar no observables con OHLCV 1m.

La salida final selecciona qué reutilizar y qué falta, un experimento recomendado y una alternativa con coste/refutador/dependencias. El roadmap final requiere decisiones económicas y capacidad real; este encargo no garantiza cumplir la meta de diciembre.

## Límites

**Recuperación Hefesto preparada, no despachada:** si falta evidencia física, el manager completa una lista acotada de IDs/rutas. El ejecutor autorizado realiza una pasada read-only por catálogo/configs/specs/builds/manifiestos/recibos/trazas existentes y capacidad compartida observable; devuelve referencias y desconocidos en su receipt canónico. No auditoría exhaustiva, tests, replay, jobs ni backtests nuevos. Si no vincula config/build/datos/receipt, declara evidencia insuficiente; la lectura no recertifica gates. Se detiene ante acceso ausente o necesidad de mutación fuera del encargo.

Sin compras, operaciones, implementación, modificación de runtime/Backtester/MM, nuevos instrumentos, reapertura de ClutiFX, nuevos gates, managers o skills. Un único WIP primario Futures; decisiones materiales al Owner. La documentación no cierra la sesión.

