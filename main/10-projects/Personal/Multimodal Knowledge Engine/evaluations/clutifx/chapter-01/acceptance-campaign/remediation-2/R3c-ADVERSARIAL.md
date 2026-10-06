# R3c — ADVERSARIAL (remediation loop 2 · clutifx Ch01)

- **Rol:** adversarial reviewer, one-shot, contexto fresco. Mandato: FALSIFICAR, no validar. Read-only en código; suites ejecutables.
- **Objeto:** 2 commits sobre `e7bc387` en `/home/kor/mke/multimodal-knowledge-engine` (HEAD = `1d06ce8`, confirmado): `be240f9` (calibración relations v4, R-M10) y `1d06ce8` (tolerancia `@N` múltiple en composition review, R-M07 parity).
- **Fuentes de falsificación:** diff completo de ambos commits; `internal/claims/review.go`, `records.go`, `records_test.go`, `review_relations_v4_test.go`; `internal/sko/closure.go`, `sko.go`, `review.go`, `review_tolerance_test.go`; `p8-final-audit2/results/FULL-RELATION-AUDIT.md`, `GROUNDING-AUDIT.md`, `L2-SKO-AUDIT.md`; corpus `p8-final-audit2/corpus/wNNNN.json`; `claims.jsonl` del run (`~/mke/clutifx-ch01-rerun2-20261004/run-rerun2/`); `R1-REMEDIATION-DESIGN.md`, `R2c-IMPLEMENTATION-REPORT.md`.
- **Veredicto resumido:** `be240f9` **CONFORMS con 1 MAJOR** · `1d06ce8` **CONFORMS**. BLOCKERS = 0 · MAJORS = 1 · MINORS = 3 · NOTES = 4.

---

## 1. Ataques y resultados

### A1 — Leak de rama (be240f9) → NO FALSIFICADO
- `groundingRelationsCalibrationV4` se referencia en exactamente un sitio: la rama `if t.Kind == TargetKindRelation` de `BuildReviewRequest` (`internal/claims/review.go:230`). La rama claims (else, `review.go:233-248`) solo referencia `groundingResolutionSafetyBlock`.
- **Verificación a nivel de bytes:** extraje el bloque else completo de `e7bc387:internal/claims/review.go` y de HEAD → `diff` vacío (claims branch byte-identical). El diff del commit toca solo el bullet de relations + consts + comentarios; `git diff --stat e7bc387..HEAD` confirma 6 archivos, sin drift colateral.
- **Anti-rubber-stamp delante en ambas:** `groundingResolutionSafetyBlock` (2 bullets identity/reference-only) está presente en las dos ramas, en ambas situado tras la calibración e inmediatamente antes de la instrucción final `- Do not use outside knowledge. Do not guess.` — posición idéntica a v3 (última palabra antes del cierre; efecto recencia a favor del safety block sobre la calibración permisiva).
- Test `TestV4RelationsCalibrationDoesNotLeakIntoClaimsBranch` pinea las dos direcciones (v3 guides presentes en claims; 3 reglas v4 ausentes en claims y presentes en relations) + el split de atomicity.
- Matiz (no defecto): el bump `PromptVersionGrounding` v3→v4 cambia la identidad/fingerprint de las requests de AMBAS ramas (la calibración de claims no cambia, su identidad sí). Es la semántica de invalidación declarada en el propio commit; no toca texto ni gates de claims.

### A2 — Over-permissiveness relations (be240f9) → PARCIAL: 1 vector residual real (MAJOR-1)
- **Puerta estructural:** `ParseReviewResponse` no cambió (solo la const del header); una relation que "conecta dos enunciados sin enlace real" parsea igual que en v3 — lo semántico es del modelo, como declara el encargo. No hay relajación mecánica.
- **Few-shots contra fuente (contraste fila a fila):**
  - `formation←close` = `rel-formacion-bajista-depende-cierre`; cita «si vemos que cierra adentro… se está formando un rango bajista» ≈ asr-00106 verbatim en corpus (w0050). ✓
  - `continuation←close-outside` = `rel-continuacion-cierra-fuera`; asr-00063+00064 cross-segment verbatim (w0035/w0036). ✓
  - `not-Turtle-Soup←absent-reaction` = `rel-no-turtle-soup-depende-de-no-reaccion`; asr-00131 «en lugar de reaccionar, sigue bajando, no es ningún tartle sub» (w0066). ✓
  - `SMT←EUR-objectives` = `rel-smt-superior-depande-eur-objetivos`; asr-00196 verbatim (w0092). ✓
  - `delete→reanalyze` = par `rel-reanalizacion-tras-eliminacion/olvido`; asr-00173 «Una vez pasa esto, ya puedes eliminar… y volver a analizar» (w0080). ✓ (rango de cita «asr-00161-73» es impreciso: la cita anclada es solo 00173.)
  - `timeframes` = `rel-bullish-range-depends-on-timeframes`; asr-00084 verbatim (w0040). ✓
  - Negativos: «podemos copiar la selección» = statement exacto de `cl-copiar-seleccion-mostrada@1`; «tres velas blancas seleccionadas» ≈ `cl-seleccion-tres-velas-blancas@1`; «se denominará reiniciado» = statement exacto de `cl-rango-reiniciado-denominacion@1` vs etiqueta `cl-rango-pendiente-rotulo@1` («RANGO PENDIENTE»); «tartel sub» alias vs definición (asr-00124). Los few-shots negativos enseñan a RECHAZAR los patrones del FP/TN reales — no enseñan a aceptar yuxtaposiciones. ✓
- **MAJOR-1 (el vector):** el bullet 2 de v4 ensancha la barra de aceptación a enlaces "implicit in the narrative" («después de X», «esto hace que Z», «una vez pasa esto»…) y el bullet 4 (consistencia: "the same way, everywhere") AMPLIFICA la dirección que tome el modelo. Bajo ese lenguaje, 2 de los 5 CORRECT_REJECTION de GROUNDING-AUDIT §3 quedan sin regla negativa que los cubra:
  - `rel-eliminacion-rango-requiere-invalidez` — patrón "dos consecuencias del mismo cause, aposición sin enactuación" (asr-00161/62): el patrón no está nombrado en ningún bullet ni few-shot negativo; "cause… implicit in the narrative" es textualmente adyacente a aceptarla.
  - `rel-falso-turtle-soup-depende-de-reaccion-real` — "adyacencia narrativa, sin enlace estructural" (asr-00131-33, MODEL_INFERRED): es de la misma familia proposicional que el few-shot positivo #3 (not-Turtle-Soup ← ausencia de reacción). Un modelo que generalice el few-shot #3 + la regla de consistencia puede voltear este rechazo correcto a SUPPORTED, y la regla de consistencia propagaría el volcado "a todas partes" por diseño.
  - No es falsificación en-repo (veredicto = modelo; dominio R6 live según precedente F-2 del loop 1), pero ataca la promesa "NI relajar los 8 rechazos correctos" en 2/8 y convierte esos 2 en expectativas R6 obligatorias.

### A3 — Few-shots correctos / exclusión de 2 de los 8 causales → NO FALSIFICADO (sin BLOCKER)
- Los 8 del Grupo A de FULL-RELATION-AUDIT §3: formacion-cierre, continuacion-cierra-fuera, no-turtle-soup-no-reaccion, no-turtlesoup-bajista, eliminacion-rango-requiere-invalidez, smt-eur-objetivos, toma-low-apertura, falso-turtle-soup-reaccion-real.
- **Excluidos del prompt:** `rel-eliminacion-rango-requiere-invalidez` y `rel-falso-turtle-soup-depende-de-reaccion-real`. GROUNDING-AUDIT §3 los clasifica **CORRECT_REJECTION (borderline)** ambos. La exclusión es CORRECTA y está documentada como desviación en R2c §Desviaciones-1. ✓
- **Los 6 incluidos:** formacion (FN clear), continuacion (FN clear), no-turtle-soup (FN clear), reanalización×2 (FN clear), bullish-timeframes (FN clear), smt (FN borderline) — **FN en AMBAS auditorías**; ninguno es un rechazo correcto. **BLOCKER = 0.** ✓
- Nota de contexto: las dos auditorías DISIENTEN en el total (GROUNDING: 10 FN + 5 CORRECT_REJECTION + 2 EVIDENCE_SELECTION; RELATION: 16 FN + 1 TN). El implementador adoptó la clasificación conservadora de GROUNDING-AUDIT — elección defensible (pinear un correct-rejection como few-shot positivo enseñaría sobre-aceptación); el coste es recall, no safety.

### A4 — normalizeSKOAddress múltiple (1d06ce8) → NO FALSIFICADO
- **Bucles y guards:** `for { i := LastIndex(id,"@"); if i <= 0 || !isAllDigits(id[i+1:]) { return id }; id = id[:i] }` — cada iteración acorta el string (terminación garantizada); `i <= 0` rechaza base vacía (`@1` → sin cambio → nunca liga); sufijo no-dígitos deja el id intacto.
- **Casos de abuso:**
  - `id@1@otro`: LastIndex apunta a `@otro` (no dígitos) → sin strip → mismatch con target → **fail-closed** ✓ (comportamiento correcto por construcción; sin fila de test — ver MINOR-3).
  - `id@01`: `01` son dígitos → strip → liga si base == target y el CAMPO version == target version. Ortografía tolerada no documentada; inofensiva (el gate de versión es un campo numérico separado). ✓
  - id vacío / `@1`: guard `i <= 0` ✓ (testeado).
  - `sko-x@`, `sko-x@a`, `sko-x@1a`, `sko-x@1@`: sin strip → fail-closed ✓ (testeado).
  - `sko-other-object@1@1` para target `sko-x`: normaliza a `sko-other-object` ≠ `sko-x` → **nunca resuelve** ✓ (testeado, con valor crudo en el mensaje).
- **Colisión entre identidades:** imposible por vocabulario — `validSKOID = ^sko-[a-z0-9]+(-[a-z0-9]+)*$` (`internal/sko/sko.go:82`), impuesto por `ValidateCompositionPerObject` (`sko.go:212`, discard antes de que el objeto llegue a review). Ningún id válido contiene `@`, luego el strip múltiple no puede colapsar dos identidades válidas, y un id con `@` (si existiera) solo podría fallar cerrado, nunca cruzar bindings.
- **Diferencia vs normalizador de claims (1 sufijo, doble sufijo malformed):** justificada empíricamente — journal P7b claims: drift de un solo sufijo (206/236); journal P7b sko: drift DOBLADO `id@1@1` en 7/33 salidas con veredicto interno COMPOSITION_SUPPORTED (L2-SKO-AUDIT §3, con el error literal `sko-range-completion@1@1` citado; 6/7 reissues recuperadas, range-completion cayó con el fatal). El requisito duro del encargo («`id@1@1` parsea») lo exige.
- **Fail-closed intacto:** schema id, campo version, enum de veredicto, dedup/empty relation_id, trailing data, DisallowUnknownFields — todos sin cambio y pineados por la tabla de 10 filas de `TestParseCompositionReviewResponseToleranceStaysFailClosed`. Los 2 SKO bloqueados correctos (objective-correction, scalp-range-conditions) se bloquean por closure gate estructural, no por parse — intocados por esta tolerancia.
- **MINOR-2:** la justificación estructural del mensaje de commit es inexacta (ver hallazgos).

### A5 — Suites → VERIFICADAS
- `go vet ./...` → **exit 0, sin output**.
- `go test ./... -count=1 -timeout 30m` → **20/20 paquetes ok, exit 0** (claims 0.020s, sko 0.017s, pipeline 97.8s, evidence 115.0s, cmd 54.8s).
- Pasa verbose: **1161 PASS · 0 FAIL · 2 SKIP**. Los 2 SKIPs son preexistentes y ambientales: `TestAcquireChildProcess` (internal/evidence) y `TestV2PhysicalProvenanceTraceResolvesToSourceSHA` (internal/pipeline, physical e2e) — ningún archivo de SKIP tocado en `e7bc387..1d06ce8` → **0 SKIPs nuevos**.
- Tests nuevos: claims +4 top-level (`review_relations_v4_test.go`: 5 pares gemelos + 8 causales + 4 FP + 1 leak = 17 subtests) y sko +3 top-level (`review_tolerance_test.go`: 4 echo + 10 fail-closed + 10 unitarios = 24 subtests). Los 7 top-level nuevos PASS.

### A6 — Contrato de versión v3→v4 → NO FALSIFICADO
- `groundingCalibrationSet` calibration-3 → calibration-4 (header sin token con forma de schema id, propiedad conservada); `PromptVersionGrounding` = `mke.claims-ground.v4`; `ReviewSchema` sigue `mke.claims-ground.v1`; `reviewSchemaAccepted` cerrado en {v1, v2} — pineado por el test preexistente que además exige que `mke.claims-ground.v3` futuro siga MALFORMED como schema de respuesta (`review_tolerance_test.go:92,120`). ✓
- Búsqueda de referencias v3 stale en .go/.md/.json/.jsonl (fuera de `wt/` y docs históricos): solo (a) el comentario histórico de lineage en `records.go:55` (correcto conservarlo) y (b) pins de test que exigen v3-malformed. Nada asume v3. El override de config (`ClaimsGroundingPromptVersion`) es passthrough sin whitelist; fingerprints computados desde la const (`v2.go:153,477`) → auto-actualizados. ✓
- `records_test.go` renombrado y actualizado a v4 (`TestReviewRequestContractV4Guides`), esperando `mke.claims-ground.v4` en ambas ramas. ✓
- NOTE: `wt/` es un checkout anidado NO trackeado (propio `.git` y `go.mod`) con copias viejas (`mke.claims-ground.v1`, `mke.ground04.v1`) — fuera de `./...`, sin efecto en build/tests; higiene.

---

## 2. Hallazgos por severidad

| ID | Sev | Commit | Hallazgo |
|---|---|---|---|
| **MAJOR-1** | MAJOR | be240f9 | **Vector residual de sobre-aceptación sobre 2 de los 8 rechazos correctos.** El lenguaje v4 "implicit in the narrative" + la regla de consistencia ("the same way, everywhere") + el few-shot #3 (not-Turtle-Soup ← reacción ausente, misma familia proposicional) carecen de contraejemplo que pinee los patrones de `rel-eliminacion-rango-requiere-invalidez` (dos consecuencias de una causa, aposición) y `rel-falso-turtle-soup-depende-de-reaccion-real` (adyacencia narrativa). No falsifica nada determinista (veredicto = modelo), pero la promesa "NI relajar los 8 rechazos correctos" queda protegida solo 6/8 en-repo. **Condiciones:** (1) R6 debe pinear esas 2 relations como INSUFFICIENT esperado; (2) recomendado: v4.1 con regla negativa explícita "two consequences of one shared cause / narrative adjacency stay GROUNDING_INSUFFICIENT". |
| **MINOR-1** | MINOR | be240f9 | Etiqueta imprecisa: `TestRelationGateAcceptsSupportedVerdictForP8bCausalRelations` dice "the 8 causal relation false negatives the P8b audit lists (its Grupo A)", pero el set = 6 del Grupo A + 2 del Grupo B (par reanalización); los miembros reales de Grupo A excluidos son justamente los 2 CORRECT_REJECTION. El SET es sano (los 8 son FN en al menos una auditoría; ninguno es rechazo correcto), el rótulo no. Igual en R2c §test-bullet. |
| **MINOR-2** | MINOR | 1d06ce8 | El mensaje de commit afirma "the composition request header is versioned, **unlike the claims record line**" como razón del strip múltiple: inexacto — la request de claims lleva el MISMO header versionado `target: id@1` (`claims/review.go:174`) más línea bare `record:`, estructuralmente simétrica a la de sko (`target:` + `object:` bare). La justificación real es la empírica (7/33 doblados en sko vs 206/236 de un sufijo en claims), que el commit también cita. Comportamiento seguro; rationale mal escrito. |
| **MINOR-3** | MINOR | 1d06ce8 | Huecos de test en el normalizador: `id@1@otro` (fail-closed correcto por construcción, sin fila) y `id@01` (strip de sufijo con cero inicial, tolerancia no documentada ni testeada). Además `isAllDigits` queda duplicado claims/sko (patrón preexistente ahora ×2). |
| **NOTE-1** | NOTE | ambos | `wt/`: checkout anidado no trackeado con código viejo (claims-ground v1 / ground04 v1). Fuera de `./...`; eliminarlo o ignorarlo explícito. |
| **NOTE-2** | NOTE | be240f9 | Discrepancia entre auditorías (FN 16 vs 10) resuelta adoptando GROUNDING-AUDIT; las 2 relations EVIDENCE_SELECTION (`no-turtlesoup-depende-bajista`, `llegada-directa`) no son recuperables por prompt sino por selección de evidencia del reconstructor — correctamente fuera de los few-shots. Deuda de reconciliation de ground-truth para futuros loops. |
| **NOTE-3** | NOTE | be240f9 | Cita de few-shot «asr-00161-73» abarca también los segmentos del caso excluido (00161/62); la cita anclada es 00173. Higienizar el rango. |
| **NOTE-4** | NOTE | 1d06ce8 | El corrective reissue de sko pinea `"sko_id" must be exactly "<id>"` pero sin la frase explícita "with no @ suffix" que sí usa claims — hoy inocuo (la deriva ahora se tolera); simetría cosmética. |

---

## 3. Veredicto por commit

### `be240f9` — calibración relations v4 (R-M10): **CONFORMS** (0 BLOCKER · 1 MAJOR · 1 MINOR)
Lo prometido se sostiene en la superficie determinista: la rama claims está **byte-identical** (verificado por extracción+diff, no por lectura), el anti-rubber-stamp sigue delante del cierre en ambas ramas, los 6 few-shots positivos son FN reales en AMBAS auditorías (ninguno es un rechazo correcto → **no hay BLOCKER**), la exclusión de los 2 CORRECT_REJECTION es correcta y documentada, los 4 FP del audit tienen regla v4 exacta pineada, y el bump de versión no deja referencias v3 stale con el schema set cerrado {v1,v2}. La recuperación de los FN causales/deixis es comportamiento del modelo: NO es verificable en-repo por construcción y queda pendiente de R6 live — con MAJOR-1 como condición: R6 debe pinear `rel-eliminacion-rango-requiere-invalidez` y `rel-falso-turtle-soup-depende-de-reaccion-real` como rechazos esperados.

### `1d06ce8` — tolerancia `@N` múltiple en composition review (R-M07 parity): **CONFORMS** (0 BLOCKER · 2 MINOR)
La tolerancia es exactamente la declarada: solo sufijos `@<digits>` sobre `sko_id`, binding tras strip, campo version intacto, resto del gate fail-closed idéntico y pineado (10 filas). Imposibilidad de colisión demostrada por vocabulario (`^sko-[a-z0-9…$`, impuesto pre-review) + tests de id distinto/mutación. La evidencia de auditoría respalda el shape doblado 7/33. MINOR-2 (rationale estructural del mensaje inexacto) y MINOR-3 (huecos de test `id@1@otro`/`id@01`) no afectan comportamiento.

### Suites
`go vet ./...` exit 0 · `go test ./... -count=1 -timeout 30m` 20/20 paquetes ok · 1161 PASS / 0 FAIL / 2 SKIP (ambos ambientales preexistentes, 0 nuevos).

---

## FEEDBACK (Agents-OS)

1. **Bootstrap en subagentes de tarea, segunda aparición.** A diferencia de lo reportado por GROUNDING-AUDIT, esta vez el skill `agents-os-bootstrap` SÍ estaba en la lista de skills disponibles (progreso). Pero el bootstrap completo resuelve VAULT_ROOT y enruta entidad para una tarea cuyo objeto vive FUERA del vault (`/home/kor/mke/...`): el costo de startup no compra nada de entidad. Sugerencia: cláusula "task-agent mode" en el bootstrap — si el encargo es one-shot sobre repo externo, basta verificar el marker, cargar constitución mínima y saltar el entity pack.
2. **"CLOSE SESSION AL TERMINAR" en encargos delegados (recurrente).** Igual que el feedback de GROUNDING-AUDIT §FEEDBACK-2: un subagente no posee el ciclo de sesión. Sugerencia ya emitida: sustituir por "entrega el veredicto final y no inicies fases nuevas". Que siga apareciendo indica que la plantilla de encargo no se actualizó — candidato a fix de plantilla único.
3. **Ground-truth no reconciliado = decisiones de implementación bajo ambigüedad.** Las dos auditorías P8b disienten en el conteo de FN de relations (10 vs 16) y en 3+ registros concretos; el implementador tuvo que adjudicar solo (acertó, y conservadoramente). Sugerencia: cuando un remediation bundle dependa de auditorías A/B, el loop debería producir PRIMERO una tabla reconciliada por-registro (etiqueta A, etiqueta B, adjudicación) y anexarla al encargo — la exclusión de few-shots y las expectativas R6 saldrían de ahí sin juicio discrecional.
4. **Los cambios prompt-only trasladan la verificación al live gate, pero el loop no genera esas expectativas automáticamente.** MAJOR-1 existía detectable por lectura (few-shot #3 comparte familia proposicional con un correct-rejection) y nadie lo enumeró como expectativa R6. Sugerencia de plantilla: todo encargo R-M que pinea reglas de prompt debe emitir dos listas — "debe pasar a SUPPORTED en R6" y "debe seguir NO-soportado en R6" — derivadas de los few-shots positivos y negativos del prompt resultante, para que el adversarial solo tenga que falsificar la derivación, no reinventarla.
