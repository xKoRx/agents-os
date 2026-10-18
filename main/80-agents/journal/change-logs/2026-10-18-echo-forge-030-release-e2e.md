---
type: change_log
schema_version: 1
scope: session
created: "2026-10-18"
updated: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
related:
  - "[[2026-10-18-zcode-glm53-forge-030-release-e2e]]"
  - "[[Echo Forge — Operación Real V2]]"
aliases: []
confidence: high
source_session:
source_feedbacks:
tags:
  - kind/change-log
  - scope/session
---

# Change Log — 2026-10-18 · Echo Forge 0.3.x release + E2E w10

## xKoRx/symphony (master `492a271`, push FF)

- `d67244b` fix(mt5): identidad MagicNumber 64-bit — exporter-plugin `enforceMagicWidth`, `magicreadback.FromHTMInputs`, gate `verifyEffectiveMagic` en `mt5_reconcile_v1` (antes de cualquier escritura durable), puerto `capabilities.MagicAllocationReader`, wiring `durable.Magic`, registro de `evaluate_strategy`. 9 archivos.
- `66dd8cd` chore: gitignore `sqx/exporter-plugin/target/` (buildvcs + untracked = vcs.modified=true).
- `492a271` chore(release): manifest 0.3.1 (linux a4117aac; vcs.modified=false 3/3).
- Integración: 6 ramas contenidas confirmadas; `fix/watcher-import-intake-deadline` sin merge (deadline knob ya en master; watchdog knob innecesario — condición `/Temp/` ya cubre el patrón certificado).

## Flota (mutaciones de rollout, dentro del ambiente operacional único de Forge)

- Releases 0.3.0 y 0.3.1 publicadas en MinIO y aplicadas por los stagers (0.3.0 CUARENTENADA por stamp; 0.3.1 canónica 4/4 verificada por proceso+ruta+SHA vía MCP).
- Plugin SQX en `/home/kor/sqx/144/user/libs/EchoForgeAutomator.jar` (3b0063e4) + snippet fuente en `user/extend/Snippets/` (1599f1be) en Zeus/Hera/Kronos con backups `*.bak-20261018`; clase re-extraída a `internal/tmp/compiled` 3/3.
- Canary focalizado por host (sqcli EchoForgeMT5Exporter con .sqx control 26100091079) ejecutado y limpiado; evidencia MQ5 conservada en /tmp/canary-evidence por host.

## Vault

- `10-projects/Echo Forge — Operación Real V2/artifacts/FORGE-0.3.0-FINAL-CERTIFICATION/` (10 archivos nuevos).
- Nota del proyecto: nuevo ESTADO OPERATIVO 21.ª sesión (2026-10-18).
- Agent run: `80-agents/journal/agent-runs/2026-10-18-zcode-glm53-forge-030-release-e2e.md`.

## No tocado

- Allocator de mágicas, Money Management, algoritmos robust/selection/ranking, CFX del owner, datos NDX, contratos congelados, Echo (0 POSTs; fail-closed).
