---
type: change_log
scope: project
date: 2026-07-29
area: "[[Meli]]"
project: "[[Cierre VIS]]"
entities:
  - "[[Fase 2 — Proceso Masivo por Site vía items_batch_search — Loader Tagging]]"
  - "[[Cierre VIS]]"
tags:
  - kind/changelog
  - area/meli
  - feature/destaques-de-precio
  - phase/2
---

# Change log — Fase 2: aislamiento del fan-out masivo + naming Fase 1

- **Editado** [[Fase 2 — Proceso Masivo por Site vía items_batch_search — Loader Tagging]]: nueva sección "🚦 Iteración actual — Aislamiento del fan-out masivo (tópico + consumer dedicados)", decisión **D6**, entrada de bitácora y `updated: 2026-07-29`.
- **Decisión D6 (arquitectura):** el fan-out unitario del masivo **no** va al `itemToProcess` global; va a un **tópico masivo dedicado + consumer dedicado** que **reutiliza** `processorFilter` + `ConsumerFilteredItems` + processor `vehicle_price_highlight_motors`. Refina D1 (se mantiene "directo a unitario"; cambia el destino). Motivo: aislar el lag de horas del backfill (cientos de miles de msgs, rate-limit insuficiente) del carril real-time compartido.
- **Hallazgo del código (baseline `feature/f2-vehicle-price-highlight-motors`):** hoy el fan-out **ya cae en el consumer global** (`resources.go:486`, `unitaryPublisher = publicToTopicService` → `itemToProcess`). El scroll-driver ya está aislado en su tópico propio.
- **Corrección técnica:** una key `massive:algo` en el mismo tópico **no aísla lag/throughput** (un tópico = un backlog/pool). El aislamiento en BigQueue es por tópico+consumer, no por atributo. Se descarta la key.
- **Plan implementation-ready** dejado en la nota (tópico + publisher + rewire de una línea + endpoint `/consume-process-item-massive` reusando la misma cadena + config/DLQ propia + tests de wiring).
- **Implementación completada en `vis-items-loader-tagging`:** agregado el publisher non-site `BIGQUEUE_TOPIC_ITEM_TO_PROCESS_MASSIVE__NONSITE_TOPIC_NAME`, el scroll-driver fue re-cableado a ese publisher y la ruta `/consume-process-item-massive` reutiliza exactamente `ConsumerFilteredItems` + `ProcessorFilter`. Prueba focal y `go test ./...`, `go vet ./...`, `go build ./...` en verde.
- **Ajuste posterior:** el tópico driver es compartido entre procesos masivos bajo `BIGQUEUE_TOPIC_MASSIVE_SCROLL__NONSITE_TOPIC_NAME`, usando el segmento `nonsite`; los runs de esta iniciativa llevan `massive:price_highlights` en el envelope de BigQueue, incluido en arranque y continuaciones.
- **Follow-ups:** poison message determinístico (CWE-841, hoy mitigado con `max_items:0`); política DLQ/max-retries del consumer masivo.
- **Naming Fase 1 (propuesta, no aplicada):** renombrar el proceso padre `pkg/process/vehicle_price_highlight_motors` (tipo `VehiclePriceHighlightMotors`) → **`vehicle_price_signals_motors` / `VehiclePriceSignalsMotors`** para resolver la colisión con el servicio-señal `pkg/services/vehicle_price_highlight.go`. Rename **solo de símbolos Go** (barato, interno; caller en `resources.go:424`); **no tocar** el process ID string `"vehicle_price_highlight_motors"` (acoplado a Fury Config/filtro/tópico — migración aparte).
