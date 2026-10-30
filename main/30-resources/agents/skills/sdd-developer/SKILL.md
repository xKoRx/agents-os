---
type: skill
schema_version: 1
name: sdd-developer
description: Orchestrate a ready SDD unit through three fresh-context roles (implement, independently verify, correct) and a separate evidence-based acceptance gate. Delegate each phase to its canonical skill; do not use to create initial SPEC/PLAN/TASKS, for isolated lookups, or to turn a worker into another manager.
scope: global
created: '2026-09-23'
updated: '2026-10-30'
entities: []
related:
  - '[[sdd-workflow]]'
  - '[[compounding-engineering-vision]]'
  - '[[technical-project-manager]]'
  - '[[e2e-gated-validation]]'
  - '[[agents-os-agent-run-register]]'
  - '[[agents-os-session-feedback]]'
  - '[[agents-os-session-close]]'
  - '[[sdd-shot-1-implement]]'
  - '[[sdd-shot-2-verify]]'
  - '[[sdd-shot-3-correct]]'
  - '[[sdd-acceptance-gate]]'
aliases:
  - sdd developer
  - sdd implementation agent
  - sdd three-shot developer
load_policy: manual
indexable: true
index_priority: critical
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/sdd
  - action/development
  - action/verification
---

# SDD Developer — orquestación de entrega

## Purpose

Orquestar una unidad SDD ready mediante IMPLEMENT → VERIFY independiente → CORRECT → ACCEPTANCE. Esta skill posee secuencia, handoff y ubicación del conocimiento ejecutable; las cuatro skills de rol poseen sus criterios. No duplicar sus procedimientos aquí ni crear un quinto implementation-worker. El gate es una decisión posterior, no otro shot de código.

## Minimal Read

1. `30-resources/agents/skills/sdd-workflow/SKILL.md` y `role-contract.md` de esta carpeta.
2. SPEC/PLAN/TASKS/VERIFICATION de la unidad activa y reglas del repo; packs de scouts suficientes y vigentes.
3. Baseline exacta, evidencia de dependencias y autoridad de aceptación.
4. `e2e-gated-validation`, release/deployment skills sólo si ese nivel pertenece al alcance autorizado.
5. Cargar el cuerpo de cada skill de rol en su contexto ejecutor; el principal usa el mapa siguiente y los retornos. Authoring/mantenimiento sólo ante mejora evidenciada.

## Inputs

Unidad/tarea, baseline, SPEC/PLAN/TASKS ready, decisiones congeladas, AC y no-objetivos, scopes y entorno autorizado, autoridad de aceptación/publicación y restricciones del repo. `role-contract.md` posee el envelope de cada despacho.

## Procedure

### 1. Confirmar readiness y capacidad

Verificar consistencia de autoridades, identidad del workspace y gates. Semántica/arquitectura abierta → `SDD_NOT_READY` y retorno a la fase dueña mediante `sdd-workflow`; tooling/evidencia externa inaccesible → bloqueo preciso. No inventar defaults de negocio ni poner todo el discovery dentro de la implementación.

Usar los scouts para gaps no triviales antes de despachar. Resolver capacidad real de contexto independiente, escritura y pruebas seguras. Si no hay subagentes, usar sesiones separadas con handoff. No declarar una revisión independiente desde el mismo contexto implementador.

### 2. Despachar los roles sin duplicar responsabilidades

| Fase | Rol asignado | Skill canónica relativa a VAULT_ROOT | Retorno habilitante |
|---|---|---|---|
| Shot 1 | `shot-1-implement` | `30-resources/agents/skills/sdd-shot-1-implement/SKILL.md` | `IMPLEMENTATION_CANDIDATE` identificado |
| Shot 2 | `shot-2-verify` | `30-resources/agents/skills/sdd-shot-2-verify/SKILL.md` | reporte independiente completo + findings/probes |
| Shot 3 | `shot-3-correct` | `30-resources/agents/skills/sdd-shot-3-correct/SKILL.md` | `FINAL_CANDIDATE_READY` con evidencia |
| Gate | `acceptance-gate` | `30-resources/agents/skills/sdd-acceptance-gate/SKILL.md` | veredicto técnico y aceptación autorizada o gap |

Cada Shot 1/2/3 usa contexto fresh y mandato self-contained con las secciones `/goal`, `/authorities`, `/baseline`, `/frozen`, `/scope`, `/execute`, `/verify`, `/reuse`, `/improve`, `/close`. Son secciones semánticas, no comandos del IDE. Incluir el `delivery_role`, `run_id`, skill obligatoria y sus revisiones según `role-contract.md`. `/close` sólo pide resultado/registros; cierre de sesión Agents-OS requiere solicitud explícita aparte.

El principal adjudica los findings de Shot 2 antes de Shot 3, preservando evidencia y aceptación del Owner cuando corresponda. Un reporte parcial no habilita la fase como si estuviera completo. No esperar que los subagentes se lancen entre sí ni entregarles la autoridad global del manager.

Un Shot 2 limpio no obliga a inventar fixes: Shot 3 puede entregar candidato sin delta tras comprobar evidencia y disposición de assets. Defectos ordinarios dentro del scope se resuelven durante el shot; no planear una cuarta ronda correctiva. Si no alcanza, reportar FAIL/BLOCKED/NOT_READY y que el principal decida un nuevo ciclo explícito. El gate puede ordenar una revalidación independiente acotada del fix, nunca arreglarlo por sí mismo.

### 3. Preservar verificación y conocimiento ejecutable

Mantener en `VERIFICATION.md` la relación `AC/invariante → test/escenario → evidencia/identidad → estado`. Pruebas quedan en sus owners canónicos: invariantes locales en el paquete, integraciones en su paquete, comportamiento cross-component en el módulo E2E existente y setup/validadores reutilizables en toolkit/test-support. Una carpeta por SPEC es convención local, no requisito universal. Si falta owner de E2E, resolverlo en PLAN; no crear framework competidor en una implementación.

Clasificar todo nuevo asset de verificación como `PERMANENT_REGRESSION`, `E2E_CANDIDATE`, `HARNESS_TOOLKIT_CANDIDATE` o `DISPOSABLE_REPRODUCER`. Los reproducers que detectan defectos reales se presumen regresiones valiosas; documentar su descarte, unificar cobertura equivalente y conservar el invariante más fuerte. No esconder código ejecutable de tests en carpetas de documentación salvo policy explícita del repo. Conservar fixtures allí sólo cuando la policy lo admita.

### 4. Aplicar gate y devolver el estado real

La skill `sdd-acceptance-gate` posee la tabla de decisión. El principal no agrega una segunda aprobación basada sólo en el resumen: comprobar sus evidencias críticas y la autoridad de quien acepta. Sin autorización efectiva, `SDD_READY_FOR_ACCEPTANCE` es intermedio, no `SDD_DELIVERY_PASS`. Aceptación de source no certifica deploy, producción ni resultado económico.

No cerrar tasks como aceptadas ni publicar releases por un candidato listo. Registrar estado real, findings adjudicados, evidencia final y siguiente fase en los artefactos existentes; no crear otro planner.

### 5. Perfeccionar roles con evidencia

Cada invocación de los cuatro roles evalúa y registra feedback compacto según `role-contract.md`; registrar agent_run cuando su trigger aplique. NO_FINDING es válido. Vincular defectos escapados, falsos positivos y retrabajo al feedback del rol que originó la conducta, no sólo al último modelo que los vio.

Cada rol mantiene su propia skill a través de `30-resources/runbooks/sdd-role-improvement.md`, en mantenimiento separado, revisión independiente y aplicación desde la siguiente invocación. El principal mantiene orquestador/contrato/runbook compartidos. No modificar skills ni criterios a mitad de una entrega para lograr PASS. Una mejora puede ocurrir tras un run fallido terminal sin exigir que el producto pase primero; no recertifica ese run.

## Output

```text
feature/task + baseline + alcance de aceptación:
shots: rol, run_id, skill/revisión, identidad, estado y evidencia
adjudication: findings aceptados/refutados/deferred y autoridad
assets: regresión/E2E/toolkit/disposable con ubicación y disposición
final_identity + verification_matrix:
gate: technical_gate, acceptance, authority, result según sdd-acceptance-gate
learning: feedback/agent_run por rol, mejoras propuestas/aprobadas/aplicadas o NONE
next_exact_phase_or_dependency:
```

## Hard Rules

- No duplicar el lifecycle de `sdd-workflow` ni los procedimientos de las cuatro skills; cada hecho tiene un owner.
- El worker asignado carga su rol, no vuelve a orquestar este pipeline. Diseño principal y decisiones del Owner siguen congelados.
- Shots 1/3 no aceptan su código; Shot 2 no lo corrige; gate no implementa. Un cambio de modelo no sustituye independencia ni evidencia.
- No planear un cuarto shot para forzar éxito ni ejecutar micro-prompts de corrección indefinidos; devolver el gap material.
- Ningún requisito obligatorio queda PASS por NOT_RUN, waiver silencioso, coverage global, pruebas tautológicas o firmas de los agentes.
- Conservar regresiones útiles y evidencia vinculada a la identidad final; no degradar verificabilidad por ahorrar tokens.
- No crear prompts/skills paralelos en el cliente. El adaptador enlaza: `role-adapters.md`.
