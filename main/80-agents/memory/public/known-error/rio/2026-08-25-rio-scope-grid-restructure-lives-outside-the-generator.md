---
type: known_error
schema_version: 1
scope: project
created: "2026-08-25"
updated: "2026-09-03"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application:
entities:
  - "[[RIO]]"
related:
  - "[[scope-inventory]]"
  - "[[2026-08-25-rio-scope-grid-restructure-summary]]"
aliases:
  - Grid RIO reestructurado se pierde al regenerar
confidence: verified
source_session: 56245ef0-5287-4493-9a9b-9376e9ec31df
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - project/scopes-rio
---

# 2026-08-25-rio-scope-grid-restructure-lives-outside-the-generator

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- El grid `rio-scope-inventory` publicado en Grid (doc `01KZXKPH3YAGGX89P04GTY7B7E`, v2) tiene la estructura narrativa nueva —presentación, Parte 1 estado, Partes 2 y 3 propuesta, Parte 4 impacto, Parte 5 decisiones, anexo—, pero cualquier corrida de `~/fuentes/rio-inspector/scope_inventory.py` regenera el HTML con la estructura vieja y plana.

## Causa

- La reestructuración del 2026-08-25 se hizo sobre el **HTML ya emitido** (cirugía de markup + CSS + un segundo script de render), no sobre el template embebido en `scope_inventory.py` (~122 KB, contiene el HTML como string). El generador nunca se enteró del cambio.

## Impacto

- El próximo agente que refresque datos y regenere el grid **revierte silenciosamente** la estructura narrativa y vuelve a publicar la versión desordenada, sin error visible: el HTML es válido y los datos son correctos, sólo cambia el orden y desaparece la presentación.

## Detección

- Si el HTML regenerado no contiene los anclajes `id="parte1"`, `id="findings"`, `id="apptable"` ni la `nav.tabnav`, está usando el template viejo.

## Mitigación

- **Resuelto 2026-09-03:** la vista narrativa v3 vive en `scope_inventory.py`; `collect` y `render` generan el mismo HTML publicable desde `rio-scopes.json` y el contrato funcional de SIG-599.
- La copia manual `rio-scope-inventory-narrativo.html` se retiró para evitar dos artefactos activos y divergentes.
- El gate del generador rechaza `target_model`, propuestas por aplicación y cualquier catálogo funcional distinto de SIG-599.

## Evidencia

- Fuente publicada: Grid doc `01KZXKPH3YAGGX89P04GTY7B7E` v2, subido con `file_new_version` + `if_version=1`.
- Evidencia histórica: la copia manual `30-resources/grids/rio-scope-inventory-narrativo.html` preservó la v2 hasta que la v3 quedó integrada al generador; luego se retiró para evitar divergencia.
- Nota operativa de la plataforma: `GET /d/<doc_id>/raw` responde 502; el download que sí funciona es `GET /d/<doc_id>?dl=1`.
- Resolución: Grid v3 publicado en el mismo doc el 2026-09-03; historial remoto conserva las versiones 1, 2 y 3.
