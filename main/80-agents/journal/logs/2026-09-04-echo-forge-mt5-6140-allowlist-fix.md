---
type: change_log
schema_version: 1
scope: session
created: "2026-09-04"
updated: "2026-09-04"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-09-04-echo-forge-mt5-report-6140-compatible-allowlist]]"
  - "[[2026-09-04-mt5-terminal-build-unsupported]]"
  - "[[2026-09-04-echo-forge-c3-lean-0290-blocked-mt5-build]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-MT5-REPORT-CERTIFIED-BUILD-ALLOWLIST-6140-FIX-NORMAL
source_feedbacks:
  - "[[2026-09-04-echo-forge-mt5-6140-allowlist-fix-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-04-echo-forge-mt5-6140-allowlist-fix

## Cambio

- **Tipo:** updated
- **Archivo(s):** known-error `2026-09-04-mt5-terminal-build-unsupported` (mitigación IMPLEMENTADO + commit `9641c9f`); checkpoint interno C3/6140 (actualizado en el mismo archivo, misma `continuity_key`); agent run `2026-09-04-zcode-glm-5.3-flash-echo-forge-mt5-6140-allowlist-fix` (nuevo); feedback de sesión (nuevo); este change log. Sin cambios a decisión canónica (se preserva como está).

## Motivo

- Implementar la decisión `EXPLICIT_CERTIFIED_BUILD_ALLOWLIST` y dejar evidencia durable del fix: el known-error debe reflejar que la mitigación ya está en source y que el desbloqueo total requiere release 0.2.91 + recert C3.

## Fuentes usadas

- symphony master `32d0740` → `9641c9f` (push origin/master); fixture físico MinIO `sqx-strategies` SHA `efbd37e4…` verificado; gates `go test`/`-race`/`vet`/legacy/normalization verdes; test dirigido temporal `Normalize` 6140 COMPLETE/43 trades.

## Resolución aplicada

- `isSupportedBuild{6090,6140}` reemplaza a `SupportedBuild=6090` como autoridad; gate por membership; diagnóstico estructural sin claim 6090-only; fixture `FIX-B6140-75` versionado; CORPUS §2/§3.1/§5.4/§6 y SPEC-PARSER (matriz, regla multi-build, procedimiento build N) actualizados; Margin Level `414.35%` INVALID congelado.

## Validación

- Source review 15/15 (parser_version intacta, 5362/6200 fail-closed, vecinos 6089/6091/6139/6141 rechazados, sin rango ni fallback, SHA/BOM exactos, corpus 6090 PASS, diff limitado a 7 Allowed Files). HEAD == origin/master == `9641c9f11b2a321041f61ea6b8d93ef199d5a38e`. Sin release, sin deploy, C3 sigue `BLOCKED / CLOSED`.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- `git revert 9641c9f` restaura `SupportedBuild=6090`; el fixture y docs quedarían huérfanos del gate (inocuos). No ejecutado.
