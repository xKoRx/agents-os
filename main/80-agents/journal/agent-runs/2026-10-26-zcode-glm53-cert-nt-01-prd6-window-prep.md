---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-26"
updated: "2026-10-26"
area: "[[Echo]]"
project: "[[Echo Futures — Runtime Pools]]"
application:
entities: []
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
model_source: session
task_type: implementation
task_complexity: high
outcome: success
verification: full
evaluator: agent
user_rework: none
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — CERT-NT-01 fase 0 PRD.6 (preparación de ventana sin restart)

## Trabajo

- **Objetivo:** mandato ONE-SHOT 2026-10-26 sobre la adjudicación PRD.6: fase 0 completa sin reinicio (refresh de estado, release del SHA exacto `4a041e6c`, WINDOW-CARD materializada en vault, inventario de 17 ingresses, storage off-host, cinco capas de desarme) y STOP en el gate de ventana Owner.
- **Alcance atribuible (Submanager GLM-5.3-Flash LOCAL):** verificación física RO vía MCP (Flink DEV, Kafka DEV, etcd RO, SSH docker-echo-dev-operator sobre .75; dev-win viewer rechazado por policy — capa NT registrada por última autoridad); build del release en `wt-main` limpio; materialización canónica de la tarjeta (materialize_schema_note.py, tipo `doc`); planner + journal.
- **Artefactos afectados:** release local `/home/kor/opt/echo-dev/releases/4a041e6cf17b27a023a1a693a48be1034c35e7dd/` (sin repoint); vault: [[WINDOW-CARD-PRD6]] (nueva, readback `e40e793c…`), bitácora del planner, change_log y este run; directorio `/srv/echo-work/ef-recovery/prd6-20261026/` pre-creado. **Cero mutaciones del runtime compartido; cero escrituras PROD.**

## Evidencia

- Estado verificado 2026-10-26T23:30Z: job `0f6901a3` RUNNING 38/38 (66,7 h), checkpoints 1970 COMPLETED / 0 failed / 0 restored, último `chk-1970`, savepoints VACÍOS, `num-retained=1`; module.yaml 20 768 B (17 ingresses + 7 egress, FEFB S2); 17 grupos `echo-statefun-*` EMPTY; FX lag≈0 (account-snapshots 136, trade-journal-master 1), market-feed frontier congelada 45.142.540, execution-events/physical-drain vacíos; ETCD binding desarmado, config_snapshot 11 991 B, freshness ausente; Core `ac0621a1` ACTIVE, sin `:9771`, sin futures-bridge.
- Release `4a041e6c`: buildvcs `vcs.modified=false` en ambos binarios; hashes en BUILD.md (`10624fd0…` core, `1e8c2c08…` runtime-control, `c84ca495…` sonda idéntica al lab); `git ls-remote origin feature/ef-runtime-pools` = `4a041e6c`.
- Hallazgos nuevos registrados en la tarjeta §5: (a) roster DEV sin enumerador autoritativo (fail-closed en ambas direcciones — definir método antes de la ventana); (b) G5 sin rsync en .75 y sin clave SSH en ninguna dirección (Owner decide clave o relay SFTP autorizado); (c) `--help` sin `seal`/`bootstrap-token` (cosmético P3 D-5); (d) discos: .75 raíz 2,3G libres, /srv/echo-work 12G libres.

## Verificación

- Lecturas cruzadas de dos canales por hecho (REST/MCP + SSH/host; Kafka admin + module.yaml); readback de la tarjeta por sha256 + validador de schema contract (0 errores); worktree limpio verificado antes del build; hashes reproducibles en BUILD.md.
- Limitación declarada: capa NT (.132) no re-verificable esta sesión (perfil viewer sin ejecución permitida); offsets de los 11 grupos FX restantes sin muestra individual (el seal captura la frontier autoritativa por ingress en P1).

## Rework

- Ninguno. STOP en `/owner-window-gate`: sin aprobación expresa del Owner no se ejecuta savepoint, paro, restore, migración ni deploy (STATUS: OWNER_WINDOW_REQUIRED).
