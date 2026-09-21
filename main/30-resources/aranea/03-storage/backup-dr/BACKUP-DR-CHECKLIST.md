---
title: "BACKUP-DR-CHECKLIST — Checklists operacionales"
type: runbook
scope: project
icon: ✅
slug: backup-dr-checklist
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-09-21
tags: [aranea, backup, checklist, ops, kind/runbook, area/personal, project/agents-os]
related: "[[BACKUP-DR-DESIGN]]"
parent: "[[BACKUP-DR-OWNER-PROJECT]]"
cssclasses: wide
---

# ✅ BACKUP-DR-CHECKLIST — Checklists operacionales

> [!warning] ESTADO (2026-09-18)
> §1, §2, §5, §7: vigentes como disciplina transversal (aplican a cada cambio/drill). §3 y §4: `DESIGNED — NOT IMPLEMENTED` — presuponen PBS/Restic/rclone operativos que hoy NO existen; NO ejecutar sus ítems como si estuvieran corriendo. Lo único con cobertura real hoy: staging R1 + automatización R1.5 (etcd-snapshot + pve node-local con timers; pi-hole GATED) — ver `BACKUP-DR-RUNBOOK` §0.

---

## §1. Pre-ejecución (antes de cualquier cambio DANGEROUS)

- [ ] Owner dio aprobación explícita (chat / ticket).
- [ ] Ventana de mantenimiento confirmada.
- [ ] Snapshot o staging del estado actual existe.
- [ ] Procedimiento de rollback documentado y testeado.
- [ ] Recursos protegidos identificados y marcados como NO TOCAR.
- [ ] Secret Zero localizado y accesible.
- [ ] Comando a ejecutar escrito en ticket / chat, copy-paste literal.
- [ ] Diff conceptual revisado por otra persona (owner o agente secundario) si cambio > 5 líneas.

### §1.1 Preflight de intervención en ventana (evergreen — instancia concreta por ventana: mandato P0 del proyecto Backup/DR)

Lecciones de la serie 19-21sep, aplicables a CUALQUIER intervención con ventana. La instancia específica (orden K2→K1→P0-1→P0-2, ABORT por intervención) vive en el mandato de la ventana del proyecto; aquí sólo el mínimo transversal:

- [ ] Estado de negocio verificado con criterio SIN filtro temporal (posiciones/sesiones de Echo por query sin filtro — un filtro de 48h no captura swings de días; lección B3 del 20sep).
- [ ] Backup/conservación previa VERIFICADA (verify TASK OK o sha contra fuente), no sólo creada — es la única reversión real si el mecanismo elimina el volumen origen (`move-volume`/restore/replace lo hacen; ningún `--delete` adicional sin autorización separada).
- [ ] Failure domains declarados antes de tocar: ¿el destino comparte chasis/disco/export con los datos T0? (pool2 comparte chasis con pool0; separa dominio de falla del SO edge, no da redundancia).
- [ ] Health del dominio sin HEALTH_ERR ni degradación activa; si dos componentes comparten recuperación mutua, prohibido intervenirlos en paralelo.
- [ ] Timers verificados ARMADOS antes de fiar del disparo: un trigger absoluto no-persistente (06:05 R2) se pierde si el host está apagado a la hora — ocurrió el 21sep (hermes 01:09-07:36); los Persistent=true sí corrigen en catch-up al arranque.
- [ ] Canal de validación independiente del plano intervenido (no validar por el servicio recién movido; métricas por curl directo, no por los MCPs alojados en el CT migrado).
- [ ] Condiciones ABORT por intervención + criterio de vuelta a operación normal ESCRITOS antes de empezar (instancia: regla 3/4 del mandato P0).
- [ ] Duraciones presupuestadas con mediciones reales (13-39 s vzdump CT chico, restore domina; 116 ~64G hasta 40 min) y punto de corte por unidad completa.

---

## §2. Post-ejecución (después de cualquier cambio)

- [ ] Comando exit 0 verificado.
- [ ] Output esperado comparado con output real.
- [ ] Logs revisados (sin ERROR/WARN unexpected).
- [ ] Smoke test ejecutado (servicio responde).
- [ ] Validación externa (PBS UI, Grafana dashboard, etc.).
- [ ] Ticket cerrado con evidencia.
- [ ] Si algo no salió como se planeó: rollback ejecutado antes de cerrar ticket.

---

## §3. Mensual (1° del mes) — `DESIGNED — NOT IMPLEMENTED` (ítems PBS/Restic/rclone requieren R2/R4/R5; ZFS scrub pool2 sí es candidato real — decisión owner pendiente)

- [ ] PBS verify ejecutado, exit 0.
- [ ] Restic check ejecutado, exit 0.
- [ ] `rclone check` subset sobre último push GDrive, exit 0.
- [ ] ZFS scrub pool0 ejecutado, exit 0.
- [ ] ZFS scrub pool2 ejecutado, exit 0.
- [ ] Ceph health OK.
- [ ] SMART short en todos los SSDs/HDDs.
- [ ] Alertas activas revisadas (ninguna stale).
- [ ] Secret Zero accesibilidad confirmada (bitwarden + USB cifrado).
- [ ] Tickets de restore drill del mes cerrados.
- [ ] Storage % uso revisado: PBS datastore, pool0, pool2, pcloud, GDrive.

---

## §4. Trimestral — `DESIGNED — NOT IMPLEMENTED` (drills cloud requieren R4/R5)

- [ ] Restore drill Restic subset desde pcloud (ap-07 drill 4).
- [ ] Restore drill ZFS chunk desde GDrive (ap-07 drill 5).
- [ ] Revisar retention policies (siguen alineadas con capacidad real).
- [ ] Revisar tier classifications (VMs tier 0/1/2/3 siguen correctas).
- [ ] Rotación de API tokens (PBS, pcloud, GDrive) si aplica.
- [ ] Test restore desde staging local (no solo cloud).

---

## §5. Restore drill (cuando se ejecute)

- [ ] Drill documentado en ticket (qué se restaura, scope).
- [ ] Entorno scratch aislado (no producción).
- [ ] Naming `drill-<vmname>-<date>`.
- [ ] Validación PASS criteria cumplida (ver BACKUP-DR-DESIGN §5 Capa G).
- [ ] Cleanup post-drill.
- [ ] PASS/FAIL registrado en log + ticket + alerta.
- [ ] Si FAIL: Request Change inmediato para investigar.

---

## §6. Semestral

- [ ] Restore drill step-ca (ap-07 drill 6) — owner-driven.
- [ ] Auditoría de obsolescencia: skills, runbooks, memoria.
- [ ] Revisión de decisiones congeladas (siguen vigentes?).
- [ ] Plan de capacidad para próximo año.

---

## §7. DANGEROUS — antes de ejecutar

Cualquiera de estos comandos requiere `DANGEROUS` + aprobación owner:

- [ ] `qm destroy`
- [ ] `qm create` (interrumpe nodo)
- [ ] `zpool attach` / `zpool detach`
- [ ] `zpool remove`
- [ ] `vgremove` / `lvremove`
- [ ] `rm -rf` sobre paths de pools/VGs
- [ ] `rclone purge` sobre remote crypt
- [ ] `restic forget --prune` sobre repo cloud
- [ ] `dd if=/dev/zero of=/dev/sdX`
- [ ] Cualquier comando sobre `local-sqx-*`

Si no está en esta lista pero parece destructivo: `DANGEROUS` por defecto.

---

**Status**: checklist vigente con estados por sección (D0 2026-09-17). §1/§2/§5/§7 transversales; §3/§4 condicionados a mecanismos no implementados.
