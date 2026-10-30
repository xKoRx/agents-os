---
type: runbook
schema_version: 1
scope: global
created: '2026-10-30'
updated: '2026-10-30'
entities:
  - '[[AGENTS OS]]'
related: []
aliases:
  - context-scout-runbook
confidence: high
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/global
  - tech/agents-os
  - action/context-retrieval
---

# Context Scout — ejecución y regresiones

## Propósito

Ejecutar `agents-os-context-scout` con evidencia recuperable, feedback idempotente y mejora acotada. La recuperación es propiedad de `80-agents/skills/agents-os-context-retrieval/SKILL.md`; dispatch y mantenimiento pertenecen a `80-agents/skills/_shared/scout-contract.md`.

## Precondiciones

Mandato con `dispatch_id`, pregunta y scope; base vigente cargada por bootstrap; límites de escritura del contrato compartido reconocidos. Si sólo hay lectura, preparar feedback para persistencia por el principal, no fingir que se guardó.

## Procedimiento

1. Registrar revisiones conocidas y comprobar el inventario mínimo de fuentes recibido. Validar vigencia de la pieza requerida, no del vault entero.
2. Seleccionar por metadata/índice/grafo según la intención; ejecutar la query canónica vigente. Si es una pregunta de continuidad, localizar primero el bloque activo y la bitácora relacionada, no todo el histórico.
3. Abrir las secciones seleccionadas. Registrar el rango realmente recibido; ante truncado, continuar por ventanas pequeñas hasta cubrir la sección requerida. Si está denegado, retornar el gap preciso, sin variantes de evasión.
4. Marcar procedencia y autoridad de cada hecho. Resolver aliases hacia la entidad canónica; distinguir material activo, archivado y rectificado. Rechazar ruido de templates o journals no solicitados.
5. Congelar el pack de esta invocación y aplicar feedback/mantenimiento del contrato compartido. Conservar su `dispatch_id` ante retry. Una falla de persistencia no dispara otra recuperación.
6. Retornar sin dumps: hechos condicionantes, fuentes, gaps, feedback y mantenimiento. El principal sólo necesita abrir evidencia crítica o un gap nuevo.

## Validación

- Positivo: una pregunta sobre decisiones vigentes y restricciones de un proyecto debe devolver fuentes seleccionadas y sus rangos, sin actualizar el proyecto.
- Negativo: saludo o pregunta general sin entidad no dispara el scout; dato exacto ya identificado puede resolverse determinísticamente.
- Adyacente: una pregunta sobre implementación de una interfaz Go se deriva por el principal a Code Scout, sin exploración duplicada.
- Regresiones: bitácora vigente contradice diagnóstico antiguo; índice vacío pero Markdown existente; respuesta truncada; pack vigente reutilizable; quota/herramienta denegada; fuente corregida después de un reporte positivo.
- Cada invocación produce feedback persistido o `pending` explícito; una corrida limpia registra `NO_FINDING` sin editar instrucciones. Métricas no observadas permanecen `unknown`.

## Rollback / recuperación

Ante fuente stale, reemplazar sólo el delta del pack; ante herramienta no disponible, usar fallback canónico. Si una mejora propia no supera validación, revertir únicamente ese delta y reportar `deferred`; no tocar entidades ni los cambios ajenos. Aplicar controles de publicación/lectura posterior del contrato compartido.

## Evidencia

Fuente + sección/rango + revisión cuando disponible; consulta y modo usados; indicador de truncado; gap y causa; recibo de feedback; paths propios modificados y resultados reales de validación si hubo mejora. No guardar cadenas de pensamiento, secretos ni un transcript de búsqueda.
