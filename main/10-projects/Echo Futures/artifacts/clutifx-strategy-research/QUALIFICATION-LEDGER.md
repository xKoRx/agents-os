# QUALIFICATION-LEDGER — Echo Futures / ClutiFX (qualification-first, 2026-10-24)

Autoridad: skill [[30-resources/agents/skills/echo-retester-master/SKILL.md|echo-retester-master]] + [[30-resources/runbooks/echo-futures-strategy-qualification-runbook.md|runbook de cualificación]]. Ejecución en Hefesto, binario `echo-backtest-clf-qual-20261024` (sha256 `7ec9e425…`) @ commit `83a9b84c` (rama `experiment/clutifx-s01`, push `a7e00a8e` con readback). Trimestre calificado: **NQU6** (contrato físico único, 2026-06-14T22:00Z→2026-09-13T22:00Z, 60 sesiones declaradas). Preset/MM/costos idénticos: `CLF-DEV-GROSS500-V1` (riskgeometry GROSS500, CHALLENGE_ONLY+CONTINUOUS_V1). Recibos: `Hefesto:~/echo-work/clutifx-backtest/qualification/receipts/` (schema `echo.strategy-qualification.v1`); guard fail-closed de admisión G5 en `research_lab.py::_run_one` (commit `a7e00a8e`, 14 tests negativos/positivos + demo E2E).

## Veredicto ejecutivo

**Gates G0–G3 PASS en las 9 identidades con código V1; G4 trimestre NQU6 = `QUARTER_NO_PASS` en las 9 (0 `CHALLENGE_PASSED` en 5 compras conciliadas) ⇒ histórico autorizado = ∅, G5 ejecutado = 0.** Resultado honesto según el mandato: ninguna estrategia ClutiFX está calificada para cómputo histórico.

## Gates por identidad (identidades con código V1)

| Identidad | Knob declarado (único eje) | G0 | G1 | G2 smoke NQU6 | G3 rollover NQM6→NQU6 | G4 trimestre NQU6 | Promoción |
|---|---|---|---|---|---|---|---|
| CLF-VAR-C02 | control STR-002 (TS_CLOSE) | PASS | PASS | PASS (9.709 evals/6.182 ready/1 señal→fill) | PASS (ready en NQU6 desde ad-20260615) | NO_PASS (9 señales, 1 compra, +335,08 USD) | QUARTER_NO_PASS |
| CLF-VAR-C06 | control STR-006 (failure swing) | PASS | PASS | PASS (9.828/6.182/0) | PASS | NO_PASS (0 señales, genuinamente raro) | QUARTER_NO_PASS |
| CLF-VAR-S01 | TS_EARLY_1M | PASS | PASS | PASS | PASS | NO_PASS (4 señales, 0 compras financiadas) | QUARTER_NO_PASS |
| CLF-VAR-S02 | TS_M30 | PASS | PASS (fix `83a9b84c` rojo→verde) | PASS (10.031/6.182/0) | PASS | NO_PASS (4 señales, 0 compras financiadas) | QUARTER_NO_PASS |
| CLF-VAR-S09 | exit temporal_v5 | PASS | PASS | PASS (1 señal→fill) | PASS | NO_PASS (9 señales, 1 compra, +335,08 USD) | QUARTER_NO_PASS |
| CLF-VAR-S10 | setup_timeframe 1h | PASS | PASS | PASS | PASS | NO_PASS (17 señales, 1 compra, +1.325,06 USD — mejor retrospectiva) | QUARTER_NO_PASS |
| CLF-VAR-S16 | range_reference immediate_prev | PASS | PASS | PASS (1 señal→fill) | PASS | NO_PASS (5 señales, 1 compra, −39,94 USD) | QUARTER_NO_PASS |
| CLF-VAR-S17 | TS_WICK_NEXT | PASS | PASS | PASS | PASS | NO_PASS (4 señales, 0 compras) | QUARTER_NO_PASS |
| CLF-VAR-S20 | redflags off | PASS | PASS | PASS (1 señal→fill) | PASS | NO_PASS (16 señales, 1 compra, +335,08 USD) | QUARTER_NO_PASS |

Recibos por identidad: `qualification/QUALIFICATION-SUMMARY.json` + 9 recibos firmados por digest; detalle económico completo en `Hefesto:~/echo-work/clutifx-backtest/reports/G4-QUARTER-ECONOMICS.md`.

## Resto del universo (34 IDs, 35 sustituciones efectivas; sin expansión cartesiana)

| Estado | Identidades | Causa exacta |
|---|---|---|
| BLOCKED_SPEC_V1 | S03 (bias EMA), S04 (bias estructura), S05a/b ×2 (bias DMI+ADX ADX≥20/≥25) | `bias_engine` V1 sólo acepta `native`; motores TESTED (P2 `f165ef08`) pero el knob no está autorizado en config V1 |
| BLOCKED_SPEC_V1 | S11 (TF objetivo 1d) | `dol_timeframes` V1 restringido a `{4h}` |
| BLOCKED_SPEC_V1 | S12≡C05, S13 (refinado 15m/30m) | sin seam de refinado de entrada en V1 (P3b) |
| BLOCKED_SPEC_V1 | S14, S15 (tolerancia FS estricta/amplia) | mapeo de knobs FS no declarado/autorizado; no se inventan valores |
| NOT_IMPLEMENTED | C01, C03, C04 (estrategias de sesión), T01, T02, T03 | código P3b no existe (worker sin commits); detectores base disponibles |
| NOT_IMPLEMENTED | C07, S18, S19 (reentrada/rearme STR-009) | versión técnica documentada; sin código en V1 |
| BLOCKED_DATA | STR-007 (SMT), STR-008 (noticias), C08, T05 | sin segundo instrumento sincronizado ni calendario económico en Hefesto; PROHIBIDO sustituto NQ |

## CLF-Q02 — completar el catálogo viable + gates (2026-10-24/25, ONE-SHOT)

Autoridad: mismo skill+runbook. Binario sellado `echo-backtest-clf-q02-20261024` sha256 `9d813228…` @ `c127b894` (rama `experiment/clutifx-s01`; commits del ciclo `cd7b2ea4` funnel-naming, `c759360e` ejes, `de37a492` snapshots de motores, `374e89ab` dedup compositor, `c127b894` scope DOL midterm). Trimestre: el MISMO NQU6 sellado (ventanas byte-idénticas a la cualificación previa). Corridas: `~/echo-work/clutifx-backtest/q02/{G2,G3,G4}/` (recibos `q02/receipts/`).

**Conciliaciones del mandato**: (A) la cifra "10 identidades G1–G3" eran CORRIDAS (smoke S10 con intento 1 cancelado); el censo de recibos da exactamente 9 identidades × 5 gates. (B) la clasificación previa dejaba 5 IDs sin clasificar (S06/S07/S08/S21/T04) — cerrados. **RCA `no_entry=UNKNOWN`**: rechazo legítimo por política del provider — `PAUSED_SESSION` (ventana operable 9:30–15:55 ET; las emisiones 4h caen fuera salvo la vela 13:00 ET); fix de diagnóstico `cd7b2ea4` nombra las causas en el funnel (reporting puro). **C02≡S09**: alias de ejecución demostrado (9/9 señales y 6/6 fills idénticos al nanosegundo); S20 identidad propia (16 señales). Detalle: `q02/reports/CLF-Q02-FUNNEL-RCA.md`.

**Gates de las variantes nuevas (15 identidades con código Q02)**: G1 suites clf+detectors verdes con tests de dominio/fronteras ancladas/ventana refinado/presupuesto re-emisión/predicado horas clave/round-trips; G2 14/14 + G3 14/14 (canario NQM6→NQU6, ready post-roll) y G4 = `QUARTER_NO_PASS` en las 15 (0 pases en 12 compras; S15/T04 sin señales). Desbloqueos: S03/S04/S05a/b (motores sesgo), S06/S07 (anclas), S11 (DOL 1d midterm), S12≡C05/S13 (refinado STR-005), C07/S19 (rearme STR-009), S15 (FS amplia), S21 (red flags duras), T04 (FS×horas clave), T01 (CME×refinado). Aliases sin corrida: S14≡C06, S18≡C02, C05≡S12. T02 `BLOCKED_SPEC` (sin ancho de stop declarado). STR-001/003/004 (+S08/T03) quedan NOT_IMPLEMENTED con detectores listos (worker bloqueado por cuota de subagentes; trabajo restante declarado).

**Recursos**: techo 5 motores (límite 6), admisión MemAvailable 1,4 GiB, RSS ~1,9 GiB/motor, cero OOM/huérfanos. **Nota de suite**: `v3/backtester` Go tiene 17 fallos + 1 hang PRE-EXISTENTES en `a7e00a8e` (A/B verificado en worktree limpio; área platform readback/faults; no bloquea la vía real — suites python OK). **Histórico: G5 eligible=0, executed=0** (23 identidades con campaña propia acumuladas, 0 pases en 17 compras).

## Antecedentes del run DEV congelado (no sustituyen gates)

- 24,06 engine-hours medidas en el lote DEV 444 sesiones; ~17,3 h detenidas en vuelo por la orden del Owner (`STOP-RECEIPT-20261024-qualification-first.md`).
- S02-DEV (identity `90356a14`): 525.959 evaluaciones, 84,1% ready, 0 señales — causa raíz TS_M30 sin vela de confirmación, corregida (`83a9b84c`); RCA: `Hefesto:~/echo-work/clutifx-backtest/reports/S02-ROOT-CAUSE-TS-M30-CONFIRMATION.md`.
- El "0 ready / 15.256 evaluaciones" previo era una mala lectura del contador de candidate warmup (14.290 callbacks finitos post-rollover, mecánica correcta); el ready real fue 84% constante.

## Recursos de la sesión de cualificación

- G2: 10 smokes (~10 sesiones) ≈ 10 min wall con 4 motores; RSS ~1,8–1,9 GiB/motor. G3: 10 canarios con roll físico ≈ 10 min wall. G4: 9 campañas del trimestre ≈ 45 min wall con 4–5 motores; cero OOM, cero huérfanos, techo global ≤6 respetado.
- Cómputo evitado: 0 históricos de 3 años lanzados; el guard rechaza admisión G5 sin recibo con pase (exit 78, testeado con 14 tests + demo E2E en la vía real de admisión).
