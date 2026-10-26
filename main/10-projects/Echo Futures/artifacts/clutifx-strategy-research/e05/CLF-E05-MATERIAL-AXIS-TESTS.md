# CLF-E05 — MATERIAL AXIS TESTS (FASE 5)

Fecha: 2026-10-26 · Método: evidencia de cableado en código (file:line sobre `experiment/clutifx-s01` @ `e8c2e47e`) + fixtures de la suite Go (verde completa: `clf` 116,9s + `detectors` 70,0s, exit 0) + comportamiento físico NQU6 (recibos Q04/Q03R1) · `OWNER_ACCEPTANCE: REVIEW`

Los diez casos especiales del mandato, más el resto de ejes materiales de la matriz. Vocabulario exacto del mandato. La regla: una variante que sólo cambia el nombre y nunca puede cambiar una regla efectiva NO es una variante material certificada.

## Casos especiales

### S03/S04/S05A/B — motores alternativos de bias: `MISWIRED_CONFIG` (E05-01)

- Instalados: sí — `config.go:90-97,288-294` valida `bias_engine ∈ {native,ema,structure,dmi_adx}` y `bias_adx_threshold`; `pipeline.go:163` construye `NewBias(cfg.biasConfig())`.
- Reciben datos y calculan: sí — `detectors/bias_engines.go` implementa los motores; `detectors/bias_test.go:50-63` prueba el agregado EMA con motor propio (`Aggregate().Engine == EngineEMA`) y lecturas distintas del nativo.
- Consultados por el gate final: **NO** — las únicas cuatro consultas de bias en producción (`decision.go:196,390`; `session_decision.go:140,246`) usan `p.bias.NativeAggregate()` (control nativo, `bias.go:368-369`); `Aggregate()` del motor configurado tiene **cero** llamadas fuera de tests.
- Pueden diferir del control en un fixture causal: **no pueden, en ningún mercado** — el gate es ciego al motor configurado. Persistencia/rollover no cambian esto (`pipeline.go:270,326,364` mantienen el mismo objeto).
- Conclusión: parámetro aceptado pero ignorado por la decisión; ejecución NQU6 idéntica a C02 al céntimo (Q04) era el síntoma. Corrección bloqueada (semántica de fuente/Owner; ver K05-DISPOSITION y KRR-008).

### C07/S19 — reemisiones/rearme: `VALID_SAME_OUTCOME_IN_SAMPLE`

- El parámetro modifica una decisión real: sí — `decision.go:158` y `:353`, `session_decision.go:73` bloquean emisión cuando `st.Emissions[key] > cfg.MaxReemissions` (`ReasonReemissionsExhausted`).
- Fixture de rearme genuino: `catalog_variants_test.go:270 TestCLFReemissionBudgetExhausts` demuestra ambos lados (bloqueo por presupuesto agotado y desbloqueo con presupuesto).
- En NQU6 el rearme nunca ocurrió (exec idéntica a C02): eje vivo, sin efecto en muestra; no es alias (S18≡C02 sí es alias por default 0, verificado en Q03).

### S09 — salida temporal vs objetivo DOL: `VALID_SAME_OUTCOME_IN_SAMPLE`

- La configuración de salida llega al motor y produce cierre distinto cuando el escenario lo exige: sí — `decision.go:89-90` (`timeExit := p.exitsRep.TimeExit && cfg.ExitMode == ExitModeTemporalV5`) y `:116`; fixture `clf_test.go:515+` demuestra el `CLOSE_ALL` en la vela de las 5:00 bajo `temporal_v5` y su ausencia bajo `target`.
- En NQU6 el stop/target siempre precedió a la vela de salida temporal (exec idéntica a C02 al céntimo, Q04): eje vivo, sin efecto en muestra.

### S20/S21 — modos de red flags: `VALID_DIFFERENT_BEHAVIOR` (S20) / `VALID_SAME_OUTCOME_IN_SAMPLE` (S21)

- Los modos distinguen comportamientos: sí — `redflags.go:114` (`off` no evalúa, jamás bloquea), `:118` (hard evalúa sólo flags duros), `:131` (full añade suaves); el gate `decision.go:185` (`ReasonRedFlagsBlocking`) consume `report.Blocking`.
- Fixture: `redflags_test.go` cubre los tres modos; físicamente en NQU6, S20 (off) emitió 16 señales vs 9 de la maestra (13 extra fuera de ventana, Q04) — los mismos fills del trimestre siguen legítimos, pero existe el fixture causal donde el filtro distingue.

### S12/S13 — refinado 15m/30m: `VALID_DIFFERENT_BEHAVIOR`

Señales, sizing, `MM_NO_ACTION` y salida certificados: EXEC-S12 propio (2 rt, 13:15/13:30) y EXEC-S13 propio (1 rt 11:30 + 2 admisiones muertas por tamaño, contabilidad reparada en FASE 2). El funnel completo por eslabón vive en `CLF-E05-Q04-ACCOUNTING-REPAIR.md` y los timelines Q04 (ya correctos).

### S06/S07/T01 — cambios de ancla: `VALID_DIFFERENT_BEHAVIOR`

Los cambios de ancla modifican velas y señales efectivamente: EXEC-S06 (09:30+13:30, 6 rt), EXEC-S07 (10:00+14:00, 3 rt), EXEC-T01 (10:30/11:15/14:15, 3 rt) — tres patrones propios y distintos de la maestra en NQU6 (Q04, fingerprints de ejecución).

## Variantes restantes (misma prueba de diferenciación)

- S10 (setup 1h), S11 (DOL 1d), S16 (leftmost): patrones de ejecución propios en NQU6 → `VALID_DIFFERENT_BEHAVIOR`.
- C03 (sesión NY continuación): subconjunto propio (06-23+08-06) → `VALID_DIFFERENT_BEHAVIOR`.
- C01/C04/S01/S02/S17 (sesión/resolución): emisiones propias demostradas; G2B `SESSION_INCOMPATIBLE` estructural (fiel al curso; adaptación = identidad nueva Owner) → `VALID_DIFFERENT_BEHAVIOR` en emisión + `SESSION_INCOMPATIBLE` como veredicto de sesión.
- C06/S15/T04 (Failure Swing): `VALID_RARE_NO_ACTIVITY` — 0 emisiones en NQU6+NQZ6; la duda de conjunción (KRR-003) exige K05 → componente `SOURCE_REVIEW_REQUIRED`.
- C05≡S12, S14≡C06, S18≡C02: `ALIAS_VERIFIED` (equivalencias demostradas en Q03, no deducción por P&L igual).
- C02: control maestro.

## Resumen (35 configs)

15 `VALID_DIFFERENT_BEHAVIOR` · 4 `VALID_SAME_OUTCOME_IN_SAMPLE` (C07,S19,S09,S21) · 4 `MISWIRED_CONFIG` (E05-01) · 3 `ALIAS_VERIFIED` · 3 `VALID_RARE_NO_ACTIVITY` · 3 `SESSION_INCOMPATIBLE`-con-emisión-propia · 1 control · 2 `HANDOFF_REQUIRED` (S08,T03) · 1 `BLOCKED_SPEC` (T02) · 2 `BLOCKED_DATA` (C08,T05). No se deduplicó nada por P&L igual: la equivalencia EXEC-MASTER (Q04) queda documentada como consecuencia del cableado, y cada clase conserva su fila.
