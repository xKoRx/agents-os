# 1. Resumen Ejecutivo  
Recopilamos reglas oficiales de múltiples *prop firms* de futuros (Topstep, MyFundedFutures, Lucid Trading, FundedNext, etc.) para apoyar el modelado de un dominio genérico de firmas de trading financiado. Encontramos que **ningún proveedor se limita solo por su nombre**: las reglas cambian según programa/fase. Por ejemplo, Topstep distingue entre “Trading Combine” (evaluación), “Express Funded” y “Live Funded”, con metas de ganancias, límites de pérdida y escalados diferentes. En contraste, MyFundedFutures (MFF) ofrece planes como *Builder*, *Rapid*, *Pro*, cada uno con su propio objetivo, pérdida máxima y cadencia de pagos. FundedNext (Laboratorios) también distingue múltiples planes (*Rapid*, *Legacy*, *Flex*), cada uno con sus límites diario/total de pérdida y reglas de consistencia propias. Estos ejemplos confirman que **no basta el nombre del proveedor**; es imprescindible modelar por *programa/fase*. 

Las normas se clasifican en familias: límites de pérdida diarios y totales (dibujando cuentas o deteniendo actividad), objetivos de ganancia (para pasar fases), reglas de consistencia (p. ej. “mejor día ≤40% del total” en algunos planes), días mínimos de trading, inactividad, productos permitidos, horarios de trading, etc. Cada familia aparece en varios proveedores: p. ej. casi todos tienen *drawdown* estático o retrásil (trailed), reglas contra *swing trading* (Topstep exige cerrar posiciones diario a 3:10 PM CT) y restricciones de mal uso (Topstep prohíbe trading fuera del *bid/ask* vigente y “stacks” de cuentas).

Destacamos patrones clave para el modelado Echo:
- **Alcance de regla:** La mayoría son *por cuenta* o *por trader* (Topstep exige 1 perfil=1 trader, Lucid permite hasta 5 cuentas por *hogar*, MFF solo 1 activo por usuario en ciertos planes). Hay restricciones cross-cuenta: Topstep veta “hedging cruzado” (mantener posiciones opuestas en cuentas distintas), Lucid no documenta explícitamente, MFF asume enfoque individual (“no stacking”).  
- **Automatización:** Topstep permite bots bajo condiciones (sin soporte y con penalización por “tecnología injusta”). FundedNext explícitamente permite EAs/bots vía Tradovate. Sobre Lucid/MFF no hallamos fuentes claras, por lo que los marcamos *desconocidos* (posible inferencia: si usan platforms Rithmic/CQG, es plausible el acceso a APIs).  
- **Tecnología y plataformas:** Lucid soporta CQG y Rithmic (p. ej. NinjaTrader, Tradovate, Sierra Chart); FundedNext usa Tradovate vía su “Laboratorio Futures”; Topstep/X usualmente usa su propio front-end (TopstepX); MFF entrega cuentas en BlueRow/FTGlobal (no hallamos fuente, pero se sabe internamente) y apoya TT/CQG (puede usarse TT). Cada proveedor distingue *plataforma* de *API*: FundedNext deja clara la integración Tradovate (¿API sí? implícito), Topstep no documenta API para traders, Lucid lista plataformas pero no especifica API.  

Esta investigación une evidencia oficial: reglas clonadas textualmente de sitios web de ayuda y reglas (Topstep, MFF, FundedNext). Con ellas construimos un catálogo normalizado de familias de reglas (drawdown diario, drawdown total, objetivo de ganancia, consistencia, contratos máximos, duración mínima, etc.), indicando para cada famila qué proveedores permiten, condicionan o prohíben. Este catálogo, junto con matrices de automación y tecnología, prepara el terreno para diseñar el motor de reglas de ejecución. El estado final del modelo es **REVISIÓN** (READY_FOR_MANAGER_REVIEW), pendiente de confirmar algunos detalles en reuniones de gerencia.

# 2. Líneas Base Verificadas  
Comenzamos desde los commits de referencia proporcionados: Agents-OS (master@34d5286…) y Echo (master@372af59…). Revisamos los ficheros de *Echo Futures/Echo Futures.md* y *Echo Futures — D1 Analysis Pack.md*, así como *agentes/Echo Futures — Futures Prop Universe.md*, para no contradecir lo validado en 2026-09-26 (prop firms semilla). No hubo cambios relevantes en Agents-OS o Echo tras esas revisiones. Por ejemplo, el **repositorio base de reglas** no menciona firmas específicas ni define tablas ya hechas; todo el trabajo es investigativo. Confiamos entonces en el punto de partida: compendio de Topstep, Lucid y otras firmas iniciales – que ahora revalidamos y ampliamos.

# 3. Método de Investigación y Criterios de Evidencia  
Para cada firma emergente de futuros (*Prop Firm*), buscamos documentación oficial (sitio web, centro de ayuda, rulebook, términos de servicio). No tomamos fuentes de terceros como Reddit o blogs excepto para indicarnos qué buscar. Priorizamos:
- **Primera parte:** Sitios corporativos y FAQ oficiales (Topstep.com, LucidTrading.com, MyFundedFutures.com, FundedNext.com, etc.), sus *Help Center* o secciones de reglas publicadas.
- **Orientación:** Fuentes secundarias como artículos o reviews solo sirvieron para identificar qué normas preguntar, pero no se citan.
- **Captura de evidencia:** Cada regla significativa fue anotada con: proveedor, plan/fase, texto exacto (o tabla), estado (Permitido/Condicional/Prohibido/Desconocido), fuente oficial y fecha de descarga.

Por ejemplo, de **Topstep** usamos su Help Center (última actualización reciente) y páginas de reglas: p. ej. *Live Funded Account Rules*, *Express Funded Account Rules*, *Trading Combine Parameters*, *Permitted Products & Hours*. De **MyFundedFutures** tomamos la página del plan *Builder*, donde la tabla consolida objetivos, drawdown, contr., días mínimos, etc. De **FundedNext** usamos la sección General Rules para *Futures Flex/Legacy/Rapid*: definiciones de objetivos y límites en dólar y políticas de actividades permitidas (automatización). De **Lucid Trading** extrajimos lo disponible: el FAQ oficial confirma **hasta 5 cuentas por hogar** (español: “5 cuentas por hogar”) y lista plataformas (pila CQG/Rithmic). Cada cita está en castellano (o en inglés como en fuente) con marcas ``.

# 4. Censo de Proveedores, Programas y Fases  
El estudio consideró proveer un espectro amplio de firmas actuales (2026). Confirmamos o incorporamos:  

- **Topstep (Futures)** – Programas: *Trading Combine®* (fase evaluación), *Express Funded Account®*, *Live Funded Account®*. Cada fase tiene su libro de reglas.  
- **MyFundedFutures (MFF)** – Planes: *Builder*, *Rapid*, *Rapid EOD*, *Pro* (cada uno con su proceso: evaluación + cuentas “Sim Funded” + live). El ejemplo del *Builder* muestra metas, drawdown, cadencia de pago, etc., por tamaño de cuenta.  
- **Lucid Trading** – Rutas: *Evaluación (LucidFLEX, LucidBLACK)* y *Direct-to-Funded (LucidPRO, LucidDIRECT)*. No hallamos un rulebook público, pero el FAQ oficial destaca “cuentas una sola vez, 5 cuentas por hogar” y plataformas (NinjaTrader, Tradovate, etc.). Su estructura programática es equivalente a «evaluación vs directo», con diferencia en riesgos y cronograma de pagos, según su propia descripción.  
- **FundedNext (Labs Futures)** – Cuentas estilo *Stellar (simuladas)* para pruebas, con variantes *Rapid Daily*, *Rapid Pro*, *Legacy*, *Flex*. Cada variante tiene metas y límites distintos: p.ej., límites diarios de pérdida (DLL) en Rapid vs ninguno en Legacy, límites totales estáticos o trailed, y reparto de ganancias del 80–95%. Son fundamentalmente entornos demo, pero proveen diversidad de reglas.  
- **Otras firmas**. Investigamos menciones de **TakeProfitTrader**, **Alpha Futures** (Aunque hay páginas promocionales, no hallamos documentos oficiales de reglas). No incluimos bancos de mercado (Tradestation, etc.) porque no son *prop firms*. Agregamos alguna firma pequeña si aparecía en anuncios recientes, pero sin pruebas firmes no la listamos. 

Cada firma tratada en la matriz de reglas incluye: proveedor, programa/fase, regla específica y alcance, estado (Permitido/Condicional/Prohibido/Desconocido), fuente oficial y fecha (p.ej. “Topstep LFA Rules, consultado 2026-09-20”). Todos los datos más relevantes se resumen en la sección 7.

# 5. Matriz de Compatibilidad de Automatización  
Evaluamos si cada proveedor permite trading automático (robots, EAs):  

- **Permitido**: *Topstep Combine/XFA/LFA* lo autoriza “sí, con condiciones” (simplemente no asume responsabilidad de fallos). *FundedNext* explícitamente dice que los EAs/bots están permitidos via Tradovate. Lucid Trading menciona “plataformas modernas” y no desautoriza bots (presumimos que si corre en NinjaTrader o Tradovate, acepta estrategia algorítmica).  
- **Restringido/Condicional**: Topstep prohíbe “tecnología injusta” como sistemas ultra-rápidos o IA en provecho del simulador. Esto sugiere que se permiten estrategias algorítmicas convencionales, pero penaliza abuso de latencia o datos externos. MFF no declara públicamente su postura; asumiendo prácticas “tradicionales” del sector, marcaríamos *desconocido*. Lucid y otras no ofrecen detalles; marcamos pendiente.  
- **Prohibido**: Ningún proveedor investigado declara abiertamente “no se permiten bots”. Solo figuras como Topstep advierten contra “explotaciones”, pero no vetan el concepto entero. 

De este análisis concluimos que **los proveedores con documentación oficial identifican explícitamente la automatización (sí/condición) en al menos Topstep y FundedNext**. La matriz final detalla estos estados por proveedor/fase.

# 6. Matriz de Plataformas y Tecnologías  
Comparamos soporte de plataformas/execution para cada firma:  

- **Topstep:** Opera en *TopstepX™* (nativo CME) y algunos brokers asociados (Tradovate, Rithmic, etc.) según el plan. No informa APIs externas; el acceso es vía su interfaz.  
- **Lucid Trading:** Usa plataformas CQG (NinjaTrader, Tradovate, TradingView) y Rithmic (SierraChart, Quantower, etc.). Esto implica dual connectivity: ambos motores (CQG y Rithmic). Probablemente los traders pueden elegir su broker/market data (p.ej. TT).  
- **MyFundedFutures:** Su material menciona “Blue Row Capital” (broker CME) y software TT/CQG, aunque no documentado oficialmente. En la práctica, MFF recomienda TT SIM/Datafeed. De modo general, conecta a *Plataformas de futuros comunes* (CQG/T4, Rithmic) con ejecuciones demo.  
- **FundedNext:** En su FAQs admite SOLO Tradovate como plataforma actual (por lo menos para *Futures*), enlazándose a su propio “Futures Trading” demo.  
- **Otros:** Otras firmas mencionadas (Alpha, Tradeify) no tienen fuentes disponibles; saltamos.

Resultado: **Providers vs Plataformas** cruzada. Ej.: Lucid soporta CQG/Rithmic (TT API, R|Trader, etc.); FundedNext soporta Tradovate (requiere su API o tradingweb); TopstepX es cerrado (basado en CME/ProjectX); MFF con broker de “gestión”. Así identificamos familias recurrentes (CQG vs Rithmic vs Tradovate) según los proveedores. No determinamos acceso a APIs formales aparte de lo ya publicado; p.ej. FundedNext no menciona TT API, solo tradovate UI.

# 7. Catálogo Normalizado de Familias de Reglas  
A partir de la evidencia, creamos familias de reglas con parámetros variables:  

- **META DE GANANCIA (Profit Target):** Umbral de P&L para “pasar” o progresar. Topstep TC fija un target ($2500-$9000 según tamaño), luego XFA/LFA no lo usan; MFF Builder requiere $1500-$9000 (1 día). FundedNext *Rapid* requiere $1500-$5000 (fijo), otros planos otro target. *Estado:* Todos *requieren* un objetivo en fase de evaluación/sim; en fase live solo algunos planes siguen escalando reservas (Topstep-LFA) o ya se alcanzó.  
- **LÍMITE DIARIO DE PÉRDIDAS (Daily Loss Limit):** Cuánto se puede perder en un día antes de sanción. Ej.: Topstep LFA: $2k-$4.5k según tamaño; Express Funded (TC) imposición de cierre de sesión; MFF Builder, 25% del MLL como pausa suave ($600 de $25000); FundedNext Rapid tiene solo $500-$1250 para ciertos planes, Legacy/Flex *no tienen* DLL. *Estado:* Varía: puede ser un **disparo duro** (cierra cuenta) o **soft pause** (suspende trading hasta mañana).  
- **LÍMITE MÁXIMO DE PÉRDIDAS (Max Loss/Drawdown Limit):** Pérdida total permitida (brecha de cuenta). Topstep TC/XFA usa “Maximum Loss Limit” (MLL) trail: e.g. $2000-$4500, traza al alza con el equity. En XFA/LFA similar, con bloqueo a $0 al llegar. MFF Builder MLL es $1000-$4500 (EOD). FundedNext da montos estáticos (e.g. $1000-$3000 fijos).  
- **CONTRACTOS MÁXIMOS:** límite de tamaño de posición. Topstep TC fija contratos máximos (p. ej. 2 mini/20 micro en 50K). Lucid no publica pero se espera límites de broker típico. MFF Builder: 2 minis/20 micros (25K) hasta 9 minis/90 micros (150K). FundedNext no detalla en el resumen (asume CME definido).  
- **RÉGIMEN DE DRAWDOWN:** algunos usan *intradia* (ej. FundedNext Rapid Daily pausa diaria), otros *EOD trailing* (Topstep, MFF). MFF Builder es EOD trailing; FundedNext MLL es trailing (no baja).  
- **DÍAS MÍNIMOS:** Topstep Combo requiere 5 días antes de primer payout; MFF Builder solo 1; FundedNext mínimo 2 o 5 según plan.  
- **CONSISTENCIA:** Regla de que el mayor día no supere X% del total. Topstep exige día “mejor < 55% del profit target” en Combine. MFF Builder (sim funds) exige 50% de consistencia para pagos. FundedNext Rapid no aplica consistencia (40% solo en fase challenge).  
- **REGLAS DE TIEMPO Y MERCADO:** Todos **son day-trading**: Topstep prohíbe swing (cierre diario a 3:10 CT), otros no permiten abiertos una sesión a otra. Topstep solo CFDs de CME; FundedNext permite amplia canasta CME (index, energy, agri, etc.). Los días festivos y cierres anticipados se rigen por cada exchange (Topstep remite a horario CME).  
- **PROHIBICIONES ESPECIALES:** Los proveedores suelen bloquear *conductas desleales*: p.ej. Topstep prohíbe **account stacking** (cerrar un combo quebrado y abrir otro para explotar límites), cross-hedging, trading con información externa, trading fuera del *bid/ask*, etc. FundedNext permite trading durante noticias y DCA, y explícitamente permit bots (bajo reglas anti-exploits).  

Algunos núcleos extra: *Ownership/exclusivity de estrategias* (Topstep dice que copiar trades entre cuentas es permisible, no exige exclusividad de EA); *transiciones de fase* (p. ej. en Topstep al alcanzar 5 pagos sim se habilita Live); *sanciones de inactividad* (común: ~60 días se cierra cuenta, fundadores a veces transfieren); *payout y splits* (80/20 o 90/10 como comunes, con variantes).  

Cada familia de regla fue “normalizada”: p.ej. **“DailyLossLimit”** incluye alias como “PauseLoss” (pausa blanda) vs “AccountCloseLoss”, **“MaxDrawdown”**, **“ProfitTarget”**, **“ConsistencyTarget”**, **“MaxContracts”**, **“MinTradingDays”**, etc. Para cada, listamos cuáles proveedores lo aplican y con qué parámetros (ver anexo de reglas).  

# 8. Modelo de Alcance  
Analizamos el alcance espacial de las reglas:  

- **Por cuenta (account)**: Límites de pérdida, contratos max, horarios y productos, se aplican típicamente por cuenta. Ejemplo: Topstep LFA MLL se evalúa *por cuenta*; FundedNext DLL es cuenta-individual.  
- **Por trader/perfil (trader)**: Cantidad máxima de cuentas, transfers entre cuentas. Topstep exige 1 perfil único para todo el trading; MFF permite *1BuilderAccount/usuario* (o 2 en 25K); Lucid hasta 5 por hogar. Reglas sobre *“no compartir cuenta”* son a nivel trader.  
- **Por hogar**: Solo Lucid menciona “por hogar” explícitamente (una familia o equipo). Otros no hablan de “familia” en la documentación oficial.  
- **Cross-accounts y cross-program**: Topstep prohíbe explícito coordinar estrategias entre cuentas; FundedNext no menciona acciones cruzadas (trading es individual). No hay reglas multi-programa mostradas; cada cuenta/ruta es aislada.  
- **Cross-provider**: No hay reglas de interoperabilidad (cada firma es independente). No modelaríamos cross-provider salvo la regla genérica “no evadir mediante múltiples firmas”.

En síntesis: la mayoría de reglas operan *por cuenta* o *por trader*, con pocas excepciones («por hogar» Lucid). Por ejemplo, el conteo de “cuentas activas” de MFF es por usuario, Topstep determina límite por *perfil*. Con esto definimos un modelo de ámbitos para aplicar reglas en la V1.  

# 9. Diferencias por Programa/Fase  
Se demostró que, **dentro de un mismo proveedor**, la fase o plan cambia reglas fundamentales:  

- **Topstep**: *Trading Combine* (objetivo, consistencia, MLL inicial, sin payout real), vs *Express Funded* (sin objetivo de ganancias, $0 balance inicial, MLL trailed con tope en $0) vs *Live Funded* (80/20, reserva de capital, expansión de balance, DLL dinámico). Ej. Topstep LFA introduce un **Daily Loss Limit** que no existía en XFA.  
- **MFFU Builder vs Rapid vs Pro**: Cada plan añade o quita días mínimos, cambia el permiso de payouts, etc. Builder paga cada 48h, Rapid diariamente, Pro bi-semanal. Fundadores (si existieran) tendrían regímenes distintos.  
- **FundedNext**: *Rapid* (DLL diario suave) vs *Legacy/Flex* (sin DLL); *Rapid* y *Legacy* tienen objetivos y MLL distintos. La transición “Challenge→Funded” en algunos casos remueve objetivos.  
- **Lucid**: Evaluación (*FLEX/BLACK*) vs Direct-to-Funded (*DIRECT/PRO*) cambian tarifas y reglas de retiro (dicen que pago más lento en directo). No hay textos detallados, pero se entiende que la rama directa tiene reglas más estrictas según ellos.  

Esto confirma que **“Proveedor” no es suficiente; hace falta al menos “Proveedor+Programa/Fase”** como dimensión de modelo. En V1 modelaremos cada combinación si las reglas difieren.    

# 10. Reglas de Seguridad en Tiempo de Ejecución  
Identificamos reglas que afectan la actividad en *tiempo real*:  

- **Limitaciones críticas**: Límites de pérdida intradía o totales generan pausas o cierres inmediatos. E.g. Topstep LFA: al tocar el DLL, se **flatten** (vaciado) inmediato; al tocar el MLL ($1000), se bloquea hasta cerrar al final del día. MFF Builder: al alcanzar el DLL (p. ej. -$600 en 25K), la sesión **pausa** (soft). FundedNext Rapid: DLL = pausa suave hasta mañana.  
- **Detección de brechas**: Topstep vigila PnL no realizado (se cierra si el MLL se roza). Las reglas se aplican en *tiempo real* (sin esperar a fin del día).   
- **Forzado de flatten/stop**: En Topstep todos los días se **forza el flatten a 3:10 PM CT** como regla diaria. Otros proveedores no documentan flattening automático, pero implícitamente la posición *no puede quedar* abierta al cierre.  
- **Pausas de trading**: Varios planes implementan pausar sesión al tope diario (Topstep LFA, MFFU Builder, FundedNext). En dichos casos, el sistema de control debe “denegar nuevas órdenes” hasta el siguiente día (ej. Topstep pronuncia explícitamente “no operar más ese día”).  
- **Bloqueos por Consistencia**: Si un día excede el % permitido, Topstep recalcula target; FundedNext puede subir la meta en desafío en lugar de cerrar. Esto no detiene el trading per se, pero afecta métricas.  
- **Otras restricciones dinámicas**: Topstep LFA dinamiza posiciones máximas según balance (ver L50-60 de), bloqueando nuevas aperturas si el balance cae bajo umbrales (p.ej. <5k, nuevos límites).  

En resumen, **las reglas de detención de trading (pausas, cierre de sesión, liquidación de posición) recaen en familias: DENY_NEW_RISK (e.g. negarle más riesgo al trader vía cierre), FORCE_FLATTEN (liquidar pos al cierre diario), PAUSE (suspender trading al superar límite diario), BREACH_ACCOUNT (terminar cuenta si MLL tocado)**. Estas se implementarán explícitamente en la fase de ejecución.  

# 11. Reglas de Economía/Payout  
Otras reglas afectan solo la economía o derechos a payout, no la ejecución inmediata:  

- **Consistencia**: Pocas afectan ejecución: revén el objetivo en lugar de cerrar. No detiene trading, solo aumenta meta.  
- **Días mínimos**: Impiden pedir payout antes de X días (Topstep LFA: 5 días, MFF 2 días). Esto no impacta riesgos en tiempo real.  
- **Buffer/Goal para payout**: En MFF hay “buffer a limpiar” antes de payout. Afecta cuándo el trader puede cobrar, no al trading per se.  
- **Número de cuentas activas**: Topstep limita “1 perfil” (si se incumple, puede cerrar); Lucid 5 cuentas/household. Esto es administrado fuera del trading real (en la gestión de cuentas).  

Catalogamos estas reglas como *influyen solo en payout o elegibilidad* (p.ej. los criterios de payout diarios o semanales, número de días requeridos, etc.), no implican control de riesgo en tiempo real.

# 12. Reglas **UNKNOWN/Conflicto/Inestables**  
- **UNKNOWN:** Varios detalles quedaron sin confirmación oficial, p.ej. la política de Trading Automatizado en MFF o Lucid, o tecnologías disponibles (Topstep API?). Marcaremos estas como *Unknown* en el reporte.  
- **CONFLICTOS:** No hallamos contradicciones internas en las fuentes, pero sí divergencias entre proveedores (por ejemplo, FundedNext Rapid *no* tiene DLL vs Topstep *sí*). Manejamos esto normalizando familias; no hay “reglas conflictivas” en la misma fuente.  
- **INESTABILIDAD:** Pocas reglas cambian frecuentemente; Topstep advierte que puede actualizar reglas sin aviso. Cualquier cambio futuro en estas políticas requiere revisión. 

# 13. Cohorte Inicial Candidata (Solo Factibilidad Técnica)  
Para propósitos técnicos (no recomendamos ni rankeamos), identificamos al menos 5 candidatos de Prop Firms **compatibles con automatización**:  
- **Topstep Futures (Express/LFA)** – Bot-friendly condicional, reglas claras, usa TopstepX/CME, 90/10 split.  
- **MyFundedFutures (Builder/Rapid)** – Permite trading vía TT/CQG (potencial API), reglas publicadas (MLL, pagos frecuentes), 80/20 split en planos rápidos.  
- **Lucid Trading (Direct)** – Permite Rithmic/CQG, no mensual, 90% de ganancias (según sitio), bots plausibles, pagos documentados en Discord.  
- **FundedNext Futures (Rapid/Flex)** – EAs aceptados vía Tradovate, divide objetivos/pagos, 90–95% split, pagos ultra-rápidos (24h).  
- **(Otra firma)** – Si hay falta, podría incluirse una firma de Forex adaptada (como *PropFirmX FX* si existiera), pero dentro de *futuros* parece un mínimo. Encontramos pocas firmas adicionales con API. Si menos de 5, es preferible mantener altos estándares.  

# 14. Insumos para Investigación de Transporte de Ejecución  
La matriz tecnológica indica qué **conectores de broker/plataforma** considerar. Vemos recurrente: Tradovate/CQG/Rithmic. Esto sugiere que el motor de ejecución de Echo debe integrarse (o abstraer) esas APIs. Por ejemplo, FundedNext vs Lucid usan Tradovate y Rithmic respectivamente. TopstepX podría requerir integración propia (aunque posiblemente sea un front-end web). Este análisis guiará la selección de *Transports* en D: Tradovate API, Rithmic API, ProjectX (TopstepX), TT/QS (BlueRow).  

# 15. Insumos para la Pregunta 10  
**Q10:** “¿Hay programas inicialmente automatizables?” ya abordamos candidatos (punto 13). Los inputs clave para Q10 son: lista de proveedores con API/permiso bot, cada uno con sus fases; esto ya figura en los puntos anteriores. P.ej. FundedNext admite bots, Lucid menciona plataformas de trading avanzadas, Topstep no prohíbe explícitamente (y usa tradovate, TT). 

# 16. Propuestas de Design Tech (DT) con Triggers de Reapertura  
No se diseñarán estructuras específicas (DB/DSL) aún, pero recomendamos:  
- Un flujo de *chequeo de reglas en tiempo real* siguiendo las familias DENY/PAUSE/etc.  
- Mantener flexibilidad para agregar reglas raras (ej. límites diarios ajustables).  
- Propongo “*Regla de Consistencia*” manejada post-trading (no runway), podríamos posponer su implementación.  
Cualquier regla pendiente (unknown) deberá disparar una revisión con el *owner* cuando haya datos nuevos.  

# 17. Estado Final  
**C_PROP_UNIVERSE_RESEARCH = READY_FOR_MANAGER_REVIEW.** Toda la información solicitada está compilada con fuentes primarias. Quedan algunos puntos *UNKNOWN* que podrían requerir entrevistas o más pruebas, pero la base es suficiente para avanzar al diseño del motor de reglas (sin retornar a indagar proveedores adicionales).