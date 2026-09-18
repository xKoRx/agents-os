---
type: change_log
schema_version: 1
scope: session
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Aranea]]"
project: "[[HERMES — Infrastructure Operations]]"
application:
entities:
  - "[[HERMES — Infrastructure Operations]]"
  - "[[HERMES — ARANEA AUTONOMOUS OPERATIONS]]"
related:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/aranea
  - project/hermes-aranea-autonomous-operations
  - domain/infrastructure
---

# 2026-09-18-h3-guest-service-enablement

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `30-resources/runbooks/linux-container-operator-contract.md` — CREATED: contrato del futuro operador Linux/containers (canales por target, Docker/systemd, recursos protegidos, rollback, abort).
  - `30-resources/runbooks/windows-operator-contract.md` — CREATED: contrato del futuro operador Windows (demostrado vs NOT CERTIFIED, canales, spec W1).
  - `30-resources/runbooks/service-lifecycle-operator-contract.md` — CREATED: contrato del futuro operador de servicios (systemd/Docker/Task Scheduler, ownership, validación semántica, rollback).
  - `30-resources/runbooks/00-index.md` + `30-resources/runbooks/log.md` — ingesta de los 3 contratos (22→25 curados).
  - `30-resources/aranea/01-topologia/fechas-captura.md` — fila de sondeos read-only H3 (23:14–23:31 UTC, drift 0).
  - `10-projects/Aranea/agentes/HERMES — Infrastructure Operations.md` — matriz H3, gate H3 (veredicto PARTIAL), I3.2, Estado actual, Bitácora, objetivo inmediato.
  - `80-agents/journal/logs/2026-09-18-h3-guest-service-enablement.md` — este log.

## Motivo

- Mandato owner H3 (2026-09-18): habilitar y certificar las capacidades administrativas de Ariadna sobre guests Linux/Windows, Docker, systemd y servicios, para que los proyectos ejecutores las consuman sin intervención humana rutinaria. Carril exclusivamente de habilitación: cero operaciones de infraestructura, cero instalaciones, cero activaciones (SSH/WinRM), cero cuentas/keys/roles nuevos.

## Fuentes usadas

- Canon: [[HERMES — Infrastructure Operations]] (matrices H1/H2 vigentes), [[proxmox-lifecycle-operator-contract]], runbook aranea-ssh-mcp, inventario/service-map H0 (`~/aranea/work/h0-20260918/A/`), change logs H1/H2 del día, secretos por referencia (llaves `~/.ssh/ariadna_*`, `agent_mcps_ops`, `agent_daedalus_ops`).
- Sondeos read-only en vivo (evidencia fuera del vault, `~/aranea/work/h3-enablement-20260918/`): sweep nativo SSH (truenas/pbs/mcps/daedalus + self: id, sudo, docker, systemd); `cluster/resources` revalidado (59 = 39 qemu + 20 lxc = 42 running + 17 stopped, exacto vs H0); qemu-guest-agent (`qm config` agent flag + `qm guest cmd` ping/get-osinfo vivo en 123/111/135/138/118); probes MCP Windows (9 eventos list-connections/read/run/negativos/CIM); config sqx-hera (discos unused reconfirmados intactos).

## Resolución aplicada

- **G1 Linux:** canales nativos revalidados 4/4 + self (sudo NOPASSWD en truenas/pbs/mcps; daedalus `hermes-ops` SIN sudo — consistente H0). Hallazgo: en mcps `hermes-ops` NO pertenece al grupo docker (grupo existe `docker:x:991` vacío) pero `sudo -n docker ps` lee 26 contenedores — Docker administrable por nativo vía sudo. Muestra de guests Linux demostrada por canal host-mediated `qm guest cmd` (sqx-hera 123 con get-osinfo completo; sqx-kronos 111 y kafka-kronos 138 ping) — canal nativo SIN SSH propio del guest; disponible sólo donde `agent: 1` (vm128/155/154 verificados sin agent).
- **G2 Windows:** probes MCP (viewer+operator): `whoami` OK; negativo viewer run-command POLICY_DENIED (enforcement correcto); `Get-CimInstance` y `Get-ScheduledTask` (CIM) **Access denied 0x80041003/CimJob_BrokenCimSession** ⇒ `worker-kronos\echo-dev` es usuario estándar sin admin; schtasks RPC no ejercido (guard del cliente, UNKNOWN). Canal nativo Windows demostrado a nivel inspección: `qm guest cmd 135 ping/get-osinfo` (Windows 10 IoT Enterprise LTSC 2024). **WINDOWS NATIVE MANAGEMENT = NOT CERTIFIED** (SSH/WinRM/admin delegado ACCESS_NOT_PROVISIONED; no se instalaron).
- **G3 superficies:** matriz A–H completa (`h3_surfaces.csv`): Docker (mcps VERIFIED read vía sudo; .75 heredado cert vigente; Compose NOT_EXERCISED), systemd system (read VERIFIED 4 targets), systemd user (VERIFIED, G4 ejercitó show/is-active), Task Scheduler (NOT CERTIFIED), filesystem/logs/recovery según canal; observabilidad heredada vigente (no duplicada).
- **G4 sesión fresca** (hijo aislado, verificado por integrador en artefactos `g4/`): 5/5 casos PASS — sqx-hera 123@hera, mcps 113@hades (LXC por DNS directo), hermes-gateway-ariadna.service (systemd --user, MainPID 915), host Docker mcps (docker ps -a con estados), worker-kronos 135@kronos — resolución nombre→VMID→nodo desde inventario vivo, `mcp_calls=0`, `mutations=0`, management independence demostrada (Linux Y Docker 100% nativos), cero secretos.
- **Anomalía existente reconfirmada, no tocada:** sqx-hera (123) conserva `unused0: pool1:vm-123-disk-0` y `unused1: local-lvm:vm-123-disk-0` (prohibido modificarlos por mandato; ejecutor futuro decide con owner).
- **Owner bundle único** (`owner_bundle_draft.md`): W1 Windows admin nativa (DECISION+SEED: usuario delegado + WinRM/OpenSSH scoped a 192.168.31.122, verificación positiva/negativa, revoke); L1 daedalus docker-grupo/sudo-scoped (opcional, DEV); L2 qemu-guest-agent en guests sin agent (política, ejecutable por ejecutor). No se re-solicitan accesos H1 ni plano MCP.

## Veredicto

**H3 PARTIAL — LINUX ENABLED / WINDOWS BLOCKED (admin nativa no certificada).** Linux, LXC, Docker (mcps) y systemd quedan habilitados con canales nativos demostrados y contratos consumibles; Windows carece de management nativo (quedará PASS cuando el owner ejecute W1 o un carril autorizado lo provisione). Cero mutaciones de infraestructura; única escritura = documentación Agents-OS + evidencia local no secreta.

## Siguiente exacta

Owner decide W1 (y opcionalmente L1/L2) desde `~/aranea/work/h3-enablement-20260918/owner_bundle_draft.md`. H4 (provisioning enablement) NO se inicia por iniciativa propia.
