---
type: "resource"
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - EAs H1 trasladadas a M15]]", "[[IMOX - Fuente adjunta - Calendario M15 estancamiento]]", "[[IMOX - Fuente adjunta - Calendario M15 RetDD]]", "[[IMOX - Fuente adjunta - CSV experimento M15]]"]
last_verified: "2026-10-25"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-25"
updated: "2026-10-25"
source_url: "https://comunidad.imoxtrading.com/c/laboratorio-a51b70/eas-en-temporalidad-m15"
related: ["[[IMOX]]", "[[IMOX — Regularización histórica hasta septiembre 2026]]"]
---

# IMOX - EAs H1 trasladadas a M15

## Síntesis vigente

Experimento de trasladar unas 40 EAs H1 a M15 con CSV y dos portfolios ejemplo. Cambiar TF es otra variante y exige validar de nuevo; el relato no demuestra portabilidad ni permite seleccionar portfolio sin revisar datos y sesgos. CSV descargado sin análisis y dos PDFs revisados parcialmente; falta reconciliación de origen, selección y métricas.

## Comentarios y matices

No se incorpora una conclusión de comentarios no leídos. La cobertura de comentarios permanece sin cerrar.

## Decisión y aplicación

Decisión: **útil**. Conocimiento o contexto útil integrado; resultados atribuidos, sin adopción automática de parámetros. Esta nota conserva investigación personal para [[IMOX]] y [[Estrategias IMOX — Forex y CFD con Echo Forge]]; no crea campañas, configura workers ni certifica resultados.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/laboratorio-a51b70/eas-en-temporalidad-m15).
- Fuente: [[IMOX - Fuente - EAs H1 trasladadas a M15]]. Texto accesible leído en Chrome autenticado el 2026-10-25; fecha visible de publicación `18 sept`. El año 2026 procede del contexto del lote, no de un timestamp nativo confirmado.
- Estado de procesamiento: `partial`. La lectura del cuerpo no implica haber revisado imágenes, vídeos o archivos.

## Pendientes y límites

Comentarios/respuestas completos sin certificar. Estado de adjuntos actualizado en las adendas de esta ficha; completar comentarios y material visual no certificado.

Material identificado: M15Demo.csv; Calendario_Portfolio_Mejor_Estancamiento.pdf; Calendario_Portfolio_Mejor_RetDD.pdf Ningún adjunto, script, plugin o comando del post fue ejecutado. La revisión actual puede incluir comentarios de octubre en publicaciones creadas hasta septiembre; no reconstruye una foto histórica de la discusión al 30 de septiembre.

## Adenda de lectura del adjunto — 2026-10-25

Fuente: [[IMOX - Fuente adjunta - Calendario M15 estancamiento]]. 4 páginas; portada y calendario final revisados, portada visual. Selección DAX/NQ/oro,386trades, RetDD4,28, PF1,23 y estancamiento11,73d según informe. Optimizado sobre la muestra observada; no es validación independiente. Identifica fuente como M15Demo(7).csv, mientras el adjunto se llama M15Demo.csv: identidad y totales por reconciliar. Ceros después de la fecha final de datos no prueban ausencia de señales. Calendarios diarios intermedios no revisados íntegramente.

## Adenda de lectura del adjunto — 2026-10-25

Fuente: [[IMOX - Fuente adjunta - Calendario M15 RetDD]]. 6 páginas; portada y calendario final revisados, portada visual. Selección DAX y dos EAs oro,396trades, RetDD5,51, PF1,36, estancamiento18,01d según informe. Muestra el tradeoff entre estancamiento y RetDD y la concentración posible en oro. Mismos límites de selección, fecha de corte y CSV de origen; no se recalcularon métricas ni todas las celdas diarias.

## Adenda de lectura del adjunto — 2026-10-25

Fuente: [[IMOX - Fuente adjunta - CSV experimento M15]]. Descargado y preservado con checksum. Contenido y asociación de EAs no analizados ni ejecutados. Falta reconciliar con M15Demo(7).csv citado por los dos informes, fechas, costes, identificadores y sesgos de selección antes de confiar en portfolios.
