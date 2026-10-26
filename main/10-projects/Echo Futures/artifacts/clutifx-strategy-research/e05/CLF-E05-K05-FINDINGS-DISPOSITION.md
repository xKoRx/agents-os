# CLF-E05 — K05 FINDINGS DISPOSITION

Fecha: 2026-10-26 · `OWNER_ACCEPTANCE: REVIEW`

## Estado del handoff: `HANDOFF_REQUIRED`

El handoff obligatorio de Daedalus **no existe**: `10-projects/Echo Futures/artifacts/clutifx-strategy-research/k05/CLF-K05-HANDOFF.json` no está en el vault (búsqueda exhaustiva por nombre `CLF-K05*` y por contenido en todo `10-projects/Echo Futures/`, cero resultados) ni en Hefesto (`~/echo-work`, run roots). Tampoco existen `CLF-K05-HEFESTO-IMPLEMENTATION-HANDOFF.md`, `CLF-K05-FIXTURE-SPECIFICATIONS.md` ni `CLF-K05-SOURCE-CERTIFICATION.md`. No hay digest que validar ni commit Echo auditado por K05.

Conforme al mandato: no se inventaron interpretaciones del curso; se ejecutaron las correcciones demostrables por recibos; se bloquearon exclusivamente los cambios dependientes de conocimiento; se registra `HANDOFF_REQUIRED`; el ciclo NO se declara completo. El trabajo independiente sí ejecutable se realizó completo (FASES 1, 2, 3, 5, 6, 7, 9, 10).

## Disposición de las áreas de corrección K05 (prioridad 1–10 del mandato)

| # | Área | Disposición E05 | Motivo |
|---|---|---|---|
| 1 | Failure Swing — conjunción y temporalidad | `SOURCE_REVIEW_REQUIRED` (KRR-003 sin cambios) | la duda R11/R12 (OB obligatorio u opcional) exige la fuente; Q04 ya la dejó formulada |
| 2 | Turtle Soup — variantes de resolución | Sin cambios; S01/S02/S17 mantienen veredicto Q03R1/Q04 | corrección exige claims K05 |
| 3 | Rango y DOL | Sin cambios de lógica | ídem |
| 4 | Sesiones y anclas | Sin cambios de lógica | ídem (adaptación de anclas = decisión Owner KRR-001/002/004) |
| 5 | Bias | **Hallazgo nuevo E05-01** (ver abajo); corrección bloqueada | la semántica correcta del gate sustituido es una decisión de fuente/Owner |
| 6 | Refinados | Sin cambios | ídem |
| 7 | Reentradas | Sin cambios; eje vivo demostrado | ídem |
| 8 | Red flags | Sin cambios; eje vivo demostrado | ídem |
| 9 | Stops y objetivos | Sin cambios | ídem (KRR-005 sigue) |
| 10 | Salidas | Sin cambios; eje temporal_v5 vivo demostrado | ídem |

## Hallazgo nuevo E05-01 (no requiere K05 para ser demostrado; sí para corregirse)

```text
FINDING_ID: E05-01
SOURCE_CLAIM: matriz §7 — S03/S04/S05 sustituyen el motor de bias del gate de entrada (la cadena nativa permanece como control interno, no como gate)
SOURCE_VERDICT: NO VERIFICABLE SIN K05 (handoff ausente)
OLD_IMPLEMENTATION: el gate de entrada consulta exclusivamente p.bias.NativeAggregate() (control nativo siempre-encendido): decision.go:196 y 390, session_decision.go:140 y 246. El agregado del motor configurado (Aggregate(), bias.go:366) tiene CERO llamadas en código de producción.
CORRECT_BEHAVIOR: el motor sustituido (ema/structure/dmi_adx) debería gobernar (o participar en) la condición de entrada según su configuración — decisión de fuente/Owner, NO resuelta aquí.
CODE_PATH: v3/sdk/futures/strategies/clf/{decision.go,session_decision.go,detectors/bias.go,detectors/bias_engines.go,config.go}
TEST_POSITIVE: bias_test.go demuestra que el motor EMA computa y su agregado difiere del nativo (NewBias(EngineEMA) → Aggregate().Engine==EMA).
TEST_NEGATIVE: ningún test puede voltear el gate vía motor sustituido: estructuralmente imposible con el cableado actual.
IMPACTED_VARIANTS: S03, S04, S05A, S05B (4 configs; veredicto Q03R1 QUARTER_NO_PASS queda como evidencia de lo que corrió — réplicas de facto de C02, exec idéntica al céntimo según Q04)
GATES_INVALIDATED: ninguno retroactivamente (el código corrió así); la INTERPRETACIÓN de esas campañas como evidencia del eje bias queda anulada. Cualquier fix futuro crea identidad nueva y exige repetir G1–G4 propio.
DISPOSITION: MISWIRED_CONFIG / IGNORED_PARAMETER · corrección BLOQUEADA (HANDOFF_REQUIRED + decisión Owner) · registrada en KRR-008
```

## Compromiso anti-relajación

No se relajó ningún detector por producir cero señales (KRR-003 sigue abierto sin tocar código); no se introdujo ninguna variante fuera del catálogo; la matriz E05 conserva exactamente los 34 IDs / 35 sets declarados.
