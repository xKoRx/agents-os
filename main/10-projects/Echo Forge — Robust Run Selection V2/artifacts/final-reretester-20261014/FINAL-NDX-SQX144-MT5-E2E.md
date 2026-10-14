# FINAL-NDX-SQX144-MT5-E2E — Ejecución física del funnel Final Reretester + MT5 Fidelity

**STATUS: RUN_ACTIVE_RECOVERABLE** (2026-10-14, sesión one-shot ~10.5h)

## Resultado ejecutivo

La infraestructura Echo Forge quedó **operacional end-to-end en SQX 144 + MT5 Kronos Windows**: las 21 estrategias Robust V2 de wave2b se re-consumen cross-FlowRun de forma durable, aplican (magic durable asignado), se reretestean con el CFX del Owner sobre 109.2M ticks reales NDX en SQX 144 (3/3 hosts), se exportan a TradeSet + MQ5, se compilan a EX5 en el worker Windows (21/21) y el primer backtest real-tick NDX_SQX ejecutó en los slots V2 llegando hasta el stage de **fidelity scoring**, que falla por un único defecto de canonicalización de instrumento en el TradeSet baseline (diagnóstico exacto + fix debajo). Seis releases canónicas (0.2.132→0.2.137) fueron cortadas y certificadas en flota 3/3 durante la sesión.

## Flujo durable ejecutado (último intento completo: wave3n + wave3o; wave3p con el fix de duración)

| Etapa | Resultado físico |
|---|---|
| robust continuation (cohort wave2b) | 21 carriers (StrategyRef + wfm_aggregate evidence + key .sqx optimizer) — PASS |
| select_robust_run | 21/21 SELECTED re-derivadas deterministamente (V2 0.35/0.01/0.01) — PASS |
| apply_selected_run | 21/21 aplicadas con magic durable V1 (instrumento NDX, código 9) — PASS |
| final_reretester (CFX Owner, SQX 144) | 21/21 retests tick completos, periodo 2025.07.01→2026.10.09 — PASS |
| trade_list_exporter (tick_retest/optimized) | 21/21 TradeSets durables — PASS |
| mt5_exporter (MQ5) | 21/21 MQ5 durables — PASS |
| mt5_compiler (Windows, slots V2) | 21/21 EX5 (MetaEditor build 6182, slots reales) — PASS |
| mt5_backtesting (real ticks NDX_SQX) | Ejecuta en slots; primera estrategia llegó a reconcile+fidelity — PASS parcial |
| mt5_score_shadow_v1 (fidelity) | FAIL: scope mismatch por instrumento crudo en TradeSet (ver §defecto) |

## Último defecto abierto (caracterizado con evidencia)

`mt5_score_shadow_v1: decode durable TradeSet: normalized trade scope mismatch`

El TradeSet baseline (EchoForgeTradeListExporter) emite `instrument = NDXm_darwinex_tick_UTC02` (símbolo SQX crudo), pero el contrato de comparabilidad de fidelity exige instrumento canónico (`ndx`) en scope Y trades (`CanonicalSymbol(raw)==raw` fail-closed). Tres fixes previos ya aplicados en esta misma frontera: duration_seconds ±1s (derivación por-lado vs total — `458c17e`), scope canalizado, inválidos.

**Siguiente fix exacto (owner-decision entre dos opciones contractuales):**
1. Java: `TradeExtractionService` emitir el instrumento canónico de la campaña (mapeo chart→concepto) — requiere catálogo en Java; o
2. Go: `mt5_score_shadow_activity.go` aceptar scope cuyo `CanonicalSymbol(scope.Instrument)` sea idéntico al del trade (comparar en dominio canónico, no crudo) + alias `ndxm_darwinex_tick_utc02 → ndx` en `canonical_scope.go` (patrón idéntico al alias `ndx_sqx` ya fusionado).

Tras el fix: `deploy_release.sh --release-only 0.2.138` → re-despachar wave (nueva identidad, flow JSON en artifacts) → funnel ~55 min → fidelity + ranking TOP 5.

## Infraestructura dejada READY (evidencia física 2026-10-14)

- **SQX 144 Zeus/Hera/Kronos 3/3**: sqcli 144.2953 operativo (licencias EA6F8A 6/6 del 13-oct preservadas), 142 intacto 3/3, datos NDX idénticos 3/3 (`f70a2f43…5572`, 2.577 GB, NDXm_darwinex_tick_UTC02), proyectos EchoForge 21 en 144 3/3, plugins EchoForge fuentes desplegados en `user/extend/Snippets/SQ` 3/3 (regeneración de Snippets.jar en boot verificada por canary: clase RobustRunExporter carga y produce output).
- **CFX Owner**: `RetestFull.cfx` Kronos Windows `C:\Users\KoR\Desktop\SQX144\user\configs\` (SHA256 `2e0c19cc…fec80`, 6383 B, editado por el owner 2026-10-14 01:35), adaptado a Linux sólo en `templateFile` (UNC→`/home/kor/sqx/user/configs/RetestFullBase.cfx`, bytes base idénticos Owner=flota `d824eb58…`) → `reretesterfull.cfx` SHA `a51c1cc3…bafb3`. Periodo efectivo CFX: 2025.07.01→2026.10.09, tick precision, H1, spread 1, comisión 5.5, swap Darwinex, engine MT5 (hedged).
- **MT5 Kronos Windows**: SlotAllocator V2 activado (`mt5/slots_root=C:\MT5\slots`, `mt5/slot_count=4`), slots 1–4 portables con terminal 6182 certificado + NDX_SQX completo (symbols.custom.dat + hcc 2023–2026 + tkc 202306–202610). Slot-1 smoke PASS: 99.587.652 ticks reales 2025.07.01→2026.10.08, test passed 24.8s. Instalación principal C:\MT5\test PRESERVADA. Worker 0.2.107 (contratos compile/backtest sin cambios desde entonces — diff verificado).
- **Fleet releases**: master `458c17e` con 6 commits de sesión; releases 0.2.133–0.2.137 cortadas y verificadas 3/3 por SHA+proceso (Prometheus no necesario).

## Fixes de producto (commits canónicos, pusheados)

| Commit | Fix | Evidencia que lo originó |
|---|---|---|
| `a801a3e` (0.2.133) | alias `ndx_sqx→ndx` en CanonicalSymbol + tests comparability | mandato §9 (fidelity fail-closed total) |
| `ca8b013` (0.2.134) | robust continuation cross-FlowRun (cohort por decisiones wfm_aggregate + artifacts optimizer) | gap contractual: continuaba desde wave2b sin re-optimizar |
| `c24c4fb` (0.2.135) | decisions = autoridad del cohort (skip artifacts sin decisión — wave2b: 34 artifacts / 21 decisiones) | wave3h |
| `3612daf` (0.2.136) | apply acepta evidencia inmutable del FlowRun productor | wave3i (aggregate evidence mismatch) |
| `21145b0` (0.2.137) | digest excluye config_folder/path_strategy (transporte) | wave3m (mt5_compile_persist CONTRACT_CONFLICT) |
| `9b06fb7`+`458c17e` (plugin Java) | duration_seconds derivado de los instantes serializados (Duration.between) | wave3n/o (17/34 trades ±1s) |
| infra ETCD | `sqx.magic_instruments` INSERT NDX=9 | wave3j (instrument_code_missing) |

## Intentos de wave (identidades quemadas, FAILED_ATTEMPT_KEEP)

wave3f (dispatch en sqx-dev-queue por ENV perdido en restart — workflow cancelado), wave3g (source_folder 04_wfm sin artifacts SQX), wave3h (join 34↔21 demasiado estricto), wave3i (magic NDX ausente + apply same-flow), wave3j (Snippets.jar 144 sin clases EchoForge), wave3k/l (idem + permisos custom Zeus), wave3m (digest transporte), wave3n (duration_seconds), wave3o (fix por-lado insuficiente), **wave3p** (scope instrumento crudo — defecto abierto documentado arriba).

## Comando de consulta del run

```bash
cd /home/kor/aranea/work/final-reretester-20261014
./forgeops-bin -app sqx-watcher -env production -op wfstat -wf <workflow_id>
./forgeops-bin -app sqx-worker -env production -op sql -q "SELECT stage_key, count(*) FROM sqx.stage_executions WHERE flow_run_id='<flow_run_ref>' GROUP BY stage_key"
```

Logs: `/var/log/symphony/symphony-worker.log` (grep por workflow_id). Watcher screens `forge-watcher-wave3p` en Daedalus (`/home/kor/aranea/work/final-reretester-20261014/watcher/`).
