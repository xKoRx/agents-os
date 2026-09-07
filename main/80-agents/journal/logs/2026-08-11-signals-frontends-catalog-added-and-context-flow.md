---
type: change_log
scope: session
created: 2026-08-11
updated: 2026-08-11
area: "[[Meli]]"
project: "[[Onboarding Signals]]"
application:
entities:
  - "[[ads-signals-frontend]]"
  - "[[ads-signals-catalog]]"
  - "[[rio-frontend]]"
  - "[[rio-materializer]]"
  - "[[signals-context-flow]]"
  - "[[RIO]]"
related:
  - "[[30-resources/applications/00-index]]"
  - "[[30-resources/rio-atlas/00-index]]"
  - "[[deploy-component]]"
  - "[[graphify]]"
aliases:
  - signals frontends catalog added
  - context of signals flow documented
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
  - area/meli
  - change/created
  - change/updated
---

# Alta de frontends + catálogo Signals y documentación del context of signals

## Cambio

- **Tipo:** created + updated
- **Archivo(s) creados:**
  - `30-resources/applications/ads-signals-frontend.md` (app, active)
  - `30-resources/applications/ads-signals-catalog.md` (app, active)
  - `30-resources/applications/rio-frontend.md` (app, **deprecated** — enum del vault; "en proceso" va en el callout)
  - `30-resources/rio-atlas/architecture/signals-context-flow.md` (contrato completo params→outputs)
  - `~/fuentes/{rio-frontend,ads-signals-frontend,ads-signals-catalog,rio-inspector}/graphify-out/` (grafos AST)
- **Archivo(s) actualizados:**
  - `30-resources/applications/rio-materializer.md` → status `deprecated` + callout
  - Reindex del grafo del vault (`graphify-obsidian update`): gate GO, 5203 nodos / 6243 edges
  - `30-resources/applications/00-index.md` (16 apps, 3 filas nuevas, 2 deprecating)
  - `30-resources/applications/RIO.md` (capa presentación/catálogo, deprecaciones, grafo 14)
  - `30-resources/rio-atlas/00-index.md` (nueva vista signals-context-flow)
  - `30-resources/rio-atlas/journeys/deploy-component.md` (gap de amplitud cerrado)
  - `~/fuentes/AGENTS.md` (repos nuevos + comando de merge con ads-signals-*)
  - `~/fuentes/graphify-signals.json` (regenerado: 14 grafos, 54030 nodos / 112407 edges; backup `.bak-20260811`)

## Motivo

- El equipo agregó 3 repos nuevos al ecosistema Signals (2 frontends + catálogo Go) que no estaban en el vault.
- `rio-frontend` y `rio-materializer` están en proceso de deprecado (rio-frontend → reemplazado por ads-signals-frontend; materializer → solo le queda el flujo de inicio Signals/Catalog).
- Onboarding: entender y documentar el **context of signals** (contrato de properties params→outputs, hoy armado en el front, objetivo mover a playmaker).

## Fuentes usadas

- Discovery de primera mano en código local (2026-08-11) de los repos en `~/fuentes` (front, playmaker, 4 CPs, sdk-events).
- `README.md`, `package.json`, `go.mod`, estructura `src/`/`internal/` de los repos nuevos.
- Plantilla `30-resources/applications/rio-playmaker.md` para las fichas.

## Resolución aplicada

- 3 fichas de aplicación nuevas con títulos/slug canónicos y alias del remote; 2 apps marcadas `deprecating` con callout de aviso.
- `graphify update` en los 4 repos nuevos → `graphify-out/` por repo; merge de Signals regenerado incluyendo `ads-signals-*` (que **no** matchean el glob `rio-*`).
- Nota `signals-context-flow` que cierra el gap del journey `deploy-component` (mapa de consumo completo de kafka/clickhouse/flink/fury + discrepancias `brokers`/`servers` y credenciales ClickHouse).

## Validación

- Los 4 `graphify-out/graph.json` existen (rio-frontend 5240 nodos, ads-signals-frontend 5847, catalog 1290, inspector 24).
- Merge OK: "Merged 14 graphs -> 54030 nodes, 112407 edges".
- Backup del merge previo en `~/fuentes/graphify-signals.json.bak-20260811`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin credenciales, secretos ni dumps de código.

## Rollback

- Archivar las 3 fichas nuevas + `signals-context-flow`, revertir status de rio-materializer/rio-frontend a `active`, restaurar `graphify-signals.json.bak-20260811`, quitar filas de índices. Conservar este log como auditoría.
