---
type: skill
schema_version: 1
name: e2e-gated-validation
description: Orquesta validaciones E2E serias como secuencia de gates con evidencia y criterios PASS/FAIL explícitos; usar cuando el usuario pida ejecutar un E2E, golden run, certificación física de una feature/release, validación end-to-end gated, o "correr el pipeline completo contra producción".
scope: global
created: "2026-08-29"
updated: "2026-08-29"
entities: []
related:
  - "[[echo-forge-golden-e2e]]"
  - "[[release-certification]]"
  - "[[deployment-proof]]"
  - "[[readonly-production-probe]]"
  - "[[distributed-incident-triage]]"
aliases:
  - validación E2E gated
  - e2e-gated-validation
  - gates de certificación
  - golden run validation
load_policy: manual
indexable: true
index_priority: critical
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/orchestrate
---

# e2e-gated-validation

## Purpose

Ejecutar una validación E2E como secuencia de gates verificables, evitando los dos modos de falla típicos: el agente que improvisa pasos sin demostrar precondiciones, y el agente que declara PASS porque un comando terminó en exit 0. Cada gate declara objetivo, precondiciones, evidencia, criterio PASS/FAIL y artifacts; no se avanza al gate N+1 si N no está probado. Es la skill orquestadora: enruta cada gate a las skills especializadas y a los runbooks del sistema concreto.

## Minimal Read

Read only:
1. El runbook del sistema objetivo si existe (ej. [[echo-forge-golden-e2e]]) — define los comandos y canales concretos.
2. La skill del gate activo: `release-certification` (baseline/source/release), `deployment-proof` (deploy/runtime), `readonly-production-probe` (observación), `distributed-incident-triage` (fallas).

## Procedure

1. Congelar el CONTRATO de la validación antes de ejecutar: qué debe pasar para PASS, qué se considera defecto de producto vs infraestructura, qué queda fuera de alcance, y la regla de re-run (típicamente FIX → NEW RELEASE → NEW IDs → NEW RUN; nunca patch-and-continue sobre la misma corrida).
2. Ejecutar la secuencia canónica de gates, registrando cada uno en un ledger:

   ```text
   baseline → source integrity → release integrity → deploy → runtime proof → golden run → triage → closure
   ```

3. Para cada gate emitir el contrato completo: objetivo, precondiciones, comandos/evidencia recolectada, criterio PASS, criterio FAIL, artifacts producidos y veredicto `PASS / FAIL / INCONCLUSIVE / NOT_EXECUTED (con razón)`.
4. Ante FAIL de un gate: clasificar la causa con `distributed-incident-triage` antes de decidir. Producto ⇒ detener, preservar evidencia, cerrar BLOCKED, abrir RCA separado. Infraestructura ⇒ remediar sólo si es seguro/reversible/sin cambio de contrato y documentar la remediación.
5. Cierre: reporte con el ledger completo (incluyendo gates NOT_EXECUTED y por qué), IDs/hashes/refs exactos, y persistencia de continuidad (checkpoint + decisión + known-error si aplica + agent run + change log).

## Output

```text
GATE <n> <nombre>: PASS|FAIL|INCONCLUSIVE|NOT_EXECUTED — evidencia: <refs exactos>
SESSION RESULT: PASS|BLOCKED / CLOSED
NEXT EXACT: <siguiente acción nombrada>
```

## Hard Rules

- Nunca avanzar al gate N+1 sin veredicto documentado del gate N; un gate INCONCLUSIVE bloquea igual que un FAIL.
- Nunca declarar PASS por exit 0 de un comando: PASS exige evidencia que distinga la hipótesis probada de su negación.
- NO FALSE PASS: un comportamiento no explicado (ej. efectos sin proceso registrado que los explique) bloquea la certificación aunque el pipeline siga funcionando.
- Durante la certificación no se corrige producto, no se cambia código, no se reutilizan IDs de corridas previas y no se mezclan versiones viejas/nuevas en los gates ya pasados.
- Los detalles mecánicos por sistema viven en runbooks; esta skill no duplica comandos.
