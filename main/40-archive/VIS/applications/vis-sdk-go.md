---
type: application
status: active
area: "[[Meli]]"
lang: Go
github: https://github.com/melisource/fury_vis-sdk-go
path: ~/fuentes/vis-sdk-go
aliases:
  - vis-sdk-go
  - fury_vis-sdk-go
  - vis-sdk-go/v2
  - items-batch-search sdk
tags:
  - area/meli
  - kind/application
created: 2026-07-28
updated: 2026-07-28
---

# vis-sdk-go

%% Naming: vis-sdk-go es el link canónico de la aplicación/SDK; aliases incluye repo y el módulo v2. %%

> [!info]+ vis-sdk-go
> **Lenguaje:** Go · **Área:** [[Meli]]
> **GitHub:** [melisource/fury_vis-sdk-go](https://github.com/melisource/fury_vis-sdk-go) · **Path local:** `~/fuentes/vis-sdk-go`
> **Módulo:** `github.com/melisource/fury_vis-sdk-go/v2`

## 📝 Descripción

- SDK Go de VIS que envuelve los servicios de item-core (`item-core.melisystems.com` en prod, `item-core.melioffice.com` fuera de prod). Consumido por [[vis-items-loader-tagging]] y otras apps VIS.
- El package `pkg/items` expone el cliente de **items-batch-search** (`BatchSearchClient`), que es la capability elegida para reemplazar BigQuery en el proceso masivo de Destaque de Precio (ver [[Fase 2 — Proceso Masivo por Site vía items_batch_search — Loader Tagging]]).

## 🔧 Datos útiles

- **Repo:** `melisource/fury_vis-sdk-go`
- **Path local:** `~/fuentes/vis-sdk-go`
- **Módulo:** `github.com/melisource/fury_vis-sdk-go/v2` (loader-tagging usa `v2.15.0`)
- **Stack / notas:** Go. Package clave `pkg/items`.

## 🔎 items-batch-search — API relevante (`pkg/items/items_batch_search.go`)

`BatchSearchClient` con métodos por `siteID` en el path (endpoints nuevos, reemplazan a los deprecados):

| Método | Endpoint | Uso |
|---|---|---|
| `ItemsBatchSearchQueryWithSiteID` | `items-batch-search/{site}/ds/query_search` | Búsqueda paginada por `From`/`Size`. **Tope duro ~9000** (el helper iterativo aborta si `total > 9000`). No sirve para barrer una góndola completa. |
| `ItemsBatchSearchCountWithSiteID` | `items-batch-search/{site}/ds/count_search` | Devuelve `total`. Útil para observabilidad/progreso, no para particionar más allá de 9000. |
| `ItemsBatchSearchScrollWithSiteID` | `items-batch-search/{site}/ds/scroll_search` | **Cursor** vía `context_id`. Cada respuesta trae items + `context_id`; se reenvía para la página siguiente; `context_id == nil` ⇒ fin. **Único mecanismo válido para barridos > 9000.** |

- Request body: `items.SearchJSON` (`Equals`, `NotEquals`, `Match`, `AnyEquals`, `Range`, `Nested`, `Exists`, `Sort`, `Fields`, `From`, `Size`, `ContextID`). Respuesta: `items.Document` (`documents[]`, `total`) / `items.DocumentScroll` (agrega `context_id`).
- `Fields: ["id"]` proyecta solo el ID → payload mínimo para enumerar.
- Helpers iterativos del SDK (`BatchSearchQueryIterativeWithSiteID`, `BatchSearchScrollIterativeWithSiteID`) **no** sirven para el masivo: el de query aborta > 9000 y el de scroll acumula todo en memoria con deadline de 10s.
- En [[vis-items-loader-tagging]] el adaptador `services.ItemService` expone `ItemsBatchSearchScroll` / `ItemsBatchSearchCount` (sin sufijo `WithSiteID`) sobre este cliente; los middlewares `SearchBatchHighlights`, `SearchItemsWithPreviousPrice` y `SearchItemsFinanceablesByMC` ya lo usan con scroll por site.

## 🤖 Contexto para agentes

- **Rol de la aplicación:** SDK/librería, no servicio desplegable. Se consume como dependencia Go.
- **Cómo se relaciona con el trabajo activo:** provee `items-batch-search` (scroll por site) que reemplaza a BigQuery en el masivo de Destaque de Precio.
- **Instrucciones locales:** verificar `AGENTS.md`/`CLAUDE.md` del repo antes de editar.
- **Comandos seguros de validación:** `go build ./...`, `go test ./pkg/items/...` dentro de `~/fuentes/vis-sdk-go`.
- **Dependencias o aplicaciones relacionadas:** [[vis-items-loader-tagging]].
- **Fuentes canónicas a consultar:** `pkg/items/items_batch_search.go`, `pkg/items/domain.go` (`SearchJSON`, `Document`, `DocumentScroll`).

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes vis-sdk-go
short mode
hide task count
```

## 🔗 Links

- [Repo GitHub](https://github.com/melisource/fury_vis-sdk-go)
- [[vis-items-loader-tagging]]
- [[Fase 2 — Proceso Masivo por Site vía items_batch_search — Loader Tagging]]
