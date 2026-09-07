---
type: change_log
schema_version: 1
scope: session
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application:
entities:
  - "[[RIO]]"
related:
  - "[[scope-inventory]]"
  - "[[2026-08-25-rio-scope-grid-restructure-lives-outside-the-generator]]"
aliases: []
confidence: verified
source_session: "copilotcli:/5b927834-436d-4b97-b477-a57d55119950"
source_feedbacks: []
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-03-rio-scope-grid-v3-reconciliation

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `~/fuentes/rio-inspector/scope_inventory.py`, `rio-scope-policy.json` y `rio-scopes.json`
  - `30-resources/grids/rio-scope-inventory.html`, `30-resources/grids/00-index.md` y [[scope-inventory]]
  - [[Estandarización de Scopes RIO]] y [[2026-08-25-rio-scope-grid-restructure-lives-outside-the-generator]]
  - Grid doc `01KZXKPH3YAGGX89P04GTY7B7E`, versión 3

## Motivo

- El Grid v2 contenía una propuesta física anterior que contradecía SIG-599: cantidad mínima fija, target por aplicación, naming materializado, routing, filtros y piloto de migración. Además, la capa narrativa vivía fuera del generador y se perdía al recolectar de nuevo.

## Fuentes usadas

- [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599), estado canónico de [[Estandarización de Scopes RIO]] y auditoría read-only con Fury CLI 5.21.0 sobre las 10 aplicaciones RIO.

## Resolución aplicada

- Se recolectó un corte Fury del 2026-09-03: 91 scopes en 9 aplicaciones con runtime y [[rio-sdk-events]] como librería sin scopes. El reporte distingue evidencia operativa, ausencia de evidencia activa y casos no concluyentes sin convertirlos en medición de tráfico.
- La propuesta del grid quedó limitada al contrato funcional: catálogo acotado `production|staging|alpha|beta|gamma`, adopción según necesidad, frontend `<environment>`, backend `<environment>-api|consumer` según función y continuidad del ambiente.
- Se eliminó el target físico por aplicación y la copia narrativa manual; la v3 completa se genera desde `scope_inventory.py`.
- Tras feedback directo se eliminó la instrucción no respaldada “Cada equipo debe confirmar…”, se retiró toda rotulación pública de versión y se reemplazó el enlace de SIG-599 por `https://spellbook.adminml.com/projects/SIG/specs/SIG-599`.
- Tras una segunda corrección, el naming backend quedó en `<environment>-<rol>-<segment>` y el generador rechaza los formatos incompletos `<environment>-api` / `<environment>-consumer`.
- SIG-599 se actualizó en Spellbook para usar la misma nomenclatura en definición, ejemplos, requisitos, criterios de aceptación e impacto cross-app; `api` y `consumer` son ejemplos de rol, no los únicos tipos backend.
- Las cuatro apariciones del patrón se codificaron como `<code>&lt;environment&gt;-&lt;rol&gt;-&lt;segment&gt;</code>` porque el renderer de Spellbook eliminaba los placeholders crudos como si fueran tags HTML.

## Validación

- Generator compile y collect PASS con `collection_errors=[]`, 87 runtimes activos reconciliados con status y un único consumer pausado sin runtime resoluble conservado como hallazgo.
- Gate contractual PASS: 91 scopes embebidos, 10 cards, sin `target_model`, sin propuestas por aplicación y sin términos técnicos anteriores.
- Render en navegador PASS: 4 secciones, 5 KPIs, 10 cards, 91 detalles, consola limpia, sin `undefined`/`null` ni overflow horizontal.
- Corrección publicada sobre el mismo documento con control optimista e idempotencia; el JSON embebido remoto es idéntico al artefacto corregido y no contiene la instrucción, la rotulación de versión ni el enlace anterior.
- Naming backend verificado en navegador y en el HTML remoto: `<environment>-<rol>-<segment>`, sin el formato anterior.
- SIG-599 reabierto por UUID tras la edición: estado `review`, contenido remoto idéntico al preparado, cuatro referencias al patrón canónico y cero restos del contrato limitado a `api`/`consumer`.
- Verificación post-fix: cuatro patrones escapados, cero apariciones crudas de `<environment>-<rol>-<segment>` y contenido remoto idéntico al preparado.
- Lint dirigido de las siete notas tocadas PASS, sin errores ni warnings. El reindexado global con `graphify-obsidian update` quedó bloqueado por 25 errores y 6 warnings preexistentes en notas ajenas a este cambio; no se modificó esa deuda fuera de alcance.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Usar rollback de Grid a la versión 2 sólo si el equipo rechaza la v3; para el código, restaurar la policy y el renderer anteriores junto con la copia narrativa, manteniendo el historial remoto.
