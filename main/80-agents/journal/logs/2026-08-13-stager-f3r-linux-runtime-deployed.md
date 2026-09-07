---
type: change_log
schema_version: 1
scope: session
created: "2026-08-13"
updated: "2026-08-13"
area: "[[Echo Forge]]"
project: "[[Stager - Cross-Platform Deployment Lifecycle]]"
application: "[[stager-app]]"
entities:
  - "[[Stager - Cross-Platform Deployment Lifecycle]]"
related:
  - "[[2026-08-13-stager-f3r-cooperative-runtime-local-pass]]"
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

# F3.R — Runtime Stager desplegado en Linux

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `stager-runtime` y `stager-runtime.service` en Zeus, Hera y Kronos.
  - `10-projects/Echo Forge/agentes/Stager - Cross-Platform Deployment Lifecycle.md`

## Motivo

- El owner ejecutó el despliegue interactivo con sudo del runtime que elimina el plazo destructivo para el drain.

## Fuentes usadas

- Salida de terminal del owner del 2026-08-13: copia del pack, instalación, recarga systemd y reinicio exitoso en `192.168.31.101`, `192.168.31.111` y `192.168.31.121`.

## Resolución aplicada

- Los tres servicios están `active` y reportan `TimeoutStopUSec=infinity`, `KillMode=process` y `SendSIGKILL=no`.
- El `grep` final no usó sudo; el archivo objetivo está protegido. El fallo ocurrió después de las mutaciones y no revierte ni invalida el servicio activo.

## Validación

- PASS remoto para unidad y proceso en los tres hosts.
- Pendiente: ejecutar `sudo grep` para registrar el valor efectivo de `shutdown_timeout` y preflight de configuración dinámica Temporal antes del canary Symphony real.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Restaurar el binario, unidad y backup de target de cada host devuelve el comportamiento previo. No se alteraron releases ni estado durable de Stager.
