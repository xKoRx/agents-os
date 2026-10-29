---
type: change_log
schema_version: 1
scope: session
created: "2026-10-29"
updated: "2026-10-29"
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
