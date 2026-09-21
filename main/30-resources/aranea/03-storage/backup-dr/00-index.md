---
title: "Backup/DR — Índice del refactor (docs evergreen)"
type: index
schema_version: 1
status: active
icon: 📚
slug: backup-dr-index
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-09-21
tags: [kind/index, area/aranea, project/agents-os, topic/backup, topic/disaster-recovery]
related: []
cssclasses: wide
---

# 📚 Backup/DR — Índice del refactor (documentación evergreen)

## 📊 De un vistazo

> **Una sola verdad activa**: este set de docs reemplaza `DESIGN-PROPOSAL.md` y `PROPUESTA-COMPLETA-ITER4.md` (ambos marcados deprecated).
>
> **Estado de ejecución (al 2026-09-18)**: la nota «NO ejecutado» anterior quedó obsoleta. Ejecutado y verificado: R0 reconciliación (2026-09-16), R1 bootstrap-config (2026-09-17: traefik-config, second-brain, hermes-state BACKUP+RESTORE_VERIFIED en staging Hermes — NO offsite), D0 saneamiento documental, R1.5 config completion (2026-09-17: etcd-snapshot + pve node-local VERIFIED+AUTOMATED, timers activos; pi-hole GATED). **R2 (2026-09-18 tarde/noche): PILOTO PBS EJECUTADO bajo mandato owner (sin reboot): disco nuevo `vm-180-disk-1` 300G + datastore `main` (fstab UUID nofail + dir 000 anti-mount-vacío), `backup@pbs` + token con ACL mínima verificada (rol `DatastoreBackup`, sin Prune/Modify), storage `aranea-pbs` active 5/5, backup piloto 155 PASS (25s, verify ok, 731M/295G), restore estructural CT 990 PASS (sin boot, fixture destruido). HALLAZGO: mp0 etcd excluido por config del CT 155 → datos NO entran al backup (decisión owner pendiente). Retención/schedules NO configurados; reboot PBS real pendiente de ventana; R2 NO certificado (faltan criterios 7d). CIERRE DEL PILOTO (2026-09-18 noche): diagnóstico definitivo — mp0 excluido por DEFAULT de PVE 8.4 (familia etcd completa comparte patrón; rootfs SÍ entra); decisión provisional MANTENER exclusión de facto, datos protegidos por R1 lógico (restore offline re-demostrado); procedimiento recuperación combinada PBS+snapshot lógico documentado (R3 servicio/R4 quorum NO demostrados). CORRECCIÓN: dir 000 anti-mount-vacío NO quedó aplicada (755 real) → riesgo escritura en raíz si falta el volumen; fail-closed propuesto (drop-in systemd Requires-mount) en bundle v3 Acción 1. Baseline 733M/295G + umbrales 70/85%; plan medición 7d acotado (7 CTs local-lvm, sin estado persistente) NO activado; Ceph pool1 87.16% nearfull → kafka GATED (no afecta set activo). Bundle ÚNICO v3 (3 acciones independientes: fail-closed / medición 7d / reboot) ESPERA OK owner. Evidencia: `80-agents/journal/logs/2026-09-18-r2-closeout.md`. EJECUCIÓN DEL MANDATO (misma noche, owner aprueba 1+2 y rechaza 3): fail-closed INSTALADO+VALIDADO en `proxmox-backup` Y `proxmox-backup-proxy` (extensión: proxy=ingreso de backups; PENDING ACTIVATION — requiere reinicio/reboot GATED, PASS no declarado); piloto 7d: driver preparado+validado, NO activado (gate insatisfecho; activación documentada en `~/aranea/work/r2-pbs-20260918/measurement/README-ACTIVACION.md`); ventana reconciliada 06:00–07:25; CORRECCIÓN placement: CT 148 rootfs en pool1 Ceph → auto-gated con pool1 ≥85% (87.21%), set efectivo 6 CTs; baseline v3 §0 sin drift. Evidencia: `80-agents/journal/logs/2026-09-18-r2-mandato-ejecucion.md`. REBOOT+ACTIVACIÓN (2026-09-19, mandato owner 2): reboot único PASS (boot 22:24, 15/15 checks, API+auth 200, aranea-pbs 5/5 active); **FAIL-CLOSED PASS declarado** (Requires de la mount en vivo en ambos servicios; A/B/C/D); **piloto 7d ACTIVO** — 6 CTs (148 excluido permanente), primer disparo PROGRAMADO dom 20sep 06:05, expiración absoluta 2026-09-26, umbrales/ventana/auto-disable probados, fix disable_timer→sudo. Evidencia: `80-agents/journal/logs/2026-09-19-r2-reboot-failclosed-activation.md`.** Roadmap R0–R8: `[[2026-09-16-R0-reconciliacion]]` §9. Lo único ejecutable con evidencia: `BACKUP-DR-RUNBOOK` §0.
> **Sesión cerrada por owner**: 2026-07-01 (histórico; proyecto reactivado 2026-09-16).
>
> **2026-07-02**: el **proyecto owner** (la ejecución con plazo y tareas) se migró a `[[BACKUP-DR-OWNER-PROJECT]]`; su ubicación vigente es `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/`. Este folder conserva solo la **documentación evergreen** del refactor: diseño, runbook, checklist, policy, template, diff conceptual y workflow de cambios. Los **subproyectos de agente** (ejecución con tareas `#owner/agent`) viven en `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/`. Los **tickets formales** (018-021) viven en `10-projects/Aranea/05-tickets/`.

---

## 📂 Catálogo

| # | Archivo | Rol | Tamaño |
|---|---|---|---|
| 0 | `DIFF-CONCEPTUAL.md` | Diff conceptual previo (qué cambiaría, qué eliminar, qué mantener) | 19 KB |
| 1 | `BACKUP-DR-DESIGN.md` | Diseño final corregido. Capas A-G. Decisiones congeladas. **Doc canónico de diseño.** | 34 KB |
| 2 | `BACKUP-DR-RUNBOOK.md` | Verdad operacional humana (comandos paso a paso) | 5 KB |
| 3 | `BACKUP-DR-CHECKLIST.md` | Pre/post/mes/trimestral/drill | 4 KB |
| 4 | `backup-policy.yaml` | Policy ejecutable (cambios solo via Request Change) | 10 KB |
| 5 | `backup-inventory-template.json` | Template inventario con JSON Schema | 10 KB |
| 6 | `REQUEST-CHANGES.md` | Workflow de evolución controlada | 5 KB |
| 7 | `RESTORE-DRILL-TEMPLATE.md` | Template de drill (reusable, copy-paste) | 9 KB |
| 8 | `FORMULARIO-DECISIONES.md` | **Formulario para responder los 4 tickets 018-021**. Owner edita en Obsidian y avisa por Telegram. | 9 KB |

**Total**: ~105 KB de docs + policy + template + formulario.

---

## 📂 Ubicación vigente bajo `10-projects/Aranea/`

| Antes | Ahora | Por qué |
|---|---|---|
| `BACKUP-DR-OWNER-PROJECT.md` | `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-OWNER-PROJECT.md` | Proyecto con plazo y tareas → carpeta propia bajo su área |
| `agent-project-00..08` (9 archivos) | `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-00..08` | Subproyectos de agente → `agentes/` de la iniciativa padre |
| (no estaban aquí) | `10-projects/Aranea/05-tickets/2026-07-02-018..021` | Tickets formales → `<proyecto>/05-tickets/` |

---

## 🗺️ Cómo leer este set

**Si eres el owner y quieres aprobar/rechazar**: lee `DIFF-CONCEPTUAL.md` primero.

**Si eres un agente que va a implementar**: lee en este orden:
1. `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-OWNER-PROJECT` (mapa general).
2. `BACKUP-DR-DESIGN.md` (la policy).
3. Tu `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-XX` específico (implementación).
4. `BACKUP-DR-RUNBOOK.md` (comandos operativos).
5. `BACKUP-DR-CHECKLIST.md` (validación).
6. `backup-policy.yaml` (parámetros).
7. `backup-inventory-template.json` (estructura inventario).

**Si quieres proponer un cambio**: lee `REQUEST-CHANGES.md` template.

---

## 🔗 Documentos históricos (mantenidos, no son verdad activa)

- `../DESIGN-PROPOSAL.md` — iter 1-4, ahora deprecated.
- `../PROPUESTA-COMPLETA-ITER4.md` — consolidación previa, ahora deprecated.
- `../BACKUP-SYSTEM.md` — Task 2 previa (políticas detalladas).
- `../AUDIT.md` — auditoría storage previa.
- `../TOPOLOGY-AUDIT.md` — auditoría topológica (10 hallazgos).

---

## 🔗 Tickets relacionados

- `10-projects/Aranea/05-tickets/2026-07-02-018` a `021` — owner tasks formales (4 tickets).
- `../../../05-tickets/2026-06-30-013-storage-redesign-backup-design.md` — ticket origen del refactor, ahora superseded.

---

## 📂 Path completo

```
VAULT_ROOT/30-resources/aranea/03-storage/backup-dr/
├── 00-index.md                       (este archivo — index de docs evergreen)
├── DIFF-CONCEPTUAL.md
├── BACKUP-DR-DESIGN.md
├── BACKUP-DR-RUNBOOK.md
├── BACKUP-DR-CHECKLIST.md
├── backup-policy.yaml
├── backup-inventory-template.json
├── REQUEST-CHANGES.md
├── RESTORE-DRILL-TEMPLATE.md
└── FORMULARIO-DECISIONES.md          ← responder acá los 4 tickets 018-021
```

**El proyecto de ejecución vive en**:
```
VAULT_ROOT/10-projects/Aranea/
├── README.md                         (índice de proyectos de Aranea)
├── BACKUP-DR-OWNER-PROJECT/
│   ├── BACKUP-DR-OWNER-PROJECT.md
│   ├── BACKUP-DR-CONTRACT.md
│   └── agentes/
│       ├── agent-project-00-policy-and-doc-cleanup.md
│       ├── agent-project-01-critical-config-backup.md
│       ├── agent-project-02-pbs-on-backup-node.md
│       ├── agent-project-03-app-consistent-data-backups.md
│       ├── agent-project-04-cloud-critical-tier.md
│       ├── agent-project-05-cloud-bulk-archive-tier.md
│       ├── agent-project-06-observability-and-alerting.md
│       ├── agent-project-07-restore-drills.md
│       └── agent-project-08-session-closeout-and-learning-loop.md
└── 05-tickets/
    ├── 2026-07-02-018-owner-task-critical-vms.md
    ├── 2026-07-02-019-owner-task-maint-window.md
    ├── 2026-07-02-020-owner-task-secret-zero.md
    └── 2026-07-02-021-owner-task-oauth-scope.md
```

---

**Status**: design-frozen.
**Sesión cerrada por instrucción del owner**: 2026-07-01.
**Migración a 10-projects/Aranea/**: 2026-07-02 (ver log `80-agents/journal/logs/2026-07-02-aranea-backup-dr-migration-to-10-projects.md`).
