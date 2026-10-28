# CLF-K05 — MISSING AND EXTRA RULES (FASES 2+5)

Registro de reglas fuente ausentes en la implementación, restricciones añadidas sin fuente, y errores de temporalidad/booleano. Cada hallazgo lleva ID estable (F-K05-NN), clasificación del vocabulario Q04, severidad, y estado (CORRECTION_READY / REQUIRES_OWNER / DECLARED_OK). Las correcciones NO se aplican desde Daedalus: van al handoff de Hefesto.

## F-K05-01 — [P1] Puerta de bias cableada al motor nativo: los ejes S03/S04/S05 son inertes por construcción — WRONG_BOOLEAN_LOGIC / IMPLEMENTATION_DEFECT

Las decisiones de entrada consultan `p.bias.NativeAggregate()` (la lectura SIEMPRE nativa de cadena de rangos) en `decision.go:196` (entryRange), `decision.go:390` (entryFailureSwing), `session_decision.go:140` (entryLondon) y `session_decision.go:246` (entryNYContinuation). `Aggregate()` — el agregado del motor configurado — no tiene ninguna llamada de producción. Consecuencia: con `bias_engine=ema|structure|dmi_adx` el motor calcula su lectura (bias.go) pero jamás gobierna; las variantes S03/S04/S05A/B no podían diferir del control C02 aunque el mercado lo permitiera, y 5 campañas pagadas midieron el mismo comportamiento por construcción, no por datos. El CSV e05 ya lo registra como `MISWIRED_CONFIG (E05-01)`; Q04 lo había atribuido erróneamente a «defaults compartidos» (ver corrección de conocimiento F-K05-11). Estado: CORRECTION_READY (la matriz pre-declaró la sustitución; la semántica del caso neutral del motor — facing/undetermined — requiere una decisión pre-declarada, propuesta en el handoff).

## F-K05-02 — [P0] Order block obligatorio en FS: EXTRA_RESTRICTION

`failureswing.go:301` resuelve el veredicto sólo con `Reaction && OrderBlock`; `c-0047` («puedes esperar si quieres al order block») y el procedimiento canónico `c-0029` (sin OB) hacen del OB una confirmación OPCIONAL. Estado: CORRECTION_READY (adjudicado por fuente; residuo de vídeo acotado §1.1 de la adjudicación).

## F-K05-03 — [P0] Predicado de reacción de FS sustituido: INVALID_OPERATIONALIZATION

`reactionClose` (`failureswing.go:321–326`) = cierre más allá del nivel fallido. Fuente (`c-0012`, `c-0029`, espejo `c-0045`/`c-0046`): reacción = «reacciona ya creando algún rango bajista/alcista» = formación de rango opuesto (átomo ch01 c-0005) sobre el TF de observación. Predicados no equivalentes en ninguna dirección. Estado: CORRECTION_READY.

## F-K05-04 — [P0] Ventana de confirmación FS acotada sin fuente: EXTRA_RESTRICTION

strict = reacción+OB en exactamente la vela siguiente (`failureswing.go:280–318`, `FirstBarAfter`); wide = N=3 (default arbitrario). La fuente no acota la confirmación a una vela: el OB puede esperarse después (`c-0047`), la reacción+OB se desarrollan en varias velas (`c-0041`) y el FS vive hasta que el extremo es finalmente tomado (`c-0048`). Estado: CORRECTION_READY (default fuente = ventana hasta invalidación; strict/wide quedan como variantes experimentales).

## F-K05-05 — [P1] Red flag dura de rangos adversos no evaluada en FS + «rangos a favor» sólo proxizada — MISSING_SOURCE_RULE

`entryFailureSwing` (`decision.go:376–382`) invoca red flags SIN `AdverseRanges` (el comentario lo declara: «no range exposure in V1»); además el pipeline no construye cadena de setup para FS (`pipeline.go:97` sólo para specs de familia rango). ch09 `c-0007`/`c-0012` son una invalidación DURA acotada y aplican a cualquier dirección: con rangos adversos activos «no podemos estar tomando longs». El contexto rangos-a-favor (`c-0058`–`c-0060`) queda reducido al bias nativo 1d. Estado: CORRECTION_READY (exponer las ranges activas de la propia cadena del FS al evaluador; la definición fina de «a favor» sobre la cadena 1h queda como OP declarada).

## F-K05-06 — [P1] Refinado (STR-005) restringido a STR-002: contradice el alcance fuente — MISSING_SOURCE_RULE / WRONG_SCOPE

`config.go:205–207` y `config.go:224–226` rechazan `refine_timeframe` en los specs de sesión y en FS. La fuente define el refinado como el procedimiento transversal de entrada de STR-001..004 (catálogo §3 STR-005; ch04 §2; ch07 `c-0214` «súper clave»: esperar rangos activos a favor antes del TS es exactamente el refinado). La entrada IDEAL de London (P3 de la vela de la 1 refinado a 15m) no es expresable en V1. Además el refinado implementado es un salto único (setup TF → 15m/30m), no la escalera 8h→4h→1h→15m dicha (el salto es OP legítima; la restricción de specs no). Estado: CORRECTION_READY como identidades NUEVAS pre-declaradas (C01r/C03r/C04r con RefineTF; G0→G4 propios) — no es un cambio silencioso del control.

## F-K05-07 — [P1] El FS como activador de rangos en los setups de sesión no existe — MISSING_SOURCE_RULE

ch07 `c-0197`–`c-0206` resuelve el caso difícil de NY EXPLÍCITAMENTE con failure swing: «a las 9: failure swing tras reiniciar el rango este de 8 horas y a las 9 hace la expansión» + `c-0204` «como pasa el failure swing, se te crea este rango de 4 horas ya para subir hacia el objetivo». El instructor usa el FS precisamente para activar rangos SIN toma del extremo y marcar objetivos imposibles sin el concepto (`c-0057`). C03/C04 exigen sweep clásico (TS): los días cuyo rango se activa por FS (el caso ensañado del curso) no producen señal. Es también el hallazgo económico nº 1 de la FASE 6. Estado: CORRECTION_READY como variante pre-declarada (premisa de rango activable por FS en C03/C04); requiere el fix FS primero.

## F-K05-08 — [P2] Salidas técnicas del curso sin implementar — MISSING_SOURCE_RULE (fuerza baja)

Minuto-59 de horas clave: precaución/salida (ch02 `c-0063`/`c-0064` [probabilística]); dos velas de 15m fuertes en contra al entrar: «yo me saldría ya» (ch08 `c-0066`–`c-0068` [personal]); salir en el alto de la nueva vela para que no se cree rango en contra (ch04 `c-0091` [personal]). Los tres son salidas TÉCNICAS (plano Strategy), no MM; no se agregan sin pre-declaración Owner (dos son personales/probabilísticas). Estado: REQUIRES_OWNER (ejés de matriz opcionales).

## F-K05-09 — [P2] Jerarquías colapsadas declaradas — DECLARED_OK con deuda

Bias {1d} vs fuente 6h–3D (`config.go:313–320`; ch03 `c-0050`); DOL sesión {4h} vs 12h/8h/6h/4h (`config.go:239–248`; ch03 `c-0207`); midterm {1d} vs 3D/2D/1D. Restricción de capacidad del motor V1 (barras declarables), honestamente documentada en el código. Deuda registrada para un motor V2 que declare 6h/8h/12h/2d/3d. No es defecto de conocimiento.

## F-K05-10 — [P2] Operacionalizaciones congeladas verificadas honestas — DECLARED_OK

`ApproachTicks`/`EndMinutes`/`WideReactionBars` (NOT_IN_SOURCE, fail-closed); `ToleranceTicks` base 0 con matiz `c-0065` como variante; proxy de expansión Asia = cierre fuera de la vela previa (`session_ctx.go:138`, NOT_IN_SOURCE numérico declarado); variante 8h del pendiente leída como gap-open contra el close previo (`pendiente.go:179–202`, lectura declarada de `c-0054` — ver nota de vídeo V-04); DST vía IANA (NOT_IN_SOURCE, decisión documentada); agrupación 2d/3d épocas fijas (NOT_IN_SOURCE congelada); topes de higiene (8 rangos activos, lookback 8, cap 64, reemisiones ≤8) declarados. Todas conservan su etiqueta y ninguna se presenta como enseñanza. OK.

## F-K05-11 — [P2] Correcciones de conocimiento (ver también CLF-K05-KNOWLEDGE-CORRECTIONS.md)

(a) Q04 `CLF-Q04-SIGNAL-EQUIVALENCE.md` afirma «IMPLEMENTATION_DEFECT: ninguno detectado (las equivalencias son consecuencia declarada de defaults compartidos…)» — FALSO para S03/S04/S05A/B: la equivalencia fue causada por el miswiring F-K05-01 (el e05 ya lo corrige como MISWIRED_CONFIG E05-01). (b) Q04 `CLF-Q04-SOURCE-VS-CODE-AUDIT.md §6` declara el catálogo canónico ausente del vault — HOY FALSO: `knowledge-library/clutifx/strategies/STRATEGIES-CATALOG.md` existe (SHA `4c471314…`, re-domiciliado 2026-10-24; decisión Owner nº 2 de Q04 ya ejecutada). (c) La discrepancia S08 (matriz «C03 base temporal» vs código base=target) — F-K05-12, requiere conciliación antes de materializar S08. Estado: CORRECTIONS_READY (documentales).

## F-K05-12 — [P2] Discrepancia matriz/código en la base de salida de C03 — REQUIRES_OWNER

Matriz S08: «Salida DOL en estrategia de sesión (base temporal)»; `config.go:253–264` fija C03 exit base = target (sólo London ideal recibe temporal_v5). La fuente da ambas salidas para la familia («al DOL; o vela de las 5» — catálogo §5.5), sin fijar cuál es la base de continuación NY. Decisión Owner: (a) C03 base=target y S08=temporal (invertir el rótulo de la matriz), o (b) C03 base=temporal y S08=DOL (cambiar el default). Cualquier opción es identidad nueva para las campañas ya corridas — no retocar en silencio.

## F-K05-13 — [P2] C04 sin puerta de bias — DECLARED_OK (documentar)

`entryNYReversal` no consulta bias — correcto por diseño (la reversión corre contra el movimiento completado; una puerta nativa 1d la anularía siempre) y coherente con `c-0150` (el recorrido lo acotan los rangos 6–8h). Sólo falta dejarlo explícito en el docstring de la spec. Acción documental, no de código.

## F-K05-14 — [P2] Cota de fidelidad intrabar — DECLARED_OK (recordatorio)

Todo concepto intrabar (manipulación del P3, reacción temprana del TS, identificación en vivo del FS) se resuelve a cierres de 1m máximo (sin ticks en el corpus, declarado en HEFESTO-BASELINE-AUDIT). La fidelidad es una cota: los ejemplos del curso deciden dentro de la vela. Ninguna corrección posible sin ticks; mantener la etiqueta en cada recibo.

## F-K05-15 — [P2] F-K05 de KRR-005 re-verificada

Ningún claim de ch02/ch11 declara ancho extra de stop para la entrada temprana (re-escaneo K05); la geometría 20×ATR×q es geometría experimental de Echo (GROSS500), NO enseñanza ClutiFX — el mandato de la misión pedía explícitamente no atribuírsela al instructor. BLOCKED_SPEC se sostiene.

## F-K05-16 — [P3] Nota de simetría SHORT

pendiente/reiniciado y PDM-soporte están definidos sólo en lado alcista en ch01/ch03; la simetría SHORT es fuente-por-uso (catálogo §3 STR-001 matiz). El código clasifica simétricamente por `side==objective` — aceptado por la decisión vigente del catálogo; sin cambio.

## F-K05-17 — [P3] Topes de higiene con efecto conductual posible

`maxActiveRanges=8` elimina silenciosamente el rango activo más viejo (`rangechain.go:475–481`, con razón nombrada en el diagnóstico) — en regímenes con >8 rangos simultáneos podría descartarse el DOL vigente. Instrumentado (transición ACTIVE_CAP_OVERFLOW); vigilar en el funnel post-fix. Sin cambio inmediato.

## F-K05-18 — [P2] La 2ª entrada del esquema (order block confirmado como trigger) no tiene camino de señal

ch04 `c-0034`/`c-0036`/`c-0039` (SET-002): «una vez que el precio HA CERRADO POR FUERA de esa vela» se toma la entrada («menos ideal pero confirma»). El predicado OB existe (en FS) pero no como trigger alternativo de FAM-001. Estado: REQUIRES_OWNER (pre-declarar eje de entrada OB en STR-002/003 — es fuente, no hipótesis; su ausencia reduce frecuencia).

## F-K05-19 — [P2] PDM sin camino de señal

CMP-008/SET-003 (ch04 `c-0017`, `c-0096`–`c-0101`; ch03 `c-0092`/`c-0213`): entrada short exigiendo respeto del alto del rango con confirmación por TF menor; y el filtro no-venta con PDM+reacción (`c-0213`). Sin implementar. Estado: REQUIRES_OWNER (frecuencia adicional fuente-backed).
