---
type: resource
schema_version: 1
status: "active"
area: "[[Trading]]"
sources: ["[[IMOX - Fuente - Building Blocks Skill]]"]
last_verified: "2026-10-24"
confidence: "verified"
aliases: []
tags: ["kind/resource", "area/trading", "topic/imox"]
created: "2026-10-24"
updated: "2026-10-24"
source_url: "https://comunidad.imoxtrading.com/c/aportes-ia/building-blocks-skill"
related: ["[[IMOX]]", "[[30-resources/applications/echo/echo-forge]]"]
---

# IMOX - Building Blocks Skill

## Síntesis vigente

Procedimiento para crear una skill que propone bloques por activo, temporalidad, dirección y familia, y entrega un `.sqb` importable con explicación. Es el post que Rodrigo buscaba sobre agentes para seleccionar bloques.

## Conocimiento extraído

### Entradas y contrato de salida

- Exportar desde la instalación objetivo un `.sqb` con todos los bloques activados y declarar la versión de SQX.
- Usar ese archivo como plantilla estructural y lista cerrada de bloques permitidos: el agente no debe inventar IDs que el SQX del usuario no conoce.
- Pedir selección según activo, timeframe, dirección y tipo de estrategia. Los ejemplos Oro H1 long breakout y NQ H1 long mean reversion son ilustrativos.
- Solicitar archivo importable y justificación de cada bloque; pedir instrucciones de instalación de la skill para reutilizarla.

### Validación e iteración

1. Importar el `.sqb` generado en SQX.
2. Comprobar ausencia de errores y coherencia de la selección.
3. Corregir en la skill la causa de los fallos, no solo el archivo individual.
4. Registrar configuraciones previas para evitar repetición, pedir tres variantes y opcionalmente un informe explicativo.
5. Evaluar con criterio propio; el autor está intentando builds cortos para descartar configuraciones inviables antes de gastar horas.

**No se entrega una skill lista para instalar:** el post enseña a crearla. Que el texto mencione `skill-creator` no autoriza a instalar o ejecutar nada en este trabajo.

## Comentarios y matices

Carlos aclara que no entrenó la skill con fórmulas y utilidad de cada indicador: se apoya en conocimiento previo del modelo. Excluyó indicadores nuevos de v144 como Volume Profile por reportes de bugs; es una decisión de su contexto, no una regla universal. Iván describe skills por activo/timeframe que generan template y resumen de What to build, Genetic, Ranking y Retest, con exigencias ajustadas. Otro miembro reporta pruebas BTC short H1; no aporta validación estadística. La discusión registra un reporte de ejemplo para documentar el minado.

## Adjuntos y cobertura

Revisado cuerpo y 16 comentarios accesibles. Reporte de ejemplo enlazado: https://academia.imoxtrading.com/documento/lo_IwxVee6I1. Su contenido completo se registra solo si se consigue descargar y revisar.

## Interés para Forge

Prioridad de consulta: **Muy alta**. Contexto de Rodrigo: la metodología de [[30-resources/applications/echo/echo-forge|Forge]] se aprendió en [[IMOX]]; los building blocks son la base para generar estrategias nuevas y variadas. Esta ficha es evidencia de investigación, no una configuración aplicada ni una campaña ejecutada.

## Evidencia y provenance

- [Publicación original de Circle](https://comunidad.imoxtrading.com/c/aportes-ia/building-blocks-skill).
- Autor: Carlos K. Lectura directa del post desde Chrome autenticado: 2026-10-24.
- Fuente resoluble: [[IMOX - Fuente - Building Blocks Skill]]. Los comentarios son testimonios u opiniones atribuidos, no validación independiente.

## Límites y contradicciones

La selección generada necesita verificación semántica y técnica. La guía 145 explica que un `.sqb` por sí solo no fija el signo nivel ± margen de órdenes pendientes; para imponer la hipótesis completa puede requerirse una plantilla. No hay evidencia de que estas propuestas mejoren out of sample frente a una alternativa controlada.
