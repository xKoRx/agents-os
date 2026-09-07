---
type: application
schema_version: 1
status: active
slug: ads-signals-catalog
area: "[[Meli]]"
lang: Go
github: https://github.com/melisource/fury_ads-signals-catalog
path: ~/fuentes/ads-signals-catalog
aliases:
  - ads signals catalog
  - signals catalog
  - catálogo de señales
tags:
  - kind/application
  - area/meli
  - app/ads-signals-catalog
created: 2026-08-11
updated: 2026-08-11
last_verified: 2026-08-11
confidence: high
---

# ads-signals-catalog

> [!info]+ ads-signals-catalog
> **Rol:** Catálogo centralizado (fuente de verdad) de las señales de Advertising — declara, descubre y gestiona señales, schemas, SLOs y destinations · **Área:** [[Meli]] · **Plataforma:** [[RIO]]
> **Repo:** [remote](https://github.com/melisource/fury_ads-signals-catalog) · **Local:** `~/fuentes/ads-signals-catalog` · **Lang:** Go

## 🎯 Responsabilidad (estable)
- Fuente única de verdad de los **metadatos de señales** del BU de Advertising: declaración, descubrimiento y gestión de señales a nivel organización.
- Persiste y sirve, por señal: definición, **schemas** de validación, **SLOs** (objetivos de servicio) y **destinations** (destinos de transporte).
- Servicio REST puro de CRUD sobre MySQL. **No publica a colas** ni provisiona infraestructura: es un registro de contratos, no un ejecutor.
- Límite de dominio: gobierna el *qué* (metadatos y contrato de la señal), no el *cómo* (transporte/infra, que resuelven [[rio-playmaker]] + control planes).

## 🔌 Contratos e interacciones (semi-estable)
- **Expone:** REST bajo `/catalog/signals` (lista paginada con filtros, get por nombre, create, update, delete) y sub-recursos por señal: `/catalog/signals/{id}/schemas`, `/catalog/signals/{id}/slos`, `/catalog/signals/{id}/destinations`.
- **Consume / produce:** MySQL 8 como store (migraciones en `migrations/mysql/`). Autenticación vía **Tiger Token** (`fury-tiger-go-helper`). No consume ni produce eventos BigQueue.
- **Llama a / lo llaman:** consultado por [[ads-signals-frontend]] (catálogo de entidades del canvas) y relacionado con el bootstrap de señales que [[rio-playmaker]] expone al SDK. El `identifier` de señal (`{dataProduct}.{signalName}`) es la clave jerárquica que enlaza catálogo ↔ pipeline.

## 🧩 Implementación (volátil · last_verified: 2026-08-11)
> Detalle que puede cambiar sin cambiar la responsabilidad.
- **Stack:** Go 1.25 · Fury Go Core (`fury_go-core` v1/v2, `fury_go-platform`) · MySQL 8 (`go-sql-driver/mysql`) · Swagger/OpenAPI 3.0.1. Versión `1.4.0`.
- **Estructura:** `internal/signals`, `internal/destinations`, `internal/schemas`, `internal/slos`, `internal/auth`, `internal/infra`. Entrypoint `cmd/api`.
- **Patrón notable:** capas internas por recurso (signals/destinations/schemas/slos) con auth Tiger Token transversal; tests con `go-sqlmock`.

## 🔗 Relaciones
- consultado por [[ads-signals-frontend]]
- relacionado con [[rio-playmaker]]
- documentado en [[signals-context-flow]]

## 📌 Provenance
- Repo: `melisource/fury_ads-signals-catalog` · Local: `~/fuentes/ads-signals-catalog`
- Fuentes leídas: `README.md`, `go.mod`, estructura `internal/` y `cmd/api/`, `migrations/mysql/`
- `last_verified: 2026-08-11` · `confidence: high`

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes ads-signals-catalog
short mode
hide task count
```
