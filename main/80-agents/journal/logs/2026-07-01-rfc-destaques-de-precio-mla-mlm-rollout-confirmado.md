---
type: change_log
scope: session
created: "2026-07-01"
updated: "2026-07-01"
area: "[[Meli]]"
project: "[[Bajo y Muy Bajo Precio]]"
application:
entities:
  - "[[Meli]]"
related:
  - "[[RFC Destaques de Precio - Hito 2]]"
aliases:
  - rfc destaques de precio rollout mla mlm
confidence: verified
source_session: "2026-07-01-rfc-destaques-de-precio-hito2-mla-mlm-rollout-summary"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# RFC Destaques de Precio - Rollout MLA/MLM Confirmado

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/slugs son solo automatización. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `sb-main/01_Projects/previous-price-motors/rfc.md`
  - `sb-main/01_Projects/previous-price-motors/Destaques de Precio — Polycard Search — Spec Técnica Propuesta.md`
  - `sb-main/01_Projects/previous-price-motors/Destaques de Precio — VIP — Spec Técnica Propuesta.md`
  - `10-projects/Destaques de Precio/Bajo y Muy Bajo Precio.md`

## Motivo

- El usuario confirmó que el rollout de Hito 2 (Destaques de Precio vía Sugeridor 2.0) se ejecutará en MLA y MLM, reemplazando el estado anterior donde MLM figuraba como "candidato de rollout por madurez, requiere confirmación de scope".

## Fuentes usadas

- Instrucción directa del usuario en esta sesión.
- RFC y specs técnicas legacy existentes en `sb-main/01_Projects/previous-price-motors/`.

## Resolución aplicada

- RFC: tabla de alcance por señal, tabla de madurez de Sugeridor por site, rollout propuesto, config JSON de sites y pendientes de definición actualizados para reflejar MLA+MLM confirmados.
- Specs técnicas Search/VIP: acotado el alcance explícito a MLA/MLM (flujo Sugeridor); MLB queda fuera de estos dos documentos porque usa un flujo separado (FIPE), documentado solo en el RFC.
- Proyecto Obsidian: estado actual y bitácora actualizados; se linkeó el nuevo proyecto de agente de seguimiento del RFC.
- Nota de excepción: `sb-main` tiene una política vigente (`CLAUDE.md`, `sdd-process.md`) que prohíbe RFC/specs locales — deberían vivir en Google Doc/Spellbook. Se decidió con el usuario mantener el RFC y specs en el archivo legacy local existente como excepción, no migrar en esta sesión.

## Validación

- Ediciones puntuales verificadas por lectura del diff aplicado (Edit tool), sin reescritura completa de archivos.
- Pendiente: el usuario debe evaluar si migra a Google Doc/Spellbook para alinear con la política vigente de `sb-main`.
