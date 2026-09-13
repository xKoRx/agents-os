---
type: skill
name: sdd-workflow
description: Clasifica y ejecuta trabajo de software mediante Spec-Driven Development, manteniendo separadas specification, plan, tasks, implementation y verification. Usar al crear o cambiar una feature no trivial, hacer backfill brownfield, producir/revisar artefactos SDD, retomar una fase, generar un handoff o corregir gaps de trazabilidad. No usar para consultas aisladas ni para imponer SDD completo a cambios triviales que el repo autorice por fast path.
scope: transversal
schema_version: 1
load_policy: manual
indexable: true
index_priority: high
created: 2026-08-08
updated: 2026-09-12
tags:
  - kind/skill
  - action/sdd
  - tech/sdd
  - scope/transversal
---

# SDD Workflow

## Purpose

Ejecutar una fase SDD con límites honestos y artefactos retomables. La
metodología vive en `30-resources/methodologies/sdd/`; esta skill sólo orquesta.

## Minimal Read

1. `30-resources/methodologies/sdd/00-index.md` para seleccionar contexto.
2. `overview.md` + la página de la fase necesaria (`lifecycle`,
   `artifact-model`, `quality-gates`, `roles` o `anti-patterns`).
3. En el repo objetivo: `AGENTS.md`/constitution, catálogo de specs y artefactos
   de la feature. Sus reglas locales mandan sobre defaults metodológicos.
4. Código/tests sólo cuando la fase permita inspección; escribir únicamente
   dentro de sus permisos.

No cargar todo el dominio ni copiar sus páginas dentro del repo.

## Inputs

- `repo_root` y autoridad local.
- pedido e intención del owner.
- feature/capability ID, si existe.
- fase actual y artefactos presentes.
- riesgo: contrato, datos, seguridad, rollout, compatibilidad, múltiples apps.

## Procedure

### 1. Resolver y clasificar

1. Verificar `repo_root`, estado del workspace y reglas locales.
2. Clasificar el pedido como capability/feature, change, bugfix, RCA, plan o
   mixed. Si es mixed, separar outputs antes de escribir.
3. Decidir fast path o ciclo completo con la política del repo. No inventar un
   threshold global; ante duda material, usar el ciclo completo o pedir decisión.
4. Resolver la identidad existente en el catálogo. En brownfield, inspeccionar
   baseline y hacer backfill just-in-time sólo de la capacidad tocada.

### 2. Ejecutar una fase

Por defecto ejecutar una sola fase por handoff. Sólo encadenar fases cuando el
usuario lo pida y cada gate intermedio esté aprobado o autorizado por la política
local.

| Fase | Acción | Output durable | Prohibición |
|---|---|---|---|
| SPECIFY | fijar outcomes, alcance, reglas, aceptación y preguntas | spec/requirements, change o RCA | implementar o decidir diff físico final |
| PLAN | inspeccionar repo y diseñar impacto, riesgos, rollout/rollback y checks | design/plan | modificar código/tests/migraciones |
| TASKS | derivar slices trazables, dependencias, archivos y gate por task | tasks | introducir diseño silencioso |
| IMPLEMENT | ejecutar una task acotada y registrar evidencia | código + estado de task | ampliar alcance o debilitar validación |
| VERIFY | contrastar spec, plan, tasks, diff y runtime | verification/veredicto | arreglar el código durante la auditoría |

Usar los nombres de archivo del repo. La responsabilidad semántica importa más
que `SPEC.md` vs `requirements.md` o `PLAN.md` vs `design.md`.

### 3. Aplicar gates y retornar al dueño del gap

1. Antes de avanzar, verificar el gate de transición en `quality-gates.md` y
   los gates adicionales del repo.
2. Gap de outcome → SPECIFY; arquitectura/impacto → PLAN; granularidad/orden →
   TASKS; defecto → IMPLEMENT; evidencia incompleta → VERIFY/IMPLEMENT.
3. Registrar el fallo antes de corregirlo. No parchear un artefacto downstream
   para ocultar una decisión upstream.
4. Tratar cambios de tests como cambios de contrato cuando corresponda. Nunca
   aceptar skips, assertions más débiles, coverage menor o mocks de conveniencia
   para fabricar verde.

### 4. Dejar continuidad

1. Actualizar catálogo/lifecycle y tareas al estado real.
2. Emitir handoff si cambia fase, sesión o responsable: feature, from/to,
   artefactos requeridos, output esperado, restricciones, evidencia y riesgos.
3. Mantener specs concretas en el repo/proyecto; promover sólo metodología
   reusable y no duplicada a `30-resources/methodologies/sdd/`.

## Output

```text
Repositorio / feature:
Clasificación:
Ruta: fast path | ciclo completo
Fase ejecutada:
Artefactos leídos:
Artefactos creados/tocados:
Gate y evidencia:
Gaps / retorno de fase:
Handoff:
Próxima fase exacta:
```

## Hard Rules

- No mezclar fases ni escribir código en SPECIFY/PLAN/TASKS.
- No usar el chat como único plan o estado.
- No duplicar specs concretas en el dominio metodológico.
- No promover comandos, thresholds o permisos de un repo como regla global.
- No marcar PASS sin ejecutar la evidencia declarada; distinguir manual,
  automatizada, no disponible y no ejecutada.
- Si el artefacto y el runtime contradicen, verificar la fuente viva y resolver
  lifecycle/provenance antes de continuar.
