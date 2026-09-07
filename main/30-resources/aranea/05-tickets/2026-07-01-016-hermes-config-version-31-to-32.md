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
id: 2026-07-01-016
title: "Migrar Hermes config v31 → v32 (gateway_running=false reportado)"
type: action
schema_version: 1
status: todo
status_detail: "Detectado 2026-07-01 04:39 UTC vía /api/status: `config_version: 31, latest_config_version: 32`. Dashboard y chat funcionan con v31; la migración es para alinear la config con lo que la versión actual espera. Requiere sesión dedicada + leer release notes."
severity: low
icon: 🎫
slug: 2026-07-01-016-hermes-config-version-31-to-32
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-08-10
owner: me
aliases:
  - ticket 016
  - config migration
  - hermes config v32
tags:
  - kind/action
  - area/personal
  - project/agents-os
  - action/ticket
related:
  - "[[2026-07-01-014-hermes-dashboard-bind-loopback-after-update]]"
  - "[[../02-servicios/dashboard-hermes-agent]]"
---

# 2026-07-01-016 — Hermes config v31 → v32

## Descripción

Migrar la configuración de Hermes desde v31 a v32 después de revisar las release notes y preparar una sesión dedicada.

## Checklist

- [ ] Ejecutar la acción y verificar la evidencia y los riesgos documentados.

## Contexto

El endpoint `/api/status` reporta:

```json
{
  "version": "0.17.0",
  "release_date": "2026.6.19",
  "config_version": 31,
  "latest_config_version": 32,
  "can_update_hermes": true,
  "gateway_running": false,
  "gateway_state": "stopped",
  "gateway_exit_reason": "Gateway restart requested"
}
```

El update de Hermes introdujo cambios que requirieron nueva config schema (`v32`).

## Side-effects observados

- El dashboard nuevo funciona con v31 (no bloqueante).
- El gateway agent (PIDs 77117 / 79382 anteriormente / 83975 actual) reporta `gateway_running: false` aunque el servicio systemd está `active`.
- **Hipótesis**: la migración a v32 probablemente ajusta cómo se reporta el estado del gateway o agrega campos nuevos. No investigable sin ejecutar `hermes config migrate` (lee release notes upstream).

## Acción

1. **Sesión dedicada** (no mezclar con el incidente 014).
2. Backup de `~/.hermes/config.yaml` y `~/.hermes/.env`.
3. Leer release notes upstream de v32 (`https://hermes-agent.nousresearch.com/docs/changelog` o equivalente).
4. Ejecutar `hermes config migrate` (subcomando inferido; verificar con `hermes --help`).
5. Validar arranque limpio:
   - Gateway arriba
   - Chat funcional
   - `/api/status` reporta `config_version: 32`, `latest_config_version: 32`.
6. Documentar diferencias en este ticket y en runbook.

## Riesgos

- La migración puede cambiar defaults que afecten comportamiento del agent.
- Si la migración toca el gateway, podría reiniciarlo (corte temporal de Telegram).
- Backup roll-backable en 5 min si hay sorpresa.

## Pendiente

- Owner decide cuándo hacerlo.
- No bloqueante para el dashboard (ya funciona con override de env vars).
