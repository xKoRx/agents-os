# R2 — COMMITS ADVERSARIAL (revisor adversarial independiente) · MKE V2 · Clutifx Chapter 01

**Fase:** R2-adversarial del remediation loop. Ataque al CONTENIDO de los 4 commits `0937e76` (grounding v3), `6b3770d` (recon v4), `87b1a92` (fold/cap defecto correctivo), `e7bc387` (gofmt-only), sobre base `6932d12` (ya revisada adversarialmente por otra sesión).
**Método:** contexto fresco, read-only sobre el repo (harnesses en `/tmp/r2adv/` via `go test -overlay`; cero archivos escritos en el repo), sin ejecutar la suite completa. Ataques = lectura de código + diffs + probes físicos propios.
**Base verificada:** HEAD `e7bc387`, branch `feature/v2-layered-knowledge-model`, `git log` cuadra con el reporte R2. GO: go1.27.1.

```
PHASE = R2-ADVERSARIAL
R2_COMMITS_ADVERSARIAL = FINDINGS
READY_FOR_FULL_RERUN = YES
```

Veredicto en una línea: **los 4 commits hacen lo que dicen, no se encontró ningún CRITICAL/MAJOR; 2 MINOR con repro físico y 5 NOTE — ninguno bloquea el R5 full rerun.**

---

## Resultados de los frentes de ataque

### Frente 1 — Prompt recon v4 (`6b3770d`): SOBREVIVE, con 2 notas

**1.1 PASS — Las 3 reglas nuevas viajan en el request FÍSICO y no contradicen las reglas congeladas.** Probe físico (`TestAdvReconV4PhysicalCoexistence`, overlay sobre `internal/pipeline/`): capturado el request real de `buildClaimsReconstructionRequest` vía `RunV2`+probe; verifica coexistencia de: regla negaciones («never fold it into the affirmative claim it corrects» + carve-out «stays inside its claim, per the ATOMICITY rule» en la MISMA bala), regla forward-reference, regla de rol, y TODOS los supervivientes v3: idioma fuente, id estable/kind por contenido, EQUIVALENT_TO restringido, epistémicas prohibidas, citación exacta de ids con «never an id from another window», y «transcribed exactly as labeled» (conservada DENTRO de la regla de rol nueva; la línea v3 «Levels, targets, entries and stops shown on screen» ausente). Los probes del repo (`TestV2IdentityRequestContractPhysical`, `TestV2IdentityEquivalencePromptParticipatesInFingerprints`) pasan pineando v4 — **sin aserciones huérfanas**: ningún test del repo pineaba la línea v3 eliminada; el pin P4 «transcribed exactly as labeled» sigue satisfecho dentro de la regla (c).

**1.2 PASS — Forward-references NO puede producir refs fuera de ventana.** La regla (b) ordena capturar el binding «quoting the anchor content» de ESTA ventana y «do not invent the future topic's content»; no ordena citar segmentos futuros. El gate duro preexistente («Every claim… cites at least one evidence id… never an id from another window» + `checkedClaimStatement` → `rc.HasRef`) rechaza cualquier ref inválida → corrective reissue, no corrupción silenciosa. No hay contradicción con «Cite every transcript segment needed…» (una regla es de citación, la otra de emisión).

**1.3 NOTE — Tensión interna en la regla (a) para el caso-límite.** La misma bala dice «Never drop a negation… never fold it into the affirmative claim it corrects» y, tres frases después, «A clause that only restricts the same single proposition… stays inside its claim». Para el solape (una negación que SÓLO restringe la proposición afirmada) el modelo recibe dos señales opuestas. Mitigado por el ejemplo explícito «tampoco tiene que ser negativa como tal» (el caso w0010 que motiva la regla) y por el cierre «per the ATOMICITY rule». Es texto verbatim del diseño §3.2a. R5 debe mirar si las negaciones-límite se pliegan u omiten (no gate-blocking).

**1.4 NOTE — Inflación de claims no tiene tope por ventana; el presupuesto es de llamadas, no de claims.** `ValidateProposal` no impone límite de cardinalidad; `runstate.BudgetLimits` sólo limita requests/imágenes/tokens/wall-clock. La regla (a) puede inflar el conteo de claims en ventanas con muchas negaciones → más invocaciones de review (~1/claim) y más tokens. La estimación transversal del diseño («~1.3KB/request ≈ <2%») mide tamaño de request, NO crecimiento de claim-count. Si R5 hereda un presupuesto cerrado del run P7 (1618 invocations), verificar headroom; con budget ilimitado el riesgo es nulo. (No es defecto de los commits: es condición de carrera del runbook R5.)

**1.5 NOTE — Regla (c) ejecutabilidad.** La verificación por rol es la regla más larga del bloque («an objective/target number comes from the declared target… OMIT the role assignment instead of picking a number»): es una instrucción de decisión bajo incertidumbre sin criterio operativo de «declared target» distinto del ejemplo. Es exactamente el refuerzo pedido por M-09 (w0037) y va en la dirección correcta; su eficacia es empiriable sólo en R5/R6 (AC3.4/AC3.6 del diseño).

### Frente 2 — Prompt grounding v3 (`0937e76`): SOBREVIVE, con 1 minor

**2.1 PASS — Header `calibration-3` no rompe ningún consumer.** (i) Ningún código parsea la línea `review_contract` (sólo la renderizan: `claims/review.go:159`, `knowledge/grounding.go:128` — V1 con `knowledge.grounding_review`/`mke.ground04.v1`, namespace distinto e intacto; `equivalence.go:72` y `sko/review.go:72` usan sus propios tokens, no tocados). (ii) Ningún test pineaba el header viejo `vmke.claims-ground.v2` (grep sobre tests: sólo el pin nuevo calibration-3 y los de equivalence/knowledge, que no cambiaron). (iii) `S2-J-03` (L2 fingerprint) liga provider/model, no el header — test en verde. (iv) La invalidación de fingerprint viaja por `EffectivePromptVersionClaimsGrounding()` → `mke.claims-ground.v3` (intencional, diseño §1.2.3); el override de operador `ClaimsGroundingPromptVersion` sigue funcionando (test P8 existente en verde). (v) `Request.PromptVersion` no se renderiza jamás en el cuerpo del prompt (sólo entra en `RequestIdentity`) → no crea un nuevo ancla por esa vía.

**2.2 PASS — Consistencia conjunto-cerrado {v1,v2} ↔ prompt v3: fail-closed se mantiene.** La instrucción de salida sigue fijando el schema congelado `mke.claims-ground.v1` (dos veces: texto + plantilla JSON inline) y el header ya no contiene token con forma de schema id. Ataque físico (`TestAdvCalibrationTokenEchoAsSchemaStaysMalformed`): una respuesta que ecuée «calibration-3» como campo `schema` **sigue siendo malformed** (fuera del conjunto cerrado) → rechazo + corrective (que nombra el schema explícito), nunca 0-parse ni tolerancia por patrón.

**2.3 PASS — Rama relations sigue sin atomicity (contrato) y ninguna guía nueva la menciona.** Verificado físicamente (`TestAdvRelationsBranchNoAtomicityHeaderDeanchored`): cero apariciones de «atomicity» (case-insensitive) en la rama relations; header calibration-3 presente; y `ParseReviewResponse` sigue rechazando atomicity en relations (test de tolerancia del repo en verde).

**2.4 MINOR (F-1) — Asimetría del contrapeso anti-rubber-stamp en la rama de CLAIMS.** La guía causal/definicional nueva viaja en AMBAS ramas, pero el contrapeso explícito «Two claims that merely co-occur without an enacted link stay GROUNDING_INSUFFICIENT» existe SÓLO en la rama de relations (verificado físicamente: `TestAdvBranchCounterweights` → relations=true, claims=false). En claims, el ancla insuficiencia es sólo la regla base («GROUNDING_SUPPORTED only when the cited evidence itself shows or states the statement») y el bloque de seguridad empuja a CONTRADICTED (no a INSUFFICIENT) ante mismatch de objeto/número/evento — no cubre el caso «transcript enuncia ambos hechos sin enactar el vínculo y el statement los une causalmente». Riesgo concreto de sobre-aceptación causal en claims: los listados «aun así»/«even when» (adversativas, no causales) como estructura enactante agrandan la superficie. Es texto verbatim del diseño §2.2 (la asimetría es del diseño, no del implementador) y los candados AC2.2 (15 rechazos correctos intactos) y AC2.4 (0 FP) de R3 existen exactamente para esto. **Acción R3 obligatoria:** incluir en los fixtures de falsificación un caso claims-branch de co-ocurrencia sin enacto (statement condicional citado a transcript que enuncia antecedente y consecuente por separado, sin «si…entonces» ni definición) y exigir INSUFFICIENT; si v3 lo aprueba, recortar los ejemplos «aun así»/«even when» de la guía causal en un bump puntual.

**2.5 NOTE (F-5) — La clase de ancla sólo se des-ancló en UN prompt de 3.** `equivalence.go:72` sigue renderizando `review_contract: claims.equivalence_review vmke.claims-equivalence-prompt.v1` (verificado físicamente) y `sko/review.go:72` su equivalente: tokens con forma de schema id al lado de gates de schema estrictos. La tolerancia de `6932d12` NO cubre el schema de equivalence (conjunto de 1). El corrective de equivalence existe (recuperación disponible) y P7/P8 no observaron eco de schema en esa task (N-08 muestra otras patologías), pero la misma clase de bug puede resurgir ahí. Fuera del diff de estos commits; observación para el backlog, no para R5.

### Frente 3 — `87b1a92` fold/cap: SOBREVIVE, con 1 minor reproducido

**3.1 PASS — Determinismo y pureza.** `foldRequestLine` = `strings.Join(strings.Fields(strings.ReplaceAll(s,"\r"," ")), " ")` — función pura, colapsa todo whitespace Unicode a un espacio. `correctiveReconstructionRequest` es función pura de (base, defecto); identidad estable verificada por el test del repo y por mi repro B3 (incluso con defecto whitespace-only). Los tests R-M06 preexistentes («names the exact defect», `TestV2ReconstructionCorrectiveReissueRecovers`, `TestV2CorrectiveReissueCarriesFullContract`) pasan SIN modificación: los defectos cortos de una línea viajan byte-idénticos.

**3.2 MINOR (F-2) — El cap 300 puede cortar un rune multi-byte y embutir UTF-8 INVÁLIDO en el system del correctivo.** `providers.SanitizeDetail` corta por BYTES (`s[:max]`). Repro físico end-to-end (`TestAdvCorrectiveReconMidRuneTruncation`): defecto cuyo byte 300 cae dentro de « → el System del correctivo queda `utf8valid=false` (`tail="…aaaaaaaaaa\xc2…[truncated]"`). El texto del defecto SÍ puede contener multi-byte en producción: los refs/valores citados por el modelo son controlados por el modelo y `%q` preserva Unicode printable («objétivo», ids con acentos). Consecuencias verificadas por lectura de código: no crashea — `mustMarshalJSON` (openrouter) coerced los bytes inválidos a U+FFFD, y `request_json` persiste la forma coerced — pero el modelo recibe mojibake y los artefactos de auditoría lo preservan. Determinista y fail-safe; **arreglo de 1 línea sugerido** (no bloqueante): cortar por runas o `strings.ToValidUTF8` antes del marker. Clasificado MINOR por frecuencia esperada (requiere defecto >300 bytes con rune justo en el borde) y por no afectar fail-closed.

**3.3 NOTE — El cap 300 degrada «names the exact rejection cause» a «names a prefix».** Repro (`TestAdvCorrectiveReconCapCutsNeededField`): un defecto con campo desconocido de 400 chars llega con el nombre del campo CORTADO (full-field-visible=false). Los productores actuales de defectos son fail-fast de una sola violación con el id del record temprano en el mensaje (los primeros ~300 bytes casi siempre bastan), y el modelo ve su propia respuesta previa (el dato discriminante es re-derivable), así que el caso es patológico. El diseño LO ACEPTA explícitamente (AC4.2: «defecto >300 chars llega plegado/acotado»): documentación del borde, no defecto.

**3.4 NOTE — Defecto 100% whitespace → causa vacía.** Repro B3: `errors.New(" \n\t ")` produce «The exact rejection was: \n» (causa vacía). Ningún productor actual construye errores vacíos/whitespace (todos los `fmt.Errorf` llevan texto fijo no vacío); cosmético.

**3.5 NOTE — El fold impide forjar LÍNEAS, no texto inline.** Un defecto puede contener literalmente `Hard rules: - …` en UNA línea plegada, que imita estructura sin crearla. Es la mitigación que el diseño eligió (líneas, no semántica); el texto inyectado queda marcado dentro de «The exact rejection was: …». Aceptado por diseño; sin acción.

### Frente 4 — Coherencia global: SOBREVIVE

- **PASS — Sin reglas duplicadas/conflictivas entre v3-heredadas y v4-nuevas** en el request físico (probe 1.1): negaciones↔ATOMICITY tienen carve-out explícito mutuamente citado; forward-reference↔citación por deixis no se pisan; regla de rol absorbe a la de niveles sin dejar las dos.
- **PASS — `e7bc387` es whitespace-only REAL**: `git show -w` arroja 0 líneas +/-; sólo alineación de comentarios/const en `v2.go` y `v2_reconstruction_reissue_test.go`. Los probes R-M05/R-M06 pasan sin cambios semánticos.
- **PASS — Probes del repo en verde** (`go test ./internal/claims/ -run 'Contract|Probe|Prompt|Reissue|PerObject|Tolerance' -count=1 -v`: 24 subtests PASS; idem en `./internal/pipeline/`: 29 PASS, incl. `TestCorrectiveReconstructionRequestFoldsAndCapsDefect` 4/4). Paquete `./internal/claims/` completo: ok.

---

## Tabla de findings

| # | Severidad | Commit | Finding | Repro | Acción |
|---|---|---|---|---|---|
| F-1 | MINOR | 0937e76 | Rama claims: guía causal sin contrapeso INSUFFICIENT de co-ocurrencia (sólo relations lo tiene) → superficie de sobre-aceptación causal en claims | `TestAdvBranchCounterweights` (overlay) | R3: fixture de falsificación claims-branch co-ocurrencia-sin-enacto (AC2.2/AC2.4); si falla, recortar «aun así»/«even when» en bump puntual |
| F-2 | MINOR | 87b1a92 | Cap 300 corta por BYTES: rune multi-byte en el borde → UTF-8 inválido en el system del correctivo (downstream coerced a U+FFFD; sin crash, determinista) | `TestAdvCorrectiveReconMidRuneTruncation` end-to-end | Corte por runas o `ToValidUTF8` (1 línea, no bloqueante) |
| N-1 | NOTE | 6b3770d | Tensión interna regla negaciones (never-fold vs carve-out) para el caso-límite; ejemplo explícito mitiga | lectura + probe físico | Observar en R5 (folds de negaciones-límite) |
| N-2 | NOTE | 6b3770d | Sin tope por ventana de cardinalidad de claims; inflación por regla (a) come headroom de budget de llamadas/tokens de R5 | `runstate/budget.go`, `ValidateProposal` | Runbook R5: budget ilimitado o headroom ≥ +20% invocaciones |
| N-3 | NOTE | 87b1a92 | Cap 300 degrada el defecto a prefijo en caso patológico (aceptado por diseño AC4.2); whitespace-only → causa vacía | 2 repros overlay | Ninguna (documentado) |
| N-4 | NOTE | (out-of-diff) | Equivalence y SKO review siguen con headers schema-id-shaped junto a gates estrictos — misma clase de ancla no des-anclada; tolerancia 6932d12 no cubre equivalence | `TestAdvSiblingEquivalenceHeaderStillSchemaShaped` | Backlog, no R5 |
| N-5 | NOTE | 0937e76 | Probe nuevo aserta «from the cited» (débil) en ambas ramas — el pin fuerte es por-guía; aceptable | lectura test | Ninguna |

## Lo que se atacó y NO cedió (verificado con repro)

1. Eco de «calibration-3» como schema de respuesta → sigue malformed (fail-closed, corrective con schema explícito).
2. Ninguna vía de citación fuera de ventana nueva en v4 (regla forward-ref acotada + gate exact-id + reissue).
3. Ninguna aserción de test huérfana por la regla de niveles eliminada (pin «exactly as labeled» sobrevive dentro de la regla (c); «Levels, targets…» ausente del request físico).
4. Header nuevo no rompe consumers: sin parser del header; V1 (`mke.ground04.v1`) intacto; S2-J-03 intacto; fingerprints invalidan por la vía diseñada (`PromptVersionGrounding`/`PromptVersionReconstruct`).
5. Relations sin atomicity (contrato) tras añadir guías.
6. Determinismo/pureza del correctivo recon (identidad estable, tests R-M06 intactos y en verde).
7. `e7bc387` whitespace-only verificado (`git show -w` = 0 líneas).

## Veredicto

```
R2_COMMITS_ADVERSARIAL = FINDINGS
READY_FOR_FULL_RERUN = YES
```

Los 4 commits implementan fielmente el diseño R1 (textos verbatim, inserciones correctas, commits atómicos, tests nuevos sin tocar los existentes). Los 2 MINOR (F-1 contrapeso causal en claims — candado R3 obligatorio antes de adjudicar M-07; F-2 UTF-8 en el cap — arreglo de 1 línea opcional) no bloquean el R5: F-1 se falsifica con los fixtures AC2.2/AC2.4 ya planificados para R3, y F-2 es determinista, fail-safe y de frecuencia de borde. Ejecutar R3 con el fixture adicional de F-1 y registrar N-2 en el runbook de R5.

**Trazabilidad de los harnesses:** `/tmp/r2adv/zz_r2adv_claims_test.go` + `/tmp/r2adv/zz_r2adv_pipeline_test.go` (overlay: `/tmp/r2adv/overlay.json`, `/tmp/r2adv/overlay2.json`), ejecutados con `go test -overlay` — el árbol del repo quedó sin ninguna modificación (los únicos no rastreados, `wt/` y `internal/claims/zz_r3_adversarial_test.go`, son preexistentes de otras sesiones y no fueron tocados).
