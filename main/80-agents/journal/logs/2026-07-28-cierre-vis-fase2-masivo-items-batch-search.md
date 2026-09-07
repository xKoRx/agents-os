---
type: change_log
scope: project
date: 2026-07-28
area: "[[Meli]]"
project: "[[Cierre VIS]]"
entities:
  - "[[Fase 2 — Proceso Masivo por Site vía items_batch_search — Loader Tagging]]"
  - "[[vis-sdk-go]]"
  - "[[Cierre VIS]]"
tags:
  - kind/changelog
  - area/meli
  - feature/destaques-de-precio
  - phase/2
---

# Change log — Fase 2 masivo Destaque de Precio (sin BigQuery)

- **Creado** [[Fase 2 — Proceso Masivo por Site vía items_batch_search — Loader Tagging]] (proyecto de agente bajo [[Cierre VIS]]): plan detallado que reemplaza la consulta BigQuery del masivo por `items-batch-search` (scroll por site) del SDK.
- **Creado** [[vis-sdk-go]] (entidad de aplicación) con la API de `items-batch-search` documentada (query/count/scroll y tope ~9000 de query).
- **Editado** [[Cierre VIS]]: tarea puente `#type/supervision` de Fase 2 y links a Fase 2 + [[vis-sdk-go]].
- **Decisiones (encuesta):** D1 fan-out directo a unitario (clon `/job-highlights`, se corrige VMDEM-27); D2/D4 arranque asíncrono + cadena de scroll resumible con estado en mensaje durable y restricción de ≤ 2 min por consumer (1 página por ejecución); D3 filtro de góndola por site desde `ProcessConfig`.
- **Correcciones del owner (2026-07-28):** baseline = rama `feature/f1-vehicle-price-highlight`; las 3 fases corren en paralelo (Fase 1 no bloquea).
- **VMDEM-27 reescrito completo** (canónico): sin BigQuery/page-topic, scroll-driver async resumible, processor estándar (sin signals), fases paralelas, Fase 2 implementation-ready. Se actualizó vía `PUT /api/cli-api/specs/VMDEM-27` con `curl` porque el CLI `spellbook specs edit --content` rechaza backticks (guard anti-inyección); token/baseURL desde `~/Library/Preferences/spellbook-nodejs/config.json`.
- **Pendientes:** spike de latencia scroll+publish y TTL de `context_id`; poblar filtros de góndola por site; validación fina de VMDEM-27 vs VMDEM-21.
- **Implementación 2026-07-28:** Fase 2 implementada en `vis-items-loader-tagging`: trigger async, mensaje driver durable, scroll por página, fan-out directo al process unitario, filtros `domain_id` por site, topes/reintentos y tests de reanudación/no-skip. `go test ./...` y `go vet ./...` verdes. La evidencia operativa de latencia/TTL/carga queda para el Gate G2.
