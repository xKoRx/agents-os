---
type: "resource"
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Análisis de viabilidad FTMO]]", "[[IMOX - Fuente adjunta - PDF simulación FTMO NQ M5]]"]
last_verified: "2026-10-25"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-25"
updated: "2026-10-25"
source_url: "https://comunidad.imoxtrading.com/c/prop-firms/analisis-de-viabilidad-ftmo"
related: ["[[IMOX]]", "[[IMOX — Regularización histórica hasta septiembre 2026]]"]
---

# IMOX - Análisis de viabilidad FTMO

## Síntesis vigente

Simulación de desafíos FTMO iniciados cada lunes con estrategias NQ en ventana NY y distintos riesgos 1–4%. Idea de experimento de tiempo a aprobación y probabilidad de fallo; no demuestra ventaja general del riesgo alto. Desafio_FTMO_NQ_m5.pdf revisado parcialmente; límites de denominadores, censura y solapamiento en la adenda.

## Comentarios y matices

No se incorpora una conclusión de comentarios no leídos. La cobertura de comentarios permanece sin cerrar.

## Decisión y aplicación

Decisión: **útil**. Conocimiento o contexto útil integrado; resultados atribuidos, sin adopción automática de parámetros. Esta nota conserva investigación personal para [[IMOX]] y [[Estrategias IMOX — Forex y CFD con Echo Forge]]; no crea campañas, configura workers ni certifica resultados.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/prop-firms/analisis-de-viabilidad-ftmo).
- Fuente: [[IMOX - Fuente - Análisis de viabilidad FTMO]]. Texto accesible leído en Chrome autenticado el 2026-10-25; fecha visible de publicación `25 sept`. El año 2026 procede del contexto del lote, no de un timestamp nativo confirmado.
- Estado de procesamiento: `partial`. La lectura del cuerpo no implica haber revisado imágenes, vídeos o archivos.

## Pendientes y límites

Comentarios/respuestas completos sin certificar. Estado de adjuntos actualizado en las adendas de esta ficha; completar comentarios y material visual no certificado.

Material identificado: Desafio_FTMO_NQ_m5.pdf Ningún adjunto, script, plugin o comando del post fue ejecutado. La revisión actual puede incluir comentarios de octubre en publicaciones creadas hasta septiembre; no reconstruye una foto histórica de la discusión al 30 de septiembre.

## Adenda de lectura del adjunto — 2026-10-25

Fuente: [[IMOX - Fuente adjunta - PDF simulación FTMO NQ M5]]. 50 páginas; revisión parcial del resumen (p.1) y ficha final (p.50), con p.1 visual. Simulación sobre backtest MT5 2020-01-01 a 2026-08-31, 347 comienzos semanales por variante, riesgos1–4%, cuenta10K, objetivos10/5%, DDtotal10 y diario5. Ojo denominador: 295 aprobados/347 tests y52 sin terminar figuran100% porque excluye censurados; no es probabilidad100% de éxito. Más riesgo puede reducir tiempo y bajar tasa de aprobación. Ventanas semanales solapadas no son ensayos independientes. Faltan revisar las48 páginas intermedias, reglas intradía y código de simulación. No proyectar sus tasas a vivo ni adoptar riesgo4%.
