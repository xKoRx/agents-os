---
type: change_log
scope: session
created: 2026-07-27
updated: 2026-07-28
area: "[[Echo Forge]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
entities:
  - "[[AGENTS OS]]"
  - "[[EchoForgeTradeListExporter]]"
  - "[[sqx-watcher]]"
related:
  - "[[sqx-watcher-systemd-service-hangs-after-deploy]]"
  - "[[sqx-watcher-validate-configs-ignores-config-folder]]"
  - "[[2026-07-27-trade-list-exporter-type-internal-project-mapping]]"
aliases: []
confidence: verified
source_session: "2026-07-27-echo-forge-trade-list-exporter"
source_feedbacks: []
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/echo-forge
---

# SQX watcher trade list exporter — known errors & decision created

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `80-agents/memory/public/known-error/symphony/sqx-watcher-systemd-service-hangs-after-deploy.md`
  - `80-agents/memory/public/known-error/symphony/sqx-watcher-validate-configs-ignores-config-folder.md`
  - `80-agents/memory/public/decision/symphony/2026-07-27-trade-list-exporter-type-internal-project-mapping.md`
  - `symphony/.agents/skills/echo-forge-testing/SKILL.md` (historial de automejora)

## Motivo

- Persistir tres deltas durables detectados durante la integración
  end-to-end del plugin `EchoForgeTradeListExporter`:
  1. Servicio `symphony-watcher.service` queda colgado tras deploy
     (proceso huérfano retiene el fsnotify watch).
  2. `validate_configs` ignora `config_folder` y busca `.cfx` en la
     raíz del watch dir.
  3. Decisión arquitectónica: el mapping
     `type: trade_list_exporter → EchoForgeTradeListExporter` se
     internaliza en el worker; el JSON de input ya no requiere
     `exporter_project` para ese tipo.

## Fuentes usadas

- Inspección en vivo de Zeus (Zeus 192.168.31.101) durante la
  sesión: `systemctl status`, `journalctl`, `pgrep`, `lsof`,
  `inotifywait`.
- Inspección del repo
  `sqx/adapters/watcher-fsnotify/fsnotify_watcher.go` y
  `sqx/activities/watcher/pipeline/builder.go`.
- Revisión del JSON `input/example/config.json` antes y después
  del cambio.

## Resolución aplicada

- Dos nuevos known errors con su workaround operativo y mitigación
  duradera documentada (cambio puntual en `builder.go`).
- Una decisión pública que consolida el contrato
  `type → exporter_project` dentro del worker.
- La skill `echo-forge-testing` incorpora el patrón reusable para
  recuperación del watcher y validación del contrato del exporter.

## Validación

- Después de aplicar la decisión:
  `input/example/config.json` no contiene `exporter_project` y
  el flow `example_flow_37` se dispatchó en Temporal con
  workflow id `sqx-main-00_configs-v1-NDX-H1-L-1785209819`.
- El reindexado dirigido de Graphify para `symphony` se ejecutó después de
  registrar el cambio de código y la actualización del procedimiento de pruebas.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin credenciales, secretos ni memoria interna.

## Rollback

- Eliminar los tres archivos si el watcher arregla los bugs y la
  decisión se revierte.
