---
type: skill
schema_version: 1
name: hermes-agent-operator
description: >-
  Diagnostica y opera Hermes Agent como servicio de infraestructura de Aranea:
  perfiles, dashboard/serve, gateways, systemd --user, updates y recovery.
  Cargar cuando el target del incidente o cambio es Hermes mismo, no cuando
  Hermes sólo actúa como operador de otro servicio. Deriva la mecánica de
  update/recovery a [[hermes-linux-update-recovery]].
scope: area
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Aranea]]"
entities:
  - "[[Aranea]]"
  - "[[HERMES — ARANEA AUTONOMOUS OPERATIONS]]"
related:
  - "[[HERMES — Infrastructure Operations]]"
  - "[[hermes-linux-update-recovery]]"
  - "[[aranea-agent-dev]]"
aliases:
  - hermes agent operator
  - hermes operations
  - hermes runtime operator
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/area
  - area/aranea
  - tech/hermes
  - tech/agents-os
  - action/hermes-operations
---

# hermes-agent-operator

## Purpose

Operar y diagnosticar el runtime de Hermes Agent en Aranea cuando Hermes mismo es el target: instalación, perfiles, dashboard/serve, gateways, `systemd --user`, update, restart, health o recuperación.

Trigger boundary:

- **Sí:** `hermes update`, Hermes no inicia, dashboard/serve falla, gateway/Telegram de Hermes está degradado, profile routing extraño, `mixed sys.modules`, `fleet_restart_pending`, service duplication o recuperación del host/runtime Hermes.
- **No:** Hermes está sano y sólo administra otro target de Aranea; usar la skill del dominio objetivo (MCP plane, backup, Proxmox, etc.).
- **Handoff:** update/recovery Linux → [[hermes-linux-update-recovery]]; capability MCP → [[aranea-mcp-plane-operator]] / [[aranea-mcps-expert]]; infraestructura general → [[HERMES — Infrastructure Operations]].

## Minimal Read

Read only:
1. `[[HERMES — Infrastructure Operations]]` — authority y estado canónico del management plane.
2. `[[hermes-linux-update-recovery]]` sólo si la tarea toca update, restart o recovery del runtime Hermes.
3. La unidad/systemd/config específica del target que la evidencia indique; no escanear todo el host.

## Procedure

1. **Fijar el target Hermes.** Distinguir host/runtime Hermes de los servicios que Hermes administra. Si el target real es otro servicio, hacer handoff antes de tocar Hermes.
2. **Resolver identidad y perfil antes de operar.** Registrar usuario efectivo, checkout, perfil sticky (`~/.hermes/active_profile`), `HERMES_HOME` efectivo y unidad exacta. No asumir que un comando bare opera `default` ni que `-p` corrige todo routing interno.
3. **Resolver supervisor real.** Para procesos persistentes, identificar PID → parent → cgroup → unidad antes de restart/kill. En SSH sin user bus, reconstruir `XDG_RUNTIME_DIR=/run/user/<uid>` y `DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/<uid>/bus` antes de usar `systemctl --user`.
4. **Preferir fresh-process evidence.** Ante imports/atributos inconsistentes después de update, probar primero un proceso Python fresco contra el checkout en disco. Un traceback del proceso updater no demuestra que el checkout nuevo esté roto.
5. **Evitar duplicación de gateways.** Antes de iniciar un gateway `default` o secundario, comprobar perfil, plataforma y credenciales por fingerprint/hash. Dos pollers con el mismo token son un fallo operacional, no una solución al bookkeeping del updater.
6. **Separar runtime health de updater bookkeeping.** Dashboard/gateway pueden estar sanos aunque quede un marker/receipt stale. No repetir `hermes update` ni revivir servicios sólo para silenciar un warning; reconciliar marker, receipt y fleet con evidencia.
7. **Aplicar el runbook mecánico** cuando corresponda y validar funcionalmente: versión/SHA fresco, dashboard HTTP, servicio activo y plataforma conectada.
8. **Persistir sólo delta durable.** Si cambia topología/authority/servicio vigente, actualizar el proyecto canónico; si emerge una secuencia repetible, actualizar el runbook. No guardar dumps ni secretos.

## Output

```text
Target Hermes:       <host/runtime/perfil/unidad>
Profile/home:         <perfil sticky + HERMES_HOME efectivo>
Supervisor:           <systemd-user/manual/otro>
Checkout/runtime:     <SHA/version + current|stale|unknown>
Intervention:         <none|restart|disable legacy|marker recovery|otro>
Functional health:    <dashboard + gateway/platform>
Updater state:        <clean|pending reconciled|blocked>
Handoff/runbook:      <ruta usada | none>
Canonical update:     <proyecto/runbook actualizado | none>
```

## Hard Rules

- No matar PIDs supervisados antes de resolver su unidad.
- No repetir `hermes update` sobre un checkout ya movido hasta distinguir code-skew de checkout realmente inconsistente.
- No iniciar gateways duplicados sin comprobar que no comparten credenciales/plataformas.
- No imprimir tokens ni `.env`; presencia y hashes son evidencia suficiente para comparación.
- `HERMES_HOME`, perfil sticky, perfil CLI y unidad systemd son identidades distintas hasta demostrar lo contrario.
- Un warning de `fleet_restart_pending` no vence evidencia funcional fresca; reconciliarlo, no obedecerlo ciegamente.
- Toda limpieza de marker requiere backup y prueba posterior de `PENDING_RESTART = False`.
- No convertir esta skill en runbook: decisiones/triage aquí; comandos mecánicos en [[hermes-linux-update-recovery]].
