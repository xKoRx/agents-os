---
type: skill
schema_version: 1
name: deployment-proof
description: Demuestra con jerarquía de evidencia que el proceso/worker que está ejecutando corresponde realmente a la release desplegada; usar ante "¿el worker corre la nueva versión?", "probar el rollout", "ALL_WORKERS_ON_NEW_RELEASE", o cuando un deploy terminó exit 0 y hay que probar el runtime.
scope: global
created: "2026-08-29"
updated: "2026-08-29"
entities: []
related:
  - "[[symphony-worker-runtime-proof]]"
  - "[[evidence-channel-discovery]]"
  - "[[e2e-gated-validation]]"
aliases:
  - prueba de deploy
  - deployment-proof
  - runtime version proof
  - rollout proof
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/verify
---

# deployment-proof

## Purpose

Responder "¿cómo demuestro que lo que está ejecutándose es realmente lo nuevo?" sin aceptar falsos positivos. Un deploy publicado no es un deploy aplicado; un proceso reiniciado no es necesariamente el binario nuevo. La skill obliga a construir la prueba según una jerarquía de evidencia y a declarar el método y sus límites.

## Minimal Read

Read only:
1. La matriz de canales del sistema (ej. [[symphony-worker-runtime-proof]]) o descubrirla con `evidence-channel-discovery` si no existe.

## Procedure

1. Enumerar los workers/procesos requeridos y capturar el estado PRE (identidades de proceso, pollers, versiones declaradas) antes del deploy.
2. Buscar evidencia DIRECTA de versión en runtime, en este orden de preferencia: readout del propio proceso (health/version endpoint), build info del binario en el host, telemetría con versión de build. Si no existe canal directo, construir prueba COMPUESTA: (a) identificación del binario publicado (sha256/manifest como autoridad del contenido), (b) demostración de que el mecanismo de rollout canónico lo entrega a cada host (stager/agent + su registro), (c) rotación observable del proceso (cambio de identidad/PID en el scheduler o task queue tras la publicación, con desaparición de las identidades previas).
3. Verificar ausencia de mezcla: ninguna identidad PRE sobrevive en los gates ya certificados; documentar todo worker que no rotó y si participó en la validación.
4. Reportar por worker: método usado, evidencia exacta (IDs, hashes, timestamps), y límite del método. `ALL_REQUIRED_ON_NEW_RELEASE: PASS` sólo si todos los requeridos tienen prueba; si alguno falta, `PARTIAL/FAIL` con lista.

## Output

```text
<worker>: METHOD=<direct|composite> EVIDENCE=<refs> LIMIT=<límite declarado> => ON_NEW_RELEASE: YES|NO|UNKNOWN
ALL_REQUIRED_WORKERS_ON_NEW_RELEASE: PASS|PARTIAL|FAIL
```

## Hard Rules

- Exit 0 del deploy NO prueba nada sobre el runtime; prohibido declarar "deploy OK" por el comando solo.
- La prueba compuesta exige las tres patas (contenido publicado + entrega demostrada + rotación de proceso); con dos patas el veredicto es INCONCLUSIVE.
- Un worker sin prueba explícita es UNKNOWN, nunca se asume; si participa en la validación siendo UNKNOWN, el gate es FAIL.
- Declarar siempre el límite del método (qué NO prueba la evidencia usada).
