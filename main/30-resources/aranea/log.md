# Aranea — Bitácora (Resource Wiki)

Append-only, cronológico. Formato: `## [YYYY-MM-DD] <op> | <detalle>` con `<op>` ∈ `ingest | query | lint`.

## [2026-08-08] lint | Activación explícita bajo el contrato Resource Wiki

- Se agregó la bitácora raíz requerida por el dominio activo.
- El historial anterior permanece en las páginas, tickets y change logs originales; no se fabricaron entradas retroactivas.
- El subíndice legacy de Backup/DR se normalizó al casing canónico `03-storage/backup-dr/00-index.md` y sus referencias vivas fueron ajustadas.

## [2026-08-10] ingest | migración T6.3 de legado Aranea → schemas vigentes

- Se clasificaron las páginas canónicas: documentación de inventario a `doc`, runbooks operacionales a `runbook` y tickets históricos a `action`.
- Se preservó el contenido histórico y se agregó metadata/routing contractual; las afirmaciones volátiles permanecen sujetas a verificación.

## [2026-08-11] lint | Auditoría base de AGENTS OS Fase 4

- El runbook transversal de migración HTTPS quedó cubierto por el índice raíz; `backup-dr/` se conserva como subíndice que comparte esta bitácora; Graphify quedó limpio y actualizado.

## [2026-09-11] ingest | Capability plane MCP Aranea

- Se actualizó `02-servicios/ml-ia.md` con el contrato operativo MCP verificado: PostgreSQL Echo PROD RO (`echo`/`mcp_echo_prod_ro`), DEV RW (`echo-develop`/`mcp_echo_dev_rw`), SSH certificado y routing Mongo Forge PROD RO / DEV RW; Mongo queda pendiente de smoke funcional posterior al restart del cliente después de corregir sus bearer env vars.

## [2026-09-13] ingest | Kafka/Flink DEV MCP y runtime Echo DEV

- `02-servicios/data-streaming.md` quedó actualizado con Kafka DEV certificado y con Flink/StateFun DEV vigente en `docker-echo-dev`; el antiguo `docker-flink` se conserva sólo como snapshot histórico.
- `02-servicios/ml-ia.md` quedó alineado con el capability plane `:3000`–`:3008`, nueve capabilities certificadas, `aranea-flink-dev-admin` y el profile host/runtime `docker-echo-dev-operator`.
- Flink DEV se cerró con source-of-truth Portainer stack `1`, config persistente bajo `/root/statefun`, control plane MCP separado del host/runtime plane y PROD explícitamente diferido.
