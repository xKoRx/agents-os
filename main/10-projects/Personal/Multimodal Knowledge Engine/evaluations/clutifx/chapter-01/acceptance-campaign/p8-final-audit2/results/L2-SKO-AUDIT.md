# L2-SKO-AUDIT — P8 auditor L2 · Clutifx 01 run **P7b** @ `e7bc387`

- **Run auditado**: `~/mke/clutifx-ch01-rerun2-20261004/run-rerun2/` (candidato `e7bc387`; repo `~/mke/multimodal-knowledge-engine` HEAD = `e7bc387`, verificado).
- **Resultado del run**: `L2_REACHED = YES` a escala completa — **26 SKOs publicados** (`skos.jsonl` `sko_count: 26`, verificado). Auditados **los 26**.
- **Método**: verificación física contra `run.db` (SQLite: `provider_invocations`, `budget_ledger`, `pipeline_state`, `pipeline_records`, `record_stages`, `record_outcomes`, `dependency_edges`), `claims.jsonl`, `skos.jsonl`, `sko/{composition,integrity,review}.jsonl`, `configs/config.rerun.v2.json` y el código del candidato (`internal/sko/sko.go`, `internal/pipeline/v2_sko_stages.go`). Nada asumido del journal.
- **Fecha**: 2026-10-05. Salida companion: `l2-sko-audit.jsonl` (26 filas, una por SKO publicado, con invocation_ids verificados contra `sko/review.jsonl`).

---

## 1) La invocación de composition — verificada físicamente

`SELECT task, COUNT(*) FROM provider_invocations` → **`sko.composition: 1`** (de 1094 invocaciones totales; además 33 `sko.composition_review`). Exactamente una, sin retry.

| campo | valor (leído de run.db) |
|---|---|
| invocation_id | `2971f1327805832d5557bc66c41d54b61b03324fb11e7d82594e0dba7b6a4bbd` |
| task / prompt_version | `sko.composition` / `mke.sko-compose.v1` |
| model / response_id | `stealth/space-bunny-alpha` / `gen-1791195481-toSBvIUXjgk0erTX0FW3` |
| response_state | **`VALIDATED`** |
| at_utc | `2026-10-05T10:25:16.935Z` |
| request_json | **77,973 bytes** (system 77,128 B; catálogo embebido **459 claims + 82 relations = 541 records** — la tarea estimaba ~553; medido: **541**) |
| response_json | **17,054 bytes (17KB ✓)** — `schema mke.sko.v1` + **28 objetos** con **162 component refs** |
| usage | prompt **20,721** / completion **57,478** / total **78,199** tokens |
| flags (`sko/composition.jsonl`) | `catalog_over_budget=false`, `composition_unavailable=false`, `composition_budget_blocked=false` |

**El catálogo embebido es exactamente el subconjunto SUPPORTED**: 459/459 claims `SUPPORTED_BY_AUTONOMOUS_REVIEW` del catálogo y 82/82 relations soportadas; excluye 307 claims (302 `UNSUPPORTED_REVIEW_UNAVAILABLE` + 4 `INSUFFICIENT` + 1 `CONTRADICTED`) y 22 relations no soportadas. Verificado 1:1 contra `claims.jsonl` (mismo `config_fingerprint` `f05c95e4…` en header de ambos archivos).

## 2) Aritmética propuesta → descarte → revisión → publicación (el fatal 10:29Z, resuelto)

**28 propuestos → −2 descartes R-M05 → 26 publicados. El composition_review fatal de 10:29Z NO restó ningún objeto.**

1. **Propuestos: 28 objetos / 162 refs** (kinds: 9 example, 8 concept, 8 rule, 2 procedure, 1 strategy).
2. **Validación independiente de las 162 refs contra el catálogo real**: exactamente **2 refs inválidas**, ambas `NOT_IN_CATALOG` a versión exacta, 0 versiones equivocidas (catálogo mono-versión @1):
   - `sko-range-chain-strategy` **c9** (0-based) → `cl-precio-actua-como-cadena@1` no existe;
   - `sko-turtle-soup` **c4** (0-based) → `cl-turtlesoup-low-sweep-bullish-reaction@1` no existe.
3. **Razones durables por objeto — correctas y verificadas**: ambas aparecen verbatim en `pipeline_state.status_reasons` (el almacén durable del run):
   - `L2 composition object discarded: object sko-range-chain-strategy: component 9 references claim cl-precio-actua-como-cadena@1 which does not exist at that exact version`
   - `L2 composition object discarded: object sko-turtle-soup: component 4 references claim cl-turtlesoup-low-sweep-bullish-reaction@1 which does not exist at that exact version`
   Son las **únicas** 2 entradas de descarte L2 en las 719 razones del run. Mecánica confirmada en el código del candidato (`internal/sko/sko.go:252` `discard(...)` per-object, R-M05; el `fail(...)` atómico antiguo quedó en `wt/`).
   - **Matiz near-miss**: ambos ids existen a una mutación de distancia y son soportados — `cl-precio-actua-como-una-cadena` («una») y `cl-turtle-soup-low-sweep-bullish-reaction` («turtle-soup» con guiones). El descarte es **correcto bajo el contrato de id exacto** y durable; el coste es conservador (2 objetos perdidos con contenido casi íntegro disponible). Mismo patrón de alucinación-de-id que rerun-1, ahora contenido a nivel objeto.
4. **Los 26 publicados son exactamente los propuestos menos los 2 descartados**: set-difference verificado en ambos sentidos (0 diferencias); además cada SKO publicado es **idéntico** al propuesto en `components/kind/name` (fidelidad campo a campo) y `dependency_edges` registra 142 = las refs de los 26.
5. **El fatal 10:29Z**: `baee7652…` a las `10:29:18.766Z`, review de `sko-range-completion`, `vlm provider parse-structured [fatal]: assistant content is not a valid JSON object`. **No eliminó ningún objeto**: `sko-range-completion` está publicado (con `UNSUPPORTED_REVIEW_UNAVAILABLE`). La aritmética correcta es **26 = 28 − 2**, no 28 − 2 − 1: el fatal solo degradó el estado de review de un objeto ya admitido por la validación estructural.

## 3) Los 33 composition_reviews — mapeo objeto → veredicto

33 invocaciones (`10:25:19Z–10:34:26Z`, ~9 min) = **26 reviews iniciales + 7 corrective reissues**. Resultado físico: **14 VALIDATED / 7 REJECTED / 12 caídas** (coincide con P7B-RESULTS.md).

- **12 caídas en el incidente de transporte** (11 con `parse retry-exhausted: response contains no choices`, entre 10:25:19 y 10:28:39, dentro de la ventana del blackout 04:34–10:28Z; +1 fatal parse = range-completion, 10:29:18) → esas 12 SKOs con `REVIEW_UNAVAILABLE`.
- **7 REJECTED — rechazo mecánico de formato, no semántico**: las 7 salidas llevan `sko_id` **con sufijo `@1`** (eco literal del target `id@1`), que resuelto a `id@1@1` ≠ target `id@1` — razón explícita en `record_outcomes` de range-completion: `reviewer_malformed_output: composition review output addresses sko-range-completion@1@1, review target is sko-range-completion@1`. En las 7 el **veredicto semántico interno fue COMPOSITION_SUPPORTED**; el pipeline las descartó por contrato de salida y lanzó corrective reissue: **6/7 reissues → VALIDATED**; la de range-completion cayó con el fatal (ver §2.5). Las 14 VALIDATED llevan `sko_id` limpio, sin excepción.
- **14 VALIDATED** = 13 `COMPOSITION_SUPPORTED` + 1 `COMPOSITION_UNSUPPORTED` (sko-scalp-range-conditions: excepción material no representable).
- **¿Algún objeto propuesto fue rechazado por el review y re-propuesto?** **No.** Hubo 1 sola composition; los reissues fueron de *review*, nunca de propuesta. Ningún objeto válido fue eliminado por un review.
- **Cierre de relaciones** (`record_outcomes`): `relation_closure_unjudged` ×4 (range-completion ×3, intermediate-course-continuation ×1 — ambas con review caído), `relation_closure_lost` ×1 (scalp — material EXCEPTION_TO hacia claim no componente). Registrados como razones, sin corrupción.

Publicación final de los 26: **12 `SUPPORTED_BY_AUTOMATED_REVIEW` + 12 `UNSUPPORTED_REVIEW_UNAVAILABLE` + 1 `UNSUPPORTED_CONTRADICTED` + 1 `UNSUPPORTED_PARTIAL`**. `sko/integrity.jsonl`: 26/26 `INTEGRITY_PASS`.

## 4) Auditoría de los 26 SKOs publicados (componentes, semántica, soporte fuente)

- **Componentes**: los **142 refs** de los 26 (todos, no una muestra — supera el mínimo de 3/SKO) verificados contra `claims.jsonl`: existencia a versión exacta **142/142**, publication `SUPPORTED_BY_AUTOMATED_REVIEW` **142/142**, versión correcta 142/142.
- **Semántica**: leídos los statements de **todos** los componentes de **cada** SKO contra su `name/kind/roles`. Clasificación (detalle por SKO en `l2-sko-audit.jsonl`):

| clase | n | SKOs |
|---|---|---|
| OK_SUPPORTED (review respaldó) | 12 | bullish-range-target, daily-bullish-objective, range-formation, range-reassessment, range-types, reset-range, smt-examples, smt-representation, tartel-sub, timeframe-range-reading, turtle-soup-long-stop, xauusd-range-example |
| OK_REVIEW_UNAVAILABLE (coherente bajo auditoría manual; review caído por incidente) | 12 | 12h-range-example, 8h-pending-range-example, bullish-continuation, candle-polarity, daily-range-observation, four-hour-range-example, gbpusd-range-example, intermediate-course-continuation, intra-turtle-soup, pending-range, range-closure, range-completion |
| PARTIAL (degradado por el pipeline, razón material verificada) | 1 | scalp-range-conditions |
| FAIL-CLOSED (contradicción interna catcheada) | 1 | objective-correction |

- **0 material WRONG publicados**; 0 OVERGENERALIZED. Notas menores: roles `condition` que elevan hechos observados (bullish-continuation), redundancia near-duplicate ES/EN o paráfrasis en ~10 SKOs (p.ej. `cl-rango-es-alcista`≈`cl-rango-alcista`) — fidelidad sin riesgo semántico. `range-completion` compone regla («va a completarlo») + excepción explícita («no siempre») que conviven como regla matizada, tal como las dicen las claims.
- **Falsos merges vía SKO (§ contracciones internas)**: el catálogo tiene **4 relations CONTRADICTS soportadas**; 3 nunca fueron co-compuestas; la 1 co-compuesta (`rel-objetivo-corregido-contradice-inicial` dentro de **sko-objective-correction**) fue **catcheada** por el pipeline (`composition_contradicted` ×2, ambos sentidos) y fail-closed a `UNSUPPORTED_CONTRADICTED` pese a que el review la había aprobado. **0 falsos merges publicados** — la red de seguridad actuó donde el review falló. Auditoría manual de los 142 statements: sin contradicciones internas adicionales (los pares modal/frecuencia de candle-polarity e intra-turtle-soup son compatibles).
- **Nota de política (no bloqueante)**: objective-correction es narrativamente una *corrección* (inicial → rechazada → corregida); el fail-closed es correcto bajo la política actual y conservador. Ver FEEDBACK.

## 5) Performance L2 (medida) y comparativa

**Latencia**: dispatch según `budget_ledger` (entradas 2474/2475, acquisition_key = invocation_id) a las `10:18:01.571Z` — idéntico al timestamp embebido en el response_id `gen-1791195481` — → invocación registrada `10:25:16.935Z` = **435.4 s (7 min 15 s) = 72.6 % del timeout de 600 s** (`composition_timeout_seconds: 600` verificado en `configs/config.rerun.v2.json`). **El timeout NO fue factor** (B-02 cert se mantiene), aunque el margen es menor que en rerun-1 (231.5 s) porque el modelo gastó 57,478 completion tokens (2.4×), thinking-heavy. Sin reintentos. Reviews posteriores: 33 invocaciones en ~9 min (34,653 tokens en las 21 con respuesta).

| métrica | B-02 (run viejo) | P6 targeted | rerun-1 @19b44c1 | **P7b @e7bc387** |
|---|---|---|---|---|
| catálogo embebido (records) | 853 (741cl+112rel) | 149cl+24rel | 1125 (997cl+128rel) | **541 (459cl+82rel, solo supported)** |
| request bytes | 121,155 | 25,550 | 160,575 | **77,973** |
| response bytes | n/d | n/d | 17,116 | **17,054** |
| prompt tokens | n/d | 6,761 | 41,972 | **20,721** |
| completion tokens | n/d | 25,909 | 23,922 | **57,478** |
| intentos / latencia | 3×≤120 s → read-body exhaust | 1× ~13 min | 1× 231.5 s | **1× 435.4 s (72.6 % de 600 s)** |
| resultado | sko_count 0 (transporte) | VALIDATED, 19 SKOs (19/19 SUPPORTED) | REJECTED atómico (7 refs inválidas en 4 objetos → 0 SKOs) | **VALIDATED, 28 propuestos → 26 SKOs (R-M05)** |

Lecturas: (a) el catálogo embebido ahora se renderiza **solo con records soportados** (`renderClaimCatalog`), por eso P7b baja a 541 records pese a 766 claims — el request se mantiene acotado (~144 B/record ≈ lineal, muy por debajo del payload que mató a B-02); (b) la latencia crece con los completion tokens (thinking del modelo), no con el catálogo — vigilable en P7c con más claims soportadas y más objetos; (c) R-M05 convirtió el modo de fallo de rerun-1 (7 refs inválidas → 0 SKOs) en (2 refs → 26 SKOs).

## 6) Veredicto

- **26/26 SKOs auditados**: 24 OK (12 respaldados por review + 12 coherentes con review caído por el incidente externo), 1 PARTIAL correcto (scalp), 1 fail-closed correcto (objective-correction).
- **0 material WRONG publicados.** Aritmética cerrada: **26 = 28 propuestos − 2 descartes R-M05** (razones durables correctas, near-miss de ids reales); el composition_review fatal 10:29Z (range-completion) no alteró el recuento.
- **Falsos merges: 0 publicados**; 1/1 contradicción interna co-compuesta catcheada y fail-closed.
- **Performance: composition en 435.4 s (72.6 % de 600 s)**, 1 intento, catálogo 541 records / 77,973 B — B-02 cert y R-M05 cert verificados end-to-end a escala real.

## FEEDBACK (Agents-OS)

**Qué funcionó y debe conservarse**
1. **R-M05 per-object fue la remediación decisiva de este run**: mismo patrón de alucinación de ids del composer que en rerun-1 (allí 7 refs/4 objetos → 0 SKOs por rechazo atómico; aquí 2 refs/2 objetos → 26 SKOs publicados). Razones por objeto durables en `status_reasons` — auditables sin reconstruir nada. Mantener el contrato de «id exacto a versión exacta»: es lo que hace el descarte objetivo.
2. **composition_contradicted (falsos merges)**: catcheó la única contradicción interna real que el review había aprobado. No relajarla.
3. **Degradación honesta**: los 12 SKOs con review caído se publican con estado `UNSUPPORTED_REVIEW_UNAVAILABLE` trazable a la causa de transporte — permitió auditar este run sin ambigüedad.

**Friction / mejoras propuestas (por prioridad)**
1. **Contrato de salida del review (`mke.sko-review.v1`)**: 7/33 salidas (21 %) fueron REJECTED **solo** porque el modelo devolvió `sko_id` con el sufijo `@1` del target (→ `id@1@1`), quemando 7 reissues y — en cascada con el incidente — dejando a range-completion sin review. Fix barato y determinista: normalizar/aceptar sufijo `@version` opcional en el parse del review output (o hacer strip antes de comparar). Habría ahorrado 8 invocaciones y 1 review perdida.
2. **Asimetría de `relation_closure_unjudged`**: solo 2 de las 12 SKOs con review caído recibieron códigos unjudged; p.ej. `sko-range-closure` tiene `rel-cierre-fuera-excepcion-scalp` tocando 2 de sus componentes y no fue marcada. Verificar la condición de disparo del closure check cuando el review muere por transporte (debería emitir unjudged para toda relación soportada que toque ≥2 componentes sin veredicto).
3. **Política de contradicción narrativa**: objective-correction compone una corrección (A → rechazo de A → B) y las dos claims son extremos de una CONTRADICTS soportada; el fail-closed es correcto hoy, pero pierde objetos legítimos. Considerar un tipo de relación `SUPERSEDES`/permiso explícito cuando la contradicción es el propio contenido del procedimiento, manteniendo fail-closed por defecto.
4. **Upgrade de reviews caídas**: las 12 `UNSUPPORTED_REVIEW_UNAVAILABLE` son candidatas a un pase de re-review (resume tipo P7c) sin recomponer; hoy no hay camino de re-review sin re-run completo.
5. **Presupuesto de completion**: la latencia de composition está dominada por los 57k completion tokens (thinking). Si P7c duplica claims soportadas, vigilar p95 de latencia vs 600 s; un cap de razonamiento o muestreo del catálogo por relevancia serían las palancas, no reducir timeout.
