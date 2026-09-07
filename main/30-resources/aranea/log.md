# Aranea — Bitácora (Resource Wiki)

Append-only, cronológico. Formato: `## [YYYY-MM-DD] <op> | <detalle>` con
`<op>` ∈ `ingest | query | lint`.

## [2026-08-08] lint | Activación explícita bajo el contrato Resource Wiki

- Se agregó la bitácora raíz requerida por el dominio activo.
- El historial anterior permanece en las páginas, tickets y change logs
  originales; no se fabricaron entradas retroactivas.
- El subíndice legacy de Backup/DR se normalizó al casing canónico
  `03-storage/backup-dr/00-index.md` y sus referencias vivas fueron ajustadas.

## [2026-08-10] ingest | migración T6.3 de legado Aranea → schemas vigentes

- Se clasificaron las páginas canónicas: documentación de inventario a `doc`, runbooks operacionales a `runbook` y tickets históricos a `action`.
- Se preservó el contenido histórico y se agregó metadata/routing contractual; las afirmaciones volátiles permanecen sujetas a verificación.

## [2026-08-11] lint | Auditoría base de AGENTS OS Fase 4

- El runbook transversal de migración HTTPS quedó cubierto por el índice raíz; `backup-dr/` se conserva como subíndice que comparte esta bitácora; Graphify quedó limpio y actualizado.
