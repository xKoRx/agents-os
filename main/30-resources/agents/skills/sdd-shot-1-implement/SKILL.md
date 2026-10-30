---
type: skill
schema_version: 1
name: sdd-shot-1-implement
description: Implementa un slice SDD ready contra diseño congelado y entrega código, tests y evidencia como candidato; no diseña, no acepta su trabajo y no orquesta otros shots.
scope: global
created: '2026-10-30'
updated: '2026-10-30'
entities: []
related:
  - '[[sdd-developer]]'
aliases:
  - shot1
  - sdd-implementer
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/sdd
---

# SDD Shot 1 — implementar un candidato verificable

## Purpose

Construir una unidad SDD aprobada con el menor cambio coherente que cumpla sus criterios de aceptación y preserve invariantes. Aplicar al despacho `delivery_role: shot-1-implement`; no a diseño inicial, RCA abierta, verificación independiente ni corrección de hallazgos adjudicados de Shot 2. Es un rol ejecutable en sesión o subagente, no un orquestador.

## Minimal Read

- `../sdd-developer/role-contract.md`: entrada, evidencia, permisos y aprendizaje comunes; rutas relativas a VAULT_ROOT salvo enlaces relativos explícitos.
- SPEC/PLAN/TASKS vigentes, reglas scoped del repo y packs de los scouts ya seleccionados; verificar los fragmentos críticos antes de escribir.
- Código y pruebas afectados; runbooks operativos sólo para operaciones autorizadas. No cargar las otras tres skills ni repetir discovery resuelto.

## Procedure

1. Comprobar readiness y baseline. Expresar el resultado observable, invariantes, no-objetivos y aceptación con fuentes. Si una decisión material de negocio/arquitectura está abierta, retornar `SDD_NOT_READY`; no ocultarla detrás de un default. Resolver detalles locales compatibles sin consultas ceremoniales.
2. Identificar el dueño actual de cada responsabilidad y el punto de extensión previsto por PLAN. Reutilizar contratos y mecanismos existentes; elegir el cambio más simple que satisfaga el caso real. Justificar una nueva abstracción sólo si resuelve una necesidad vigente, no por flexibilidad hipotética.
3. Antes del primer cambio, vincular cada AC activo a una prueba y al resultado esperado independiente. Priorizar rutas críticas, entradas inválidas y efectos laterales pertinentes. Para bugfix, reproducir el fallo cuando sea seguro y posible; para feature nueva, establecer el comportamiento faltante. Si no puede reproducirse, registrar el límite, no fabricar RED.
4. Confirmar aislamiento de escrituras y efectos de tests/herramientas conforme al contrato común. Implementar un slice cohesivo; mantener ownership, errores explícitos, limpieza de recursos y compatibilidad. No añadir refactors ajenos ni rutas de fallback que escondan un fallo.
5. Ejecutar primero la prueba discriminante y después las regresiones afectadas y gates exigidos. Ante fallo, formular una causa contrastable y elegir la evidencia que distingue esa causa de una alternativa relevante antes de otro parche. No repetir el mismo intento sin nueva evidencia.
6. Revisar el diff como consumidor del contrato: ¿qué conducta nueva permite?, ¿qué conducta válida preserva?, ¿qué efecto puede quedar después de error/cancelación? Corregir defectos ordinarios dentro del alcance; escalar el gap material preciso si exige cambiar lo congelado.
7. Fijar identidad final del candidato y evidencia vinculada; disponer tests/probes según `sdd-developer`. Registrar feedback de rol y agent_run cuando corresponda. Retornar candidato, nunca aceptación; no cambiar el procedimiento que gobierna esta ejecución.

## Output

Envelope de `role-contract.md` más:

```text
status: IMPLEMENTATION_CANDIDATE | IMPLEMENTATION_PARTIAL | SDD_NOT_READY | SDD_BLOCKED_EXTERNAL
candidate_identity: repo, baseline, commit/tree/diff y estado dirty observado
acceptance_matrix: AC -> test/escenario -> esperado/observado -> evidencia -> estado
delta: archivos, responsabilidades afectadas y decisiones locales con justificación breve
regressions: resultado, baseline comparable y límites
reusable_assets: clasificación y ubicación canónica propuesta
next: revisión independiente del candidato exacto o gap preciso
```

`IMPLEMENTATION_CANDIDATE` requiere gates de Shot 1 cumplidos; una suite omitida obligatoria produce PARTIAL/BLOCKED, no candidato listo por confianza.

## Hard Rules

- No diseñar arquitectura nueva ni cambiar SPEC, criterios, policy, permisos, freeze o reglas de riesgo para facilitar el código.
- No saltar tests, debilitar assertions ni bajar umbrales para fabricar verde. La política de coverage del repo/Owner se aplica después de proteger lo crítico, sin inventar porcentajes.
- No confundir código compilado con integración, ni test seleccionado con aserción ejecutada; conservar evidencia del comportamiento.
- No autoaceptarse ni lanzar Shot 2/3. El principal dirige las transiciones.
- Ownership de mejora: esta skill. Mejoras del procedimiento se procesan después del retorno por `30-resources/runbooks/sdd-role-improvement.md`; producto y método no se parchean juntos.
