---
type: change_log
schema_version: 1
scope: session
created: "2026-10-14"
updated: "2026-10-14"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: symphony
entities:
  - "[[Echo Forge — Operación Real V2]]"
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-10-14-echo-forge-licencias-flota

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - 10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2.md (entrada de bitácora de la regularización de licencias por campaña ETCD)

## Motivo

- Mandato owner posterior a la release 0.2.132: regularizar la licencia en los 3 workers mediante la modificación del registro ETCD (key + fecha), dejando los 3 hosts exactamente iguales (2 versiones, 144 con bd completa, licencia nueva en todos).

## Fuentes usadas

- ETCD producción (control archivado sep-24 con key 921C51; estados/summaries z0-h0-k0; config maintenance), license.db de la flota leídas con strings (codes en claro), logs de sqcli en user/log (error "installation directory is read-only"), prueba física de bootstrap/update como echo-dev en Zeus, código del CampaignEngine/MaintenanceExecutor/quiesce-etcd.

## Resolución aplicada

- Config de mantenimiento de producción alineada al contrato KISS; control armado con EA6F8A + machine-id c8e7f988… + request 2026-10-14T00:00:00Z; Zeus-144 bootstrapeado y Zeus-142 corregido en dos causas raíz (licencia almacenada expirada bloquea update; directorio de instalación no escribible por kor); campaña final 3/3 COMPLETED; control neutralizado a {}; 6/6 license.db con EA6F8A; machine-id uniforme.

## Validación

- Estados y summary en ETCD, mtimes y contenido de las 6 license.db, pollers Temporal 3/3 con PIDs vivos, workers 0.2.132 estables tras 4 ciclos de quiesce/respawn.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos plenos; los codes de licencia de flota (trials de 6 caracteres) se referencian donde ya son legibles en la propia flota

## Rollback

- Revertir el delta documental por Git; el estado operativo (licencias/ETCD) no se revierte salvo decisión owner.
