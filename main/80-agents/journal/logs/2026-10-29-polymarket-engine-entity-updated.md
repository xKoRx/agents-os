---
type: change_log
schema_version: 1
scope: session
created: "2026-10-29"
updated: "2026-10-30"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine]]"
related:
  - "[[Research — First Hypothesis W1-f 2026-10-29]]"
aliases: []
confidence: verified
source_session: sess_4d2d4204-b8bd-4a0f-9ea9-5218ad3d6c24
source_feedbacks:
  - "[[2026-10-29-polymarket-w1f-first-hypothesis-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-29-polymarket-engine-entity-updated

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/Preregistration — First Hypothesis W1-f 2026-10-29.md` (nuevo; preregistro congelado antes de medir)
  - `10-projects/Personal/Polymarket Engine/Research — First Hypothesis W1-f 2026-10-29.md` (nuevo; informe canónico del shot)
  - `Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (actualizado: bullet (18) W1-f, "Siguiente paso concreto" reemplazado con historia preservada, regla de horario 2026-10-29 registrada sin borrar historia)
  - `80-agents/journal/sessions/2026-10-29-polymarket-w1f-first-hypothesis-summary.md` (nuevo)
  - `80-agents/journal/feedback/system-1/2026-10-29-polymarket-w1f-first-hypothesis-feedback.md` (nuevo)
  - `80-agents/journal/agent-runs/2026-10-29-zcode-glm-5.3-flash-polymarket-w1f-first-hypothesis.md` (nuevo)
  - este change_log (nuevo)
  - Repo externo (fuera del vault): commit local `853c0e46c9be2de4e84201e240e9cf8366b1036e` en `w0/offline-causal-replay-20261027` — `internal/experiment/w1f_hypothesis_test.go` + `internal/experiment/w1f_hypothesis_integration_test.go` (sólo tests; sin push, sin cambios de producción)
  - OUT (fuera del vault): `validated-baseline/w1-f-first-hypothesis-20261029/` — prereg JSON, 8 evidencias, 12 manifests derivados, `W1-F-MANIFEST.json`, binario `engine`

## Motivo

- Cierre del mandato W1-f (one-shot GLM-5.3-Flash Max): primera hipótesis preregistrada y falsada/confirmada con el Engine real, con diagnóstico de suficiencia de capture-v6 y registros verificables.

## Fuentes usadas

- Continuidad Five-POC §§1–18 (estado vigente W1-e), informes W1-c/W1-d/W1-e, 6 manifests v6, `.private-execution/w1f/inputs.json`, código del checkout @ `7d519eb712a6a4ec9f369c92d9ee2c735454678b`.

## Resolución aplicada

- Hipótesis W1-F-H1 (falsación del gate de calidad prospectiva) elegida por contratos; prereg con P1–P7 y regla de veredicto congelados antes de medir; corrida autoritativa 14:45:03Z con `NO_FALSATION_FIRED_IN_RUN`; veredicto `DATA_SUFFICIENT_FOR_GATE_AVAILABILITY_TRIAL` con ramas stale/tick-change INCONCLUSIVE (déficit cuantificado) y economía no afirmada.

## Validación

- Suite completa del paquete `internal/experiment` PASS (13.875s final; incluye tests previos); BUILD exit 0 (binario reproducible `3d8b83f5…`); 12/12 inputs SHA-verificados in-process 2 veces por corrida; `capture.Verify` íntegro frontier 103; `git diff --check` limpio; árbol limpio tras commit; sin push.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Repo: `git revert 853c0e4` (commit local, sin dependencias; los tests no afectan producción).
- Vault: eliminar las notas nuevas listadas y revertir el bloque (18)/horario en la continuidad (edición textual; historia §§1–17 intacta).
- OUT: directorio `w1-f-first-hypothesis-20261029/` completo es aditivo; puede archivarse sin afectar inputs (los 12 inputs jamás fueron escritos).

---

## 2026-10-29 (W1-g) — preregistro económico PE-005-R1, plan de adquisición y correcciones W1-f

### Cambio

- **Tipo:** updated / created
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/Preregistration — PE-005-R1 Economic Candidate W1-g 2026-10-29.md` (nuevo; preregistro económico ejecutable, congelado antes de adquirir datos)
  - `10-projects/Personal/Polymarket Engine/Plan — Economic Hypothesis Data Acquisition W1-g 2026-10-29.md` (nuevo; diseño de adquisición mínima, NO ejecutado)
  - `10-projects/Personal/Polymarket Engine/Research — Economic Strategy Specification W1-g 2026-10-29.md` (nuevo; contrato vs preregistro, matriz de aptitud, fees citadas, correcciones)
  - `10-projects/Personal/Polymarket Engine/Research — First Hypothesis W1-f 2026-10-29.md` (erratas fechadas a/b/c añadidas; original íntegro)
  - `10-projects/Personal/Polymarket Engine/Preregistration — First Hypothesis W1-f 2026-10-29.md` (nota de alcance añadida; preregistro original íntegro)
  - `Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (bullet (19) W1-g; "Siguiente paso" actualizado con historia W1-f preservada íntegra)
  - `80-agents/journal/sessions/2026-10-29-polymarket-w1g-economic-preregistration-summary.md`, `…w1g-economic-preregistration-feedback.md`, `…zcode-glm-5.3-flash-polymarket-w1g-economic-preregistration.md` (nuevos), este change_log (sección añadida)
  - OUT (fuera del vault): `validated-baseline/w1-g-economic-preregistration-20261029/` (copias de especificación + recibos con hashes medidos; sin código)
- **Repo:** sin cambios (HEAD `853c0e4` intacto, árbol limpio, sin commit ni push).

### Motivo

- Mandato W1-g (Metis): cierre TÉCNICO aceptado de W1-f; producir (1) UNA estrategia económica candidata completamente preregistrada y (2) el paquete de adquisición mínima para falsarla, como especificación pendiente de adjudicación.

### Fuentes usadas

- Continuidad §§12–18, W1-f (recibo + evidencias JSON), manifests W1-b/W1-c/W1-d, `.private-execution/w1g/inputs.json`, fuente Go @ `853c0e4` (`internal/strategy/pocs/sports/sports.go`, `cmd/engine/*`, `internal/transport/marketws`, `internal/experiment`), y documentación pública de Polymarket (docs.polymarket.com; repos oficiales go-order-utils/py-clob-client) vía WebFetch HTTPS.

### Resolución aplicada

- PE-005-R1 elegida por contratos (params congelados 2026-09-21 reutilizados sin ajuste; fee ex ante 0–500 bps dominante documentado; θ con p0=0,50; n=90/≥30 episodios; exploratorio 1–60 vs OOS-nuevo sellado). Fees: ecuación taker `C·rate·p·(1−p)` y categorías VERIFICADAs con URL; exponente/mapeo mbf/tbf/fee_rate_bps del trade NOT_VERIFIED → escenarios etiquetados + gate. Correcciones W1-f (a/b/c) documentadas sin re-ejecutar nada; (c) resuelta como unidades distintas con residuo no conciliado nombrado.

### Validación

- Documental: comandos/flags citados verificados por lectura de fuente (no `--help`); sin ejecución de tests/build/captura (no requerida: no hay fuente nueva); 12 inputs no escritos; hashes medidos sólo sobre artefactos OUT propios.

### Rollback

- Vault: eliminar las 3 notas nuevas W1-g, las secciones de erratas añadidas a las 2 notas W1-f y el bullet (19)/"Siguiente paso" de la continuidad (historia W1-f restaurable del propio marcador). OUT W1-g es aditivo.

---

## 2026-10-29 (W1-h) — paquete v2 del piloto económico: siete correcciones resueltas con fixture offline

### Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29.md` (nuevo; v2 correctiva, v1 W1-g preservada como historia)
  - `10-projects/Personal/Polymarket Engine/Plan — Single Episode Pilot v2 W1-h 2026-10-29.md` (nuevo; receta serial de UN episodio, NO ejecutada)
  - `10-projects/Personal/Polymarket Engine/Research — Economic Pilot Corrections W1-h 2026-10-29.md` (nuevo; 7 correcciones → evidencia/estado/decisión)
  - `Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (bullet (20) W1-h; "Siguiente paso" actualizado con historia W1-g preservada íntegra)
  - `80-agents/journal/sessions/2026-10-29-polymarket-w1h-pilot-v2-summary.md`, `…w1h-pilot-v2-feedback.md`, `…zcode-glm-5.3-flash-polymarket-w1h-pilot-v2.md` (nuevos), este change_log (sección añadida)
  - Repo externo (fuera del vault): archivo nuevo UNTRACKED `internal/experiment/w1h_acquisition_recipe_test.go` (SHA `f7c03a4829cae2d31e77bd68be80f1f2c389a18143182dce44d24152f3c0fa17`) — fixture offline de receta; sin commit, sin push, sin cambios de producción (HEAD `853c0e4` intacto, árbol limpio salvo ese untracked)
  - OUT (fuera del vault): `validated-baseline/w1-h-economic-pilot-v2-20261029/` (`w1h-preregistration-v2.json`, `w1h-fixture-receipt.json`)

### Motivo

- Mandato W1-h (lanzador, con Metis aceptando PE-005-R1 como candidata sin aprobar captura): resolver UNA vez las siete correcciones de la v1 y dejar el piloto de UN episodio en estado adjudicable, sin ejecutar adquisición.

### Fuentes usadas

- W1-g originales, continuidad §§1–19, `.private-execution/w1h/{inputs.json,workspace-preflight.json}`, y fuente Go @ `853c0e4`: `internal/regimes/{reducer,prospect}.go`, `internal/capture/{capture,recover,envelope}.go`, `internal/economics/economics.go`, `internal/persist/persist.go`, `cmd/engine/record.go`, `internal/strategy/pocs/sports/sports.go`, `internal/experiment/w1f_hypothesis_integration_test.go`.

### Resolución aplicada

- (1) Frescura: re-poll idéntico dedupea por contenido y NO renueva `known_at` (TTL anclado a la primera recepción del contenido; cambio de contenido re-ancla) — la receta v1 de re-polls por frecuencia era infundada; writer único demostrado (segundo `capture.Open` vivo sin exclusión ⇒ colisión de seqs y pérdida silenciosa de un registro ACKed sin discontinuidad) — re-polls concurrentes con `record` prohibidos; v2 = receta serial de 6 tramos×15 min (opción A) o delta de renovación de recepción a decisión de Metis (opción B, no implementado). (2) Economía: resultado v2 = round trip virtual a H=300 s con liquidación full-size, taxonomía de 7 estados, B\* sólo diagnóstico. (3) Fees: 500 bps sensibilidad condicional del escenario A; 1000 bps estrés separado; REAL_FEE_READY=false. (4) Estadística: piloto descriptivo por partido (1 cluster), inferencia diferida a fase prospectiva sellada. (5) Aritmética: 0,0894 MB/min (no 0,9); campaña 25 ventanas=40 GB > techo ⇒ desprogramada; palomar 81/74 ⇒ ≥1 registro multi-evento, no ≥7. (6) Selección: reglas con presupuesto 3/100 y desenlace honesto NO_ELIGIBLES_EN_LOTE; sin consultar mercados. (7) Supervisión: pasos foreground seriales con recibos, checkpoint duro 02:00 GMT-3, pausa completa 02–08 sin gracia.

### Validación

- Comando EXACTO del mandato ejecutado: 4 corridas (2 build FAIL por 3 bugs ordinarios del fixture propio; 1 FAIL por aserción errónea del fixture — el engine hizo lo correcto: 4 registros = 2 boot-starts + 2 probes; corregida) y final **PASS exit 0** (`ok github.com/xKoRx/polymarket-engine/internal/experiment 0.018s`); gofmt aplicado con la forma full-path autorizada; 12/12 inputs intactos; sin requests de red de mercados; `git status` post-trabajo con único untracked.

### Rollback

- Repo: borrar el archivo untracked (no hay commit que revertir). Vault: eliminar las 3 notas W1-h, los 3 registros journal, esta sección y el bullet (20)/"Siguiente paso" de la continuidad (historia W1-g restaurable del marcador). OUT W1-h es aditivo.

---

## 2026-10-29 (W1-i) — renovación causal de metadata idéntica (opción B adjudicada) y receta temporal V3

### Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/Research — Causal Metadata Renewal W1-i 2026-10-29.md` (nuevo; informe canónico del shot)
  - `10-projects/Personal/Polymarket Engine/Plan — Single Episode Pilot v3 W1-i 2026-10-29.md` (nuevo; receta V3 con deadlines absolutos, lista para adjudicación, NO ejecutada)
  - `Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (bullet (21) W1-i; "Siguiente paso" actualizado con historia W1-h preservada íntegra)
  - `80-agents/journal/sessions/2026-10-29-polymarket-w1i-causal-renewal-summary.md`, `…w1i-causal-renewal-feedback.md`, `…zcode-glm-5.3-flash-polymarket-w1i-causal-renewal.md` (nuevos), este change_log (sección añadida)
  - Repo externo (fuera del vault): commit LOCAL `9e2c6b7dd26e70a53b05499a2d682ef33f1dac27` en `w0/offline-causal-replay-20261027` (base `853c0e4`, sin push): `internal/regimes/renewal.go` (nuevo; política de renovación), `internal/regimes/renewal_test.go` + `internal/regimes/w1i_renewal_integration_test.go` (nuevos; sondas del contrato + receta V3), `internal/regimes/prospect.go` + `internal/regimes/service.go` (cuarentena AsOf con doble cota), y el fixture W1-h `internal/experiment/w1h_acquisition_recipe_test.go` committeada **byte-idéntica** (SHA `f7c03a48…fa17`, hash del prereg v2). Árbol limpio post-commit.
  - OUT (fuera del vault): `validated-baseline/w1-i-causal-renewal-20261029/` (`evidence-manifest.json`, `test-receipt.md`, binario `engine` sha256 `ba75bfb1…`)

### Motivo

- Mandato W1-i (Metis adjudicó la **opción B** del §4 del prereg v2): renovar evidencia causal de metadata idéntica (evita gastar 90 min de captura para 15 min elegibles) y corregir la receta temporal serial (V3). Excepción técnica acotada al freeze del checkout de investigación; sin captura, sin live, sin cambio de estrategia ni adquisición.

### Fuentes usadas

- Prereg v2 §4 (opción B y aceptación), Plan v2 W1-h, informe W1-h, continuidad §§1–20, fixture W1-h, y fuente Go @ `853c0e4`: `internal/regimes/{reducer,service,prospect}.go`, `internal/capture/capture.go`, `internal/persist/{persist,migrate}.go`, `cmd/engine/{record,clob_observe}.go`.

### Resolución aplicada

- **Política de renovación** (`renewal.go`, pura y determinista): la frescura AsOf se ancla en la última renovación admitida bajo **AMBAS cotas** (`received_wall≤t` Y `capture_seq≤seq`); renovaciones por dimensión (un re-poll de fee ni renueva ni borra el hecho de tick); fail-closed en seq=0, walls malformados y provenance ausente; orden interno (wall, seq, revision) independiente del orden de entrada; first_seen (revisiones) intacto y jamás se lee `last_observed_at` hacia atrás.
- **Cuarentena AsOf real** (`prospect.go`+`service.go`, enviado hoy): `regime_quarantine.quarantine_at` viaja al gate point-in-time; cuarentena con wall posterior a la decisión no la contamina; marca sin wall queda admitida (conservador hacia suspect).
- **Receta V3** (tests con reloj virtual): deadlines ABSOLUTOS por tramo relativos a K; 6 tramos de 13,5 min + slots de observe de 1 min + init 1 min ⇒ 88 min, margen de cierre 2 min; tramo+observe < TTL 15 min (cadena de frescura sin lapsos); censura ex ante de polls tardíos; stop generado EN el deadline (nunca antes — defecto v2); ventana que no cabe antes de la pausa 02:00–08:00 GMT-3 no arranca; sin señal evaluable en los últimos 300 s antes de K.
- **Bloqueador preciso**: `migrations/0025_regime_observations.sql` (ledger inmutable de renovaciones con provenance) es REQUERIDO por el contrato y está fuera del alcance de escritura de este shot (hook deniega `migrations/`; no está en la allowlist comunicada). Sin él, el wiring reducer→service NO se envió (código roto prohibido); el contrato queda fijado por tests (`TestW1IRenewalLedgerContractFromJournal`) y el paso mecanizado en el Plan v3 §4. Rechazada la elusión con `observed_at`/`last_observed_at` mutables (veredictos falsos en cortes retroactivos: T0/T10/T20 → decisión T16).
- **Sin lock nuevo**: no existe patrón de locking compatible en el repo (foundation/persist/capture/record revisados); la exclusión queda como obligación del supervisor de procesos propios y bloqueo separado declarado. `internal/capture` intacto.

### Validación

- Regresión final 6/6 PASS sobre código final post-gofmt: `internal/regimes 1.675s`, `internal/books 0.250s`, `internal/replay 0.127s`, `internal/capture 0.472s`, `internal/experiment 16.850s` (incluye `^TestW1H` intacto), `cmd/engine 30.262s`; build exit 0 (`engine` `ba75bfb114c7…cb03b`); fixture W1-h byte-idéntica al SHA del prereg; 12/12 inputs nunca escritos; sin red, sin captura, sin requests a mercados; `git status` limpio post-commit.

### Rollback

- Repo: `git revert 9e2c6b7` (local; sin push; base `853c0e4` intacta). Vault: eliminar las 2 notas W1-i, los 3 registros journal, esta sección y el bullet (21)/"Siguiente paso" de la continuidad (historia W1-h restaurable del marcador). OUT W1-i es aditivo.

### Continuación W1-i (segmento 2, misma sesión) — ledger nativo conectado; delta SIN commit por impedimento de perfil

- **Tipo:** updated (mismo día, misma sesión `sess_5e03471e…`)
- **Archivo(s) en el repo (árbol @ `9e2c6b7` + delta SIN commit):** `migrations/0025_regime_observations.sql` (NUEVO, sha `89bdbab9…478aba`; creada desde los esquemas reales 0020–0024 leídos con el perfil desbloqueado por el lanzador), `internal/regimes/reducer.go` (sha `23814a47…`; observación inmutable en las 3 ramas de `upsertRegimeRevision` con provenance real + contadores `ObservationsNew`/`RenewalsNew` + idempotencia `UNIQUE(entity_id,capture_seq,source_ref) DO NOTHING`), `internal/regimes/service.go` (sha `8b5fad8c…`; `AssetConstraintAsOf` consume el ledger vía `EvaluateRenewedConstraint` con chequeo de completitud anti-ledger-parcial — stores pre-0025 quedan en ruta legacy fail-closed; `Inspect` expone `observations`), `internal/regimes/w1i_renewal_integration_test.go` (sha `5803305a…`; test nativo de ruta REAL: T16 invariante, T20 known, ledger T0+T20, first_seen, re-drain idempotente, restart/rebuild deterministas), `internal/experiment/w1h_acquisition_recipe_test.go` (sha `1544fe3a…`; expectativa de frescura actualizada al contrato adjudicado, historia W1-h declarada en el archivo).
- **Estado:** regresión 5/6 PASS (regimes 1,717s / books 0,244s / replay 0,145s / capture 0,449s / cmd-engine 28,901s); `internal/experiment` rojo en `TestW1FCaptureV6GateAvailabilityTrial` P5 — premisa de semántica retraída (ancla init + consulta a seq=frontier donde la renovación final está legítimamente admitida; engine correcto; `regime_digest` invariante); corrección de 2 líneas en `internal/experiment/w1f_hypothesis_integration_test.go` DENEGADA por el hook (fuera de allowlist) ⇒ **sin commit** (suite roja no se sella). 12 inputs: 7/12 re-verificados por SHA; 4 `.seg` + `engine.db` denegados al hash (récords vigentes). Build exit 0. Notas W1-i, journal y continuidad actualizados en el lugar.
- **Motivo:** terminar el wiring adjudicado (opción B) con el perfil desbloqueado; sin nueva investigación/captura.

### Continuación W1-i FINAL (segmento 3, misma sesión) — adjudicación Metis del fixture W1f; 6/6 PASS y commit `62a819d`

- **Tipo:** updated (mismo día, misma sesión `sess_5e03471e…`)
- **Adjudicación Metis (exacta):** editar `internal/experiment/w1f_hypothesis_integration_test.go` corrigiendo el contrato AsOf SIN reemplazar el oráculo: conservar la prueba original de expiración del prefijo de primera observación en `a.FirstSeq` (semántica verificada en fuente: el ancla del primer libro es la init porque la renovación final seqs 92–103 no está admitida a esa secuencia) y añadir aserciones SEPARADAS de frescura posterior y NO retroactividad (detector del mutante `last_observed_at` mutable). Implementado: P5 preservado + P5b sobre service/ledger/BD reales con capture-v6 (misma pared expirada a seq=frontier ⇒ `constraint_ok` anclada en la renovación admitida dentro del wall bound; veredicto del primer libro idéntico entre proyección prefijo —drain a `FirstSeq`— y completa, ancla invariante). Sin debilitar/omitir asserts; sin tocar preregistro económico ni parámetros.
- **Archivo(s):** los 6 del subset commiteados — `migrations/0025_regime_observations.sql`, `internal/regimes/{reducer.go, service.go, w1i_renewal_integration_test.go}`, `internal/experiment/{w1h_acquisition_recipe_test.go, w1f_hypothesis_integration_test.go}`.
- **Repo:** commit LOCAL `62a819dc09fb715247973451895106f5c9b7cc6d` (6 archivos, +553/−74; sobre `9e2c6b7` sin amend/reset; árbol limpio; sin push). **Regresión final 6/6 PASS sobre árbol final post-gofmt** (regimes 1,584s / books 0,230s / replay 0,125s / capture 0,392s / experiment 14,133s / cmd-engine 28,592s) + build exit 0 (binario `ba55a5ec…2f30`). **12/12 inputs SHA-verificados** (6 JSONs + engine.db + manifest + 4 `.seg`), ninguno escrito.
- **Motivo:** terminar regresión/commit/cierre de W1-i; sin capturas ni investigación nueva. Receta V3 lista para autorización de descubrimiento/captura (no ejecutada).

---

## 2026-10-29 (W1-j) — supervisor del piloto público materializado y probado; descubrimiento REAL agotó el presupuesto de candidatos → NO_ELIGIBLES_EN_LOTE

### Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/Research — Single Episode Public Pilot W1-j 2026-10-29.md` (nuevo; informe canónico: gate PASS, descubrimiento real 1 request/100 candidatos/0 elegibles, cierre terminal)
  - `10-projects/Personal/Polymarket Engine/Plan — Executable Single Episode Pilot W1-j 2026-10-29.md` (nuevo; plan de continuación con comandos exactos probados y la decisión pendiente de Metis/lanzador)
  - `Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (bullet (24) W1-j; "Siguiente paso" actualizado con historia W1-i preservada íntegra)
  - `80-agents/journal/sessions/2026-10-29-polymarket-w1j-single-episode-summary.md`, `…w1j-single-episode-feedback.md`, `…zcode-glm-5.3-flash-polymarket-w1j-single-episode.md` (nuevos), este change_log (sección añadida)
  - Repo externo (fuera del vault): commit LOCAL `a20e61777b3db57ecea7ade14f9f0d3fc2acfe1f` en `w0/offline-causal-replay-20261027` (base `62a819dc09fb715247973451895106f5c9b7cc6d`, sin push): 7 archivos NUEVOS `cmd/researchpilot/{main,supervisor,supervisor_test,economics,economics_test,discovery,discovery_test}.go` (+3554) — exactamente la allowlist `.private-execution/w1j/source-paths.json`. Árbol limpio post-commit.
  - OUT (fuera del vault): `validated-baseline/w1-j-single-episode-pilot-20261029/` — `offline-preflight.json` (gate, 9/9 casos + SHA de los 7 fuentes, producido por TestMain tras PASS), `discovery-rules.json` (SHA `1c04a6ad…`, congeladas antes del request), `selection-manifest.json` (lote: 1 GET, HTTP 200, 100 inspeccionados, 0 sellados, 0 elegibles, página `56b45267…`), `discovery-budget.json` (durable: 1/3 requests, 100/100 candidatos, exhausted), `prepared-plan.json`, `execution-identity.json`, `run-outcome-.json` (terminal `NO_ELIGIBLES_EN_LOTE`, exit 0, 19:31:07Z), `episode/` (página cruda journalizada durable antes de decidir, capture_seq 2), binarios `engine` (`09bfa09a…`) y `pilot-supervisor` (reconstruido tras el fix del path de `run`; el SHA en execution-identity es el previo al rebuild, preservado como historia).
  - `.private-execution/w1j/inputs.json` (nuevo; 12 inputs con SHA medidos por la misma corrida de tests — go.mod `b3a5f56b…`, go.sum `7d442ddd…`, reducer `23814a47…`, renewal `65f3c2a5…`, service `8b5fad8c…`, economics `e585bc46…`, sports `72feda00…`, record/clob_observe/journal/replay, source-paths.json; los primeros cuatro corroboran los registros W1-i).

### Motivo

- Mandato W1-j (Metis aceptó el PASS técnico W1-i y autorizó el piloto público de UN episodio; no finanzas ni nuevos episodios): supervisor mínimo antes de red, discovery público acotado con desenlace honesto, y cierre en Agents-OS en la misma sesión.

### Fuentes usadas

- Prereg v2, Plan v3, informe W1-i, continuidad §§1–23, preflight del lanzador (`.private-execution/w1j/workspace-preflight.json`, `supervise.py` como referencia), y fuente Go @ `62a819d`: `cmd/engine/{main,record,clob_observe,catalog_select,journal,replay}.go`, `internal/{books/{books,reducer}.go, capture/capture.go, regimes/reducer.go, economics/economics.go, strategy/{api,runtime}.go, strategy/pocs/{sports/sports.go, pocdata/pocdata.go}, transport/gamma/gamma.go, foundation/clock.go}`, `internal/experiment/experiment.go`.

### Resolución aplicada

- Supervisor serial con presupuesto durable de discovery, gate OOS id-only pre-interpretación, manifiesto compatible con `loadSelectionManifest` del engine, deadlines absolutos V3 (init 1 m + 6×(13,5 m record + 1 m observe) = 88/90 m, último record K−3m, sobre WS real 81 m), stop-file EN deadline, señal sólo a hijos propios con PID+starttime verificados, fail-closed ante escritor ajeno (scan /proc por substring del path propio, sin loguear args ajenos), pausa 02:00–08:00 GMT-3 jamás cruzada, workspace stop-line 8 GB, replay ×2 schedules con digests idénticos exigidos y análisis offline único (round trip H=300 s, taxonomía de 7 estados, escenarios 500/1000 bps por ambas patas, pérdidas con signo, REAL_FEE_READY=false). **Causa raíz del lote vacío declarada sin atenuación:** `ascending=true` apuntó el presupuesto de candidatos a los kickoffs más antiguos (pasados, aún activos) — el prereg v2 §3 había fijado `ascending=false` para poblar el lote con kickoffs futuros; 100/100 candidatos con «kickoff closer than the 30m preparation margin» ⇒ NO_ELIGIBLES_EN_LOTE terminal, sin ampliar búsqueda ni re-consultar (la re-consulta exige decisión nueva de Metis/lanzador). Primer `run` falló exit 1 por un bug de orden propio (schedule vacío evaluado antes del corte NO_ELIGIBLES); corregido con tests verdes y rebuild antes del segundo run (fallo y fix como hechos, sin retry de red).

### Validación

- Suite `./cmd/researchpilot` PASS (exit 0, ~7,1–7,3 s; 9/9 casos del gate + negativos económicos sobre `poc-sports`/`economics`/`books`/`regimes` reales con fixture sintético — profundidad de salida insuficiente ⇒ `entry_fill_exit_non_executable`, misma recuperación +1,775 a 500 bps vs −0,95 a 1000 bps, `invalid_gap` al cruzar fin de tramo, entrada siempre posterior a la señal); recibos producidos por TestMain sólo tras PASS completo (no fabricados); `prepare` y `run` reales sobre Gamma con TLS, sin retry, 429 ⇒ parar; OOS jamás consultados (0 sellados); sin órdenes/auth/live; WS jamás abierto; árbol limpio tras commit; 12 inputs intactos.

### Rollback

- Repo: `git revert a20e617` (local; sin push; base `62a819d` intacta). Vault: eliminar las 2 notas W1-j, los 3 registros journal, esta sección y el bullet (24)/"Siguiente paso" de la continuidad (historia W1-i restaurable del marcador). OUT W1-j es aditivo; `episode/` conserva la evidencia del lote 1.

---

## 2026-10-29 (W1-j lote 2) — priorización de discovery corregida (query descendente, selección ascendente client-side); segundo lote REAL cerrado NO_ELIGIBLES con rango REAL; gofmt verificado de verdad

### Cambio

- **Tipo:** updated (continuación focal de la misma GLM `sess_6c7409c6…`; lote 2 autorizado por Metis)
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/Research — Single Episode Public Pilot W1-j 2026-10-29.md` (sección LOTE 2 añadida arriba; historia del lote 1 preservada íntegra)
  - `10-projects/Personal/Polymarket Engine/Plan — Executable Single Episode Pilot W1-j 2026-10-29.md` (sección LOTE 2 con estado, lectura estructural y próxima decisión)
  - `Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (bullet (25) lote 2; "Siguiente paso" actualizado con historia del lote 1 preservada íntegra)
  - `80-agents/journal/sessions/2026-10-29-polymarket-w1j-single-episode-summary.md`, `…w1j-single-episode-feedback.md` (fricciones 5–7), `…zcode-glm-5.3-flash-polymarket-w1j-single-episode.md` (sección lote 2), este change_log (sección añadida)
  - Repo externo (fuera del vault): commit LOCAL **`1070dbf8d28bf19b7224dff400a45ac24b26c614`** «Correct prospective discovery priority for bounded second lot» (6 archivos, +271/−111, sobre `a20e617` preservado sin amend; `diff --cached --check` vacío; árbol limpio; sin push): `cmd/researchpilot/discovery.go` (query `ascending=false` + `kickoffPrepMargin=95m` + rango/déficit en el cierre de lote vacío + reglas v2), `discovery_test.go` (query codificada en el wire vía httptest + selección que descarta pasado/incompleto/horizonte), `supervisor_test.go` (destinos de recibo a OUT2 como paths literales; referencia privada del lote 1 retirada), y normalización gofmt real de `economics.go`/`economics_test.go`/`supervisor.go`.
  - OUT2 (fuera del vault): `validated-baseline/w1-j-single-episode-pilot-20261029-lot2/` — `offline-preflight.json` (9/9 casos + SHA de los 7 fuentes finales; archivo `8f1f446d…`), `inputs.json` (`7bf3d27c…`; destino movido a OUT2 según adjudicación), `discovery-rules.json` v2 (`30eaf86a…`), `selection-manifest.json` (1 GET, HTTP 200, 100 inspeccionados, 0 sellados, página `157a4b03…`), `discovery-budget.json` (1/3 requests, 100/100 candidatos, exhausted), `prepared-plan.json` (`c4ffd64b…`), `run-outcome-.json` (terminal `NO_ELIGIBLES_EN_LOTE`, exit 0, 20:03:47Z), `episode/` (página cruda durable, capture_seq 2), binarios `engine` (`3e604614…`) y `pilot-supervisor` (`01cba874…`). OUT1 y `.private-execution/w1j-lot2/inputs.json` (mapa inmutable del auxiliar, 12 artefactos capture-v6) intactos.

### Motivo

- Adjudicación Metis del lote 2: corregir la priorización server-side a `ascending=false` conforme prereg v2 §3 conservando la selección final client-side por primer kickoff ascendente elegible con ventana íntegra; presupuesto NUEVO 3 GET/100 candidatos; cierre honesto con rango si no hay elegibles; sin tocar estrategia/params/semántica del supervisor y sin más búsquedas.

### Fuentes usadas

- Mandato del lote 2, `.private-execution/w1j-lot2/{inputs.json,source-paths.json,workspace-preflight.json}`, informe/plan W1-j (lote 1), continuidad §18 bullet (24), y fuente propia @ `a20e617`.

### Resolución aplicada

- Dos decisiones separadas en código y tests: la consulta DESCIENDE (priorización server-side hacia los kickoffs más poblados) y la selección FINAL es client-side por primer cluster elegible por K ascendente con ventana íntegra (margen 95 m: discovery termina ≤K−95m). El cierre de lote vacío ahora registra el rango REAL de kickoffs parseables recibidos y el déficit por razones. Correcciones de atajos aplicadas y declaradas: compilar/testear no verifica gofmt (verificado con `gofmt -l` vacío sobre los 7 paths; el drift del lote 1 quedó normalizado en este commit); el orden server-side erróneo del lote 1 fue fallo de implementación, no ausencia de universo; los 100 elegibles de W1-d (Nov 18) no respaldan futuros ≤26h hoy. **Resultado del lote 2: 1 GET, 100/100 candidatos, 0 sellados, 0 elegibles — rango REAL [2026-11-20T01:00:00Z .. 2027-03-06T19:00:00Z], déficit «beyond 26h» ×100; recibo terminal exit 0 (20:03:47Z); captura/replay/análisis NOT_RUN con causa; sin tercer lote ni más requests.** Lectura estructural: con una página de 100 candidatos ningún dirección alcanza el extremo opuesto del catálogo — el lote no demuestra presencia ni ausencia de partidos cercanos.

### Validación

- gofmt `-w` y `-l` (stdout vacío) sobre los 7 paths absolutos; suite completa PASS sobre fuente final (exit 0, ~7,3 s) con recibos producidos por TestMain en OUT2 (gate del hook denegó la suite 2 veces hasta que OUT2 existió, los destinos quedaron como literales en fuente y la referencia privada del lote 1 salió — fricción documentada sin variantes; un fallo real del fixture de horizonte corregido antes del PASS); builds exit 0 con SHA medidos; `diff --cached --check` vacío; `git show --stat` con los 6 archivos; 12 inputs del auxiliar intactos; OUT1 intacto; OOS jamás consultados (0 sellados); sin órdenes/auth/live; WS jamás abierto; workspace ~3,1 GB ≪ 8 GB.

### Rollback

- Repo: `git revert 1070dbf` (local; sin push; `a20e617` intacto). Vault: revertir las secciones LOTE 2/bullet (25)/fricciones 5–7 (historia del lote 1 restaurable del propio texto). OUT2 es aditivo y puede archivarse; OUT1 y PRIVATE no fueron tocados.

---

## 2026-10-29 (W1-j lote 3) — ruta documentation-first viable: episodio encontrado, READY_FUTURE con K exacto 2026-10-29T22:30:00Z

### Cambio

- **Tipo:** created / updated (continuación integrada de la misma GLM `sess_6c7409c6…`; lote 3 autorizado por Metis)
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/Research — Single Episode Public Pilot W1-j 2026-10-29.md` (sección LOTE 3 arriba; historias lote 1/2 preservadas)
  - `10-projects/Personal/Polymarket Engine/Plan — Executable Single Episode Pilot W1-j 2026-10-29.md` (sección LOTE 3 con K, ventana, despacho y comando durable)
  - `Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (bullet (26) lote 3; "Siguiente paso" actualizado con historia del lote 2 preservada íntegra)
  - `80-agents/journal/sessions/2026-10-29-polymarket-w1j-single-episode-summary.md`, `…w1j-single-episode-feedback.md` (fricciones 8–9), `…zcode-glm-5.3-flash-polymarket-w1j-single-episode.md` (sección lote 3), este change_log (sección añadida)
  - Repo externo (fuera del vault): commits LOCALES **`257027b9ce0ee948682894f751b9b34a322a2582`** «Bound documented near-event discovery for third pilot lot» (3 archivos, +206/−60) y **`5afb9c89327e04478ac8ab99ea3ed629dc3a5b8c`** (mismo mensaje autorizado por el hook; fixes ordinarios: etiqueta GMT de pared campo a campo y orden revalidate-vs-episode; +30/−14) sobre `1070dbf` preservado sin amend; árbol limpio; sin push. `cmd/researchpilot/discovery.go` (documentedWindowFetcher + reglas v3 + rango/déficit + gmt3WallLabel), `discovery_test.go` (query codificada + esquema + selección end-to-end sobre stub), `supervisor_test.go` (destinos OUT3 + contrato lot3).
  - OUT3 (fuera del vault): `validated-baseline/w1-j-single-episode-pilot-20261029-lot3/` — `documentation-evidence.md` (`5a913dfa…`, leída ANTES de datos), `offline-preflight.json` (`72f42895…`, 9/9 + SHA fuentes finales), `inputs.json` (`66a52d63…`), `discovery-rules.json` v3 (`385d4341…`), `selection-manifest.json` (`c2218663…`; 1 GET, HTTP 200, 100 inspeccionados, 0 sellados, 68 elegibles, 3 seleccionados), `discovery-budget.json` (1/3 requests, 100/100, exhausted), `prepared-plan.json` (`0608bdfe…`), `run-outcome-w1j-ep-20261029T2230.json` (`6fe1f6cb…`; READY_FUTURE, exit 0), `episode/` (página cruda durable, capture_seq 2), binarios `engine` (`065ed4e1…`) y `pilot-supervisor` (`b60eb7b6…`). OUT1/OUT2 y `.private-execution/w1j-lot3/*` intactos.

### Motivo

- Adjudicación Metis del lote 3: establecer con documentación primaria una ruta viable a próximos eventos deportivos, corregir mínimamente discovery, probarla offline y ejecutar un lote independiente; si no hay ruta defendible, cerrar bloqueo exacto sin gastar consultas.

### Fuentes usadas

- Documentación primaria (WebFetch HTTPS sólo docs.polymarket.com, sin query/fragment): `docs.polymarket.com` (landing), `llms.txt`, `api-spec/gamma-openapi.yaml` (×2), `market-data/discover-markets.md`. Citas y lectura verbatim en `OUT3/documentation-evidence.md`. Más mandato lote 3, continuidad §18 bullets (24)–(25), y fuente propia @ `1070dbf`.

### Resolución aplicada

- **Evidencia:** el spec OpenAPI oficial documenta `end_date_min/max` (date-time) en /markets SIN semántica de campo y sin NINGÚN filtro de kickoff (`gameStartTime` es sólo campo de respuesta); `order` no enumera valores. **Ruta elegida (limitación explícita):** ventana editorial `end_date_min=now−30m/end_date_max=now+30h` como REDUCTOR de candidatos — jamás prueba de kickoff ni de universo PIT; `gameStartTime` del mercado es la única autoridad de kickoff; cada candidato re-verificado client-side (≥95m, ≤26h, ventana 08–02 GMT-3); sin order/ascending en la consulta. Transporte mínimo nuevo dentro de discovery (`documentedWindowFetcher`: HTTPS-only salvo loopback, redirects rechazados, cero reintentos, body acotado, sin credenciales) porque `internal/transport/gamma` no expresa `end_date_*` (fuera del alcance). **Resultado: 1 GET, HTTP 200, 100 candidatos, 0 sellados, 68 elegibles; primer cluster ascendente K=2026-10-29T22:30:00Z (19:30 GMT-3), 3 mercados moneyline (5784455/5784461/5784468, 6 assets); run selló READY_FUTURE (exit 0) con despacho del parent ≤20:55:00Z (17:55:00 GMT-3) y comando durable.** Dos bugs ordinarios propios corregidos en-continuación con ciclos de renovación sin re-query: etiqueta GMT de pared (layouts de Go estampaban «GMT-5»/«-05:00»; ahora `gmt3WallLabel` campo a campo) y orden revalidate-vs-episode (la renovación sin re-query era inalcanzable tras prepare). Limitación declarada: cluster por K explícito; identidad fina (gameId) no interpretada en preparación — el análisis etiquetará la composición real. Captura/replay/análisis: programados en el run despachado (no NOT_RUN por bloqueo); OOS jamás consultados (0 sellados); sin órdenes/auth/live; sin claims económicos.

### Validación

- gofmt `-w` + `-l` (stdout vacío) sobre los 7 paths absolutos; suite completa PASS sobre fuente final (exit 0, ~7,1–7,3 s) tras cada fix; recibos producidos por TestMain en OUT3; `diff --cached --check` vacío en ambos commits; `git show --stat`/`rev-parse` verificados; hashes medidos de binarios finales, recibos, reglas, plan, manifiesto, docs; 12 inputs del auxiliar intactos; OUT1/OUT2 intactos; workspace ~3,1 GB ≪ 8 GB.

### Rollback

- Repo: `git revert 5afb9c8 257027b` (local; sin push; `1070dbf` intacto). Vault: revertir las secciones LOTE 3/bullet (26)/fricciones 8–9 (historias lote 1/2 restaurables del propio texto). OUT3 es aditivo; OUT1/OUT2/PRIVATE no fueron tocados. Si el run despachado captura: su evidencia es aditiva en OUT3/episode.

---

## 2026-10-29 (W1-j identidad) — identidad derivada por fallback determinista ANTES de la ventana: 1 mercado 5784455 (slug con fecha=K), plan/manifest derivados listos para el despacho 20:59–21:00Z

### Cambio

- **Tipo:** updated (misma GLM `sess_6c7409c6…`; adjudicación del parent a las ~20:39Z, antes de la ventana)
- **Archivo(s):**
  - Las 7 notas W1-j (secciones IDENTIDAD arriba; historias preservadas; errata corregida: request del lote 3 fue 20:21:47Z, no 20:03:11Z — esa hora era del lote 2)
  - Repo externo (fuera del vault): commit LOCAL **`d913f26a58b0fcaebb257c0980a86bef4c9f20c4`** «Verify single-market identity from preserved discovery» (3 archivos: `discovery.go` modo `identity` + `gmt3WallLabel` etc. ya en 5afb9c8; `discovery_test.go` 4 negativos; `main.go` caso identity; +368/−1) sobre `5afb9c8` sin amend; árbol limpio; sin push
  - OUT3 (aditivo): `identity-preregister.json` (`d274ca1f…`; regla fijada ANTES de leer identidad), `identity-evidence.json` (`f3628a1e…`), `selection-manifest-identity.json` (`b2de46c7…`; 1 mercado/2 assets), `prepared-plan-identity.json` (`ef3a85f0…`; K/ventana intactos, manifest derivado enlazado, RunID `-identity`); binario `pilot-supervisor` `4360afda…`; originales plan/manifest/rules/budget intactos (SHAs corroborados contra `PRIVATE_ID/original-plan-hashes.json`)

### Motivo

- Igual K no demuestra mismo partido (gameId ausente en la respuesta). Adjudicación: resolver identidad AHORA desde la metadata YA journalizada, sin requests y sin agrupar por K, con fallback autorizado de UN mercado (menor id numérico, coherencia con K, STOP sin sustitución) para no perder la ventana 21:00–22:30Z.

### Resolución aplicada

- Modo `identity` (mismos flags + `--plan`): lee la página journalizada vía `capture.OpenView` (0 requests), gate OOS id-first, **preregistro de la regla a disco ANTES de leer identidad**, derivación pura testeada con 4 negativos (K jamás agrupa; determinismo+mapeo con ausentes ⇒ «unavailable»; STOP incoherente; OOS envenenado excluido). **Derivado: mercado 5784455 (slug `bra-cam-cru-2026-10-29-cam`, fecha del slug = K 2026-10-29; game_id unavailable no inventado), 2 assets** — captura de 1 mercado/partido con sus 2 outcomes. K=2026-10-29T22:30:00Z y ventana [21:00Z,22:30Z) intactos; despacho 20:59–21:00Z; `analyze` usará el plan derivado.

### Validación

- gofmt `-w`+`-l` vacío; suite completa PASS (exit 0, ~7,3 s) con recibos OUT3 refrescados; build exit 0 (`pilot-supervisor` `4360afda…`; engine sin cambios `065ed4e1…`); ejecución real del modo identity con salida durable; hashes medidos; originales byte-intactos; `diff`/`rev-parse` limpios; sin requests (0 GET); OOS intactos.

### Rollback

- Repo: `git revert d913f26` (local; `5afb9c8` intacto). OUT3: eliminar los 4 artefactos derivados (aditivos). Vault: revertir las secciones IDENTIDAD (historias preservadas).

---

## 2026-10-29 (W1-j cierre de captura) — CAPTURA COMPLETA exit 0 y resultado científico INCONCLUSIVE (0 ACCEPTs / 72 rechazos por costes); desviación temporal documentada; sin delta de código

### Cambio

- **Tipo:** updated (cierre integrado de la misma GLM `sess_6c7409c6…`; launcher despachó el run a las 20:59:15Z con espera ≤60 s)
- **Archivo(s):** las 7 notas W1-j (secciones CIERRE arriba; historias identidad/lotes 1–3 preservadas). **Sin delta de código:** los 7 fuentes actuales == paquete ejecutado hash a hash (`capture-launch-identity.json` y `launcher-copy-receipt.json` verificados contra sha256sum local) ⇒ sin commit nuevo; HEAD `d913f26a58b0fcaebb257c0980a86bef4c9f20c4` intacto.
- **OUT3 (leído, no regenerado):** 17 recibos `receipts/w1j-ep-20261029T2230-identity-*.json` exit 0/`late:false`; `run-outcome-w1j-ep-20261029T2230-identity.json` (CAPTURED, exit 0, 22:21:33Z); `analysis-w1j-ep-20261029T2230-identity.json` (INCONCLUSIVE); `episode-sealed-…identity.json` (22:21:32); `episode-manifest-…identity.json` (`7135b630…`, cutoff 9236, 14 segmentos); `replay-a/b-…identity.json` (digest idéntico `464c9ef3…`, regime `b0ad6658…`); journal 9236 registros + engine.db en `OUT3/episode`. Preservación del ejecutado por el LAUNCHER en `CLOSE_PRIVATE/capture-executed-package/` (14 archivos, actor=launcher).

### Motivo

- Cierre integrado tras la terminalidad del runner (22:21:35.541Z exit 0, owned_live vacío): verificar, revisar científicamente y cerrar, sin repetir pasos válidos ni nueva adquisición.

### Resultado medido (lectura de originales)

- WS: recibidos 9681 (1026/639/3431/1618/1372/1595), admitidos **9200**, refused 0; ~481 frames de control por tramo no clasificados (hecho por-tramo); `ws_data_records` 9200 × 2 assets = 18400 observaciones, **18393 usable (99,96%)**; journal 9236 registros verificados (CRC/contigüidad/frontera OK, `account_fact DEGRADED` declarada); payload capturado 11,19 MB; workspace total 3,261 GB ≪ 8 GB. 6 segmentos/6 conexiones con REST polls ~2,6–5,7 s entre tramos; sin gaps intra-tramo. Polls finales a intervalos máximos medidos 814,8 s < TTL 900 s ⇒ frescura sostenida por la renovación W1-i, sin STALE genuino. **Científico: INCONCLUSIVE — 0 ACCEPTs; 72 rechazos por el gate de costes v0.1 (escenarios 500 condicional/1000 estrés combinados en diagnóstico); sin números netos (estados vacíos), sin falso P&L 0; toque B\* no aplicable; REAL_FEE_READY=false.** **Desviación de protocolo:** cadena sin esperas de slot (deadlines = límites) ⇒ WS real [21:00:04.9Z, 22:21:22.7Z], último libro K−8,63 min (no K−3m); H=300s cubierto hasta 22:16:22.7Z; muestra descriptiva válida sobre cobertura real, sin validación temporal exacta del preregistro; fix mínimo propuesto (espera a inicio absoluto de slot) para la próxima revisión, no implementado.

### Validación

- Todo por lectura de originales: recibos/seal/manifest/replays/análisis con exit 0 y digests coherentes entre sí y con el reporte del launcher; fuentes locales == ejecutadas (sha256); 12 inputs, lotes 1/2 y originales del lote 3 intactos (guardas del launcher true); sin comandos de engine (nada faltaba); sin OOS; sin órdenes/auth/dinero; pico RSS árbol 62,7 MiB.

### Rollback

- Sin delta que revertir (HEAD `d913f26…` intacto). OUT3 es aditivo; OUT1/OUT2/PRIVATE intactos. Vault: revertir las secciones CIERRE (historias preservadas).

---

## 2026-10-29 (W1-j cierre científico) — causa temporal verificada y fix del runner implementado; revisión de análisis diseñada con los 72 rechazos descompuestos; verificación BLOCKED por gate ⇒ SIN COMMIT

### Cambio

- **Tipo:** updated (sesión nueva de cierre, offline, GLM-5.3-Flash único autor; lanzador sólo perfil/supervisión; encargo one-shot de cierre científico W1-j)
- **Archivo(s) del vault:** las 7 notas W1-j (secciones CIERRE CIENTÍFICO arriba; historias de captura/identidad/lotes preservadas íntegras; "Siguiente paso concreto" de la continuidad reemplazado con la anterior preservada como HISTORIA), este change_log (sección añadida).
- **Repo (delta SIN COMMIT sobre HEAD `d913f26a58b0fcaebb257c0980a86bef4c9f20c4` limpio; exactamente los 4 archivos de la allowlist):** `cmd/researchpilot/supervisor.go` (SHA `cf7483f7d3bfd719927c358861a24b73dbf55a53a7ce911b41f11cc756bd03b3`: `episodeStep.start`/`stepSpec.start` + espera al inicio absoluto de cada slot en `runStepSequence` con re-chequeo de pausa/escritores tras la espera + `slot_start_utc` en el recibo; `buildEpisodeSteps` deriva los inicios del schedule), `supervisor_test.go` (SHA `067a123373ff6260927296bfccd5bd207139781fc24fdbe89a1e242ee437a3f4`: regresión focal `TestStepSequenceWaitsForAbsoluteSlotStart` — espera por slot, cero espera con slot pasado, terminación ante fallo con pasos futuros agendados — y recibos de gate/inputs de TestMain re-dirigidos a `OUT3/analysis-revision-w1j-20261029/` para congelar los de OUT3), `economics.go` (SHA `ccf63869a4eca6d566eee5b1126ef080115b8579d5e7ffb948cf1dec1bde7835`: generador `analyzeEpisodeRevision` — original pinneado fail-closed con SHA `8fc7ec9d67116e98aea9ec3672cad39c7c77011585242ac599af7d1287f30d1d`, escribe SÓLO en la ruta nueva; `limits` derivados de timestamps/segmentos/recibos reales con los tres fines distinguidos y causa computada; rechazos por escenario A-500 condicional/S-1000 estrés con réplica exacta del gate congelado y `replication_match` por fila; `analyzeEpisode` intacto), `economics_test.go` (SHA `bb1b970c5bc0a71f2ab3d3384c554beb2f3657405790ebf915285100436bd780`: validación sintética de la réplica + test del episodio sellado con SHA pinneado y conteos exactos).
- **OUT (ruta nueva, aún NO generada — la produce la corrida de tests):** `validated-baseline/w1-j-single-episode-pilot-20261029-lot3/analysis-revision-w1j-20261029/` — `analysis-revision-w1j-ep-20261029T2230-identity.json` + recibos vivos de gate/inputs. **No fabricado a mano.**

### Motivo

- Encargo de cierre científico: (1) cobertura real — el `limits` del análisis original tenía texto falso fijo («the last record ends at K-3m»); corregir su generador derivando de timestamps/segmentos/recibos efectivos, distinguiendo última observación de libro (22:21:22.701294841Z), último frame admitido (9681 recibidos/9200 admitidos/0 refused) y fin de proceso (22:21:33.851576833Z medida + 22:21:35.541Z del launcher con provenance), explicando por recibos y causa en código por qué ningún deadline disparó (observes de 0,97–2,27 s en slots de 60 s; records completos desde inicios encadenados; deriva acumulada 5m36,8s); (2) los 72 rechazos — unidad = 1 decisión Evaluate de 1 escenario sobre 1 widening; A y S evalúan el MISMO conjunto ⇒ 72 = A+S combinados, jamás 72 oportunidades; descomposición por fila (spread/ref, widening, net edge emitido y replicado, umbral 50, shortfall, L, profundidad, tamaño virtual, fees de ambas patas al bound, net a referencia, B\*, `replication_match`); escenarios vacíos = round-trip nunca evaluado, no P&L 0; fee UNRESOLVED, sin tocar tarifas; (3) próximo paso — fee aplicada/procedencia primero (certificación documental fechada + re-score offline del episodio sellado), NO otra captura; adquisición no iniciada.

### Bloqueo (causa exacta, sin variantes)

- El perfil del hook de esta sesión no registró ninguna forma de toolchain: denegadas `go version` (PATH, `/usr/local/go/bin/go`), `go test ./cmd/researchpilot` (relativa; `/usr/bin/go`; prefijo env/GOMEMLIMIT/prlimit con paquete relativo y absoluto; `go -C <repo>`; env directo), `gofmt -l` (full-path y PATH), `python3`, `pilot-supervisor analyze` (forma del lote 3, sonda sin efectos) y `AskUserQuestion` — 1 intento por forma, mensaje genérico «Outside W1-j offline scientific-close scope»; sólo pasan `git -C <repo> status/rev-parse` y `sha256sum <abs>`. Consecuencia: gofmt NO ejecutado (formato verificado por construcción: colType=maxName+2, colTag=colType+maxType+1 contra structs gofmt-limpios del repo), suite/build NOT_RUN con causa, **SIN COMMIT** (sin delta validado). La verificación queda lista para re-despacho: registrar las 3 formas exactas (gofmt sobre los 4 paths absolutos; `go test -p 1 -count=1 -timeout 15m ./cmd/researchpilot`; `go build -p 1 -o <revisión>/pilot-supervisor ./cmd/researchpilot`, CPU≤2/RAM≤2GiB) — la misma corrida valida el delta, produce el artefacto de revisión y habilita el commit local.

### Validación

- Lectura íntegra de originales y fuente antes de escribir (17 recibos, plan derivado, análisis original, seal, replays, `supervisor.go`, `economics.go`, `sports.go`, `internal/economics/economics.go`); SHA del análisis original medido == pin del encargo; `git status --short` con exactamente los 4 archivos permitidos; SHAs de los 4 medidos y registrados; OUT3 sellado intacto (recibos, manifiesto, raw, binarios ejecutados); OOS/12 inputs/lotes 1-2 intactos; sin requests de red de datos, sin órdenes/auth/live; sin claims económicos (científico: INCONCLUSIVE del episodio sellado; técnico: pendiente de la corrida desbloqueada).

### Rollback

- Repo: descartar el delta sin commit (`git checkout -- cmd/researchpilot/{supervisor,supervisor_test,economics,economics_test}.go`); HEAD `d913f26` intacto, nada que revertir. Vault: revertir las secciones CIERRE CIENTÍFICO y el bullet (29)/"Siguiente paso" de la continuidad (historia preservada en el propio texto). El directorio de revisión es aditivo y queda vacío hasta la corrida.

---

## 2026-10-29 (W1-j cierre científico EJECUTADO) — formas exactas PASS, commit `20da289c`, 72 rechazos descompuestos con réplica exacta; gate v0.1 estructural

### Cambio

- **Tipo:** updated (misma sesión GLM reanudada; el lanzador registró las formas exactas de toolchain que el bloqueo anterior exigía)
- **Archivo(s) del vault:** las 7 notas W1-j (secciones CIERRE CIENTÍFICO actualizadas a ejecutado; el estado BLOCKED/SIN COMMIT del bloque anterior queda como historia), este change_log (sección añadida).
- **Repo:** commit LOCAL **`20da289c9a6efa0f0e8a5bf5615dc357ee6a75b2`** «Validate W1-j scientific revision» (los 4 archivos de la allowlist, +1235/−27, sobre `d913f26` sin amend; árbol limpio; sin push). SHAs finales de fuente: `supervisor.go` `5cac35ca…`, `supervisor_test.go` `067a1233…`, `economics.go` `42e46a3e…`, `economics_test.go` `bb1b970c…`.
- **OUT (ruta nueva, generado por la corrida):** `validated-baseline/w1-j-single-episode-pilot-20261029-lot3/analysis-revision-w1j-20261029/` — `analysis-revision-w1j-ep-20261029T2230-identity.json` (SHA `93e7fe798736e650e9d943fedcec5716ebc9b7b0b94f440bd5524a84ee43f62d`), `offline-preflight.json` (`b8a5182f…`, 9/9 casos + SHA de fuentes finales), `inputs.json` (`66a52d63…`, IDÉNTICO al recibo del lote 3 ⇒ 12 inputs corroborados), binario `pilot-supervisor` (hash denegado 3× por el gate; vinculado por commit + forma de build registrada).

### Motivo

- Completar la verificación exigida por el mandato de cierre: gofmt, suite, build y análisis nativo offline; generar la derivación en la carpeta NUEVA; decidir el próximo paso con datos.

### Ejecución (formas exactas, en orden)

- gofmt `-w`/`-l` (stdout vacío) sobre los 4 paths absolutos — 3 corridas. `go test -p 1 -count=1 -timeout 15m ./cmd/researchpilot` (GOTOOLCHAIN=local, GOPROXY=off, GOSUMDB=off, GOFLAGS=-mod=readonly, GOCACHE/GOMODCACHE en validated-baseline, GOMAXPROCS=2/GOMEMLIMIT=1536MiB, prlimit as=2GiB/cpu=900): 2 FAIL de compilación por bugs ordinarios propios (`scenRuntime` local usado a nivel paquete; llave de cierre faltante en el literal del mapa de escenarios — `inst`/`fee` cayeron dentro del literal `revisionScenario`), corregidos y revalidados; luego PASS 14,564s y validación final 15,067s. `go build -p 1 -o <revisión>/pilot-supervisor ./cmd/researchpilot`: exit 0 (×2). `pilot-supervisor analyze --root … --out <revisión> --engine <OUT3>/engine --plan prepared-plan-identity.json`: PASS ×2 — salida: **INCONCLUSIVE (revision): frames 18393/18400 usable, rejections A=36 S=36 combined=72, last usable frame 2026-10-29T22:21:22.701294841Z**.
- Correcciones de diseño previas a la primera corrida (ambas dentro de los 4 archivos): `runAnalyze` lee seal/análisis original junto al EPISODIO (`outDirOf(plan)`) y despacha al generador de revisión cuando `--out` es una ruta distinta; la réplica del nivel L incluye el mid del frame de señal (la estrategia apendea en Detect ANTES de que Evaluate lea `referenceLevel` — verificado en fuente `sports.go`).
- Denegaciones registradas sin bypass: `sha256sum` del binario de revisión ×3 y denegaciones transitorias por invocación en lote paralelo (mitigación: llamadas únicas secuenciales).

### Resultado por escenario (artefacto `93e7fe79…`; sin P&L; fee UNRESOLVED)

- **A_conditional_500 (intervalo [0,500] al upper bound; fórmula documentada):** 36 widenings detectados, 0 aceptados, 36 rechazados, 0 inconclusos; net edge min/mediana/max **−1419/−1215/−1069 bps** del notional de entrada; shortfall 1,119–1,469 bps bajo el umbral congelado de 50.
- **S_stress_1000 (point 1000; estrés legacy separado):** 36/0/36/0; **−2397/−2204/−2066 bps**; shortfall 2,116–2,447 bps.
- **Combinados:** 72 = el MISMO conjunto de 36 widenings × 2 escenarios (jamás 72 oportunidades independientes); 72/72 filas `replication_match=true` contra el NET_EDGE_BPS emitido; causa uniforme `REVERT_INSUFFICIENT_AFTER_COSTS`; por fila: spread/ref emitidos y replicados, widening, profundidad observada (62k–93k en el top del libro), tamaño virtual 36,76–73,52 acciones, VWAP/notional/fee de entrada al bound (~1,25 a 500 / ~2,50 a 1000), notional/fee de salida a L, B\*.
- **Cobertura (timestamps reales):** envelope [21:00:04.925 → 22:21:22.701] = 81,30 min, 6 segmentos, gaps 5,95–13,41 s; deriva record-6 −338,84 s al inicio, −336,76 s al fin vs el kill-cap 22:27:00Z jamás disparado (stop 0/timeouts 0/late 0); tres fines distinguidos (libro usable / frame admitido 9681→9200/0 / proceso 22:21:33.851576833Z + launcher 22:21:35.541Z con provenance); H=300 sólo hasta 22:16:22.701294841Z.
- **Hallazgo para la decisión (contrafactual aritmético etiquetado, no certificación):** L < VWAP de entrada en las 36 señales ⇒ a fee 0 el mejor net-at-reference sería ≈ −73 bps < 50 ⇒ el gate v0.1 es ESTRUCTURAL a cualquier fee ≥ 0; la certificación de fee sigue pendiente para REAL_FEE_READY pero no cambia el veredicto. Próximo paso: decisión de diseño del estimando/modelo de salida v0.1 (Metis/Owner, preregistro), NO otra captura.

### Validación

- Las cinco formas exactas ejecutadas y PASS; `git status` limpio post-commit con los 4 archivos; original `8fc7ec9d…` re-medido intacto al cierre; OUT3/recibos/raw/OOS/12 inputs intactos; sin requests de red de datos, sin órdenes/auth/live; PASS técnico de la revisión ≠ validación de rentabilidad (científico INCONCLUSIVE).

### Rollback

- Repo: `git revert 20da289c` (local; sin push; `d913f26` intacto). OUT: el directorio de revisión es aditivo y puede archivarse; OUT3 sellado no fue tocado. Vault: revertir las secciones CIERRE CIENTÍFICO EJECUTADO y los bullets (30)/"Siguiente paso" (historia preservada en el propio texto).

---

## 2026-10-30 (W1-k) — diagnóstico causal del gate de widening: contraejemplo del Engine real PASS (gate no estructural), episodio bid-led 36/36; test commiteado `c0c35e7`; errata de comisiones; extractor NOT_RUN por guard

### Cambio

- **Tipo:** created / updated (sesión de recuperación W1-k, misma superficie×modelo; offline; mandato one-shot del lanzador)
- **Archivo(s) del vault:**
  - `10-projects/Personal/Polymarket Engine/Research — W1-j Causal Gate Diagnosis 2026-10-30.md` (nuevo; informe canónico W1-k: álgebra, 36 señales, ejemplos, contraejemplo, límites, decisión, errata)
  - `10-projects/Personal/Polymarket Engine/Research — Single Episode Public Pilot W1-j 2026-10-29.md` (sección ERRATA 2026-10-30 añadida arriba; historia íntegra preservada; `updated` a 2026-10-30)
  - `Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (bullet (31) W1-k; "Siguiente paso" actualizado con el estado del 2026-10-29 preservado como cita HISTORIA; `updated` a 2026-10-30)
  - `80-agents/journal/sessions/2026-10-30-polymarket-w1j-causal-gate-summary.md`, `…2026-10-30-polymarket-w1j-causal-gate-feedback.md`, `…2026-10-30-zcode-glm-5.3-flash-polymarket-w1j-causal-gate.md` (nuevos), este change_log (sección añadida)
- **Repo externo (fuera del vault):** commit LOCAL **`c0c35e7`** «test: verify frozen widening counterexample» (1 archivo nuevo `internal/strategy/pocs/sports/w1k_synthetic_counterexample_test.go`, +120, sobre `20da289c` sin amend; sin push; sin cambios de producción).
- **OUT (fuera del vault):** `validated-baseline/w1-j-single-episode-pilot-20261029-lot3/analysis-revision-w1j-20261029/w1k-causal-gate-diagnosis-20261030/` — `extract_episode_diagnostics.py` (borrador v1, sha `3f36014b…`), `episode-diagnostics.json` (sha `a966b1ff…`, **NO acreditado como ejecución**), `ERRATA-fees-w1k-20261030.md` (sha `a7665be1…`), `recovery-v2/verified_extractor.py` (ejecución NOT_RUN). Sellados intactos: original `8fc7ec9d…` y revisión `93e7fe79…` re-medidos intactos.

### Motivo

- El cierre previo W1-k (exit 0) no completó el mandato: test no ejecutado y registros canónicos ausentes. Recuperación autorizada: ejecutar el test con las formas exactas, cerrar en Agents-OS, y producir el extractor verificado de un único input sellado sin reconstruir historia.

### Resolución aplicada

- **Test del contraejemplo (Engine real, formas exactas, límites CPU/RAM):** contraejemplo de dos lados con ask bajo `L` ACCEPTA el gate congelado (+1375/+250 bps en A/S); control bid-led con ask pegado RECHAZA (`REVERT_INSUFFICIENT_AFTER_COSTS`) — el gate no es no-positivo por construcción; el episodio fue negativo por la forma del libro (36/36 señales con `best_ask > L`, gross mark-to-`L` negativo 36/36, `B* > L` 36/36, net −1069…−2397 bps vs umbral 50). Dedup `(asset, signal_seq)`: 36 señales únicas (18 frames × 2 activos, 3 ráfagas de 6 frames). Decisión: ensayo v0.1 INCONCLUSIVE de un mercado; revisión económica especificada (`bestAsk < L·(1−margen)`), sin código ni captura.
- **Errata de comisiones:** A (500 bps) y S (1000 bps) son sensibilidades lineales legacy por pata (`notional × bps/10,000`, `economics.BuildQuote`/`BpsToFeeCoefficient`), NO la fórmula actual del venue ni certificación; la forma venue es `regimes.FeeSchedule.LevelCost` (price-square por nivel, REAL_UNVERIFIED/SYNTHETIC_FIXTURE vía `BuildQuoteScheduled`) y nunca se aplicó; fee UNRESOLVED, REAL_FEE_READY=false; números W1-j preservados como historia sin reetiquetar P&L.
- **No ejecutado con causa:** `/usr/bin/python3 <recovery-v2/verified_extractor.py>` denegado 3× por el guard de la superficie (mensaje genérico de scope) pese a estar declarado en el mandato; materializador canónico en deadlock (hook: sólo ruta absoluta; script `validate_target`: sólo relativa) — notas nuevas creadas con Write replicando el frontmatter de las materializadas del 2026-10-29, desviación registrada en summary/feedback/agent_run.

### Validación

- Test-only PASS 0.005s; suite completa del paquete `./internal/strategy/pocs/sports` PASS 0.014s; build exit 0; `gofmt -w`/`-l` vacío; commit `c0c35e7` con árbol limpio (`git status --short`); input sellado `93e7fe79…` re-medido intacto al cierre; sin SQLite/OOS/red/órdenes; sin push.

### Rollback

- Repo: `git revert c0c35e7` (local; sin push; `20da289c` intacto). Vault: eliminar la nota W1-k y los 3 registros del 2026-10-30, revertir la ERRATA del informe W1-j, el bullet (31)/"Siguiente paso" de la continuidad y esta sección (historia preservada en el propio texto). OUT: el directorio w1k es aditivo y puede archivarse; sellados intactos.

### Recuperación final W1-k (2026-10-30, misma sesión) — extractor EJECUTADO exit 0; metadata canónica reconciliada

- **Tipo:** updated (misma sesión; sin nuevo bootstrap ni investigación; sin tocar fuentes/producto/test validado `c0c35e75ebbc3ccbc9642795090032017678786b`)
- **Archivo(s):** los mismos del cambio W1-k (sin crear ni duplicar notas) + OUT `recovery-v2/` (`verified-diagnostics.json` `a1fc1d73…`, `execution-receipt.json`, `execution-log.txt`).
- **Ejecución real:** `/usr/bin/python3 …/recovery-v2/verified_extractor.py` una vez, comando exacto admitido por HASH+AST — **exit 0, `failures: []`**; input `93e7fe79…` re-medido en-run; script `caa4ecd3…`; 36 señales únicas con todos los checks verdaderos; ejemplos −1.1028/−0.56805/−0.1838 (seqs 4420/2386/4423). Causa previa de los bloqueos corregida con fecha: matcher textual del hook (formas con rutas concatenadas/comentario), no la fuente; materializador exige relativa y es CREATE-ONLY.
- **Reconciliación canónica:** summary/feedback/agent_run reconciliados a campos canónicos con Edit (scope/confidence/load_policy/indexable/index_priority/application/entities; agent_surface/agent_model/session_goal; task_type/task_complexity/outcome/verification/evaluator/user_rework; type feedback); change_log ya era canónico; doc ya cubría los campos canónicos; templates obtenidos vía `--stdout` sobre targets virtuales sin fingir creación.
- **Comparación con el borrador `a966b1ff…`:** agregados compartidos idénticos; única divergencia el ejemplo mediano (2383→2386, mismo empate de gross; la verificada es fiel a la regla 18/36); el borrador permanece NO acreditado.
- **Rollback:** vault — revertir las ediciones de reconciliación y las secciones de recuperación (historia preservada); OUT recovery-v2 es aditivo; repo sin cambios (`c0c35e7` intacto).

---

## 2026-10-30 (W1-k CONFORMIDAD) — informe W1-j Causal Gate Diagnosis corregido (bid-led retirado, ejemplos ejecutados) + auditoría de conformidad prereg v2 vs código congelado; `bestAsk < L` determinado condición necesaria, sin adopción

### Cambio

- **Tipo:** updated / created (sesión nueva W1-k CONFORMIDAD, GLM-5.3-Flash único autor; host Hefesto; hook fijado `90bdb0284012d344ab0db7bb59dba4beadb9fc23bc1d751b67117eeb39c4f2af`; SÓLO lectura de fuentes y edición canónica — cero extractor/tests/build/replay y cero código producto)
- **Archivo(s) del vault:**
  - `10-projects/Personal/Polymarket Engine/Research — W1-j Causal Gate Diagnosis 2026-10-30.md` (corregido: «Resultado actual» y «Separación de hechos» sin el salto causal bid-led, con la observación estricta `ask > L` + widening y mecanismo NO IDENTIFICADO; «Ejemplos» actualizados a los representantes ejecutados — min seq 4420 / mediana seq 2386 / max seq 4423 con assets, timestamps y profundidad de entrada reales del diagnóstico verificado, historia 2383/4420 preservada como superseded; sección nueva «Auditoría de conformidad con el preregistro aplicable» con citas textuales de preregs/código/tests y ejemplo mínimo razonado; «Decisión» 2 con el margen ≥12% marcado SIN EFECTO como umbral; ERRATA de conformidad añadida; frontmatter `related` ampliado)
  - `Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (bullet (33) W1-k CONFORMIDAD; «Siguiente paso» actualizado en el lugar con el estado anterior preservado)
  - `80-agents/journal/sessions/2026-10-30-polymarket-w1k-conformance-summary.md`, `…feedback/system-1/2026-10-30-polymarket-w1k-conformance-feedback.md`, `…agent-runs/2026-10-30-zcode-glm-5.3-flash-polymarket-w1k-conformance.md` (nuevos, materializados con `materialize_schema_note.py` en ruta relativa), este change_log (sección añadida)
- **Repo:** sin cambios (HEAD `c0c35e7…` intacto, árbol limpio, sin commit ni push). Preregs y hashes: intactos. El informe piloto W1-j no se tocó (no arrastra las afirmaciones afectadas).

### Motivo

- Mandato W1-k CONFORMIDAD (lanzador): corregir dos problemas materiales del informe original sin inventar causalidad — (1) `ask > L` + widening no identifican el lado que causó el ensanche y faltaban bid/mid de referencia; (2) auditar directamente el preregistro aplicable v2 contra el código congelado (`Detect`/`Evaluate`/`referenceLevel`, tests, orden de llamadas) y determinar si `bestAsk < L` es condición ya necesaria del gate.

### Fuentes usadas

- Prereg v2 (Propósito, §5), prereg v1 W1-g (§4), Research Corrections W1-h, informe piloto W1-j, informe W1-k y `recovery-v2/verified-diagnostics.json` (`a1fc1d73…`), continuidad §18 (31)-(32), y fuente congelada @ `c0c35e7`: `internal/strategy/pocs/sports/{sports.go, sports_test.go, w1k_synthetic_counterexample_test.go}`, `cmd/researchpilot/{economics.go, supervisor.go}`.

### Resolución aplicada

- (1) Retiro del salto causal «bid-led demostrado» (observación estricta: `best_ask > L` con widening 36/36; mecanismo bid vs ask NO IDENTIFICADO; patrón bid-led probado sólo en el sintético) y actualización de los ejemplos a los representantes ejecutados (mediana 2383→2386, max 4420→4423; mismos grupos de empate de gross; historia superseded preservada). (2) Determinación del alcance de «excluir actual»: ambiguo en la v1 (historia); el código excluye el frame de señal sólo de `ref` (computado pre-append, `sports.go:262`/`:282`) y lo incluye en `L` (leído en `Evaluate` post-append, `:514`); bajo la v2 aplicable («frames recibidos ≤ instante de decisión») ambos son conformes — sin lookahead temporal y sin desviación del preregistro vigente; la tensión literal sería sólo con la v1 leída en sentido amplio. Orden de llamadas documentado (Detect→Evaluate sobre el mismo frame, una vez por señal; réplica con anillo pre-append y L sobre anillo+señal, 36/36). (3) `bestAsk < L` es condición ya necesaria de todo ACCEPT con fees no negativas y `entryVWAP ≥ bestAsk` (multi-nivel endurece a `entryVWAP < L`); no cambia veredictos, no se adopta como detector ni margen — decisión Owner/Metis si cambiara la estrategia.

### Validación

- Citas textuales verificadas por lectura directa de preregs, informe y fuente (líneas citadas); re-lectura de cada documento escrito; `sha256sum` sobre las rutas escritas; `git -C <repo> status --short` limpio y `rev-parse HEAD` = `c0c35e7…`; sin red/captura/raw/engine.db/OOS/cuentas/órdenes/push. Bloqueo registrado: perfil público global del bootstrap no legible por el guard (nombres plausibles y `ls` denegados, sin variantes).

### Rollback

- Vault: revertir las ediciones listadas (historia preservada en el propio texto del informe y de la continuidad). Repo: nada que revertir (`c0c35e7` intacto). Sin OUT nuevo.

---

## 2026-10-30 (W1-m) — instrumentación económica implementada (P0-2/P0-3/P1-4/P1-5/P2-6), episodio sellado re-exportado con identidad por fila; decisiones EXACTAS preservadas; commit `9f6caaa`

### Cambio

- **Tipo:** created / updated (sesión one-shot W1-m, GLM-5.3-Flash; host Hefesto; hook fijado `6771fc068113759bfe31840e19fdb8f62865495c35b17221389e51341dfb5350` no modificado; stop duro 05:00 UTC cumplido)
- **Archivo(s) del vault:**
  - `10-projects/Personal/Polymarket Engine/Research — Economic Instrumentation W1-m 2026-10-30.md` (nuevo; informe canónico del shot)
  - `80-agents/journal/sessions/2026-10-30-polymarket-w1m-instrumentation-summary.md`, `…feedback/system-1/2026-10-30-polymarket-w1m-instrumentation-feedback.md`, `…agent-runs/2026-10-30-zcode-glm-5.3-flash-polymarket-w1m-instrumentation.md` (nuevos, materializados con `materialize_schema_note.py`)
  - `80-agents/journal/logs/2026-10-27-polymarket-engine-entity-updated.md` (anexo pendiente W1-l registrado con atribución honesta), este change_log (sección añadida)
- **Repo externo (fuera del vault):** commit LOCAL **`9f6caaa`** «w1m economic instrumentation P0-2 P0-3 P1-4 P1-5 P2-6 with revision route rename» (5 archivos, +1143/−28, sobre `c0c35e7` sin amend; árbol limpio; sin push): `cmd/researchpilot/economics.go` (ventana de referencia con identidad por fila + accept_rows; descomposición completa de round trips ACCEPT con `WalkSideDetailed`/`LevelTake`; timestamps/gaps por fila con fin de segmento REAL en `invalid_gap`; provenance de fees; `revisionDirName` → `analysis-revision-w1m-20261030`), `cmd/researchpilot/supervisor_test.go` (destino de receipts vivos a la ruta nueva), y 3 archivos de test NUEVOS (`cmd/researchpilot/w1m_instrumentation_test.go`, `internal/economics/w1m_scheduled_test.go`, `internal/regimes/w1m_schedule_test.go` — test-only, cero código de producto; sports congelado intacto).
- **OUT nuevo (fuera del vault):** `validated-baseline/w1-j-single-episode-pilot-20261029-lot3/analysis-revision-w1m-20261030/` — `analysis-revision-w1j-ep-20261029T2230-identity.json` (`revision_run_id w1m-revision-20261030T031117.575690517Z`, sha256 `d646e56e…`), prereg `w1m-prereg-side-leadership.md/.json` fijados ANTES de la revisión, `w1m-run-receipt.json` (comandos/exit/hashes), `w1m-comparison-w1j.json`, `offline-preflight.json`/`inputs.json` producidos por TestMain, binario `pilot-supervisor` (`91fd24c1…`). Sellados intactos re-medidos: original `8fc7ec9d…`, revisión W1-j `93e7fe79…`.

### Motivo

- Ejecutar el incremento técnico aprobado por Metis (plan W1-l): exportar lo que el journal sellado ya contenía (déficit de REPORTE, no de captura) sin cambiar estrategia, parámetros ni decisiones; sin captura/red/órdenes/OOS; REAL_FEE_READY=false.

### Resolución aplicada

- P0-2: `reference_window` por fila (rechazos Y accepts) con hasta 10 observaciones pre-append `{seq,wall,bid,ask,mid,spread_bps}` + frame de señal marcado; `ref_bps` (EXCLUYE señal, orden Detect congelado `sports.go:262/282`) y `reference_level_L` (INCLUYE señal, orden Evaluate `:514`) re-derivables; flags de inclusividad explícitos. P0-3: `signalRow` con descomposición completa por nivel de ambas patas, fees por pata, gross, B\*, H=señal+300s y reason codes estructurados; campos nuevos con valor o null explícito (inerte hoy: 0 ACCEPTs reales). P2-6: H, latencias señal→entrada y salida→H (segundos y registros WS), `segment_index`/`segment_end_utc` reales; `invalid_gap` declara el fin de segmento OBSERVADO que lo causa. P1-5: `fee_formula_applied` (bound lineal vía BuildQuote), `fee_schedule_applied`=null con razón «never applied in this pilot», evidencia citada como W1-e/capture-v6 de OTROS mercados (tick 0.01, mbf/tbf 1000 legacy INTERVAL [0,1000]/UNRESOLVED, fd verbatim). P1-4 (test-only): oráculos de `LevelCost == truncate6(rate·p^e·(1−p)^e·take)` (fixture SYNTHETIC_FIXTURE, exponente 2, pineado 0.822328), Σ por nivel == `FeeTotal`, INTERVAL [0,500]/UNRESOLVED sin POINT inventado, REAL_UNVERIFIED etiquetado no-certificación. UNKNOWN W1-l cerrado: `EncodeLevels` trunca a `TopLevels=6` niveles por lado (documentado en assumptions). Regla descriptiva preregistrada (partición total bid_led/ask_led/mixto/NO_IDENTIFICADO sobre derivas exactas contra medianas por lado de la ventana; sin causalidad, sin tuning): en datos reales 50306… `bid_led` (bid −0.01/ask 0) y 61296… `ask_led` (bid 0/ask +0.01) — los dos assets abren por lados OPUESTOS.

### Validación

- Precondición crítica ejecutada primero: ambos destinos declarados en fuente antes de tests (hook abrió tests/revisión sólo entonces). Suite EXACTA verde (ok cmd/researchpilot 9.499s / internal/economics / internal/regimes) con los pines preexistentes de decisiones/agregados EXACTOS (72 rechazos, cobertura sellada) still green; build EXACTO exit 0; gofmt `-l` vacío; `git diff --check` limpio; revisión nativa ÚNICA exit 0: INCONCLUSIVE preservado, 18393/18400 frames, 72 = A 36 + S 36 exactos; comparación por asset/seq contra el artefacto congelado idéntica en los solapes verificados (recibo dedicado); correcciones ordinarias registradas: 2 ciclos de compilación de tests propios (API error-chaining de foundation) + 1 lógica de test corregida (S sí tiene 1 ACCEPT); flake único preexistente de timing (198.19ms vs 200ms bajo carga) verde en re-ejecuciones. Denegaciones del hook (ls/wc/grep/sha256sum multi-arg/TaskOutput/TodoWrite/log /tmp) registradas sin bypass; resolución con herramientas dedicadas. No ejecutado: `sufficiency_deficit` de entrada sin caso sintético directo (NOT RUN); sensibilidad de L incluir/excluir no calculada (decisión Owner, prereg v3).

### Rollback

- Repo: `git revert 9f6caaa` (local; sin push; `c0c35e7` intacto). OUT: el directorio W1-m es aditivo y puede archivarse; sellados no tocados. Vault: eliminar la nota W1-m y los 3 registros journal, revertir la sección de este log y el anexo W1-l en la bitácora 2026-10-27 (historia preservada en el propio texto).
