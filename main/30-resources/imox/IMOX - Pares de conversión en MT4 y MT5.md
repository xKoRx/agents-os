---
type: "resource"
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Pares de conversión en MT4 y MT5]]"]
last_verified: "2026-10-25"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-25"
updated: "2026-10-25"
source_url: "https://comunidad.imoxtrading.com/c/aportes-y-recursos/por-que-mostrar-siempre-los-pares-de-conversion-en-mt4-5"
related: ["[[IMOX]]", "[[IMOX — Regularización histórica hasta septiembre 2026]]"]
---

# IMOX - Pares de conversión en MT4 y MT5

## Síntesis vigente

El autor midió que un par de conversión oculto puede provocar tick value cero y lote de reserva. Antes de desplegar: resolver divisa del contrato/cuenta, dejar visible el cruce necesario y revisar logs LotsIfNoMM. Caso probado por él en MT5 Darwinex y observado en MT4; no equivale a imposibilidad universal de programar una espera ni a tabla de símbolos válida para todo broker.

## Comentarios y matices

La discusión acepta Show All como opción simple, pero otros prefieren exponer solo cruces necesarios por carga de red. Hay experiencias sin fallo por reinicios o especificación del broker; el problema debe verificarse en cada terminal.

## Decisión y aplicación

Decisión: **útil**. Conocimiento o contexto útil integrado; resultados atribuidos, sin adopción automática de parámetros. Esta nota conserva investigación personal para [[IMOX]] y [[Estrategias IMOX — Forex y CFD con Echo Forge]]; no crea campañas, configura workers ni certifica resultados.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/aportes-y-recursos/por-que-mostrar-siempre-los-pares-de-conversion-en-mt4-5).
- Fuente: [[IMOX - Fuente - Pares de conversión en MT4 y MT5]]. Texto accesible leído en Chrome autenticado el 2026-10-25; fecha visible de publicación `27 sept`. El año 2026 procede del contexto del lote, no de un timestamp nativo confirmado.
- Estado de procesamiento: `partial`. La lectura del cuerpo no implica haber revisado imágenes, vídeos o archivos.

## Pendientes y límites

Comentarios/respuestas completos sin certificar. Adjunto o material adicional pendiente: Capturas técnicas.

Material identificado: Capturas técnicas Ningún adjunto, script, plugin o comando del post fue ejecutado. La revisión actual puede incluir comentarios de octubre en publicaciones creadas hasta septiembre; no reconstruye una foto histórica de la discusión al 30 de septiembre.
