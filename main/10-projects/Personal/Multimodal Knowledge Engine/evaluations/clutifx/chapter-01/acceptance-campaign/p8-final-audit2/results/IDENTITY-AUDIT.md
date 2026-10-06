# IDENTITY-AUDIT — Ladder de identidad, capítulo 01 Clutifx (run P7b @ e7bc387)

Auditoría fuente-grounded del P8 final (segunda pasada, post-P7b) sobre las **59 llamadas `claims.equivalence_review`**, los **veredictos servidos desde caché**, las **11 identity collisions** que rechazaron ventana y las **32 acumulaciones aplicadas** del run `clutifx-ch01-rerun2-20261004/run-rerun2` (store canónico: 766 claims + 104 relations; 130 ventanas del capítulo, 131 intentos de recon: 82 aceptadas, 49 rechazadas — 38 por provider-unavailable y 11 por identidad; w0028 entró vía re-run correctivo tras un primer recon REJECTED por evidence ref malformada «asr-00052 [362440-381560]»; status final INCOMPLETE por diseño, con los rechazos en `status_reasons`).

Fuentes auditadas: `run.db` (`provider_invocations`, `pipeline_state.status_reasons`, `record_stages`, `pipeline_records`, `dependency_edges`), store canónico `claims.jsonl`, respuestas de reconstrucción por ventana (incluida la línea `w0028:corrective`), análisis precomputado `equivalence_rows.json` + `accumulations.json` + `metrics.json`, `documentation.md` (línea del ladder), y los informes `p1-audit/results/IDENTITY-AUDIT.md` (baseline full-live-v2) y `p8-final-audit/results/IDENTITY-AUDIT.md` (candidato P7 @ 19b44c1). Toda clasificación humana se hizo leyendo los DOS statements de cada caso (request_json / status_reasons / respuestas de recon) con juicio semántico propio.

Veredicto agregado en una línea: **0 falso merges (hard-failure PASS: 0 FALSE_EQUIVALENT live y 0 aplicado-material sobre 111 merges verificados físicamente), 3 falsos splits claros + 1 ambiguo sobre 59 reviews (6,8 %, mejorando el 9,9 % de P7 y el 23,5 % del baseline), 5/5 divergencias deterministas son inestabilidad de clasificación (P7 6/6, baseline 15/16, sin casos estructurales), 32/32 acumulaciones PASS con verificación física independiente y los 111 merges explicados al 100 % (49 live + 7 caché + 55 deterministas, 0 DIVERGENT fusionado, 0 sin adjudicar), el reviewer es internamente estable en pares repetidos (0 conflictos) pero mostró 1 inconsistencia interna real (D4 w0062 vs E48 w0087: mismo mapeo etiqueta→fuente con veredictos opuestos), la caché sólo sirvió merges (7) y ningún rechazo —a diferencia de P7 (58 merges + 1 rechazo cacheado)—, y la fragmentación cross-slug MEJORÓ respecto de P7 (40 pares byte-idénticos vs 77) sin volver al baseline (13), con la cobertura de los 11 rechazos en ~47 % (intermedia entre el ~38 % de P7 y el ~85–90 % del baseline).**

Nota sobre el brief: el brief anunciaba «5 semánticas DIVERGENT + 3 epistemic + 2 kind + 1 otra» y pedía identificar adjudicaciones de caché «sin invocación». La fuente muestra **6 semánticas DIVERGENT + 3 epistemic + 2 kind** (la «1 otra» no existe: las 11 se descomponen 6+3+2) y **0 veredictos de rechazo servidos por caché**: las 6 semánticas tienen invocación live propia; la caché sólo transfirió 7 merges EQUIVALENT. Cifras del brief tratadas como esperadas-y-a-verificar; manda la fuente.

---

## 1. Las 11 identity collisions (rechazos de ventana)

Composición verificada contra `pipeline_state.status_reasons` y `metrics.json` (`rejected_detail`: 49 ventanas rechazadas = 38 provider-unavailable + 11 identity divergence): **5 deterministas** (2 kind-flip + 3 epistemic-flip + **0 estructurales**; en los 5 casos el stage cierra «window rejected closed without an equivalence review») + **6 semánticas DIVERGENT** (todas con invocación live VALIDATED; w0023, w0044, w0058, w0062, w0073, w0077). Ningún rechazo fue servido por caché (a diferencia del w0093 de P7).

| # | Window | Record | Causa | Store (A) vs Entrante (B) | Clasificación |
|---|---|---|---|---|---|
| 1 | w0006 | `cl-range-taking-candle-closes-inside` | deterministic / kind (claim vs rule) | «La vela que toma un extremo de la vela anterior cierra dentro de esa vela anterior» (claim) vs «Para identificar un rango, esa vela distinta cierra dentro de la vela de referencia» (rule) | **MODEL_CLASSIFICATION_INSTABILITY** (misma condición técnica; el propósito «para identificar un rango» añadido en B indujo el flip de kind) |
| 2 | w0008 | `cl-rango-alcista` | deterministic / epistemic (INSTRUCTOR_SAID vs VIDEO_OBSERVED) | «El rango mostrado es un rango alcista en este caso» vs «El rango mostrado es un «rango alcista»» | **MODEL_CLASSIFICATION_INSTABILITY** (B sólo añade comillas de rótulo y cae «en este caso»; deíctico dual-fuente; el record sí se acumuló luego en w0012 vía E6 EQUIVALENT) |
| 3 | w0023 | `cl-precio-completa-rango-bajista` | semantic / DIVERGENT (live) | «El precio va a completar el rango bajista central.» vs «El precio va a completar ahora el rango bajista.» | **TRUE_DIVERGENCE** (deltas mutuos: A porta «central» —qué rango—, B porta «ahora» —inmediatez—; ninguno implica al otro) |
| 4 | w0044 | `cl-candle-takes-range-low` | semantic / DIVERGENT (live) | «La vela en cuestión ha tomado el low de este rango.» vs «La vela dibujada ha tomado el low del rango dibujado.» | **FALSE_DIVERGENT** (sólo varían los deícticos co-referentes «en cuestión/este» vs «dibujada/dibujado»; mismo predicado y valor) |
| 5 | w0054 | `cl-rango-pendiente-doble-alcista` | deterministic / kind (claim vs rule) | «En el caso pendiente, el doble es alcista» (claim) vs «El rango pendiente se abre con un doble alcista» (rule) | **MODEL_CLASSIFICATION_INSTABILITY** (mismo hecho de estrategia con re-framing del sujeto; el re-framing induce el flip claim→rule; marginal) |
| 6 | w0058 | `cl-candle-takes-range-low` | semantic / DIVERGENT (live) | «La vela en cuestión ha tomado el low de este rango.» vs «En tiempo real, la vela tomó el low del rango pendiente.» | **AMBIGUOUS** (núcleo idéntico; B añade el qualifier deíctico-contextual «en tiempo real»; resolución DIVERGENT fail-closed contract-consistente) |
| 7 | w0061 | `cl-timeframe-8h` | deterministic / epistemic (INSTRUCTOR_SAID vs VIDEO_OBSERVED) | «El gráfico se muestra en 8h» vs «La temporalidad mostrada es 8h» | **MODEL_CLASSIFICATION_INSTABILITY** (misma proposición; flip epistémico puro) |
| 8 | w0062 | `cl-fuente-forex-com` | semantic / DIVERGENT (live) | «La cabecera del gráfico muestra «FOREX.com».» vs «La fuente del gráfico es FOREX.com.» | **FALSE_DIVERGENT** (mismo mapeo etiqueta→fuente que E48, donde el MISMO reviewer aceptó «El encabezado del gráfico indica «FOREX.com»» ≈ «La fuente indicada en el gráfico es FOREX.com» como EQUIVALENT: inconsistencia interna demostrada) |
| 9 | w0073 | `cl-divisa-usd` | semantic / DIVERGENT (live) | «El eje de precios del gráfico está expresado en USD.» vs «La divisa seleccionada es USD.» | **TRUE_DIVERGENCE** (B añade el estado de selección de plataforma, no observable en A; la variante co-referente correcta «La divisa del eje de precios es USD» sí fue aceptada como EQUIVALENT en E10) |
| 10 | w0077 | `cl-idea-alcista-esperar-nueva-vela` | semantic / DIVERGENT (live) | «Si tenemos una idea alcista, tendremos que esperar a una nueva vela.» vs «Si tenemos una idea alcista, tendremos que esperar ahora a una nueva vela.» | **FALSE_DIVERGENT** (único delta «ahora», muletilla discursiva que no altera la regla condicional) |
| 11 | w0084 | `cl-timeframe-8h` | deterministic / epistemic (INSTRUCTOR_SAID vs VIDEO_OBSERVED) | «El gráfico se muestra en 8h» vs «El gráfico principal usa el marco temporal de 8h» | **MODEL_CLASSIFICATION_INSTABILITY** (segundo flip del mismo record tras w0061, con statement B distinto: inestabilidad sistemática sobre la misma proposición) |

Saldo de los 11 rechazos: **5 inestabilidad de clasificación determinista + 3 falsos splits semánticos + 1 ambiguo resuelto DIVERGENT = 9 rechazos injustificados (82 %); 2 rechazos correctos (w0023, w0073, 18 %)**. Ningún rechazo protegió al store de un merge dañino. Patrón nuevo respecto de P7: el reviewer ya NO parte por qualifiers añadidos («inicial», E23) ni por definitez («una/la», E41) — los dos falsos splits por paráfrasis restante son el cambio de sujeto co-referente display→atribución (w0062) y la partícula discursiva «ahora» (w0077).

---

## 2. Las 59 adjudicaciones live (claims.equivalence_review)

Las 59 invocaciones están `VALIDATED`, contrato `mke.claims-equivalence-prompt.v1` (idéntico al baseline y a P7), modelo `stealth/space-bunny-alpha`, con la instrucción congelada «when in doubt, answer DIVERGENT» y las clases materiales (negación, números, condiciones, qualifiers, dirección, modalidad, scope). Veredictos: **53 EQUIVALENT / 6 DIVERGENT** (coincide con `metrics.json` y con `equivalence_rows.json`).

| Veredicto | n | Clasificación del auditor |
|---|---|---|
| EQUIVALENT | 53 | **53 CORRECT_EQUIVALENT, 0 FALSE_EQUIVALENT** (7 marginales-but-defendables aplicados: E6 w0012, E8 w0021, E13 w0029, E23 w0055, E36 w0070, E41 w0078, E48 w0087; + E46 w0084 anulado por rechazo de ventana) |
| DIVERGENT | 6 | 3 FALSE_DIVERGENT (casos 4, 8, 10 de §1), 2 TRUE_DIVERGENCE (casos 3, 9), 1 AMBIGUOUS (caso 6) |

Los 53 EQUIVALENT son paráfrasis genuinas de la misma proposición: familias EURUSD-instrumento/símbolo (14), temporalidad 15m (15), 8h (3), fuente FOREX.com (3), fecha 24/6/2025 (5), divisa/eje USD (2), regla cierre-fuera (2), y misceláneos correctos (rótulo RANGO PENDIENTE, rangos base de la estrategia, rangos bearish-Libra-SMT, temporalidad diaria, rango alcista). Los deltas aceptados son siempre no-materiales: comillas («EURUSD»/«15M» vs sin comillas), «mostrado» vs «indicado»/«visible»/«del gráfico», 15M vs «de 15 minutos», elipsis contextuales, registro («vais a ver» vs «se verán», con caída de «ya»), y bilingüismo bullish/alcista (E24). **El caso más laxo del run es E41** («Si una vela cierra fuera…» genérico vs «Si la vela cierra fuera…» específico: definitez una/la, exactamente el patrón w0094 del baseline, aquí juzgado EQUIVALENT): defendible porque el predicado y la condición son idénticos y el merge no distorsiona (el canónico queda en la formulación genérica), pero marca que el umbral de laxitud se movió respecto del baseline. E23 (añade «inicial») es el segundo más discutible; ninguno de los dos produce daño material en el store.

**Auto-consistencia del reviewer:** los 59 requests contienen 58 pares de statements distintos; 1 par se repitió en dos ventanas («El instrumento del gráfico mostrado es EURUSD.» / «El instrumento mostrado es EURUSD.», E30 y E52) y en ambos el veredicto fue EQUIVALENT. **0 conflictos de veredicto sobre pares idénticos.**

**Inconsistencia interna (nueva, no existía en P7):** el mapeo display→atribución se resolvió de forma opuesta en dos familias: D4 (w0062: «cabecera muestra «FOREX.com»» vs «fuente es FOREX.com» → DIVERGENT) contra E48 (w0087: «fuente indicada» vs «encabezado indica «FOREX.com»» → EQUIVALENT) y E36 (w0070: «etiqueta de temporalidad es «15M»» vs «timeframe es 15M» → EQUIVALENT). El reviewer no tiene un criterio estable sobre cuándo la etiqueta visible y la propiedad atribuida son la misma proposición; costó 1 rechazo injustificado (w0062).

---

## 3. Falsos merges y hard-failure check

- **FALSE_EQUIVALENT: 0 de 59 reviews; 0 de 56 merges semánticos aplicados (49 live + 7 por caché) y 0 de 55 acumulaciones deterministas (todas byte-idénticas).** Ningún merge unió proposiciones materialmente distintas; ningún DIVERGENT terminó fusionado (verificado ventana a ventana en §4).
- **Hard-failure check: applied material FALSE_EQUIVALENT = 0 → PASS.**
- Política whole-window consistente: 4 veredictos EQUIVALENT correctos fueron anulados porque la ventana entrante se rechazó por OTRA colisión del mismo window (E4 w0006, E24 w0061, E39 w0077, E46 w0084). Sin huella en el store: correcto. Nota: la regla «cierre fuera del rango» (análogo del w0078 del baseline) fue finalmente mergeada por E41 en w0078, la ventana siguiente a la anulada w0077.
- Caché content-addressed: **7 merges transferidos sin invocación nueva**, todos con par byte-idéntico a una revisión live previa («El instrumento mostrado es EURUSD.»+«…mostrado en el gráfico…» ×4 desde E44; «…es de EURUSD» ×1 desde E50; «El marco temporal mostrado es 15M.»+«La temporalidad mostrada es 15M.» ×2 desde E37). Transferencia sound (mismo par ⇒ mismo veredicto), pero invisible en el journal de proveedor (mismo hallazgo de auditabilidad que P7, allí con 58 merges + 1 rechazo; aquí 7 merges + 0 rechazos).

---

## 4. Las 32 acumulaciones (auditoría física)

Re-verificación independiente (no sólo el PASS declarado): para cada uno de los 32 records con ≥2 ventanas se recomputaron, desde `claims.jsonl` + las respuestas `claims.reconstruction` VALIDATED de las ventanas efectivas, la igualdad statement canónico = rendering first-observed, la unión exacta de `evidence_ids` (sorted-unique), la unión exacta de `provenance.invocation_ids` (todas resuelven a invocaciones recon VALIDATED reales), la uniformidad de kind/epistemic entre todos los renderings fusionados y la correspondencia ventana-a-ventana de `windows_observed`. **32/32 CORRECT_ACCUMULATION; 0 PROBLEMATIC** (coincide con el PASS de `accumulations.json`); kind y epistemic uniformes en 32/32.

Vía de decisión de los **111 merges** (ventanas 2..n de cada record), reconstruida exhaustivamente:

| Vía | n | Verificación |
|---|---|---|
| Review live EQUIVALENT | 49 | Existe invocación VALIDATED para (record, ventana) con veredicto EQUIVALENT; coincide 1:1 con las 49 reviews EQUIVALENT de ventanas aceptadas |
| Caché de par EQUIVALENT | 7 | El par (canónico, propuesto) fue adjudicado EQUIVALENT en otra invocación; sin llamada nueva |
| Determinista idéntico | 55 | Statement propuesto byte-idéntico al canónico (55/55; sin casos de igualdad sólo-tras-normalización) |
| DIVERGENT fusionado | **0** | — |
| Sin adjudicación | **0** | — |

El statement canónico quedó siempre en el rendering first-observed (32/32). Top-acumuladores: `cl-instrumento-eurusd` (45 ventanas, 44 merges), `cl-timeframe-15m` (9), `cl-temporalidad-15m` (8), `cl-chart-instrument-eurusd` (6), `cl-chart-timeframe-15m` (5), `cl-chart-source-forex-com` y `cl-chart-symbol-eurusd` (4 cada uno). Ejemplo de auto-reparación post-rechazo: `cl-rango-alcista` fue rechazado en w0008 por flip epistémico (caso 2 de §1) y acumuló correctamente en w0012 vía E6 EQUIVALENT.

Eventos nuevos verificados: (a) **re-run correctivo w0028** — el primer recon de w0028 fue REJECTED por citar la evidence ref malformada «asr-00052 [362440-381560]»; el re-invocador (`w0028:corrective`) produjo salida VALIDATED con statements regenerados (p. ej. «La temporalidad utilizada en este ejemplo es la diaria (1D)»), y toda la cadena de revisión/merge (E12, E13) y el store usan la línea correctiva, con el union de evidencia/invocaciones cuadrando exactamente; (b) el flag `applied` de `equivalence_rows.json` (23) y `metrics.identity.merges_applied` (23) **subcuentan** los merges live reales (49) porque el detalle del stage `EVIDENCE_ACCUMULATED` sólo nombra la primera ventana acumulada de cada record — mismo artefacto documentado en P7; los merges físicos verificados son 111.

---

## 5. Falsos splits: comparación baseline → P7 → P7b

- **Falsos splits claros: 3** (w0044 deícticos co-referentes, w0062 display→atribución, w0077 «ahora») **+ 1 AMBIGUOUS resuelto DIVERGENT** (w0058, «en tiempo real»). Tasa de sobre-rechazo: 4/59 = **6,8 %** de las reviews (P7: 7/71 = 9,9 %; baseline: 4/17 = 23,5 %). Tendencia de mejora continua del reviewer a lo largo de los tres runs. Todos en la dirección segura (costo de cobertura, no de integridad), consistentes con «when in doubt, DIVERGENT».
- **Análogo w0078 (regla «cierre fuera»): RESUELTO.** El baseline lo rechazó (AMBIGUOUS); P7 lo mergeó (w0076→w0077); P7b lo mantiene mergeado y además aceptó la variante con definitez una/la (E41, w0076→w0078), el patrón w0094 del baseline, ahora como verdict marginal-correcto.
- **Análogo w0028 (modalidad obligación/imperativo): no se reprodujo** (no hay pares modalmente divergentes en P7b).
- **Análogo w0094 (definitez «La»/«Una»): reapareció y se aceptó** (E41): el reviewer de P7b es más laxo que el del baseline en definitez, sin daño material verificado.
- Persiste el defecto de sujeto co-referente que ya concentraba 3 de los 6 falsos splits de P7 (instrumento/gráfico, activo/mostrado): aquí costó w0062 (cabecera/fuente). El otro defecto residual es la sensibilidad a partículas discursivas («ahora», w0077). El qualifier añadido («inicial», E23) ya NO produce split: el péndulo se movió hacia el lado laxo en ese eje.

---

## 6. Estabilidad kind/epistemic baseline → P7 → P7b

| Métrica | Baseline (full-live-v2) | P7 (rerun @ 19b44c1) | **P7b (rerun2 @ e7bc387)** |
|---|---|---|---|
| Divergencias deterministas | 16 (12 kind + 2 epistemic + 2 estructurales) | 6 (2 kind + 4 epistemic + 0 estructurales) | **5 (2 kind + 3 epistemic + 0 estructurales)** |
| % inestabilidad de clasificación (no semántica) | 15/16 | 6/6 | **5/5** |
| Único TRUE_DIVERGENCE determinista | 1 (w0118, contenido genuinamente distinto) | 0 | **0** |
| Colisiones estructurales (relation endpoint) | 2 | 0 | **0** (104 relations, sin colisiones) |
| Colisiones semánticas | 6 | 11 (10 live + 1 caché) | **6 (6 live + 0 caché)** |
| Colisiones totales / ventanas rechazadas por identidad | 38 / 22 | 17 / 17 | **11 / 11** (de 130 ventanas) |

Los 5 flips son atribución kind/epistemic del recon sobre deícticos dual-fuente (el instructor enuncia lo que se ve: 3 epistemic) y sobre re-framings de formulación (2 kind: propósito añadido y cambio de sujeto). El caso más severo es `cl-timeframe-8h`, que flippeó DOS VECES (w0061 y w0084) con statements entrantes distintos: la inestabilidad es sistemática sobre esa proposición, no puntual. La revisión semántica mantiene el patrón logrado en P7: prácticamente todo el rechazo por identidad es ya decisión del reviewer (6 de 11) y no ruido de clasificación (5 de 11), y el reviewer acierta el 82 % de las colisiones (falsos splits 4 de 11 contando el ambiguo).

---

## 7. Fragmentación del store baseline → P7 → P7b

Identidad por statement (byte-idéntico = igualdad exacta; normalizado = minúsculas, sin comillas/puntuación, espacios colapsados) entre ids distintos:

| Métrica | Baseline | P7 (@19b44c1) | **P7b (@e7bc387)** |
|---|---|---|---|
| Pares byte-idénticos | 13 pares (26 records) | 77 pares (68 records) | **40 pares (48 records)** |
| Grupos byte-idénticos | — | 29 grupos | **17 grupos** |
| Grupos normalizado-idéntico / pares | — | 30 grupos / 78 pares | **18 grupos / 41 pares** |

La duplicación byte-idéntica bajó ~2× respecto de P7 (77 → 40 pares) pero sigue ~3× por encima del baseline (13). Familias núcleo en P7b:

- **«Lo mostrado es EURUSD» (~17 records núcleo + ~19 extendidos con EURUSD en el statement):** 6 records con statement **byte-idéntico** «El instrumento mostrado es EURUSD.» (`cl-chart-instrument-eurusd`, `cl-eurusd`, `cl-eurusd-instrument`, `cl-grafico-instrumento-eurusd`, `cl-instrumento-eurusd`, `cl-instrumento-mostrado-eurusd`; mezcla de slugs inglés/español) + variantes de sujeto co-referente (`cl-instrument-eurusd` «del gráfico mostrado», `cl-chart-symbol-eurusd`/`cl-simbolo-grafico-eurusd` «símbolo», `cl-eurusd-instrumento`/`cl-chart-eurusd` «gráfico principal/corresponde», `cl-instrumento-grafico-eurusd` «etiquetado como», + etiquetas de serie y diagramas SMT).
- **Temporalidad 15m (17 records con 15M/15 minutos, ~11 núcleo):** 3 grupos byte-idénticos (`cl-eurusd-15m-timeframe`/`cl-marco-temporal-15m`/`cl-timeframe-15m`; `cl-temporalidad-15m`/`cl-temporalidad-mostrada-15m`; + «El timeframe del gráfico mostrado es 15M.» en `cl-chart-timeframe-15m` singleton de su texto) y paráfrasis «de 15 minutos».
- **Temporalidad 8h (10 records, ~6 núcleo):** sin pares byte-idénticos tras la deduplicación de P7, pero `cl-timeframe-8h`/`cl-chart-timeframe-8h`/`cl-temporalidad-8h`/`cl-temporalidad-grafico-8h`/`cl-marco-temporal-8h`/`cl-grafico-temporalidad-8h` coexisten como paráfrasis paralelas — incluidos los dos records enfrentados por los flips epistémicos (`cl-timeframe-8h` vs el accumulateador `cl-chart-timeframe-8h`).
- **Fuente FOREX.com (8 records):** `cl-cabecera-forex-com`/`cl-fuente-forex-com` byte-idénticos; «fuente/etiqueta de fuente/encabezado/serie» como variantes.
- **Fecha 24/6/2025 (4 byte-idénticos en un grupo), eje/moneda USD (~11 núcleo: 3 byte-idénticos «El eje de precios está expresado en USD.» + 2 «La moneda del eje de precios es USD.» + divisa/selector/cotización), y una cola larga de pares bilingües slug-español vs slug-inglés** (`cl-smt-dos-tipos`/`cl-smt-two-types`, `cl-turtle-soup-requiere-toma-liquidez`/`cl-turtlesoup-toma-liquidez`, `cl-cantidad-apertura`/`cl-position-quantity`, `cl-objetivo-diferencia`/`cl-position-target-value`, `cl-stop-diferencia`/`cl-position-stop-value`, `cl-rango-alcista-completado`/`cl-rango-alcista-se-completa`, `cl-paleta-colores-abierta`/`cl-drawing-color-palette-open`, `cl-estrategia-basa-rangos`/`cl-estrategia-se-basa-principalmente-en-rangos`, etc.).

**Diagnóstico (estable desde el baseline):** el ladder funciona intra-id (111 acumulaciones correctas, `cl-instrumento-eurusd` con 45 ventanas) pero la identidad **nunca se fuerza cross-slug**: la recon sigue emitiendo un slug nuevo por ventana para los metadatos del gráfico y cada slug nuevo funda un record canónico propio aunque el statement sea byte-idéntico — el caso extremo es el grupo de 6 records «El instrumento mostrado es EURUSD.», uno de los cuales (`cl-instrumento-eurusd`) acumuló 45 ventanas mientras sus 5 hermanos byte-idénticos quedaron congelados. El Mejor valor de P7b se explica por la menor densidad de re-observaciones rechazadas (menos ventanas perdidas que re-importan contenido bajo ids nuevos) y por la mejora del reviewer; el costo del ruido de identidad sigue siendo duplicación, no vacíos.

---

## 8. Consecuencia de cobertura de los 11 rechazos

Cruce de los 125 claims propuestos en las 11 ventanas rechazadas contra el store final (statement propio o similitud lexical ≥ 0,75 sobre tokens > 3 chars):

- **59/125 (~47 %) del contenido propuesto existe en el store** (piso por matching lexical; parte existe con paráfrasis que el matcher no captó). Intermedio entre el ~38 % de P7 y el ~85–90 % estimado del baseline: la auto-reparación por ventanas vecinas sigue siendo mucho menos eficaz que en el baseline.
- Pérdidas concentradas y verificadas por búsqueda dirigida: **w0084 (1/8 cubierto — el peor)**: las líneas ascendentes de la comparación SMT EURUSD/GBPUSD y el nuevo alto de EURUSD; **w0006 (3/12)**: la condición inside-bar como regla de identificación de rango y el metadato 5m/USD de esa ventana; **w0058 (3/7)**: la reacción de la vela tras tomar el low y la anticipación del rango pre-cierre; **w0073 (4/9)**: las dos velas blancas/una negra y la línea horizontal sobre la vela blanca; **w0061 (9/15)**: los bordes del rango 1.15325/1.14555 (el store conserva otros niveles, no esos). w0023, w0044, w0054, w0062 y w0077 pierden contenido menor (7/11, 5/10, 8/15, 11/22 y 5/8 cubierto respectivamente), aunque w0077 arrastra además la anulación de E39 (variante nominalizada de la regla cierre-fuera) que sí entró por w0078.
- Los dos rechazos **deterministas** finales (w0061, w0084 — ambos flips epistémicos de `cl-timeframe-8h`) y el determinista temprano (w0006) siguen siendo los de mayor costo, igual que en P7: las ventanas grandes y tardías concentran contenido único que ningún vecino re-propone.

---

## 9. Reconciliación con la línea declarada del ladder (`documentation.md`)

El run declara: «identity ladder: 1004 claims + 125 relations proposed, 3 exact duplicates, 132 identity collisions (59 deterministic-equivalent accumulations, 62 semantic-equivalent merges, 11 divergent), 68 semantic-equivalence reviews, 11 windows rejected». Coincidencias exactas: **11 divergent** y **11 windows rejected**. Discrepancias (contadores proposal-side del run, no store-side): 68 «semantic-equivalence reviews» vs **59 invocaciones reales** en `provider_invocations`; 62 «semantic-equivalent merges» vs **56 físicos** (49 live + 7 caché); 59 «deterministic-equivalent accumulations» vs **55 físicos** (todos byte-idénticos); 1004/125 propuestos vs **766/104 comprometidos** en el store. Mismo patrón de P7: los contadores del ladder usan definiciones propias del run; la fuente física manda.

---

## 10. Archivo de datos

`results/identity-audit.jsonl` — 104 filas: 59 `equivalence` (todas las adjudicaciones live, incluidas las 6 DIVERGENT que son a su vez las colisiones semánticas; marca `applied_merge` y `window_incoming_rejected`), 5 `collision_deterministic` (kind/epistemic sin review, con ambos statements y metadatos), 7 `cache_merge` (transferencias sin invocación), 32 `accumulation` (re-verificación física campo a campo) y 1 `summary` con los totales y el hard gate. Cada fila de caso: ambos statements, veredicto del modelo, clasificación humana, flag material y justificación.

## FEEDBACK (Agents-OS)

- Bootstrap cumplió su contrato en one-shot en esta segunda sesión de auditoría (warm pattern respecto de la P7): marker resuelto, sin lecturas amplias del vault, routing directo al trabajo. El formato de informe con sección FEEDBACK final y cierre explícito en el brief volvió a funcionar sin fricción.
- Fricción de contrato de fase (recurrente, 2º run consecutivo): el brief traía una descomposición de las 11 colisiones que no cuadra con la fuente («5 semánticas + 1 otra» vs 6 semánticas + 3 epistemic + 2 kind reales) y pedía buscar veredictos cacheados de rechazo que en P7b no existen (la caché sólo sirvió 7 merges). Misma recomendación de P7, ahora con más fuerza: que los briefs de fase citen el `documentation.md`/`metrics.json` del run como fuente única y marquen sus cifras como «esperadas, verificar»; el costo de la divergencia se paga en re-trazado y en riesgo de clasificar mal por casación con lo esperado.
- Fricción de layout de artefactos: el directorio de análisis precomputado de P7b vive bajo el run VIEJO (`~/mke/clutifx-ch01-full-live-20261001/analysis-p7b/`) aunque contiene datos del rerun2 (timestamps de 2026-10-04). Recomendación: un `analysis-*/` por directorio de run, o un README de una línea que declare a qué run corresponde cada directorio de análisis.
- Fricción de entorno (recurrente): `sqlite3` CLI sigue sin existir en esta máquina; Python stdlib resuelve, pero el runbook de una línea con el one-liner sugerido en el feedback de P7 seguiría ahorrando el primer intento fallido de cada sesión que toca `run.db`.
- Hallazgo de datos que merecería fix aguas arriba: `metrics.identity.merges_applied` (23) y el flag `applied` de `equivalence_rows.json` subcuentan los merges live reales (49) porque `EVIDENCE_ACCUMULATED` sólo nombra la primera ventana; y los 7 merges por caché no dejan rastro en `provider_invocations`. Un contador físico de merges en `metrics.json` (o un row de caché en el journal con `served_from=pair_cache`) haría la auditoría de identidad directamente reconciliable sin reconstrucción.
- Convención nueva a documentar: los re-runs correctivos introducen window-ids con sufijo (`w0028:corrective`) que no calza 1:1 con los targets de las reviews (`w0028`); una nota en `documentation.md` sobre la convención de sufijos de reintento ahorraría la deducción inversa que hubo que hacer en esta auditoría.
- El reporte al coordinator debe ser el resumen ejecutivo completo (colisiones por causa, clasificación humana, falsos merges, acumulaciones, fragmentación old→P7→P7b, kind-stability, hard gate) — entregado al final de la sesión, junto con este feedback, sin inventario de memorias.
