---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Tipos de estrategia en trading algorítmico]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/aportes-y-recursos/tipos-de-estrategia-en-trading-algoritmico"
related: ["[[IMOX]]", "[[30-resources/applications/echo/echo-forge]]"]
---

# IMOX - Tipos de estrategia en trading algorítmico

## Síntesis vigente

Taxonomía para diversificar las lógicas de construcción. El autor detectó más de 85 % de breakout en sus EAs y propone definir qué familia se quiere construir antes de pedir configuraciones a la IA.

## Conocimiento extraído

### Familias expuestas en el post

| Familia | Tipos enumerados |
|---|---|
| Tendencia y ruptura | Ruptura de máximos, expansión de rango, ruptura de canal, momentum, seguimiento de tendencia y pullback. |
| Reversión | Reversión a la media, falsa ruptura/fade, giro desde mínimos y giro por patrón. |
| Volatilidad, sesión y calendario | Squeeze, estrategias de sesión/intradía como ORB o gap fill y estacionalidad/calendario. |
| Fuera del alcance fácil de SQX | Pares/arbitraje estadístico, rotación entre activos, carry, market making/microestructura y lógica macro/fundamental/sentimiento/ML con datos externos. |

El objetivo es conectar lógica económica, forma de entrada y configuración de Builder/AlgoWizard; el PDF promete ejemplos, construcción en SQX, referencias y cómo pedir `.cfx`. La cuarta familia describe límites del flujo estándar, no imposibilidad absoluta de implementar extensiones.

## Comentarios y matices

Varios miembros reconocen concentración en breakout. Oscarrené cuenta que Bar and Time/estacionalidad le falla en crosschecks. Cristobal plantea adaptar la validación al mecanismo del edge y observar demos durante tiempo suficiente; no demuestra que relajar una prueba sea correcto. Es un desacuerdo metodológico que se debe resolver antes de cambiar gates. Los resultados recientes de miembros no prueban causalidad entre familia y rendimiento.

## Contraste con el PDF descargado

Se recibió y revisó el PDF de 15 páginas, con detalle en clasificación (p. 1), construcción por familia (pp. 2–10), pedidos `.cfx` (pp. 11–12) y diversificación (pp. 13–14).

**Cinco decisiones complementarias a los ejes de campaña:** lógica, tipo de orden, horizonte, disparador y salida. Se suman mercado, sesión y dirección. Dos EAs con indicadores diferentes pueden representar la misma apuesta si coinciden en estas decisiones.

Para pedir un `.cfx`, declarar familia, activo, dirección, horizonte y lo que se debe excluir; dejar rangos razonables para la búsqueda de SQX y exigir resumen de lo configurado. La guía propone clasificar el portfolio existente y generar las familias que faltan. No entrega un `.cfx` listo ni impone valores universales.

El mapa separa seguir el movimiento frente a revertirlo, y velocidad intradía frente a días/semanas. Pullback es híbrido: filtra tendencia y entra contra el último movimiento. Cambiar Bollinger por Donchian no garantiza cambiar la apuesta.

Recomienda revisar correlación en varias escalas, operaciones solapadas y coincidencia de drawdowns. Los estudios citados sobre momentum/futuros/factores son referencias del autor: no se consultaron ni verificaron directamente en esta ingesta y no prueban rentabilidad de una EA concreta.

## Adjuntos y cobertura

Post y comentarios accesibles revisados. PDF complementario: https://academia.imoxtrading.com/documento/fCSxIo7WlOmA. Descarga facilitada por Rodrigo; PDF leído localmente con su autorización. Hay una captura de comentario sobre Bar and Time, no certificada celda por celda.

## Interés para Forge

Prioridad de consulta: **Muy alta**. Contexto de Rodrigo: la metodología de [[30-resources/applications/echo/echo-forge|Forge]] se aprendió en [[IMOX]]; los building blocks son la base para generar estrategias nuevas y variadas. Esta ficha es evidencia de investigación, no una configuración aplicada ni una campaña ejecutada.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/aportes-y-recursos/tipos-de-estrategia-en-trading-algoritmico).
- Autor: Cristobal Aljaro. Lectura directa del post desde Chrome autenticado: 2026-10-24.
- Fuente resoluble: [[IMOX - Fuente - Tipos de estrategia en trading algorítmico]]. Los comentarios son testimonios u opiniones atribuidos, no validación independiente.

## Límites y contradicciones

La clasificación es una herramienta de investigación; cambiar de indicador no demuestra diversidad económica ni descorrelación. La hipótesis y los criterios de validación deben fijarse antes de mirar el resultado.
