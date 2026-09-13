---
type: skill
schema_version: 1
name: evidence-channel-discovery
description: Descubre y documenta qué canales de evidencia existen realmente en un sistema antes de investigarlo, con autoridad y limitaciones de cada uno; usar al empezar a trabajar en un sistema desconocido, ante "¿cómo veo X de este sistema?", o cuando una investigación previa encontró canales muertos que hay que registrar.
scope: global
created: "2026-08-29"
updated: "2026-08-29"
entities: []
related:
  - "[[symphony-worker-runtime-proof]]"
  - "[[readonly-production-probe]]"
aliases:
  - descubrimiento de canales
  - evidence-channel-discovery
  - matriz de evidencia
  - canales de observabilidad
load_policy: manual
indexable: true
index_priority: medium
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/discover
---

# evidence-channel-discovery

## Purpose

Evitar el "tour turístico" repetido por SSH/logs/métricas que cada agente hace al enfrentar un sistema desconocido. Antes de investigar, determinar qué canales existen REALMENTE, qué autoridad tiene cada uno para cada pregunta, y cuáles están muertos — y persistir la matriz para que la siguiente sesión no repita el recorrido.

## Minimal Read

Read only:
1. La matriz ya persistida del sistema si existe (ej. [[symphony-worker-runtime-proof]]); sólo descubrir lo que falte.

## Procedure

1. Listar las preguntas de evidencia esperadas del sistema (¿qué versión corre?, ¿qué ejecutó?, ¿qué escribió?, ¿está vivo?).
2. Enumerar canales candidatos por pregunta: readout del proceso, build info del binario, registry/manifest, telemetría (traces/metrics/logs), DBs de control, event log del orquestador, acceso a host (SSH/consola).
3. Probar cada canal con el mínimo costo posible (un query, un curl, una conexión) y registrar el resultado real, no el esperado; un canal que responde con datos viejos, parciales o de otro componente es un canal con autoridad limitada, no un canal válido.
4. Persistir la matriz con el formato pregunta → canal → autoridad (alta/media/ninguna) → limitación, y enlazarla desde el runbook del sistema; los canales muertos se documentan igual (evitan re-tours).

## Output

```text
| Pregunta | Canal | Authority | Limitación |
```

## Hard Rules

- Autoridad se demuestra probando el canal hoy, no por documentación o memoria de sesiones previas.
- Un canal que nunca fue poblado por los componentes (ej. un agregador de logs sin streams de los workers) tiene autoridad NINGUNA para esas preguntas y se registra como tal.
- La matriz se persiste en el runbook del sistema, no en memoria de sesión; es conocimiento, no comportamiento.
