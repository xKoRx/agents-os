---
type: runbook
schema_version: 1
scope: area
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Aranea]]"
project: "[[HERMES — Infrastructure Operations]]"
application:
entities:
  - "[[Aranea]]"
  - "[[HERMES — Infrastructure Operations]]"
related:
  - "[[linux-container-operator-contract]]"
  - "[[service-lifecycle-operator-contract]]"
  - "[[proxmox-lifecycle-operator-contract]]"
aliases:
  - windows operator contract
  - contrato operador Windows
  - H3 windows operator contract
confidence: high
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/area
  - area/aranea
  - action/lifecycle
  - tech/windows
---

# windows-operator-contract

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

Contrato consumible que describe CÓMO deberá operar un proyecto ejecutor autorizado targets Windows de Aranea (hoy: worker-kronos VM 135 @ kronos, Windows 10 IoT Enterprise LTSC 2024, build 26100). Habilitación H3 (2026-09-18). **Estado de la habilitación: PARTIAL** — la administración nativa Windows NO está certificada; este contrato define qué SÍ está demostrado, qué NO, y la especificación de habilitación pendiente (owner bundle W1). NO activa ni autoriza operaciones.

## Autoridad demostrada vs no demostrada (2026-09-18)

| Superficie | Estado | Detalle |
|---|---|---|
| Lectura básica como `worker-kronos\echo-dev` (MCP viewer/operator) | **VERIFIED** | `whoami` OK viewer+operator (23:16 UTC); write-path operator cert 2026-09-11/17 vigente |
| Enforcement viewer | **VERIFIED** | `run-command` en viewer `mt5-kronos` → POLICY_DENIED (consistente H2-fix 2.8.0) |
| WMI/CIM (`Get-CimInstance`, `Get-ScheduledTask` vía CIM) | **DENIED** | Access denied 0x80041003 / CimJob_BrokenCimSession — `echo-dev` es usuario estándar sin token admin |
| Task Scheduler (CIM o RPC/schtasks) | **NOT DEMONSTRADO** | CIM denegado; schtasks RPC no ejercido (guard del cliente) — clasificar UNKNOWN, no PASS |
| SSH nativo con llave propia de Ariadna | **ACCESS_NOT_PROVISIONED** | no instalado; no activar por iniciativa propia |
| WinRM / PowerShell Remoting | **ACCESS_NOT_PROVISIONED** | ídem |
| Inspección host-mediated read-only | **VERIFIED** | `qm guest cmd 135 ping/get-osinfo` vía `ssh ariadna@kronos` + sudo (canal nativo, sin MCP) |
| Publisher de evidencia (Task Scheduler SYSTEM cada 5 min) | **VERIFIED** (cert 2026-09-17 vigente) | camino agent-facing: JSON publicado → lectura `echo-dev` RO; freshness ≤15 min; NO es canal de gestión |

**WINDOWS NATIVE MANAGEMENT (nivel administración completa) = NOT CERTIFIED.** No declarar PASS global por tener publisher funcional ni por el plano consumidor MCP (CONSUMER_PLANE_ONLY). MT5, Task Scheduler y Windows productivo permanecen fuera de alcance sin gate owner.

## Procedimiento (con lo disponible)

1. Resolución de target por inventario (VM 135 @ kronos, running); nunca por nombre suelto.
2. Inspección read-only: primero `qm guest cmd 135` (nativo, host-mediated); luego plano MCP (`mt5-kronos` viewer para lectura, `mt5-kronos-operator` para write-path `echo-dev`); luego evidence JSON del publisher como fuente de superficie/health.
3. Toda lectura por MCP respeta el boundary del perfil: viewer = sólo read-command; POLICY_DENIED y Access Denied son boundaries válidos, no errores a "resolver" elevando permisos por cuenta propia.
4. Cualquier operación de gestión (servicios, tareas programadas, usuarios, firewall, registro) = **REQUIERE owner bundle W1 ejecutado** (usuario delegado + WinRM/SSH scoped) o gate owner directo con consola (noCanvas/VNC).
5. MT5 / datos de negocio: fuera de este contrato en cualquier circunstancia ([[Echo]] y proyectos de trading tienen su propio carril GATED).

## Validación

- Lectura: identidades y estados contrastados en dos fuentes cuando existan (qm guest cmd vs MCP vs evidence JSON); contradicción = investigar.
- Publisher: `generated_at_utc` ≤ 15 min y `partial=false` antes de usar el JSON como evidencia de superficie; STALE ⇒ UNKNOWN, no inferir salud.
- Registrar evidencia (timestamp, canal, comando, salida recortada) en el proyecto ejecutor.

## Rollback / recuperación

- Break-glass: consola Proxmox del owner sobre VM 135 (noCanvas/VNC) — única ruta garantizada si SSH/WinRM/MCP fallan a la vez.
- Rollback publisher: `aranea-evidence-rollback2.bat` materializado (SHA verificado), sólo elevado y autorizado por owner; no rutina.
- Revoke de accesos futuros (W1): deshabilitar usuario delegado o regla firewall scoped (owner, minutos).
- Si ssh-mcp está degradado: registrar incidente y operar por canales nativos/qm guest cmd; su reparación pertenece a [[HERMES — Agent Access Operations]].

## Especificación de habilitación pendiente (resumen)

Única spec: owner bundle W1 en `~/aranea/work/h3-enablement-20260918/owner_bundle_draft.md` — usuario local administrativo delegado `ariadna-win` + WinRM (o OpenSSH for Windows) restringido a hermes-vm 192.168.31.122 por firewall/TrustedHosts, verificación positiva/negativa y revoke en minutos. Hasta entonces: **WINDOWS NATIVE MANAGEMENT = NOT CERTIFIED**.

## Evidencia

- `~/aranea/work/h3-enablement-20260918/evidence/g2_windows_mcp_probes_20260918.md` (9 probes 2026-09-18, con resultados y clasificaciones).
- `qm guest cmd 135 ping/get-osinfo` vivos (g1_qemu_agent_probe, 23:21 UTC).
- Certificaciones vigentes no repetidas: SQX/worker-kronos MCP (runbook aranea-ssh-mcp), publisher (2026-09-17).
