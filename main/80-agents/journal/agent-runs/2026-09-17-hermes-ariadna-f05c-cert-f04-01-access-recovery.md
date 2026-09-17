---
type: agent_run
schema_version: 1
scope: session
created: "2026-09-17"
updated: "2026-09-17"
area: "[[Echo]]"
project: "[[Echo + Echo Forge — Deferred Certification Backlog]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
aliases: []
agent_surface: Hermes
agent_model: GLM-5.3-Flash
model_source: host
task_type: ops
task_complexity: medium
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

# Agent Run — 2026-09-17-hermes-ariadna-f05c-cert-f04-01-access-recovery

## Trabajo

- **Objetivo:** desbloqueo de Echo Forge CERT-F04-01 — restaurar la capability mínima para identificar y converger el worker Windows (`worker-kronos`) sin ejecutar el gate: demostrar topología real (Stager/Reconcile → proceso → ejecutable → hash → release) read-only, resolver acceso mínimo (A/B/C), certificar la capability consumer-side y dejar la decisión de convergencia preparada. Sin reinstalar, sin segundo worker, sin tocar ETCD ni Stager.
- **Alcance atribuible a esta combinación superficie×modelo:** probing consumer-side del plane `aranea-ssh` (viewer + operator sobre worker-kronos), diagnóstico y recovery operacional de `ssh-mcp` (pool 64), stageo del inspector elevado vía `sftp-upload` con verificación sha256 bidireccional, producción del OWNER ACTION BUNDLE, delta en backlog + change_log.
- **Artefactos afectados:** vault (backlog delta, change_log, este agent-run) y `~/aranea/work/f04-window/` (bundle owner). En `worker-kronos` sólo `C:\Windows\Temp\stager-identity-inspect.ps1` (3373 B, sha256 `4f6712bc159ea155…`), read-only para el host fuera de eso. Cero cambios de configuración del Access Plane.

## Evidencia

- **Validaciones ejecutadas:** (1) superficie `ssh-mcp` v2.8.0 con 11 tools; `list-connections` 7 perfiles, `mt5-kronos` viewer + `mt5-kronos-operator` operator, ambos `echo-dev`; negativo H2 viewer `run-command` → `POLICY_DENIED` vigente; (2) identidad re-verificada `worker-kronos\echo-dev` (sin elevación); (3) PID actual resuelto: `sqx-mt5-worker` PID **1700** (igual al handoff previo; Path/StartTime ocultos), `stager-runtime` PID 30700; poller vivo `netstat :7233` ESTABLISHED 1700→`192.168.31.46`, OTel `192.168.31.60:14317`; (4) servicio `StagerRuntime` START=2, ImagePath `C:\ProgramData\Stager\bin\stager-runtime.exe service --target-config C:\ProgramData\Stager\target.yaml`, **ObjectName `.\kor`**; (5) tarea `StagerReconcile`: ausente del listado completo `schtasks /Query /FO CSV` (exit 0, sólo matches Flighting) y CIM denegado ⇒ presencia no demostrable; (6) boundaries no-admin ratificados: `tasklist /FI` Access denied, `sc.exe query` FAILED 5, `C:\ProgramData\Stager` (CURRENT/PENDING/releases) denegados, TaskCache denegado; `C:\stager` listing Hidden-only pero `install-stager.ps1` y `stager-target.yaml.example` legibles por path (icacls `/inheritance:r` grant Administrators+SYSTEM confirmado en fuente del instalador); (7) drain PASS re-confirmado (último job `echo-forge-full-golden-20260905T221730Z`); (8) `C:\SQX` inexistente, `C:\stager_old` existente; (9) stageo del inspector verificado byte-exacto (sha256 local == remote, 3373 B); (10) recovery `docker restart ssh-mcp` tras 503 pool-64 con `/status` healthy + `connections:[]` previos (diagnóstico antes del restart).
- **Resultado observable:** capability restaurada PARCIALMENTE — todo el plano observable sin elevación quedó demostrado con canal certificado; el paso 0 (hash del ejecutable en ejecución, CURRENT/releases, presencia de la tarea) queda instrumentado (inspector stageado) y owner-gated. Convergencia 0.2.98: **UNKNOWN** hasta ejecución del inspector; receta bifurcada por decisión de modelo (stager aceptado vs `C:\SQX` canónico) en el OWNER ACTION BUNDLE.
- **Limitaciones de la evidencia:** sin elevación no hay SHA256 del running ni lectura de `C:\ProgramData\Stager`; la ausencia de `StagerReconcile` es "no visible por dos APIs", no demostración absoluta (TaskCache denegado); el valor de `ENV` para el start canónico sigue sin documentar en repo (parámetro owner).

## Evaluación

- **Correctness:** cada afirmación cerrada contra la autoridad que la posee (registro para el servicio, netstat/Get-Process para el runtime, listing completo de schtasks para la tarea, ACL/installer para el boundary); fail-closed respetado; prohibiciones del brief intactas (no Stager disable/stop, no segundo worker, no ETCD, no campañas, no CERT-F04-01).
- **Autonomy:** reutilizados helper de sesión certificado, canal `sftp-upload` certificado y recovery documentado; cero re-implementación de transporte; cero perfiles/keys nuevos (opción C como inspector, no como ampliación de permisos).
- **Efficiency:** 4 sesiones MCP únicas (viewer, operator×3 fases) + upload; el barrido de identidad reusó las denegaciones ya conocidas como clasificación, no como reintentos.
- **Tool use:** `aranea-ssh` viewer/operator con lecturas allowlist + `sftp-upload`; `mcps-ops` sólo para gestión del plane (lecturas + restart documentado); ningún secreto impreso.

## Resultado

- **Outcome:** success — capability mínima instrumentada y certificada en su alcance; paso 0 owner-gated con bundle exacto; sin cambios de gates ni del plane.
- **Rework posterior:** ninguno. Pendiente owner: ejecutar el inspector elevado y decidir modelo de deployment; luego el manager re-evalúa la convergencia y la autorización de EXEC.
- **Aprendizaje para comparar herramientas:** n/a (sesión operacional de access plane).
