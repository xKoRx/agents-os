---
type: change_log
schema_version: 1
scope: session
created: "2026-10-31"
updated: "2026-10-31"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[Research — Target Fee Inventory W1-o 2026-10-31]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-10-31-polymarket-w1o-fee-inventory-feedback]]"
  - "[[2026-10-31-code-scout-w1o-fees-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-31-polymarket-w1o-fee-inventory-entity-updated

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `10-projects/Personal/Polymarket Engine/Research — Target Fee Inventory W1-o 2026-10-31.md` (creada: informe del inventario de fee del objetivo 5784455)
  - `10-projects/Personal/Polymarket Engine/Polymarket Engine — Continuidad Five-POC 2026-09-20.md` (actualizada: sección de cierre W1-o)
  - `10-projects/Personal/Polymarket Engine/Polymarket Engine — MVP.md` (actualizada: ítem de alcance y bitácora del 31 de octubre)
  - `80-agents/journal/sessions/2026-10-31-polymarket-w1o-fee-inventory-summary.md` (creada)
  - `80-agents/journal/feedback/system-1/2026-10-31-polymarket-w1o-fee-inventory-feedback.md` (creada)
  - `80-agents/journal/feedback/system-1/2026-10-31-code-scout-w1o-fees-feedback.md` (creada durante el scouting de esta sesión)
  - `80-agents/journal/agent-runs/2026-10-31-zcode-minimax-m3.1-flash-polymarket-w1o-fee-inventory.md` (creada)
  - `80-agents/journal/logs/2026-10-31-polymarket-w1o-fee-inventory-entity-updated.md` (creada: este registro)

## Motivo

- Cerrar el paso documental que W1-nR dejó abierto: **auditar en lectura offline la identidad de fee del mercado objetivo `5784455` y sus 2 assets con su `known_at` real, pasando el conjunto por el `FeeResolverV1` existente**, y comparar explícitamente con la evidencia W1-e de otros mercados sin transferir tasas ni fechas. El hueco era literal: la metadata de fee del objetivo estaba **no inspeccionada** («no inspeccionado» ≠ «ausente»).
- Orden del Owner: procesar con MiniMax código, documentación, fixtures y capturas **exploratorias** públicas de Polymarket y sus metadatos de fee; quedan excluidos credenciales, cuentas y validación reservada/OOS. Sin red de mercado, sin capturas nuevas, sin trading, sin replay de estrategia, sin frameworks nuevos y sin cambios de L o de parámetros.

## Fuentes usadas

- `10-projects/Personal/Polymarket Engine/Research — Single Episode Public Pilot W1-j 2026-10-29.md` (modo identity, gate OOS id-first; página gamma en capture_seq 2).
- `10-projects/Personal/Polymarket Engine/Research — Default Suite Isolation W1-nR 2026-10-30.md` (tabla de fees: metadata del objetivo NO inspeccionada; regla de L pendiente del Owner).
- Metadata autorizada del lote 3: `selection-manifest-identity.json` (sha256 `b2de46c7…`), `prepared-plan-identity.json` (sha256 `ef3a85f0…`), `identity-evidence.json` (sha256 `f3628a1e…`).
- Código reutilizado sin duplicarlo: `internal/capture.OpenView`, `internal/protocol` (parsers Gamma/CLOB/Market WS), `internal/regimes.ResolveFee` (`fee_resolver_v1`), `cmd/engine/clob_observe.go`, `cmd/researchpilot/{discovery,economics}.go`.
- Artefactos del shot: `inventory.json` (sha256 `06da2780…`), `inventory.md`, `run-receipt.json`, `scout-pack.json`, `implementation-ready.json`, binario `fee-inventory` (sha256 `231eebf8…`).

## Resolución aplicada

- Se creó `cmd/feeinventory` (extractor + 13 tests), que lee el episodio **sólo** por `capture.OpenView`, verifica la identidad del target contra el journal, separa declared/cap de mercado, declared/cap por asset (heredado), trade-informed y settlement, y falla cerrado sin escribir salida si la identidad no se confirma o se contradice.
- Se corrigieron tres descripciones causales: el ancla `as_of_kickoff_K` es el estado **conocido hasta K** (no habilita decisiones anteriores ni fee retroactiva); `source_as_of_raw` (updatedAt/gst/timestamp de evento) se preserva crudo **sin** acreditar fee-effective-as-of, vigencia inicial ni antigüedad de fórmula; `known_at_utc` se deriva de `Envelope.ReceivedWall` como reloj observado de recepción, con `capture_seq` como prueba de orden/durabilidad y corte.
- Se corrigió un finding de revisión: el agregado de lexemas trade-observados perdía el `asset_id` al aplanarse (dos assets pueden compartir lexema); se añadió `asset_id` a la fila y un test sintético que falla si se pierde la atribución o se mezclan conteos.
- Resultado registrado: cap declarado `maker/taker = 1000` bps con `fees_enabled=true` en 8 lecturas, `fd`/`r` crudos sin escala ni fórmula inferidas, 78/78 trades con `fee_rate_bps = "0"` (60 y 18 por asset), `INTERVAL [0,1000]` en declared, `POINT 0 bps` en trade-informed, settlement `NOT_CERTIFIED` y `REAL_FEE_READY = false`; ninguna fee se trasladó desde W1-e u otros mercados.

## Validación

- Test focal `./cmd/feeinventory`: 1 corrida, exit 0, `ok … 0.009s`, 13 casos PASS, sobre los hashes aprobados por el supervisor (`main.go 39305a69…`, `main_test.go a473635c…`).
- `gofmt -l` vacío sobre los dos paths propios; `go build -p 1` exit 0 (binario sha256 `231eebf8…`).
- Extractor ejecutado **una** vez sobre el episodio W1-j (exit 0): `inventory.json` (sha256 `06da2780…`) leído en rangos completos (3116 líneas) y derivado a `inventory.md` y `run-receipt.json`.
- Commit local `7c9adaea59251b39ac1559db1ed63d4566996206` con sólo los dos paths propios; `git status --short` limpio, `git diff --check` limpio; sin push.
- No medido por esta sesión (lo verifica el supervisor): integridad de los 90 archivos sellados, sincronización remota del vault y procesos del host.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Las notas nuevas del journal y la nota de research se pueden retirar sin tocar evidencia; la entidad MVP y la continuidad sólo recibieron deltas aditivos (sin borrado de historia), de modo que revertir este cambio consiste en quitar las secciones W1-o añadidas. El commit de código es local y sin push: `git revert 7c9adaea59251b39ac1559db1ed63d4566996206` devuelve el repo al estado previo sin afectar los 90 archivos sellados ni los artefactos del episodio.
