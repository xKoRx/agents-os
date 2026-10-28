---
type: doc
schema_version: 1
status: active
area: "[[Trading]]"
project: "[[Echo I+D — Futures]]"
related:
  - "[[FUT-R01-INDICE]]"
  - "[[FUT-R01-RESEARCH-MANDATE]]"
  - "[[Echo I+D — Cobertura Futures]]"
aliases:
  - "RV-01 consolidado campañas prop NQ"
tags:
  - kind/doc
  - area/trading
  - project/echo-rnd
created: "2026-10-28"
updated: "2026-10-28"
---

# ECHO FUTURES — RV-01: revisión adversarial y consolidado

## Propósito

Determinar si los retornos DR-01–04 disponibles sustentan una decisión investigable coherente sobre campañas prop NQ con USD 4.000. Esta entrega incorpora una reparación focal documental; no ejecuta una quinta investigación general, código de producto, simulaciones, backtests, compras, operaciones, pruebas físicas ni contacto con terceros.

**Fecha de corte:** 28-10-2026, America/Santiago. **Corpus congelado:** `xKoRx/agents-os@aa7c33a890c3686676c944d8448fdafa68886a9f`. **Autoridad económica:** corrección Owner y cápsulas de [[FUT-R01-RESEARCH-MANDATE]] v4, leídas; la instrucción posterior del Owner autoriza reorganizar documentación, publicar este consolidado sobre `master`, dar feedback y cerrar esta sesión. Esa autorización documental no cambia gasto, operación, producto ni G0–G5.

## Contenido

## 1. Dictamen ejecutivo

**`NO_APTO_AUN` para considerar que los cuatro retornos sustentan de manera completa y coherente la elección de un experimento de campaña definido y reproducible.** Existe una pregunta de investigación válida y se puede preparar una especificación acotada. El bloqueo no es que falte demostrar rentabilidad ni readiness operativa antes de investigar: faltan entradas originales, una interfaz contractual consistente y un protocolo causal suficientemente definido. Esas carencias cambian qué se estudiaría, qué se contaría como cobro y qué significaría un resultado. La propuesta de §10 es una hipótesis para especificar, no un experimento ya cerrado por los cuatro DR.

La reparación de esta entrega corrige la aritmética, limita los teoremas, separa programas Rapid, resuelve contradicciones de retiro, rectifica atribuciones académicas y reemplaza criterios de validación ambiguos. **No recupera por invención el original DR-01, no completa el informe DR-02 faltante y no certifica una ruta de órdenes Echo.** Por eso el dictamen permanece `NO_APTO_AUN` después de la reparación.

La conclusión económica que sí queda en pie es condicional: una señal con expectativa por trade no positiva puede merecer investigación si la transformación contractual, los costes y el calendario producen una distribución de caja útil. La asimetría por sí sola no demuestra ese resultado. Resolver evaluaciones más rápido puede ayudar o acelerar el agotamiento; conservar cada cuenta indefinidamente tampoco es el objetivo por defecto.

**Salida propuesta al manager:** cerrar RV-01 como entrega documental, mantener la selección de campaña pendiente y preparar una sola ficha experimental de persistencia de cierre NQ. Su alternativa es una identidad existente de reversión, MR06, después de reconciliar su especificación y evidencia. Ninguna de las dos queda autorizada a ejecución por este informe.

### Independencia y alcance de la revisión

Esta sesión revisora recibió un snapshot anterior a su trabajo y no redactó los retornos que contiene. Los tres apoyos de revisión se repartieron matemática/caja, contratos y evidencia/validación; sus conclusiones fueron contrastadas con los documentos y fuentes decisivas. No se decidió por mayoría ni se cuentan como tres verificaciones independientes de un mismo hecho. La revisión no fue ciega: se leyeron también los controles de ingestión y se verificó si sus advertencias eran reproducibles.

**Clasificación de esta entrega: AUTORREVISIÓN ADVERSARIAL DOCUMENTAL.** Hay separación comprobable de esta ejecución respecto de los archivos recibidos, pero no independencia histórica de autoría acreditada: las notas de origen dicen que la identidad de los autores no está verificada. No se certifica revisión externa independiente ni diversidad de modelos. Los apoyos internos no subsanan esa limitación; las reparaciones redactadas aquí tampoco reciben una aprobación externa ficticia.

## 2. Inventario real de entradas

Se localizaron los artefactos por árbol del repositorio y sus referencias explícitas, y se leyó íntegramente el material seleccionado. La búsqueda de contenido de GitHub no recuperó coincidencias fiables incluso para nombres existentes; no se usó ese resultado vacío como prueba de inexistencia. La ausencia que se declara es en el corpus recuperado y en las referencias disponibles, no una afirmación sobre todos los chats o adjuntos históricos del Owner.

| ID | Entrada disponible | Integridad y fuentes | Estado para RV-01 |
|---|---|---|---|
| I0 | [Mandato v4 y corrección Owner](FUT-R01-RESEARCH-MANDATE.md) | Informe antecedente, corrección económica y cuatro cápsulas más RV-01 completos. Su encabezado de recepción quedó desactualizado respecto del planner. | Autoridad de alcance; su estado histórico no prueba que los DR no se hayan realizado. |
| I1 | [DR-01: captura estructurada](retornos/echo-futures-dr01-deep-research-2026-10-28.md) | 85 líneas. Declara ser captura editorial, no transcripción byte a byte de «Texto pegado(7).txt». Sólo preserva cuatro enlaces, sin lectura primaria certificada. | **Original completo ausente.** Se audita la captura, atribuyendo literalmente sus propias frases, no las del adjunto perdido. |
| I1c | [[Echo Futures — DR-01 matemática de campañas prop]] | Curación con ocho rectificaciones; tampoco sustituye el original. | Evidencia de lo que se advirtió al ingresar DR-01. |
| I2 | [DR-02 preservado](retornos/FUT-R01-DR-02-contratos-prop-NQ-2026-10-28.md) | 38 líneas: control de uso, resumen, matriz y cuatro notas. Marcado `PARCIAL`. Sin URLs oficiales reproducibles. | Se leyó todo lo preservado; **no acredita el retorno contractual completo requerido**. |
| I3 | [DR-03 preservado](retornos/FUT-R01-DR-03-mecanismos-NQ-2026-10-28.md) | 101 líneas. El archivo declara reproducir íntegro «Texto pegado(10).txt» después del control de ingestión. Bibliografía nominal, no registro completo de lectura. | Texto íntegro disponible según provenance; integridad respecto del adjunto externo no verificable por hash. |
| I4 | [DR-04 preservado](retornos/FUT-R01-DR-04-indicadores-reglas-validacion-NQ-2026-10-28.md) | 144 líneas, incluido control de ingestión; declara reproducir las 128 líneas del retorno «Texto pegado(9).txt». No contiene URLs primarias ni el diccionario completo que afirma entregar. | Texto íntegro disponible según provenance; integridad respecto del adjunto externo no verificable por hash. |
| I5 | [[Echo I+D — Futures]] y [[Echo I+D — Cobertura Futures]] | Planner y matriz vigentes en el snapshot. Inventario TG/FBC/ORB/MR y límites de antecedentes R03. | Contexto interno; no se inspeccionó otra vez código, datasets ni receipts físicos. |
| I6 | [[30-resources/runbooks/echo-futures-strategy-qualification-runbook]] | Autoridad de cualificación leída en las secciones pertinentes. | G0–G5 conservados; esta revisión no les asigna PASS. |
| I7 | PDF adjunto `ssrn-4824172.pdf`, versión 03-02-2025 | Se leyeron portada, datos, partes de método/gamma y Q13 con la tabla de futuros. No se declara lectura íntegra de todos los apéndices. | Fuente primaria focal para evitar tanto la transferencia SPY→NQ como el error opuesto de decir que el documento no incluye futuros. |

El índice [[FUT-R01-INDICE]] conserva ruta anterior, ruta nueva y blob Git de cada archivo movido. **Los originales disponibles se trasladan sin modificar su contenido.** Las advertencias nuevas viven en este consolidado y en sus enlaces de navegación.

## 3. Tabla de hallazgos

**BLOQUEANTE:** impide sustentar una parte indispensable de la decisión pedida. **MATERIAL:** puede cambiar la selección, signo económico, trayectoria o significado de la evidencia. **MENOR:** afecta trazabilidad o precisión sin determinar por sí solo el resultado. La severidad describe el problema en el insumo; la columna de reparación aclara qué quedó resuelto en RV-01 y qué permanece pendiente. Las líneas se refieren al snapshot de entrada, cuyos bytes se preservan.

| ID / severidad | Claim exacto disponible | Evidencia y diagnóstico | Impacto | Reparación mínima / disposición |
|---|---|---|---|---|
| H01 **BLOQUEANTE** | I1 L5: «captura editorial… no es transcripción byte a byte»; I2 L3: «DR-02 \| PARCIAL». | I1 L85 impide citar la captura como original exacto; I2 termina tras cuatro notas y no trae fuentes reproducibles. | No se puede afirmar revisión de cuatro retornos originales completos. | **Pendiente:** recuperar los originales existentes, si se conservan, o aceptar explícitamente un expediente nuevo limitado a lo disponible. No reconstruir ni reetiquetar resúmenes como originales. |
| H02 **BLOQUEANTE** | I2 L28: «MFFU Rapid 50K… Sim (balance 0, EOD trl)… 50% eval.»; L38: «2 días… 50%». | E2 y E3 distinguen Rapid estándar y Rapid EOD. El primero tiene funded intradía; el segundo otra combinación de consistencia/días/capacidad. | La fila describe un híbrido no demostrado. Cambian barreras, duración y sizing NQ. | **Reparado como diagnóstico:** separar programas; **pendiente** elegir uno y completar su vector por fase/cohorte. No basta renombrar el drawdown. |
| H03 **BLOQUEANTE** | I2 L28/L32: «ELEGIBLE… bots» / «bots OK»; plataformas «Tradovate (Rithmic)» y «TopstepX (Rithmic)». | No hay cadena documental origen de órdenes→software/bridge→plataforma→programa/fase. E5 demuestra que una API con bots permitidos puede restringir origen y live. Costes completos tampoco están presentes. | No existe todavía una interfaz contractual verificable para campaña algorítmica Echo. | **Pendiente:** una ruta primaria y una alternativa como máximo, con campos decisivos soportados o `UNKNOWN`; prueba física futura separada. No inferir que toda ruta esté prohibida. |
| H04 **BLOQUEANTE para usar el protocolo tal cual** | I4 L111: «asumimos fills al nivel extremo de la vela»; L116: «stop al máximo Favorable, target al mínimo Adverso». | No se define una trayectoria causal ni una cota demostrada. OHLC M1 no determina secuencia stop/target/HWM, quote, mark o fill. | Puede fabricar pases, pérdidas y retiros; llamarlo conservador no fija el sentido del sesgo de caja. | **Reparado conceptualmente** en §6: eventos identificables, escenarios explícitos o `DATA_REQUIRED`. **Pendiente:** evidencia de datos y motor para el experimento elegido. |
| H05 **MATERIAL** | I1 L47: «0,2×500 − 0,8×100 = +20» y split 50% «−30». | La propia captura y curación ya advierten que el fee se paga en todas las compras y que pase no equivale a pago. | El caso favorable pasa a 0; el segundo a −50, antes de otros costes, aun concediendo que 0,2 fuera probabilidad de cobro. | **Resuelto algebraicamente:** coste universal, `q` de dinero recibido y costes completos; no constituye estimación NQ. |
| H06 **MATERIAL** | I1 L15: «E_0 con USD 400»; L27: «tiempo… E_0(E_0 + T)». | Fee externo ≠ estado de cuenta. Para la notación justa ±1 usada, el tiempo es `E0×T`; con barreras −L,+T es `L×T` en unidades de paso. E1. | Desordena probabilidades y el argumento de velocidad. | **Resuelto:** separar caja/estado; fórmulas y supuestos en §4. No convertir duración en trades a calendario sin tasas de oportunidades y días contractuales. |
| H07 **MATERIAL** | I1 L29: «ruina casi segura eventualmente» e «invariancia de P_pass ante mayor sizing como generalización». | Dos barreras, abiertos al horizonte, saltos, costes, trailing y lotes enteros cambian el problema. Media histórica no positiva no acredita supermartingala condicional. | Un teorema restringido se vuelve descarte o garantía universal. | **Resuelto como límite:** §4 conserva las condiciones y un contraejemplo de overshoot; falta cualquier estimación NQ. |
| H08 **MATERIAL** | I1 L53: pasar «podría elevar la probabilidad de éxito funded». | Selección de una racha pasada no produce ventaja predictiva con futuros IID y mismo estado inicial. | Sobrevalora pase→funded→cobro si se toma como mejora demostrada. | **Resuelto:** condicionar al pase, activación, estado, calendario y política; exigir evidencia para persistencia. No iniciar funded al azar y llamar a eso conversión de campaña. |
| H09 **MATERIAL** | I4 L86: «Retiro neto esperado: media de retiro tras pagar cuotas»; L91: financiar intento como «función… de PnL neto». | No distingue cobrado/solicitado/SIM ni define calendario y denominadores completos. No hay resultados ejecutados que prueben doble descuento efectivo. | Puede inflar caja, ocultar pendientes o restar costes dos veces. | **Resuelto como diccionario mínimo** en §5; mantener pendientes y conciliación de cada coste. No atribuir errores contables ejecutados que no se observaron. |
| H10 **MATERIAL** | I2 L32: LucidFlex «máx $2.000… Bruto ≈6.667 → +$3.000 neto (90%)». | E4 confirma cap por solicitud y split. Con esa regla, el máximo tras split es USD 1.800 antes de otros cargos. | USD 3.000 en un primer pago único es incompatible con la fila, aunque crezca el beneficio. | **Resuelto:** separar solicitud bruta, recibido y acumulado de varios pagos; este último requiere otros ciclos. |
| H11 **MATERIAL** | I2 L30: Topstep «Request hasta 50%… Bruto ≈3.333 → +$3.000 neto». | Contradicción interna: 3.333×50%×90%≈1.500. El umbral continuo sería 3.000/(0,5×0,9)=6.666,666…; redondeos y otros límites siguen pendientes. | Subestima el beneficio requerido. | **Resuelto algebraicamente**, sin certificar la fila contractual Topstep. Usar la función de retiro completa, no sólo dividir por split. |
| H12 **MATERIAL** | I2 L28: «permite bots y news»; L32: «no en funded» bajo consistencia. | E2/E3 distinguen T1 news entre evaluación/funded; E4 añade días rentables por ciclo de payout. Ausencia de consistencia no elimina requisitos de cobro. | Una política admisible al pasar puede no servir para cobrar; tiempo mínimo y supervivencia contractual cambian. | **Reparado documentalmente:** permisos y contadores por fase/ciclo. No imponer conservación indefinida ni prohibir todo riesgo alto. |
| H13 **MATERIAL** | I2 L35: «Precio eval: costo único… OneUp… doble de 25K… LucidFlex… fuente no oficial». | Precios extrapolados y costes/renovaciones incompletos; faltan adquisiciones fallidas, activación y cargos externos verificables. | No contrasta USD 400/funded ni capacidad de financiar una campaña de USD 4.000. | **Pendiente:** desembolsos por evento y cohorte. USD 400 conserva categoría de referencia Owner. No sustituir desconocidos por promociones o cero. |
| H14 **MATERIAL** | I3 L17: «últimos 30’ predice… resto del día»; L43: «o viceversa»; L83: primera hora→última hora. | E7 confirma la dirección resto del día→últimos 30 minutos. El experimento propuesto cambia ventanas y no replica esa regla. | Una lectura literal puede filtrar futuro; una adaptación no hereda resultados ajenos. | **Resuelto:** cronología causal; toda adaptación se identifica como hipótesis propia. No se certifican cifras específicas NQ de una tabla no leída. |
| H15 **MATERIAL** | I3 L25: «evidencia… acciones suecas… la lógica se traslada (HECHO)». | E8 describe crudo y umbral respecto de apertura, no evidencia NQ de la receta 15m con filtros añadidos. | Confunde activo y regla; infla respaldo del ORB adaptativo. | **Resuelto:** evidencia externa y transferencia hipotética separadas. La publicación final es 2013, con antecedente/online 2012. |
| H16 **MATERIAL** | I3 L27: «alto decay post-publicación»; L44: dealers «están net short gamma»; L47: «Observabilidad: 100% en OHLCV». | E9 acota una señal específica; no identifica causalidad de publicación. OHLCV no mide inventario gamma ni ejecución. E10 incluye futuros Nasdaq, pero no demuestra caja prop. | Narrativa convertida en observación y contraevidencia extendida a toda una familia. | **Resuelto como alcance:** regularidad de precios ≠ mecanismo medido ≠ beneficio prop. Mantener lectura parcial explícita y no descartar evidencia pertinente por no ser el titular del paper. |
| H17 **MATERIAL** | I3 L70/L80: «No cubierta…» / «Cubre hueco»; L60: independencia «con correlación baja». | I5 ya enumera MR04, MR06 y MR09; el worker sólo recibió reglas parciales. Baja correlación no prueba independencia de colas, sequías y desembolsos. | Puede duplicar investigaciones y contar variantes/MM/firmas como estrategias distintas. | **Pendiente acotado:** reconciliar candidato con inventario existente. No imputar al worker datos privados no suministrados; retirar certeza sobre huecos. |
| H18 **MATERIAL** | I3 L78: «retornos adversos… más de 50% (fail)… se descarta utilidad»; L83: «Hipótesis nula: Sharpe≠0 o tasa≠50%». | Criterios incompatibles con campaña/caja y contraste de ausencia mal formulado. | Descarta por acierto/expectativa de trade lo que el mandato exige valorar por campaña. | **Resuelto:** refutación de una hipótesis de precio específica y refutación económica se informan por separado; no hay umbral universal WR/PF/Sharpe. |
| H19 **MATERIAL** | I4 L47: «0.5×ATR… 0.5 pts» y «1×ATR (0.25 pts)»; L22: sigma logarítmica en «puntos NQ»; L98: «0.5 NQ». | Un mismo ATR no produce esos valores; retorno logarítmico es adimensional; contrato no es presupuesto de riesgo. Quedan `x`, umbrales y reentradas sin cerrar. | Fichas no deterministas ni implementables tal como están. | **Resuelto como criterio:** una ficha con unidades/predicados completos, contratos enteros y veto si no cabe 1 NQ. No sustituir MNQ ni ajustar stop para forzar admisión. |
| H20 **MATERIAL** | I4 L132: variar sólo MM mediante «apalancamiento 2x, stops más amplios». | Ampliar stop cambia geometría, salidas y duración Strategy. | Confunde efecto MM con otra estrategia y favorece reutilización inválida de trayectorias. | **Resuelto:** comparación MM congela geometría; cualquier cambio de stop/target es otro trial/versionado. Más riesgo no garantiza una pérdida acotada al stop. |
| H21 **MATERIAL** | I4 L94: «definimos fórmula, denominador y umbral»; L106/L134: CV «aleatorio de parámetros» y permutar «para calibrar PBO». | No está el protocolo concreto ni inventario de intentos/datos ya usados. No se ejecutaron pruebas, por lo que no se demuestra leakage efectivo. | Permite selección retrospectiva y falsa confirmación virgen. | **Pendiente acotado:** preregistro de un diseño, historial de ensayos y cortes por tiempo; §6. R03 permanece confirmación temporal retrospectiva. |
| H22 **MENOR** | I1 L19: «~2 años hasta fin de 2026». | Recepción 28-10-2026 y meta 31-12-2026. | Calendario incoherente si se usa para contar intentos. | **Resuelto:** fijar fecha de arranque y corte; no estimar sesiones ni ciclos a partir de dos años ficticios. |
| H23 **MENOR** | I2 L9: Rapid se presenta luego «sin buffer». | Esa segunda frase no se reproduce en las 38 líneas disponibles; la fila Rapid sí indica 2.100. | Un aviso de ingestión no prueba una contradicción ausente. | **Resuelto:** no usar ese claim como hallazgo contractual confirmado. Conservar la incertidumbre del original. |
| H24 **MENOR** | I4 L73: «PF>2 estilo institucional»; L134: «siguiente paso (DR-05)»; I0 L37: otros DR «NO EJECUTADOS». | Umbral sin fuente universal, extensión no mandatada y estado de recepción obsoleto frente al planner. | Puede añadir un gate doctrinal, investigación indefinida o duplicar DR ya realizados. | **Resuelto:** retirar autoridad del umbral/DR-05; índice y planner actualizados. El mandato movido se preserva como documento histórico, sin reescribirlo. |

## 4. Reparación focal de matemática y causalidad

### Barreras: caso que sí sostiene las fórmulas

En el paseo justo de pasos ±1, empezando en PnL 0, con barreras fijas −L y +T, L y T enteros positivos, sin overshoot y detención en la primera barrera, se obtiene `P(pase)=L/(L+T)` y `E[τ]=L×T` pasos. En coordenadas 0→a con inicio x: `P=x/a`, `E[τ]=x(a−x)`. E1 respalda esas identidades y explicita condiciones de parada. No es un modelo empírico NQ.

La extensión adversarial necesita `E[ΔX_(n+1) | F_n]≤0`, integrabilidad y una política causal. Una media muestral o marginal de trades no positiva no demuestra esa condición. Si la parada es válida, la absorción ocurre y los únicos terminales son −L y +T, `E[X_τ]=pT−(1−p)L≤0` implica `p≤L/(L+T)`. Con horizonte finito debe conservarse el término de posiciones/cuentas abiertas: `E[X_(τ∧H)]=T·P(pase≤H)−L·P(pérdida≤H)+E[X_H·1{τ>H}]`. No reemplazar probabilidad eventual por cobro antes de una fecha.

Estas identidades restringen el proceso de PnL bajo sus supuestos; no son una prueba de que la caja externa prop tenga la misma esperanza. El desembolso de compra, la activación, el split, los caps y la posibilidad/fecha de cobro conforman otra función económica.

**Contraejemplo analítico, no simulación ni regla comercial:** barreras −1,+2. Con pasos justos ±1, la probabilidad de pase es 1/3. Con pasos justos ±2, el primer paso termina la etapa: pase con 1/2 y pérdida −2 con 1/2. El overshoot altera la probabilidad aun con media cero. Por tanto, más sizing no cambia únicamente el tiempo. Este ejemplo no recomienda saltar límites ni estima NQ.

### Trailing, enforcement y discretización

Para cada fase deben distinguirse al menos el estado usado —balance realizado, equity, mark y costes—, cuándo actualiza el máximo/suelo, cuándo controla una infracción, condición `toca`/`cruza`, lock, liquidación y tratamiento de órdenes pendientes. **EOD describe una frecuencia de actualización; no demuestra por sí solo que una infracción sólo se controle al cierre.** El parámetro de enforcement no queda certificado por decir EOD.

El trailing intradía depende de la trayectoria de máximos y retrocesos. No puede reemplazarse por una barrera fija ni observarse sólo con equity a cierre de trade. El sizing entero NQ, los saltos, fills y costes también producen discontinuidades: una política de 1% y otra de 2% pueden terminar en la misma cantidad de contratos o en vetos diferentes. La pérdida presupuestada por stop no es una garantía frente a overshoot.

### Pase y fase funded

La funded debe provenir de los pases de la misma campaña, con su estado, activación, calendario y política. Una funded inicializada artificialmente sirve sólo como ensayo condicional declarado; no estima conversión desde compras. Con futuros IID e igual estado inicial, haber pasado por una racha favorable no mejora por sí solo las próximas probabilidades. Con regímenes o dependencia podría cambiar la distribución, pero eso se demuestra con datos y no por selección narrativa.

La comparación de políticas debe separar velocidad, probabilidad de pase, probabilidad de cobro condicionado, importe, duración y necesidad de compras futuras. El óptimo de resolver una evaluación no tiene por qué optimizar caja de campaña. Tampoco hay un mandato de salvar cada funded: se modela únicamente la supervivencia que el contrato y el objetivo elegido exijan.

## 5. Reparación focal de caja, retiros y cohortes

La identidad contable adoptada es:

`B(t) = USD 4.000 + Σ pagos netos efectivamente recibidos hasta t − Σ desembolsos externos hasta t`.

`B(t)` no incluye saldo SIM, beneficio contractual, payout elegible, solicitado ni aprobado pendiente. Cada uno conserva su estado y fecha. Las obligaciones ya comprometidas deben informarse aparte para determinar caja libre y financiación del siguiente intento; no se borran por no haberse cargado todavía.

Los desembolsos externos incluyen compra, reset, renovación, activación, datos/API/plataforma y cargos de cobro que efectivamente correspondan. Cada concepto debe marcarse como pagado externamente o descontado dentro del PnL/payout. Las comisiones y el slippage que ya redujeron el PnL contractual no se restan por segunda vez de caja. Si en live algún cargo se paga externamente, se registra conforme a su tratamiento real. «Neto del split» todavía puede diferir del dinero recibido después de otros cargos.

### Denominadores y horizonte

| Métrica | Definición mínima | Tratamiento de pendientes / límite |
|---|---|---|
| Compras e intentos | ID de compra y relación con resets/renovaciones; toda salida de caja registrada. Reportar ambos contadores si reset no equivale a compra nueva. | No redefinir retrospectivamente el denominador Owner de evaluaciones compradas. |
| Pase a H | Compras de la cohorte que lograron pase antes de H / todas las compras de esa cohorte. | Separar pérdidas, pendientes, canceladas y censura; abierto no se declara pérdida ni éxito. |
| Activación | Funded activadas / todos los pases de la misma cohorte y corte. | Desglosar elegibles, no elegibles y pendientes; una tasa sólo sobre elegibles debe llevar otro nombre. Pendiente de activar no es funded operativa. |
| Primer cobro a H | Cuentas con dinero recibido antes de H / evaluaciones compradas; además la tasa condicionada a activación. | Solicitudes y aprobaciones pendientes quedan visibles. |
| Adquisición por funded | Costes de adquisición agregados / funded activadas, con desglose por concepto y cohorte. | Si no hay activadas, no producir un coste cero; cociente no definido. Informar cohortes abiertas. |
| Coste por pagadora | Costes completos agregados pertinentes / cuentas que recibieron dinero. | No usar sólo la trayectoria ganadora ni ocultar costes de fallidas. |
| Caja y financiación | `B(H)`, mínimo de caja libre, déficit respecto del inicio, obligaciones y posibilidad de costear la siguiente acción admitida. | Tener EV positivo no garantiza liquidez antes del cobro. |
| Calendario | Tiempo desde compra a pase/activación/solicitud/recepción; ciclos posteriores y censura. | No medir sólo ganadoras resueltas ni extrapolar dos años al cierre de 2026. |
| Dependencia | Pérdidas y sequías simultáneas, exposición común, compras/retiros coincidentes y estados de régimen. | Variantes, MM y firmas no son repeticiones independientes por nombre. |

El embudo `q=P(pase)×P(activación|pase)×P(cobro|activación)` es una identidad si eventos, cohorte y horizonte son compatibles y anidados. No requiere independencia. Las aspiraciones 1/3 y 1/3–1/2 no estiman sus factores; 1/10 sigue referido a evaluaciones compradas. `F/p_pass` sólo describe un modelo geométrico IID de fee fijo, sin límites, ni costes omitidos; no reemplaza la contabilidad de una campaña finita.

Para un primer cobro, `E[ΔB(H)]=P(recibido≤H)×E[importe recibido | recibido≤H]−E[costes externos≤H]`. Es una identidad, no una estimación. La expectativa de número de cobros puede sumarse sin independencia; la probabilidad de al menos uno y el riesgo de agotamiento no pueden calcularse con la fórmula IID por conveniencia.

### Payout: separar tres preguntas

1. **Solicitar USD 3.000 antes del split.** Al 90% serían USD 2.700 y al 80% USD 2.400 antes de otros cargos, siempre que el contrato admita la solicitud.
2. **Recibir USD 3.000 después del split.** El umbral continuo del importe sujeto al split es 3.000/0,9=USD 3.333,333… o 3.000/0,8=USD 3.750, respectivamente. A centavos, sin asumir un redondeo favorable, el primero requiere USD 3.333,34. Eso todavía no determina el beneficio de cuenta necesario si hay porcentaje retirable, cap, buffer, cargos o incrementos mínimos de solicitud.
3. **Acumular USD 3.000 en varios pagos.** Es otro objetivo, con nuevos ciclos y tiempo/exposición entre ellos; no puede usarse para decir que se alcanzó el primer retiro único.

En LucidFlex 50K, el cap documentado de solicitud USD 2.000 y split 90% limita un pago a USD 1.800 antes de cargos. La fórmula de la fila Topstep que combina 50% retirable con 90% de split requiere, por su propia aritmética, el doble del beneficio allí escrito. Estas correcciones no necesitan un backtest. Para Rapid, el documento observado habla de buffer; su semántica exacta de retención y saldo posterior debe fijarse antes de adoptar la cifra de USD 5.433 del retorno.

## 6. Reparación focal de evidencia y validación

### Qué sostiene la literatura leída

**E7 — Baltussen:** el predictor es el retorno hasta antes de la última media hora y el resultado se mide después. La página editorial aporta introducción y conclusión, no sólo abstract. No se recuperó para esta revisión la tabla completa NQ; no se certifican su fecha de inicio, coeficientes, Sharpe o coste específico. Primera hora→última hora, entrada al mediodía y stops VWAP son hipótesis adaptadas, no la misma regla.

**E8 — Holmberg:** los pasajes primarios recuperados permiten corregir activo y definición de ORB. No se leyó todo el PDF. Una ruptura del rango de 15 minutos con filtro de volumen/volatilidad no hereda resultados de umbrales porcentuales desde apertura en crudo.

**E9 — Rosa:** se leyeron abstract y disponibilidad de datos. La contraevidencia se refiere a overnight→última media hora; no prueba que todo momentum intradía sea inútil ni que la publicación causara la pérdida de predictibilidad. Un régimen estimado ex post tampoco puede entrar como filtro disponible en tiempo real sin su definición causal.

**E10 — Zarattini, Aziz y Barbon:** el resultado titular de 1.985%/Sharpe 1,33 pertenece al estudio SPY. El adjunto sí contiene Q13 y una tabla de futuros con fila Nasdaq; por eso sería falso clasificarlo como documento sin evidencia de futuros. Ese apéndice es un resultado reportado por autores: no demuestra aquí contrato físico, roll, costes, implementación NQ, admisibilidad prop ni cash. No se transfieren sus cifras a las recetas DR-03/04 ni se usan como probabilidades Owner.

### Matriz mínima de observabilidad

| Objeto | Qué puede sostener OHLCV M1, si está íntegro y bien fechado | Qué permanece sin identificar |
|---|---|---|
| Señal en cierre | Indicadores de barras cerradas, retornos entre referencias, horario y volumen definidos. | Dato realmente disponible en decision_time, gaps, warm-up/roll y calidad requieren censo. |
| Mecanismo gamma/flujo | Correlaciones de precios pueden motivar una hipótesis. | Posición de dealers, inventario gamma y causa de la operación no se observan por OHLCV. |
| Stop/target dentro de barra | Si un nivel queda fuera del rango registrado puede excluirse el toque en esa serie; dentro del rango hay posibilidad de toque. | Orden temporal entre niveles, lado negociable, cola, cantidad y fill. |
| Trailing de equity | Restricciones parciales si se conoce posición, costes, regla y precio usado. | Recorrido de HWM/retroceso y liquidación cuando depende de información intrabar faltante. |
| Caja | Los precios alimentan el PnL contractual. | Recepción del dinero, tarifas, rechazo y tiempos son estados del contrato/ledger, no datos de precio. |

El high de una barra es el máximo registrado de esa serie en su intervalo. No se justifica afirmar que hubo un pico mayor de la misma serie; puede haber datos faltantes u otra serie quote/mark, pero eso exige evidencia. Un «bound» requiere demostrar límites sobre todas las trayectorias causales compatibles con los datos y reglas. Si distintas trayectorias admisibles cambian pase/cobro o el orden entre políticas, el resultado es no identificable con ese input. No se arregla escogiendo siempre un extremo ni descartando silenciosamente barras conflictivas.

### Protocolo de selección mínimo

- Congelar antes de observar resultados la pregunta, identidad Strategy, sus tres bloques, geometría, MM, programa/fase, datos, costes, horizonte y criterio de comparación. Ningún `x`, «umbral» o variante de salida queda a elección posterior.
- Registrar todos los ensayos relevantes: señales, parámetros, filtros, ventanas, stops/targets, MM, firmas y decisiones previas que influyeron en elegir el candidato. Una parrilla escondida dentro de «ajustes finos» sigue siendo selección múltiple.
- Clasificar datos como descubrimiento, selección, confirmación retrospectiva o reserva verdaderamente no usada. R03 conserva su etiqueta retrospectiva. Haber cambiado el nombre de la ventana, aplicar PBO/DSR o hacer walk-forward no elimina el uso previo.
- Respetar dependencia temporal y cuentas simultáneas. La unidad de incertidumbre no puede ser cada trade IID cuando hay sesiones/regímenes/campañas compartidas. Cualquier purga/embargo depende del solapamiento real de ventanas y labels; no se inventa un valor universal.
- Separar refutación de una regularidad de precios de utilidad prop. Evidencia contradictoria bajo un criterio de refutación predeclarado puede refutar una promesa específica; no alcanzar significación estadística por sí solo no demuestra media no positiva. Ninguno de esos resultados constituye descarte universal de una campaña. Escasez significa incertidumbre, nunca permiso para rebajar G0–G5.

Las tres fichas de I4 son ilustraciones con errores; ninguna queda elevada a spec. Corregir unidades no autoriza completar sus parámetros a gusto del revisor. El stop técnico es parte de Strategy; el presupuesto, cantidad, vetos y límites por etapa corresponden a MM. Las explicaciones de fuente/datos/costes pertenecen a la ficha de investigación y no crean bloques nuevos dentro de Strategy.

## 7. Contratos: lo verificado y lo que sigue faltando

La consulta fue focal y fechada 28-10-2026. Las fechas mostradas por las páginas son metadatos observados; no prueban por sí solas fecha efectiva, cohorte ni prevalencia sobre un acuerdo firmado. Este cuadro es una reparación documental de claims decisivos, **no un RuleSet ejecutable**.

| Fuente / ruta | Corrección que cambia la decisión | Dependencia remanente |
|---|---|---|
| E2 — Rapid estándar 50K, página 24-08-2026 | Evaluación y funded tienen DD distinto; el permiso de noticias también cambia entre fases. | Actualización/enforcement, payout/saldo posterior, costes, restricciones de política y ruta Echo por fase. |
| E3 — Rapid EOD 50K, página 24-08-2026 | Programa separado: evaluación 30%/4 días/3 minis, funded EOD; no heredar 50%/2 días del estándar. Remite a live. | Cohorte, contrato aplicable, interpretación completa del buffer y transición; no combinar programas. |
| E4 — LucidFlex payouts, página 28-07-2026 | 50K: cinco días ≥150 por ciclo, beneficio neto positivo, solicitud hasta 50% del profit con cap 2.000, split 90%. Solicitud puede perder elegibilidad; recepción es posterior. | Evaluación, DD/enforcement, fees, ruta de órdenes y condiciones live completas. No extrapolar indefinidamente SIM: la página limita ciclos y remite a live. |
| E5 — TopstepX API, página 17-09-2026 | Permite bots propios, pero exige origen en dispositivo personal; servidor privado no puede transmitir, activar ni relayar órdenes. ProjectX API no disponible para live. | Si la arquitectura elegida origina órdenes en servidor, esa ruta entra en conflicto con la documentación; no se inspeccionó la arquitectura física de Echo en RV-01. Otra ruta/dispositivo requiere su propio análisis. |
| E6 — Términos Topstep, §§27–28 | El permiso técnico no elimina restricciones de conducta, entorno simulado, posiciones opuestas y VPN/VPS. | No se concluye autorización de hedge/copy entre firmas. Son relaciones por política, titular, programa y fase; desconocido no equivale a permitido. |

No se adoptan tarifas ni comisiones de I2 como vigentes. Se descartó usar como autoridad un PDF histórico de acuerdo Express que apareció en búsqueda pero no pudo abrirse —404—; un snippet antiguo no resuelve el contrato actual. Tampoco se infiere que «alto riesgo» sea siempre incumplimiento: debe confrontarse la política concreta con las cláusulas aplicables. La tolerancia contractual al riesgo y su utilidad económica son preguntas diferentes.

## 8. Coincidencias sólidas y contradicciones entre módulos

### Coincidencias sólidas

1. El marco Owner y la curación DR-01 fijan correctamente campaña/caja, capital finito, separación Forex y ausencia de edge por trade como descarte universal. La referencia 400 y las tasas aspiracionales permanecen supuestos.
2. Los retornos reconocen que señal, MM y contrato interactúan; DR-04 preserva oportunidades y vetos en vez de tratar subconjuntos MM como señales independientes.
3. Se admite que riesgo alto, resolución rápida, horizonte, costes y payout deben estudiarse juntos. No hay base para imponer un porcentaje conservador ni para prometer que la máxima agresividad domina.
4. Dos firmas sobre la misma señal NQ no crean independencia; la selección funded debe condicionarse al proceso de adquisición/pase.
5. No hay resultados propios de RV-01 de simulación, ejecución o cobro; los encabezados de ingestión correctamente rechazan una promoción automática. Las advertencias son útiles, pero no reemplazan la reparación de las interfaces.

### Contradicciones que importan

| Cruce | Contradicción | Resolución de RV-01 |
|---|---|---|
| DR-01 ↔ DR-02 | Probabilidades de barreras simples frente a contrato híbrido y payout con estados adicionales. | No conectar esos números hasta fijar programa/fase y semántica de barreras/retirada. |
| DR-01 ↔ DR-04 | Caja recibida frente a métricas expresadas como PnL/«retiro tras cuotas». | Ledger único y fechas/denominadores explícitos; no doble descuento. |
| Owner ↔ DR-03/04 | Utilidad de campaña frente a WR>50%, PF/Sharpe y media positiva como filtros universales. | Métricas descriptivas separadas de la decisión de caja. |
| DR-03 ↔ DR-04 | Cronología/receta académica variable frente a protocolo que presume señal congelada. | Una especificación causal; cambios son adaptaciones/trials, sin heredar evidencia. |
| DR-04 ↔ separación Strategy/MM | Stop ampliado presentado como sizing puro. | Geometría congelada para MM; otro stop implica otra Strategy/versión. |
| DR-03 ↔ inventario interno | «Hueco» nuevo sin conocer MR04/MR06/MR09 y posible solapamiento con MR01. | Reconciliar antes de duplicar; existencia tampoco significa equivalencia ni cualificación. |
| Mandato histórico ↔ planner | «NO EJECUTADOS» frente a recepciones posteriores. | Preservar documento histórico y usar índice/planner actualizados como estado; no pedir repetir cuatro investigaciones. |

## 9. Dependencias y decisiones Owner

### Dependencias que no se pueden suponer resueltas

| Dependencia | Qué falta exactamente | Responsable / condición de término |
|---|---|---|
| Integridad de retornos | Original DR-01 y eventual tramo/fuentes faltantes DR-02; identidad de autores para independencia verificable. | Reponer archivos existentes o aceptar un expediente limitado. Sin fabricar contenidos ni ordenar otra investigación amplia. |
| Contrato y costes | Un vector coherente por Provider/Program/Size/Stage/Platform/cohorte: barreras/enforcement, días/consistencia, reglas de riesgo, payout, transición live y cargos. | Manager prepara un paquete focal para una ruta y una alternativa. Campo indispensable sin fuente ⇒ dependencia explícita y cierre. |
| Origen de órdenes | API/bridge, ubicación del proceso que dispara/modifica/cancela, propiedad del bot, copia/hedge y permisos por fase. | Confirmación documental del camino elegido; cualquier contacto externo o prueba física exige otro alcance autorizado. |
| Datos y ejecución | Contratos NQ, sesiones/DST, roll, warm-up, cobertura, timestamps y resolución necesaria para eventos económicos. | Inventario/receipts del frente técnico. OHLCV M1 mencionado no acredita cobertura física. |
| Identidad y selección | Qué candidato ya existe, qué se ha probado y qué ventanas influyeron en selección. | Planner/cobertura y receipts; no volver virgen R03 ni heredar PASS. |
| Condición económica de decisión | Horizonte, importe/cobro útil, caja comprometida, pérdidas toleradas y política de continuidad. | Decisión Owner antes de comprometer recursos o interpretar una frontera como selección. |

### Decisiones reservadas al Owner

- Precisar si el objetivo USD 3.000 es solicitud bruta, dinero después de split/cargos o acumulado de varios pagos, y qué horizonte de cobro interesa. Mientras tanto se mantienen los escenarios separados.
- Elegir la preferencia entre mayor probabilidad de cobro temprano, mayor caja esperada/mediana, menor agotamiento y cobros posteriores cuando existan trade-offs. No se inventa un score ni se impone supervivencia de cuenta.
- Fijar pérdida máxima tolerada, desembolsos comprometibles, WIP y regla de detener/reponer. USD 4.000 es capital inicial, no gasto autorizado ni reserva predeterminada.
- Seleccionar programa/fase/plataforma sólo después de una ruta consistente. Las dos firmas de la meta son aspiración de cartera, no requisito para duplicar el primer piloto.
- Aceptar el candidato y su alternativa, o aparcarlos. No se confirma factibilidad de 5+5 con retiros al 31-12-2026 por haber terminado DR/RV.

## 10. Siguiente experimento propuesto y alternativa

### Candidato principal: persistencia de cierre NQ con dos políticas MM

**Pregunta:** con una definición causal fija de persistencia antes del cierre, ¿una política de mayor riesgo admitido por etapa cambia favorablemente la distribución de caja frente a una referencia, al incorporar compras, funded condicionada, elegibilidad, cobros y horizonte? Una regularidad de retornos es una entrada; el resultado de decisión es campaña/caja.

**Siguiente trabajo propuesto al manager:** preparar la ficha determinista y su expediente de datos/contrato. **El experimento no se ejecutó ni queda autorizado por RV-01.** La corrección literaria da un candidato, no una estrategia ganadora ni una réplica ya especificada.

| Elemento | Diseño acotado propuesto | Límite que debe cerrarse antes de ejecución |
|---|---|---|
| Strategy, tres bloques | SETUP: signo del retorno acumulado hasta un instante previo al tramo final; FILTRO: ninguno inicialmente, salvo veto explícito de dato inválido; OBJETIVO/RIESGO: cierre temporal y geometría técnica única. | Congelar referencia de precio, sesión/instante, entrada causal, stop/objetivo y salida. Si difiere del paper, marcar `HYPOTHESIS/OPERATIONALIZATION`. Sin `x` libre. |
| MM separado | Dos políticas fijadas de antemano, con distinto presupuesto/agresividad admisible por etapa. | No asumir que 1%/2% sea la comparación correcta. Definir base del porcentaje o monto, contratos enteros, vetos y estado. Geometría no cambia. |
| Contrato | Un programa exacto, fases evaluación/funded y horizonte común. | Sin híbridos Rapid, fees supuestos ni cash de solicitud. Hasta completar vector no hay valoración contractual aceptable. |
| Comparación | Misma secuencia exógena de oportunidades y mismos datos; registro de señales, vetos, órdenes, fills, estados y caja. | No conservar sólo trades ejecutados de la política ganadora ni arrancar funded sin su condicionamiento. |
| Selección temporal | Un diseño y dos MM; inventario de antecedentes y periodos usados. | No seleccionar la mejor ventana/política en el mismo bloque presentado como confirmación virgen. |
| Resultado | Frontera de caja recibida, tiempos, déficit/agotamiento, coste por activada/pagadora y pendientes. | Si una política ayuda en tiempo pero empeora caja/riesgo, mostrar el trade-off para Owner. No proclamar dominancia por sólo un promedio. |

**Refutadores y salidas:** una incompatibilidad de sesión/contrato bloquea esa combinación; falta de resolución necesaria deja `DATA_REQUIRED`; una hipótesis de precio puede quedar refutada sin declarar inviabilidad prop universal; una valoración de caja desfavorable dentro de supuestos definidos permite descartar esa combinación; ambigüedad que cambia el orden de políticas deja resultado inconcluso. No subir riesgo, abrir otra parrilla ni añadir filtros después para rescatar el resultado dentro del mismo ensayo.

### Alternativa: MR06 ya inventariada, reversión tras shock

Si el candidato principal resulta redundante o incompatible, la alternativa propuesta es **MR06 Volatility Shock Snapback**, descrita en I5. Se estudia una sola identidad existente, con especificación y evidencia reconciliadas; no se presenta como un mecanismo recién descubierto. Compararía reversión con persistencia, usando el mismo contrato y contabilidad cuando sea posible, pero sin suponer independencia ni reutilizar la cualificación del otro candidato.

MR06 puede exigir información intrabar o reglas adicionales según su ejecución real. La descripción de catálogo no acredita disponibilidad de datos ni PASS. Si tampoco puede cerrarse esa identidad con evidencia existente, se aparca la ejecución y se registra la dependencia concreta. No se abre una quinta búsqueda para reemplazarla indefinidamente.

### G0–G5: autoridad preservada

El runbook I6 requiere cualificación por identidad y conserva G2A/G2B/G2C, lifecycle propio, G3 y admisión G4/G5. G4 usa un contrato físico trimestral calificado de al menos 45 sesiones elegibles; no se concatenan vencimientos para fabricar ese mínimo. G5 exige la promoción/recibos correspondientes, incluido pase según autoridad vigente. Esta revisión no cambia esas definiciones, no rebaja puertas por rareza y no crea una excepción llamada «piloto» o «research». No se ejecutó ningún gate. G4 funciona como filtro de cualificación/cómputo; no convierte su muestra seleccionada en confirmación estadística virgen.

## 11. Reparación realizada, límite de trabajo y cierre

La reparación focal de RV-01 queda incorporada en §§4–7: identidades matemáticas; condición condicional/temporal; ledger de caja y denominadores; payout con cap/porcentaje; separación Rapid; origen de órdenes Topstep; cronología/activo de literatura; y protocolo que reconoce datos no identificables y selección previa. Se rectificó además un falso positivo de la ingestión —«Rapid sin buffer» no reproducible— y se conservó la evidencia de futuros del apéndice Nasdaq. No se alteraron los retornos recibidos.

**Permanecen abiertos H01, el vector de H02/H03, la evidencia de datos de H04 y los cierres específicos de identidad/selección.** Su ausencia impide afirmar que este paquete de cuatro retornos ya sustente un experimento de campaña definido y reproducible; por eso no se eleva a `APTO_CON_CONDICIONES`. Sí hay base para el siguiente trabajo documental acotado: reponer la evidencia existente y cerrar la ficha propuesta, o aparcarla. No se exige rentabilidad demostrada para investigar ni se necesita repetir DR-01–04 completos.

**Regla de término para el próximo paquete focal:** entregar los originales recuperables y una matriz de las dependencias anteriores con `RESUELTO` o `NO RESUELTO` y fuente. Una entrega y una adjudicación; si queda un campo indispensable desconocido, conservar `NO_APTO_AUN` y terminar. No encadenar DR-05 ni búsquedas de nuevas firmas para obtener una respuesta favorable. Este apartado propone un alcance futuro; no afirma que ese trabajo pendiente ya se hizo.

**Estado de sesión:** revisión y consolidado documental terminados; reorganización y feedback registrados. Aceptación Owner, elección de campaña, ejecución, gasto y cualificación permanecen pendientes bajo sus autoridades. El cierre de esta sesión no cierra el programa Futures ni acepta los resultados de laboratorio.

## Fuentes

## 12. Registro de fuentes críticas y alcance realmente leído

Se verificaron sólo fuentes capaces de cambiar el dictamen. No se rehicieron las investigaciones de firmas, indicadores ni estrategias. No se certifican lecturas que no ocurrieron. Los IDs I0–I7 remiten al inventario interno de §2 y sus blobs preservados; las citas exactas de la tabla son del material disponible, no reconstrucciones.

| ID | Fuente primaria / URL | Sección leída y alcance | Limitación |
|---|---|---|---|
| E1 | [MIT, Polyanskiy, Lecture 26: Martingales II](https://ocw.mit.edu/courses/6-436j-fundamentals-of-probability-fall-2018/f8ffbc1a27d17d83aaca980fc499d477_MIT6_436JF18_lec26.pdf), 2018 | Definición, optional stopping y gambler’s ruin, §§1–2.1, pp.1–4. | Material docente, no validación empírica NQ. Las aplicaciones a caja son razonamiento de esta revisión. |
| E2 | [MFFU Rapid Plan 50k](https://help.myfundedfutures.com/en/articles/13134709-rapid-plan-50k-a-comprehensive-look) | Página de evaluación/SIM funded/payouts; fecha mostrada 24-08-2026. | No certifica contrato firmado, cohortes, ruta de órdenes ni todo el régimen live. |
| E3 | [MFFU Rapid EOD 50k](https://help.myfundedfutures.com/en/articles/16158363-rapid-eod-50k-a-comprehensive-look) | Parámetros, payout y FAQ; fecha mostrada 24-08-2026. | La prosa de noticias contiene doble negación; la tabla y FAQ distinguen fases. No usar errata como permiso. |
| E4 | [LucidFlex Payouts](https://support.lucidtrading.com/en/articles/12945796-lucidflex-payouts) | Requisitos/ciclos, límites, split y procesamiento; fecha mostrada 28-07-2026. | No cubre toda evaluación, tarifas, orden originada en Echo o contrato live. |
| E5 | [TopstepX API Access](https://help.topstep.com/en/articles/11187768-topstepx-api-access) | Origen de actividad, servidor privado, bots y FAQ live; fecha mostrada 17-09-2026. | Capacidad de API no demuestra elegibilidad del titular ni implementación física. |
| E6 | [Topstep Terms of Use](https://www.topstep.com/terms-of-use) | §§27–28: conducta y VPN/VPS; contexto de acuerdos por fase. | No se decide una controversia legal ni se certifica el acuerdo de una cuenta concreta. PDF Express histórico encontrado en búsqueda devolvió 404 y no se adoptó. |
| E7 | [Baltussen et al., Hedging demand and market intraday momentum](https://www.sciencedirect.com/science/article/pii/S0304405X21001598), JFE 2021, DOI 10.1016/j.jfineco.2021.04.029 | Pasajes editoriales de introducción y conclusión: definición de ventanas y dirección temporal. | Copia PDF del autor no accesible por redirect/timeout; tabla NQ completa y costes específicos no certificados. |
| E8 | [Holmberg, Lönnbark y Lundström, Assessing the profitability of intraday opening range breakout strategies](https://www.sciencedirect.com/science/article/pii/S1544612312000438), FRL 2013, DOI 10.1016/j.frl.2012.09.001 | Pasajes primarios indexados de introducción/highlights y registros universitarios; activo y definición de umbral. | Apertura editorial 403 y PDF universitario timeout. No se declara lectura completa ni transferencia NQ. |
| E9 | [Rosa, Understanding intraday momentum strategies](https://onlinelibrary.wiley.com/doi/abs/10.1002/fut.22375), 2022 | Abstract y Data Availability; señal overnight→últimos30m y activos de la muestra. | No se leyeron tablas/método completo; no se infieren coeficientes NQ ni decay causal por publicación. |
| E10 | [Zarattini, Aziz y Barbon, Beat the Market](https://ssrn.com/abstract=4824172), versión 03-02-2025 | PDF adjunto I7: portada, §2 Data, pasajes de método/gamma y Q13/tabla Nasdaq, página PDF35. | El PDF completo existe en los adjuntos del proyecto; no se transfiere al repositorio ni se afirma lectura integral. El headline SPY y la extensión de futuros son resultados de autores, no de Echo. |

**Consulta externa:** 28-10-2026. Los enlaces de las firmas describen documentación pública observada en esa fecha; cualquier selección posterior exige versión/cohorte aplicable. Los archivos de entrada quedan trazados por commit/blob en [[FUT-R01-INDICE]].
