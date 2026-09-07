---
type: skill
schema_version: 1
name: distributed-incident-triage
description: Investiga fallas donde participan varios subsistemas construyendo una timeline común y encontrando el primer punto de divergencia; usar ante incidentes multi-sistema, fallos de pipeline distribuido, "algo falló y no sé en qué capa", o cuando hay que clasificar un fallo como producto vs infraestructura vs version skew.
scope: global
created: "2026-08-29"
updated: "2026-08-29"
entities: []
related:
  - "[[echo-forge-cross-system-triage]]"
  - "[[readonly-production-probe]]"
  - "[[evidence-channel-discovery]]"
aliases:
  - triage de incidente distribuido
  - timeline forense
  - clasificación causa raíz
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/diagnose
---

# distributed-incident-triage

## Purpose

Investigar fallas multi-subsistema con método forense en vez de hipótesis sueltas: construir una timeline normalizada de todos los side effects observables, correlacionarlos, encontrar el primer punto de divergencia y clasificar la causa. Produce un veredicto defendible: producto / infraestructura / deployment-version-skew / dependencia externa / inconclusive.

## Minimal Read

Read only:
1. El runbook del sistema para las fuentes de evidencia concretas (ej. [[echo-forge-cross-system-triage]]).

## Procedure

1. Definir el hecho anómalo con precisión (qué se esperaba, qué se observó, IDs exactos).
2. Inventariar las fuentes de evidencia disponibles por subsistema (event log del orquestador, object store, DBs de control/evidencia, logs locales/remotos, traces) y registrar cuáles NO están accesibles — la ausencia de una fuente también es evidencia.
3. Extraer de cada fuente los eventos con timestamps normalizados a una sola zona horaria y formar la timeline común; capturar para cada entrada el actor/proceso que la produjo cuando sea determinable.
4. Correlacionar: buscar side effects SIN actor registrado (escrituras sin ejecución que las explique), ejecuciones SIN side effect, y huecos temporales; el primer punto donde observación y registro divergen es el foco.
5. Clasificar la causa sobre la divergencia: defecto de producto (código produjo el comportamiento), infra (componente caído/lento/red), version skew (mezcla de releases), dependencia externa, o INCONCLUSIVE (con lo que faltaría para cerrar).
6. Preservar la evidencia cruda referenciada (IDs, hashes, keys, queries reproducibles) antes de cerrar; NO remediar nada durante el triage salvo infra segura y reversible, documentado.

## Output

```text
TIMELINE: <eventos normalizados con actor>
FIRST_DIVERGENCE: <evento + qué debió pasar y no pasó>
CLASSIFICATION: PRODUCT|INFRA|VERSION_SKEW|EXTERNAL|INCONCLUSIVE — <razón>
EVIDENCE: <refs exactas preservadas>
```

## Hard Rules

- Un side effect sin actor explicado NO se desecha ni se explica por conveniencia: queda como anomalía abierta y tipicamente fuerza INCONCLUSIVE o defecto de orquestación.
- No corregir nada durante el triage; el fix es un ciclo separado bajo la regla FIX → NEW RELEASE → NEW IDs → NEW RUN.
- Sin logs del proceso emisor, la clasificación se limita a lo observable: decirlo explícitamente en lugar de inferir.
