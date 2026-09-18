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

# 2026-09-18-h2-proxmox-enablement

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated + created
- **Archivo(s):**
  - `10-projects/Aranea/agentes/HERMES — Infrastructure Operations.md` — objetivo inmediato actualizado a H2, matriz de autoridad H2 nueva (resumen por familia), tareas I3.1 marcada DONE, Estado actual y Bitácora con veredicto H2, handoff al ejecutor.
  - `30-resources/runbooks/proxmox-lifecycle-operator-contract.md` — CREATED: contrato consumible del futuro operador Proxmox (canales, target proof, recursos protegidos, concurrencia, timeouts/parciales, validación, rollback, abort).
  - `30-resources/runbooks/00-index.md` + `30-resources/runbooks/log.md` — ingesta del runbook nuevo (22 curados).
  - `30-resources/aranea/01-topologia/fechas-captura.md` — fila de la auditoría read-only H2 (20:41–21:02 UTC, drift 0).
  - `80-agents/journal/logs/2026-09-18-h2-proxmox-enablement.md` — este log.

## Motivo

- Mandato owner H2 (2026-09-18): habilitar la capacidad administrativa Proxmox para que un proyecto ejecutor opere lifecycle de VMs/LXC sin bootstrap humano rutinario. Carril exclusivamente de habilitación: cero operaciones de infraestructura. Complementa H1 (Backup & Storage enablement) sin tocar sus resultados.

## Fuentes usadas

- `[[HERMES — Infrastructure Operations]]`, `[[HERMES — ARANEA AUTONOMOUS OPERATIONS]]`, `[[BACKUP-DR-OWNER-PROJECT]]`, change log `2026-09-18-h1-enablement`, inventario `inventory_59.json` (run h0-20260918-r1), secretos por referencia (`~/aranea/secrets/.f04-pve-token.json`).
- Auditoría read-only en vivo (evidencia fuera del vault, `~/aranea/work/h2-enablement-20260918/`): SSH sweep ×5 nodos (pveversion 8.4.20 5/5, quorum Quorate 5/5, storage.cfg 10 storages, ACL/roles/usuarios/tokens, sudoers `90-ariadna-pve` 5/5, `authorized_keys` con `from=192.168.31.122`, configs de guests protegidos 108/111/123/135/145/180, listsnapshots = 0 snapshots, ha-manager sin recursos, datacenter.cfg vacío); API probe con token (19 endpoints GET): 200 reales (`/version`, `/cluster/resources` 59 guests, `/nodes`, per-VM status/config/agent/snapshot-GET, `/nodes/{n}/network` lectura, `/cluster/tasks` filtrado), 403 reales (`/cluster/status`, `/cluster/backup`, `/cluster/ha`, `/nodes/{n}/status`), 200-filtrado-vacío (`/storage`, `/nodes/{n}/storage`, `/pools`); Ceph HEALTH_WARN (osd.0/osd.2 nearfull, pools pool1 y .mgr nearfull, 129 pgs active+clean).

## Resolución aplicada

- Matriz H2: 34 operaciones clasificadas en familias A–G (9 `AUTHORIZED_AND_VERIFIED`, 24 `AUTHORIZED_NOT_EXERCISED`, 1 `OUT_OF_SCOPE` = destroy con gate owner; ninguna PARTIAL ni BLOCKED). CSV completo: `~/aranea/work/h2-enablement-20260918/h2_authority_matrix.csv`.
- Separación explícita API-token vs SSH root-equivalent: el token queda limitado a lectura per-VM (`VM.Audit`/`VM.Backup` en `/vms`, verificado usuario y token con permisos idénticos); todo lifecycle SSH/sudo existe como root-equivalent y queda NO EJERCIDO (correcto: H2 no ejecuta).
- Hallazgo técnico nuevo registrado: PVE filtra por permiso devolviendo 200 con lista vacía en `/storage`, `/cluster/tasks` y `/pools` — un 200-filtrado no prueba vacío real ni permiso; queda como regla en el contrato del operador.
- G4 sesión fresca Ariadna (hijo aislado, read-only): resolución de `sqx-hera` desde inventario (VM 123 @ hera, running) con verificación viva API+SSH (uptimes coincidentes), ACL/rol leídos en vivo (`AriadnaVMBackup` = `VM.Audit,VM.Backup`, privsep=1), negativo demostrado: POST start/shutdown con el token → 403 `VM.PowerMgmt` (sin ejecución), clasificación de operaciones por canal y management independence (cero llamadas MCP). Resultado resumido en la nota del proyecto; reporte y transcript en `~/aranea/work/h2-enablement-20260918/` (`g4_report.md`, `g4_child_transcript.log`).
- Correcciones post-G4 (integrador): identidad exacta de críticos verificada en vivo — LXC `mcps` = VMID **113** @ hades (192.168.31.219, onboot=1) y hermes-vm = VM **118** `agent` @ kronos (una suposición previa "201" sin evidencia fue corregida en matriz y contrato); anómalo registrado: `sqx-hera` (123) arrastra **2 discos `unused`** (`pool1:vm-123-disk-0`, `local-lvm:vm-123-disk-0`) — huérfanos que distorsionan accounting de storage y el comportamiento futuro de un destroy; matiz del hijo: `vzdump` con este token es parcial (`VM.Backup` presente pero endpoint de nodo puede exigir privilegios adicionales no verificados — sin garantía hasta que lo ejerza el ejecutor).
- Reconciliación documental: secciones Boundary/Acceptance/Estado/Tareas del proyecto re-leídas bajo el principio enablement-only ya vigente desde H1; H2 queda certificado como habilitación; sin reescritura de historia (logs H0/H1 intactos).

## Validación

- Zero infrastructure mutations: ningún start/stop/create/destroy/snapshot/config-change; ningún restart de servicios; ningún login UI; secretos nunca impresos (token leído de disco, referencias por nombre).
- Cruce API↔SSH consistente: 59 guests (39 qemu + 20 lxc) y estados por nodo coinciden con inventario H0.
- Publicación vault→GitHub verificada: al inicio del mandato los 4 archivos H1 estaban en `origin/master` byte-idénticos (productor al 17:57 -03; el estancamiento de las 17:02 ya se había resuelto); tras la edición H2, el delta completo (7/7 archivos incluido el runbook nuevo y el change log) confirmado byte-idéntico en `origin/master` (`c9230ba`, 18:12 -03). Repo local Hermes fast-forwardeado; jamás push directo.
- Handoff: `30-resources/runbooks/proxmox-lifecycle-operator-contract.md` + matriz H2 listos para consumo del proyecto ejecutor futuro; sin owner action bundle (la autoridad existente alcanza para el objetivo enablement de H2).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos (las rutas `~/aranea/...` son referencias de workspace del runtime Hermes ya usadas por la nota del proyecto; ningún valor de credencial).

## Rollback

- Cambio exclusivamente documental: revertir = restaurar versiones previas de los archivos tocados (git del productor vault→GitHub mantiene historia; el repo local `~/workspace/agents-os-repo` es consumidor). Sin efectos sobre infraestructura.
