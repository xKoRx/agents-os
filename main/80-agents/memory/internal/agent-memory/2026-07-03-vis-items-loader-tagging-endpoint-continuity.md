---
type: agent_memory
scope: internal
created: "2026-07-03"
updated: 2026-09-09
index_priority: never
memory_state: archived
entities:
  - "[[Bajó de Precio]]"
  - "[[vis-items-loader-tagging]]"
confidence: high
load_policy: manual
indexable: false
tags:
  - agent/internal
  - area/meli
---

# 2026-07-03 - vis-items-loader-tagging endpoint continuity

Si un futuro agente retoma una pregunta sobre Previous Price Motors en `vis-items-loader-tagging`, el punto clave es este:

- Estado vigente 2026-07-23: `/consume-price-discount-motors` fue eliminado; la entrada debe resolverse mediante template processing.
- El proceso `price_before_discount_motors` y sus filtros siguen vigentes para `/consume-process-item`; no eliminar la configuración Motors junto con el endpoint.
- También se eliminó el override de factory que seleccionaba un tópico alternativo cuando el scope era test; `GetPublisher` y `GetScheduledPublisher` vuelven a resolver solo el env var recibido.
- El payload histórico directo del endpoint eliminado usaba `msg.item_id`, `msg.seller_id` y `msg.category_id` (snake_case); el payload de `/consume-process-item` usa `msg.id`, `msg.sellerId`, `msg.categoryId`, `msg.headers` y `filters.modified_fields` (camelCase en `msg`).
- El pipeline reutilizado sigue siendo `/consume-process-item` + `ProcessorFilter` + `PriceBeforeDiscount` instanciado con config Motors.
- No conviene presentar esto como "se duplicó endpoint por capricho": la separación evita contaminar `price_before_discount` Real Estate con thresholds, dominio y vertical Motors.
- Fuentes históricas: `PRICE_DROP_MOTORS.md`, `pkg/handlers/price_discount*_handler.go`, `cmd/api/initializers/router.go`, `cmd/api/initializers/resources.go`, `pkg/middlewares/filter.go`.

Para B2C/MC, separar los roles: `/consume-user` ejecuta `B2CUser` y `B2CHighlight`. Si falta `IS_FINANCEABLE_VEHICLE_RISK_PROFILE`, `B2CUser` solo publica al topic de `vis-credits-consumer` cuando el seller tiene `accepts_secured_loans`, el item está verificado y ya existe `VEHICLE_RISK_PROFILE_IDENTIFIER`; el credits consumer consulta Segments Wrapper y persiste `IS_FINANCEABLE`, `FINANCEABLE_BY` y, para `MLB-CARS_AND_VANS`, `IS_FINANCEABLE_VEHICLE_RISK_PROFILE`. Si aún no existe el identificador PRV, el mismo `/consume-user` publica `process:vehicle_risk_profile` al topic interno para crear primero la PRV. `/consume-process-item` con `update_listing_type` es un paso posterior y no resuelve la ausencia inicial del sale term.

El repositorio `vis-credits-consumer` quedó registrado como aplicación canónica en el Vault; su endpoint operativo para recalcular sale terms es `POST /vis-credits-consumer/item-financeable`, mientras `item-filter` decide qué ítems encolar.

Para regularizaciones masivas, el endpoint acepta el payload mínimo `{\"msg\":{\"id\":\"MLB...\"}}`; el script operativo debe limitarse a una request por segundo y conservar status HTTP por ítem.

## 2026-07-25 — Backfill retroactivo de Bajó de Precio Motors

- Implementado en `vis-items-loader-tagging` como flujo aislado de ingreso y
  validación; no comparte el processor online.
- Entrada manual: `POST /price-drop-motors-backfill` con
  `{"item_ids":["MLB..."]}`.
- Tópico de trabajo:
  `BIGQUEUE_TOPIC_PRICE_DROP_MOTORS_BACKFILL__NONPROD_TOPIC_NAME`, construido
  con `GetSegmentedPublisher(..., "nonprod")`; consumer:
  `/consume-price-drop-motors-backfill`. El segmento es obligatorio para que
  BigQueue acepte la publicación.
- La validación usa la configuración `price_before_discount_motors`, pero la
  lógica fue duplicada bajo `pkg/process/price_drop_motors_backfill/`: último
  cambio efectivo dentro de 30 días, precio actual igual al `new_value`, baja
  dentro de thresholds, moneda estable, restricciones Motors y precio anterior
  estable durante los días configurados antes del evento de baja.
- La expiración conserva la ventana original (`drop_at + 30 días`) publicando
  el `PriceDropCalendarMessage` normal sobre el tópico productivo existente
  `BIGQUEUE_TOPIC_PRICEDROP_BADGE_EXPIRE_TOPIC_NAME`; el apagado sigue en
  `/consume-price-drop-calendar-cleanup`. No crear tópico ni consumer de
  expiración exclusivos para el backfill.
- Validación local al implementar: `go test ./...`, `go vet ./...`,
  `go build ./...` y race focal de los paquetes nuevos, todo en verde.

## 2026-07-25 — Plan Hito 2 producer

- Contrato confirmado: `VEHICLE_PRICE_HIGHLIGHT_TIER` usa `LOW`, `VERY_LOW` o
  limpieza, junto a `PREVIOUS_PRICE` y `HAS_LOWER_PRICE`.
- Plan durable actualizado en `[[Hito 2 - vis-items-loader-tagging]]`.
- Decisión corregida el 2026-07-27: no introducir `signals`, scopes ni una
  capability coordinadora. Crear `vehicle_price_highlight_motors` como
  implementación directa de `models.Processor`, reutilizando
  `/consume-process-item`, `ProcessorFilter`, `ProcessConfig` y `Orchestrator`.
- El processor nuevo ejecuta siempre Bajó de Precio y Destaque de Precio y
  delega sus reglas en services/helpers pequeños. El proceso masivo y el
  consumer de atributos publican el mismo `models.BqPayload` existente con
  `process:vehicle_price_highlight_motors`.
- Reutilizar `/consume-process-item`/`ProcessorFilter`; no crear consumer de
  evaluación alternativo.
- Implementar un consumer de ingreso dedicado para cambios en atributos
  baneadores. Este consumer no evalúa ni escribe: publica un único mensaje que
  solicita reevaluar Bajó de Precio y Destaque de Precio.
- No denominar Backfill al proceso masivo de Hito 2. El handler consulta una
  sola vez todos los `item_id` en BigQuery, materializa/normaliza esa lista,
  calcula `total_items` con su longitud y construye páginas con los IDs
  explícitos. Los consumers de página no consultan BigQuery; solo hacen fan-out
  a mensajes unitarios.
- El ejemplo de 1000 ítems por página no está confirmado: definir el tamaño por
  límite de bytes, cuota, memoria y pruebas de carga.
- El plan se implementa en tres partes: servicio unitario común, proceso masivo
  robusto y consumer de atributos baneadores.
- No mezclar con el proceso `highlights` existente: pertenece a Real
  Estate/Verdi.

## 2026-07-27 — Rollout del processor de Destaque

- Despliegue 1: registrar `vehicle_price_highlight_motors`, migrar todos los
  productores al ID nuevo y conservar `price_before_discount_motors` deprecado
  únicamente para drenar mensajes antiguos.
- Ningún mensaje debe contener ambos process filters: `ProcessorFilter`
  seleccionaría y ejecutaría los dos processors.
- Despliegue 2: después de confirmar cero productores, backlog, DLQ y una
  ventana operativa sin invocaciones antiguas, retirar solamente la instancia
  y configuración `price_before_discount_motors`.
- No borrar el package `price_before_discount` ni su instancia/config
  `price_before_discount`: Real Estate sigue utilizándolos.
