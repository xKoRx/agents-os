# Echo Futures — D2-08 Strategy Runtime Worker — Change Log

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - main/10-projects/Echo Futures/Echo Futures — D2-08 Strategy Runtime.md (nuevo; autoridad candidata de Q11)
  - main/10-projects/Echo Futures/Echo Futures.md (sección D2-08 añadida; sin tocar decisiones previas)
  - main/80-agents/memory/internal/agent-memory/2026-09-28-echo-futures-d2-08-continuity.md (nuevo; continuity_key `echo-futures/d2-08-worker`)

## Motivo

- Worker ONE-SHOT D2-08 (mandato del owner vía SUBMANAGER): resolver `Q11 — Strategy Runtime` del gate D2 tras el cierre de D2-07 (OD-D2-07-1 CLOSED, D2-07 Manager CLOSED 2026-09-28), que desbloqueó D2-08.

## Fuentes usadas

- [[Echo Futures]] (decisiones owner D2-01..03, closures D2-04..07, rollout D6), [[Echo Futures — D2-04 Operation Order Fill Position]], [[Echo Futures — D2-05 Instrument Session Provider]], [[Echo Futures — D2-06 Market Runtime]], [[Echo Futures — D2-07 Execution Runtime]].
- Source físico `xKoRx/echo@372af59a` (clon `~/aranea/work/d4-shot1-20260925/echo`, fetch sin delta): `v3/core/internal/functions/{strategy_config,execution_planner,mm_engine}.go`, `v3/sdk/domain/reference_event.go`, `v3/sdk/mm/*`, `v3/sdk/statefun/constants.go`, `v3/sdk/kache/`, `v3/core/deploy/flink-statefun/develop/module.yaml`.

## Resolución aplicada

- Q11 cerrado como `CLOSED_CANDIDATE` con `READY_FOR_MANAGER_REVIEW`: `echo/strategy_engine` (key `strategy_id`) como owner del estado técnico; trigger contract declarativo; evaluación ⇒ 0..N Signals ordenadas con `signal_id` + `(strategy_eval_seq, signal_seq)`; egress `echo.signals.v1` EXACTLY_ONCE; fan-out con target set linealizado y semántica enabled/disabled; MM como plugin de `echo/operation` con triggers propios (mercado opt-in); boundary LIVE/EXACT_REPLAY/BACKTEST con lógica pura; seam legacy `ReferenceEvent→Signal` en Core; reuse map con evidencia física por path/blob.
- Reconciliación documentada: "0 or 1 Signal" del mandato vs `0..N` de la decisión owner D1 (A1) — congelada lista ordenada `0..N` con el caso 0/1 dominante.
- Sin reapertura de D2-01..07; sin código; sin providers; sin owner decisions nuevas (sólo ratificaciones técnicas ordinarias al manager).

## Validación

- Baseline Echo re-verificada por fetch (`origin/master = 372af59a…`, sin delta).
- Contraste físico de los archivos mandato §4 y sus dependencias directas (blobs y contenido citados en el artifact §21/Fuentes).
- Read-back físico post-commit de las tres rutas editadas (ver handoff de sesión).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales de máquina (el path del clon es workspace externo registrado, no persistido como autoridad), secretos ni memoria interna.

## Rollback

- `git revert` del commit de persistencia de esta sesión; sin efectos fuera del vault.
