---
type: resource
schema_version: 1
status: active
area: '[[Trading]]'
sources:
- '[[IMOX - Fuente - Gestión variable - Error de timeframe y límite de lotes]]'
last_verified: '2026-10-26'
confidence: high
aliases: []
tags:
- kind/resource
- area/trading
- topic/imox
created: '2026-10-26'
updated: '2026-10-26'
related:
- '[[IMOX]]'
---

# IMOX - Gestión variable - Error de timeframe y límite de lotes

## Síntesis vigente

Caso de EA M15 adjuntada a H1 y límite generado de 30 lotes frente a máximo de 10 del broker reportado. El autor aclara en comentarios inicio en 0,01 y duplicación tras cada pérdida: es martingala, no evidencia de edge estable. La enseñanza operacional es comprobar timeframe, límites y errores reales, además de la curva histórica. La sugerencia previa de Rodrigo de bajar tamaño no certifica viabilidad.

## Evidencia y provenance

[[IMOX - Fuente - Gestión variable - Error de timeframe y límite de lotes]] · [Circle](https://comunidad.imoxtrading.com/c/errores/estrategia-de-gestion-variable) · Stephan Nesteryuk Bendas; revisión 2026-10-26. Afirmaciones atribuidas al autor o a miembros; no comprobación independiente de resultados, código o condiciones comerciales.

## Límites y contradicciones

Imágenes/logs no revisados completos; no se verificó el contrato del broker ni se recomienda la martingala.

Decisión de ingesta: `useful`. Estado de lectura: `partial`; el recurso conserva conocimiento útil incluso si quedan medios o respuestas pendientes.
