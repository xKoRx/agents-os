# CLF-Q03 — SESSION COMPATIBILITY (FASE 2)

Fecha: 2026-10-25 · Herramienta canónica: `campaign-lab/session_compatibility.py` (repo, con 7 tests)
Gate: diagnóstico obligatorio de G2, clasificación que decide la ejecución de G4 por identidad.

## 1. El gate

`STRATEGY_SESSION_COMPATIBILITY` analiza la traza real (`economic.ndjson[.gz]`) de una corrida y produce, por identidad:

- horario efectivo de cada señal OPEN en `America/New_York` (DST correcto vía zoneinfo; jamás offset fijo);
- ventana de entrada que el AccountPolicy realmente impone (E2T/GAU50: `[09:30, 15:55)` ET, pausa hasta el siguiente NY open);
- correlación de rechazos por `SignalID` desde los records `OPERATION_APPLY/CAMPAIGN_SIGNAL` (nunca por razón predominante del día);
- distribución horaria local de las emisiones;
- evidencia de ejecución posible cuando existe intersección.

Clasificación: `SESSION_COMPATIBLE` (≥1 señal en ventana), `SESSION_INCOMPATIBLE` (señales emitidas y TODAS fuera de ventana ⇒ no ejecutar G4 para esa identidad; no significa estrategia incorrecta ni perdedora), `INCONCLUSIVE_NO_SIGNALS` (sin señales: la frecuencia la decide el G4). Prohibido modificar horarios de Provider o ventanas de prop firms para fabricar entradas.

Tests: `campaign-lab/test_session_compatibility.py` (7): conversión DST verano/invierno, frontera exclusiva 15:55 ET, correlación por SignalID, CLOSE_ALL no cuenta, distribución horaria, roundtrip de archivo con digest.

Delta metodológico mínimo aplicado (runbook §4 + skill `echo-retester-master` paso 4, `updated: 2026-10-25`).

## 2. Aplicado a las trazas G4 reales de Q02 (sin re-ejecutar nada)

| identidad | señales | en ventana | fuera | rechazadas por sesión | clasificación |
|---|---|---|---|---|---|
| C02 | 9 | 3 | 6 | 4 | SESSION_COMPATIBLE |
| C06 | 0 | 0 | 0 | 0 | INCONCLUSIVE_NO_SIGNALS |
| S01 | 4 | 0 | 4 | 4 | **SESSION_INCOMPATIBLE** |
| S02 | 4 | 0 | 4 | 4 | **SESSION_INCOMPATIBLE** |
| S09 | 9 | 3 | 6 | 4 | SESSION_COMPATIBLE |
| S10 | 17 | 4 | 13 | 11 | SESSION_COMPATIBLE |
| S16 | 5 | 2 | 3 | 3 | SESSION_COMPATIBLE |
| S17 | 4 | 0 | 4 | 4 | **SESSION_INCOMPATIBLE** |
| S20 | 16 | 3 | 13 | 10 | SESSION_COMPATIBLE |

Reproduce exactamente el RCA Q02 (las 17:00Z conversiones de C02/S09 dentro de ventana; S01/S02/S17 con 0 conversiones por emisiones 4h/1m fuera de la ventana E2T). Bajo el gate nuevo, G4 NO se habría ejecutado para S01/S02/S17 — el ahorro es el trimestre que Q02 gastó en descubrirlo. Detalle por señal: `q03/session-compatibility/STRATEGY_SESSION_COMPATIBILITY-<ident>-G4.json` (los conteos por señal difieren de los por día: C02 tiene 6 señales fuera de ventana pero sólo 4 rechazadas por sesión — las otras 2 fueron absorbidas por otras guardas).

## 3. Q03 G2 smokes (ventana corta 2026-06-14→06-25, contrato NQU6)

| identidad | señales | en ventana | clasificación | lectura |
|---|---|---|---|---|
| C01 (London ideal) | 0 | 0 | INCONCLUSIVE_NO_SIGNALS | el soup-before-London es genuinamente raro en 11 sesiones; G4 evalúa frecuencia |
| C03 (NY continuación) | 1 | 1 | **SESSION_COMPATIBLE** | evidencia de ejecución: señal → admisión → 2 fills |
| C04 (NY reversal) | 0 | 0 | INCONCLUSIVE_NO_SIGNALS | el patrón objetivo-en-London + reversal-5:00 es raro en 11 sesiones |

Cero señales con 63,7% `ready` no es fallo del motor: es `READY_LOW_SIGNAL` (runbook §4). Las tres identidades pasan a G3/G4 para evaluar frecuencia real.
