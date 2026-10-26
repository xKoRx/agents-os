# CLF-K05 — HEFESTO IMPLEMENTATION HANDOFF

Destinatario: implementador Echo (Hefesto) · Base auditada: `xKoRx/echo` @ `e8c2e47e` (`experiment/clutifx-s01`, tree limpio) · Naturaleza: INSTRUCCIONES EXACTAS de corrección; Daedalus no modifica código. Cada corrección lleva: qué cambiar, dónde (símbolo/línea), comportamiento esperado, fixture que lo demuestra (FX-NN de `CLF-K05-FIXTURE-SPECIFICATIONS.md`) y gates a repetir. Orden de aplicación recomendado: H1 → H2-H4 (mismo paquete FS) → H5 → regresiones → re-gates; H6-H8 son identidades nuevas pre-declaradas (ciclo propio cada una).

## H1 — Puerta de bias por motor configurado (F-K05-01 · P1 · CORRECTION_READY)

En las cuatro puertas de entrada, sustituir `p.bias.NativeAggregate()` por el agregado del motor configurado `p.bias.Aggregate()`, manteniendo la lectura nativa como diagnóstico del payload:
- `v3/sdk/futures/strategies/clf/decision.go:196` (entryRange) y `decision.go:390` (entryFailureSwing).
- `v3/sdk/futures/strategies/clf/session_decision.go:140` (entryLondon) y `:246` (entryNYContinuation).
- NO tocar `entryNYReversal` (sin puerta de bias por diseño; añadir comentario explícito, F-K05-13).

Semántica pre-declarada necesaria (fijar ANTES de codificar, es decisión de identidad): con el motor configurado en neutral (`facing|mixed|none|undetermined|di_equal|warmup`) la entrada se rechaza con `CLF_BIAS_NOT_FAVORING` (fail-closed, coherente con ch08 R5 «rangos enfrentados ⇒ ignorar el TF»); propuesta por defecto, alternativa «fallback a nativo en neutral» SOLO si el Owner la pre-declara. Citas del payload: conservar `ch03 R1·c-0050 / ch02 R16·c-0086` y añadir la etiqueta del motor. Tests: FX-05 (tres motores × direcciones cruzadas + neutral) y regresión de que `engine=native` conserva el comportamiento C02 bit-a-bit (fixture de humo contra el golden NQU6 existente). Gates a repetir: G0/G1 de S03/S04/S05A/B como identidades de comportamiento NUEVAS (los recibos previos de estas variantes quedan invalidados como medición del eje; preservarlos como historia con nota KC-02).

## H2 — Order block opcional en FS (F-K05-02 · P0 · CORRECTION_READY)

`detectors/failureswing.go`: introducir `FSOrderBlockMode string` (`required` (compatibilidad) | `optional` (nuevo default SOURCE)); en `advanceAttempt`, con `optional` resolver en cuanto `Reaction && motive` (el OB deja de ser condición de resolución y se registra como diagnóstico del veredicto: `order_block_present bool`); con `required` comportamiento actual. Cablear el knob en `Config` (`fs_order_block_mode`, default `optional`, fail-closed en valores desconocidos; C06 existente pasa a `required` explícito en su parameter set para conservar identidad histórica). Fixture FX-01. Nota: el default `optional` cambia el comportamiento del spec `CLF_FAILURE_SWING_V1` ⇒ nueva identidad de config (nuevo `configuration_hash`); las campañas C06/S15/T04 previas se preservan como baseline de contraste (ya lo prevé Q04 §5).

## H3 — Predicado de reacción = creación de rango opuesto (F-K05-03 · P0 · CORRECTION_READY)

`detectors/failureswing.go`: sustituir `reactionClose` por la detección de `EventRangeCreated` con `Range.Side == opuesto(Dir)` en la propia cadena del detector (la cadena ya corre en `feedBase`; sólo falta exponer los eventos de la cadena interna — `RangeChain.FeedEvents()` ya existe). La reacción queda confirmada por el cierre de la vela que crea el rango (causal). Eliminar el predicado de cierre (o dejarlo como diagnóstico `close_beyond_level` informativo). Fixture FX-02 (par A/B). Citas: `ch06 c-0012/c-0029` + átomo `ch01 c-0005`.

## H4 — Ventana por defecto hasta invalidación (F-K05-04 · P0 · CORRECTION_READY)

`detectors/failureswing.go`: nuevo modo de ventana `until_invalidation` (default SOURCE): la observación permanece abierta mientras el extremo fallido NO sea tomado y el intento no sea sustituido; `strict`/`wide` quedan como modos experimentales con su semántica actual. La invalidación usa el hecho ya disponible en `tryNewAttempt`/`markConsumed` (toma del extremo por una vela posterior). Re-arma tras veredicto o invalidación (el flujo P3a ya lo hace). Fixture FX-03. `FSTolerance` pasa a ortogonal al modo de ventana (renombrar el knob en config si se quiere claridad: `fs_window_mode` + `fs_reaction_bars` para wide).

## H5 — Rangos adversos de la propia cadena en el evaluador FS (F-K05-05 · P1 · CORRECTION_READY)

`v3/sdk/futures/strategies/clf/pipeline.go`: para `SpecFailureSwingV1` exponer las ranges activas de la cadena interna del FS (getter nuevo en `FailureSwing`, p.ej. `AdverseActive(dir)`) y pasarlas en `decision.go:376–382` como `AdverseRanges`. La lectura «rangos a favor» (c-0058–c-0060) queda documentada como la lectura de la misma cadena en la dirección del trade (diagnóstico), sin bloqueo adicional (la preferencia pendientes>reiniciados es personal dicha). Fixture FX-04. Citas: `ch09 c-0007/c-0012`.

## H6 — [IDENTIDAD NUEVA pre-declarada] Refinado en specs de sesión (F-K05-06 · P1 · REQUIRES_OWNER_AUTORIZACIÓN de eje)

Permitir `RefineTF` en `SpecLondonIdealV1`/`SpecNYContinuationV1`/`SpecNYReversalV1` (relajar `config.go:205–207`), reutilizando el mecanismo `pendingRefine`/`resolveRefine` (`decision.go:279–339`) con la ventana de la vela de sesión correspondiente. Nuevas identidades C01r/C03r/C04r (hash propio), fixtures FX-06, ciclo G0→G4 completo cada una. La escalera 8h→4h→1h→15m queda como eje opcional declarado (no bloquea).

## H7 — [IDENTIDAD NUEVA pre-declarada] Rango activado por FS como premisa de sesión (F-K05-07 · P1 · REQUIRES_OWNER_AUTORIZACIÓN + depende H2-H4)

En C03/C04: aceptar como «rango claro» previo un rango activado por veredicto FS legítimo del día (el FS del paquete, ya con H2–H4) además del sweep clásico. La premisa objetiva-tomada y las red flags no cambian. Fixture FX-07; fuentes: `ch07 c-0197–c-0206`, `ch06 c-0028/c-0057`.

## H8 — [IDENTIDAD NUEVA pre-declarada] Materializaciones pendientes del propio ciclo (KRR-007)

(a) S08 tras la decisión de base de salida (F-K05-12/KC-04): config de C03 con `exit_mode` alternativo; (b) T03: condicionante `C04 ∧ MidTermDOL()!=nil ∧ !MidTermDOL().Taken` (el scope midterm ya existe en `dol.go`). Ambas con G0→G4 propios.

## No-cambios explícitos (prohibidos sin nueva autorización)

Anclas horarias del curso (KRR-001/002/004 → decisión Owner); T02 stop-extra (KRR-005); STR-007/008 sin datasets sellados (KRR-006); red flags y sus fuerzas; los topes de higiene; el contrato Strategy/MM (sin cuentas ni fills en la Strategy); las salidas técnicas personales/probabilísticas (F-K05-08) salvo pre-declaración; NADA que convierta un OR fuente en AND o un condicional en obligatorio.

## Definition of done por corrección

Suite verde + fixture dedicado + determinismo (mismo build+inputs) + sin lookahead (arnés vigente) + citas claim-a-claim en los Details + recibos G-propio por identidad afectada + plan_digest/identidad de ejecución sellada en toda campaña nueva. Las variantes afectadas NUNCA heredan el PASS de otra (regla dura del runbook).
