# MT5 VERSION-AGNOSTIC — FINAL REMEDIATION (2026-10-15)

**STATUS: MT5_VERSION_AGNOSTIC_FINAL_PASS_WITH_DEPLOY_BLOCKED**

Sesión one-shot ZCode/GLM-5.3-Flash sobre el mandato "ECHO FORGE — MT5
VERSION-AGNOSTIC FINAL REMEDIATION" (manager GPT-6). Base: release 0.2.142 /
`f1d29e0` (allow-list eliminada y smoke 6230 ya ACEPTADOS). Host operacional:
`WORKER-KRONOS`. Sin rediseño, sin allow-list, sin repetir wave3t ni campaña
de 21 estrategias; sin tocar fórmula Fidelity, ranking, Robust V2, datos ni
integración Echo.

## Qué cerró (symphony master `5046650`, sobre release 0.2.142 / `f1d29e0`)

- **GAP 1:** Gate B (`report_smoke.go`) sólo `PASS` con `TradeSet COMPLETE`,
  `trades_closed>0`, trades normalizados válidos, crosschecks del parser en
  verde y build del HTM == instalación ejecutada (`htm_build`). `INVALID` →
  `FAIL` tipado; `EMPTY` → `UNPROVEN` (no certifica).
- **GAP 2:** `EvaluateReportSmokeGate` acepta sólo evidencia explícita y
  vigente: PASS/FAIL/UNPROVEN conocidos, campos obligatorios de PASS,
  identidad contractual parser/normalizer; legacy/divergente → revalidación;
  inconsistente/desconocido → fail cerrado; evidencia anterior conservada
  (`previous_status`/`previous_terminal_sha256`).
- **GAP 3:** smoke sin reporte válido → `UNPROVEN`; los jobs masivos
  siguientes fallan cerrado (`ErrReportSmokeNotCertified`, contract error) sin
  ejecutar física; desbloqueo sólo con canario (`smoke_canary: true` en el
  request de `MT5BacktestArtifactWorkflow`, workflow existente — sin registry
  ni scheduler nuevo). Fallas reintentables repiten como smoke, sin
  certificar a medias.
- **GAP 4:** Gate A con `Symbol=NDX_SQX` verificado **físicamente** en slot-1
  (probe `TestPreflightSlot_PhysicalNDXSQX`, PASS 0.38s): el check `.hcc`
  cubre `bases/Custom/history/NDX_SQX` sin falso rechazo; ticks `.tkc` no
  participan. Sin corrección requerida.
- **Tests 1–9** obligatorios implementados y verdes (`report_smoke_test.go`,
  `preflight_test.go`, T10b end-to-end en `mt5_artifact_activities_test.go`).
  Flake preexistente de `sqx/workflows` demostrado idéntico vs baseline.

## Release y despliegue

- Release **0.2.143** publicada en MinIO: windows `sqx-mt5-worker.exe`
  SHA256 `50f61b638a043af566bb4bc3764bbeb293eb08f64d480bb25954b345478b7fe3`
  (37 519 872 B), manifest `e05e1cb4…` (21:44:44Z). Commits: `3dbc33e` fix,
  `9702e8c` manifest, `5046650` docs.
- **Despliegue a worker-kronos BLOCKED_INFRA (preexistente, no de esta
  sesión):** `StagerReconcile` falla desde 16:21 local con `recover durable
  activation: restart runtime service: …disabled` — la activación durable de
  0.2.142 quedó `phase=signaled` sin ack (StagerRuntime Stopped+Disabled por
  decisión owner) y el recovery aborta cada ciclo ANTES de stagear
  `releases\0.2.143` (Last Result 1). El worker sigue sano en 0.2.142.
  **Desbloqueo = decisión owner**: (a) arrancar StagerRuntime puntualmente
  para ack, (b) cerrar la activación en el estado durable del stager, o (c)
  tool stager de ack/dismiss. Detalle operativo en
  `.agents/skills/worker-troubleshooting/SKILL.md` (repo symphony).
- Rollout Linux (zeus/hera/kronos) no verificado: verificador de
  `deploy_release.sh` falla por SSH keyless desde daedalus (documentado).
- Sin smoke físico adicional: no requerido — la evidencia 6230 sigue vigente
  y 0.2.143 no está desplegada. Al desplegar, la evidencia legacy de
  slot-1..4 (sin contratos) fuerza una revalidación (re-smoke) en el primer
  backtest de cada slot, que asciende la evidencia al formato estricto.

Run: `80-agents/journal/agent-runs/2026-10-15-zcode-glm53-echo-forge-mt5-gateb-final-remediation.md`
