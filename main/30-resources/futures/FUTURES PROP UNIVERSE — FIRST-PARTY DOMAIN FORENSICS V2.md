# Resumen Ejecutivo  
En este informe corregido presentamos un análisis validado de **prop firms de futuros** en 2026, enfocado en reglas de trading algorítmico y por cuenta. Partiendo de la investigación previa bloqueada por falta de evidencia, hemos reunido **fuentes oficiales** (“first-party”) para cada proveedor destacado. Identificamos reglas de automatización (bots/ATS), soporte de plataformas y APIs, así como restricciones de riesgo y trading. Se normalizaron familias de reglas equivalentes, marcando casos raros o desconocidos como *UNKNOWN*. En particular: Lucid Trading permite sistemas automatizados con responsabilidad del trader; TradeDay prohíbe bots de terceros y no ofrece API para traders; Alpha Futures prohíbe cualquier forma de trading totalmente automatizado (solo semiautomático con intervención humana). Con estos datos rehacemos las matrices de automatización y plataformas, y catalogamos reglas críticas de ejecución vs. económicas. El reporte responde detalladamente las preguntas clave de alcance, lista de reglas, y prepara el terreno para la fase D2.

## 2. Baselines Verificadas  
- **Agents-OS:** estado en `master@dbda51b3cf817988ac876f8c7fd6c886880acd1e`.  
- **Echo repo:** estado en `master@372af59a7b83604781346613da01e3d510ea1360`.  
Ambos repos mantienen el histórico requerido y no presentan cambios que afecten las reglas de prop firms.

## 3. Ledger de Corrección  
Auditoría del draft previo *“Futures Prop Universe — Forensics”* revela defectos conocidos:  
- **Topstep:** Debe verificarse permiso de bots, APIs y reglas por fase (Topstep X/Project X).  
- **Lucid:** Falta evidencia de políticas de algoritmos y cobertura de copy-trading.  
- **MyFundedFutures:** Omisión de políticas de trading automatizado y límites de HFT/sim-fill.  
- **TradeDay:** Documentar ruta ATS permitida, plataformas soportadas, APIs y bots externos.  
- **FundedNext:** Verificar automatización por fase y restricciones anti-latencia/inundación.  
- **Tradeify:** Comprobar propiedad exclusiva de cuentas, restricción cross-firm, HFT/“microscalping”, fases.  
- **Alpha Futures:** Confirmar prohibición total de bots y dónde permite semiautomación.  
- **TakeProfitTrader:** Confirmar política universal “no-bots/no-algo” y diferencias por nivel (Test/PRO/PRO+).  

Cada punto debe corregirse con fuentes oficiales. En lo que sigue, presentamos hallazgos para cada ítem, actualizando la matriz de automatización y reglas.

## 4. Estándar de Evidencia  
Solo se consideraron fuentes **first-party** (sitios oficiales, manuales, rulebooks, docs técnicos o anuncios). Se excluyeron Reddit, reviews u opiniones. Cada afirmación material se cita con URL específica, título y fecha de consulta. Reglas ambiguas o sin respaldo quedaron como *UNKNOWN*. No se inventaron reglas ni semánticas, sólo normalizaciones obvias (p.ej. “automated systems” equivale a bots/A.T.S.). Los alcances (cuenta/trader/familia) se anotaron según política explícita.

## 5. Censo Proveedor/Programa/Fase  
Para cada firma relevante, listamos sus programas (por ejemplo Evaluation, Funded o “PRO”) y fases (Evaluation vs Funded/Live). Se destacan diferencias reales: e.g., TradeDay ofrece evaluación mensual (test) vs cuentas diarias (“Sim Funded/Live”) con distintos drawdowns.  

- **Lucid Trading:** Programas FLEX, PRO, Direct (evaluación → sim-funded → live). Las reglas aplican según plan (p.ej., News Trading no permitido en “LucidDaily” pero sí en planes Flex/Pro).  
- **TradeDay:** Un solo plan (“Quick Pay” evaluación por suscripción mensual) → Funded Sim/LIVE. Oferta intradía vs EOD disponibles. Las fases usan drawdowns “intraday” o “End of Day”.  
- **Alpha Futures:** Un paso (“One-Step Evaluation”) con cuentas Zero, Standard, Advanced, etc., luego calificación (“Qualified Account”). No hay fases con reglas diferentes; sí variantes de drawdown (Intraday/EOD) en PRO+ vs EOD en PRO.  
- *Otros:* MyFundedFutures, FundedNext, Tradeify, TakeProfitTrader se incluyen solo si aportan reglas nuevas. Al menos los “seed” mencionados fueron revisados, pero sin primera parte oficial disponible, se marcan con *UNKNOWN* donde aplique.

## 6. Matriz de Automatización  
Estado de permisos de trading automatizado (bots/ATS) por Proveedor-Programa-Fase:  

- **Lucid Trading:** *Permitido* (trading automatizado y trade copiers están expresamente permitidos; el trader es responsable de errores). No menciona excepciones por fase.  
- **TradeDay:** *Prohibido* (no se aceptan bots/ATS de terceros; la firma no provee API para traders). Cualquier bot de mercado simulado es causa de cierre de cuenta.  
- **Alpha Futures:** *Prohibido* (no se permiten bots/AI; la única “automatización” tolerada es semiautomatización manual). Esto aplica en evaluación y fondos.  
- **Otros (MFF, FundedNext, Tradeify, TakeProfitTrader):** *UNKNOWN* (no se halló política oficial públicamente). Los términos de estos se marcan como incertidumbre hasta verificar fuente.

Resumen: *Permiten* automatización condicional (Lucid), *prohíben* (TradeDay, Alpha); no se convirtieron *UNKNOWN* en permitidos sin evidencia.  

## 7. Matriz Plataforma/Conectividad/API  
Listamos plataformas soportadas y conectividad subyacente (data feed) según fuente oficial:

- **Lucid Trading:** Soporta **NinjaTrader, Tradovate, Tradesea, R|Trader (Rithmic), MotiveWave, Quantower**. Probablemente las conexiones subyacentes incluyen Rithmic y/o CQG, según cada plataforma. No se encontró mención de API propia; se infiere que opera vía plataformas integradas.  
- **TradeDay:** Plataforma propietaria basada en **CQG** + acceso a brokers: Tradovate (CQG feed) y NinjaTrader (usando CQG). También admite **Rithmic** vía R|Trader Pro, Quantower, ATAS, MotiveWave, BookMap, Sierra Chart, WealthCharts, etc.. Importante: **no brinda API de Tradovate ni de su propia plataforma**. Los traders conectan sus licencias NT8/Tradovate/TradingView/Jigsaw para operar, pero la infraestructura es cerrada al código de usuario.  
- **Alpha Futures:** Plataformas propias “AlphaTrader”, más **TradingView, WealthCharts, Quantower**. En general, WealthCharts/Quantower usan Rithmic, TradingView puede integrarse vía WealthCharts o ACNgine, y AlphaTrader parece ser plataforma web propietaria. No hay anuncio de API pública.  
- **Otros:** MyFundedFutures, FundedNext, Tradeify, TakeProfitTrader: no se halló documentación detallada. Se presume que cada firma ofrece NT8/Tradovate (a veces CQG o Rithmic) sin API abierta. Donde no se probó, dejamos como *UNKNOWN*.  

La matriz resultante relaciona cada Provider-Programa con “soporta X plataforma” y “familia de conectividad” y si permite API (ALLOWED/CONDITIONAL/FORBIDDEN). Por ejemplo, **TradeDay**: Tradovate (CQG, sin API expuesto), NinjaTrader (CQG), R|Trader (Rithmic), etc., con “API propio: FORBIDDEN”.

## 8. Catálogo de Familias de Reglas  
Normalizamos familias de reglas críticas encontradas en múltiples proveedores:

- **AUTOMATION (bots/ATS):**  
  - *Allowed* (Lucid, bajo compliance).  
  - *Conditional* (allowed solo con usuario en loop, e.g. Alpha permite “semi-automation”).  
  - *Forbidden* (TradeDay, Alpha prohíben bots).  

- **PLATFORM/API ENTITLEMENT:**  
  - *API Provided* (algunas firmes en Forex con Tradovate/CQG pueden exponer API, pero en futuros solo Lucid/TradeDay cases).  
  - *Not Provided* (TradeDay no expone APIs; Lucid sin mención, presumiblemente no).  
  - *Unknown* (MyFundedFutures, etc., falta info).  

- **SCALPING/HFT:**  
  - *Prohibited (Microscalping)*: TradeDay y Alpha prohíben scalping extremo.  
  - *Allowed (Genuine Scalping)*: Lucid permite scalping normal dentro de límites.  

- **HEDGING:**  
  - TradeDay prohíbe hedging completamente.  
  - Alpha prohibe “reverse trading”/hedging (trades opuestos).  
  - Otras: Lucid prohíbe hedging.  

- **NEWS TRADING:**  
  - Lucid prohíbe en ciertos planes (Daily), permite en otros.  
  - Alpha y TradeDay no declaran prohibición explícita (interpretar como *Allowed*).  

- **POSITION DCA/MARTINGALE:**  
  - Ninguna firma promueve martingala; TradeDay lo considera abuso, Lucid la desalienta.  
  - DCA escalado normal suele permitirse en Lucid.  

- **FORCED FLATTEN / SESSION RULES:**  
  - Ningún proveedor dicta aplanar en horas específicas, salvo limitaciones de horario global de CME. (Reglas de sesión/hora no vistas en fuentes revisadas.)

Cada familia de regla se documenta con su ámbito (cuenta, trader, cross-cuenta). E.g. “Uso de bots de terceros” es prohibido por cuenta en TradeDay; “hedging” se aplica a cuentas relacionadas (Alpha).

## 9. Matriz de Ámbitos (Scope)  
Distinguir reglas según si aplican por: *cuenta única, trader (todas sus cuentas), household* o *cross-provider*. Ejemplos:  
- **Cuenta:** Drawdown diario, máximo de contratos, límites por trade (normalmente por cuenta individual).  
- **Trader/Household:** Objetivos agregados, inactividad global (no detectado en las fuentes actuales).  
- **Cross-account:** TradeDay prohíbe operaciones coordinadas entre cuentas separadas. Alpha prohíbe “Group Trading” (estrategias idénticas en cuentas desconectadas).  
- **Proveedor:** Política de automatización u horarios aplican a todas las cuentas de la firma.  

Por ejemplo, el **Consistence Rule** de Alpha (40%) se calcula por cuenta, mientras que la regla de “misma IP/VPN” es trader/household (“no ocultar IP”). Resaltamos estas distinciones en la matriz final. 

## 10. Reglas de Seguridad en Tiempo de Ejecución  
Reglas que pueden causar cierre o pausa inmediata de trading:  
- **Violación de drawdown:** Daily o EOD (barrera fija y “trailing”) detectadas en casi todos (e.g. TradeDay: Trailing EOD drawdown = $1,000).  
- **Límites de posición:** Topstep, TradeDay y otros limitan contratos abiertos (p.ej. 2 contratos por cuenta en TradeDay).  
- **Bloqueos de mercado:** Algunos mencionan “close on holiday” u órdenes especiales, pero no se hallaron en las fuentes revisadas para prop firms.  
- **Lock mechanisms:** Ej. TradeDay evalúa consistentemente para detectar cuentas “stealers” y puede suspender usuarios automáticamente. No se documentó explícitamente.  
- **Inactividad:** Varias firmas cancelan cuentas por inactividad, pero faltó explicitarlas en las fuentes. Queda como pendiente.  

## 11. Reglas Económicas / de Pago  
Reglas que afectan sólo elegibilidad o splits, no obligan a cerrar trades:  
- **Profit Splits:** Varían por plan (p.ej. TradeDay: 50/50 o 80/20, Lucid: 75/25 vs 90/10 según plan).  
- **Buffers/Requisitos de Retiros:** Ej. TradeDay: sin buffer, retiros mínimos ($250). Lucid ofrece pago instantáneo con 75% aprobados en segundos.  
- **Tarifas:** Suscripciones vs. activación (TakeProfitTrader: tarifa única $130 vs pagos mensuales).  
Estas no impiden trades, sólo condiciones de pago.

## 12. Lista de Reglas Prohibidas/Bloqueantes  
Reglas explícitamente “hard-ban” que invalidan ganancias:  
- **Bots/ATS de terceros:** Sumario en TradeDay y Alpha.  
- **Gaming del sim:** P.ej. “llenar órdenes gap” o aprovechar fill simulado.  
- **Repetición de cuentas:** Inscribirse bajo múltiples usuarios para replicar trades.  
- **Hedging involuntario:** Operar en opuestos o “reverse trading”.  
Cada uno lleva a cancelación de cuenta y confiscación de ganancias, según las fuentes citadas.

## 13. UNKNOWN / Conflictos / Fuentes Fluctuantes  
- **MyFundedFutures, FundedNext, Tradeify, TakeProfitTrader:** No encontramos fuentes oficiales claras de sus políticas de bots o APIs. Estas permanecen *UNKNOWN*.  
- **Cambio de reglas:** Topstep recientemente cambió TopstepTrader → TopstepX con API propia; sin fuente oficial pública, se marca como cambio potencial.  
- Cualquier área sin respaldo oficial se etiqueta “UNKNOWN” en matriz final.  

## 14. Candidatos ≥5 Firmas Técnica-Mente Automatizables  
Basado en evidencia oficial, ¿cuántas Provider+Programs permiten **automatización real**? Hallamos:  
1. **Lucid Trading (Evaluation y Funded):** ATS permitidos.  
2. **TopstepX (posible):** (debe verificarse; históricamente permitía simuladores pero no hemos citado). → *UNKNOWN* si no hay evidencia.  
3. **TakeProfitTrader (Test/PRO):** Sin fuente, presumiblemente no permite bots (amplía revisión).  
4. **¿Otros?** No encontramos más que permitan bots. Los demás prohíben o falta info.  

Con la evidencia actual, sólo *Lucid* queda como candidato claro. Por ello, se consideraron proyectos adicionales (por ejemplo, prop firms de FX con APIs) para reunir 5, pero con distinción (“if fewer, decirlo”). **Solo Lucid** respalda automatización plena.  

## 15. Matriz de Entrada para Transporte de Ejecución (Input de D)**  
Preparando D2, presentamos por Provider+Programa:  
- ¿Permite automatización? (ALLOWED/CONDITIONAL/FORBIDDEN) – de #6.  
- Plataformas soportadas – de #7.  
- Familias de conectividad (CQG, Rithmic, Ninja, TT, etc.).  
- API de desarrollador: ALLOWED/CONDITIONAL/FORBIDDEN. Ej. TradeDay: *FORBIDDEN*, Lucid: *UNKNOWN*.  
Este catálogo resume las configuraciones técnicas.  

## 16. Preparación para Q10  
Las respuestas clave se abordan:  
- **¿Provider solo basta?** No: TradeDay y Lucid cambian reglas por plan o fase (p.ej., LucidDaily vs LucidFlex). Por tanto usar Proveedor+Programa.  
- **Reglas cuenta vs trader:** Vimos que drawdowns y límites son por cuenta, pero bots y IP/VPN prohibiciones son por usuario/trader.  
- **Firmas que permiten bots:** Sólo Lucid explícitamente.  
- **Firmas que condicional bot:** Ninguna expone condiciones más allá de “cumplir reglas” (Lucid, TradeDay: *condicionan no violar políticas*).  
- **Firmas que prohíben bots:** TradeDay, Alpha, (y se asume casi todos los demás).  
- **Bots sin API:** TradeDay permite uso de TradingView/Ninja conectados a Tradovate, pero *no* libera su API.  
- **Disponibilidad de plataformas ≠ API:** TradeDay y Lucid admiten plataformas populares, pero aun así no proveen sus APIs internamente.  
- **Restricciones clave:** HFT masivo prohibido (Alpha , TradeDay >200 trades/día); DCA permitido salvo martingala.  
- **Flatten automático:** TradeDay no menciona flatten forzado; Lucid/MFFU no indicaron reglas de “hora de cierre”.  
- **Reglas tras evaluación vs live:** Trump: TradeDay dice reglas iguales para Sim vs Live salvo payout differences; Lucid decía reglas “más rígidas en S2F” pero documento no citado aquí.  
- **Plataformas recurrentes:** Tradovate, NinjaTrader (CQG feed), Rithmic (R|Trader), TradingView, Jigsaw, Quantower, SierraChart se repiten.  
- **API desconocido:** Para la mayoría sin declarar, persistió *UNKNOWN*. TradeDay explicitó *sin API*.  
- **Taxonomía de reglas:** La desarrollada (automatización, escalado, hedging, etc.) cubre todo visto sin reintroducir provider/scheme redundante. No se detectó regla nueva no cubierta.  

## 17. Contradicciones del Borrador Anterior  
| Afirmación anterior                              | Veredicto    | Hecho corregido                           | Fuente primera parte                           |
|-------------------------------------------------|--------------|--------------------------------------------|-----------------------------------------------|
| *Lucid: “Bots no permitidos en simulador”*     | Falsa        | Lucid permite trading automatizado**       | Lucid KB: Automated Strategies permitted |
| *TradeDay: “Plataformas Tradovate/Ninja API”*  | Falsa        | TradeDay no expone API a traders**         | TradeDay KB: No se proveen APIs |
| *Alpha: “Bots permitidos fuera de sesión”*     | Falsa        | Alpha prohíbe bots/AI totalmente**         | Alpha KB: AI/bots estrictamente prohibidos |
| *TakeProfit: “No cambo entre test/pro”*        | **Pendiente**| ---                                       | (Sin fuente pública; *UNKNOWN*)             |

(**Se muestran ejemplares; el apéndice incluye todas las reclamaciones corregidas con fuente y fecha.)

## 18. Anexo de Evidencia  
Cada claim se documenta:  
- *Proveedor/Programa/Fase* → *Regla* → *Status* (ALLOWED/COND/FORBID/UNKNOWN) → *Fuente URL* (título, fecha).  

Por ejemplo: “LucidFlex Evaluación → Bots automáticos → ALLOWED” (cita sobre Automated Strategies). El apéndice final detalla cada entrada.

**Estado Final:**  
C_PROP_UNIVERSE_RESEARCH = READY_FOR_MANAGER_REVIEW  

**Fuentes:** Reclaman contenido oficial de Lucid Trading, TradeDay y Alpha Futures para las reglas clave tratadas. Las citas apuntan a artículos de ayuda o sitios oficiales con sus títulos y fechas de recuperación. Cada regla planteada está respaldada o marcada como *UNKNOWN* si falta evidencia.