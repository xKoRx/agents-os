# GROUNDING-AUDIT — Capítulo 01 Clutifx (acceptance-campaign / p8, aceptación exhaustiva del rerun @ 19b44c1)

**Auditoría fuente-grounded del grounding reviewer sobre el candidato rerun (`run-rerun-20261003`).**
Fecha: 2026-10-04. Ámbito: **64 records non-supported (100 %, sin muestreo)** = 46 claims + 18 relations, más **muestra distribuida de 61 records SUPPORTED** (50 claims, 1 de cada 20 por orden de `claims.jsonl`; 11 relations, 1 de cada 12) para falsos positivos.
Salida detallada: `grounding-audit.jsonl` (64 líneas).

Método: para cada record se compararon (1) la evidencia citada, (2) el veredicto y razones del reviewer, y (3) la fuente real: transcript de la ventana del corpus P8 (`corpus/wNNNN.json`, segmentos citados + adyacentes) y los PNG citados en `~/mke/clutifx-ch01-20260930/media-run/evidence/objects/` para todo claim visual. Para los casos de fallo de formato se consultó además `run.db` → `provider_invocations` (task `claims.grounding_review`, `response_json` de cada intento). Criterios de clasificación: los del baseline P1 (FALSE_NEGATIVE = la fuente sostiene el record y el reviewer lo rechazó, incluye garble-identity, deixis y cláusula causal; EVIDENCE_SELECTION_PROBLEM = la reconstrucción citó mal/truncado y el adyacente lo sostenía; PROVIDER_FAILURE = el reviewer nunca evaluó semánticamente).

> **Nota de población**: el brief hablaba de 5 parse-fatal + 11 malformed = 16 casos especiales. En los datos hay **14 casos provider únicos**: 5 `UNSUPPORTED_REVIEW_UNAVAILABLE` por parse fatal, y **10** records con veredicto malformed (9 `UNSUPPORTED_INSUFFICIENT` + `cl-intraturtlesoup-open-pnl-label`, que está en ambas listas). Los 9+1 se resuelven uno a uno abajo. El resto del brief es correcto: 64 non-supported verificados (46 claims + 18 relations).

## 1. Métricas principales

| Métrica | Rerun P8 | Baseline P1 | Umbral |
|---|---|---|---|
| Non-supported total | **64** (46 claims + 18 rel) | 80 | — |
| **FN claims** | **21 / 46** | 14 / 80 | — |
| **FN relations** | **9 / 18** | (incluidos en los 14) | — |
| **FN total** | **30 / 64** | 14 / 80 | — |
| **candidate_grounding_false_negative_rate** | **46,9 % (30/64)** | 17,5 % (14/80) | **≤ 10 % → NO CUMPLE** |
| FN de causa provider (malformed + parse fatal) | 14 (21,9 % de la población) | 1 | — |
| FN semánticos (error del reviewer sobre lo que vio) | 16 (25,0 %) | 14 (17,5 %) | — |
| Falsos positivos (muestra distribuida) | **0 / 61** (0 claims, 0 relations) | 1/30 claims + 1/112 relations | no subir |

**Veredicto: el candidato NO supera la aceptación de grounding.** El FN rate (46,9 %) triplica el baseline y está muy lejos del umbral ≤ 10 %. La safety rule «no aceptar si suben los falsos positivos» no se activa (0/61), pero el colapso viene de otro sitio: **el backend del reviewer (schema/addressing + parse) dejó sin veredicto válido al 22 % de la población non-supported**, y encima los FN semánticos subieron de 17,5 % a 25 %.

## 2. Distribución de clasificaciones (64 records)

| Clasificación | n | % | Nota |
|---|---|---|---|
| FALSE_NEGATIVE | 30 | 46,9 % | 21 claims + 9 relations |
| EVIDENCE_SELECTION_PROBLEM | 15 | 23,4 % | 11 claims + 4 relations; conocimiento correcto, citación fallida |
| ACTUALLY_CONTRADICTED | 8 | 12,5 % | 8 claims; las 8 contradicciones verificadas son reales |
| CORRECT_REJECTION | 7 | 10,9 % | 2 claims + 5 relations |
| ATOMICITY_PROBLEM | 4 | 6,3 % | 4 claims COMPOSITE degradados; los 4 sobre-estrictos (0 splits justificados) |

- **Impacto de no-publicación (proposiciones verdaderas y sostenidas en la fuente): 49/64 = 76,6 %** (30 FN + 15 EVIDENCE_SELECTION + 4 atomicity sobre-estrictos). Recuperables con fixes.
- El reviewer acertó al rechazar en 15/64 (8 contradicciones + 7 correct rejections), todas verificadas contra frames/transcript.

### Desglose de los 30 FN por root_cause

| root_cause | n | Detalle |
|---|---|---|
| malformed-verdict | 9 | schema `mke.claims-ground.v2` ≠ v1 y/o dirección `@1@1`; en TODOS los 9 el reviewer había emitido `GROUNDING_SUPPORTED` y el pipeline lo descartó |
| parse-fatal | 5 | `parse-structured [fatal]: assistant content is not a valid JSON object`; nunca hubo veredicto |
| causal | 8 | dependencias definicionales/condicionales enunciadas sin conector literal («si… esto es lo que llamaremos», «En el caso de…», «que si no conoces… porque») |
| deixis | 5 | «eso», «10», «0100», «al final», «en libra» resolubles por discurso/ventana |
| garble-identity | 3 | «Felur Swing» ≡ failure swing; «libra» ≡ GBPUSD; «GIP» ≡ GBP (¡mismo caso que P1!) |

Sub-patrones de los 16 FN semánticos: (a) exigencia de literalidad en dependencias definicionales (8); (b) deixis de discurso no resuelta (5); (c) equivalencia de identidad ASR no aplicada (3). **Los 3 sub-patrones son exactamente los mismos que P1 señaló** (recomendación 2 de P1 no implementada en el prompt de grounding).

## 3. Los 14 casos provider, uno a uno

### 3.1 Parse fatal — `UNSUPPORTED_REVIEW_UNAVAILABLE` (5)

| record_id | ¿La fuente sostiene el statement? | Veredicto |
|---|---|---|
| `cl-eurusd-candle-gains-lower-wick` | **SÍ** — frames 1448s→1452s: la vela negra del lado EURUSD gana una mecha inferior («lo haremos con mecha... Y el de euro que sea así») | **FALSE_NEGATIVE (parse-fatal)**. Replay. |
| `cl-intraturtlesoup-open-pnl-label` | **SÍ** — frame 1036s: «Apertura PyG: 0,01497, Cantidad: 1550387». Nota: el 1er intento del reviewer SÍ fue `GROUNDING_SUPPORTED` (v1) pero fue rechazado por dirección `@1@1`; el reissue murió en parse fatal | **FALSE_NEGATIVE (parse-fatal)**. Replay + fix de addressing. |
| `cl-los-rangos-son-importantes-para-encontrar-entradas` | **SÍ** — «la estrategia se basa principalmente en los rangos... es muy importante para encontrar las entradas» (asr-00020-21) | **FALSE_NEGATIVE (parse-fatal)**. |
| `cl-marco-temporal-alternativo-30` | **SÍ** — «esto lo miró en 15 pero si queréis utilizar 10 25 30» | **FALSE_NEGATIVE (parse-fatal)**. |
| `cl-right-chart-switch-to-gbpusd` | **SÍ** — frame 503s panel derecho XAUUSD · 1D · FOREXCOM → frame 504s GBPUSD · 1D · FOREX.com | **FALSE_NEGATIVE (parse-fatal)**. Replay. |

Todos cuentan en el FN rate (30) con causa anotada `parse-fatal`, según la instrucción del brief.

### 3.2 Malformed verdict — `UNSUPPORTED_INSUFFICIENT` (9; el reviewer SÍ dio veredicto semántico y el pipeline lo descartó)

| record_id | Veredicto semántico del reviewer (descartado) | ¿La fuente lo sostiene? |
|---|---|---|
| `cl-entrada-posicion-corta-114697` | SUPPORTED ×2 (schema v2≠v1 en ambos) | **SÍ** — frame 1756s: entrada corta en 1,14697 |
| `cl-fecha-24-06-2025` | SUPPORTED ×2 (v1 con `@1`, v2 schema) | **SÍ** — frame 561s: «24/6/2025 EURUSD \| 15M» |
| `cl-informacion-curso-intermedio-no-relevante` | SUPPORTED ×2 (schema + `@1@1`) | **SÍ** — cita literal de asr-00003 |
| `cl-observar-rangos-diario-es-facil` | SUPPORTED ×2 (schema + `@1@1`) | **SÍ** — «Es un ejercicio fácil si vamos... a la temporalidad diaria» |
| `cl-operar-solo-grafico-diario` | SUPPORTED ×2 (schema + `@1@1`) | **SÍ** — «podrías hasta operar solo viendo el gráfico diario» |
| `cl-rango-actual-toma-low-vela-anterior` | SUPPORTED ×2 (schema v2≠v1) | **SÍ** — «toma el low de la vela anterior» (asr-00101) |
| `cl-rango-bajista-completa-ordenes` | SUPPORTED ×2 (schema v2≠v1) | **SÍ** — asr-00042/43 verbatim |
| `cl-seleccion-vela-blanca-pequena` | SUPPORTED ×2 (schema v2≠v1) | **SÍ** — frame 684s: vela blanca pequeña con tiradores |
| `cl-smt-convierte-esto-en-rango` | SUPPORTED ×2 (schema + `@1@1`) | **SÍ** — «esta sería una SMT, lo que convertiría esto en un rango» |

Los 9 son **FALSE_NEGATIVE de causa provider** (`malformed-verdict`): el reviewer nunca falló semánticamente; el contrato de salida (schema version y addressing del record_id) sí. **Este bloque entero es recoverable con un fix de formato, sin tocar prompts.**

## 4. Falsos positivos (muestra distribuida de 61 supported)

**0/61 (0 claims de 50, 0 relations de 11).** Verificación: todas las claims text-cited son verbatim o implicación directa; las 11 verificaciones visuales (temporalidad 15M/1D, rectángulo negro seleccionado en GBPUSD 1488s, nivel 1,15611 en 240s, nivel 1,13976 en 1599s, tres rectángulos 1112s, relleno negro + opacidad 83 % en 565s, transición 2 paneles→1 en 553-554s, línea en el máximo de la vela negra GBPUSD 1371s, anotación INTRATURTLESOUP reposicionada 1036→1040s, línea 1,15803 en 1813s, objetivo 1,15034 en 1764s) confirman las reasons del reviewer. **La safety rule no se activa: los falsos positivos no subieron** (baseline 1/30 claims y 1/112 relations; ahora 0).

Dos observaciones de consistencia (no son FP): (i) `rel-felur-swing-explanation-depends-on-chapter` fue publicada SUPPORTED con el garble «Felur Swing», mientras la claim gemela `cl-capitulo-failure-swing` fue rechazada por ese mismo garble — la asimetría de criterio SUPPORTED-vs-INSUFFICIENT de P1 persiste; (ii) `rel-timeframe-25-alternativa-a-15` fue publicada SUPPORTED sobre asr-00257 («si queréis utilizar 10 25 30»), la misma cita por la que `cl-marco-temporal-alternativo-10` fue rechazado por «no identifica ese 10 como marco temporal».

## 5. Comparación old (P1) vs new (P8 rerun)

| Dimensión | P1 (run L1) | P8 rerun @ 19b44c1 | Δ |
|---|---|---|---|
| FN rate | 17,5 % (14/80) | **46,9 % (30/64)** | ▲ +29,4 pp — empeora |
| FN de causa provider | 1/80 (parse fatal) | **14/64** (5 parse fatal + 9 veredictos válidos descartados por schema/addressing) | ▲▲ nuevo modo de fallo dominante |
| EVIDENCE_SELECTION_PROBLEM | 48/80 (60 %) | 15/64 (23,4 %) | ▼ mejora real de la reconstrucción (citas menos truncadas) |
| Contradicciones reales detectadas | 4/4 correctas | 8/8 correctas | = reviewer fiable en lo verificable |
| Atomicity degradados | 5 (2 splits justificados, 3 sobre-estrictos) | 4 (0 justificados, 4 sobre-estrictos) | ≈ sobre-estrictitud persiste (concesivas y multi-verbo) |
| Falsos positivos muestra | 1/30 claims, 1/112 relations | 0/61 | = sin regresión |
| Garble-identity FN | 3 (Turtle Soup ×2, GIP) | 3 (Felur Swing, libra, GIP — **el mismo caso GIP repite**) | = capa de equivalencia de identidad sigue sin alimentar al reviewer |
| Deixis FN | 7 | 5 | = patrón persiste |
| Causal/definicional FN | 3 | 8 | ▲ ahora domina en relations |

Lectura: la reconstrucción mejoró (menos citas truncadas: 60 % → 23 %), pero el rerun introdujo/regresó un fallo sistémico de contrato del reviewer (schema v2 vs v1 y addressing `@1@1`) que convierte veredictos SUPPORTED en no-supported, y los FN semánticos residuales son los mismos patrones que P1 ya documentó sin fix.

## 6. Recordatorio de ejecución (cumplimiento del brief)

- Población 64/64 auditada sin muestreo; clasificación obligatoria aplicada a los 64 (0 PROVIDER_FAILURE como clase final: los 14 casos provider cuya fuente sostiene el statement se cuentan como FALSE_NEGATIVE con root_cause `parse-fatal`/`malformed-verdict`, según la regla del brief).
- Fila JSONL por record con `classification/root_cause/material/evidence_checked/source_quote/justification`: `grounding-audit.jsonl` (64 líneas).
- `material=YES` en los 49 records cuya proposición está sostenida por la fuente (FN + ESP + ATOMICITY); `NO` en los 15 rechazos correctos.

## FEEDBACK (Agents-OS)

1. **El bootstrapping de sesión funcionó bien, pero el brief venía con un dato de población impreciso**: decía «11 records GROUNDING_INSUFFICIENT por malformed verdict» y los datos contienen 9 INSUFFICIENT malformed + 1 REVIEW_UNAVAILABLE que además lleva marca de malformed-reissue (14 casos provider únicos, no 16). Sugerencia: cuando un brief de auditoría cuantifique sub-poblaciones derivadas de un escaneo, adjuntar el listado de IDs (como sí se hizo con los 5 parse-fatal) o indicar «≈» para las cifras estimadas; el auditor tuvo que reconciliar el descuadre por su cuenta.
2. **Las rutas de entradas estuvieron bien especificadas y estables** (`claims.jsonl` canónico, corpus por ventana con paths absolutos de PNG, journal sqlite para fallos de formato, baseline P1 para comparación). El patrón «corpus pre-horneado por ventana + journal durable» ahorra reconstruir el contexto del reviewer y debería ser el estándar de las campañas de aceptación.
3. **Faltaba una definición operativa de `material` en el schema de la fila JSONL** (aparece en el formato exigido pero el brief no la define); el auditor la operationalizó como «la proposición está sostenida por la fuente y su no-publicación pierde conocimiento». Sugerencia: definir los valores de los campos obligatorios en el propio brief para que audits sucesivos sean comparables.
4. **Herramienta**: no había `sqlite3` CLI en el host; el journal se leyó con el módulo `sqlite3` de Python. Si el journal va a ser entrada estándar de auditorías, un dump JSONL junto al run (p.ej. `provider_invocations.jsonl`) evitaría dependencias del entorno.
