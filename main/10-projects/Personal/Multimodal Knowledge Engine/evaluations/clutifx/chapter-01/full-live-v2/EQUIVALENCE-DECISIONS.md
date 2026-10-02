# EQUIVALENCE-DECISIONS — todas las identity collisions del capítulo

Autoridad durable: línea `identity ladder` de documentation.md — 1039 claims + 168 relations propuestos, 1 exact duplicate, **38 identity collisions** (1 deterministic-equivalent accumulation, 15 semantic-equivalent merges, 22 divergent), **21 adjudicaciones semánticas** (17 llamadas live + 4 re-verdictos content-addressed desde journal), 22 ventanas rechazadas por el ladder.

## 1. Adjudicaciones semánticas (claims.equivalence_review) — 17 llamadas live

Clasificación humana del operador (no cambia el veredicto del engine; señala diferencias number/negation/direction/condition/qualifier/scope/modality).

| # | Claim | Windows | Verdict engine | Clasificación humana | Applied? |
|---|---|---|---|---|---|
| 1 | `cl-instrumento-eurusd` | w0017→w0024 | EQUIVALENT | **OBVIOUSLY_EQUIVALENT** — misma proposición (qué instrumento muestra el gráfico); «mostrado» vs «del gráfico» no es diferencia material | SÍ (merge) |
| 2 | `cl-observar-formacion-rangos` | w0027→w0028 | DIVERGENT | **AMBIGUOUS** — modality/qualifier: «hay que ir viendo» (obligación progresiva) vs «observar» (imperativo); misma acción y objeto, matiz de modalidad discutible | no (ventana entrante rechazada) |
| 3 | `cl-instrumento-eurusd` | w0017→w0042 | EQUIVALENT | **OBVIOUSLY_EQUIVALENT** — misma proposición; «gráfico abierto» = el gráfico en cuestión | no* |
| 4 | `cl-grafico-eurusd` | w0031→w0057 | EQUIVALENT | **OBVIOUSLY_EQUIVALENT** — notación EUR/USD vs EURUSD únicamente (la normalización conservativa no fusiona separadores interiores por diseño) | SÍ (merge) |
| 5 | `cl-stop-loss-long-debajo-turtle-soup` | w0068→w0069 | EQUIVALENT | **OBVIOUSLY_EQUIVALENT** — misma condición, misma acción (long) y mismo requisito (stop seguro bajo el Turtle Soup); 2ª persona vs impersonal y «tendría» vs «tiene» no cambian la proposición | SÍ (merge) |
| 6 | `cl-cierre-fuera-invalida-rango` | w0077→w0078 | DIVERGENT | **AMBIGUOUS** — sujeto «vela» vs «precio» + predicado «deja de ser un rango» vs «deja de ser válido» (identidad vs validez); materialmente la misma regla, dos diferencias de qualifier | no (ventana entrante rechazada) |
| 7 | `cl-grafico-eurusd` | w0031→w0082 | EQUIVALENT | **OBVIOUSLY_EQUIVALENT** — misma proposición con paráfrasis («muestra el par EURUSD») | no* |
| 8 | `cl-smt-no-requerida-entre-dos-velas` | w0093→w0094 | DIVERGENT | **OBVIOUSLY_EQUIVALENT** — única diferencia: definiteness «La SMT» vs «Una SMT»; la negación de necesidad (no tiene que aparecer/ser) tiene idéntico alcance. Veredicto DIVERGENT = sobre-rechazo conservador (falso split, costo de cobertura) | no (ventana entrante rechazada) |
| 9 | `cl-instrumento-grafico-eurusd` | w0004→w0097 | EQUIVALENT | **OBVIOUSLY_EQUIVALENT** — orden de palabras únicamente | SÍ (merge) |
| 10 | `cl-temporalidad-grafico-8h` | w0082→w0097 | EQUIVALENT | **OBVIOUSLY_EQUIVALENT** — «configurada» vs «indicada»; mismo valor 8 horas | SÍ (merge) |
| 11 | `cl-euro-puede-llegar-arriba` | w0097→w0098 | DIVERGENT | **OBVIOUSLY_DIVERGENT** — condition: B añade la condición explícita «si el euro no tiene que crear el rango» ausente en A | no (ventana entrante rechazada) |
| 12 | `cl-ir-al-grafico` | w0012→w0109 | DIVERGENT | **AMBIGUOUS** — qualifier: A añade «ahora un momento» (temporal), B añade propósito «para verlo claro» (información nueva); misma acción declarada | no (ventana entrante rechazada) |
| 13 | `cl-temporalidad-grafico-15m` | w0042→w0115 | EQUIVALENT | **OBVIOUSLY_EQUIVALENT** — 15 minutos = 15M; «gráfico» vs «gráfica» | SÍ (merge) |
| 14 | `cl-grafico-eurusd` | w0031→w0070 | EQUIVALENT | **OBVIOUSLY_EQUIVALENT** — «es de» vs «corresponde a»; misma proposición | no* |
| 15 | `cl-temporalidad-15m` | w0024→w0122 | EQUIVALENT | **OBVIOUSLY_EQUIVALENT** — «indicada» añadido; mismo valor 15 minutos | no (ventana entrante rechazada) |
| 16 | `cl-vela-apertura` | w0120→w0122 | DIVERGENT | **OBVIOUSLY_DIVERGENT** — estructura del predicado: A es taxonómica («la apertura es una de las partes de la vela»), B es un evento («la vela abre»); part-whole vs evento | no (ventana entrante rechazada) |
| 17 | `cl-grafica-eurusd` | w0002→w0130 | EQUIVALENT | **OBVIOUSLY_EQUIVALENT** — misma proposición («pantalla muestra gráfica del par EUR/USD» vs «gráfica corresponde al par EURUSD») | SÍ (merge) |

\* no* = el merge quedó registrado pero la fila durable de stage guarda sólo la primera acumulación por record (append-only); la aplicación real se verificó contra la unión de provenance del record canónico (ver §3).

### Statements comparados en cada adjudicación

**1. `cl-instrumento-eurusd` (w0017→w0024, EQUIVALENT, humano OBVIOUSLY_EQUIVALENT)**
- existente: «El instrumento mostrado es EURUSD.»
- entrante: «El instrumento del gráfico es EURUSD.»

**2. `cl-observar-formacion-rangos` (w0027→w0028, DIVERGENT, humano AMBIGUOUS)**
- existente: «Hay que ir viendo cómo se forman los rangos.»
- entrante: «Observar cómo se forman los rangos.»

**3. `cl-instrumento-eurusd` (w0017→w0042, EQUIVALENT, humano OBVIOUSLY_EQUIVALENT)**
- existente: «El instrumento mostrado es EURUSD.»
- entrante: «El gráfico abierto es de EURUSD.»

**4. `cl-grafico-eurusd` (w0031→w0057, EQUIVALENT, humano OBVIOUSLY_EQUIVALENT)**
- existente: «El gráfico mostrado es de EUR/USD.»
- entrante: «El gráfico mostrado es de EURUSD.»

**5. `cl-stop-loss-long-debajo-turtle-soup` (w0068→w0069, EQUIVALENT, humano OBVIOUSLY_EQUIVALENT)**
- existente: «Si aquí estás buscando ya para tomar longs, tu stop loss tendría que estar seguro debajo del Turtle Soup.»
- entrante: «Si en este punto se busca tomar un long, el stop loss tiene que quedar seguro por debajo del Turtle Soup.»

**6. `cl-cierre-fuera-invalida-rango` (w0077→w0078, DIVERGENT, humano AMBIGUOUS)**
- existente: «Si la vela cierra fuera del rango, el rango deja de ser un rango.»
- entrante: «Si el precio cierra afuera del rango, el rango deja de ser válido.»

**7. `cl-grafico-eurusd` (w0031→w0082, EQUIVALENT, humano OBVIOUSLY_EQUIVALENT)**
- existente: «El gráfico mostrado es de EUR/USD.»
- entrante: «El gráfico abierto muestra el par EURUSD.»

**8. `cl-smt-no-requerida-entre-dos-velas` (w0093→w0094, DIVERGENT, humano OBVIOUSLY_EQUIVALENT)**
- existente: «La SMT no tiene que aparecer entre estas dos velas.»
- entrante: «Una SMT no tiene que ser entre estas dos velas.»

**9. `cl-instrumento-grafico-eurusd` (w0004→w0097, EQUIVALENT, humano OBVIOUSLY_EQUIVALENT)**
- existente: «El instrumento mostrado en el gráfico es EURUSD.»
- entrante: «El instrumento del gráfico mostrado es EURUSD.»

**10. `cl-temporalidad-grafico-8h` (w0082→w0097, EQUIVALENT, humano OBVIOUSLY_EQUIVALENT)**
- existente: «La temporalidad configurada del gráfico es de 8 horas.»
- entrante: «La temporalidad indicada para el gráfico mostrado es de 8 horas.»

**11. `cl-euro-puede-llegar-arriba` (w0097→w0098, DIVERGENT, humano OBVIOUSLY_DIVERGENT)**
- existente: «Euro puede llegar hasta arriba.»
- entrante: «Si el euro no tiene que crear el rango, puede llegar hasta arriba.»

**12. `cl-ir-al-grafico` (w0012→w0109, DIVERGENT, humano AMBIGUOUS)**
- existente: «Vamos a ir ahora un momento al gráfico.»
- entrante: «Vamos a ir al gráfico para verlo claro.»

**13. `cl-temporalidad-grafico-15m` (w0042→w0115, EQUIVALENT, humano OBVIOUSLY_EQUIVALENT)**
- existente: «La temporalidad del gráfico es de 15 minutos.»
- entrante: «La temporalidad de la gráfica es 15M.»

**14. `cl-grafico-eurusd` (w0031→w0070, EQUIVALENT, humano OBVIOUSLY_EQUIVALENT)**
- existente: «El gráfico mostrado es de EUR/USD.»
- entrante: «El gráfico mostrado corresponde a EURUSD.»

**15. `cl-temporalidad-15m` (w0024→w0122, EQUIVALENT, humano OBVIOUSLY_EQUIVALENT)**
- existente: «La temporalidad del gráfico es de 15 minutos.»
- entrante: «La temporalidad indicada del gráfico es de 15 minutos.»

**16. `cl-vela-apertura` (w0120→w0122, DIVERGENT, humano OBVIOUSLY_DIVERGENT)**
- existente: «Una de las partes de la vela es la apertura.»
- entrante: «La vela abre.»

**17. `cl-grafica-eurusd` (w0002→w0130, EQUIVALENT, humano OBVIOUSLY_EQUIVALENT)**
- existente: «La pantalla muestra una gráfica del par EUR/USD.»
- entrante: «La gráfica mostrada corresponde al par EURUSD.»

## 2. Divergencias deterministas (sin llamada al reviewer) — 16 de las 22

| Window | Record | Diferencia |
|---|---|---|
| w0034 | record cl-grafico-eurusd@1 identity collision: kind differs (observation vs parameter) (window w0031, then window w0034) |
| w0045 | record cl-nueva-vela-abre-aqui@1 identity collision: kind differs (observation vs claim) (window w0044, then window w0045) |
| w0049 | record cl-rango-diario@1 identity collision: kind differs (claim vs observation) (window w0017, then window w0049) |
| w0058 | record cl-rango-pendiente@1 identity collision: epistemic differs (VIDEO_OBSERVED vs INSTRUCTOR_SAID) (window w0051, then window w0058) |
| w0059 | record cl-rango-pendiente@1 identity collision: epistemic differs (VIDEO_OBSERVED vs INSTRUCTOR_SAID) (window w0051, then window w0059) |
| w0062 | record cl-instrumento-eurusd@1 identity collision: kind differs (parameter vs observation) (window w0017, then window w0062) |
| w0065 | record cl-grafico-eurusd@1 identity collision: kind differs (observation vs parameter) (window w0031, then window w0065) |
| w0072 | record cl-grafico-temporalidad-15m@1 identity collision: kind differs (observation vs parameter) (window w0070, then window w0072) |
| w0074 | record cl-instrumento-eurusd@1 identity collision: kind differs (parameter vs observation) (window w0017, then window w0074) |
| w0088 | record cl-ejemplos-capitulo-aparte@1 identity collision: kind differs (claim vs procedure_step) (window w0086, then window w0088) |
| w0102 | record cl-activo-eurusd@1 identity collision: kind differs (observation vs parameter) (window w0055, then window w0102) |
| w0116 | record cl-instrumento-eurusd@1 identity collision: kind differs (parameter vs observation) (window w0017, then window w0116) |
| w0117 | record cl-instrumento-eurusd@1 identity collision: kind differs (parameter vs observation) (window w0017, then window w0117) |
| w0118 | record cl-smt-aplicada-estrategia@1 identity collision: kind differs (procedure_step vs claim) (window w0086, then window w0118) |

Las 6 divergencias semánticas restantes son las filas con veredicto DIVERGENT de §1 (windows w0028, w0078, w0094, w0098, w0109, w0122). Las 2 divergencias estructurales de relations (w0054, w0092) están en la tabla anterior.

## 3. Aplicación de acumulaciones (EQUIVALENT → APPLY) — auditada físicamente

12 merges aplicados live sobre 7 records canónicos. Por cada record se verificó físicamente (LIVE_ACCUMULATION_AUDIT = **PASS**):

- canonical statement = first-observed rendering (el statement canónico es el de la primera ventana, nunca el del merge);
- EvidenceIDs = sorted unique union de todas las ventanas proponentes;
- Provenance.InvocationIDs = sorted unique union;
- todos los invocation IDs resuelven en el journal;
- las dependency edges cubren todos los evidence refs.

| Record | Ventanas que observaron la proposición | Merges aplicados | Evidencia canónica |
|---|---|---|---|
| `cl-grafica-eurusd@1` | w0002 → w0130 | 1 | 2 refs |
| `cl-grafico-eurusd@1` | w0031 → w0057 → w0070 → w0082 → w0086 → w0119 | 5 | 10 refs |
| `cl-instrumento-eurusd@1` | w0017 → w0024 → w0042 | 2 | 5 refs |
| `cl-instrumento-grafico-eurusd@1` | w0004 → w0097 | 1 | 2 refs |
| `cl-stop-loss-long-debajo-turtle-soup@1` | w0068 → w0069 | 1 | 3 refs |
| `cl-temporalidad-grafico-15m@1` | w0042 → w0115 | 1 | 3 refs |
| `cl-temporalidad-grafico-8h@1` | w0082 → w0097 | 1 | 3 refs |

### FALSE MERGE WATCH

**POTENTIAL_FALSE_SEMANTIC_MERGE = NO.** Los 11 veredictos EQUIVALENT del reviewer son todos OBVIOUSLY_EQUIVALENT para el operador; ningún OBVIOUSLY_DIVERGENT recibió merge. En dirección inversa (sobre-rechazo conservador, costo de cobertura y no de integridad): la adjudicación #8 (`cl-smt-no-requerida-entre-dos-velas`, humano OBVIOUSLY_EQUIVALENT, veredicto DIVERGENT) rechazó w0094 completa; las 3 AMBIGUOUS (#2, #6, #12) también resolvieron DIVERGENT fail-closed, consistente con la instrucción congelada «when in doubt, answer DIVERGENT».

### Contadores y su reconciliación

- 21 adjudicaciones = 17 llamadas live + 4 re-verdictos: las re-colisiones con el mismo par de statements reusan el veredicto journalado content-addressed sin nueva llamada (w0086, w0119 aplicados; w0118 y w0122 en ventanas luego rechazadas).
- 15 semantic-equivalent merges decididos; 12 aplicados (los 3 restantes pertenecían a ventanas rechazadas por otra colisión: atomicidad whole-window).
- 1 deterministic-equivalent accumulation (w0011, `cl-estrategia-se-basa-principalmente-en-rangos`: statement idéntico tras normalización conservativa).
- El stage row `EVIDENCE_ACCUMULATED` es append-only por (record,version,stage,state): guarda el PRIMER merge de cada record; la aplicación real se verificó contra las uniones canónicas (no contra ese detalle).
