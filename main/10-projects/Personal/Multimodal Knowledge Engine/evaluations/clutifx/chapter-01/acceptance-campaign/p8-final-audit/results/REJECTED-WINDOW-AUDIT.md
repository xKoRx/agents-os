# REJECTED-WINDOW-AUDIT — Capítulo 01 Clutifx, rerun @ 19b44c1 (19 ventanas rechazadas)

Auditoría de las 19 ventanas rechazadas fail-closed del candidato rerun (`clutifx-ch01-rerun-20261003/run-rerun`,
130 ventanas; 111 aceptadas / 19 rechazadas): 17 por divergencia de identidad y 2 por defecto de formato.

- **Método**: por ventana se leyó transcript y frames del corpus (`p8-final-audit/corpus/wNNNN.json`, claims/relations
  vacíos para las rechazadas), la razón exacta en `run-rerun/run.db` → `pipeline_state.status_reasons`, y la cobertura
  se probó contra el **store canónico del rerun** `run-rerun/claims.jsonl` (1.043 claims + 146 relaciones) usando
  `records_introduced` por ventana de `analysis-rerun/coverage.json` (merges por equivalencia re-canónicos con el id
  de la ventana ORIGEN: lo propuesto por una rechazada puede estar almacenado vía la ventana ganadora). No se infiere
  recuperación por solape temporal: cada cobertura citada lleva record ID, y los 119 ids citados se verificaron
  programáticamente contra `claims.jsonl` (100% existen). Frames visualmente materiales inspeccionados: w0058
  (p74880000: rectángulo pendiente 1,15231/1,1467 con vela tomando el low y reacción — almacenado) y w0128
  (p178920000: trazado descendente en 15M hasta 1,14868 — la observación visual está, la regla no).
- **Fecha**: 2026-10-04. Datos por ventana en `rejected-windows.jsonl` (mismo directorio).
- **Calibración**: método y granularidad idénticos al baseline `p1-audit/results/REJECTED-WINDOW-AUDIT.md`.

## Conteo de consecuencias

| Consecuencia | Ventanas | N |
|---|---|---|
| NO_MATERIAL_LOSS | w0029, w0054, w0058, w0066, w0075, w0081, w0088, w0093, w0098, w0122, w0127 | **11** |
| PARTIAL_MATERIAL_LOSS | w0004, w0006, w0009, w0013, w0032, w0035, w0111, w0128 | **8** |
| MATERIAL_LOSS | — | **0** |

**Resultado global: ninguna ventana rechazada perdió conocimiento material de forma íntegra.**
8 de 19 dejan un residuo material acotado (1–2 proposiciones cada una); **n proposiciones materiales residuales
totales = 10**, bajo el umbral estricto de 19 del baseline (10 < 19 ✓). 11 de 19 no dejan residuo.

### Ventanas con pérdida residual material (las 8)

| Ventana | Razón | Residuo no almacenado |
|---|---|---|
| w0004 | semántica DIVERGENT (w0003, `cl-informacion-curso-intermedio-no-relevante`) | «Voy a empezar desde cero aquí también» |
| w0006 | semántica DIVERGENT (w0005, `cl-pintar-vela-ahora`) | La primera figura dibujada sería una vela bajista pintada de negro (solo quedó la figura inversa positiva de w0008) |
| w0009 | semántica DIVERGENT (w0005, `cl-rectangulo-relleno-blanco`) | «La mayoría de las veces la vela tomante sí es la siguiente» + «tampoco tiene que ser negativa (bajista)» |
| w0013 | determinista kind (w0007, `cl-rango-alcista-mostrado`: claim vs observation) | «Déjame borrar esto porque ya ha quedado claro» (borrado del dibujo del ejemplo) |
| w0032 | determinista epistemic (w0031, `cl-timeframe-1d`: INSTRUCTOR_SAID vs VIDEO_OBSERVED) | «Esto no es suficiente para operar, si no el curso sería muy rápido» |
| w0035 | semántica DIVERGENT (w0026, `cl-rangos-indican-direccion-precio`) | «Después hay señales de reversión y señales de continuación» (promesa no almacenada) |
| w0111 | determinista epistemic (w0063, `cl-marco-temporal-inicial-8h`: VIDEO_OBSERVED vs INSTRUCTOR_SAID) | «Es un poco exagerado porque está cerrado muy fuera» (el order block del ejemplo) |
| w0128 | determinista epistemic (w0065, `cl-temporalidad-grafico-15m`: VIDEO_OBSERVED vs INSTRUCTOR_SAID) | «Una vela de 4 horas vista en 15 minutos se ve como una bajada muy agresiva» + «el foco en la temporalidad baja puede liar; aléjate y mira 4 horas» |

Patrón de las pérdidas: nunca es el contenido colisionado (eso siempre quedó en la ventana ganadora); son
**proposiciones adyacentes únicas** — cuantificadores estadísticos del método (w0009), caveats de suficiencia
(w0032), micro-acciones de dibujo (w0006, w0013), promesas de señales futuras (w0035), calificativos del ejemplo
(w0111), la regla multi-timeframe y su consejo de foco (w0128) — que el ladder de identidad no transfiere a la
ventana vecina.

## Comparación old-vs-new

| Métrica | Run viejo (full-live) | Rerun @ 19b44c1 |
|---|---|---|
| Ventanas rechazadas | 26 (104 aceptadas) | **19** (111 aceptadas) −27% |
| Identidad | 22 | 17 |
| Formato | 4 (bad evidence ref) | 2 (1 bad-ref + 1 bad-relation-id) |
| Ventanas con residuo | 10 | 8 |
| **Proposiciones materiales residuales** | **19** | **10** |
| MATERIAL_LOSS íntegro | 0 | 0 |

- **Intersección de poblaciones**: solo 5 ventanas rechazaron en ambos runs (w0054, w0058, w0088, w0098, w0122),
  y en todas cambió la causa concreta (p. ej. w0054: structural→DIVERGENT; w0058: epistemic→bad-ref;
  w0122: DIVERGENT→epistemic). 21 ventanas del viejo ahora se aceptan; 14 del rerun son nuevas caídas.
- **Composición de causas**: el viejo se hundía por re-declaración determinista de parámetros de contexto con
  otro `kind` (11 ventanas) y por bad-refs (4). El rerun desplaza el fallo a la **fase de equivalencia
  (DIVERGENT, 11 de 17)**, dominada por el mismo activo esquivo: re-declaración de parámetros de contexto con
  otra redacción — instrumento (w0066, w0098), timeframe (w0081, w0088, w0093, w0128), anotaciones de la vela
  4H (w0122, w0127) y paráfrasis de definiciones (w0004, w0006, w0009, w0029, w0035, w0054).
- **El viejo lossy más caro se recuperó**: la narrativa de anticipación en tiempo real (w0058/w0059 del viejo,
  2×PARTIAL) ahora está almacenada casi literal por w0059 (aceptada en el rerun): `cl-regla-anticipar-rango-antes-cierre`,
  `cl-vela-sube-tras-low`, `cl-limites-rango-mostrado`, `cl-anticipacion-rango-mas-avanzada`, `cl-anticipacion-se-practica`.
  También entraron las reglas de marcos alternativos 10/25/30 (w0117: `cl-timeframe-10/25/30`) y los parámetros
  de la operación corta (w0116), pérdidas PARTIAL del viejo.
- **Residuo por causa en el rerun**: DIVERGENT 6 de las 10 proposiciones; deterministas 4; formato 0.

## Los 2 casos de formato (w0058, w0075)

- **w0058** — `record cl-rango-pendiente-formado cites unknown evidence ref "asr-00115 [818800-840040]"`.
  Mismo modo de decoración que el viejo w0003/w0005/w0043 (intervalo temporal pegado como sufijo del ID;
  el asr-00115 real es 818800–840040). Reconstrucción semántica correcta: las 4 proposiciones de la ventana
  (rango pendiente creado; vela toma y sube; en tiempo real se vio tomar el low y reaccionar; anticipable
  antes del cierre) están almacenadas vía w0059/w0045 → **NO_MATERIAL_LOSS**.
- **w0075** — `relation 1: relation id "cl-reaccion-requerida-para-consideracion" is not a stable mke id
  (want rel- prefix…)`: relación propuesta con prefijo `cl-` en vez de `rel-`. Modo nuevo, no visto en el viejo.
  Contenido de la relación (el Turtle Soup requiere toma + reacción) almacenado por w0067/w0068; el cierre fuera
  → rango eliminado, por w0076/w0078/w0080 → **NO_MATERIAL_LOSS**.
- **Veredicto de patrón**: bad-ref 4→2 con ventanas distintas (las 4 del viejo —w0003, w0005, w0043, w0110—
  hoy se aceptan). Ambos incidentes del rerun son **transientes de una ventana** (un slip de formateo cada uno,
  en modes distintos: sufijo de intervalo vs prefijo de namespace), no un patrón estructural del pipeline:
  el constraint de schema con patrón de ID propuesto en el baseline (`^asr-[0-9]{5}$` + `^rel-[a-z0-9-]+$`)
  habría aceptado ambos sin tocar semántica.

## Análisis por ventana

### Bloque 1 — DIVERGENT semántico (11): w0004, w0006, w0009, w0029, w0035, w0054, w0066, w0081, w0088, w0093, w0098

El equivalence_review falló ante paráfrasis/sinonimia superficial y en 10 de 11 la ventana ganadora ya tenía
el contenido colisionado. Nota: la razón de w0004 está truncada en el journal antes del veredicto, pero lleva
el formato de dos statements del review DIVERGENT (paráfrasis «No hay información…» vs «La información… no es…»).

- **w0004** ≡ w0003 → `cl-informacion-curso-intermedio-no-relevante@1` (w0003). Además cubren `cl-sin-curso-
  intermedio-no-pasa-nada`, `cl-formato-similar-curso-intermedio`, `cl-vamos-directamente-al-grano` (w0003);
  «inculcar un concepto nuevo, el rango» en `cl-capitulo-cubre-conceptos-desconocidos` (w0002) +
  `cl-ranges-basic-concept` (w0118) + la definición `cl-rango-vela-extremo-cierre-interior`/`cl-rango-vela-no-siguiente`
  (w0005); «pintar la vela» en `cl-pintar-vela-ahora` (w0005). Residuo: «empezar desde cero aquí también» → PARTIAL (1).
- **w0006** ≡ w0005 → `cl-pintar-vela-ahora@1`. Definición y etiqueta «rango» en w0005/w0007
  (`cl-rango-tras-extremo-y-cierre-adentro`, `cl-colocacion-etiqueta-rango`); la figura inversa (positiva) en
  w0008 (`cl-figura-repetida-invertida`, `cl-figura-derecha-vela-positiva`) — implica la bajista pero no la
  enuncia. Residuo: «vela bajista pintada de negro» → PARTIAL (1).
- **w0009** ≡ w0005 → `cl-rectangulo-relleno-blanco@1`. «No tiene por qué ser la siguiente» ya en
  `cl-rango-vela-no-siguiente` (w0005). Residuos: el cuantificador «la mayoría de veces sí es la siguiente» y
  «tampoco tiene que ser negativa (bajista)» (sin ningún record con «negativa/mayoría» en el store) → PARTIAL (2).
- **w0029** ≡ w0027 → `cl-observar-completado-rangos@1`; «ejercicio fácil» ×3 (w0027/w0028), failure swing abajo
  + «más tarde» (w0027: `cl-failure-swing-inferior-grafico-diario`, `cl-explicacion-failure-swing-posterior`),
  ejemplo bullish→extremo contrario + «cierra un poco fuera» con mecha (w0030: `cl-regla-rango-cierra-dentro-otro-extremo`,
  `cl-rango-ejemplo-bullish`, `cl-precio-cierra-fuera-rango`) → NO_MATERIAL_LOSS.
- **w0035** ≡ w0026 → `cl-rangos-indican-direccion-precio@1`; «navegar al precio» exacto en
  `cl-importancia-rangos-navegar-precio` (w0034); regla de continuación en `cl-continuation-rule-close-outside-no-bearish-range`
  (w0036). Residuo: la promesa «hay señales de reversión y de continuación» no quedó como record → PARTIAL (1).
- **w0054** ≡ w0053 → `cl-rango-pendiente-abre-hacia-doble@1`; el resumen completo reiniciado/pendiente vive en
  w0053 (`cl-rango-reiniciado-abre-contra-doble`, `cl-rango-pendiente-crea-rango-alcista`,
  `cl-rango-reiniciado-puede-crear-rango-bajista`, `cl-reinicio-rango-apertura-arriba` w0049); «ejemplo en el
  gráfico» + «objetivo diario = el del ejemplo» en w0055/w0056 (`cl-show-chart-example`, `cl-daily-target-matches-example`,
  `cl-objetivo-diario-es-ejemplo-anterior`) → NO_MATERIAL_LOSS.
- **w0066** ≡ w0018 → `cl-chart-instrument-eurusd@1`; «pongámosle de cuatro horas» exacto en
  `cl-temporalidad-vela-cuatro-horas` (w0065); toma del low + reacción = tartel sub en w0067/w0068
  (`cl-low-sweep-with-bullish-reaction-is-turtle-soup`, `cl-turtle-soup-bullish-reaction`); «si sigue bajando no
  es tartel sub» (`cl-price-continued-down-without-reaction`, `cl-shown-move-not-turtle-soup`, w0067); «tiene que
  ser una toma de liquidez» (`cl-turtle-soup-requires-liquidity-sweep` w0067, `cl-toma-de-liquidez-alias` w0064)
  → NO_MATERIAL_LOSS.
- **w0081** ≡ w0025 → `cl-eurusd-timeframe-15m@1`; todo el pasaje pre-SMT almacenado por w0080/w0082:
  eliminar rango y olvidarse (`cl-eliminar-rango-tras-condicion`, `cl-ignorar-rango-tras-condicion`,
  `cl-rango-completo-se-puede-eliminar`), volver a analizar (`cl-reanalizar-comportamiento-precio`),
  objetivo más arriba (`cl-comprobar-objetivo-superior`), siguiente capítulo (`cl-estrategia-siguiente-capitulo`),
  SMT en curso intermedio (`cl-smt-explicada-en-curso-intermedio`), muchos la conocen (`cl-muchos-conocen-smt`),
  SMT conocida euro/libra (`cl-esquema-zigzag-es-smt-conocida`, `cl-euro-ejemplo-smt`, `cl-libra-ejemplo-smt`)
  → NO_MATERIAL_LOSS.
- **w0088** ≡ w0085 → `cl-chart-timeframe-8h@1`; euro/libra y forma de la SMT (`cl-smt-ejemplo-eurusd/gbpusd`,
  `cl-smt-forma-sugerida`, w0085), capítulo aparte (`cl-smt-ejemplos-capitulo-aparte` w0085,
  `cl-capitulo-aparte-de-ejemplos` w0086, `cl-examples-separate-chapter` w0087), dos tipos (`cl-smt-two-types`
  w0089), objetivo alcista en euro (`cl-smt-bullish-euro-target` w0089) → NO_MATERIAL_LOSS.
- **w0093** ≡ w0085 → `cl-chart-timeframe-8h@1`; long en libra, euro en objetivos, SMT y giro directo (w0092:
  `cl-posicion-long-libra`, `cl-euro-llega-objetivos-actuales`, `cl-smt-posible-zona-objetivos-euro`,
  `cl-precio-giro-directo-smt`); «no tiene que ser entre las dos velas, como se ve muchas veces», SMT para
  objetivos y para formar rango, dibujo con mecha, extremo no tomado, euro igual a libra (w0094: `cl-smt-need-not-
  be-between-candles`, `cl-smt-between-candles-often-shown`, `cl-smt-can-reach-objectives`, `cl-smt-can-form-range`,
  `cl-gbpusd-range-use-wick`, `cl-wick-makes-range-realistic`, `cl-range-extreme-not-taken`, `cl-eurusd-match-gbpusd-form`)
  → NO_MATERIAL_LOSS.
- **w0098** ≡ w0018 («serie izquierda rotulada EURUSD») → cubierta mejor aún por `cl-comparacion-eurusd-gbpusd`
  (w0097); caso S&T no visible (`cl-escenario-caso-st`, `cl-casos-st-no-visibles` w0097); regla 4H libra-crea/euro-
  sube (`cl-regla-rango-libra-indica-euro`, `cl-regla-llegada-arriba-sin-rango`, `cl-euro-sin-rango-hasta-target`
  w0097); «para aclarar el concepto de SMT» (`cl-ejemplo-aclara-smt` w0097); failure swing: curso intermedio,
  definición sin nuevo bajo, varios casos (w0099/w0100: `cl-failure-swing-covered-in-intermediate-course`,
  `cl-failure-swing-no-new-low`, `cl-failure-swing-multiple-cases` + dupes w0100) → NO_MATERIAL_LOSS.

### Bloque 2 — deterministas kind/epistemic (6): w0013, w0032, w0111, w0122, w0127, w0128

- **w0013** kind claim↔observation vs w0007 → `cl-rango-alcista-mostrado@1` (w0007). «Más fácil de entender en
  el gráfico» → `cl-grafico-facilita-comprension-rango` (w0012); «ejemplos reales de rangos» materializado en
  w0014 (`cl-recuadro-de-rango-dibujado`, `cl-recuadro-senalado-es-rango`, `cl-proxima-demostracion-rango-bajista`).
  Residuo: el borrado del dibujo → PARTIAL (1).
- **w0032** epistemic vs w0031 → `cl-timeframe-1d@1` (w0031). «El precio se mueve formando y completando rangos»
  → `cl-price-always-moves-in-ranges`, `cl-price-completes-formed-range` (w0021), `cl-rangos-se-van-completando`
  (w0034). Residuo: «no es suficiente esto para operar» → PARTIAL (1).
- **w0111** epistemic vs w0063 → `cl-marco-temporal-inicial-8h@1` (w0063). «Esto es un order block»
  (`cl-zona-senalada-es-order-block` w0110); cierre afuera → entrada (w0113/w0114/w0116/w0117:
  `cl-long-tras-cierre-fuera`, `cl-long-after-close-outside`, `cl-take-after-outside-close`,
  `cl-entrada-short-tras-cierre-fuera`); M15 más fácil + la venta tomada (`cl-m15-order-blocks-mas-faciles`,
  `cl-order-block-venta-hoy-no-visible-en-15`, `cl-order-block-venta-hoy-poco-claro-en-10`,
  `cl-buscar-venta-con-order-block-visible`, w0112). Residuo: «cierre exagerado, muy fuera» → PARTIAL (1).
- **w0122** epistemic vs w0121 → `cl-vela-cuatro-horas@1` (w0121). 1:00 y 5:00 hora Nueva York
  (`cl-nivel-inferior-0100-nueva-york`, `cl-nivel-superior-0500-nueva-york`, w0121); «es el cierre»
  (`cl-cierre-0500` w0123, `cl-reference-close-0500` w0124); «abre, manipula, sube y baja hasta cerrar con la
  mecha arriba» (`cl-apertura-0100`, `cl-manipular-construccion-hasta-mecha`, `cl-dejar-mecha-arriba`,
  `cl-ajustar-construccion-antes-del-cierre` w0123; `cl-vela-apertura-manipulacion-distribucion-cierre` w0120)
  → NO_MATERIAL_LOSS.
- **w0127** kind observation↔parameter vs w0121 → `cl-anotacion-0100@1` (w0121). «Crea un rango alcista»
  (`cl-movimiento-mostrado-crea-rango-alcista` w0126); «a la vez hace el power 3» (`cl-rango-alcista-durante-
  power-three-ideal` w0126, `cl-power3-concept` w0124, `cl-construccion-power-3` w0123); «longs brutales para
  llegar arriba» (`cl-rango-alcista-durante-power-three-ideal` — situación ideal para comprar —,
  `cl-compras-ideales-en-manipulacion` w0123, `cl-bullish-buys-manipulation` w0124,
  `cl-entrada-preferida-power-3-nueva-vela` w0125) → NO_MATERIAL_LOSS.
- **w0128** epistemic vs w0065 → `cl-temporalidad-grafico-15m@1` (w0065). El trazado descendente en 15M está
  (`cl-linea-gris-descenso-115139-114868`, `cl-temporalidad-mostrada-15m`, w0129) pero no la regla ni el consejo.
  Residuos (2): «la vela de 4h se ve en 15m como una bajada muy agresiva» y «el foco en la temporalidad baja
  puede liar; aléjate y pon el foco en 4 horas» → PARTIAL (2). Verificado visualmente en frame p178920000.

## Notas transversales

1. **El parámetro de contexto sigue siendo la principal fuente de rechazo espurio** (ahora vía equivalence DIVERGENT
   en vez de kind determinista): ≥10 de las 17 identity re-declaran instrumento/timeframe/duración-anotada. Un
   registro canónico de contextos por-ventana eliminaría la mitad de los rechazos del rerun también.
2. **Los cuantificadores estadísticos del método se pierden de forma sistemática** cuando la ventana ganadora
   solo almacenó el lado cualitativo (w0009 «la mayoría de las veces»; w0032 «no es suficiente»; w0111
   «exagerado»). La re-canonicalización por equivalencia conserva la proposición pero no sus calificativos.
3. **Verificación de records**: 119/119 de los `surviving_record_ids` citados en `rejected-windows.jsonl` existen
   en `run-rerun/claims.jsonl` (chequeo programático).
4. El residuo total (10) es la mitad del baseline (19) y se concentra en proposiciones satélite (1–2 por ventana);
   sigue sin existir MATERIAL_LOSS íntegro en ningún run.

## FEEDBACK (Agents-OS)

1. **El bootstrap fue suficiente y bien calibrado**: las rutas de entradas dadas en el encargo resolvieron a la
   primera; no hizo falta explorar el vault más allá del corpus/resultado del proyecto. La regla de reutilizar
   base en turnos warm no aplicó (sesión one-shot).
2. **Razones truncadas en el journal** (`status_reasons` guarda strings con `…[truncated]` embebido): la razón de
   w0004 pierde el veredicto («returned DIVERGENT») exactamente cuando es larga. Sugerencia: guardar la razón
   completa en un campo estructurado (p. ej. `reason_class` + `collision_window` + `statements` como JSON) en
   `pipeline_state`, y truncar solo la vista de texto.
3. **Los ids en `coverage.json` llevan sufijo `@N`** (`cl-x@1`) mientras `claims.jsonl` separa `id`/`version`
   (`cl-x`): todo consumidor tiene que normalizar. Sugerencia: un solo formato canónico (ids sin sufijo) en los
   artefactos de análisis.
4. **Sin CLI `sqlite3` en el host**: la lectura de `run.db` requirió Python. Si los runs van a auditarse a mano,
   un dump JSON/LJSON del estado (o `python3 -m sqlite3`-style helper en el repo del run) ahorraría fricción.
5. **Granularidad de proposición**: la unidad «proposición material» funciona bien (10 residuos comparables al
   baseline), pero las micro-acciones de dibujo (borrar/repintar) quedan en zona gris entre «material» y
   «procedimental». Sugerencia para la próxima campaña: decidir en el protocolo si las acciones de herramienta
   (sin consecuencia semántica) cuentan como material; hoy el store las canoniza a veces sí y a veces no, y eso
   mueve el residuo ±1 por ventana.
