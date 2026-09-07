---
type: change_log
scope: session
created: 2026-06-27
updated: 2026-06-27
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[agents-os]]"
  - "[[Meli]]"
  - "[[Áreas]]"
related:
  - "[[agent-constitution]]"
aliases:
  - canonical linking policy update
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - area/personal
  - change/updated
  - kind/changelog
  - project/agents-os
  - project/agentsos
  - scope/session
---
# Canonical Linking Policy Updated

## Cambio

- Se definió la regla canónica de identidad para Second Brain + AGENTS OS/Graphify:
  link canónico para Obsidian, `aliases` para variantes humanas y `slug`/tags/paths
  para automatización.
- Se actualizó documentación operativa, contratos compartidos, skills, adaptadores,
  templates y notas de área vivas.
- Las notas de área pasaron de `area: <slug>` a `slug: <slug>` para reservar
  `area:` como routing link canónico en proyectos, recursos y memorias.

## Fuente / Evidencia

- Solicitud del usuario el 2026-06-27: documentar y aplicar la política a los dos
  sistemas, y alinear el repo completo.
- Búsqueda previa confirmó que no había links vivos `[[meli]]` o `[[areas]]`;
  el riesgo principal era falta de contrato y metadata ambigua.

## Validación

- `rg --pcre2` sobre fuentes vivas ya no encuentra `area: <slug>` operativo en
  notas de área; los `area:` restantes son links canónicos como `area: "[[Meli]]"`.
- `rg` sobre variantes `[[meli]]`, `[[areas]]` y rutas `90-graphify` solo devolvió
  ejemplos de la regla o material generado/excluido.
- Las 11 notas vivas bajo `20-areas/` tienen `slug:` y aliases mínimos.
- `graphify-obsidian update` reconstruyó `95-graphify/obsidian/` con 746 nodes,
  658 edges y 88 communities.
- `graphify-obsidian explain "Meli"` y `graphify-obsidian explain "meli"`
  resolvieron ambos a `20-areas/Meli.md`.
- `graphify-obsidian explain "Áreas"` y `graphify-obsidian explain "areas"`
  resolvieron ambos a `20-areas/Áreas.md`.
- Búsqueda en `95-graphify/obsidian/graph.json` no encontró paths bajo
  `80-agents/journal/`, por lo que raw sessions, summaries y logs siguen fuera
  del grafo normal.

## Riesgo / Follow-up

- No se renombraron archivos con acentos o mayúsculas porque el canon humano
  actual ya es estable; renombrarlos tendría más riesgo para Obsidian que beneficio
  de retrieval.
- No queda follow-up técnico inmediato; mantener la regla en futuras notas y
  ejecutar hygiene si aparece una variante nueva.
