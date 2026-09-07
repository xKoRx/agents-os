---
title: "RESTORE-DRILL-TEMPLATE — Runbook operativo de restore drills"
type: doc
schema_version: 1
status: active
icon: 🔄
slug: restore-drill-template
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-02
updated: 2026-08-10
tags:
  - kind/doc
  - area/personal
  - project/agents-os
  - domain/backup-dr
  - doc/drill-template
  - artifact/legacy-template
  - lifecycle/frozen
related:
  - "[[BACKUP-DR-DESIGN]]"
  - "[[BACKUP-DR-RUNBOOK]]"
  - "[[BACKUP-DR-CHECKLIST]]"
  - "[[agent-project-07-restore-drills]]"
  - "[[04-backups/runbook-mensual]]"
  - "[[04-backups/runbook-trimestral]]"
parent: "[[BACKUP-DR-OWNER-PROJECT]]"
cssclasses: wide
---

# 🔄 RESTORE-DRILL-TEMPLATE

## Propósito

Conservar la plantilla operacional legacy para documentar restore drills Backup/DR; no es un template canónico del schema ni se promueve a runbook sin evidencia adicional.

## Contenido

> **Template operativo** para los 6 restore drills definidos en `BACKUP-DR-DESIGN §5 Capa G` y `agent-project-07`. Cada drill se ejecuta usando esta plantilla, completando los campos `{{}}`.
>
> **Regla**: backup NO es válido sin drill PASS reciente. Cerrar ticket con PASS criteria cumplida + output adjunto.

---

## §1. Encabezado obligatorio del drill

```yaml
drill:
  drill_id: "DRILL-YYYY-MM-DD-NN"     # ej: DRILL-2026-07-15-01
  date_executed: "YYYY-MM-DD"
  time_started: "HH:MM"
  time_finished: "HH:MM"
  duration_minutes: <minutos>
  drill_type: "<drill_1|drill_2|drill_3|drill_4|drill_5|drill_6>"
  agent_project: "agent-project-07-restore-drills"
  ticket_ref: "ticket-id-en-segundo-brain"
  executed_by: "<nombre-agente>"
  supervised_by: "<owner-o-agente-secundario>"
  environment: "scratch"             # SIEMPRE scratch, NO producción
  scheduling: "<mensual|trimestral|semestral|según_necesidad>"
```

---

## §2. Alcance del drill

```yaml
scope:
  what_is_restored: "<VM-id|dump-name|chunk-name|restic-subset>"
  source: "<pbs|pcloud-crypt-restic|gdrive-crypt-rclone|sanoid-snapshot|staging-local>"
  target: "<scratch-vm-id|scratch-path|restore-target>"
  expected_size: "<bytes>"
  expected_recovery_time_objective: "<minutes>"
```

---

## §3. Pre-flight (debe ser todo PASS para empezar)

```yaml
preflight:
  approvals:
    owner_approval_received: true        # explícito en chat/ticket
    ticket_id: "<ticket-id>"
  credentials:
    secret_zero_accessible: true
    passphrase_retrieved: true            # pbs / restic / rclone / stepca
  source_health:
    source_snapshot_exists: true           # pvesm list / restic snapshots / rclone lsf
    source_readable: true                  # proxmox-backup-manager verify > 0 (no errors)
  environment:
    scratch_environment_isolated: true    # vlan scratch o namespace separado
    scratch_resources_available: true     # cpu + ram + disk suficientes
  rollback_plan_documented: true          # cómo deshacer el drill sin tocar prod
```

---

## §4. Comandos ejecutados (secuencia completa)

```bash
# Cada comando con su output resumido (no todo el stderr — solo PASS/FAIL relevante).
# Ejemplo para drill_1_vm_pbs:

qmrestore <archive> <new-vmid> --storage local-lvm \
  --ipconfig0 ip=192.168.31.<scratch>/24,gw=192.168.31.1
qm start <new-vmid>
ssh root@192.168.31.<scratch> 'systemctl is-system-running'
ssh root@192.168.31.<scratch> 'pg_isready -h 127.0.0.1' # si aplica
ssh root@192.168.31.<scratch> 'curl -fsS http://localhost:9119/health' # si aplica
```

```bash
# drill_4_restic_pcloud
restic -r $RESTIC_REPO restore latest --target /tmp/restore --include "<subset>"
sha256sum -c /tmp/restore/<file>.sha256
diff -q /tmp/restore/<file> /production/<file>
```

```bash
# drill_5_zfs_gdrive
rclone copy gdrive-crypt:<path-chunk> /tmp/restore-chunk --progress
sha256sum -c /tmp/restore-chunk/manifest.sha256
cat /tmp/restore-chunk/chunk.part.* | zfs recv -F <dataset>
zfs list -o name,mountpoint <dataset>
```

> **Regla**: el runbook de cada drill `agent-project-07 §Implementation plan` tiene los comandos exactos. Esta sección es solo el "registro de ejecución".

---

## §5. Tiempo de restore (métrica clave)

```yaml
restore_time_metrics:
  t0_drill_start: "HH:MM:SS"
  t1_source_picked: "HH:MM:SS"
  t2_data_transferred: "HH:MM:SS"
  t3_data_verified: "HH:MM:SS"
  t4_service_validated: "HH:MM:SS"   # servicio respondiendo correctamente
  t5_drill_complete: "HH:MM:SS"
  total_seconds: <int>
  rto_target: "<seconds>"            # RTO objetivo configurado en ap-07
  rto_met: true|false
```

---

## §6. Errores encontrados y resoluciones

```yaml
errors:
  - step: "preflight|execution|verification|cleanup"
    command: "<comando que falló>"
    error_message: "<output>"
    category: "<transient|configuration|data|environment>"
    resolution: "<qué se hizo para superar>"
    impact: "<low|medium|high|destructive>"
    rollback_executed: true|false
```

---

## §7. Validación (PASS criteria)

```yaml
validation:
  - criterion: "<criterio PASS específico del drill>"
    check_method: "<comando o inspección>"
    expected: "<resultado esperado>"
    actual: "<resultado real>"
    pass: true|false
  - criterion: "checksum matches"
    check_method: "sha256sum -c"
    expected: "OK"
    actual: "OK"
    pass: true
```

---

## §8. Acciones correctivas (si alguna validación es FAIL)

```yaml
corrective_actions:
  - action: "<qué se hace para corregir>"
    owner: "<owner|agente>"
    due: "<YYYY-MM-DD>"
    ticket_link: "<ticket-id>"
  - action: "rollback del restore a scratch"
    owner: "agente"
    due: "ahora"
```

---

## §9. Evidencia adjunta

```yaml
evidence:
  logs:
    - "/var/log/aranea-backup/drill-N.log"
    - "/tmp/restore-output.txt"
  outputs:
    - "restic check stdout"
    - "zfs list output"
  screenshots:
    - "dashboard post-restore (si aplica)"
    - "service healthcheck (curl /health)"
  ticket_link: "<ticket-id-con-todos-outputs>"
```

---

## §10. Decisión final

```yaml
decision:
  result: PASS|FAIL
  reviewer: "<nombre-owner-o-agente-secundario>"
  reviewer_signature: "<chat-ack|ticket-ack>"
  next_drill_due: "<YYYY-MM-DD>"
  notes: "<cualquier observación relevante>"
  
  if FAIL:
    open_request_change: true
    ticket_blocker: "<ticket-id-del-RC>"
    backup_considered_valid_until: "<YYYY-MM-DD> o 'invalidated'>"
```

---

## §11. Cleanup obligatorio post-drill

```yaml
cleanup:
  scratch_vm_destroyed: true
  scratch_data_wiped: true
  pvesm_list_clean: true
  tag_drill_<vmname>_<date> REMOVED: true
  logs_archived: true
  evidence_in_ticket: true
```

---

## §12. Criterios PASS canónicos por tipo de drill

### drill_1_vm_pbs (mensual)
- [ ] VM scratch arrancó sin error.
- [ ] `systemctl is-system-running` retorna `running`.
- [ ] Servicios críticos (ssh, network, app-specific) responden.
- [ ] Cleanup completo post-drill.

### drill_2_pg (mensual)
- [ ] `pg_restore --list` ejecuta sin error.
- [ ] Row count de tablas críticas >= producción (`SELECT count(*) FROM ...`).
- [ ] Checksum match entre dump original y restored (`pg_dump ... | sha256sum` vs restored `pg_dump ... | sha256sum`).

### drill_3_mongo (mensual)
- [ ] `mongorestore --dryRun` ejecuta sin error.
- [ ] Collection count restored == producción (`db.getCollectionNames().length`).
- [ ] Sample queries devuelven datos esperados.

### drill_4_restic_pcloud (trimestral)
- [ ] `restic check` exit 0.
- [ ] Subset restaurado en /tmp/restore.
- [ ] Diff contra producción: 0 diferencias en archivos críticos.

### drill_5_zfs_gdrive (trimestral)
- [ ] `rclone check` exit 0.
- [ ] Chunk restaurado en /tmp/restore-chunk.
- [ ] `zfs recv` exit 0.
- [ ] `zfs list` muestra dataset con mountpoint correcto.
- [ ] Mount + read/write OK.

### drill_6_stepca (semestral)
- [ ] `step ca restore` exit 0.
- [ ] `step ca verify` exit 0 (cert nuevo firmado por CA recuperada).
- [ ] Cert presente en `step path` de algún cliente.
- [ ] Owner-driven (no automatizable).

---

## §13. Notas de implementación

- **Frecuencias**: drill 1-3 mensual, drill 4-5 trimestral, drill 6 semestral. Ver `BACKUP-DR-CHECKLIST §3-6`.
- **Tickets**: cada drill genera un ticket `DRILL-YYYY-MM-DD-NN` con esta plantilla como cuerpo.
- **Ventana**: drill 1 requiere 30 min ventana corta; drills 2-6 no requieren ventana.
- **Storage**: drill 1 usa espacio en `local-lvm` (no `local-sqx-*`); drills 2-6 escriben a `/tmp` o staging local.
- **Auditoría**: el agente expone estos registros como artefactos de `agent-project-08` cierre de sesión.

---

## §14. Cierre y trazabilidad

```yaml
traceability:
  ticket_input: "<ticket-id-de-owner-task-que-origina-drill>"
  ticket_output: "<ticket-id-de-cierre-del-drill>"
  inventory_snapshot: "<path-al-inventory-ejecutado-cerca-del-drill>"
  policy_at_drill_time: "<version-de-backup-policy-yaml-vigente>"
  runbook_version: "<version-de-BACKUP-DR-DESIGN-vigente>"
```

---

## Status y referencias

- **Status**: design-frozen (no ejecutado).
- **Versión**: 1.0.
- **Sesión de creación**: 2026-07-02.
- **Sesión de cierre (cuando se ejecute el primer drill)**: owner firma en ticket.

## Source files

- `BACKUP-DR-DESIGN.md` §5 Capa G
- `BACKUP-DR-RUNBOOK.md` §5-6 (procedimientos específicos)
- `BACKUP-DR-CHECKLIST.md` §5 (drill checklist)
- `agent-project-07-restore-drills.md` (per-drill implementation plan)

## Captured

Template operacional extraído del diseño. Cada drill ejecutado en el futuro materializa §1-§11 con datos reales.
