---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-15"
updated: "2026-10-15"
area: "[[Aranea]]"
project: "[[Echo Forge — Robust Run Selection V2]]"
application:
entities: []
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM 5.3 (account:zai-individual-coding-plan/GLM-5.3-Flash, host-reported)
model_source: host
task_type: coding
task_complexity: high
outcome: success
verification: passed
evaluator: agent
user_rework: unknown
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-10-15-zcode-glm53-echo-forge-mt5-runtime-hardening

## Trabajo

- **Objetivo:** mandato "ECHO FORGE — WINDOWS MT5 RUNTIME HARDENING" (manager GPT-6): regularizar el mecanismo operacional de `sqx-mt5-worker.exe` sin repetir wave3t — investigar la degradación session 0, decidir restauración SCM vs runner interactivo, eliminar `C:\Temp\session_worker.ps1`, añadir crash-restart/singleton/update, certificar ciclo de vida con pruebas acotadas y documentar límites.
- **Alcance atribuible a esta combinación superficie×modelo:** investigación forense del host (logs de slots MT5, WER, System/Application event log, uptime), diseño+implementación del supervisor PowerShell e instalador, instalación y pruebas físicas A–E en worker-kronos vía aranea-ssh (perfil `mt5-kronos-admin`), helper efímero de dispatch Temporal en symphony, commits `b5d65b9` (pusheado a `xKoRx/symphony` master) y evidencia en vault.
- **Artefactos afectados:** `deploy/windows/session-worker/{Start-EchoForgeSessionWorker.ps1,Install-EchoForgeSessionWorker.ps1,README.md}` (nuevo), `.agents/skills/worker-troubleshooting/SKILL.md` (§10 nueva + nota §9), `AGENTS.md` (línea LocalSystem obsoleta corregida); host: `C:\ProgramData\Stager\bin\Start-EchoForgeSessionWorker.ps1` (SHA256 `08BD7361…4D94`), tarea `\EchoForgeMT5WorkerSession` re-registrada (sin límite 72h, repetición 15 min), `C:\Temp\session_worker.ps1` eliminado; vault: `10-projects/Echo Forge — Robust Run Selection V2/artifacts/mt5-serial-recovery-20261014/WINDOWS-RUNTIME-HARDENING-20261015.md` (nuevo).

## Evidencia

- **Validaciones ejecutadas:** (A) `/run` de tarea viva rechazada por `IgnoreNew`; (B) `taskkill /F` del worker → relanzado <60s desde `releases\0.2.141` con `previous_local_worker_dead_proven=true`; (C) segunda instancia manual exit 1 fail-closed; (D) update por CURRENT con binario byte-idéntico (SHA `BF247D61…EFC96` verificado en ambas rutas) — swap ida y vuelta en ≤30s; (E) backtest real `MT5BacktestArtifactWorkflow` `smoke-hardening-01-20261015` con EX5 durable 89171ea6 (SHA256 `92b025f2…b7f20` verificado por descarga+hash): `last test passed` 0:01:02, `activity.ok status=success` 15:28:23Z, HTM 787.084 B + 4 journals durables en `07_smoke_runtime_hardening_20261015/`. Probe session-0 (SYSTEM, tarea efímera borrada): backtest completo con HTM y cero `MDI create failed`.
- **Resultado observable:** `MT5_OPERATIONAL_CERTIFIED_WITH_CONSTRAINTS`. Worker vivo PID 30840 bajo `releases\0.2.141`, supervisor v2.1 activo, consola KoR Active, CURRENT `0.2.141`, `StagerReconcile` habilitado. Session 0: degradación transitoria recurrente documentada (boundary real 14-oct 10:36, RADAR_PRE_LEAK 09:07, probe PASS 15-oct 11:03) — `StagerRuntime` sigue Disabled por decisión, no por imposibilidad.
- **Limitaciones de la evidencia:** reboot del host NO probado (gate owner); update con release real nueva no ejercitado end-to-end (ruta idéntica a D); el smoke E usó `Symbol=NDX` 2024-H1 (prueba de ciclo de vida, no de fidelidad); LiveUpdate de MT5 descargó build 6230 durante la prueba (drift de runtime pendiente de decisión owner, `Config\common.ini` sin clave de bloqueo verificada).

## Evaluación

- **Correctness: 5** — cada afirmación respaldada por log/hash/prefijo durable; defecto de la v1 del supervisor (loop bloqueante) detectado por la propia prueba D y corregido en v2 antes del cierre.
- **Autonomy: 5** — sin bloqueos al owner; los gates (autologon, reboot, LiveUpdate) quedaron declarados como límites y no como aprobados.
- **Efficiency: 4** — el smoke E tardó ~40 min extra por la elección de rango/símbolo del ini (lección: replicar la config certificada `NDX_SQX` para smokes).
- **Tool use: 4** — aranea-ssh sin sesión interactiva en Windows (usar run-command + sftp-upload con scripts); `$_` se elimina en tránsito (evitar en inline); `sc` es alias de Set-Content (usar `sc.exe`).
- **Overall: 4.5**

## Resultado

- **Outcome:** success — mecanismo versionado, instalado, probado y documentado; sin cambios en Robust V2/Fidelity/ranking/integración Echo; release 0.2.141 intacta.
- **Rework posterior:** ninguno conocido. Pendientes owner: (1) decisión autologon post-reboot, (2) decisión LiveUpdate (bloqueo vs aceptar drift 6182→6230), (3) re-evaluación SCM tras reboot de mantenimiento + probe session-0.
- **Aprendizaje para comparar herramientas:** la cadena MCP aranea (ssh RO/admin por perfil, MinIO presign+hash local, etcd/Temporal) cubrió el ciclo completo de forense→cambio→certificación sin acceso GUI al host Windows; el transporte SSH elimina `$_` y `&&` en PowerShell, lo que obliga a subir scripts por SFTP para cualquier lógica no trivial.
