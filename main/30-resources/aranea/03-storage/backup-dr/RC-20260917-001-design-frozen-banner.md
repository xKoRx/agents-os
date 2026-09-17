---
type: request_change
rc_id: RC-20260917-001
status: proposed
scope:
  - doc
impact: low
risk: low
owner_review_required: true
origin_session: D0-documentation-consistency-2026-09-17
created_at: 2026-09-17
tags:
  - change/request
  - scope/aranea
  - artifact/doc
  - risk/low
links:
  - "[[BACKUP-DR-DESIGN]]"
  - "[[REQUEST-CHANGES]]"
---

# Request Change: RC-20260917-001 — Banner de estado DESIGN_FROZEN en BACKUP-DR-DESIGN

## Summary

Añadir al inicio del cuerpo de `BACKUP-DR-DESIGN.md` (inmediatamente después del título `# 🛡️ BACKUP-DR-DESIGN — Diseño final Backup/DR Aranea`) un callout de advertencia que haga explícita dentro del propio documento su condición `DESIGN_FROZEN` y la distinción diseño-aprobado vs implementación verificada.

## Reason

Mandato D0 (manager review, punto 3): el documento de diseño describe implementaciones hoy superadas o inexistentes (PBS integrado, dumps, cloud tiers, stack de alertas) sin que su condición congelada sea explícita dentro del propio archivo. Un agente que recupere sólo el DESIGN no distingue diseño de operación.

## Evidence

- R0 2026-09-16: 0 mecanismos de backup operativos; PBS VM 180 running pero sin integrar.
- R1 2026-09-17: únicas unidades VERIFIED = traefik-config, second-brain, hermes-state (staging Hermes, no offsite).
- `BACKUP-DR-DESIGN.md` §0 TL;DR y §8.1 contienen referencias a mecanismos no implementados sin banner de estado (§8.1 menciona `docker-observability`, históricamente; la plataforma vigente es ARGUS vm 160).

## Target artifacts

- `30-resources/aranea/03-storage/backup-dr/BACKUP-DR-DESIGN.md` — UNA inserción de callout + `updated` en frontmatter.

## Proposed change

Texto exacto del callout (sin tocar ninguna otra línea; F-01..F-14 intactos):

```markdown
> [!warning] DESIGN_FROZEN — documento de diseño, NO estado operativo
> Este documento está **congelado**: describe la arquitectura objetivo aprobada (F-01..F-14, capas A-G), no lo implementado. Lo VERIFIED hoy (R1, 2026-09-17): staging Hermes con traefik-config, second-brain y hermes-state — ver `BACKUP-DR-RUNBOOK` §0 y change log `2026-09-17-backup-dr-r1-bootstrap-config`. Estado del proyecto y roadmap vigente: `[[2026-09-16-R0-reconciliacion]]` §9. Las secciones cuyo mecanismo no existe aún (PBS integrado, dumps, cloud tiers) NO deben ejecutarse desde este documento.

```

## Proposed diff conceptual

```diff
 # 🛡️ BACKUP-DR-DESIGN — Diseño final Backup/DR Aranea
+
+> [!warning] DESIGN_FROZEN — documento de diseño, NO estado operativo
> Este documento está **congelado**: describe la arquitectura objetivo aprobada (F-01..F-14, capas A-G), no lo implementado. Lo VERIFIED hoy (R1, 2026-09-17): staging Hermes con traefik-config, second-brain y hermes-state — ver `BACKUP-DR-RUNBOOK` §0 y change log `2026-09-17-backup-dr-r1-bootstrap-config`. Estado del proyecto y roadmap vigente: `[[2026-09-16-R0-reconciliacion]]` §9. Las secciones cuyo mecanismo no existe aún (PBS integrado, dumps, cloud tiers) NO deben ejecutarse desde este documento.


 ## Propósito
```

## Safety impact

- Ninguno en runtime. Cambio de presentación documental.
- NO modifica decisiones congeladas F-01..F-14, capas, retention, proveedores ni clasificación Tier 0.
- NO crea segunda policy ni altera intención owner.

## Acceptance criteria

- El banner existe al inicio del cuerpo del DESIGN y menciona lo VERIFIED (R1) y el roadmap R0-R8.
- `diff` del archivo = exactamente la inserción del callout + `updated:` en frontmatter.
- Ningún bloque de decisiones congeladas difiere.

## Rollback plan

Eliminar el callout insertado y restaurar `updated:` — reversión de una inserción.

## Owner decision

- [ ] approved
- [ ] rejected
- [ ] needs changes
