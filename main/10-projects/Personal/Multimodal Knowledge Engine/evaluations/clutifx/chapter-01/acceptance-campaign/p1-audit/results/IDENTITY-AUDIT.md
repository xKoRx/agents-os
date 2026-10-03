# IDENTITY-AUDIT — Ladder de identidad, capítulo 01 Clutifx (run full-live-v2)

Auditoría fuente-grounded de las **38 identity collisions**, las **17 adjudicaciones live** (`claims.equivalence_review`) y las **12 acumulaciones sobre 7 records** del run `full-live-v2` (1039 claims + 168 relations propuestos, 1 duplicado exacto, 22 ventanas rechazadas por ladder).

Fuentes auditadas: `fixtures/identity-equivalence-live.jsonl`, `fixtures/rejected-window-recon-invocations.jsonl`, `fixtures/rejected-overlap.json`, store canónico `full-live-v2/claims.jsonl`, `run.db` (`record_stages`, `pipeline_records`, `provider_invocations`), `documentation.md` (líneas ladder), `EQUIVALENCE-DECISIONS.md`, `accumulation-audit.json`, `transcript.json`, y corpus de ventanas (`corpus/wNNNN.json`).

Veredicto agregado en una línea: **0 falso merges aplicados, 2 falso splits claros (w0094, w0028), 15/16 divergencias deterministas son inestabilidad de clasificación (no semántica), 7/7 acumulaciones PASS, y la consecuencia de cobertura agregada de los 22 rechazos es baja (~85–90 % del contenido re-propuesto y aceptado por ventanas vecinas bajo ids nuevos).**

---

## 1. Las 38 colisiones

Composición verificada contra `documentation.md` y `run.db`: **16 deterministas divergentes** (12 kind + 2 epistemic + 2 structural) + **6 semánticas DIVERGENT** + **1 deterministic-equivalent** + **15 semantic-equivalent merges** (11 veredictos EQUIVALENT live + 4 re-veredictos content-addressed).

### 1a. Tabla de las 22 colisiones que rechazaron ventana

| # | Window | Record | Mecanismo / divergencia | Store (statement, kind, epi) | Entrante (statement, kind, epi) | Clasificación | Consecuencia de cobertura |
|---|---|---|---|---|---|---|---|
| 1 | w0034 | `cl-grafico-eurusd` | deterministic / kind (observation vs parameter) | «El gráfico mostrado es de EUR/USD», observation | «El activo del gráfico mostrado es EURUSD», parameter | **MODEL_CLASSIFICATION_INSTABILITY** | Baja: re-cubierto por w0033/w0035/w0036 |
| 2 | w0045 | `cl-nueva-vela-abre-aqui` | deterministic / kind (observation vs claim) | «La nueva vela abre por aquí», observation, INSTRUCTOR_SAID | «La nueva vela que abre va a abrir por aquí», claim | **MODEL_CLASSIFICATION_INSTABILITY** | Baja: re-cubierto por w0046/w0047 |
| 3 | w0049 | `cl-rango-diario` | deterministic / kind (claim vs observation) | «Se identifica un rango diario en la vista diaria», claim | «En la figura se representa un rango diario», observation | **MODEL_CLASSIFICATION_INSTABILITY** | Baja: re-cubierto por w0050/w0051/w0052 |
| 4 | w0054 | `rel-rango-bajista-depende-apertura-arriba` | deterministic / structural (subject endpoint) | subject `cl-rango-reiniciado-rango-bajista-posible` («El rango reiniciado crea un posible rango bajista») | subject `cl-rango-reiniciado-crea-rango-bajista-posible` («La apertura por arriba del rango reiniciado crea un posible rango bajista») | **MODEL_CLASSIFICATION_INSTABILITY** (re-render del slug; mismo type, objeto y evidencia asr-00110) | Baja: el par claim+claim equivalente ya existía vía w0053/w0055 |
| 5 | w0058 | `cl-rango-pendiente` | deterministic / epistemic (VIDEO_OBSERVED vs INSTRUCTOR_SAID) | «El rango está pendiente», VIDEO_OBSERVED | «Este es un rango pendiente», INSTRUCTOR_SAID | **MODEL_CLASSIFICATION_INSTABILITY** (deíctico dual-fuente, asr-00115) | Parcial: narración en tiempo real y anticipación pre-cierre no están en store |
| 6 | w0059 | `cl-rango-pendiente` | deterministic / epistemic | «El rango está pendiente», VIDEO_OBSERVED | «El rango creado está pendiente», INSTRUCTOR_SAID | **MODEL_CLASSIFICATION_INSTABILITY** | Parcial: parámetros 1,14569/1,15231 perdidos (store guarda 1.14565/1.15325 de w0061) |
| 7 | w0062 | `cl-instrumento-eurusd` | deterministic / kind (parameter vs observation) | «El instrumento mostrado es EURUSD», parameter | «El instrumento mostrado es EURUSD», observation — **byte-idéntico** | **MODEL_CLASSIFICATION_INSTABILITY** (caso más limpio) | Parcial: comentarios sobre nombres de rangos (asr-00120) sin record |
| 8 | w0065 | `cl-grafico-eurusd` | deterministic / kind | «El gráfico mostrado es de EUR/USD», observation | «El gráfico visible corresponde a EURUSD», parameter | **MODEL_CLASSIFICATION_INSTABILITY** | Baja: re-cubierto por w0066/w0067 |
| 9 | w0072 | `cl-grafico-temporalidad-15m` | deterministic / kind | «El gráfico mostrado utiliza una temporalidad de 15 minutos», observation | «La temporalidad del gráfico mostrado es de 15 minutos», parameter | **MODEL_CLASSIFICATION_INSTABILITY** | Baja: re-cubierto por w0073 |
| 10 | w0074 | `cl-instrumento-eurusd` | deterministic / kind | «El instrumento mostrado es EURUSD», parameter | ídem byte-idéntico, observation | **MODEL_CLASSIFICATION_INSTABILITY** | Parcial: regla de re-entrada tras rangos en contra sin record |
| 11 | w0088 | `cl-ejemplos-capitulo-aparte` | deterministic / kind (claim vs procedure_step) | «Los ejemplos se explicarán en un capítulo aparte», claim | «El ponente abordará los ejemplos en un capítulo aparte», procedure_step (asignación errónea: es un anuncio) | **MODEL_CLASSIFICATION_INSTABILITY** | Baja: re-cubierto por w0089/w0090 |
| 12 | w0092 | `rel-smt-requiere-reversal-directo` | deterministic / structural (subject endpoint) | subject `cl-formacion-correlada-es-smt` («La formación mostrada se considera un tipo de SMT») | subject `cl-configuracion-senalada-es-smt` («La configuración señalada se identifica como un SMT») | **MODEL_CLASSIFICATION_INSTABILITY** (paráfrasis del mismo hecho, asr-00193/194) | Parcial: regla de vigilancia «atento a los dos pares» sin record |
| 13 | w0102 | `cl-activo-eurusd` | deterministic / kind | «El gráfico corresponde al par EURUSD», observation | «El ejemplo se realiza sobre EURUSD», parameter | **MODEL_CLASSIFICATION_INSTABILITY** | Baja: re-cubierto por w0101/w0103/w0104 |
| 14 | w0116 | `cl-instrumento-eurusd` | deterministic / kind | ídem byte-idéntico, parameter | ídem, observation | **MODEL_CLASSIFICATION_INSTABILITY** | Parcial: lecturas de la operación corta (1,15078/1,14741) sin record |
| 15 | w0117 | `cl-instrumento-eurusd` | deterministic / kind | ídem byte-idéntico, parameter | ídem, observation | **MODEL_CLASSIFICATION_INSTABILITY** | Parcial: lecturas intermedias de la herramienta long |
| 16 | w0118 | `cl-smt-aplicada-estrategia` | deterministic / kind (procedure_step vs claim) | «La SMT se explica aplicada a la estrategia», procedure_step (asr-00190) | «La SMT aplicada a la estrategia está entre los conceptos básicos», claim (asr-00260) | **TRUE_DIVERGENCE** (contenido distinto: marco de explicación vs pertenencia a conceptos básicos; el reuso del slug causó la colisión) | Baja-moderada: la lista de conceptos básicos quedó cubierta tardíamente por w0129 (`cl-temas-tratados`) |
| 17 | w0028 | `cl-observar-formacion-rangos` | semantic / DIVERGENT | «Hay que ir viendo cómo se forman los rangos», procedure_step | «Observar cómo se forman los rangos», procedure_step | **FALSE_DIVERGENT** (misma acción y objeto; sólo modalidad obligación vs imperativo; falso split conservador) | Baja: re-cubierto por w0029/w0030/w0033 |
| 18 | w0078 | `cl-cierre-fuera-invalida-rango` | semantic / DIVERGENT | «Si la vela cierra fuera del rango, el rango deja de ser un rango», rule | «Si el precio cierra afuera del rango, el rango deja de ser válido», rule | **AMBIGUOUS** (dos qualifiers menores: vela/precio elidido en ASR; identidad vs validez; fail-closed contract-consistente) | ~Nula: variantes en w0075 (`cl-cierre-fuera-rango-invalida`), w0076 (`cl-cierre-fuera-deja-de-ser-rango`), pasos de espera en w0079 |
| 19 | w0094 | `cl-smt-no-requerida-entre-dos-velas` | semantic / DIVERGENT | «La SMT no tiene que aparecer entre estas dos velas», rule | «Una SMT no tiene que ser entre estas dos velas», rule | **FALSE_DIVERGENT** (única diferencia: definitez «La» vs «Una»; el falso split más claro del run) | Baja: la proposición sobrevive vía w0093; resto en w0093/w0095 |
| 20 | w0098 | `cl-euro-puede-llegar-arriba` | semantic / DIVERGENT | «Euro puede llegar hasta arriba», claim | «Si el euro no tiene que crear el rango, puede llegar hasta arriba», claim | **CORRECT_DIVERGENT** (el entrante añade condición material; asr-00206 lo confirma) | ~Nula: condicional cubierto por `cl-rango-libra-indica-no-necesidad-euro` y `cl-escenario-euro-sin-rango-para-target`; failure swing por w0099/w0100 |
| 21 | w0109 | `cl-ir-al-grafico` | semantic / DIVERGENT | «Vamos a ir ahora un momento al gráfico» (w0012, asr-00023/24) | «Vamos a ir al gráfico para verlo claro» (asr-00243/244) | **AMBIGUOUS** (núcleo idéntico, qualifiers distintos; colisión causada por reuso del slug entre dos eventos de habla a 165 s y 1683 s) | Menor: statement recuperado por w0108 (`cl-ir-al-grafico-para-ver-claro`); se pierde el anuncio «esperar en M15 para subir / capítulo entradas» |
| 22 | w0122 | `cl-vela-apertura` | semantic / DIVERGENT | «Una de las partes de la vela es la apertura» (asr-00264, taxonómica) | «La vela abre» (asr-00270, evento) | **CORRECT_DIVERGENT** (part-whole vs evento; segmentos distintos) | ~Nula: re-cubierto por w0123/w0124/w0130 |

### 1b. Deterministic-equivalent (1)

| Record | Ventanas | Resultado |
|---|---|---|
| `cl-estrategia-se-basa-principalmente-en-rangos` | w0010 → w0011 | w0011 re-propuso byte-idéntico «La estrategia se basa principalmente en los rangos» con la misma evidencia `[asr-00020]` (segmento 145.0–152.6 s que cruza el corte de 149 s). Resuelto sin reviewer: stage `DUPLICATE_SUPPRESSED` (w0011). Dedup idempotente correcto; store final con 1 evidencia y 1 invocation (verificado en `run.db`). |

### 1c. Los 15 semantic-equivalent merges (11 live EQUIVALENT + 4 re-veredictos)

| # | Par | Record | Applied | Clasificación |
|---|---|---|---|---|
| 1 | w0017→w0024 (live #1) | `cl-instrumento-eurusd` | SÍ | CORRECT_EQUIVALENT |
| 2 | w0017→w0042 (live #3) | `cl-instrumento-eurusd` | SÍ | CORRECT_EQUIVALENT |
| 3 | w0031→w0057 (live #4) | `cl-grafico-eurusd` | SÍ | CORRECT_EQUIVALENT (EUR/USD vs EURUSD: notación) |
| 4 | w0068→w0069 (live #5) | `cl-stop-loss-long-debajo-turtle-soup` | SÍ | CORRECT_EQUIVALENT |
| 5 | w0031→w0082 (live #7) | `cl-grafico-eurusd` | SÍ | CORRECT_EQUIVALENT (paráfrasis; clave content-addressed reusada ×4) |
| 6 | w0004→w0097 (live #9) | `cl-instrumento-grafico-eurusd` | SÍ | CORRECT_EQUIVALENT (orden de palabras) |
| 7 | w0082→w0097 (live #10) | `cl-temporalidad-grafico-8h` | SÍ | CORRECT_EQUIVALENT («configurada» vs «indicada»: marginal pero defendible) |
| 8 | w0042→w0115 (live #13) | `cl-temporalidad-grafico-15m` | SÍ | CORRECT_EQUIVALENT (15M = 15 minutos) |
| 9 | w0031→w0070 (live #14) | `cl-grafico-eurusd` | SÍ | CORRECT_EQUIVALENT |
| 10 | w0002→w0130 (live #17) | `cl-grafica-eurusd` | SÍ | CORRECT_EQUIVALENT |
| 11 | re-veredicto w0086 | `cl-grafico-eurusd` | SÍ | CORRECT_EQUIVALENT («El gráfico mostrado corresponde a EURUSD», mismo par que #9) |
| 12 | re-veredicto w0119 | `cl-grafico-eurusd` | SÍ | CORRECT_EQUIVALENT (ídem) |
| 13 | w0024→w0122 (live #15) | `cl-temporalidad-15m` | NO (ventana rechazada por colisión de `cl-vela-apertura`) | CORRECT_EQUIVALENT |
| 14 | re-veredicto w0118 | `cl-grafico-eurusd` | NO (ventana rechazada por colisión de `cl-smt-aplicada-estrategia`) | CORRECT_EQUIVALENT |
| 15 | re-veredicto w0122 | `cl-grafico-eurusd` | NO (ventana rechazada por colisión de `cl-vela-apertura`) | CORRECT_EQUIVALENT |

Reconciliación: 15 decididos, 12 aplicados, 3 anulados por rechazo whole-window — coincide con EQUIVALENCE-DECISIONS.md. La tabla de stages `EVIDENCE_ACCUMULATED` (append-only) guarda sólo el primer merge por record; la aplicación real se verificó contra las uniones canónicas de `pipeline_records` (§3).

---

## 2. Las 17 adjudicaciones live

Todas las invocaciones están `VALIDATED`, contrato `mke.claims-equivalence-prompt.v1`, con instruction congelada «when in doubt, answer DIVERGENT» y clases materiales: negación, números, condiciones, qualifiers, dirección, modalidad, scope.

| # | Record | Ventanas | Veredicto | Clasificación auditor | Justificación con fuente |
|---|---|---|---|---|---|
| 1 | `cl-instrumento-eurusd` | w0017→w0024 | EQUIVALENT | **CORRECT_EQUIVALENT** | Misma proposición (qué instrumento muestra el gráfico); «mostrado» vs «del gráfico» no es material. Merge aplicado y verificado. |
| 2 | `cl-observar-formacion-rangos` | w0027→w0028 | DIVERGENT | **FALSE_DIVERGENT** | asr-00052 «ir viendo cómo se van formando rangos»: misma acción y objeto; sólo modalidad (obligación progresiva vs imperativo). Falso split conservador. |
| 3 | `cl-instrumento-eurusd` | w0017→w0042 | EQUIVALENT | **CORRECT_EQUIVALENT** | «El gráfico abierto es de EURUSD» = «El instrumento mostrado es EURUSD». Merge aplicado. |
| 4 | `cl-grafico-eurusd` | w0031→w0057 | EQUIVALENT | **CORRECT_EQUIVALENT** | EUR/USD vs EURUSD: notación únicamente. Merge aplicado. |
| 5 | `cl-stop-loss-long-debajo-turtle-soup` | w0068→w0069 | EQUIVALENT | **CORRECT_EQUIVALENT** | Misma regla condicional (asr-00136); 2ª persona vs impersonal y «tendría» vs «tiene» no cambian la proposición. Merge aplicado. |
| 6 | `cl-cierre-fuera-invalida-rango` | w0077→w0078 | DIVERGENT | **AMBIGUOUS** | «vela…deja de ser un rango» vs «precio…deja de ser válido»: dos qualifiers menores sobre la misma regla (asr-00168 elide el sujeto). Fail-closed contract-consistente; materialmente defendible como EQUIVALENT. |
| 7 | `cl-grafico-eurusd` | w0031→w0082 | EQUIVALENT | **CORRECT_EQUIVALENT** | Paráfrasis («muestra el par EURUSD»). Merge aplicado. |
| 8 | `cl-smt-no-requerida-entre-dos-velas` | w0093→w0094 | DIVERGENT | **FALSE_DIVERGENT** | asr-00197 «No es que tenga que ser una SMT entre estas dos velas»: única diferencia «La» vs «Una» (definitez); alcance de la negación idéntico. Sobre-rechazo de una equivalencia obvia. |
| 9 | `cl-instrumento-grafico-eurusd` | w0004→w0097 | EQUIVALENT | **CORRECT_EQUIVALENT** | Sólo orden de palabras. Merge aplicado. |
| 10 | `cl-temporalidad-grafico-8h` | w0082→w0097 | EQUIVALENT | **CORRECT_EQUIVALENT** | Mismo valor 8 h; «configurada» vs «indicada» es matiz aceptable en lectura de UI. Merge aplicado. |
| 11 | `cl-euro-puede-llegar-arriba` | w0097→w0098 | DIVERGENT | **CORRECT_DIVERGENT** | El entrante añade la condición «si el euro no tiene que crear el rango» (asr-00206 la confirma). Condición = diferencia material. |
| 12 | `cl-ir-al-grafico` | w0012→w0109 | DIVERGENT | **AMBIGUOUS** | Núcleo idéntico con qualifiers distintos («ahora un momento» vs «para verlo claro»); dos eventos de habla unidos por reuso del slug. Fail-closed contract-consistente. |
| 13 | `cl-temporalidad-grafico-15m` | w0042→w0115 | EQUIVALENT | **CORRECT_EQUIVALENT** | 15M = 15 minutos; «gráfica» vs «gráfico». Merge aplicado. |
| 14 | `cl-grafico-eurusd` | w0031→w0070 | EQUIVALENT | **CORRECT_EQUIVALENT** | «es de» vs «corresponde a»: misma proposición. Merge aplicado. |
| 15 | `cl-temporalidad-15m` | w0024→w0122 | EQUIVALENT | **CORRECT_EQUIVALENT** | «indicada» añadido; mismo valor. Decidido pero no aplicado (ventana rechazada por otra colisión). |
| 16 | `cl-vela-apertura` | w0120→w0122 | DIVERGENT | **CORRECT_DIVERGENT** | Taxonómica (part-whole, asr-00264) vs evento (asr-00270): estructuras de predicado genuinamente distintas. |
| 17 | `cl-grafica-eurusd` | w0002→w0130 | EQUIVALENT | **CORRECT_EQUIVALENT** | Misma proposición. Merge aplicado (evidencia p1080000 + p182520000 = 2028 s en timebase 90 kHz, consistente con w0130 33:48–34:02). |

**Saldo de correctitud: 11 CORRECT_EQUIVALENT, 2 CORRECT_DIVERGENT, 2 FALSE_DIVERGENT, 2 AMBIGUOUS, 0 FALSE_EQUIVALENT.**
**Falso merges aplicados: 0.** Ningún veredicto EQUIVALENT unió proposiciones materialmente distintas; ninguno de los OBVIOUSLY_DIVERGENT recibió merge. Los 2 falsos splits (adjudicaciones #2 y #8) son sobre-rechazos conservadores en la dirección segura (costo de cobertura, no de integridad), consistentes con la instrucción congelada «when in doubt, DIVERGENT».

Resultado post-merge en el store (verificación física de los 12 merges aplicados): los 7 records canónicos conservan el statement first-observed, las uniones de evidencia son sorted-unique y las unions de provenance resuelven exactamente a las ventanas proponentes (ver §3). No se detectó reescritura de statements ni contaminación de significado.

---

## 3. Las 12 acumulaciones sobre 7 records

Verificación independiente (no sólo el PASS declarado en `accumulation-audit.json`): para cada record se comparó el payload canónico de `pipeline_records` con las proposals de las ventanas proponentes (corpus + run.db), se comprobó orden/unidad de las uniones y que cada `provenance.invocation_ids` resuelve en `provider_invocations` al target de la ventana esperada.

| Record | Ventanas | Merges | Evidencias | Checks | Clasificación |
|---|---|---|---|---|---|
| `cl-grafica-eurusd@1` | w0002→w0130 | 1 | 2 | statement = first-observed; unión sorted-unique; 2 invocations = {w0002, w0130}; mismo significado | **CORRECT_ACCUMULATION** |
| `cl-grafico-eurusd@1` | w0031→w0057→w0070→w0082→w0086→w0119 | 5 | 10 | ídem; 6 invocations resuelven exactamente a las 6 ventanas; los 5 merges son paráfrasis de la misma proposición | **CORRECT_ACCUMULATION** |
| `cl-instrumento-eurusd@1` | w0017→w0024→w0042 | 2 | 5 | ídem; 3 invocations = {w0017, w0024, w0042} | **CORRECT_ACCUMULATION** |
| `cl-instrumento-grafico-eurusd@1` | w0004→w0097 | 1 | 2 | ídem | **CORRECT_ACCUMULATION** |
| `cl-stop-loss-long-debajo-turtle-soup@1` | w0068→w0069 | 1 | 3 | ídem; la paráfrasis de w0069 no reescribió el statement canónico | **CORRECT_ACCUMULATION** |
| `cl-temporalidad-grafico-15m@1` | w0042→w0115 | 1 | 3 | ídem | **CORRECT_ACCUMULATION** |
| `cl-temporalidad-grafico-8h@1` | w0082→w0097 | 1 | 3 | ídem | **CORRECT_ACCUMULATION** |

**7/7 CORRECT_ACCUMULATION; 0 PROBLEMATIC.** Adicionalmente, el caso deterministic-equivalent de w0011 (`cl-estrategia-se-basa-principalmente-en-rangos`) resolvió por `DUPLICATE_SUPPRESSED` con unión trivial — también correcto. La unión nunca cambió el significado: todos los merges unieron paráfrasis de la misma proposición y el statement canónico quedó siempre en el rendering first-observed.

---

## 4. Caracterización de los patrones de divergencia determinista (mandato del owner)

1. **parameter vs observation (el patrón dominante: 8 de 12 kind-collisions).** Sobre hechos de metadato del gráfico — «el instrumento/gráfico es EURUSD», «la temporalidad es 15m/8h/1D» — el recon alterna entre `parameter` (metadato de la plataforma) y `observation` (hecho visible). Casos extremos: el statement entrante fue **byte-idéntico** al canónico en w0062, w0074, w0116 y w0117 (`cl-instrumento-eurusd`, «El instrumento mostrado es EURUSD», 4 veces con kind=observation contra el canónico parameter). Es pura inestabilidad taxonómica del modelo, no semántica.
2. **claim vs observation (2 casos).** Deícticos narrados por el instructor sobre lo que se ve («la nueva vela abre por aquí», «un rango diario»): el modelo no decide de forma estable si el hecho es enunciado (claim) o percepción (observation). w0045 y w0049.
3. **procedure_step vs claim (2 casos).** w0088: un anuncio sobre contenido futuro («los ejemplos irán en un capítulo aparte») clasificado procedure_step — asignación entrante errónea, la del store (claim) era correcta. w0118: aquí además el contenido era genuinamente distinto (marco de explicación vs pertenencia a conceptos básicos) → única TRUE_DIVERGENCE determinista; el disparador fue el reuso del slug.
4. **VIDEO_OBSERVED vs INSTRUCTOR_SAID (2 casos).** Deícticos dual-fuente: el instructor enuncia mientras señala la pantalla («este es un rango pendiente», asr-00115). Ambas clases epistémicas son defendibles para el mismo segmento y el modelo las alterna (w0051 vs w0058/w0059). La regla determinista trata el flip como divergencia; semánticamente es la misma proposición con atribución ambigua.
5. **Relation endpoint divergence (2 casos).** El modelo re-renderiza la misma regla causal bajo un slug nuevo (`cl-rango-reiniciado-rango-bajista-posible` vs `cl-rango-reiniciado-crea-rango-bajista-posible`; `cl-formacion-correlada-es-smt` vs `cl-configuracion-senalada-es-smt`) y la relation — con type, objeto y evidencia idénticos — colisiona por el endpoint. La divergencia vive en la asignación de ids, no en la relación.

**Síntesis del patrón:** 15 de las 16 divergencias deterministas son `MODEL_CLASSIFICATION_INSTABILITY` (11 kind/epistemic + 2 structural + w0088) y 1 es TRUE_DIVERGENCE de contenido (w0118). El ladder ejecutó correctamente su regla en los 16 casos; la inestabilidad está aguas arriba, en la recon (kind/epistemic/slug), y el efecto neto es convertir ruido de clasificación en rechazo de ventanas completas.

---

## 5. Conteos de false merges / false splits

- **FALSE_EQUIVALENT (falso merge): 0 de 21 adjudicaciones; 0 de 12 merges aplicados.** Ninguna unión combinó proposiciones materialmente distintas.
- **FALSE_DIVERGENT (falso split): 2 claros** (w0094 `cl-smt-no-requerida-entre-dos-velas` — definitez «La»/«Una»; w0028 `cl-observar-formacion-rangos` — modalidad obligación/imperativo) **+ 2 AMBIGUOUS resueltos DIVERGENT** (w0078, w0109). Todos fail-closed según contrato.
- **Inestabilidad de clasificación vs divergencia real:** de las 22 colisiones con rechazo, 15 son MODEL_CLASSIFICATION_INSTABILITY, 6 son divergencias semánticas reales o plausibles (de las cuales 2 falsos splits, 2 correctas, 2 ambiguas) y 1 TRUE_DIVERGENCE determinista (w0118).
- **Fragmentación estructural del store (hallazgo transversal):** la identidad sólo se fuerza en colisión de record_id; proposiciones idénticas bajo slugs distintos coexisten. En el store canónico hay **13 pares de records con statement byte-idéntico** (26 records), p. ej. `cl-temporalidad-15m` y `cl-temporalidad-grafico-15m` comparten literalmente «La temporalidad del gráfico es de 15 minutos» (parameter, VIDEO_OBSERVED ambos), y la familia «el gráfico es EURUSD» cuenta con ~12 records distintos (`cl-grafico-eurusd`, `cl-grafica-eurusd`, `cl-chart-eurusd`, `cl-chart-is-eurusd`, `cl-activo-eurusd`, `cl-activo-grafico-eurusd`, `cl-grafica-activo-eurusd`, `cl-grafico-instrumento-eurusd`, `cl-instrumento-mostrado-eurusd`, `cl-grafico-par-eurusd`, `cl-instrumento-eurusd`, `cl-instrumento-grafico-eurusd`). El acierto de la curación semántica en los merges convive con esta duplicación no resuelta.

---

## 6. Consecuencia de cobertura agregada de los 22 rechazos por ladder

Cruzando cada proposal rechazada (`rejected-window-recon-invocations.jsonl`) con el store canónico y las ventanas vecinas aceptadas (`rejected-overlap.json`, corpus):

- **~85–90 % del contenido de las 22 ventanas rechazadas existe en el store**, re-propuesto (casi siempre con renderings casi idénticos) por las ventanas inmediatamente vecinas bajo ids nuevos. Ejemplos verificados ventana a ventana: w0028→w0029/w0030/w0033; w0034→w0033/w0035/w0036; w0045→w0046/w0047; w0049→w0050/w0051/w0052; w0054→w0053/w0055; w0065→w0066/w0067; w0072→w0073; w0078→w0075/w0076/w0079; w0088→w0089/w0090; w0092→w0091/w0093; w0094→w0093/w0095; w0098→w0097/w0099/w0100; w0102→w0101/w0103/w0104; w0109→w0108/w0107; w0116–w0118→w0119/w0120/w0129; w0122→w0123/w0124/w0130.
- **Pérdidas durables identificadas (pequeñas, ninguna estructural):** narración en tiempo real de w0058/w0059 (toma del low y reacción en vivo; anticipación pre-cierre; lectura 8 h); parámetros de rango 1,14569/1,15231 (el store conserva las variantes 1.14565/1.15325 de w0061); comentarios de w0062 sobre los nombres de los rangos; regla de re-entrada de w0074; vigilancia de dos pares de w0092; anuncio «esperar en M15 para subir / capítulo entradas» de w0109; lecturas de la operación corta de w0116 (1,15078/1,14741) y lecturas intermedias de la herramienta long de w0117.
- **Doble filo de la auto-reparación:** que las vecinas recuperen el contenido rechazado se debe a que re-propone bajo ids nuevos, que es exactamente el mecanismo que produce la fragmentación del §5. El ladder rechaza ventanas por ruido de clasificación, el vecino re-importa el mismo contenido con otro slug, y el store gana duplicados en vez de perder conocimiento: el costo real del ruido es duplicación + inestabilidad de identidad, no vacíos de cobertura.
- Los 3 re-veredictos EQUIVALENT anulados por rechazos whole-window (w0118, w0122 + live #15) no dejaron huella en el store, correcto según la política whole-window.

---

## 7. Archivo de datos

`results/identity-audit.jsonl` — 51 líneas: 27 `collision` (16 deterministas + 6 semánticas DIVERGENT + 1 deterministic-equivalent + 4 re-veredictos), 17 `adjudication` (las llamadas live), 7 `accumulation`. Cada línea incluye store vs entrante (en `justification`), clasificación y consecuencia de cobertura.
