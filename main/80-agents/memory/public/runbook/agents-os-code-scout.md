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
  - code-scout-runbook
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

# Code Scout — exploración técnica y regresiones

## Propósito

Ejecutar `agents-os-code-scout` sin diseñar ni mutar el sistema observado. `80-agents/skills/_shared/scout-contract.md` posee dispatch, permisos, feedback y mantenimiento; este runbook posee los pasos de inspección del código.

## Precondiciones

Repo/scope autorizados, pregunta concreta y `dispatch_id`; herramientas de lectura/búsqueda permitidas. Un nombre de host, un path local o un checkout no demuestran qué binario corre en producción.

## Procedimiento

1. Identificar repo/ref/commit y cambios locales visibles con operaciones de lectura autorizadas. No hacer pull, checkout, reset o limpieza para facilitar la inspección. Si el principal entregó evidencias actuales suficientes, reutilizarlas.
2. Leer instrucciones aplicables al scope y localizar documentación/ADRs, manifests y símbolos por búsqueda. No adivinar secuencias de nombres de archivo ni leer miles de líneas para compensar una herramienta denegada.
3. Consultar el grafo de código existente mediante su interfaz comprobada. Sin grafo o con revisión desconocida, usar búsqueda/símbolos y declarar el límite. No invocar `graphify-obsidian` sobre un repo como sustituto automático de un índice de código.
4. Abrir fragmentos relevantes con callers/callees hasta entender los límites de responsabilidad. Si el resultado está cortado, completar rangos necesarios. No afirmar cobertura de archivos no recibidos.
5. Contrastar docs/rules con el código. Etiquetar cada patrón como observado con símbolo y evidencia, declarado con documento, o inferido y pendiente. Registrar drift sin proponer solución.
6. Inspeccionar estáticamente tests y herramientas relacionados: TestMain/setup/teardown, rutas de escritura, lectura de datasets reales, red, credenciales, subprocesses y hooks. Mostrar riesgos y verificaciones ausentes; no ejecutar para «ver qué pasa».
7. Congelar mapa técnico; persistir feedback y ejecutar sólo mantenimiento propio admitido por el contrato compartido; retornar al principal.

## Validación

- Positivo: describir el flujo y contratos de un módulo Go con paths/símbolos; explicar qué patrón existe con evidencia, no cómo debería rediseñarse.
- Negativo: «implementa este cambio» no autoriza implementación al scout; devuelve frontera y contexto disponible al principal.
- Adyacente: decisiones/continuidad del vault se solicitan al principal para Context Scout; no se crean otros subagentes.
- Regresiones: docs desactualizados frente a código; grafo stale; checkout dirty; binario diferente al source; test que sobrescribe evidencia sellada aunque antes salió verde; ausencia de búsqueda por símbolo; permiso denegado.
- Debe quedar explícito qué se inspeccionó y qué no se ejecutó. Feedback siempre; cambio de instrucciones sólo con hallazgo propio reproducible y gate de authoring válido.

## Rollback / recuperación

Sin lectura suficiente, retornar PARTIAL/BLOCKED con la primitiva y rango necesarios. No evadir denegaciones ni rebajar la prueba exigida. Un defecto del repo o de su documentación es un hallazgo para el principal, no una edición del scout. Ante conflicto en mantenimiento propio, conservar ambas evidencias y diferir; nunca sobrescribir a otro agente.

## Evidencia

Repo + ref/commit/dirty conocidos; path + símbolo/rango por hecho; estado del grafo; docs frente a código; mapa de efectos laterales; gaps; recibo de feedback; mantenimiento propio y validación realizada. Una inspección estática no certifica ejecución ni seguridad completa.
