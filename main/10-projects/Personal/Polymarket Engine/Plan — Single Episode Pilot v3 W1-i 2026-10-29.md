---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related:
  - "[[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]]"
  - "[[Plan — Single Episode Pilot v2 W1-h 2026-10-29]]"
  - "[[Research — Causal Metadata Renewal W1-i 2026-10-29]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
aliases:
  - "W1-i single episode pilot plan v3"
tags:
  - kind/doc
  - topic/research-ops
created: "2026-10-29"
updated: "2026-10-29"
---

# Plan — Single Episode Pilot v3 W1-i 2026-10-29

## Propósito

- Receta **ejecutable por especificación, NO ejecutada** de UN episodio piloto descriptivo, que reemplaza la secuencia temporal de [[Plan — Single Episode Pilot v2 W1-h 2026-10-29]] en las dos piezas corregidas: (i) los deadlines **absolutos por tramo** con presupuesto total ≤90 min que **incluye** discovery/REST/reconexión/cierre (la v2 no cabía: 6×15 min de `record` más los observes excedían la ventana), y (ii) la **renovación causal de metadata idéntica** (opción B adjudicada, implementación W1-i con un paso de wiring pendiente, §4). Nada de este plan inicia red, captura ni servicios: requiere adjudicación de Metis (esta spec + §4 completado + ventana autorizada). V1/V2 preservadas como historia.

## Contenido

### 1. Presupuesto temporal V3 (deadlines absolutos relativos a K; tests: `TestW1IRecipeAbsoluteDeadlines`)

| Tramo | Ventana absoluta | Duración |
|---|---|---|
| Discovery (`catalog select`, ≤3 requests) | termina ≤ `K−95 min` | acotado, fuera del sobre |
| `clob observe --phase init` | `[K−90m, K−89m)` | 1 min |
| Tramos `record` i=1..6 | `[K−89m + (i−1)·14,5m, +13,5m)` | 6×13,5 = 81 min |
| `clob observe --phase final` tras cada tramo i | `[fin tramo i, +1m)` | 6×1 = 6 min (el 6º = final) |
| Cierre (verify/manifest/sellado) | `[K−2m, K)` | margen 2 min |

- Total pasos = **88 min ≤ 90 min**, con **margen de cierre 2 min**; tramo+observe = 14,5 min **< TTL 15 min**: la cadena de completaciones de observe queda espaciada bajo el TTL y **la elegibilidad nunca decae** (la razón de ser de la opción B).
- Regla de **censura ex ante**: un poll cuyo outcome aterriza después del deadline de su slot se **descarta y declara** (jamás se captura como a-tiempo ni se estira al slot siguiente). Deadline inclusivo.
- **Sin señal evaluable en los últimos 300 s antes de K** (sin horizonte permitido, conforme v2): `señal+300s ≤ K`.
- Si la ventana `[K−90m, K)` **no cabe íntegra** antes de la pausa 02:00–08:00 GMT-3 (half-open) o antes de K: **NO iniciar captura** (nunca truncar).

### 2. Precondiciones de despacho (todas obligatorias)

1. **§4 completado**: migración `0025_regime_observations.sql` + wiring reducer/service (≈40 líneas mecanizadas abajo) con la regresión 6/6 PASS repetida. **Sin §4, la receta V3 pierde su razón de ser** (el gate enviaría `observation_stale` desde el tramo 2).
2. Adjudicación Metis de esta spec + ventana autorizada; perfil por-shot del hook con las formas exactas (lección W1-d).
3. Kickoff elegible por prereg v2 §3 (descubrimiento 3 requests/100 candidatos; `NO_ELIGIBLES_EN_LOTE` honesto permitido). UN partido; ≤4 mercados/8 assets.
4. Espacio: proyección ≤3,1 GB ≪ stop-line 8 GB (preflight del lanzador antes de arrancar; abortar al stop-line; jamás borrar datos para caber).

### 3. Identidad y artefactos

- Data-dir nuevo por episodio con run-id único: `w1i-ep<YYYYMMDDTHHMM>-<runid>/`; jamás sobrescribir; inputs W1-h y fixtures previos intactos.
- La renovación requiere **UN journal**: cada re-poll es un record durable con `(received_wall, capture_seq)` — el ledger se proyecta de ahí (§4); los gaps entre tramos siguen siendo gaps declarados (señal que cruza gap ⇒ `invalid_gap`, v2 intacto).

### 4. Wiring de la opción B — EJECUTADO en el segmento 2 (sin commit; queda UN desbloqueo)

**Estado (actualiza la especificación original, que se preserva abajo como historia):** los pasos 1–3 ya EXISTEN en el árbol de trabajo @ `9e2c6b7` sin commit — `migrations/0025_regime_observations.sql` creada desde los esquemas reales (0020–0024 leídos; `IF NOT EXISTS`, `INTEGER PRIMARY KEY`, `UNIQUE (entity_id, capture_seq, source_ref)` con `DO NOTHING` como idempotencia de re-proyección), reducer conectado en las 3 ramas con contadores `ObservationsNew`/`RenewalsNew`, y `AssetConstraintAsOf` consumiendo el ledger vía `EvaluateRenewedConstraint` con **chequeo de completitud** (cada revisión con su primera observación; ledger parcial ⇒ ruta legacy fail-closed, reconstrucción por replay — jamás frescura inventada) e `Inspect` con `observations`. Test nativo `TestW1IRenewalLedgerNativeThroughService` cubre la ruta REAL (T16 invariante, T20 known, ledger T0+T20, first_seen, re-drain idempotente, restart/rebuild deterministas). Fixture W1-h actualizada sólo en frescura (historia declarada). Regresión: 5/6 paquetes PASS; `internal/experiment` rojo en UNA sonda — `TestW1FCaptureV6GateAvailabilityTrial` P5 — cuyo premisa es la semántica retraída (ancla init con consulta a seq=frontier, donde la renovación final está legítimamente admitida; el engine es correcto y `regime_digest` invariante). **Único paso pendiente:** la corrección de 2 líneas en `internal/experiment/w1f_hypothesis_integration_test.go` (sondas de expiración P5 en `a.FirstSeq`, PIT-consistente con el ancla; comentario explicativo ya redactado) — archivo denegado por el hook en esta continuación. Desbloqueado eso: re-corrida 6/6 y commit 'Renew causal prospective metadata observations for research' con el subset completo (migración + reducer + service + fixtures).

**Especificación original (historia del diseño, ejecutada según lo indicado):**

1. **Migración** `migrations/0025_regime_observations.sql` — runner embedded, forward-only (persist aplica cada `.sql` en una transacción y registra checksum):

   ```sql
   CREATE TABLE regime_observations (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       entity_id INTEGER NOT NULL REFERENCES regime_entities(id),
       revision INTEGER NOT NULL,
       content_hash TEXT NOT NULL,
       capture_seq INTEGER NOT NULL,
       received_wall TEXT NOT NULL,
       source_ref TEXT NOT NULL,
       capture_ref TEXT NOT NULL,
       provenance TEXT NOT NULL
   );
   CREATE INDEX idx_regime_observations_entity ON regime_observations(entity_id, received_wall, capture_seq, id);
   ```

2. **Reducer** (`internal/regimes/reducer.go`, en `upsertRegimeRevision`, los tres branches): (a) revisión nueva → INSERT observación (revision=latestRev+1, seq=rec.Seq, wall=rec.ReceivedWall, captureRefOf/provenanceJSON) + `stats.ObservationsNew++`; (b) dedup contenido idéntico → INSERT observación (revision=latestRev) + `ObservationsNew++`, `RenewalsNew++`, `last_observed_at` se mantiene como hoy (sólo metadata de inspección, jamás leída por AsOf); (c) contenido que retorna → SELECT id,revision del hash visto → INSERT observación de esa revisión. Contador `RenewalsNew`/`ObservationsNew` en `ApplyStats.Add`.
3. **Service** (`AssetConstraintAsOf`): si la entidad tiene filas en `regime_observations` (JOIN revisions por (entity_id, revision)) → `regimes.EvaluateRenewedConstraint` (ya enviada y probada); si no tiene ninguna → ruta legacy por revisiones (hoy: stores proyectados pre-0025 degradan a semántica W1-h fail-closed — reconstruir con `replay` para ganar renovaciones; nunca frescura falsa). Extender `Inspect` con las observaciones (auditoría de renovaciones con provenance).
4. **Aceptación** (ya fijada por tests): `TestW1IRenewalLedgerContractFromJournal` pasa SIN tocar el test (el ledger deja de ser derivado a mano y pasa a leerse de la tabla); sondas W1-e invariantes; no-lookahead drain invariante; regesión 6/6 PASS; `replay` ×2 schedules reproduce el ledger (las renovaciones se re-proyectan del journal).
5. **Compatibilidad declarada**: formato journal intacto (0 cambios en capture); stores viejos no reconstruidos quedan en ruta legacy (degradación fail-closed documentada); sin backfill mágico ni parsing de provenance en SQL.

### 5. Secuencia serial del episodio y supervisión de procesos propios

- Misma forma que v2 §4 (catalog select → observe init → [record 13,5m → observe final]×6 → verify → manifest → replay ×2 → sellado), con los deadlines absolutos de §1 y los flags reales de v2 §1.
- **Exclusión por supervisor (obligación propia, NO lock de SO):** antes de CADA paso que abra el data-dir: (i) verificar que no haya proceso propio vivo usando ese data-dir (lista de procesos propios + su status-file/heartbeat); (ii) **fallar cerrado** si existe un writer desconocido o incierto — no recuperar writers ajenos vivos, no matar procesos ajenos, no tocar permisos OS. **Límite documentado:** esto NO es exclusión global entre procesos ajenos al operador; la exclusión real por data-dir (lock) queda como bloqueo separado — no hay patrón compatible en el repo (W1-i §4 del informe).
- **Stop-file EN deadline:** el supervisor prepara el checkpoint ANTES (verify del tramo anterior, recibo) pero **genera la señal exactamente EN el deadline** del paso (crear el stop-file antes corta el `record` inmediatamente — defecto v2); pausa completa 02:00–08:00 GMT-3 sin gracia; checkpoint/cierre preparados antes de 02:00.
- Fallo de paso ⇒ el paso muere con recibo; el siguiente exige decisión del operador; sin retry automático; tras 1310/ECONNRESET: preservar logs/exit, `journal verify` antes de cualquier relanzamiento, estado incierto declarado.

### 6. Presupuesto y límites

- Requests: discovery ≤3 (aparte) + `clob observe` 7 invocaciones ×12 lecturas REST (v2 §6) reportadas por separado; sin reintentos; 429/`retry_after_seconds` ⇒ registro y fin del paso.
- Bytes: ancla medida 0,0894 MB/min; peor caso hipotético 20× ≈ 0,16 GB; medición real al sellar; stop-line 8 GB dura; TOTAL workspace ≤10 GB.
- Recursos: un comando a la vez; CPU 2 / RAM 2 GiB (prlimit); horario 08–02 GMT-3 todos los días; sin daemon/cron/background huérfano.

### 7. Qué NO es este plan

- No ejecuta nada hoy; no programa campañas (25 ventanas siguen desprogramadas: 40 GB > techo); no promete elegibilidad (con la opción B la expectativa pasa de ≈15/90 a ≈88/90 de ventana elegible con metadata estática — se MIDE, no se asume); no convierte el piloto en validación de rentabilidad; no certifica fees (`REAL_FEE_READY=false`).

## Fuentes

- [[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]] (spec vinculante; §4 opción B adjudicada), [[Plan — Single Episode Pilot v2 W1-h 2026-10-29]] (receta v2, preservada).
- [[Research — Causal Metadata Renewal W1-i 2026-10-29]] (implementación y bloqueador). Código: commit `9e2c6b7dd26e70a53b05499a2d682ef33f1dac27` (`internal/regimes/renewal.go` + tests `w1i_renewal_integration_test.go`: deadlines, censura, stop, arranque).
- Fuente @ `853c0e4` leída para flags/comandos reales: `cmd/engine/{record,clob_observe,catalog_select}.go`, `internal/capture/capture.go`, `internal/persist/migrate.go`. [[Polymarket Engine — Continuidad Five-POC 2026-09-20]].
