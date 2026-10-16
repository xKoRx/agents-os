# E2E-EXECUTION-REPORT — FLOW_EXAMPLE_2 (SQX 144 · NDX · 2026-10-16)

## Veredicto

**FLOW_EXAMPLE_2_E2E_BLOCKED** — el flujo completo no cabía en el presupuesto del mandato y fue detenido por parada controlada en la línea T+40 del protocolo §6, con evidencia durable preservada en el punto exacto. Etapas 1–6 **PASS** físicas reales; etapa 7–8 **PARTIAL** (18/30 optimizer, 15/30 WFM/robust); etapas 9–17 **NOT_EXECUTED**; etapa 18 (STOP PRE-ECHO) **RESPECTED** (cero integraciones Echo).

- Causa raíz del bloqueo: el CFX del Owner `builder_test.cfx` produce una cohorte grande (777 estrategias aceptadas en 20m24s con `passed-count 1000` / `MaxStrategies 1000`) y la cadena downstream (retest + optimizer×30 + MT5×30) no completa en 40 min. Parámetro exacto: `<StopCondition type="passed-count" passedStrategies="1000" restartCount="5" .../>` + `<MaxStrategies>1000</MaxStrategies>` (builder_test.cfx líneas 250/122). NO se modificó el CFX (mandato §1/§7).
- T0 del intento limpio: 2026-10-16T21:12:24Z (pickup de flota de Run A). Línea T+40: 21:52:24Z. Cancelación ejecutada: 21:52:34Z (mecanismo canónico CancelWorkflow; FlowRun CANCELLED durable en 21:53:2xZ).
- Nota de reloj: los primeros dos despachos (21:00:50Z y 21:08:28Z) fallaron por error operacional del operador (ENV del watcher, ver "Fallos registrados") y NO consumieron flota ni ejecutaron task alguna; se termina y documenta como FAILED_ATTEMPT_KEEP. Si el Owner computa T0 desde el primer despacho, la línea era 21:40:50Z — la parada se habría aplicado 12 min antes; el punto de corte informado habría sido el mismo punto de evidencia o anterior.

## Ejecuciones equivocadas (§3) — estado

- Campaña errónea `569c152c-322d-404a-92c1-0ee3ae1d8afc`: ya CANCELLED durable desde 15:24:46Z (sesión anterior; workflow real `sqx-forge-campaign-v1-2fab2660-…`, razón PARENT_CANCELLED). Verificado hoy: sin FlowRuns RUNNING de ese intento (todas las filas del día terminal, última 18:51Z CANCELLED = Flow B wave 7).
- FlowRuns equivocados Flow B: terminal (CANCELLED/FAILED), verificados en `sqx.flow_runs` antes de despachar.
- Flota al inicio: 3/3 workers `0.2.146` (Zeus 15:05, Kronos 15:06, Hera 16:36 — Hera REINCORPORADA hoy), 0 procesos sqcli/java, sin screens forge-watcher previos.
- Residuos propios documentados (FAILED_ATTEMPT_KEEP): FlowRuns `fc5f798c` (w1) y `bda2300e` (w2) en PG status RUNNING sin worker que selle (namespaces sqx-dev sin pollers), workflows TERMINATED server-side en sqx-dev (`sqx-main-v1-a0ab67f9…`, `sqx-main-v1-36841973…`); configs `NDX_flow_example_2_v1_w1/_w2` quemados; artefactos MinIO subidos por el watcher en scope development. El workflow ajeno `sqx-main-v1-ab32f685…` (14-oct, sqx-dev) NO fue tocado.

## Identidad y specs (§2, §4)

- Flujo: `flow_example_2` — NDX, L, H1, v1, sqx_version 144, fuente física `USATECHIDXUSD_dukascopy_UTC02` (declarada por los 4 CFX), MT5 `NDX_SQX`.
- Estructura física: **DOS FlowRuns canónicos** (skill `forge-wave-dispatch` §4b) porque el flujo único choca el defecto demostrado `resetBatchKeepBindings` vs `source ranking_snapshot` (wave 6, 2026-10-16) y §7 prohíbe modificar source de producto:
  - **Run A** (wave 3, `NDX_flow_example_2_v1_w3`, FlowRun `0f28eea9-4f2d-4874-ad99-25677eae92c8`, wf `sqx-main-v1-f15e2d0f-1564-45cd-8df4-c9391daa09d7`): builder → overview (durable V1) → classification → early ranking → selection.
  - **Run B** (wave 4, `NDX_flow_example_2_v1_w4`, FlowRun `e2d29ff8-30f7-470d-b036-ef2bf5580204`, wf `sqx-main-v1-5ad47c97-1df0-4225-b098-de850f5791b5`): `selection_cohort: sha256:f7dd10aa…` → group retester (batch 10, max_parallel 3) → group optimizer (batch 1, max_parallel 3) + evaluate_wfm + select_robust_run → apply → final reretester → tradelist → report → MQ5 → EX5 → MT5 → fidelity → ranking → promotion.
- Magic apply: **888111** (configurado; NOT_EXECUTED por la parada). Top por tipo: **5**. Ranking final: score_descending.v1 top_n 100 (ranking completo, sin proyección global de 5). Promotion configurada: finalist_promotion **2.0.0** (aceptada por runtime; la usada por el spec certificado de campaña del mismo día).
- Validación: `runtime.ValidateWorkflowSpec` SPEC_VALID en ambos specs; spec serializado por el watcher inspeccionado en `sqx.configs.config_json` = idéntico al JSON (sin pérdida de campos).
- RequestID/Wave nuevos: `flow-example-2-20261016T212000Z-run-a-w3`, `flow-example-2-20261016T214100Z-run-b-w4` (los request_id de w1/w2 quedaron quemados con sus configs).

## Matriz de tareas

Ver `TASKS-RESULTS.csv` (stage, estado, host, duración, input/output, evidencia).

## Resultados del funnel (evidencia durable real)

- **Builder real**: 777 estrategias aceptadas (20m24s, Zeus, sqcli 144 `/home/kor/sqx/144/sqcli -project action=start name=custom`). El wiring `output` del CFX del Owner es correcto (el defecto de wiring `Results` de la mañana NO está presente en estos CFX).
- **Clasificación durable**: `indicator_signature.v1` → snapshot `sha256:f2326c4d793e96c2668563bc0423cc06f979c38bd8e5c921f5eea4a63c1ded72`, 777 entradas, **7 tipos lógicos**: RANGE_CLOSE,LOW_RANGE=350 · RANGE_CLOSE,OPEN_RANGE=203 · RANGE_CLOSE_RANGE=144 · RANGE_CLOSE,HIGH,LOW_RANGE=51 · RANGE_CLOSE,HIGH_RANGE=24 · RANGE_CLOSE,LOW,OPEN_RANGE=3 · RANGE_CLOSE,HIGH,LOW,OPEN_RANGE=2.
- **Early ranking** `weighted_combination_minmax.v1` (drawdown 40 COST / profit_factor 30 BENEFIT / sharpe_ratio 30 BENEFIT — ponderaciones vigentes preservadas), PER_LOGICAL_TYPE top_n 5 → **7 ranking snapshots** (uno por partición, con metric_components normalizados por entrada).
- **Selection** `per_logical_type` top_n 5 → **SelectionSnapshot sellado `sha256:f7dd10aaa006762e775f61fcfc053ee8818c958c9f95836ffa01ce7f76d16a33` con 30 estrategias** (5+5+5+5+5+3+2; los tipos con menos de 5 candidatas aportan todas). StrategyRefs exactas y lineage en `FINALISTS-BY-TYPE.csv`.
- **Grouping/routing**: Run B sembró la cohort vía `selection_cohort` (source canónico vigente, sin re-import) y fan-out **3 children** de retester (batch 10) procesados en la flota: **30/30 COMPLETED, 0 FAILED, 0 rechazos espurios**.
- **Optimizer real** (CFX del Owner intacto: genetic type 3, maxOptimizations 3000, WF period 10/15, automatic maxSteps 5): **18/30 COMPLETED** al corte (ritmo observado ~1.6 runs/min con 3 hosts). **WFM/Robust V2**: 15 evaluate_wfm COMPLETED + 15 select_robust_run COMPLETED (`robust_run_selection_v2` cliff 0.35 / eps 0.01/0.01, parámetros aceptados del proyecto). 12 estrategias quedaron sin optimizer/WFM (NOT_EXECUTED).
- **Parada controlada**: CancelWorkflow 21:52:34Z → FlowRun CANCELLED durable 21:53:2xZ. Completados en vuelo antes del corte se preservaron; `apply_selected_run` y posteriores NO arrancaron. Un stage row `evaluate_wfm` quedó RUNNING no-terminal por la cancelación (fila de bookkeeping; workflow CANCELLED — documentado, sin leak de flota observable por la vía durable).
- **Etapa 17**: la selección final por tipo con ScoreEvidence/Fidelity NO existe (etapas 10–15 NOT_EXECUTED). Entregado `FINALISTS-BY-TYPE.csv` como **PROJECTION_ONLY** exacto desde el SelectionSnapshot durable (30 refs por tipo con rank y builder_ranking_value), sin inventar decisiones. Fórmula Fidelity no modificada (nunca llegó a ejecutarse).

## Presupuesto (§6)

- Objetivo 20–30 min: **incumplido por física del CFX** (builder solo 20m24s). Checkpoint T+30: investigación = flujo avanzando, etapa dominante builder (20m24s de 20m28s de Run A). Línea T+40: parada controlada aplicada (21:52:34Z), punto alcanzado registrado, evidencia conservada, sin re-despachos automáticos.
- Estimación para completar la cadena (para decisión del Owner): desde el corte restan ~12 optimizer + ~12 WFM/robust (~8–10 min a ritmo observado), apply (segundos), final reretester full-precision 30 estrategias (no medido; etapa pesada), MT5 30 backtests en concurrencia serial por host (~15–40 min) + exporters. Orden de magnitud: **30–60 min adicionales** sobre el corte.

## Fallos registrados del operador (§10)

1. **ENV del watcher**: lancé el watcher sin el prefijo `ENV=production` de la línea canónica de la skill → cargó scope development (`temporal.namespace sqx-dev`, sin workers) y despachó w1 a un namespace muerto. Identidad `w1` quemada. El cancel canónico no alcanza a un workflow sin workers (el cancel viaja como workflow task) → TERMINATE server-side.
2. **Carrera al matar el watcher**: `screen -X quit` no mató el pipeline hijo de inmediato; el watcher viejo (dev) sobrevivió lo suficiente para consumir el paquete w2 recién empacado → segunda identidad quemada y segundo huérfano en sqx-dev (terminado igual). Lección: tras matar un watcher, verificar con pgrep que no queda ningún proceso ANTES de re-empacar `input/`; cualquier paquete consumido por un watcher en scope equivocado quema la identidad del wave silenciosamente ("dispatch exitoso" en su log).
3. Los dos huérfanos NO ejecutaron task física alguna (no hubo pollers); costo: 2 identidades + filas PG RUNNING que ningún worker sellará (residuo documentado, mismo patrón que los zombies PENDING de agosto).

## Deuda observabilidad

El MCP aranea-ssh expiró a mitad de sesión (reintento sin éxito) y el MCP temporal quedó bound a un namespace distinto de `sqx-prop` (conocido). El drenaje físico post-cancel no pudo re-verificarse por SSH en caliente; el estado durable (CANCELLED) y el comportamiento certificado del path de cancelación (0 sqcli en la operación idéntica de la sesión anterior) son la evidencia disponible. Prometheus no expuso series por host en la ventana consultada. Verificación recomendada para el próximo operador: `pgrep -af sqcli|java` en los 3 hosts antes del próximo despacho.

## Handoff para completar la certificación (opción Owner)

Re-despachar SOLO Run B con wave nuevo (identidad `NDX_flow_example_2_v1_w<N>` libre) reutilizando el MISMO `selection_cohort sha256:f7dd10aa…` (durable, intacto) y ventana de 60–90 min. No repetir builder ni selección. El spec está en `CONFIG-FLOW-EXAMPLE-2-RUN-B.json` (cambiar wave/request_id).
