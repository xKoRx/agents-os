---
type: known_error
schema_version: 1
scope: application
created: "2026-09-02"
updated: "2026-09-02"
area: "[[Echo Forge]]"
project: "[[Echo Forge]]"
application: "[[sqx-watcher]]"
entities:
  - "[[Symphony]]"
  - "[[Zeus]]"
  - "[[Hera]]"
  - "[[Kronos]]"
related:
  - "[[sqx-deployer]]"
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
aliases:
  - watcher stager current path mismatch
  - sqx-watcher 0.2.85 self-terminates under stager
  - /opt/symphony/current watcher guard
confidence: verified
source_session: "ECHO-FORGE-C3-RESUME-FROM-PUBLISHED-0.2.85-NORMAL"
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
---

# 2026-09-02-sqx-watcher-stager-current-link-mismatch

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- El watcher exacto de 0.2.85 inicia contra `/var/lib/symphony/input` pero termina antes de consumir el config de qualification.
- Su guard de upgrade resuelve `/opt/symphony/current` al legado 0.2.40 mientras el ejecutable activo está en `/opt/stager/releases/0.2.85/bin/sqx-watcher`.

## Causa

- `sqx/cmd/sqx-watcher/main.go:389-402` evalúa `/opt/symphony/current` y cancela cuando el ejecutable activo queda fuera de ese path resuelto.
- En Zeus, el link legacy y `symphony-watcher.service` inactivo siguen apuntando a `/opt/symphony/releases/0.2.40`; el runtime gestionado por stager está activo independientemente en 0.2.85.

## Impacto

- La qualification nueva `forge-c3-supply-v2-20260902T191118Z-84F1` no llegó a Temporal; supply quedó no probado y Campaign no pudo comenzar.
- Arrancar el servicio legacy crearía mixed-version; cambiar el link/unit sería un workaround no autorizado durante certificación física.

## Detección

- Inspeccionar el ejecutable activo y el path resuelto de `/opt/symphony/current` antes de entregar input.
- Exigir que el lifecycle canónico lance el watcher relativo a la release bajo el mismo contrato de current path que el runtime stager.

## Mitigación

- Intento exacto: `/opt/stager/releases/0.2.85/bin/sqx-watcher /var/lib/symphony/input`; PostgreSQL y Temporal inicializaron, luego el guard registró `current_active_path=/opt/symphony/releases/0.2.40` y terminó.
- El SHA del watcher 0.2.85 era exacto; no hubo mutación de source, artifacts, release authority ni base de datos.

## Evidencia

- Zeus: `/opt/symphony/current/bin/sqx-watcher` resolvía a 0.2.40; el proceso 0.2.85 se inició directamente desde `/opt/stager/releases/0.2.85` y terminó por el guard.
- La config nueva quedó entregada atómicamente con SHA exacto, pero no fue procesada; el log remoto `/var/lib/symphony/sqx-watcher-c3-v2.log` conserva la secuencia de arranque y terminación.
