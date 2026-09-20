---
type: change_log
schema_version: 1
scope: session
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
application:
entities:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[MASTER-PLAN-STORAGE-BACKUP-DR]]"
related:
  - "[[MATRIZ-59-GUESTS-BACKUP]]"
  - "[[ROADMAP-WP-BACKUP-DR]]"
  - "[[MANDATOS-IMPLEMENTACION-BACKUP-DR]]"
aliases:
  - "Master plan storage backup DR 2026-09-20"
confidence: high
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
---

# 2026-09-20-master-plan-storage-backup-dr

%% Mandato owner ONE-SHOT «ARANEA STORAGE + BACKUP/DR MASTER PLAN»: planificación completa sin implementar infraestructura. Cero mutaciones de infraestructura. %%

## Cambio

- **Tipo:** documentation + planning
- **Archivo(s) creados:**
  - `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/MASTER-PLAN-STORAGE-BACKUP-DR.md` — arquitectura objetivo (decisiones D1-D7), problemas a corregir, ventana, bloqueantes owner.
  - `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/MATRIZ-59-GUESTS-BACKUP.md` — 59/59 guests con placement (SO/datos backend), decisión KEEP/MIGRATE/DEFER, mecanismo, destino y RPO propuesto + unidades de datos no-guest.
  - `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/ROADMAP-WP-BACKUP-DR.md` — WPs A0-A8, B1-B4, S1-S4, DR1-DR6 con ejecutor/dependencias/gates/validación/rollback/DoD + orden y paralelismo.
  - `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/MANDATOS-IMPLEMENTACION-BACKUP-DR.md` — 8 prompts one-shot (MP-01..MP-08) + matriz de activación.
  - `BACKUP-DR-OWNER-PROJECT.md` — sección de planificación + 1 entrada bitácora (patch incremental).
  - `~/aranea/work/master-plan-20260920/CAPACITY-METRICS.md` (FUERA del vault) — métricas de capacidad baseline.
- **Sin mutaciones:** infraestructura (PVE/Ceph/TrueNAS/PBS/guests), BACKUP-DR-DESIGN.md, BACKUP-DR-CONTRACT.md, tickets 018-021, R1/R1.5/R2 (piloto intacto), estados de otros proyectos, frontmatter status/progress del proyecto.

## Motivo

- Mandato owner: cerrar la planificación integral de storage, backups y DR (sistema completo, no otra VM). Prohibido implementar; prohibido repetir discovery cerrado.

## Fuentes usadas (sin repetir discovery)

- Proyecto vivo (estado al 20sep: G1A CERRADO-TOTAL, G1B PASS, R2 piloto día 2/7), contrato (§2 Tier0 23→16 unidades, reglas §4), R0 (inventario 59/59 + F-01..F-14 + roadmap R0-R8 + ADDs §6), assessment 19-09 (HANDOFF + adversarial E1-E3) + change log del assessment, dirección owner 19-09 registrada en el proyecto, bitácoras G1A/G1B/R2 (16-20sep), Infrastructure Operations H0-H6 (routing NEED→ejecutor), guest-disk-map.json 59/59.

## Decisiones de diseño principales (detalle en master plan)

1. Placement sin regla universal: patrón actual SO=pool1 + datos=zvol pool0 se MANTIENE para PG/Mongo/MinIO (correcto, no migrar); SOs fuera de pool1 queda estratégico condicionado al carril Ceph.
2. Roles: PBS=receptor único local (vzdump+dumps+ingesta); staging→PBS vía A0; pool0 snapshots=rollback local; pool2=2ª copia local NO off-host; pCloud=crítico off-site; GDrive=bulk; pool2/pool0_backup STALE intacto (F-09).
3. PBS datastore 295G = cuello de botella: crecer +300G post-D-piloto (VG tiene 567G libres), umbral 70%.
4. DBs: dumps G1A agendados (A1); PG PITR (A2) gated ventana; Mongo RPO 1h requiere decisión topológica owner (standalone NO demostrable); MinIO semanal + versioning gated.
5. DR por 6 escenarios con regla anti-círculos: ningún restore depende del guest caído, de hades vivo ni de pool1 vivo.
6. RTO por clase propuesto (tabla D4.1) — requiere validación por drill y aprobación owner de números.
7. Roadmap: riesgo primero (off-site/Secret Zero → schedules → pool0 snap/REPL → vzdump → Ceph → edge → runbook); ventanas sábado madrugada; nada arriesgado contra Echo de domingo.

## Verificación

- Matriz generada programáticamente desde guest-disk-map.json (59 filas, 0 faltantes, 0 duplicadas; coverage check ejecutado).
- Revisión adversarial independiente por agente aislado (hallazgos aplicados antes del cierre; veredicto registrado en bitácora del proyecto).
- Tablas markdown validadas (separadores correctos tras corrección de 4 artefactos).
- Cero mutaciones de infraestructura en esta sesión.

## Hallazgos / Resultado

- PLAN PERSISTIDO COMPLETO (4 entregables + evidencia). Estado operativo fuera del plan: R2 piloto día 2/7 (intacto), G1A/G1B certificados, 3-2-1 sigue NO CUMPLE hasta A7/A8+020/021.
- Primer bloque propuesto post-aprobación: WP-A0+A1 (AUTO, sin ventana).
