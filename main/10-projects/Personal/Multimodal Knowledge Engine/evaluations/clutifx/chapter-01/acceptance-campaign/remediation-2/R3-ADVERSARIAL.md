# R3 — ADVERSARIAL VERIFICATION · MKE V2 · Clutifx Chapter 01

**Fase:** R3 del remediation loop (falsificación del bundle R2; NO validación).
**Candidato:** `/home/kor/mke/multimodal-knowledge-engine` HEAD `e7bc387` (5 commits R2 sobre `edec9a8`, que trae R-M05 `8ae543a` y R-M06 `edec9a8`; base P7 `19b44c1`). Árbol limpio salvo `wt/` preexistente (no tocado; restaurado tras los experimentos).
**Método:** extracción de los request/response REALES del journal P7 (`run.db`, lectura Python), re-ejecución de esos bytes por el parser remediado (harness Go temporal dentro del repo, eliminado después; árbol sin cambios), batería negativa propia, experimentos scripted-replay sintéticos, suites completas, diff audit.
**Evidencia P7:** los 20 invocations de los 10 records terminales: 9 records × (base + correctiva, ambas `REJECTED`, veredicto descartado `GROUNDING_SUPPORTED`+`ATOMIC` en las 18) + `cl-intraturtlesoup-open-pnl-label` (1.er intento `REJECTED` v1+`@1`; 2.º intento parse-fatal sin respuesta).

---

## Ataque 1 — AC1.1 con evidencia física: los 9 reales + negativos

### 1a. Tabla 9/9 (+1) — respuestas REALES del journal por el validador nuevo (`6932d12`)

Los `response_json` del journal SON los bytes que el parser recibe en vivo (`v2_stages.go:141` persiste `string(resp.Structured)` verbatim; `ParseReviewResponse(attempt.raw, …)` en `:1220/:1248`). Re-marshalled 1:1, byte-fiel. Cada fila = target real (id, version 1, kind del request) + bytes reales → parser actual.

| # | record | inv 1.er intento | forma (schema / record_id) | inv correctiva | forma correctiva | ¿Parsea hoy? | Veredicto superviviente |
|---|---|---|---|---|---|---|---|
| 1 | cl-entrada-posicion-corta-114697 | `2b9375db…` | v2 / id`@1` | `2bbfcfd3…` | v2 / id limpio | SÍ ambas | `GROUNDING_SUPPORTED`+`ATOMIC` |
| 2 | cl-fecha-24-06-2025 | `3168a703…` | v1 / id`@1` | `e94ddc08…` | v2 / id limpio | SÍ ambas | ídem |
| 3 | cl-informacion-curso-intermedio-no-relevante | `d45ee0f2…` | v1 / id`@1` | `bc3e6259…` | v2 / id limpio | SÍ ambas | ídem |
| 4 | cl-observar-rangos-diario-es-facil | `9592e68e…` | v1 / id`@1` | `93aa9155…` | v2 / id limpio | SÍ ambas | ídem |
| 5 | cl-operar-solo-grafico-diario | `664439e0…` | v1 / id`@1` | `881013bf…` | v2 / id limpio | SÍ ambas | ídem |
| 6 | cl-rango-actual-toma-low-vela-anterior | `00e6571f…` | v2 / id limpio | `e5cf9f07…` | v2 / id limpio | SÍ ambas | ídem |
| 7 | cl-rango-bajista-completa-ordenes | `bc61393b…` | v2 / id limpio | `a9385562…` | v2 / id limpio | SÍ ambas | ídem |
| 8 | cl-seleccion-vela-blanca-pequena | `255c4a0e…` | v2 / id limpio | `483d9110…` | v2 / id limpio | SÍ ambas | ídem |
| 9 | cl-smt-convierte-esto-en-rango | `a38dd140…` | v1 / id`@1` | `2fb40d02…` | v2 / id limpio | SÍ ambas | ídem |
| +1 | cl-intraturtlesoup-open-pnl-label | `eef5fd64…` | v1 / id`@1` | `68fd7f26…` | (parse-fatal, sin respuesta) | SÍ el 1.er intento | ídem |

**Resultado: 19/19 respuestas reales parsean al veredicto que el reviewer emitió** (`GROUNDING_SUPPORTED`+`ATOMIC`), binding al id desnudo correcto. Cero veredictos alterados. El detail del rechazo P7 (`schema id … want v1`, `addresses id@1…`) ya no se produce con estos bytes.

### 1b. Negativos (batería adversarial propia, 13 casos, todos fail-closed)

Construidos sobre el parser real; mensaje preserva los valores raw donde aplica:

| caso abusivo | resultado |
|---|---|
| schema inventado `mke.claims-ground.v3` | RECHAZADO, raw en mensaje |
| schema inventado `mke.claims-ground.v9` | RECHAZADO |
| doble sufijo `cl-x@1@1@1` | RECHAZADO (normaliza a `cl-x@1` ≠ target), raw `cl-x@1@1@1` en mensaje |
| drift real de id (par P8: `cl-precio-cierra-fuera-de-rango` vs target `…-fuera-rango`) | RECHAZADO, raw en mensaje |
| veredicto fuera del enum (`"verdict":"SUPPORTED"`) | RECHAZADO |
| JSON válido pero `record_id` de OTRO record real (`cl-15m-timeframe`) | RECHAZADO, raw en mensaje |
| header v2 con body vacío / whitespace-only | RECHAZADO (decode error) |
| sufijo con espacio (`cl-x@1 `) | RECHAZADO, raw en mensaje |
| id en mayúsculas (`CL-X@1`) | RECHAZADO (case-sensitive), raw |
| `version` float (`1.5`) | RECHAZADO |
| `record_id` vacío | RECHAZADO |
| array JSON en vez de objeto | RECHAZADO |
| trailing data tras el objeto | RECHAZADO |

Además confirmé las 15 negativas del test de R2 (`review_tolerance_test.go`) y el conjunto cerrado exactamente {v1,v2} sin matching por patrón (`TestReviewSchemaAcceptedIsClosedSet`; lectura de código: `reviewSchemaAccepted` literal de 2 entradas, gate `!reviewSchemaAccepted[r.Schema]` en `review.go:118`).

**Bordes de tolerancia documentados (F-5):** `cl-x@7` (dígito de sufijo equivocado), `cl-x@01`, y sufijos de dígitos enormes SÍ parsean — el gate es el campo `version`, los dígitos del sufijo no se contrastan con `t.Version`. Es consecuencia directa del diseño («strips exactly one @<digits>»); no encontré vía de colisión (ver Ataque 2).

**AC1.4 contra el replay real:** ver F-1 — con los fixtures ya exportados por P8 el replay grabado rinde **+9**, no +10 (la entrada de `cl-intraturtlesoup-open-pnl-label` es un error-fatal, no su respuesta).

---

## Ataque 2 — Permissiveness (M-07)

1. **¿Colisión cross-record tras normalizar? IMPOSIBLE.** `normalizeRecordAddress` sólo puede igualar `t.RecordID` si el id respondido ES `t.RecordID + "@<dígitos>"`; los ids reales tienen charset `[a-z0-9-]` (`validClaimID`/`validRelationID`/`validRecordID`, `records.go:217-218`, `knowledge/records.go:268`) — ningún id legal contiene `@`, y un id de OTRO record nunca normaliza al target. Un veredicto dirigido a otro record no puede aterrizar en éste.
2. **¿Veredicto que el reviewer NO dio? NO.** La tolerancia no sintetiza ni transforma veredictos: devuelve `r.Verdict` tal cual, tras el enum congelado y el binding. Lo único que hace es NO descartar un veredicto sí emitido. El caso «dirección equivocada que colisiona» se cierra por (1).
3. **Dientes del anti-rubber-stamp (Pieza 2):** el bloque existe verbatim en AMBAS ramas (`review.go:43-44`, renderizado en `:215` y `:232`; probe `TestReviewRequestContractV3Guides` assertea las 2 líneas). La línea «different object, different number, different event → GROUNDING_CONTRADICTED exactly as before» cubre textualmente el mecanismo de los 8 ACTUALLY_CONTRADICTED (4 son número-con-rol equivocado, cubiertos por «different number»; 2 son lectura del frame correcta; 1 temporal; 1 exclusividad). **PERO no existe NINGÚN test conductual**: AC2.2 (15/15 veredictos idénticos re-reviewados con v3), AC2.3 y AC2.4 exigen inferencia del modelo y el mandato R3 es offline → **F-2**. Hasta R5/R6, la protección es sólo prompt-texto pinneado, no comportamiento medido.
4. **Notas:** la guía relations de dependencia-enunciada cierra con «Two claims that merely co-occur without an enacted link stay GROUNDING_INSUFFICIENT», que es el diente textual contra las 4 rel CORRECT_REJECTION por yuxtaposición taxonómica. `CorrectiveReviewRequest` hereda `base.System` → el correctivo viaja con las guías nuevas + bloque de seguridad (sin cambios propios, verificado en diff).
5. **Identidad/replay de la Pieza 1:** parse-side puro; `RequestIdentity` (task, prompt_version, System, schema, text, image-hashes) no cambia por la Pieza 1; la Pieza 2 cambia bytes a propósito vía bump v3. Coherente con el diseño.

---

## Ataque 3 — Recon v4 (M-08/M-09), contra los prompts commiteados

Texto verbatim del diseño en `v2_stages.go:950-963`; regla de niveles v3 REEMPLAZADA (no coexisten; test negativo en `TestV2IdentityRequestContractPhysical`). Puntos de ataque evaluados:

1. **Over-suppression (regla b):** la exención «pure meta fillers with no window content stay omitted» ahora está ESCRITA en el prompt (antes era comportamiento ad hoc). El criterio «while stating something substantive about this window» + ejemplo positivo (rangos-bearish↔SMT) y negativo (w0042) acotan la frontera, pero un modelo sobre-aplicando el filler-exemption podría silenciar bindings legítimos → MISSING_MATERIAL nuevo. Riesgo residual REAL pero de dirección conocida y medible en R6 (AC3.5); el diseño lo asume implícitamente al fijar MISSING_MATERIAL=0 como gate R6. Sin falsificación posible offline.
2. **Explosión de negaciones (regla a):** la regla cierra con el fusible atómico «A clause that only restricts the same single proposition (removing it changes what is asserted) stays inside its claim, per the ATOMICITY rule» — mismo criterio de independencia-evaluable que la ATOMICITY y su bullet compañero preexistentes. Cada negación emitida es una claim atómica (no viola atomicity), acotada por contenido de ventana; el riesgo de inflación es de volumen (~proporcional a negaciones reales del corpus), no de forma. El reviewer COMPOSITE sigue como segunda valla. Sin explosión estructural.
3. **Regla c (rol):** introduce una licencia de OMISIÓN nueva («OMIT the role assignment instead of picking a number»). Dirección fail-safe (omitir antes que mal-asignar) y alineada con AC3.4; el riesgo de sobre-omisión (roles legítimos no asignados) queda de nuevo en R6 (AC3.6). Conserva «transcribed exactly as labeled» (aserciones P4 intactas y verdes).
4. **w0067-recurre:** confirmado que ninguna regla nueva lo toca (es ladder de identidad, familia MI-03) — el riesgo residual declarado por R1 al owner sigue siendo la cobertura correcta.

---

## Ataque 4 — Falsificación R-M05/R-M06

### R-M05 — sobrevive a la falsificación

- **Duplicado con validez partida (adversarial nuevo):** id propuesto 2× donde la 1.a ocurrencia es inválida (claim fantasma) y la 2.a sería válida → AMBAS descartadas (`occurrences[po.ID]>1` se evalúa por iteración ANTES de cualquier corto-circuito de validez; verificado ejecutando `ValidateCompositionPerObject` con ese proposal). No hay asimetría por orden ni por validez que smugglee una ocurrencia. Orden canónico por (id, índice) verificado.
- **0-válidos → rechazo cerrado** con redacción histórica (`CompositionRejectionMessage`, tests existentes `TestV2CompositionAllObjectsInvalidRejectsClosed` + `TestValidateCompositionPerObjectAllInvalidAggregates` con orden canónico).
- **Propuesta vacía → comportamiento intacto:** `len(objects)==0 && len(discards)==0` no entra en la rama de rechazo; 0 candidatos → ladder no-op → el gate de salida L2 falla cerrado como antes (lectura de `composeSKOs` + test `TestV2CompositionEmptyProposalKeepsBehavior`).
- **Refs buenas 100% validadas:** mismos checks intra-objeto en el mismo orden; el alcance del fallo es lo único que cambia. `ValidateComposition` (wrapper all-or-nothing) conserva exactamente 0 callers de producción (grep sobre `internal/` + `cmd/`).
- **Proyección del patrón P8:** 7 refs inválidas en 4 objetos, 19/23 válidos (L2-SKO-AUDIT §2) → con el gate por-objeto los 19 prosiguen; la razón de descarte nombra objeto+componente+claim (formato verificado en los tests y en el diff de `v2_sko_stages.go:99-124`).

### R-M06 — sobrevive a la falsificación, con 3 notas

- **Ciclo-infinito: IMPOSIBLE.** `correctiveReconstructionReissue` no se llama a sí misma; el segundo defecto termina en `rejectClaimsWindow` (`v2_stages.go:479-486`). Exactamente un reissue por intento de ventana, identidad = función pura de (request base, defecto) — verificado en `TestCorrectiveReconstructionRequestFoldsAndCapsDefect/derivation stays a pure function`.
- **Doble cobro de budget: NO.** `invokeV2` cobra por invocation identity; base y correctivo tienen identidades distintas y un cargo cada uno (`TestV2ReconstructionReissueChargesItsOwnInvocation`: labels `w1-theory`=1 y `w1-theory:corrective`=1, w2 budget-refused). Resume no re-cobra committed budget (`v2_stages.go:147`).
- **R-1 (fold+cap):** verificado con los 4 subtests (multilínea «Hard rules:» falsificado NO puede inyectarse como estructura; >300 chars llega acotado; corto viaja verbatim — aserción existente del contrato de defecto exacto intacta).
- **R-MI04 parity en resume (terminal): VERIFICADO EXPERIMENTALMENTE** — run con correctivo inválido → resume sobre el mismo OutDir → la causa re-proyectada es el SEGUNDO defecto (mi experimento: `resume cause = "…unknown evidence ref \"seg-999\""` en la fila de ventana). Sin crash, paridad exacta.
- **F-4 (asimetría de recuperación en resume):** si el crash cae ENTRE el rechazo del base y la terminalización del correctivo, el resume corta-circuita en la fila base REJECTED (`v2_stages.go:330-337`) y NUNCA consulta el correctivo — incluso si el correctivo llegó a VALIDARSE en el journal se descarta. El camino de grounding reviews sí re-intenta el correctivo en resume (`strictClaimReview` → `attempt.rejected` → `correctiveClaimReissue`). Fail-closed y determinista ambos caminos; la asimetría sólo cuesta yield (ventana perdida) en una ventana de crash estrecha.
- **ClassFatal del provider en el correctivo → run-kill:** igual que en el base (vía `fatal()`); el «nunca run-kill» del diseño refiere a fallos acotados retry-exhausted → UNAVAILABLE (test `TestV2ReconstructionCorrectiveReissueProviderFailure`). Consistente, sin hallazgo.

---

## Ataque 5 — Replay / recorded-script del camino correctivo (AC4.3)

**Clave compartida demostrada por código + experimento:** `correctiveReconstructionRequest` hace `corrected.System = base.System + "\nCORRECTIVE REISSUE:…"` → la 1.a línea `target: wXXXX` no se mueve → `markerTarget` (`recorded/script.go:121-135`) devuelve el MISMO target para base y correctivo → misma clave `(task,target)`. Mini-experimento con fixture sintético (script `mke.recorded-script.v1` + 2 ventanas):

- **Ventana terminal en live (base y correctivo con el mismo contenido inválido):** replay re-alimenta el MISMO fixture dos veces → 2 invocations REJECTED, segundo defecto en ambas filas, ventana REJECTED cerrada, **sin fatal «no scripted response»**, run completa. ✓
- **Ventana corregida en live (exporter prioriza VALIDATED):** el fixture del correctivo (autocontenido, valida contra el índice) re-alimenta el intento base → 1 invocation VALIDATED, misma outcome de ventana/records con una invocation menos — exactamente el contrato documentado por P8. ✓
- Limitación conocida confirmada: una suite scripted no puede dar respuestas DISTINTAS a base y correctivo del mismo target (duplicado = error de carga, `script.go:100-102`). **F-6:** las entradas `:corrective` de `scenarioMalformed` (`v2_pipeline_test.go:212-215`) son claves muertas — ningún correctivo (ni SKO review ni recon) cambia el marker.

**AC1.4 contra los fixtures P7 reales (F-1, hallazgo principal):** el `replay/script.json` exportado en P8 (1391 entradas, prioridad VALIDATED) trae para los 9 records respuestas en formas toleradas (9/9 verificadas parseables, veredicto SUPPORTED) pero para `cl-intraturtlesoup-open-pnl-label@1` trae una **entrada de ERROR fatal** (`class: fatal, parse-structured`), no su 1.er intento (v1+`@1`, que el validador nuevo SÍ acepta). El replay grabado del P7 con binario remediado rinde **+9 SUPPORTED, no +10**: ese record sólo se recupera live en R5. El «+10» de diseño §1.3/AC1.4 no es alcanzable con el fixture-set existente.

---

## Ataque 6 — Suites

| comando | resultado |
|---|---|
| `go vet ./...` | exit 0, sin output |
| `go test ./internal/claims/... ./internal/pipeline/... ./internal/sko/... -count=1` | **ok / ok / ok — 0 FAIL** |
| desglose con `-v` (harness R3 temporal incluido y luego eliminado) | claims **24 PASS** (+2 R3 temporales) · pipeline **289 PASS, 1 SKIP** (+3 R3 temporales; 101s) · sko **10 PASS** (+1 R3 temporal) |
| SKIPs | exactamente 1: `TestV2PhysicalProvenanceTraceResolvesToSourceSHA` — skip ambiental preexistente (`MKE_V2_E2E_DIR`/`MKE_V2_E2E_MEDIA` ausentes), sin relación con el bundle. **Cero SKIPs nuevos, cero tests neutralizados.** |
| `gofmt -l` sobre los 13 archivos del diff `19b44c1..HEAD` | limpio (exit 0) |

Los números confirman exactamente los reportados por R2 (24/289+1 SKIP/10). Los experimentos R3 (19 fixtures de journal, 13 negativos, 2 replays scripted, split-validity R-M05, resume-parity) pasaron todos y fueron retirados; el árbol quedó sin modificaciones.

---

## Ataque 7 — Diff audit `19b44c1..HEAD`

13 archivos, +1549/−77, 7 commits. **Todo dentro del alcance del diseño:** Pieza 1 (`review.go` + `review_tolerance_test.go`), Pieza 2 (`review.go`, `records.go`, `records_test.go`), Pieza 3 (`records.go`, `v2_stages.go`, `v2_identity_remediation_test.go`), R-M05/R-M06 ya en base (`sko.go`, `v2_sko_stages.go`, tests de composition/reissue), R-1 (`87b1a92`, sólo función de test nueva), higiene gofmt (`e7bc387`: `v2.go` y `v2_reconstruction_reissue_test.go`, sólo alineación; la alineación del campo `PromptClaimsRecon` en `fingerprintDoc` es whitespace, no cambia el doc). Sin archivos fuera de alcance.

**Contrato/header que asumen validador y exporter:**
- `ReviewSchema` sigue congelado en `mke.claims-ground.v1` en las plantillas de salida de AMBAS ramas y en el correctivo; `OutputSchemaID: ReviewSchema` intacto (`review.go:207/223/246/258`). El header deja de tener forma de schema id (`calibration-3`), eliminando el inductor; el conjunto de tolerancia NO incluye v3.
- `PromptVersionReconstruct` v4 se renderiza en `task_contract` y entra al fingerprint vía `fingerprintDoc` (constantes, no literals); `EffectivePromptVersionClaimsGrounding` usa v3 por defecto y **el config del rerun (`configs/config.rerun.v2.json`) no trae override de prompt** → R5 corre v3/v4.
- Ningún cambio en `internal/knowledge` (gate V1 intacto), `internal/recorded` (reglas de clave intactas), ni en el exporter.
- Vocabulario congelado (verdicts, publication states, schema ids de payload): intacto.

---

## Tabla de hallazgos

| # | Severidad | Título | Evidencia | Impacto | Fix mínimo |
|---|---|---|---|---|---|
| F-1 | **MAJOR** | El replay grabado del P7 rinde +9, no el «+10» de AC1.4: el fixture de `cl-intraturtlesoup-open-pnl-label@1` es una entrada ERROR-fatal | `replay/script.json` (entrada con `error.class=fatal`); 9/9 restantes verificados parseables; parser real acepta su 1.er intento (`eef5fd64…`, v1+`@1`) | Si R6/R3-ejecutor corre AC1.4 tal cual, fallará a 9 y dispararía una re-remediación innecesaria; el record sí se recupera live en R5 | Re-acotar AC1.4 a «+9 en replay grabado; el +1 (intraturtlesoup) se observa sólo en R5 live», o re-exportar el fixture prefiriendo respuestas REJECTED-parseables sobre entradas de error |
| F-2 | **MAJOR** | AC2.2/2.3/2.4 asignadas a R3 exigen inferencia del modelo; el mandato R3 es offline → los dientes del anti-rubber-stamp no tienen EVIDENCIA conductual, sólo textual (probe) | `grounding-audit.jsonl` (8 ACTUALLY_CONTRADICTED + 7 CORRECT_REJECTION); probes sólo assertean strings (`records_test.go:220-282`); sin acceso a provider en R3 | El gate M-07b (FN ≤10%) y el riesgo rubber-stamp quedan sin medir hasta R5/R6; un v3 sello no sería detectado antes | Reasignar AC2.2-2.4 a R5/R6 (solapan AC2.5/safety P8) o proveer harness LLM antes de R5; explícitar en el plan que R3 las declara NO-EJECUTABLES offline (hecho aquí) |
| F-3 | MINOR | AC1.1 no quedó pineado en-repo con los fixtures exactos del journal (ids de invocation); R2 usó formas representativas | `review_tolerance_test.go:35-56` (fixtures sintéticos); fixtures reales vivieron sólo en el harness temporal de esta sesión (eliminado) | El testsuite no detectaría una regresión futura del validador contra los bytes reales del P7 | Commitear (post-aprobación) el table test con los 19 pares (invocation_id → raw response) como testdata |
| F-4 | MINOR | Resume tras crash entre base-reject y terminalización del correctivo descarta un correctivo VALIDADO (asimetría con el camino de grounding) | `v2_stages.go:330-337` (short-circuit en base REJECTED sin consultar el correctivo) vs `strictClaimReview` (`:1216-1219`) | Yield perdido (ventana rechazada teniendo respuesta válida en journal); fail-closed, determinista, ventana de crash estrecha | En el short-circuit de resume, consultar la fila del correctivo (identidad derivable) antes de rechazar la ventana |
| F-5 | NOTE | Bordes de tolerancia: dígitos del sufijo `@N` no se contrastan con la versión (`cl-x@7`, `@01`, sufijos enormes se aceptan; el campo `version` es el gate) | `normalizeRecordAddress` (`review.go:94-99`); experimento BOUNDARY | Inofensivo (binding real = id+version; charset de ids prohíbe `@`); amplía marginalmente la superficie aceptada más allá de las formas P7 | Documentar la frontera en la taxonomía de auditoría R6; opcional: exigir `@%d==t.Version` si se quiere cerrar |
| F-6 | NOTE | Claves de script `:corrective` muertas: ningún correctivo cambia el target marker (ni SKO review ni recon) | `v2_pipeline_test.go:212-215`; `correctiveReconstructionRequest` y `correctiveCompositionReissue` sólo apendan al System | Confusión futura: un script que asuma marcadores distintos para diferenciar respuestas no se comportará como cree (la entrada `:corrective` jamás se consulta) | Corregir el fixture de `scenarioMalformed` y documentar en REPLAY-AUDIT que base y correctivo comparten clave por diseño |
| F-7 | NOTE | Causa terminal grabada dependiente del timing de crash: crash pre-terminal deja el PRIMER defecto como causa de ventana tras resume (vs SEGUNDO en run íntegro) | `rejectInvocationDetailV2(base, second)` sólo corre si no hubo crash; experimento resume-parity sin crash PASS | Paridad R-MI04 se mantiene para la causa grabada al momento del crash; ambas caen en REJECTED cerrado | Ninguno obligatorio; documentar como clase de divergencia aceptada |
| F-8 | NOTE | Deuda preexistente (no del bundle): el resume de grounding reviews usa placeholder genérico como primer defecto cuando ambos intentos quedan rechazados | `v2_stages.go:1216-1218` (`fmt.Errorf("…rejected in a previous attempt")`) | Sólo texto de reasons; la categoría terminal es idéntica (UNSUPPORTED_INSUFFICIENT/reviewer_malformed_output) | Mismo patrón que R-MI04-recon: grabar el primer defecto en la fila base (ya se hace en-run) y leerlo en resume |

**Conteo: BLOCKER 0 · MAJOR 2 · MINOR 2 · NOTE 4.**

---

## Veredicto por pieza

| Pieza | Veredicto | Base |
|---|---|---|
| 1 — Tolerancia validador (`6932d12`) | **CONFORMS-WITH-FINDINGS** | 19/19 respuestas reales del journal parsean al veredicto emitido; 13+15 negativos fail-closed; conjunto cerrado {v1,v2} sin patrones; colisión cross-record imposible. Findings F-1 (bookkeeping AC1.4), F-3 (pineo AC1.1), F-5 (bordes) |
| 2 — Reviewer v3 (`0937e76`) | **CONFORMS-WITH-FINDINGS** | Textos verbatim del diseño en ambas ramas + anti-rubber-stamp; header des-anclado; probes completos. Finding F-2: sin evidencia conductual hasta R5/R6 (AC2.2-2.4 no ejecutables offline) |
| 3 — Recon v4 (`6b3770d`) | **CONFORMS** | 3 reglas verbatim, regla de niveles v3 reemplazada no-coexistente, fusible atomicity dentro de la regla de negaciones; riesgos de over-suppression/sobre-omisión de dirección conocida y medibles en R6 (AC3.5/3.6); sin explosión estructural |
| 4 — R-M05/R-M06 verificación | **CONFORMS-WITH-FINDINGS** | Todas las falsificaciones sobreviven: duplicado partida-validez descarta ambas; 0-válidos rechaza cerrado; sin ciclo ni doble cobro; R-1 fold/cap con anti-inyección; R-MI4 resume-parity verificada experimentalmente; scripted-replay del correctivo viable en ambas direcciones (AC4.3 ✓). Findings F-4, F-6, F-7 (notes) |

**Veredicto global: el bundle NO fue falsificado — 0 BLOCKER, 0 defectos de permiso indebido o de fail-closed. Los 2 MAJOR son de contabilidad de aceptación/re-plan (F-1, F-2), no de código: resolverlos es re-acotar ACs y re-asignar verificación, no re-programar. El bundle está listo para R5 con F-1 y F-2 resueltos a nivel de plan.**

---

## FEEDBACK (Agents-OS)

1. **La ruta de verificación por fase volvió a funcionar, pero AC1.4/AC2.2-2.4 eran parcialmente in-ejecutables tal como estaban redactadas:** AC1.4 presupone un comportamiento del exporter (elige el 1.er intento de un target all-rejected) que el fixture real contradice, y AC2.2-2.4 presuponen acceso a inferencia que un R3 read-only no tiene. Sugerencia: cuando un AC de R3 dependa de artefactos de fases previas (fixtures exportados) o de LLM, marcarlo «R3-con-condiciones» y listar la condición en la columna Verificable por; hubiese ahorrado descubrir F-1/F-2 por la vía adversarial.
2. **El journal como fuente de fixtures es frágil de un solo lado:** `response_json` es byte-fiel (persistió `resp.Structured` crudo) — eso hizo AC1.1 trivial y concluyente. Pero el exporter de replay YA tomó decisiones irreversibles sobre qué respuesta representa cada target (error-fatal en vez del 1.er intento rechazado), y esa decisión condiciona qué fixes son "observables" en replay. Sugerencia: que el exporter grabe por target TODAS las respuestas del historial (o al menos 1.er intento + última) en vez de 1-fixture-por-clave, y que la selección sea una política del consumidor, no del exportador.
3. **`sqlite3` CLI sigue ausente (4.ª mención); Python funcionó de nuevo.** El patrón ya es estándar de facto en la campaña; formalizarlo en el doc de campaña evitaría que cada fase lo re-descubra.
4. **Los harness adversariales desechables funcionan bien con la disciplina de limpieza:** crear test temporal dentro del paquete → correr → borrar → `git status` limpio. Sugerencia para el loop: explicitar en el brief de R3 que esto está permitido (lo estuvo implícitamente aquí vía "puedes correr tests"), porque es la única forma de ejercitar `internal/` desde fuera del módulo.
5. **N-10 (gobernanza) sin cambio:** `wt/` sigue sin rastrear y sin dueño documentado; las sugerencias de R1/R2 (ADOPTIONS.md + registro del estado del worktree en el vault) siguen vigentes y sin mecanismo.
6. **Detalle útil para R6:** la tabla de hallazgos de esta sesión distingue «frontera de tolerancia» (F-5) de «clase terminal» — cuando R6 cuente la clase malformed-verdict, conviene mantener la distinción entre records recuperados (SUPPORTED), records con contenido genuinamente inválido (rechazo correcto) y records con drift de forma no tolerado (rechazo + reissue + auditable), porque los tres coexistirán en R5.
