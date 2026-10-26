---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Cartera de largo plazo y EAs - Regímenes y diversificación]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/psicotrading/mi-cartera-a-largo-plazo-y-mis-eas-una-comparacion-que-me-ha-dado-que-pensar"
related: ["[[IMOX]]", "[[30-resources/applications/echo/echo-forge]]"]
---

# IMOX - Cartera de largo plazo y EAs - Regímenes y diversificación

## Síntesis vigente

La subida del activo no implica que una EA de timing deba ganar. El autor propone estudiar qué movimientos captura cada lógica y diversificar familias, mercados, direcciones y temporalidades.

## Conocimiento extraído

El autor compara una cartera indexada con cinco fondos y sus EAs: la cartera está expuesta continuamente y diversificada geográficamente; las EAs entran y salen según reglas y estaban concentradas en pocos activos. Los rendimientos personales del post son contexto, no benchmark de estrategias equivalentes.

Preguntas que propone:

- ¿Qué hacía el activo cuando perdió la EA: tendencia, rango o volatilidad?
- ¿Ese régimen ya producía pérdidas en su backtest o es una degradación nueva?
- ¿Sufren long y short simultáneamente?
- ¿Hay muestra suficiente antes de declarar que está rota?

Una ruptura puede sufrir falsas salidas de rango y un pullback puede no entrar en una tendencia sin retrocesos. Cambiar de activo sin cambiar el mecanismo puede conservar la concentración de riesgo.

## Comentarios y matices

Algunos miembros ven menos ruido en H4, sin demostración universal. Otro exige superar al activo; se conserva como opinión, no criterio acordado. Xavi propone comparar entradas con una distribución aleatoria conservando cantidad, dirección y duración para distinguir timing de exposición al mercado. La atribución a IA de un mercado más difícil es especulativa y no está demostrada.

## Adjuntos y cobertura

Cuerpo y diez comentarios revisados. Los bloques de código con desglose financiero no se transcriben íntegramente: son contexto personal ajeno, no configuración para las campañas.

## Interés para Forge

Prioridad de consulta: **Alta**. Contexto de Rodrigo: la metodología de [[30-resources/applications/echo/echo-forge|Forge]] se aprendió en [[IMOX]]; los building blocks son la base para generar estrategias nuevas y variadas. Esta ficha es evidencia de investigación, no una configuración aplicada ni una campaña ejecutada.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/psicotrading/mi-cartera-a-largo-plazo-y-mis-eas-una-comparacion-que-me-ha-dado-que-pensar).
- Autor: David Muñoz. Lectura directa del post desde Chrome autenticado: 2026-10-24.
- Fuente resoluble: [[IMOX - Fuente - Cartera de largo plazo y EAs - Regímenes y diversificación]]. Los comentarios son testimonios u opiniones atribuidos, no validación independiente.

## Límites y contradicciones

Una comparación útil debe controlar capital, riesgo, costes, exposición y horizonte. No concluir que una EA está sana solo porque perdió en un régimen conocido; es una hipótesis para contrastar.
