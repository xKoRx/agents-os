---
type: journal
kind: session-summary
status: active
tags:
  - kind/summary
  - kind/journal
  - tech/agents-os
  - tech/echo-forge
created: 2026-07-28
updated: 2026-07-28
source_session: "echo-forge-trade-list-deploy-0.2.5-snippets"
main_entity: "[[Symphony]]"
---

# 2026-07-28 — Echo Forge: bug latente en `user/extend/Snippets/` no detectado por primer deploy

## TL;DR

Tras desplegar `EchoForgeAutomator.jar` con el fix `reordered.isEmpty()` en
Zeus/Hera/Kronos, el flow `example_flow_41` volvió a fallar con el mismo
`IndexOutOfBoundsException` en `TradeExtractionService.java:181`. SQX no carga
el plugin desde `user/libs/`, recompila en runtime desde
`user/extend/Snippets/SQ/CustomAnalysis/` que mantenía el `.java` viejo.
Sincronización de Snippets + rebuild del JAR completada. Flow cancelado, sin
relanzar.

## Detalle mínimo

- Síntoma: `IndexOutOfBoundsException` en `TradeExtractionService.java:181` durante `trade_list_exporter`.
- Causa raíz: SQX escanea `user/extend/Snippets/` y recompila dinámicamente los `.java`. La copia en Snippets no se actualizó al deployar el `.jar` y mantenía `Instant periodStart = reordered.get(0).entryTimeUtc();` en línea 181.
- Fix: `rsync --delete` desde el repo local a `user/extend/Snippets/SQ/CustomAnalysis/` en los 3 workers + rebuild del `.jar` (hash `6e2a8223…`).
- Estado: workflow `sqx-main-00_configs-v1-NDX-H1-L-1785288415` cancelado; no se relanzó (petición del usuario).

## Lecciones

Ver L3: [[2026-07-28-echo-forge-tradelist-java-snippets-stale]].

## Próximo paso

Relanzar `example_flow_41` cuando el usuario lo indique. Antes del relanzamiento
confirmar que `user/extend/Snippets/` y `user/libs/EchoForgeAutomator.jar` están
sincronizados con el repo.
