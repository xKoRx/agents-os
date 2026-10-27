---
type: "resource"
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - EAs D1 de SQX sin operaciones en MT5]]"]
last_verified: "2026-10-25"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-25"
updated: "2026-10-25"
source_url: "https://comunidad.imoxtrading.com/c/aportes-y-recursos/eas-d1-de-sqx-no-operaban-o-casi-en-el-tester-de-mt5-y-como-arreglarlo"
related: ["[[IMOX]]", "[[IMOX — Regularización histórica hasta septiembre 2026]]"]
---

# IMOX - EAs D1 de SQX sin operaciones en MT5

## Síntesis vigente

Caso D1 futuros Darwinex: señales a las 00:00 rechazadas Market closed; OpenBarDelay según sesión recupera coincidencia. Comprobar inputs persistidos del tester; un delay global de 60 puede inutilizar M15/H1 o desplazar forex. La recomendación OHLC M1 del autor está condicionada a su caso; no valida estrategias dependientes del recorrido intrabar.

## Comentarios y matices

Comentarios: en 22 EAs NDX CFD de Darwinex, otro miembro no ve pérdidas de señales Market closed con delay 0. Luis diferencia futuros y datos anteriores a 2025, y menciona TradeStation/RTH/continuos; distinguir continuo ajustado/no ajustado, sesión y reglas de precio. Estas experiencias no convierten una fuente de datos en superior para todo uso.

## Decisión y aplicación

Decisión: **útil**. Conocimiento o contexto útil integrado; resultados atribuidos, sin adopción automática de parámetros. Esta nota conserva investigación personal para [[IMOX]] y [[Estrategias IMOX — Forex y CFD con Echo Forge]]; no crea campañas, configura workers ni certifica resultados.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/aportes-y-recursos/eas-d1-de-sqx-no-operaban-o-casi-en-el-tester-de-mt5-y-como-arreglarlo).
- Fuente: [[IMOX - Fuente - EAs D1 de SQX sin operaciones en MT5]]. Texto accesible leído en Chrome autenticado el 2026-10-25; fecha visible de publicación `20 sept`. El año 2026 procede del contexto del lote, no de un timestamp nativo confirmado.
- Estado de procesamiento: `partial`. La lectura del cuerpo no implica haber revisado imágenes, vídeos o archivos.

## Pendientes y límites

Comentarios/respuestas completos sin certificar. Adjunto o material adicional pendiente: Tres capturas de diagnóstico.

Material identificado: Tres capturas de diagnóstico Ningún adjunto, script, plugin o comando del post fue ejecutado. La revisión actual puede incluir comentarios de octubre en publicaciones creadas hasta septiembre; no reconstruye una foto histórica de la discusión al 30 de septiembre.
