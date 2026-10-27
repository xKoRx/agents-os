---
type: "resource"
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Auditorías de universos de estrategias]]", "[[IMOX - Fuente adjunta - Skill auditoría de universo SQX]]"]
last_verified: "2026-10-25"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-25"
updated: "2026-10-25"
source_url: "https://comunidad.imoxtrading.com/c/aportes-ia/auditorias-de-universos-de-estrategias"
related: ["[[IMOX]]", "[[IMOX — Regularización histórica hasta septiembre 2026]]"]
---

# IMOX - Auditorías de universos de estrategias

## Síntesis vigente

Audita universo con código EA, trades y stats: familias reales, P&L diario, clustering, regímenes y roles CORE/SATELLITE/BENCH/REDUNDANT para decidir qué minar. Comentarios añaden Pearson/Spearman, participation ratio distinto de ENB, Jaccard, estrés/colas y solape de entradas; piden scripts deterministas. Skill SKILL.md de 25,66 KB descargada y leída: extractores declarados para Build136, pendiente adaptación/validación144; ver adenda. No confundir 40 variantes con 40 apuestas independientes.

## Comentarios y matices

Discusión accesible: el autor concreta Pearson/Spearman diario, participation ratio, clustering y solape de entradas, y análisis de estrés/drawdowns. Otros proponen Jaccard y scripts reproducibles, así como Custom Analysis de SQX para grupos de entrada/correlación. Quedan respuestas/adjunto por cerrar; no equiparar ENB con una media simple de correlaciones.

## Decisión y aplicación

Decisión: **útil**. Conocimiento o contexto útil integrado; resultados atribuidos, sin adopción automática de parámetros. Esta nota conserva investigación personal para [[IMOX]] y [[Estrategias IMOX — Forex y CFD con Echo Forge]]; no crea campañas, configura workers ni certifica resultados.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/aportes-ia/auditorias-de-universos-de-estrategias).
- Fuente: [[IMOX - Fuente - Auditorías de universos de estrategias]]. Texto accesible leído en Chrome autenticado el 2026-10-25; fecha visible de publicación `20 sept`. El año 2026 procede del contexto del lote, no de un timestamp nativo confirmado.
- Estado de procesamiento: `partial`. La lectura del cuerpo no implica haber revisado imágenes, vídeos o archivos.

## Pendientes y límites

Comentarios/respuestas completos sin certificar. Estado de adjuntos actualizado en las adendas de esta ficha; completar comentarios y material visual no certificado.

Material identificado: SKILL.md (25,66 KB) e imágenes Ningún adjunto, script, plugin o comando del post fue ejecutado. La revisión actual puede incluir comentarios de octubre en publicaciones creadas hasta septiembre; no reconstruye una foto histórica de la discusión al 30 de septiembre.

## Adenda de lectura del adjunto — 2026-10-25

Fuente: [[IMOX - Fuente adjunta - Skill auditoría de universo SQX]]. Lectura textual completa. Extractores mq4/SQStats validados en Build 136; recalibrar con 144/MT5 antes de usar. Distingue evidencia A backtest, B diversidad y C holdout/live; desconocido no equivale a ausente. Propone código+trades+SQX reconciliados, clustering, regímenes, estrés, DSR/PBO y prioridades por gap. Límites detectados al leer: el número efectivo de su fórmula es participation ratio, no intercambiable con cualquier ENB; usar cuantiles de toda la muestra para vol/estrés no constituye umbral causal aprendido solo con pasado; el proxy de precios desde operaciones es endógeno y no demuestra régimen no observado; orden stop no determina por sí sola la familia económica. Umbrales y parsing son ejemplos, no contrato Forge. Instrucciones externas archivadas como evidencia, sin instalarlas ni ejecutarlas.
