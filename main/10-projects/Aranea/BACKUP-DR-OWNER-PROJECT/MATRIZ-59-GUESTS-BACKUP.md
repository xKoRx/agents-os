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
EOF