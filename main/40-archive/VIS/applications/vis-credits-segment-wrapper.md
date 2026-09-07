---
type: application
status: active
area: "[[Meli]]"
lang: Go
github: https://github.com/melisource/fury_vis-credits-segment-wrapper
path: ~/fuentes/vis-credits-segment-wrapper
slug: vis-credits-segment-wrapper
aliases:
  - vis-credits-segment-wrapper
  - fury_vis-credits-segment-wrapper
  - VIS Credits Segment Wrapper
  - Credits Segments
tags:
  - area/meli
  - kind/application
  - app/vis-credits-segment-wrapper
created: 2026-07-17
updated: 2026-07-17
---

# vis-credits-segment-wrapper

> [!info]+ vis-credits-segment-wrapper
> **Lenguaje:** Go · **Área:** [[Meli]]
> **GitHub:** [melisource/fury_vis-credits-segment-wrapper](https://github.com/melisource/fury_vis-credits-segment-wrapper) · **Path local:** `~/fuentes/vis-credits-segment-wrapper`

## 📝 Descripción

- API que evalúa la disponibilidad de Credits para un ítem y determina los segmentos/bancos compatibles según configuración, sale terms, atributos, usuario y servicios externos.
- El endpoint relevante para el consumer es `GET /vis-credits-segments/available/{item_id}`.

## 🔧 Datos útiles

- **Repo:** `melisource/fury_vis-credits-segment-wrapper`
- **Path local:** `~/fuentes/vis-credits-segment-wrapper`
- **Configuración de segmentos:** `assets/segments.yaml`
- **Scope de ejecución:** `scope.type`; el flujo consumer registra `/available` cuando es `consumer` o `all`.
- **Cliente de riesgo vehicular:** `securedloans.DefaultVehicleRiskProfileClient` en producción y `BetaDefaultVehicleRiskProfileClient` cuando el ítem es de test.

## 🤖 Contexto para agentes

- **Rol de la aplicación:** fuente de decisión para `is_financeable` e integración de Credits a partir de filtros configurados.
- **Cómo se relaciona con el trabajo activo:** [[vis-credits-consumer]] llama `/vis-credits-segments/available/{item_id}` para decidir los sale terms de financiabilidad; [[vis-items-loader-tagging]] alimenta el flujo que dispara ese consumer.
- **Regla MLB relevante:** el segmento `MCFull` exige `category_id=MLB1744`. También tiene un filtro `IS_FINANCEABLE_VEHICLE_RISK_PROFILE=242085` (“Sí”), pero ese filtro está limitado a `card` y `fallback`; no se evalúa en `/available`.
- **Filtro adicional:** el banco `mlb-mc` exige `user_type=car_dealer`, tag interno `accepts_secured_loans`, año del vehículo entre los límites configurados y, para `/available`, que `is_vehicle_risk_profile_financeable=true`.
- **Implicación operativa:** para `/available`, un `false` con `players=[]` apunta a que ningún banco hizo match. En `mlb-mc`, las causas críticas son `user_type=car_dealer`, tag interno `accepts_secured_loans`, `VEHICLE_YEAR` dentro del rango y que el cliente de riesgo vehicular responda `Scoring.IsFinanceable=true`; si falta `VEHICLE_RISK_PROFILE_IDENTIFIER`, el filtro retorna `false` sin llamar al servicio.
- **Fuentes canónicas a consultar:** `assets/segments.yaml`, `internal/core/usecase/credit_available_usecase.go`, `filter/evals.go`, `clients/process/segment.go`, `clients/vehicle_risk_profile.go`, `cmd/api/engine/ignition.go`.

## ✅ Tareas relacionadas

```tasks
sort by priority
not done
description includes vis-credits-segment-wrapper
short mode
hide task count
```

## 🔗 Links

- [[vis-credits-consumer]]
- [[vis-items-loader-tagging]]
