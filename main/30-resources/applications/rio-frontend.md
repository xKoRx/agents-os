---
type: application
schema_version: 1
status: deprecated
slug: rio-frontend
area: "[[Meli]]"
lang: TypeScript
github: https://github.com/melisource/fury_rio-frontend
path: ~/fuentes/rio-frontend
aliases:
  - rio frontend
  - RIO Frontend legacy
tags:
  - kind/application
  - area/meli
  - app/rio-frontend
  - lifecycle/deprecated
created: 2026-08-11
updated: 2026-08-11
last_verified: 2026-08-11
confidence: high
---

# rio-frontend

> [!warning] En deprecación
> **`rio-frontend` está en proceso de deprecado.** Su reemplazo es [[ads-signals-frontend]] (RIO Frontend v3, FSD). Documentar aquí solo para entender el legacy y la migración; el desarrollo nuevo va en ads-signals-frontend.

> [!info]+ rio-frontend
> **Rol:** UI legacy (SPA) de RIO — gestión de data products, definiciones de componente, deployments y service instances · **Área:** [[Meli]] · **Plataforma:** [[RIO]]
> **Repo:** [remote](https://github.com/melisource/fury_rio-frontend) · **Local:** `~/fuentes/rio-frontend` · **Lang:** TypeScript

## 🎯 Responsabilidad (estable)
- SPA de gestión de la plataforma RIO: administra data products, **component definitions**, deployments y service instances con una UI clásica (canvas DrawFlow).
- Cubre el mismo dominio funcional que [[ads-signals-frontend]] pero sobre la generación anterior de UI; **está siendo reemplazada** y no debería recibir features nuevos.
- Límite de dominio: presentación/orquestación de intención; delega provisioning y cómputo a [[rio-playmaker]] + control planes + [[rio-materializer]].

## 🔌 Contratos e interacciones (semi-estable)
- **Expone:** app Nordic/ODIN (SPA) con BFF en `api/` (handlers `v2`). Rutas legacy hacia [[rio-playmaker]]: `POST /v2/data-products/{name}/components/{name}/definitions`, `GET/POST /v2/relations/...` (algunas lecturas van directo a la DB de relaciones).
- **Consume / produce:** proxya al backend RIO; la lógica de relaciones vive en `app/components/v2/component-relation-logic/` (COMPONENT_OUTPUTS, COMPONENT_DATA_DEPENDENCIES, resolución de templates `${X.field}`) — misma deuda que ads-signals-frontend: relaciones y outputs definidos en el cliente.
- **Migración:** la funcionalidad se está trasladando a [[ads-signals-frontend]]; los contratos con Playmaker convergen a las rutas `/pipeline/...` nuevas.

## 🧩 Implementación (volátil · last_verified: 2026-08-11)
> Detalle que puede cambiar sin cambiar la responsabilidad.
- **Stack:** TypeScript/JavaScript · React · Nordic v9 (9.12.0) + ODIN · SCSS + Tailwind · Webpack/Babel · Andes + Radix UI · Jest. Versión `202607.7.0`.
- **Canvas:** DrawFlow (generación anterior; ads-signals-frontend usa React Flow/XYFlow).
- **Patrón notable:** `component-relation-logic/` como fuente estática de compatibilidad y outputs por tipo de componente — el equivalente legacy de `src/technologies/relations.ts` en la UI nueva.

## 🔗 Relaciones
- reemplazado por [[ads-signals-frontend]]
- llama a [[rio-playmaker]]
- documentado en [[signals-context-flow]]

## 📌 Provenance
- Repo: `melisource/fury_rio-frontend` · Local: `~/fuentes/rio-frontend`
- Fuentes leídas: `README.md`, `package.json`, discovery dirigido de `app/components/v2/component-relation-logic/`, `api/handlers/v2/`
- `last_verified: 2026-08-11` · `confidence: high`

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes rio-frontend
short mode
hide task count
```
