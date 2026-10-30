---
type: skill
schema_version: 1
name: sdd-acceptance-gate
description: Evalúa evidencia del candidato SDD final y aceptación autorizada; separa PASS técnico, autorización y bloqueos sin modificar producto ni convertirse en cuarto shot correctivo.
scope: global
created: '2026-10-30'
updated: '2026-10-30'
entities: []
related:
  - '[[sdd-developer]]'
aliases:
  - acceptance-gate
  - sdd-gate
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/sdd
---

# SDD Acceptance Gate — evidencia, decisión y autoridad

## Purpose

Determinar si la entrega satisface su contrato sobre la identidad final y registrar la aceptación autorizada o el bloqueo exacto. Aplicar a `delivery_role: acceptance-gate`; no es un cuarto shot de implementación. Puede ejecutarlo el principal no implementador o un revisor independiente; un subagente sin autoridad delegada sólo recomienda aceptación.

## Minimal Read

- `../sdd-developer/role-contract.md` y SPEC/PLAN/AC vigentes con alcance de aceptación y autoridad explícitos.
- Baseline, identidad final, reportes de Shots 1–3, adjudicación y `VERIFICATION.md`; abrir evidencia primaria de los claims críticos.
- Skills de release/deploy/E2E sólo cuando ese nivel sea parte expresa del gate. Evidencia de source no prueba runtime.

## Procedure

1. Fijar qué se acepta: source, integración, runtime u otro alcance explícito; quién tiene autoridad; qué contexto independiente produjo la verificación. El autor de Shot 1/3 no certifica en el mismo contexto su trabajo. Sin independencia o mandato de aceptación, mantener el límite visible.
2. Comprobar que código, configuración, dependencias y evidencia corresponden al candidato final. Distinguir evidencia aún aplicable de evidencia invalidada por cambios. Un test verde del candidato anterior no demuestra el fix posterior; cambios sólo documentales requieren equivalencia de inputs demostrada, no supuesta.
3. Reconciliar todos los AC obligatorios, invariantes y findings. Para cada claim crítico identificar fuente, escenario/oráculo, resultado real y límite. No aceptar por mayoría de agentes, número de tests, coverage, autoridad del modelo ni cansancio de iteraciones.
4. Revalidar independientemente los fixes materiales y el delta de Shot 3 mediante reproducer original u otra prueba discriminante segura sobre la identidad final. Reutilizar evidencia vigente no afectada; no rehacer discovery ni toda la campaña por ritual. Si hace falta ejecución externa, pedir un despacho de verificación acotado al principal; no arreglar producto desde el gate.
5. Evaluar impacto real de lo pendiente. Clasificar conforme a la tabla siguiente, sin diluir un requisito incumplido con notas de riesgo. Un problema previo fuera de scope no bloquea automáticamente; documentar por qué no afecta este contrato. Toda exclusión/waiver debe tener autoridad y no equivaler a PASS del criterio excluido.
6. Registrar `technical_gate`, `acceptance`, evidencias, riesgos y próxima acción. Con todos los requisitos probados, aceptar sólo si el actor es Owner o tiene delegación explícita vigente para este alcance. Sin ella emitir `SDD_READY_FOR_ACCEPTANCE`; aprobación técnica no inventa consentimiento.
7. Emitir feedback sobre calidad del gate, señales engañosas y cobertura de evidencia; asociar al feedback del rol responsable los defectos escapados/falsos positivos. La revisión de procedimientos ocurre en mantenimiento separado y no cambia este veredicto retroactivamente.

### Tabla de decisión

| Condición | Resultado |
|---|---|
| Semántica/AC/arquitectura necesarios no están definidos o se contradicen materialmente | `SDD_NOT_READY` |
| Hay un AC/invariante obligatorio incumplido, fix fallido o violación material del scope | `SDD_DELIVERY_FAIL` |
| No hay fallo demostrado pero falta evidencia/independencia/capacidad externa exigida | `SDD_BLOCKED_EXTERNAL`, enumerando gates desconocidos |
| Todos los gates técnicos y registros exigidos completos; autoridad de aceptación ausente | `SDD_READY_FOR_ACCEPTANCE` (intermedio, no entrega aceptada) |
| Todos los gates completos y aceptación autorizada explícita para esa identidad | `SDD_DELIVERY_PASS` |

Si coexisten fallo y falta de evidencia, conservar ambos: un fallo demostrado no desaparece detrás de BLOCKED. Emitir un resultado principal y las condiciones adicionales.

## Output

```text
feature/task + final_identity + acceptance_scope:
technical_gate: PASS | FAIL | INCOMPLETE | NOT_READY
acceptance: ACCEPTED | REJECTED | PENDING_AUTHORITY | NOT_EVALUABLE
authority: actor + mandato/evidencia o ausente
result: SDD_DELIVERY_PASS | SDD_DELIVERY_FAIL | SDD_NOT_READY | SDD_BLOCKED_EXTERNAL | SDD_READY_FOR_ACCEPTANCE
matrix: AC/finding -> evidencia válida para final_identity -> resultado
independent_fix_checks: realizados, fuente y límites
residual_risks + required_next_action:
feedback/agent_run/maintenance: según contrato común
```

## Hard Rules

- No editar producto, cambiar criterios, aprobar sus propias correcciones ni rebajar gates para terminar el ciclo.
- `unknown`/NOT_RUN no equivalen a PASS; restaurar un artefacto después de una violación no demuestra que nunca ocurrió.
- No prometer cero bugs ni extrapolar certificación de tests a rentabilidad, seguridad completa o producción.
- La autorización para aceptar source no autoriza merge, deploy, trading, gasto o cambios de datos; cada operación sigue su mandato específico.
- Ownership de mejora: esta skill, no SPEC ni autoridad de aceptación. Usar `30-resources/runbooks/sdd-role-improvement.md` y revisión independiente para cualquier ajuste futuro.
