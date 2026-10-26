---
type: resource
schema_version: 1
status: active
area: '[[Trading]]'
sources:
- '[[IMOX - Fuente - Robustez entre brokers - Estudio de 189 estrategias]]'
- '[[IMOX - Fuente adjunta - PDF Robustez entre brokers]]'
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

# IMOX - Robustez entre brokers - Estudio de 189 estrategias

## Síntesis vigente

Estudio propio: 627 pruebas, 189 estrategias y siete instrumentos; Darwinex como referencia frente a AXI, FP Markets, IC Markets y Oanda. Compara conservación de Ret/DD, con listón personal 0,80, y verifica barras/sesiones. Sólo el 27% del subconjunto con al menos tres destinos aguanta todos; el conjunto no es una muestra aleatoria del mercado. La referencia está favorecida porque allí se construyó. Stop, TF alto y menor actividad conservan mejor en su muestra; no son garantías causales. En comentarios advierte que FP Markets incluye histórico reconstruido M1 y que copiar señales no elimina spread/slippage.

## Evidencia y provenance

[[IMOX - Fuente - Robustez entre brokers - Estudio de 189 estrategias]] · [Circle](https://comunidad.imoxtrading.com/c/laboratorio-a51b70/las-mismas-estrategias-en-cuatro-brokers-que-aguanta-y-que-se-cae) · Xavi Lorente; revisión 2026-10-26. Afirmaciones atribuidas al autor o a miembros; no comprobación independiente de resultados, código o condiciones comerciales.

## Límites y contradicciones

Trades, terminales y calidad histórica no auditados independientemente; no importar listón 0,80 ni ranking de brokers a Forge.

Decisión de ingesta: `useful`. Estado de lectura: `partial`; el recurso conserva conocimiento útil incluso si quedan medios o respuestas pendientes.

## Detalles contrastados en el PDF

Las tablas distinguen 627 pruebas del universo total, 189 EAs, 156 con trades individuales para rasgos y 95 comparadas en los cuatro destinos; no intercambiar denominadores. El dato de conservación no es ranking general de calidad del broker. El texto anuncia siete instrumentos con tamaños de muestra muy dispares y fuerte peso NQ; no extrapolar porcentajes a todos los activos/estrategias. Hay una inconsistencia aritmética a verificar: el ejemplo textual de beneficio 94% y DD 104% no basta por sí solo para convertir Ret/DD 4 en 3; esa frase no se usa como cálculo certificado. Calidad de ticks, cortes y sesiones siguen siendo variables de control.
