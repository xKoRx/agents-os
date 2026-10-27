---
type: "resource"
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Monitor de estrategias Darwinex Demo con IA]]", "[[IMOX - Fuente adjunta - PDF Demo Monitor]]"]
last_verified: "2026-10-25"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-25"
updated: "2026-10-25"
source_url: "https://comunidad.imoxtrading.com/c/aportes-ia/como-construi-un-sistema-para-evaluar-automaticamente-estrategias-en-cuentas-darwinex-demo-con-chat-gpt-y-codex"
related: ["[[IMOX]]", "[[IMOX — Regularización histórica hasta septiembre 2026]]"]
---

# IMOX - Monitor de estrategias Darwinex Demo con IA

## Síntesis vigente

Monitor forward multicuenta mediante acceso inversor: historial MT5 → SQLite → métricas por comment → ventanas 90/60/30/7 días → score/evidencia → candidatas WFM → HTML/Excel. Separa monitoreo de selección/ejecución. Guía leída: el detalle está en la adenda y la normalización completa de Quality sigue sin especificarse; no sustituye identidad estable por asumir que comment siempre es único.

## Comentarios y matices

No se incorpora una conclusión de comentarios no leídos. La cobertura de comentarios permanece sin cerrar.

## Decisión y aplicación

Decisión: **útil**. Conocimiento o contexto útil integrado; resultados atribuidos, sin adopción automática de parámetros. Esta nota conserva investigación personal para [[IMOX]] y [[Estrategias IMOX — Forex y CFD con Echo Forge]]; no crea campañas, configura workers ni certifica resultados.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/aportes-ia/como-construi-un-sistema-para-evaluar-automaticamente-estrategias-en-cuentas-darwinex-demo-con-chat-gpt-y-codex).
- Fuente: [[IMOX - Fuente - Monitor de estrategias Darwinex Demo con IA]]. Texto accesible leído en Chrome autenticado el 2026-10-25; fecha visible de publicación `27 sept`. El año 2026 procede del contexto del lote, no de un timestamp nativo confirmado.
- Estado de procesamiento: `partial`. La lectura del cuerpo no implica haber revisado imágenes, vídeos o archivos.

## Pendientes y límites

Comentarios/respuestas completos sin certificar. Estado de adjuntos actualizado en las adendas de esta ficha; completar comentarios y material visual no certificado.

Material identificado: Guia-Demo-Monitor-con-ChatGPT-y-Codex.pdf Ningún adjunto, script, plugin o comando del post fue ejecutado. La revisión actual puede incluir comentarios de octubre en publicaciones creadas hasta septiembre; no reconstruye una foto histórica de la discusión al 30 de septiembre.

## Adenda de lectura del adjunto — 2026-10-25

Fuente: [[IMOX - Fuente adjunta - PDF Demo Monitor]]. Texto completo, 7 páginas. Identidades: cuenta=(servidor,login), deal=(cuenta,ticket), operaciones por POSITION_ID y estrategia por comment de apertura recuperado inequívocamente; UNKNOWN si no. Runs staging/atómicos, hashes estables, conflictos sin sobrescribir y Decimal para reconciliar. Métricas ALL/D90/D60/D30/D7 con as_of UTC. Evidence usa trades, días activos/calendario y recencia; score separa calidad y evidencia. Propone gates 90 días, 30 trades, Score60, Evidence70%, PF/RetDD1,5 y confirmación14d antes de WFM manual; son parámetros del autor, no adoptados. La composición exacta/normalización de Quality no queda completamente especificada: no basta para reproducir su score. Reporting consume cifras canónicas; delivery idempotente no reintenta estados ambiguos. No se implementó ni programó nada.
