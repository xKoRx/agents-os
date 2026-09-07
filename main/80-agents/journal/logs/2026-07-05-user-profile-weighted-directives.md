---
type: change_log
scope: user
created: 2026-07-05
updated: 2026-07-05
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agent-constitution]]"
aliases: []
confidence: verified
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/user
  - project/agents-os
---

# 2026-07-05 — perfil de usuario: rediseño a directivas priorizadas

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `80-agents/memory/public/user-preference/rjara-agent-profile.md`

## Motivo

Petición del usuario: hacer la ficha más práctica y óptima de parsear por
agentes. La versión previa eran bullets en prosa sin jerarquía de obligatoriedad
ni contexto de identidad.

## Fuentes usadas

- Ficha previa (v2026-06-30).
- Constitución § "Memorias compactas y autoentendibles" (densidad, una directiva
  por línea) y § economía de tokens.
- 3 decisiones de diseño confirmadas por el usuario (ver abajo).

## Resolución aplicada

- **Formato → directivas priorizadas.** Cada preferencia es una línea imperativa
  etiquetada por peso: `[DURA]` (obligatoria), `[FUERTE]` (preferir salvo razón),
  `[BLANDA]` (gusto). Bloque-guía al inicio explica la convención.
- **Nueva sección "Identidad y contexto"** con nombre, organización e idioma
  confirmados; equipo, rol, dominio y stack quedan como placeholders explícitos
  `<completar>` — no se inventaron (regla de no completar vacíos por inferencia).
- **Tensión de tono resuelta:** pirata pesado/cascarrabias = default `[DURA]`;
  cálido/directo/colaborativo = fondo `[FUERTE]`. Antes ambas líneas pesaban
  igual y podían leerse como contradictorias.
- Todo el contenido semántico previo (interacción, trabajo, memoria) se conservó,
  comprimido a una línea por directiva. Sin pérdida de reglas.
- `updated` → 2026-07-05.

## Validación

- Contenido previo mapeado 1:1 a directivas etiquetadas (ninguna regla perdida).
- Frontmatter (`type`, `load_policy: always`, tags always-load, `index_priority`)
  intacto.
- Pendiente del usuario: dictar los 4 campos `<completar>` de Identidad para
  cerrar los placeholders.
