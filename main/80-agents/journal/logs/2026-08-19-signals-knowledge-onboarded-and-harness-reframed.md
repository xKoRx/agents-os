---
type: change_log
schema_version: 1
scope: session
created: "2026-08-25"
updated: "2026-08-25"
area: "[[Meli]]"
project: "[[Signals Knowledge Harness]]"
application:
entities:
  - "[[signals-knowledge]]"
  - "[[Signals Knowledge Harness]]"
  - "[[Onboarding Signals]]"
related:
  - "[[RIO]]"
  - "[[30-resources/00-RESOURCE-WIKI|Resource Wiki]]"
aliases: []
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

# 2026-08-19-signals-knowledge-onboarded-and-harness-reframed

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `30-resources/knowledges/00-index.md` — creado (dominio nuevo, `type: index`).
  - `30-resources/knowledges/log.md` — creado.
  - `30-resources/knowledges/signals-knowledge.md` — creado (`type: resource`).
  - `30-resources/knowledges/sources/signals-knowledge-repo.md` — creado (`type: source`).
  - `10-projects/Meli/Signals Knowledge Harness/Signals Knowledge Harness.md` — creado y reencuadrado (root project).
  - `10-projects/Meli/Onboarding Signals/Onboarding Signals.md` — actualizado (bitácora + links).

## Motivo

El equipo pasó el repo `signals-knowledge` (bundle OKF de conocimiento Signals/RIO, autor Carlos Montecinos). Hacía falta modelarlo como external-resource del vault, separar la iniciativa de cambio (harness/contribución) del proyecto de comprensión (onboarding), y — a pedido del usuario — reencuadrar esa iniciativa: de "proponer un harness" a "llevar el repo a ser el SecondBrain agéntico de la iniciativa Signals", con contenido + harness + tooling como un solo delivery y el repo como futura fuente única de verdad para el `rio-atlas`.

## Fuentes usadas

- Repo real `~/fuentes/signals-knowledge` (README, index.md, `.fury`, árbol completo, git log/remote).
- Contrato de esquema (`schema-contract.md`) y `materialize_schema_note.py` para los 4 tipos nuevos.
- Perfil de directorio de Carlos Montecinos (`cmontecinos`) vía `meli-directory-mcp`.
- `30-resources/rio-atlas/00-index.md` y notas de `applications/` para calcular el delta de contenido propio vs. repo.

## Resolución aplicada

- Modelado por decisión explícita del usuario: `resource` (no `application` ni tipo nuevo `external-resource`) en un dominio nuevo `30-resources/knowledges/`, con `source` de provenance (`repo`+`path` relativo a `~/fuentes`, invariante 12).
- Proyecto `Signals Knowledge Harness` creado como iniciativa raíz separada del onboarding (regla de no mezclar comprensión↔cambio), luego reencuadrado a pedido del usuario: visión de SecondBrain agéntico, alcance de tres frentes (contenido/harness/tooling) fusionado en el mismo proyecto, y decisión de fuente única de verdad (el repo pasa a ser la canónica; el `rio-atlas` gradúa contenido hacia allá vía PR).
- Registrado el stakeholder real (Carlos Montecinos, autor del bundle, relación ya establecida) y el estado de la conversación con él.

## Validación

- `lint.py --strict` en verde (ERROR=0 WARN=0) sobre las 5 notas nuevas/editadas de Sistema 2.
- Grafo de links del repo externo auditado (98 links, 0 rotos, 0 huérfanos) como evidencia de calidad antes de decidir el modelo de contribución.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad más allá del nombre público de Carlos (ya conocido por el usuario), sin paths de máquina fuera de `~/fuentes` (permitido por invariante 11 como referencia de workspace), sin secretos.

## Rollback

- Los 4 archivos nuevos en `30-resources/knowledges/` y el proyecto nuevo son reversibles por borrado directo (sin dependientes aún). Las ediciones a `Onboarding Signals.md` son aditivas (bitácora + links); revertibles desde el historial del vault.
