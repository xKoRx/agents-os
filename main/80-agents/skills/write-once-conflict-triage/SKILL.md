---
type: skill
schema_version: 1
name: write-once-conflict-triage
description: Investiga conflictos de inmutabilidad (CONTRACT_CONFLICT, checksum mismatch, idempotency violation, colisión de key) identificando writers, bytes y timeline para clasificar duplicate execution vs stale artifact vs retry legítimo vs race; usar ante "artifact checksum mismatch", "bytes differ", conflictos write-once o errores non-retryable de integridad.
scope: global
created: "2026-08-29"
updated: "2026-08-29"
entities: []
related:
  - "[[echo-forge-cross-system-triage]]"
  - "[[distributed-incident-triage]]"
aliases:
  - triage de conflicto write-once
  - conflicto de idempotencia
  - checksum mismatch
load_policy: manual
indexable: true
index_priority: medium
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/diagnose
---

# write-once-conflict-triage

## Purpose

Cuando aparece un conflicto de escritura inmutable (write-once), el conflicto mismo es evidencia de que DOS productores intentaron escribir bytes distintos bajo la misma identidad lógica. La skill encapsula el método para separar "producto roto" (doble producción legítima de la misma entidad), "infra/race" (entrega duplicada del orquestador), "retry legítimo con bytes estables" (que NO debería conflictuar si el contrato es correcto) y "artifact stale". El contrato write-once que rechaza es correcto por diseño: el triage apunta al DUPLICADO, jamás al rechazo.

## Minimal Read

Read only:
1. El runbook del sistema para las fuentes y layout de keys (ej. [[echo-forge-cross-system-triage]]).

## Procedure

1. Extraer del error: key lógica exacta, bucket/namespace, expected ref (size/SHA) que trajo el writer, y el hash físico almacenado cuando sea legible; capturar también metadatos del objeto (user metadata suele identificar flujo/wave/ejecución).
2. Identificar el objeto en conflicto físicamente: contenido (head), size, SHA256, timestamps de escritura; verificar si los bytes almacenados corresponden al primer intento o a un writer posterior.
3. Construir la timeline de AMBOS intentos con `distributed-incident-triage`: quién programó/ejecutó cada writer (workflow, activity, attempt, identidad de proceso), y si cada intento tiene registro en el orquestador; un intento sin registro es anomalía de orquestación, no del contrato.
4. Clasificar: (a) DUPLICATE EXECUTION — la misma unidad lógica ejecutó dos veces y produjo bytes no deterministas; (b) RACE/ENTREGA DUPLICADA — el orquestador entregó la tarea a más de un worker; (c) STALE ARTIFACT — bytes previos legítimos bajo la misma key por colisión de identidad/naming; (d) CONTRACT DEFECT — un retry legítimo con bytes idénticos fue rechazado (esto sí acusa al contrato/verificador).
5. Verificar la salud del contrato: el rechazo debió ser non-retryable, fail-closed, sin overwrite y con consumer calls 0; si se sobrescribió o se consumió bytes no verificados, eso es un SEGUNDO defecto más grave.
6. Veredicto + evidencia preservada (hashes, keys, IDs, timeline); el fix es ciclo separado.

## Output

```text
CONFLICT: <key> expected=<size/sha> stored=<size/sha/timestamp>
ATTEMPTS: <cada intento con actor registrado sí/no>
VERDICT: DUPLICATE_EXECUTION|RACE|STALE_ARTIFACT|CONTRACT_DEFECT
CONTRACT_HEALTH: fail-closed OK|violado (<cómo>)
```

## Hard Rules

- El write-once NO se debilita ni se "repara" para hacer pasar el flujo: el rechazo correcto es la función working as intended.
- Nunca borrar ni modificar los objetos en conflicto: son la evidencia central.
- Doble producción con bytes no deterministas (timestamps, IDs en el contenido) es defecto del productor aunque el orquestador lo haya duplicado; clasificar ambas capas por separado.
