# IDENTITY-AUDIT — Ladder de identidad, capítulo 01 Clutifx (candidato rerun @ 19b44c1)

Auditoría fuente-grounded del P8 (aceptación exhaustiva) sobre las **71 llamadas `claims.equivalence_review`**, las **17 identity collisions** que rechazaron ventana y las **38 acumulaciones aplicadas** del run `clutifx-ch01-rerun-20261003/run-rerun` (store canónico: 1043 claims + 146 claim relations; 130 ventanas: 111 aceptadas, 19 rechazadas — 17 por identidad, 1 por evidence ref inválida w0058, 1 por relation id malformado w0075; status final INCOMPLETE por diseño, con los rechazos en `status_reasons`).

Fuentes auditadas: `run.db` (`provider_invocations`, `pipeline_state.status_reasons`, `record_stages`, `pipeline_records`, `record_outcomes`), store canónico `claims.jsonl`, respuestas de reconstrucción por ventana, análisis precomputado `equivalence_rows.json` + `accumulations.json`, `documentation.md` (línea del ladder), y el baseline `p1-audit/results/IDENTITY-AUDIT.md` (run full-live-v2). Toda clasificación humana se hizo leyendo los DOS statements de cada caso (request_json / status_reasons / respuestas de recon) con juicio semántico propio.

Veredicto agregado en una línea: **0 falso merges (hard-failure PASS: 0 FALSE_EQUIVALENT aplicado, 0 material), 6 falsos splits claros + 1 ambiguo resuelto DIVERGENT sobre 71 reviews (9,9 %, mejor que el 11,8 % del baseline), 6/6 divergencias deterministas son inestabilidad de clasificación (baseline 15/16, sin casos estructurales), 38/38 acumulaciones PASS con verificación física independiente (153 merges explicados al 100 %: 59 live + 58 caché + 36 deterministas, 0 sin adjudicar), y la fragmentación cross-slug EMPEORÓ (77 pares byte-idénticos vs 13 del baseline), con una consecuencia de cobertura de los 17 rechazos bastante mayor que la del baseline (~38 % de cobertura lexical del contenido propuesto vs ~85–90 % estimado antes).**

---

## 1. Las 17 identity collisions (rechazos de ventana)

Composición verificada contra `pipeline_state.status_reasons` y `metrics.json`: **6 deterministas** (2 kind-flip + 4 epistemic-flip + **0 estructurales**; en los 6 casos el stage cierra «window rejected closed without an equivalence review») + **11 semánticas DIVERGENT** (10 con invocación live VALIDATED + 1 servida por caché de pares sin invocación, w0093). Las 11 semánticas corresponden a los 10 veredictos DIVERGENT live (w0004, w0006, w0009, w0029, w0035, w0054, w0066, w0081, w0088, w0098) más el caso cacheado w0093.

| # | Window | Record | Causa | Store (A) vs Entrante (B) | Clasificación |
|---|---|---|---|---|---|
| 1 | w0013 | `cl-rango-alcista-mostrado` | deterministic / kind (claim vs observation) | «El dibujo mostrado es un rango alcista» (claim) vs «El gráfico muestra un ejemplo etiquetado «rango alcista»» (observation) | **MODEL_CLASSIFICATION_INSTABILITY** |
| 2 | w0032 | `cl-timeframe-1d` | deterministic / epistemic (INSTRUCTOR_SAID vs VIDEO_OBSERVED) | «El gráfico mostrado es únicamente diario (1D)» vs «El marco temporal mostrado es 1D» | **MODEL_CLASSIFICATION_INSTABILITY** |
| 3 | w0111 | `cl-marco-temporal-inicial-8h` | deterministic / epistemic (VIDEO_OBSERVED vs INSTRUCTOR_SAID) | «El marco temporal mostrado inicialmente es 8h» vs «En las primeras imágenes, el gráfico mostrado está en 8 horas» | **MODEL_CLASSIFICATION_INSTABILITY** |
| 4 | w0122 | `cl-vela-cuatro-horas` | deterministic / epistemic (INSTRUCTOR_SAID vs VIDEO_OBSERVED) | «El esquema dibujado sería una vela de 4 horas» vs «La vela del ejemplo está rotulada como «4 HORAS»» | **MODEL_CLASSIFICATION_INSTABILITY** (el rótulo confirma la inferencia) |
| 5 | w0127 | `cl-anotacion-0100` | deterministic / kind (observation vs parameter) | «Se añade la anotación «0100» junto al nivel horizontal inferior» vs «La figura temporal muestra la marca «0100»» | **MODEL_CLASSIFICATION_INSTABILITY** (núcleo idéntico; A registra evento+posición) |
| 6 | w0128 | `cl-temporalidad-grafico-15m` | deterministic / epistemic (VIDEO_OBSERVED vs INSTRUCTOR_SAID) | «La temporalidad visible del gráfico es «15M»» vs «La temporalidad del gráfico mostrado es 15 minutos» | **MODEL_CLASSIFICATION_INSTABILITY** |
| 7 | w0004 | `cl-informacion-curso-intermedio-no-relevante` | semantic / DIVERGENT | «No hay información del curso intermedio que sea totalmente relevante para entender esto ahora» vs «La información del curso intermedio no es totalmente relevante para entender el contenido actual» | **FALSE_DIVERGENT** (universal vs genérico de la misma negación; mensaje material idéntico) |
| 8 | w0006 | `cl-pintar-vela-ahora` | semantic / DIVERGENT | «Voy a pintar la vela ahora» vs «Pintar ahora la vela grande en el gráfico» | **FALSE_DIVERGENT** (mismo acto; B explicita el referente ya definido; modalidad anuncio/paso) |
| 9 | w0009 | `cl-rectangulo-relleno-blanco` | semantic / DIVERGENT | «Se aplica relleno blanco al rectángulo grande» vs «El rectángulo situado a la derecha pasa de tener relleno oscuro a tener relleno blanco» | **TRUE_DIVERGENCE** (B añade el estado previo «relleno oscuro» y otra descripción del objeto) |
| 10 | w0029 | `cl-observar-completado-rangos` | semantic / DIVERGENT | «Observar cómo se completan los rangos en la temporalidad diaria» vs «Observar cómo se completan los rangos» | **AMBIGUOUS** (núcleo idéntico; qualifier deíctico-contextual «en la temporalidad diaria»; fail-closed contract-consistente) |
| 11 | w0035 | `cl-rangos-indican-direccion-precio` | semantic / DIVERGENT | «Los rangos normalmente indican hacia dónde va el precio» vs «Los rangos de nuestra estrategia permiten saber hacia dónde va el precio» | **TRUE_DIVERGENCE** (tendencia general vs capacidad del scope «nuestra estrategia») |
| 12 | w0054 | `cl-rango-pendiente-abre-hacia-doble` | semantic / DIVERGENT | «El rango pendiente se abre en dirección a nuestro doble» vs «El rango pendiente abre en dirección al doble» | **FALSE_DIVERGENT** («nuestro» vs «el», «se abre» vs «abre»: nada material) |
| 13 | w0066 | `cl-chart-instrument-eurusd` | semantic / DIVERGENT | «El instrumento mostrado es EURUSD» vs «El gráfico mostrado es EURUSD» | **FALSE_DIVERGENT** (paráfrasis con sujetos co-referentes) |
| 14 | w0081 | `cl-eurusd-timeframe-15m` | semantic / DIVERGENT | «La temporalidad del gráfico mostrado es 15M» vs «El gráfico de EURUSD se muestra inicialmente en un marco temporal de 15 minutos» | **TRUE_DIVERGENCE** (B añade «de EURUSD» e «inicialmente») |
| 15 | w0088 | `cl-chart-timeframe-8h` | semantic / DIVERGENT | «El marco temporal del gráfico activo es 8h» vs «El marco temporal del gráfico mostrado es 8h» | **FALSE_DIVERGENT** (el falso split más claro del run: único delta el adjetivo) |
| 16 | w0093 | `cl-chart-timeframe-8h` | semantic / DIVERGENT **servido por caché** (sin invocación) | ídem caso 15, statements idénticos | **FALSE_DIVERGENT** (mismo par re-adjudicado desde la caché de pares) |
| 17 | w0098 | `cl-chart-instrument-eurusd` | semantic / DIVERGENT | «El instrumento mostrado es EURUSD» vs «La serie izquierda de la comparación está rotulada EURUSD» | **TRUE_DIVERGENCE** (etiqueta de serie comparada ≠ instrumento mostrado) |

Saldo de los 17 rechazos: **6 inestabilidad de clasificación determinista + 6 falsos splits semánticos + 1 ambiguo resuelto DIVERGENT = 13 rechazos injustificados (76 %); 4 rechazos correctos (24 %)**. Ningún rechazo protegió al store de un merge dañino.

Hallazgo de auditabilidad (w0093): `status_reasons` declara «claims.equivalence_review returned DIVERGENT» pero **no existe invocación alguna** para el par `w0085->w0093` en `provider_invocations`: el pipeline reutilizó el veredicto del par idéntico w0088 vía caché content-addressed. Funcionalmente determinista y correcto (mismo par ⇒ mismo veredicto), pero invisible en el journal de proveedor.

---

## 2. Las 71 adjudicaciones live (claims.equivalence_review)

Las 71 invocaciones están `VALIDATED`, contrato `mke.claims-equivalence-prompt.v1` (idéntico al baseline), modelo `stealth/space-bunny-alpha`, con la instrucción congelada «when in doubt, answer DIVERGENT» y las clases materiales (negación, números, condiciones, qualifiers, dirección, modalidad, scope). Veredictos: **61 EQUIVALENT / 10 DIVERGENT** (el brief de la fase decía 60/11; la fuente manda).

| Veredicto | n | Clasificación del auditor |
|---|---|---|
| EQUIVALENT | 61 | **61 CORRECT_EQUIVALENT**, 0 FALSE_EQUIVALENT |
| DIVERGENT | 10 | 5 FALSE_DIVERGENT (casos 7, 8, 12, 13, 15 de §1), 4 TRUE_DIVERGENCE (casos 9, 11, 14, 17), 1 AMBIGUOUS (caso 10) |

Los 61 EQUIVALENT son todos paráfrasis genuinas de la misma proposición: familias EURUSD-instrumento (17), temporalidad 15m (17), 8h (11), fuente FOREX.com (5), fecha 24/6/2025 (4), moneda/eje USD (4), y misceláneos correctos (failure swing, rango reiniciado, cierre-fuera-invalida-rango, cambiar temporalidad, rectángulo seleccionado, etiqueta RANGO PENDIENTE). Los deltas aceptados son siempre no-materiales: comillas («15M» vs 15M), «mostrado» vs «indicado»/«visible», 15M vs «de 15 minutos», deícticos («este rango» vs «el rango señalado»), elipsis contextuales, y dos pares modalidad anuncio/paso (veredicto #11 «Vamos a cambiar» vs «Cambiar»: EQUIVALENT correcto). El caso más laxo es #18 (rectángulo seleccionado, se pierde «con puntos de control»): marginal pero defendible, precedente idéntico al «configurada vs indicada» del baseline.

**Auto-consistencia del reviewer:** los 71 requests contienen 69 pares de statements distintos; 2 pares se repitieron (misma llamada literal en ventanas distintas) y en ambos casos el veredicto fue idéntico. **0 conflictos de veredicto sobre pares idénticos.**

---

## 3. Falsos merges y hard-failure check

- **FALSE_EQUIVALENT: 0 de 71 reviews; 0 de 117 merges semánticos aplicados (59 live + 58 por caché) y 0 de 36 acumulaciones deterministas.** Ningún merge unió proposiciones materialmente distintas; ningún DIVERGENT terminó fusionado (verificado ventana a ventana en §4).
- **Hard-failure check: applied material FALSE_EQUIVALENT = 0 → PASS.**
- Política whole-window consistente: 2 veredictos EQUIVALENT correctos fueron anulados porque la ventana entrante se rechazó por OTRA colisión (w0088 y w0093 mergeaban `cl-chart-instrument-eurusd` y cayeron por la colisión de `cl-chart-timeframe-8h`). Mismo patrón que el baseline (3 anulados allí), sin huella en el store: correcto.
- Reconciliación con la línea declarada del ladder (`documentation.md`): «182 identity collisions (37 deterministic-equivalent accumulations, 128 semantic-equivalent merges, 17 divergent), 139 semantic-equivalence reviews, 17 windows rejected». Los 17 divergentes coinciden exactamente con esta auditoría; los contadores de merges (128/37) usan definiciones propias del run que no cuadran 1:1 con los 153 merges físicos verificados (117 semánticos + 36 deterministas) ni con las 71 invocaciones (+ caché). Los veredictos cacheados (58 merges + 1 rechazo) no dejan rastro en `provider_invocations`.

---

## 4. Las 38 acumulaciones (auditoría física)

Re-verificación independiente (no sólo el PASS declarado): para cada uno de los 38 records con ≥2 ventanas se recomputaron, desde `claims.jsonl` + las respuestas de `claims.reconstruction`, la igualdad `statement` canónico = rendering first-observed, la unión exacta de `evidence_ids` (sorted-unique), la unión exacta de `provenance.invocation_ids` (todas resuelven a invocaciones reales) y la cobertura de `dependency_edges` sobre toda la evidencia. **38/38 CORRECT_ACCUMULATION; 0 PROBLEMATIC** (coincide con el PASS de `accumulations.json`).

Vía de decisión de los **153 merges** (ventanas 2..n de cada record), reconstruida exhaustivamente:

| Vía | n | Verificación |
|---|---|---|
| Review live EQUIVALENT | 59 | Existe invocación VALIDATED para (record, ventana) con veredicto EQUIVALENT |
| Caché de par EQUIVALENT | 58 | El par (statement canónico, statement propuesto) fue adjudicado EQUIVALENT en otra invocación; sin llamada nueva |
| Determinista idéntico | 36 | Statement propuesto idéntico al canónico tras normalización (minúsculas/comillas/espacios) |
| DIVERGENT fusionado | **0** | — |
| Sin adjudicación | **0** | — |

El statement canónico quedó siempre en el rendering first-observed (38/38), la unión nunca cambió de significado y ningún record acumuló una propuesta DIVERGENT. Ejemplos verificados: `cl-instrumento-eurusd` (56 ventanas, 55 merges, todos paráfrasis EURUSD), `cl-chart-instrument-eurusd` (14 ventanas), `cl-chart-timeframe-8h` (6), `cl-cierre-fuera-deja-de-ser-rango` (w0076→w0077, el par que el baseline había partido en w0077/w0078: hoy mergeado correctamente), `cl-cambiar-temporalidad-diaria` (w0017→w0027, par modalidad anuncio/paso aceptado).

Nota metodológica: el flag `applied` de `equivalence_rows.json` (22) subcuenta los merges porque el detalle del stage `EVIDENCE_ACCUMULATED` sólo nombra la primera ventana acumulada de cada record; los merges reales verificados físicamente son 153.

---

## 5. Falsos splits: comparison con el baseline (¿evitó el candidato w0078/w0028?)

- **Falsos splits claros: 6** (w0004 negación universal/genérica, w0006 modalidad pintar-vela, w0054 «nuestro/el doble», w0066 y w0088/w0093 paráfrasis instrumento-gráfico / activo-mostrado 8h) **+ 1 AMBIGUOUS resuelto DIVERGENT** (w0029 qualifier temporalidad-diaria). Tasa de sobre-rechazo: 7/71 = **9,9 %** de las reviews (baseline: 2 claros + 2 ambiguos sobre 17 = 11,8 %). Todos en la dirección segura (costo de cobertura, no de integridad), consistentes con «when in doubt, DIVERGENT».
- **Análogo w0078 (regla «cierre fuera» con qualifiers menores): EVITADO.** El baseline rechazó w0078 (AMBIGUOUS); el candidato adjudicó el par equivalente w0076→w0077 como EQUIVALENT y lo mergeó físicamente (§4).
- **Análogo w0028 (modalidad obligación/imperativo): PARCIAL.** El patrón se aceptó en #11 (cambiar a temporalidad diaria) pero se rechazó en w0006 (pintar la vela): el reviewer es inconsistente entre pares modalmente idénticos.
- **Análogo w0094 (definitez «La»/«Una»): no se reprodujo** (esa proposición SMT no generó revisión en el candidato).
- Persisten dos formas de sobre-rechazo propias del reviewer: paráfrasis con cambio de sujeto co-referente (instrumento/gráfico, activo/mostrado — 3 de los 6 falsos splits) y caída de un qualifier contextual (w0029). 3 de los 6 falsos splits concentran el mismo defecto: no tratar adjetivos co-referentes («mostrado»/«activo»/«principal») como no-materiales.

---

## 6. Estabilidad kind/epistemic old vs new

| Métrica | Baseline (full-live-v2) | Candidato (rerun @ 19b44c1) |
|---|---|---|
| Divergencias deterministas | 16 (12 kind + 2 epistemic + 2 estructurales) | **6 (2 kind + 4 epistemic + 0 estructurales)** |
| % inestabilidad de clasificación (no semántica) | 15/16 | **6/6** |
| Colisiones totales | 38 | 17 (11 semánticas + 6 deterministas) |
| Ventanas rechazadas por identidad | 22 | **17** (de 130, mismas ventanas) |
| Único TRUE_DIVERGENCE determinista | w0118 (contenido genuinamente distinto) | **ninguno** |
| Colisiones estructurales (relation endpoint) | 2 | **0** (146 relations, sin colisiones) |

La revisión semántica prácticamente eliminó la conversión de ruido de clasificación en rechazo (16 → 6 deterministas, sin casos estructurales ni TRUE_DIVERGENCE determinista) y desplazó la carga hacia el reviewer, que acierta el 85 % de las veces pero introduce 6 falsos splits propios (§5). El reviewer mismo es internamente estable (0 conflictos en pares repetidos). La inestabilidad restante vive aguas arriba, en la recon: los 6 flips son atribución kind/epistemic de deícticos dual-fuente (el instructor enuncia lo que se ve) — exactamente el patrón 1/2/4 del baseline, ahora con un tercio de los casos.

---

## 7. Fragmentación del store old vs new

Identidad por statement NORMALIZADO (minúsculas, sin comillas/puntuación/espacios extra) entre ids distintos:

| Métrica | Baseline | Candidato |
|---|---|---|
| Grupos con statement byte-idéntico en ids distintos | — | **29 grupos / 68 records / 77 pares** |
| Pares byte-idénticos | 13 pares (26 records) | **77 pares** |
| Grupos normalizado-idéntico | — | 30 grupos / 70 records / 78 pares |

Familia «el gráfico es EURUSD» (proposición «lo mostrado es EURUSD»):

- **13 records core** (baseline ~12): 10 con el statement **byte-idéntico** «El instrumento mostrado es EURUSD.» (`cl-chart-eurusd`, `cl-chart-instrument-eurusd`, `cl-chart-symbol-eurusd`, `cl-displayed-instrument-eurusd`, `cl-eurusd`, `cl-eurusd-instrument`, `cl-eurusd-instrumento`, `cl-instrument-eurusd`, `cl-instrumento-mostrado-eurusd`, `cl-symbol-eurusd` — mezcla de slugs inglés/español) + `cl-instrumento-eurusd` («indicado en el encabezado», ya acumulador de 56 ventanas), `cl-instrumento-cabecera-eurusd`, `cl-instrumento-principal-eurusd` («El gráfico mostrado corresponde a EURUSD»).
- **~18 records extendidos** sumando las variantes de etiqueta de la comparación SMT (`cl-chart-left-eurusd`, `cl-eurusd-diagram-label`, `cl-left-sequence-eurusd`, `cl-trayectoria-eurusd-izquierda`, `cl-smt-ejemplo-eurusd`).

Otras familias semánticas obvias (misma proposición con otras palabras): temporalidad 15m ~12 records (3 grupos normalizado-idénticos: `cl-15m-timeframe`/`cl-eurusd-15m-timeframe`/`cl-temporalidad-mostrada-15m`; `cl-chart-timeframe-15m`/`cl-timeframe-15m`; `cl-temporalidad-15m`/`cl-timeframe-eurusd-15m`, más 5 renderings únicos), temporalidad 8h ~8, fuente FOREX.com ~9 (`cl-chart-source-forex-com`/`cl-source-forex-com` byte-idénticos; «fuente/plataforma/proveedor/broker»), fecha 24/6/2025 4 (3 byte-idénticos + 1 sin «en el gráfico»), eje/cotización USD ~10, y una cola larga de pares bilingües slug-español vs slug-inglés (`cl-objetivo-alcista`/`cl-bullish-objective`, `cl-rango-diario-alcista`/`cl-daily-range-bullish`, `cl-rangos-son-importantes`/`cl-ranges-are-important`, `cl-segundo-rectangulo-negro`/`cl-second-black-rectangle-appears`, etc.).

**Diagnóstico:** el ladder funciona intra-id (153 acumulaciones correctas), pero la identidad **nunca se fuerza cross-slug**: la recon sigue emitiendo un slug nuevo por ventana para las proposiciones de metadato del gráfico, y cada slug nuevo funda un record canónico propio aunque el statement sea byte-idéntico. El candidato multiplicó la duplicación byte-idéntica del baseline por ~6 (13 → 77 pares) porque la mayor densidad de re-observaciones que antes se perdía con las ventanas rechazadas ahora se conserva — pero conservada bajo ids paralelos. El costo del ruido de identidad sigue siendo duplicación, ahora con mejor cobertura.

---

## 8. Consecuencia de cobertura de los 17 rechazos

Cruce de los 227 claims propuestos en las 17 ventanas rechazadas contra el store final (statement propio o similitud lexical ≥ 0,75):

- **~38 % del contenido propuesto existe en el store** (estimación de piso por matching lexical; parte del contenido existe con paráfrasis que el matcher no captó, p. ej. los cierres «0500» de w0122 sí están como `cl-cierre-0500`/`cl-reference-close-0500`). Aun con ese margen, la pérdida aparente es muy superior al ~10–15 % estimado en el baseline (~85–90 % de re-cobertura por vecinos).
- Pérdidas concretas verificadas por búsqueda dirigida: lecturas de la herramienta de posición long (objetivo 0,00881, apertura 0,00937, RR 8,65 y 10,49, cantidad 4.761.904 — el store sólo conserva los RR 1 y 1,91 y el stop 0,00084→0,00170), «longs brutales aquí», la serie de decisiones post-ruptura del rango de w0081, la configuración SMT de w0088 (grupos EURUSD/GBPUSD cuerpo a cuerpo) y las anotaciones 0100/0500 hora Nueva York (parcialmente presentes).
- El peor costo lo dejan los dos rechazos **deterministas** finales: w0127 (23 de 27 claims sin cobertura) y w0128 (15 de 18), ambos por flips epistémicos de la misma proposición (§1 casos 4 y 6). La auto-reparación por ventanas vecinas del baseline fue aquí mucho menos eficaz: las ventanas grandes y tardías del capítulo concentran contenido único que ningún vecino re-propone.

---

## 9. Archivo de datos

`results/identity-audit.jsonl` — 78 filas: 71 `equivalence` (las adjudicaciones live; incluye los 10 DIVERGENT que son a su vez las colisiones semánticas live) + 7 `collision` (6 deterministas sin review + w0093 servida por caché). Cada fila: caso, target, ventanas, ambos statements, veredicto del modelo, clasificación humana, flag material y justificación.

## FEEDBACK (Agents-OS)

- Bootstrap cumplió su contrato en one-shot: marker resuelto, base mínima cargada, gate de dominio en DEFAULT (cero matches), sin lecturas amplias del vault. La sesión fue un subagente de fase con cierre explícito pedido en el brief; el routing directo a `agents-os-session-close` al final funcionó sin necesidad de skill adicional para la auditoría misma.
- Fricción de entorno (no de OS): `sqlite3` CLI no existe en esta máquina y hubo que caer a Python stdlib; si las fases de aceptación van a seguir auditando `run.db`, vale un runbook de una línea con el one-liner Python (o instalar sqlite3).
- Fricción de contrato de fase: el brief traía cifras que no cuadran con la fuente (60/11 vs 61/10 real; «38 acumulaciones» sí exacto). Recomendación: que los briefs de fase citen el `documentation.md` del run como fuente única de cifras o marquen explícitamente las cifras como «esperadas, verificar». Prefiero asumir la fuente siempre, pero el costo de la divergencia se paga en re-trazado.
- Regla `[DURA]` anti hard-wrap: en documentos largos como este, el render de tablas + regla de una-línea-por-párrafo convive bien, pero el brief pedido exige celdas de tabla muy densas; ninguna fricción real, sólo señalizarlo como patrón ya validado para reports de auditoría.
- El reporte al coordinator debe ser el resumen ejecutivo completo (colisiones por causa, clasificación humana, falsos merges, fragmentación, estabilidad, hard-failure) — entregado al final de la sesión, junto con el feedback, sin inventario de memorias.
