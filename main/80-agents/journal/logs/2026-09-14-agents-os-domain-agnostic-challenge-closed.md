---
type: change_log
schema_version: 1
scope: session
created: "2026-09-14"
updated: "2026-09-14"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[AGENTS OS - Desarrollo Agnóstico por Dominio]]"
  - "[[AGENTS OS - Context Hygiene and Canonical Integrity]]"
  - "[[doctor-verde-falso-por-duplicados-core-federado]]"
aliases:
  - challenge desarrollo agnostico cerrado
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Challenge del proyecto de desarrollo agnóstico cerrado y corrección reubicada

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated + created
- **Archivo(s):**
  - `80-agents/memory/public/known-error/agents-os/doctor-verde-falso-por-duplicados-core-federado.md` (created)
  - `10-projects/Personal/AGENTS OS/agentes/AGENTS OS - Desarrollo Agnóstico por Dominio.md` (updated → `archived`)
  - `10-projects/Personal/AGENTS OS/agentes/AGENTS OS - Context Hygiene and Canonical Integrity.md` (updated → PHASE 3.5)
  - `10-projects/Personal/AGENTS OS/AGENTS OS.md` (updated → corrección de estado)

## Motivo

- El owner pidió validar si un plan de cinco fases, derivado de un harness externo, aportaba de verdad. El challenge adversarial lo cerró en `NOT_READY` y dos agentes convergieron en un consenso explícito.
- La constitución exige `change_log` consolidado ante cambios en proyectos y memoria pública.

## Fuentes usadas

- `80-agents/skills/agents-os-doctor/scripts/doctor.py` (ejecutado), `30-resources/agents-os/core-export/{sources.list,build-core.py}`, `80-agents/skills/agents-os-bootstrap/SKILL.md`, `80-agents/agents-os/agent-constitution.md`, `30-resources/agents/skills/sdd-workflow/SKILL.md`, comparación byte a byte entre `80-agents/` y `30-resources/`.

## Resolución aplicada

- Se descartó crear `agent-development-workflow`, la capa de capabilities abstractas, el `autonomy envelope` y el dominio ficticio. `delivery checkpoint` queda en backlog hasta tener consumidor concreto.
- El proyecto de diseño pasó a `archived` como registro del challenge; D6 salió de "Decisiones cerradas" y los gates G1-G4 quedaron cancelados.
- La corrección real se incorporó como PHASE 3.5 de Context Hygiene, antes del Doctor unificado: deduplicar skills y runbooks con `30-resources/` como autoridad, corregir `sources.list` y `build-core.py` en el mismo cambio atómico, externalizar el registro de dominios con resolución `0/1/>1` fail-closed, desacoplar el hot path incluida la constitución, y dejar la detección como check nuevo del provider `Canonical`.
- Se corrigió el cockpit: Context Hygiene no estaba entregado en Review; va 75% con PHASE 4 congelada sin runtime.

## Validación

- `agents-os-doctor`: `HIGH=0 MEDIUM=13` al momento del diagnóstico; los 13 quedaron explicados como migración federada incompleta, no como deuda de índice.
- Duplicación verificada por comparación byte a byte: 13 skills (12 idénticas) y 9 runbooks con tres divergencias materiales (172, 143 y 4 líneas).
- Referencias del artefacto exportado verificadas en la copia construida del core; la constitución viaja con reglas operativas de dominio.
- Sin cambios de runtime, tooling, bootstrap ni routers en esta sesión.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir los tres archivos de proyecto a su estado del 2026-09-13/14 y borrar el known error. Nada más fue tocado, así que el rollback es documental y completo.
