---
type: action
schema_version: 1
project:
status: done
created: 2026-08-10
updated: 2026-08-10
tags:
  - kind/action
  - area/aranea
---

## Descripción

Registro histórico de ejecución para [[Aranea]].

## Checklist

- [x] Resultado histórico preservado

---
id: 2026-07-01-017
title: "Healthcheck programado para dashboard Hermes"
type: action
schema_version: 1
status: todo
status_detail: "Backlog del cierre del ticket 014. Crear script/cron que verifique HTTP /api/status, Traefik route, tunnel alive, y alerte si `gui.log` empieza a tirar `origin_mismatch`. Reduce tiempo entre incidentes y refuerza los smoke tests documentados en el runbook."
severity: low
icon: 🎫
slug: 2026-07-01-017-dashboard-healthcheck-script
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-08-10
owner: me
aliases:
  - ticket 017
  - dashboard healthcheck
tags:
  - kind/action
  - area/personal
  - project/agents-os
  - action/ticket
related:
  - "[[2026-07-01-014-hermes-dashboard-bind-loopback-after-update]]"
  - "[[../02-servicios/dashboard-hermes-agent]]"
  - "[[../02-servicios/observabilidad]]"
---

# 2026-07-01-017 — Dashboard healthcheck

## Descripción

Implementar un healthcheck programado para Hermes Dashboard, Traefik, el túnel SSH y las señales `origin_mismatch`.

## Checklist

- [ ] Ejecutar la acción y verificar la evidencia y los riesgos documentados.

## Contexto

El cierre del ticket 014 requiere **smoke tests manuales** cada vez que se cambia algo. Eso no es operacional: el costo de revisar el dashboard después de un update, un reinicio, o un cambio de Traefik debería ser **automatizado y notificado**.

## Acción propuesta

Crear script `~/aranea/bin/dashboard-healthcheck.sh` (o instalar cron via `hermes cron create`) que ejecute cada 5-15 minutos:

```bash
#!/usr/bin/env bash
# 1. Dashboard local HTTP
curl -sS -o /dev/null -w "%{http_code}\n" http://127.0.0.1:9119/api/status
# 2. End-to-end via Traefik
curl -kI -H 'Host: dashboard.lab.aranea' https://192.168.31.11/api/status | head -1
# 3. Tunnel SSH alive (desde Traefik)
timeout 5 ssh agent_traefik_traefik@192.168.31.11 'curl -sS http://127.0.0.1:19119/api/status'
# 4. gui.log: buscar `origin_mismatch` reciente
tail -n 50 ~/.hermes/logs/gui.log | grep -c origin_mismatch
# 5. systemd units estado
systemctl --user is-active hermes-dashboard hermes-gateway
systemctl is-active aranea-traefik-tunnel
```

Salida → alerta a Telegram vía `hermes send` si alguna falla.

## Pendiente

- Owner decide frecuencia del cron (5min vs 15min).
- Owner decide qué falla es "alertable" vs "silent log".
- Skeleton script ya está implícito en el runbook de dashboard.
- Se puede usar como base la skill existente `aranea_agent_ro_inventory_refresh` (cron cada N minutos, escritura silenciosa, alerta solo si algo cambia).
