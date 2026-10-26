---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Guía de Building Blocks SQX 145]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/aportes-y-recursos/guia-de-building-blocks-de-sqx-145"
related: ["[[IMOX]]", "[[30-resources/applications/echo/echo-forge]]"]
---

# IMOX - Guía de Building Blocks SQX 145

## Síntesis vigente

Biblioteca de piezas de SQX 145 que el autor declara extraída del código del programa. Complementa la taxonomía de estrategias y la generación de `.sqb` con semántica, parámetros y opuestos para cortos.

## Conocimiento extraído

La guía descargada tiene **151 páginas** y declara 562 bloques en 51 fichas: 387 Signals, 112 Indicators y 63 Stop/Limit, estos últimos divididos en 54 niveles y 9 márgenes. Además trata cuatro tipos de órdenes y ocho salidas. Menciona un CSV completo; ese CSV no se recibió en esta ingesta.

### Lectura necesaria antes de generar presets

- Separar filtro de estado, disparador de evento, valor numérico para comparadores, nivel de entrada y margen de orden.
- `Shift=1` consulta la última vela cerrada. Distinguir valores fijos, rangos y parameter sets; los números negativos reservados del preset representan comodines de configuración, no valores numéricos de indicador.
- Los opuestos para cortos no se deducen por cambiar el nombre: algunos umbrales se reflejan y los bloques sin dirección pueden ser su propio opuesto.
- La familia depende de orden, bloques y salidas en conjunto. Un `.sqb` no fija el signo nivel ± multiplicador × margen; puede requerirse template para imponerlo.
- Los indicadores sueltos y comparadores abren nuevas combinaciones; la guía propone apagarlos cuando se busca una hipótesis acotada.
- No asumir equivalencia con otros motores: señala diferencias en Keltner, señal MACD, Momentum y VWAP, y variantes según plataforma para varios indicadores.

### Construcción y economía del pipeline

La sección inicial separa filtros baratos, controles de coste/ambigüedad/exposición y pruebas caras. Propone ordenar crosschecks por coste y reservar retests intensivos/WF para supervivientes. Enumera tareas para construir, detener por tiempo o cantidad, filtrar, retestear, guardar, limpiar y repetir. Sugiere medir estrategias aceptadas por hora.

Los ejemplos monetarios, umbrales y tiempos que aparecen son propios del documento. No se adoptan como configuración de Forge.

## Comentarios y matices

Comentarios destacan su utilidad como contexto para IA y su relación con el post de tipos de estrategia. El autor indica que resubió una versión más ligera por el límite anterior de 5 MB. No se encontró validación independiente del inventario contra la instalación de Rodrigo.

## Adjuntos y cobertura

PDF descargado por Chrome y leído localmente con autorización: `GUIA SQX 145 - Building Blocks (completa).pdf`, 151 páginas. Enlace: https://academia.imoxtrading.com/documento/1EjVCY3jkxHw. Copia personal marcada por la Academia; no redistribuir.

## Interés para Forge

Prioridad de consulta: **Muy alta**. Contexto de Rodrigo: la metodología de [[30-resources/applications/echo/echo-forge|Forge]] se aprendió en [[IMOX]]; los building blocks son la base para generar estrategias nuevas y variadas. Esta ficha es evidencia de investigación, no una configuración aplicada ni una campaña ejecutada.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/aportes-y-recursos/guia-de-building-blocks-de-sqx-145).
- Autor: Villarrubia. Lectura directa del post desde Chrome autenticado: 2026-10-24.
- Fuente resoluble: [[IMOX - Fuente - Guía de Building Blocks SQX 145]]. Los comentarios son testimonios u opiniones atribuidos, no validación independiente.

## Límites y contradicciones

Se revisaron el post, comentarios y las secciones iniciales de lectura/construcción del PDF, y se inspeccionó su inventario. No se certificó individualmente la fórmula de los 562 bloques contra el código de SQX. La versión objetivo del minado de Rodrigo sigue por confirmar; no trasladar automáticamente 145 a 144.
