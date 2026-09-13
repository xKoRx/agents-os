---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo Forge — Factory V2 Completion]]"
sprint:
start: 2026-09-10
due:
progress: 95
repo: xKoRx/symphony
jira:
prs:
aliases:
  - F-04 Magic allocation version seal handoff
  - Echo Forge F-04 implementation
  - StrategyVersion seal handoff
tags:
  - kind/project
  - area/echo
  - agent/owner
created: "2026-09-10"
updated: "2026-09-13"
---

# Echo Forge — F-04 Magic allocation, version seal and handoff

%% Naming: Echo Forge — F-04 Magic allocation, version seal and handoff es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo Forge — F-04 Magic allocation, version seal and handoff
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo Forge — Factory V2 Completion]] · **Repo:** `xKoRx/symphony`
> Subproyecto de implementación de la fase F-04. Contrato: [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]].

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo Forge — Factory V2 Completion]] enlaza esta fase. El humano sigue el track desde [[Echo — Producto Integrado]].

## 🎯 Objetivo

Materializar el pipeline contractual Forge: allocation durable de magic → stamp/readback → compile/verify bytes → StrategyVersion seal → HandoffManifestV1 write-once → thin adapter. S0 pin `91671f6f`. CC = `CC_MISSING_OWNER_GATE` (no allocation física de producción). No escribir DB Echo. No tercer dominio Integration.

## 📊 Estado actual

- **C5.1–C5.6 IMPLEMENTED (2026-09-12) — READY FOR MANAGER REVIEW.** Commit `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`, parent C4 `bba833d7b57c767d6ce5ebfeae7a7b71b5785782`, pushed fast-forward en `feature/f04-magic-version-handoff`. `StrategyManifestIdentityReader` lee la fila exacta `sqx.strategies` por StrategyRef; instrument/timeframe/direction/canonical durable son authority; CanonicalStrategyID permanece opaco y sólo se compara exacto contra el carrier; OperationSide `L|LONG→LONG`, `S|SHORT→SHORT`, `B|BOTH/empty/unknown→CONTRACT_CONFLICT` antes de manifest/POST; requested instrument/timeframe/direction son gates WorkflowSpec tras TrimSpace exacto case-sensitive; observed/requested instrument/timeframe salen de la fila durable; parser legacy retirado. Tests C5 `-race` PASS, negative proofs 0 referencias; registry full sweep quedó limitado por timeout 10m de embedded-postgres y su subconjunto histórico no mostró fallas nuevas; migration NONE. C4.1–C4.6 permanecen CLOSED @ `bba833d7b57c767d6ce5ebfeae7a7b71b5785782`. **F-04 overall permanece NOT CLOSED / no physical-ready.** T2.11/T2.12/T2.13 permanecen OPEN.
- **Dependencia `aranea-ssh` (2026-09-13):** previous `UNHEALTHY / HTTP 503 session limit 64`; current `PASS / CLOSED — ARANEA SSH MCP HEALTH RESTORED`. `initialize`, `tools/list`, `resources/list`, cuatro smokes viewer y 5/5 ciclos create/use/DELETE pasaron; no se ejecutó restart por el agente y la causa histórica permanece `UNKNOWN` por falta de observabilidad server-side retrospectiva. F-04 queda `UNBLOCKED FOR T2.12 RESUME`, sin ejecutar T2.12 en esta sesión; release `0.2.98` se conserva y T2.11/T2.12/T2.13 permanecen OPEN.
- **C4.1–C4.6 IMPLEMENTED (2026-09-12).** CLOSED @ `bba833d7b57c767d6ce5ebfeae7a7b71b5785782`. Allocation desde `sqx.strategies`; mapper `MagicV1DirectionFromStrategy`; TaskSpec magic no requested; migration NONE. El residual de seal/handoff lo posee C5 (arriba), no se reabre C4.
- **TOP C4 CONTRACT CLOSED (2026-09-12).** One-shot TOP resolvió el defecto físico Magic V1 ↔ F-01: instrument/direction salen de `sqx.strategies`, no de `CanonicalStrategyID`. F-01 permanece CLOSED. TaskSpec `magic_number` no es requested. Multi-strategy soportado. `DATABASE MIGRATION: NONE`. Listo para NORMAL C4 sobre `feature/f04-magic-version-handoff` @ `d645ed6`. T2.11/T2.12/T2.13 permanecen OPEN. E-04 runtime/join es one-shot separado tras golden Forge.
- **T2.1–T2.10 IMPLEMENTED (2026-09-12).** NORMAL ejecutó el plan TOP congelado sobre worktree aislado limpio. Compile Evaluation `mt5_compiler@mt5-compile.v1` producida por `mt5_compile_persist_v1` (sqx-worker), carrier `CompileEvaluationRef` exacto, `UseDurableMagicAllocation: true` en el caller productivo, `forge_seal_handoff_v1` (seal+handoff tras Finalist V2, G22 incluido), HTTP ingress E-04 real + GET-by-key + fail-closed sin config. SOURCE+CONTRACT+CONCURRENCY (`-race`)+MIGRATION PASS. **PHYSICAL: STOP — C4 (Magic V1 parseaba CanonicalStrategyID opaco).** HEAD `d645ed6c2f438995d636a8213b1e4a3f5f26cbea` pushed fast-forward.
- S0 pin ya certificado por F-04; no se reabre ni se copian tipos desde Echo.
- CC: **resuelto — Magic Number V1 frozen** (owner decision 2026-09-11; `YYMMIIIDSSS`, XAUUSD=001). E-04 authority real: `xKoRx/echo@a99f9a63354bbe72219d1e590bb93757ed08e45e`; T2.13 espera golden auténtico **y** runtime E-04 aparte.
- `DATABASE MIGRATION: 015_strategy_magic_version_seal_handoff` + `016_magic_number_v1_allocator`. C4 no agrega migración.
- `GOD REQUIRED: NONE`.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/symphony | `feature/f04-magic-version-handoff` | `bba833d7b57c767d6ce5ebfeae7a7b71b5785782` | [[Echo Forge — Factory V2 Completion]] F-04 | [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] | **T1+T2.1–T2.10+C4.1–C4.6+C5.1–C5.6 DONE @ `b57bfb2`; READY FOR MANAGER REVIEW; T2.11–T2.13 OPEN; F-04 not closed/physical-ready** |

## Parent / SPEC / baselines

- Parent: [[Echo Forge — Factory V2 Completion]]
- SPEC: [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] — `VAULT_ROOT/30-resources/applications/Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract.md`
- Frozen: S0 pin; Live Authority §3; F-01/F-02/F-03 CLOSED no se reabren; B1/B2 no-touch.

## Source map

Magic TaskSpec: `sqx/core/runtime/config.go` `ApplySelectedRunTaskConfig.MagicNumber`; validate `mt5_task_config.go`. Apply: `sqx/adapters/apply-selected-run/binding/contract.go` `ApplicationConfig` + `HashIdentity`; physical `durable_apply_selected_run_physical.go` `writeApplySelectedRunProperties`; Java `EchoForgeRobustRunExporter`. Compiler físico `sqx/adapters/mt5/artifact_compiler.go` `ArtifactCompiler.Compile` via `MT5ArtifactActivities.CompileArtifact` (`mt5_compile_artifact` en `sqx-mt5-queue`). Caller compile: `generic_workflow.go` `executeMT5CompilerTask` → `executeMT5ArtifactTask` → child `MT5CompileArtifactWorkflow`. Identity `persistence_identity.go` `NewEvaluationRef` / `NewStageExecutionIdentity`. Finalist V2: `runFinalistPromotion` / `decision.go` policy `2.0.0`. F-04 actual: `sqx/core/forge/handoff_producer.go`, `sqx/core/capabilities/handoff.go`, StrategyVersion stores y migration 015/016. **Gap cerrado en planning:** compile no llama `ResolveStageExecution`/`PutEvaluation`/`CompleteStageExecution`; el patrón vivo a reusar es `persistMT5ReconcileV1` + `durable_apply_selected_run.go` recover/complete. `UseDurableMagicAllocation` existe pero el caller `runDurableApplySelectedRun` nunca lo setea. No existe HTTP E-04 en Symphony (`FakeConsumerIngress` only).

## Requirement-to-evidence

Estado vigente tras T1 (`ea8be76`) y T2 (`d645ed6`). La tabla histórica "todo missing" quedó obsoleta; se corrige in-place sin reescribir historia (el detalle por tarea vive en Atomic tasks y bitácora).

| Req | State | Evidence |
|---|---|---|
| Durable unique magic CAS | **done (T1/T2.6)** | migration 015 `sqx.strategy_magic` + allocator CAS; caller productivo con `UseDurableMagicAllocation: true` |
| Same identity replay | **done (T1)** | Allocate replay-first reusa motor CAS/UNKNOWN_COMMIT (`magic_v1.go`, tests `-race`) |
| Stamp readback == allocated | **done (T1/T2.7)** | `magic-readback` XML+MQ5 + `VerifyMagicReadback` en assembler; mismatch fail closed sin seal |
| Seal S0 StrategyVersionRef | **done (T1/T2.7)** | `SealStrategyVersion` write-once + `forge_seal_handoff_v1` (receta S0, recompute) |
| HandoffManifestV1 write-once | **done (T1/T2.7/T2.8)** | `BuildHandoffManifest` con caller productivo tras Finalist V2; persist write-once |
| Thin adapter + fakeconsumer | **done (T1/T2.9)** | port `HandoffIngress`: fakeconsumer CONTRACT + HTTP E-04 real (`http_ingress.go`) |
| G22 zero POST | **done (T1/T2.8)** | `HandoffMembersForDecision` membership vacía → 0 manifests/0 deliveries/0 POST (tests assembler) |
| CC gate | **resuelto (T1)** | Magic Number V1 owner allocator; `CC_MISSING_OWNER_GATE` eliminado de producción |
| No Echo DB writes | **done (T2.9)** | HTTP client sin SQL; grep SOURCE sin writes Echo |
| HashIdentity ≠ H() | **done (T1/T2)** | test desigualdad persistente; compile digest usa receta D16 MT5 (schema+JSON), seal usa recetas S0 |
| Compile EvaluationRef | **done (T2.1–T2.5)** | binding `mt5-compile.v1` + `mt5_compile_persist_v1`; cardinalidad 1, recovery exacto |

## Decision register

## Resultado de esta sesión — 2026-09-13

- `BASELINE_GATE: PASS` — `git ls-remote origin refs/heads/feature/f04-magic-version-handoff == b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`; no se tocó el checkout local dirty ni se hizo republish.
- `WINDOWS VIEWER POLICY PROOF: FAIL` — `mt5-kronos` viewer admitió sólo `hostname` → `worker-kronos` y `whoami` → `worker-kronos\\echo-dev`; `Get-Service -Name StagerRuntime`, `sc.exe query StagerRuntime`, `ver`, `tasklist.exe /FI \"IMAGENAME eq sqx-mt5-worker.exe\"`, `Get-Process -Name sqx-mt5-worker`, `Get-ChildItem C:\\ProgramData\\Stager` y `where.exe sqx-mt5-worker.exe` fueron operaciones únicas rechazadas con `POLICY_DENIED: Profile \"mt5-kronos\" is read-only, so \"safe\" commands are refused. Clear readOnly on the profile to allow them.`
- La evidencia requerida de servicio, proceso, path, release y poller es read-only; `mt5-kronos` es el perfil contractual viewer; las formas mínimas admisibles intentadas quedaron policy-denied. Resultado: `PHYSICAL BLOCKED — ARANEA MCP POLICY GAP — MT5 VIEWER`.
- No se obtuvo Windows effective path/release; no se declara `worker-kronos` en `0.2.98`, no se usó operator, no se generaron WorkflowID/RunID/FlowRunRef, no se ejecutó LICENSE, T2.12 ni T2.11; T2.13 permanece OPEN y fuera de scope.
- Próximo paso exacto: corregir la allowlist viewer Windows o exponer un probe read-only equivalente; repetir sólo rollout proof sobre la release existente, sin republish.

## Corrección de autoridad runtime — 2026-09-13 02:17

- **Corrección histórica obligatoria:** el intento anterior observó los marcadores legacy `/opt/symphony/CURRENT` y `/opt/symphony/current`; esos marcadores son **LEGACY / NON-AUTHORITATIVE**. Por tanto, la conclusión anterior `0.2.98 absent` **no fue probada** y se conserva sólo como historia, no como estado vigente.
- `BASELINE_GATE: PASS` — `origin/feature/f04-magic-version-handoff == b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`; worktree de certificación detached en ese SHA; cambios dirty ajenos preservados.
- `RELEASE_INTEGRITY: PASS` — la release ya publicada `0.2.98` conserva `vcs.revision=b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`; los seis artefactos locales coinciden en tamaño/SHA256 con `deploy/manifest.json`. No se hizo build ni republish.
- **Autoridad Linux real observada vía `stager-runtime.service`:** Zeus `MainPID=2633846`, worker `2633855`, `/opt/stager/releases/0.2.98/bin/symphony`, activation `fedae05f396c3c3331fe6874f94c827a`, `phase=committed`, `CURRENT/PENDING=0.2.98`, poller `sqx-main-queue`; Hera `MainPID=1231833`, worker `1231842`, mismo executable/release, activation `06c12ff55d4685f2dbbfc339367499be`, `phase=committed`, `CURRENT/PENDING=0.2.98`, poller `sqx-main-queue`; Kronos `MainPID=1203611`, worker `1203622`, mismo executable/release, activation `09de2d65259a9ebd5e613a16cebfd727`, `phase=committed`, `CURRENT/PENDING=0.2.98`, poller `sqx-main-queue`. Los tres servicios están `active (running)` y sus logs registran worker registrado/Started Worker.
- **Legacy separado:** en los tres hosts `/opt/symphony/CURRENT=9.9.11`, `/opt/symphony/current→/opt/symphony/releases/0.2.40`; `/var/lib/symphony/PENDING` no existe donde fue consultado. Se registra explícitamente como **LEGACY / NON-AUTHORITATIVE** y no se modificó.
- **Windows no probado:** el perfil viewer `mt5-kronos` rechazó las lecturas necesarias de `StagerRuntime`, proceso `sqx-mt5-worker`, path, start y poller con `POLICY_DENIED`; no se elevó a operator sólo para inspección. No existe evidencia admisible para afirmar `C:\ProgramData\Stager\releases\0.2.98` activo.
- `ROLLOUT_PROOF: INCONCLUSIVE`; último stage probado: release publicada y materialización/activación Linux por Stager; primer stage no probado: autoridad runtime Windows. `PHYSICAL BLOCKED — ENVIRONMENT — RUNTIME_AUTHORITY_GAP`; no es evidencia de release mixta ni defecto de producto.
- No se generó WorkflowID/RunID/FlowRunRef; LICENSE, T2.12 físico y T2.11 golden siguen `OPEN`; T2.13 sigue `OPEN` y fuera de scope. Próxima acción exacta: habilitar una lectura viewer admisible para `mt5-kronos` y repetir rollout proof sin publicar otra release.

## Certificación física — 2026-09-13

- `BASELINE_GATE: PASS` — `origin/feature/f04-magic-version-handoff == b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`; dirty extranjero preservado; worktree aislado `symphony-f04-cert-20260913` detached en el SHA certificado.
- `PRE_RELEASE: PASS` — grep de `strategyIdentityFromCanonicalID|ParseMagicV1AllocationIdentity` en `sqx/` = 0; focos C4/C5 con `-race`, build y vet PASS.
- `RELEASE: PASS` — `release-authority` AUTO asignó `0.2.98` (`published=0.2.97`, consistente); `deploy_release.sh --release-only "" 60` compiló Linux/Windows, publicó `worker/sqx/manifest.json` en MinIO y dejó hashes/tamaños coincidentes para seis artefactos. `vcs.revision=b57bfb2c...`; `vcs.modified=true` de watcher/Windows explicado por artefactos operacionales ignorados.
- `ROLLOUT: INCONCLUSIVE` — la espera de 60 s no es prueba de runtime; no existe MCP SSH/runtime para observar `CURRENT`, `ACTIVATION`, rotación PID/pollers y MetaEditor/licencia en Zeus, Hera, Kronos Linux y Windows MT5. No se usó SSH directo.
- `PHYSICAL BLOCKED — ENVIRONMENT` — no se modificó input ni se disparó WorkflowID/RunID; no se produjo StrategyRef, Magic, EvaluationRef, StrategyVersion, DecisionRef o HandoffManifest auténtico. La causa exacta es ausencia de capability MCP SSH/runtime para el gate de rollout/licencia, con SSH directo fuera de autoridad.
- `T2.12: OPEN`; `T2.11: OPEN`; `T2.13: OPEN`. Primer bloqueo: capability de observación runtime ausente; no hay evidencia de defecto de producto.
- Evidencia durable: repo `xKoRx/symphony`, worktree `symphony-f04-cert-20260913`, `deploy/0.2.98/` y `deployer_screen.log`; registro de agente en `80-agents/journal/agent-runs/2026-09-13-codex-unknown-f04-physical-certification.md`.

## Reanudación física — 2026-09-13

- `MCP DISCOVERY: PARTIAL` — el cliente expone `aranea_mongo_forge_ro/rw` y `aranea_postgres_ro/rw`, ambos probados; `aranea-ssh` está declarado en la configuración con bearer `SET`, pero no expone tools en esta sesión.
- `ARANEA SSH: UNHEALTHY` — dos handshakes MCP contra `aranea-ssh` fallaron con HTTP 503: `Server is at its session limit (64). Close an existing session and retry.`; no se pudo ejecutar `read-command`/`run-command` ni leer hosts.
- `RELEASE 0.2.98: PASS` — authority local y branch remoto permanecen en `0.2.98`/`b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`; seis artefactos coinciden en tamaño/SHA256 y `deployer_screen.log` registra seis uploads más manifest recuperado y publicado en MinIO.
- `ROLLOUT: INCONCLUSIVE` — sin `aranea-ssh` sano no hay prueba por Zeus, Hera, Kronos o `worker-kronos` de `CURRENT`, symlink activo, ACTIVATION/PENDING, rotación de PID, pollers, MetaEditor/SQX o licencia.
- `PHYSICAL BLOCKED — ARANEA MCP UNHEALTHY` — host/runtime requerido: Zeus, Hera, Kronos y Windows `worker-kronos`; capability requerida: `aranea-ssh` viewer `read-command` y operator sólo para acciones explícitamente autorizadas; operación intentada: handshake MCP `resources/list` contra `http://mcps.lab.aranea.cl:3000/`; error exacto: HTTP 503 por límite de 64 sesiones. Stager/control-plane sólo demuestra publicación/manifest y no puede responder el estado físico de hosts, procesos o licencia.
- No se modificó product code, input, release, binaries ni configuración remota; no se generó WorkflowID/RunID/FlowRunRef y T2.12/T2.11 no iniciaron.
- `T2.12: OPEN`; `T2.11: OPEN`; `T2.13: OPEN`. Se conserva el intento anterior como historia (`release PASS`, `rollout INCONCLUSIVE`, `physical not started`); esta reanudación corrige la clasificación operacional a MCP unhealthy sin reescribirla.
- Evidencia nueva: `80-agents/journal/sessions/2026-09-13-f04-physical-resume-summary.md`, `80-agents/journal/agent-runs/2026-09-13-codex-unknown-f04-physical-resume.md`, `80-agents/journal/feedback/system-1/2026-09-13-f04-physical-resume-session-feedback.md` y `80-agents/journal/change-logs/2026-09-13-f04-physical-resume-project-update.md`.

## Registro de sesión física — 2026-09-13 01:58 America/Santiago

- Nueva conversación/agente NORMAL — PHYSICAL CERTIFICATION / EVIDENCE AGENT.
- Objetivo: certificar `0.2.98` sobre `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`, probar rollout y continuar T2.12/T2.11 sólo con evidencia física auténtica; T2.13 queda fuera de alcance.
- Precondición inicial: `aranea-ssh` visible en MCP y listo para revalidación; no se ha creado WorkflowID/RunID/FlowRunRef.
- Registro temprano: baseline remoto y release se verificarán antes de cualquier acción writable; dirty extranjero del checkout local queda preservado.

## Resultado sesión física — 2026-09-13 02:05 America/Santiago

- `BASELINE_GATE: PASS` — `git ls-remote origin refs/heads/feature/f04-magic-version-handoff == b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`; el checkout de certificación está detached en ese SHA. Dirty operacional `deploy/manifest.json` del worktree de certificación y dirty extranjero del checkout principal se preservan sin stage/commit.
- `RELEASE_INTEGRITY: PASS` — manifest operativo declara `0.2.98`; los seis artefactos locales coinciden en SHA256/tamaño; `deployer_screen.log` registra 6 uploads, manifest recuperado/publicado y `release_version=0.2.98`. No se volvió a publicar.
- `ROLLOUT_PROOF: FAIL` — Zeus/Hera/Kronos: `/opt/symphony/releases/0.2.98` no existe, `/opt/symphony/PENDING=0.2.40`, `/opt/symphony/current -> /opt/symphony/releases/0.2.40`; el log Stager no contiene `0.2.98`. Además, `/opt/symphony/CURRENT` contiene `9.9.11`, inconsistente con symlink/PENDING. `mt5-kronos` viewer rechazó lecturas PowerShell con `POLICY_DENIED`; no se elevó por comodidad.
- `PHYSICAL BLOCKED — ENVIRONMENT`: último stage probado = release publicada por Stager; primer stage fallido = materialización/activación runtime `0.2.98`. No se creó WorkflowID/RunID/FlowRunRef, no se evaluó licencia y no se ejecutó candidato. T2.12/T2.11/T2.13 permanecen OPEN.
- Próximo paso exacto: Manager/owner debe recuperar el Stager/deployer canónico para materializar `0.2.98` en Zeus, Hera, Kronos y MT5; luego repetir rollout proof desde esta release sin republish. Esta sesión no autoriza symlink manual, copia host-by-host ni una release nueva.
- Evidencia de cierre: `80-agents/journal/sessions/2026-09-13-f04-physical-certification-blocked-summary.md`, `80-agents/journal/agent-runs/2026-09-13-0205-codex-unknown-f04-physical-certification-blocked.md`, `80-agents/journal/feedback/system-1/2026-09-13-f04-physical-certification-blocked-session-feedback.md` y `80-agents/journal/change-logs/2026-09-13-f04-physical-certification-blocked.md`. Golden evidence: `NONE`.

| ID | status | resolution | source | phase |
|---|---|---|---|---|
| D1 sequence | TECHNICAL_RESOLUTION | Allocation **before Apply** for Apply cohort; Finalist V2 admits seal/handoff only | Live Authority §3; padre F-04 hypothesis | 1 |
| D2 mapping | TECHNICAL_RESOLUTION | 1:1 StrategyRef↔magic; 1:N StrategyVersion same magic | S0 G04/G05; Live Authority | 1 |
| D3 namespace | TECHNICAL_RESOLUTION | `forge-live` | S0 fixtures | 1 |
| D4 allocation_ref | TECHNICAL_RESOLUTION | `H("forge-magic-allocation.v1",[ns,canonical,magic_decimal])` | Live Authority | 1 |
| D5 CAS | TECHNICAL_RESOLUTION | UNIQUE(ns,strategy_ref)+UNIQUE(ns,magic)+SELECT-then-INSERT; conflict magic → next candidate N=32; never random/MAX+1/hostname | this SPEC | 1 |
| D6 reserved | TECHNICAL_RESOLUTION | `11111` y `888111` no allocatable | source defaults | 1 |
| D7 CC | TECHNICAL_RESOLUTION | `CC_MISSING_OWNER_GATE`; production physical Allocate fail-closed; tests inject MagicCandidateSource | O2 owner | 1 |
| D8 readback | TECHNICAL_RESOLUTION | XML `.sqx` + MQ5; mismatch FAIL CLOSED; no EX5 parse | source gap | 1 |
| D9 requested | TECHNICAL_RESOLUTION | **C4 corrected:** TaskSpec `magic_number` is legacy Apply stamp, not F-04 requested authority. F-04 stamps allocated and overwrites it. No dedicated requested field exists; do not invent one in C4. Reserved `888111`/`11111` in TaskSpec are historical defaults. | source `AllocatedEffectiveConfig` + `ValidateWorkflowSpec`; PHYSICAL `888111` | 3 |
| D10 seal recipe | TECHNICAL_RESOLUTION | S0 `StrategyVersionRef`; effective_inputs via `C()`/`H()` not HashIdentity | S0 evidence.go | 1 |
| D11 handoff | TECHNICAL_RESOLUTION | S0 `HandoffManifestV1` + IdempotencyKey + PayloadDigest; G22 0 POST | S0 promotion.go | 1 |
| D12 adapter | TECHNICAL_RESOLUTION | Port `HandoffIngress`; CONTRACT fakeconsumer; no provisional E-04 URL | E-04 To Do | 1 |
| D13 post-commit | TECHNICAL_RESOLUTION | timeout post-commit → `UNKNOWN_RECEIPT`; no re-POST | S0 G35; this SPEC | 1 |
| D14 migration | TECHNICAL_RESOLUTION | `015_strategy_magic_version_seal_handoff` | last 014 | 1 |
| D15 hashes | TECHNICAL_RESOLUTION | keep HashIdentity on Apply Evaluation internals; S0 recipes only on seal/handoff/allocation_ref | FR-4 | 1 |
| D16 compile_evaluation_ref | TECHNICAL_RESOLUTION | Autoridad = `domain.EvaluationRef` de un compile StageExecution `mt5_compiler@mt5-compile.v1` persistido en Mongo EvaluationEvidence + `sqx.stage_execution_results`. Produce sólo tras compile físico success verificado. Cardinalidad 1. Recovery por ref exacta / `LoadEvaluation`, nunca latest. MIGRATION 017 NO. | Durable Foundation; `persistMT5ReconcileV1` analog; this TOP 2026-09-12 | 2 |
| D17 C4 allocation inputs | TECHNICAL_RESOLUTION | Instrument = `sqx.strategies.instrument`; direction = `sqx.strategies.direction`; mapper `MagicV1DirectionFromStrategy`; catalog `sqx.magic_instruments`; CanonicalStrategyID opaque never parsed; replay conflict via `DecodeMagicV1` III+D; no new migration. | PHYSICAL `d645ed6` / F-01 `0509342`; this TOP 2026-09-12 | 3 |
| D18 C5 manifest identity | TECHNICAL_RESOLUTION | HandoffStrategy + MemberProof instrument/timeframe/direction from `sqx.strategies` by StrategyRef; CanonicalStrategyID opaque; OperationSide LONG/SHORT via C4 mapper; BOTH fail closed (S0 has no BOTH; Echo unchanged); requested/observed = same durable row; WorkflowSpec is exact-match gate not authority; no SQX/MQ5 instrument/TF readback; StrategyIdentityView not extended; migration NONE. | `forge_seal_handoff.go` @ `bba833d`; S0 `91671f6f` trading.go/promotion.go; this TOP 2026-09-12 | 4 |

## Technical resolution — compile Evaluation (frozen 2026-09-12)

Hipótesis preferida **aceptada con prueba de source**. `EvaluationEvidence` existente representa compile; `ResolveStageExecution` / `PutEvaluation` / `CompleteStageExecution` / `LoadStageExecutionResults` / `LoadEvaluation` ya sellan refs inmutables. No hay stage contract compile hoy (`mt5_compiler@` ausente); se congela uno nuevo con la fórmula canónica `CanonicalStageKey(taskType, producerContractVersion)`, no un identity system nuevo.

### Source trace (authority → símbolo → identidad durable → replay)

1. **Caller ArtifactTaskRequest:** `generic_workflow.go` `executeMT5CompilerTask` → `executeMT5ArtifactTask` → `startMT5ArtifactChildren`. Identidad de routing: `RequestID` + `SourceKey`; durable: `FlowIntentToken`+`FlowRunRef`+`TaskPath`+`StrategyRef`+`SourceArtifact`. Replay Temporal: child workflow ID `MT5ArtifactChildWorkflowID`; no es EvaluationRef.
2. **StageExecution compile (hoy ausente):** debe crearse como Apply/MT5 reconcile, no existe en compile. Identidad futura: `NewStageExecutionIdentity` `TaskType=mt5_compiler` `ProducerContractVersion=mt5-compile.v1` subject STRATEGY `Generation=1`. Replay: `ResolveStageExecution` converge por `execution_intent_key`; retry Temporal no crea otro slot.
3. **Child workflow:** `MT5CompileArtifactWorkflow` → `ExecuteMT5CompileArtifactActivity`. Identidad Temporal only. Replay: MaximumAttempts ilimitado; contract/source_not_found non-retryable.
4. **Compile activity:** `MT5ArtifactActivities.CompileArtifact` (`mt5_compile_artifact`) en `sqx-mt5-queue`. Resultado `ArtifactTaskResult` (EX5/log/source). Retry infra; functional fail retorna `Status=failed` error nil — **no Evaluation**.
5. **Compiler físico:** `mt5.ArtifactCompiler.Compile` / `evaluateCompileArtifacts`. Bytes EX5+log en MinIO. SHA/size son integridad de artifact, no EvaluationRef.
6. **Evidence writer comparable:** `apply-selected-run/binding.BuildEvidence` + `DurableApplySelectedRunActivity.persistApplyEvidenceAndComplete`; MT5 analog `adapters/mt5/binding.PersistEvidence` llamado desde `persistMT5ReconcileV1` en **parent queue** (`sqx-worker`), no en Windows.
7. **Helpers Evaluation:** `domain.NewEvaluationRef(stageExecutionRef, subject.Digest, scopeDigest, producerContractVersion)`; Apply `BuildEvidence`; MT5 `binding.BuildSubject`/`BuildScope`.
8. **PutEvaluation:** `capabilities.ImmutableEvidenceStore.PutEvaluation` → `adapters/metadata-mongo/evidence_store.go`. Same digest ACK; distinct digest CONTRACT_CONFLICT.
9. **CompleteStageExecution:** `ControlPlane.CompleteStageExecution` inserta `sqx.stage_execution_results` y sella COMPLETED. Replay same ref set ACK; distinct set CONTRACT_CONFLICT. Empty set sólo si no hay producer-output.
10. **Exact readback:** `LoadStageExecutionResults(exact StageExecutionRef)` + `LoadEvaluation(exact EvaluationRef)`. Apply `recoverCompleted` exige `len(EvaluationRefs)==1`.
11. **Finalist V2:** `generic_workflow.go` `runFinalistPromotion` → `FinalistPromotionActivityName`. Decision write-once. Membership estructural; rank no entra.
12. **StrategyVersion seal:** `ControlPlane.SealStrategyVersion` / `domain.StrategyVersionIdentity.Ref` receta S0. Capacidades `VerifyMagicReadback` + `VerifyCompiledArtifactForSeal` existen **sin caller productivo**.
13. **Handoff producer:** `forge.BuildHandoffManifest` copia `HandoffArtifacts.CompileEvaluationRef` a S0 `BuildLineage`. Callers productivos: **ninguno** (sólo tests). Delivery: `capabilities.DeliverHandoff` + `echo-handoff.FakeConsumerIngress`.

### Compile Evaluation contract

| Campo | Valor frozen |
|---|---|
| `stage.key` | `mt5_compiler` (TaskSpec.Type vivo) |
| `stage.contract_version` | `mt5-compile.v1` |
| StageKey | `mt5_compiler@mt5-compile.v1` |
| Subject | `STRATEGY` / StrategyRef UUID / digest `HashIdentity("mt5-compile-strategy-subject.v1", JSON {schema,strategy_ref})` — artefact SHA no entra al subject |
| InputEvaluationRefs | exactamente uno: role `source_evaluation` = `StrategyArtifact.EvaluationRef` del carrier (la Evaluation SQX que `mt5_exporter` ya `LoadEvaluation`). Compile persist **no** busca Apply por latest. Assembler F-04 exige que esa Evaluation tenga `Stage.Key=apply_selected_run` y `ContractVersion=sqx-apply-selected-run.v1`; si no, no seal/handoff |
| Scope JSON | `{"schema":"mt5-compile-scope.v1","platform":"MetaTrader5","compiler":"MetaEditor64 /portable"}`. Prohibido: host, worker, Temporal IDs, timestamps, request ID, artifact SHA |
| ScopeDigest | `HashIdentity("mt5-compile-scope.v1", canonical JSON)` |
| Producer.component | `sqx-mt5-compile` |
| Producer.contract_version | `mt5-compile.v1` (identidad semántica; participa en EvaluationRef) |
| Producer.build_ref | `mt5-compile.v1` (provenance de contrato, no git SHA; igual convención Apply) |
| Artifacts | INPUT `STRATEGY_MQ5` = source MQ5 durable; OUTPUT `EX5` = PrimaryDurable; EVIDENCE `LOG` = compile log durable. SQX es dependencia upstream vía `source_evaluation`, no INPUT directo del compile |
| Payload | `{"schema":"mt5-compile-payload.v1","result":"success","error_count":0}` — no duplicar bytes ya en ArtifactRef |
| ConfigurationSnapshot | `{"schema":"mt5-compile-config.v1","compiler":"MetaEditor64 /portable","platform":"MetaTrader5"}` — no `{}` |
| Variant | `{"schema":"mt5-compile-variant.v1","operation":"compile"}` |
| EvaluationRef | `domain.NewEvaluationRef(stageRef, subject.Digest, scopeDigest, "mt5-compile.v1")` |
| CreatedAt | metadata only; no identidad (igual MT5 evidence) |

### Success / failure

- **Success:** EX5 non-empty + SHA/size match + compile log `Result: 0 errors` + source MQ5 SHA == expected `SourceArtifact` (`VerifyCompiledArtifactForSeal` **antes** de `ResolveStageExecution`). Entonces Persist: Resolve → PutEvaluation → CompleteStageExecution(`[exactly 1 ref]`).
- **Functional failure:** no Evaluation de éxito; no Complete con ref usable. No crear fila StageExecution (parser-before-write como `mt5_reconcile_v1`). No es candidato de seal/handoff.
- **Infra / cancel:** error retryable; sin fake success; StageExecution no se abre. Cancel Temporal nativa del compile activity.

### Replay / UNKNOWN_COMMIT / cardinality

- Mismo StageExecution + mismos bytes/evidence → mismo EvaluationRef (PutEvaluation ACK; Complete ACK).
- Mismo slot + contenido inmutable distinto → PutEvaluation / Complete `CONTRACT_CONFLICT` (payload digest o result set).
- Evidence ACK perdido: retry recomputa el mismo ref y `LoadEvaluation(exact)`; no latest.
- UNKNOWN_COMMIT: retryable; `ResolveStageExecution` reconcilia UUID existente; un solo EvaluationRef.
- Retry Temporal / Run ID distinto: no cambia `ExecutionIntentKey` ni EvaluationRef.
- **Cardinalidad:** 1 StageExecution success → exactamente 1 EvaluationRef. 0 → no seal/handoff. >1 → `CONTRACT_CONFLICT`. Nunca first/latest.

### Caller seam (no topología global)

No se declara “compile always followed by seal”. Dos seams existentes y opt-in:

1. **Produce (MUST):** `executeMT5ArtifactTask` tras compile `PersistenceModelV1` + `ArtifactStatusSuccess` → nueva activity `mt5_compile_persist_v1` en queue padre (`sqx-worker`), espejo de `persistMT5ReconcileV1`. El persist **no** corre en `sqx-mt5-queue`. Devuelve StageExecutionRef+EvaluationRef; el parent escribe `StrategyArtifact.CompileEvaluationRef` **sin** pisar `EvaluationRef` (Apply/source).
2. **Consume (MUST):** `runFinalistPromotion` tras Decision V2 completed → activity `forge_seal_handoff_v1`. Por cada member: exact Finalist Decision + StrategyRef + MagicAllocation + Apply EvaluationRef (carrier `EvaluationRef` validado como Apply) + Compile EvaluationRef (carrier o `LoadStageExecutionResults` de la StageExecution re-resoluble por intent) + bytes verificados → `SealStrategyVersion` → `BuildHandoffManifest` → persist write-once → `DeliverHandoff`. G22: membership vacío → 0 manifests.

`UseDurableMagicAllocation` debe setearse en `runDurableApplySelectedRun` para el path F-04; hoy el flag existe y el caller productivo lo deja false.

### Migration

**MIGRATION 017 REQUIRED: NO.** Mongo EvaluationEvidence + PG `stage_executions` + `stage_execution_results` expresan el hecho. 015/016 no-touch. Un reader `LoadStageExecutionIdentityByIntent` sería MAY sobre índice UNIQUE existente, no migración.

### E-04 join (plan, no HTTP client en este TOP)

Tras T2 compile+seal+handoff: Finalist real → manifest canónico → `POST /api/v1/forge/promotions` → receipt `INGESTED` → GET by-key → golden T21/AC-37. Consumer Echo `@ a99f9a63354bbe72219d1e590bb93757ed08e45e`. Puerto `HandoffIngress.Deliver(ctx, ns, *HandoffManifestV1, payloadDigest)`.

### PHYSICAL (operacional, no planning blocker)

Host mínimo para NORMAL cert: (1) SQX/sqcli con licencia válida para exporter MQ5 — si SQX reporta expired: STOP owner, sin trial-key; (2) MetaEditor64 `/portable` en worker `sqx-mt5-queue`; (3) PG control plane + Mongo evidence + object store; (4) reachability HTTP Echo promotions. No convertir viewers read-only en workers. `mt5-kronos` inaccesible es blocker de ejecución, no de este plan.

### Dirty worktree

`specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json` es dirty foráneo. NORMAL trabaja en worktree aislado o lo preserva. No restaurar/borrar/commitear en F-04.

## Planned diff

Fase 1 (T1.x) **done** en `ea8be76`. Fase 2 (T2.x) **done** en `d645ed6` salvo PHYSICAL/golden. **C4 MUST (NORMAL): DONE en `bba833d` (2026-09-12).** **C5 MUST (NORMAL):**

- create `StrategyManifestIdentityReader` on control plane: `SELECT canonical_strategy_id, instrument, direction, timeframe FROM sqx.strategies WHERE id = $1`; do **not** extend `StrategyIdentityView`
- modify `forge_seal_handoff.go` — delete `strategyIdentityFromCanonicalID`; load durable row; map OperationSide; spec exact-match gate; requested/observed from row
- modify `generic_workflow.go` — pass `spec.Direction` as request gate only
- delete `ParseMagicV1AllocationIdentity` / `isInstrumentShapedToken` once zero consumers
- tests C5.5; SOURCE grep C5.6
- no new migration; do not modify `015_*.sql` / `016_*.sql`; do not change Echo S0; do not reopen C4 allocation

C4 DONE @ `bba833d` (do not reopen):

- modify `sqx/core/domain/magic_v1.go` — retire `ParseMagicV1AllocationIdentity`; add `MagicV1DirectionFromStrategy` ✅ (parser retirado del allocation path; C5 retira el consumer de seal)
- modify `sqx/adapters/registry-postgres/magic_v1.go` — `AllocateMagicV1` SELECT instrument/direction from `sqx.strategies`; replay conflict via `DecodeMagicV1` ✅
- modify `sqx/adapters/registry-postgres/magic_allocation_test.go` `f04Strategy` — persist instrument/direction under test ✅
- modify `sqx/adapters/apply-selected-run/binding/contract.go` `AllocatedEffectiveConfig` — TaskSpec magic is not requested ✅
- modify tests listed in C4.5; SOURCE grep C4.6 ✅
- no new migration; do not modify `015_*.sql` / `016_*.sql` ✅ (015/016 byte-untouched, 017 inexistente)

### MUST (T2, already done)

- create `sqx/adapters/mt5-compile/binding/` (`contract.go`, `evidence.go`, `subject.go`) — no reusar `adapters/mt5/binding` (ese paquete es `mt5_backtesting@mt5-backtest.v1`)
- create `sqx/activities/worker/mt5_compile_persist_activity.go` activity name `mt5_compile_persist_v1`
- modify `sqx/cmd/sqx-worker/main.go` register persist (parent worker, **not** mt5-worker)
- modify `sqx/workflows/generic_workflow.go` `executeMT5ArtifactTask`: tras compile V1 success llamar persist (espejo `persistMT5ReconcileV1`); `runFinalistPromotion` tras V2 → seal/handoff
- modify `sqx/core/runtime/config.go` `StrategyArtifact.CompileEvaluationRef` omitempty; no pisar `EvaluationRef`
- modify `sqx/workflows/durable_apply_selected_run_workflow.go` set `UseDurableMagicAllocation: true` en el path F-04
- create `sqx/activities/worker/forge_seal_handoff.go` (`forge_seal_handoff_v1`) using existing `VerifyMagicReadback` / `VerifyCompiledArtifactForSeal` / `SealStrategyVersion` / `BuildHandoffManifest` / `DeliverHandoff`
- create `sqx/adapters/echo-handoff/http_ingress.go` implementing `HandoffIngress` over Echo POST `/api/v1/forge/promotions` + GET by-key
- tests: persist identity/replay/conflict/UNKNOWN_COMMIT/cardinality; assembler fail-closed sin compile eval; SOURCE greps no latest

### MAY

- `StageExecutionReader.LoadStageExecutionIdentityByIntent` sobre UNIQUE `execution_intent_key` (no migración)
- `StageProducerOutput` para EX5 compile (Apply lo usa; compile locator no depende de StageExecution UUID)
- campo `EvaluationRef` en `ArtifactTaskResult` (el persist result basta)

### NO-TOUCH

Migrations `015_strategy_magic_version_seal_handoff` y `016_magic_number_v1_allocator`. Magic V1 `YYMMIIIDSSS` / XAUUSD=001. F-01 CanonicalStrategyID. F-02 membership. F-03 SQX lifetime. B1/B2 ownership/takeover/Slot Pool. StrategyVersion S0 recipe. S0 `BuildLineage` fields. Echo source/DB. ranking-as-membership. delivery terminal semantics / `UNKNOWN_RECEIPT`. F-05. `adaptive_workflow.go`. `adapters/mt5/binding` backtest contracts. Foreign dirty `phase4_performance.json`. Invented EvaluationRef from SHA/key/workflow ID.

## No-touch

F-01 CanonicalStrategyID/publication. F-02 policy `finalist_promotion@2.0.0`. F-03 timeouts. F-05. B1A/B1B/B2 Slot Pool/fencing/takeover. Echo source. S0 types (consume, don't fork). `adaptive_workflow.go`. Foreign dirty symphony. Invented CC ranges. Provisional Echo HTTP distinto de E-04. Magic V1 codec layout `YYMMIIIDSSS` / catálogo 016. HashIdentity newline como `H()`. Product cardinality restricted to selection=1. Migration 017. Data repair of the cancelled physical run. C4 allocation algorithm. BOTH→LONG/SHORT mapping.

## Execution sequence

T1.1–T1.18 **done**. T2.1–T2.10 **done**. **C4.1–C4.6 DONE (2026-09-12, `bba833d`) CLOSED.** Siguiente: **NORMAL C5.1–C5.6.** T2.11 golden capture. T2.12 PHYSICAL. T2.13 cross-lane T21/AC-37 (E-04 runtime one-shot separado).

C5.2 after C5.1. C5.3 after C5.2. C5.4 after C5.2. C5.5 after C5.1–C5.4. C5.6 after C5.5. T2.11 after C5 + physical-capable host. T2.13 after T2.11 golden **and** separate E-04 runtime one-shot.

## Dependencies

F-01 CLOSED (stable IDs). F-02 CLOSED (V2 membership). F-03 CLOSED (no-touch). E-01 S0 pin. E-04 optional for INTEGRATION (development E-04 may run now; integrate/CROSS_LANE gated by E-03 CONTRACT_PASS). CC owner for PHYSICAL allocation.

## ✅ Tareas

> [!note]+ Ownership
> Board `#owner/agent`. Cada ítem es una TASK atómica para NORMAL tras autorización del manager.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. %%
> - [x] T1.1 go.mod pin S0 contracts + test HashIdentity ≠ H() #owner/agent #type/dev #area/echo
> - [x] T1.2 migration 015 strategy_magic + versions + manifests + deliveries #owner/agent #type/dev #area/echo
> - [x] T1.3 allocator CAS/replay/reserved 11111+888111 #owner/agent #type/dev #area/echo
> - [x] T1.4 CC_MISSING_OWNER_GATE + fixture MagicCandidateSource #owner/agent #type/dev #area/echo
> - [x] T1.5 Apply stamp usa allocated; requested must match #owner/agent #type/dev #area/echo
> - [x] T1.6 readback XML MagicNumber del .sqx #owner/agent #type/dev #area/echo
> - [x] T1.7 readback MQ5 MagicNumber #owner/agent #type/dev #area/echo
> - [x] T1.8 mismatch FAIL CLOSED no seal/handoff #owner/agent #type/dev #area/echo
> - [x] T1.9 compile verify size/sha/0-errors/source sha #owner/agent #type/dev #area/echo
> - [x] T1.10 StrategyVersion seal S0 write-once #owner/agent #type/dev #area/echo
> - [x] T1.11 HandoffManifestV1 producer S0 + MemberProof V2 #owner/agent #type/dev #area/echo
> - [x] T1.12 handoff_manifests write-once DetectSealedConflict #owner/agent #type/dev #area/echo
> - [x] T1.13 HandoffIngress + fakeconsumer CONTRACT #owner/agent #type/dev #area/echo
> - [x] T1.14 delivery states; no re-POST post-commit #owner/agent #type/dev #area/echo
> - [x] T1.15 corpus G04–G10 G19–G25 G22 #owner/agent #type/dev #area/echo
> - [x] T1.16 concurrent allocation same/different identity #owner/agent #type/dev #area/echo
> - [x] T1.17 BWC no backfill 888111; brownfield sin fila magic #owner/agent #type/dev #area/echo
> - [x] T1.18 SOURCE greps ownership/latest/ranking/HashIdentity-on-S0 #owner/agent #type/dev #area/echo
> - [x] T2.1 compile Evaluation binding contract `mt5-compile.v1` #owner/agent #type/dev #area/echo
> - [x] T2.2 `mt5_compile_persist_v1` activity + PutEvaluation/CompleteStageExecution #owner/agent #type/dev #area/echo
> - [x] T2.3 wire persist after durable compile success in `executeMT5ArtifactTask` #owner/agent #type/dev #area/echo
> - [x] T2.4 carrier `CompileEvaluationRef` exact pointer #owner/agent #type/dev #area/echo
> - [x] T2.5 exact recovery UNKNOWN_COMMIT cardinality CONTRACT_CONFLICT #owner/agent #type/dev #area/echo
> - [x] T2.6 `UseDurableMagicAllocation` productive caller #owner/agent #type/dev #area/echo
> - [x] T2.7 seal assembler exact Apply+Compile+readback+verify #owner/agent #type/dev #area/echo
> - [x] T2.8 handoff assembler after Finalist V2 #owner/agent #type/dev #area/echo
> - [x] T2.9 Echo HTTP `HandoffIngress` POST+GET by-key #owner/agent #type/dev #area/echo
> - [x] T2.10 Echo ingest auth/config #owner/agent #type/dev #area/echo
> - [x] C4.1 retire CanonicalStrategyID parser; add MagicV1DirectionFromStrategy #owner/agent #type/dev #area/echo
> - [x] C4.2 AllocateMagicV1 loads instrument/direction from sqx.strategies #owner/agent #type/dev #area/echo
> - [x] C4.3 replay/conflict DecodeMagicV1 III+D without new migration #owner/agent #type/dev #area/echo
> - [x] C4.4 AllocatedEffectiveConfig: TaskSpec magic_number is not requested #owner/agent #type/dev #area/echo
> - [x] C4.5 C4 contract/concurrency tests including opaque ID and cohort N `-race` #owner/agent #type/dev #area/echo
> - [x] C4.6 SOURCE grep: no parse of CanonicalStrategyID for magic semantics #owner/agent #type/dev #area/echo
> - [x] C5.1 LoadStrategyManifestIdentity from sqx.strategies by StrategyRef #owner/agent #type/dev #area/echo
> - [x] C5.2 replace strategyIdentityFromCanonicalID; OperationSide from durable direction; BOTH fail closed #owner/agent #type/dev #area/echo
> - [x] C5.3 requested/observed from durable row; WorkflowSpec exact-match gate #owner/agent #type/dev #area/echo
> - [x] C5.4 retire ParseMagicV1AllocationIdentity (zero consumers) #owner/agent #type/dev #area/echo
> - [x] C5.5 C5 contract tests including opaque ID, decoy string, LONG/SHORT/BOTH `-race` #owner/agent #type/dev #area/echo
> - [x] C5.6 SOURCE grep: no CanonicalStrategyID business-token parser on handoff path #owner/agent #type/dev #area/echo
> - [ ] T2.11 authentic Forge golden capture #owner/agent #type/dev #area/echo
> - [ ] T2.12 PHYSICAL certification host capabilities #owner/agent #type/dev #area/echo
> - [ ] T2.13 cross-lane smoke Echo T21/AC-37 #owner/agent #type/dev #area/echo

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

## Atomic tasks

Contrato de cada TASK: `archivo/símbolo → cambio exacto → authority → failure/retry → tests → DONE`. Sin decisiones arquitectónicas en NORMAL.

### T1.1 pin S0 contracts + HashIdentity ≠ H()

- **Modelo:** NORMAL
- **Archivos/símbolos:** `sqx/go.mod` (o módulo que compile el worker) require `github.com/xKoRx/echo/v3/sdk/contracts` @ `91671f6f46ffa889a79aed0979cb3b4e5821ed33`; test nuevo junto a `persistence_identity.go`.
- **Cambio:** importar el módulo nested S0. Test: mismo tag+parts → `domain.HashIdentity` ≠ `wire.HashTagged`. No modificar `hashIdentity`.
- **Authority:** FR-4; S0 `wire/hash.go` + `hash_legacy_inequality_test.go` patrón.
- **Failure/retry:** n/a (compile).
- **Tests:** `TestHashIdentity_DoesNotEqualS0H`.
- **DONE:** `go test` del paquete identity + módulo contracts se importa. Pin exacto en go.mod.
- **Stop:** fork de tipos S0 dentro de Symphony → PLAN_CONFLICT.

### T1.2 migration 015

- **Modelo:** NORMAL
- **Archivos:** `sqx/adapters/registry-postgres/migrations/015_strategy_magic_version_seal_handoff.up.sql` + `.down.sql`; runner de migrations existente.
- **Cambio:** tablas/UNIQUE/CHECK/FK exactos de la SPEC. Down solo DROP de esas tablas.
- **Authority:** SPEC migration section; last `014`.
- **Failure/retry:** restart-safe; no rewrite history.
- **Tests:** brownfield: DB con 014 applied → 015 up; strategies sin fila magic; down/up.
- **DONE:** migration aplica sobre dump 014; down no toca 001–014.
- **Stop:** ALTER destructivo de `sqx.strategies` history → PLAN_CONFLICT.

### T1.3 allocator CAS

- **Modelo:** NORMAL
- **Archivos:** `sqx/core/capabilities` `MagicAllocator`; `sqx/core/domain` allocation types; `sqx/adapters/registry-postgres` insert/SELECT.
- **Cambio:** algoritmo Allocate de la SPEC. `allocation_ref` vía `contracts`/`wire.HashTagged("forge-magic-allocation.v1", ...)`. Reserved skip.
- **Authority:** D3–D6.
- **Failure/retry:** matrix Allocate rows.
- **Tests:** replay same StrategyRef; two StrategyRefs unique; unique-violation retry next candidate; reserved 888111 rejected.
- **DONE:** tests verdes; PRODUCTION source no MAX+1.
- **Stop:** hostname/worker in key → PLAN_CONFLICT.

### T1.4 CC gate + fixture source

- **Modelo:** NORMAL
- **Archivos:** `MagicCandidateSource` interface; production impl returns `CC_MISSING_OWNER_GATE`; test fixture yields injected int64s.
- **Cambio:** production Allocate físico no INSERT sin CC. CONTRACT tests usan fixture source.
- **Authority:** D7.
- **Failure/retry:** CC missing = no INSERT, non-terminal for CONTRACT.
- **Tests:** production path error code; fixture path allocates.
- **DONE:** grep no hardcoded CC ranges.
- **Stop:** inventar rangos Forex → viola CC gate.

### T1.5 Apply stamp allocated

- **Modelo:** NORMAL
- **Archivos/símbolos:** `EffectiveConfig` / `durable_apply_selected_run_physical.go` `writeApplySelectedRunProperties`; validate requested vs allocated.
- **Cambio:** properties `strategy.magic_number=<allocated>`. Si TaskSpec magic presente y ≠ allocated → `CONTRACT_CONFLICT` pre-stamp.
- **Authority:** D8/D9. No cambiar D13 four-properties set salvo el valor de magic.
- **Failure/retry:** pre-stamp conflict terminal; Apply recovery existing KEEP.
- **Tests:** allocated written; mismatch requested fails before SQX.
- **DONE:** properties usan allocated; 888111 no se escribe en path F-04 salvo que estuviera uniquely allocated (prohibido).
- **Stop:** seguir leyendo ETCD hot-path F-04.

### T1.6 XML readback

- **Modelo:** NORMAL
- **Archivos:** parser de `<Variable name="MagicNumber">` (o nodo equivalente del exporter) sobre bytes `.sqx` de output.
- **Cambio:** extraer int64; comparar con allocated.
- **Authority:** Java `EchoForgeRobustRunExporter` node.
- **Failure/retry:** parse fail = mismatch path.
- **Tests:** fixture XML 11111 vs 888111 vs allocated; missing node fails closed.
- **DONE:** parser no asume requested.
- **Deps:** T1.5.

### T1.7 MQ5 readback

- **Modelo:** NORMAL
- **Archivos:** parser de `input … MagicNumber` en `.mq5` exportado.
- **Cambio:** igual T1.6 sobre mq5.
- **Authority:** SQX `SourceCode.generate`.
- **Tests:** mq5 con MagicNumber distinto falla.
- **DONE:** ambos readbacks en el pipeline.
- **Deps:** T1.5. Paralelo T1.6.

### T1.8 mismatch FAIL CLOSED

- **Modelo:** NORMAL
- **Archivos:** orquestación seal/handoff gate.
- **Cambio:** si XML≠allocated OR mq5≠allocated: no compile-as-seal-input, no StrategyVersion, no manifest.
- **Authority:** SPEC stamp contract.
- **Failure/retry:** terminal `CONTRACT_CONFLICT`.
- **Tests:** requested==allocated pero XML 11111 → no seal.
- **DONE:** test de no-seal en mismatch.
- **Deps:** T1.6+T1.7.

### T1.9 compile byte verify

- **Modelo:** NORMAL
- **Archivos:** `artifact_compiler.go` evaluateCompileArtifacts (reuse, no Slot Pool).
- **Cambio:** gate seal exige size/sha EX5, log 0 errors, source mq5 sha == exported mq5.
- **Authority:** existing compiler success gate.
- **Failure/retry:** compile fail retry técnico; digest mismatch terminal.
- **Tests:** missing ex5 / sha mismatch / nonzero errors → no seal.
- **DONE:** no seal without verified bytes.
- **Stop:** parsear EX5 magic.

### T1.10 StrategyVersion seal

- **Modelo:** NORMAL
- **Archivos:** store `sqx.strategy_versions`; `contracts.StrategyVersionRef(...)`.
- **Cambio:** persist write-once; effective_inputs via S0 `C()`/`H()`; no HashIdentity.
- **Authority:** S0 `evidence.go` StrategyVersionRef.
- **Failure/retry:** replay same digest OK; distinct → CONTRACT_CONFLICT.
- **Tests:** same inputs same ref; different exec sha different ref; HashIdentity of config ≠ effective_inputs_sha256.
- **DONE:** roundtrip Validate-equivalent identity.
- **Deps:** T1.2+T1.8+T1.9.

### T1.11 HandoffManifestV1 producer

- **Modelo:** NORMAL
- **Archivos:** producer construye `contracts.HandoffManifestV1`; `Validate(supported=[forge-echo-ingestion.v1])`.
- **Cambio:** MemberProof desde Finalist V2 (requested/observed == strategy instrument/TF; tested hashes == version). Rank/score no entran. Empty membership → 0 manifests.
- **Authority:** S0 promotion.go; F-02 membership.
- **Failure/retry:** Validate fail = no persist.
- **Tests:** G08 identity mismatch; G09 version digest; G11/G12 structural; G22 zero.
- **DONE:** `Validate` PASS on golden assembled from S0-compatible fields.
- **Deps:** T1.10. Stop: ranking-as-membership.

### T1.12 handoff write-once store

- **Modelo:** NORMAL
- **Archivos:** `sqx.handoff_manifests` adapter.
- **Cambio:** persist canonical body + payload_digest; DetectSealedConflict.
- **Authority:** S0 conflict.go.
- **Tests:** G06 converge; G07 409; G23/G24 as applicable at store layer.
- **DONE:** second persist same key different digest fails; same digest no-op.
- **Deps:** T1.11.

### T1.13 HandoffIngress + fakeconsumer

- **Modelo:** NORMAL
- **Archivos:** port + adapter wrapping `fakeconsumer.Consumer.Ingest`.
- **Cambio:** un manifest por llamada; ns `forge-live`. Cero HTTP inventado.
- **Authority:** S0 fakeconsumer.go.
- **Failure/retry:** CONTRACT statuses 201/200/409.
- **Tests:** Ingest G01-like body 201; replay 200; non-effects AssertNone.
- **DONE:** `fakeconsumer` tests del producer Forge verdes contra pin.
- **Stop:** URL Echo inventada.

### T1.14 delivery states

- **Modelo:** NORMAL
- **Archivos:** `sqx.handoff_deliveries`.
- **Cambio:** estados SPEC; timeout post-commit → `UNKNOWN_RECEIPT` sin re-POST.
- **Authority:** D13; G35.
- **Tests:** pre-commit retry increments attempts; post-commit unknown does not call Ingest twice with distinct side-effect simulation.
- **DONE:** matrix rows Echo unavailable / timeout pre / timeout post cubiertas.
- **Deps:** T1.13.

### T1.15 corpus G04–G10 G19–G25 G22

- **Modelo:** NORMAL
- **Archivos:** tests que cargan testdata del módulo contracts pin (o copies via `go:embed` del módulo, no fork).
- **Cambio:** producer/consumer gates listados en SPEC CERTIFICATION CONTRACT.
- **Authority:** `testdata/v1/manifest.json` @ 91671f6f.
- **Tests:** G04 reuse version/magic; G05 new version; G06/G07; G08–G10; G19 id limits; G20 magic>int32; G21 wire number; G22 zero POST; G23/G24/G25 where producer emits wire.
- **DONE:** corpus subset PASS; G22 assert 0 Deliver calls.
- **Deps:** T1.11–T1.13.

### T1.16 concurrency allocation

- **Modelo:** NORMAL
- **Archivos:** tests allocator (pgtestdb o control_plane_integration pattern).
- **Cambio:** none production beyond T1.3.
- **Authority:** D5.
- **Tests:** parallel Allocate distinct refs unique magics; same ref converges; crash/unknown via unique constraint.
- **DONE:** race detector on allocator tests.
- **Deps:** T1.3.

### T1.17 BWC brownfield

- **Modelo:** NORMAL
- **Archivos:** tests migration + allocator.
- **Cambio:** none backfill.
- **Authority:** BWC SPEC.
- **Tests:** existing strategy without magic row; Allocate does not write 888111; Apply legacy path still compiles (no-touch unless F-04 path selected).
- **DONE:** no UPDATE of historical config_snapshot magics.
- **Deps:** T1.2+T1.3.

### T1.18 SOURCE greps

- **Modelo:** NORMAL
- **Archivos:** tests/scripts de certificación.
- **Cambio:** none functional.
- **Authority:** SOURCE gates.
- **Tests:** grep F-04 path: no ListObjects-as-authority; no Echo SQL; no TopProjection as membership; no HashIdentity in allocation_ref/version_ref/payload_digest helpers.
- **DONE:** SOURCE scoped PASS.
- **Deps:** T1.3+T1.8+T1.10+T1.13.

### T2.1 compile Evaluation binding

- **Modelo:** NORMAL
- **Archivos:** create `sqx/adapters/mt5-compile/binding/{contract,evidence,subject}.go`
- **Cambio:** constantes y `BuildEvidence`/`BuildStrategySubject`/`BuildEvaluationRef` exactos de D16. `CanonicalStageKey("mt5_compiler","mt5-compile.v1")`. No tocar `adapters/mt5/binding`.
- **Authority:** D16; `domain.NewEvaluationRef`.
- **Failure/retry:** Validate() fail = no persist.
- **Tests:** same inputs same ref; subject ignores artifact SHA; scope excludes host/temporal.
- **DONE:** `go test` del paquete binding; StageKey exacto.
- **Stop:** inventar identity hash distinto de `NewEvaluationRef`.

### T2.2 mt5_compile_persist_v1

- **Modelo:** NORMAL
- **Archivos:** create `sqx/activities/worker/mt5_compile_persist_activity.go`; register `sqx/cmd/sqx-worker/main.go`
- **Cambio:** FetchDurable MQ5/EX5/log; `VerifyCompiledArtifactForSeal` **antes** de ResolveStageExecution; Resolve → PutEvaluation → CompleteStageExecution(`[one]`). Queue padre, no `sqx-mt5-queue`.
- **Authority:** D16; analog `MT5ReconcileActivity.Execute` + Apply persist.
- **Failure/retry:** functional fail no llama persist (T2.3). Infra/UNKNOWN_COMMIT retryable. CONTRACT_CONFLICT non-retryable.
- **Tests:** success seals one ref; missing EX5/0-errors no abre StageExecution; replay ACK; distinct payload conflict.
- **DONE:** activity registrada en sqx-worker; tests verdes `-race`.
- **Stop:** persistir Evaluation desde SHA de EX5 o workflow ID.

### T2.3 wire executeMT5ArtifactTask

- **Modelo:** NORMAL
- **Archivos:** `sqx/workflows/generic_workflow.go` `executeMT5ArtifactTask`
- **Cambio:** si operation compile && PersistenceModelV1 && success, llamar persist (espejo `persistMT5ReconcileV1`). No persistir failed compiles. No asumir backtest después.
- **Authority:** D16 caller produce seam.
- **Tests:** workflow test V1 success invokes persist; failed compile does not; legacy model does not.
- **DONE:** grep único caller productivo del persist.
- **Deps:** T2.2.

### T2.4 carrier CompileEvaluationRef

- **Modelo:** NORMAL
- **Archivos:** `sqx/core/runtime/config.go` `StrategyArtifact`; update en `executeMT5ArtifactTask` post-persist
- **Cambio:** campo omitempty `CompileEvaluationRef`. No pisar `EvaluationRef` (source/Apply).
- **Authority:** D16; carrier comment "exact upstream Evaluation".
- **Tests:** apply eval preserved; compile ref set only on persist success.
- **DONE:** JSON roundtrip carrier.
- **Deps:** T2.3.

### T2.5 recovery / UNKNOWN_COMMIT / cardinality

- **Modelo:** NORMAL
- **Archivos:** tests persist + control_plane pattern
- **Cambio:** none production beyond T2.2 recoverCompleted analog.
- **Tests:** LoadEvaluation exact after lost ACK; Complete replay same set; second distinct ref CONTRACT_CONFLICT; len!=1 fail-closed; Temporal attempt/run ID no cambia ref.
- **DONE:** `-race` en persist tests.
- **Deps:** T2.2.

### T2.6 UseDurableMagicAllocation caller

- **Modelo:** NORMAL
- **Archivos:** `sqx/workflows/durable_apply_selected_run_workflow.go`
- **Cambio:** set `UseDurableMagicAllocation: true` en el request productivo F-04. No rediseñar Magic V1.
- **Authority:** existing flag in `DurableApplySelectedRunRequest`.
- **Tests:** request flag true; mismatch requested≠allocated still fail-closed.
- **DONE:** grep productivo del flag = 1 caller no-test.
- **Stop:** dejar el flag false y sellar igual.

### T2.7 seal assembler

- **Modelo:** NORMAL
- **Archivos:** create `sqx/activities/worker/forge_seal_handoff.go` (seal path)
- **Cambio:** exact Apply+Compile evals; fetch SQX/MQ5/EX5/log; `VerifyMagicReadback` + `VerifyCompiledArtifactForSeal`; `SealStrategyVersion`. Sin compile eval o Apply stage mismatch → no seal.
- **Authority:** existing `capabilities/strategy_version.go`; S0 recipe.
- **Tests:** mismatch magic no seal; compile leftover failed no seal; same inputs same version ref.
- **DONE:** seal write-once tests.
- **Deps:** T2.3+T2.6.

### T2.8 handoff assembler after Finalist V2

- **Modelo:** NORMAL
- **Archivos:** `forge_seal_handoff.go` + `generic_workflow.go` `runFinalistPromotion`
- **Cambio:** tras Decision V2, por member `BuildHandoffManifest` con `CompileEvaluationRef=string(eval.Ref)` real; persist+`DeliverHandoff`. G22 cero members → 0 POST. Si el flow no tiene compile eval exacta, fail-closed para F-04 members.
- **Authority:** `BuildHandoffManifest`; F-02 membership.
- **Tests:** G22; non-member skip; missing compile eval no inventa ref.
- **DONE:** producer llamado desde no-test.
- **Deps:** T2.7.

### T2.9 Echo HTTP HandoffIngress

- **Modelo:** NORMAL
- **Archivos:** create `sqx/adapters/echo-handoff/http_ingress.go`
- **Cambio:** POST `/api/v1/forge/promotions` + GET by-key. Misma firma `HandoffIngress`. No fork S0. No escribir DB Echo.
- **Authority:** E-04 SPEC v1.0.2 @ consumer `a99f9a6`.
- **Tests:** CONTRACT sigue fakeconsumer; HTTP client tests no cuentan como CROSS_LANE GOLDEN.
- **DONE:** adapter implementa el port; fakeconsumer intacto.
- **Stop:** URL/path inventado distinto de E-04.

### T2.10 auth/config

- **Modelo:** NORMAL
- **Archivos:** config/ETCD del HTTP ingress según contrato E-04 auth
- **Cambio:** wiring de credenciales/base URL. Fail-closed si ausente. No secret en repo.
- **Authority:** E-04 ingest auth.
- **Tests:** missing auth no POST.
- **DONE:** no secret en repo.
- **Deps:** T2.9.

### C4.1 retire CanonicalStrategyID parser

- **Modelo:** NORMAL
- **Archivos/símbolos:** `sqx/core/domain/magic_v1.go` delete or unexport `ParseMagicV1AllocationIdentity`; add `MagicV1DirectionFromStrategy(string) (MagicV1Direction, error)` mapping `L|LONG→1`, `S|SHORT→2`, `B|BOTH→3`, else fail closed; `MagicV1DirectionCode` debe delegar o unificarse. Tests `magic_v1_test.go`.
- **Cambio:** CanonicalStrategyID opaco F-01 no se parsea. Keep Encode/Decode/Validate `YYMMIIIDSSS`.
- **Authority:** D17; F-01 CLOSED.
- **Failure/retry:** unknown token → `ErrInvalidMagicNumber`, no default LONG.
- **Tests:** opaque id is not parsed; L/S/B and LONG/SHORT/BOTH; unknown fail closed.
- **DONE:** production path has zero `ParseMagicV1AllocationIdentity`.
- **Stop:** make CanonicalStrategyID parseable or change F-01 format → PLAN_CONFLICT.

### C4.2 AllocateMagicV1 loads strategies row

- **Modelo:** NORMAL
- **Archivos:** `sqx/adapters/registry-postgres/magic_v1.go` `AllocateMagicV1`; SQL `SELECT canonical_strategy_id, instrument, direction FROM sqx.strategies WHERE id = $1`. Do **not** extend `StrategyIdentityView` (F-01 identity stays Ref+CanonicalStrategyID).
- **Cambio:** missing row / empty instrument|direction / canonical argument ≠ row → `ErrContractConflict` or `ErrInvalidArguments`. `InstrumentCode` exact catalog. Then existing `allocateMagicV1`.
- **Authority:** D17; `AdoptStrategy` producer.
- **Tests:** f04Strategy helper must persist the instrument/direction under test (today it always inserts XAUUSD/L — fix that). Opaque canonical + XAUUSD/L → 001/D=1. EURUSD row → code 003. Unknown instrument → `ErrInstrumentCodeMissing`. GOLD/xauusd alias → fail closed.
- **DONE:** public `AllocateMagicV1` never splits CanonicalStrategyID on `_`.
- **Deps:** C4.1.

### C4.3 replay/conflict without new migration

- **Modelo:** NORMAL
- **Archivos:** `AllocateMagicV1` replay path **before** returning `LoadMagicAllocation` hit and after identity-race reread. `DecodeMagicV1(existing.Magic)` vs current catalog code + direction digit.
- **Cambio:** mismatch III or D → `ErrContractConflict`, no `Next`, no UPDATE. Canonical mismatch → same error. Month-boundary replay still returns prior magic without incrementing October counter.
- **Authority:** D17; schema 015 `magic_decimal` + 016 catalog immutability.
- **Tests:** same ref replay no sequence increment; instrument change conflict; direction change conflict; UNKNOWN_COMMIT matrix untouched in `AllocateMagic`.
- **DONE:** no migration 017; 015/016 files byte-untouched.
- **Stop:** adding columns to `strategy_magic` is forbidden; 015 is sufficient.
- **Deps:** C4.2.

### C4.4 requested vs legacy vs allocated

- **Modelo:** NORMAL
- **Archivos:** `sqx/adapters/apply-selected-run/binding/contract.go` `AllocatedEffectiveConfig`; tests `contract_test.go`; `sqx/activities/worker/durable_apply_selected_run_magic_test.go` (today asserts 888111 mismatch is conflict — invert for F-04 path).
- **Cambio:** TaskSpec `MagicNumber` is never requested on F-04. Always stamp allocated. nil, `888111`, `11111`, or any other TaskSpec value does not fail the allocation stamp. Legacy `EffectiveConfig` unchanged and still requires MagicNumber. `ValidateWorkflowSpec` magic_number required stays (BWC); do not invent `requested_magic`.
- **Authority:** D9 C4-corrected.
- **Tests:** allocated proceeds with TaskSpec 888111; reserved never written as allocated; SQX/MQ5 readback still vs allocated.
- **DONE:** grep F-04 path: no `requested != allocated` against TaskSpec.MagicNumber.
- **Deps:** none (parallel C4.1).
- **Stop:** treat template XML MagicNumber or filename as requested → PLAN_CONFLICT.

### C4.5 C4 tests including cohort N

- **Modelo:** NORMAL
- **Archivos:** `magic_v1_test.go` domain+postgres; replace `f04V1Canonical("XAUUSD", 'L', ...)` as identity authority with opaque ids plus explicit strategy.instrument/direction.
- **Cambio:** cover the SPEC C4 gates: opaque ID; instrument/direction; replay; conflict; concurrency `-race`; cohort N distinct refs; shared `(YYMM,instrument)` counter; direction does not partition; Apply/readback regression still exact.
- **Authority:** SPEC C4 gates.
- **DONE:** `go test -race` on `./sqx/core/domain` `./sqx/adapters/registry-postgres` `./sqx/adapters/apply-selected-run/binding` plus worker magic tests green for new cases; pre-existing 4 registry-postgres failures remain the documented baseline set.
- **Deps:** C4.1–C4.4.

### C4.6 SOURCE grep C4

- **Modelo:** NORMAL
- **Cambio:** grep F-04 allocation path: no `ParseMagicV1AllocationIdentity`; no Split CanonicalStrategyID for L/S; no latest; no MAX+1; no hostname; no Echo SQL; no selection=1 architecture limit.
- **DONE:** SOURCE PASS documented.
- **Deps:** C4.5.

### C5.1 LoadStrategyManifestIdentity

- **Modelo:** NORMAL
- **Archivos/símbolos:** nueva capability `StrategyManifestIdentityReader.LoadStrategyManifestIdentity(ctx, StrategyRef)` en `sqx/core/capabilities`; impl `sqx/adapters/registry-postgres` `SELECT canonical_strategy_id, instrument, direction, timeframe FROM sqx.strategies WHERE id = $1`. **No** extender `StrategyIdentityView`.
- **Cambio:** missing row → not found / `ErrInvalidArguments`; empty instrument|direction|timeframe → `ErrContractConflict`; canonical row ≠ member carrier → `ErrContractConflict`. TrimSpace only.
- **Authority:** D18; same row as C4 `magicV1StrategySemantics` plus timeframe.
- **Failure/retry:** fail closed non-retryable; no manifest.
- **Tests:** opaque canonical + explicit row XAUUSD/L/H1 loads those values; missing row fails; empty timeframe fails.
- **DONE @ `b57bfb2`:** public handoff path never splits CanonicalStrategyID; SQL reader and sqlmock fail-closed tests pass with `-race`.
- **Stop:** new column/migration → PLAN_CONFLICT. Extending StrategyIdentityView → PLAN_CONFLICT.

### C5.2 OperationSide from durable direction

- **Modelo:** NORMAL
- **Archivos:** `sqx/activities/worker/forge_seal_handoff.go` delete `strategyIdentityFromCanonicalID`; type-assert the new reader; map via `MagicV1DirectionFromStrategy` then 1→`contracts.SideLong`, 2→`contracts.SideShort`, 3→ conflict. Never default LONG.
- **Cambio:** BOTH/unknown fail closed before `BuildHandoffManifest`.
- **Authority:** D18; S0 `OperationSide` @ `91671f6f`.
- **Tests:** L and LONG → LONG; S and SHORT → SHORT; B and BOTH → no manifest/no POST; empty/X → conflict.
- **DONE @ `b57bfb2`:** grep `strategyIdentityFromCanonicalID` = 0; focused LONG/SHORT/BOTH/unknown tests pass with no-effects assertions.
- **Deps:** C5.1.
- **Stop:** map BOTH to LONG/SHORT or change Echo → PLAN_CONFLICT.

### C5.3 requested/observed + spec gate

- **Modelo:** NORMAL
- **Archivos:** `forge_seal_handoff.go`; `sqx/workflows/generic_workflow.go` `runForgeSealHandoff` pass `spec.Direction` as `RequestedDirection` (gate only).
- **Cambio:** wire requested/observed/strategy identity = durable row values after TrimSpace. Request fields must equal the row exactly (no EqualFold). Empty spec fields fail closed.
- **Authority:** S0 G11/G12 exact equality; D18.
- **Tests:** spec XAUUSD/H1/L + row EURUSD/M15/S → conflict; matching spec emits row values on all three surfaces; decoy canonical does not change observed.
- **DONE @ `b57bfb2`:** G11/G12 still enforced by `manifest.Validate`; producer does not hide drift; exact case-sensitive gate and `RequestedDirection` are tested.
- **Deps:** C5.2.

### C5.4 retire ParseMagicV1AllocationIdentity

- **Modelo:** NORMAL
- **Archivos:** `sqx/core/domain/magic_v1.go` delete `ParseMagicV1AllocationIdentity` and `isInstrumentShapedToken`; update tests that still call them.
- **Cambio:** zero remaining consumers including handoff.
- **Authority:** D17 leftover + D18.
- **DONE @ `b57bfb2`:** `rg ParseMagicV1AllocationIdentity` = 0 in `sqx/`; parser/helper and direct residuals removed.
- **Deps:** C5.2.
- **Stop:** keep the parser “just in case” → PLAN_CONFLICT.

### C5.5 C5 tests

- **Modelo:** NORMAL
- **Archivos:** `forge_seal_handoff_test.go` (replace `sealTestCanonicalID = "XAUUSD_L_H1_..."` with opaque F-01-shape id + durable row fixture); registry-postgres identity reader tests; keep G22 assembler tests.
- **Cambio:** cover SPEC C5 gates. `go test -race` on `./sqx/activities/worker` focused C5 + `./sqx/core/forge` + `./sqx/adapters/registry-postgres` new cases. Pre-existing red sets must stay identical to `bba833d`.
- **Authority:** SPEC C5 gates.
- **DONE @ `b57bfb2`:** opaque success; decoy override fails; LONG/SHORT/BOTH/unknown; missing/incomplete row; canonical mismatch; exact instrument/timeframe/direction gates; Encode() body; G22/G24 intact, all focused with `-race`.
- **Deps:** C5.1–C5.4.

### C5.6 SOURCE grep C5

- **Modelo:** NORMAL
- **Cambio:** grep F-04 handoff/seal path: no `strategyIdentityFromCanonicalID`; no `ParseMagicV1AllocationIdentity`; no `strings.Split` of CanonicalStrategyID for instrument/direction/timeframe; no latest; no Echo SQL writes.
- **DONE @ `b57bfb2`:** SOURCE PASS documented; parser references and semantic canonical parsing/equalfold are absent from `sqx/`/handoff path.
- **Deps:** C5.5.

### T2.11 authentic golden capture

- **Modelo:** NORMAL
- **Cambio:** exportar preimages reales (Decision V2, StrategyVersion, allocation, MQ5/EX5/log, manifest bytes+digest) versionados. No corpus S0. No builder sintético.
- **DONE:** registro golden con hashes; `FORGE_GOLDEN_FIXTURE_PENDING=NO` sólo con bytes reales.
- **Deps:** C5 + T2.8. PHYSICAL may gate this.

### T2.12 PHYSICAL

- **Modelo:** NORMAL (one-shot physical **después** de C4, no esta sesión)
- **Cambio:** none architecture. Host: sqcli licencia válida + MetaEditor64 `/portable` + PG/Mongo/object store. Candidato mínimo XAUUSD dirección única, promotion 2.0.0, robust selection=1 (cert only). License expired → STOP owner. No viewers-as-workers.
- **DONE:** evidencia física de allocation V1 + stamp+compile+persist EvaluationRef + seal/handoff. Sin host: `PHYSICAL: BLOCKED — entorno`, no fingir PASS.
- **Deps:** C5.1–C5.6 + T2.3.

### T2.13 cross-lane T21/AC-37

- **Modelo:** NORMAL (one-shot **separado** Echo E-04 runtime/deploy/join, después del golden Forge)
- **Cambio:** POST golden auténtico a Echo `a99f9a6` → INGESTED → GET by-key. Cero activation. No modificar Echo source en C4 ni en el NORMAL C4.
- **DONE:** AC-37 PASS o explícito pending si PHYSICAL blocked o E-04 runtime ausente.
- **Deps:** T2.9+T2.11 + E-04 runtime config/deploy.

## 📆 Bitácora

- **2026-09-13 (NORMAL — T2.12/T2.11 one-shot).** Baseline remoto PASS en `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`; dirty extranjero preservado. Focos C4/C5 `-race`, build y vet PASS; grep de parsers = 0. Release canónico por `release-authority` AUTO → `0.2.98` → manifest publicado en MinIO, con hashes/tamaños de seis artefactos coincidentes y `vcs.revision` exacta. `ROLLOUT INCONCLUSIVE` por ausencia de capability MCP SSH/runtime y prohibición vigente de SSH directo; no se ejecutó candidato ni se creó golden. T2.12/T2.11/T2.13 permanecen OPEN. SESSION CLOSE + FEEDBACK realizados.

- **2026-09-12 (NORMAL F-04 C5.1–C5.6, implementación y evidencia).** Baseline remoto verificado `origin/feature/f04-magic-version-handoff == bba833d7b57c767d6ce5ebfeae7a7b71b5785782`; worktree aislado `symphony-f04-c4` CLEAN y detached sobre ese commit; dirty externo en checkout principal (`specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json`), worktree `symphony-f04-t2` (`deploy/manifest.json`, `input/example/config.json`, misma fixture) y worktree `symphony-aranea-mcp-runbooks` registrados y preservados sin tocar. Commit separado `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`, parent `bba833d7b57c767d6ce5ebfeae7a7b71b5785782`, push fast-forward a `feature/f04-magic-version-handoff`. Paths source: `sqx/core/capabilities/strategy_manifest_identity.go`, `sqx/adapters/registry-postgres/strategy_manifest_identity.go`, `sqx/adapters/registry-postgres/strategy_manifest_identity_test.go`, `sqx/activities/worker/forge_seal_handoff.go`, `sqx/activities/worker/forge_seal_handoff_test.go`, `sqx/workflows/generic_workflow.go`, `sqx/core/domain/magic_v1.go`. Reader dedicado usa `SELECT canonical_strategy_id, instrument, direction, timeframe FROM sqx.strategies WHERE id = $1`; fila durable por StrategyRef es authority, carrier canonical sólo consistencia exacta, sin extender `StrategyIdentityView`. `L|LONG→contracts.SideLong`, `S|SHORT→contracts.SideShort`, `B|BOTH|empty|unknown→CONTRACT_CONFLICT` fail-closed antes de Validate/Encode/Persist/Deliver; `manifest.Encode()` byte-exact preservado. Requested instrument/timeframe/direction se transportan desde WorkflowSpec como gates TrimSpace exactos case-sensitive; manifest requested/observed instrument/timeframe salen de la fila durable. Parser `strategyIdentityFromCanonicalID`, `ParseMagicV1AllocationIdentity` e `isInstrumentShapedToken` eliminados; `rg 'strategyIdentityFromCanonicalID|ParseMagicV1AllocationIdentity' sqx/` = 0; scan sin EqualFold/Split semántico en el handoff. Tests: `go test -count=1 -race ./sqx/core/domain ./sqx/core/forge ./sqx/core/capabilities` PASS; `go test -count=1 -race ./sqx/activities/worker -run '^TestForgeSealHandoff_'` PASS; reader focalizado `registry-postgres` PASS; build-only/vet de paquetes tocados PASS. Worker full reproduce exactamente 16 fallas baseline; registry full HEAD timeout 10m en embedded-postgres y el subconjunto histórico mostró sólo 2 de las 4 fallas históricas, sin nuevas fallas C5. G22 empty membership, G24 source-binding conflict y canonical body encoding cubiertos/intactos. `MIGRATION: NONE`; 015/016 no-touch; 017 ausente. T2.11/T2.12/T2.13 OPEN; F-04 overall NOT CLOSED; no release/deploy/physical/Echo.

- **2026-09-12 (TOP F-04 C5 MANIFEST IDENTITY CONTRACT CLOSED).** Manager review post-C4: `forge_seal_handoff.go` todavía parsea CanonicalStrategyID (`strategyIdentityFromCanonicalID` → `ParseMagicV1AllocationIdentity` + Split timeframe). C4.1–C4.6 permanecen CLOSED @ `bba833d`. D18: instrument/timeframe/direction del manifiesto = `sqx.strategies` por StrategyRef; S0 OperationSide LONG/SHORT; BOTH fail closed sin cambiar Echo y sin mapear a LONG/SHORT; requested/observed = misma fila; WorkflowSpec gate exacto (no EqualFold); no readback SQX/MQ5 de instrument/TF; StrategyIdentityView no se extiende; `MIGRATION: NONE`. Tareas C5.1–C5.6 To Do. T2.11–T2.13 OPEN. F-04 no physical-ready. Veredicto `READY FOR NORMAL — F-04 MANIFEST IDENTITY CONTRACT CLOSED`. SESSION CLOSE esta sesión.
- **2026-09-12 (NORMAL C4.1–C4.6, implementación).** Baseline verificado: `origin/feature/f04-magic-version-handoff` = `d645ed6` exacto (baseline frozen pre-C4; branch local `9fad768` simplemente behind, sin commits post-baseline en ningún lado); dirty foráneo documentado (`phase4_performance.json` en checkout principal; `deploy/manifest.json`+`input/example/config.json` en worktree físico `symphony-f04-t2`) preservado sin tocar; worktree aislado nuevo `symphony-f04-c4` detached @ `d645ed6` CLEAN. Implementado (commit único `bba833d7b57c767d6ce5ebfeae7a7b71b5785782`, pushed fast-forward `d645ed6..bba833d`): (C4.1) `domain/magic_v1.go` — `MagicV1DirectionFromStrategy` (TrimSpace+ToUpper; L|LONG→1, S|SHORT→2, B|BOTH→3; resto fail closed `ErrInvalidMagicNumber`, nunca default LONG), `MagicV1DirectionCode` delega al mapper (un solo vocabulario); `ParseMagicV1AllocationIdentity` retirado del allocation path con doc de residual. (C4.2) `registry-postgres/magic_v1.go` — `AllocateMagicV1` nuevo step 0 `SELECT canonical_strategy_id, instrument, direction FROM sqx.strategies WHERE id = $1`: missing row → `ErrInvalidArguments`; instrument vacío → `ErrContractConflict`; canonical row ≠ argumento → `ErrContractConflict`; direction → mapper fail closed; instrument → `InstrumentCode` catálogo exacto TrimSpace-only (alias/lowercase no se reparan → `ErrInstrumentCodeMissing`); `magicV1CandidateSource` lleva code pre-resuelto; entry unexported `allocateMagicV1` eliminada. (C4.3) replay/conflict gate post-`AllocateMagic` cubre replay-first, identity-race y UNKNOWN_COMMIT reconciliation: `DecodeMagicV1(record.Magic)` vs code+direction corrientes y `record.CanonicalStrategyID` vs argumento → `ErrContractConflict` terminal (no Next, no UPDATE); C1 UNKNOWN_COMMIT/identity-race/(ns,magic)-collision intactos. (C4.4) `binding/contract.go` `AllocatedEffectiveConfig` — eliminado el gate `requested != allocated`; TaskSpec magic (nil, 888111, 11111, cualquiera) se sobrescribe con allocated; legacy `EffectiveConfig` byte-exact intacto; `ValidateWorkflowSpec` sin cambios. Tests (C4.5): fixtures `f04Strategy(instrument, direction)` explicitan la fila; `f04V1Canonical` retirado como authority (ids opacos F-01-shape `<token>_<hash>`); decoy test `XAUUSD_L_H1_decoy` + fila EURUSD/S → magic `26090032001` (la fila gana sobre el string); replay sin incremento; month-boundary conserva magic; instrument drift y direction drift → `ErrContractConflict` sin reasignar ni consumir ordinal; missing row/canonical drift/direction X o vacía/instrument vacío fail closed sin filas ni contadores; cohort N=5 multi-instrumento multi-dirección → 5 magics distintos, contador compartido `(YYMM,instrument)`, direcciones no particionan; concurrentes 3 direcciones → secuencias {1,2,3} y 8 workers únicos (`-race`); worker: TaskSpec 888111/11111/42/nil → stamp allocated; reserved nunca asignado. **Comandos y resultados:** `go build ./sqx/{core,adapters,activities,workflows,cmd}/...` + `go vet` (4 paquetes) OK; `go test -count=1 -race ./sqx/core/domain ./sqx/adapters/apply-selected-run/binding` PASS (1.2s); `go test -count=1 -race -run TestMagicV1 ./sqx/adapters/registry-postgres` PASS (448s); `go test -count=1 -race -run 'TestAllocatedEffectiveConfig|TestResolveEffectiveConfig' ./sqx/activities/worker` PASS; paquete completo registry-postgres: 4 fallos = set histórico documentado; activities/worker: 16 fallos idénticos a baseline `d645ed6` (diff vacío); workflows: 21=21 idéntico (solo timing); gates `-race` F-04 (forge, echo-handoff, mt5-compile, capabilities, runtime, magic-readback, migrations) PASS. **C4.6 negative proof:** grep productivo `ParseMagicV1AllocationIdentity` → sólo definición domain + `forge_seal_handoff.go:544` (`strategyIdentityFromCanonicalID`, bloque de identidad del manifest, NO allocation); allocation path (registry magic_v1.go, magic_allocation.go, binding contract.go, durable_apply_selected_run.go) con cero referencias y cero Split semántico del canonical; sin latest/MAX+1/hostname/Echo-SQL/selection=1 en el path. **RESIDUAL FLAGGEADO para manager:** el parser sobrevive con ese único consumer no-allocation porque `forge_seal_handoff.go` está fuera del scope C4 autorizado y su corrección exige decisiones no frozen (fuente de observed timeframe/side del manifest); con ID F-01 opaco el seal falla cerrado (fail-closed, sin datos falsos), no corrompe. MIGRATION: NONE — 015/016 byte-untouched, 017 inexistente. F-01/F-02/F-03/Echo/adaptive/mt5-binding untouched. Sin rollout, sin release, sin deploy, sin physical, sin golden, sin merge a master. Veredicto: **READY FOR MANAGER REVIEW — F-04 C4 IMPLEMENTED**; siguiente acción: manager source review of C4 implementation.
- **2026-09-12 (TOP F-04 C4 CONTRACT CLOSED).** Inspección dirigida `d645ed6` + F-01 `0509342` + Magic V1 `ea8be76`. Root cause: `ParseMagicV1AllocationIdentity` + `AllocateMagicV1` parsean CanonicalStrategyID; F-01 ID es opaco; `sqx.strategies.instrument/direction` ya son durables (AdoptStrategy ← WorkflowSpec). D9 corregido: TaskSpec `magic_number` es stamp legado, no requested. Replay conflict via DecodeMagicV1 sin migration nueva. Multi-strategy soportado; robust selection=1 sólo receta de cert. E-04 T2.13 registrado como one-shot separado. Veredicto `READY FOR NORMAL — F-04 C4 CONTRACT CLOSED`. SESSION CLOSE esta sesión.
- **2026-09-12 (TOP F-04 C4 — sesión abierta).** One-shot independiente TOP CONTRACT/PLANNING. Alcance: resolver el defecto físico `ParseMagicV1AllocationIdentity` vs CanonicalStrategyID opaco F-01; congelar autoridades explícitas de instrument/direction/requested vs allocated; NO implementar source, NO deploy, NO physical, NO merge, NO tocar Echo. Baseline inspeccionado: Symphony `d645ed6c2f438995d636a8213b1e4a3f5f26cbea`. T2.11/T2.12/T2.13 permanecen OPEN.
- **2026-09-12 (T2.12 vía deployment plane — rollout PASS, defecto de contrato Magic V1 ↔ F-01 → STOP — MANAGER REVIEW).** El manager rechazó el bloqueo previo "ARANEA MCP": Symphony ya posee deployment plane canónico y la autoridad de despliegue es el Stager, no se requiere capability operator en hosts. Ejecutado desde worktree exacto `d645ed6` (`symphony-f04-t2`, CLEAN): (1) **Release `0.2.97`** asignado por `release-authority` (AUTO, published `0.2.96` CONSISTENTE), publicado con `./deploy_release.sh --release-only "" 60` → build linux worker+watcher+windows `sqx-mt5-worker.exe` desde `d645ed6`, manifest confirmado en MinIO (`worker/sqx/manifest.json` v0.2.97); rollout Stager verificado por Host MCP read-only: zeus/hera/kronos `CURRENT=0.2.97` + `ACTIVATION.json phase=committed` (0.2.96→0.2.97 22:09–22:11Z), workers reiniciados y binario 0.2.97 contiene `mt5_compile_persist_v1`/`forge_seal_handoff_v1`; pollers Temporal vivos 3 en `sqx-main-queue` + 1 en `sqx-mt5-queue` (`19880@worker-kronos`); en mt5-kronos `C:\ProgramData\Stager` es ACL-bloqueado para echo-dev incluso vía perfil operator (no elevado) — evidencia Windows = `sqx-mt5-worker` (PID 19880) + `stager-runtime` vivos y poller activo post-publicación. **El bloqueo previo "deployment imposible vía Host MCP" quedó refutado.** (2) **Flujo XAUUSD F-04 real** vía mecanismo canónico input/watcher (`example_flow_80`, config corregido: promotion `2.0.0`, sin requested-magic legacy 888111 — el path durable con confirmación estricta requested==allocated lo hace fail-closed). FlowRun `eb2ebaa0-3056-445a-9d46-0953c25b2516`, workflow `sqx-main-v1-6c30394a` (Temporal `sqx-prop`): builder→retester (18 StageExecutions)→optimizer (12)→evaluate_wfm (12)→select_robust_run (4) todos COMPLETED con evidence inmutable insertada y 4 decisiones `OPTIMIZER_SELECTION/SELECTED/ENFORCE`. (3) **Fallo físico determinístico en durable apply (×4):** `ParseMagicV1AllocationIdentity` (`sqx/core/domain/magic_v1.go:183`, frozen T1) espera F-01 canonical id `<INSTRUMENT>_<D>_<timeframe>_...` pero el registro productivo F-01 emite `<43-char-key>_<43-char-hash>` (p.ej. `Z5h4dKXha7...LUQ_rjjX7Kcl...`, columnas separadas instrument/direction/timeframe sí existen) → `unknown direction token: invalid magic number` fail-closed ANTES de cualquier INSERT: 0 filas `strategy_magic`, contador mensual intacto (0), 0 sellos/manifests — estado limpio, sin bypass. Workflow cancelado por el agente (run propio, retry determinístico sin salida). **Sección 16: STOP — MANAGER REVIEW** — defecto de contrato entre dos piezas frozen (formato F-01 vs parser Magic V1); los tests CONTRACT pasaron porque los fixtures usaban el formato imaginado, gap de fixture no cubierto por el corpus. Hallazgos operativos adicionales: (a) el flujo ejemplo commitado NO es candidato F-04 (requested 888111 reservado → CONTRACT_CONFLICT pre-stamp; promotion 1.0.0 no encadena seal/handoff); (b) cohortes multi-estrategia son incompatibles con confirmación estricta requested==allocated (un solo requested constante por flow) → el run físico F-04 requiere cohorte de selección robusta = 1; (c) **E-04 sin operar en ambos lados**: sin ETCD `/sqx-worker/production/echo/ingest/*` (worker arranca fail-closed 0 POST) y sin ETCD `/echo/production/gateway/forge_ingest/*` (gateway desplegado además anterior a authority `a99f9a6`) → T2.13 requiere aprovisionamiento de config + despliegue Echo, fuera del alcance Symphony. SOURCE T2.1–T2.10 sigue PASS; T2.11/T2.12/T2.13 requieren resolución del manager.
- **2026-09-12 (T2.12 vía Host MCP — corrección de método y evidencia).** El manager rechazó el bloqueo por DNS/SSH directo y exigió usar las superficies MCP de Aranea. Verificación vía `mcp__aranea-ssh` (Host MCP): todos los hosts son alcanzables — (a) `mt5-kronos` (perfil operator): MetaEditor64 en `C:\MT5\Darwinex master3\MetaEditor64.exe`, worker físico `sqx-mt5-worker` corriendo (PID 42572, servicio elevado, path no legible sin admin), sin sqcli en el host (no requerido ahí: compile-only); (b) `sqx-zeus` (viewer): worker padre `symphony` corriendo como `kor` desde `/opt/stager/releases/0.2.96/bin/symphony` con log `/var/log/symphony/symphony-worker.log`, SQX instalado (`/home/kor/sqx/sqcli` ejecutable 0755 + `internal/license.db`); (c) `sqx-hera`/`sqx-kronos` (viewer): deployments watcher `/opt/symphony/current/bin` (sqx-watcher + symphony). **Bloqueo real = capability de ejecución:** los perfiles MCP de los hosts Linux son viewer read-only (`open-session`/`run-command` → POLICY_DENIED; `read-command` sólo allowlist ls/cat/grep/find/stat/df), por lo que NO es expresable vía MCP: desplegar el build F-04 `d645ed6` (el fleet corre 0.2.96, pre-F-04, sin allocation caller/compile persist/seal/handoff/HTTP ingress), reiniciar workers, ejecutar `sqcli` (stamp + verificación de licencia) ni operar el control plane (Temporal/PG/ETCD/MinIO, host no expuesto en perfiles MCP). En `mt5-kronos` hay operator, pero un compile aislado manual no produce evidencia durable contractual (StageExecution/EvaluationRef/StrategyVersion/manifest) y tocar el worker Windows sin el build F-04 sería cambiar el fleet sin autorización de deploy. Veredicto: **PHYSICAL: BLOCKED — ARANEA MCP** (condición "Host MCP no dispone de la capability necesaria para ejecutar los procesos requeridos"); SOURCE T2.1–T2.10 sigue PASS; sin bypass directo. Desbloqueo pedido al manager: perfil operator (o MCP de deploy/ejecución) para sqx-zeus + host del control plane, o autorización de deployment F-04 al fleet.
- **2026-09-12 (NORMAL T2.1–T2.10, implementación).** Baseline verificado (`9fad768` = origin feature; ancestros `ea8be76` y `origin/master 0b9742b` OK) y worktree aislado detached `symphony-f04-t2` CLEAN. Implementado: (1) `sqx/adapters/mt5-compile/binding` con StageKey `mt5_compiler@mt5-compile.v1`, subject/scope frozen (sin host/worker/Temporal/SHA), artifacts INPUT MQ5 / OUTPUT EX5 / EVIDENCE LOG, ref vía `domain.NewEvaluationRef`; (2) `mt5_compile_persist_v1` en sqx-worker — verificación `VerifyCompiledArtifactForSeal` ANTES de `ResolveStageExecution` (functional fail no abre slot), cardinalidad 1, recoverCompleted exacto, UNKNOWN_COMMIT retryable, conflict no-retryable; (3) wiring en `executeMT5ArtifactTask`: persist tras compile V1 success, carrier `StrategyArtifact.CompileEvaluationRef` sin pisar `EvaluationRef`; (4) `UseDurableMagicAllocation: true` en `runDurableApplySelectedRun`; (5) `forge_seal_handoff_v1`: Decision V2 → membership estructural → exact Apply/compile Evaluations → replay allocation → readbacks → seal write-once → `BuildHandoffManifest` → `DeliverHandoff` (G22: 0 members = 0 manifests/0 deliveries/0 POST; non-F-04 members skip; inputs sin membership = conflict); (6) `http_ingress.go` E-04 real (`@a99f9a6`): POST bytes exactos `manifest.Encode()` + GET by-key para outcome ambiguo (200 converge, 404 permite retry same key/body, lookup ambiguo → UNKNOWN_RECEIPT), receipt verificado contra autoridad; (7) config ETCD `echo/ingest/base_url` + `echo/ingest/bearer_token` sin defaults → `FailClosedIngress` 0 POST; (8) `runFinalistPromotion` retorna Decision y encadena seal/handoff sólo para V2. Commits atómicos `01dca16`→`870966b`→`898506f`→`d645ed6`, pushed fast-forward. Gates: `-race` verde en mt5-compile/echo-handoff/forge/capabilities/runtime/apply-binding/magic-readback + tests nuevos worker/workflows; fallos pre-existentes verificados IDÉNTICOS a baseline (workflows 21, activities/worker 16 — set exacto; registry-postgres 4 históricos); migrations 015/016 intactas y 017 inexistente; SOURCE greps sin latest/MAX+1/random/hostname/rank-membership/Echo-SQL/blind-repost/fakeconsumer-en-producción (HashIdentity sólo receta D16 evidence, no recetas S0). PHYSICAL: mt5-kronos DNS no resuelve (ping/ssh) y hosts Linux viewer → **BLOCKED — entorno**; sin host no hubo superficie SQX, no aplica license STOP. T2.11/T2.12/T2.13 abiertos (requieren físico/integración real). Foreign dirty `phase4_performance.json` preservado en el worktree original; el worktree de implementación quedó CLEAN.
- **2026-09-12 (TOP compile Evaluation authority).** Baseline verificado: HEAD `9fad768` merge de `ea8be76`+`0b9742b`; `origin/master` ancestro; feature ahead 9. Dirty foráneo `phase4_performance.json` preservado. Source prueba: compile físico produce EX5/log durables pero **cero** StageExecution/Evaluation; Apply y `mt5_reconcile_v1` sí sellan EvaluationRef. D16 frozen: `mt5_compiler@mt5-compile.v1` + `NewEvaluationRef`; persist en sqx-worker analog reconcile; MIGRATION 017 NO. Caller: `executeMT5ArtifactTask` produce, `runFinalistPromotion` consume. T2.1–T2.13 To Do. PHYSICAL operacionalmente pending. E-04 consumer READY `@ a99f9a6`. Veredicto TOP READY.
- **2026-09-12 (E-04 DEPENDENCY — FORGE GOLDEN FIXTURE).** Fetch completo y revisión de `master`/`origin/master` @ `0b9742b09019526a8119f086199d15d1f0d42cb1` y `feature/f04-magic-version-handoff`/`origin/feature/f04-magic-version-handoff` @ `ea8be76c4587b2d00e4cad8cf2a67c4fd8e6680f`; worktree limpio y `git diff --check` PASS. La feature no es descendiente del master actual (`merge-base --is-ancestor` devuelve 1), por lo que ambos pins quedan explícitos y no se mezclan.
- **2026-09-12 (producer audit).** `rg` sobre `sqx/core`, `sqx/adapters`, `sqx/activities` y `sqx/workflows` encontró `BuildHandoffManifest` únicamente en la definición productiva y cuatro llamadas de `handoff_producer_test.go`; no existe caller no-test que lo alimente desde Decision V2, StrategyVersion sellada, MagicAllocation persistida y artefactos verificados. `go test -count=1 -race ./sqx/core/forge ./sqx/adapters/echo-handoff` PASS sólo certifica el contrato sintético.
- **2026-09-12 (physical evidence audit).** El módulo S0 resuelto es `github.com/xKoRx/echo/v3/sdk/contracts@91671f6f46ff`; su corpus G04/G05/G12 contiene payloads de contrato, no preimages físicos de F-04. La feature no trackea `.mq5`, `.ex5` ni `compile.log`; su `testdata/v1` sólo contiene G06/G07/G20/G21/G22. En Zeus, Hera y Kronos, las búsquedas read-only no encontraron `handoff`, `StrategyVersion` o magic allocation; sólo aparecieron `.sqx` históricos y `.mq5` antiguos, sin `.ex5`/compile evidence del flujo F-04 actual.
- **2026-09-12 (decision).** No se copió S0, no se reutilizó corpus como golden, no se construyó payload a mano, no se calculó digest esperado y no se tocaron semántica F-04/Echo ni repos externos. Estado final: `BLOCKED / FORGE_GOLDEN_FIXTURE_PENDING`; Manager debe proporcionar o habilitar una ejecución F-04 real que produzca Decision V2 + StrategyVersion + allocation + readback/compile bytes y permita exportar todos los preimages referenciados.
- **2026-09-12 (F-04 correction audit).** Se verificó el seam único de `GenericSQXWorkflow`: la asignación durable no está activada en el request productivo y `ArtifactTaskResult` no persiste un `compile_evaluation_ref`; el resultado compile sólo transporta EX5, compile log y `SourceKey`. La corrección no se implementó porque no existe una autoridad durable simultánea para alimentar `BuildHandoffManifest` sin fabricar un ref o abrir una decisión arquitectónica. El sondeo read-only de `mt5-kronos` falló por resolución DNS; no se ejecutó SQX ni se declaró licencia. STOP — MANAGER REVIEW.
- **2026-09-11** — Join E-04: planning [[Echo — E-04 Forge Ingestion E1]] congela `POST /api/v1/forge/promotions` + GET by-key + envelope S0. F-04 CONTRACT `fakeconsumer` no se reabre. INTEGRATION real sigue esperando implementación E-04 **y** E-03 CONTRACT_PASS. No se inventa URL provisional distinta.
- **2026-09-10 (cierre NORMAL)** — Sello/readback/seal/handoff implementados: `sqx/adapters/magic-readback` (XML+MQ5 parsers fail-closed), `capabilities.VerifyMagicReadback`+`VerifyCompiledArtifactForSeal` (bytes reales, 0-errors), `domain` recetas S0 (EffectiveInputs/RuntimeContext/ExecutionManifest/DependenciesDigest vía `ExactInputRefsDigest`, StrategyVersionRef por recompute), store `SealStrategyVersion` write-once (replay/conflict), `core/forge` producer `BuildHandoffManifest` (Validate S0 PASS, membership estructural, G22 `HandoffMembersForDecision`), migration 015 con UNIQUE(decision_ref,version_ref) G24, stores handoff_manifests/handoff_deliveries, `capabilities.DeliverHandoff` (estados + UNKNOWN_RECEIPT sin re-POST + attempts), `adapters/echo-handoff` fakeconsumer CONTRACT (201/200/409/G24/non-effects/corpus G06-G07-G20-G21). Race verde en todos los paquetes F-04. Fixture de benchmark `specs/.../phase4_performance.json` lo reescriben tests ajenos — restaurado, worktree CLEAN.
- **2026-09-10 (sesión NORMAL)** — Branch `feature/f04-magic-version-handoff` (nombre del briefing; difiere del registrado arriba). T1.1–T1.4 committeados: pin S0 resuelto por SSH directo (`v0.0.0-20260910031519-91671f6f46ff`), migración 015 + runner + tests fresh/brownfield/down/restart, allocator CAS SELECT-then-INSERT con replay/colisión/reservados/exhaustión N=32, `GateMagicCandidateSource` = producción (`CC_MISSING_OWNER_GATE`), concurrencia same/distinct con `-race` verde. Nota: 4 tests pre-existentes fallan en baseline (`TestUpsertStrategyV2_V0V1V2Coexistence`, `TestControlPlane_AdoptStrategyV1ConcurrentFilenameVariantsConverge`, `TestRegisterStrategy_LegacyRollbackTargetsOnlyV0`, `TestControlPlane_AdoptStrategyV1UnexpectedUniqueFailsWithoutPoisonedRead`) — set idéntico en baseline y branch, sin regresión F-04. Delegación MiniMax bloqueada por plan limit; NORMAL ejecutó directo.
- **2026-09-11 (owner gate Magic V1, NORMAL)** — Sobre `1999da1`, commit `ea8be76`: codec `domain/magic_v1.go` (Encode/Decode/Validate, round-trip obligatorio, dirección L/S parseada estricta del canonical id, BOTH reservado D=3 sin inventar flow), migration `016_magic_number_v1_allocator` (`sqx.magic_instruments` con UNIQUE instrument/code + CHECK 001..999 + trigger inmutable; `sqx.magic_monthly_counters (period YYMM, instrument_code) → last_sequence` CHECK 0..999; seed XAUUSD=001 y AUDUSD/EURUSD/GBPUSD/NZDUSD/USDCAD/USDCHF/USDJPY=002..008 lexicográfico una vez), `ControlPlane.AllocateMagicV1` (upsert atómico initialize-or-increment RETURNING, guard <999 → `MAGIC_MONTHLY_CAPACITY_EXHAUSTED` sin wrap/reset, `INSTRUMENT_CODE_MISSING`, clock UTC determinista `cp.now`, replay-first reusa motor CAS/UNKNOWN_COMMIT), wiring productivo: `NewDurableApplySelectedRunActivity` deriva `MagicAllocatorV1` del control plane (gate fake sólo en tests). Correctivo: `assigned_at`/`sealed_at` truncados a µs → replay byte-equal (3 tests que fallaban por precisión en esta máquina quedan verdes; baseline queda en los 4 documentados). Tests: codec completo, concurrencia XAUUSD L/S/BOTH → {001,002,003} compartiendo contador, replay sin consumir ordinal y conservando magic septiembre en octubre, capacity #999 PASS/#1000 exhaust, catálogo exacto+inmutable+SILVER=009, PG fresh/brownfield 015→016/constraints/down/restart, todos `-race`. Físico: sondeo mt5-kronos vía SSH (MetaEditor64 en `C:\MT5\*`, worker desplegado; sin SQX/sqcli ni PG registry alcanzable; hosts Linux viewer) → PHYSICAL BLOCKED entorno, no se finge. Módulos privados Go resueltos por SSH (git insteadOf + GOPRIVATE). Fixture `phase4_performance.json` re-escrito por tests ajenos — restaurado, worktree CLEAN.
- **2026-09-10 (corrección G1, NORMAL)** — Correctivos sobre `24b807f`: `928d3db` (C1: UNKNOWN_COMMIT reconcilia solo vía SELECT durable — read failure preserva `ErrUnknownCommit` sin segundo Next/INSERT; identity race `pk_strategy_magic` converge solo leyendo al ganador, winner invisible falla cerrado `ErrContractConflict`; solo colisión `(ns,magic)` avanza candidate) y `1999da1` (C2: `canonicalBody` debe ser byte-equal a `manifest.Encode()` antes de todo efecto, sin JSONEq; C3: replay conflictivo preserva state/receipt/attempts, G24 sin delivery huérfana, guard atómico en `SaveHandoffDelivery` — INGESTED terminal, UNKNOWN_RECEIPT solo acepta re-park, sin state-machine nueva). Tests: 7 sqlmock fail-closed allocator, 2 contract (body gate + preservation con fakeconsumer), 5 PostgreSQL aislados migration 015 (INGESTED/UNKNOWN_RECEIPT/G24/replay idéntico/guard). Gates re-ejecutados: SOURCE 111 pass, CONTRACT+S0 corpus race verde, CONCURRENCY 26/26 `-race`, MIGRATION 5/5; sweep paquete completo = mismo set de 4 fallos pre-existentes baseline (verificado con/sin cambios, sin regresión). Migration 015 sin tocar. `PHYSICAL`/`INTEGRATION` unchanged. MiniMax delegación bloqueada (plan limit); ejecución directa.

## 🧭 Decisiones

Ver Decision register. D16 compile Evaluation **frozen**. D17 C4 allocation inputs **frozen**. D18 C5 manifest identity **frozen**. **C4.1–C4.6 CLOSED (`bba833d`). C5.1–C5.6 IMPLEMENTED @ `b57bfb2` — READY FOR MANAGER REVIEW;** T2.11–T2.13 siguen OPEN; F-04 no physical-ready/not closed.

### Acceptance gates T2

| Gate | Owner | Pass when |
|---|---|---|
| SOURCE | NORMAL | grep F-04: no latest, no SHA-as-EvaluationRef, no Echo SQL, no HashIdentity on S0 recipes, persist not on mt5-queue; C5: no CanonicalStrategyID business-token parser on handoff path |
| CONTRACT | NORMAL | compile Evaluation identity/replay/conflict; Complete cardinality 1; assembler sin eval no sella; G22; fakeconsumer intacto; C5 identity from durable row |
| CONCURRENCY | NORMAL | same StageExecution concurrent persist converges; distinct content CONTRACT_CONFLICT; `-race` |
| MIGRATION | NORMAL | 017 absent; 015/016 untouched |
| PHYSICAL | NORMAL | stamp+compile+persist EvaluationRef en host con sqcli+MetaEditor; license expired → STOP owner; sin host = BLOCKED entorno |
| INTEGRATION | NORMAL | POST golden auténtico → Echo INGESTED + GET by-key (T21/AC-37); no mock PASS |

## 🔗 Docs / Links

- [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]
- [[Echo Forge — Factory V2 Completion]]
- [[Echo — E-01 Canonical SDK Foundation S0]]
- [[Echo — Live Platform V1]]
- [[Echo Forge — F-02 Finalist Model V2 Contract]]
- [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]
- [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]

## 💡 Ideas

### Backlog de ideas

- Join INTEGRATION T2.9–T2.13 contra Echo `@ a99f9a6` cuando Manager autorice NORMAL.

### Motivos / principios

- Fail closed. Write-once. S0 pin único. CC no se inventa.

### Memoria pública / interna

- **Memoria pública:** esta nota + SPEC.
- **Memoria interna:** no duplicar el contrato.
- **Motivo:** Agents OS planner único.
