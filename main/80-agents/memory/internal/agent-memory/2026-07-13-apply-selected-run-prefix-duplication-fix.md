---
type: agent_memory
scope: internal
created: 2026-07-13
updated: 2026-07-13
tags:
  - kind/agent_memory
  - tech/go
  - app/symphony
  - topic/workflow
  - topic/testing
---

# Continuidad Operativa: Corrección de Duplicación de Prefijo en apply_selected_run

## Diagnóstico y Causa Raíz
Se diagnosticó el fallo en la etapa `apply_selected_run` de la ejecución v27 del pipeline de Symphony.
- **Causa Raíz:** Al remover los fallbacks de descarga dinámicos en una actualización previa (donde si la descarga del `sourceKey` exacto falla, se produce un error catastrófico inmediato), quedó al descubierto un bug en la construcción del `sourceFileName` en `robust_activity.go`.
- El campo `base` (que almacena `selectedRun.StrategyID`, derivado del archivo listado por `list_strats`) ya contiene la convención de nomenclatura estructurada (`[Instrument]_[Direction]_[Timeframe]_[StrategyName]_[Version]_[ID]`).
- La actividad reconstruía el nombre concatenando de forma incondicional estos mismos parámetros una vez más, produciendo una clave duplicada con doble prefijo en MinIO (ej. `EURUSD_L_H1_stratname_v1_EURUSD_L_H1_stratName_v1_someID.sqx`). Al no existir tal archivo, la descarga fallaba con un error 404.

## Solución Aplicada
1. En `robust_activity.go` (método `Execute` de `ApplySelectedRunActivity`), se implementó una validación para verificar si `selectedRun.StrategyID` contiene los componentes del prefijo (instrumento y timeframe).
   - Si los contiene (`containsConvention`), se utiliza directamente `base + ".sqx"` como nombre de archivo origen.
   - Si no los contiene (caso de tests unitarios con IDs cortos como `"S1"`), se mantiene la concatenación anterior por compatibilidad.
2. En `robust_activity_test.go`, se extendió el `mockStorage` con un callback `onDownload` para interceptar la clave y validar que no contenga el prefijo duplicado.
3. Se añadió el test unitario `TestApplySelectedRunActivity_Execute_WithConvention` que valida exitosamente este comportamiento.
