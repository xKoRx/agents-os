---
type: "resource"
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Detección de régimen]]"]
last_verified: "2026-10-25"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-25"
updated: "2026-10-25"
source_url: "https://comunidad.imoxtrading.com/c/aportes-y-recursos/deteccion-de-regimen-como-lo-estais-abordando"
related: ["[[IMOX]]", "[[IMOX — Regularización histórica hasta septiembre 2026]]"]
---

# IMOX - Detección de régimen

## Síntesis vigente

Distingue detector retrospectivo para discovery de filtro causal operable. Su Trend Map usa regresión de 20 días en log-precio y pendiente normalizada; el detector causal no mejoró consistentemente el baseline; HMM aún no implementado. Evitar trasladar etiquetas retrospectivas a señales en vivo o asumir resultados del HMM.

## Comentarios y matices

Comentarios: algunos switches de régimen no aportaron, pueden ser redundantes con entradas y eliminar ganadoras. Piden backtest original frente a variante con filtro y resolver diferencia entre TF del detector y TF de la EA. Orquestador aún en investigación, no producto probado.

## Decisión y aplicación

Decisión: **útil**. Conocimiento o contexto útil integrado; resultados atribuidos, sin adopción automática de parámetros. Esta nota conserva investigación personal para [[IMOX]] y [[Estrategias IMOX — Forex y CFD con Echo Forge]]; no crea campañas, configura workers ni certifica resultados.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/aportes-y-recursos/deteccion-de-regimen-como-lo-estais-abordando).
- Fuente: [[IMOX - Fuente - Detección de régimen]]. Texto accesible leído en Chrome autenticado el 2026-10-25; fecha visible de publicación `23 sept`. El año 2026 procede del contexto del lote, no de un timestamp nativo confirmado.
- Estado de procesamiento: `partial`. La lectura del cuerpo no implica haber revisado imágenes, vídeos o archivos.

## Pendientes y límites

Comentarios/respuestas completos sin certificar. Falta comprobar ausencia de adjuntos/cambios y completar discusión.

Material identificado: No se certificó un inventario independiente de adjuntos. Ningún adjunto, script, plugin o comando del post fue ejecutado. La revisión actual puede incluir comentarios de octubre en publicaciones creadas hasta septiembre; no reconstruye una foto histórica de la discusión al 30 de septiembre.
