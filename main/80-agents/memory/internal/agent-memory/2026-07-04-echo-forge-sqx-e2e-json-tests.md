---
type: agent_memory
scope: internal
created: 2026-07-04
updated: 2026-07-04
tags:
  - kind/agent_memory
  - tech/go
  - app/echo-forge
  - topic/testing
  - topic/temporal
---

# Continuidad Operativa: Pruebas E2E de SQX Basadas en JSON

## Qué se hizo
- Creamos un conjunto de pruebas E2E en `sqx/workflows/sqx_e2e_json_test.go` para verificar la orquestación de `GenericSQXWorkflow`.
- Creamos 6 archivos de configuración JSON en `input/examples/` (only_builder, only_retester, only_optimizer, builder_retester, builder_retest_optimizer, builder_export_rank_subflow).
- Todos los tests se ejecutan en 0.18s usandomocks de actividades del SDK de Temporal (`testsuite.TestWorkflowEnvironment`).

## Aprendizaje Crítico ( known error resuelto para mockear )
- Al mockear `begin_workflow_span` y `begin_group_span`, el workflow espera que la telemetría devuelta tenga un `SpanID` no nulo.
- Si el mock retorna simplemente `req.Telemetry` (que tiene `SpanID == nil`), la ejecución del workflow paniquea inmediatamente con `runtime error: invalid memory address or nil pointer dereference` al intentar des-referenciar `*tctx.Telemetry.SpanID` en `generic_workflow.go:63`.
- **Solución**: Los mocks deben instanciar y retornar explícitamente un `trace.SpanID` y `trace.TraceID` válidos (no vacíos) dentro del objeto `telemetry.Context`.
