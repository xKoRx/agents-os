---
type: agent_memory
scope: internal
created: "2026-07-12"
updated: 2026-09-09
index_priority: never
memory_state: archived
load_policy: manual
indexable: false
tags:
  - kind/agent-memory
  - scope/internal
---

# Análisis de Redundancia y Subflujos Paralelos en Tareas Group de Echo Forge

## Contexto y Síntoma
En una ejecución de prueba con la configuración `NDX H1 L v17`, se generaron cerca de 50 estrategias en la tarea de Builder. Posteriormente, se crearon aproximadamente 90 subflujos (actividades de proyectos en subworkflows), lo cual resultó en una carga excesiva e ineficiente.

## Diagnóstico Técnico
1. **Granularidad de Firmas Lógicas**:
   Las ~50 estrategias generadas por el builder poseen firmas lógicas únicas basadas en `BuildSignature(entry, price, exit)`. Al agruparlas en `ClassifyAndRank`, resultaron cerca de 45-50 tipos lógicos distintos.

2. **Paralelismo Sin Concurrencia Limitada**:
   En `generic_workflow.go#handleGroupTask`, cuando la tarea es de tipo `group` y su `Source` es de tipo `ranking` sin un `logical_type` específico, el motor inicia el procesamiento por tipo lógico disparando goroutines con `workflow.Go` en paralelo para **todos** los tipos lógicos cargados:
   ```go
   for _, logicalType := range logicalTypes {
       workflow.Go(ctx, func(ctx workflow.Context) { ... })
   }
   ```
   Esto provocó que se levantaran ~45 goroutines en paralelo.

3. **Subflujos Paralelos vs. Tareas Internas**:
   - Cada uno de los 45 subworkflows (`GroupSQXWorkflow`) corre de forma **paralela** respecto a los otros subworkflows.
   - Dentro de cada subworkflow, las subtasks (`02_retester` y `03_optimizer`) sí se ejecutan de manera **secuencial** (esperando con `.Get(ctx, &resp)` la finalización de una antes de iniciar la siguiente).
   - Por ende, a nivel del Worker de Temporal, en un momento dado se ejecutan hasta 45 actividades `project` en paralelo (una por subworkflow activo), lo cual satura los recursos del servidor.

4. **Omisión de `pool_max` y `target_tops`**:
   - `pool_max` y `target_tops` no limitan la cantidad de tipos lógicos a procesar ni detienen dinámicamente los subflujos en paralelo cuando el objetivo global ya se cumplió.

## Estrategia de Corrección (Secuencialización de Subflujos)
Para corregir esto y asegurar que los subworkflows se procesen de forma estrictamente secuencial (uno a la vez), se debe eliminar el paralelismo de goroutines a nivel de tipos lógicos en `generic_workflow.go`:

1. **Eliminar `workflow.Go` y `typeResultChan`**:
   Procesar el bucle `for _, logicalType := range logicalTypes` de forma directa y secuencial.
2. **Ejecutar Child Workflow de forma Síncrona**:
   Llamar a `workflow.ExecuteChildWorkflow(...).Get(ctx, &childOut)` dentro del bucle principal de tipos lógicos. Esto garantiza que no se inicie el subworkflow del siguiente tipo lógico hasta que el actual haya terminado de procesar todas sus subtareas secuenciales.
3. **Propagar Early Exit global**:
   Al correr secuencialmente, se puede evaluar la cantidad acumulada de estrategias validadas contra `target_tops` al final de cada subworkflow, permitiendo un `break` temprano de todo el procesamiento del grupo si ya se tienen los finalistas requeridos.
