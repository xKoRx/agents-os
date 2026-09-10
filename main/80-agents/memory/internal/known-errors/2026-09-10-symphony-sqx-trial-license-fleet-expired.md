---
type: known_error
schema_version: 1
scope:
created: "2026-09-10"
updated: "2026-09-10"
area: "[[Echo]]"
project: "[[Echo Forge — F-03 SQX long-running]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge — F-03 SQX long-running]]"
related:
  - "[[Echo Forge — F-03 SQX Long-Running Contract]]"
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
aliases:
  - sqx trial expired
  - licencia SQX expirada
  - License is invalid Trial license expired
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/session
  - tech/symphony
  - tech/sqx
  - tech/echo-forge
  - severity/high
  - status/diagnosed
---

# 2026-09-10-symphony-sqx-trial-license-fleet-expired

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- `sqcli` (SQX 142.2399) exit 1 en <5 s en cualquier invocación: `Failed to check license - License is invalid - Trial license expired..` seguido de `Exit app - Failed to check license`. No escribe log de task en `user/projects/<p>/log/`.
- El worker lo observa como `execution error: command 'sqcli' failed with exit code 1` y (por diseño F-03, retry transiente infinito) el workflow queda reintentando hasta cancel manual.

## Causa

- La instalación SQX del lab Linux comparte Hardware ID `C0CCF0856B2C` (VMs con serials QEMU por defecto) y corre sobre licencia trial; la trial expiró entre el 2026-08-24 (último maintenance `license=869A77` completado en z0) y el 2026-09-10.
- Replicar el control de mantenimiento `sqcli license=869A77` (y las claves históricas `5F89F5`, `71CE83`) falla con el mismo error: ninguna clave vigente. La licencia SQX es comercial per-seat/per-VM gestionada por el owner.

## Impacto

- Bloquea toda certificación/ejecución PHYSICAL que requiera compute SQX real en Zeus (`sqx-ulab-zeus-0`) y Hera (`sqx-ulab-hera-0`): certificación PHYSICAL de [[Echo Forge — F-03 SQX long-running]] quedó `BLOCKED` con el lab ya aprovisionado.
- Segunda recurrencia documentada: el mismo blocker detuvo la certificación durable del track [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]] (worker Zeus 0.2.69, intentos 1 y 2).

## Detección

- `grep -iE "error|license" <log manual>` tras ejecutar `sqcli -project action=list` directo en el host; o metadata `full_command`/`exit_code` del worker en `/tmp/f03-cert/logs/worker.log` (cert f03cert).

## Mitigación

- Única resolución: owner restaura una licencia SQX válida en los hosts requeridos y se repite la certificación con `request_id` nuevo. No hay bypass técnico: no mocks, no `sleep`, no MT5.
- Reaplicar licencia desde el control de mantenimiento (`maintenance/control` en ETCD) sólo funciona con clave vigente.

## Evidencia

- Hera y Zeus: `./sqcli -project action=list` → `Verifying license ... Trial license expired`, exit 1 (2026-09-10); `./sqcli license={869A77,5F89F5,71CE83}` → exit 1.
- ETCD `/sqx-worker/production/maintenance/state/z0` = completed 2026-08-24 (última aplicación exitosa conocida).
- Certificación F-03: workflow `sqx-main-v1-d917aa11-ad27-49a5-bebd-cfd142c2e6ad` (ns `sqx-prop`) desplegó sqcli real y falló en el license check; cancelado vía `temporal workflow cancel` → `CANCELED` sin reanudación por retry.
