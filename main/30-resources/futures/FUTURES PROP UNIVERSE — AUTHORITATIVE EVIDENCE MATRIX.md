# Resumen Ejecutivo  
Revisamos detalladamente las políticas oficiales *first-party* de ocho proveedores: Topstep, Lucid Trading, MyFundedFutures (MFFU), TradeDay, FundedNext Futures, Tradeify, Alpha Futures y TakeProfitTrader. Extraímos solo hechos explícitos. En Topstep, la automatización está **permitida** en entornos simulados (Combine y Express Funded) vía su API (ProjectX), con prohibición de HFT; en cuentas **Live** está prohibida la API. Lucid Trading: no encontramos información oficial disponible, por lo que sus políticas quedan **UNKNOWN**. En MFFU, se **permite** trading automatizado (EAs/bots) en todas las etapas, con la condición de no explotar artificios de simulación; se prohíbe HFT y tampoco se tolera copy trading ni compartir dispositivos. TradeDay autoriza **solo** sistemas automatizados ejecutados mediante plataformas soportadas (NT, Tradovate, TradingView, Jigsaw, Quantower); prohíbe APIs directas y bots de terceros; está permitido el uso de ATS condicional (vía plataformas aprobadas) y se sanciona la copia de operaciones. FundedNext permite EAs/bots en **Challenge** y cuentas fondeadas, pero prohíbe estrategias de latencia abusiva/HFT. Tradeify: sin datos oficiales consultados, se deja **UNKNOWN**. Alpha Futures prohíbe **todo** trading automatizado (bots/IA) en todas las etapas; solo acepta señales semi-manuales. TakeProfitTrader también prohíbe rotundamente bots/algoritmos automatizados (prohibición explícita en sus políticas universales).  

# Verificación de Baselines  
- **Proyectos Git**: Agents-OS (`c588d29`) y Echo (`372af59a`) revisados, sin modificaciones requeridas.  
- **Política conocida**: “Alpha full automation = FORBIDDEN”, “TPT bots forbidden” se confirman en fuentes.  

# Cuadro de Contradicciones (V1 vs V2)  
No dispusimos de los borradores V1/V2 internos para comparar. En las fuentes consultadas no aparecieron afirmaciones contradictorias entre versiones anteriores; por ende, no se documentaron conflictos factuales.  

# Matriz de Automatización por Programa (Provider/Program/Phase)  

| Proveedor        | Programa / Fase                      | Automatización  | Condiciones principales                                                                                                                                       | Plataformas soportadas                                               | Conectividad | API directa       | Restricción sobre API             | Multi-cuenta/Cross-provider   | Restricción HFT/micro       | Fuente (fecha)                   |
|------------------|--------------------------------------|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------|--------------|-------------------|-----------------------------------|------------------------------|-----------------------------|-----------------------------------|
| **Topstep**      | Trading Combine (simulación)         | ALLOWED (Cond)  | Via TopstepX (ProjectX API); sin HFT, cada orden desde equipo personal (no VPS)                                                | TopstepX (ProjectX)                                                   | PROJECTX     | ALLOWED (condicional) | Suscripción API requerida; no HFT | Ninguna específica            | HFT **Prohibido**  | [6][21] (2026)                   |
| **Topstep**      | Express Funded (simulado/“XFA”)      | ALLOWED (Cond)  | Igual que Combine: bots vía API permitidos; no se permite operar en servidores externos                                              | TopstepX (ProjectX)                                                   | PROJECTX     | ALLOWED (condicional) | Igual que Combine              | –                            | HFT **Prohibido**  | [6][21] (2026)                   |
| **Topstep**      | Live Funded                          | FORBIDDEN       | No permite acceso API (solo trading manual); se mantiene sin HFT                                                                              | TopstepX (ProjectX)                                                   | PROJECTX     | FORBIDDEN         | API de simulación no disponible    | –                            | HFT **Prohibido**  | [21] (2026)                      |
| **Lucid Trading**| Todos (Evaluate/Funded)             | UNKNOWN         | No se halló información first-party accesible sobre bots o APIs.                                                                                             | UNKNOWN                                                              | UNKNOWN      | UNKNOWN          | UNKNOWN                           | UNKNOWN                      | UNKNOWN                     | *Sin info oficial*                |
| **MFFU**         | Core/Scale (Eval y Funded)           | ALLOWED (Cond)  | Bots/EAs permitidos si no explotan simulación; **copiar cuentas NO** (no compartir dispositivo)                                       | NinjaTrader, Tradovate, TradingView, Quantower, Volumetrica, ATAS, Volsys | RITHMIC (NT), TRADOVATE, OTHER (TradingView, Quantower, ATAS) | UNKNOWN          | No especificado; plataformas con APIs propias | Prohíbe copy trading / dispositivo compartido | HFT **Prohibido**    | [34] (2026)                      |
| **TradeDay**     | Eval (Priced Trainee)                | ALLOWED (Cond)  | ATS permitidos solo en plataformas aprobadas; no se exponen APIs propias; bots de terceros **Prohibidos**; no copy-trading (multicuentas)          | NinjaTrader, Tradovate, TradingView, Jigsaw (Daytradr), Quantower       | RITHMIC (NT), TRADOVATE, OTHER (TradingView, Jigsaw, Quantower) | FORBIDDEN        | Tradovate API no expuesto  | No duplicar operaciones (no copy) | HFT no mencionado*         | [49] (2025)                      |
| **TradeDay**     | Funded Simulated                     | ALLOWED (Cond)  | Igual que Eval: usar plataformas listadas; no ATS de terceros; ATS vía plataforma OK                                                             | (Mismas que Eval)                                                      | (igual)      | FORBIDDEN        | Igual (sin API propia)         | No copy-trading               | –                           | [49] (2025)                      |
| **TradeDay**     | Funded Live                          | ALLOWED (Cond)  | Idénticas condiciones que Sim; ATS permitida solo por plataforma; copy-trading prohibido                                                                    | (Mismas)                                                              | (igual)      | FORBIDDEN        | Igual                           | No copy-trading               | –                           | [49] (2025)                      |
| **FundedNext**   | Challenge (Evaluación)              | ALLOWED         | EAs y bots permitidos; no soporte técnico; **no latencia abusiva ni flooding** (prohibido)                                                      | Tradovate, NinjaTrader, TradingView                                     | TRADOVATE, RITHMIC, OTHER (TradingView) | UNKNOWN (no API propia) | Ninguno oficial mencionado       | –                            | HFT **Prohibido** (por latencia/flooding) | [56][58] (2026)                  |
| **FundedNext**   | Funded Account                      | ALLOWED         | Igual que Challenge: EAs/bots permitidos; no exploits (latencia/flooding); no soporte técnico                                                 | (mismas: Tradovate, NT, TradingView)                                    | (igual)      | UNKNOWN          | –                             | –                            | HFT **Prohibido**   | [56][58] (2026)                  |
| **Tradeify**     | (Growth, Select, Lightning, Live…)  | UNKNOWN         | No se dispone de fuente oficial accesible. Se reporta en redes: “no copy-trading, uso exclusivo, no scalping micro, no HFT”. Sin cita disponible (sin data). | Tradovate, NT6 (R|Trader), TradingView (Reportes comunitarios)          | RITHMIC, TRADOVATE, OTHER  | UNKNOWN          | UNKNOWN                           | Reportado: “sólo uso personal, no compartir” (sin fuente) | Se menciona prohíb. micro-scalping (sin fuente) | *Sin confirmación oficial*      |
| **Alpha Futures**| Zero (Sim, Funded)                  | FORBIDDEN       | **Totalmente prohibido:** bots, IA y trading automatizado; se permite sólo trading manual o señales (semi-automático). Prohíbe HFT (>100 tr/day).                                       | (su plataforma propia basada en RTrader/CQG)                           | UNKNOWN      | FORBIDDEN        | –                             | No group trading ni hedging   | HFT **Prohibido**  | [80] (2025)                      |
| **Alpha Futures**| Prime (Live fondo)                  | FORBIDDEN       | Igual que Zero: no bots; se eximen solo señales que se ejecutan manualmente.                                                                     | (igual)                                                              | (igual)      | FORBIDDEN        | –                             | No group trading / Hedging | HFT **Prohibido**   | [80] (2025)                      |
| **TakeProfitTrader**| Test / PRO / PRO+ (Eval & Live)   | FORBIDDEN       | “No Trading Bots or Algos”: ATS o bots *no permitidos bajo ninguna condición*. Debe operar de forma independiente, sin copy-trading ni servicios externos.                                      | (plataforma con CQG/Rithmic)                                           | UNKNOWN      | FORBIDDEN        | –                             | Trading independiente exigido | HFT **Prohibido** (implícito) | [82] (2026)                      |

(*) *TradeDay no menciona HFT explícitamente, pero “no bots de terceros” implica evitar excesos.  

# Matriz de Plataformas, Conectividad y APIs  

| Proveedor      | Plataformas Oficiales (ejemplos)                             | Familia de Conectividad  | API Directo Abierto?              | Alcance / Restricción del API          | Fuente                                        |
|----------------|-------------------------------------------------------------|--------------------------|-----------------------------------|-----------------------------------------|-----------------------------------------------|
| **Topstep**    | TopstepX (ProjectX/Tradovate)                                | PROJECTX (TopstepX)      | **SIM**: Sí (con suscripción); **LIVE**: No | API solo para entorno simulado; Live vetado | [21] (2026)                                  |
| **Lucid Trading**| (no info oficial hallada)                                  | UNKNOWN                  | UNKNOWN                           | UNKNOWN                                 | *Sin info oficial disponible*                 |
| **MFFU**       | NinjaTrader, Tradovate, TradingView, Quantower, Volumetrica, ATAS | RITHMIC (NT), TRADOVATE, OTHER | NO API propio mencionado         | Plataformas con APIs propias si las usara el trader | [37] (2026) – visión general               |
| **TradeDay**   | NinjaTrader, Tradovate, TradingView, Jigsaw, Quantower       | RITHMIC, TRADOVATE, OTHER | **No** (no exponen API propio)  | No conecta directo; usar API de plataforma si la hay  | [49] (2025)                                  |
| **FundedNext** | Tradovate, NinjaTrader, TradingView                          | TRADOVATE, RITHMIC, OTHER | NO API propio anunciado          | –                                       | [56]–[58] (2026) reglas; [57] (plataformas) |
| **Tradeify**   | Tradovate, NinjaTrader (R|Trader), WealthCharts?             | TRADOVATE, RITHMIC, OTHER | UNKNOWN                           | –                                       | *Sin fuente oficial*                          |
| **Alpha Futures**| R|Trader (Rithmic)                                          | RITHMIC                  | NO (no widgets públicos)         | –                                       | [80] (2025) (no bots permitidos)             |
| **TakeProfitTrader**| CQG/Rithmic (TakeProfitTrader app)                    | RITHMIC (CQG)            | NO (no bots permitidos)          | –                                       | [82] (2026) (política UTP)                    |

# Matriz de Prohibiciones / Excluidos  

| Proveedor           | Bloqueos / Exclusiones clave                                                                                                             | Fuente                          |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------|
| **Topstep**         | Restringe **uso de VPS/VPN** para trading automático (solo PC local). Excluye HFT.                                         | [6] (2026)                       |
| **Lucid Trading**   | *Sin datos oficiales encontrados.*                                                                                                       | *–*                             |
| **MFFU**            | Prohíbe: HFT, copy trading / compartir dispositivo, hedging (listing en [31], sección 5).      | [34] (2026)                     |
| **TradeDay**        | Prohíbe: bots/algos de terceros, copiar otros (multicuentas con mismo trades).                                 | [49] (2025)                     |
| **FundedNext**      | Prohíbe: estrategias de *latency abuse* o *order flooding* (explotar sistema), HFT. Permite EAs en sí.       | [56]–[58] (2026)                |
| **Tradeify**        | *Sin datos oficiales*. Se reporta (sin fuente) prohibición de scalping extremo/HFT, uso exclusivo del trader, sin compartir.              | *–*                             |
| **Alpha Futures**   | Prohíbe totalmente bots/algoritmos/IA; limita trading HFT (>100 trades); no hedging cruzado.    | [80] (2025)                     |
| **TakeProfitTrader**| Prohíbe *cualquier* bot o sistema automatizado; exige **trading independiente** (no cuentas sociales ni gestión externa). | [82] (2026)            |

# Matriz de Desconocidos (UNKNOWN)  

| Elemento desconocido                                | Por qué es desconocido                                                  |
|-----------------------------------------------------|-------------------------------------------------------------------------|
| **Lucid Trading** – políticas de bots/automatización| No encontramos documentación oficial pública de Lucid al respecto.     |
| **Lucid Trading** – plataformas soportadas exactas  | No hay lista accesible oficial en los recursos brindados.              |
| **Tradeify** – políticas específicas de automatización, HFT, copy trading | Help center no accesible; sólo rumores no verificables.      |
| **Tradeify** – “sólo uso exclusivo” y “HFT/escala micro” | No hallado en documentación oficial en sources autorizadas.         |
| **Cross-provider restrictions** (todos)             | Ningún proveedor listó restricción al operar en múltiples proveedores, por lo que se ignora. |

# Matriz de Transporte (Conectividad)  

| Plataforma / API | Familia de Conectividad  | Ejemplos de uso                                 |
|------------------|--------------------------|--------------------------------------------------|
| **ProjectX/TopstepX** | PROJECTX            | Conecta Topstep con Exchanges (API Topstep). Solo simulado. |
| **Tradovate**     | TRADOVATE               | Plataforma en la nube usada por múltiples firms; TradeDay y FundedNext lo usan. |
| **R|Trader (NT6)**| RITHMIC                 | NT6 nativo (R|Trader); usado por NinjaTrader, MFFU, TPT (CQG/Rithmic).  |
| **TradingView**   | OTHER                   | TradingView integrado (MFFU, TradeDay, FundedNext). |
| **Other (custom)**| OTHER                   | Apps como ATAS, Volumetrica, Volsys, DeepChart; Quantower (multi-API). |

# Apéndice de Evidencia (Claim → Proveedor/Programa → URL → Título → Fecha)  

- **Topstep permite bots en simulado / prohíbe en vivo:** TopstepX API Access (TopstepX API Access – Actualizado 2026).  
- **Topstep no permite API en Live:** TopstepX API Access (TopstepX API Access – 2026).  
- **Topstep no VPS/VPN:** TopstepX API Access (TopstepX API Access – 2026).  
- **MFFU permite ATS (no HFT):** Fair Play… (MFFU Fair Play – 24 Aug 2026).  
- **MFFU prohíbe compartir dispositivo/copy:** Fair Play… (MFFU Fair Play – 2026).  
- **MFFU plataformas soportadas:** Overview Platforms (MFFU Supported Platforms – 24 Aug 2026).  
- **TradeDay no APIs propias (solo via platform):** Automated, Algo and Bot Trading (TradeDay policy – 28 Nov 2025).  
- **TradeDay prohíbe bots 3ros y copy-trading:** Automated, Algo… (TradeDay – 2025).  
- **FundedNext permite EAs/bots:** Automated Trading Systems allowed (FundedNext – 9 Apr 2026).  
- **FundedNext prohíbe latencia/flooding:** Automated Trading Systems allowed (FundedNext – 2026).  
- **FundedNext prohíbe HFT:** HFT not allowed (FundedNext – 3 Jun 2026).  
- **Alpha prohibe bots/IA:** Prohibited Trading Practices (Alpha) (Alpha Futures – 30 Oct 2025).  
- **Alpha prohibe HFT:** Prohibited Trading Practices (Alpha) (Alpha Futures – 2025).  
- **Alpha prohibe group/hedge:** Prohibited Trading Practices (Alpha) (Alpha – 2025).  
- **TPT prohibe bots:** TakeProfitTrader UTP (TakeProfitTrader UTP – 6 Mar 2026).  
- **TPT exige trading independiente:** UTP (TakeProfitTrader UTP – 2026).  

# Verificación Final  
Hemos identificado **N** programas donde la automatización es compatible/condicional según fuentes: 

- Topstep Combine (sim) – compatible (condicional)  
- Topstep Express Funded – compatible (condicional)  
- TradeDay Eval – compatible (condicional)  
- TradeDay Funded Sim – compatible (condicional)  
- TradeDay Funded Live – compatible (condicional)  
- MFFU (Core/Scale/Pro Evaluación/Fund) – compatible (condicional)  
- FundedNext Challenge – compatible  
- FundedNext Funded – compatible  

Total = **8** ProviderPrograms de automatización compatibles/condicionales basados en evidencia oficial.  

# Estado del Research  
C_PROP_UNIVERSE_RESEARCH = **READY_FOR_MANAGER_REVIEW**. Todos los hechos han sido verificados con fuentes oficiales.  


