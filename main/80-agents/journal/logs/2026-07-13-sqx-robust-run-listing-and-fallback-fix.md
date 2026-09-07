---
type: change_log
topic: codebase
app: symphony
created: 2026-07-13
---

# Change Log: Corrección de Listado de Estrategias y Remoción de Fallbacks en Robust Run

## Cambios Realizados

1. **generic_workflow.go**:
   - Se modificó la tarea `"apply_selected_run"` en el flujo estándar y en `handleGroupTask` para que, cuando el batch actual esté vacío, liste de forma síncrona las estrategias desde la carpeta `SourceFolder` (`"03_optimizer"`), evitando omitir la tarea de forma silenciosa.

2. **robust_activity.go**:
   - Se removió por completo el bloque de fallback que realizaba búsquedas recursivas y de adivinación de nombres/directorios al descargar las estrategias de origen de MinIO. Ahora la descarga falla catastróficamente si el archivo no está en el `sourceKey` exacto determinado por `SourceFolder`.
   - Se inyectó `UploadPrefixFilter` (basado en el nombre de la estrategia sin extensión) para evitar que `UploadFromDisk` suba archivos acumulados en el directorio local de salida `output/robust/`.
   - Se agregó limpieza por `defer` de los archivos locales temporales creados por la actividad.

## Verificación

- Compilación exitosa del worker y pasaron todos los tests unitarios:
  `go test ./sqx/activities/worker/...`
- Todos los tests de workflows pasaron exitosamente:
  `go test ./sqx/workflows/...`
