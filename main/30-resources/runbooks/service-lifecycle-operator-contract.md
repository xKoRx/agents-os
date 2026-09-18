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
  - "[[windows-operator-contract]]"
  - "[[proxmox-lifecycle-operator-contract]]"
  - "[[BACKUP-DR-OWNER-PROJECT]]"
aliases:
  - service lifecycle operator contract
  - contrato operador servicios
  - H3 service operator contract
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
  - tech/systemd
  - tech/docker
---

# service-lifecycle-operator-contract

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

Contrato consumible que describe CÓMO deberá operar un proyecto ejecutor autorizado el ciclo de vida de **servicios** (systemd system/user, Docker/Compose, tareas programadas Windows) sobre los guests de Aranea, después de que el acceso al guest esté resuelto (ver [[linux-container-operator-contract]] y [[windows-operator-contract]]). Habilitación H3 (2026-09-18); este contrato NO autoriza operaciones: la ejecución pertenece al proyecto del servicio (p.ej. Echo/Forge DEV, observabilidad). Este carril NO ejecuta repairs.

## Alcance y superficies

| Superficie | Dónde existe | Canal | Estado H3 |
|---|---|---|---|
| systemd system services | nodos PVE, truenas, pbs, mcps, guests Linux | SSH+sudo (nodos/VMs management) o canal del guest | read VERIFIED 4/4 targets revalidados; mutación NOT_EXERCISED |
| systemd user services | hermes-vm (dashboard, gateway-ariadna) | self `systemctl --user` | VERIFIED |
| Docker Engine | mcps (26 conts, plano MCP), .75 DEV | mcps: `sudo docker` vía mcps-ops; .75: MCP root DEV | mcps read VERIFIED; .75 heredado cert vigente |
| Docker Compose | mcps (Portainer stack 1 declarativo), .75 stacks | según host; compose interno portainer_data | AUTHORIZED_NOT_EXERCISED |
| Task Scheduler Windows | worker-kronos (publisher SYSTEM) | owner/consola (echo-dev sin CIM) | NOT CERTIFIED (ver [[windows-operator-contract]]) |
| Logs/observabilidad | plano observability-ro + journalctl | MCP observability (su función) / SSH | VERIFIED (heredado, vigente) |
| Recovery administrativo | transversal | canales nativos + consola owner | VERIFIED (management independence re-verificada) |

## Precondiciones

- Servicio y guest resueltos desde el catálogo de servicios (service_map H0 o posterior): `nombre lógico → guest/VMID → nodo → canal`; servicio sin guest identificado = abortar consulta de mutación.
- Saber quién posee el servicio: plano MCP (`*-mcp*` en mcps) pertenece a [[HERMES — Agent Access Operations]]; Echo/Forge productivo a su proyecto; el resto al proyecto ejecutor con autoridad explícita.
- Pre-state capturado: `systemctl show` (unit), `docker inspect` (contenedor), versión/hash de compose, o `schtasks /query` — la base del rollback.
- Ventana y blast radius: servicios productivos (echo, kafka, postgres, hasura PROD) exigen ventana del proyecto ejecutor; DEV/observables pueden operar directo según su contrato.

## Procedimiento

1. Preflight: estado actual del servicio + dependencias vivas (puertos, salud) para poder distinguir "estaba roto" de "lo rompí".
2. Reinicio: `systemctl restart <unit>` / `docker restart <c>` / `schtasks /end + /run` — uno a la vez, con timeout explícito; NUNCA reinicios en cadena "por si acaso" (máquina de estados de servicios con dependencias: etcd/kafka/postgres exigen orden de arranque documentado por su proyecto).
3. Durante el restart NO operar en paralelo sobre el mismo guest (coordinar con [[proxmox-lifecycle-operator-contract]] si hay lifecycle simultáneo).
4. Cambio de configuración de servicio: backup pre, cambio mínimo, reload preferido sobre restart cuando la unit lo soporte, validación por la capa semántica.
5. Compose (DEV .75): jamás `compose up -d` como implicit rollback; diff del compose antes de aplicar; Portainer stack 1 en mcps es declarativo — cambios por su dueño (Agent Access Operations).
6. Task Scheduler Windows: con W1 no ejecutado, toda operación es owner-gated; lectura de resultado por evidence JSON del publisher (freshness ≤15 min).

## Validación

- La capa que posee la semántica valida: unit `active (running)` + proceso + puerto + health endpoint + (críticos) consumidor real operando. Un exit 0 o "Active: active" NO prueban el servicio.
- Ventana de observación post-restart (al menos un ciclo del servicio o 60 s para units simples) antes de dar por cerrada la operación.
- Registrar: timestamp, servicio, guest, canal, acción, salida, validación; desviaciones a la bitácora del proyecto ejecutor.

## Rollback / recuperación

- Rollback de restart = esperar/recuperar el estado previo documentado (unit file/imagen/compose previos); rollback de config = reaplicar backup pre.
- Servicio caído post-change: journalctl/logs ANTES de segundo intento; si el servicio no levanta, revertir config y escalar al owner si es productivo.
- Recovery de acceso (no del servicio): [[linux-container-operator-contract]] §Rollback; break-glass = consola PVE del owner.
- Abort inmediato: target ambiguo, servicio de otro dueño (plano MCP/Echo PROD) sin gate, secreto expuesto, resultado incierto tras un reintento, efecto en servicio no objetivo (dependencia no documentada).

## Evidencia

- Superficies A–H con estado por target: `~/aranea/work/h3-enablement-20260918/h3_surfaces.csv`.
- Revalidación viva 2026-09-18: sudo/docker/systemd leídos en mcps, truenas, pbs, hermes-vm; sin mutaciones (ZERO INFRASTRUCTURE MUTATIONS del mandato).
- Change log: `80-agents/journal/logs/2026-09-18-h3-guest-service-enablement.md`.
