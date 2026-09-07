---
type: application
schema_version: 1
status: active
slug: ads-signals-frontend
area: "[[Meli]]"
lang: TypeScript
github: https://github.com/melisource/fury_ads-signals-frontend
path: ~/fuentes/ads-signals-frontend
aliases:
  - ads signals frontend
  - signals frontend
  - RIO Frontend v3
tags:
  - kind/application
  - area/meli
  - app/ads-signals-frontend
created: 2026-08-11
updated: 2026-08-11
last_verified: 2026-08-11
confidence: high
---

# ads-signals-frontend

> [!info]+ ads-signals-frontend
> **Rol:** UI moderna (RIO Frontend v3) de la plataforma Signals — compositor visual de data products/pipelines y su ciclo de vida · **Área:** [[Meli]] · **Plataforma:** [[RIO]]
> **Repo:** [remote](https://github.com/melisource/fury_ads-signals-frontend) · **Local:** `~/fuentes/ads-signals-frontend` · **Lang:** TypeScript

## 🎯 Responsabilidad (estable)
- Interfaz self-serve del equipo Signals para construir y operar **data products** (pipelines de streaming) sin tocar infraestructura: canvas drag-and-drop de nodos Kafka, Flink, ClickHouse y storage.
- Gestiona el ciclo de vida completo de componentes en la UI: draft → deploy → stop, con detección de conflictos (versión de pipeline / OCC) y gates de aprobación.
- Catálogo de entidades (schemas/contratos de datos) y observabilidad: badges de salud por nodo, estado de despliegue y acciones runtime (Kafka peek, Flink start/stop, ClickHouse query).
- **Reemplaza a [[rio-frontend]]** (el legacy en deprecación). Es la UI destino del ecosistema.
- Límite de dominio: es solo presentación/orquestación de intención; no provisiona infra ni ejecuta cómputo (eso es de [[rio-playmaker]] + control planes + [[rio-materializer]]).

## 🔌 Contratos e interacciones (semi-estable)
- **Expone:** app Nordic (BFF propio en `api/`) que sirve el canvas y proxya al backend. Rutas clave hacia [[rio-playmaker]]: `PATCH /data-products/{name}/environments/{env}/pipeline/components/{name}/config` (properties del componente), `PATCH /data-products/{name}/pipeline/relations` (relaciones entre nodos), `GET /components/{id}/outputs` (outputs del CP tras deploy).
- **Consume / produce:** llama al BFF interno que normaliza snake_case ↔ camelCase antes de Playmaker. Lee outputs de despliegue (`OutputEntry[]`) para resolver referencias entre componentes.
- **Punto caliente (deuda de arquitectura):** hoy el **front arma las relaciones y las properties derivadas** en TypeScript — `COMPATIBILITY_RULES`/`CONNECTION_PRESETS` (`src/technologies/relations.ts`), el `properties_map` de Flink (`src/features/flink-properties-sync/`) y las `destinations[]` de catalog-signal (`src/features/catalog-destinations-sync/`, con debounce de 2 s). Esa lógica **debería vivir en [[rio-playmaker]]** — objetivo central del [[Onboarding Signals]] (context of signals). Ver [[signals-context-flow]].

## 🧩 Implementación (volátil · last_verified: 2026-08-11)
> Detalle que puede cambiar sin cambiar la responsabilidad.
- **Stack:** TypeScript · Nordic v9 (9.12.1) · Kraken KFP v8 · Tailwind CSS v4 · React Flow (XYFlow) para el canvas · Jest (unit). Versión `202608.10.0`.
- **Arquitectura:** Feature-Sliced Design (FSD) — capas `src/entities/`, `src/features/`, `src/widgets/`, `src/technologies/`. Registro único de tecnologías en `src/technologies/registry.ts` (dispatch por tipo de componente: Form + adapter).
- **Patrón notable:** cada tecnología expone un `TechnologyAdapter` con `toApiPayload`/`toFormValues`; validación propia (`ComponentSchema<T>`, sin Zod/Yup). Skills locales del repo: `signals-ui`, `technology-scaffold`, `fsd-scaffold`, `flowise-check`.
- **Dos rutas de persistencia:** ruta A nueva (`PATCH .../pipeline/components/{name}/config`) y ruta B legacy (`POST /components/{id}/definitions`).

## 🔗 Relaciones
- reemplaza a [[rio-frontend]]
- llama a [[rio-playmaker]]
- relacionado con [[ads-signals-catalog]]
- documentado en [[signals-context-flow]]

## 📌 Provenance
- Repo: `melisource/fury_ads-signals-frontend` · Local: `~/fuentes/ads-signals-frontend`
- Fuentes leídas: `README.md`, `package.json`, discovery dirigido de `src/technologies/`, `src/features/flink-properties-sync/`, `src/features/catalog-destinations-sync/`, `api/`
- `last_verified: 2026-08-11` · `confidence: high`

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes ads-signals-frontend
short mode
hide task count
```
