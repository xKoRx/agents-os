---
type: known_error
schema_version: 1
scope: application
created: "2026-10-14"
updated: "2026-10-14"
area: "[[Meli]]"
project: "[[RIO E2E local]]"
application: "[[rio-playmaker]]"
entities:
  - "[[RIO E2E local]]"
  - "[[rio-playmaker]]"
related:
  - "[[Descripción PR — rio-playmaker]]"
  - "[[2026-10-14-codex-gpt-6-rio-e2e-local-pr1286]]"
aliases:
  - develop descarta resultados DEPROVISION
  - undeploy por bus no completa en develop
confidence: high
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - area/meli
  - application/rio-playmaker
  - project/rio-e2e-local
---

# RIO Playmaker — develop descarta resultados de DEPROVISION por bus

## Síntoma

- Un undeploy originado por DEPROVISION no alcanza estado completado en el entorno basado en develop; el resultado queda descartado en Playmaker.

## Causa

- DeploymentResultHandlerImpl en develop considera terminal el deployment y descarta el resultado entrante con reason=already_terminal o reason=terminal_component_run.

## Impacto

- Los E2E que dependen de completar undeploy fallan; el cleanup de fixtures que invoca undeploy también queda bloqueado y puede hacer fallar escenarios no relacionados.

## Detección

- Consultar application.log del run y correlacionar el UUID del deployment del test; buscar la línea de descarte del resultado y el campo reason.

## Mitigación

- En el E2E local, no depender de undeploy en cleanup. Si el caso creó un topic físico propio, borrarlo directamente con Kafka Admin; dejar que el teardown del stack desechable elimine las filas de fixtures.
- Etiquetar develop-gap los casos cuyo objetivo sí es probar undeploy/DEPROVISION y excluirlos de localIntegrationTest por defecto. No compensar el comportamiento de develop desde src/local.

## Evidencia

- Diagnóstico del owner para la ejecución E2E previa: descartes con already_terminal y terminal_component_run.
- En la iteración actual, los siete E2E predeterminados pasaron después de desacoplar cleanup y etiquetar los casos de undeploy como develop-gap.
