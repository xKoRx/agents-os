---
type: skill
schema_version: 1
name: agents-os-project-impact-brief
description: Audit a project or architectural proposal against the current implementation and explain the smallest critical subset a human owner needs to make a safe go/no-go decision. Use when the user asks whether a project makes sense, is implementable or ready, what impact a change has, what will change and where, or requests an ultra-summary of risks, trade-offs, migration and rollout without reading agent-facing documentation.
scope: global
created: "2026-08-15"
updated: "2026-08-15"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-context-retrieval]]"
  - "[[agents-os-implementation-planning]]"
aliases:
  - critical project brief
  - project impact audit
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/project-impact
---

# AGENTS OS Project Impact Brief

## Purpose

Contrastar una propuesta con la realidad vigente, decidir su implementabilidad y transmitir al owner sólo el impacto crítico necesario para autorizar o corregir la ejecución.

## Minimal Read

1. Invocar `agents-os-context-retrieval` para seleccionar el proyecto, entidades relacionadas y fuentes canónicas.
2. Leer la propuesta completa o todas las secciones que puedan cambiar alcance, contratos, migración, rollout o decisión.
3. Inspeccionar únicamente evidencia vigente que pueda refutarla: código, schemas, índices, configs, fixtures, tests, runtime y estado del repositorio.

## Procedure

1. Formular la decisión que el owner debe tomar y el cambio irreversible o costoso que intenta evitar.
2. Construir un ledger interno con tres clases: `CONFIRMADO` (evidencia directa), `INFERIDO` (deducción señalada) y `DESCONOCIDO` (gate pendiente). No mezclar propuesta con realidad.
3. Comparar propuesta versus realidad en siete superficies: ownership y fronteras; flujo e integración; identidad e idempotencia; modelos e historial; compatibilidad y migración; operación, observabilidad y rollback; costo cognitivo y operacional.
4. Trazar cada cambio material a componentes concretos: contratos/tipos, writers, readers, stores, workflows, índices, tests, despliegue y documentación. Si una superficie no cambia, declararlo sólo cuando evite una confusión probable.
5. Clasificar el proyecto: `READY`, `READY_WITH_GATES` o `NOT_READY`. Usar `READY` sólo cuando no queden desconocidos críticos ni contradicciones que puedan cambiar el diseño. Un gate debe tener evidencia de cierre observable.
6. Detectar el orden mínimo seguro. Mover contratos habilitantes antes del primer writer aunque el roadmap los ubique después; conservar generalizaciones y migraciones masivas para después del primer vertical slice.
7. Explicar el 20% crítico en este orden: veredicto; modelo mental antes→después; qué cambia y dónde; qué no cambia; beneficios/costos; formas concretas de cagarla; gates y siguiente corte implementable.
8. Separar `ahora`, `después` y `no hacer`. Marcar como ilustrativas cifras o thresholds no aprobados.
9. Si el usuario autorizó cambios al proyecto, actualizar su estado, decisiones, tareas y contradicciones verificadas sin duplicar la evidencia extensa.

## Output

```text
Veredicto: READY | READY_WITH_GATES | NOT_READY
En una frase: <decisión y consecuencia>
Antes → después: <modelo mental>
Cambios: <componente → impacto>
Se mantiene: <fronteras explícitas>
Ganancias / costos: <trade-off real>
No la cagues con: <3–5 fallas de mayor impacto>
Gates: <evidencia observable para comenzar o avanzar>
Primer corte: <vertical slice reversible y verificable>
Confianza: alta | media | baja · Desconocidos: <lista o ninguno>
```

## Hard Rules

- No declarar “perfectamente implementable” cuando falte evidencia representativa, identidad durable, ownership, compatibilidad de readers/writers o rollback.
- No convertir el resumen ejecutivo en resumen por capítulos; excluir historia y detalle que no cambien la decisión.
- No aceptar como estado actual una afirmación documental refutada por código, datos, fixtures o runtime.
- No proponer big-bang si existe un vertical slice backward-compatible.
- No esconder doble escritura, consistencia eventual, pérdida de historia, colisiones de IDs ni cambios de semántica detrás de nombres genéricos como “refactor”.
- No confundir resultado calculado con decisión de negocio, retry técnico con nueva evaluación, artefacto raw con dato estructurado ni proyección con fuente histórica.
- Citar archivos, símbolos o evidencia operativa para cada contradicción material; marcar explícitamente toda inferencia.
