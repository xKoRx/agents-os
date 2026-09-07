---
type: skill
schema_version: 1
name: readonly-production-probe
description: Crea y ejecuta probes temporales read-only para inspeccionar sistemas reales (producción o staging) sin modificar estado ni inventar canales; usar ante "necesito ver qué hay en producción", inspección de DB/cola/object store/workflow engine, o diagnóstico que requiera datos físicos del runtime.
scope: global
created: "2026-08-29"
updated: "2026-08-29"
entities: []
related:
  - "[[symphony-prod-probe]]"
  - "[[evidence-channel-discovery]]"
aliases:
  - probe read-only
  - inspección de producción
  - herramienta de diagnóstico temporal
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - tech/go
  - action/diagnose
---

# readonly-production-probe

## Purpose

Obtener evidencia física de sistemas reales de forma segura y reproducible, sin hardcodear secretos, sin contaminar el repositorio y sin confundir código de diagnóstico con código producto. El patrón canónico: bootstrap real → dependencias selectivas → queries/describe/inspect → evidencia estructurada → cleanup.

## Minimal Read

Read only:
1. El runbook del sistema para el patrón concreto (ej. [[symphony-prod-probe]]).

## Procedure

1. Resolver acceso por la configuración real de la aplicación (DI/config existente), nunca por credenciales hardcodeadas ni copiadas a archivos nuevos; si el bootstrap de la app ya lee secretos de su fuente (etcd/env/vault), reutilizarlo.
2. Escribir el probe dentro del módulo/servicio objetivo cuando necesite importar paquetes `internal/` (los lenguajes lo exigen); ubicación de diagnóstico claramente marcada como no-producto en el encabezado.
3. Implementar sólo operaciones de lectura: GET/Stat/List/describe/SELECT; subcomandos por pregunta (salud, colas, workflows, objetos, filas); salida estructurada con IDs y hashes; enmascarar secretos en la salida.
4. Compilar y ejecutar; capturar la evidencia needed; iterar sobre el mismo archivo en vez de acumular herramientas.
5. Cleanup obligatorio: eliminar el probe al cierre de la sesión y verificar que el worktree queda sólo con el dirty preexistente; la evidencia persiste en notas, no en el repo.

## Output

```text
<probe> <modo> → <hechos estructurados: IDs, estados, hashes, timestamps>
CLEANUP: probe eliminado; worktree = dirty preexistente únicamente
```

## Hard Rules

- Read-only por diseño: ninguna operación de escritura, delete, update ni comandos de mutación, ni siquiera "para probar".
- Sin secretos en el código ni en la salida del probe; nada persiste credenciales.
- El probe es efímero: se crea para la sesión y se elimina al cierre; jamás se commitea como producto.
- Si el sistema ofrece un CLI/API oficial de observación, preferirlo antes que escribir un probe.
