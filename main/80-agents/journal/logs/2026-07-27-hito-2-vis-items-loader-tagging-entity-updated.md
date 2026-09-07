---
type: change_log
scope: session
created: "2026-07-27"
updated: "2026-07-27"
area: "[[Meli]]"
project: "[[Implementación Hito 2 - Destaques de Precio]]"
application: "[[vis-items-loader-tagging]]"
entities:
  - "[[Hito 2 - vis-items-loader-tagging]]"
related:
  - "[[Bajó de Precio]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/meli
  - app/vis-items-loader-tagging
---

# Hito 2 vis-items-loader-tagging — processor estándar y rollout

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Destaques de Precio/agentes/Hito 2 - vis-items-loader-tagging.md`
  - `10-projects/Destaques de Precio/Implementación Hito 2 - Destaques de Precio.md`

## Motivo

- El owner rechazó la abstracción `signals` y pidió reutilizar las capabilities
  existentes para salir rápido.

## Fuentes usadas

- Decisión explícita del owner del 2026-07-27.
- HEAD `fbb1bbf0` de `vis-items-loader-tagging`.
- `pkg/models/process.go`: contrato `models.Processor`.
- `pkg/middlewares/filter.go`: selección por `process:<ID>`.
- `pkg/orchestrator/orchestrator.go`: `ItemModificable` compartido y un único
  `PutItem`.
- `cmd/api/initializers/resources.go`: registro simultáneo de processors e
  instancias Motors/Real Estate de `PriceBeforeDiscount`.

## Resolución aplicada

- Se reemplazó el coordinador/signals por
  `vehicle_price_highlight_motors`, una implementación estándar de
  `models.Processor`.
- El processor nuevo ejecuta siempre Bajó de Precio y Destaque de Precio y
  delega responsabilidades en services/helpers acotados.
- Se definió rollout en dos despliegues:
  1. convivencia y drenaje de `price_before_discount_motors`;
  2. retiro exclusivo de la instancia/configuración Motors antigua.
- Se protegió explícitamente el processor genérico `price_before_discount` y
  su instancia Real Estate.
- Se marcó VMDEM-27 para actualización antes de aprobación.

## Validación

- `validate_plan.py`: 3 fases, 3 gates, 3 despachos, 11 referencias locales,
  0 errores y 0 warnings.
- Búsqueda focalizada sin referencias residuales a `MotorsPricingSignals`,
  `PriceDropEvaluator` ni `VehiclePriceHighlightEvaluator`.
- Graphify reindexado; `explain` resolvió el nodo canónico y sus secciones de
  arquitectura, decisiones, gates y rollout.
- Working tree de la aplicación preservado; no se modificó código ni archivos
  no versionados del usuario.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni datos de ítems.

## Rollback

- Revertir las dos notas de proyecto y restaurar la decisión arquitectónica
  previa; no hay cambios de código que revertir.
