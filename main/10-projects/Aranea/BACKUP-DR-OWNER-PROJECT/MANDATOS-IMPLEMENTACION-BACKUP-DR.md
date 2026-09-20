---
title: "MANDATOS DE IMPLEMENTACIÓN — prompts one-shot por bloque (2026-09-20)"
type: doc
schema_version: 1
status: active
icon: 📨
slug: backup-dr-mandatos-implementacion
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: 2026-09-20
updated: 2026-09-20
aliases:
  - Mandatos implementación backup DR
  - Prompts one-shot WPs
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
  - project/backup-dr
related:
  - "[[MASTER-PLAN-STORAGE-BACKUP-DR]]"
  - "[[ROADMAP-WP-BACKUP-DR]]"
  - "[[MATRIZ-59-GUESTS-BACKUP]]"
---

# 📨 MANDATOS DE IMPLEMENTACIÓN — prompts one-shot

> Un prompt por bloque ejecutable. Cada mandato es autosuficiente: referencia los entregables del plan, declara alcance, prerrequisitos, criterios de cierre y prohibiciones. Ejecutor por defecto = Ariadna (carril Backup/DR). Copiar el bloque como mandato. Regla transversal de todos: cero cambios a diseño congelado F-01..F-14 sin RC, tickets 018-021 intocables (los resuelve el owner), R2 piloto intacto hasta decisión D, y evidencia en `~/aranea/work/<bloque>-<fecha>/` + change log.

## MP-01 — Cobertura base AUTO (WP-A0 + A1 + A3 + A4-AUTO + A5)

```
MANDATO ONE-SHOT — BACKUP-DR: COBERTURA BASE (A0/A1/A3/A5)
Actúa como operador del proyecto BACKUP-DR-OWNER-PROJECT. Reutiliza: MASTER-PLAN-STORAGE-BACKUP-DR, ROADMAP-WP (A0,A1,A3,A4,A5), MATRIZ-59-GUESTS, patrón G1A/G1B (driver, cifrado, custodia claves BACKUP-DR-KEY-RECOVERY) y staging R1/R1.5 existente.

ALCANCE (todo AUTO, sin ventana, cero mutaciones en guests de trading):
1. WP-A0: ingestar a PBS (host/r0d-config-*) los run-dirs R1/R1.5 vigentes; round-trip sha de 1 unidad; corregir prune-backups `keep-all=1` de nfs-storage en 5 nodos (diff antes/después).
2. WP-A1: timers systemd en hermes — PG 152 dump diario, Mongo 153 dump diario (patrón g1a-driver: dump→cifrado AES→ingesta pxar→verify PBS). MinIO 157 semanal recurrente EXCLUIDO de este mandato: requiere gate owner separado (regla 4.1/018 — MinIO es ADD no aprobado); si el owner lo autoriza en chat, se agrega al timer con el mismo patrón G1B. Retención 30d sin prune. Credenciales por stdin/forced-command whitelist; claves por custodia existente. Horarios: dumps 03:00-03:45, ANTES de los timers R1 04:00/05:00 (mismo host; no re-agendarlos).
3. WP-A3: dump diario CouchDB 116 + ingesta; drill restore a scratch con conteo de docs.
4. WP-A5: export semanal de compose/env/units de 126/129/141/127/128/158/142/113 + /etc/proxmox-backup-* de PBS 180 (sin secretos en claro).
5. WP-A4 (sólo parte AUTO): incluir el stream semanal MinIO en el timer; versioning MinIO queda EXCLUIDO (gated).

VALIDACIÓN / CIERRE: 2 ciclos de los jobs diarios + 1 ciclo del semanal (si MinIO fue autorizado) con VERIFY_TASK_OK + manifest sha + 1 drill de restore (PG o Mongo) desde PBS; timers active+enabled; cero impacto en R2 (día 7/7 y decisión D intactos). Criterio de cierre: PASS = PG+Mongo (+CouchDB) VERIFIED+AUTOMATED + drill PASS + R2 intacto verificado.
PROHIBIDO: tocar postgresql.conf/mongod.conf, jobs.cfg PVE, Ceph, tickets, diseño congelado, prune del datastore main, y cualquier reinicio de guests. Fallar PASS → reportar BLOCKED con evidencia sin reintentos Ciegos.
```

## MP-02 — Off-site crítico (WP-A7) [requiere 020+021]

```
MANDATO ONE-SHOT — BACKUP-DR: OFF-SITE CRÍTICO restic→pCloud (A7)
Prerrequisitos gates: ticket 020 (Secret Zero operativo) y 021 (decisión OAuth) RESUELTOS por el owner; proveedor pCloud revalidado. Sin ambos: NO iniciar.

ALCANCE: repo restic cifrado en pCloud (F-08: crítico); push semanal de configs R1/R1.5 + dumps PBS exportados + referencias de custodia de claves; drill de descarga+descifrado en máquina limpia (hermes off, prueba de recuperación sin infra local).
VALIDACIÓN/CIERRE: 1 snapshot VERIFIED off-site + drill completo de recuperación PASS + retención documentada. PASS = 3-2-1 cumple para configs/dumps.
PROHIBIDO: subir plaintext sin cifrar, mezclar con tier bulk, guardar credenciales en vault/agentes (solo referencias seguras).
```

## MP-03 — vzdump T0 producción (WP-B1) [requiere D-piloto + 018 + 019 + crecimiento datastore]

```
MANDATO ONE-SHOT — BACKUP-DR: VZDUMP TIER0 PRODUCCIÓN (B1)
Prerrequisitos gates: decisión D-piloto R2 (post 7/7 días, ~28sep) con retención final aprobada; ticket 018 (lista Tier 0 definitiva); ticket 019 (ventana inicial); disco PBS scsi1 crecido según MASTER-PLAN D3 (+300G, serial pbs-data, antes de activar jobs) — crecimiento incluido en este mandato como fase 1 gated.

ALCANCE: (fase 1) crecer datastore PBS + verify; (fase 2, en ventana) jobs vzdump diarios 02:00 para Tier 0 (lista 018) + semanal T1/T2, exclusiones §6.3 del diseño, mod snapshot, bandwidth limit conservador; (fase 3) verify jobs + restore drill de 1 VM T0 completa a scratch sin boot.
VALIDACIÓN/CIERRE: 7 días de jobs VERIFIED + drill restore PASS + espacio datastore bajo umbral 70%. PASS = cobertura imagen-level T0 AUTOMATED.
PROHIBIDO: vzdump de MT4/echo fuera del horario aprobado; backup de discos local-sqx-* (F-04); solapar con dumps G1A (03:00-04:30); tocar piloto R2 timers.
```

## MP-04 — PG PITR + decisión Mongo RPO (WP-A2/A2b) [ventana 019]

```
MANDATO ONE-SHOT — BACKUP-DR: RPO 1h EN DATOS DE TRADING (A2)
Prerrequisitos: WP-A1 PASS (MP-01 parcial); ventana 019; OK owner explícito para mutar config de PostgreSQL 152 (PROD trading). Mongo (A2b) SÓLO si el owner aprobó la decisión de topología (replica set 1 nodo o PBM); si no, registrar RPO Mongo=24h como deuda aceptada y NO tocar Mongo.

ALCANCE PG: medir tasa WAL 24h (UNKNOWN→medido); configurar archive_mode=on, archive_timeout=60s, archive_command rsync→staging hermes (WAL fuera de pool0); pg_basebackup semanal; reinicio controlado en ventana; drill PITR (restore a segundo objetivo, SELECTs reales patrón G1A).
VALIDACIÓN/CIERRE: PITR VERIFIED con RPO medido (esperado ≤5min) + rollback probado (archive_mode=off, conf revertida). PASS = RPO PG ≤1h DEMOSTRADO.
PROHIBIDO: tocar Mongo sin la decisión topológica firmada; cambiar tuning no relacionado; ejecutar sin ventana.
```

## MP-05 — pool0 snapshots + REPL pool0→pool2 + scrub (WP-A6) [ventana para full]

```
MANDATO ONE-SHOT — BACKUP-DR: ROLLBACK LOCAL Y 2ª COPIA DE POOL0 (A6)
Prerrequisitos: decisión owner de datasets (default propuesto en ROADMAP A6); ventana 019 para full inicial; autorización de ejecución en TrueNAS (H1 WS/API). F-09 intacto: dataset nuevo pool2/pool0_new/, jamás tocar pool0_backup.

ALCANCE: scrub pool2 (read-only, AUTO, puede ir antes de ventana); snapshot schedules (horario zvols T0 pg/mongo/minio data + HA; diario aranea_storage/trading_documents/home/proxmox_storage; retención corta controlada); zfs send -n dry-run de la selección; full inicial REPL→pool2/pool0_new en ventana; incremental diaria (producción chico) y semanal (aranea_storage) vía replicación nativa TrueNAS.
VALIDACIÓN/CIERRE: 1º full VERIFIED (comparación zfs send -nv ending snap) + drill rollback de 1 zvol desde snapshot a dataset de prueba + scrub pool2 0 errores. PASS = snapshots activos + REPL viva.
PROHIBIDO: autoclean/aggressive retención sin decisión; tocar árboles legacy pool2 (limpieza = decisión owner separada); frigate media en la replicación.
```

## MP-06 — Edge/infra configs + observabilidad (WP-B2 + B3)

```
MANDATO ONE-SHOT — BACKUP-DR: EDGE CONFIGS + SEÑALES EN ARGUS (B2/B3)
ALCANCE B2: export config OPNsense semanal (canal POR VERIFICAR — SSH admin demostrado por H1 pero API/backup de OPNsense no; si falta acceso → bundle puntual); export config TrueNAS (SSH admin certificado; API key ya existe para WS — verificar qué canal permite export config; unidad nueva); pi-hole: SOLO diagnóstico del estado .149 L2-dead + preparación (token FTL6 sigue gated; la decisión de retiro/reactivación es del owner); CA 200: ejecutar la decisión que el owner haya tomado (si no hay decisión: NO tocar, registrar pendiente).
ALCANCE B3 (tras A1/B1 corriendo): señales en ARGUS vía management path — edad de último backup por unidad, VERIFY tasks PBS, espacio datastore, timers failed; alertas mínimas del diseño §8; test de disparo real de 1 alerta.
VALIDACIÓN/CIERRE: 3-4 unidades config VERIFIED (OPNsense, TrueNAS, PBS, + pi-hole si se resolvió) + alerta de prueba disparada y recibida. PASS = edge configs protegidos + backup dejó de ser silencioso.
PROHIBIDO: mutar servicios edge en producción (pi-hole/OPNsense/CA = sólo lectura hasta decisión owner); credenciales en claro.
```

## MP-07 — Carril Ceph/Storage (WP-S1..S4) [ejecutor CEPH/STORAGE — NO Backup/DR]

```
MANDATO ONE-SHOT — CEPH/STORAGE: CORRECCIONES GATED (S1/S2/S4; S3 = decisión)
Rol: ejecutor Ceph/Storage según routing H5/H6 (contratos ceph-storage-operations / cluster-node-maintenance). Backup/DR NO toca Ceph. Ceph NO_GO vigente para nuevos discos pool1 hasta gates de este carril.

ALCANCE: (S4, RO, inmediato) instrumentar métricas OSD/slow-ops → ARGUS. (S1, gated dueño) inventario y liberación de imagen RBD huérfana vm-112-disk-0 (120G, lock stale) + discos 162/170 tras confirmación por VMID; resolver riesgo LUN2 (100 vs 151) documentando bloqueo de arranque simultáneo. (S2, ventana) mClock global→balanced + recovery_sleep>0 con medición antes/después + bluestore compact osd.0/2. (S3) propuesta numerada de estructura (OSDs SATA existentes vs mover SOs vs mantener): decisión owner, sin ejecutar.
VALIDACIÓN/CIERRE: HEALTH sin degradación; freed GB medidos (S1); latencia osd.0/2 antes/después (S2); NOT_PROVEN de lag reemplazado por series medibles (S4). PASS = margen pool1 ampliado y perfil balanced con evidencia.
PROHIBIDO: reweight/ratio/PG changes/CRUSH edits/borrados sin confirmación por VMID del dueño; cualquier acción durante operación de Echo; mezclar con jobs de backup.
```

## MP-08 — Drills recurrentes + runbook (WP-R7 + B4)

```
MANDATO ONE-SHOT — BACKUP-DR: DRILLS + RUNBOOK CANÓNICO (R7/B4)
ALCANCE: ejecutar drills DR-1 (restore VM+CT desde PBS) y DR-4 (arranque MinIO desde G1B) si no están frescos (<35d); DR-2/DR-3/DR-5/DR-6 según disponibilidad de ventanas/off-site (ver ROADMAP bloque DR); consolidar BACKUP-DR-RUNBOOK.md (procedimientos de restore por unidad, claves por referencia, RPO/RTO por clase) + checklists; validar con un agente fresco ejecutando 1 restore guiado.
VALIDACIÓN/CIERRE: cada drill PASS con evidencia; runbook validado por owner. PASS = sistema recuperable por tercero con el runbook.
PROHIBIDO: drills destructivos sobre producción; drill de DR-6 sin 020 resuelto (sólo versión parcial).
```

## Matriz de activación

| Mandato | Bloquea inicio | Puede partir YA |
|---|---|---|
| MP-01 | nada (AUTO) | ✅ tras aprobar plan |
| MP-02 | 020 + 021 | — |
| MP-03 | D-piloto + 018 + 019 | crecimiento datastore como fase gated |
| MP-04 | MP-01 + 019 (+OK owner PG; decisión Mongo para A2b) | — |
| MP-05 | datasets decisión + 019 (scrub puede ir antes) | scrub pool2 ✅ |
| MP-06 | B2 parcial (pi-hole/CA decisión); B3 tras MP-01/MP-03 | exports OPNsense/TrueNAS tras verificar canal ✅/❓ |
| MP-07 | S1 (dueño), S2 (ventana); S4 ✅ | S4 ✅ (ejecutor Ceph) |
| MP-08 | MP-01 (y MP-02 parcial para DR-6) | — |
