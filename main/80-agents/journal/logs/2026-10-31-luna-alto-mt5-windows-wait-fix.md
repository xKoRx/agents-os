---
type: change_log
schema_version: 1
scope: session
created: "2026-10-31"
updated: "2026-10-31"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
related:
  - "[[Echo + Echo Forge — Environment Contract]]"
aliases: []
confidence: verified
source_session: "2026-10-31-luna-alto-mt5-windows-wait-fix"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-31-luna-alto-mt5-windows-wait-fix

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes-humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `80-agents/memory/internal/agent-memory/2026-10-31-echo-forge-luna-alto-mt5-windows-wait-continuity.md` (checkpoint privado nuevo, `continuity_key: echo-forge/luna-alto-20261031-mt5-windows-wait`, `load_policy: manual`) — creado.
  - `80-agents/journal/logs/2026-10-31-luna-alto-mt5-windows-wait-fix.md` (este change_log) — creado.
  - Repo `xKoRx/symphony`, rama `codex/forge-independent-logical-types` (worktree privado `~/aranea/work/forge-independent-logical-types-20261029`): `412c50e` (fix), `ac306fc` (bookkeeping del manifest 0.6.4), `41ac205` (correcciones de Shot 2), `31e6990` (Shot 1b + riesgo V6b declarado). Release `0.6.5` publicada con `vcs.modified=false` y `vcs.revision=31e6990`.

## Motivo

- El worker MT5 en Windows (`mt5-kronos`, release 0.6.4) quedó **bloqueado 5,5 h** con un `terminal64.exe` vivo tras `Terminal exit with code 0`: el cálculo había terminado (55 270 679 ticks, HTM y CSV escritos) y el proceso se quedó en el teardown post-salida (`MQL5.community authorization failed` → `LiveUpdate timeout on stop`). El executor no tenía timeout (`configured_timeout_ms=0`) ni gracia, y su `select` no tenía rama viva; la activity `mt5_backtest_artifact` quedó `Started` con `start_to_close_timeout` de 100 años, la lease del slot nunca se liberó y los 5 hermanos quedaron `Scheduled`. Run B quedó bloqueado sin poder materializar Top 4 ni ingesta en Echo.
- El fix separa **fin del cálculo**, **drenaje del proceso propio** y **resultado durable reconocido**: la señal terminal correlacionada al intento (journal por offsets + HTM del path del intento) arma una **gracia de cierre acotada y configurable**; expirada, se termina **sólo el job propio** y el resultado conserva el **código de salida y la razón físicos** (una muerte por temporizador nunca es exit 0). El PASS exige drenaje acreditado + parser nativo del reporte de ese intento; si falta cualquiera, es error técnico con evidencia conservada.
- El checkpoint registra la causa con evidencia, el plan de drenaje, los hallazgos del verificador independiente (H1–H6, V6b) y la deuda que queda declarada.

## Fuentes usadas

- `80-agents/journal/logs/2026-10-31-echo-forge-luna-alto-top4-campaign-continuity.md` y `10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2.md` (continuidad LUNA_ALTO).
- `30-resources/aranea/07-integration/Echo + Echo Forge — Environment Contract.md` §0.1 (sqx-prop único workspace), `30-resources/runbooks/stager-windows-mt5-cutover-and-occupieddrain.md`, `30-resources/runbooks/symphony/echo-forge-golden-e2e.md` y la skill de repo `.agents/skills/echo-forge-testing/SKILL.md` (procedimiento canónico de pruebas).
- Evidencia física: FlowRun `a5eafeb7-da3a-4986-9bfb-e2b005da2144` (wave `LUNA_ALTO_20261031b`), child `…-754c3d397dcee983` attempt 227; logs de `mt5-kronos` (`session-worker.out-20261031-135126.log`, `logs\20261031.log` del terminal, `Tester\logs\20261031.log`); evidencia del stager `C:\ProgramData\Aranea\evidence\stager-evidence-latest.json`; `wavecount` de los oráculos de `~/aranea/work/luna-alto-20261031/bin/`.

## Resolución aplicada

- Shot 1 (implementador local) → `412c50e`. Shot 2a (verificador independiente, autor distinto) → los 7 oráculos PASS, sin regresión de atribución. Shot 3a (correcciones de los hallazgos) → `41ac205` y `31e6990`, re-verificados (R1–R5 PASS).
- Shot 2b: release `0.6.5` publicada por el mecanismo canónico, **`vcs.modified=false`** (se corrige el defecto de higiene heredado de 0.6.4); drenaje del slot ocupado en orden (señal de drain → admisión cerrada probada por contadores de intento intactos → terminación de **sólo** la raíz del job propio verificada por identidad → lease liberada → adopción de 0.6.5 por el supervisor); canario de **backtests consecutivos en el mismo worker y slot, sin reinicio, sin kill manual y sin limpieza manual entre ellos** (4× `activity.ok status=success` a 67–76 s de separación); el intento que llevaba 5,5 h colgado completó en 58,2 s.
- Batería Windows ejecutada **nativamente** (binario de test cross-compilado en Linux, transferido y verificado por SHA256, ejecutado en `mt5-kronos`): 15 PASS / 3 FAIL, con los 3 FAIL **preexistentes y ambientales** (invocan `/bin/sleep` y `sh -c`), probado ejecutando también el binario del commit base en el mismo host ⇒ cero regresiones en la vía Win32.

## Validación

- Regresión de atribución medida por el manager: `cmd-executor` ok; `mt5` 7; `mt5/binding` 27; `normalization` 10; `report` 28; `activities/worker` 68 ⇒ **140 preexistentes, conjunto de nombres idéntico** antes y después.
- Impacto físico en el wave: `mt5-backtest.v1` de **0 → 6** evaluaciones; el grupo **iteró con candidatas nuevas** (`apply-selected-run` 6→12, `retester` 6→12, `optimizer` 6→12, `wfm` 102→204, `final-reretester` 6→10, `mt5-compiler` 6→7); evaluaciones totales 258 → **401**.
- **Pendiente, no cerrado**: el cierre del group y la ingesta a Echo DEV por task de Forge (la tabla `strategy_ingestion_receipts` sigue con **1 sola** fila, de un smoke del 2026-10-28, que no es una entrega por task). Ese es el gate que sigue abierto.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- El release `0.6.5` se revierte con el mecanismo de rollback del stager (ACTIVATION `rollback_of`), no con una release nueva improvisada. El código está en la rama `codex/forge-independent-logical-types` sin pushear ⇒ revertir es `git revert` de `412c50e`…`31e6990` más un release nuevo. Los commits son **normales y privados**: no hay tag ni release publicada en git que deshacer.
