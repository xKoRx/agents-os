# Grids locales — Bitácora

Append-only, cronológico. Formato: `## [YYYY-MM-DD] <op> | <detalle>` con `<op>` ∈ `ingest | query | lint`.

## [2026-08-12] ingest | Activación del dominio
- Alta de `rio-scope-inventory.html` como primer grid del dominio, con `rio-scopes.json` y SIG-599 como fuentes de verdad y el HTML como vista derivada.

## [2026-09-03] ingest | rio-scope-inventory schema v4
- Reconciliación del inventario con el corte Fury 2026-09-03 y publicación del documento remoto en Grid.

## [2026-09-08] ingest | rio-deployments-critical-flow
- Alta de la presentación técnica de seis slides sobre el flujo de deployments en RIO, verificada contra código y documentación local y mantenida sólo en local.

## [2026-09-09] lint | Backfill de bitácora
- El dominio estaba `status: active` sin `log.md`, contra el contrato de `00-RESOURCE-WIKI.md`. Se reconstruyó la bitácora desde las entradas del catálogo; las fechas provienen de `00-index.md` y de los change logs del journal, no de una nueva verificación de contenido.
