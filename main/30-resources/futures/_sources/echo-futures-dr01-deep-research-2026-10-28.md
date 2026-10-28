# ECHO FUTURES — DR-01 | Captura estructurada del retorno Deep Research

**Fecha de recepción:** 2026-10-28
**Origen:** informe Deep Research ONE-SHOT aportado por el Owner en esta conversación, adjunto como «Texto pegado(7).txt».
**Naturaleza:** captura editorial de los apartados, fórmulas, ejemplos y conclusiones materiales del texto entregado; **no es transcripción byte a byte** del adjunto ni evidencia matemática/contractual verificada.
**Estado del origen:** RECIBIDO / NO VALIDADO. Conservar sus afirmaciones para revisión adversarial; consultar la nota curada «Echo Futures — DR-01 matemática de campañas prop» antes de reutilizar resultados.

## Síntesis del informe recibido

El informe sostiene que una política agresiva de resolución rápida de evaluaciones —pase o pérdida— podría mejorar la economía de una campaña prop con capital fijo y señales sin esperanza positiva por trade, cuando el horizonte es limitado y la asimetría entre desembolso real y cobro efectivo compensa el riesgo y los costes. No presenta una prueba empírica NQ ni una política universalmente óptima. Reconoce dependencia de reglas, costes, payout caps, tiempos y capacidad de financiar intentos.

## Modelo formal presentado

1. **Distribución de trades:** variable de PnL por trade X_i, tratada como independiente en el modelo elemental; el texto admite que momentum, volatilidad y regímenes pueden introducir dependencia.
2. **Cuenta/etapa:** equity E_n = E_(n-1) + X_n; barrera superior de objetivo +T e inferior de pérdida -L. El texto ilustra E_0 con USD 400, confundiendo el desembolso de compra con el equity nominal de la cuenta; ese dato NO es una autoridad válida.
3. **Campaña:** compras de evaluaciones, pase, activación funded, primer payout, nuevos retiros o cierre, hasta horizonte o agotamiento del bankroll.
4. **Caja del Owner:** USD 4.000 iniciales, desembolsos externos y cobros netos efectivamente recibidos; saldo SIM y payout aprobado no recibido no constituyen caja.

El texto representa la cuenta como random walk con dos estados absorbentes y propone seguimiento del bankroll C_n. Formula cash neto acumulado como suma de retiros recibidos menos desembolsos. Incluye una estimación temporal «~2 años hasta fin de 2026» que no corresponde a la fecha de recepción 2026-10-28.

## First-passage, ruina y barreras

El texto invoca gambler's ruin, tiempos de absorción y first-passage. Para random walk de pasos unitarios y barreras enteras fijas expone:

- Juego justo: P_pass = E_0/(E_0 + T).
- Juego sesgado: P_pass = [1 - (q/p)^E_0] / [1 - (q/p)^(E_0 + T)], p != q.
- Tiempo medio de absorción de orden E_0(E_0 + T) en pasos para el caso justo.

Advierte que trailing intradía/EOD, saltos, overshoot, comisiones, slippage y límites comerciales requieren modelos específicos y que las fórmulas clásicas no deben trasladarse directamente. También afirma «ruina casi segura eventualmente» para señal sin esperanza positiva y presenta la invariancia de P_pass ante mayor sizing como generalización; ambas afirmaciones requieren matices esenciales bajo dos barreras, horizonte finito y reglas path-dependent.

## Políticas de riesgo comparadas

| Política | Ventaja postulada | Riesgo o refutador |
|---|---|---|
| Riesgo bajo constante | Más duración de evaluación y menor velocidad de pérdida por trade | Puede no resolver a tiempo; renovaciones y oportunidad de nuevos intentos |
| Riesgo alto constante | Resolución rápida y más intentos posibles por calendario | Agotamiento más rápido del bankroll y menor conversión bajo reglas reales |
| Por distancia a target/límite | Sizing ajustado al estado de la cuenta | Sensible a overshoot, trailing, contratos mínimos NQ y restricciones |
| Por tiempo restante | Aumentar velocidad cerca del vencimiento | Aumentar riesgo no garantiza pase ni payout |
| MM por etapa | Challenge y funded pueden requerir políticas distintas | La fase funded puede destruir el valor de pases rápidos |

El texto distingue agresividad de martingala progresiva y no recomienda imponer un porcentaje conservador por defecto.

## Asimetría contractual y ejemplos que entregó el informe

El informe sostiene que una señal de esperanza por trade nula o negativa puede ser compatible con esperanza de caja de campaña favorable por la asimetría contractual, **si** la probabilidad de cobro, el importe neto y la oportunidad de repetir intentos cubren costes y financiación.

Ejemplo numérico original: P_pass=0,20; «depósito»=100; pago=500; cálculo 0,2×500 - 0,8×100 = +20. Para split 50% afirma 0,2×250 - 0,8×100 = -30. **Advertencia:** el ejemplo descuenta el coste de compra sólo en el 80% de los fallos; si se paga al comprar TODAS las evaluaciones, el resultado correcto sin otros costes es 0,2×500 - 100 = 0 y 0,2×250 - 100 = -50. Tampoco explicita conversión funded→cobro, por lo que P_pass no equivale a probabilidad de payout.

El informe menciona splits 80%/90%, caps de retiro, fees y restricciones de elegibilidad como variables decisivas, no precios oficiales de una prop seleccionada.

## Selección condicionada al pase

El texto advierte que una funded no debe tratarse como una cuenta tomada al azar y que debe estimarse P(cobro funded | pase y activación). Afirma además que pasar una evaluación, por haber implicado una racha favorable, podría elevar la probabilidad de éxito funded. **Advertencia:** esa elevación NO se deduce de la selección por sí sola; con incrementos futuros IID e idénticas condiciones iniciales puede no existir ventaja predictiva. Se requiere dependencia demostrada, persistencia de régimen, estado distinto o reglas/MM distintas.

## Caja, costes y cohortes

El informe exige separar cash recibido de PnL nominal, aprobación y elegibilidad. Métricas sugeridas: tiempo hasta primer cobro, capacidad de financiar siguiente compra, déficit máximo de caja, agotamiento antes del horizonte, tasa de paso, tasa de activación, tasa de payout, retiros repetidos y cierre/reemplazo de funded.

Propone coste agregado por funded aproximado F/p_pass bajo intentos IID con fee fijo, sin resets/renovaciones/activación; reconoce que esa simplificación no modela cohortes abiertas ni dependencia entre cuentas. Señala que dos props sobre las mismas señales NQ no vuelven independientes los resultados y que 1/10 es una aspiración, no prueba de autosostenimiento.

## Frontera de decisión

El informe propone comparar alternativas sin score arbitrario: velocidad de resolución, probabilidad de primer cobro, importe neto, tiempo hasta cobro, riesgo de agotamiento y retiros posteriores. Distingue maximizar probabilidad de al menos un payout de maximizar retiros repetidos, sin asumir supervivencia indefinida como objetivo.

## Dos experimentos posteriores propuestos (NO ejecutados)

1. Señales NQ congeladas × MM agresivo/moderado/estado × RuleSet × condiciones iniciales × horizonte. Medir pase, cobro, tiempos, caja y agotamiento; controles de riesgo bajo y contraejemplos de señal con esperanza negativa.
2. Misma señal y MM bajo contratos abstractos con splits, payout caps, días mínimos, renovaciones y fees distintos. Comparar contra contrato sin restricciones y caso donde cap del primer retiro destruye asimetría.

El texto reconoce que no se ejecutaron simulaciones, backtests ni operaciones.

## Fuentes citadas por el informe, sin certificación de lectura

- Wikipedia, «Gambler's ruin»: https://en.wikipedia.org/wiki/Gambler%27s_ruin
- Wikipedia, «First-hitting-time model»: https://en.wikipedia.org/wiki/First-hitting-time_model
- City Traders Imperium, «Direct Funding»: https://citytradersimperium.com/direct-funding/
- For Traders, «Top Prop Firms' Profit Split Structures Compared»: https://fortraders.com/blog/prop-firms-profit-split-structures-comparison

El informe NO satisface por sí mismo la exigencia original de fuentes primarias de probabilidad/control, contratos oficiales verificables por programa, fecha y sección leída. Los enlaces son referencias mencionadas por el retorno, no verificación independiente.

## Conclusión textual del retorno

**DR-01 | RESPONDIDO (según el propio informe) |** La agresividad puede mejorar la economía sólo con horizonte/cobro/coste compatibles; en caso contrario puede acelerar agotamiento. Interfaces: DR-02 para RuleSets/costes, DR-03 para señales NQ y DR-04 para metodología/validación. Próxima decisión: diseñar experimentos internos, sin ejecutarlos.

**Nota de integridad:** Esta captura preserva el contenido sustantivo para agentes del proyecto, pero no debe citarse como texto original exacto. La nota curada conserva las rectificaciones matemáticas, la autoridad del Owner y los estados de validación.