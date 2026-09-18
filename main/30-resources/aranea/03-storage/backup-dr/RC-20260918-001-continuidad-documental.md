---
type: request_change
rc_id: RC-20260918-001
status: approved
scope:
  - doc
impact: low
risk: low
owner_review_required: true
origin_session: backup-dr-continuidad-documental-2026-09-18
created_at: 2026-09-18
tags:
  - change/request
  - scope/aranea
  - artifact/doc
  - risk/low
links:
  - "[[BACKUP-DR-DESIGN]]"
  - "[[BACKUP-DR-RUNBOOK]]"
  - "[[BACKUP-DR-CHECKLIST]]"
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[agent-project-02-pbs-on-backup-node]]"
  - "[[2026-09-16-R0-reconciliacion]]"
---

# Request Change: RC-20260918-001 — Corrección de continuidad documental Backup/DR (R1.5)

## Summary

Corregir los residuos documentales que sobrevivieron a D0/R1.5 en 6 artefactos, para que un agente fresco identifique inequívocamente qué está implementado, qué está pendiente y qué instrucciones son exclusivamente históricas. Paquete A–F aprobado por el owner en chat (2026-09-18) y aplicado en la misma sesión.

## Reason

Mandato owner 2026-09-18 (corrección de continuidad documental antes de R2): el índice evergreen decía «NO ejecutado» (falso desde R1); el banner del diseño sólo reconocía R1; runbook y checklist omitían la automatización R1.5 (timers activos); el proyecto PBS mezclaba el procedimiento histórico de creación con el vigente de adopción; el proyecto owner conservaba referencias operativas a crear la VM 180 (obsoleto desde R0: la VM ya existe).

## Evidence

- R0 (2026-09-16): PBS VM 180 ya EXISTE running; «crear VM» quedó obsoleto.
- Change log R1 (2026-09-17): traefik-config, second-brain, hermes-state BACKUP+RESTORE_VERIFIED.
- Change log R1.5 (2026-09-17): etcd-snapshot + pve node-local VERIFIED+AUTOMATED, timers 04:00/05:00/SAT 08:30 activos y probados; pi-hole GATED.
- Escaneo grep 2026-09-18 previo a la corrección: índice con «NO ejecutado» como estado, banners/callouts sólo-R1, «crea VM»/«creación VM» operativos en owner project y README.

## Target artifacts

1. `30-resources/aranea/03-storage/backup-dr/00-index.md` — callout «NO ejecutado» → estado de ejecución real (R0/R1/D0/R1.5 DONE, R2 pendiente gate).
2. `30-resources/aranea/03-storage/backup-dr/BACKUP-DR-DESIGN.md` — banner DESIGN_FROZEN reconoce R1 + R1.5 (una línea; F-01..F-14 intactos).
3. `30-resources/aranea/03-storage/backup-dr/BACKUP-DR-RUNBOOK.md` — §0 incorpora etcd-snapshot y pve-config node-local, párrafo de automatización (timers), callout y footer alineados.
4. `30-resources/aranea/03-storage/backup-dr/BACKUP-DR-CHECKLIST.md` — banner alineado a R1+R1.5 (secciones intactas).
5. `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-02-pbs-on-backup-node.md` — separación física: «Implementation plan — procedimiento vigente (adopción)» + sección «HISTORICAL — creación desde cero» (contenido julio preservado íntegro); rollback dividido en vigente (no destructivo) e HISTORICAL (destructivo); referencias operativas de creación → adopción; AGENT-TASK-02-1/2/3 marcados HISTORICAL; añadida AGENT-TASK-02-0 (gate de adopción).
6. `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-OWNER-PROJECT.md` — razón de OWNER-TASK-MAINT-WINDOW alineada a adopción; estado del calendario superseded incluye R1.5; bitácora 2026-09-18.
7. `10-projects/Aranea/README.md` — resumen ejecutivo con R1.5; ticket 019 dice «adopción/integración PBS 180» (antes «creación VM PBS»).

## Proposed change

Diffs presentados y aprobados por el owner en chat (2026-09-18), opción «Aplicar A–F completo». Sin cambios a CONTRACT §2/§4, F-01..F-14, backup-policy.yaml, tickets 018-021, ni R0/change logs previos. Cero comandos de infraestructura.

## Proposed diff conceptual

Consolidado en el change log `80-agents/journal/logs/2026-09-18-backup-dr-continuidad-documental.md` (7 archivos, 25 patches, hashes pre/post).

## Safety impact

- Ninguno en runtime. Sólo documentación. Historia preservada (nada borrado; julio reubicado bajo etiqueta HISTORICAL).
- El rollback destructivo (`qm destroy 180`) queda confinado a la sección HISTORICAL, subordinado al procedimiento histórico de creación.

## Acceptance criteria

- [x] Índice sin «NO ejecutado» como estado (queda 1 mención explicativa dentro del callout nuevo).
- [x] Banner del diseño menciona R1 + R1.5 y ambos change logs.
- [x] Runbook §0 con 5 unidades + párrafo de automatización R1.5; checklist alineado.
- [x] ap-02: creación desde cero y rollback destructivo exclusivamente bajo secciones HISTORICAL; vigente = adopción con AGENT-TASK-02-0.
- [x] Owner project y README sin referencias operativas a crear la VM 180.
- [x] YAML frontmatter válido en los 7 archivos (parser).
- [x] Grep post: 0 «crea VM»/«creación VM PBS» operativos; «qm destroy» sólo bajo HISTORICAL.

## Rollback plan

Reversión texto a texto: restaurar callout del índice (2 líneas), línea del banner del diseño, §0/callout/footer del runbook, banner del checklist, bloque Implementation plan + Rollback del ap-02, reason del owner project, 2 líneas del README. Los hashes pre/post en el change log permiten restauración exacta.

## Owner decision

- [x] approved (owner 2026-09-18 en chat: «Aplicar A–F completo»; aplicado en la misma sesión)
- [ ] rejected
- [ ] needs changes
