---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - AnchoredVWAP - Exportación y compatibilidad por versión]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/aportes-y-recursos/indicador-anchoredvwap"
related: ["[[IMOX]]", "[[30-resources/applications/echo/echo-forge]]"]
---

# IMOX - AnchoredVWAP - Exportación y compatibilidad por versión

## Síntesis vigente

Fallo de exportación MT4/MT5 de estrategias que usan AnchoredVWAP en la instalación del autor; las respuestas corrigen la idea de excluirlo para siempre y aportan un parche para 144.

## Conocimiento extraído

El autor no pudo exportar una EA BTCUSD. La explicación reproducida en el post señala que faltaba `MetaTrader4/blocks/AnchoredVWAP.tpl` en las rutas de templates de código.

La lista visible de bloques afectados es:

- `AnchoredVWAPRising`.
- `CloseAboveAnchoredVWAP`.
- `Indicators.AnchoredVWAP`.
- `Stop/Limit Price Levels.AnchoredVWAP`.

Su propuesta inicial fue desactivarlos para evitar construir estrategias no exportables. Esa propuesta queda **matizada por las respuestas**: Jorge PF enlaza el parche `SQX_144_patch_AnchoredVWAP.zip` y Luis reporta funcionamiento en 145.

Enlace comunicado: https://cdn.strategyquantcdn.com/install/sq/144/SQX_144_patch_AnchoredVWAP.zip. No se descargó ni instaló el parche.

## Comentarios y matices

Varios miembros reproducen el problema. Las instrucciones de instalación en comentarios no son precisas sobre carpeta o contenido: no convertirlas en runbook. La discusión distingue volumen de ticks en CFDs de volumen negociado en futuros; la interpretación de la señal exige conocer el feed. Luis menciona COT en 145 y aconseja no usarlo sin entenderlo.

## Adjuntos y cobertura

Cuerpo y 16 comentarios accesibles revisados; lista de cuatro nombres verificada visualmente en Chrome. Captura del error observada; no se auditó el ZIP.

## Interés para Forge

Prioridad de consulta: **Muy alta**. Contexto de Rodrigo: la metodología de [[30-resources/applications/echo/echo-forge|Forge]] se aprendió en [[IMOX]]; los building blocks son la base para generar estrategias nuevas y variadas. Esta ficha es evidencia de investigación, no una configuración aplicada ni una campaña ejecutada.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/aportes-y-recursos/indicador-anchoredvwap).
- Autor: Jorge Eduardo Camilo Bouzon. Lectura directa del post desde Chrome autenticado: 2026-10-24.
- Fuente resoluble: [[IMOX - Fuente - AnchoredVWAP - Exportación y compatibilidad por versión]]. Los comentarios son testimonios u opiniones atribuidos, no validación independiente.

## Límites y contradicciones

No hay certificación de exportación para la versión/instalación de Rodrigo. Antes de habilitar un bloque en campañas, construir un ejemplo mínimo, exportar y compilar en el motor objetivo. Es una verificación propuesta, no realizada.
