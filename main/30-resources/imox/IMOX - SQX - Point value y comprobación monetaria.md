---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - SQX - Point value y comprobación monetaria]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox", "topic/sqx144"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/aportes-y-recursos/point-value-en-sqx-no-es-el-valor-del-tick-y-como-me-salieron-p-l-100-veces-mas-pequenos"
related: ["[[IMOX]]"]
---

# IMOX - SQX - Point value y comprobación monetaria

## Síntesis vigente

El autor confundió `Point value in $` con valor del tick al configurar BTCUSD. Sus ratios parecían buenos mientras el P/L monetario era cien veces demasiado pequeño.

## Definición y control descritos

El campo representa valor monetario de **una unidad completa de precio por un lote**, no un incremento mínimo de cotización. En su caso BTCUSD de contrato de un BTC usó 0,01 donde correspondía uno.

Ejemplo publicado: movimiento de −643,99 a 0,01 lotes produce −6,44 antes de otros ajustes; la configuración errónea mostraba −0,06. Revisar una operación conocida puede descubrir un error que PF o Ret/DD no revelan bajo un simple escalado.

Para contratos lineales, el cálculo de control propuesto es movimiento de precio × lotes × point value, con signo según long/short; luego reconciliar costes, swap y conversión monetaria. No usar esa forma simple sin validar especificaciones de contratos no lineales u otras modalidades de cálculo.

Las tablas BTC/Nasdaq/DAX del autor son de su cuenta y momento. Los nombres de símbolo no fijan tamaño de contrato ni conversión: obtener las especificaciones del broker/servidor/producto de la campaña.

## Qué implica para el arranque

Antes de minar, verificar instrumento, tamaño de contrato, tick/pip, divisa, point value, lote mínimo/paso, sesión y costes. Después comparar P/L de una operación con el esperado y MT5. Un profile importado es un punto de partida, no una prueba automática de corrección.


## Evidencia y provenance

- [Post original en Circle](https://comunidad.imoxtrading.com/c/aportes-y-recursos/point-value-en-sqx-no-es-el-valor-del-tick-y-como-me-salieron-p-l-100-veces-mas-pequenos).
- Autor: Jefté Villarreal Herenas. Revisión directa en Chrome: 2026-10-24.
- [[IMOX - Fuente - SQX - Point value y comprobación monetaria]]. Se distinguen instrucciones escritas del administrador, prácticas de miembros y análisis propio.

## Límites y contradicciones

Cuerpo y ocho comentarios accesibles revisados; algunos contienen contenido no expuesto en texto completo. No se consultó especificación actual de AXI/Darwinex ni se auditaron sus contratos. Se conserva como evidencia de un error y control de configuración, no recomendación financiera.
