---
type: agent_memory
schema_version: 1
scope: "project"
created: "2026-10-08"
updated: "2026-10-08"
area: "[[Meli]]"
project: "[[SIG-616 — Autorización de operaciones por equipo]]"
application: "[[rio-playmaker]]"
entities: ["[[SIG-616 — Autorización de operaciones por equipo]]"]
related: ["[[2026-10-08-codex-unknown-sig-616-autorizacion-dashboard-review]]"]
aliases: []
confidence: "high"
memory_state: "active"
continuity_key: "sig-616-operation-authorization-observability"
load_policy: "Al retomar el dashboard ACME o la revisión HTTP de los PRs 763 y 1282 vinculados a SIG-616."
indexable: false
index_priority: "low"
tags: ["kind/agent-memory", "scope/project", "project/sig-616"]
---

# SIG-616 — Continuidad de observabilidad de autorización

## Continuidad

- Sesión de revisión y diseño cerrada por pedido del usuario. Se completó el análisis factual con los dos subagentes solicitados; no hubo cambios de código, comentarios remotos, aprobación de merge ni publicación en Datadog. Consultar el run relacionado para evidencia y límites.
- Fuentes revisadas: [frontend PR 763](https://github.com/melisource/fury_ads-signals-frontend/pull/763), HEAD `90274795879dc873c09c3a19dc7b7232f2289562`, base `1e2764bdf6450c741aacf58690e80f594a6d31dd`; [Playmaker PR 1282](https://github.com/melisource/fury_rio-playmaker/pull/1282), HEAD `33111d39b74f8d2413791df0a44130dd9e04526e`, base `44c290591a104e1471f43f132007fb6d13169684`. Revalidar los heads antes de reutilizar conclusiones.
- Alineación con SIG-616: enforcement sigue en Playmaker, Tiger autentica y ACME autoriza después de resolver ownership persistido. Los PRs no modifican D14 ni D27: ACME no verificable continúa fail-closed 403; basta team O project ausente/vacío/blanco para skip, pero identidad, headers y access level siguen obligatorios. No confundir alineación con aprobación integral de implementación.
- Hallazgos HTTP: Entity Service pasa de 424 a 503, pero el cliente agrupa no-200, parseo inválido y RestException sin conservar causa; el advice fija `UPSTREAM_ERROR` en 502 y colapsa también errores GenAI 503/504. Revisar `ControllerExceptionHandler`, `EntityServiceClientImpl`, `ControlPlaneClientImpl` y `GenAILLMClientImpl`. Otros cambios: pipeline 412→409; KMS timeouts→504, otros fallos upstream→502, 429/503/504 preservados; el advice puede sobreescribir el status original según alias.
- Propuesta pendiente, sin decisión canónica nueva: clasificar 502 para conexión/respuesta upstream inválida, 504 para timeout, 503 para indisponibilidad temporal y 500 para error interno inesperado; distinguir dependencia mediante código de aplicación. Migrar ACME 403 a 5xx requiere decidir aparte porque D14 sigue vigente. Referencias: [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.6) y [RFC 9209](https://www.rfc-editor.org/rfc/rfc9209.html#section-2.3.4).
- Propuesta de dashboard: un resultado por request que llega a guards de enforcement, con `decision=allowed|denied|skipped|error`, endpoint estático y método; fallos ACME separados de permiso insuficiente aunque ambos respondan 403. Skip por missing_team, missing_project o ambos; si hay owners validados y omitidos, allowed con has_skip; autorización aceptada sigue aceptada aunque el negocio falle después. Inventariar guards comunes y legacy, incluidos pipeline y delete con autorización compuesta. No contar cada llamada ACME ni filtros de lectura como decisión de operación.
- Borradores entregados en esta conversación de Codex: `authorization-dashboard.json` y `authorization-metric-contract.json`. Counter candidato `signals.rio.platform.operation_authorization.result`, perfil `.result` con `status=succeeded|failed` y decisión semántica separada; `fury_app` inyectado y `scope` de Fury. JSON validado sintácticamente; métricas sin implementar y dashboard sin validar/importar en Datadog. No convertir borradores en política aprobada.
- Gate formal: preflights Zord de ambos PRs pasaron, pero auto-review rechazó ejecutarlos porque enviarían diffs privados a ocho revisores/proveedores fuera del alcance explícito de dos subagentes. No hubo autorización posterior para Zord; mantener BLOCKED y no eludir el rechazo. No se ejecutaron suites locales; backend CI 6088 reportó cinco checks SUCCESS y Code Reviewer SKIPPED, sin demostrar deploy del head revisado.

## Señales de carga

- Cargar sólo para retomar SIG-616 observabilidad ACME, los PRs citados o su contrato HTTP; la entidad canónica mantiene autoridad sobre D14/D27.

## Próxima acción

- Ajustar y verificar la clasificación HTTP en heads actuales; cerrar el catálogo de guards/endpoints y el contrato de decisiones antes de instrumentar Playmaker y probar la ingestión/dashboard. Resolver Zord sólo si existe autorización explícita para su alcance adicional.
