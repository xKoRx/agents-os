---
type: application
status: active
area: "[[Meli]]"
lang: Go
github: https://github.com/melisource/fury_search-api-go
path: ~/fuentes/search-api-go
aliases:
  - search-api-go
  - fury_search-api-go
tags:
  - area/meli
  - kind/application
created: 2026-08-04
updated: 2026-08-04
---

# search-api-go

> [!info]+ search-api-go
> **Lenguaje:** Go · **Área:** [[Meli]]
> **GitHub:** [melisource/fury_search-api-go](https://github.com/melisource/fury_search-api-go) · **Path local:** `~/fuentes/search-api-go`

## 📝 Descripción

- Servicio de Search que decora resultados y mantiene los modelos cacheados de items/productos, incluyendo el flujo de sincronización desde Items API.

## 🔧 Datos útiles

- **Repo:** `melisource/fury_search-api-go`
- **Path local:** `~/fuentes/search-api-go`
- **Stack / notas:** Go · Gin · task-based DAG · BigCache/Redis/KVS · BigQueue

## 🤖 Contexto para agentes

- **Rol de la aplicación:** Propagar atributos de items hacia el modelo Search API y las capas de caché/respuesta.
- **Cómo se relaciona con el trabajo activo:** Implementación de `PRICE_HIGHLIGHT_TIER` para [[Destaque de Precio Search — Search API Go]], bajo [[Cierre VIS]].
- **Instrucciones locales:** `AGENTS.md` y `.agents/`
- **Comandos seguros de validación:** `go test ./...`; `golangci-lint run -c .golangci.yml`
- **Dependencias o aplicaciones relacionadas:** [[search-middleware]], [[java-polycard-sdk]], [[vis-items-loader-tagging]]
- **Fuentes canónicas a consultar:** [[Destaque de Precio Search — Search API Go]]

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes search-api-go
short mode
hide task count
```

## 🔗 Links

- [Repo GitHub](https://github.com/melisource/fury_search-api-go)
- [[Destaque de Precio Search — Search API Go]]
