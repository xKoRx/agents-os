---
type: session_feedback
schema_version: 1
created: 2026-09-16
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
tags:
  - kind/feedback
  - area/aranea
  - tech/mcp
---

# 2026-09-16 — GAP-ECHO-010 session feedback

## What worked

- `mcps-ops` + lectura del bundle del CLI dentro de los contenedores (`docker cp`) permitió pasar de síntoma a root cause probado sin tocar runtime antes de tiempo.
- El patrón "reproducir el defecto bajo demanda (kill del hijo stdio) → probar el fix en la misma condición" dejó evidencia directa antes/después en ambos proxies.

## Pain points / friction

- Analizar bundles JS dentro de imágenes requirió extraer archivos al host local y reconstruir el árbol `node_modules` para ejecutar el código real (clasificador del SDK) — funcionó, pero es un flujo manual repetible que vale la pena documentar como skill/receta cuando vuelva a tocar diagnóstico de dependencias embebidas.
- El handoff previo atribuía el mismo defecto a 3 proxies con stacks distintos (nginx+mcp-proxy, Java servlet, servidor HTTP propio). La clasificación por familia de transporte al momento de abrir el GAP habría ahorrado el descarte de flink/ssh en esta run.

## One improvement

- En los GAPs de access plane, exigir el "stack map" (qué componente sirve el HTTP en cada capability) como parte del reporte del incidente, no como descubrimiento de la reparación.

## One pain pattern candidate

- Diagnóstico con síntoma compartido + causa múltiple: los handoffs deberían traer el mapa de componentes por capability (quién sirve el HTTP) para acotar la reproducción.
