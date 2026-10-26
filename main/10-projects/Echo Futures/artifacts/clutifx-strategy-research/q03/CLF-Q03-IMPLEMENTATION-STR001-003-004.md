# CLF-Q03 — IMPLEMENTACIÓN STR-001 / STR-003 / STR-004 (FASE 4)

Fecha: 2026-10-25 · Commit `2ee3f7fc` (base `c127b894`) · Paquete: `v3/sdk/futures/strategies/clf` (+ `session_ctx.go`, `session_decision.go`)

## 1. Diseño general

Las tres estrategias de sesión montan sobre la MAQUINARIA EXISTENTE de STR-002 (cadena de rangos, emisión Turtle Soup, DOL de sesión, bias nativo, red flags, exits) — cero detectores duplicados. Lo nuevo es un **contexto de sesión por día** (`SessionState`, estado JSON puro) y las decisiones de entrada por spec:

- Velas de sesión del curso 4h: 21/17/1/5/9 `America/New_York` (ch07 R1·c-0002/c-0003; ch02 R3), clasificación por la location IANA del ancla (DST correcto, B12).
- Hechos del día: `AsiaExpansion` (cierre de la 21:00 fuera de la vela previa — operacionalización de cadena ch01 R7; la definición numérica de "expansión" es NOT_IN_SOURCE), `LondonTaken` (objetivo de sesión tomado DURANTE la ventana London — la premisa ch07 c-0147), `FiveCandle` (cierre 5:00 contra el objetivo elimina el día, ch07 c-0166–c-0168), `NineOpen` (apertura 9:00 contra la dirección, ch09 R7·c-0073). Bloque-día = [21:00 → 21:00) NY.
- Red flags completas con los inputs de sesión cableados (`ObjectiveTaken`, `AsiaExpansionPrevious`, `NineCandleOpensAdverse`); STR-002/C02 queda intacto (sus recibos no se invalidan).

## 2. Las tres specs

### CLF_LONDON_IDEAL_V1 — STR-001 "London ideal" (C01, T1)
- Emisión TS con la referencia ANTERIOR a London (ch07 R2·c-0010 "TS ya hecho") dentro de `[01:00, 05:00)` ET (ch07 c-0003: la vela operable es la 1; R3·c-0030/c-0061 EXCLUYE la sopa hecha por la propia vela de London — su emisión a las 05:00 cae fuera de ventana).
- Gates: dirección == DOL de sesión, DOL apuntando a favor, red flags completas (con ObjectiveTaken probabilístico y AsiaExpansion), bias nativo a favor (checklist R27·c-0229 "rangos a favor").
- Stop = extremo barrido (ch07 R16·c-0109 / ch01 c-0067); objetivo diagnóstico = DOL; salida base = **temporal vela 5:00** (matriz C01; ch07 R14·c-0075–c-0077).
- Escenarios 2/3 del curso cubiertos por la estructura: sin sopa previa a London no hay entrada (escenario 2); la creación del pendiente ES el disparador (escenario 3).

### CLF_NY_CONTINUATION_V1 — STR-003 "NY continuación" (C03, T1)
- Emisión TS dentro del span de la vela 9:00 `[09:00, 13:00]` con referencia en vela ANTERIOR (ch07 R19·c-0145 / c-0054: "TS formado a las 9", la vela 5 crea, la 9 cabalga).
- Gates: DOL de sesión alineado y NO tomado hoy (`dol.Taken || Session.LastDolTaken != nil` — el hecho del día sobrevive al recompute del DOL); cierre 5:00 contra la dirección ⇒ bloquea el día; red flags con `NineCandleOpensAdverse`; bias a favor.
- Salida base = objetivo (DOL); `exit_mode` versionado.

### CLF_NY_REVERSAL_V1 — STR-004 "NY reversal" (C04, T1)
- Premisa: objetivo de sesión TOMADO durante London (`Session.LondonTaken`, primer completado del día-block, ch07 c-0147 / ch02 R12·c-0068).
- Emisión TS dentro del span de la vela 5:00 `[05:00, 09:00]` en dirección OPUESTA al objetivo tomado (ch07 R20·c-0148: la 5:00 toma el extremo previo y crea el rango contrario — exactamente el pendiente que la emisión materializa).
- Stop = extremo barrido (espejo ch01 c-0067 / ch03 c-0164); objetivo = extremo opuesto del rango recién creado (ch01 R2·c-0025 vía R20; cota V1 del alcance 6–8h de ch07 c-0150). Sin gate de bias (la fuente no lo exige; la hard flag de rangos en contra sigue protegiendo). `ObjectiveTaken` viaja como evidencia probabilística.
- Fail closed: sin rango recién creado ⇒ `CLF_REVERSAL_RANGE_MISSING` (jamás objetivo fabricado).

## 3. Reglas del contrato (verificadas por tests)

Cada Strategy: implementa el contrato actual (`StrategySpec/Requirements/DecodeConfig/EncodeState/Evaluate`), declara Requirements (4h+1d; 30m sólo con TS_M30), snapshots completos con roundtrip JSON por evaluación, evalúa con barras cerradas y causalidad 1m (la emisión es el puntero del detector antes/después del feed), sin información futura, sin MM interno, sin tocar Provider. Presupuesto de re-emisión STR-009 y warmup silencioso heredados.

Config fail-closed de sesión: SetupTF debe ser 4h, ancla course (las horas de sesión son horas course), DOL scope {4h} (el mid-term es eje de STR-002), `refine_timeframe` prohibido (es STR-005-sobre-STR-002), knobs FS prohibidos, exit default por spec (C01 temporal_v5; C03/C04 target).

Corrección estructural adicional: `capture/restore` del pipeline extendido a la familia de rango (las specs de sesión no persistían chain/TS/DOL → warmup perpetuo detectado por el propio G1). Y en `pipeline.feed` el observador de sesión lee el puntero del DOL ANTES del feed 1m: `checkTaken` marca y ELIMINA el rango completado en la misma llamada (la transición de toma se perdería).

## 4. Tests (suite verde completa: clf 111s OK, detectors 63s OK)

`session_specs_test.go` — geometrías 1m scripted sobre el patrón probado del fixture STR-002, colocadas en las velas de sesión (t0 = 2026-02-16 21:00 ET):

1. C01 positivo: emisión en la apertura de London (bar 1679 = Feb-18 01:00), stop en el barrido, salida temporal 5:00 (bar 1920).
2. C01 negativo R3: la sopa hecha POR London emite a las 05:00 → `CLF_OUTSIDE_LONDON_WINDOW`, sin entrada.
3. C03 positivo: la 5:00 hace la sopa, la emisión a las 09:00 cabalga (bar 2159).
4. C03 negativo: objetivo tomado durante London → `CLF_CONTINUATION_TAKEN` (con el hecho del día sobreviviendo al recompute).
5. C04 positivo: objetivo tomado en London + 5:00 barre y cierra adentro → LONG opuesto, objetivo = extremo del rango nuevo (99.45 ≠ stop 96.85), premisa en diagnósticos.
6. Warmup silencioso ×3 specs (sin draft, sin ciclo).
7. Gates de config fail-closed (4 rechazos nombrados).
8. Semántica de ventanas + DST (EST/EDT, bordes inclusivos/exclusivos por spec).
9. Matriz de gates (10 casos): soup-stale, DOL mismatch, no-DOL, presupuesto agotado, red-flag dura por rango adverso, five-against, sin-premisa, mismo-lado, rango-faltante, espejo SHORT con objetivo al low.
10. Rechazo de spec desconocida actualizado al nuevo mensaje.

Cobertura de los archivos nuevos: helpers de sesión ~92–100%; entradas 72–91%; las ramas restantes son defensivas fail-closed (`ReasonReversalNoRange` sin entrada real que la alcance con detectores íntegros) o errores de I/O (`return err`).
