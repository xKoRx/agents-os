---
type: agent_memory
schema_version: 1
scope: project
created: "2026-09-17"
updated: "2026-09-18"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
application:
entities: ["[[BACKUP-DR-OWNER-PROJECT]]", "[[BACKUP-DR-DESIGN]]", "[[Aranea]]"]
related: ["[[2026-09-16-R0-reconciliacion]]", "[[2026-09-17-backup-dr-d0-documentation-consistency]]"]
aliases: []
confidence: "high"
memory_state: active
continuity_key: "aranea/backup-dr/documentation-consistency"
supersedes:
superseded_by:
load_policy: "when_project_loaded"
indexable: true
index_priority: high
tags:
  - kind/agent-memory
  - scope/project
  - area/aranea
  - project/backup-dr
  - domain/backup-dr
---

# 2026-09-17-backup-dr-doc-consistency-continuity

## Continuidad

- D0 Backup/DR completado PASS (2026-09-17; workload cerrado — el proyecto Backup/DR sigue ACTIVE, sin session close de owner): saneamiento documental completo del dominio. Estado canónico: `[[2026-09-16-R0-reconciliacion]]` §9 (roadmap R0-R8) + change logs `2026-09-16-backup-dr-r0-reconciliacion` y `2026-09-17-backup-dr-r1-bootstrap-config` + `2026-09-17-backup-dr-d0-documentation-consistency`.
- Regla operativa ganada: **cada instrucción operacional lleva estado** (`DESIGNED — NOT IMPLEMENTED` / `BLOCKED — OWNER GATE` / `VERIFIED` + evidencia). Aplicado en BACKUP-DR-RUNBOOK (§0 VERIFIED R1 + 8 marcadores) y BACKUP-DR-CHECKLIST (§3/§4 condicionados). Patrón transferible a otros dominios de [[Aranea]].
- Histórico se neutraliza **archivo por archivo** (banner HISTORICAL + `indexable: false` + `confidence: low`), nunca sólo en el README de la carpeta: retrieval individual reintroduciría instrucciones muertas. 9/9 legacy marcados en 03-storage/04-backups.
- Los 9 agent-projects usan **un plan vigente por archivo**: los supuestos julio reemplazados (crear PBS 180 → adoptar; docker-observability → ARGUS vm 160; restore sólo-R7 → restore por fase) quedan marcados HISTORICAL inline, preservando el resto del plan como operativo.
- RC-20260917-001 (banner DESIGN_FROZEN dentro de BACKUP-DR-DESIGN) aprobado y aplicado; registro en REQUEST-CHANGES.md.
- **PBS identity conflict resuelto (2026-09-18)**: premisa owner «PBS = VMID 123» refutada por evidencia viva (agent-read kronos+hera 14:22/14:37): **123 = `sqx-hera`** (hera, running) y **180 = `pbs`** (kronos, running). `IDENTITY_CONFLICT` registrado; 0 correcciones documentales (el vault estaba correcto: 123 figura en H0 solo como renombre SQX). R2/adopción PBS 180 sigue bloqueada por gate owner, sin cambios. **Corrección de la tarde (misma fecha)**: la dimensión IP era la discrepancia real — PBS escucha en **192.168.31.123:8007** (PTR pbs.lab.aranea); .180 no tiene host (era IP del plan julio); sqx-hera = .111 (fib_trie guest + PTR). Regla reforzada: VMID ≠ IP, resolver por red/PTR/puerto de servicio. Corregidos RUNBOOK/ap-02/R0/ITER4 + este log. Detalle: change log `2026-09-18-pbs-identity-conflict` (con addendum de la tarde).
- **R2 discovery efectivo (2026-09-18 tarde, mandato owner)**: accesos instalados por el owner demostrados — `~/.ssh/ariadna_pbs` → `ariadna@192.168.31.123` (PBS) y `~/.ssh/ariadna_pve` → `ariadna@<cada nodo>` (5/5), sudo NOPASSWD en PBS y kronos. PBS 4.2.6-1/Debian 13 VIVA pero VIRGEN (0 datastores, solo root@pam, 0 jobs; tasks solo logrotate/aptupdate). F-06 nivel disco OK (`scsi0: local-kronos:vm-180-disk-0`); capacidad: VG local-kronos 567.5G libres, root PBS 38G insuficiente ⇒ LV dedicado propuesto (A1 300G/A2 500G/A3 650G). Huella tier 0 §2 medida live: alloc 660G, used-in-guest ~165-185G/ciclo ⇒ retención 7d+4w+12m ~600G. Decisión 0.2 = REUTILIZAR. Tickets 018/019 siguen `todo` ⇒ bundle owner único en `~/aranea/work/r2-pbs-20260918/` (A datastore, B credenciales token-recomendado, C formalización); cero mutaciones (storage.cfg sha intacto, jobs.cfg vacío). Lección: "accesos disponibles" del owner = buscar keys `ariadna_*` en `~/.ssh/` del día. Hallazgo de cobertura: los data-disks de PG/mongo viven en `iscsi-aranea` con `backup=0` y truenas pasa un disco físico completo ⇒ quedan fuera de vzdump ⇒ su cobertura es por dumps R3, no por PBS. Evidencia: `2026-09-18-r2-pbs-discovery-effective`.
- Pendiente R1 (deuda owner, NO D0): pve-config (subcommand `config` en agent-read), etcd-snapshot (etcd-client + endpoint), pihole-config (api_token FTL v6); automatización (timer/pruning del wrapper r1-backup.sh) y retención = decisión owner. R2 gate: PBS 180 + tickets 018-021.
- **R1.5 ejecutado (2026-09-17, mandato one-shot)**: etcd :2379 SÍ alcanzable desde hermes-vm (corrección del filtro asumido; snapshot cluster viable sin owner); pi-hole .149 está L2-dead (ARP FAILED desde athena) — no es sólo filtrado; DNS LAN hoy resuelve via .31, no 149. Timers frozen instalados (04:00/05:00/SAT 08:30). Pendiente owner: sección `config` en agent-read (root en 5 nodos), acme-stepca.json (root LXC 115), pi-hole (red + token). Detalle: change log `2026-09-17-backup-dr-r15-config-completion`.

## Señales de carga

- Cargar si se trabaja Backup/DR, saneamiento documental de un dominio, o el próximo workload R1.5/R2.

## Próxima acción

- R2 (adopción PBS 180) bloqueada por gate owner; R1.5 (completar unidades gated + automatización) requiere decisión owner sobre canales de acceso. No iniciar sin mandato.
