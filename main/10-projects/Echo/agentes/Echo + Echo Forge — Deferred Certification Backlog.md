---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[Echo Forge — Factory V2 Completion]]"
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[Echo — E-04 Forge Ingestion E1]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
aliases:
  - Echo certification backlog
  - F-04 deferred certification
tags:
  - kind/doc
  - area/echo
  - project/echo
created: "2026-09-13"
updated: "2026-09-17"
---

# Echo + Echo Forge — Deferred Certification Backlog

## Propósito

Mantener en un carril único, ordenado y no ejecutado las certificaciones físicas y cross-lane que quedaron fuera del critical path de desarrollo de Echo/Echo Forge.

## Contenido

### Decisión de gestión congelada

La certificación física/de infraestructura se retira temporalmente del critical path de desarrollo mientras se construye el Aranea MCP Access Plane; no se waiva. `IMPLEMENTED != CERTIFIED`. No se cambia ningún contrato frozen, no se inventa evidencia y no se marcan PASS T2.11, T2.12 ni T2.13.

### Taxonomía de estado

| Estado | Significado | Evidencia mínima |
|---|---|---|
| PLANNED | Trabajo definido, no ejecutado | alcance y dependencias |
| IMPLEMENTED | Código/configuración materialmente implementado | diff y tests del scope |
| SOURCE VERIFIED | Fuente y contratos verificados | revisión/gates source |
| RELEASED | Artefacto publicado desde SHA autorizado | manifest y digest |
| DEPLOYED | Runtime objetivo ejecuta el artefacto autorizado | deployment proof |
| PHYSICALLY CERTIFIED | Receta real ejecutada sobre runtime físico | evidencia durable end-to-end |
| CROSS-LANE CERTIFIED | Handoff real aceptado por el lane consumidor | receipt y read-back |
| CLOSED | Todos los estados requeridos por la fase están satisfechos | veredicto final y referencias |

Los estados son dimensiones de evidencia; `CLOSED` nunca se deriva de `IMPLEMENTED` o `RELEASED` por sí solos.

### Estado de entrada

F-04: `IMPLEMENTED` y `SOURCE VERIFIED` en product SHA `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`, release `0.2.98` publicada; rollout Linux PASS; Windows bloqueado por policy del viewer MCP. F-04 no está `PHYSICALLY CERTIFIED`, `CROSS-LANE CERTIFIED` ni `CLOSED`. E-04 está `INTEGRATED`, pero T21/AC-37 y `FINAL CLOSED` siguen pendientes. F-05 conserva su split implementación/certificación.

### Backlog ordenado; no ejecutar en esta sesión

#### CERT-F04-01 — Forge physical chain / T2.12

- **Prerequisite product SHA/release:** F-04 `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43` / `0.2.98`.
- **Prerequisite infrastructure:** Aranea Access Plane operacional y certificado para los targets de ejecución/observación y el control plane usado por el flujo.
- **Required MCP capabilities:** SSH viewer para identificar runtime; SSH operator/run-command en los hosts que ejecutan SQX/MT5; acceso scoped de observación/escritura al PG/Mongo/object-store del flujo; observación/control Temporal o capability equivalente autorizada; secretos permanecen fuera del agente.
- **Physical recipe:** desplegar y probar la release autorizada en los runtimes canónicos; ejecutar un flujo F-04 real con catálogo CC owner, compile MetaEditor/SQX, persistencia de EvaluationRef, readbacks, seal y handoff; no usar mocks como PASS.
- **Durable evidence:** release/deployment proofs, FlowRun/workflow IDs, Decision V2, allocation/readback, compile inputs/outputs/log, EvaluationRefs, StrategyVersion, HandoffManifest y delivery state.
- **PASS criteria:** el mismo SHA corre en los runtimes requeridos; el flujo real completa sin bypass; bytes, refs, allocation, seal y manifest son verificables y cardinality-safe. Hasta entonces: `PLANNED`/`BLOCKED BY INFRA`, no PASS.

#### CERT-F04-02 — Authentic Forge golden / T2.11

- **Prerequisite product SHA/release:** CERT-F04-01 PASS sobre `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43` / `0.2.98`.
- **Prerequisite infrastructure:** mismo access plane y almacenamiento durable/exportable para todos los preimages referenciados por el flujo.
- **Required MCP capabilities:** lectura de evidencia Forge, artefactos y metadatos del control plane; transferencia segura de los bytes auténticos; no capability sintética ni fixture manual.
- **Physical recipe:** capturar desde la ejecución física el golden Forge completo: producer F-04 auténtico, StrategyVersion sellada, artefactos compile/readback, EvaluationRefs y manifest; preservar hashes y provenance.
- **Durable evidence:** fixture/preimages byte-exactos, SHA256/size, refs, producer identity, release manifest y enlace al run físico.
- **PASS criteria:** todos los bytes que el manifest/reference declara existen y verifican; producer es `echo-forge-handoff`; corpus no es copia de S0 ni fakeconsumer. No ejecutar ni marcar PASS ahora.

#### CERT-E04-01 — Echo cross-lane golden / T21

- **Prerequisite product SHA/release:** golden auténtico CERT-F04-02 y Echo E-04 integrado en `a99f9a63354bbe72219d1e590bb93757ed08e45e` o release posterior explícitamente verificada.
- **Prerequisite infrastructure:** runtime Echo desplegado y observable; endpoint de promotions alcanzable desde el producer; PG/artifact store/read surface disponibles.
- **Required MCP capabilities:** observación del runtime Echo y HTTP; lectura scoped del resultado/receipt; acceso de evidencia PG/artifacts según el runbook; no admin secret reutilizado.
- **Physical recipe:** enviar el manifest auténtico por `POST /api/v1/forge/promotions`, verificar `INGESTED`, recuperar por GET by-key y repetir el lookup idempotente sin activar/provisionar/capitalizar.
- **Durable evidence:** request/body digest, HTTP status, receipt, mapping/version/promotion rows, artifact hashes y GET by-key outcome.
- **PASS criteria:** Echo acepta exactamente el golden auténtico, persiste una única proyección consistente, devuelve receipt/read-back estable y no produce efectos fuera de E-04. T21/AC-37 permanece OPEN hasta ejecutar esto.

#### CERT-F04-03 — Real Echo join / T2.13

- **Prerequisite product SHA/release:** CERT-F04-02 PASS, CERT-E04-01 PASS, Forge `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43` / `0.2.98` y Echo runtime del E-04 integrado.
- **Prerequisite infrastructure:** ambos runtimes observables/operables por el Access Plane, rutas Forge→Echo habilitadas y control plane con evidencia durable.
- **Required MCP capabilities:** capabilities CERT-F04-01 más observación HTTP/Echo y read-back de receipt/rows; ninguna sustitución por fakeconsumer.
- **Physical recipe:** repetir un run Forge real desde Finalist/StrategyVersion hasta `POST` real y `GET by-key` en Echo, conservando la cadena de identidad y hashes.
- **Durable evidence:** run IDs, release/deployment proofs, manifest/body digest, receipt `INGESTED`, read-backs y no-effects.
- **PASS criteria:** handoff real→receipt real→lookup real converge exactamente una vez y los artefactos se pueden inspeccionar. Hasta entonces, join `DEFERRED`.

#### CERT-F05-01 — Cohesive release/deployment proof

- **Prerequisite product SHA/release:** F-01/F-02/F-03 integrados y F-04 implementación revisada; candidato cohesivo posterior a `b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43`.
- **Prerequisite infrastructure:** release/deployment proof para cada runtime objetivo y observación suficiente para separar código, binario y proceso.
- **Required MCP capabilities:** source/release/deployment read-back; operator sólo donde la receta lo requiera; no cerrar con marcadores legacy.
- **Physical recipe:** publicar desde la rama autorizada, verificar manifest/digest y demostrar que cada runtime ejecuta el mismo release antes de cualquier FULL golden.
- **Durable evidence:** release manifest, SHA/blob equality, deployment proofs, runtime identity y matriz de superficies tocadas.
- **PASS criteria:** release cohesivo trazable a source autorizado y runtime; no mezclar binario viejo con HEAD nuevo.

#### CERT-F05-02 — FULL authentic golden and result surfaces

- **Prerequisite product SHA/release:** CERT-F05-01 PASS y CERT-F04-02/CERT-F04-03 según el alcance del release.
- **Prerequisite infrastructure:** SQX/licencia válida, MetaEditor, runtimes Forge/Echo y acceso durable a result surfaces.
- **Required MCP capabilities:** ejecución/observación de todos los runtimes incluidos, control-plane evidence y lectura de result surfaces; nada sintético para el veredicto físico.
- **Physical recipe:** ejecutar la campaña FULL real con matriz determinística, cómputos largos, cancellation/retry/drain sólo donde el delta lo exige, y golden/result surfaces inspeccionables.
- **Durable evidence:** campaign/run IDs, per-stage evidence, finalistas, artifacts, warnings/funnel, result surfaces, cancellation/recovery proof y golden refs.
- **PASS criteria:** factory usable y explicable; zero finalists honesto sigue siendo resultado válido, pero no se declara PRODUCT CAPABILITY sin la evidencia requerida.

#### CERT-F05-03 — Final Factory V2 closure

- **Prerequisite product SHA/release:** CERT-F05-01 y CERT-F05-02 PASS; cross-lane PASS cuando el release incluya Echo join.
- **Prerequisite infrastructure:** todos los runtimes/capabilities requeridos siguen observables durante la campaña.
- **Required MCP capabilities:** conjunto certificado de F04/F05 y read-back de evidencia final.
- **Physical recipe:** ejecutar la matriz final de release, confirmar no-regresiones del delta y emitir el manifest de certificación de Factory V2.
- **Durable evidence:** cert manifest, release/source/runtime mapping, golden refs, unresolved accepted debt y veredictos por gate.
- **PASS criteria:** sólo entonces F-05 puede marcar `PHYSICALLY CERTIFIED`/`CLOSED`; no recertifica B1A/B1B/B2 sin delta.

### Dependencias y clasificación de trabajo restante

| Trabajo | Clase | Decisión |
|---|---|---|
| F-04 T2.11/T2.12/T2.13 | C — HARD BLOCKED | Requiere ejecución física, golden auténtico y/o runtime cross-lane; queda deferred, no waived. |
| F-05 implementación/pre-cert: matriz release, result/read surface y checklist de conformance | A — CAN CONTINUE NOW | Tiene valor real y usa contratos/fixtures existentes sin afirmar certificación. |
| F-05 release/physical/FULL golden/cierre | B — CAN IMPLEMENT BUT CANNOT CERTIFY | La preparación y el tooling avanzan; el veredicto necesita CERT-F05-01…03. |
| E-04 T01–T20 | A — CAN CONTINUE NOW | Ya está integrado; no se reabre. |
| E-04 T21/AC-37 | C — HARD BLOCKED | Exige golden Forge auténtico y join real; synthetic S0/fakeconsumer no satisfacen el gate. |
| E-02 implementation/verification | B — CAN IMPLEMENT BUT CANNOT CERTIFY | No depende de T2.11–T2.13; conserva su PHYSICAL_PARTIAL y gates propios. |
| E-05 implementation/corrections | B — CAN IMPLEMENT BUT CANNOT CERTIFY | No depende de T2.11–T2.13; su cierre actual depende de S0 erratum/control-plane evidence y su propia verificación. |
| E-06 Reference enrollment and binding | B — CAN IMPLEMENT BUT CANNOT CERTIFY | El diseño/implementación puede avanzar; read-back y primera observación requieren runtime físico. |
| E-07 Raw facts, DEAL and coverage | B — CAN IMPLEMENT BUT CANNOT CERTIFY | Puede avanzar con fixtures; offline/restart/partial/late-cost certification requiere observación real. |
| E-08 Routing, EconomicCommand and risk reservation | B — CAN IMPLEMENT BUT CANNOT CERTIFY | Source/shadow puede avanzar; crash/UNKNOWN/reservation certification requiere runtime. |
| E-09 Execution copy and reconciliation | B — CAN IMPLEMENT BUT CANNOT CERTIFY | Puede implementarse; Execution Fidelity PHYSICAL requiere Reference/Execution real. |
| E-10 Strategy Quality and eligibility | A — CAN CONTINUE NOW | Quality/eligibility puede avanzar con fixtures, coverage explícita y abstención; no depende de golden Forge físico. |
| E-11 PortfolioVersion shadow | A — CAN CONTINUE NOW | Selection/allocation shadow determinista puede avanzar con fixtures y CASH; no toca dinero real. |
| E-12 Apply/rebalance/replacement/retirement | B — CAN IMPLEMENT BUT CANNOT CERTIFY | La implementación DEMO puede avanzar; PHYSICAL DEMO requiere runtime real y ACK/recovery. |
| E-13 Front/read/ops and V1 closure | B — CAN IMPLEMENT BUT CANNOT CERTIFY | Read/ops surfaces pueden avanzar; PRODUCT CAPABILITY/restore requiere evidencia física. |

### Delta de convergencia Windows owner — 2026-09-17 (misión NORMAL F05C-F04-01-WINDOWS-CONVERGENCE con autoridad owner explícita; ningún gate ejecutado, ningún estado de gate cambiado)

Misión de ejecución de la receta owner del preexec lock contra el artefacto publicado `worker/sqx/0.2.98/windows-amd64/sqx-mt5-worker.exe` (SHA256 `0bceda4badd982b25b01f13ec40a23eb95c8179e28d8a6d955036b30fc7aa474`, size 37250048). Veredicto: **`WINDOWS CONVERGENCE BLOCKED`** — la precondición B sigue FAIL (`BLOCKED — OWNER ACTION REQUIRED`) y la receta queda refinada con un descubrimiento material: la autorización owner de la misión no crea capability; el plano MCP certificado sólo entra a `worker-kronos` como `echo-dev` sin membresía `BUILTIN\Administrators`, y el stop del incumbent es cross-identity.

- **Paso 0 — identity read-back: INDETERMINABLE (boundary de diseño, no fallo transitorio).** `whoami /groups` sin `S-1-5-32-544` (sólo Users; Mandatory Level Medium); `Get-Process -Id 1700` sin Path/StartTime; `tasklist /v /fi "PID eq 1700"` Access denied; `(Get-Process -Id 1700).Modules` RuntimeException (sin `PROCESS_QUERY`, por DACL también sin `PROCESS_TERMINATE`); `sc.exe queryex` OpenSCManager FAILED 5; `Get-ScheduledTask` CIM Access denied; `C:\Windows\Prefetch\SQX-MT5-WORKER*` UnauthorizedAccessException; `C:\ProgramData\Stager` ACL-bloqueado. El SHA256 del ejecutable real de PID 1700 no es obtenible por canal certificado ⇒ la comparación con `0bceda4b…` (y por tanto el paso 2 y la condición del paso 3) no es ejecutable por el agente.
- **Descubrimiento: el worker Windows es stager-managed.** Registro HKLM legible: servicio `StagerRuntime` START=2 TYPE=16, ImagePath `C:\ProgramData\Stager\bin\stager-runtime.exe service --target-config C:\ProgramData\Stager\target.yaml`; `C:\stager\install-stager.ps1` (legible) registra además la tarea `StagerReconcile` cada 1 minuto como SYSTEM RunLevel Highest (reconcile de releases contra manifest) y aplica `icacls /inheritance:r` con grant sólo Administrators+SYSTEM — el ACL-block de `C:\ProgramData\Stager` es by design; `stager-target.yaml.example` declara driver `windows-scm`, entrypoint `bin/worker.exe`, restart_backoff 5s. PID 1700 (`sqx-mt5-worker`) es el entrypoint supervisado por ese servicio. **Tensión de modelo de deployment:** el contrato canónico Windows (`deploy/windows/sqx-mt5-worker/README.md`: owner-operated foreground, "deliberately does not install a Windows service") convive con este stager-managed activo; decidir es owner (aceptar stager como modelo Windows, o converger a C:\SQX deshabilitando `StagerReconcile`+`StagerRuntime` — si no, el reconcile re-activa el servicio en ≤1 min y produce doble poller).
- **Idle/drain: PASS.** `C:\MT5\test\EchoForgeJobs` sin actividad desde 2026-09-05 21:18 (último `echo-forge-full-golden-20260905T221730Z-…`); netstat PID 1700 con sólo 2 ESTABLISHED (Temporal `192.168.31.46:7233` poller vivo + OTel `192.168.31.60:14317`); sin transferencias activas ⇒ el stop del incumbent es seguro desde drain, cuando exista canal con elevación.
- **Backup y scripts canónicos: verificados en source @ `3d0e8c9`.** `Install-EchoForgeMT5Worker.ps1` crea `releases\<ver>\` + backup automático del binario previo en `backups\<ts>\`; `Rollback-EchoForgeMT5Worker.ps1` restaura sólo desde `backups\`; `Start-EchoForgeMT5Worker.ps1` exige `ENV` (bootstrap ETCD existente) y valida paths portable. Artefacto de staging byte-exacto verificado local: worktree cert `symphony-f04-cert-20260913` @ `b57bfb2` `deploy/0.2.98/windows-amd64/sqx-mt5-worker.exe` == digest publicado == read-back MinIO del preexec lock.
- **Capacidad de instalación: factible; stop: imposible; segundo poller: rechazado.** echo-dev puede crear `C:\SQX` (probe creado y eliminado, footprint cero) y `sftp-upload` está certificado en `mt5-kronos-operator`; pero sin elevación no se puede detener PID 1700 ni el par servicio/tarea stager. Arrancar el worker canónico con el incumbent vivo fue descartado: consumidores competentes sobre `sqx-mt5-queue` contaminarían el determinismo de CERT-F04-01.
- **Acción exacta pendiente owner (sin cambios de gates):** (1) paso 0 elevado en `worker-kronos`: `Get-Process -Id 1700 | Select Path` + `Get-FileHash <path> -Algorithm SHA256` + inventario con hashes de `C:\ProgramData\Stager\target.yaml` y `releases\*`; (2) si hash == `0bceda4b…` y el owner acepta el modelo stager ⇒ Windows converged sin instalar (registrar identidad+poller como deployment proof); (3) si prevalece el modelo canónico C:\SQX ⇒ `Disable-ScheduledTask -TaskName StagerReconcile` + `sc.exe stop StagerRuntime` + `sc.exe config StagerRuntime start= disabled` + confirmar terminación de PID 1700, staging byte-exacto en `C:\staging\`, `Install-EchoForgeMT5Worker.ps1 -ArtifactPath C:\staging\sqx-mt5-worker.exe -InstallDirectory C:\SQX\sqx-mt5-worker -Version 0.2.98` (WhatIf → real), `Start-EchoForgeMT5Worker.ps1` con `ENV` autorizado (WorkerPath `C:\SQX\sqx-mt5-worker\sqx-mt5-worker.exe`, MetaEditor `C:\MT5\test\MetaEditor64.exe`, Terminal `C:\MT5\test\terminal64.exe`, InstallationRoot `C:\MT5\test`, JobsRoot `C:\MT5\test\EchoForgeJobs`), proofs (hash == `0bceda4b…`, proceso nuevo con Path legible, poller `sqx-mt5-queue`), rollback canónico ante fallo.

Evidencia de la misión: agent-run `2026-09-17-zcode-glm-5.3-flash-f05c-cert-f04-01-windows-convergence`, change_log `2026-09-17-f05c-cert-f04-01-windows-convergence`.

### Delta de readiness R1 — 2026-09-17 (misión NORMAL F05C-CERT-F04-01-READINESS-R1; corrección manager del preflight aceptada; ningún gate ejecutado, ningún estado de gate cambiado)

El manager corrigió el preflight 2026-09-16: CERT-F04-01 NO está demostrado como BLOCKED por infraestructura; la ausencia de un MCP Temporal dedicado no es un blocker demostrado; el Access Plane congeló política REUSE-FIRST (SSH/logs + read models PostgreSQL antes de crear/extender Temporal); `mt5-kronos-operator` ya existe y no se crean MCPs preventivamente. Misión ejecutada read-only para decidir si CERT-F04-01 puede correr con capabilities existentes. Veredicto: **`CERT-F04-01 READY TO EXECUTE`** (receta exacta emitida; prompt siguiente `F05C-CERT-F04-01-EXEC` producido, NO ejecutado, pendiente autorización manager). Los cuatro blockers del preflight quedan resueltos o reclasificados con evidencia:

- **Temporal — no requerido (T5 permanece DEFERRED).** Ningún dato exigido por la autoridad de CERT-F04-01 requiere MCP Temporal ni history/replay. Mapeo por dato: WorkflowID/RunID/status/TaskQueue/Namespace → worker log `/var/log/symphony/symphony-worker.log` (legible por SSH; líneas `ExecuteActivity` con WorkflowType/WorkflowID/RunID/Attempt; el sanitizador de entropía oculta parcialmente UUIDs) + read models PG vía `sqx-flowkit` (`run stages`); ParentWorkflowID/RunID → estructura logs+refs (no exigido por el gate); history/replay → no exigido por CERT-F04-01 (pertenece a un Temporal dedicado si algún gate futuro lo demuestra). Canal demostrado en vivo: flota Linux `CURRENT=0.2.98` (Zeus/Hera/Kronos), Zeus `stager-runtime` active con worker `/opt/stager/releases/0.2.98/bin/symphony` PID 2633855, `ACTIVATION.json` committed `fedae05f…` 0.2.97→0.2.98, `Started Worker Namespace sqx-prop TaskQueue sqx-main-queue`.
- **Read models PostgreSQL — canal existente demostrado.** El control plane Forge real es `192.168.31.220:5432/trading_systems_test` schema `sqx` (server compartido con `temporal`/`temporal_visibility`/`echo`; los perfiles MCP PG cubren sólo `echo`/`echo-develop`). El canal autorizado es `sqx-flowkit` (CLI read-only entregado por F-05-I; boot ETCD+PG `/sqx-flowkit/production/` provisionado): demostrado en vivo desde Daedalus con `campaign list` exit 0 sobre campañas reales (`a9e73e66` COMPLETED del recert `0.2.92`). Cobertura: `campaign get/list` (ForgeCampaign), `run get/stages` (FlowRun, funnel, timeline de stages), `strategy get` (identidad, participations, magic `{registry_namespace, magic_decimal, allocation_ref, assigned_at}`, `strategy_versions {version_ref, payload_digest, sealed_at}`, `handoffs {idempotency_key, payload_digest, wave_key, version_ref, decision_ref, delivery.state}`). EvaluationRefs/compile evidence por Mongo `forge` RO (certificado). Limitación documentada: los documentos flowkit no emiten las columnas `temporal_workflow_id/temporal_run_id` de `sqx.stage_executions`; su captura en EXEC va por worker log (RunID visible) o CLI Temporal local read-only instalado en Daedalus si el sanitizador impidiera la evidencia (instalar un CLI local no es crear MCP).
- **Gate owner del catálogo CC — STALE, ya resuelto.** Owner decision 2026-09-11 (Magic Number V1 frozen `YYMMIIIDSSS`, XAUUSD=001) materializada en migration `016_magic_number_v1_allocator` (catálogo immutable `sqx.magic_instruments` XAUUSD=1…USDJPY=8 + contadores mensuales) presente en el SHA de la release `b57bfb2`; `CC_MISSING_OWNER_GATE` tiene 0 ocurrencias en producción @ `b57bfb2` y @ `3d0e8c9`; `UseDurableMagicAllocation: true` cableado en el caller productivo; namespace `forge-live`. No existe decisión owner pendiente; no bloquea.
- **Windows/MT5 — capability existe; observación ejercitada vía operator.** Viewer `mt5-kronos` re-demostrado POLICY_DENIED para las lecturas del gate (H2 enforcement intacto). `mt5-kronos-operator` ejecutó lecturas read-only: proceso `sqx-mt5-worker` PID 1700 RUNNING; `C:\MT5\test` con `MetaEditor64.exe`/`terminal64.exe`/`metatester64.exe` (build 2026-09-05), root `EchoForgeJobs`, `MQL5/` y `Tester/`; worker MT5 es proceso foreground owner-operated (no servicio Windows, README de deploy). UNKNOWNs acotados que la propia campaña resuelve como deployment proof del gate: identidad build/path del worker Windows en ejecución no legible con autoridad no-admin (Path/StartTime ocultos, WMI y `tasklist /V` denegados; path canónico `C:\SQX` del README inexistente; exes viejos `f33/f36` de agosto en `C:\stager`), y materialización del binario `0.2.98` Windows en `worker-kronos` no demostrada (rollout 2026-09-13 INCONCLUSIVE vigente). No son gaps de capability: son pasos internos del gate.
- **MinIO/etcd — sin requerimiento de evidencia para este gate.** MinIO (bucket `sqx-strategies`, uploads con etag/size en worker log): los bytes se verifican in-flow (`VerifyCompiledArtifactForSeal`, readbacks) y sus digests quedan en evidencia durable (flowkit + Mongo); la autoridad de CERT-F04-01 no exige export agent-side de preimages — ese requerimiento pertenece a CERT-F04-02 y se resuelve ahí (hoy sin canal dedicado, registrado como REQUIRED_LATER del gate siguiente). etcd: sólo config (postgres/telemetry/temporal/echo ingest); ninguna evidencia del gate vive en etcd; la ausencia de `echo/ingest/base_url`+bearer deja la entrega de handoffs en fail-closed (0 POST) por diseño — es el asunto de CERT-F04-03 (join real), no de este gate. Evidencia startup Zeus: `Echo E-04 ingest no configurado: entrega de handoffs en fail-closed (0 POST)`.
- **Separación explícita de lanes:** la identidad de build del runtime Echo PROD vs E-04 (UNKNOWN del preflight) pertenece a CERT-E04-01, no a este gate. Loki no ingiere logs de `sqx-worker` (canal = archivo por SSH, demostrado). Licencia SQX: se verifica en ejecución (receta PHYSICAL F-04: si reporta expired → STOP owner).

Evidencia de la misión: agent-run `2026-09-17-zcode-glm-5.3-flash-f05c-cert-f04-01-readiness-r1`, change_log `2026-09-17-f05c-cert-f04-01-readiness-r1`.

### Delta de preexec lock — 2026-09-17 (misión NORMAL F05C-F04-01-PREEXEC-LOCK; corrección manager del handoff R1 aceptada; ningún gate ejecutado, ningún estado de gate cambiado)

El manager corrigió el handoff R1: `deploy/manifest.json` Git @ `3d0e8c9` declara `0.2.96` y el repositorio no contiene `deploy/0.2.98`, por lo que esas rutas no sustentan la publicación de 0.2.98; los UNKNOWNs Windows que R1 clasificó como pasos internos de la campaña sí gatean la autorización de EXEC y deben cerrarse antes de la campaña. Misión read-only que cerró las tres precondiciones del EXEC. Veredicto: **`NO READY TO EXECUTE`** — A PASS, B FAIL (`BLOCKED — OWNER ACTION REQUIRED`), C PASS, D PASS, E FAIL por B; el prompt maestro `F05C-CERT-F04-01-EXEC` no se redacta hasta cerrar B.

- **A — Autoridad remota 0.2.98: PASS.** Read-back con el CLI `release-authority` @ `3d0e8c9` (`--target 0.2.98`, sólo ListObjects/GetObject sobre MinIO producción): `published_version=0.2.98`, `authority_state=CONSISTENT`, `target_state=EXACT_MATCH` — los 6 objetos `worker/sqx/0.2.98/` (5 linux-amd64 + 1 windows-amd64) verifican byte-exacto (SHA256+tamaño) contra el manifest publicado `worker/sqx/manifest.json` (bucket `deploy`). Artefacto Windows: `worker/sqx/0.2.98/windows-amd64/sqx-mt5-worker.exe`, size 37250048, sha256 `0bceda4badd982b25b01f13ec40a23eb95c8179e28d8a6d955036b30fc7aa474`. Source: `vcs.revision=b57bfb2c3d2c4e0a96d2b3fa654cea41e1a64f43` (buildinfo del exe Windows; `vcs.modified=true` ya explicado por artefactos operacionales ignorados). Publicación: `deployer_screen.log` del worktree de certificación registra 6 uploads + "Manifest publicado `release_version=0.2.98`" entre 2026-09-13T03:20:38Z y 03:20:41Z.
- **B — Windows identidad/convergencia: FAIL.** `worker-kronos`: `sqx-mt5-worker` PID 1700 RUNNING con conexión ESTABLISHED a Temporal `192.168.31.46:7233` (poller vivo), pero identidad de build NO atribuible con autoridad echo-dev no elevada (`Get-Process` Path/StartTime/FileVersion ocultos por integridad; WMI `Win32_Process` Access denied 0x80041003; `C:\ProgramData\Stager` ACL-bloqueado). Inventario legible sin coincidencias: `C:\SQX` inexistente (la instalación canónica nunca se ejecutó), `C:\stager` sólo exes f33/f36 (2026-08-13; SHA256 `F7BBFE65…`/`FC9895B6…`; tamaños 52007936/52034048 ≠ 37250048), `C:\stager_old` binarios era 0.2.40. WINDOWS NOT CONVERGED. Receta owner emitida con scripts canónicos `deploy/windows/sqx-mt5-worker/` @ baseline: paso 0 identity read-back elevado (`Get-Process … Path` + `Get-FileHash` del ejecutable en ejecución; si hash == `0bceda4b…` → converged sin instalar); si no converge → transferir el artefacto verificado a `C:\staging\`, preflight `Install-EchoForgeMT5Worker.ps1 -WhatIf` (instalación versionada `releases\0.2.98\` + backup automático a `backups\<ts>\`), stop/drain del worker foreground actual (sólo owner, ventana dedicada, sin kill indiscriminado, sin sustituir binario bajo proceso activo), install real, `Start-EchoForgeMT5Worker.ps1` (WorkerPath `C:\SQX\sqx-mt5-worker\sqx-mt5-worker.exe`, MetaEditor `C:\MT5\test\MetaEditor64.exe`, terminal `C:\MT5\test\terminal64.exe`, InstallationRoot `C:\MT5\test`, JobsRoot `C:\MT5\test\EchoForgeJobs`), read-back de convergencia (hash `C:\SQX\…\sqx-mt5-worker.exe` == `0bceda4b…` + poll `sqx-mt5-queue` confirmado), rollback con `Rollback-EchoForgeMT5Worker.ps1` desde `backups\<ts>\` + restart; STOP conditions: hash mismatch post-instalación, poller ausente, validación MetaEditor fallida, licencia SQX expired.
- **C — Input canónico CERT-F04-01: PASS.** Mecanismo de arranque: escribir el input JSON en el `watch_dir` del servicio `sqx-watcher` (ETCD key `watch_dir`, default `./input`; mecanismo canónico input/watcher del run físico 2026-09-12). Provenance congelado vía `sqx-flowkit campaign get a9e73e66-5062-44d7-b665-22740383c676` (recert 0.2.92: COMPLETED TARGET_REACHED, `target_finalists=1`, 1 wave, flow_run `4f135030-ad0c-4b41-9e32-f2f8c466c50b`, duración ~9 min) — provenance, NO autorización: el input de EXEC se deriva de esa estructura con los deltas 0.2.98/F-04. Deltas obligatorios del contrato §PHYSICAL: XAUUSD, dirección única `L`, promotion `2.0.0` (`finalist_promotion`), robust selection = 1, sin requested-magic 888111, `UseDurableMagicAllocation: true` productivo @ release. Identidad: `request_id` nuevo por run con patrón `<nombre>-<UTC yyyyMMddTHHMMSSZ>-<hex8>`; routing RequestID+SourceKey y durable FlowIntentToken/FlowRunRef. Namespace Temporal `sqx-prop`; queues `sqx-main-queue` (Linux) / `sqx-mt5-queue` (Windows); namespace Forge `forge-live`. Límites: `target_finalists=1`, `max_waves=1`; timeout/cancel: Temporal nativo (`mt5.timeout` → StartToClose +2 min) y cancel del run propio. Observación: worker log por SSH + `sqx-flowkit` campaign/run/strategy + Mongo `forge` RO. Evidencia esperada: release/deployment proofs, FlowRun/workflow IDs, Decision V2, allocation/readback, compile inputs/outputs/log, EvaluationRefs, StrategyVersion, HandoffManifest y delivery state.
- **Delivery fail-closed: CLÁUSULA CITADA.** Contrato F-04 §PHYSICAL: la cadena física termina en `HandoffManifest` y "E-04 runtime/deploy/join es one-shot posterior (T2.13)"; "No mezclar E-04 runtime config/ETCD/gateway con C4". Delivery matrix: `Echo unavailable → HANDOFF_CREATED` (retry, non-terminal) y "Si E-04 aún no tiene read: no fingir INTEGRATION PASS". El fail-closed (0 POST, entregables en `HANDOFF_CREATED` por falta de `echo/ingest/base_url`) es por tanto resultado compatible con CERT-F04-01; la entrega `INGESTED`/join real pertenece a CERT-F04-03. El delivery state del run es evidencia durable exigida, no gate de PASS.
- **D — Observación: PASS** (canales re-demostrados hoy: SSH worker log, `sqx-flowkit` exit 0 contra producción, Mongo `forge` RO certificado, operator Windows para lecturas autorizadas). **E — Blockers: FAIL por B**; sin otros blockers concretos.
- **Único siguiente paso:** owner ejecuta el paso 0 (identity read-back elevado en `worker-kronos`) y, si hash ≠ `0bceda4b…`, la receta de convergencia canónica; con Windows converged el manager re-evalúa A–E y autoriza la redacción y despacho de `F05C-CERT-F04-01-EXEC`.

Evidencia de la misión: agent-run `2026-09-17-zcode-glm-5.3-flash-f05c-cert-f04-01-preexec-lock`, change_log `2026-09-17-f05c-cert-f04-01-preexec-lock`.

### Preflight de entrada a F-05-C — 2026-09-16 (misión NORMAL F05C-ENTRY-PREFLIGHT, read-only; ningún gate ejecutado, ningún estado cambiado)

F-05-I está CLOSED (`IMPLEMENTED / SOURCE VERIFIED`, cierre declarativo commit `3d0e8c958765da23840e00bf1a0ac017fc47597a`, HEAD == `origin/codex/f05-release-prep` verificado; handoff F-05-C presente en repo: read-surface + conformance checklist + manifest template con los 7 gates OPEN). El orden frozen de ejecución permanece intacto: **CERT-F04-01 → CERT-F04-02 → CERT-E04-01 → CERT-F04-03 → CERT-F05-01 → CERT-F05-02 → CERT-F05-03**. Veredicto del preflight: **ningún gate es ejecutable hoy**; el primer gate del orden está `BLOCKED BY INFRA`. Las certificaciones históricas B1A/B1B/B2/F-03 conservan su alcance original y no se extrapolan a la release actual (matriz @ `3d0e8c9` verificada: 7 gates DEFERRED, allowlist histórica intacta).

- **CERT-F04-01 — BLOCKED BY INFRA.** Released `0.2.98` desde `b57bfb2` ✓ (as_of 2026-09-13); Linux Zeus/Hera/Kronos OBSERVED/RUNNING vía `stager-runtime.service` ✓; observación runtime Echo ✓ (viewer `echo-runtime-prod` + observability, GAP-ECHO-004 CLOSED). Faltan: (a) capability Temporal de observación/control — sigue `REQUIRED_LATER` deferred por decisión owner en [[ACCESS-CERTIFICATION]], y `etcd` sin capability (`UNKNOWN_NEEDS_SOURCE_PROOF`); (b) gate owner del catálogo CC (allocation real); (c) canal de evidencia Windows: el viewer `mt5-kronos` sigue con policy gap (sólo identidad), el perfil `mt5-kronos-operator` está certificado (H2 smoke) pero la observación de servicio/release/path **no fue ejercitada** — última campaña física 2026-09-13 quedó rollout INCONCLUSIVE con Windows sin evidencia; (d) MinIO/object-store sin capability MCP en el plane (lectura de artefactos del flujo quedaría sin canal dedicado). Ningún flujo F-04 real ejecutado bajo `0.2.98`: no existen FlowRun/workflow IDs, Decision V2, allocation/readback, compile logs, EvaluationRefs, StrategyVersion ni HandoffManifest reales que certificar.
- **CERT-F04-02 — BLOCKED** (depende de CERT-F04-01 PASS; además el almacenamiento durable/exportable de preimages necesita canal — MinIO fuera del plane). No existe golden auténtico: `FORGE_GOLDEN_FIXTURE_PENDING` sigue vigente; S0/fakeconsumer/sintéticos no califican.
- **CERT-E04-01 — BLOCKED** (clase C HARD; depende de CERT-F04-02). E-04 integrado: `a99f9a63` es ancestro de `origin/master` echo @ `5dd998f1` ✓ source-side. **UNKNOWN material nuevo:** la identidad de build del runtime Echo PROD (`.71`) vs E-04 no está demostrada — logs vivos exponen `service.version=2.0.0` sin SHA, los PIDs observados (core desde ~ago20, gateway desde ~sep09) preceden al merge E-04 (2026-09-12) y el endpoint `POST /api/v1/forge/promotions` no fue verificado en runtime; falta deployment proof o verificación de identidad de build antes de considerar ese prerequisto satisfecho. T21/AC-37 permanece OPEN.
- **CERT-F04-03 — BLOCKED** (cadena completa: CERT-F04-02 + CERT-E04-01 PASS).
- **CERT-F05-01 — BLOCKED POR ORDEN FROZEN.** Su prerequisto de producto quedó **recién cumplido** con el cierre F-05-I: existe candidato cohesivo posterior a `b57bfb2` (`codex/f05-release-prep` @ `3d0e8c9`, F-01…F-04 integrados y F-05-I implementado/source verified). No ejecutar antes de tiempo: el trigger exige la cadena completa previa. Al momento de ejecutar requerirá publicar release cohesiva desde rama autorizada y deployment proofs por runtime (incluido el canal Windows, hoy sin evidencia).
- **CERT-F05-02 / CERT-F05-03 — BLOCKED** (cadena; CERT-F05-03 es el único que puede declarar F-05 `PHYSICALLY CERTIFIED`/`CLOSED`). Estado de licencia SQX vigente no verificado en este preflight.
- **Dependencia dominante a resolver primero (decisión owner/manager):** habilitar observación/control Temporal (o equivalente autorizado — re-visitar la decisión T5 deferred del Access Plane); en paralelo: gate owner del catálogo CC, canal de evidencia Windows vía `mt5-kronos-operator` (sólo lectura, policy acotada) y deployment proof de identidad Echo vs E-04. Sin esos cuatro ítems, la cadena CERT no arranca.
- **Misión NORMAL de readiness propuesta (pendiente autorización manager; NO ejecuta ningún gate):** (1) demostrar identidad de build del runtime Echo PROD vs E-04 (deployment proof / read-back de identidad vía viewer u observability, read-only); (2) ejercitar el canal de observación Windows `mt5-kronos-operator` para servicio/release/path/poller (sólo lectura, con justificación de autoridad mínima); (3) producir el diseño de la capability Temporal read-only para el Access Plane (insumo para la decisión owner sobre T5). Evidencia del preflight: agent-run `2026-09-16-zcode-glm-5.3-flash-f05c-entry-preflight`, change_log `2026-09-16-f05c-entry-preflight`.

### Delta de readiness por certificación de accesos — 2026-09-15b (GAP-ECHO-004 CLOSED)

Actualiza el delta anterior tras instalar el owner seed en `.71` y recertificar el viewer `echo-runtime-prod` end-to-end. **No cambia ninguna clase A/B/C ni ejecuta gates productivos.**

- **GAP-ECHO-004 → CLOSED:** owner seed instalado (identidad dedicada `echo-dev` uid/gid 1001, sudo DENIED; key `echo-dev.pub` del plane en `authorized_keys`) y viewer `echo-runtime-prod` certificado desde Daedalus real: identity PASS (`echo-dev@echo`, sin sudo), initialize/tools-list PASS, listeners 80/9080/9090/8080/8090, negative `run-command` → POLICY_DENIED MUST DENY, leak CLEAN. Runtime observado: `echo-gateway` (PID 713) y `echo-core` (PID 110701) RUNNING como `kor`, `echo-functions` (StateFun) RUNNING; **Bridge NOT_DEPLOYED** (registrado con evidencia; no se levanta).
- **E-02:** el gate físico Gateway pasa de BLOCKED-pending a **observación SSH directa PASS** (procesos/listeners/identity); sigue sin control verbs (restart = PROD, fuera de scope). `E02_PHYSICAL_CERTIFICATION_BLOCKED` se mantiene por sus gates propios (Hasura DEV roles/hook, Kafka PublishSync/redelivery, Flink restart/recovery), todos con capability certificada disponible para ejecutarse.
- **CERT-F04-01/CERT-F04-02 (F-04 T2.12/T2.11):** el prerrequisito de observación del runtime Echo queda **completo por vía directa** (viewer SSH) además de la observabilidad. Sigue `BLOCKED BY INFRA` por Temporal/equivalente.
- **CERT-E04-01 (E-04 T21/AC-37):** sigue `HARD BLOCKED` (clase C) por golden Forge auténtico + join real; el prerrequisito de observación runtime ya no es gap.
- **Condición de acceso vigente:** todas las capabilities requeridas del Access Plane están operacionales y certificadas (viewer runtime incluido). El trigger de reactivación de este backlog queda **abierto**; la limitación conocida del viewer es de cobertura (sin systemctl/docker/curl productivo, journal propio únicamente) — los logs productivos siguen por `aranea-observability-ro`.
- **Deuda separada no bloqueante:** host key ED25519 de `.71` idéntica a `sqx-zeus` (clon sin regenerar); rotación owner-side opcional con actualización de `trustedHostKey` del perfil en el mismo cambio.

### Delta de readiness por certificación de accesos — 2026-09-15 (gaps stale reconciliados)

Actualiza el delta 2026-09-14 tras el cierre H1/H2, la certificación `aranea-observability-ro` (:3009, PASS 12/12 + consumer PASS) y la resolución del target runtime Echo. **No cambia ninguna clase A/B/C ni ejecuta gates productivos.**

- **Gaps stale eliminados:** Hasura DEV/PROD (`aranea-hasura-dev-admin`/`aranea-hasura-prod-ro`), Kafka DEV (`aranea-kafka-dev-admin`) y Flink DEV (`aranea-flink-dev-admin` + `docker-echo-dev-operator`) están **certificados y operativos** desde 2026-09-12/13 — los GAP-ECHO-001/002/003 de la matriz de 2026-09-14 eran históricamente stale. Observabilidad PROD (GAP-ECHO-007) queda cubierta por `aranea-observability-ro`.
- **E-02:** sus verificaciones físicas pendientes contra Hasura-DEV/Kafka/Flink **ya tienen capability certificada para ejecutarse** (siguen sin ejecutarse: no se corrieron en esta sesión). `etcd`/tokens reales siguen `NOT_OBSERVED` (sin capability). Clase B se mantiene; `E02_PHYSICAL_CERTIFICATION_BLOCKED` ahora depende sólo de ejecutar esas verificaciones y del target Gateway.
- **E-02 Gateway physical:** target real resuelto — `.211` muerto; runtime vivo = PROD `192.168.31.71` (`prod.echo.gateway.lab.aranea`, `/health` 200). Viewer SSH `echo-runtime-prod` staged; verificación SSH pending owner key install. Observación vía `aranea-observability-ro` operativa (logs `service=echo-core` `env=production` en vivo).
- **CERT-F04-01/CERT-F04-02 (F-04 T2.12/T2.11):** el prerrequisito de observación del runtime Echo queda **parcialmente cubierto por observabilidad** (logs/metrics PROD en vivo); la observación directa SSH queda pendiente de la única owner action (instalar `echo-dev.pub` del plane en `.71`). Sigue `BLOCKED BY INFRA` por Temporal/equivalente.
- **CERT-E04-01 (E-04 T21/AC-37):** sigue `HARD BLOCKED` (clase C); el prerrequisito de observación runtime queda parcial (observabilidad sí, SSH viewer pending).
- **CERT-F04-03 / CERT-F05-01…03:** sin cambio; dependen de los gates anteriores.
- **Condición de acceso vigente:** H1/H2 RESOLVED; el trigger de reactivación de este backlog queda **abierto sólo para la certificación SSH viewer sobre `.71`** (post owner action) — el resto de capabilities requeridas ya está operacional.

### Delta de readiness por certificación de accesos — 2026-09-14

Fuente: [[ACCESS-CERTIFICATION]] (run 2026-09-14, veredicto `ACCESS_CERTIFICATION_PARTIAL`). Este delta **no cambia ninguna clase A/B/C ni cierra carriles**; registra qué superficies de acceso quedaron verificadas físicamente y qué gaps siguen bloqueando cada gate.

- **Verificado y disponible para gates físicos:** PostgreSQL PROD-RO y DEV-RW (DML sin DDL en DEV), MongoDB forge RO/RW, Kafka DEV admin (con `delete_topic` eventual — post-condición obligatoria de cleanup), Flink DEV control-plane read, SSH operator sobre SQX/MT5/docker-echo-dev (identidades re-verificadas).
- **E-02:** sus verificaciones físicas pendientes contra `psql`/Kafka/Flink/Hasura-DEV ya tienen capability certificada para ejecutarse; `etcd`/tokens reales siguen `NOT_OBSERVED` (sin capability). Clase B se mantiene.
- **CERT-F04-01/CERT-F04-02 (F-04 T2.12/T2.11):** bases de acceso re-verificadas; siguen `BLOCKED BY INFRA` por la ausencia de observación del runtime Echo y de capability Temporal/equivalente autorizada. Prerrequisito nuevo explícito: capability de observación del host Echo runtime (192.168.31.71:8090, visto en webhooks Hasura).
- **CERT-E04-01 (E-04 T21/AC-37):** sigue `HARD BLOCKED`; el mismo prerrequisito de observación del runtime Echo es el gap dominante. Clase C se mantiene.
- **CERT-F04-03 / CERT-F05-01…03:** sin cambio; dependen de los gates anteriores.
- **E-05…E-13:** sin cambio de clase; para sus futuros gates físicos queda disponible la superficie DEV certificada arriba, y quedan nombrados como `REQUIRED_LATER`: observación runtime Echo, etcd, observabilidad (OBS3), Temporal (T5), Kafka/Flink PROD.
- **Condición de acceso vigente:** el trigger de reactivación de este backlog **sigue cerrado** hasta resolver H1 (credenciales expuestas por `export_metadata`), H2 (boundary viewer SSH no aplicado) y la capability de observación del runtime Echo.

### Próxima tarea única recomendada para NORMAL

**Consumidas:** F-05-I — Cohesive release/read-surface preparation quedó CLOSED 2026-09-16 (`IMPLEMENTED / SOURCE VERIFIED` @ `3d0e8c958765da23840e00bf1a0ac017fc47597a`; ver [[Echo Forge — F-05-I Cohesive release and read surfaces]]); la misión NORMAL de readiness propuesta por el preflight 2026-09-16 quedó **consumida y superada** por el delta `2026-09-17 — Readiness R1 CERT-F04-01` (con la corrección manager: sin diseño Temporal RO, REUSE-FIRST). **Corrección vigente (preexec lock 2026-09-17):** `F05C-CERT-F04-01-EXEC` **NO está autorizado**; el veredicto READY de R1 quedó condicionado por el lock: A (autoridad remota 0.2.98) y C (input canónico) están cerradas, B (convergencia Windows) está `BLOCKED — OWNER ACTION REQUIRED` con receta emitida en el delta `2026-09-17 — Preexec lock`. **Recomendación vigente:** owner ejecuta la receta de convergencia Windows (paso 0 identity read-back elevado + instalación canónica si el hash ≠ `0bceda4b…`); con Windows converged, el manager re-evalúa A–E y autoriza redactar/despachar `F05C-CERT-F04-01-EXEC`; ejecutar sólo CERT-F04-01, sin saltar a CERT-F04-02 ni a ningún otro gate.

### Trigger de reactivación

Activar este backlog cuando las capabilities requeridas del Aranea MCP Access Plane estén operacionales y certificadas, y los runtimes objetivo sean observables y operables por la policy correspondiente. En ese momento ejecutar estrictamente CERT-F04-01 → CERT-F04-02 → CERT-E04-01 → CERT-F04-03 → CERT-F05-01 → CERT-F05-02 → CERT-F05-03; no usar una fecha calendario ni saltar gates.

## Fuentes

- [[Echo Forge — Factory V2 Completion]] y [[Echo Forge — F-04 Magic allocation, version seal and handoff]]: F-04/F-05 scope, SHA, release, T2.11–T2.13 y evidencia histórica.
- [[Echo — Producto Integrado]] y [[Echo — Live Platform V1]]: DAG E-01…E-13, E-04 T21/AC-37 y reglas de paralelismo.
- [[Echo — E-04 Forge Ingestion E1]]: E-04 INTEGRATED, T21 POST-INTEGRATION, synthetic ≠ cross-lane golden.
- [[AGENT-PLATFORM - MCP Access Plane]] y [[aranea-agent-dev]]: capabilities/policy de acceso Aranea y límite de no inventar autoridad.
- Decisión explícita del owner en esta sesión: desarrollo continúa; certificación física se difiere, no se waiva.
