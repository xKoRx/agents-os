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
id: 2026-07-01-014
title: "Hermes Dashboard muerto tras update v0.17.0 — recovery completo"
type: action
schema_version: 1
status: done
status_detail: "✅ Cerrado 2026-07-01 16:48 UTC. Cuatro fixes aplicados en orden: (A) bind loopback en unit dashboard; (B) tunnel system-service sin 216/GROUP; (C) Traefik `passHostHeader:false` + URL tunnel; (D) Traefik `hermes-dashboard-origin-rewrite` middleware; (E) drop-in override con env vars y `--open-profile ariadna`. Owner confirmó chat funcional desde Safari. DNS y config v31→v32 siguen abiertos como tickets separados."
severity: medium
icon: 🎫
slug: 2026-07-01-014-hermes-dashboard-bind-loopback-after-update
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-08-10
closed: 2026-07-01
owner: me
executor: ariadna
aliases:
  - ticket 014
  - ticket dashboard-bind
  - ticket dashboard-recovery
tags:
  - kind/action
  - area/personal
  - project/agents-os
  - action/ticket
related:
  - "[[2026-06-29-008-dashboard-no-password-via-reverse-tunnel]]"
  - "[[2026-06-29-007-expose-dashboard-via-traefik]]"
  - "[[2026-07-01-015-dashboard-dns-ariadne-to-traefik]]"
  - "[[2026-07-01-016-hermes-config-version-31-to-32]]"
  - "[[2026-07-01-017-dashboard-healthcheck-script]]"
  - "[[../../02-servicios/dashboard-hermes-agent]]"
  - "[[../../../80-agents/memory/public/learning/aranea/hermes-dashboard-reverse-proxy-websocket-origin]]"
  - "[[../../../80-agents/memory/public/learning/aranea/hermes-dashboard-systemd-source-of-truth]]"
  - "[[../../../80-agents/journal/sessions/2026-07-01-1130-hermes-dashboard-post-update-recovery-summary]]"
---

# 2026-07-01-014 — Hermes Dashboard recovery post-update v0.17.0 (CLOSED)

## Descripción

Recuperar Hermes Dashboard después del update v0.17.0 y validar el acceso completo mediante Traefik y el túnel.

## Checklist

- [x] Acción ejecutada y validada; causas, fixes y evidencia permanecen documentados abajo.

## Contexto

Owner reportó el 2026-07-01: "el dashboard de hermes no carga, murió después del update de hermes". Análisis posterior descubrió 4 causas concurrentes que se enmascaraban mutuamente. Cierre tras 5 iteraciones de fix.

## Causas raíz (4 concurrentes)

### C1 — Auth hardening post-update v0.17.0

`v0.17.0 / 2026.6.19` deprecó `--insecure` y endureció binds no-loopback. El unit `hermes-dashboard.service` quedó apuntando a `--host 0.0.0.0` → loop de restarts → systemd apagó el service (`start-limit-burst`).

### C2 — Dos fuentes de verdad

Existía un proceso manual (`PID 79382`, 03:01) con flags distintos al unit (`-p default dashboard --open-profile ariadna --no-open` con env heredado del agent gateway, no del unit). Debugging ambiguo.

### C3 — Traefik apuntaba a config del ticket 007

`aranea-dashboard.yaml` quedó con valores del ticket **007** original:
- URL: `http://192.168.31.122:9119` (Hermes directo, no tunnel)
- Sin `passHostHeader: false`
- Sin `hermes-host-rewrite` middleware

Resultado: HTTP devolvía **502 Bad Gateway**.

### C4 — Tunnel system-service needed

`hermes-tunnel-traefik.service` (user) tenía `status=216/GROUP` en loop infinito. Documentado como "pendiente" en ticket 008 pero no resuelto.

### C5 — WebSocket origin mismatch

Post-fix C3 (Traefik pasa `Host` al backend), el browser abre WebSocket con `Origin: https://dashboard.lab.aranea`. Dashboard bindeado a `127.0.0.1` rechaza con **4403 origin_mismatch**. El middleware `hermes-host-rewrite@file` documentado en ticket 008 nunca estuvo aplicado.

### C6 — Chat embebido con env vars faltantes

Una vez resuelto C5, el chat tab lanza `GatewayClient.start()` → `startSpawnedGateway()` (porque `profile=ariadna` omite `HERMES_TUI_GATEWAY_URL` por aislamiento) → `spawn(python, ...)` con `python=undefined` por env vars faltantes (`HERMES_PYTHON_SRC_ROOT`, `HERMES_PYTHON`, PATH sin Hermes Node primero).

## Resolución (5 fixes aplicados en orden)

### Fix A — Bind loopback en unit

```diff
ExecStart=... dashboard --host 0.0.0.0 --port 9119 --no-open
+ ExecStart=... dashboard --host 127.0.0.1 --port 9119 --no-open
```

`daemon-reload` + `reset-failed` aplicado. Start pendiente por hook del gateway.

### Fix B — Tunnel system-service

Migrado a `/etc/systemd/system/aranea-traefik-tunnel.service`:
- `User=hermes`, `Group=hermes`
- `Restart=always`, `RestartSec=10`, `StartLimitIntervalSec=300`, `StartLimitBurst=10`
- `ExecStart=/usr/bin/ssh -N -T ...` con key dedicada
- Wrapper bash innecesario (systemd como PID 1 puede resolver grupos)

Backup del process de SSHH uérfanos en Traefik (PIDs 22241, 22262 del user-session anterior) requerido por el dueño en el host Traefik antes del `kill`.

### Fix C — Traefik `passHostHeader: false` + URL tunnel

Apply CHANGE_ID `dashboard-passhost-false-2026-07-01`. Backup `20260701-012306`.

```diff
services:
  hermes-dashboard:
    loadBalancer:
-     passHostHeader: true
+     passHostHeader: false
      servers:
-       - url: "http://192.168.31.122:9119"
+       - url: "http://127.0.0.1:19119"
```

**Criterio del owner**: `passHostHeader: false` antes que middleware es preferible (más limpio). Si no funciona, recurrir a header rewrite middleware.

### Fix D — Traefik middleware Origin rewrite

Apply CHANGE_ID `dashboard-origin-rewrite-2026-07-01`. Backup `20260701-015400`.

```yaml
http:
  middlewares:
    hermes-dashboard-origin-rewrite:
      headers:
        customRequestHeaders:
          Origin: "http://127.0.0.1:19119"

  routers:
    hermes-dashboard:
      middlewares:
        - lan-only@file
        - hermes-dashboard-origin-rewrite@file
```

Browser sigue enviando `Origin: dashboard.lab.aranea` (no controlable); Traefik lo reemplaza antes de pasar al backend (`bound_host=127.0.0.1`).

### Fix E — Drop-in override del dashboard

Creado `~/.config/systemd/user/hermes-dashboard.service.d/override.conf`:

```ini
[Service]
WorkingDirectory=/home/hermes
Environment="HERMES_HOME=/home/hermes/.hermes"
Environment="HERMES_PYTHON_SRC_ROOT=/home/hermes/.hermes/hermes-agent"
Environment="HERMES_PYTHON=/home/hermes/.hermes/hermes-agent/venv/bin/python"
Environment="PATH=/home/hermes/.hermes/node/bin:/home/hermes/.local/bin:/home/hermes/bin:/home/hermes/.hermes/hermes-agent/venv/bin:/home/hermes/.hermes/hermes-agent/node_modules/.bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=
ExecStart=/home/hermes/.hermes/hermes-agent/venv/bin/python -m hermes_cli.main -p default dashboard --host 127.0.0.1 --port 9119 --open-profile ariadna --no-open
```

Backup del unit base: `~/reset-backups/hermes-dashboard.service.before-env-profile-20260701-164244.txt`.

Proceso manual PID 79382 terminado (`kill -TERM` → murió limpiamente). Unit levantado con `systemctl --user enable --now`.

## Validación final

| Check | Resultado |
|---|---|
| `hermes-dashboard.service` | active (PID 83975, Main PID 83975) |
| `hermes-gateway.service` | active (PID 77117, intacto desde 01:38) |
| `aranea-traefik-tunnel.service` | active (PID 80754) |
| Drop-in override cargado | `/home/hermes/.config/systemd/user/hermes-dashboard.service.d/override.conf` |
| `curves -k -H 'Host: dashboard.lab.aranea' https://192.168.31.11/api/status` | HTTP 200, JSON response OK |
| `/` HTML title | `Hermes Agent - Dashboard` ✅ |
| PTY WebSocket | `pty accepted peer=127.0.0.1 mode=loopback cred=token` ✅ |
| Owner test en Safari | chat abierto, sin `paths[0] undefined` ✅ |
| HTTP backend loopback Traefik (vía tunnel) | 200 OK desde `192.168.31.11` (loopback Traefik) |

## Archivos tocados

| Path | Cambio |
|---|---|
| `~/.config/systemd/user/hermes-dashboard.service` | bind `0.0.0.0` → `127.0.0.1` (parche inicial) |
| `~/.config/systemd/user/hermes-dashboard.service.bak.1782873265` | backup del parche inicial |
| `~/.config/systemd/user/hermes-dashboard.service.d/override.conf` | NUEVO drop-in (Fix E) |
| `~/reset-backups/hermes-dashboard.service.before-env-profile-20260701-164244.txt` | backup del unit antes del drop-in |
| `/etc/systemd/system/aranea-traefik-tunnel.service` | NUEVO system-service (Fix B) |
| `/etc/traefik/dynamic/aranea-dashboard.yaml` | Fix C + Fix D aplicados vía wrapper |
| `/var/lib/aranea/traefik/backups/20260701-012306/` | backup Traefik post-fix C |
| `/var/lib/aranea/traefik/backups/20260701-015400/` | backup Traefik post-fix D |

## Pendientes para el cierre definitivo (otros tickets)

- **`2026-07-01-015`** — DNS: `dashboard.lab.aranea` → `192.168.31.122` en vez de `192.168.31.11`. Revisar zona DNS.
- **`2026-07-01-016`** — Hermes config v31 → v32. Ejecutar `hermes config migrate` en sesión dedicada.
- **`2026-07-01-017`** — Healthcheck programado para el dashboard (HTTP + Traefik + tunnel + GUI log patterns).

## Lecciones (5)

1. **Antes de proponer fix, buscar en `session_search` + filesystem (tickets).** El approach canónico del ticket 008 era correcto pero nunca lo leí hasta que vos me corregiste. No reinventar.
2. **Una fuente de verdad: el unit systemd.** No dejar procesos manuales compitiendo.
3. **`passHostHeader: false` antes que middleware de rewrite** (criterio del owner). Más limpio, menos magia.
4. **WebSocket requiere validación separada de HTTP.** Tres gates: `_ws_auth_reason`, `_ws_host_origin_reason`, `_ws_client_reason` — cada una con código de close distinto (4401/4403/4408).
5. **Drop-in override > modificar unit base** para preservar paridad con el agente y revertir fácil.

## Métricas

- Tickets creados en sesión: 4 (014 + 3 follow-ups)
- Fixes Traefik aplicados: 2 (con backup automático del wrapper)
- Backup del unit: 3 archivos persistidos
- Skill generada: 1 (`hermes-dashboard-recovery`)
- Learnings: 2 (reverse-proxy-websocket-origin, systemd-source-of-truth)
- Service files nuevos: 1 (`aranea-traefik-tunnel.service` system)
- Drop-in override: 1 (`hermes-dashboard.service.d/override.conf`)
- Sin secretos publicados en tickets: ninguno
- Owner confirmaciones: 6 (incluyendo "funcionó")
