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

Contrato consumible que describe CÓMO deberá operar un proyecto ejecutor autorizado targets Windows de Aranea (hoy: worker-kronos VM 135 @ kronos, Windows 10 IoT Enterprise LTSC 2024, build 26100, endpoint vivo `192.168.31.128` = `mt5-kronos.lab.aranea.cl`). Habilitación H3 (2026-09-18) + bootstrap W1 (2026-09-18 noche). **Estado de la habilitación: ENABLED — VERIFIED SCOPE (W1 PASS)** — la administración nativa Windows está certificada con alcance explícito a worker-kronos VM 135; este contrato define qué SÍ está demostrado, qué NO, y las condiciones de operación. NO activa ni autoriza operaciones de servicio (eso es del proyecto ejecutor); MT5 permanece fuera de este contrato.

## Autoridad demostrada vs no demostrada (2026-09-18, post-W1)

| Superficie | Estado | Detalle |
|---|---|---|
| **SSH nativo `ariadna-win@192.168.31.128`** | **VERIFIED (W1)** | llave ED25519 `~/.ssh/ariadna_win` con `from="192.168.31.122"` en `C:\ProgramData\ssh\administrators_authorized_keys` (ACL `inheritance:r; SYSTEM:F; Administrators:F`); host key pinneada (`SHA256:OKjlEQRES+YmmLYmq3SS5z4LRtegcD0Xl0mRubZY3us`); alias `worker-kronos` en ssh_config de hermes-vm; token de Administrators completo (S-1-5-114 + S-1-5-32-544); logs en `C:\ProgramData\ssh\logs\sshd.log` |
| Lectura administrativa CIM (servicios, tareas) | **VERIFIED (W1)** | `Get-CimInstance Win32_Service` y `Get-ScheduledTask` PASS por SSH (con `echo-dev` siguen denegadas 0x80041003) |
| Lectura básica como `worker-kronos\echo-dev` (MCP viewer/operator) | **VERIFIED** | `whoami` OK viewer+operator (23:16 UTC); write-path operator cert 2026-09-11/17 vigente |
| Enforcement viewer | **VERIFIED** | `run-command` en viewer `mt5-kronos` → POLICY_DENIED (consistente H2-fix 2.8.0) |
| WMI/CIM con `echo-dev` | **DENIED** (by design) | Access denied 0x80041003 — echo-dev es usuario estándar; usar el canal W1 para administración |
| WinRM / PowerShell Remoting | **NOT PROVISIONED** | no instalado (5985/5986 cerrados); no activar por iniciativa propia |
| Inspección host-mediated read-only | **VERIFIED** | `qm guest cmd 135 ping/get-osinfo` vía `ssh ariadna@kronos` + sudo (canal nativo, sin MCP); `qm guest exec` requiere autorización de mutación si se usa para escribir |
| Firewall/listener | VERIFIED (preexistente) | regla "OpenSSH SSH Server (sshd)" In/Private/TCP22/RemoteIP Any preexistente al bootstrap W1 (dependencia del plano consumer .161: la conexión .161→:22 estaba viva antes, durante y después de W1); W1 NO añadió reglas — su restricción de origen vive en el `from=` de la llave |
| Publisher de evidencia (Task Scheduler SYSTEM cada 5 min) | **VERIFIED** (cert 2026-09-17 vigente) | camino agent-facing: JSON publicado → lectura `echo-dev` RO; freshness ≤15 min; NO es canal de gestión |

**WINDOWS NATIVE MANAGEMENT = CERTIFIED, scope worker-kronos VM 135 únicamente.** No extrapolar a otras Windows de la flota. MT5, Task Scheduler writes y Windows productivo permanecen fuera de alcance sin gate owner. El acceso de W1 equivale a administrador local: la restricción de origen NO reduce sus permisos dentro del guest.

## Procedimiento (con lo disponible)

1. Resolución de target por inventario (VM 135 @ kronos, running, endpoint `192.168.31.128`); nunca por nombre suelto ni por IP memorizada sin verificar DNS/qm.
2. Administración nativa W1: `ssh worker-kronos "<PowerShell>"` desde hermes-vm (alias en ssh_config; llave `ariadna_win`; host key pinneada — NO aceptar keys nuevas del target; `from=` bloquea orígenes ≠ .122). Toda operación respeta el alcance del gate del proyecto ejecutor: lecturas libres; escrituras (servicios, tareas, registro, usuarios, firewall) sólo dentro de la autoridad que ese proyecto tenga delegada.
3. Inspección read-only sin SSH: primero `qm guest cmd 135` (nativo, host-mediated); luego plano MCP (`mt5-kronos` viewer para lectura, `mt5-kronos-operator` para write-path `echo-dev`); luego evidence JSON del publisher como fuente de superficie/health. El plano MCP es CONSUMER_PLANE: para administración usar W1.
4. Toda lectura por MCP respeta el boundary del perfil: viewer = sólo read-command; POLICY_DENIED y Access Denied son boundaries válidos, no errores a "resolver" elevando permisos por cuenta propia.
5. MT5 / datos de negocio: fuera de este contrato en cualquier circunstancia ([[Echo]] y proyectos de trading tienen su propio carril GATED).

## Validación

- Lectura: identidades y estados contrastados en dos fuentes cuando existan (qm guest cmd vs MCP vs evidence JSON); contradicción = investigar.
- Publisher: `generated_at_utc` ≤ 15 min y `partial=false` antes de usar el JSON como evidencia de superficie; STALE ⇒ UNKNOWN, no inferir salud.
- Registrar evidencia (timestamp, canal, comando, salida recortada) en el proyecto ejecutor.

## Rollback / recuperación

- Break-glass: consola Proxmox del owner sobre VM 135 (noCanvas/VNC) — única ruta garantizada si SSH/WinRM/MCP fallan a la vez.
- Revoke del canal W1 (minutos, sin destruir nada): `Disable-LocalUser -Name 'ariadna-win'` (reversible con Enable) o vaciar `C:\ProgramData\ssh\administrators_authorized_keys` (la ACL sobrevive). Ejecutable por el owner por consola o por Ariadna con gate.
- Rollback completo W1 (RB-01/02/03, método primario NO depende del canal nuevo — vía `ssh ariadna@192.168.31.120` + `qm guest exec`): `Remove-LocalUser -Name 'ariadna-win'` + `Remove-Item C:\ProgramData\ssh\administrators_authorized_keys -Force` (en el baseline no existían) + limpieza local en hermes-vm (`~/.ssh/config` bloque worker-kronos, `known_hosts` entrada .128, `~/.ssh/ariadna_win*`). Verificación post-rollback documentada en `~/aranea/work/w1-windows-native-20260918/README.md`.
- Rollback publisher: `aranea-evidence-rollback2.bat` materializado (SHA verificado), sólo elevado y autorizado por owner; no rutina.
- Si ssh-mcp está degradado: registrar incidente y operar por canales nativos/qm guest cmd/SSH W1; su reparación pertenece a [[HERMES — Agent Access Operations]].

## Especificación de habilitación pendiente (resumen)

Ninguna pendiente para worker-kronos: **el owner bundle W1 fue EJECUTADO y certificado el 2026-09-18 noche** (mandato owner; transporte OpenSSH reutilizado; identidad `ariadna-win`; llave `from=.122`; alcance VM 135). Resto de la flota Windows sigue sin canal propio y requiere su propio gate. Detalle de ejecución, mutaciones exactas, evidencia y rollback: `~/aranea/work/w1-windows-native-20260918/` + change log `2026-09-18-w1-windows-native-bootstrap`.

## Evidencia

- `~/aranea/work/w1-windows-native-20260918/` — bootstrap W1 completo: README (estado pre, mutaciones, rollback), `evidence_certification.md` (positivos/negativos/logs/post-estado), `discovery/` (JSON crudos qm guest exec pre/post), `W1_INSTALL_IDEMPOTENT.ps1` (sha256 `26bf13f6…`), `g4/` (golden hijo fresco 10/10 PASS `mcp_calls=0`).
- `~/aranea/work/h3-enablement-20260918/evidence/g2_windows_mcp_probes_20260918.md` (9 probes 2026-09-18, con resultados y clasificaciones).
- `qm guest cmd 135 ping/get-osinfo` vivos (g1_qemu_agent_probe, 23:21 UTC).
- Certificaciones vigentes no repetidas: SQX/worker-kronos MCP (runbook aranea-ssh-mcp), publisher (2026-09-17).
