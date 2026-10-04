# R2 — IMPLEMENTATION REPORT · MKE V2 · Clutifx Chapter 01

**Fase:** R2 del remediation loop (implementa EXACTAMENTE el diseño R1; sin rediseño, sin expansión de alcance).
**Base:** `/home/kor/mke/multimodal-knowledge-engine`, branch `feature/v2-layered-knowledge-model`, arranque en `edec9a8` (verificado con `git log --oneline -3` al inicio: no aparecieron commits nuevos sobre el HEAD esperado; no hubo que rebasear).
**Salida:** 5 commits atómicos locales (NO pusheados a origin, según mandato). `git status` limpio salvo el directorio no rastreado `wt/` preexistente, que no toqué ni commiteé.

```
e7bc387 style(pipeline): gofmt alignment drift inherited from 584034c/edec9a8
87b1a92 fix(pipeline): fold and cap reconstruction corrective defect text (R-M06/R-1)
6b3770d feat(claims): harden claims reconstruction prompt to mke.claims-recon.v4 (R-M08/M09)
0937e76 feat(claims): calibrate grounding reviewer prompt to mke.claims-ground.v3 incl. relations (R-M07)
6932d12 fix(claims): tolerate declared v1/v2 grounding review schemas and @N suffix drift (R-M07)
```

---

## Pieza 1 — Tolerancia de formato del validador grounding (M-07a) · `6932d12`

**Archivos:** `internal/claims/review.go`, `internal/claims/review_tolerance_test.go` (nuevo, 144 líneas).

Implementado exactamente como el diseño §1.2:

1. **Schema-id: conjunto cerrado** `reviewSchemaAccepted = {ReviewSchema (v1), "mke.claims-ground.v2"}`; el gate `r.Schema != ReviewSchema` pasó a `!reviewSchemaAccepted[r.Schema]`. Sin matching por patrón; las variantes `mke-claims-ground-v1` y `mke.grounding.v1` quedan FUERA (documentado en el comentario del var). El payload (fields, enums, atomicity) se valida idéntico para ambos ids.
2. **Dirección:** helper puro `normalizeRecordAddress` (strips exactamente UN sufijo `@<dígitos>` via `strings.LastIndex` + `isAllDigits`) + `isAllDigits`. Gate: `normalizeRecordAddress(r.RecordID) != t.RecordID || r.Version != t.Version`. El mensaje de error preserva los valores RAW (`cl-x@1@1` → normaliza a `cl-x@1` → sigue rechazando; drift C nunca resuelve).
3. **Fail-closed intacto:** verdict fuera de enum, atomicity inválida/ausente en claims, atomicity presente en relations, version ≠ target, doble sufijo, drift, schema fuera del conjunto, datos tras el objeto JSON, `DisallowUnknownFields` — todo sigue rechazando.
4. **Identidad/replay:** fix parse-side; sin cambios en bytes de request → `RequestIdentity` estable. El camino del reissue (`ex.rejectInvocationV2` + `correctiveClaimReissue` en `v2_stages.go`) quedó intacto.

**Tests (`review_tolerance_test.go`):**
- `TestParseReviewResponseToleratesP7TerminalShapes`: los 9 record ids terminales del P7 + `cl-intraturtlesoup-open-pnl-label` (1.er intento) como fixtures REPRESENTATIVOS de las 3 familias de forma medidas por R1 (v2+`@1` dominante ×9, v2-clean, v1+`@1`) → todos parsean a `GROUNDING_SUPPORTED`+`ATOMIC` con binding al id desnudo. (Los fixtures EXACTOS del journal con invocation ids son AC1.1, ruta de verificación R3.)
- `TestParseReviewResponseToleranceStaysFailClosed`: 15 negativos (drift ×2, doble sufijo, sufijo no-dígito, `@1` desnudo, sufijo+version≠target, `mke-claims-ground-v1`, `mke.grounding.v1`, `mke.claims-ground.v3` futuro, verdict inválido, atomicity MAYBE/ausente en claim, atomicity en relation, trailing data, unknown field) con preservación de valor raw en mensaje.
- `TestReviewSchemaAcceptedIsClosedSet`: el conjunto es exactamente {v1,v2}, tamaño 2, sin variantes (AC1.3).
- `TestNormalizeRecordAddressStripsExactlyOneSuffix`: tabla de 9 casos del helper puro.

## Pieza 2 — Reviewer grounding prompt v3 (M-07b) · `0937e76`

**Archivos:** `internal/claims/review.go`, `internal/claims/records.go`, `internal/claims/records_test.go`.

1. **`PromptVersionGrounding` → `mke.claims-ground.v3`** (`records.go`), con comentario de versión que documenta el bump. `ReviewSchema` sigue congelado en `mke.claims-ground.v1` (el contrato de salida NO se mueve).
2. **Header des-anclado (viaja con este bump, diseño §1.2.3):** la línea del header ahora es `review_contract: claims.grounding_review calibration-3` (constante `groundingCalibrationSet`, sin ningún token con forma de schema id). `Request.PromptVersion` sigue siendo `mke.claims-ground.v3` (superficie de invalidación/fingerprint intacta; el override `ClaimsGroundingPromptVersion` no se tocó).
3. **Rama de RELATIONS — bloque de calibración nuevo** (el hallazgo estructural: las guías v2 sólo viajaban en claims y los 8 FN causales eran relations): guías Identity (identidad fonética «Felur Swing»=failure swing, «GIP»=GBP, «libra»=GBPUSD, «S&T»=SMT), Deixis/anáfora, y dependencia-enunciada («enacted as a definition, a conditional rule or a scenario… even without the literal words "depends on"») — texto verbatim del diseño §2.2a, insertado antes de «Do not use outside knowledge».
4. **Rama de CLAIMS:** guía garble v2 REEMPLAZADA por la guía Identity ampliada (fonética + frame/label + auto-cita); guía deixis v2 REEMPLAZADA por la guía Deixis ampliada (anáfora, «al final», «0100»/«10» ligados por el habla); guía causal/definicional NUEVA — texto verbatim del diseño §2.2b.
5. **Anti-rubber-stamp (bloque compartido, ambas ramas):** constante `groundingResolutionSafetyBlock` con las 2 líneas del diseño §2.2c (resolutions bind identity and reference ONLY; garbled form no licencia una proposición DIFERENTE), colocada antes de «Do not use outside knowledge» en ambas ramas.
6. **Few-shots REALES del P8:** viajan como los mini-ejemplos entre paréntesis dentro de las guías (sin bloque de ejemplos, per diseño — no inflar ~1400 reviews/run). `CorrectiveReviewRequest` hereda el base sin cambios propios.

**Tests:** probe `TestReviewRequestContractV2Guides` → `TestReviewRequestContractV3Guides` (records_test.go): pin v3 en ambas ramas; header des-anclado presente y sin token `vmke.claims-ground.`; guías identity/deixis en AMBAS ramas; guía de dependencia enunciada en relations; guía causal/definicional en claims; calibración ATOMIC (R-M01) retenida en claims; las 2 líneas anti-rubber-stamp presentes; la guía garble estrecha v2 ausente; rama relations sigue libre de atomicity.

## Pieza 3 — Recon prompt v4 (M-08+M-09) · `6b3770d`

**Archivos:** `internal/claims/records.go`, `internal/pipeline/v2_stages.go` (`buildClaimsReconstructionRequest`), `internal/pipeline/v2_identity_remediation_test.go`.

1. **`PromptVersionReconstruct` → `mke.claims-recon.v4`** (`records.go`), comentario de versión extendido (v4 = R-M08/M09).
2. **Regla (a) negaciones/excepciones** (diseño §3.2a, texto verbatim): insertada a continuación del bloque ATOMICITY (tras su bullet compañero «Never pack an independent exception…» — ambas bullets forman la regla ATOMICITY, y la regla nueva cierra citándola: «…per the ATOMICITY rule»). Declara negaciones/correcciones/excepciones como proposiciones de primera clase, con prohibición explícita de plegarlas u omitirlas.
3. **Regla (b) forward-references** (diseño §3.2b, texto verbatim): insertada inmediatamente tras la regla de citación de deixis («…cite that segment too»), con el filler puro («esto ya lo vamos a ver más adelante») quedando omitido.
4. **Regla (c) verificación de niveles por rol** (diseño §3.2c, texto verbatim): REEMPLAZA la línea v3 «Levels, targets, entries and stops shown on screen are transcribed exactly as labeled; never assign a proposition a level the cited evidence does not show or state for it.» (no coexisten; verificado por test negativo).

**Tests:** probes de `v2_identity_remediation_test.go` actualizados — `TestV2IdentityRequestContractPhysical` pinea v4, assertea las 3 reglas nuevas y que la regla de niveles v3 desapareció; `TestV2IdentityEquivalencePromptParticipatesInFingerprints` pinea v4. Las aserciones P4 existentes (R-M03/M02/M01/M04, incluida «transcribed exactly as labeled», que la regla nueva conserva) quedaron intactas y verdes.

## Mitigación R-1 (obligatoria, diseño §4.2 riesgo R-1) · `87b1a92`

**Archivos:** `internal/pipeline/v2_stages.go` (`correctiveReconstructionRequest`), `internal/pipeline/v2_recon_reissue_test.go` (solo función nueva añadida; los tests R-M06 existentes quedaron SIN modificar).

El defecto incrustado en el correctivo pasa de `firstDefect.Error()` verbatim a `providers.SanitizeDetail(foldRequestLine(firstDefect.Error()))` — plegado a una línea (provider data is never prompt structure) + cap 300 chars. Determinista (identidad del correctivo = función pura de request+defecto, estable tras crash/resume). Los defectos cortos de una línea viajan byte-idénticos (el contrato «nombra el defecto exacto» se conserva — verificado contra la aserción existente de `v2_reconstruction_reissue_test.go`).

**Test nuevo** `TestCorrectiveReconstructionRequestFoldsAndCapsDefect` (4 subtests): defecto corto verbatim; defecto multilínea plegado (una línea falsificada «Hard rules:» NO puede inyectarse como estructura); defecto >300 chars llega acotado (sin texto raw desbordado); identidad estable.

## Commit de higiene · `e7bc387`

`gofmt` bajo go1.27.1 señalaba 2 archivos preexistentes del paquete pipeline heredados de los commits base `584034c` (R-B02) y `edec9a8` (R-M06): `v2.go` y `v2_reconstruction_reissue_test.go` (alineación de comentarios en bloques const; solo whitespace, 2 líneas). Alineados en commit separado para que la verificación obligatoria quede limpia en los paquetes tocados. Los tests R-M05/R-M06 siguen verdes sin modificación semántica.

---

## Verificación (comandos + resultados)

| Comando | Resultado |
|---|---|
| `gofmt -l` sobre los 9 archivos del diff `edec9a8..HEAD` | limpio (exit 0) |
| `go vet ./internal/... ./cmd/...` | exit 0, sin output |
| `go test ./internal/claims/... -count=1 -timeout 30m` | **ok — 24 PASS / 0 FAIL** |
| `go test ./internal/pipeline/... -count=1 -timeout 30m` | **ok (101s) — 289 PASS / 0 FAIL / 1 SKIP** |
| `go test ./internal/sko/... -count=1 -timeout 30m` | **ok — 10 PASS / 0 FAIL** |
| R-M05/R-M06 (`TestV2Composition*`, `TestV2Reconstruction*`, `TestSKO*`, `TestCorrectiveReconstruction*`) | 12/12 PASS, archivos sin modificar (solo añadidos, nunca editados) |

El único SKIP es `TestV2PhysicalProvenanceTraceResolvesToSourceSHA` (requiere `MKE_V2_E2E_DIR`/`MKE_V2_E2E_MEDIA`, skip ambiental preexistente, sin relación con R2).

**Cobertura de los acceptance criteria asignables a R2:** AC1.2/1.3 (tabla negativa + conjunto cerrado), AC2.1 (probes v3 ambas ramas + anti-rubber-stamp + header des-anclado), AC3.1 (v4 pineado, reglas presentes, regla v3 reemplazada no coexistente), AC4.2-parcial R-1 (defecto plegado/acotado). AC1.1 (fixtures exactos del journal), AC1.4 (recorded-replay P7), AC2.2–2.4, AC3.2–3.4, AC4.1–4.3 son ruta R3 según el plan del diseño; AC*.5/6 son ruta R5/R6.

## Desviaciones del diseño

1. **Punto de inserción de la regla (a) de recon v4:** el diseño dice «insertar tras la regla ATOMICITY»; la inserté tras el bloque ATOMICITY completo (después de su bullet compañero «Never pack an independent exception…», antes de la regla de citación). La regla nueva cierra citando la ATOMICITY («…stays inside its claim, per the ATOMICITY rule»), por lo que leerse inmediatamente después del bloque completo es la lectura que mantiene la coherencia. Sin cambio de texto.
2. **Header de-anclado como constante** `groundingCalibrationSet = "calibration-3"` (el diseño especifica el renderizado exacto de la línea; la constante es solo el mecanismo Go para que probe y prompt compartan una única fuente).
3. **Commit de higiene gofmt extra (`e7bc387`)**, no previsto en el diseño: los 2 archivos con drift preexistente en el paquete pipeline (herencia de `584034c`/`edec9a8`) se alinearon para que el chequeo obligatorio de gofmt esté verde. Nota: `gofmt -l` bajo go1.27.1 sigue señalando ~23 archivos PREEXISTENTES de paquetes no tocados (`internal/media`, `internal/evidence`, `internal/runstate`, `cmd/mke`) por drift de toolchain — fuera de alcance de R2 (sería un reformat masivo); el check de R2 fue `gofmt -l` sobre los archivos del diff (limpio) + vet + tests.
4. **Test de los 9 terminales con fixtures representativos**, según la propia instrucción del brief (no el journal completo): 3 familias de forma documentadas por R1 cubriendo los 10 records; los fixtures exactos con invocation ids siguen siendo AC1.1 de R3.

Sin más desviaciones: los textos de prompt de las Piezas 2 y 3 y de la mitigación R-1 aterrizan verbatim del diseño.

```text
PHASE = R2
STATUS = IMPLEMENTATION_COMPLETE
BUNDLE = [P1 6932d12, P2 0937e76, P3 6b3770d, R-1 87b1a92, hygiene e7bc387]
NEXT = R3 adversarial (falsifica R-M05/R-M06 AC4.1-4.3; fixtures AC1.1/1.2, AC2.2-2.4, AC3.2-3.4; recorded-replay P7 → +10 exactos AC1.4) → R5 full rerun
```

---

## FEEDBACK (Agents-OS)

1. **Brief de implementación one-shot: excelento.** Rutas exactas (diseño, repo, branch, HEAD esperado) + verificación previa de `git log` + taxonomía de commits sugerida hicieron la sesión determinista: cero preguntas, cero ambigüedad. El patrón «texto completo de las líneas nuevas/cambiadas» del diseño R1 es EL habilitador: los prompts aterrizan byte-exactos sin interpretación.
2. **El enrutamiento de verificación por fase (R2/R3/R6) dentro de cada AC evitó scope creep:** saber que los fixtures exactos del journal son AC1.1-de-R3 mantuvo el test de R2 en fixtures representativos como pedía el brief. Sugerencia: conservar esta columna «Verificable por» en futuros diseños; es la que impide que el implementador absorba trabajo de la fase adversarial.
3. **Higiene de repo preexistente, sin dueño en el loop:** gofmt bajo go1.27.1 señala ~23 archivos preexistentes fuera de los paquetes de la campaña (media/evidence/runstate/cmd). Cada fase termina haciendo un chequeo de gofmt ambiguo («¿verde para mis archivos o para el repo?»). Sugerencia: un commit único de normalización gofmt por parte del owner FUERA de los commits de remediation, o fijar la versión de toolchain en el doc de campaña.
4. **N-10 se manifestó de nuevo, ahora como artefacto no rastreado:** encontré un directorio `wt/` sin rastrear en la raíz del repo al inicio de la sesión (no aparece en ningún brief; no lo toqué). Refuerza la sugerencia de R1 (ADOPTIONS.md): el estado del worktree (artefactos del owner, sin commit) debería vivir documentado en el vault, no solo en conversaciones.
5. **`sqlite3` CLI sigue ausente** (3.ª mención en la campaña): irrelevante para R2 (los tests usan la suite embebida), pero R3 necesitará extraer los fixtures exactos del `run.db` P7 — el patrón de lectura con Python ya quedó documentado por R1/GROUNDING-AUDIT; reiterar el dump `provider_invocations.jsonl` junto al run ahorraría ese paso.
6. **Bootstrap/startup:** sesión subagente one-shot con entradas obligatorias explícitas; no hizo falta routing del vault más allá de las rutas dadas. La estructura del brief (Entradas/Entregables/Verificación/Commits/Salida) funcionó como contrato completo de sesión.
