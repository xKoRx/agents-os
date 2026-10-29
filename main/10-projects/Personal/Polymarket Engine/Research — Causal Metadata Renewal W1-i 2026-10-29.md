---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related:
  - "[[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]]"
  - "[[Plan — Single Episode Pilot v3 W1-i 2026-10-29]]"
  - "[[Research — Economic Pilot Corrections W1-h 2026-10-29]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
aliases:
  - "W1-i causal metadata renewal"
tags:
  - kind/doc
  - topic/research-ops
created: "2026-10-29"
updated: "2026-10-29"
---

# Research — Causal Metadata Renewal W1-i 2026-10-29

## Propósito

- Ejecutar la **opción B adjudicada por Metis** (prereg [[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]] §4): el contenido idéntico re-observado **renueva evidencia causal desde su NUEVA recepción** — no prueba estabilidad entre polls, no cambia el pasado, no reescribe first_seen — y dejar la receta temporal serial **V3** con deadlines absolutos lista para adjudicación. One-shot OFFLINE de implementación+pruebas+commit local sobre [[Polymarket Engine — Continuidad Five-POC 2026-09-20]]; excepción técnica acotada al freeze del checkout de investigación: **sin captura, sin live, sin cambio de estrategia, sin adquisición**. Estado al inicio: HEAD `853c0e46c9be2de4e84201e240e9cf8366b1036e`, rama `w0/offline-causal-replay-20261027`, árbol limpio salvo el fixture untracked de W1-h.

## Contenido

### 1. Estado final

- **Commit local** `9e2c6b7dd26e70a53b05499a2d682ef33f1dac27` ("Renew causal prospective metadata observations for research", base `853c0e4` intacta, sin push): 6 archivos, +1773/−14, árbol limpio post-commit.
- **Regresión final 6/6 PASS** sobre código final post-gofmt: `internal/regimes 1.675s`, `books 0.250s`, `replay 0.127s`, `capture 0.472s`, `experiment 16.850s` (incluye `^TestW1H` intacto), `cmd/engine 30.262s`. Build exit 0: `validated-baseline/w1-i-causal-renewal-20261029/engine`, sha256 `ba75bfb114c70c98aaf116a14513c93c58ec4644cc2c1a2773189027a22cb03b`.
- 12/12 inputs W1-h **nunca escritos**; sin red, sin requests a mercados, sin captura nueva. Recibos y hashes: OUT `evidence-manifest.json` + `test-receipt.md`.

### 2. Qué se envió (dentro de la allowlist)

- **`internal/regimes/renewal.go` (nuevo)** — política pura `EvaluateRenewedConstraint`: el gate AsOf se ancla en la **última renovación admitida bajo AMBAS cotas** (`received_wall ≤ t` **Y** `capture_seq ≤ seq`); renovación por **dimensión** (un re-poll de fee ni renueva ni borra el hecho de tick; unknown sigue unknown); **fail-closed** en seq=0, walls malformados y provenance ausente (seq 0 nunca cuenta, nunca se inventa); orden interno determinista (wall, seq, revision), independiente del orden de entrada; el veredicto porta la provenance del ancla que gobernó. **first_seen (revisiones) queda intacto**: contenido y observación son dimensiones distintas; jamás se lee `last_observed_at` hacia atrás.
- **`internal/regimes/prospect.go` + `service.go`** — **cuarentena AsOf con doble cota real, enviado hoy**: `regime_quarantine.quarantine_at` viaja al gate point-in-time; una cuarentena recibida con wall posterior a la decisión **no la contamina** (no-lookahead real, no comparación superficial); una marca sin wall queda admitida por secuencia (falla hacia suspect, nunca hacia limpieza falsa). Ambas políticas comparten `quarantineAdmittedAt`.
- **Tests del contrato** (15 nuevos): sondas puras (T0/T20→T16 stale aun tras procesar T20; T20 known con seq admitido; first_seen separado; empates wall/seq; wall regression; por dimensión; cuarentena PIT; malformed; determinismo bajo shuffle; ledger sin observación sintética) + integración sobre **store real** (persist+reducer+service): sondas W1-e invariantes, dedup sin renovar (baseline que la opción B cambia), **invariante no-lookahead de drain** (AsOf viejo nunca muta al drenar más records — detector de mutaciones) y el **contrato del ledger** que fijará el wiring.
- **Fixture W1-h `internal/experiment/w1h_acquisition_recipe_test.go`: committeada byte-idéntica** — SHA `f7c03a4829cae2d31e77bd68be80f1f2c389a18143182dce44d24152f3c0fa17`, exactamente el hash registrado en el prereg v2. **No se reescribió ninguna expectativa**: la semántica de producción no cambió en este shot (el wiring del ledger es el bloqueador declarado), así que la corrección 1 de W1-h sigue siendo verdad para el código enviado; la nueva semántica queda especificada y probada como contrato.

### 3. Bloqueador preciso (protocolo del mandato: acción/archivo/porqué, sin elusión)

- **Acción requerida:** crear `migrations/0025_regime_observations.sql` (rango de regimes 0020–0029, siguiente libre 0025) con el ledger inmutable `regime_observations(entity_id, revision, content_hash, capture_seq, received_wall, source_ref, capture_ref, provenance)` + índice `(entity_id, received_wall, capture_seq, id)`.
- **Porqué:** el contrato obligatorio exige **retener las renovaciones reales (plural) con provenance** y responder AsOf bajo doble cota sin mutar el pasado. Celdas mutables (`regime_revisions.observed_at`, `regime_entities.last_observed_at`) **no pueden**: con ≥3 renovaciones (T0/T10/T20) una decisión T16 obtendría STALE donde la verdad es FRESH vía T10 — exactamente los cortes retroactivos autorizados T−75/−45/−15. Demostrado y nombrado; elusión rechazada.
- **Por qué no se envió:** el hook del workspace deniega TODO acceso (lectura/escritura) a `migrations/` y el archivo no está en la allowlist comunicada. Enviar el wiring sin la tabla dejaría `record`/`replay` rotos ("no such table") — bug ordinario prohibido. **Lo que sí queda:** política completa probada + contrato fijado por `TestW1IRenewalLedgerContractFromJournal` + paso mecanizado en [[Plan — Single Episode Pilot v3 W1-i 2026-10-29]] §4 (SQL exacto y las tres ediciones del reducer/service, ~40 líneas).
- **Recibos no legibles:** `.private-execution/w1i/{source-paths.json, workspace-preflight.json, source-before/}` fueron denegados por el hook (lectura y listado); la allowlist se honró tal como fue comunicada en el mandato. El respaldo `source-before/` fue creado por el lanzador antes del shot (no re-verificable desde esta sesión).

### 4. Writer único y lock — decisión

- No existe **patrón compatible de locking** en el repo (foundation sin lock.go; persist sin exclusión de app; `capture.Open` sin exclusión entre procesos — defecto fijado por W1-h; `record` sin lockfile/O_EXCL). Por mandato: **no se implementó locking nuevo**; `internal/capture` quedó intacto y el fixture de writers concurrentes de W1-h sigue válido sin re-derivación. La exclusión es obligación del **supervisor de procesos propios** antes de cada paso (Plan v3 §5): verificar que no haya writer vivo ajeno sobre el data-dir y **fallar cerrado** ante writer desconocido; el límite (no es exclusión global entre procesos ajenos) queda documentado como bloqueo separado.

### 5. Receta V3 (resumen; especificación completa en el Plan v3)

- 6 tramos de **13,5 min** + slots de `clob observe` de **1 min** + init 1 min = **88 min**, margen de cierre **2 min**; deadlines **absolutos** por tramo relativos a K; tramo+observe **< TTL 15 min** (cadena de frescura sin lapsos — resuelve el overflow de la v2, donde 6×15+observe no cabía en 90); polls tardíos **censurados ex ante**; stop generado **EN el deadline** (nunca antes — defecto v2 del stop-file anticipado); ventana que no cabe íntegra antes de la pausa 02:00–08:00 GMT-3 **no arranca**; sin señal evaluable en los últimos 300 s antes de K (sin horizonte permitido, conforme v2). Todo fijado por tests con reloj virtual (sin sleeps, sin red).

### 6. Qué NO es este shot

- No es captura ni preparación de captura (la ventana se adquiere sólo con adjudicación de Metis del Plan v3); no certifica fees ni ticks (`REAL_FEE_READY=false` intacto; sin fee 0); no valida rentabilidad; no habilita live/órdenes/cuentas; no cambia estrategia ni inferencia para pasar tests; los tests técnicos demuestran semántica, jamás un resultado económico.

## Fuentes

- [[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]] §4 (opción B y aceptación), [[Plan — Single Episode Pilot v2 W1-h 2026-10-29]] §7 (alcance exacto del delta), [[Research — Economic Pilot Corrections W1-h 2026-10-29]].
- Fuente Go @ `853c0e4`: `internal/regimes/{reducer,service,prospect}.go`, `internal/capture/capture.go`, `internal/persist/{persist,migrate}.go`, `cmd/engine/{record,clob_observe}.go`, fixture `internal/experiment/w1h_acquisition_recipe_test.go` (hash del prereg).
- Código W1-i: commit `9e2c6b7dd26e70a53b05499a2d682ef33f1dac27`; hashes por archivo y recibos de corrida en OUT `validated-baseline/w1-i-causal-renewal-20261029/` (`evidence-manifest.json`, `test-receipt.md`).
- [[Polymarket Engine — Continuidad Five-POC 2026-09-20]] §§1–20 (bullet (21) registra este shot).
