---
type: change_log
schema_version: 1
created: "2026-09-22"
area: "[[Aranea]]"
project: "[[Echo Forge — Import Task V1]]"
entities:
  - "[[Echo Forge — Import Task V1]]"
  - "[[Echo Forge]]"
related:
  - "[[aranea-ssh-mcp]]"
aliases: []
load_policy: manual
indexable: true
index_priority: low
tags:
  - kind/change-log
  - area/aranea
---

# 2026-09-22 — Import V1: recuperación de infra, CFX publicado, RT-1 v2

## Contexto

Mandato one-shot de cierre de Import V1 (G0–G8). El estado recibido bloqueaba G3/G5/G7 al canal `aranea-ssh` (503) y Mongo RO (`session not found`), y el CFX no existía.

## Cambios en el repo `xKoRx/symphony` (branch `feature/sqx-import-task-v1`, push FF `329ee94..f02bf39`)

- `213747c` docs(import): RT-1 v2 re-issue (loader contract `ENV`→`/sqx-worker/<ENV>/` demostrado contra `sqx/cmd/sqx-worker/main.go` + SDK `etcd.New` `fmt.Sprintf("/%s/%s/")`; CFX generado/validado/publicado; identidad Kronos por triple vía; preflight host-level PASS; manifest congelado de 8 NDX_W3; receta de runbook ejecutable con `config` y universo real).
- `f02bf39` chore: fixture `specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json` restaurado a bytes del baseline (efecto lateral de tests que se coló en `213747c`); `f5_warning_example.json` restaurado en el worktree (sin commit: vuelve a estado HEAD).
- Cero cambios de código; sin master (`745bc8b` intacto); SPEC y amendments frozen sin tocar.

## Cambios físicos fuera del repo

- **ssh-mcp (LXC mcps):** restart documentado por management path (`hermes`→`mcps-ops`→`sudo docker restart ssh-mcp`) ante firma canónica de pool agotado; baseline previo (imagen `local/ssh-mcp:2.8.0-d2d7696-h2fix`, mounts, `unless-stopped`) capturado; smoke server+consumer PASS; cero producto tocado. `config.toml` verificado en 600/65532 (sin drift final).
- **MinIO `sqx-strategies`:** objeto NUEVO `wave_import_cert_v1/usatechidxusd_darwinex/l_h1/SQX/v1/00_configs/EchoForgeImportExporter.cfx` (1841 B, SHA256 `64ab2674…`, etag `652b9666…`, read-back verificado). Write-once: primer y único put del namespace del wave.

## Evidencia clave

- Pool agotado: `503 Server is at its session limit (64)` reproducido y mapeado al runbook [[aranea-ssh-mcp]] §Operación.
- G3: VM 111 `sqx-kronos` @ .121 (MAC `bc:24:11:e2:35:ab`), worker flota 0.2.105 PID 1400507 (SHA `e1f62e06…`), `passed` ≈200+ NDX_W3 (z0=83/k0=69/h0=48 visibles), cero XAUUSD en los tres hosts, plugin jar SHA `aaa30d44…`.
- G4: CFX validado contra `postProcessCFX` real (2 pases idempotentes, binding `input`, fail-closed sin plugin).
- G6: binario `sqx-worker` @ `329ee94` SHA256 `5f8df487…` (`vcs.modified=false`); regresión = baseline exacto (21 workflows + 1 fixture-gate); build con entorno CGO de usuario para libzmq 4.3.5 sin sudo.
- G7: **BLOCKED a RT-1 v2 (CONFIRMED del owner)** — nada arrancado, flota intocada.

## Owner action pendiente

CONFIRMED/DENIED de `RT1-REQUEST-G7-OPCION-B.md` v2 (host VM 111 kronos, ventana ≤2 h, universo `USATECHIDXUSD_darwinex/L/H1` a confirmar contra retests originales, siembra de `/sqx-worker/import-cert-dev/` o delegación expresa).
