# AUDIT FORENSE — FALLA L2 SKO COMPOSITION (clutifx ch01, run live 2026-10-01/02)

Producto auditado: HEAD `ef53530756a27009517030a1bd29f0472bb3ad48` (branch `feature/v2-layered-knowledge-model`), adapter `openrouter`, modelo `stealth/space-bunny-alpha`.
Alcance: sólo medición y clasificación de causa raíz con evidencia. Sin decisiones de diseño, sin patches.
Fuentes: `fixtures/l2-composition.json`, journal `run-live/run.db` (snapshots `run.db.after-w0093-fatal`), logs `logs/run-resume2.log`, código `~/mke/multimodal-knowledge-engine/internal/` a HEAD ef53530.

## 1. El request (medición física)

Del fixture `l2-composition.json` (snapshot de la invocación crash-eada):

| Métrica | Valor |
|---|---|
| `request_bytes` (body HTTP real) | **121.155 bytes** |
| JSON del request completo (fixture) | 122.243 bytes |
| `system` | **119.988 chars / 120.741 bytes UTF-8** |
| `text_parts` | 1 part: `"Compose the knowledge objects."` (31 chars) |
| `image_ids` | null (request sólo texto) |
| `task` / `prompt_version` / schema | `sko.composition` / `mke.sko-compose.v1` / `mke.sko.v1` |

Composición del catálogo (conteo por regex sobre el `system`, estructura verificada contra `renderClaimCatalog`, `internal/pipeline/v2_sko_stages.go:120-131`):

- **741 claims** (líneas `- claim …`, promedio 136 chars c/u) — campos por entrada: `id@version`, `kind`, `epistemic`, `statement` (folded a una línea).
- **112 relations** (líneas `- relation …`, promedio 150 chars c/u) — campos: `id@version`, `type`, `subject_id@version`, `object_id@version`.
- **Total catálogo: 853 registros ≈ 117,6k chars** del system; el resto (~2,4k chars) es el contrato de tarea + hard rules (`BuildCompositionRequest`, `internal/sko/review.go:29-76`).
- El catálogo proviene del L1 final del run: 853 supported records (= "853 supported" del log de fin; 933 records totales menos 80 non-supported).

Estimación de tokens del request (método: cota chars/4 sobre UTF-8, apropiada para prosa española con tokenizadores tipo BPE, típicamente 3,5–4 chars/token):

- System: 119.988 / 4 ≈ **30,0k tokens**.
- Body completo: 121.155 / 4 ≈ **30,3k tokens** (cota superior).

Gate de catálogo: NO intervino. `CompositionCatalogLimit` no está declarado en `configs/config.v2.json` (sólo `schema` + `review_timeout_seconds: 120`) → `catalogLimitOrUnlimited()` devuelve nil (`internal/pipeline/v2.go:133-136`) → el boundary de `v2_sko_stages.go:55-63` no se activó y la composición se intentó con los 853 registros sin truncamiento.

## 2. El response (estado exacto)

Del fixture y del journal (`provider_invocations`, fila `ecae03753f944…`, `target=sko-composition`):

- `error_class`: **`retry-exhausted`**; `error_detail`: `vlm provider read-body [retry-exhausted]: retry budget of 2 exhausted; last failure: response body read failed`.
- `response_state`: vacío (nunca se persistió respuesta); `response_bytes`: **0**; `usage_json`: **vacío** (nunca llegó a parsearse usage); `model`: vacío.
- **No hay body capturado, ni parcial**: el adapter hace `io.ReadAll` y, ante error, descarta los bytes parciales y retorna error (`internal/providers/openrouter/openrouter.go:256-259`). Lo único que se sabe del HTTP es que **los headers sí llegaron** (`httpResp, err := a.cfg.HTTP.Do(...)` no falló; si hubiera fallado, el op habría sido `transport`, no `read-body`). El status code nunca se examinó (la lectura del body precede al check de status, `openrouter.go:256-262`).
- Razón durable en el run: `documentation.md:48` y `pipeline_state.status_reasons` → `L2 composition unavailable: vlm provider read-body [retry-exhausted]: retry budget of 2 exhausted; last failure: response body read failed`. Resultado: 0 SKOs (`run-live/skos.jsonl` = header con `sko_count:0`), run terminó INCOMPLETE exit 4 a las 2026-10-02T06:14Z.

## 3. Cronometría — el hallazgo central

Timestamps del journal (todos UTC):

| Evento | at_utc |
|---|---|
| Último settle de grounding review previo (re-issue correctivo de `rel-visita-sitio-requiere-url-mostrada`, VALIDATED) | 06:05:23.687988419Z |
| Entrada a `invokeV2` de composition (`at := ex.atUTC()` en `v2_stages.go:92`; ese mismo `at` queda en la fila del ledger y en la fila de invocación fallida) | **06:05:23.794024749Z** |
| Primera escritura durable posterior al fallo (primer `record_outcomes` del finalize) | **06:11:25.715772636Z** |

Duración observada dentro de `Infer`: 06:11:25.716 − 06:05:23.794 = **361,92 s**.

Predicción del código para 3 intentos que agotan íntegros su timeout por intento: 3 × 120 s + backoff 0,5 s + 1,0 s = **361,5 s** (+ ~0,4 s de overhead HTTP por intento). Match dentro de 0,42 s.

- El timeout por intento de composition es `Limits.Timeout = 120 s`: `BuildCompositionRequest` recibe `reviewTimeoutSecondsV2()` = `Config.ReviewTimeoutSeconds` = **120** (`config.v2.json: review_timeout_seconds`), con fallback `DefaultReviewTimeout = 60 s` (`internal/knowledge/grounding.go:187-188`) que no aplicó.
- El `--timeout 600` del pipeline NO aplica a composition: ese flag alimenta `opts.Timeout`, que sólo usan los requests de reconstruction (`v2_stages.go:854-857`). El deadline global de 600 s de pipeline nunca intervino (el run siguió ~9 min más tras el fallo y terminó exit 4, no por timeout).

## 4. Qué hizo el adapter (semántica de retry)

`Infer` (`internal/providers/openrouter/openrouter.go:143-172`):

1. Reintenta **sólo** errores `ClassRetryable` (línea 159). La falla `read-body` es `ClassRetryable` (`openrouter.go:256-259`: `Op: "read-body", Detail: "response body read failed"`), así que se reintentó.
2. Budget: `DefaultMaxRetry = 2` (`openrouter.go:46`) = 2 reintentos adicionales tras el primer intento → **3 intentos HTTP totales**.
3. Backoff: `DefaultBackoff` lineal capped (`openrouter.go:72-78`): intento 0 espera 500 ms, intento 1 espera 1 s (nunca llegó al cap de 5 s).
4. Al agotar: `ClassRetryExhausted` con el detalle exacto observado (`openrouter.go:162-168`: `retry budget of %d exhausted; last failure: %s`).
5. Contexto por intento: cada intento corre con su propio `context.WithTimeout(ctx, 120 s)` (`openrouter.go:151-153`). Un deadline que explota **durante** `Do` se clasifica `transport / "request timed out"` (`classifyTransport`, `openrouter.go:278-287`), pero un deadline que explota **durante la lectura del body** cae en el path de `io.ReadAll` y se reporta como `read-body / "response body read failed"` — el código no distingue deadline de conexión rota en ese path.

Por qué terminó `composition_unavailable` y no fatal: `composeSKOs` (`v2_sko_stages.go:72-82`) hace UNA invocación; si el error es `ClassFatal` retorna y mata el run; para cualquier otra clase (`retry-exhausted` incluida) hace `ex.reasons += "L2 composition unavailable: …"`, `ex.compositionUnavailable = true` y `return nil` — el run continúa hacia INCOMPLETE honesto. Contrato, no accidente.

## 5. Clasificación de causa raíz

**Primaria: timeout por intento insuficiente para el tamaño de generación del request (request/response-size related + timeout), reportado a través de la clase de transporte `read-body`.**

Evidencia que lo sostiene:

1. Los 3 intentos consumieron exactamente su deadline de 120 s (361,92 s observados ≈ 361,5 s teóricos; desviación 0,12%). Una falla puramente transiente de red (RST, truncamiento) no produce 3/3 intentos con duración idéntica al deadline.
2. Con headers recibidos y body inconcluso a los 120 s, el backend había aceptado el request (no hay 4xx; el path de rechazo por tamaño habría clasificado fatal `http`, `openrouter.go:309-327`).
3. El mismo backend, en el mismo run, generó completions de magnitud comparable SÓLO bajo el timeout de 600 s de reconstruction: w0057 = 23.426 prompt + 14.688 completion tokens (journal, `usage_json`), w0093 = 23.517 + 18.002 tokens; la recon de w0093 en resume #2 demoró del orden de 10 min (invocada ~01:50Z, VALIDATED 01:57:05Z). Una composición sobre 741 claims tiene salida esperada de esa misma escala (un componente por claim usado) — no era completable en 120 s a la throughput observada.
4. El request se subió rápido (121 KB) y el ciclo completo de 3 intentos + backoff cabe en los 361,9 s observados; no hubo espera muerta adicional.

Lo que NO se puede afirmar con la evidencia capturada (0 bytes de body): si a los 120 s el backend seguía generando (lo más parsimonioso, dado el punto 3) o estaba colgado. Ambos sub-casos producen el mismo registro `read-body`.

Contribuciones del adapter/config (conducta, no causa disparadora): reintentar el request idéntico (temperature 0, `openrouter.go:388`) sin adaptación ×3 multiplicó el costo en tiempo sin cambiar el resultado; el deadline de composition comparte el valor de review (120 s) en vez del timeout de reconstruction (600 s); el catálogo sin límite permitió un request de ~30k tokens de una pieza.

Veredicto en una línea: **causa raíz = per-attempt timeout (120 s) estructuralmente insuficiente para generar la salida de un catálogo de 853 registros, enmascarado como falla de transporte `read-body` por la clasificación del adapter; no fue transitorio puro, no fue rechazo por tamaño, no fue el timeout de 600 s del pipeline.**

## 6. Budget / conteo de intentos

- Intentos lógicos de composition en todo el run (3 tramos): **1** (una sola fila `sko.composition` en el journal; `composeSKOs` no tiene loop de stage).
- Intentos HTTP dentro de esa invocación: 3 (1 + 2 retries, budget `MaxRetries=2`), todos con el request byte-idéntico.
- Después del `retry-exhausted`, el stage NO se reintentó: `compositionUnavailable=true` y el pipeline siguió a INCOMPLETE (exit 4, salida durable parcial, 0 SKOs).
- Qué habría requerido un retry operacional: re-lanzar el mismo comando sobre `--out run-live`; `allocatePipelineRunDirV2` (`internal/pipeline/v2.go:402-440`) adopta el directorio sólo si `status=RUNNING` + mismo config fingerprint — tras exit 4 el estado es `INCOMPLETE`, así que un resume adicional habría sido rechazado por el contrato de adopción (habría requerido intervención operativa sobre el estado o un out-dir nuevo; no se hizo: el mandato aceptó INCOMPLETE). La fila de la invocación quedó con `response_state` vacío, de modo que un reintento en condiciones habría re-invocado el request idéntico (content-addressed, `RequestIdentity`, `internal/providers/providers.go:122-143`) por el default branch de `invokeV2`.

## 7. Anexo: trazabilidad de cifras

- Fixture: `p1-audit/fixtures/l2-composition.json` (`request_bytes=121155`, `response_bytes=0`, `error_class=retry-exhausted`, `at_utc=2026-10-02T06:05:23.794024749Z`).
- Journal final: `~/mke/clutifx-ch01-full-live-20261001/run-live/run.db`, `provider_invocations` fila `ecae0375…` (1 fila, `error_class='retry-exhausted'`, `usage_json=''`, `length(request_json)=121155`).
- Timing: `budget_ledger` fila release `06:05:23.794024749Z`; primer `record_outcomes` post-fallo `06:11:25.715772636Z` (933 filas de outcomes escritas entre 06:11:25.7 y 06:14:13.3).
- Config: `~/mke/clutifx-ch01-full-live-20261001/configs/config.v2.json` (`review_timeout_seconds: 120`, sin `composition_catalog_limit`); `--timeout 600` en `logs/run-resume2.log` (comando `time -v`).
- Salida: `run-live/skos.jsonl` (`sko_count:0`), `run-live/documentation.md:48` (reason) y `:131` (ladder: 1039 claims + 168 relations proposed, 22 windows rejected).
