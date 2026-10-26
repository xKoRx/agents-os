---
type: runbook
schema_version: 1
scope: area
created: "2026-10-24"
updated: "2026-10-25"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
related:
  - "[[30-resources/agents/skills/echo-retester-master/SKILL]]"
  - "[[30-resources/agents/skills/e2e-gated-validation/SKILL]]"
aliases:
  - runbook de calificacion de estrategias
  - echo-retester-master-runbook
  - strategy quarter first qualification
confidence: high
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/area
  - area/echo
  - tech/backtester
  - action/validate
---

# echo-futures-strategy-qualification-runbook

## Propósito y límites

Procedimiento ejecutable, repetible y verificable para **calificar cada nueva identidad** `Strategy × variante × MM` antes de permitir cómputo histórico costoso de Echo Futures. La skill `echo-retester-master` decide gates y promoción; este runbook posee pasos, receipts, checks de admisión, manejo de fallos y recuperación.

Aplica a ClutiFX, cursos futuros, código de estrategias nuevo, nuevas versiones de un setup y perfiles monetarios candidatos. No autoriza LIVE, mutación de cuentas reales, otro scheduler, alteraciones de RuleSet/Provider ni cambios de contratos del runtime. Los paths absolutos aquí son únicamente ejemplos de Hefesto: resolver los reales en cada corrida.

**Fuente del mandato Owner (2026-10-24):** desarrollar y probar cada identidad; usar el contrato físico NQ más reciente con ~3 meses realmente cubiertos; para avanzar al histórico una identidad debe haber aprobado **al menos un challenge** en ese contrato. Hasta entonces prohibido correr períodos DEV de cientos de sesiones y el histórico completo. Este criterio es un gate de economía de cómputo, NO una certificación de éxito futuro.

## Precondiciones y autoridades

1. Ejecutar `agents-os-bootstrap` una sola vez si corresponde a cold start. Verificar el planner actual `10-projects/Echo Futures/agentes/Echo Futures — Optimización de Campañas.md` y el proyecto particular de estrategias. Contexto reutilizable en warm start; no recorrer el vault completo.
2. Resolver el checkout de `xKoRx/echo`, branch/HEAD, WIP, `git status --porcelain`, árbol y build efectivo. Preservar cambios legítimos; trabajar en rama/commit del proyecto autorizado, sin reset.
3. Leer **fuente autoritativa del catálogo de estrategias**, contratos `v3/sdk/futures/strategy`, MM, Provider, motor `v3/backtester`, datasets sellados y runner real (identificado por inspección). No inventar argumentos `run`/`prepare` ni símbolos.
4. Inspeccionar inventario NQ físico, calendario, períodos de roll, resoluciones de timeframe y exclusiones `RESEARCH_SESSION_EXCLUDED`; los 10 días de NQZ6 del reporte R03 **NO constituyen un trimestre**.
5. Registrar `RUN_ID`, `source_sha`, `binary_sha256` (verificar `vcs.modified=false`), identidad de corpus, `window_id`, lista congelada de `strategy_id/variant_id/profile_id` y `owner_authorization`.
6. El presupuesto de ejecuciones viene de la orden Owner y de gates reales. No interpretar `ONE-SHOT` como permiso ilimitado ni prometer trabajo después de cerrar una sesión.

## 0. Control inmediato: recuperar el cómputo mal encaminado

1. Identificar exclusivamente procesos propios del encargo, supervise/runners/cron y su job/attempt/PGID. Observar con `ps -eo pid,ppid,pgid,rss,etime,args`, `pgrep -a -f` sólo para descubrir; verificar dueño/working directory/command line antes de actuar.
2. Poner en `PAUSED_BY_OWNER_GATE_CHANGE` las nuevas admisiones del lote DEV multicontrato. **No** lanzar nuevos jobs hasta inventariar estado. Interrumpir ordenadamente corridas caras que no cumplen los gates, conservando sus logs, plan, identity y resultados parciales como `INTERRUPTED_BY_OWNER`; nunca convertidas en estrategia perdida. No `pkill` global ni matar procesos de otros proyectos.
3. Reutilizar pruebas válidas de cualquier control (p. ej., C02 E2E), pero **nunca transferir el PASS a S02/C06 ni a otras variantes**. Guardar como muestra diagnóstica la ejecución S02 TS_M30 con `ready=0/15.256` y el cruce de roll que reprodujo el problema.
4. No reinstalar servicios, modificar swap/BIOS, limpiar otro trabajo ni tocar producción.

## 1. Identidades, catálogo y trazabilidad (G0)

Crear un `candidate-ledger` con una **fila por identidad completa**:

```text
strategy_id       Identidad de la lógica de entrada, p.ej. CLF-STR-002
variant_id        Variación semántica exacta (CLF-VAR-S2-...), fuente/OP/HIP
profile_id        MM y presupuesto (R250/R500/R750, NATIVE, etc.)
signal_family_id  Familia de entrada compartida; 1 voto por familia, no por MM
build_sha         Build efectivo del motor
strategy_sha      Código/config que materializa la variante
dataset_sha       Fuente de mercado/calendario/roll y transformaciones
owner_authority   Matriz y parámetros expresamente autorizados
```

- Referenciar `CLUTIFX-STRATEGIES-MASTER.md`, `CLUTIFX-OBJECTIVE-DETECTORS.md`, `CLUTIFX-EXPERIMENT-MATRIX.md` (34 IDs etiquetados/35 sustituciones, NO producto cartesiano), o catálogo de curso equivalente.
- Distinguir enseñanza `SOURCE`, `OPERATIONALIZATION` y `HYPOTHESIS`. La hipótesis del agente nunca se presenta como enseñanza del instructor.
- `STR-005` (refinado) y `STR-009` (reentrada) son capacidades dependientes de una base; no se cuentan como familias independientes sólo por nombre.
- Si dos variantes producen señales idénticas y tienen mismo MM, documentar equivalencia y alias; **no ejecutar duplicados**. Idéntico patrón con otro MM sí es configuración distinta para aprobación, pero nunca estrategia independiente.
- Datos inexistentes (segundo instrumento SMT, calendario de noticias, ticks requeridos) ⇒ `DATA_REQUIRED`; no fabricar valores ni degradar fidelidad silenciosamente.
- **G0 PASS** exige catálogo congelado, input/data/params rastreables y baseline de reproducción. Todo cambio semántico después crea nueva versión.

## 2. Selección del contrato trimestral objetivo (PRE-DATA)

Antes de construir pedidos económicos:

1. Inventariar todos los contratos físicos NQ con primero/último minuto, cobertura por sesión, gaps, DST, días válidos, roll schedule, source manifest hash y disponibilidad de indicadores.
2. Preferir el **más reciente con cobertura trimestral verificable**, ideal 55–65 sesiones de mercado, **mínimo 45 sesiones elegibles con datos ejecutables reales en UN contrato físico**. Elegir por recencia/cobertura, nunca por PnL. Si el contrato más reciente es corto (p. ej. NQZ6 10 sesiones), declarar el dato e intentar el **anterior contrato trimestral completo** (p. ej. NQU6 sólo si los recibos lo demuestran). No juntar dos vencimientos para alcanzar artificialmente 45. Revalidar en cada ciclo: el censo físico 2026-10-25 midió NQZ6 = 17 elegibles (cobertura 2026-09-10→2026-10-06, 2 cortas) y NQU6 = 60 sesiones calificadas 2026-06-14→2026-09-13; NQZ6 califica para G2 LAST-CONTRACT, no para trimestre.
3. Congelar `contract_id`, `stream_id`, fechas de primer/último dato, `warmup_start`, `trade_start`, `end_exclusive`, timezone/calendario y exclusiones. La ventana de mercado y el historial de warmup se verifican por bytes, no por nombre del job.
4. Demostrar que indicadores/HTF reciben un prefix **causal y semánticamente válido**: si un DOL 1D/3D necesita historia previa, sólo usarla si el contrato vigente autoriza continuidad/ajuste y el prefijo está correctamente sellado. Si la fuente no alcanza el lookback legítimo ⇒ `DATA_REQUIRED`.
5. Si ningún contrato aporta ≥45 sesiones elegibles y warmup permitido, **NO pasar a G4/G5**. La obtención/completitud de datos es un trabajo separado, no habilita ejecutar un DEV multicontrato de 444 días como "proxy".

G4 usa TODA la ventana calificada declarada; no truncarla a los días que contienen un pase. G2/G3 pueden usar segmentos cortos para ahorrar tiempo, identificados como canarios técnicos y nunca como G4.

## 3. G1 — Implementar y validar la lógica técnica POR IDENTIDAD

Para cada `strategy_id+variant_id+profile_id`:

1. Compilar y validar `StrategySpec/Requirements/DecodeConfig/EncodeState/Evaluate` en el contrato real; la Strategy no compra cuentas ni decide el MM.
2. Pruebas deterministas positivas y negativas LONG/SHORT (si aplica): setup presente/ausente; límites de umbral; stop/tick alignment; reentradas, invalidación, salida y cierre por sesión; filtros realmente activados.
3. Prueba de causalidad: evaluaciones sólo después de `BarClose`, no leer información de barras futuras; agregación 1m→HTF verificable; timestamps y `America/New_York` con DST cuando sea un concepto del setup.
4. `ready` debe transicionar dentro del presupuesto de barras exigido por `Requirements`. Verificar el contador `evaluations/evaluations_ready` y los predicados bloqueantes; el tiempo de warmup se deriva de los TF/lookbacks y no de un número arbitrario.
5. Integración mínima por variante: `Strategy → Signal → Operation → MM → Provider → order → fill → ledger → close` con ejecución física del simulador en fixture donde existe el patrón. Ninguna cuenta/stop artificial para fabricar `CHALLENGE_PASSED`.
6. Repetibilidad con mismo build+inputs; `Strategy/MM` aplicados coinciden con config sellada.

**PASS**: suite enfocada verde, ejemplos positivos/negativos y determinismo, camino económico E2E ejercitado. Una variante no hereda automáticamente `PASS` de su control aunque comparta paquete.

**FAIL**: `warmup` infinito, `ready=0` después del lookback completo, requirement mismatch, calendario no materializado, señal sin tick/contrato correcto, index lookahead, MM incorrecto, etc. Diagnosticar, corregir, incrementar versión semántica cuando corresponda y repetir sólo gates afectados.

## 4. G2 — Validación física por identidad sobre el ÚLTIMO CONTRATO (split G2A/G2B/G2C)

**Contrato.** Identificar el contrato físico NQ más reciente con datos verificables en el corpus y su cobertura real (censo de sesiones: el primer/último byte, sesiones completas, elegibles y cortas); usar UN solo contrato, sin concatenar vencimientos ni ampliar ventanas en silencio. Al 2026-10-25: NQZ6 = último contrato (cobertura 2026-09-10→2026-10-06, 17 elegibles, 2 cortas), NQU6 = último trimestre completo (60 sesiones calificadas). La ventana sellada del último contrato se registra en `WINDOW_REGISTRY` con `purpose: LAST_CONTRACT` y `contracts: [NQZ6]` (2026-10-25).

**Tres subgates, todos por identidad, sin heredar PASS ajeno:**

- **G2A — readiness / signals / detectors.** Smoke breve del inicio de trading + días ejecutables con lookback legítimo. Recibo por identidad con el funnel completo (ver abajo). `evaluations_ready=0` con barras suficientes ⇒ `FAILED_CORRECTNESS` inmediato; setup no ocurrido ⇒ `READY_LOW_SIGNAL`.
- **G2B — STRATEGY_SESSION_COMPATIBILITY.** Obligatorio antes de G4: cada señal OPEN a `America/New_York` con DST (zoneinfo), confrontada con la ventana que el AccountPolicy impone (E2T/GAU50: `[09:30, 15:55)` ET), correlación por `SignalID` desde `OPERATION_APPLY/CAMPAIGN_SIGNAL`. Veredictos `SESSION_COMPATIBLE` / `SESSION_INCOMPATIBLE` (⇒ sin G4; no es veredicto comercial) / `INCONCLUSIVE_NO_SIGNALS`. Herramienta: `campaign-lab/session_compatibility.py`. Prohibido modificar horarios de Provider para fabricar entradas.
- **G2C — FULL TRADE LIFECYCLE.** Sobre la traza económica real de la corrida G2: ≥1 fill de entrada, ≥1 fill de salida y ≥1 **round-trip reconciliado** reconstruido posición-a-conciencia por `campaign-lab/qualification_ledger.py` (reutiliza `research_lab.reconcile_trades`: un trade cierra sólo cuando la posición neta vuelve a cero; dinero exacto en ticks; fees reales por lado). Posición abierta al horizonte se reporta como `open_at_horizon` y jamás cuenta como trade completo. La operación completa conserva su identidad (entry_at/exit_at, dirección, qty, precios, bruto/fees/neto) e informa win/loss/break-even; ganar no se exige.

**Funnel obligatorio por variante** (cantidades, rechazos y motivo en cada transición; todo cero relevante con explicación verificable):

```text
source minutes → bars closed → requirements satisfied → evals → ready evals
→ detector predicates → opportunities → signals → session eligibility
→ account selection → money management → provider accepted/rejected
→ orders → entry fills → position lifecycle → exit fills
→ trade journal / cash ledger → reconciliation
```

Los rechazos de campaña se clasifican por `input_kind=CAMPAIGN_SIGNAL` + `reasons` (`CAMPAIGN_ALLOWED` vs `CAMPAIGN_UNAVAILABLE`/`SESSION_ENTRY_WINDOW`/`SESSION_SAFETY_CUTOFF`/`SIZE_BELOW_MIN_CONTRACT`/…), correlacionados por `SignalID`; el conteo por señal difiere del conteo por día y ambos se registran.

## 5. G3 — Canary corto de rollover y recuperación de ready (obligatorio)

**G2 monocontrato NO detecta rewarm defectuoso entre rollovers.**

1. Elegir del corpus un roll físico probado (p. ej., ventana corta alrededor del roll 2023-12, confirmando la fecha en el schedule; no codificar fechas recordadas).
2. Ejecutar una ventana **corta** que contenga barras suficientes antes/después del roll y lookback/prefix causal permitido. No usar todo DEV 444 sesiones para demostrar recuperación.
3. Registrar, por contrato y sesión: `BarClose`, demanda TF, estado de warmup, `evaluations`, `ready`, errores de fuente, número de barras de formación/retención, `first_ready_after_roll` y `last_ready_before_roll`.
4. Determinar explícitamente política de reset por rollover: qué estado de `Strategy` se reinicia, qué indicadores se recalientan y de qué corpus obtienen historia. El estado `ready` debe recuperarse dentro del presupuesto declarado por Requirements, no "eventualmente".
5. Validar que en la ventana posterior existan eventos evaluados y `ready=true` cuando su lookback está disponible; contrastar con un fixture positivo y las reglas reales. El patrón puede ser raro sin que sea fallo de readiness.
6. **Ejemplo forense**: S02 TS_M30 alcanzó `0 ready / 15.256 evaluaciones` en 21 meses y reportó ráfagas de warmup en rollovers. Esa identidad **G3 FAIL**, nunca G4/G5 mientras no haya corrección de estado/Requirements/datos.

Para indicadores de lookback muy largo cuya primera oportunidad ready no cabe en un canario compacto, proporcionar prefijo causal legítimo y un fixture de rehidratación para probar la transición; si no es demostrable, G3 `INCONCLUSIVE/DATA_REQUIRED` y no promover.

## 6. G4 — Contrato trimestral: admisión fail-closed antes del histórico

**Este es el único gate que autoriza el histórico largo, y ya no arranca sin cualificación propia.**

- **Admisión (2026-10-25):** toda campaña QUARTER pasa por `qualification_guard.admit_quarter` en la única costura de spawn (`research_lab._run_one`, cubre `run` y `resume --execute`). Exige por identidad: G0/G1/G2A/G2B/G2C/G3 PASS, veredicto de sesión `SESSION_COMPATIBLE`, G2C con ≥1 entry fill + ≥1 exit fill + ≥1 round-trip reconciliado, y la **identidad de ejecución sellada** declarada en el plan: `execution_purpose: QUARTER`, `contract_set` igual a los contratos físicos que el plan realmente lee (filas acotadas del `source_read_plan`), `window_identity` igual a los stamps del plan y `plan_digest` fijando los bytes preparados exactos (JSON canónico del plan sin la declaración de cualificación — `research_lab.plan_identity_digest`). Cualquier campo ausente, ilegible o en desacuerdo ⇒ `QUALIFICATION-BLOCKED.json` con causa exacta, exit 78, cero motores.
- **El propósito lo decide el plan, no la etiqueta.** `effective_execution_purpose` clasifica `SMOKE | LAST_CONTRACT | ROLLOVER_CANARY | QUARTER | HISTORICAL` desde la ventana sellada registrada, el conjunto de contratos físicos y el horizonte económico; un propósito declarado contradictorio bloquea (`PURPOSE_CONTRADICTS_EXECUTION_IDENTITY`). Un estudio multicontrato de 90 días es `HISTORICAL` por conjunto de contratos, aunque su duración quepa en un trimestre.
- **Campañas bit-idénticas:** un recibo de cualificación que ya trae G4 bloquea la puerta (`RECEIPT_NOT_A_QUALIFICATION_CHAIN`); la campaña ejecutada con su recibo existente ES la evidencia y no se repite.
- Ejecutar `CHALLENGE_ONLY + CONTINUOUS` bajo las reglas y costos vigentes, por cada identidad distinta que aprobó la cadena completa. El horizonte es **el contrato trimestral validado** (≥45 sesiones elegibles físicas), no una concatenación de rolls.
- Cuentas continuas y policy real: cada pase/pérdida termina la cuenta correspondiente; denominador = TODAS las compras. **PROMOCIÓN (literal Owner):** `CHALLENGE_PASSED >= 1` *y* cadena G0–G3+G2C PASS *y* ledger/fills/fees/cierre conciliados *y* sin bloqueo técnico abierto.
- **CERO PASES (ejecución válida):** `QUARTER_NO_PASS` ⇒ NO G5. Documentar oportunidades/trades/compras, pérdidas/pendientes y razón. Compra sin pase no es pase; pausa no es pérdida.
- **FASE DE INVESTIGACIÓN:** sólo variantes predeclaradas en la matriz; cambiar umbrales tras mirar resultados crea identidad nueva.

## 7. G5 — Histórico completo SOLO para promovidas

- La cola histórica debe generarse **como intersección exacta** `declared identities ∩ G4 PASS receipts ∩ matching source/build/dataset policy`. Una identidad ausente o mismatch no entra en la cola, aunque se escriba manualmente en un manifiesto.
- Guard fail-closed **en la vía real de admisión de jobs** (research_lab `_run_one`, única costura de spawn que comparten `run` y `resume --execute`): `qualification_guard.admit_historical` valida el recibo por digest de artefactos, identidad exacta, cadena funcional completa **incluida G2C** (una identidad que nunca completó una operación no promueve, aunque otro recibo diga G4), build+strategy+variant+MM/política y la compatibilidad verificable de las fuentes/calendario/roll. **El corpus trimestral y el corpus histórico tienen digests DISTINTOS por definición**: cada uno se valida contra su manifiesto; comparar procedencia/semántica y, si corresponde, bytes del tramo de contrato coincidente, NO igualdad de hashes de todo el dataset.
- **Anti-falsificación de identidad/fase (2026-10-25):** ni `tier` ni `execution_purpose` declarados por el job deciden nada — el propósito efectivo se deriva del plan sellado (ventana registrada, conjunto de contratos físicos realmente leídos, horizonte económico) y toda contradicción bloquea antes del spawn (`PURPOSE_CONTRADICTS_EXECUTION_IDENTITY`, `TIER_CONTRADICTS_EXECUTION_CLASS`). Un job que se auto-degrada, un histórico etiquetado como trimestre y un estudio multicontrato corto que intenta pasar por quarter caen todos en la misma costura. Las superficies fuera del entrypoint autorizado (llamadas directas al binario del motor, `platform-batch` manual) NO están protegidas por el guard de Python: el guard cubre la vía de admisión autorizada y esa frontera se declara explícitamente, jamás se promete cobertura total.
- Una corrección de reporting puro regenera derivados sin motor. Cambio de lógica de señal, MM, Provider que altere decisiones/fills, fuente, warmup/roll o símbolos invalida recibos dependientes y exige repetir G1–G4 antes de G5. Recibos de ciclos previos se reutilizan como evidencia mientras su identidad y versiones sigan válidas; el guard compara digests y rechaza mezclas.
- Usar corpus histórico físicamente sellado, con rollovers y causalidad; respetar exclusiones, cierres diarios, comisiones y políticas. No mezclar resultados pre/postfix. Conservar todos los intentos y sus hashes.
- Métricas de salida: por identidad y por familia, compras, pases, Wilson95, pérdidas/pendientes, gasto separado, costo/pase, mediana días hasta pase; entradas/día, cobertura de días, máxima sequía, net expectancy/payoff/DD, histogramas temporales, solapamiento de señales y dependencia de perfiles MM. Excluir duplicados de señal del conteo de familias.
- Resultado histórico para ranking **retrospectivo**: el trimestre de promoción ya influyó en qué candidato se probó. Marcarlo como dato de desarrollo, no OOS virgen. Validación independiente requiere datos posteriores realmente no usados.

## 8. Política de recursos: Hefesto

- Host dedicado con memoria física reportada ~14 GiB y swap ~12 GiB; medir recursos reales en cada sesión, nunca asumir valores memorizados.
- Única cola/supervisor existente, techo GLOBAL `max_engines=6` incluyendo diagnósticos/oráculos. Objetivo 5–6 cuando sea seguro. Verificar `/proc` por PID + job/attempt para impedir dos supervisores simultáneos.
- Admisión estimando `RSS` de la clase de job y memoria disponible con margen, PSI `/proc/pressure/memory`, crecimiento de swap y uso del host. Swap es amortiguador, NO capacidad nominal de RAM.
- Ninguna tanda de seis obligatoria si provoca OOM/alta presión sostenida; el gate frena nuevas admisiones, drena, recupera y vuelve a aumentar. Sin deadlocks, orphan, duplicados, backfill de jobs no cualificados.
- Poner juntos smoke/fixtures no justifica 6 motores: paralelizar sólo la matriz trimestral/histórica ya gateada.
- Guardar `resource-receipt`: max simultáneos, duración, RSS p95/pico, MemAvailable mínima, PSI, swap pico/tendencia, OOM, sesiones completadas y consumo por stage. Si G1/G2 descubre fallo, computación histórica desperdiciada debe ser literalmente cero.

## 9. Máquina de estados / contratos de recibo

Estados disjuntos por identidad, por gate:

```text
DECLARED → IMPLEMENTED → CORRECTNESS_PASS → SMOKE_PASS
→ ROLLOVER_PASS → QUARTER_PASS → HIST_ELIGIBLE → HIST_COMPLETE
                           ↘ QUARTER_NO_PASS  (NO HIST)
Cualquier gate → FAILED_CORRECTNESS | DATA_REQUIRED | BLOCKED_ENGINE
                | LOW_FREQUENCY | INCONCLUSIVE | INTERRUPTED_BY_OWNER
```

Un `LOW_FREQUENCY` con G1 y readiness probado **puede ejecutar el trimestre completo**, pero no G5 sin pase. `FAILED_CORRECTNESS` jamás cuenta como fracaso económico.

Recibos mínimos sugeridos, usando esquema local equivalente cuando ya exista uno:

```json
{
  "schema": "echo.strategy-qualification.v1",
  "run_id": "EXAMPLE-ONLY",
  "identity": {
    "strategy_id": "CLF-STR-002",
    "variant_id": "CLF-VAR-S2-T1",
    "profile_id": "SG-R500",
    "family_id": "CLF-FAM-001"
  },
  "binding": {
    "source_sha": "<source SHA>",
    "strategy_config_sha256": "<config SHA256>",
    "binary_sha256": "<binary SHA256>",
    "qualification_dataset_sha256": "<quarter dataset SHA256>",
    "calendar_sha256": "<calendar SHA256>",
    "contract_id": "<verified physical NQ contract>",
    "market_sessions_eligible": 60,
    "warmup_budget_ref": "<requirements/lookbacks digest>"
  },
  "gates": {
    "G0": {"status": "PASS", "receipt_sha256": "<digest>"},
    "G1": {"status": "PASS", "receipt_sha256": "<digest>"},
    "G2A": {"status": "PASS", "evaluations": 1000, "ready": 800, "signals": 12, "receipt_sha256": "<digest>"},
    "G2B": {"status": "PASS", "verdict": "SESSION_COMPATIBLE", "signals": 12, "in_window": 4, "receipt_sha256": "<digest>"},
    "G2C": {"status": "PASS", "entry_fills": 4, "exit_fills": 4, "reconciled_roundtrips": 4,
            "open_at_horizon": 0, "wins": 1, "losses": 3, "receipt_sha256": "<digest>"},
    "G3": {"status": "PASS", "first_ready_after_roll": "<timestamp>", "receipt_sha256": "<digest>"},
    "G4": {
      "status": "PASS",
      "purchased": 4,
      "passed": 1,
      "lost": 2,
      "pending": 1,
      "trades": 90,
      "days_with_entry": 35,
      "reconciled": true,
      "receipt_sha256": "<digest>"
    }
  },
  "promotion": "HIST_ELIGIBLE"
}
```

Todos los números del ejemplo son **ficticios**. El archivo real debe provenir de eventos/recibos verificables, jamás de copiar el ejemplo. `receipt_sha256` = SHA real de archivo inmutable, no autorrefrencial. Distinguir `FAILED` por defecto del motor de `QUARTER_NO_PASS` comercial.

### Guard en scheduler/adaptador (pseudocódigo, NO CLI existente)

```text
admit_quarter(job, receipts, plan):                      # CLF-Q03-R1
  r = receipts.exact_identity(job.strategy, job.variant, job.mm)
  assert r.G0..G3.pass && r.G2A.pass && r.G2B.verdict == SESSION_COMPATIBLE
  assert r.G2C.entry_fills >= 1 && r.G2C.exit_fills >= 1 && r.G2C.reconciled_roundtrips >= 1
  assert !r.carries_G4                                  # no bit-identical re-runs
  assert job.execution_purpose == effective_purpose(plan) == QUARTER
  assert job.contract_set == plan.physical_contracts    # bounded source-read rows
  assert job.window_identity == plan.{warmup,trade,end}
  assert job.plan_digest == plan_identity_digest(plan)  # plan minus qualification
  assert exact_match(r.source, r.strategy_config, r.binary, r.mm_profile,
                     r.calendar, job.declarations, engine_binary)
  else -> BLOCKED_QUALIFICATION_GATE with exact code and no engine spawn

admit_historical(job, receipts, engine):                 # todo lo anterior + G4
  assert r.G4.pass && r.G4.passed >= 1 && r.G4.reconciled
  assert r.G4.market_sessions_eligible >= 45
  assert quarter_dataset_digest == r.binding.quarter_dataset (sealed separately)
  assert historical_dataset_digest != quarter_dataset_digest
  assert lineage(symbol, bar_semantics, calendar_family) compatible
  else -> BLOCKED_QUALIFICATION_GATE with exact code and no engine spawn
```

El agente debe **adaptar** este contrato a las herramientas reales que encuentre; no copiar el pseudocódigo como Python funcional ni inventar flags. Cuando un mismo motor haya evolucionado entre quarter e histórico, demostrar compatibilidad semántica del cambio; de otro modo repetir qualification con el nuevo build. Las superficies invocables por fuera del entrypoint autorizado (binario directo) no están cubiertas por el guard: la frontera se declara, no se promete en falso.

## 10. Diagnóstico y recuperación (tabla de decisiones)

| Síntoma | Causa posible y evidencia mínima | Acción |
|---|---|---|
| `evaluations=0` | Requirements/serving ausente, falta de barras, trigger equivocado | Ver primeras barras, ventana y `BarClose`; FIX G1/G2 |
| `evaluations>0`, `ready=0` tras lookback | Warmup perpetuo, reset por roll, prefix HTF inválido | G1/G3 FAIL; no DEV/histórico |
| `ready>0`, `signals=0` | Setup raro o predicado/horario defectuoso | Fixture positivo + valores causales; si raro, G4 una vez |
| Señales pero 0 fills | MM no admite mínimo, cap, estrategia sin cuenta, Provider reject | Contar por etapa; si bug FIX, si rechazo válido reportar |
| Fills pero 0 compras | Censo/identidad o compra/selección fuera de ventana | Reconciliar compras contra cash ledger/accounts |
| Compra pero 0 pases | No cumplió RuleSet/objetivo o horizonte insuficiente | G4 NO_PASS; no G5 |
| Rollover rompe ready | NQ físico cambia y nuevo warmup nunca alcanza lookback | G3 FAIL + test cross-roll + reparar estado/plan |
| NQZ6 sólo 10 sesiones | Fuente trimestre incompleta | Buscar trimestre físico anterior verificable; si no hay DATA_REQUIRED |
| Engine error `DRAIN_NOT_CONVERGENT` | Conflicto Provider/MM/Operation | RCA/test focalizado, no backtest de años |
| Error `PROTECTED_CLOSE_ORDER_MISMATCH` | Stop ya finalizado vs conversión protegida | Reutilizar regresión R03; nunca desactivar check |
| OOM/PSI alta/swap creciendo | Más RSS que margen físico | Pausar admisión, reducir concurrencia, preservar intentos |
| Repetición misma causa ×2 | Fallo sistémico no reparado | Breaker, suspender sólo frente afectado; no loops de retries |

Para cada fallo emitir `first_divergence_stage`, primer timestamp físico, log/trace/evento, causa, propietario, fix+prueba antes/después y `affected_identity_set`. No reiniciar desde cero toda la historia por defecto.

### Casos de "no opera" (obligatorios, de barato a caro; CLF-Q03-R1)

Ninguna variante termina como `0 trades`/`NO_ACTIVITY`/`COMPLETE`/`UNKNOWN`/`LOW_FREQUENCY` sin diagnóstico causal y clasificación persistente:

| Caso | Síntoma | Inspección (orden barato→caro) | Clasificación |
|---|---|---|---|
| A | Nunca alcanza ready | composición TF, Requirements, warmup, resets, datos | `TECHNICAL_DEFECT` (fix + repetir gates) |
| B | Ready, cero oportunidades | cada predicado del setup contra el contrato; catálogo y claims | `VALID_RARE_NO_ACTIVITY` o defecto de construcción |
| C | Oportunidades, cero señales | lógica de decisión e invalidaciones vs knowledge | fix de código o `SOURCE_REVIEW_REQUIRED` |
| D | Señales fuera de horario | Strategy vs AccountPolicy, intersección posible | `SESSION_INCOMPATIBLE` (fiel al curso; adaptación = identidad nueva autorizada) |
| E | Señales sin fills | cuenta, MM, min lot, stops, Provider, rechazos | `SIGNAL_REJECTED_VALID_POLICY` vs `SIGNAL_EXECUTION_DEFECT` |
| F | Entradas sin operación completa | fills, cierre, órdenes protectoras, lifecycle, reconciliación | no funcional hasta demostrar cierre real |
| G | Roundtrips, todos perdedores | entrada, stop/target, dirección, filtros, costos, sesión vs patrón fuente | `FULLY_TRADED_NEGATIVE_SAMPLE`; evidencia negativa conservada, sin cambiar la estrategia para conseguir un ganador |
| H | Operaciones completas, cero challenges | resultado G4 conciliado | `QUARTER_NO_PASS`; sin histórico |

### Knowledge Review Loop (reutilizable para cualquier curso)

Cuando una variante no opera o su lógica no puede validarse, emitir UNA ficha por problema material en `CLF-<CICLO>-KNOWLEDGE-REVIEW-QUEUE.md` (formato completo en la skill §8 y en el mandato): `REVIEW_ID`, identidad, `CURRENT_STATUS` (`NEEDS_ITERATION | SOURCE_REVIEW_REQUIRED | VALID_RARE_NO_ACTIVITY | SESSION_INCOMPATIBLE | BLOCKED_SPEC | BLOCKED_DATA`), `SOURCE` (curso, capítulo, claim_ids, frame_ids, timestamp de video, path del knowledge), `EXPECTED_BEHAVIOR` vs `IMPLEMENTED_BEHAVIOR`, `OBSERVED_LAST_CONTRACT` (funnel numérico), `FIRST_CAUSAL_DIVERGENCE`, `ROOT_CAUSE` (`CONFIRMED | HYPOTHESIS | UNKNOWN`), `KNOWLEDGE_QUESTION` concreta para el Owner, `VIDEO_REVIEW_TARGET` (capítulo y minuto; `NOT_RESOLVED` si no es recuperable — jamás inventado), `RECOMMENDED_ACTION` (`FIX_CODE | REVIEW_VIDEO | CLARIFY_SPEC | KEEP_RARE | ADAPT_MARKET | BLOCKED_DATA`) y `RETEST_SCOPE` (gates afectados, jamás todo el histórico por defecto). No volver a analizar el curso entero: la ficha apunta exactamente a la parte de conocimiento en duda.

## 11. Verificación anti-regresión de la propia metodología

Antes de declarar que el runner aplica la skill, ejecutar **pruebas negativas de admisión**, sin computación cara. Matriz CLF-Q03-R1 (cada rechazo demuestra **cero motores lanzados**, sentinel del stub + recibo `QUALIFICATION-BLOCKED.json` con causa exacta):

1. Estrategia que sólo compila: job QUARTER sin cadena de cualificación ⇒ `RECEIPT_MISSING`.
2. `ready=true` pero cero señales, o señales sin órdenes, u órdenes sin fills, o entrada sin cierre conciliado: G2C con `entry_fills/exit_fills/reconciled_roundtrips` incompletos ⇒ `G2C_NOT_FULL_TRADE`.
3. Sesión incompatible: G2B con veredicto `SESSION_INCOMPATIBLE` ⇒ `G2B_NOT_SESSION_COMPATIBLE`.
4. G2C de otra variante: identidad del recibo ≠ identidad declarada ⇒ `IDENTITY_MISMATCH`.
5. G2C con artefacto alterado: digest del artefacto ≠ bytes ⇒ `RECEIPT_ARTIFACT_TAMPERED`.
6. G4 sin G2C PASS / cadena incompleta ⇒ `GATE_G2C_NOT_PASS`/`GATE_<X>_NOT_PASS`.
7. G5 sin G4 PASS ⇒ `GATE_G4_NOT_PASS`; G5 con cero challenges ⇒ `G4_NO_PASS`; G4 no conciliado ⇒ `G4_UNRECONCILED`; <45 sesiones ⇒ `SESSIONS_BELOW_MINIMUM`.
8. Histórico mal etiquetado como trimestre ⇒ `PURPOSE_CONTRADICTS_EXECUTION_IDENTITY` (el propósito efectivo lo decide el plan).
9. Horizonte multicontrato corto intentando evadir clasificación ⇒ clasificado `HISTORICAL` por conjunto de contratos ⇒ exige cadena G5 ⇒ `RECEIPT_MISSING` sin recibos.
10. `resume --execute` sin recibos (histórico y quarter) ⇒ bloqueado en la misma costura.
11. Identidad duplicada que intenta heredar un PASS ⇒ `IDENTITY_MISMATCH`; plan re-preparado con otro digest ⇒ `PLAN_DIGEST_MISMATCH`; contratos declarados ≠ contratos leídos ⇒ `CONTRACT_SET_MISMATCH`.
12. Recibo que ya trae G4 (campaña bit-idéntica) ante la puerta quarter ⇒ `RECEIPT_NOT_A_QUALIFICATION_CHAIN`.
13. Positivos: quarter con cadena completa e identidad sellada ⇒ admitido una vez; G5 con G4 PASS + digests compatibles ⇒ admitido; alias demostrado exacto ⇒ no se ejecuta dos veces.

E2E real sobre el runner (sin stub): job quarter sin cualificación ⇒ `RECEIPT_MISSING`, exit 78, 0 motores; job histórico sin recibo ⇒ ídem.

Validación documental skill: caso positivo = nuevo STR-002 ClutiFX; caso negativo = consultar rankings de R03 (no lanzar motores); caso adyacente = deploy Echo PROD (derivar a `echo-prod-deploy`, sin carga aquí).

## 12. Publicación, salida y cierre

Entregar bajo el proyecto/run root existente sin crear un segundo planner:

- `QUALIFICATION-LEDGER.csv` con 1 fila por identidad y G0–G5 (incluidos G2A/G2B/G2C), reconciliada con la matriz (1 fila por ID, sin omisiones).
- `CONTRACT-DATA-RECEIPT.md` (elección física del trimestre y del último contrato, sesiones y falta de datos).
- `G1-CORRECTNESS.md`, `G2-LASTCONTRACT-ALL-VARIANTS.csv` (funnel por identidad), `G2-FULL-TRADE-EVIDENCE.md` (round-trips conciliados con identidad preservada), `G3-ROLL-RECOVERY.md`.
- `G4-QUARTER-ECONOMICS.csv` (pases y rechazos separados).
- `G5-HIST-ELIGIBLE-MANIFEST.json` (sólo promocionadas, digests verificados).
- `KNOWLEDGE-REVIEW-QUEUE.md` (fichas del loop; una por problema material no resuelto).
- `ZERO-TRADE-RCA.md` y `SESSION-COMPATIBILITY.md` (diagnóstico causal y veredictos G2B por identidad).
- `COMPUTE-BUDGET-RECEIPT.md` (wall/CPU/RAM/swap por gate y número de históricos evitados).
- `DECISION-STRATEGIES.md` (familias distintas, frecuencia, economía, incertidumbre) sólo cuando exista evidencia completa.
- `REPRODUCE.md` con comandos exactos capturados del tooling real y fuente/build/corpus; `STATUS.md` inequívoco.

Datos y trazas pesadas permanecen fuera de Git en run root, con checksums; docs compactos y código en la rama autorizada, sin merge ni LIVE. Planner/agent-run/change_log y feedback de fricción real. Ejecutar `agents-os-session-close` sólo cuando se pidió cierre; no simular async sin supervisor/automation reales.

### Veredicto final obligatorio

```text
IDENTITIES: declared=__, data_blocked=__, G1_pass=__, G2_pass=__,
            G3_pass=__, G4_pass=__, G4_no_pass=__, G5_hist_started=__
CONTRACT: <NQ symbol> <trade_start>..<end_exclusive> <sessions>=45?
ROLLOVER: <window> ready recovered? earliest-ready after roll
COMPUTE_SAVED: <failed early> identities x historical jobs avoided (medido/no inventar tiempo)
HISTORICAL_AUTHORITY: <exact ID list; 0 if no passed quarter>
SPAWN_GUARD: PASS / FAIL with negative tests
RESOURCE: GLOBAL engines(max), MemAvailable(min), PSI, swap(max), OOM
OWNER_ACCEPTANCE: REVIEW
AGENTS_OS: <planner/run/feedback/close>
```

## Rollback / recuperación

- Abort a los primeros gates incorrectos; preservar `candidate-ledger`, binario/planes/intentos como evidencia.
- Si falla el guard nuevo, deshabilitar **sólo el despacho histórico** hasta arreglarlo; nunca deshabilitar tests/Provider para sortearlo.
- Si existe implementación local previa de `echo-retester-master` u otro runbook con el mismo propósito, reconciliar por delta con esta autoridad publicada; no mantener dos políticas contradictorias ni pisar trabajo local no sincronizado.
- Si un campo, dato o contrato no puede verificarse, terminar `INCONCLUSIVE/DATA_REQUIRED` con prueba exacta del faltante, no publicar `READY` falso.
