---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Misma EA entre brokers - Nasdaq y productos distintos]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/axi-select/misma-ea-distinto-broker-mismo-nasdaq-distinto-producto-que-cambia-realmente"
related: ["[[IMOX]]", "[[30-resources/applications/echo/echo-forge]]"]
---

# IMOX - Misma EA entre brokers - Nasdaq y productos distintos

## Síntesis vigente

Comparación forward de seis EAs en Nasdaq entre AXI NAS100.fs/USTECH y Darwinex NDX. La unidad a validar propuesta es EA + broker + ticker + feed + ejecución.

## Conocimiento extraído

Muestra de unos dos meses: tres de seis EAs seleccionadas y otras tres en observación. Se comparan operaciones coincidentes, signo ganador/perdedor, rendimiento normalizado, drawdown y correlación; no beneficio monetario bruto por diferencias de valor por punto.

- EA1: USTECH replica 100 % de trades de Darwinex y signo, con rendimiento normalizado 92,7 %; NAS100.fs coincide aproximadamente 83 %. Elige USTECH.
- EA2: USTECH coincide 100 % en operaciones/signo y aproximadamente en rendimiento; elige USTECH.
- EA3: NAS100.fs coincide 87,5 % y 100 % de signo de las emparejadas, con rendimiento 83,9 %; elige NAS100.fs.
- Correlación de P/L diario de la cartera elegida: EA1/EA2 −2 %, EA2/EA3 −29 %, EA1/EA3 +55 %.
- Selección solo por beneficio: +1,79 %, DD de balance cerrado 0,37 %, correlación media absoluta 36 %, PF 3,80. Selección conjunta: +1,58 %, DD 0,23 %, correlación 29 %, PF 4,06. Son cifras del mismo pequeño estudio, no rendimiento esperado.

Caso ilustrativo adicional: una EA mostraba resultado final parecido pero solo alrededor de 50 % de signo coincidente; mirar operaciones individuales revela lo que una curva agregada oculta.

## Comentarios y matices

Cristobal advierte que meses de coincidencia pueden romperse con pocas operaciones y que el tamaño de muestra importa. El autor confirma que las instancias estaban en la misma VPS. Define correlación: sumar P/L de operaciones cerradas por día, alinear fechas y poner cero cuando no hubo cierres. No incluyó en esa métrica solapamiento de posiciones, dirección ni exposición flotante; acepta añadirlos. Otros miembros reportan diferencias incluso entre servidores del mismo broker.

## Adjuntos y cobertura

Cuerpo y respuestas adicionales revisados. Tres infografías del post y un adjunto de comentario identificados; cifras y método extraídos del texto, sin auditar cada detalle de esos gráficos.

## Interés para Forge

Prioridad de consulta: **Alta**. Contexto de Rodrigo: la metodología de [[30-resources/applications/echo/echo-forge|Forge]] se aprendió en [[IMOX]]; los building blocks son la base para generar estrategias nuevas y variadas. Esta ficha es evidencia de investigación, no una configuración aplicada ni una campaña ejecutada.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/axi-select/misma-ea-distinto-broker-mismo-nasdaq-distinto-producto-que-cambia-realmente).
- Autor: Gerard Uriarte Castillo. Lectura directa del post desde Chrome autenticado: 2026-10-24.
- Fuente resoluble: [[IMOX - Fuente - Misma EA entre brokers - Nasdaq y productos distintos]]. Los comentarios son testimonios u opiniones atribuidos, no validación independiente.

## Límites y contradicciones

La correlación de cierres diarios no mide por sí sola riesgo simultáneo. La selección y la evaluación usan una muestra corta; no hay validación estadística independiente ni se puede recomendar un ticker universal.
