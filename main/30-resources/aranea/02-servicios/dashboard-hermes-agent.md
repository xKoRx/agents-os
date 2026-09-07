---
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
related: []
aliases: []
tags:
  - kind/doc
created: 2026-08-10
updated: 2026-08-10
---

# 🐍 Hermes Agent Dashboard — runbook canónico

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


## 🎯 Estado final conocido bueno (post-incidente 2026-07-01)

Arquitectura funcionando **al cierre de sesión**:

```text
Safari (browser)
  ↓ https://dashboard.lab.aranea:443
Traefik (192.168.31.11) — router hermes-dashboard
  ├─ lan-only@file              (filtra LAN 192.168.31.0/24)
  ├─ hermes-dashboard-origin-rewrite@file  (reescribe Origin al loopback del backend)
  ├─ tls.certResolver: stepca   (cert step-ca, válido)
  ↓ http://127.0.0.1:19119  (loopback de Traefik)
SSH reverse tunnel
  Servicio systemd de sistema: aranea-traefik-tunnel.service
  Comando: ssh -N -T -R 127.0.0.1:19119:127.0.0.1:9119 \
                   agent_traefik_tunnel@192.168.31.11
  ↓
Hermes VM 127.0.0.1:9119
  Fuente de verdad: hermes-dashboard.service (user systemd unit)
  Comando: /home/hermes/.hermes/hermes-agent/venv/bin/python \
           -m hermes_cli.main -p default dashboard \
             --host 127.0.0.1 --port 9119 --open-profile ariadna --no-open
  Env vars (heredadas del unit drop-in override.conf):
    HERMES_HOME=/home/hermes/.hermes
    HERMES_PYTHON_SRC_ROOT=/home/hermes/.hermes/hermes-agent
    HERMES_PYTHON=/home/hermes/.hermes/hermes-agent/venv/bin/python
    PATH=/home/hermes/.hermes/node/bin:...  (Hermes Node primero)
```

**Tabla de servicios vivos al cierre** (verificado 2026-07-01 16:48 UTC):

| Servicio | Scope | Estado | PID |
|---|---|---|---|
| `hermes-dashboard.service` | user | active | 83975 |
| `hermes-gateway.service` | user | active | 77117 |
| `aranea-traefik-tunnel.service` | system | active | 80754 |
| `aranea-traefik-apply` (Traefik) | root | active | traefik.pid |

---

## 🔧 Configuración relevante

### `hermes-dashboard.service` (user unit)

Archivo base: `~/.config/systemd/user/hermes-dashboard.service`

```ini
[Unit]
Description=Hermes Dashboard
After=network.target

[Service]
Type=simple
ExecStart=/home/hermes/.hermes/hermes-agent/venv/bin/hermes dashboard \
  --host 127.0.0.1 --port 9119 --no-open
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
```

Drop-in override (fuente de verdad operativa):

`~/.config/systemd/user/hermes-dashboard.service.d/override.conf`

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

> ⚠️ El override añade las 4 Environment vars, redefine ExecStart (con `-m hermes_cli.main` directo + `--open-profile ariadna`), y resetea el anterior con `ExecStart=` (línea vacía). El bloque `WorkingDirectory=/home/hermes` mantiene paridad con el agent gateway.

### `aranea-traefik-tunnel.service` (system unit)

`/etc/systemd/system/aranea-traefik-tunnel.service`

```ini
[Unit]
Description=Aranea reverse SSH tunnel (Hermes dashboard -> Traefik)
Documentation=tag/2026-07-01-014
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=300
StartLimitBurst=10

[Service]
Type=simple
User=hermes
Group=hermes
ExecStart=/usr/bin/ssh -N -T \
  -i /home/hermes/.ssh/agent_traefik_tunnel_dashboard \
  -o IdentitiesOnly=yes \
  -o ExitOnForwardFailure=yes \
  -o ServerAliveInterval=30 \
  -o ServerAliveCountMax=3 \
  -o StrictHostKeyChecking=accept-new \
  -R 127.0.0.1:19119:127.0.0.1:9119 \
  agent_traefik_tunnel@192.168.31.11
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

> Migrado desde user-service con `216/GROUP` a system-service. Systemd como PID 1 puede resolver el grupo `hermes` sin restricciones.

### Traefik — `/etc/traefik/dynamic/aranea-dashboard.yaml`

```yaml
http:
  routers:
    hermes-dashboard:
      rule: "Host(`dashboard.lab.aranea`)"
      entryPoints:
        - websecure
      service: hermes-dashboard
      middlewares:
        - lan-only@file
        - hermes-dashboard-origin-rewrite@file
      tls:
        certResolver: stepca

  services:
    hermes-dashboard:
      loadBalancer:
        passHostHeader: false
        servers:
          - url: "http://127.0.0.1:19119"

  middlewares:
    hermes-dashboard-origin-rewrite:
      headers:
        customRequestHeaders:
          Origin: "http://127.0.0.1:19119"
```

**Notas**:

- `passHostHeader: false` hace que Traefik reescriba el `Host` al del server URL.
- `hermes-dashboard-origin-rewrite@file` reescribe el `Origin` porque los browsers WebSocket envían `Origin` por su cuenta; el dashboard Hermes, bindeado a `127.0.0.1`, rechaza cualquier `Origin` que no matchee con `127.0.0.1` (devuelve **4403 origin_mismatch**).
- Estos dos reescritos hacen que el navegador vea `dashboard.lab.aranea` mientras que el backend ve `127.0.0.1:9119`.

---

## 💥 Causas raíz del incidente (resumen postmortem)

Cuatro causas concurrentes se enmascararon mutuamente. Cada una aislada se ve "menos grave"; juntas, lo tumbaron todo:

### C1 — Update Hermes v0.17.0 endureció bind + auth

Junio 2026 release (`v0.17.0 / 2026.6.19`) introdujo:
- `--insecure` deprecado y eliminado.
- Bind a IP no-loopback requiere auth provider registrado.
- Refuerza de validación `Host`/`Origin` en WebSocket (`_ws_host_origin_reason` en `gatewayClient.ts`).

`hermes-dashboard.service` no se actualizó automáticamente. Mientras el unit quedó con `--host 0.0.0.0`, el dashboard reventaba en restart loop.

### C2 — Dos fuentes de verdad del dashboard

Existía un proceso manual corriendo desde las 03:01 con flags distintos a los del unit:

| Aspecto | Proceso manual (PID 79382) | Unit systemd |
|---|---|---|
| Comando | `... dashboard --port 9119 --host 127.0.0.1 --open-profile ariadna` | `... dashboard --port 9119 --host 127.0.0.1` (sin profile) |
| Env vars | Heredadas del gateway agent (sin `HERMES_PYTHON_SRC_ROOT`) | Ninguna por defecto |

Esto produjo debugging ambiguo: cambios al unit no afectaban al proceso real, y al matar PID 79382 se rompió la sesión ariadna activa.

### C3 — Traefik apuntaba a config antigua

`aranea-dashboard.yaml` quedó con valores del ticket **007**, no del **008**:

| Aspecto | Ticket 007 (viejo) | Ticket 008 (correcto) | Estado pre-fix |
|---|---|---|---|
| Backend URL | `http://192.168.31.122:9119` (Hermes directo) | `http://127.0.0.1:19119` (vía tunnel) | **007** ❌ |
| `passHostHeader` | `true` | `true` | **007** ✅ |
| Host rewrite middleware | no | sí | **007** ❌ |

Resultado: HTTP devolvía **502 Bad Gateway** porque la URL era inalcanzable y el dashboard bindeado local.

### C4 — Tunnel SSH `216/GROUP` en user service

El unit systemd user `hermes-tunnel-traefik.service` no podía resolver supplementary groups del usuario `hermes`, generando `status=216/GROUP`. **Eso estaba documentado como "Pendiente" en el ticket 008** pero nunca se resolvió. La única forma de continuar era el wrapper bash que setea `USER_GROUPS` manualmente — frágil, huérfano tras reinicios.

Causa real: el unit era user-service; system-services no tienen esta restricción.

---

## 🚨 Síntomas → Causa → Fix

| Síntoma | Causa raíz | Fix aplicado |
|---|---|---|
| `hermes-dashboard.service` en `dead`, logs muestran `Refusing to bind dashboard to 0.0.0.0` | C1 (auth hardening post-update) | Cambiar `ExecStart` a `--host 127.0.0.1` (loopback) |
| `aranea-traefik-tunnel.service` en restart-loop infinito (216/GROUP) | C4 (user-service limit) | Migrar a `/etc/systemd/system/aranea-traefik-tunnel.service` (system-service) |
| `curl https://192.168.31.11/api/status` → **502 Bad Gateway** | C3 (Traefik URL incorrecta) | Fix apply `dashboard-passhost-false-2026-07-01`: URL → `http://127.0.0.1:19119`, `passHostHeader: false` |
| WebSocket cierra con **4403 origin_mismatch**: `origin=https://dashboard.lab.aranea bound=127.0.0.1` | C1 (binding mismatch) + falta de reescritura Origin | Fix apply `dashboard-origin-rewrite-2026-07-01`: middleware `hermes-dashboard-origin-rewrite@file` con `headers.customRequestHeaders.Origin: http://127.0.0.1:19119` |
| Chat (PTY) crashea con `TypeError [ERR_INVALID_ARG_TYPE]: paths[0] undefined` (Node 18 stack) | C2 + C1 upgrade: `startSpawnedGateway()` falla por env vars faltantes (HERMES_PYTHON_SRC_ROOT, HERMES_PYTHON, PATH Hermes Node) | Drop-in override en `~/.config/systemd/user/hermes-dashboard.service.d/override.conf` con las 4 Environment vars + redefine ExecStart con `-m hermes_cli.main` directo y `--open-profile ariadna` |
| `systemctl is-active` dice `active` pero dashboard falla en chat | Validación insuficiente: `active` ≠ funcional | Smoke test real: HTTP + WebSocket PTY + chat end-to-end |

---

## 🧪 Smoke tests obligatorios (no cerrar nada sin ellos)

Antes de declarar cualquier cambio como "resuelto", ejecutar **todos** estos checks. `active` solo no alcanza.

### Comandos shell

```bash
# 1. Estado de los 3 servicios
systemctl --user status hermes-dashboard.service --no-pager -l
systemctl --user status hermes-gateway.service --no-pager -l
systemctl status aranea-traefik-tunnel.service --no-pager -l

# 2. Health HTTP local (dashboard en Hermes)
curl -sS http://127.0.0.1:9119/api/status | jq '{gateway_running, gateway_state, config_version, latest_config_version}'

# 3. Health HTTP backend-via-tunnel (probar SOLO desde Traefik mismo, no desde Hermes)
#    Desde Traefik (192.168.31.11):
#    curl -sS http://127.0.0.1:19119/api/status | jq '.version, .gateway_state'

# 4. Health HTTP end-to-end via Traefik
curl -kIv -H 'Host: dashboard.lab.aranea' https://192.168.31.11/api/status
curl -kI -H 'Host: dashboard.lab.aranea' https://192.168.31.11/

# 5. Validar env vars en el PID nuevo (debe tener HERMES_PYTHON_SRC_ROOT y PATH con Hermes Node primero)
PID=$(pgrep -u hermes -f 'hermes_cli.main.*dashboard.*9119' | head -1)
tr '\0' '\n' < /proc/$PID/environ | grep -E '^(HERMES_HOME|HERMES_PYTHON_SRC_ROOT|HERMES_PYTHON|PATH)='
```

### Validación manual final (la única confiable)

1. Abrir **Safari** (u otro browser).
2. Navegar a `https://dashboard.lab.aranea`.
3. Esperar a que cargue el dashboard (HTML title: `Hermes Agent - Dashboard`).
4. Abrir la pestaña **Chat**.
5. Confirmar que **no aparece** el error:
   > `TypeError [ERR_INVALID_ARG_TYPE]: The "paths[0]" argument must be of type string. Received undefined`
6. Confirmar en `~/.hermes/logs/gui.log` que aparece:
   > `pty accepted peer=127.0.0.1 mode=loopback cred=token`

Si **todas** esas pasan, el dashboard es operativo.

---

## 📋 Logs útiles (en orden de sospecha)

```bash
# 1. WebSocket + PTY rejections (causa más común post-fix Traefik)
tail -n 200 ~/.hermes/logs/gui.log

# 2. Errors generales del agent
tail -n 200 ~/.hermes/logs/errors.log

# 3. Gateway Telegram (no debe confundirse con dashboard)
tail -n 200 ~/.hermes/logs/gateway.log

# 4. Tunnel SSH reverse a Traefik
journalctl -u aranea-traefik-tunnel.service -n 100 --no-pager

# 5. Unit del dashboard (si arrancó de nuevo)
systemctl --user status hermes-dashboard.service --no-pager -l
```

Patrones clave a buscar:

| Buscar | Significado |
|---|---|
| `origin_mismatch` | (HTTP-fix) WebSocket rechazado por mismatch de Origin |
| `host_mismatch` | (HTTP-fix) WebSocket rechazado por mismatch de Host |
| `Failed to determine supplementary groups` | unit user-service con 216/GROUP (debe migrarse a system) |
| `Refusing to bind dashboard` | unit con `--host 0.0.0.0` post-update (debe ser `--host 127.0.0.1`) |
| `paths[0]` / `ERR_INVALID_ARG_TYPE` | (chat fix) env vars faltantes en drop-in override |
| `pty accepted` | ✅ WebSocket PTY válido |
| `pty refused` | ❌ alguna de las gates (_ws_auth_reason, _ws_host_origin_reason, _ws_client_reason) rechazó |

---

## ❌ Anti-patrones aprendidos

1. **No declarar "resuelto" solo porque `systemctl is-active` dice `active`.** El hook del gateway miente: `active (running)` puede coexistir con proceso staled (e.g. ssh PID con forward fallido). Siempre smoke test.

2. **No validar el túnel `-R 127.0.0.1:19119` desde Hermes contra `192.168.31.11:19119`.** Ese listener vive en loopback de **Traefik**, no es reachable desde Hermes. Si lo intentás, obtienes `connection refused` y confundís la causa raíz.

3. **No dejar procesos manuales vivos compitiendo con systemd.** El debugging se vuelve ambiguo. Solo una fuente de verdad: el unit.

4. **No mezclar en un mismo cierre: DNS, Traefik, túnel, dashboard, gateway migration.** Atomiza. Si falla uno, sabés qué. Si combinas, no sabés qué.

5. **WebSocket requiere validación separada de HTTP.** HTTP 200 no garantiza WebSocket 200. Hay gates adicionales (`_ws_host_origin_reason`, `_ws_auth_reason`) que solo aplican a upgrades.

6. **Si el dashboard usa profile explícito, preservar `--open-profile <name>` en el unit.** El state del perfil ariadna vive en `~/.hermes/profiles/ariadna/`. Sin el flag, el dashboard arranca con perfil default y pierde contexto de sesión.

7. **No usar `--insecure` post v0.17.0** (deprecado). Si el unit lo trae, el dashboard NO va a bindear a `0.0.0.0` con auth.

---

## ↩️ Rollback (NO ejecutar; solo documentar)

Cada cambio es **independiente y reversible** vía backup.

| Cambio | Backup | Rollback |
|---|---|---|
| `aranea-dashboard.yaml` fix A (`passHostHeader: false`) | `20260701-012306` | `sudo aranea-traefik-apply apply <backup_id>` (wrapper provee `list-backups`) |
| `aranea-dashboard.yaml` fix B (Origin rewrite middleware) | `20260701-015400` | mismo |
| Drop-in override del dashboard | `~/reset-backups/hermes-dashboard.service.before-env-profile-20260701-164244.txt` | `sudo systemctl --user revert hermes-dashboard.service.d/` (o `rm -rf ~/.config/systemd/user/hermes-dashboard.service.d/` + `daemon-reload`) |
| `aranea-traefik-tunnel.service` (system) | (no backup; reescritura a partir del user-service) | `sudo systemctl disable --now aranea-traefik-tunnel.service` + rehabilitación del unit user previo |

Verificar config efectiva antes de tocar:

```bash
# Dashboard unit merge (base + drop-in)
systemctl --user cat hermes-dashboard.service

# Tunnel unit
sudo systemctl cat aranea-traefik-tunnel.service

# Traefik dynamic config
sudo cat /etc/traefik/dynamic/aranea-dashboard.yaml
```

---

## ⏭️ Pendientes / follow-ups (tickets separados)

Tickets abiertos como seguimiento, **NO bloqueantes** del fix del dashboard:

1. **`2026-07-01-015-dashboard-dns-ariadne-to-traefik`** — `dashboard.lab.aranea` resuelve a `192.168.31.122` (Hermes directo). Debería apuntar a `192.168.31.11` (Traefik). Safari desde LAN hoy funciona por suerte (Traefik responde en :443 desde LAN), pero en otros escenarios (otros devices, mobile fuera de casa vía WireGuard, etc) va a fallar. **Acción**: revisar `dns-tls.md` y zona DNS (probablemente en Pi-hole en athena).
2. **`2026-07-01-016-hermes-config-version-31-to-32`** — `/api/status` reporta `config_version: 31, latest_config_version: 32`. Investigar `hermes config migrate` o el equivalente oficial. **Acción**: leer `~/.hermes/check_update_state` o equivalente, correr migrate en sesión dedicada.
3. **`2026-07-01-017-dashboard-healthcheck-script`** — Crear cron / script que verifique HTTP /api/status, Traefik route status, tunnel `19119` reachable desde Traefik, y alerta si `gui.log` empieza a tirar `origin_mismatch`. **Acción**: nueva skill/cron tras cerrar el incidente principal.
4. **Investigación upstream Hermes** — ¿Hay flag oficial `allowed_hosts` / `public_url` / `trusted_proxy` en v0.17.0 que acepte `dashboard.lab.aranea` como hostname válido y elimine el middleware de Origin rewrite? **Acción**: revisar release notes upstream, abrir issue si aplica.

---

## 🔗 Referencias

- Tickets del sistema:
  - [[../05-tickets/2026-06-29-007-expose-dashboard-via-traefik|2026-06-29-007]]: exposición inicial con doble auth
  - [[../05-tickets/2026-06-29-008-dashboard-no-password-via-reverse-tunnel|2026-06-29-008]]: túnel reverso SSH (loopback + tunnel)
  - [[../05-tickets/2026-07-01-014-hermes-dashboard-bind-loopback-after-update|2026-07-01-014]]: este incidente
- Source files: rutas de unit files, `/etc/traefik/dynamic/aranea-dashboard.yaml`, `/home/hermes/.config/systemd/user/hermes-dashboard.service.d/override.conf`
- Learnings: [[../../../80-agents/memory/public/learning/aranea/hermes-dashboard-reverse-proxy-websocket-origin|reverse-proxy-websocket-origin]] y [[../../../80-agents/memory/public/learning/aranea/hermes-dashboard-systemd-source-of-truth|systemd-source-of-truth]]
- Skill operativa: `~/.hermes/profiles/ariadna/skills/devops/hermes-dashboard-recovery/`
- Journal session: [[../../../80-agents/journal/sessions/2026-07-01-1130-hermes-dashboard-post-update-recovery-summary]]

## Source files

- Tickets `~/aranea/tickets/2026-06-29-007`, `008`
- Ticket `~/aranea/tickets/2026-07-01-014`
- `/home/hermes/.config/systemd/user/hermes-dashboard.service`
- `/home/hermes/.config/systemd/user/hermes-dashboard.service.d/override.conf`
- `/etc/systemd/system/aranea-traefik-tunnel.service`
- `/etc/traefik/dynamic/aranea-dashboard.yaml`
- `journalctl -u hermes-dashboard`, `-u aranea-traefik-tunnel`

## Captured

Iter final 2026-07-01 16:48 UTC tras sesión interactiva con owner. Tres Traefik apply + un override drop-in, sin tocar DNS, gateway, ni config_version.
