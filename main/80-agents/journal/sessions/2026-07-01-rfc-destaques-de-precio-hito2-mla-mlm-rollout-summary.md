---
type: session
scope: session
created: "2026-07-01"
updated: "2026-07-01"
area: "[[Meli]]"
project: "[[RFC Destaques de Precio - Hito 2]]"
application:
entities:
  - "[[Meli]]"
related:
  - "[[Bajo y Muy Bajo Precio]]"
aliases: []
confidence: high
source_session: "2026-07-01-rfc-destaques-de-precio-hito2-mla-mlm-rollout"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# 2026-07-01 - RFC Destaques de Precio Hito 2 - Rollout MLA/MLM

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Actualizar el proyecto "Bajo y Muy Bajo Precio" (Hito 2 de Destaques de Precio) con el rollout confirmado en MLA y MLM, continuar (no reescribir) el RFC ya existente, generar/actualizar specs técnicas, crear un proyecto de agente para el seguimiento del RFC con su tarea puente, y cerrar sesión siguiendo AGENTS OS.

## Contexto cargado

- Bootstrap AGENTS OS completo: constitución, perfil de usuario, memoria interna (`agents-os-operating-continuity.md`).
- Proyecto canónico `[[Bajo y Muy Bajo Precio]]` en `10-projects/Destaques de Precio/`.
- RFC legacy `rfc.md` y 4 specs técnicas/funcionales legacy en `sb-main/01_Projects/previous-price-motors/`.
- `CLAUDE.md` y reglas `.claude/rules/` de `sb-main`, que documentan la política vigente de RFC/specs externos (Google Doc/Spellbook), en conflicto con el estado real (RFC/specs locales legacy).

## Trabajo realizado

- Se identificó un conflicto de política: `sb-main` prohíbe RFC/specs locales (deben vivir en Google Doc/Spellbook), pero el proyecto activo depende de un RFC y specs técnicas locales legacy. Se preguntó al usuario antes de proceder; decidió mantener el archivo legacy como excepción.
- Se actualizó `rfc.md`: rollout de Hito 2 (vía Sugeridor 2.0) confirmado en MLA y MLM (antes MLM era "candidato por madurez, requiere confirmación"). Se actualizaron: tabla de alcance por señal, tabla de madurez de Sugeridor por site, rollout propuesto, config JSON de sites, y se removió el pendiente de definición sobre MLM.
- Se actualizaron las specs técnicas de Search y VIP para acotar explícitamente su alcance a MLA/MLM (flujo Sugeridor, dos tiers) y dejar fuera a MLB (flujo FIPE separado, documentado solo en el RFC). Se simplificaron tablas de labels que mezclaban MLB/MLA.
- Se actualizó el proyecto Obsidian `Bajo y Muy Bajo Precio.md`: estado actual, bitácora y link al nuevo proyecto de agente.
- Se creó `[[RFC Destaques de Precio - Hito 2]]` como proyecto de agente (`owner: agent`, `parent: [[Bajo y Muy Bajo Precio]]`) en `10-projects/Destaques de Precio/agentes/`, con checklist de tareas, bitácora y decisiones. Se sembró la tarea puente humana en el proyecto padre.

## Artifacts creados o modificados

- `sb-main/01_Projects/previous-price-motors/rfc.md` (modificado)
- `sb-main/01_Projects/previous-price-motors/Destaques de Precio — Polycard Search — Spec Técnica Propuesta.md` (modificado)
- `sb-main/01_Projects/previous-price-motors/Destaques de Precio — VIP — Spec Técnica Propuesta.md` (modificado)
- `10-projects/Destaques de Precio/Bajo y Muy Bajo Precio.md` (modificado)
- `10-projects/Destaques de Precio/agentes/RFC Destaques de Precio - Hito 2.md` (creado)

## Memoria propuesta o creada

- Learning: preguntar al usuario antes de proceder cuando un artefacto existente choca con una política de repo vigente, en vez de asumir una resolución silenciosa.

## Decisiones

- El RFC y las specs técnicas se mantienen en el archivo legacy local de `sb-main` como excepción a la política vigente (RFC/specs externos), por decisión explícita del usuario — no se migró a Google Doc/Spellbook en esta sesión.
- Las specs funcionales de Search/VIP no se tocaron: quedan como registro histórico del refinamiento 2026-06-23; el estado vigente vive en el RFC y las specs técnicas.

## Pendiente

- Puntos abiertos del pivot FIPE en MLB (fuente técnica del precio FIPE, rango real de elegibilidad, lista marca/modelo/año de exclusión, wording, trigger de reproceso) — sin resolver, listados en el RFC y en el proyecto de agente.
- Evaluar si migrar RFC/specs a Google Doc + Spellbook para cumplir la política vigente de `sb-main`.
