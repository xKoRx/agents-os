---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Guía SQX 144 - Conocimiento de Telegram]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/aportes-y-recursos/guia-sqx-v144-todo-lo-valioso-del-grupo-de-telegram-en-un-solo-pdf"
related: ["[[IMOX]]", "[[30-resources/applications/echo/echo-forge]]"]
---

# IMOX - Guía SQX 144 - Conocimiento de Telegram

## Síntesis vigente

Recopilación de conocimiento comunitario sobre transición 136→144: motor, instrumentos, ATR, IA, familias y errores de construcción.

## Conocimiento extraído

El post anuncia:

- Diferencias de motor y resultados entre versiones; las cifras de estrategias generadas son experiencias de la guía, no benchmark reproducido.
- El ajuste histórico de multiplicar el periodo ATR por diez ya no se aplicaría en 144, según el autor.
- Datos Darwinex integrados y Broker Profiles; advierte comprobar tipo de instrumento en lugar de asumir CFD.
- Configuración del MCP y flujos con IA, con atención a permisos.
- Familias por lógica, activo, dirección y timeframe; embudo de exploración y explotación.
- FAQ y bugs de Builder, Retester, Optimizer y MQL5.

No asumir que migrar una EA conserva métricas: revisar motor, sesiones y timezone.

## Comentarios y matices

Los comentarios accesibles agradecen consolidar material difícil de recuperar de Telegram y lo usan como contexto para IA. No añaden una matriz verificada de bugs resueltos ni validación de cifras. El total anunciado por Circle puede diferir de lo cargado en pantalla; no se certifica exhaustividad de las 32 entradas.

## Contraste con la guía descargada

Se leyó la versión v2 de `GUIA_SQX144_IA.pdf`, doce páginas, con foco en §§2.4, 3, 4.5 y coherencia interna.

- **Cuatro ejes de familia:** lógica, activo, dirección y temporalidad. Para una campaña, especificar además orden y salidas, como precisa la guía 145.
- **Exploración/explotación:** generar variedad, retestear, optimizar con estabilidad y verificar en MT5; solo después explorar más en bloques asociados a supervivientes. Los datos usados para adaptar una generación pasan a ser datos de selección.
- **Conflicto explícito:** §3.2 propone todos los bloques en exploración; la adenda §4.5 recomienda separar por familia y no activar todos. La propia guía reconoce la diferencia y permite adoptar builders por familia. No hay una única receta canónica para copiar sin decidir el experimento.
- **Otra inconsistencia:** §1.1 dice que casi todo lo generado en 144 sobrevive al retester, pero el ejemplo inmediato afirma descartes de 90–100 % en 142/144 y 20–30 % en 136. Las condiciones no resuelven esa tensión: no usar esas tasas como expectativa.
- La adenda recomienda filtros iniciales flexibles, menos generaciones y umbrales de Ret/DD menos restrictivos. Sus ejemplos (15 frente a 40 generaciones, Ret/DD 5 frente a 9) no son parámetros aprobados para Forge ni resultados transferibles sin medir.
- La guía propone preservar exportaciones, controlar costes y comprobar concordancia SQX/MT5. Sus tiempos, timezone, compatibilidades y coeficientes de riesgo se tratan como información dependiente de versión/broker.

Las afirmaciones generales sobre permisos de MCP y modificaciones automáticas no sustituyen el contrato de herramientas real de Forge. No se instalaron conectores ni se cambió SQX.

## Adjuntos y cobertura

Post y comentarios accesibles revisados. PDF: https://academia.imoxtrading.com/documento/SWJm82jARbUt. PDF recibido, 12 páginas; revisión local autorizada y verificación visual de páginas seleccionadas.

## Interés para Forge

Prioridad de consulta: **Alta**. Contexto de Rodrigo: la metodología de [[30-resources/applications/echo/echo-forge|Forge]] se aprendió en [[IMOX]]; los building blocks son la base para generar estrategias nuevas y variadas. Esta ficha es evidencia de investigación, no una configuración aplicada ni una campaña ejecutada.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/aportes-y-recursos/guia-sqx-v144-todo-lo-valioso-del-grupo-de-telegram-en-un-solo-pdf).
- Autor: Oscarrené Duarte Hernández. Lectura directa del post desde Chrome autenticado: 2026-10-24.
- Fuente resoluble: [[IMOX - Fuente - Guía SQX 144 - Conocimiento de Telegram]]. Los comentarios son testimonios u opiniones atribuidos, no validación independiente.

## Límites y contradicciones

Fuente secundaria comunitaria. Las reglas de versión y errores deben contrastarse con el build concreto antes de automatizarlas. El resumen del post no sustituye el PDF.
