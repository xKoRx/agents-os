---
type: resource
schema_version: 1
status: active
area: '[[Trading]]'
sources:
- '[[IMOX - Fuente - Claude en CustomProjects para analizar databanks]]'
last_verified: '2026-10-24'
confidence: verified
aliases: []
tags:
- kind/resource
- area/trading
- topic/imox
created: '2026-10-24'
updated: '2026-10-26'
source_url: https://comunidad.imoxtrading.com/c/aportes-y-recursos/como-estoy-usando-claude-dentro-de-mis-customprojects-de-sqx-para-analizar-los-databanks
related:
- '[[IMOX]]'
- '[[30-resources/applications/echo/echo-forge]]'
---

# IMOX - Claude en CustomProjects para analizar databanks

## Síntesis vigente

Embudo automatizado entre Build y robustez: exportación Java, análisis Python/Claude Code y movimiento mediante snippet Java. La IA propone; un validador determinista decide si el resultado es aceptable para mover estrategias.

## Conocimiento extraído

1. **ExportForClaude:** CustomAnalysis recorre el databank y exporta trades y P/L IS/OOS, agregados anuales IS y mensuales OOS; no modifica el banco.
2. **Script externo:** `.bat` → Python valida proyecto/banco, sesión de Claude Code y métricas MCP; invoca `claude -p` con esquema JSON.
3. **Contrato:** un SELECT/BACKUP/REJECT por estrategia, score, evaluación IS, OOS, degradación y motivo.
4. **Validación:** nombres existentes, mínimo de trades OOS y cobertura de todos los candidatos. Si falla algo, no se mueve nada.
5. **MoveSelected:** snippet Java consume `selection.json`, mueve las elegidas y escribe resumen al log antes de MC1/MC2.
6. **Evidencia:** carpeta exchange con entrada exacta, respuesta cruda, reporte y copia por ejecución.

Fricciones declaradas: el MCP de su SQX 144 expone columnas pero no trades/equity ni movimiento; `rg.orders()` incluía trades de crosschecks HBP y requirió filtrado; con 100 estrategias el modelo a veces evaluaba solo unas 30; salida abundante sin consumir podía bloquear el script; la API HTTP interna de movimiento no le funcionaba con el proyecto en ejecución.

Costes, nombres de modelo y volúmenes de tokens del post son reportes del autor, no verificación de tarifas o disponibilidad actual. No se configura ninguna cuenta de IA en esta ingesta.

## Comentarios y matices

Jose retiró una descorrelación temprana que dejaba 1–5 de 100; las variantes de una hipótesis son naturalmente parecidas. Asier propone reducir las cientos de candidatas antes de MC por coste. Jose advierte que la de mejor curva puede no ser la robusta: descartar sus compañeras demasiado pronto puede dejar cero supervivientes. No hay consenso ni ensayo controlado que resuelva el intercambio entre coste y falso descarte.

## Adjuntos y cobertura

Cuerpo, nueve comentarios y captura del flujo revisados. Imagen confirma Build → ExportForClaude → run_analysis.bat → MoveSelected → Builder_PASSED/robustez.

## Interés para Forge

Prioridad de consulta: **Alta**. Contexto de Rodrigo: la metodología de [[30-resources/applications/echo/echo-forge|Forge]] se aprendió en [[IMOX]]; los building blocks son la base para generar estrategias nuevas y variadas. Esta ficha es evidencia de investigación, no una configuración aplicada ni una campaña ejecutada.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/aportes-y-recursos/como-estoy-usando-claude-dentro-de-mis-customprojects-de-sqx-para-analizar-los-databanks).
- Autor: Jose2ms. Lectura directa del post desde Chrome autenticado: 2026-10-24.
- Fuente resoluble: [[IMOX - Fuente - Claude en CustomProjects para analizar databanks]]. Los comentarios son testimonios u opiniones atribuidos, no validación independiente.

## Límites y contradicciones

La decisión de una IA no prueba edge. Si OOS alimenta el selector y las iteraciones, ya no es una evaluación independiente del proceso. No se compartió aquí un paquete implementable auditado.

## Delta observado el 2026-10-26

Relectura de cuerpo y nueve comentarios anunciados. Se mantiene el desacuerdo sobre correlación temprana y coste de MC1/MC2: puede ahorrar cómputo y también eliminar una variante que después resultaría más robusta. Los tiempos/cantidades de miembros siguen siendo experimentos personales. La revisita textual no renueva la verificación de todos los materiales previos.
