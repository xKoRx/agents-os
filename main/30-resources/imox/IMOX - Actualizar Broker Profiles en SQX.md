---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Actualizar Broker Profiles en SQX]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/aportes-y-recursos/manten-actualizados-los-broker-profiles-en-sqx"
related: ["[[IMOX]]", "[[30-resources/applications/echo/echo-forge]]"]
---

# IMOX - Actualizar Broker Profiles en SQX

## Síntesis vigente

Actualizar instrumentos y sesiones con datos del broker real antes de confiar en los perfiles preinstalados de SQX.

## Conocimiento extraído

El post sitúa la función desde SQX 141 y describe este procedimiento:

1. Localizar `custom_indicators/BrokerProfileInstrumentsSessionsScripts/Update_SQX_Instruments_information` en la instalación de SQX.
2. Ejecutarlo como script en MT5 conectado al broker objetivo.
3. Genera dos XML: instrumentos y sesiones, únicamente de los símbolos mostrados en Market Watch.
4. Importar ambos en Data Manager → Broker Profiles de SQX.

Documentación enlazada por el autor: https://strategyquant.com/doc/strategyquant/broker-profiles/#getting-correct-instruments-sessions-from-broker. No se visitó fuera de Chrome ni se ejecutó el script.

## Comentarios y matices

El autor relata un cambio de mínimo de lote en CFDs AXI de 1 a 0,1. Otro miembro dice ajustar manualmente swap y comisión incluso usando el importador. No asumir que actualizar el profile incorpora todos los costes efectivos.

## Adjuntos y cobertura

Sin adjuntos de contenido adicional identificados.

## Interés para Forge

Prioridad de consulta: **Alta**. Contexto de Rodrigo: la metodología de [[30-resources/applications/echo/echo-forge|Forge]] se aprendió en [[IMOX]]; los building blocks son la base para generar estrategias nuevas y variadas. Esta ficha es evidencia de investigación, no una configuración aplicada ni una campaña ejecutada.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/aportes-y-recursos/manten-actualizados-los-broker-profiles-en-sqx).
- Autor: Pablo Meiriño Feijoo. Lectura directa del post desde Chrome autenticado: 2026-10-24.
- Fuente resoluble: [[IMOX - Fuente - Actualizar Broker Profiles en SQX]]. Los comentarios son testimonios u opiniones atribuidos, no validación independiente.

## Límites y contradicciones

Validar broker, servidor, ticker, sesiones, timezone, tamaño de contrato y costes de la campaña concreta. Los cambios reportados no son especificaciones vigentes garantizadas.
