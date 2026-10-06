# GROUNDING-AUDIT · P8 final · Clutifx Ch01 · run P7b (`e7bc387`, runtime `~/mke/clutifx-ch01-rerun2-20261004/run-rerun2/`)

Auditor: GROUNDING (one-shot, contexto fresco). Fecha: 2026-10-05.
Método: veredicto independiente citation-grounded contra el corpus fuente (`corpus/wNNNN.json` + frames PNG en `/home/kor/mke/clutifx-ch01-20260930/media-run/evidence/objects/`) y el journal (`run.db.provider_invocations`). Las etiquetas de los workers A1–A4 se usaron solo como pista. El estándar aplicado al reviewer es el SUYO (prompt `mke.claims-ground.v3`, review_contract `calibration-3`, leído del journal), no uno inventado.

---

## 1. Población y desglose por causa

**non_supported_total = 343 · VERIFICADO** (307 claims + 22 relations + 14 SKOs con `publication` `UNSUPPORTED_*`).

| Causa (journal + reasons) | Records | Detalle |
|---|---|---|
| PROVIDER_FAILURE (transport) | **273** | 272 `vlm provider transport [retry-exhausted]` (timeout) + 1 `read-body [retry-exhausted]` (rel-no-turtlesoup-depende-no-reaccion) |
| PROVIDER_FAILURE (parse) | **46** | 44 `parse [retry-exhausted]` («response contains no choices») + 2 `parse-structured [fatal]` («assistant content is not a valid JSON object»: cl-pattern-many-timeframes, sko-range-completion) |
| Semántico (veredicto real del reviewer) | **24** | 21 INSUFFICIENT (4 claims + 17 relations), 2 CONTRADICTED (1 claim + 1 SKO), 1 PARTIAL (SKO) |
| **Total** | **343** | 273+46+24 = 343 ✓ (= 307 claims + 22 relations + 14 SKOs) |

Reconciliación con el journal: `claims.grounding_review` = 563 VALIDATED + 306 retry-exhausted + 1 fatal; `sko.composition_review` = 21 VALIDATED + 11 retry-exhausted + 1 fatal; `claims.equivalence_review` = 59 VALIDATED (sin fallos). Los ~306 del parte coinciden con los retry-exhausted de grounding_review.

**Cero veredictos rescatables perdidos**: para los 319 REVIEW_UNAVAILABLE no existe NINGUNA invocación VALIDATED con veredicto SUPPORTED en el journal (búsqueda por record_id en `request_json`). No hay fail-closed residual: la tolerancia del validador no tuvo nada que recuperar en este run — la tormenta mató las respuestas antes de que existieran.

## 2. FN rate (dos versiones)

FN semántico total = **10** (todas relations; 0 claims, 0 SKOs). Ver §4.

- **(a) Congelada: 10/343 = 2,92 %**
- **(b) Adjudicada por causa: 10/24 = 41,7 %** (denominador = 343 − 273 transport − 46 parse = los 24 records que sí recibieron veredicto). Restringido a claims+relations (excluye los 2 SKOs, cuyo bloqueo es estructural de composición): 10/18 = 55,6 %.
  - Variante conservadora (solo FN «clear», excluidos los 4 borderline): 6/24 = 25,0 %.

Lectura: el reviewer v3 NO sobre-rechaza el soporte de claims (0/5 claims semánticos es FN; 1 es contradicción real verificada en píxeles y 4 son atomicity). El sobre-rechazo está concentrado en **relations DEPENDS_ON**: 10/17 rechazos semánticos de relaciones son FN (6 claros + 4 borderline), todos del mismo tipo: el reviewer no aplica la cláusula de enactuación estructural («definition, conditional rule or scenario… even without the literal words») ni la regla deixis que su propio contrato le impone, y exige identificación/enunciación literal que el contrato no pide.

**Inconsistencia demostrada (mismo estándar, dos veredictos):**
- `rel-continuacion-sin-rango` SUPPORTED vs `rel-continuacion-cierra-fuera` INSUFFICIENT — **misma evidencia citada** (asr-00063+00064, condicional «si la vela cierra fuera y no te forma un rango bajista, lo que puedes esperar es que continúe»).
- `rel-formacion-bajista-depende-apertura` SUPPORTED vs `rel-formacion-bajista-depende-cierre` INSUFFICIENT — mismos segmentos (asr-00105/00106), misma estructura condicional; se aceptó la apertura y se rechazó el cierre.

## 3. Desglose semántico completo (24 records)

| Record | Veredicto pipeline | Clasificación auditor | Base |
|---|---|---|---|
| cl-line-horizontal-115000-drawn | CONTRADICTED | **ACTUALLY_CONTRADICTED** | Frames p63360000/p63720000: la línea termina en la banda 1,15021/1,15026/**1,15029**; no hay 1,15000. Rechazo correcto, pixel-preciso |
| cl-reviews-referencia-tipos-rango | INSUFFICIENT | **ATOMICITY_PROBLEM** | asr-00109 + frame soportan ambas correspondencias; COMPOSITE (2 mapeos). Policy-consistente; el reconstructor v4 no divide |
| cl-rightmost-candle-sweeps-high-closes-inside | INSUFFICIENT | **ATOMICITY_PROBLEM** | asr-00106 soporta; COMPOSITE (toma high / cierra adentro) |
| cl-valor-dialogo-un-minuto | INSUFFICIENT | **ATOMICITY_PROBLEM** | Frame p23490000 verificado: «1» + «1 minuto» visibles; COMPOSITE |
| cl-vigilar-eur-y-par-correlacionado | INSUFFICIENT | **ATOMICITY_PROBLEM** | asr-00195 soporta; COMPOSITE (caso límite: 1 instrucción, 2 objetos) |
| rel-continuacion-cierra-fuera | INSUFFICIENT | **FALSE_NEGATIVE** (clear) | Condicional explícito cross-segmento; hermano con misma evidencia SUPPORTED |
| rel-formacion-bajista-depende-cierre | INSUFFICIENT | **FALSE_NEGATIVE** (clear) | «si vemos que cierra adentro… se está formando»: escenario enactuado; el motivo «si vemos = comprobación» no está en el contrato |
| rel-no-turtle-soup-depende-de-no-reaccion | INSUFFICIENT | **FALSE_NEGATIVE** (clear) | «en lugar de reaccionar, sigue bajando, no es ningún tartle sub» + regla definicional inmediata |
| rel-reanalizacion-tras-eliminacion | INSUFFICIENT | **FALSE_NEGATIVE** (clear) | Cadena «ya puedes eliminar… y volver a analizar»; el propio reviewer concede «la evidencia sí encadena» y exige además re-probar el antecedente del objeto (fuera del alcance de la relación) |
| rel-reanalizacion-tras-olvido | INSUFFICIENT | **FALSE_NEGATIVE** (clear) | Misma cadena enumerada y ordenada |
| rel-bullish-range-depends-on-timeframes | INSUFFICIENT | **FALSE_NEGATIVE** (clear) | «y todo esto basado en las temporalidades»: anafora «todo esto» resoluble por regla deixis + «basado en» |
| rel-borde-superior-bearish-depends-rango | INSUFFICIENT | **FALSE_NEGATIVE** (borderline) | Frame p45270000: borde superior del rectángulo exactamente en 3.394,75 resaltado; exigencia de identificación verbal innecesaria |
| rel-busqueda-rango-usa-temporal-12h | INSUFFICIENT | **FALSE_NEGATIVE** (borderline) | Relativo «que ya lo tenemos en 12 horas» vincula objeto y localización en una emisión |
| rel-smt-superior-depande-eur-objetivos | INSUFFICIENT | **FALSE_NEGATIVE** (borderline) | Escenario único: «pero euro llega a los objetivos, puede haber una SMT ahí arriba» |
| rel-toma-low-requiere-apertura | INSUFFICIENT | **FALSE_NEGATIVE** (borderline) | Enumeración ordenada (abrir → tomar low → formar) enactúa la presuposición |
| rel-no-turtlesoup-depende-bajista | INSUFFICIENT | **EVIDENCE_SELECTION_PROBLEM** | Objeto dice «después de tomar el low»: está en asr-00130, NO citado (solo citaron asr-00131). Mejor selección lo recupera |
| rel-llegada-directa-definida-por-objetivo | INSUFFICIENT | **EVIDENCE_SELECTION_PROBLEM** | Identidad del objetivo=1,35843 exige los frames que el reconstructor sí citó para el claim objeto y aquí omitió |
| rel-bearish-completion-depends-on-formation | INSUFFICIENT | CORRECT_REJECTION (borderline) | asr-00083 telegráfico, sin enactuación más allá del orden |
| rel-eliminacion-rango-requiere-invalidez | INSUFFICIENT | CORRECT_REJECTION (borderline) | Dos consecuencias del cierre fuera; apposición sin enactuación entre ellas |
| rel-falso-turtle-soup-depende-de-reaccion-real | INSUFFICIENT | CORRECT_REJECTION (borderline) | Adyacencia narrativa, sin enlace estructural entre las dos claims |
| rel-pendiente-8h-continua-pendiente-12h | INSUFFICIENT | CORRECT_REJECTION | «pendiente también» = comparación de estado, no dependencia |
| rel-copia-depende-seleccion-d | INSUFFICIENT | CORRECT_REJECTION | Co-ocurrencia; la copia no depende de la inclusión de «D» |
| sko-objective-correction | CONTRADICTED | **ATOMICITY_PROBLEM** (estructural) | Componentes soportados; bloquea una CONTRADICTS soportada que ES el significado del procedimiento (corrección de objetivo, roles initial/rejected/corrected). La política de coherencia no distingue enmienda de incoherencia |
| sko-scalp-range-conditions | PARTIAL | **ATOMICITY_PROBLEM** (estructural) | Closure correcto: la EXCEPTION_TO material alcanza un claim no-componente; composición incompleta, no falta de soporte |

Resumen: FALSE_NEGATIVE 10 · ATOMICITY_PROBLEM 6 · CORRECT_REJECTION 5 (4 borderline) · EVIDENCE_SELECTION_PROBLEM 2 · ACTUALLY_CONTRADICTED 1.

## 4. Los 9 casos R-M07 (P7 19b44c1 malformed-verdict fail-closed) en P7b

| Claim (P7) | En P7b | Resultado |
|---|---|---|
| cl-operar-solo-grafico-diario | `cl-operate-daily-chart-only` (w0033), sim. 0,84 | **RECUPERADO — SUPPORTED**. La respuesta lleva `record_id` con sufijo `@1` (el patrón que en P7 era fatal) y el validador la aceptó: la tolerancia R-M07 funciona |
| cl-informacion-curso-intermedio-no-relevante | 2 equivalentes (w0002 sim. 0,95; w0003 sim. 0,92) | **RECUPERADO — SUPPORTED ×2** |
| cl-rango-actual-toma-low-vela-anterior | `cl-rango-cuatro-horas-toma-low-vela-anterior` (w0045), sim. 0,67 | **RECUPERADO — SUPPORTED** |
| cl-seleccion-vela-blanca-pequena | Equivalente `cl-seleccion-vela-blanca` (w0046) | **RECUPERADO por equivalente — SUPPORTED** (el claim exacto no se reextrajo en w0049, su ventana) |
| cl-fecha-24-06-2025 | Extraído **11 veces** (w0002…w0074, incl. `cl-fecha-24-6-2025` idéntico en w0007) | EXTRAÍDO, veredicto muerto por transporte (sin respuesta no hay nada que tolerar) |
| cl-observar-rangos-diario-es-facil | 2 equivalentes (w0027, w0028) | EXTRAÍDO, veredicto muerto por transporte |
| cl-entrada-posicion-corta-114697 | w0115 `rejected: provider unavailable` | **NO EXTRAÍDO** (ventana muerta en reconstrucción por transporte; asr-00253/254 están en el corpus sin claims) |
| cl-smt-convierte-esto-en-rango | w0095 `rejected: provider unavailable` | **NO EXTRAÍDO** (ventana muerta por transporte; asr-00198..00200 sin claims) |
| cl-rango-bajista-completa-ordenes | w0023 `rejected: identity divergence` | **NO EXTRAÍDO — única causa NO-transporte** (divergencia de identidad en reconstrucción). Cobertura parcial del contenido en w0015 (`cl-precio-completa-rango-bajista`, SUPPORTED) |

**AC R-M07**: la tolerancia RECUPERA los casos allí donde el reviewer llegó a responder (4/9 SUPPORTED, uno de ellos con el patrón `@1` que mataba P7); los otros 5/9 quedaron antes de esa capa: 4 ventanas muertas por la tormenta de transporte y 1 (w0023) por divergencia de identidad — este último requiere seguimiento propio (ver §7).

## 5. Muestreo dirigido de transport/parse (15 records)

Selección estratificada determinista (orden por id) + los 2 parse-fatal. Verificación contra fuente (transcripción y frames visualizados):

| Record | Causa journal | ¿La fuente lo sostendría? |
|---|---|---|
| cl-abrir-cambiar-intervalo | transport | SÍ — frame p70110000: diálogo «Cambiar intervalo» abierto (verificado) |
| cl-black-rectangular-form-moved-left | transport | SÍ — p94320000→p94680000: rectángulo negro se mueve a la izquierda (verificado) |
| cl-campo-h-116045 | transport | SÍ — p540000: OHLC «H 1,16045» legible (verificado) |
| cl-chart-left-eurusd | transport | SÍ — p47250000: cabecera izquierda «EURUSD · 15 · FOREX.com» (verificado) |
| cl-comprobacion-muchas-temporalidades | transport | SÍ — asr-00054 literal |
| cl-diagramas-algunos-tipos-rango | transport | SÍ — asr-00109 «Estos serían un poco los tipos de rangos» + frame |
| cl-ejemplo-linea-horizontal-maximos | transport | SÍ — p84240000: línea horizontal por ambos máximos del esquema (verificado) |
| cl-estructura-actual-ya-no-es-rango | transport | SÍ — asr-00168 «esto ya no es un rango» |
| cl-existen-senales-reversion | transport | SÍ — asr-00062 «hay señales de reversión» |
| cl-finta-puede-confundirse-como-turtle-soup | transport | SÍ — asr-00132/00133 literal |
| cl-gbpusd-rango-borde-inferior-134155 | transport | SÍ — p46890000: borde inferior del rectángulo GBPUSD 1D en 1,34155 resaltado (verificado) |
| cl-grafico-inicial-derecho-gbpusd | transport | SÍ — p49590000: panel derecho «GBPUSD · 4h» (verificado) |
| cl-pattern-many-timeframes | parse-fatal | SÍ — asr-00054 |
| cl-smt-eur-completa-objetivo | parse | SÍ — asr-00194 («que euro pueda llegar a completar» como condición del SMT) |
| sko-range-completion | parse-fatal | N/A — composición; sin respuesta no hay veredicto que recrear (componentes todos extraídos) |

**14/14 auditables (100 %) confirmados como soportados por la fuente** → los 319 REVIEW_UNAVAILABLE son en su práctica totalitud contenido perdido por transporte, no ruido de extracción. Consistente con A1–A4: exactitud alta en lo publicado; el coste del run está en lo que no llegó a publicarse.

## 6. Falsos positivos (muestra distribuida de SUPPORTED)

40 records (32 claims + 6 relations + 2 SKOs), muestreo determinista distribuido por id; 8 claims numéricos/visuales verificados en frame, el resto por transcripción literal; relations por enactuación explícita.

**FP = 1/40 (2,5 %)** — baseline P7: 0/61.

- **cl-ranges-always-complete** («Los rangos siempre se van completando», SUPPORTED, evidencia asr-00059) es **FALSE_POSITIVE**: asr-00059 es una autocorrección garbled («se te van completando siempre no siempre por esto») y asr-00060 lo desambigua («por qué a veces no se completan»). El reviewer leyó «siempre» literal y validó lo contrario de lo dicho; además coexiste publicado con `cl-ranges-not-always-complete` / `cl-rangos-no-siempre-se-completan` (SUPPORTED, mismo segmento): par contradictorio publicado. El resto (39) es soporte correcto, incluidos los numéricos verificados en frame (1,15179; 0,23 %; 1.14569; 56 %; 5M; H 1,16045) — precisión visual del reviewer alto, sin FPs numéricos detectados.

## 7. Observaciones para remediación (no bloqueantes del verdicto)

1. **Relations DEPENDS_ON**: 10/17 rechazos semánticos son FN por no aplicación de las cláusulas de enactuación/deixis del propio contrato calibration-3. La inconsistencia same-evidence (2 pares demostrados) sugiere recalibración del prompt relation-review con contraejemplos de condicionales cross-segmento y enumeraciones ordenadas, o un chequeo determinista de conectores («si», «porque», «después de», «una vez», «y todo esto basado en») previo al veredicto.
2. **Atomicity en reconstrucción (v4)**: 4 claims publicados como INSUFFICIENT-COMPOSITE totalmente soportados. El reviewer aplica bien el criterio; el que under-split es el reconstructor. R-* candidata en el prompt de reconstrucción.
3. **Coherencia de SKO**: `sko-objective-correction` bloqueado por una CONTRADICTS soportada que es parte de la semántica del procedimiento (corrección). Candidato: excepción de coherencia para contradicción-enmienda con roles.
4. **Identity divergence (11 ventanas, incl. w0023 con los R-M07)**: no es transporte ni grounding; dejó 11 tramos del capítulo sin claims en P7b (p. ej. 05:04–05:16, 18:04–18:24, 21:26–21:44). Requiere investigación propia antes de P7c si no está ya cubierta.
5. **Autocorrecciones del instructor** («siempre no siempre»): 1 FP. Candidato: regla de identidad/disfluencia que trate la autocorrección inmediata como corrección (el segundo término manda).

## FEEDBACK (Agents-OS)

Contexto de esta sesión: tarea one-shot de auditoría en contexto fresco, sin bootstrap previo cargado.

1. **Marker/AGENTS_OS_MANAGED invisible en subagentes de tarea**: el bloque gestionado llegó vía AGENTS.md del workspace, pero el skill `agents-os-bootstrap` no estaba disponible en la lista de skills de este agente (no aparecía en los disponibles). Si el bootstrap es «la única máquina de startup», o debe inyectarse como skill disponible para todo agente que vea el marker, o el bloque debe indicar explícitamente qué hacer cuando el skill no es alcanzable (hoy: regla inaplicable en la práctica).
2. **One-shot + «CLOSE SESSION AL TERMINAR»**: el encargo pedía cerrar la sesión, pero un subagente de tarea no posee el ciclo de sesión (la cierra el coordinador). Sugerencia: para tareas one-shot delegadas, sustituir la instrucción de cierre por «entrega el resumen final y no inicies fases nuevas» — el efecto real es el mismo y evita ambigüedad.
3. **Pistas de workers anteriores (summary-A\*.md) sin riesgo de anclaje**: funcionó bien pasarlas «como pista, veredicto independiente»: el veredicto cambió en al menos un caso respecto a lo esperable por anclaje (FNs en relations que los workers no marcaban). Mantener ese patrón de encargo: pistas separadas del criterio.
4. **Entregables duales (md + jsonl)**: buen patrón; conviene fijar en la plantilla de encargo el esquema mínimo del jsonl (root_cause/confidence/audited) para que auditorías sucesivas sean diff-ables. Esta auditoría usó: `classification`, `confidence` (clear|borderline), `root_cause`, `audited`, `would_source_support`, `transport_sample`.
5. **Rutas con espacios** («Multimodal Knowledge Engine»): todos los comandos necesitaron quoting; coste menor pero constante. Si el vault está bajo control del usuario, considerar un symlink sin espacios para pipelines de auditoría (`/home/kor/mke-audit → vault path`).

---

### Anexo: métricas finales

- `non_supported_total` = **343** (verificado)
- Desglose: transport **273** · parse **46** (44 retry-exhausted + 2 fatal) · semántico **24**
- FN congelada: **10/343 = 2,92 %**
- FN adjudicada: **10/24 = 41,7 %** (claims+relations solo: 10/18; variante conservadora solo-FN-claros: 6/24 = 25,0 %)
- FP muestra distribuida: **1/40** (baseline P7 0/61)
- Transport sample: **14/14 auditables sostenidos por la fuente** (1 SKO N/A)
- R-M07: **4 recuperados SUPPORTED (1 vía equivalente), 2 extraídos con veredicto muerto por transporte, 3 no extraídos (2 transporte, 1 identity divergence)**
- Detalle fila a fila: `grounding-audit.jsonl` (392 filas: 319 provider-failure con root_cause, 24 semánticos, 9 R-M07, 40 FP-sample)
