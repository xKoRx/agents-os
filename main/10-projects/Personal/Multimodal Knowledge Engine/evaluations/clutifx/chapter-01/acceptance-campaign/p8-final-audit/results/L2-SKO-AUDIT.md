# L2-SKO-AUDIT — P8 auditor L2 · Clutifx 01 rerun @ 19b44c1

- **Run auditado**: `~/mke/clutifx-ch01-rerun-20261003/run-rerun/` (candidato rerun @ `19b44c1`, repo `~/mke/multimodal-knowledge-engine`; HEAD actual `8ae543a`, 1 commit posterior al candidato).
- **Estado del run**: `INCOMPLETE` (pipeline_state), **skos: 0**.
- **Método**: verificación física contra `run.db` (SQLite, tablas `provider_invocations`, `budget_ledger`, `pipeline_state`), `claims.jsonl`, `sko/composition.jsonl`, `skos.jsonl` y `configs/config.rerun.v2.json`. Nada asumido del journal.
- **Fecha**: 2026-10-04. Salidas companion: `l2-invalid-refs.json`.

---

## 1) La invocación de composition — verificada físicamente

`SELECT task, COUNT(*) FROM provider_invocations` → `sko.composition: 1` (de 1618 invocaciones totales). Exactamente una.

| campo | valor (leído de run.db) |
|---|---|
| invocation_id | `7879f510e3b1d7beccb3e55c471b2d7764aa40f64d6510fdb1c65a1267dd4f82` |
| task / target | `sko.composition` / `sko-composition` |
| prompt_version | `mke.sko-compose.v1` |
| model / response_id | `stealth/space-bunny-alpha` / `gen-1791131076-wBuYmYUbAO4ZdY2eWlwD` |
| response_state | `REJECTED` |
| at_utc | `2026-10-04T16:28:27.804673233Z` (última invocación del run, índice 1617/1617) |
| request_json | 160,575 bytes (catálogo embebido en `system`: **997 claims + 128 relations = 1125 records**; `text_parts` = 30 bytes) |
| response_json | 17,116 bytes — `schema: mke.sko.v1` + **23 objetos** (kinds: 12 rule, 7 concept, 2 strategy, 2 example) con **164 component refs** |

`sko/composition.jsonl` (1 línea, proyección del run):
`composition_rejected: composition proposal rejected: object sko-range-chain-strategy component 0 references claim cl-estrategy-chain-of-ranges@1 which does not exist at that exact version`
(`catalog_over_budget=false`, `composition_unavailable=false`, `composition_budget_blocked=false`).

`sko/integrity.jsonl` y `sko/review.jsonl`: **0 líneas** — con la propuesta rechazada el pipeline nunca llegó a review/integrity/publicación.

## 2) Razón del rechazo y validación de las 164 refs contra el catálogo real

Catálogo canónico (`claims.jsonl`, mismo `config_fingerprint` que el header de skos): **1043 claims (todos @1) + 146 claim_relations + 1 header = 1190 records**. No existe ninguna claim a versión distinta de @1.

Resultado de validar cada componente de los 23 objetos contra ese catálogo:

- **7 refs inválidas en 4 objetos** (detalle exacto en `l2-invalid-refs.json`); **19/23 objetos 100 % válidos**; 157/164 refs válidas (95.7 %).
- Razones: **7 × not-exists, 0 × wrong-version**. La prueba de «versión equivocada» no ocurre: el catálogo es mono-versión (@1).

| objeto | kind | comps | refs inválidas | near-miss |
|---|---|---|---|---|
| `sko-range-chain-strategy` | strategy | 7 | 2 | `cl-estrategy-chain-of-ranges@1` → **existe `cl-strategy-chain-of-ranges@1`** (slip de la «e» intrusa); `cl-estrategy-cadena-de-rangos@1` → **existe `cl-estrategia-cadena-de-rangos@1`** (estrategy/estrategia) |
| `sko-reset-range` | rule | 12 | 3 | `cl-reinizado-requiere-{contra-tendencia,objetivo-bullish,rango-bajista}@1` → sin match de id; vecino semántico `cl-regla-rango-bajista-bullish-reiniciado@1` |
| `sko-failure-swing` | concept | 8 | 1 | `cl-failure-swing-puede-darse-varios-casos@1` → **existe `cl-failure-swing-varios-casos@1`** (id derivado del statement «El failure swing puede darse por varios casos.») |
| `sko-broker-low-comparison` | concept | 9 | 1 | `cl-rango-se-crearia-tras-comparacion@1` → sin match en catálogo |

**Hipótesis del slip confirmada como plausible**: el catálogo contiene simultáneamente `cl-estrategy-seguir-cadena-precios@1` (híbrido ES/EN «estrategy») y `cl-strategy-chain-of-ranges@1`. El compositor mezcló el prefijo «estrategy-» con «chain-of-ranges». 3 de las 7 refs inválidas (las de `sko-range-chain-strategy` y `sko-failure-swing`) tienen un id correcto a una mutación de distancia; las otras 4 (las 3 «reinizado-requiere» y «rango-se-crearia») parecen ids parafilados directamente del texto, no del catálogo.

**Patrón, no caso único**: el mensaje de rechazo reporta solo el primer componente inválido (fail-fast, index 0 de `sko-range-chain-strategy`), pero el daño real era **7 refs en 4 objetos**. Rechazar la propuesta completa por la primera ref descartó **19 objetos válidos** que habrían pasado cualquier revisión.

## 3) Performance L2

- **Config** (`~/mke/clutifx-ch01-rerun-20261003/configs/config.rerun.v2.json`, verificado físicamente): `"composition_timeout_seconds": 600` presente (y `"review_timeout_seconds": 120`).
- **Latencia real**: dispatch según `budget_ledger` (entradas 4265/4266, acquisition_key = invocation_id) a las `16:24:36.324Z` → invocación registrada a las `16:28:27.804Z` = **231.5 s (3 min 52 s)**. **39 % del timeout de 600 s — el timeout NO fue factor.** Una sola petición, sin reintentos: el fallo de transporte de B-02 (`read-body retry-exhausted`) no se repitió.
- **Tokens** (usage_json): prompt 41,972 / completion 23,922 / total 65,894. Ratio 160,575 B / 41,972 tok ≈ 3.83 B/tok (catálogo JSON por token razonable; la estimación ~160 kB ≈ 42 k tokens cuadra con lo facturado).
- **Comparación con B-02** (`clutifx-ch01-full-live-20261001/run-live`, verificado): catálogo embebido **741 claims + 112 relations = 853 records** (coincide con la cifra 853 del journal), request **121,155 bytes** (coincide exacto), `error_detail: vlm provider read-body [retry-exhausted]: retry budget of 2 exhausted` (3 intentos — consistente con el 3×120s), sko_count 0. El rerun creció ×1.32 en bytes y ×1.32 en catálogo embebido y además **completó** la lectura y el parseo.

| métrica | B-02 (run viejo) | P6 targeted | Rerun @19b44c1 |
|---|---|---|---|
| catálogo embebido (records) | 853 (741cl+112rel) | ~130–149 claims | 1125 (997cl+128rel) |
| request bytes | 121,155 | 25,550 | 160,575 |
| prompt tokens | n/d (usage vacío) | 6,761 | 41,972 |
| completion tokens | n/d | 25,909 | 23,922 |
| intentos / latencia | 3 × ≤120 s → read-body exhaust | 1 × ~13 min (dispatch 01:20:13 → 01:33:59) | **1 × 231.5 s** (<< 600 s) |
| resultado | sin respuesta (transporte) | VALIDATED, 19 SKOs | REJECTED (validación de refs) |

## 4) Destino tras el rechazo

- **No hubo retry ni corrective reissue**: `COUNT(*) task='sko.composition'` = 1; es además la última invocación del run (nada se ejecutó después). El run terminó ahí.
- `pipeline_state.status = INCOMPLETE`; `status_reasons` = **102 entradas**:
  - **19** rechazos de ventana (identity collisions / DIVERGENT en equivalence_review, epistemic/kind deterministic divergences, 1 evidence ref desconocida, 1 relation id no-estable).
  - **64 non-supported** exactos: 46 claims + 18 relations (49 `UNSUPPORTED_INSUFFICIENT`, 10 `UNSUPPORTED_CONTRADICTED`, 5 `UNSUPPORTED_REVIEW_UNAVAILABLE`), más 18 entradas de detalle por-record (`GROUNDING_INSUFFICIENT`/`REVIEW_UNAVAILABLE` con razón).
  - **1** rechazo L2: la composition (esta auditoría).
- `skos.jsonl`: **solo header**, `sko_count: 0` (verificado), `schema mke.sko.v1`, mismo `source_id`/`config_fingerprint` que el catálogo de claims. `sko/` contiene composition.jsonl (1 línea de rechazo) y review/integrity vacíos.

## 5) Comparación con P6 (targeted live) y con el run viejo

P6 (`clutifx-ch01-p6-gate-20261003/run-p6`, verificado): catálogo **149 claims** + 24 relations; composition **1 invocación, VALIDATED**, request 25,550 bytes / 6,761 prompt tokens; **19 objetos, 97 refs, 0 inválidas**; review.jsonl 19 records; `skos.jsonl sko_count: 19`.

| escala | P6 | Rerun | factor |
|---|---|---|---|
| claims en catálogo | 149 | 1043 | ×7.0 |
| request bytes | 25,550 | 160,575 | ×6.3 |
| prompt tokens | 6,761 | 41,972 | ×6.2 |
| refs propuestas | 97 | 164 | ×1.7 |
| objetos propuestos | 19 | 23 | ×1.2 |

**Qué cambia con la escala**: el tamaño de salida del compositor es casi constante (completion 25.9k vs 23.9k tokens) pero la superficie de validación crece. La tasa de slip observada en el rerun fue 7/164 ≈ 4.3 % de refs; con rechazo atómico, P(fallar el gate) = P(≥1 ref inválida en toda la propuesta), que crece con el catálogo. En P6 el compositor no cometió ni un error (0/97) y el mecanismo funcionó; en el rerun, con ×1.7 refs y un vocabulario de ids ES/EN híbrido (estrategy/estrategia/strategy conviven), un solo slip ya condenaba las 23. **La diferencia P6↔rerun es de exposición al error por escala, no de mecanismo** — el mecanismo de composition funcionó a escala chica y el validador hizo exactamente lo que su contrato decía (rechazo atómico fail-closed).

## 6) Clasificación del defecto y remediation

### Clasificación

- **Defecto**: granularidad de la validación L2 — el gate de composition es atómico a nivel de *propuesta* (fail-closed todo-o-nada). No es una violación del frozen contract de publicación: **nada inválido llegó a publicarse** (el sistema falló cerrado correctamente) y L0/L1 quedaron intactos y congelados.
- **Clase: MAJOR** (gate-blocking puntual, no BLOCKER). Para el gate **L2_REACHED=YES** (exige SKOS_TOTAL>0) este candidato **falla tal como está** → L2_REACHED=NO con causa única y determinista: 7 refs inválidas en 4 objetos condenaron 19 objetos válidos (95.7 % de las refs eran correctas). No hay corrupción de datos, no hay breach del contrato de salida, y el arreglo no toca L0/L1.
- Nota de repositorio: la remediation (a) **ya está implementada y commiteada en HEAD `8ae543a`** («fix(v2): validate composition proposals object by object (R-M05)», 2026-10-04 17:20 UTC, 52 min después del fallo; 446 inserciones en `internal/sko/sko.go`, `internal/pipeline/v2_sko_stages.go` + tests; prompt/schema del compositor sin cambios). El candidato evaluado es su padre `19b44c1`.

### Opciones

| opción | diff | semántica «fail-closed» | ¿full rerun? |
|---|---|---|---|
| **(a) validación por-objeto** (descartar objetos con refs inválidas, publicar los válidos; rechazo total solo si 0 objetos válidos) | ya implementada en `8ae543a`, lado pipeline únicamente | **preservada en el invariante que importa**: nunca se publica una ref no resuelta al catálogo; la atomicidad se mueve de propuesta→objeto, con razón durable por objeto. Coste conocido: se pierden 4 objetos (entre ellos el strategy central `sko-range-chain-strategy`) — pérdida de cobertura documentable, no de integridad | **No**: targeted live del stage L2 sobre el catálogo congelado (claims.jsonl @21278b86…); la misma respuesta de composition validada con el código nuevo produce 19 objetos que siguen el flujo normal de reviews |
| (b) corrective reissue de composition (patrón claims.reconstruction para schema) | loop de reissue + presupuesto (~66k tokens extra) | se mantiene atómico → un nuevo slip vuelve a rechazar las 23 | targeted live, con no-determinismo (nueva salida = nueva superficie de error) |
| (c) tolerancia de versión (@N → @latest) | trivial en código | **irrelevante aquí**: catálogo mono-versión @1 y 0 refs fallaron por versión; las 7 son not-exists a nivel de id. Riesgo semántico real (publicar contra versión no revisada) sin beneficio medido en este run | no aplica |
| (d) no-fix (deuda documentada) | 0 | intacto | **sí full live** (~1618 invocaciones) con P(fallo) alta de nuevo: a 4.3 % de slip por ref, P(≥1 slip en 164 refs) ≈ 1 − 0.957^164 ≈ 99.9 % |

### Recomendación (KISS/YAGNI)

**(a)** — ya escrita, testeada y commiteada en HEAD; conservarla como remediation y validarla con un **targeted live de stage L2** sobre el catálogo grabado del rerun (composition + composition reviews; L0/L1 no se re-ejecutan). Expectativa con la evidencia actual: 19/23 objetos publicables (los 4 con refs inválidas se descartan con razón durable por objeto). No implementar (b) ahora: solo si la cobertura de los 4 objetos descartados (especialmente la cadena de rangos) resulta necesaria — sería un único reissue acotado con el rejection reason como feedback, y seguiría conviviendo con el gate por-objeto de (a) como red de seguridad. (c) y (d) descartadas por la evidencia.

---

## FEEDBACK (Agents-OS)

1. **Bootstrap inaccesible desde subagentes**: esta sesión corrió como subagente ZCode one-shot y el harness rechaza la tool Skill (`Skill is not allowed for subagent`), pese a que AGENTS.md ordena invocar `agents-os-bootstrap` al inicio. Fallback aplicado: lectura directa del `SKILL.md` + orientación mínima. Sugerencia: documentar en AGENTS.md/bootstrap una **ruta degradada explícita para subagentes** (marker → leer SKILL.md como archivo → orientación mínima → feedback), para que el mandato no produzca un dead-end silencioso.
2. **One-shot con salidas fuera del vault**: el routing por marker funcionó (VAULT_ROOT resuelto), pero los entregables de la auditoría viven en el repo de proyecto (`~/mke/...`) y el vault solo aloja `results/`. La convención funcionó bien; sería útil que el entity pack de MKE referencie la ruta canónica de `acceptance-campaign/p8-final-audit/results/` para futuros auditores.
3. Sin fricción adicional: el resto del turno fue warm/task-local, sin necesidad de entity retrieval.
