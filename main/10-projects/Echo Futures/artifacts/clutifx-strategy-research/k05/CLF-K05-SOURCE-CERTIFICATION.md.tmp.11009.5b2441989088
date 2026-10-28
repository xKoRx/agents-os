# CLF-K05 — SOURCE CERTIFICATION (FASE 1 · reconstrucción de reglas)

Misión: CLF-K05 · Fecha: 2026-10-26 · Autoridad: claims vigentes `ACTIVE ∧ SUPPORTED` de `knowledge-library/clutifx/ch01..ch12` (la capa por capítulos es la autoridad; `strategies/STRATEGIES-CATALOG.md` SHA `4c471314…` es superficie derivada re-domiciliada y VERIFICADA presente — corrige el hallazgo §6 de Q04 que la daba por ausente). Clases: `SOURCE` = enseñado; `OP` = operacionalización necesaria (no enseñada, declarada); `HIP` = hipótesis experimental; `UNRESOLVED` = evidencia insuficiente.

Regla de lectura aplicada: el lenguaje probabilístico del instructor («normalmente», «a lo mejor», «seguramente», «yo creo») se preserva como contexto, jamás como condición obligatoria; los ejemplos no se generalizan sin sustento; ningún OR de escenarios se implementa como AND.

## STR-001 — London ideal (P3 de la vela de la 1 tras TS hecho)

```text
STRATEGY_ID: CLF-STR-001 · familia FAM-001 · variante C01
SOURCE: ch07 §3 (c-0010 escenario ideal, c-0005–c-0007 entrada 2:30, c-0030/c-0061 la vela de London que hace el TS no expande, c-0038 preferencia TS-vela-siguiente, c-0214 rangos activos a favor SÚPER CLAVE); ch02 c-0081 (TS siempre a favor); ch01 c-0121/c-0122 (compras en la manipulación del P3); ch09 c-0060/c-0061 (red flag Asia); ch07 c-0229 checklist.
MARKET_CONTEXT: Forex mayor enseñado (EURUSD/GBPUSD/GBPJPY). NQ: NQ_ADAPTATION_HYPOTHESIS.
SESSION: vela 4h de la 01:00 NY (marco 21/17/1); llegada al gráfico 2:30 (c-0006).
TIMEFRAMES: análisis 1 año→15m; ejecución 4h→1h→15m.
PRECONDITIONS: bias derivado [SOURCE ch03]; DOL de sesión intacto [SOURCE]; TS a favor YA hecho antes de la vela de London (a menudo vela diaria o 21/1) [SOURCE c-0010]; sin rango reiniciado en contra activo [SOURCE ch03 c-0029/c-0056, ch09 c-0007 duro].
SETUP: la vela de la 1 operable; si ya hizo un pequeño P3, entrar en el tramo en curso [SOURCE c-0006].
CONFIRMATION: aperturas tomando el extremo A FAVOR (CMP-019) [SOURCE ch09 c-0021/c-0022]; cuerpos hacia el rango [EXAMPLE ch03 c-0108 — no obligatoria].
ENTRY: en la manipulación del P3 de la vela de la 1 [SOURCE c-0121]; refinada por TFs hasta 15m [SOURCE STR-005 transversal].
STOP: bajo el TS [SOURCE ch01 c-0067; ch11 c-0021/c-0023].
TARGET: el DOL [SOURCE].
EXITS: DOL o vela de las 5 [SOURCE ch04 c-0113/c-0114; ch07 c-0075–c-0077].
INVALIDATION: cierre fuera del rango base [ch01 c-0076]; completitud low+high [ch01 c-0078]; rango en contra [ch09].
REENTRY: intra-TS STR-009 [ch11 c-0024/c-0025].
RED_FLAGS: 4 de ch09 + Asia-expansion + DOL-tomado-probabilístico [SOURCE].
REQUIRED_DATA: 1m NQ suficiente [OP]; ancla de sesión a congelar [UNRESOLVED Owner: KRR-001].
MANDATORY: TS previo, DOL a favor e intacto, rangos a favor, sin adversos, red flags, stop bajo TS.
OPTIONAL: refinado al P3 exacto; cuerpos-confirmación [ejemplo].
RECOMMENDATIONS: llegar 2:30; preferencia del instructor TS en la vela previa.
SOURCE_AMBIGUITIES: el ancla horaria FX no existe en NQ (estructura); la definición intrabar de «reacción» y del P3.
OPERATIONALIZATION_REQUIRED: ventana [01:00,05:00) ET [OP implementada]; emisión en cierres causales [OP]; P3 proxy = apertura de vela [OP declarada].
NQ_ADAPTATION_REQUIRED: ancla CME/cash como identidad NUEVA (S06/S07 precedentes) — decisión Owner.
GAP_MATERIAL_K05: el refinado de la entrada NO es expresable sobre los specs de sesión (config.go rechaza RefineTF fuera de STR-002) — el curso define el refinado como transversal a STR-001..004 (F-K05-06).
```

## STR-002 — Rango pendiente hacia el DOL (familia maestra)

```text
STRATEGY_ID: CLF-STR-002 · FAM-001 · control C02
SOURCE: ch07 c-0024/c-0032 (escenario 3), c-0091/c-0113/c-0114 «precisión máxima», c-0038; ch04 c-0021/c-0023 (3ª entrada del esquema); ch03 c-0087/c-0012/c-0190; ch01 R1/R9/R10/R15/R20/R21/R23 (átomo rango, pendiente, TS, eliminación, completitud); ch09 c-0007 (adversos duro).
MARKET_CONTEXT: NQ_DIRECTLY_TESTABLE.
SESSION: no anclada a sesión en fuente; el eje de ancla es experimental (S06/S07).
TIMEFRAMES: cadena 4h nativa del control [OP/eje S10]; objetivo 4h [OP/eje S11=1d midterm].
PRECONDITIONS: TS ya pasado (a menudo diario); expansión primera ocurrida; DOL claro.
SETUP: rango PENDIENTE a favor formándose hacia el DOL (pullback) [SOURCE c-0041/c-0042]; variante 8h sin tomar extremo [SOURCE ch01 c-0054].
CONFIRMATION: el TS del propio pendiente (sweep + reacción) [SOURCE c-0059/c-0063].
ENTRY: «en la vela siguiente al pendiente» [SOURCE ch03 c-0190]; refinado opcional a 15m [SOURCE].
STOP: bajo el TS/pendiente [SOURCE c-0067]. TARGET: el DOL [SOURCE]. EXITS: DOL o vela de las 5 [SOURCE].
INVALIDATION: pendiente → reiniciado (cierre al otro lado) [SOURCE]; objetivo tomado antes de entrar [red flag 3].
REENTRY: STR-009 [SOURCE, límite no enseñado ⇒ UNRESOLVED max_reemissions=OP].
RED_FLAGS: 4 de ch09.
MANDATORY: rango a favor, TS con reacción, DOL alineado, adversos no activos, stop en el sweep.
OPTIONAL: refinado; variante 8h.
SOURCE_AMBIGUITIES: TF del objetivo (4h vs 1D) — eje declarado; conflicto ch02 R9 vs ch03 R11 sobre contrarios resuelto en COVERAGE (bloqueo de activos vs ordenación del recorrido) [decisión vigente, revisada K05: sostiene].
OPERATIONALIZATION_REQUIRED: leftmost_unbroken [OP basada en c-0005+c-0059]; tolerancia «cierra dentro» base 0 [OP; matiz c-0065 como variante]; compositor 1m→HTF anclado NY [OP]; DST IANA [OP declarada].
VEREDICTO IMPLEMENTACIÓN: FIEL en maquinaria (pipeline, TS 4 modos, DOL, bias nativo, red flags, stop, salidas) con las reducciones declaradas: bias {1d} vs fuente 6h–3D; DOL sesión {4h} vs 12h/8h/6h/4h (F-K05-09, bloqueo de capacidad del motor, no de conocimiento).
```

## STR-003 — NY continuación (vela de las 9)

```text
STRATEGY_ID: CLF-STR-003 · FAM-001 · control C03
SOURCE: ch07 §5 (c-0134, c-0145 condición, c-0146, c-0160/c-0161, c-0166–c-0168 «cómo abren las velas», c-0054 TS formado a las 9 válido); ch09 c-0057–c-0059 (secuencia 1-5-9); ch09 c-0073 (9 abre en contra = red flag).
PRECONDITIONS: DOL NO tomado tras London [SOURCE c-0067]; rangos ya creados; TS por vela ANTERIOR (la de las 5) o formado a las 9 (c-0054); 5:00 sin cerrar en contra [SOURCE c-0166–c-0168].
ENTRY: subirse al movimiento en la vela de las 9 [SOURCE c-0145]; «mejor zona» por incertidumbre 9-vs-siguiente [c-0160/c-0161].
STOP/EXIT: ídem familia [SOURCE]; salida base del control: objetivo [OP matriz; ver discrepancia con S08 abajo].
INVALIDATION: 5 cierra en contra completando el rango → sin expansión hoy [SOURCE]; DOL tomado.
RED_FLAGS: + 9-abre-en-contra [SOURCE].
GAP_MATERIAL_K05: si el rango se ACTIVA POR FAILURE SWING (ch07 c-0197–c-0206: el caso de las 9 del curso ES un FS que reinicia el rango de 8h), el día no produce señal porque la entrada exige sweep clásico (F-K05-07).
DISCREPANCIA_MATRIZ: S08 declara «C03 base temporal» pero el código fija C03 exit base = target (config.go:259) — conciliar antes de materializar S08 (F-K05-12).
```

## STR-004 — NY reversal (vela de las 5 tras objetivo completado)

```text
STRATEGY_ID: CLF-STR-004 · FAM-001 · control C04
SOURCE: ch07 c-0147/c-0148/c-0150 (6–8h acota); ch02 c-0068/c-0076; ch08 c-0084/c-0051 (anti-regla de venta); ch01 c-0025 (el rango corre a su otro extremo); ch09 c-0045 (objetivo tomado = probabilístico, no bloqueo).
PRECONDITIONS: objetivo COMPLETADO durante London [SOURCE c-0147]; vela de las 5 toma el low/high anterior y crea rango OPUESTO [SOURCE c-0148].
ENTRY: en la vela de las 5, dirección contraria al objetivo completado [SOURCE]; o esperando el TS del rango nuevo.
STOP: bajo el extremo del reversal [SOURCE por espejo c-0067/c-0164]. TARGET: extremo opuesto del rango creado acotado por 6–8h [SOURCE c-0150; V1 usa la cadena 4h — reducción declarada].
INVALIDATION: la 5 cierra alcista completando el rango previo → esperar día siguiente [SOURCE c-0168].
NOTA IMPLEMENTACIÓN: C04 no lleva puerta de bias — correcto (la reversión va CONTRA el movimiento completado; una puerta nativa la mataría); objetivo tomado pasa como flag probabilística no bloqueante [SOURCE ch09].
GAP_MATERIAL_K05: ídem F-K05-07 (el ejemplo NY del curso pasa por FS).
```

## STR-005 — Refinado multi-TF (procedimiento transversal, NO estrategia independiente)

```text
STRATEGY_ID: CLF-STR-005 · overlay de entrada
SOURCE: ch04 §2 (c-0007–c-0014, c-0063–c-0069); ch08 c-0022/c-0069; ch07 c-0214.
REGLA CLAVE: «esperar rangos activos a tu favor antes del TS» (c-0214, «súper clave»).
ESCOALA: 8h→4h→1h→15m bajando TF a TF buscando el MISMO fenómeno [SOURCE c-0013]; límite personal «nunca bajo de 15» (c-0011) vs «hasta 5 minutos para la entrada más perfecta» (c-0067) — TENSIÓN declarada; piso conservador 15m [decisión vigente].
STOP: bajo el TS de la TF de entrada [SOURCE].
HALLAZGO K05: en el código el refinado vive SOLO sobre SpecRangeDOLV1 y como UN salto (setup TF → 15m/30m), no como escalera; la fuente lo define transversal a STR-001..004 y escalonado (F-K05-06; el salto directo es OP, la restricción de specs contradice fuente).
```

## STR-006 — Failure swing

Ver adjudicación completa: `CLF-K05-FAILURE-SWING-ADJUDICATION.md`. Resumen del certificado: definición c-0004/c-0046 (falla el nuevo extremo y va directo al otro lado); rango activado sin toma «en algunos casos» (c-0028); identificación canónica = reacción-creando-rango-opuesto + UNO de 3 motivos (c-0029), OB opcional (c-0047); no predecible (c-0016/c-0030); extremo-final-de-vela solo NO basta (c-0011/c-0015); objetivo = rango de la vela fallida (c-0007/c-0063); rangos a favor para operarlo (c-0058–c-0060); 1h mejor TF del motivo (c-0040, creencia dicha); entrada refinable 30/15 (c-0013).

## STR-007 — SMT (casos 1 y 3)

`MULTI_INSTRUMENT_DATA_REQUIRED` + `FX_NATIVE` fiel. Definición redefinida ch05 c-0002 (rangos completados no percibidos); caso 1 c-0069–c-0072; caso 3 c-0078–c-0083; negación clave c-0076; DXY −1 c-0085, salida anticipada c-0096/c-0097; sin preferencia de par (c-0019). PROHIBIDO sustituto NQ (matriz). Sin cambio K05. El seam de motivo-FS-SMT ya existe y es nil fail-closed — correcto.

## STR-008 — Noticias (variantes A y B)

`NQ_ADAPTATION_HYPOTHESIS` + `RUNTIME_GAP` calendario. Núcleo: la noticia acelera hacia el DOL (c-0026), se opera la vela que la contiene (c-0023), entrada en el P3 de esa vela (c-0107/c-0116), BE al llegar con posición (c-0097), dolls intactos (c-0193), sin TS previo = red flag whipsaw (c-0062), FOMC evitar (c-0015). Variante B posicionarse antes (c-0039–c-0043). Sin calendario con timestamp ⇒ BLOCKED_DATA (verificado físicamente; KRR-006 sostiene). Sin cambio K05.

## STR-009 — Reentrada intra-TS

`NQ_DIRECTLY_TESTABLE` con cota: la regla fuente es stop-físico-golpeado + vela vuelve a cerrar dentro del mismo rango (ch11 c-0024/c-0025; ch01 c-0068–c-0077, c-0070 «si la vela sigue cerrando dentro, el rango sigue operativo»). El contrato Strategy es account-agnostic: el stop físico no es observable en la Strategy ⇒ C07 implementa rearme técnico por presupuesto (`max_reemissions`), declarado NO-equivalente (matriz). La regla fuente plena pertenece a la costura Strategy×MM/engine — trabajo de integración futuro, no defecto de la Strategy. Límite de reentradas UNRESOLVED (no enseñado).

## Setups parciales (CLF-SET-001..007) — clasificación

SET-001 (derivación London→NY) [SOURCE, regla de skip]: implementada parcialmente vía windows de sesión (C01 rechaza TS hecho POR London; C03/C04 cubren NY); el «esperar el rango y posicionarse para NY» explícito no es un camino de señal propio — aceptable (regla de derivación). SET-002 (OB confirmado como trigger de FAM-001, «menos ideal pero confirma») [SOURCE]: NO implementado como trigger de entrada alternativo en ninguna spec — el OB solo existe dentro del FS. **F-K05-18 (MISSING_SOURCE_RULE, P2): la 2ª entrada del esquema (ch04 c-0034/c-0036/c-0039) no tiene camino de señal.** SET-003 (PDM espejo short con confirmación M30) [SOURCE parcial]: no implementado (PDM como entrada no existe; el filtro no-venta c-0213 tampoco) — F-K05-19 (P2). SET-004 (añadir en trade abierto) [gestión]: plano MM. SET-005 (espera completitud del contrario) [SOURCE, sincronización]: cubierta por lógica completitud/eliminación de la cadena. SET-006 (salir en el alto de la nueva vela) [personal]: sin implementar — F-K05-08. SET-007 (vela 12h condicional) [ejemplo]: sin implementar (12h no declarable en V1).

## Componentes (CMP-001..024) — verificación de cobertura

CMP-001/002/003/004/005/006/007/009/011/016/019/023/024 implementados y fieles (rangechain, pendiente, TS, DOL, FS-rango, insidecandle, aperturas, izquierda, HTF). CMP-008 (PDM) sin camino de señal (solo mención de comentario) — F-K05-19. CMP-010 (P3) implementado como marcador causal de apertura (po3.go) — la manipulación es retrospectiva por diseño causal, correcto; la ENTRADA en manipulación refinada queda cubierta solo vía STR-002+refine (F-K05-06). CMP-012/013/014/015 (SMT/DXY) BLOCKED_DATA. CMP-017 (objetivo tomado) implementado en dol.go (touch 1m, recompute, borrado). CMP-018 red flag par correlacionado: seam nil — correcto. CMP-020 secuencia 1-5-9: parcial en session_ctx (Five/Nine facts); la rama «si expande la 1, la 5 es TS de reversal y la expansión va a la 9» vive en C04/C03 por separado, no como secuencia explícita — aceptable como descomposición. CMP-021/022 sin camino (BLOCKED_DATA / ejemplo). CMP-020 c-0063 UNCERTAIN preservada.

## Gestión (§5) y frontera Strategy/MM

Stop inicial bajo TS [implementado como technical stop]; «stop no se mueve» [el motor/MM posee el físico — correcto]; BE estructural, parciales 50/80, coherencia parcial⇒BE, salida por reacción contraria, minuto-59, rango-en-contra-en-trade, pirámides, riesgo por etapa, tope 1%/2R, retirada, journal: plano MM/policy — fuera de Strategy por diseño (catálogo §5; frontera vigente correcta). Las salidas TÉCNICAS que sí son Strategy (F-K05-08): minuto-59 (ch02 c-0063/c-0064, probabilística), dos-15m-en-contra (ch08 c-0066–c-0068, personal), alto-de-la-nueva-vela (ch04 c-0091, personal) — sin implementar, candidatas a ejes pre-declarados, NO se agregan sin Owner.
