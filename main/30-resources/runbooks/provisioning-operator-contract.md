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
  - "[[linux-container-operator-contract]]"
  - "[[windows-operator-contract]]"
  - "[[service-lifecycle-operator-contract]]"
  - "[[BACKUP-DR-OWNER-PROJECT]]"
aliases:
  - provisioning operator contract
  - contrato operador provisioning
  - H4 provisioning contract
confidence: high
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/area
  - area/aranea
  - action/provisioning
  - tech/proxmox
---

# provisioning-operator-contract

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

Contrato consumible que describe CÓMO deberá provisionar (crear) infraestructura nueva — VM Linux, LXC y a futuro Windows — un proyecto ejecutor autorizado en el clúster Proxmox `aranea` (athena .10, zeus .100, hera .110, kronos .120, hades .90; PVE 8.4.20). Habilitación H4 (2026-09-18): este contrato **NO autoriza ni ejecuta provisioning por sí solo** — la autorización operativa nace del proyecto ejecutor y de sus gates propios. REUSE > EXTEND > CREATE: hereda [[proxmox-lifecycle-operator-contract]] (canales, target proof, protección de recursos, rollback) y [[linux-container-operator-contract]] (guests Linux); este contrato añade sólo la capa de CREACIÓN que aquellos no cubren.

- Autoridad del canal: SSH `ariadna@<nodo>` + sudo (root-equivalent, H1/H2). El token API `ariadna@pve!backup-dr` **NO es token de provisioning** (sólo `VM.Audit`+`VM.Backup` en `/vms`; sin `VM.Allocate`/`VM.Clone`/`Datastore.AllocateSpace` — verificado 2026-09-18). No ampliar sus privilegios; provisioning existe vía SSH/sudo y queda `AUTHORIZED_NOT_EXERCISED` (matriz H2, familias C/D).
- Evidencia base y estado vivo al momento del contrato: `~/aranea/work/h4-provisioning-20260918/probes/` (2026-09-18/19 UTC), matriz H4 en [[HERMES — Infrastructure Operations]].

## Clasificación de autoridad H4 (resumen; detalle en matriz H4)

| Operación | Canal | Estado habilitación |
|---|---|---|
| Verificación target/VMID/nodo/storage/red | API (`VM.Audit`; 200-filtrado no probatorio) + SSH/sudo | VERIFIED (lecturas) |
| `qm clone` / `qm create` / `pct create` | SSH/sudo | AUTHORIZED_NOT_EXERCISED |
| `qm set` / `pct set` post-create | SSH/sudo | AUTHORIZED_NOT_EXERCISED |
| Inventario ISO/vztmpl (`pvesm list`) | SSH/sudo | VERIFIED |
| Descargar ISO/vztmpl nuevos (`pveam`, wget a NFS) | SSH/sudo | AUTHORIZED_NOT_EXERCISED — spec del ejecutor |
| `qm template` (convertir en template) | SSH/sudo | AUTHORIZED_NOT_EXERCISED — **NO reversible trivialmente; vetado sobre guests existentes** |
| destroy/teardown | SSH/sudo | OUT_OF_SCOPE salvo recurso creado por el propio ejecutor en la misma tarea (doble target proof) |

## Precondiciones (cadena de resolución obligatoria)

Todo pedido de provisioning se resuelve en esta cadena; saltar un eslabón = abortar:

```
solicitud (servicio X, entorno Y, dueño)
→ autorización del proyecto ejecutor (gate propio; este contrato no autoriza)
→ target proof: nombre lógico inequívoco, entorno, dueño registrado
→ VMID: verificado libre EN VIVO contra `sudo qm list`+`sudo pct list` (todos los nodos) e inventario vigente; colisión = abortar; registrar el VMID elegido durablemente en el registro del ejecutor (H4 NO reserva)
→ nodo: capacidad CPU/RAM medida + colocación (ver tabla Capacidad)
→ storage: espacio real medido EN VIVO (`pvesm status` + `vgs`/`lvs` del nodo) — criterio en sección Capacidad
→ red: bridge correcto (default vmbr0 192.168.31.0/24; casos especiales: vmbr1 @athena, bridge `ceph` — sólo si el servicio lo exige y su spec lo declara)
→ IP: **una IP aparentemente libre NO está disponible** — verificar en vivo (ping sweep del segmento + consulta DNS `*.lab.aranea` + leasa DHCP si aplica); asignación estática documentada por el ejecutor; H4 NO reserva IPs ni toca OPNsense/Pi-hole/DHCP/DNS
→ identidad administrativa: por sección Bootstrap e identidad
→ inventario/Agents-OS: registro canónico post-creación (G6.H) — un guest sin registro está huérfano
```

### Recursos protegidos (intocables — heredado H2/H3, sin excepciones)

- Storages `local-sqx-zeus/kronos/hera`, `local-kronos`, `pool-kronos`: **NO como destino** de provisioning (LVM `nodes`-restricted `shared=0`, discos de negocio `backup=0`). Los discos `unused0/unused1` de sqx-hera (123) NO se utilizan (decisión congelada BACKUP-DR-DESIGN).
- VM TrueNAS (145 @ hades, passthrough by-id), VM PBS (180 @ kronos), plano MCP (CT 113 @ hades), hermes-vm (118 @ kronos): jamás destino, jamás modificados como efecto lateral.
- Los 59 guests existentes: jamás `qm template`, jamás overwrite; teardown sólo con doble target proof + owner salvo recurso propio del ejecutor creado en la misma tarea.

## Capacidad — criterio NO_GO medible (G3, estado 2026-09-18/19)

El ejecutor mide ANTES de crear y registra la medición en su evidencia. Criterio: espacio libre en destino ≥ tamaño del disco nuevo **+ 20% del uso actual del pool/volumen de destino como colchón**; sin esa holgura demostrada = NO_GO.

| Destino | Estado medido 2026-09-18/19 | Veredicto provisioning |
|---|---|---|
| `pool1` (Ceph RBD) | HEALTH_WARN: 2 OSD nearfull + 2 pools nearfull; 87.17% (834G/956.8G; 122.8G avail); PGs active+clean | **NO_GO hasta que el proyecto operativo de Ceph resuelva nearfull** (condición H4; no se repara desde este carril) |
| `nfs-storage` (TrueNAS pool0 → NFS) | 1.4T total, 402G usado, **943G libres** (29.86%) | GO (re-medir en vivo) |
| `local-lvm` @ athena | thinpool 348.8G al 9.02%; VG pve 16G free | GO para discos pequeños/medianos |
| `local-lvm` @ hera | thinpool 337.9G al 27.98%; VG pve 16G free | GO (nodo de los templates) |
| `local-lvm` @ hades | thinpool 53.9G al **61.95%**; VG 14.75G free; root 30% | GO con cautela: sólo discos ≤10G re-medidos; hades sostiene el plano MCP |
| `local-lvm` @ zeus | thinpool 399.9G al 20.33%; **VG pve 0G free** | GO thinpool-only |
| `local-lvm` @ kronos | thinpool 53.9G al 4.46%; **VG pve 0G free** | GO thinpool-only |
| `aranea-pbs` (backup) | NO es destino de provisioning (content backup) | N/A |

Colocación por defecto: hera o athena para clones/VM Linux (templates @hera, VG con holgura); hades sólo cargas ligeras.

## Rutas reales de provisioning (G2 — inventario verificado)

Templates QEMU existentes (los 3 del clúster, todos @hera, todos sobre `local-lvm`):
- **117 `ubuntu-server`** — Ubuntu (creada 2024-06, qemu 8.1.5; 5 vCPU/12244M/32G scsi virtio-scsi-single; agent:1; net0 virtio vmbr0 fw=1). **SIN drive cloud-init** (`ide2 none`): el clone requiere bootstrap in-guest (consola/SSH post-arranque).
- **120 `k8s-node-2`** — misma generación/params, tag kubernetes. Sin cloud-init.
- **109 `win-serv-22`** — Windows Server 2022, OVMF/q35, 8c×2s/32G/120G, `virtio-win-0.1.248.iso` en ide0. **NO usable como ruta de creación Windows hoy** (ver sección Windows).

Hallazgo de flota: **0/39 VMs con drive cloud-init** (scan en vivo 2026-09-18) — la automatización de identidad post-clon es manual o por herramienta del ejecutor hasta que un proyecto autorizado construya un template cloud-init (spec abajo).

ISOs disponibles (`nfs-storage:iso/`, muestra relevante): `debian-12.4.0-netinst`, `ubuntu-24.04.2-live-server` (+22.04.3/25.04/26.04.1), Windows (11 24H2, W10 LTSC 2021, WS2025, W11 IoT LTSC 2024), virtio-win 0.1.240/248/271, PBS/PVE/OPNsense/clonezilla/gparted.
Templates LXC (`vztmpl`): en `nfs-storage`: debian-12 (12.2/12.12), **debian-13 (13.1-2, 13.6-1)**, ubuntu-24.04-2, ubuntu-24.10, alpine-3.21; en `local`: debian-12-standard_12.12.

- **R1 — VM Linux por clon de template 117/120:** `qm clone 117 <vmid-nuevo> --name <nombre> --node hera --storage local-lvm --full` (full clone; linked crearía dependencia del template). Post-clone: `qm set` (cores/mem/net0 estática), arranque, identidad in-guest por consola/`qm guest exec` o SSH con credencial del ejecutor; instalar/activar qemu-guest-agent si falta.
- **R2 — VM Linux por ISO:** `qm create` con `--iso nfs-storage:iso/<debian-12.4-netinst|ubuntu-24.04.2-live-server>` + instalación asistida (consola del ejecutor) o autoinstall vía snippet (nfs-storage soporta `content snippets`). Más lento; usar cuando R1 no calce (otra versión/OS).
- **R3 — LXC por vztmpl (ruta mínima habilitada):** `pct create <vmid> nfs-storage:vztmpl/debian-13-standard_13.6-1_amd64.tar.zst --rootfs local-lvm:<size> --net0 name=eth0,bridge=vmbr0,ip=<ip>/24,gw=192.168.31.1 --unprivileged 1 --ostype debian --hostname <nombre> --cores N --memory M --ssh-public-keys <refs del ejecutor>`. Identidad post-create por `pct exec` (patrón [[linux-container-operator-contract]]). Precedentes de flota: 14/20 LXCs unprivileged en local-lvm/nfs-storage con IP estática vmbr0.
- **Spec pendiente (creación, no ejecución en H4):** template Ubuntu/Debian con cloud-init (`virt-customize`/`cloud-image` + drive `ide2 cloudinit,media=cdrom`) para automatizar identidad post-clon; lo construye un proyecto autorizado cuando exista demanda repetida.

Datos que el ejecutor debe proporcionar en su solicitud: nombre lógico, entorno, VMID elegido+verificado, nodo, storage+size, IP+hostname/DNS deseados (verificados vivos), cores/mem, dueño, necesidad de backup (sí/no + política), canal de administración post-creación.

## Windows (G2.E / estado real)

- W1 certificó **administración nativa de una VM existente** (worker-kronos 135): SSH `ariadna-win`, llave `from=.122`, host key pinneada. **NO certificó creación de VMs Windows.** H4 NO declara provisioning Windows habilitado.
- Existen insumos (template 109 win-serv-22 @hera; ISOs Win11/W10LTSC/WS2025 + virtio-win en nfs-storage), pero la ruta (OVMF+virtio+unattend+identidad admin in-guest) está **sin especificar ejecutable y sin certificar**: creación Windows = NOT_PROVEN. Un proyecto que la requiera produce su spec usando [[windows-operator-contract]] como canal de administración posterior. Lecciones W1 aplicables: verificar VMID/nombre reales, IP viva ≠ IP histórica, admin local = privilegio elevado, `from=` ≠ firewall completo; **no reutilizar automáticamente la llave W1 en otras VMs**.

## Bootstrap e identidad (G5)

- **Cuenta administrativa dedicada por guest** (patrón H1/W1): usuario admin local propio del guest, llave SSH ED25519 dedicada por target (`~/.ssh/ariadna_<target>`), `authorized_keys` con `from="192.168.31.122"` (hermes-vm) donde el SO lo soporte. **No crear identidad root-equivalent compartida para todo Aranea.**
- Host key del guest nuevo se pinea desde fuente independiente (consola PVE / `qm guest exec`) — nunca TOFU puro.
- Secretos por referencia: contraseñas generadas in-guest y descartadas (patrón W1) o bóveda del ejecutor; jamás en vault/evidencia/chat.
- Timezone `America/Santiago`; hostname FQDN `*.lab.aranea` consistente con DNS; actualizaciones iniciales según política del ejecutor.
- Recuperación independiente del MCP: consola PVE del owner = break-glass universal; SSH nativo ariadna = management path; `qm guest cmd` (si agent) = segunda vía de inspección.
- Rotación/revocación: borrar línea de `authorized_keys` del guest (o `Disable-LocalUser` en Windows) + eliminar llave en hermes-vm; registrar en el change log del ejecutor.

## Onboarding obligatorio post-creación (G6 — gate del ejecutor)

Un guest nuevo NO está "entregado" hasta completar:

- **A. Inventario canónico:** alta en `30-resources/aranea` (nodo-doc/servicios) + service map del inventario vigente; VMID+hostname+IP+dueño+rol.
- **B. Acceso administrativo nativo:** identidad de la sección Bootstrap operando, probada positiva y negativa.
- **C. Backup/DR:** si la política del workload exige backup: **GO-LIVE = BLOCKED mientras no exista ruta operativa demostrada** (PBS/R2 de [[BACKUP-DR-OWNER-PROJECT]] conserva su propio estado y gates; a la fecha del contrato PBS sin datastores operativos certificados y 0 jobs PVE). Un workload que acepta vivir sin backup lo declara explícitamente con riesgo asumido por su dueño. H4 no crea backups ni configura PBS.
- **D. Observabilidad ARGUS:** alta del servicio en el plano `aranea-observability-ro` existente (dashboards/labels); H4 no configura ARGUS — define la obligación de onboarding y su verificación (métrica/log del servicio visible).
- **E. Health checks:** comando/endpoint de salud documentado en su nota de servicio.
- **F. Runbook operativo:** nota/runbook del servicio con arranque/parada/logs (o extensión del existente).
- **G. Recovery/revoke:** cómo se recupera el acceso, cómo se revoca identidad y cómo se destruye el recurso (teardown abajo).
- **H. Registro durable:** change log del ejecutor + entrada en la entidad Agents-OS correspondiente.

## Teardown y recuperación

- Sólo recursos creados por el propio ejecutor en su tarea, con doble target proof (VMID+nombre+dueño en su registro) y verificación pre-destroy de que no hay datos sin dueño. `qm destroy`/`pct destroy` con `--destroy-unreferenced-disks 1` sólo si su registro confirma propiedad de los discos.
- Rollback de un provisioning fallido: destruir el recurso parcial propio, re-verificar VMID/IP libres, reintentar con corrección; jamás reutilizar un VMID dudoso sin verificar en vivo.
- Declarar explícitamente la política de backup del disco creado (`qm set`/`pct set`) según el gate C.

## Concurrencia, idempotencia, timeouts, parciales

- Un solo operador de creación por nodo (clone/create son pesados); no crear dos recursos con el mismo VMID/IP en paralelo (verificación viva + registro previo evita la carrera; ante duda, abortar y re-verificar).
- Idempotencia: create/clone/destroy NO son idempotentes — verificar existencia antes (`qm status`/`pct status` + `qm list`/`pct list`); config `set` sí.
- Timeouts explícitos por paso (clone: minutos según size; bootstrap in-guest: minuto a minuto con evidencia); estado parcial = diagnosticar por estado real, no reintentar a ciegas (regla de continuidad).
- Evidencia auditable por operación: timestamp UTC, VMID+nodo, canal, identidad (sin secretos), comando, resultado, task ID, config pre/post, clasificación outcome. Artefactos voluminosos fuera del vault (`~/aranea/work/...`).

## Validación

- La capa que posee la semántica valida: guest arranca (`status/current`), red responde (IP verificada en vivo), identidad admin entra (positivo) y credencial equivocada NO entra (negativo), servicio del guest UP según su rol.
- Contrastar dos fuentes cuando existan (API + SSH + `qm guest cmd`); contradicción = investigar, no promediar.
- Registrar el cambio en el proyecto ejecutor; devolver hallazgos de canon a [[HERMES — Infrastructure Operations]].

## Rollback / recuperación

- Recurso parcial/fallido: destroy del recurso propio + verificación de liberación (VMID/IP/storage).
- Bootstrap fallido in-guest: revertir por consola PVE; si el guest quedó inaccesible, destroy + re-create es el camino (no hay datos aún en un guest recién creado).
- Sin red de seguridad de backups al crear: el rollback de datos NO existe hasta que R2 opere (factor de riesgo dominante, heredado de [[proxmox-lifecycle-operator-contract]]).
- Abort inmediato y escalamiento al owner: target ambiguo, recurso protegido involucrado, quorum perdido, secreto expuesto, resultado incierto tras un reintento, o cualquier efecto fuera del scope autorizado.

## Evidencia

- Auditoría read-only H4 (authority/permisos, templates, ISO/vztmpl, capacidad por nodo, Ceph, red, scan cloud-init/LXC, VG free): `~/aranea/work/h4-provisioning-20260918/probes/` (captura 2026-09-18 22:17 UTC / 2026-09-19 01:17 UTC).
- Matriz H4 y estado del gate: [[HERMES — Infrastructure Operations]]; change log: `80-agents/journal/logs/2026-09-18-h4-provisioning-enablement.md`.
- Estado vivo al momento del contrato: quorum 5/5, 59 guests (39 qemu + 20 lxc), 3 templates QEMU (109/117/120 @hera), 0 cloud-init en flota, Ceph HEALTH_WARN nearfull (pool1 87.17%), 0 jobs backup / PBS sin datastores operativos.
