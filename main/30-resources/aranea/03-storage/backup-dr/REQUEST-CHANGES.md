---
title: "REQUEST-CHANGES — Cambios propuestos a policy/runbook/skill/memory"
type: doc
schema_version: 1
status: active
icon: 🔄
slug: backup-dr-request-changes
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-08-10
tags:
  - kind/doc
  - area/personal
  - project/agents-os
  - domain/backup-dr
  - doc/request-changes
  - workflow/change-request
related:
  - "[[BACKUP-DR-DESIGN]]"
parent: "[[BACKUP-DR-OWNER-PROJECT]]"
cssclasses: wide
---

# 🔄 REQUEST-CHANGES — Cambios propuestos a policy/runbook/skill/memory

## Propósito

Documentar el workflow legacy para proponer cambios controlados a artefactos Backup/DR; esta nota no es un `change_log` ni registra por sí sola un cambio aplicado.

## Contenido

> Workflow de evolución controlada. **Cualquier cambio a policy/runbook/skill/memory debe producir un Request Change**, no una edición silenciosa.
>
> **Reglas**:
> 1. NO editar `backup-policy.yaml` directamente — abrir RC.
> 2. NO editar `BACKUP-DR-DESIGN.md` para cambiar decisiones congeladas — abrir RC.
> 3. NO modificar memoria del agente en bulk — abrir RC.
> 4. Owner revisa cada RC y aprueba/rechaza.

---

## Template de Request Change

```markdown
---
type: request_change
rc_id: RC-YYYYMMDD-XXX
status: proposed
scope:
  - policy | runbook | skill | memory | inventory | template | project
impact: low | medium | high | critical
risk: low | medium | high | destructive
owner_review_required: true
origin_session: <session-id-or-link>
created_at: <ISO-8601>
tags:
  - change/request
  - scope/<area>
  - artifact/<policy|runbook|skill|memory|inventory|template|project>
  - risk/<low|medium|high|destructive>
links:
  - <related-doc>
---

# Request Change: <title>

## Summary

## Reason

## Evidence

## Target artifacts

## Proposed change

## Proposed diff conceptual

## Safety impact

## Acceptance criteria

## Rollback plan

## Owner decision
- [ ] approved
- [ ] rejected
- [ ] needs changes
```

---

## RC abiertos (estado)

### (vacío — sin RC abiertos al cierre de sesión 2026-07-01)

Cuando se abra el primer RC, agregarlo aquí con formato:

```markdown
### RC-YYYYMMDD-XXX — <título>
- status: proposed | approved | rejected | needs_changes
- scope: ...
- impact: ...
- risk: ...
- created_at: ...
- owner_decision: ...
- link: (anclar el doc del RC)
```

---

## Ejemplos de RC probables (no abiertos)

Estos son RC que se ANTICIPAN que se necesitarán durante implementación o evolución. NO son reales hasta que se abran formalmente.

### RC-anticipado-1: ampliar tier 0 con VMs adicionales

- **Cuándo**: después de validar 30d de backups, owner puede pedir agregar VMs a tier 0.
- **Target**: `backup-policy.yaml` tiers.tier_0.candidates_pending_owner.
- **Proposed change**: agregar vmid y nombre.
- **Acceptance**: drills PASS en 3 ciclos consecutivos.

### RC-anticipado-2: rotar passphrase Restic

- **Cuándo**: cada 12 meses (próximo: 2027-07).
- **Target**: Secret Zero + `backup-policy.yaml`.
- **Proposed change**: nueva passphrase + actualizar bitwarden + USB cifrado.
- **Rollback**: restaurar passphrase anterior (improbable si comprometido).

### RC-anticipado-3: agregar tier bulk secundario (ej. Backblaze B2)

- **Cuándo**: si GDrive muestra problemas o cierra cuenta.
- **Target**: `backup-policy.yaml` cloud_tiers.
- **Proposed change**: nuevo provider con chunking + manifest + check.
- **Acceptance**: restore drill subset PASS.

### RC-anticipado-4: incluir backup externo Ceph si hades SPOF materializa

- **Cuándo**: si hades cae una vez y causa pérdida material.
- **Target**: `backup-policy.yaml` (rompe F-10).
- **Proposed change**: habilitar `rbd export` weekly → PBS.
- **Riesgo**: contradice F-10 congelada. Requiere RC con impacto crítico.
- **Rollback**: revertir rbd export jobs.

### RC-anticipado-5: cambiar ventana de mantenimiento

- **Cuándo**: owner re-evalúa horarios.
- **Target**: `backup-policy.yaml` jobs.*.time + cron jobs.
- **Proposed change**: nuevos horarios.

### RC-anticipado-6: agregar nodo backup secundario (NO hades)

- **Cuándo**: si kronos como único PBS host se considera SPOF.
- **Target**: `backup-policy.yaml` destinations.
- **Restriction**: requiere comprar HW (rompe F-01) o reusar otro SSD libre.
- **Discusión previa**: si hay SSD libre en otro nodo (no SQX).

---

## Workflow para abrir un RC

1. Crear archivo `RC-YYYYMMDD-XXX-<titulo>.md` en esta carpeta.
2. Llenar template completo.
3. Owner notificado (Telegram + dashboard).
4. Owner revisa y emite decisión en el doc (approved/rejected/needs_changes).
5. Si approved: ejecutar el cambio + actualizar este README.
6. Si rejected: archivar con motivo.
7. Si needs_changes: iterar.

---

## Auditoría de RC

Mensualmente (1° del mes) revisar:
- RC abiertos > 30d sin decisión → escalar.
- RC rechazados con motivo recurrente → considerar cambio de policy.
- RC aprobados ejecutados correctamente → cerrar formalmente.

---

**Status**: active (vacío al cierre). Workflow definido.
**Sesión cerrada por instrucción del owner**: 2026-07-01.
