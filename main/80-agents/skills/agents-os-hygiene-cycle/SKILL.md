---
type: skill
name: agents-os-hygiene-cycle
scope: global
created: 2026-07-14
updated: 2026-08-08
description: Orchestrate periodic AGENTS OS maintenance by regularizing misaligned notes, processing accumulated System 1 and Graphify feedback through Kaizen, promoting reusable value, writing shareable change logs for system changes, and reindexing Graphify. Use for scheduled weekly/monthly hygiene, before sharing improvements with the team, after repeated feedback, or when the user asks to clean, align, compact, or improve AGENTS OS.
tags:
  - kind/skill
  - action/hygiene
  - action/kaizen
  - tech/agents-os
---

# agents-os-hygiene-cycle

## Purpose

Ejecutar el ciclo periódico completo que mantiene AGENTS OS alineado y convierte
fricción acumulada en mejoras verificables y compartibles.

## Minimal Read

1. `../agents-os-hygiene-review/SKILL.md`
2. `../agents-os-kaizen-memory/SKILL.md`
3. `../agents-os-graphify-maintenance/SKILL.md`
4. `../../templates/change-log.md`
5. El último reporte bajo `../../journal/hygiene/`, si existe.
6. El último reporte bajo `../../journal/feedback/kaizen-reports/`, si existe.

## Procedure

1. Determinar ventana y cadencia:
   - uso activo: semanal;
   - uso liviano: mensual;
   - ejecutar antes si se acumulan 10 feedbacks nuevos o aparece un blocker;
   - respetar otra frecuencia confirmada en el perfil local.
2. Ejecutar `agents-os-hygiene-review` con `since-last-review`; usar
   `full-system-1` solo para auditorías profundas o antes de una release.
3. Regularizar automáticamente únicamente lo permitido por la Fix Policy de la
   skill de higiene. Verificar los hallazgos antes de editar.
4. Ejecutar `agents-os-kaizen-memory` sobre feedbacks posteriores a su último
   watermark. Agrupar patrones, ruido de retrieval, fallas de Graphify,
   redundancias, fricción de templates y oportunidades de skills.
5. Promover valor reusable solo cuando haya evidencia suficiente:
   - patrón repetido en dos o más sesiones;
   - blocker severo reproducible; o
   - mejora medible confirmada por un forward-test.
6. Clasificar cada promoción como learning, decision, known error, runbook,
   skill, contrato, template o corrección de una entidad canónica. Invocar la
   skill especializada correspondiente; no mezclar tipos de artefacto.
7. Si la corrida modifica constitución, reglas, skills, templates, contratos,
   memoria pública o entidades Sistema 2, crear un único change log agregado:
   - ruta: `80-agents/journal/logs/YYYY-MM-DD-agents-os-hygiene-cycle.md`;
   - `share_scope: team` para mejoras agnósticas y reutilizables;
   - `share_scope: local` para ajustes del perfil o contexto personal;
   - incluir feedbacks fuente, archivos afectados, decisión, validación y
     rollback o forma de revertir;
   - excluir identidad, paths locales, contenido de memoria interna y secretos.
8. Reindexar mediante `agents-os-graphify-maintenance` si hubo cambios
   indexables. Validar títulos canónicos, una relación y una memoria promovida.
9. Actualizar los reportes de higiene/Kaizen y fijar el siguiente review. Dejar
   propuestas estructurales pendientes cuando requieran decisión humana.

## Output

```text
Window:
Hygiene report:
Notes regularized:
Feedbacks processed:
Promotions:
System changes:
Change log: none | local | team
Graphify:
Next review:
Pending decisions:
```

## Hard Rules

- No convertir una queja aislada en regla compartida salvo blocker severo.
- No hacer rewrites masivos ni compactar memoria sin juicio por nota.
- No exponer memoria interna en reportes o change logs.
- No etiquetar como `team` un cambio que contiene identidad, paths o preferencias.
- No cambiar una fuente canónica sin log y validación proporcional.
- No crear una automatización recurrente sin aprobación y cadencia explícita.
- No declarar la corrida exitosa si Graphify queda stale tras cambios indexables.
