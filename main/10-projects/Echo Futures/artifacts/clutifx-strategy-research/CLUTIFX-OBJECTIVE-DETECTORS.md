# CLUTIFX-OBJECTIVE-DETECTORS — Detectores estructurales v1.0 (RECONSTRUIDO)

Proyecto: Echo Futures · Misión CLUTIFX GOD (2026-10-23) · Congelado en GATE P1

> **PROVENANCE:** Reconstruido desde claims SUPPORTED MKE (compilación `mke-strategies.md` §B). Regularizaciones de mandato §3.1–§3.4 aplicadas (ver STRATEGIES-MASTER). 

## Contrato de ingeniería de cada detector

Todo detector del paquete `clf` debe ser: determinista (sin relojes/IO/aleatoriedad — lo exige el contrato `Strategy`), causal (sólo barras cerradas hasta `decision_time`; sembrado de contraejemplos con lookahead deliberado en conformance tests), reutilizable (estrategias lo componen), configurable (params tipados vía `DecodeConfig`), compatible con warmup (estado `NOT_READY` con razón) y **diagnóstico**: cada activación/no-activación emite `TechnicalDiagnostic` con la regla citada (chNN, c-XXXX) y el estado del detector.

## Regularización del eje "reacción" (mandato TIER 2 "R1/R3/R4")

**La taxonomía R1/R3/R4 NO existe en la fuente** (verificado ch04 rules/documentation/concepts/claims — NOT_IN_SOURCE). Se sustituye por la taxonomía causal real de resolución de reacción del TS (3 modos, todos citados):

| Modo | Regla fuente | Emisión causal |
|---|---|---|
| `TS_CLOSE` (control) | confirmación por cierre de la vela base dentro del rango (ch01 R1·c-0005 clásico) | al cierre de la vela del TF base |
| `TS_EARLY_1M` (S01) | tras TS + reacción NO hace falta el cierre (ch02 R5·c-0035; ch04 R6·c-0027) | primer cierre 1m contra la dirección del sweep |
| `TS_M30` (S02) | duda en 15m porque la 4h no cerró → confirmación en M30 (ch04 R23·c-0099) | cierre de la vela M30 |

S17 queda redefinido como confirmación por **mecha de la vela siguiente** (ch09 c-0035/c-0036: la siguiente vela toma el extremo y reacciona dejando mecha) — modo `TS_WICK_NEXT`, causal (requiere cierre de la vela siguiente).

## B. Detectores compartidos
## B. Detectores compartidos

### B1. Rango — creación, extensión, completitud, eliminación, estados
- Creación: vela (NO necesariamente la siguiente) toma un extremo de la vela anterior y cierra dentro (ch01, R1·c-0005). Refinamiento: tras TS + reacción NO hace falta el cierre para considerarlo rango (ch02, R5·c-0035; ch04, R6·c-0027).
- Extensión (regla direccional): tomado extremo y cerrado dentro, normalmente el precio va al otro extremo (ch01, c-0025); "siempre—no siempre" (c-0031); el precio se mueve por rangos "siempre" como hallazgo del equipo (c-0016) y actúa como cadena (c-0017).
- Completitud: el rango completa cuando toma low Y high (ch01, R21·c-0078); objetivos/rangos completados se borran (ch02, R7·c-0037, c-0038).
- Eliminación: cierre fuera del rango → eliminado (ch01, R20·c-0076, c-0077; ch02, R6·c-0056); tras eliminar: olvidar y esperar nueva vela que abra/tome low/forme rango nuevo (ch01, R23·c-0079, c-0080).
- Matices: cierre apenas fuera que "parece prácticamente dentro" se considera rango (ch07, R13·c-0065; ch08, R18·c-0010); los cuerpos respetan el low aunque cierre afuera (ch03, R12·c-0054, c-0108); apertura por debajo/arriba puede formar rango bullish/bearish (ch03, R13·c-0097, c-0182, c-0100, c-0118); rango que cierra por fuera "un poco" → mejor no marcarlo como objetivo (ch05, R13·c-0044).
- Estados: "no tenemos nada" = sin rango en esa TF (ch02, R8·c-0049); rangos enfrentados en un TF → ignorar ese TF y bajar (ch08, R5·c-0050, c-0052).
- Rangos contrarios antes del objetivo: el precio no va directo, "tiene que completar los [contrarios] primero" (ch02, R9·c-0051–c-0053). TENSIÓN/CONFLICT (resoluble, decidir en implementación): ch03, R11·c-0094, c-0096 — NO hace falta completar TODOS los contrarios al bias ("con que el de 6h complete y el de 8h no, basta"; c-0214: rango alcista ya innecesario si se formó bajista y el DOL sigue intacto). ch02 exige completar los contrarios inferiores antes del objetivo; ch03 acota que no todos. CONFLICT de alcance, no de dirección.

### B2. Pendiente vs reiniciado
- Pendiente (a favor): abre por debajo, toma el low, cierra adentro o reacciona (ch01, R9·c-0041); "a favor de nuestra tendencia" (R10·c-0042); 8h: sin tomar extremo (R14·c-0054); habilita entrada (ch03, c-0087, c-0190).
- Reiniciado (en contra): abre por arriba, toma el high, cierra adentro → rango bajista (ch01, R11·c-0044, c-0045); abre en contra del objetivo (R12·c-0049; R13·c-0055).
- Lectura de aperturas (ch09): "abrir por abajo" = la vela toma el LOW de la anterior (crea rango a favor → long para la siguiente); "abrir por arriba" = toma el HIGH (c-0020–c-0023); no es la dirección de la apertura en sí.
- La vela que toma el extremo NO tiene por qué ser la inmediatamente siguiente (ch01, c-0005).

### B3. DOL — identificación y "objetivo tomado"
- DOL = objetivo/liquidez al que va el precio (GLOSARIO; ch02, c-0099, c-0100; ch03, c-0070). Identificación: rangos de TF más alta + vela de la izquierda predominando → ir para allí (ch03, R8·c-0070).
- DOL sesión: 12h/8h/6h/4h; DOL medio plazo: 3D/2D/1D (ch03, R2·c-0207, c-0208); mensual/semanal = sólo contexto (c-0206, c-0051).
- Objetivo tomado: detectable por el checklist (ch07, c-0229 "¿está el doll tomado?"); peor situación al llegar a London (c-0039); a las 5, el precio toma el low/high según el DOL: DOL bearish → sigue; DOL bullish → toma el low, crea rango bullish y sube (ch02, c-0099).
- Para noticias: DOLs intactos = vía libre; tomado → menor volatilidad o reversal (ch10, c-0122, c-0193, c-0194).

### B4. HTF bias
- El bias lo dan las TFs altas: 6h, 8h, 12h, 1D, 2D, 3D (ch03, R1·c-0050).
- Jerarquía: mensual/semanal → contexto HTF; 3D/2D/1D → medio plazo; 12h/8h/6h/4h → DOL de la sesión; <4h → entradas y momento (ch03, R2·c-0206–c-0209).
- "HTF manda": comprar en TF inferior con la vela superior sin rango creado → stop; el precio crea primero el rango superior (ch02, R16·c-0086–c-0088, c-0100); en 8h y 12h hay que tener los rangos ya a favor (ch07, R26·c-0234, c-0235).
- Procedimiento multi-TF: marcar rangos en todas las TFs y comprobar que "estén en dirección a lo mismo" (ch02, R10·c-0054, c-0040, c-0045); entrar desde la TF más alta e ir bajando (ch08, R1·c-0002, c-0022, c-0069); "solo time-based" sin DOL/bias = operar en ciego (ch03, R3·c-0144).
- Días de bias bloquean la dirección contraria aunque el DOL esté a favor (ch03, c-0212).

### B5. Turtle Soup
- Definición: tomar el alto/bajo para crear o completar un rango Y tener la reacción después hacia el otro lado (ch01, R15·c-0059).
- Condición necesaria: si sigue en la dirección de la toma, NO es TS (ch01, R16·c-0063); posibles fintas (R17·c-0064).
- Refinamiento ch02: tras TS + reacción no hace falta que la vela cierre (ch02, c-0035; ch04, c-0027).
- Stop: debajo/sobre el TS (ch01, c-0067; ch03, c-0164; ch04, c-0048; ch07, c-0109; ch10, c-0060).
- Siempre se quiere un TS a favor de la tendencia (ch02, c-0081); sin rango activo a favor antes del TS no se compra (ch07, c-0214).
- Intra-TS: tomar + reacción + cerrar dentro del mismo rango, sobre un TS ya hecho (ch01, R19·c-0068, c-0075).

### B6. Reacción — tipos R1/R3/R4
NOT_IN_SOURCE. En ch04 no existe clasificación alguna de reacciones "R1/R3/R4" (verificado en rules.md, documentation.md, concepts.md, claims.jsonl). La "reacción" aparece sólo como condición genérica del TS (ch04, c-0027; ch01, c-0063) y como PDM ("la reacción en el alto del rango", ch04, c-0017).

### B7. Power of 3
- Definición: la vela se conforma de APERTURA, manipulación, distribución y cierre (ch01, R33·c-0116, c-0117). [Nota: la spec pedía "acumulación/manipulación/distribución"; la palabra "acumulación" NO es literal de ch01; ch09 habla de "consolidación, expansión, reversa" como tres momentos (c-0062).]
- Compras ideales en contexto alcista: en la etapa de manipulación de la vela (ch01, R35·c-0121 — "siempre, siempre, siempre").
- Procedimiento: a las 4:30 esperar a que abra la nueva vela de 4h a las 5 para entrar en el Power of 3, "punto óptimo" (ch01, R36·c-0122); equivalencia apertura-nueva vela/cierre-anterior (R37·c-0123).
- Aperturas de vela → posibles rangos nuevos (ch02, c-0024: nuevas velas = nuevos rangos y Power of 3; ch03, R18·c-0040).
- Coincidencia rango + Power 3 = entradas fuertes (ch01, R38·c-0126, c-0127); en 15m la manipulación "te puede liar" (R39·c-0128).
- En noticias: posicionarse en el Power 3 de la vela de la noticia (ch10, c-0197, c-0107, c-0116).

### B8. Failure swing — legítimo vs falso
- Legítimo: identificado por reacción + order block + UNO de los 3 motivos (SMT / extremo a final de vela / feed de otro broker) (ch06, R11·c-0029, c-0046; R7, R8, R10).
- Falso/abusivo: predecirlo mientras pasa (R2·c-0016, c-0030); asumirlo sólo por ver el extremo al final de la hora (R9·c-0011, c-0015); obsesionarse (R1).
- Rango activado aunque no tome el extremo (R5·c-0007, c-0028, c-0063); entrada sin esperar activación clásica (R6·c-0019).
- Motivo visible en 1h (otras velas "no concuerdan con el horario de apertura"); 5m da el minuto exacto (R13·c-0040, c-0036).

### B9. Inside candle
- Definición operativa: vela que no ha tomado NI el high NI el low de la vela anterior (ch09, R8·c-0084).
- Regla: "tú no haces nada: no compras, no vendes" (c-0084); baja la probabilidad (c-0026, c-0034, c-0090); aplica en cualquier TF, también 1h (c-0033).
- Habilitación: cuando la vela toma el low/alto y crea el rango (c-0085, c-0081); esperar la vela que tome algún extremo (c-0086); resolución ideal: siguiente vela toma high y reacciona dejando mecha → rango bajista + confirmación (c-0035, c-0036).
- Con noticias: inside + noticia = riesgo de whipsaw (ch10, c-0192).

### B10. Red flags (lista completa ch09, con fuerza)
1. Rangos en contra / velas que abren al revés — FUERZA DURA (dicha sin hedge, acotada al escenario): "nunca" buscar longs ahí arriba (c-0007), "no podemos estar tomando longs" (c-0012); dura hasta que el rango reinicie o cree pendiente a favor (c-0011); sobre todo en horas clave 3, 5, 8 y 9 ("quizá 8 quitaría", c-0003); a las 5, nuevo alto simultáneo en 6h/4h/3h/2h/1h/12h puede crear rangos bajistas (c-0010); gestión: parciales + break even (c-0015), cerrar y reentrar cuando vuelvan a favor (c-0078).
2. Inside candles — FUERZA DURA (pausa operativa): no hacer nada (c-0039, c-0084); ver B9.
3. Objetivo ya tomado — PROBABILÍSTICA: no entrar donde ya se tomaron objetivos (c-0040, c-0044, c-0046); "la probabilidad es mucho más baja" (c-0045, c-0101, c-0103); cada entrada es una salida (c-0048, c-0049); variante sesión: levantarse con objetivo (1D/2D/1S) ya tomado = red flag para esa sesión (c-0051, c-0053); más fácil operar hacia el objetivo que desde él (c-0052, c-0104); excepción de riesgo consciente (c-0107, c-0108, ch09 R9); venta tras objetivo clara si se formaron bajistas "por todos lados" (c-0124, c-0125).
4. Par correlacionado ya tomó su target — PROBABILÍSTICA: si un par llegó y el otro no, red flag para operar el segundo (c-0126–c-0128, c-0130, c-0131); mitigación: beneficios o break even cuando uno de los dos llega (c-0129).
5. Sesión: venir de expansión en la vela de las 21 (Asia) → London baja la probabilidad (c-0060, c-0061); secuencia deseada 1(TS)→5(expansión) (c-0057); si expande la 1, esperar TS de reversal en la 5 y expansión a las 9 (c-0058); "expansión, expansión, expansión" no [UNCERTAIN c-0063].
6. Vela de las 9 abriendo en contra → red flag para el short; tomar cuando se forme el rango 4h a favor (ch09, R7·c-0073, c-0074).
7. En noticias: mismas red flags; exigir rangos a favor, no inside, DOLs intactos (ch10, c-0189–c-0195); sin TS = red flag de whipsaw (ch10, c-0062).
- NOT_IN_SOURCE: métrica numérica de "probabilidad" (fuerzas cualitativas; el "100% que va a llegar" de c-0100 es hipérbole, ch09 documentation §8).

### B11. Confirmaciones
- Pares de confirmación según la noticia: noticias USD → pares USD en la misma dirección; pares inversos al revés; todos bullish para comprar (ch10, R6·c-0028, c-0029, c-0031; R7·c-0035, c-0036).
- Order block como confirmación de cambio de tendencia (ch04, R8·c-0039; ch01, c-0106, c-0108 — uso en M15).
- Confirmación en M30 si la 15m duda porque la 4h no cerró (ch04, R23·c-0099).
- Confirmación de rango bajista tras inside: siguiente vela toma high, reacciona dejando mecha (ch09, c-0035, c-0036).
- No entrar sin confirmación de nuevos rangos bajistas (ch08, R15·c-0084).
- DXY como confirmación: bullish en EUR → bearish en DXY, "ya os lo puedo asegurar" (ch05, c-0085; ch10, c-0186, c-0187).

### B12. Horas clave (America/New_York)
- 5:00 — abren 90m/2h/3h/4h/6h/12h: nuevos rangos y Power of 3; propensa a Turtle Soups; reversión/retracement/continuación (ch02, R3·c-0010, c-0024).
- 17:00 — igual que las 5 + vela de 8h (ch02, c-0022; c-0014: 12h abre 17 y 5).
- 3:00 — 1h+2h; intrasesión/London; expansión frecuente (ch02, R3; c-0018).
- 8:00 — aperturas USA; noticias 8:30 (ch02, R3); noticias del dólar 8:30/8:45 (ch07, c-0153).
- 9:00 — nueva vela 4h y 8h (ch02, R3; ch07, c-0145).
- Velas de sesión 4h: 21 / 17 / 1 (la 1 = London) (ch07, c-0002, c-0003); en 6h: 23 / 17 / 11 (ch07, c-0009); en 6h la 23 engloba London y la 5 engloba NY (ch02, c-0067).
- Precaución/salida en horas clave: al tomar alto/bajo en hora clave se crea rango a favor o en contra → "mejor salir con precaución y asegurar" (ch02, R4·c-0064, c-0063).
- Horas clave donde no quieres rango en contra: 3, 5, 8, 9 (ch09, c-0003).
- Entrada al gráfico: 2:30 para London (ch07, c-0006); 1:00 en día con noticia a las 2 (ch10, c-0043); "justo a las 8" antes de noticia 8:15 (ch10, c-0166).
- NOT_IN_SOURCE: tratamiento de cambio de horario (DST) — la fuente dice "hora New York (UTC-4)" (ch02, c-0012); usar America/New_York es decisión de implementación.

### B13. Salidas
- El objetivo (take profit en el objetivo/DOL) (ch04, R24·c-0113; ch08, R4: entrar antes de completados → mejor ratio).
- La nueva vela de las 5 — "punto aún más óptimo"; puede no girar y seguir hasta girar a las 5 (ch04, R24·c-0113, c-0114); salida por tiempo: si no llega al objetivo, salir en la vela de las 5 cerca del target; último parcial puede correr (ch07, R14·c-0075–c-0077).
- Entry Model: gestionar la salida por 30 minutos — si en 30m hay rango clean, usar el de 30m (ch04, c-0110). [Contenido completo del Entry Model: NOT_IN_SOURCE.]
- En vivo: salir en el alto de la nueva vela por seguridad para que no se cree rango en contra (ch04, R20·c-0091); rangos bajistas en 4h/3h/2h al llegar a la zona = salida del long (y entrada del short) (ch04, R25·c-0115, c-0117).
- Gestión: break even al ver completarse el movimiento / formarse rango en contra (ch03, R15·c-0106, c-0199; ch08, R11·c-0077, c-0080; ch08, R17·c-0044, c-0063); parciales por objetivos intermedios (ch03, c-0088), en nuevos extremos de nuevas velas (c-0166), por posible rango en contra (c-0169); break even + parciales tras completar un rango (ch09, c-0117, c-0120); BE no es razón para cerrar con objetivo claro (ch07, R17·c-0131); dos velas de 15m fuertes en contra justo al tomar → salir (ch08, R13·c-0068); SMT/DXY: salir o parciales si DXY toma objetivo antes (ch05, c-0096, c-0097).
- Horas clave: salir con precaución (ch02, R4).

### B14. Order block / PDM
- Order block: una vela alcista que CIERRA por fuera de la última vela bajista (sobre tendencia bajista; espejo para shorts) (ch01, R30·c-0107).
- Entrada: una vez la vela cierra por fuera → tomar long (ch01, R32·c-0110, c-0112; ch04, R7·c-0034); confirma que "el precio ya no baja más", aunque no es la ideal (ch04, c-0036); uso del instructor para confirmaciones en TF baja, M15 (ch01, R31·c-0106, c-0108).
- Tras failure swing: el order block creado tras el fallo puede ser el cambio de tendencia; en 15m se puede esperar (ch06, R12·c-0038, c-0041, c-0047).
- PDM (ch03 lo define): en alcista, el precio se apoya en el low del rango sin romperlo y lo usa de soporte para subir (ch03, R14·c-0092); con PDM + reacción alcista NO se vende aunque el DOL esté abajo (c-0213). Uso espejado en bajista: "la reacción en el alto del rango" (ch04, c-0017); entrada de short exigiendo respeto del nivel (ch04, R22·c-0096, c-0097); "no pasan muchas veces" (c-0096). Expansión de la sigla: NOT_IN_SOURCE (q-ch03-004).
- Orden de precedencia en entradas: TS → PDM/order block → Power 3 de TF menor + pendiente (ch04, R4).

---

## Fixtures obligatorias de conformance (P2)

Para cada detector: secuencias OHLC controladas con `input bars / known information at decision_time / expected detector state / expected Signal / expected technical stop / expected lifecycle transition`. Casos mínimos: rango con vela NO adyacente (1 y varias intermedias); rangos superpuestos y enfrentados (TF ignorada, ch08 R5); orden completitud vs invalidación (cierre fuera vs low+high); DOL ya tomado; TS sin reacción; sweep con reacción posterior; expansión sin confirmación causal; pivot no confirmado; FS legítimo (3 motivos) vs falso; señal antes de cierre válido (debe FALLAR); LONG vs SHORT espejo; cruces de sesión y DST; cambio de contrato (rollover, CycleAware); warmup insuficiente (NOT_READY); gaps; config inválida (error); rearme/reentrada; emisión duplicada (rechazada); decisiones simultáneas (orden determinista).
