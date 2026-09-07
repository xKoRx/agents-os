---
type: application
status: active
area: "[[Meli]]"
lang: Go
github: https://github.com/melisource/fury_vis-credits-consumer
path: ~/fuentes/vis-credits-consumer
slug: vis-credits-consumer
aliases:
  - vis-credits-consumer
  - fury_vis-credits-consumer
  - VIS Credits Consumer
  - credits consumer
tags:
  - area/meli
  - kind/application
  - app/vis-credits-consumer
created: 2026-07-17
updated: 2026-07-17
---

# vis-credits-consumer

> [!info]+ vis-credits-consumer
> **Lenguaje:** Go · **Área:** [[Meli]]
> **GitHub:** [melisource/fury_vis-credits-consumer](https://github.com/melisource/fury_vis-credits-consumer) · **Path local:** `~/fuentes/vis-credits-consumer`

## 📝 Descripción

- Consumer de VIS Credits que consulta Segments Wrapper para determinar la financiabilidad de un ítem y actualiza sus sale terms en Item API.
- Para `MLB-CARS_AND_VANS`, además persiste `IS_FINANCEABLE_VEHICLE_RISK_PROFILE`, usando el valor correspondiente a si los jugadores financieros incluyen Mercado Crédito.

## 🔧 Datos útiles

- **Repo:** `melisource/fury_vis-credits-consumer`
- **Path local:** `~/fuentes/vis-credits-consumer`
- **Stack / notas:** Go. `financeable-by.sale-term=true` habilita `FINANCEABLE_BY`.
- **Endpoint de actualización:** `POST /vis-credits-consumer/item-financeable`.
- **Endpoint de filtro:** `POST /vis-credits-consumer/item-filter`; consulta Segments Wrapper y publica solo los ítems que requieren actualización.
- **Parámetro de prueba:** `?version=alpha` hace que el cliente de Segments use la versión alpha; en scope test también se agrega automáticamente.

## 🤖 Contexto para agentes

- **Rol de la aplicación:** fuente de verdad para marcar la financiabilidad del ítem y mantener el sale term de riesgo de vehículo.
- **Cómo se relaciona con el trabajo activo:** [[vis-items-loader-tagging]] publica al flujo de Credits los ítems B2C que están verificados, tienen `accepts_secured_loans`, ya poseen `VEHICLE_RISK_PROFILE_IDENTIFIER` y aún no tienen `IS_FINANCEABLE_VEHICLE_RISK_PROFILE`.
- **Flujo relevante:** `vis-items-loader-tagging` → topic `BIGQUEUE_TOPIC_VIS_PRV_EVENTS_TOPIC_NAME` → consumer de Credits → Segments Wrapper → Item API. El `item-financeable` handler escribe `IS_FINANCEABLE`, `FINANCEABLE_BY` y, para `MLB-CARS_AND_VANS`, `IS_FINANCEABLE_VEHICLE_RISK_PROFILE`.
- **Dependencias o aplicaciones relacionadas:** [[vis-items-loader-tagging]], Segments Wrapper, Item API, Catalog Domains y BigQueue.
- **Fuentes canónicas a consultar:** `controllers/item.go`, `services/item.go`, `clients/segments.go`, `config/application.properties`.

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes vis-credits-consumer
short mode
hide task count
```

## 🔗 Links

- [[vis-items-loader-tagging]]
