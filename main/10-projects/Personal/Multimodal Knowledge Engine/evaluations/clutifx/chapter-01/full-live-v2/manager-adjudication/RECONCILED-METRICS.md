# RECONCILED-METRICS — CLUTIFX CH01 full-live-v2

Reconciliación física del Review Bundle (`555a4260`) contra fuentes durables, en el orden de autoridad congelado:

1. `run.db` durable (`~/mke/clutifx-ch01-full-live-20261001/run-live/run.db` + snapshots de crash)
2. `claims.jsonl` / artefactos canónicos (byte-a-byte en este bundle)
3. journal de invocaciones de provider (`provider_invocations`)
4. proyecciones deterministas (`record_outcomes`, `record_stages`, `window-coverage.json`, audits)
5. tooling de review derivado (`METRICS.json`, analyze/build scripts)
6. narrativas (README/RUN/MANAGER-REVIEW/bitácora)

Método: cada número fue re-contado físicamente desde su fuente (SQL sobre run.db, parse de claims.jsonl, reproducción de la heurística derivada). Donde la narrativa discrepaba, se corrigió la narrativa; ningún artefacto durable fue alterado. Las discrepancias de reporting se listan en **REPORTING-ERRATA.md**.

Run: producto `ef53530756a27009517030a1bd29f0472bb3ad48` · source `4de8f12d…` · config fingerprint `10418ccf…` · `CLUTIFX_CH01_FULL_LIVE = INCOMPLETE_USEFUL` (exit 4 terminal ordenado).

---

## 1. Windows (130 canónicas)

| Contador | Valor | Autoridad física |
|---|---|---|
| attempted | **130** | 130 filas `claims.reconstruction` en el journal (126 VALIDATED + 4 REJECTED) |
| accepted | **104** | `coverage.json`: 104 ventanas accepted, cada una con ≥1 record introducido; suma de records introducidos = 933 = todos los canónicos |
| rejected | **26** | `coverage.json` + 26 razones window-level en `status_reasons` |
| → bad evidence ref | **4** (w0003, w0005, w0043, w0110) | Filas REJECTED del journal: JSON válido con refs inventadas (`asr-00003 [34850-49400]`, `asr-00005 [61640-81320]`, `asr-00098 [572710-594750]`, `transcript asr-00245`) |
| → identity divergence | **22** | 16 deterministas (kind/epistemic/structural, sin llamada al reviewer) + 6 semánticas DIVERGENT (ver §5) |
| → other reconstruction rejection (JSON malformado / decode) | **0** | 0 filas con decode fallido; las 4 REJECTED son validación de propuesta, no malformación |
| unavailable | **0** | `unavailable_list` vacío; ninguna región sin intentar |

Categorías congeladas (mutuamente excluyentes): `bad_evidence_ref = 4` · `identity_divergence = 22` · `malformed_json = 0` · `unavailable = 0`. La etiqueta `other` del bundle (w0003/w0005/w0043) no es una categoría real: es la razón de historia de resume («rejected in a previous attempt») que ocultó la razón original de validación (ver ERRATA E-03/E-04).

## 2. L1 — propuestas y canónico

| Contador | Valor | Autoridad física |
|---|---|---|
| claims propuestas | **1039** | línea `identity ladder` de documentation.md (durable, byte-idéntica en replay) |
| relations propuestas | **168** | ídem |
| exact duplicates suprimidos | **1** | `record_stages` state `DUPLICATE_SUPPRESSED` = 1 |
| canonical claims | **803** | `claims.jsonl` (803 `record_type:claim`, verificado por conteo) |
| canonical relations | **130** | `claims.jsonl` (130 `record_type:claim_relation`) |
| integrity | **933/933 INTEGRITY_PASS** | `record_outcomes` + campo integrity de los 933 records |
| kind (claims) | claim 251 · observation 250 · parameter 104 · rule 101 · procedure_step 97 | conteo sobre claims.jsonl |
| epistemic (claims) | INSTRUCTOR_SAID 561 · VIDEO_OBSERVED 233 · MODEL_INFERRED 9 | conteo sobre claims.jsonl |
| epistemic (relations) | INSTRUCTOR_SAID 114 · VIDEO_OBSERVED 3 · MODEL_INFERRED 13 | conteo sobre claims.jsonl |
| epistemic (combinado 933) | 675 / 236 / 22 | suma de los dos anteriores (alcance del número de RUN.md) |
| relation types | DEPENDS_ON 117 · EXCEPTION_TO 7 · CONTRADICTS 4 · EQUIVALENT_TO 2 | conteo sobre claims.jsonl |

## 3. Grounding (nivel record, antes de publicación)

| Grounding | Claims | Relations |
|---|---|---|
| GROUNDING_SUPPORTED | **746** | **112** |
| GROUNDING_INSUFFICIENT | **52** | **17** |
| GROUNDING_CONTRADICTED | **4** | **1** |
| REVIEW_UNAVAILABLE | **1** (`cl-rango-rectangular-vertical`) | 0 |

Autoridad: `record_outcomes` (SQL) y campo `grounding.status` de los 933 records en claims.jsonl — ambos coinciden exactamente.

## 4. Publicación (nivel canónico publicado)

| Publicación | Claims | Relations |
|---|---|---|
| SUPPORTED_BY_AUTOMATED_REVIEW | **741** | **112** |
| UNSUPPORTED_INSUFFICIENT | **57** | **17** |
| UNSUPPORTED_CONTRADICTED | **4** | **1** |
| UNSUPPORTED_REVIEW_UNAVAILABLE | **1** | 0 |
| **Total** | 803 | 130 |

**Degradación COMPOSITE (atomicidad whole-window): exactamente 5 claims** pasaron de `GROUNDING_SUPPORTED` a `UNSUPPORTED_INSUFFICIENT` (0 relations degradadas):

- `cl-comparacion-diaria-eurusd-gbpusd@1`
- `cl-dialogo-muestra-un-minuto@1`
- `cl-linea-une-maximos-eurusd-gbpusd@1`
- `cl-rango-se-puede-eliminar-por-cierre-fuera@1`
- `cl-vela-abre-toma-high-cierra-adentro@1`

Aritmética cerrada: 52 INSUFFICIENT + 5 COMPOSITE = 57 claims INSUFFICIENT publicadas; 741 + 112 = **853 supported**; 62 + 18 = **80 non-supported** (74 INSUFFICIENT + 5 CONTRADICTED + 1 REVIEW_UNAVAILABLE). Coherente en run.db, claims.jsonl, status_reasons (113 líneas = 26 window + 6 record + 1 L2 + 80 publicación) y replay.

`SUPPORTED_BY_AUTOMATED_REVIEW` no implica verdad externa ni humana (contrato congelado); por eso la revisión del Owner no parte de estos marcadores.

## 5. Identity (ladder)

| Contador | Valor | Autoridad física |
|---|---|---|
| identity collisions | **38** | línea ladder durable |
| → deterministic-equivalent | **1** (w0011, `cl-estrategia-se-basa-principalmente-en-rangos`: idéntico tras normalización conservativa; **sin crecimiento de unión** — el record canónico conserva 1 evidence ref y 1 invocation) | `pipeline_records` del record |
| → semantic-equivalent (decididos) | **15** | 11 veredictos EQUIVALENT de las 17 llamadas live + 4 re-verdictos content-addressed (todos EQUIVALENT) |
| → divergent | **22** = 16 deterministas + 6 semánticos | EQUIVALENCE-DECISIONS §1/§2 + razones durables |
| exact duplicates | **1** | stage row |
| semantic reviews live (llamadas) | **17** | 17 filas journal `claims.equivalence_review` (17 VALIDATED) — 11 EQUIVALENT / 6 DIVERGENT |
| re-verdictos content-addressed (sin llamada) | **4** (w0086, w0119 aplicados; w0118, w0122 en ventanas luego rechazadas) | EQUIVALENCE-DECISIONS §contadores |
| adjudicaciones totales | **21** = 17 live + 4 re-verdictos | ídem |
| **acumulaciones decididas** | **15** semantic-equivalent (veredicto EQUIVALENT) | ídem |
| **acumulaciones aplicadas** | **12** evidence unions + **12** provenance unions | uniones canónicas verificadas (ver tabla siguiente) |
| **records acumulados** | **7** | `record_stages` EVIDENCE_ACCUMULATED = 7 filas (una por record: append-only guarda sólo el primer merge) + accumulation-audit |
| relation accumulations aplicadas | **0** | handoff + ausencia de stages |
| merges decididos no aplicados | **3** (pertenecían a ventanas rechazadas por otra colisión: #15 w0122, re-verdictos w0118/w0122) — atomicidad whole-window | EQUIVALENCE-DECISIONS §contadores |

Uniones aplicadas por record (verificadas contra `pipeline_records`): `cl-grafica-eurusd` 1 merge/2 refs · `cl-grafico-eurusd` 5/10 · `cl-instrumento-eurusd` 2/5 · `cl-instrumento-grafico-eurusd` 1/2 · `cl-stop-loss-long-debajo-turtle-soup` 1/3 · `cl-temporalidad-grafico-15m` 1/3 · `cl-temporalidad-grafico-8h` 1/3 → **12 aplicaciones sobre 7 records**. El 7 de `METRICS.json.identity` cuenta records (stage rows), no aplicaciones (ver ERRATA E-02).

Clasificación humana del operador sobre las 17 live: 12 OBVIOUSLY_EQUIVALENT / 3 AMBIGUOUS / 2 OBVIOUSLY_DIVERGENT · `POTENTIAL_FALSE_SEMANTIC_MERGE = NO` · 1 sobre-rechazo conservador (#8, humano OBVIOUSLY_EQUIVALENT → engine DIVERGENT, costo de cobertura de w0094). Para política: el hotspot determinista es parameter-vs-observation sobre el mismo hecho visual recurrente (EURUSD/temporalidad), 12 de las 16 divergencias deterministas; 2 son epistemic (w0058, w0059) y 2 estructurales de relations (w0054, w0092).

## 6. Reliability (contadores separados, no un solo "failure")

| Clase | N | Autoridad física |
|---|---|---|
| Fatales que mataron el run (reconstruction) | **2** | w0057 y w0093, `parse-structured [fatal]: assistant content is empty` — durables en snapshots `run-fatal-w0057-snapshot/run.db` y `run.db.after-w0093-fatal` (status RUNNING al crash); recuperados por crash/resume contractual; re-invocadas live y VALIDATED (por eso no quedan filas fatal en el journal final) |
| Transport failure de composition (no mata el run) | **1** | fila journal `sko.composition` con `read-body [retry-exhausted]: retry budget of 2 exhausted` |
| Fatal de parse en grounding (sólo 1 record) | **1** | fila journal `claims.grounding_review` fatal → `cl-rango-rectangular-vertical` REVIEW_UNAVAILABLE |
| Correctivos de grounding (respuesta inicial malformada, reissue OK) | **115** | 115 filas REJECTED + reissue VALIDATED (1048 = 932 VALIDATED + 115 REJECTED + 1 fatal) |
| Ventanas con bad evidence refs | **4** (3.1%) | journal REJECTED (refs inventadas dentro del response_json) |
| Ventanas con JSON malformado | **0** | ídem |
| CLASS_FATAL (corrupción/clase contractual) | **0** en run final; los 2 fatales de provider son la clase transiente del backend, no ClassFatal | `class_fatal` counter |

`HANDOFF.PROVIDER_TRANSPORT_FAILURES = 3` agrupa (2 fatales de reconstruction + 1 read-body de composition); `HANDOFF.CLASS_FATAL = 2` cuenta sólo los run-killing. Ambos quedan subsumidos por esta tabla de 3 clases + correctivos (ver ERRATA E-06).

## 7. Lenguaje (verificación física final)

| Valor | Claims |
|---|---|
| español | **803** |
| inglés | **0** |
| otro | **0** |

Método único y documentado: inspección física de los 803 statements de claims.jsonl. 796 contienen marcadores españoles (tildes o palabras funcionales); los 7 restantes (`cl-current-range-is-pending`, `cl-este-rango-sigue-operativo`, `cl-euro-puede-llegar-arriba`, `cl-puedo-buscar-muchos-ejemplos`, `cl-rango-pendiente-nombre`, `cl-rango-reiniciado-nombre`, `cl-rangos-bajistas-otra-vez`) fueron inspeccionados uno a uno: son español sin tildes («Este rango se llama «rango pendiente».», «Puedo buscar muchos ejemplos.», …); uno contiene «bearish», loanword del propio instructor presente verbatim en el transcript (asr-00067). Cero statements en inglés. No se infirió lenguaje desde IDs.

El `language: {es: 796, other: 7}` de METRICS.json es salida de una heurística derivada (`lang_of` en analyze_run.py: empate de marcadores ES/EN → "other") y queda desautorizado como reporting (ERRATA E-01).

## 8. Runtime — llamadas / tokens / wall / budget

| Métrica | Valor | Nota de reconciliación |
|---|---|---|
| Filas de journal | **1196** | 130 recon + 17 equivalence + 1048 grounding + 1 composition |
| Llamadas cobradas (consumed) | **1194** | ledger consumed; = 1196 filas − 2 filas de error sin cargo (grounding fatal, composition transport) |
| Ledger tocado (consumed + released) | **1198** calls / **1960** images / 8,600,403 tokens | released = 4 reservas huérfanas de los 2 crashes (calls) + 19 (images) |
| Línea durable de budget (documentation.md) | vlm_call 1194/2400 · vlm_image 1941/8000 · vlm_token 8,600,403/60,000,000 | línea canónica; coinciden los tres | 
| Tokens | **8,600,403** = 6,293,102 prompt + 2,307,301 completion | suma re-calculada desde `usage_json` de las 1194 filas con usage |
| Costo reportado | **null** | el adapter no expone costo; no se inventa |
| Wall de cómputo | **9h27m17s** = 2:28:31 + 2:27:46 + 4:31:00 | 3 tramos; first invocation 20:50:01Z, last 06:05:23Z |
| Omissions de budget | **0** | ningún BUDGET_EXHAUSTED |

Los cuatro contadores de llamadas (1196/1194/1198/1194) miden cosas distintas (filas de journal vs cobradas vs tocadas por el ledger vs línea de documentación) — legítimamente diferentes, ver ERRATA E-07.

## 9. L2 — fallo exacto

```text
L2_REACHED = NO
SKOs canónicos = 0 (skos.jsonl: header con sko_count 0)
Intentos de composition = 1 (no hubo reintento manual; comportamiento contractual)
Razón durable (status_reasons):
  L2 composition unavailable: vlm provider read-body [retry-exhausted]:
  retry budget of 2 exhausted; last failure: response body read failed
```

Es la 2.ª vez en 3 corridas live (el stress gate sí alcanzó L2 → transiente de backend, no defecto determinista del código).

## 10. Gates vigentes (sin cambios; la decisión es del Owner)

```text
FULL_CHAPTER_EXECUTION          = TECHNICALLY_USEFUL
IDENTITY_REMEDIATION_AT_SCALE   = PASS
LIVE_ACCUMULATION               = PASS   (12 aplicaciones / 7 records, auditoría física)
WHOLE_WINDOW_ATOMICITY          = PASS   (0 residuo en 26 ventanas rechazadas)
REPLAY                          = PASS   (outcome idéntico; deltas enumerados en RUN.md)

L1_OWNER_REVIEW_READY           = YES
L2_CHAPTER_RESULT               = FAIL_UNAVAILABLE
CHAPTER_01_ACCEPTED             = PENDING_OWNER_REVIEW
READY_TO_SCALE_CORPUS           = NO
```
