---
type: agent_memory
schema_version: 1
scope: domain
created: 2026-09-24
updated: 2026-09-24
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
related:
  - "[[Echo + Echo Forge — Environment Contract]]"
aliases: []
confidence: verified
memory_state: active
continuity_key: echo/forge-v2-prework-license
load_policy: manual
indexable: true
index_priority: low
trigger: cuando se re-dispache el cierre del gate de prework SQX DEV o se toque licencia SQX en Daedalus
tags:
  - agent/internal
  - kind/agent-memory
  - area/echo
  - project/echoforge
---

# Forge V2 prework — licencia no efectiva en Daedalus (2026-09-24, 3.ª sesión)

## Estado durable

- `sqcli` en Daedalus NO acepta licencia: con la copia flota en el sitio rechaza en línea (`License is not valid for this computer`, HWID `C487C9A88600`, Build 142.2399); sin license.db responde `Missing license`. La identidad de licencia SQX es 100% local: una activación heada en portal/vendor NO cambia el comportamiento de `sqcli` sin el registro local.
- El `internal/license.db` retirado en esta sesión era la copia flota sembrada por el prework 2 (`license=D0C25B`, SHA256 `a25ce029…`, probado RO contra Kronos). Backup: workspace `forge-prework3-20260924/stale-license.db.copy-of-kronos`. NO restaurarlo (mandato prohíbe reutilizar credenciales de flota).
- Runtime candidato intacto y re-verificado: baseline `d9032ff8` limpio local=origin; binarios `7af048f0…`/`b2e9c227…` en `~/aranea/work/forge-prework2-20260924/bin/`; prefijos ETCD `/sqx-{worker,watcher}/forgev2dev/` + cola `sqx-forgev2-dev-v1` sin pollers; sin procesos residuales.

## Próximo paso exacto

- Owner completa la activación local de la licencia legítima en Daedalus (que `internal/license.db` quede bound a `C487C9A88600` vía el flujo oficial con la credencial nueva). Verificación owner antes de re-dispachar: output literal de `sqcli -v` mostrando aceptación (sin "Failed to check license").
- Re-dispachar la sesión de cierre: `sqcli` acepta → 1 worker en cola exclusiva → camino real watcher→MinIO→Temporal→worker→sqcli→SQX→EchoForgeOverviewExporter → evidencia con input/output SHA → teardown → `PREWORK_PASS`.
