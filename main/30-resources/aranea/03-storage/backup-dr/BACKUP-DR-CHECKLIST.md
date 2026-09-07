---
title: "BACKUP-DR-CHECKLIST — Checklists operacionales"
type: runbook
scope: project
icon: ✅
slug: backup-dr-checklist
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-07-01
tags: [aranea, backup, checklist, ops, kind/runbook, area/personal, project/agents-os]
related: "[[BACKUP-DR-DESIGN]]"
parent: "[[BACKUP-DR-OWNER-PROJECT]]"
cssclasses: wide
---

# ✅ BACKUP-DR-CHECKLIST — Checklists operacionales

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

## §3. Mensual (1° del mes)

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

## §4. Trimestral

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

**Status**: design-frozen. Checklists NO ejecutados.
**Sesión cerrada por instrucción del owner**: 2026-07-01.
