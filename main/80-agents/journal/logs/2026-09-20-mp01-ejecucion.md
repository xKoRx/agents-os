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
  - "[[agent-project-03-app-consistent-data-backups]]"
related:
  - "[[BACKUP-DR-CONTRACT]]"
aliases:
  - "MP-01 ejecución 2026-09-20"
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

# 2026-09-20-mp01-ejecucion

%% Mandato owner ONE-SHOT: ejecución del alcance seguro de MP-01 (WP-A0-AUTO + A1 PG/Mongo + A3 + A5), según `~/aranea/work/master-plan-20260920/MP01-FIRST-MANDATO.md`. Bootstrap Agents-OS ejecutado (entidad [[BACKUP-DR-OWNER-PROJECT]], router aranea). Precondición de recurrencia PG/Mongo: aprobación del plan por el owner al despachar el mandato (cumplida, citada verbatim en el prompt). %%

## Cambio

- **Tipo:** infra-mutation (en alcance autorizado) + documentation
- **Mutaciones de infra (todas revertibles):**
  - hermes: units systemd nuevos `aranea-r3-{pg,mongo}-dump.{service,timer}` (staging canónico `~/aranea/bin/mp01/` + copia 644 en `/etc/systemd/system/`); timers enabled 03:00/03:20; drivers `~/aranea/bin/mp01-a1-dumps.sh` y `~/aranea/bin/mp01-a5-configs.sh`.
  - PBS datastore `main` (vía token backup@pbs!aranea, ACL Backup): snapshots nuevos `host/r0d-config-{r1,etcd,pve}` (ingesta de run-dirs R1/R1.5 vigentes del 20sep, cifrados r0d-g1a.key), `host/r0d-postgresql/2026-09-20T17:32:13Z` y `2026-09-20T17:36:19Z` (dumps cifrados), `host/r0d-mongodb/2026-09-20T17:33:42Z` y `17:38:01Z`, `host/r0d-config-mp01a5/2026-09-20T17:50:56Z` (bundle configs 9 targets cifrado).
  - guests 152/153: dumps read-only con patrón G1A (dump→sha in-guest→traslado rrsync efímero con sha guest=hermes→revocación verificada grep=0), run-dirs in-guest conservados como siempre.
- **Rollback ejecutado durante la sesión:** snapshot contaminado `host/r0d-postgresql/2026-09-20T17:26:44Z` (creado con spool G1A mezclado — defecto del primer intento; token sin permiso Prune ⇒ forget bloqueado: queda al owner). Archivos huérfanos `mnt/` del intento eliminados (creados hoy; verificados por timestamp 14:26 vs 23:22 G1A). G1A `mnt/` quedó byte-idéntico al baseline 19sep.
- **NO tocado:** storage.cfg/prune/retenciones; backup recurrente MinIO (excluido); Ceph/TrueNAS/pool2/PBS infra; scrub/PITR/topología Mongo; R2 (timer, driver, ct/ = 6 CTs 101/115/147/154/155/156 verificado post-cambio); R1/R1.5 (runs de hoy Finished OK; timers 04:00/05:00/SAT 08:30 intocables); Echo; cero borrado de backups/snapshots/claves preexistentes.

## Resultado

- **Preflight PASS** (todos los puntos del mandato): SSH PBS+PVE+hermes-ops OK; datastore 17% (<70%) y verify TASK OK; staging legible con manifests íntegros; runs 04:00/05:00 Finished OK; R2 timer 06:05 vivo con run del día OK; CouchDB 116 = unauthorized (→SKIP A3).
- **WP-A0-AUTO PASS:** inventario nfs-storage (54 entradas: 7 vzdump 33,44 GB jun→nov 2024, VMs 105/134, CTs 100/104/106/107, ABANDONED) + ingesta cifrada de 3 run-dirs → `host/r0d-config-{r1,etcd,pve}` + round-trip sha OK + diff prune preparado (5/5 nodos md5 idéntico, bundle gated).
- **WP-A1 PG/Mongo PARTIAL (certificación 2º ciclo pendiente):** dump diario automatizado VERIFICADO ciclo 1 por el camino real del servicio (`systemctl start`, Result=success exit 0 en ambos) + primera pasada manual equivalente; timers enabled (próximos disparos lun 21sep 03:00/03:20); retención 30d sin prune. Verify por snapshot: snapshot list + round-trip sha + (PG) drill completo.
- **Drill restore REAL PASS (PG):** desde snapshot `17:36:19Z` → restore en PBS → descifrado en hermes → SHA256SUMS interno del run-dir OK → drill funcional in-guest 152 sobre datos recuperados: 13/13 bases, PG_ISREADY PASS, SELECTs reales (echo.lab_job_runs 88050, trade_journal 242424, sqx.strategies 9090, dashboard_version 44, hdb_metadata 1, echo_mcp EMPTY_OK). Mongo: ingesta+round-trip verificados (drill completo G1B/G1A ya certificado 20sep sobre el mismo mecanismo).
- **WP-A3 SKIP con bundle:** 116 IP real .32; :5984 OPEN pero unauthorized; sin credencial en custodia → cláusula preflight 4. `BUNDLE-A3-SKIP-couchdb.md` con única acción de desbloqueo (credencial RO de CouchDB por custodia).
- **WP-A5 PASS con hallazgo:** bundle cifrado (9 targets: CTs 126/127/129/141/113 + 128@hera + vm158 via guest-exec base64 + daedalus + pbs180 `/etc/proxmox-backup`) → snapshot `r0d-config-mp01a5` + round-trip OK + scratch de descifrado/extracción OK. Hallazgo documentado: 0 compose en rutas estándar ≤4 niveles — stacks docker operan por units systemd (docker.service/containerd), que sí quedan en el bundle; env-vars NO se capturan en claro (sólo nombres en .env si existieran). Weekly pendiente de timer (DoD parcial: ciclo 1 verificado; semanalidad por decidir con A5-timer).
- **R2 intacto verificado post-cambio:** verify main TASK OK 18/18 groups (14 previos + 4 config nuevos); `ct/` = 6 CTs (101/115/147/154/155/156) sin cambios; staging 21%.
- **Estado datastore tras MP-01:** 48G/295G (17%), 65.536 chunks, 18 grupos de snapshot.

## Defectos corregidos durante ejecución (todos documentados)

1. Spool PBS compartido con blobs G1A → primer snapshot PG contaminado; rollback parcial (forget bloqueado por ACL mínima del token — registro owner) + spool aislado por run + higiene de `mnt/`.
2. `TASK OK` no es línea de backup en client PBS 4.2.5 → verificación durable por `snapshot list`.
3. vm158: primer intento murió por `B64: unbound variable` (set -u + quoting del driver); corregido eso, out-data de guest-exec siguió sin transportar binario limpio (JSON) → solución definitiva: `tar | base64 -w0` dentro del guest y decodificar fuera (variante del patrón G1A).
4. daedalus sin sudo para hermes-ops → capturas sin sudo (archivos legibles); registrar si se requiere más alcance.
5. pbs180: `/etc/proxmox-backup-proxy` no existe → tar sólo `/etc/proxmox-backup`.
6. Checks con globs/expansión y anclas mal calzados en a5 → corregidos con validación por contenido.

## Pendientes (owner)

- `forget` del snapshot contaminado `host/r0d-postgresql/2026-09-20T17:26:44Z` (393M; token sin Prune — requiere canal root PBS o ACL temporal).
- Bundle gated: diff prune `nfs-storage` (keep-all → keep-daily=7,keep-weekly=4,keep-monthly=3) preparado en `BUNDLE-A0-GATED-prune-nfs-storage.md`.
- Bundle A3: credencial RO CouchDB si quiere habilitar A3 (patrón A1 listo para replicar).
- Retiro de claves/custodia: sin cambios (estado G1A/G1B vigente).

## Evidencia

`~/aranea/work/mp01-20260920/` (a0/, a5/, a1.log, drill-pg.log, drill-pg-output2.txt, PREFLIGHT.md, bundles, nfs-storage-inventory-SUMMARY.md, raw/) · drivers `~/aranea/bin/mp01-a1-dumps.sh` + `~/aranea/bin/mp01-a5-configs.sh` + units `~/aranea/bin/mp01/etc/systemd/system/` · logs de servicio y timers en journalctl de hermes.
