---
title: "MATRIZ — 59 guests: placement y cobertura de backup (2026-09-20)"
type: doc
schema_version: 1
status: active
icon: 🗂️
slug: backup-dr-matriz-59-guests
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: 2026-09-20
updated: 2026-09-20
aliases:
  - Matriz 59 guests backup
  - MATRIZ backup DR 2026-09-20
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
  - project/backup-dr
related:
  - "[[MASTER-PLAN-STORAGE-BACKUP-DR]]"
  - "[[ROADMAP-WP-BACKUP-DR]]"
  - "[[BACKUP-DR-CONTRACT]]"
cssclasses:
  - wide
---

# 🗂️ MATRIZ — 59 guests: placement y cobertura de backup

> Derivada de evidencia verificada: `guest-disk-map.json` (59/59, assessment 19-09) + R0 + G1A/G1B + interiors 19-20sep. No repite el master plan: es el denominador operativo. Cambios al scope Tier 0 → contrato regla 4.1 + ticket 018.

## Leyenda

- **Clase**: T0a/T0b/T0c/T0d = contrato §2 · ADD-CRIT/ADD-IMP/ADD-T2/ADD-UNK = propuestas R0 §6 (no aprobadas; requieren 018) · T3/T3-SQX = policy tier 3.
- **Decisión**: KEEP / MIGRATE / DEFER / UNKNOWN sobre el guest completo; el detalle de datos va en mecanismo.
- **Mecanismo**: VZ = vzdump→PBS (activo sólo en piloto R2 hoy; producción post-WP-B1 gated 018/019/D-piloto) · CFG = backup config nivel app (R1/R3) · DUMP = dump lógico cifrado→PBS (G1A/G1B) · SNAP = snapshot ZFS zvol (WP-A6, hoy NO existe) · etcd-snap = snapshot lógico cluster (R1.5 activo) · REC = reconstruible sin backup · NONE = sin protección hoy.
- **Estado hoy (verificado)**: staging→PBS activo = 4 unidades config R1/R1.5 + dumps one-shot G1A/G1B + piloto vzdump 6 CTs (día 2/7). Todo lo demás = gap.

## Resumen por clase

| Clase | Guests | Protección vigente | Gap dominante |
|---|---|---|---|
| T0a/T0b edge+storage | 130,145,149,115 | traefik CFG activo; OPNsense/TrueNAS/pi-hole NINGUNO | export config OPNsense/TrueNAS; pi-hole token + L2-dead |
| T0c quorum | 101,147,154,155,156,148,136,138,139 | etcd-snap cluster diario (5 miembros; 148 cubierto como datos) | vzdump kafka SOs post-D; datos kafka UNKNOWN→018 |
| T0d Echo trading | 124,133,134,144,140,152,153,160,126,129 | PG/Mongo DUMP one-shot VERIFIED (no agendado) | schedules + PITR + vzdump; argus/flink/hasura datos→018 |
| ADD-CRIT | 116,118 | vault + hermes-state CFG activos | CouchDB dump; ingesta staging→PBS |
| ADD-IMP/T2 | 113,103,105,106,157,158,142,141,127,128,132,119,137,180,135 | MinIO DUMP one-shot VERIFIED | MinIO schedule; vzdump flota; HA zvol SNAP |
| T3/SQX | 108,111,123,135 + 12 stopped lab | NONE por diseño (F-04 / tier3) | — (defensión documental, no gap) |
| stopped T3 DEFER | 100,112,151,162,170 | NONE | riesgos latentes LUN2 + RBD huérfana (WP-S1) |

## Matriz 59/59

| VMID | Nombre | Tipo | Estado | SO (backend) | Datos (backend) | Decisión | Mecanismo backup | Destino | RPO propuesto | Notas |
|---|---|---|---|---|---|---|---|---|---|---|
EOF| 100 | win11-gpu-red | VM | stopped | — | virtio0:iscsi-aranea | KEEP (decomisión a revisar) | NONE (lab); LUN2 double-attach latente con 151 → resolver (WP-S1) | — | — | win11-gpu-red |
| 101 | etcd-athena | CT | running | mp0:local-lvm; rootfs:local-lvm | — | KEEP | etcd snapshot cluster (R1.5 VERIFIED 05:00) + VZ piloto ACTIVO | PBS | snap 1d | quorum 5 hosts; sobrevive pérdida de 1-2 nodos |
| 102 | mt5-wsl-red | VM | stopped | ide0:nfs-storage; scsi0:local-lvm | — | KEEP | NONE (lab) | — | — | mt5-wsl-red |
| 103 | emqx | CT | running | rootfs:nfs-storage | — | KEEP | VZ post-D | PBS | 30d | emqx 4G nfs |
| 104 | ryma-linux | VM | stopped | scsi0:local-kronos | — | KEEP | NONE (lab) | — | — | ryma-linux local-kronos |
| 105 | homeassistant | VM | running | — | scsi0:iscsi-aranea | KEEP | SNAP zvol (WP-A6) + VZ post-D | pool0 snap; PBS | 1d snap | homeassistant, zvol iscsi 50G |
| 106 | jobs | VM | running | scsi0:pool1 | — | KEEP | VZ post-D | PBS | 7d | jobs |
| 107 | develop | VM | stopped | scsi0:pool1 | — | KEEP | NONE (lab) | — | — | develop pool1 |
| 108 | sqx-zeus | VM | running | scsi0:local-sqx-zeus; scsi1:local-sqx-zeus | — | KEEP | NONE por diseño (F-04 + dirección owner); artefactos SQX vía MinIO G1B; vzdump opcional → 018 | — | — | sqx-zeus; local-sqx-zeus sagrado |
| 109 | win-serv-22 | VM | stopped | ide0:nfs-storage; scsi0:local-lvm | — | KEEP | NONE (lab) | — | — | win-serv-22 |
| 110 | testing | VM | stopped | scsi0:local-lvm | — | KEEP | NONE (lab) | — | — | testing |
| 111 | sqx-kronos | VM | running | scsi0:local-sqx-kronos; scsi1:local-sqx-kronos | — | KEEP | NONE por diseño (F-04 + dirección owner); artefactos SQX vía MinIO G1B; vzdump opcional → 018 | — | — | sqx-kronos; local-sqx-kronos sagrado + worker 135 |
| 112 | kronos-sqx-deprecado | VM | stopped | ide0:nfs-storage; scsi0:pool-kronos | — | DEFER (decomisión) | NONE; imagen RBD 120G huérfana lock stale → liberación gated dueño (WP-S1); disco ACTIVO = LVM pool-kronos | — | — | kronos-sqx-deprecado |
| 113 | mcps | CT | running | rootfs:nfs-storage | — | KEEP | VZ post-D (NO está en piloto) + CFG mcps-ops (WP-A5) | staging+PBS | cfg 7d | plano de acceso; rootfs nfs-storage 20G |
| 114 | mt4-test | VM | stopped | scsi0:pool1 | — | KEEP | NONE (lab) | — | — | mt4-test pool1 |
| 115 | traefik | CT | running | rootfs:local-lvm | — | KEEP | CFG R1 VERIFIED diario 04:00 + VZ | staging hermes + PBS (A0) | cfg 1d | acme-stepca.json recovery-critical (CA 200 stopped) |
| 116 | obsidian-sync | CT | running | rootfs:nfs-storage | — | KEEP | CFG vault (R1 VERIFIED) + DUMP CouchDB (WP-A1 ext) + VZ post-D | staging+PBS | vault 1d; DB 7d | LiveSync CouchDB 64G rootfs nfs |
| 117 | ubuntu-server | VM | stopped | scsi0:local-lvm | — | KEEP | NONE (lab) | — | — | ubuntu-server |
| 118 | agent | VM | running | scsi0:pool1; scsi1:pool1 | — | KEEP | CFG R1 hermes-state VERIFIED 1d + VZ post-D + ingesta staging→PBS (WP-A0) | staging→PBS; off-site R4 | 1d | VM agent; discos pool1 (scsi0+scsi1) |
| 119 | tailscale-gateway | CT | running | rootfs:local-lvm | — | KEEP | VZ post-D | PBS | 30d | tailscale-gateway |
| 120 | k8s-node-2 | VM | stopped | scsi0:local-lvm | — | KEEP | NONE (lab) | — | — | k8s-node-2 |
| 123 | sqx-hera | VM | running | scsi0:local-sqx-hera; scsi1:local-sqx-hera | — | KEEP | NONE por diseño (F-04 + dirección owner); artefactos SQX vía MinIO G1B; vzdump opcional → 018 | — | — | sqx-hera; local-sqx-hera sagrado |
| 124 | mt4-real | VM | running | ide0:nfs-storage; scsi0:pool1 | — | KEEP | VZ post-D (terminal completo SO+datos MT4) | PBS | 7d | mt4-real; credenciales broker fuera de alcance |
| 125 | mt4-test | VM | stopped | scsi0:pool1 | — | KEEP | NONE (lab) | — | — | mt4-test pool1 |
| 126 | docker-flink | CT | running | rootfs:pool1 | — | KEEP | CFG compose (WP-A5) + VZ post-D | staging+PBS | cfg 7d | flink |
| 127 | docker-observability | CT | running | rootfs:pool1 | — | KEEP | CFG compose (WP-A5) + VZ post-D | staging+PBS | cfg 7d | ARGUS corre en 160; 127 legacy/dev |
| 128 | docker-kafka | CT | running | rootfs:pool1 | — | KEEP | CFG compose (WP-A5) + VZ post-D | staging+PBS | cfg 7d |  |
| 129 | docker-hasura | CT | running | rootfs:pool1 | — | KEEP | CFG compose (WP-A5) + VZ post-D | staging+PBS | cfg 7d | hasura |
| 130 | opnsense | VM | running | scsi0:local-lvm | — | KEEP | VZ + CFG (export config OPNsense, gap hoy) | PBS; off-site R4 | cfg 7d | Firewall SPOF; recovery NOT_CERTIFIED (H5). WP-B2 |
| 132 | docker-monitoreo | CT | running | rootfs:local-lvm | — | KEEP | VZ post-D | PBS | 30d | docker-monitoreo local-lvm |
| 133 | mt4-ftmo | VM | running | ide0:nfs-storage; scsi0:pool1 | — | KEEP | VZ post-D | PBS | 7d | mt4-ftmo |
| 134 | mt4-ttp | VM | running | ide0:nfs-storage; scsi0:pool1 | — | KEEP | VZ post-D | PBS | 7d | mt4-ttp |
| 135 | worker-kronos | VM | running | scsi0:local-sqx-kronos | — | KEEP (excl. F-04) | NONE por diseño (disco local-sqx-kronos, F-04) | — | — | worker-kronos Windows; W1 gestión certificada, backup excluido |
| 136 | kafka-hera | VM | running | scsi0:pool1 | scsi1:local-lvm | KEEP | VZ (SO) post-D; data scsi1: valor UNKNOWN → 018 | PBS | 7d si aplica | kafka DEV |
| 137 | docker-frigate.14 | CT | running | rootfs:nfs-storage | — | KEEP | VZ post-D (config); media frigate EXCLUIDA (reconstruible) | PBS | 30d cfg | docker-frigate.14 nfs |
| 138 | kafka-kronos | VM | running | scsi0:pool1 | scsi1:local-kronos | KEEP | VZ (SO) post-D; data scsi1: UNKNOWN → 018 | PBS | 7d si aplica |  |
| 139 | kafka-zeus | VM | running | scsi0:pool1 | scsi1:local-lvm | KEEP | VZ (SO) post-D; data scsi1: UNKNOWN → 018 | PBS | 7d si aplica |  |
| 140 | echo | VM | running | scsi0:pool1 | — | KEEP | VZ post-D + CFG (deploy Forge en repo) | PBS | 7d | echo trading core |
| 141 | docker-echo-dev | CT | running | rootfs:pool1 | — | KEEP | CFG compose (WP-A5) + VZ post-D | staging+PBS | cfg 7d |  |
| 142 | daedalus | VM | running | scsi0:pool1 | — | KEEP | VZ post-D + CFG hermes-ops (WP-A5) | PBS | 7d | daedalus DEV |
| 144 | mt4-demo | VM | running | scsi0:pool1 | — | KEEP | VZ post-D | PBS | 7d | mt4-demo |
| 145 | truenas | VM | running | scsi10:local-lvm(SO) | scsi0:UNKNOWN(passthrough); scsi1:UNKNOWN(passthrough); scsi11:UNKNOWN(passthrough); scsi2:UNKNOWN(passthrough); scsi3:UNKNOWN(passthrough); scsi4:UNKNOWN(passthrough); scsi5:UNKNOWN(passthrough); scsi6:UNKNOWN(passthrough); scsi7:UNKNOWN(passthrough); scsi8:UNKNOWN(passthrough); scsi9:UNKNOWN(passthrough) | KEEP | CFG (export config TrueNAS via API, gap hoy) + SNAP/REPL en datasets | PBS + off-site R4 | cfg 1d | pool0/pool2 sobreviven a pérdida del SO; config export = crítico. WP-B2 |
| 147 | etcd-hades | CT | running | mp0:local-lvm; rootfs:local-lvm | — | KEEP | etcd snapshot cluster + VZ piloto ACTIVO | PBS | snap 1d |  |
| 148 | etcd-keeper | CT | running | rootfs:pool1 | — | KEEP | etcd snapshot cluster (datos); rootfs REC sin VZ (excluido PERMANENTE por mandato R2) | PBS (snapshot lógico) | snap 1d | UI sin quorum; reincorporación al driver eliminada |
| 149 | pi-hole | CT | running | rootfs:local-lvm | — | KEEP | VZ + CFG (token FTL6 GATED; servicio .149 L2-dead hoy) | PBS | cfg 7d | Resolver estado del servicio (posible retiro) + token. WP-B2 |
| 151 | win-development | VM | stopped | ide0:nfs-storage | sata0:iscsi-aranea; scsi0:iscsi-aranea | DEFER (decomisión) | NONE; apunta LUN2 (zvol zeus-win) junto a VM 100 → doble attach (WP-S1) | — | — | win-development; zvols win 2×203G valor UNKNOWN → owner |
| 152 | postgresql | VM | running | scsi0:pool1 | scsi1:iscsi-aranea | KEEP | DUMP G1A (13 bases VERIFIED) → agendar (WP-A1); WAL/PITR = WP-A2 gated; SNAP zvol (WP-A6) | PBS (+off-site R4); zvol snap pool0→pool2 | hoy one-shot; objetivo ≤1h con WAL | SO pool1; datos zvol pool0 LUN4 — placement CORRECTO, no migrar |
| 153 | mongodb | VM | running | scsi0:pool1 | scsi1:iscsi-aranea | KEEP | DUMP G1A (archive VERIFIED) → agendar (WP-A1); RPO 1h requiere replica set/PBM = gated; SNAP zvol (WP-A6) | PBS (+off-site R4) | hoy one-shot; 24h dumps; ≤1h NO demostrable standalone | standalone sin auth; zvol pool0 LUN5 |
| 154 | etcd-kronos | CT | running | mp0:local-lvm; rootfs:local-lvm | — | KEEP | etcd snapshot cluster + VZ piloto ACTIVO | PBS | snap 1d |  |
| 155 | etcd-hera | CT | running | mp0:local-lvm; rootfs:local-lvm | — | KEEP | etcd snapshot cluster + VZ piloto ACTIVO | PBS | snap 1d |  |
| 156 | etcd-zeus | CT | running | mp0:local-lvm; rootfs:local-lvm | — | KEEP | etcd snapshot cluster + VZ piloto ACTIVO | PBS | snap 1d |  |
| 157 | minio | VM | running | scsi0:pool1 | scsi1:iscsi-aranea | KEEP | DUMP G1B (12 buckets 64,76G PASS) → agendar (WP-A4); versioning OFF = gated; SNAP zvol (WP-A6) | PBS (+off-site R5 bulk) | hoy one-shot; semanal propuesto | SO pool1; datos zvol pool0 LUN6 — placement CORRECTO, no migrar |
| 158 | temporal | VM | running | scsi0:pool1 | — | KEEP | VZ post-D + CFG (WP-A5) | PBS | 7d | temporal DEV |
| 159 | ubuntu-dev | VM | stopped | scsi0:pool1 | — | KEEP | NONE (lab) | — | — | ubuntu-dev pool1 |
| 160 | argus | VM | running | scsi0:pool1 | scsi1:pool1; scsi2:pool1; scsi3:pool1; scsi4:pool1 | KEEP | VZ (SO) post-D; data scsi1-4 pool1: retención vs reconstruible → 018 | PBS | 7d (SO) | argus observability |
| 162 | sqx-ulab-kron-1 | VM | stopped | scsi0:pool1 | — | DEFER (decisión dueño) | NONE; discos RBD 20G activos → liberar o conservar (WP-S1, gate dueño) | — | — | sqx-ulab-kron-1 |
| 170 | sqx-ulab-zeus-1 | VM | stopped | scsi0:pool1 | — | DEFER (decisión dueño) | NONE; discos RBD 20G activos → liberar o conservar (WP-S1, gate dueño) | — | — | sqx-ulab-zeus-1 |
| 180 | pbs | VM | running | scsi0:local-kronos; scsi1:local-kronos | — | KEEP | CFG PBS (/etc/proxmox-backup-*) + meta datastore (WP-B2); datastore = destino, no se auto-respalda | PBS config→staging+off-site | cfg 7d | Pérdida disco data = pérdida copias locales → mitigar 2º target pool2 (opción) + off-site |
| 200 | ca | CT | stopped | rootfs:local-lvm | — | KEEP (decisión pendiente) | NINGUNO hoy; claves CA = R-11 si reactiva | — | — | step-ca; owner decide: reactivar+backup claves (WP-B2) o retiro formal |

## Unidades de datos relevantes (no-guest)

| Unidad | Hoy | Cobertura objetivo | Nota |
|---|---|---|---|
| zvols iSCSI pool0 (pg_data LUN4, mongo_data LUN5, minio_data LUN6) | sin snapshots (verificado E1) | SNAP horario/diario (WP-A6) + REPL pool0→pool2 (WP-A6) | backups app-consistent mandan (WP-A1/A2/A4) |
| pool0/iscsi zvol restantes (win ×3 ≈ 606G, HA 50G, debian) | sin snapshots | SNAP + REPL según ficha; win = UNKNOWN dueño (WP-S1) | LUN2 double-attach latente |
| pool0/aranea_storage 1,09T | sin snapshots | SNAP diario + REPL semanal (WP-A6) | mayor dataset producción |
| pool0/trading_systems 485G | sin snapshots | SNAP + REPL; inclusión a confirmar dueño | |
| pool0/proxmox_storage 416G (NFS PVE) | prune keep-all=1 riesgo llenado | SNAP + REPL diaria; corregir prune | CTs críticos + ISOs |
| pool0/apps (frigate media 68,6G) | sin snapshots | EXCLUIDO media; config sí | reconstruible |
| pool2/backup + pool0_backup + zfs_backup (~4,2T legacy) | STALE jul-2025 | PRESERVADOS tal cual (F-09); limpieza = decisión owner separada | libera espacio para REPL |
| pool2 libre | 2,15T | destino REPL (≈1,1-1,6T primer full) | cabe sin limpiar legacy |
| staging hermes (~/aranea/backup-staging) | 9,1G/49G activo | mantener + ingesta periódica→PBS (WP-A0) | 4 unidades R1/R1.5 |
| PBS datastore main 295G | piloto R2 día 2/7 | retención final post-D-piloto; NO redimensionar en piloto | crecer post-piloto |

## Cobertura de claves/secretos (referencias seguras)

- `r0d-g1a.key` (dumps PG/Mongo) y `r0d-g1b.key` (MinIO): custodia certificada — [[BACKUP-DR-KEY-RECOVERY]].
- Off-site (R4/R5) cifrará con Secret Zero → ticket 020. PBS datastore passphrase = mismo gate.

## Exclusiones declaradas (NO son gaps)

- F-04: `local-sqx-{zeus,hera,kronos}` + worker 135 + sqx 108/111/123 discos SQX.
- Media frigate, ISOs, caches, `/tmp`, logs >7d (diseño §6.3).
- Labs T3 stopped (12) salvo decisión 018 contraria.
- pool1 NO recibe backups nuevos hoy (NO_GO nearfull) ni export masivo (F-10): SOs productivos en pool1 se cubren con vzdump→PBS cuando el gate D lo habilite.
