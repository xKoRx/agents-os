# R1 — REMEDIATION DESIGN · MKE V2 · Clutifx Chapter 01

**Fase:** R1 del remediation loop (entrada: P8 = FINDINGS, 3 gates congelados fallando: B-08 L2, M-07 FN, M-08 MISSING_MATERIAL; M-09 regression watch).
**Candidato base:** `/home/kor/mke/multimodal-knowledge-engine` HEAD `edec9a8` (contiene R-M05 `8ae543a` y R-M06 `edec9a8`, adoptados, NO pusheados; origin en `19b44c1`).
**Evidencia primaria:** run P7 `~/mke/clutifx-ch01-rerun-20261003/run-rerun/` (`run.db` 1618 invocations + `claims.jsonl` 1189 records + corpus P8 `../p8-final-audit/corpus/`), audits P8 (`../p8-final-audit/results/`).
**Método R1:** diseño ONE-SHOT, sin implementar. Todo número de este documento fue re-medido por R1 desde el journal durable (scripts reproducibles; `sqlite3` CLI no existe en el host — lectura con módulo `sqlite3` de Python).

**Contenido del bundle (4 piezas, 1 full rerun R5):**

| # | Pieza | Finding | Clase de fix | Archivos |
|---|---|---|---|---|
| 1 | Tolerancia de formato del validador grounding (M-07a) | M-07 (9 records) | validador, parse-side | `internal/claims/review.go` |
| 2 | Reviewer grounding prompt v3 (M-07b) | M-07 (16 FN semánticos) | prompt v2→v3 | `internal/claims/review.go`, `records.go`, `records_test.go` |
| 3 | Recon prompt v4 (M-08+M-09) | M-08, M-09 | prompt v3→v4 | `internal/claims/records.go`, `internal/pipeline/v2_stages.go`, tests de probe |
| 4 | Verificación de R-M05/R-M06 adoptados | B-08 + robustez recon | verificación (ya commiteados) | sin cambios (2 riesgos marcados) |

---

## PIEZA 1 — Tolerancia de formato del validador grounding (M-07a)

### 1.1 Diagnóstico (verificado en código y journal)

**Flujo real:** `providers.Response.Structured` → `claims.ParseReviewResponse` (`internal/claims/review.go:55`) → gate estricto: (a) `r.Schema != ReviewSchema` rechaza (`review.go:65-67`); (b) `r.RecordID != t.RecordID || r.Version != t.Version` rechaza (`review.go:68-70`); (c) enum de verdict y atomicity estrictos. El fallo NO limpia la invocación: `ex.rejectInvocationV2` + `correctiveClaimReissue` (`internal/pipeline/v2_stages.go:1216-1223`), y un segundo rechazo terminaliza en `claimsMalformedAfterReissue` → record `UNSUPPORTED_INSUFFICIENT` con reason `reviewer_malformed_output`.

**Cifras del journal P7 (236 filas `claims.grounding_review` con `response_state=REJECTED`, 1416 filas de la task en total).** Cross-tab exacto medido por R1:

| Subcausa | Filas | Definición precisa |
|---|---:|---|
| B: dirección `id@N` | **206** | `record_id` trae el sufijo `@1` del header `target: cl-x@1` Y el campo `version` trae `1` → el mensaje del validador renderiza «addresses cl-x@1@1, review target is cl-x@1» |
| A: schema-id variante | **37** | `schema` ≠ `mke.claims-ground.v1`: 35 con `mke.claims-ground.v2`, 1 con `mke-claims-ground-v1` (guiones), 1 con `mke.grounding.v1` |
| A∩B | (9) | ambas en la misma fila |
| C: id-drift | **2** | `record_id` es OTRO id (`cl-precio-cierra-fuera-de-rango` vs target `cl-precio-cierra-fuera-rango`; `rel-elimacion-…` vs `rel-eliminacion-…`) — fallo de binding genuino |

Reconciliación con el brief (A=26/B=206/C=2): el 26 del brief son las filas v2 con dirección limpia (35 v2 − 9 v2∩B = 26). B=206 y C=2 coinciden exactamente.

**Causa raíz A — desalineación interna introducida por M-01 (`a7cf608`).** El M-01 añadió al header del request la línea `review_contract: claims.grounding_review vmke.claims-ground.v2` (`review.go:102`, `PromptVersionGrounding`), mientras la instrucción de salida sigue fijando el schema id congelado v1 (`review.go:151/162`, constante `ReviewSchema = "mke.claims-ground.v1"` en `records.go:34`). El request lleva DOS identificadores de versión con la misma forma `mke.claims-ground.*`; el modelo copia el del contrato (~15% de las reviews). **Prueba del ancla:** en los 9 casos terminales, la respuesta CORRECTIVA (cuyo texto instruye explícitamente `conforming to schema id "mke.claims-ground.v1"`, `review.go:195`) arregló el addressing en 9/9 pero volvió a emitir `mke.claims-ground.v2` en 9/9 — porque la línea del header que induce el ancla permanece en el system prompt del correctivo. La anchura del ancla es el header, no la instrucción.

**Causa raíz B — eco del header de dirección.** El request abre con `target: cl-x@1` y `record: cl-x version 1` (`review.go:101,103`); la plantilla pide `"record_id":"<the record id under review>"`. El modelo hace eco del `cl-x@1` del header en `record_id` y además rellena `version: 1`. El correctivo SÍ lo arregla (instrucción «no "@" suffix», `review.go:196`), pero el defecto base sigue costando un reissue por record.

**No es contenido inválido:** las 236 filas rechazadas llevan TODAS verdict del enum congelado y (en claims) atomicity válida; en los 9 terminales el veredicto descartado era `GROUNDING_SUPPORTED` + `ATOMIC`. El pipeline descartó veredictos semánticamente completos por etiquetas de formato.

**Los 9 records terminales** (todos `UNSUPPORTED_INSUFFICIENT`, veredicto SUPPORTED descartado, fuente verificada por P8 §3.2): `cl-entrada-posicion-corta-114697`, `cl-fecha-24-06-2025`, `cl-informacion-curso-intermedio-no-relevante`, `cl-observar-rangos-diario-es-facil`, `cl-operar-solo-grafico-diario` (≈ w0033 MISSING_MATERIAL: «podrías hasta operar solo viendo el gráfico diario», asr-00058), `cl-rango-actual-toma-low-vela-anterior`, `cl-rango-bajista-completa-ordenes`, `cl-seleccion-vela-blanca-pequena`, `cl-smt-convierte-esto-en-rango`. Además `cl-intraturtlesoup-open-pnl-label` (`UNSUPPORTED_REVIEW_UNAVAILABLE`): su 1.er intento fue v1+`@1` (inv `eef5fd640f79`, respuesta de 361 bytes) y murió en parse-fatal el reissue (inv `68fd7f26666b`) — con tolerancia ese 1.er intento valida.

### 1.2 Diseño mínimo

**Un solo archivo: `internal/claims/review.go`** (el gate de V1 `internal/knowledge/grounding.go` NO se toca — la clase defecto es exclusiva de V2 claims).

1. **Schema-id: conjunto cerrado.** Aceptar exactamente `{"mke.claims-ground.v1", "mke.claims-ground.v2"}` como valores válidos de `schema`:

```go
// reviewSchemaAccepted lists the schema ids a review reply may declare. v2 is
// accepted because the P7 journal proved the review_contract header line
// (which carries the calibration version) anchors the model into echoing it:
// 37/236 rejected replies carried "mke.claims-ground.v2" (or a one-off
// variant) with a semantically complete verdict. The set is CLOSED: any other
// string stays malformed, and the payload contract (fields, enums, atomicity)
// is validated identically for both ids.
var reviewSchemaAccepted = map[string]bool{ReviewSchema: true, "mke.claims-ground.v2": true}
```

La variante con guiones (`mke-claims-ground-v1`) y `mke.grounding.v1` quedan FUERA (n=1 cada una, one-offs que el reissue ya recupera; normalizarlas sería tolerancia por patrón, no conjunto cerrado).

2. **Dirección: normalizar UN sufijo `@<dígitos>` antes del binding.** Nuevo helper puro:

```go
// normalizeRecordAddress strips exactly one trailing "@<digits>" from the
// replied record id (the P7 model echoed the "target: id@1" request header
// into record_id in 206/236 rejected replies). A doubled suffix ("id@1@1" ->
// "id@1") does NOT resolve and stays malformed; a genuinely different id
// never resolves. The version field must still equal the target version, and
// audit error messages keep the raw replied values.
func normalizeRecordAddress(id string) string {
    if i := strings.LastIndex(id, "@"); i > 0 && isAllDigits(id[i+1:]) {
        return id[:i]
    }
    return id
}
```

En `ParseReviewResponse`: comparar `normalizeRecordAddress(r.RecordID) != t.RecordID || r.Version != t.Version` para el gate, preservando los valores RAW en el mensaje de error. `cl-x@1@1` → normaliza a `cl-x@1` → sigue rechazando (doble sufijo nunca tolerado). Drift (C) sigue rechazando.

3. **Des-anclar el header (viaja con el bump v3 de la Pieza 2).** La línea del header deja de tener forma de schema id: `review_contract: claims.grounding_review calibration-3` (renderizado del set de calibración, no del `mke.claims-ground.*`). `Request.PromptVersion` sigue siendo `mke.claims-ground.v3` (superficie de invalidación/fingerprint intacta; el override de config `ClaimsGroundingPromptVersion` no se usa en R5). Esto elimina el inductor para las respuestas nuevas; la tolerancia del validador queda como cinturón (y es lo que recupera los journals/replays antiguos).

4. **Qué NO se tolera (lista explícita, fail-closed intacto):** verdict ausente o fuera del enum congelado; atomicity ausente/inválida en claims; atomicity presente en relations; `version` de campo ≠ target; `record_id` de OTRO record (drift) o con doble sufijo; schema id fuera del conjunto cerrado; datos tras el objeto JSON; campos desconocidos (`DisallowUnknownFields` se mantiene). Un `mke.claims-ground.v3` en el futuro sería un nuevo ancla-bug → rechazo + reissue + auditoría R6, no tolerancia.

5. **Identidad/replay:** el fix es parse-side; los bytes del request no cambian por la Pieza 1 sola → `RequestIdentity` estable en ambos sentidos. El camino del reissue queda intacto (pasará a dispararse mucho menos).

### 1.3 Verificación contra journal (hecha por R1 con el diseño propuesto)

- **9/9 records terminales → SUPPORTED.** Simulación sobre las respuestas reales del journal (base y correctiva de cada uno): todas pasan el gate tolerado con `GROUNDING_SUPPORTED` + `ATOMIC` + binding resuelto. Sin llamada nueva al provider.
- **`cl-intraturtlesoup-open-pnl-label` → SUPPORTED** vía su 1.er intento (v1+`@1`): +1 record.
- **Balance del replay P7:** 1125→1135 supported, 64→54 non-supported.
- **Ruta de verificación OBLIGATORIA para R3:** la recuperación es observable por **recorded-script replay** (export `run.db` → fixtures → rerun con binario nuevo), NO por journal-invocation replay: `attemptClaimReview` corta-circuita filas `REJECTED` sin re-parsear (`v2_stages.go:1279-1280`), así que el replay por identidad de invocación no re-deriva el gate. El replay de script sí re-alimenta la respuesta por el parser actual. Cifra esperada en ese replay: +10 supported (los 9 + intraturtlesoup; los 4 parse-fatal puros se quedan UNAVAILABLE en replay y se re-ejercitan frescos en R5).
- **Negativos (table test):** drift, doble sufijo, `mke.grounding.v1`, `mke-claims-ground-v1`, verdict inválido, atomicity en relation, atomicity ausente en claim → todos siguen rechazando.

### 1.4 Acceptance criteria — Pieza 1

| # | Criterio | Verificable por |
|---|---|---|
| AC1.1 | Table test: las 9 respuestas terminales del P7 (fijadas como testdata con invocation ids) parsean a `GROUNDING_SUPPORTED`+`ATOMIC` con el binding correcto | R3 |
| AC1.2 | Table test negativo: 8 formas inválidas listadas en 1.2.4 siguen rechazando con mensaje que preserva los valores raw | R3 |
| AC1.3 | El conjunto aceptado es exactamente {v1, v2} (sin matching por patrón) — lectura de código | R3 |
| AC1.4 | Recorded-replay del run P7 con binario remediado: exactamente los 10 records de §1.3 voltean a SUPPORTED; 0 divergencias nuevas en el resto | R3 |
| AC1.5 | En R5: los 9-class malformed-verdict dejan de existir como clase terminal (0 records `UNSUPPORTED_INSUFFICIENT` con reason `reviewer_malformed_output` por schema/addressing; lo que quede de la clase debe ser contenido genuinamente inválido) | R6 |
| AC1.6 | AC de M-08 parcial: `cl-operar-solo-grafico-diario` (o su equivalente v4) publicado SUPPORTED en R5 (cierra w0033) | R6 |

---

## PIEZA 2 — Reviewer grounding prompt v3 (M-07b: los 16 FN semánticos)

### 2.1 Diagnóstico

Los 16 FN semánticos P8 (`../p8-final-audit/results/GROUNDING-AUDIT.md` §2, filas `grounding-audit.jsonl`): 8 causal/definicional + 5 deixis + 3 garble-identity. La guía v2 (M-01, `a7cf608`) YA tiene líneas de garble y deixis — pero:

1. **Las guías de calibración SOLO viajan en la rama de claims.** `BuildReviewRequest` tiene dos textos: relations (`review.go:147-155`) sin NINGUNA guía de calibración; claims (`review.go:156-171`) con las 3 guías v2. **Los 8 FN causales son TODAS relations.** El M-01 nunca llegó a la población donde más duele.
2. **La guía garble es demasiado estrecha:** exige «when the cited evidence (frame or on-screen label) shows they are the same thing». Los 3 garble-FN son identidad FONÉTICA/verbal sin etiqueta visual que la muestre: «Felur Swing»≡failure swing (asr-00213; statement canónico «Va a haber un capítulo de failure swing»), «libra»≡GBPUSD (frames GBPUSD + «en libra puede pasarte algo así, no llega al objetivo»), «GIP»≡GBP (asr-00199/200 — RE-currente desde P1).
3. **La guía deixis no autoriza resolver anáfora/discurso:** «el bearish» = el rango enunciado en la misma frase («forma uno bearish, completa el bearish»), «10» = marco temporal alternativo («si queréis utilizar 10 25 30»), «0100» = marca del esquema Power 3 citada en el frame, «al final» = deixis de cierre de sección, «la otra vela» = la vela previa de la definición.
4. **No existe guía causal/definicional:** el reviewer exige conector literal de dependencia. Los 8: «esto es lo que llamaremos un rango pendiente» (×2 definiciones condicionales), «En el caso de…», «que si no conoces… porque», «Después de… Pues…», y las 3 dependencias constitutivas de la definición SMT.

### 2.2 Diseño mínimo (evolución del prompt v2, mismo bloque de calibración)

Cambios en `internal/claims/review.go` `BuildReviewRequest`; `PromptVersionGrounding` → **`mke.claims-ground.v3`** en `internal/claims/records.go`. Texto completo de las líneas nuevas/cambiadas:

**a) Rama de RELATIONS — bloque de calibración nuevo** (insertar antes de «Do not use outside knowledge»; hoy no existe):

```text
- Identity: an ASR-garbled spoken form and the canonical term are the same thing when the garble is a phonetic distortion of the term («Felur Swing» = failure swing, «GIP» = GBP, «libra» = GBPUSD, «S&T» = SMT) or when the cited frame shows the instrument/label they name. Judging a statement that uses the canonical term against a transcript that garbles it is not outside knowledge.
- Deixis and anaphora («the other candle», «the bearish one», «that», bare numbers after a timeframe mention) resolve from the cited transcript segments and cited frames: when the referent is identifiable within the cited context, treat it as resolved instead of rejecting for an unnamed referent.
- A dependency between the two claims is stated when the cited transcript enacts it as a definition, a conditional rule or a scenario («this is what we will call X», "if ... then", "in the case of ...", "because", "pues"), even without the literal words "depends on". Two claims that merely co-occur without an enacted link stay GROUNDING_INSUFFICIENT.
```

**b) Rama de CLAIMS — sustituir 2 guías y añadir 1** (junto a las v2 existentes):

```text
- Identity (reemplaza la guía garble v2): an ASR-garbled spoken form and the canonical term are the same thing when the garble is a phonetic distortion of the term, when the cited frame or on-screen label shows the same object under the canonical name, or when the statement itself quotes the transcript's own wording. Supporting the canonical form against the garbled form is verbatim support of the same proposition, not outside knowledge.
- Deixis (reemplaza la guía v2): resolve deixis, anaphora and discourse references («this», «the other candle», «al final», a bare «0100» or «10» tied by the speech to an on-screen mark) from the cited context before judging; when the referent is identifiable within the cited evidence, the statement is not rejected for naming it indirectly.
- Causal/definicional (nueva): a statement that reproduces a definition, a conditional or a consequence enounced by the cited transcript is supported by it even when the link is enacted by structure («esto es lo que llamaremos…», "if ... then", "aun así", "even when") rather than by a literal connector word.
```

**c) Anti-rubber-stamp (bloque compartido, ambas ramas)** — las reglas nuevas no convierten al reviewer en sello:

```text
- These resolutions bind identity and reference ONLY: the proposition asserted must still be the one the cited evidence states. If the evidence shows something different from what the statement asserts (different object, different number, different event), judge GROUNDING_CONTRADICTED exactly as before.
- A statement quoting a garbled form does not license supporting a DIFFERENT proposition: only the garble↔canonical pairing is resolved.
```

**Few-shots REALES del P8** (van en el diseño; en el prompt viajan como los mini-ejemplos entre paréntesis de arriba — NO como bloque de ejemplos completo, para no inflar ~1400 reviews/run):

- Soporte correcto (causal-definicional): rel-smt-visibility-scope — «Este es un tipo de SMT que si no conoces la estrategia no vas a poder ver de ningún modo porque a veces estos datos están un poco ocultos» ⇒ la dependencia está enunciada verbatim con «que si no… porque».
- Soporte correcto (deixis): cl-completa-rango-bearish — «forma uno bearish, completa el bearish» ⇒ la anáfora se resuelve dentro del segmento citado.
- Soporte correcto (garble): cl-capitulo-failure-swing — transcript «va a haber un capítulo de Felur Swing» ⇒ soporta statement «Va a haber un capítulo de failure swing».
- Rechazo correcto que DEBE seguir funcionando: cl-fuente-cambia-a-oanda — statement «La fuente mostrada cambia de FOREX.com a OANDA» con ambos frames citados mostrando FOREX.com ⇒ `GROUNDING_CONTRADICTED` (veredicto P8 correcto).
- Rechazo correcto que DEBE seguir funcionando: cl-second-rectangle-color-change — statement «relleno negro y después blanco» con frames mostrando blanco→negro ⇒ `GROUNDING_CONTRADICTED` (veredicto P8 correcto).

**Tests:** actualizar probes en `internal/claims/records_test.go` (pin v3; cada guía nueva presente en AMBAS ramas; línea anti-rubber-stamp presente; header des-anclado de la Pieza 1). `CorrectiveReviewRequest` hereda el base — sin cambios propios.

### 2.3 Acceptance criteria — Pieza 2

| # | Criterio | Verificable por |
|---|---|---|
| AC2.1 | Probes: prompt v3 pinneado; las guías identity/deixis/causal aparecen en la rama de relations (hoy ausente) y en la de claims; las 2 líneas anti-rubber-stamp presentes | R3 |
| AC2.2 | Fixture de regresión: los 15 targets de rechazo correcto del P8 (8 ACTUALLY_CONTRADICTED + 7 CORRECT_REJECTION, ids en `grounding-audit.jsonl`) re-reviewados con v3 sobre su evidencia citada reproducen el MISMO veredicto 15/15 | R3 (adversarial: intentar falsificar con inputs lindantes) |
| AC2.3 | Fixture semántico: ≥13/16 FN semánticos re-reviewados con v3 pasan a `GROUNDING_SUPPORTED` (objetivo ≥12 para no comprometer el gate; 16/16 posible) | R3 |
| AC2.4 | Safety: 0 falsos positivos nuevos en la muestra de 61 supported re-reviewada con v3 | R3 |
| AC2.5 | En R5: FN rate (fórmula P1) ≤10% medido sobre la población non-supported; los sub-patrones causal/deixis/garble desaparecen como clases dominantes (0 garble-FN recurrentes, en particular ningún caso GIP por tercera vez) | R6 |

---

## PIEZA 3 — Recon prompt v4 (M-08 + M-09)

### 3.1 Diagnóstico

- **M-08/w0010 (negación perdida):** asr-00017 «o lo mismo, tampoco tiene que ser negativa como tal» (127310–134420) — corrección del WRONG baseline `cl-vela-negativa-mayoria` — ausente de TODO el store. La recon v3 no tiene ninguna regla que ordene capturar negaciones/excepciones como proposiciones propias; el modelo las deja caer o las pliega en la afirmativa.
- **M-08/w0036 (forward-reference perdida):** asr-00067 «…que en Libra están formados, ya lo vais a ver en el tema de la SMT, ahora» — el vínculo rangos-bearish-de-Libra↔tema-SMT no existe como record. La v3 sólo ordena CITAR segmentos que resuelven deixis, no capturar el anuncio que BINDS contenido de esta ventana a un tema futuro.
- **M-09/w0037 (nivel con rol equivocado, STILL_WRONG):** statement publicado «El objetivo de hoy del rango bullish de GBPUSD está en 1,37489» (SUPPORTED). Journal de la recon w0037 (inv `c92ec169…`): el modelo emitió EN LA MISMA RESPUESTA `cl-gbpusd-bullish-range-upper-135843` (borde superior CORRECTO, 1.35843) y el target-137489 — leyó como «objetivo de hoy» el número de OTRA línea dibujada; el transcript dice «teníamos este objetivo para hoy» (asr-00069). La regla v3 («transcribed exactly as labeled; never assign a level the cited evidence does not show») garantiza que el NÚMERO está bien etiquetado, pero NO que el objeto etiquetado juegue el ROL que el statement le asigna (objetivo vs línea dibujada vs marca de escala vs rejilla). Mismo mecanismo en w0063 (`cl-nivel-horizontal-1-15728`: marca de escala vs línea 1.15803) y w0103 (`cl-rango-nivel-inferior-112695`). El reviewer no puede falsificarlo: su frame también muestra el número — el defecto es de ASIGNACIÓN DE ROL upstream.

### 3.2 Diseño mínimo (evolución de `ef0e594`)

`PromptVersionReconstruct` → **`mke.claims-recon.v4`** (`internal/claims/records.go`); reglas en `buildClaimsReconstructionRequest` (`internal/pipeline/v2_stages.go:945-960`). Tres reglas nuevas/reemplazadas, texto completo:

**a) Negaciones/excepciones (insertar tras la regla ATOMICITY):**

```text
- Negations, corrections and exceptions are first-class propositions: when the transcript says what something is NOT, or narrows a stated rule («tampoco tiene que ser negativa como tal», "aun así", "excepto cuando"), emit that restriction as its own atomic claim citing the exact segment. Never drop a negation because it qualifies an affirmative proposition, and never fold it into the affirmative claim it corrects. A clause that only restricts the same single proposition (removing it changes what is asserted) stays inside its claim, per the ATOMICITY rule.
```

**b) Forward-references verbatim (insertar tras la regla de citación de deixis):**

```text
- When the instructor binds what this window shows to a named later topic while stating something substantive about this window («estos rangos bearish ya los vais a ver en el tema de la SMT»), capture that binding as its own INSTRUCTOR_SAID claim quoting the anchor content; do not drop it as filler and do not invent the future topic's content. Pure meta fillers with no window content («esto ya lo vamos a ver más adelante») stay omitted.
```

**c) Verificación de niveles por rol (REEMPLAZA la regla actual «Levels, targets, entries and stops…» de la línea 958):**

```text
- On-screen numbers are transcribed exactly as labeled, AND a number may only be assigned the role its labeled object actually plays: an objective/target number comes from the declared target (the object the instructor states or marks as the objective), a range bound from the drawn range's own edge labels, an entry/stop from the position tool's fields. Axis ticks, grid marks and other drawn lines are never the source of a role they do not carry. When the transcript assigns a role («teníamos este objetivo para hoy») and the frame shows several numbers, bind the role to the specific labeled object the speech refers to and cite that exact frame; when the cited evidence does not disambiguate which object plays the role, transcribe the object labels as plain parameter claims and OMIT the role assignment instead of picking a number.
```

**Tests:** bump de probes existentes (`v2_identity_remediation_test.go` pins v3 → v4 y asserted cada regla nueva viaja; `records.go` comentario de versión).

### 3.3 Acceptance criteria — Pieza 3

| # | Criterio | Verificable por |
|---|---|---|
| AC3.1 | Probes: recon v4 pinneada; reglas (a)(b)(c) presentes en el request; la regla de niveles v3 REEMPLAZADA (no coexisten) | R3 |
| AC3.2 | Fixture w0010: dado transcript con asr-00017, la recon emite la negación como claim propia atómica citando asr-00017 (no la pliega ni la omite) | R3 |
| AC3.3 | Fixture w0036: dado asr-00067, la recon emite el binding rangos-Libra↔SMT como claim INSTRUCTOR_SAID; dado «esto ya vamos a llegar más adelante» (w0042, no-material), la recon lo omite | R3 |
| AC3.4 | Fixture w0037: dado el transcript+frames de w0037, la recon NO asigna 1,37489 al rol «objetivo de hoy»; o emite el objetivo de la zona declarada (1.35843/1.36031) o emite los parámetros de etiqueta sin rol + omite el rol | R3 |
| AC3.5 | En R5: MISSING_MATERIAL = 0 en aceptadas (w0010 y w0036 representadas; w0033 vía Pieza 1; w0067 ver riesgo R-4) | R6 |
| AC3.6 | En R5: regression watch — `cl-vela-negativa-mayoria` sale de ABSENT_AND_MISSING (su corrección existe publicada); ningún parámetro publica un rol cuyo objeto etiquetado no lo juega en w0037/w0094/w0103-análogos (audit de frames R6); `cl-chart-symbol-gbpusd` y `cl-rango-nivel-inferior-112695` o se corrigen o dejan de publicar | R6 |

---

## PIEZA 4 — Verificación de R-M05 y R-M06 (adoptados, `8ae543a` / `edec9a8`)

### 4.1 R-M05 — composition por-objeto: CONFORME

- **Diseño verificado** (`internal/sko/sko.go` `ValidateCompositionPerObject`, `internal/pipeline/v2_sko_stages.go` `composeSKOs`): gate estructural por objeto; descarte con razón durable por objeto (`CompositionDiscard{ObjectID, Index, Detail}`) que nombra objeto + componente + claim exacta que falló, en redacción histórica; orden canónico de descartes (por object id, luego posición); id propuesto >1 vez descarta TODAS sus ocurrencias (sin resolver por orden de array); propuesta sin ningún objeto válido → rechazo cerrado con redacción histórica (`CompositionRejectionMessage`); propuesta vacía → comportamiento intacto. `ValidateComposition` se conserva como wrapper all-or-nothing (sólo tests lo usan — verificado: 0 callers de producción).
- **NO relaja la validación de las 157 refs buenas:** mismos checks, mismo orden intra-objeto (`ValidateClaimID`, duplicado de componente, `ClaimByID(id, version)` exacto, role no vacío, ordinales) — sólo cambia el ALCANCE del fallo (objeto vs propuesta). Los 19 objetos válidos continúan por el ladder NORMAL (`reviewCompositions`: integridad → touching relations → composition review → closure gate → publicación): el ladder queda intacto.
- **Tests:** 230 líneas pipeline (`DiscardKeepsValidObjects`, `AllObjectsInvalidRejectsClosed`, `EmptyProposalKeepsBehavior`) + 99 líneas sko (`PerObjectDiscardsOnlyInvalid`, `DuplicateIDs`, `AllInvalidAggregates` + gates históricos). Cobertura adecuada.
- **Expectativa live:** del patrón P8 (7 refs not-exists en 4 objetos; 19/23 válidos) → 19 objetos proseguen a review; gate `SKOS_TOTAL > 0` con ≥1 publicación. El invocation `sko.composition` pasa a VALIDATED (antes REJECTED) → exportable/reproducible en replay (la nota P8 ya obliga a re-exportar la fase L2 desde el run remediado).

### 4.2 R-M06 — reissue correctivo de recon: CONFORME con 2 riesgos a mitigar en R2/R3

- **Diseño verificado** (`internal/pipeline/v2_stages.go:365-478`): fallo de `DecodeReconstruction`/`ValidateProposal` → exactamente UN corrective reissue; identidad del correctivo = función pura de (request base, defecto) → una única identidad por intento de ventana, estable tras crash/resume; cargo de budget propio (test `ChargesItsOwnInvocation`); la ventana continúa sólo si el correctivo valida, con el correctivo como provenance; segundo defecto → ventana rechazada cerrada con el SEGUNDO defecto grabado en AMBAS filas (paridad R-MI04: el resume re-proyecta la causa terminal); fallo del provider en el correctivo → UNAVAILABLE record-scoped, nunca run-kill (test). Atomicity: `commitReconstructedWindow` sin cambios → commit whole-window intacto. Fail-closed: nada se repara silenciosamente; 2 fallos = rechazo terminal. Tests: 627 líneas (352+275) con los 4 caminos (recupera, persiste, provider-fail, budget).
- **Riesgo R-1 (inyección, mitigar en R2):** `correctiveReconstructionRequest` incrusta `firstDefect.Error()` VERBATIM en el system del correctivo; el texto del defecto incrusta strings controladas por el modelo (ids, field names del decoder JSON). El correctivo de grounding NO hace eco del defecto — diferencia de diseño. `%q` escapa saltos de línea pero la longitud es ilimitada. **Mitigación mínima:** plegar el defecto con `foldRequestLine` + `providers.SanitizeDetail` (300 chars) antes de incrustarlo. Determinista, 2 líneas.
- **Riesgo R-2 (replay, verificar en R3 — sin cambio de formato):** `mke.recorded-script.v1` casa por (task, target-marker) con duplicados = error de carga (`recorded/script.go:90-93`); el correctivo conserva el `target: wXXXX` del base → comparten clave. Es representable bajo la regla del exporter P8 (1 fixture por (task,target), prioridad VALIDATED, documentada en `REPLAY-AUDIT.md`): ventana corregida en live → replay re-alimenta la respuesta del correctivo (contenido autocontenido, valida en el intento base) → mismo outcome con una invocación menos (filas de budget excluidas por contrato); ventana terminal → replay re-alimenta la misma inválida dos veces → mismo rechazo, texto del defecto puede re-wrapping (clase de divergencia ya aceptada por P8). **Acción R3:** añadir un test de scripted-replay del camino correctivo (base inválida + fixture misma clave) para probar que no hay fatal «no scripted response» y que el outcome es estable. Limitación conocida (no bloqueante para R5 live): una suite scripted no puede dar respuestas DISTINTAS a base y correctivo del mismo target.

### 4.3 Acceptance criteria — Pieza 4

| # | Criterio | Verificable por |
|---|---|---|
| AC4.1 | Falsificación R-M05: propuesta con ≥1 objeto inválido y ≥1 válido → válido publicado (tras su review), inválido descartado con razón que nombra objeto+claim; id duplicado descarta todas las ocurrencias; propuesta 0-válidos → rechazo histórico; refs buenas 100% validadas (tests existentes + adversarial nuevo) | R3 |
| AC4.2 | Falsificación R-M06: recon inválida → 1 reissue con defecto exacto; correctivo válido → ventana continúa con provenance del correctivo; correctivo inválido → rechazo cerrado con 2.º defecto en ambas filas y resume re-proyecta la causa terminal; defecto >300 chars llega plegado/acotado al request (mitigación R-1) | R3 |
| AC4.3 | Test scripted-replay del camino correctivo R-M06 sin replay-gap fatal | R3 |
| AC4.4 | En R5: L2_REACHED = YES con skos.jsonl no vacío; los objetos descartados (patrón esperado ~4) con razón durable por objeto en `reasons` | R6 |

---

## Por qué las 4 piezas viajan en UN solo full rerun (R5)

1. **Invalidación de comparabilidad:** cualquier bump de prompt (v3 de reviewer, v4 de recon) cambia la config fingerprint y el output materialmente — la doctrina del repo (`prompt.go:5-7`) define ese efecto como intencional. Dos bumps en ciclos separados = dos reruns completos de ~15h y ~12M tokens para medir interacciones que además se confunden (el output de recon v4 es el input del reviewer v3).
2. **El gate M-07 no cierra por partes:** M-07a sola deja el FN en ~21/55 ≈ 38% (9 recuperados deterministas de 30); el umbral ≤10% requiere M-07b (16 semánticos) y la re-ejecución de los 5 parse-fatal, que sólo un rerun ejercita fresco. El bundle tiene suelo determinista (9) y palancas semánticas en el mismo ciclo.
3. **M-08 comparte mecanismo con M-07:** w0033 se cierra por la Pieza 1; w0010/w0036 por la Pieza 3 — medirlas en runs distintos partiría la métrica MISSING_MATERIAL.
4. **R-M05/R-M06 ya están en el binario:** cualquier rerun que los excluya exige reconstruir un candidato artificial; viajan gratis y su ejercicio live (L2 y reissues) es requisito de su propia adopción (R3 los falsifica primero).
5. **Economía del loop:** R4 targeted-live queda absorbido (decisión P8): L2 y parse-fatal se ejercitan en R5.

## Riesgos y mitigaciones (transversales)

| Riesgo | Pieza | Mitigación |
|---|---|---|
| El reviewer v3 se vuelve sello (suben falsos positivos) | 2 | Bloque anti-rubber-stamp en el prompt; AC2.2 (15 rechazos correctos intactos) y AC2.4 (0 FP) como candados R3; safety rule P8 vigente en R6 |
| Nuevo ancla de schema (`mke.claims-ground.v3` emitido por el modelo tras el bump) | 1+2 | Header des-anclado (sin token con forma de schema id); conjunto cerrado SIN v3 → rechazo+reissue+auditable; R6 cuenta la clase |
| w0067-recurre (identidad EURUSD/15M visible antes de canónica) vuelve a contar como MISSING | 3 | No es alcanzable por reglas de recon (es comportamiento del ladder de identidad, familia MI-03): riesgo residual declarado AL OWNER ahora — si R6 lo cuenta, es candidato a exemption documentada, no a más remediación |
| Parse-fatal persiste (clase sin reissue contractual, MI-08) | — | Queda en deuda documentada (KISS): 5/1189=0.42%, fail-closed, no gate-blocking por sí misma; palanca MI-08 pre-declarada si R6 exige 0 REVIEW_UNAVAILABLE |
| R-M06 eco de defecto sin acotar (inyección/longitud) | 4 | Mitigación R-1 obligatoria en R2 (fold+cap 300) |
| Replay L2/reissues | 4 | Re-export de fixtures desde el run R5 (ya mandato P8) + AC4.3 |
| Tokens/wall-time | 2+3 | Crecimiento ~1.3KB/request puntual ≈ <2% del run; sin cambios de timeout ni budget (composition_timeout_seconds intacto, ladder intacto) |

## Contrato congelado — checklist

- Fail-closed default: intacto (Pieza 1 tolera sólo veredictos semánticamente completos y bien dirigidos; todo lo demás rechaza; Pieza 4 fail-closed terminal verificado).
- Ladder de identidad: intacto (ninguna pieza lo toca).
- Vocabulario frozen (verdicts, publication states, schema ids de payload): intacto — `ReviewSchema` sigue siendo v1; v2 es alias de ACEPTACIÓN de input, no cambio de contrato de salida.
- `composition_timeout_seconds`: se queda (R-B02).
- N-06 (persistir forma/hash de fatals) y MI-05 (dedup cross-slug): deuda explícita, fuera de esta ronda.

## Plan de verificación resumido para R2/R3

1. R2 implementa Piezas 1-3 + mitigación R-1; bumps de versión v3/v4; probes actualizados; commites separados por pieza.
2. R3: (a) falsifica R-M05/R-M06 (AC4.1-4.3); (b) ejecuta fixtures AC1.1/1.2, AC2.2-2.4, AC3.2-3.4; (c) recorded-replay del run P7 con binario nuevo → +10 exactos (AC1.4).
3. R5: full rerun live (config sin overrides de prompt version).
4. R6: P8 con tooling reutilizable; adjudicar gates: L2 (AC4.4), FN ≤10% (AC2.5), MISSING_MATERIAL = 0 (AC3.5), M-09 (AC3.6).

---

## FEEDBACK (Agents-OS)

1. **Bootstrap y sesión: limpio.** El arranque con entradas obligatorias explícitas (rutas de P8, repo, run.db, commits base) permitió diseñar sin preguntas; ninguna ruta falló.
2. **El dato de subcausas del brief no era re-derivable tal cual:** el brief decía «A schema-v2/want-v1 = 26» pero el journal contiene 37 filas con schema variante (26 = sólo las v2 con dirección limpia; 9 v2 más llevan también el sufijo @1 y se contaban en B). Sugerencia: cuando un brief herede cifras de un escaneo previo, adjuntar el criterio de clasificación (o el script) junto al número; R1 tuvo que reconstruir el cross-tab para reconciliar. Los otros dos números (206/2) cuadraron exactos.
3. **`sqlite3` CLI sigue sin existir en el host** (ya lo dijo el feedback de GROUNDING-AUDIT): el journal se leyó de nuevo con Python. Reiterar la recomendación: dump `provider_invocations.jsonl` junto al run, o documentar el patrón de lectura Python como estándar de campaña.
4. **Verificación de fixes adoptados necesita replay por SCRIPT, no por identidad de invocación:** las filas REJECTED del journal cortan-circuitan sin re-parsear (`v2_stages.go:1279`), así que «el fix recupera records determinísticamente desde journal» sólo es cierto por la ruta recorded-script (fixtures re-alimentan el parser actual). Sugerencia para el diseño de campaña: nombrar explícitamente qué ruta de replay valida cada fix, para que R3 no corra la ruta equivocada y declare falso un fix que funciona.
5. **Las cifras de «recuperables» deberían venir con su contrfactual simulado:** poder verificar 9/9 (y el +1 intraturtlesoup) antes de commitear el diseño evitó diseñar sobre una expectativa optimista. Para futuros R1: pedir (o permitir producir) la simulación del contrfactual como parte del brief.
6. **N-10 (gobernanza de commits fuera de mandato) sigue sin mecanismo:** R1 volvió a encontrar los commits del owner en el HEAD local sin trazable aprobación formal en la sesión. Sugerencia: que el estado de adopción (adoptado/pendiente/rechazado + quién) viva en un archivo del vault (`acceptance-campaign/ADOPTIONS.md`) que cada fase actualice, no sólo en las conclusiones de los informes.
```text
PHASE = R1
STATUS = DESIGN_COMPLETE
BUNDLE = [P1 validador-tolerante, P2 reviewer-v3, P3 recon-v4, P4 verificación R-M05/R-M06]
NEXT = R2 implementación (por pieza, commits separados) → R3 adversarial
```
