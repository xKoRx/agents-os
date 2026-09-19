---
type: change_log
schema_version: 1
scope: session
created: "2026-09-19"
updated: "2026-09-19"
area: "[[Aranea]]"
project: "[[HERMES — Infrastructure Operations]]"
application:
entities:
  - "[[HERMES — Infrastructure Operations]]"
  - "[[HERMES — ARANEA AUTONOMOUS OPERATIONS]]"
related:
  - "[[provisioning-operator-contract]]"
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

# 2026-09-19-h4-provisioning-enablement

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated + created
- **Archivo(s):**
  - `30-resources/runbooks/provisioning-operator-contract.md` — CREATED (materializado con `materialize_schema_note.py` y completado): contrato del futuro operador de provisioning H4.
  - `30-resources/runbooks/00-index.md` + `30-resources/runbooks/log.md` — ingesta del runbook nuevo (26 curados).
  - `30-resources/aranea/01-topologia/fechas-captura.md` — fila de la auditoría read-only H4 (2026-09-18 22:17 / 2026-09-19 01:17 UTC).
  - `10-projects/Aranea/agentes/HERMES — Infrastructure Operations.md` — objetivo inmediato actualizado a H4 cerrado, matriz de autoridad H4 nueva (familias A–H), gate H4 con resultado, tarea I3.3 DONE, Estado actual y Bitácora con veredicto H4.
  - `80-agents/journal/logs/2026-09-19-h4-provisioning-enablement.md` — este log.

## Motivo

Mandato owner one-shot del 2026-09-18: completar H4 — habilitar y certificar la capacidad administrativa de provisioning (VM Linux y LXC como alcance mínimo; Windows clasificado aparte) para que los proyectos ejecutores aprovisionen infraestructura nueva de forma segura, reproducible y sin bootstrap humano rutinario, sin ejecutar ninguna creación desde este carril.

## Alcance ejecutado (cero mutaciones de infraestructura)

- **Primer gate (publicación):** reconciliación vault↔GitHub por contenido (`git show origin/master:main/<path>` + sha256): 9 archivos H1/H2/H3/W1 `PUBLISHED_IDENTICAL` (último sync 22:04). Nota técnica: el repo espejo usa prefijo `main/` sobre los paths del vault. Sin push directo; pipeline externo vivo; repo local Hermes confirmado como consumidor (behind 46, esperado).
- **Auditoría read-only 5/5 nodos** (probes en `~/aranea/work/h4-provisioning-20260918/probes/`): permisos `pveum` user/token/ACL/perms/roles (token `ariadna@pve!backup-dr`: sólo `VM.Audit`+`VM.Backup` en `/vms`; idéntico al usuario; sin `VM.Allocate`/`VM.Clone`/`Datastore.AllocateSpace` — NO es token de provisioning y no se amplió); `cluster/resources` 59=39+20 exacto con flag template; templates: 3 QEMU (109 win-serv-22 / 117 ubuntu-server / 120 k8s-node-2, todos @hera, local-lvm), 0 LXC locales; `pvesm status/cfg/list` iso+vztmpl; capacidad `df`+`vgs`+`lvs` por nodo; Ceph `-s` desde zeus/hera/kronos; `/etc/network/interfaces` ×5; scan cloud-init (0/39 VMs); rootfs/net0 de los 20 LXCs.
- **Veredictos de capacidad:** pool1 (Ceph) HEALTH_WARN nearfull 87.17% ⇒ NO_GO provisioning sobre pool1; nfs-storage 943G libres ⇒ GO; local-lvm GO en athena/hera (y thinpool-only zeus/kronos); hades GO con cautela (61.95%, sostiene plano MCP).
- **Contrato:** [[provisioning-operator-contract]] (cadena de resolución; rutas R1 clon 117/120 / R2 ISO / R3 `pct create` debian-13; criterio capacidad; protegidos; bootstrap/identidad G5; onboarding G6 con gate backup-BLOCKED; teardown; concurrencia/idempotencia/timeouts; escalamiento).
- **Golden G8:** hijo aislado (sesión fresca, sólo inventario+matriz H2+contrato) resolvió 2 specs (VM Linux `metrics-dev`, LXC `redis-dev`) contra estado vivo real y clasificó 6 negativos (N1 storage protegido NO_GO; N2 pool1 capacidad NO_GO; N3 VMID/IP sin prueba → verificación viva + clasificación; N4 token API sin permisos POLICY_DENIED; N5 backup obligatorio → GO-LIVE BLOCKED; N6 solicitud ambigua → AMBIGUOUS). Cero preguntas al owner sobre datos documentados; cero mutaciones. Verificado por el integrador.
- **Owner action bundle:** NO REQUERIDO — la autoridad existente (SSH/sudo) alcanza para el objetivo enablement; no se pidieron permisos, tokens ni templates nuevos.

## Hallazgos nuevos (para operadores futuros)

1. **Athena no puede consultar Ceph** (`Error initializing cluster client … conf_read_file`): el nodo sin OSD/mon carece de keyring/conf local; consultas Ceph sólo desde zeus/hera/kronos (mons). Registrado como regla operativa en la matriz H4 y contrato.
2. **0/39 VMs con cloud-init** en toda la flota: la automatización de identidad post-clon no existe hoy; el template cloud-init es spec pendiente para un proyecto autorizado (demanda repetida).
3. VG `pve` sin espacio libre en zeus y kronos (0G): cualquier volume nuevo de metadata (no thinpool) en esos nodos exige expansión previa por el ejecutor.
4. El repo espejo GitHub antepone `main/` a los paths del vault — relevante para toda verificación futura vault↔origin.

## No hecho (explícito)

- Ninguna creación/clonación (R1/R2/R3 quedan AUTHORIZED_NOT_EXERCISED).
- Provisioning Windows: NOT_PROVEN (W1 = administración de una VM existente, no creación).
- Template cloud-init: sólo spec, no creación.
- Sin tocar PBS, Backup/DR, red, DNS, DHCP, OPNsense, Pi-hole.
- Sin ampliar permisos del token ni crear identidades.

## Evidencia

- `~/aranea/work/h4-provisioning-20260918/probes/` (authority, storage, ceph, capacidad, red, templates, cloud-init scan, lxc rootfs, vg free).
- Golden G8: transcript del hijo en cache de delegación de la sesión; síntesis en matriz H4 de [[HERMES — Infrastructure Operations]].
- Verificación de publicación: sha256 vault vs `origin/master:main/<path>` (9/9 idénticos).
