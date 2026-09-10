---
type: doc
scope: vault
created: 2026-07-25
updated: 2026-08-08
project: "[[AGENTS OS - Hot Path y Cierre Silencioso]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-bootstrap]]"
  - "[[agents-os-doctor]]"
load_policy: manual
indexable: true
index_priority: medium
tags:
  - kind/benchmark
  - tech/agents-os
  - project/agents-os
  - kind/doc
  - scope/vault
---

# AGENTS OS Hot Path — End-to-End Benchmark Gate

Gate reproducible para validar que la iteración Hot Path cumple su tesis:
**reducir tokens sin perder una fuente que cambie la decisión.**

## Cuándo correrlo

- Después de una iteración estructural (P0/P1/P2/P3).
- Antes de declarar una beta lista.
- Cuando `agents-os-doctor` reporta HIGH findings en paths o startup.
- Como baseline periódico (mensual) para detectar drift silencioso.

## Métrica relevante

No es cumplir un número rígido. Es **reducir tokens sin perder una fuente
que cambie la decisión**. El benchmark mide ambos lados: tokens cargados y
calidad de la decisión.

## Setup

- Agente fresco (sin caché de sesión previa).
- Vault en estado limpio (sin archivos temporales).
- Graphify indexado al inicio.
- Una tarea real con entidad clara.

## Escenarios (5)

Cada escenario registra: tokens aproximados cargados, latencia hasta la
primera acción útil, fuentes usadas, fuentes omitidas, calidad de la
decisión (1-5), fricción encontrada.

### 1. Cold start

- Conversación nueva.
- Tarea sobre una entidad no cargada.
- Medir: tokens del stack base (constitución + perfil + 1 nota global
  interna) + tokens del primer context pack.
- Objetivo blando: 3-6k tokens de startup + contexto de entidad relevante.

### 2. Warm turn, misma entidad

- Continuación de la tarea anterior en la misma conversación.
- Medir: tokens nuevos cargados en este turno.
- Objetivo blando: <1k tokens nuevos.
- Verificar: NO se releyó constitución/perfil/bootstrap.

### 3. Cambio de entidad

- Misma conversación, switch a otra entidad.
- Medir: tokens del nuevo pack de entidad.
- Objetivo blando: 1-3k tokens para el swap.
- Verificar: constitución/perfil/global interna no se recargaron.

### 4. Graphify degradado

- Simular Graphify caído (sandbox/cache roto, como el conocido de `~/.cache`).
- Medir: tasa de éxito del fallback a Markdown search.
- Verificar: bootstrap declaró retrieval como degradado y reportó el gap.
- Verificar: la decisión final no se vio afectada por la degradación.

### 5. Cinco escenarios de cierre

Correr cinco rutas representativas del delta classifier:

| Modo | Delta simulado | Artefactos esperados | Reporte al usuario |
|---|---|---|---|
| Sin delta | Sesión exploratoria sin conocimiento nuevo | Ninguno | 1-2 líneas |
| Solo continuidad | Update operational, no L3 | Checkpoint interno | 1-2 líneas |
| Conocimiento reusable | Aprendizaje nuevo verificado | L3 + log + reindex dirigido | 1-2 líneas, sin inventario |
| Transcript | Transcript disponible o placeholder solicitado | L0; L1 solo si agrega navegación | 1-2 líneas |
| Auditoría explícita | `cierre con detalle` | Inventario completo | Bloque detallado |

Verificar por cada modo: el inventario entregado al usuario coincide con lo
esperado (no más, no menos). Tactico no es un modo aparte: es la fila 1 o 2.

## Aprobación del gate

El gate pasa cuando TODOS estos se cumplen:

- **Reducción de startup ≥ 60%** vs. baseline pre-Hot-Path (~21-24k tokens
  → ≤ ~8-10k de cold start completo incluyendo entity pack).
- **Warm turn <1.5k** tokens nuevos.
- **Swap-entity <4k** tokens para el nuevo pack.
- **Fallback degradado funcional** — Graphify caído no rompe la sesión.
- **Reporte de cierre correcto** en los cinco escenarios.
- **`agents-os-doctor` pasa limpio** (0 HIGH, ≤ 3 MEDIUM aceptables).
- **Calidad de decisión ≥ 4/5** en escenarios 1-3 (no se perdió ninguna
  fuente que cambiara la decisión).

## Registro de corridas

Cada corrida del gate deja una entrada en `80-agents/journal/logs/` con
nombre `YYYY-MM-DD-hot-path-benchmark-run-N.md` y los datos por escenario.

- **2026-07-27 — validación estática:** doctor strict limpio y cold base
  estimado en ~4.856 tokens. No cuenta como gate E2E porque no usó agente
  fresco ni cubrió warm/swap/cierres.

## Pendiente

- Primera corrida formal del gate queda pendiente hasta que el owner
  libere los cambios (P1/P2/P3 ya aplicados estructuralmente; falta
  forward-test real con agente fresco).
- El proyecto hermano `[[AGENTS OS - Beta y Hardening]]` puede adoptar este
  mismo gate como su benchmark de beta.

## Rollback

- Si el gate falla estructuralmente (no por drift temporal), revertir la
  fase que lo rompió usando los logs atómicos P1/P2/P3.
- Los targets blandos no son motivo de rollback por sí solos: solo lo son
  si la calidad de decisión baja.
