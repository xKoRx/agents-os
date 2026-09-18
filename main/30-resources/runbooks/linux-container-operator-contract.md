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
  - "[[proxmox-lifecycle-operator-contract]]"
  - "[[windows-operator-contract]]"
  - "[[service-lifecycle-operator-contract]]"
  - "[[HERMES — Agent Access Operations]]"
aliases:
  - linux container operator contract
  - contrato operador Linux
  - H3 linux operator contract
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
  - tech/linux
---

# linux-container-operator-contract

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

Contrato consumible que describe CÓMO deberá operar un proyecto ejecutor autorizado la administración de guests Linux, LXCs, Docker/Compose y systemd en Aranea. Habilitación H3 (2026-09-18); este contrato NO activa ni autoriza operaciones: la autoridad nace del proyecto ejecutor y de sus gates propios. La autoridad por target vive en la matriz H3 (`~/aranea/work/h3-enablement-20260918/h3_matrix.csv`, resumen en [[HERMES — Infrastructure Operations]]).

## Canales y autoridad por target (clasificación H3, 2026-09-18)

| Target | Canal | Identidad | Autoridad demostrada | Dependencia MCP |
|---|---|---|---|---|
| Nodos PVE ×5 (como dependencia de guests) | SSH `ariadna@<nodo>` + sudo | ariadna key `ariadna_pve` | root-equivalent (H2); `qm guest cmd` = inspección inside-guest read-only host-mediated | ninguna |
| mcps (LXC 113 @ hades) | SSH `hermes-ops@mcps` + sudo | key `agent_mcps_ops` | root-equivalent leído (docker 26 conts vía sudo; grupo docker NO asignado) | ninguna |
| daedalus (.75, LXC 141) | MCP `docker-echo-dev-operator` (root, SOLO DEV) | echo-dev plane key | root DEV certificado 2026-09-13/17; nativo `daedalus-ops` SIN sudo ni grupo docker (`ACCESS_NOT_PROVISIONED`) | sí (CONSUMER_PLANE) |
| truenas (VM 145) | SSH `ariadna@.91` + sudo + WS DDP FULL_ADMIN | keys `ariadna_truenas` / api-key | root-equivalent + admin NAS (H1) | ninguna |
| pbs (VM 180) | SSH `ariadna@.123` + sudo | key `ariadna_pbs` | root-equivalent (H1) | ninguna |
| hermes-vm (VM 118) | local/self + `systemd --user` | runtime | recovery runbook vigente | ninguna |
| SQX ×3 (108/111/123) | MCP `sqx-zeus|hera|kronos` operator (`echo-dev`, sin sudo) + `qm guest cmd` host-mediated | echo-dev | operator write-path no-root (cert 2026-09-13); inspección read-only vía nodo | MCP sí; host-mediated no |
| echo PROD (.71/140) | MCP `echo-runtime-prod` viewer RO | echo-dev sin sudo | RO estricta (cert 2026-09-15); mutación POLICY_DENIED por diseño | sí (CONSUMER_PLANE) |
| Resto guests Linux running | sin canal propio hoy (`UNKNOWN/NO_CHANNEL`); algunos con qemu-guest-agent utilizable vía nodo | — | `qm guest cmd` disponible sólo donde `agent: 1` (vm128/155/154 verificados sin agent) | ninguna |

## Precondiciones

- Resolución inequívoca del target `nombre lógico → VMID + nodo + estado` contra el inventario vigente (H0 o posterior); ambigüedad = abortar.
- Confirmar el estado STOPPED_EXPECTED antes de inferir fallo: un guest detenido esperado NO es incidente ni requiere encendido para certificar.
- Canal según tabla anterior; si el target sólo tiene canal MCP, la operación NO puede usarse como recovery del propio plano MCP (management path nativo obligatorio para recovery, [[HERMES — Infrastructure Operations]]).
- En mutaciones dentro de un guest: autorización operativa del proyecto ejecutor + captura de estado pre (config/snapshot de config, versión de compose, unit file) como base de rollback.

### Recursos protegidos

- VMs SQX sobre `local-sqx-*` (108/111/123) y worker-kronos (135): discos `backup=0`, sin snapshots — ver contrato Proxmox; dentro del guest aplica doble cuidado (sin rebuilds de disco, sin cambios de firewall).
- echo PROD (.71): viewer RO; jamás reiniciar servicios desde el canal viewer (POLICY_DENIED correcta); cualquier operación es del ejecutor Echo con su propia autoridad.
- plano MCP en mcps (contenedores `*-mcp*`): su ciclo de vida es de [[HERMES — Agent Access Operations]] — un ejecutor de servicios NO reinicia ssh-mcp ni hermanos como efecto lateral; recovery del plano por `mcps-ops` según runbook.
- Ceph y storages: fuera de este contrato (H2/H5).

## Procedimiento

1. Elegir canal en este orden: (1) canal nativo SSH propio del target si existe; (2) canal host-mediated `qm guest cmd` desde el nodo PVE para inspección read-only; (3) plano MCP ssh-mcp para operación con identidad de consumidor (`echo-dev`); (4) consola PVE del owner como break-glass. La observabilidad (MCP observability-ro) complementa pero NO sustituye el management path.
2. Docker en mcps: siempre `sudo -n docker ...` (hermes-ops no está en el grupo docker); jamás añadir el usuario a grupos como efecto lateral de una tarea.
3. Docker en .75: root DEV sólo por el perfil MCP dedicado; NO crear compose paralelo ni `compose up -d` rutinario (hash drift de Portainer); seguir runbook Flink para ciclo del stack.
4. systemd system: `systemctl status/is-active/journalctl` primero; restart sólo con pre-state capturado, ventana y validación del servicio (puerto/proceso/health), jamás `--force` ni `reset-failed` como martillo.
5. systemd user (hermes-vm): `systemctl --user`; recovery completo por [[hermes-linux-update-recovery]].
6. Escritura de configuración en guests: backup pre con timestamp, cambio mínimo, readback, validación semántica por la capa que posee el estado (proceso/puerto/endpoint), registro en el proyecto ejecutor.
7. Concurrencia: un operador por guest; composits y restarts de un mismo stack serializados; no operar el mismo VMID simultáneamente con el contrato Proxmox (coordinar con el ejecutor de lifecycle).
8. Timeouts y parciales: toda mutación con timeout explícito; estado parcial = diagnosticar por estado real (no reintentar a ciegas) según la regla de continuidad (efecto incierto no se repite sin prueba durable de que no ocurrió).
9. Idempotencia: preferir operaciones declarativas (config set, unit enable) verificables; create/destroy exigen verificación de existencia previa.

## Validación

- Post-change por capa semántica: servicio UP = puerto escuchando + health del servicio + (si aplica) consumidor real; un exit 0 NO valida.
- Contrastar dos fuentes cuando existan (SSH dentro del guest vs `qm guest cmd` vs observabilidad); contradicción = investigar, no promediar.
- Registrar el cambio y la evidencia (timestamp, target, canal, comando, salida) en el proyecto ejecutor; devolver hallazgos de canon a [[HERMES — Infrastructure Operations]].

## Rollback / recuperación

- Config de guest: reaplicar backup pre capturado.
- Servicio: operación inversa (start/stop) + validación; tras caída no planificada, journalctl ANTES de cualquier reintento.
- Docker: usar imagen/tag/compose previos documentados; en mcps, jamás `docker system prune` como "limpieza" (borra volúmenes dangling del plano).
- Acceso: llaves nativas en `~/.ssh/` de hermes-vm (`from=192.168.31.122`); si hermes-vm muere, el owner reinstala por consola física; consola PVE del owner = break-glass universal de guests.
- Abort y escalamiento al owner: target ambiguo, recurso protegido involucrado, secreto expuesto, efecto fuera de scope, resultado incierto tras un reintento.

## Evidencia

- Matriz H3 por target + superficies A–H: `~/aranea/work/h3-enablement-20260918/` (`h3_matrix.csv`, `h3_surfaces.csv`, `evidence/`); G4 golden read-only en `g4/`.
- Change log: `80-agents/journal/logs/2026-09-18-h3-guest-service-enablement.md`.
- Estado vivo revalidado 2026-09-18: 59 guests (42 running), canales nativos PVE/TrueNAS/PBS/mcps 5/5 con sudo, daedalus sin sudo, qemu-guest-agent verificado vivo en 111/118/123/135/138.
