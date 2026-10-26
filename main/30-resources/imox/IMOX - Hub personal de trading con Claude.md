---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Hub personal de trading con Claude]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/plugins-627f40/mi-hub-de-trading-personal-hecho-con-claude-y-a-mi-medida"
related: ["[[IMOX]]", "[[30-resources/applications/echo/echo-forge]]"]
---

# IMOX - Hub personal de trading con Claude

## Síntesis vigente

App privada para centralizar cuentas y EAs, alimentada por un EA reportero y ficheros sincronizados. Complementa el catálogo de minados del primer post de la biblioteca.

## Conocimiento extraído

### Tres piezas

1. VPS Windows con EA reportera MT4/MT5 que no opera: escribe el historial.
2. Sincronización a Drive mediante app de escritorio o rclone/tarea programada, según Windows.
3. App privada que lee esos archivos con el conector y sesión de Claude.

### Tres vistas

- Cuentas propias, challenges, fondeadas y Darwins: neto, retorno, DD, Ret/DD, PF, winrate, equity y restricciones de props.
- Demos: separar EAs por magic, clasificar por activo/familia/timeframe y estado demo→real; comparar curvas y resultados en R para controlar diferencias de lotaje.
- Portfolios: selección incremental que mejora Ret/DD con límites por número, activo, timeframe, correlación, operaciones y DD. Configura R por EA y simula retos con reglas del destino. Incluye avisos de señal repetida y riesgo por operación.

Es descripción de una herramienta personal, no producto entregado ni algoritmo de selección auditado.

## Comentarios y matices

Xavi propone comparar demo con backtest y alertar por inactividad fuera de lo normal; Miguel comprueba que una semana sin operar sí cabía en el historial. David recuerda que construir EAs variadas es prioritario frente a gastar todo el esfuerzo en herramientas. Víctor añade servidores, calendario de noticias restringidas, mapa visual de familias por activo y finanzas/gastos. Un problema de lectura Drive se reporta resuelto sin detalle técnico reproducible. Las capturas adicionales del autor se declaran dummy.

## Adjuntos y cobertura

Cuerpo y 24 comentarios accesibles revisados. Una imagen principal y tres capturas dummy en comentarios identificadas; capacidades extraídas del texto. No hay repositorio o paquete implementable compartido.

## Interés para Forge

Prioridad de consulta: **Media**. Contexto de Rodrigo: la metodología de [[30-resources/applications/echo/echo-forge|Forge]] se aprendió en [[IMOX]]; los building blocks son la base para generar estrategias nuevas y variadas. Esta ficha es evidencia de investigación, no una configuración aplicada ni una campaña ejecutada.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/plugins-627f40/mi-hub-de-trading-personal-hecho-con-claude-y-a-mi-medida).
- Autor: Guillem Tarin Arque. Lectura directa del post desde Chrome autenticado: 2026-10-24.
- Fuente resoluble: [[IMOX - Fuente - Hub personal de trading con Claude]]. Los comentarios son testimonios u opiniones atribuidos, no validación independiente.

## Límites y contradicciones

No se probaron privacidad, autenticación, sincronización, identidad ni simulador. Los límites numéricos y alertas descritos no se adoptan como reglas de riesgo de Rodrigo.
