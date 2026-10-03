# AUDIT FORENSE — FATALES DE PROVIDER `assistant content is empty` (w0057, w0093; clutifx ch01)

Producto: HEAD `ef53530756a27009517030a1bd29f0472bb3ad48`, adapter `openrouter`, modelo `stealth/space-bunny-alpha`.
Alcance: evidencia + clasificación retryable-vs-fatal según la semántica existente + costo operacional del resume. Sin patches.
Fuentes: `fixtures/provider-fatals.json`, journals SQLite (`run-fatal-w0057-snapshot/run.db`, `run.db.after-w0093-fatal`, `run-live/run.db`), logs de `~/mke/clutifx-ch01-full-live-20261001/logs/`, `PROGRESS.md` del run, código `internal/` a HEAD.

## 1. Cronología del run (3 tramos, timestamps UTC)

| Tramo | Inicio | Fin | Salida | Evento |
|---|---|---|---|---|
| attempt-1 (live) | 20:42:19Z (`live-start.utc`) | ~23:10:50Z (2:28:31) | exit 5 | FATAL #1 w0057 @ 23:07:42.034937815Z |
| resume #1 | 23:14:18Z (`resume-start.utc`) | ~01:42:04Z (2:27:46) | exit 5 | FATAL #2 w0093 @ 2026-10-02T01:32:38.919034021Z |
| resume #2 (final) | 01:43:00Z (`resume2-start.utc`) | ~06:14:13Z (4:31:00) | exit 4 (INCOMPLETE) | w0057 re-invocada → VALIDATED 01:43:20Z; w0093 re-invocada → VALIDATED 01:57:05Z; luego L2 → retry-exhausted (ver L2-FAILURE-AUDIT.md) |

## 2. Evidencia por fatal

### FATAL #1 — w0057 (snapshot `attempt1-fatal-w0057`)

- `invocation_id`: `2164c633e51af722812a2e6b0d71507993eca7c1bc20d983fccebdb652098193` (content-addressed: sha256 sobre task + prompt_version + system + schema + text parts + hashes de imagen, `internal/providers/providers.go:122-143`).
- Request: `request_json` 5.408 chars / 5.411 bytes; `system` 4.699 chars; `text_parts` 1 × 24 chars (`"Reconstruct this window."`); **8 image_ids** (frames p72090000–p72720000, canonical-v1); task `claims.reconstruction`, prompt `mke.claims-recon.v2`, schema `mke.claims.v1`.
- Response: `response_json` **""** (vacío), `response_state` **""**, `usage_json` **""** — el backend devolvió 200 sin contenido de assistant; ni usage llegó a parsearse.
- `error_class` **fatal**; `error_detail` `vlm provider parse-structured [fatal]: assistant content is empty`; at_utc 2026-10-01T23:07:42.034937815Z.
- Log: `logs/run-live-fatal-w0057.log` — `claims reconstruction provider failed for window w0057: vlm provider parse-structured [fatal]: assistant content is empty`, exit status 5.
- Estado durable al fatal (snapshot `run-fatal-w0057-snapshot/run.db`): 57 recon invocations (53 VALIDATED, 3 REJECTED por output malformado, 1 fatal), 3 equivalence reviews. El proceso murió antes de escribir terminal state → `pipeline_state.status=RUNNING` (dato clave para la adopción, §5).

### FATAL #2 — w0093 (snapshot `attempt2-fatal-w0093`)

- `invocation_id`: `9e8fcc17dd3ae6e616c53be4f4da7a9734002ab5d94104f01d97e4a1ef6c6bad`.
- Request: 5.723 chars / 5.734 bytes; `system` 5.006 chars; text 24 chars; 8 frames (p127530000–p128160000); misma task/prompt/schema.
- Response: vacío en las tres casillas (response_json / response_state / usage_json), igual que #1.
- `error_class` fatal; mismo `error_detail`; at_utc 2026-10-02T01:32:38.919034021Z.
- Log: `logs/run-resume1-fatal-w0093.log`, exit 5.
- Estado durable al fatal (`run.db.after-w0093-fatal`): 93 recon rows (89 VALIDATED, 3 REJECTED, 1 fatal w0093), 8 equivalence reviews. Notar que la fila de w0057 ya estaba VALIDADA (éxito del resume #1) — el snapshot contiene exactamente 1 fila con error.

### Reintentos exitosos (run final)

Mismos `invocation_id` que los fatales (par 1-a-1 en `provider-fatals.json`): el reintento fue el request byte-idéntico, re-derivado por contenido.

- w0057 → `response_state=VALIDATED` @ 2026-10-02T01:43:20.561671227Z; usage `{"prompt_tokens":23426,"completion_tokens":14688,"total_tokens":38114}`; response_id `gen-1790896486-Jcih8dDuxD51lPql9r9j`.
- w0093 → `response_state=VALIDATED` @ 2026-10-02T01:57:05.91813034Z; usage `{"prompt_tokens":23517,"completion_tokens":18002,"total_tokens":41519}`; response_id `gen-1790906005-zzGh3LMFRWLcKLvuw2ie`.
- En `run-live/run.db` ambas filas quedaron con `error_class=''` (upsert de la misma invocation_id; `PutInvocation`). Con usage de 14,7k/18k completion tokens, cada reintento generó durante minutos: la llamada w0093 demoró ~6–10 min (VALIDATED 01:57:05Z, invocada tras el replay que terminó ~01:50Z).

## 3. Clasificación actual del adapter (código exacto)

La clase se decide en DOS puntos de `internal/providers/openrouter/openrouter.go`:

1. `extractJSONObject` (líneas 464-468): contenido vacío → `errors.New("assistant content is empty")` (el helper compartido equivalente es `internal/providers/extract.go:17-21`, con el contrato "must never become published knowledge" en líneas 13-16).
2. `parseChatResponse` (líneas 420-423): **cualquier** error de `extractJSONObject` (vacío, no-JSON, no-objeto) mapea a `&providers.Error{Class: providers.ClassFatal, Op: "parse-structured", Detail: err.Error()}`. Aquí es donde `assistant content is empty` se vuelve fatal — no hay distinción entre contenido ausente y contenido malformado.

Contraste interno del mismo archivo: un 200 **sin array de choices** se clasifica `ClassRetryable` con comentario explícito (líneas 404-417): "A 200 with no choices is, on a live proxy backend, a transient upstream anomaly, not a caller mistake: it provably recurs on a straight replay… it is classified retryable. After the bounded retry budget it surfaces as retry-exhausted and the caller keeps the honest durable partial output instead of losing the run."

Cadena que convierte la clase de provider en muerte del run:

3. `invokeV2` (`internal/pipeline/v2_stages.go:114-122`): persiste la invocación fallida (`error_class=fatal`, `response_state` vacío) y envuelve como `ClassIncomplete "provider invocation failed"`.
4. `reconstructClaimsWindow` → `claimsReconstructionFailure` (`v2_stages.go:335-341` y `388-395`): si `providerClassOf(cause) == providers.ClassFatal` → `return fatal("claims reconstruction provider failed for window %s: %v", …)` — error de pipeline `ClassFatal` que sube y termina el proceso.
5. Contrato de exit codes (`internal/pipeline/errors.go:10`): "0=complete, 2=invalid-input, 3=unsupported, 4=incomplete, 5=fatal, 6=retry-exhausted"; `ExitCode` (líneas 41-56) mapea ClassFatal → 5. Observado: exit 5 en ambos logs.

¿Reintentos en otra capa? **Ninguno.**

- No hay SDK HTTP: el adapter usa `net/http` directo (`openrouter.go:112, 251`); una respuesta 200 cuya lectura de body falla no tiene retry de transporte.
- El loop de `Infer` (líneas 151-171) reintenta sólo `ClassRetryable` (línea 159); un fatal retorna en el **primer** intento HTTP, sin backoff.
- A nivel de stage no hay loop: `reconstructClaims` itera ventanas (una invocación por ventana, `v2_stages.go:303-314`) y `claimsReconstructionFailure` eleva el fatal sin reintento. Balance: esta clase recibe exactamente 1 intento por proceso, siempre.

## 4. ¿Debía ser retryable según la semántica existente?

**Veredicto: sí, para la variante vacía (los 2 casos observados), la semántica existente del propio adapter la señala como retryable; la clase fatal es un efecto colateral de que `parse-structured` agrupa vacío y malformado en una sola categoría.** Evidencia:

1. **Precedente del propio adapter para contenido estructuralmente ausente**: el caso no-choices (200 sin choices) es `ClassRetryable` con el racional citado en §3-punto 2 — "transient upstream anomaly on a live proxy backend… provably recurs on a straight replay". `assistant content is empty` es la misma categoría sobre el mismo backend proxy (stealth model vía OpenRouter): 200 bien formado al que le falta el contenido. El código que separa ambas clases es exactamente `openrouter.go:404-417` (retryable) vs `openrouter.go:420-423` + `464-468` (fatal).
2. **Empíricamente transiente, verificado 2 veces**: 2 eventos en 132 llamadas de reconstruction (1,5%); no persistente — w0057 falló y su replay directo inmediato produjo 38.114 tokens VALIDATED; luego pasaron 36 ventanas más sin evento hasta w0093 (ritmo ~1 cada ~36 ventanas, `PROGRESS.md:47`); w0093 también sucumbió… no: también éxito en replay directo con 41.519 tokens. El criterio del adapter ("provably recurs on a straight replay") se cumplió en ambos casos con el request byte-idéntico (misma invocation_id, temperatura 0, `openrouter.go:388`).
3. **La seguridad que motiva lo fatal es de publicación, no de reintento**: el contrato de `extract.go:13-16` prohíbe que contenido malformado se publique; con clase retryable + budget 2, el peor caso termina `retry-exhausted` → rama default de `claimsReconstructionFailure` (`v2_stages.go:403-408`) → ventana UNAVAILABLE → run INCOMPLETE honesto. Nada se publica. La clase fatal no es necesaria para honrar ese contrato.
4. **El diseño durable ya trata estas filas como re-invocables**: la invocación fallida se persiste con `response_state` vacío y el resume la re-invoca por el default branch (`v2_stages.go:326-341` + `committedResponseV2` `v2_stages.go:165-179`, que sólo replay-ea estados no vacíos). El procedimiento de resume que efectivamente funcionó dos veces depende de que esta operación sea repetible.
5. **Inconsistencia entre stages del mismo run**: la misma familia de error en grounding review (`cl-rango-rectangular-vertical`, "assistant content is not a valid JSON object", fila `error_class=fatal` @ 05:08:00Z) NO mató el run — `strictClaimReview` mapea fallas de provider a outcome record-scoped `REVIEW_UNAVAILABLE` (`v2_stages.go:1093-1095` → `internal/claims/review.go:223-227`; durable en `record_outcomes` y `status_reasons`). Sólo reconstruction eleva esta familia a run-fatal (`v2_stages.go:393-395`).

Contra-punto registrado (por honestidad de la auditoría): la clase fatal de `parse-structured` también cubre contenido PRESENTE pero malformado (no-JSON / no-objeto), donde un replay determinista a temperatura 0 puede seguir fallando; defender fatal ahí es razonable. El defecto de clasificación observado es que el caso vacío viaja por el mismo camino sin distinción (`openrouter.go:420-423` no distingue los tres errores de `extractJSONObject`).

## 5. Costo operacional real del resume

**Adopción**: ambos resumes re-lanzaron el mismo comando con `--out run-live`; `allocatePipelineRunDirV2` (`internal/pipeline/v2.go:402-440`) adopta sólo un directorio con `status=RUNNING` + mismo `config_fingerprint` (contrato crash/resume; línea 434-437). Se cumplió: al fatal #1 el proceso murió sin escribir terminal state (status quedó RUNNING, `PROGRESS.md:40`); fingerprint constante `10418ccf…` en `pipeline_state` durante los 3 tramos.

**Replay sin nuevas llamadas (verificación por conteo de invocaciones):**

| Corte | recon rows | VALIDATED | REJECTED | fatal/pendiente | equivalence |
|---|---|---|---|---|---|
| fin attempt-1 | 57 | 53 | 3 (w0003, w0005, w0043) | 1 (w0057) | 3 |
| fin resume #1 | 93 | 89 | 3 | 1 (w0093) | 8 |
| final (run.db) | 130 | 126 | 4 (+w0110) | 0 | 17 |

- Las filas crecen SOLO por ventanas nunca intentadas (57 → 93 → 130); ningún window validado tiene una segunda fila: 130 filas para 130 ventanas. Las transiciones fatal→éxito fueron UPSERT de la misma `invocation_id`, no filas nuevas.
- Llamadas provider de reconstruction en total: **132 = 130 ventanas + exactamente 2 re-invocaciones** (w0057 en resume #1, w0093 en resume #2). Ninguna otra ventana se re-invocó jamás.
- Prueba de timing del replay: resume #2 arrancó 01:43:00Z y w0057 quedó revalidada a las 01:43:20.561671227Z — 92 ventanas replayeadas del journal en ~20 s (imposible con llamadas live: la propia w0057 generó 14.688 completion tokens ≈ minutos). El timestamp 01:43:20 es el refresh de `MarkInvocationState` sobre la fila VALIDADA por el replay (`internal/runstate/pipeline.go:289-305`), no una nueva llamada. En resume #1, igualmente, w0001-w0056 no se tocaron (0 filas nuevas) y sólo w0057 se re-invocó.
- Effecto del replay en resultados: replay no re-cobra budget (`invokeV2` `v2_stages.go:147`: "resume never re-charges committed budget") ni muta contenido (identidad content-addressed).

**Costo agregado de los 2 fatales:**

- Operativo: 2 resumes manuales del operador (cada uno = snapshot de evidencia + relanzamiento + monitoreo); replay de journal ≈ segundos-minutos por tramo.
- En llamadas: 2 llamadas perdidas (contenido vacío, sin usage capturado — costo de backend no observable en el journal).
- En wall-clock: attempt-1 perdió el tramo en curso (sólo la ventana w0057; el trabajo validado quedó durable) y el run completo se extendió por 3 tramos: 20:42:19Z → 06:14:13Z con 2 gaps de operación (~4 min y ~1 min entre logs .utc).
- Consumo total del run (3 tramos, ledger `state='consumed'`): **1.194 vlm calls / 1.941 images / 8.600.403 tokens** (límites: 2.400 / 8.000 / 60M — sin presión de budget).
- Resultado final: exit 4 INCOMPLETE con salida durable parcial (853 supported / 80 non-supported; `run-resume2.log`), 0 SKOs por la falla L2 aparte (documentada en L2-FAILURE-AUDIT.md).

## 6. Trazabilidad

- Fixture: `p1-audit/fixtures/provider-fatals.json` (4 snapshots; pares fatal/retry unidos por `invocation_id`).
- Journals: `~/mke/clutifx-ch01-full-live-20261001/run-fatal-w0057-snapshot/run.db` (fin attempt-1), `run.db.after-w0093-fatal` (fin resume #1), `run-live/run.db` (final).
- Logs: `run-live-fatal-w0057.log`, `run-resume1-fatal-w0093.log`, `run-resume2.log` + `*-start.utc`.
- Código: `internal/providers/openrouter/openrouter.go` (46-48, 72-78, 143-172, 251-263, 278-287, 399-423, 464-481), `internal/providers/extract.go` (13-21), `internal/pipeline/v2_stages.go` (82-122, 303-341, 388-409, 1093-1095), `internal/pipeline/errors.go` (10, 41-56), `internal/pipeline/v2.go` (402-440), `internal/runstate/pipeline.go` (289-305), `internal/providers/providers.go` (122-143).
- Bitácora del operador: `~/mke/clutifx-ch01-full-live-20261001/PROGRESS.md` (líneas 39-50).
