# P4 — IMPLEMENTATION REPORT

**Base:** `ef53530` → **HEAD candidato:** `2afdb6c` (5 commits FF sobre `feature/v2-layered-knowledge-model`, sin push).
**Reportado por:** Primary Manager (verificación física de la implementación del worker; el worker completó los 5 commits + config antes de agotar su ventana; este reporte consolida la evidencia verificada directamente contra el repo).

## Commits (en orden)

| SHA | Commit | Cubre |
|---|---|---|
| `6dec7e5` | fix(providers): classify empty assistant content as retryable (R-B01) | B-01 |
| `584034c` | feat(v2): decouple composition attempt timeout into composition_timeout_seconds (R-B02) | B-02 |
| `ef0e594` | feat(v2): harden claims reconstruction prompt to mke.claims-recon.v3 (R-M03/M02/M01/M04) | M-03, M-02, M-01(recon), M-04 |
| `a7cf608` | feat(claims): calibrate grounding reviewer prompt to mke.claims-ground.v2 (R-M01) | M-01(reviewer), MI-01 |
| `2afdb6c` | fix(v2): preserve the original rejection category across resume (R-MI04) | MI-04 |

Diff total: 12 archivos, +444/−16. Scope check: sólo los archivos autorizados en P3 (`openrouter.go`, `v2.go`, `v2_sko_stages.go`, `v2_stages.go`, `claims/review.go`, `claims/records.go`, `runstate/pipeline.go` + tests + config). Sin guardas tocadas, sin L0/V1/benchmark golden.

## Evidencia por remediación

**R-B01** — `parseChatResponse` ahora clasifica `TrimSpace(content)==""` como `ClassRetryable Op=parse` con rationale de familia transiente (idéntico al caso hermano sin-choices); contenido presente pero malformado sigue `ClassFatal`. Tests nuevos: `TestEmptyContentIsRetriedAndRecovers` (vacío → retry → éxito), `TestPersistentEmptyContentSurfacesRetryExhausted` (vacío persistente → retry-exhausted, no fatal), `TestEmptyContentClassificationBoundaries` (malformado sigue fatal). Red-green: la clasificación previa era fatal (P1 lo verificó en producción).

**R-B02** — `CompositionTimeoutSeconds` nuevo en config v2 (validación: negativo rechazado, omitempty válido), `compositionTimeoutSecondsV2()` selecciona campo>0 si no fallback al timeout del pipeline (600s); sólo la llamada de composition lo usa (composition review/equivalence/grounding quedan en 120s). Tests: `TestV2ConfigAcceptsCompositionTimeout`, `...WithoutFieldStaysValid`, `...RejectsNegativeCompositionTimeout`, `TestV2CompositionTimeoutSelection`.

**R-M03/M02/M01/M04** — prompt `mke.claims-recon.v3` con las 6 reglas nuevas verificadas en el diff: (1) ids exactos sin rango/prefijo/otra ventana; (2) citación del segmento adyacente con deixis/antecedente/causa; (3) kind por contenido con estabilidad cross-window; (4) guía operativa de kind; (5) guía de epistemic (INSTRUCTOR_SAID si hay contraparte hablada); (6) niveles transcritos exactos, nunca niveles no mostrados.

**R-M01(reviewer)/MI-01** — `mke.claims-ground.v2`: calibración de garble-ASR↔término canónico con evidencia, resolución de deixis desde contexto citado, y ATOMIC vs COMPOSITE («una proposición con su razón enunciada es ATOMIC»).

**R-MI04** — `runstate/pipeline.go` + `v2_rejection_category_test.go`: la categoría contractual original de rechazo se preserva en re-validación cross-attempt (test `TestV2ResumePreservesOriginalRejectionCategory`).

## Verificación de suites (ejecutada por el Manager sobre HEAD `2afdb6c`)

- `go build ./...` → exit 0. `go vet ./...` → limpio.
- Paquetes tocados + resto: providers/... ok · pipeline ok (106.9s) · claims ok · sko ok · knowledge ok · runstate ok · benchmark ok (32.7s) · media ok (31.2s) · evidence ok (116.6s) · publish ok · provenance ok. **Suite completa verde.**

## Config de rerun (P7)

`config-rerun.v2.json` en este directorio: la config canónica del run (`configs/config.v2.json` @ ef53530) + `"composition_timeout_seconds": 600`. Prompts nuevos vía versiones contractuales (v3/v2) — sin cambio de esquema de config adicional.

## Desviaciones del diseño

Ninguna funcional. El corrective reissue opcional de R-M03 no se implementó (el diseño lo marcaba opcional-si-trivial; el worker optó por prompt-hardening puro — el gate de P6 lo validará con las 4 ventanas bad-ref).
