---
title: Troubleshooting RIO
layer: L3
audience: [support, engineering, operations, agents]
last_verified: 2026-10-05
confidence: high
sensitivity: internal
---

# Troubleshooting RIO

## Entrar por síntoma

| Síntoma | Runbook |
|---|---|
| Cualquier problema Flink/Flink SQL | [Hub Flink](flink.md) |
| Job Flink queda en `STARTING` | [Starting colgado](flink-starting-stuck.md) |
| Stop no termina o delete queda pendiente | [Stop/delete Flink](flink-stop-delete-stuck.md) |
| Deploy Flink falla, UI queda vacía o faltan logs | [Deploy y logs Flink](flink-deploy-and-logs.md) |
| No sé dónde está el corte | [Triage transversal](triage.md) |
| Deployment pendiente, trabado o fallido | [Deployment](deployment-stuck-or-failed.md) |
| Señal dropped/partial/ausente | [Signals delivery](signals-delivery.md) |
| Topic/acción Kafka no converge | [Kafka](kafka.md) |
| Verificar E2E local CP con Kafka real/memoria y consultar gates históricos | [E2E Kafka candidato](kafka-real-e2e.md#corte-local-de-trabajo--0510) |
| Tabla/MV ClickHouse falla, queda pendiente o diverge del provider | [ClickHouse](clickhouse.md) |
| Start/stop/materialización en timeout | [Materializer](materializer.md) |
| Acción completó pero runtime no converge | [Acciones y runtime](actions-and-runtime.md) |
| UI/API responde 401/403 o no muestra acción | [Autenticación y acceso](authentication-and-access.md) |
| Draft/schema/entity no valida o activa | [Entity contracts](entity-contracts.md) |
| Filtros de logs/monitor/cuota no aparecen | [Observabilidad](observability.md) |
| UI vacía, relación visual incorrecta o dato stale | [Consistencia UI](ui-state-consistency.md) |
| Mantenimiento, capacidad, ramp-up, compatibilidad o capability vigente | [Readiness y capabilities](operational-readiness-and-capability.md) |

Antes de compartir evidencia, lee [recolección segura](safe-evidence.md).

Cuando el síntoma ya identifica endpoint, action o `component_type`, salta a su [feature ID y ancla de código](../09-feature-catalog/README.md) antes de formular una hipótesis.

## Regla de oro

Localiza el último límite confirmado y prueba el siguiente. Un log de entrada confirma recepción; no confirma efecto externo. Un recurso creado confirma efecto; no confirma resultado publicado. Un resultado terminal confirma contrato; no garantiza que la vista/UI ya se refrescó.
