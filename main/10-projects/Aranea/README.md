---
title: "Aranea — Proyectos"
type: index
status: active
icon: 🕸️
slug: aranea-projects-index
area: "[[Aranea]]"
project:
created: 2026-07-02
updated: 2026-07-02
aliases:
  - Aranea projects
  - Proyectos Aranea
tags:
  - aranea
  - homelab
  - kind/index
  - area/aranea
cssclasses:
  - wide
---

# 🕸️ Aranea — Proyectos

> Carpeta por área (convención PARA + AGENTS OS): todos los proyectos del **área [[Aranea]]** viven acá.
> Documentación evergreen (topología, servicios, storage, tickets históricos) sigue en `30-resources/aranea/`.

---

## 🔄 Cierre de sesión 2026-07-02 — handover

> **Status**: sesión cerrada limpiamente. Owner revisará en otra sesión.
> **Perfil del agente**: Ariadna (memoria inyectada).

### 🎯 Lo que se logró hoy (2 hitos)

| # | Hito | Evidencia |
|---|---|---|
| 1 | **Migración Backup/DR a `10-projects/Aranea/`** por convención PARA (proyectos con plazo y tareas) | 15 archivos movidos (1 proyecto, 9 subproyectos, 4 tickets + 1 README + 1 log de cambio); frontmatter corregido en 14 archivos; 0 links rotos |
| 2 | **Instalación operativa de `graphify-obsidian`** en la VM Hermes (venv dedicado + wrapper canónico + alias legacy) | Binario en `~/.local/share/graphify-venv/bin/graphify` (paquete `graphifyy` 0.9.4); wrapper en `~/.local/bin/graphify-obsidian`; smoke tests de `query`, `explain`, `path` pasando contra el grafo vivo (último reindex 2026-07-02 05:25 UTC) |

### 📂 Documentos clave para revisar (links visuales)

#### 🎯 Empezar por aquí (resumen ejecutivo)

- **[[10-projects/Aranea/BACKUP-DR-OWNER-PROJECT]]** ← proyecto owner del refactor Backup/DR, ahora en su ubicación correcta por convención PARA. Design-frozen. 9 subproyectos agente + 4 owner-tasks CRÍTICAS.
- **[[30-resources/aranea/03-storage/backup-dr/00-index]]** ← docs evergreen del refactor (diseño, runbook, checklist, policy). El proyecto migró; los docs se quedaron.
- **[[30-resources/tools/graphify]]** ← nota canónica de la tool, actualizada con el estado "INSTALADO en VM Hermes" y comandos disponibles.

#### 🛠️ Tickets activos (owner-driven, gating implementation)

- **[[10-projects/Aranea/05-tickets/2026-07-02-018-owner-task-critical-vms]]** — open. Confirmar lista tier 0 (VMs críticas). Bloquea ap-02 PBS schedule.
- **[[10-projects/Aranea/05-tickets/2026-07-02-019-owner-task-maint-window]]** — open. Declarar ventana de mantenimiento preferida. Bloquea ap-02 (creación VM PBS).
- **[[10-projects/Aranea/05-tickets/2026-07-02-020-owner-task-secret-zero]]** — open (severity high). Confirmar ubicación caja fuerte + USB cifrado. Bloquea ap-04/ap-05 cloud tier.
- **[[10-projects/Aranea/05-tickets/2026-07-02-021-owner-task-oauth-scope]]** — open (severity high). Decidir quién ejecuta OAuth flows (pcloud/GDrive). Bloquea ap-04/ap-05.

#### 📚 Contexto histórico (sigue vigente)

- **[[30-resources/aranea/03-storage/DESIGN-PROPOSAL]]** — ⚠️ DEPRECATED 2026-07-01 (reemplazado por el set `backup-dr/`) y luego migrado a `10-projects/Aranea/`. Histórico de iteraciones 1-4.
- **[[30-resources/aranea/03-storage/backup-dr/DIFF-CONCEPTUAL]]** — diff conceptual del refactor + nota de migración 2026-07-02 (los archivos del proyecto migraron; los evergreen se quedaron).
- **[[30-resources/aranea/03-storage/backup-dr/BACKUP-DR-DESIGN]]** — diseño congelado, 34 KB, capas A-G, decisiones F-01..F-14.

#### 🧠 Skills / herramientas creadas o tocadas

- **`graphify-obsidian`** — wrapper canónico para retrieval de documentos del vault. Comando verificado funcionando con grafo al día.
- **`graphify`** — alias del wrapper.
- **`graphify-aranea`** — wrapper legacy delegado al binario nuevo (sin cambios necesarios; ya enrutaba bien).
- Skill `second-brain-vault-conventions` — aplicada explícitamente para la decisión de ubicación.

### ⚠️ Restricciones aplicadas (no negociables)

1. **NO comprar HW nuevo** (capex $0) — regla Aranea, no aplica a esta sesión pero se respetó en todo el refactor previo.
2. **NO indexar el vault automáticamente al instalar** — el owner pidió instalar + wrapper fácil; yo no corrí `graphify-obsidian update` (el grafo del día ya estaba vivo del Mac del owner vía LiveSync, last reindex 2026-07-02 05:25 UTC).
3. **NO contaminar el venv de Hermes** — graphify se instaló en venv dedicado `~/.local/share/graphify-venv/` para no romper la toolchain de Hermes.
4. **Convención PARA estricta** — solo proyecto owner + subproyectos agente + tickets migraron a `10-projects/Aranea/`. Documentación evergreen quedó en `30-resources/aranea/03-storage/backup-dr/`.

### ✅ 4 decisiones pendientes del owner (próxima sesión)

1. **Resolver los 4 tickets formales 018-021** (gating completo de la implementación Backup/DR).
2. **Provisionar Graphify local en VM Hermes** si se requiere retrieval allí;
   `graphify-obsidian explain ...` auto-refresca un índice fuera del vault.
3. **Decidir si las otras 3 carpetas de Aranea con material operativo** (`03-storage/`, `02-servicios/`, `04-backups/`) también deberían tener sub-proyectos en `10-projects/Aranea/`, o quedarse como sub-carpetas de `30-resources/aranea/`.
4. **Promover `graphify-personal`** desde stub a wrapper real (apunta a los repos personales `symphony`, `echo`, `sdk`) si quieres que el agente pueda grafar esos codebases en la VM — actualmente solo es alias sin script de soporte.

### 🛣️ Roadmap (no cambios en esta sesión)

Esta sesión NO modificó el roadmap del proyecto Backup/DR (sigue siendo el del iter 4 congelado 2026-07-01):
```
Fase 0 (cuando owner apruebe) → scrub pool2, ceph compact, sanoid config
Fase 1 (~1 día)              → VM PBS en kronos sobre SSD libre
Fase 2 (~medio día)          → ZFS recv en hera
Fase 3 (~medio día)          → rclone crypt sobre pcloud + GDrive
Fase 4 (~medio día)          → pool2 stage + scrub mensual
Fase 5 (continuo)            → restore drills mensuales
```

### 🎓 Lecciones aprendidas (para próxima sesión)

1. **Convención PARA: leer `90-system/convenciones.md` + skill `second-brain-vault-conventions` ANTES de crear o mover archivos del vault.** El proyecto Backup/DR vivía en `30-resources/aranea/03-storage/backup-dr/` por herencia, no por convención. Faltó la validación inicial. Aplicar siempre: ¿el archivo es proyecto (con plazo y tareas) o es evergreen (runbook/policy/diseño)? → define carpeta. → Aplica a TODO el vault, no solo a este proyecto.
2. **`pip install --break-system-packages` en el venv de Hermes** no es opción: contamina la toolchain de Hermes. Para tools no-Hermes → venv dedicado en `~/.local/share/<tool>-venv/` + symlink/wrapper en `~/.local/bin/`. Patrón documentado y replicable para próximas tools.
3. **El wrapper `graphify-obsidian` debe forzar `--graph` al cache local**
   resuelto por `graphify-obsidian cache-path`; nunca al vault.
4. **Las queries del wrapper controlan freshness y auto-refrescan**. No usar
   cron, watcher ni el binario crudo dentro del vault.

### 📊 Métricas de la sesión

- **2 hitos**.
- **~18 archivos movidos/creados/actualizados** (1 proyecto, 9 subproyectos, 4 tickets, 2 índices, 1 wrapper, 1 README, 1 log de migración).
- **14 frontmatters corregidos** (`area: "[[Personal]]"` → `[[Aranea]]`, `area/personal` → `area/aranea`, campos `owner/root/priority/parent` en proyecto raíz).
- **0 links rotos** post-migración (auditado con `search_files`).
- **1 skill operativa nueva en PATH**: `graphify-obsidian`.
- **Capex**: $0. **Opex mensual**: $0.

### ⏸️ Lo que NO se hizo (esperando input del owner)

- ❌ Ningún ticket 018-021 resuelto (pendiente decisión owner).
- ❌ Ningún comando de implementación ejecutado en VMs Aranea.
- ❌ `graphify-obsidian update` no se corrió (grafo vivo del Mac del owner vía LiveSync fue suficiente para `query/explain/path`).
- ❌ `graphify-personal` no se implementó (queda como stub legacy; no afecta la sesión de hoy).

---

## 📑 Índice de proyectos

| # | Proyecto | Status | Owner | Prioridad | Doc |
|---|---|---|---|---|---|
| 1 | [[BACKUP-DR-OWNER-PROJECT]] | design-frozen | me | P1 | proyecto owner |
| 2 | [[SERVICIOS-DOCS-OWNER-PROJECT]] | paused | me | P1 | proyecto pausado (prioridad Backup/DR) |

## 📂 Estructura

```
10-projects/Aranea/
├── README.md                                    (este archivo)
├── BACKUP-DR-OWNER-PROJECT.md                   (proyecto owner — design-frozen)
├── SERVICIOS-DOCS-OWNER-PROJECT.md              (proyecto paused — prioridad Backup/DR)
├── agentes/                                     (subproyectos de agente — owner: agent)
│   ├── agent-project-00-policy-and-doc-cleanup.md
│   ├── agent-project-01-critical-config-backup.md
│   ├── agent-project-02-pbs-on-backup-node.md
│   ├── agent-project-03-app-consistent-data-backups.md
│   ├── agent-project-04-cloud-critical-tier.md
│   ├── agent-project-05-cloud-bulk-archive-tier.md
│   ├── agent-project-06-observability-and-alerting.md
│   ├── agent-project-07-restore-drills.md
│   ├── agent-project-08-session-closeout-and-learning-loop.md
│   └── agent-project-09-service-docs-rollout.md  (paused — prioridad Backup/DR)
└── 05-tickets/                                  (tickets formales del proyecto)
    ├── 2026-07-02-018-owner-task-critical-vms.md
    ├── 2026-07-02-019-owner-task-maint-window.md
    ├── 2026-07-02-020-owner-task-secret-zero.md
    ├── 2026-07-02-021-owner-task-oauth-scope.md
    └── 2026-07-02-022-deferred-service-docs.md  (paused — prioridad Backup/DR)
```

## 📝 Convention

- **Proyectos del área Aranea** → esta carpeta, un archivo por proyecto (sin subcarpeta propia).
- **Subproyectos de agente** (`owner: agent`) → `agentes/`, con `parent: "[[Proyecto humano padre]]"`.
- **Tickets formales** → `05-tickets/`, uno por owner-task o blocker.
- **Documentación evergreen** del refactor → `30-resources/aranea/03-storage/backup-dr/`.

## ➕ Cómo agregar un nuevo proyecto de Aranea

1. Crear el archivo `.md` en `10-projects/Aranea/` desde el template `70-templates/project.md`.
2. Setear `area: "[[Aranea]]"`, `owner: me`, `root: true` (si es iniciativa raíz) o `parent: "[[...]]"`.
3. Si tiene subproyectos de agente, crear `agentes/<slug>.md` con `parent: "[[Proyecto raíz]]"`.
4. Si tiene tickets, crear `05-tickets/<YYYY-MM-DD-NNN-slug>.md`.
5. Actualizar este README (agregar fila en la tabla).
6. Log en `80-agents/journal/logs/`.

## 🔗 Links

- [[20-areas/Aranea]] — nota de área (visión, estado, servicios, riesgos)
- [[30-resources/aranea/00-index]] — índice de docs evergreen
- [[30-resources/aranea/03-storage/backup-dr/00-index]] — índice de docs Backup/DR
- [[30-resources/tools/graphify]] — nota canónica de la tool graphify (estado actualizado)
- [[80-agents/journal/logs/2026-07-02-aranea-backup-dr-migration-to-10-projects]] — log de migración
