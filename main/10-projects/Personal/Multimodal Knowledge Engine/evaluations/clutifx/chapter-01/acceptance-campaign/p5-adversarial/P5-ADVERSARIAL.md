# P5 — ADVERSARIAL REVIEW OF P4 REMEDIATION

**Reviewer:** adversarial independiente (contexto fresco, sin relación con el implementador).
**Objeto:** remediación P4 (`ef53530..2afdb6c`, 5 commits) contra el diseño `../p3-design/P3-REMEDIATION-DESIGN.md` y el reporte `../p4-implementation/P4-IMPLEMENTATION-REPORT.md`.
**Método:** verificación física de todo (nada se aceptó por reportado): lectura hunk-por-hunk de las 20 hunks del diff, ejecución propia de suites, y harness adversarial propio en `/tmp` (overlay `go test -overlay`, nunca escrito dentro del repo).

```
REMEDIATION_ADVERSARIAL = FINDINGS
READY_FOR_LIVE_GATES = YES   (condicionado a F-1; el path de gates P6/P7 usa config-rerun.v2.json que fija el campo)
```

---

## 1. Verificación de baseline

| Check | Comando | Resultado |
|---|---|---|
| HEAD | `git rev-parse HEAD` | `2afdb6cef3ab77dc81665fdeddf20502e6e94cc7` |
| Branch | `git branch --show-current` | `feature/v2-layered-knowledge-model` |
| Commits | `git log --oneline ef53530..HEAD` | 5 commits (6dec7e5, 584034c, ef0e594, a7cf608, 2afdb6c), FF sobre ef53530 |
| Tree | `git status --short` | sólo `?? wt/` (untracked, NO tocado en toda la sesión) |
| Diff | `git diff --stat ef53530..2afdb6c` | 12 archivos, +444/−16 — coincide con el reporte P4 |

## 2. Suites ejecutadas por el reviewer (resultado real)

| Suite | Comando | Resultado |
|---|---|---|
| Build | `go build ./...` | **exit 0** |
| Vet | `go vet ./...` | **exit 0, limpio** |
| Test completo | `go clean -testcache && go test -count=1 ./...` | **exit 0, 20/20 paquetes ok con caché forzada fresca** (cmd/mke 63.3s, benchmark 36.2s, evidence 121.2s, pipeline 111.4s, media 34.7s, providers/…, claims, runstate, sko, publish, provenance, knowledge) |

Nota: la primera pasada (`go test ./...`) salió mayormente `(cached)`; se repitió con `-count=1` tras `go clean -testcache` para que el verde sea evidencia propia.

## 3. Hallazgos

### F-1 — MAJOR (R-B02): config legacy sin el campo nuevo achica el budget de composition por debajo del pre-remediación; el comentario del commit es factualmente falso

**Repro (cadena verificada físicamente):**

1. Código viejo @ ef53530 (`git show ef53530:internal/pipeline/v2_sko_stages.go`, línea 70):
   `req := sko.BuildCompositionRequest(renderClaimCatalog(...), ex.reviewTimeoutSecondsV2())` — el intento de composition heredaba `review_timeout_seconds` (fallback interno `knowledge.DefaultReviewTimeout = 60s`, `internal/knowledge/grounding.go:187`).
2. Código nuevo @ 2afdb6c (`internal/pipeline/v2_stages.go:1237-1251`): sin `composition_timeout_seconds`, el fallback es `ex.opts.Timeout` (= flag `--timeout`, default **60**, `cmd/mke/pipeline.go:100`; 0 en librería → `DefaultTimeout` 60s).
3. El propio test del implementador `TestV2CompositionTimeoutSelection` (segundo caso) fija este comportamiento: field unset → composition = `opts.Timeout`.

**Efecto:** config legacy con `review_timeout_seconds: 120` y `--timeout` default 60 → el intento de composition pasa de **120s (pre-P4) a 60s (post-P4)**: MÁS apretado exactamente en la etapa cuyo BLOCKER (B-02) era timeout por payload creciente. El comentario en `v2.go:66-70` y el mensaje de commit afirman que el fallback "`is what every legacy document without this field already exercised`" — **falso**: legacy ejercía `review_timeout_seconds`, no `opts.Timeout`.

**Mitigaciones verificadas:** el gated rerun usa `config-rerun.v2.json` con `"composition_timeout_seconds": 600` (verificado en `../p4-implementation/config-rerun.v2.json`) → el path de gates NO está afectado. El diseño P3 especificó este fallback ("si no `ex.opts.Timeout`"), así que el implementador fue design-conformante: el defecto es de la premisa del diseño + la justificación falsa del comentario, no de fidelidad de implementación.

**Clasificación:** MAJOR (vector de regresión real para despliegues no migrados, en la superficie del BLOCKER; requiere migrar configs o documentar que `composition_timeout_seconds` es obligatorio en producción).

### F-2 — MINOR (R-B01): exposición residual — `content` como array de partes sigue siendo FATAL

**Repro físico** (harness overlay en `/tmp/p5adv/zz_p5_adversarial_test.go`, ejecutado con `go test -count=1 -overlay /tmp/p5adv/overlay.json -run TestP5 ./internal/providers/openrouter/`):

```
array content -> class=fatal op=parse detail="response is not valid JSON"
```

El DTO de request reconoce "string or part array" (`openrouter.go:178`), pero el DTO de response declara `Content string` (`openrouter.go:211`): un backend que responde 200 con `content` en formato array de partes falla el unmarshal del body completo y es **fatal**, aunque sea la misma familia de anomalía transiente que B-01 remedió para el caso string-vacío. Pre-existente (no introducido por P4), fuera del shape exacto del defecto (string vacío), pero misma clase de riesgo run-killing. Queda documentado como deuda.

### F-3 — MINOR (gate de proceso): gate "coverage ≥95% en paquetes tocados" NO se cumple y el reporte P4 no lo menciona

Medición propia (`go test -count=1 -cover`) HEAD vs baseline ef53530 (clon en `/tmp/p5base`):

| Paquete | HEAD | ef53530 |
|---|---|---|
| providers/openrouter | 86.6% | 86.5% |
| claims | 68.0% | 68.0% |
| runstate | 92.6% | 93.4% (−0.8: rama de error "corrupt journal" de `MarkInvocationRejectedDetail` sin test directo en el paquete) |
| pipeline | 89.7% | (no medido en base; HEAD < 95%) |

El shortfall es pre-existente (no hay regresión material; la única caída es runstate −0.8pp por la rama de error nueva). Los caminos nuevos SÍ están cubiertos por los tests nuevos (verificados por lectura, §5). Pero el Gate 1 de P3 ("coverage ≥95% en paquetes tocados") está incumplido y el reporte P4 declara los gates sin mencionar esta métrica.

### F-4 — NOTE (R-B01): presupuesto — 1 VLMCall por invocación, no por attempt; los tokens de attempts fallidos no se contabilizan

Verificado físicamente (`TestP5RetryExhaustedCarriesUsageOfNothing`): 3 intentos HTTP → 1 reserva `BudgetVLMCall` en `invokeV2`; en fallo la reserva se libera (`ReleaseReservations`, `v2_stages.go:124-133`) y ningún token se registra (el `Response{}` cero descarta el usage de todos los attempts). Consecuencia: un backend persistentemente vacío quema intentos y wall-clock sin consumir budget (el budget no puede frenarlo), acotado por MaxRetries+1 intentos × #ventanas. Es la semántica pre-existente del caso hermano sin-choices, ahora extendida a empty-content: consistente, no una violación.

### F-5 — NOTE (R-B02): asimetría de fingerprint entre los dos timeouts

`ReviewTimeoutSeconds` participa del config/L1 fingerprint (`v2.go:150-193`); `CompositionTimeoutSeconds` está deliberadamente excluido (`fingerprintDoc` no lo incluye). Es defensable (parámetro de ejecución que no puede alterar respuestas committed; `RequestIdentity` nunca hashea `Limits.Timeout` — verificado `providers.go:122-139`), y habilita correctamente que `config-rerun.v2.json` adopte/resume con el campo añadido. Pero dos runs con budgets de composition distintos comparten fingerprint en artefactos de auditoría, tratamiento inconsistente con el campo hermano frozen.

### F-6 — NOTE (R-MI04): alcance de la preservación de categoría

La lectura de `error_detail` en resume sólo existe en el path de claims-reconstruction (`v2_stages.go:341-349`). Las demás superficies REJECTED en resume (grounding review `v2_stages.go:1124`, equivalence `:644`, composition review `v2_sko_stages.go:312`) siguen imprimiendo el placeholder genérico "rejected in a previous attempt" en las razones de reissue. La divergencia de identidad se preserva por otra vía (la invocación queda VALIDATED y el ladder determinista reproduce el `rejectCause` en `commitClaimCandidates` — verificado por lectura del flujo `reconstructClaimsWindow:388-395`). Fuera de la superficie adjudicada de MI-04 (window coverage), residual documentado.

### F-7 — NOTE (prompt v3): ambigüedad residual observation-vs-claim, sin contradicciones con reglas frozen

Leído el prompt completo @ HEAD (`v2_stages.go:855-873`). Verificado que NO hay contradicción: ATOMICITY, idioma fuente, EQUIVALENT_TO, epistemics prohibidos, relation-ids y no-invención están intactos byte-a-byte; ninguna regla nueva exige algo que el schema no exprese; la regla "cite every segment needed" es output-side (evidence_ids) y el request YA incluía todos los segmentos de la ventana (`windowSegments` loop, `v2_stages.go:841-845`) → **no hay inflación sin techo del prompt**. La frontera kind observation/claim sigue siendo juicio del modelo ("price movement" = observation vs "trading-content assertion" = claim); el ladder frozen fail-closed permanece como guardia (sin cambios en el diff).

### F-8 — NOTE (R-B02): peor caso wall-clock por invocación de composition ahora 3×600s

`Infer` reintenta hasta `MaxRetries` (loop en `openrouter.go`, attempts = MaxRetries+1) con el timeout por intento: 3×600s = 30 min por invocación antes de degradar a `composition_unavailable`. Acotado, pero conviene vigilarlo en P7 (ventanas con backend lento).

## 4. Ataques que NO rompieron la remediación (verificación positiva)

| Ataque | Verificación | Resultado |
|---|---|---|
| Exit codes / publicación (R-B01) | `errors.go:47-74`, `composeSKOs` (`v2_sko_stages.go:78-90`), `claimsReconstructionFailure` (`v2_stages.go:405-427`): retry-exhausted → fila de ventana UNAVAILABLE → run continúa → INCOMPLETE (exit 4); nada se publica; fatal (exit 5) sólo para malformado real | **Contract intacto** |
| "Convertir malformado en empty" | Harness físico: `json-null-word`/`json-string`/`json-array`/`truncated-json`/BOM-sólo → **fatal op=parse-structured**; sólo whitespace puro (tabs, espacios) → retryable (sin información, semántica honesta) | **No explotable** |
| `content: null` / ausente | Físico: JSON null unmarshals a string vacía → retryable (correcto: anomalía transiente) | OK |
| Op `parse` vs `parse-structured` rompe consumidores | `providerClassOf` usa sólo class; `SanitizeDetail` es agnóstico; contract tests no enumeran Op; exit mapping intacto; ningún consumidor de código del string de detail | **Sin ruptura** |
| Replay recorded con fixtures frozen diverge | `internal/providers/recorded`: fixtures guardan `Structured` ya parseado y los scripts construyen `providers.Error` directamente — **ninguno pasa por `parseChatResponse`**; no existe replay script en el repo con "assistant content is empty" (grep completo, único hit en `wt/` no tocado). El cambio sólo afecta el adapter live | **Determinismo de replay intacto** |
| Fingerprint/crash-resume adoption (R-B02) | `fingerprintDoc`/`L1Fingerprint`/`L2Fingerprint` no incluyen el campo (leído); el timeout no puede alterar respuestas committed; los bumps v3/v2 SÍ cambian el L1 fingerprint (invalidación contractual correcta vía constantes, `v2.go:477`) | **Sound** |
| Validación config 0/negativo | `Validate()` rechaza negativo, acepta 0 = fallback (comentado en `v2.go:65-70`); tests del implementador cubren los 3 casos | OK |
| Bump de versión incompleto | Grep de `claims-recon.v2`/`claims-ground.v1` en código/config/testdata: sólo quedan `ReviewSchema = "mke.claims-ground.v1"` (schema de salida frozen, intencional y comentado) y comentarios históricos; probes fijan v3/v2; benchmark/holdout sin pins hardcoded | **Completo** |
| Corrupción de journal (R-MI04) | `MarkInvocationRejectedDetail` exige exactamente 1 fila en (PERSISTED, REJECTED); 0 filas → "corrupt journal" → stickyFatal (fail-closed); journals pre-cambio caen al placeholder (migración documentada) | **Fail-closed** |
| Determinismo del detail re-grabado | Validador (`claims/records.go:315-327`): primer ref desconocido sobre bytes almacenados fijos + `dedupSorted` + `SanitizeDetail` → mismo texto en re-reject | **Determinista** |
| Guardas frozen (alcance) | 20 hunks enumerados y revisados uno a uno: cero cambios en ladder, atomicidad whole-window, fail-closed DIVERGENT, exit codes, L0/V1/benchmark golden | **Intactas** |

## 5. Auditoría de tests del implementador (¿vacuos?)

Ninguno resultó vacuo:

- `TestEmptyContentIsRetriedAndRecovers` / `TestPersistentEmptyContentSurfacesRetryExhausted`: httptest real con contador atómico de llamadas (asserts 2 y 3 llamadas exactas), wrap real de `ClassRetryExhausted` con causa retryable. Ejercita lo que dice.
- `TestEmptyContentClassificationBoundaries`: pin directo de `parseChatResponse` en los 3 bordes (vacío/whitespace retryable, malformado fatal).
- `TestV2CompositionTimeoutSelection`: pin físico de `Limits.Timeout` por task sobre un probe del executor, campo-set y fallback.
- `TestV2ResumePreservesOriginalRejectionCategory`: crash real en `FPAfterWindowInvocation:w1-theory` + resume + aserción doble sobre `claims/reconstruction.jsonl` (contiene `unknown evidence ref "seg-999"`, NO contiene el placeholder). No es vacuo; es el test más fuerte del set. Gap: no cubre la rama identidad-divergencia (se preserva por replay del ladder, F-6) ni la de error "corrupt journal" (F-3).
- `TestReviewRequestContractV2Guides` + probe v3 en `v2_identity_remediation_test.go`: fijan versión y presencia literal de las 8 reglas nuevas en el request.

## 6. Veredicto

```
REMEDIATION_ADVERSARIAL = FINDINGS
READY_FOR_LIVE_GATES = YES
```

Sin CRITICAL ni FAIL: el contrato de salida (exit codes, publicación bloqueada en UNAVAILABLE→INCOMPLETE, replay determinista, guardas frozen, fail-closed del journal) resiste todos los ataques físicos ejecutados, y los tests del implementador son sustantivos. **F-1 (MAJOR)** debe resolverse antes de cualquier despliegue que no sea el gated rerun: corregir el comentario falso (`v2.go:66-70`) y tratar `composition_timeout_seconds` como obligatorio en configs de producción (o restaurar el fallback a `review_timeout_seconds` cuando el campo esté ausente). F-2/F-3 son deuda aceptable documentada; los gates P6/P7 pueden correr con `config-rerun.v2.json` (que fija 600s).
