---
type: "resource"
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - FTMO - Recuperación con escalera de riesgo]]"]
last_verified: "2026-10-26"
confidence: "high"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-26"
updated: "2026-10-26"
related: ["[[IMOX]]"]
---



# IMOX - FTMO - Recuperación con escalera de riesgo

## Síntesis vigente

Experimento personal: selecciona cartera con seis meses y mide en los seis siguientes; usa remuestreo por bloques y distingue P/L cerrado de equity flotante. Propone EA que publica riesgo por escalones de saldo; reconoce que el fallback tras caída vuelve a un riesgo mayor que el escalón bajo, y que órdenes pendientes conservan tamaño previo. Las cuentas con misma cartera son la misma exposición duplicada. La regla de aumentar tras ganar está apagada y aún no se probó junto con la escalera.

## Evidencia y provenance

[[IMOX - Fuente - FTMO - Recuperación con escalera de riesgo]] · [Circle](https://comunidad.imoxtrading.com/c/prop-firms/como-voy-a-intentar-recuperar-mis-dos-cuentas-de-ftmo) · David Muñoz; revisión 2026-10-26. Afirmaciones atribuidas al autor o a miembros; no comprobación independiente de resultados, código o condiciones comerciales.

## Límites y contradicciones

Simulación/código y discusión extensa no auditados; porcentajes de recuperación son condicionales a muestra y supuestos, no pronóstico.

Decisión de ingesta: `useful`. Estado de lectura: `partial`; el recurso conserva conocimiento útil incluso si quedan medios o respuestas pendientes.
