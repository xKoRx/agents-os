# P7 — Remediation Round 2: REVISIÓN ADVERSARIAL INDEPENDIENTE (R-M05 / R-M06)

- **Rol:** REVIEWER ADVERSARIAL INDEPENDIENTE (contexto fresco, ronda 2)
- **Fecha:** 2026-10-03
- **Repo:** `/home/kor/mke/multimodal-knowledge-engine`, branch `feature/v2-layered-knowledge-model`
- **Baseline declarado:** HEAD `edec9a8` (R-M05 `8ae543a` + R-M06 `edec9a8` sobre `19b44c1`)
- **HEAD real al revisar:** `6932d12` — un commit adicional (`R-M07`, tolerancia de schema de grounding review) que no toca ninguno de los dos frentes revisados. Ambos commits objetivo están presentes y sin modificar. `git status` limpio (read-only; sin commits; harnesses en `/tmp`).
- **Método:** lectura completa de `internal/sko/sko.go` (`ValidateCompositionPerObject`, `CompositionRejectionMessage`, `ValidateComposition`), `internal/pipeline/v2_sko_stages.go` (caller L2), `internal/pipeline/v2_stages.go` (`correctiveReconstructionReissue`, `correctiveReconstructionRequest`, ladder de identidad), helpers (`invokeV2`, `rejectInvocationDetailV2`, `ClaimByID`, `SanitizeDetail`, `RequestIdentity`, presupuesto `checkLimitTx`) — más **6 tests de ataque puntuales** vía `go test -overlay` desde `/tmp`. La suite completa NO se re-ejecutó (verificada 20/20 por el Manager); sólo se re-corrieron los tests existentes de las áreas atacadas como control de no-regresión.

---

## Veredicto

```
R2_ADVERSARIAL       = FINDINGS
READY_FOR_FULL_RERUN = YES
```

0 CRITICAL, 0 MAJOR, 1 MINOR (reproducido físicamente), 6 NOTE. El MINOR no afecta la corrección del conocimiento publicado ni bloquea el rerun completo: es una fuga de una reserva de presupuesto en la ventana de crash del correctivo R-M06, acotada a 1 `vlm_call` por ocurrencia.

---

## Hallazgos

### CRITICAL — ninguno

### MAJOR — ninguno

### MINOR

#### F-1 (R-M06): crash durante el correctivo deja una reserva de presupuesto huérfana que el resume nunca libera

- **Repro:** test `TestAdvRM06CrashDuringCorrectiveResumeIsTerminalWithDefect1` (overlay, `/tmp/mke-r2-adv/pipeline_attack_test.go`). Simula: base de `w1-theory` inválida → `rejectInvocationDetailV2(base, defect1)` (durable) → el `Infer` del correctivo entra en panic (crash). Se inserta a mano la respuesta correctiva VÁLIDA como `PERSISTED` (lo que un crash 1 ms después habría dejado) y se resume con proveedor sano.
- **Observado (3 efectos, 2 por diseño, 1 defecto):**
  1. **Por diseño (correcto):** el resume corta por la fila base `REJECTED` → ventana terminal con **defect 1** re-proyectado, cero llamadas de reconstrucción para `w1` (ni re-intento base ni re-ejecución del correctivo: el loop de reissue es imposible también a través del resume).
  2. **Por diseño (correcto):** la respuesta correctiva válida huérfana nunca se decodifica (`cl-orphan` no se publica; la fila queda `PERSISTED` intacta). La ventana queda cerrada honestamente.
  3. **DEFECTO:** la reserva `vlm_call` del correctivo (hecha en `invokeV2` antes del `Infer`) queda **pendiente para siempre** — el resume jamás invoca `corrID` de nuevo, así que ni `ReleaseReservations(corrID)` ni `SettleReservation` la tocan. Log del test: `FINDING: stale reservation for the crashed corrective stays pending after resume (1 rows)`.
- **Impacto cuantificado:** `checkLimitTx` (`internal/runstate/budget.go`) computa `reserved + consumed` contra el límite duro → la fila huérfana consume 1 slot de `vlm_call` del presupuesto del run resumido y de cualquier resume posterior. Con presupuestos por defecto el efecto es marginal; con presupuesto ajustado, una llamada fantasma por crash.
- **Por qué es R-M06-específico:** antes de R-M06 el mismo crash dejaba reservas huérfanas sólo para invocaciones que el resume **sí re-invoca** (`invokeV2` libera las reservas stale de su propio `invocationID` al empezar) → la fuga se auto-reparaba. El correctivo introduce la primera invocación que el resume nunca vuelve a tocar.
- **Fix sugerido (no aplicado):** liberar las reservas de `corrID` cuando la ventana se rechaza terminal en el resume, o barrido de reservas stale al inicio del resume (ya existe `reconcile.go` con `ReleaseReservations` por efecto — extender el barrido a claves de invocación no re-ejecutables).

### NOTE

#### N-1 (R-M05): ataque de inyección en reasons — REPELIDO (defensa verificada)
`TestAdvRM05ReasonInjectionSurface`: ids de objeto/claim/kind hostiles (`"sko-x\";\nDROP ALL--"`, `"cl-x\";UNION--"`, `"Rule!\n; drop table"`) quedan en `CompositionDiscard.Detail` siempre vía `%q` (escapado Go-literal, una sola línea) o, cuando van con `%s`, sólo después de pasar la validación de charset (`validSKOID`/`validClaimID` no admiten metacaracteres). `CompositionRejectionMessage` se mantiene monolínea con la forma histórica. No hay superficie de inyección hacia reasons/proyecciones (y la causa nunca re-entra a un prompt — `compositionRejected` sólo aterriza en `sko/composition.jsonl`, verificado en `v2_projections.go:476`).

#### N-2 (R-M05): `ValidateComposition` (gate atómico viejo) sin uso en producción
`grep` sobre `internal/`+`cmd/`: cero callers fuera de `sko_test.go`. Además hoy es un wrapper del propio gate por-objeto (`sko.go:300-306`), así que no existe doble estándar ni path con semántica vieja.

#### N-3 (R-M05): pass-through estructural de claim stale/superseded/no-soportada es diseño, y el guard posterior existe
`ClaimByID` resuelve cualquier versión exacta, incluidas superseded (`records.go:361`). El gate estructural las deja pasar (por diseño: "semantic support is judged by the later stages"); `reviewCompositionOne` las degrada con `component_stale`/`component_unsupported` → `INSUFFICIENT` (`v2_sko_stages.go:183-207`). Verificado por lectura + test (`TestAdvRM05ExactVersionAndSupersededPassThrough`: versión inexistente sí descarta con el wording exacto `does not exist at that exact version`).

#### N-4 (R-M05): determinismo verificado también en la esquina de ids inválidos duplicados
`TestAdvRM05DuplicateInvalidCharsetIDsDeterministic`: dos ocurrencias del mismo id que falla charset se descartan indexadas (`object 0:`/`object 2:`) y el sort canónico `(ObjectID, Index)` las estabiliza; los tests existentes ya cubren el caso id válido duplicado y el shuffle de orden.

#### N-5 (R-M06): drift de texto de causa entre fila base y causa terminal cuando el correctivo valida y la ventana se rechaza después
`TestAdvRM06ValidCorrectiveThenDivergentCommitRejectsWindowOnce` (repro físico): correctivo VÁLIDO cuyo commit cae en divergencia determinista de identidad → **sin segundo reissue** (exactamente 2 llamadas, 1 correctiva), ventana `REJECTED` con `InvocationID = corrID` y causa de divergencia, run continúa a L2 y termina INCOMPLETE, w1 publicado. Residuo (aceptable): la fila base queda `REJECTED` con defect 1 mientras la fila del correctivo queda `VALIDATED` — la causa terminal (divergencia) vive sólo en la window row/reasons. Como un run INCOMPLETE no admite resume (`allocatePipelineRunDirV2` exige status RUNNING), jamás se re-proyecta la causa equivocada; y si hay crash posterior, defect-1 es el estado durable honesto. Categoría R-MI04 preservada (ambas son "output rejected"); sólo el texto difiere.

#### N-6: cobertura existente confirmada como control de no-regresión
Re-ejecutados (verde): paquete `sko` completo (incluye los 4 tests R-M05), y en `pipeline` los `TestV2Reconstruction*` (R-M06 worker+manager, presupuesto 1:1 en ledger por label `w1-theory` / `w1-theory:corrective`), `TestV2Composition*` (discard parcial VALIDATED, all-invalid REJECTED canónico, proposal vacía histórica) y `TestV2CatalogBudgetBoundsFullPresentedCatalog` (G-01/G-02 intactos: el gate de presupuesto precede a cualquier llamada y el reason nombra el valor real configurado, sin punteros; R-M05 no tocó ese path). Provenance de SKOs publicados = invocación de composition (`v2_sko_stages.go:125`); provenance de records del correctivo = invocación correctiva (test existente lo assertiona).

---

## Matriz de ataques

| # | Frente | Ataque | Resultado |
|---|--------|--------|-----------|
| 1 | R-M05 | claim existe pero `version≠1` | Descarta con wording exacto; versión existente (incl. superseded) pasa estructural y la degrada el stage de review (N-3) |
| 2 | R-M05 | componente duplicado intra-objeto; ordinal duplicado; 0 componentes; nombre/kind/rol vacíos | Descartan per-objeto (tests existentes + N-4) |
| 3 | R-M05 | dos objetos con mismo SKO id (válido e inválido charset) | Todas las ocurrencias descartadas, sin resolución por orden de array; determinismo canónico |
| 4 | R-M05 | SKO id inválido (charset) | Descarta indexado, id crudo `%q`-escapado |
| 5 | R-M05 | inyección de reason desde el composer | **REPELIDO** (N-1): `%q` + charset-first |
| 6 | R-M05 | orden determinista de discards bajo shuffle | Estable por (id, posición) |
| 7 | R-M05 | doble estándar con gate viejo | Ninguno (N-2) |
| 8 | R-M05 | caller: VALIDATED parcial / REJECTED total / vacía; provenance; G-01/G-02 | Correcto (tests existentes verdes + lectura) |
| 9 | R-M06 | loop de reissue (in-run y vía resume) | Imposible: el correctivo nunca recursa; el resume corta en base REJECTED (0 llamadas w1 en repro físico) |
| 10 | R-M06 | identidad content-addressed = función pura (base, defect) | Sí: defect determinista (ValidateProposal array-order/first-error; decode estricto); identidad distinta assertionada por tests existentes |
| 11 | R-M06 | crash DURANTE el correctivo → resume | Terminal defect-1, huérfana nunca se publica, **F-1: reserva de presupuesto leaked** |
| 12 | R-M06 | defect FATAL dispara reissue indebido | No: reissue sólo entra por errores de decode/validate (validación pura); FATAL de provider se clasifica antes (`claimsReconstructionFailure`) y dentro del reissue (`ClassFatal` → retorno/fatal) |
| 13 | R-M06 | provenance y presupuesto del correctivo | Provenance = corrID; 2 invocaciones cobradas 1:1 (ledger por label) |
| 14 | Interacción | correctivo válido → ladder DIVERGENT | Sin segundo reissue, sin crash; ventana rechazada con corrID; run continúa; R-M05 cierra la proposal vacía de forma atómica (N-5) |
| 15 | Interacción | G-01 over-budget + R-M05 | Reason literal intacta, 0 llamadas composer, sin discards (path previo al gate) |

---

## Comandos y outputs

```bash
# Ataques R-M05 (package sko, overlay)
cd /home/kor/mke/multimodal-knowledge-engine && \
  go test -count=1 -overlay /tmp/mke-r2-adv/overlay-probe.json -run 'TestAdvRM05' ./internal/sko/
# → ok  mke/internal/sko  0.006s   (4 tests: pass-through exact-version/superseded,
#   inyección REPELIDA, determinismo ids inválidos duplicados, vacías/ordinales)

# Ataques R-M06 (package pipeline, overlay)
cd /home/kor/mke/multimodal-knowledge-engine && \
  go test -count=1 -overlay /tmp/mke-r2-adv/overlay-pipeline.json -v -run 'TestAdvRM06' ./internal/pipeline/
# → PASS TestAdvRM06CrashDuringCorrectiveResumeIsTerminalWithDefect1
#      zz_adv_attack_test.go:203: FINDING: stale reservation for the crashed
#      corrective stays pending after resume (1 rows)
# → PASS TestAdvRM06ValidCorrectiveThenDivergentCommitRejectsWindowOnce
#      zz_adv_attack_test.go:273: divergence projected: "window w2-exception: claims
#      reconstruction output rejected: record cl-close-inside@1 identity collision:
#      kind differs (claim vs rule) ...; deterministic divergence, window rejected
#      closed without an equivalence review"
# → ok  mke/internal/pipeline  0.106s

# Control de no-regresión de las áreas atacadas (tests existentes)
go test -count=1 ./internal/sko/                                    # → ok
go test -count=1 -run 'TestV2Reconstruction|TestV2Composition|TestV2CatalogBudget' ./internal/pipeline/
# → ok  mke/internal/pipeline 0.699s
```

Harnesses (borrables): `/tmp/mke-r2-adv/{sko_attack_test.go,pipeline_attack_test.go,probe_test.go,overlay-*.json}`. Repo sin modificaciones (`git status` limpio, sin commits).

---

## Conclusión

Las dos remediaciones resisten el ataque. R-M05 compone exactamente lo que promete (descarte per-objeto con reasons durables canónicas, inyección-repelente, preservando el gate atómico para all-invalid y el presupuesto G-01/G-02), y R-M06 entrega exactamente un reissue content-addressed con provenance y cobro propios, sin loop, sin FATAL indebido, con paridad R-MI04 en las filas durables. El único defecto nuevo reproducido (F-1, MINOR) es la reserva de presupuesto huérfana tras crash-en-correctivo: acotado, honesto, no bloquea el rerun completo — queda apuntado para la siguiente ronda de remediación.
