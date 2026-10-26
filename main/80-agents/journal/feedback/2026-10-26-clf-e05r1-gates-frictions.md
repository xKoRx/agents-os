---
type: session_feedback
schema_version: 1
scope: area
created: "2026-10-26"
updated: "2026-10-26"
area: "[[Echo]]"
project: "[[Echo Futures — Optimización de Campañas]]"
application:
entities: ["[[Echo Futures]]"]
related: []
aliases: []
feedback_kind: system_gap
severity: medium
recurrent: false
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session-feedback
  - scope/area
  - area/echo
---

# session feedback — CLF-E05-R1: tres fricciones reales de gates

1. **El clasificador de propósito bloquea canarios de rollover frescos.** `effective_execution_purpose` clasifica una ventana corta de roll (11 días, NQM6) como HISTORICAL ⇒ `PURPOSE_CONTRADICTS_EXECUTION_IDENTITY` (exit 78, 0 motores) para un ROLLOVER_CANARY declarado. El precedente Q03-R1 (reutilizar el G3 del ciclo propio) funciona pero deja al canario SIN re-ejecutar cuando el build cambia. Sugerencia: registrar la ventana de roll canario en `WINDOW_REGISTRY` con `purpose: ROLLOVER_CANARY` (la ruta que el propio clasificador consulta para ventanas cortas) — entonces un canario fresco por build sería admisible sin debilitar el guard.
2. **La retención de evidencia de motivo (4 buckets rodantes) era un límite de estado latente.** Con la ventana `strict` de 1 vela nunca se notó; `until_invalidation` lo expuso: todo swing que resolviera >4h tras su referencia reportaba MOTIVE_UNAVAILABLE. Corregido congelando la composición de la referencia en el intento al armar. Lección: cada extensión de ventana de un detector debe auditar la retención de SU evidencia (los límites de estado no son ortogonales a la semántica de ventana).
3. **Los fixtures de K05 (FX-01/FX-02) llevaban la mecánica invertida en su prosa** («toma el low ⇒ side SHORT»; el código/ch01 c-0007: toma HIGH ⇒ rango bajista side SHORT). El handoff se consumió con los claims como autoridad (c-0029/c-0045/c-0046 + ch01 c-0005/c-0007/c-0009) y la prosa de los fixtures se trató como especificación informal. Lección: en los handoffs entre hosts, los fixtures deberían citar el átomo estructural (yaKC-08) y verificar la dirección del Side contra el código receptor antes de publicarse.
