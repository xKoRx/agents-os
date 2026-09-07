---
type: session
scope: session
status: closed
status_detail: "Sesión abierta 2026-07-01, cerrada limpia 2026-07-01 16:48 UTC. Owner confirmó en Safari que el chat funciona. Ticket 014 cerrado. 3 tickets follow-up abiertos (DNS, config v31→v32, healthcheck). 2 learnings creados. Runbook + skill reescritos."
created: "2026-07-01"
updated: "2026-07-01"
closed: "2026-07-01T16:48:00Z"
session_id: "2026-07-01-1130-hermes-dashboard-post-update-recovery"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
tags:
  - session
  - incident
  - hermes
  - dashboard
  - loopback
  - auth-hardening
  - post-update
  - aranea
  - area/personal
  - project/agents-os
source_files:
  - "[[2026-07-01-1130-hermes-dashboard-post-update-recovery-raw]]"
  - "[[../../../../../../../../home/hermes/obsidian/SecondBrain/main/30-resources/aranea/02-servicios/dashboard-hermes-agent]]"
  - "[[../../../../../../../../home/hermes/obsidian/SecondBrain/main/30-resources/aranea/05-tickets/2026-07-01-014-hermes-dashboard-bind-loopback-after-update]]"
load_policy: manual
indexable: true
index_priority: high
aliases:
  - hermes-dashboard-recovery-2026-07-01
  - dashboard-post-update
---

# 📓 2026-07-01 — Hermes Dashboard recovery post-update v0.17.0

## TL;DR

Owner pidió recuperar el dashboard que murió tras un `hermes update`. **El
approach canónico ya existía documentado** (ticket 008 del 2026-06-29) — solo
había que reaplicarlo. Fix parcial aplicado al unit, **owner debe ejecutar el
`start` desde una shell externa** (el hook del gateway bloquea auto-restart).

## Goal

Recuperar `https://dashboard.lab.aranea` sin passwords, después de que un
update de Hermes dejó el service `hermes-dashboard` en `dead`.

## Hallazgos clave

### 1. La causa raíz NO era del infra — era del update

- v0.17.0 del 2026.6.19 endureció auth: `--insecure` deprecado, **cualquier
  bind no-loopback requiere auth provider registrado**.
- `hermes-dashboard.service` quedó con `--host 0.0.0.0` (generado antes del
  hardening).
- Cada restart: `Refusing to bind dashboard to 0.0.0.0 — the auth gate engages
  on non-loopback binds`. Loop hasta `StartLimitBurst=5` → `dead`.

### 2. El approach canónico ya existía y NO debíamos reinventarlo

El usuario me corrigió a tiempo: *"me parece que habíamos bindeado la ip local
no?? revisa en el historial"*. Sin esa corrección, habría propuesto cambios
nuevos.

**Búsqueda en `session_search` + filesystem** encontré:

- Ticket `2026-06-29-008-dashboard-no-password-via-reverse-tunnel.md`
  (status: applied) — paso 5 exactamente: cambiar `--host 0.0.0.0` →
  `--host 127.0.0.1` + tunnel SSH reverso a Traefik.
- El unit `hermes-tunnel-traefik.service` ya estaba bien (status actual:
  `activating` — enganchado al dashboard dead).
- `config.yaml` sin bloque `dashboard.basic_auth` (correcto post-ticket 008).

### 3. Limitación operacional nueva: hook del gateway bloquea auto-restart

Tercera corrección crítica del environment. El agente Hermes tiene un hook
de seguridad que rechaza `systemctl --user {start|stop|restart}` desde dentro
del proceso gateway (mataría el agent antes del comando → systemd inconsistente).

```
Blocked: cannot restart or stop the gateway from inside the gateway process.
The gateway would kill this command before it could complete (SIGTERM
propagates to child processes). Run `hermes gateway restart` from a separate
shell outside the running gateway.
```

Comandos que **SÍ funcionaron desde dentro**:
- `cp` del unit (backup)
- `sed`/`patch` al ExecStart
- `systemctl --user daemon-reload`
- `systemctl --user reset-failed hermes-dashboard`

Comandos que **NO funcionaron**:
- `systemctl --user start hermes-dashboard.service` (hook)

**Implicancia**: el dashboard no se puede auto-remediar desde la sesión del
agent actual. Owner debe ejecutarlo desde otra shell/SSH/sesión.

## Acciones ejecutadas

| # | Acción | Resultado |
|---|---|---|
| 1 | Diagnosticado dead state via `systemctl --user show` y `journalctl -u hermes-dashboard -n 60` | ✅ |
| 2 | Confirmado approach vía `session_search` + filesystem | ✅ |
| 3 | Backup del unit: `hermes-dashboard.service.bak.1782873265` | ✅ |
| 4 | Patch del ExecStart: `--host 0.0.0.0` → `--host 127.0.0.1` | ✅ |
| 5 | `systemctl --user daemon-reload` | ✅ exit 0 |
| 6 | `systemctl --user reset-failed hermes-dashboard` | ✅ exit 0 |
| 7 | `systemctl --user start hermes-dashboard.service` | ❌ hook bloqueó |

## Pendiente para el owner

```bash
# Desde otra shell (o próxima sesión del agent):

systemctl --user start hermes-dashboard.service
systemctl --user status hermes-dashboard.service --no-pager

# 3 validaciones de salud:
curl -sS -o /dev/null -w "HTTP %{http_code}\n" http://127.0.0.1:9119/
systemctl --user is-active hermes-tunnel-traefik   # tiene que pasar de activating a active
curl -k -sS -o /dev/null -w "HTTP %{http_code}\n" \
  -H 'Host: dashboard.lab.aranea' --max-time 5 \
  https://dashboard.lab.aranea/
```

Resultado esperado: `active` + `200` + `active` + `200`.

## Decisiones tomadas

| # | Decisión | Por qué |
|---|---|---|
| D1 | NO usar `--insecure` (deprecado) | No existe en v0.17, error garantizado |
| D2 | NO agregar `dashboard.basic_auth` interno | Tu arquitectura (ticket 008) elimina doble auth |
| D3 | NO tocar `hermes-tunnel-traefik.service` | Ya está correcto, solo espera al dashboard |
| D4 | NO tocar `config.yaml` | Ya está sin bloque `dashboard.basic_auth` |
| D5 | Reutilizar el approach del ticket 008 | Owner lo confirmó después de corregir la propuesta inicial |

## Outputs / artefactos creados

- `[[2026-07-01-1130-hermes-dashboard-post-update-recovery-raw]]` — bitácora cruda
- `[[../../30-resources/aranea/05-tickets/2026-07-01-014-hermes-dashboard-bind-loopback-after-update]]` — ticket
- `[[../../30-resources/aranea/02-servicios/dashboard-hermes-agent]]` — runbook canónico
- Update a `[[../../30-resources/aranea/05-tickets/README]]` (índice)

## Lecciones (para skill `hermes-dashboard-bind-loopback-post-update`)

1. **Antes de proponer, buscar en `session_search` y filesystem**. Mi primer
   impulso fue proponer cambios nuevos — el owner me paró a tiempo.
2. **Después de `hermes update`, revisar unit files**. v0.17.0 endureció auth
   sin avisar a los service files.
3. **Hook del gateway bloquea self-restart**. Documentado en la nota del
   runbook. Owner debe ejecutar start desde fuera.
4. **`config.yaml` puede tener bloque `dashboard:` vacío intencionalmente** —
   no es "config incompleto", es el approach "loopback + tunnel" canónico.
5. **`--insecure` eliminado en v0.17.0** — antes era un workaround, ahora
   hay que ir por el camino correcto (loopback + tunnel).

## Follow-ups

- [ ] **CRÍTICO**: owner ejecuta `start` externo y valida los 3 endpoints
- [ ] Cuando confirme OK, agregar a `runbook-incidentes.md`
- [ ] Indexar el ticket 014 en `00-index.md` handover (cuando se apruebe el fix cerrado)
- [ ] Crear skill `hermes-dashboard-bind-loopback-post-update` (al cerrar ticket)
- [ ] Considerar mover el ticket 014 a `closed` con output real del fix

## Métricas

- **Turnos de conversación**: ~10 (incluye los 3 de clarificación)
- **Comandos ejecutados**: ~25
- **Archivos creados/modificados**: 4 (runbook, ticket, README index, raw)
- **Bloqueos del hook**: 1 (start) — esperado y documentado
- **Inventos detectados por el owner**: 1 (propuesta inicial antes de buscar en historial)
