---
type: runbook
schema_version: 1
scope: area
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Aranea]]"
project: "[[HERMES — Infrastructure Operations]]"
application:
entities:
  - "[[Aranea]]"
  - "[[HERMES — ARANEA AUTONOMOUS OPERATIONS]]"
related:
  - "[[hermes-agent-operator]]"
  - "[[HERMES — Infrastructure Operations]]"
aliases:
  - Hermes Linux update recovery
  - Hermes update recovery
  - Hermes mixed sys.modules recovery
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/area
  - area/aranea
  - tech/hermes
  - action/update-recovery
---

# hermes-linux-update-recovery

## Propósito

Ejecutar y recuperar un `hermes update` en el host Linux de Hermes cuando existen perfiles, `systemd --user`, dashboard/serve persistentes o el updater reporta `mixed sys.modules`, `fleet_restart_pending`, imports inconsistentes o runtimes pre-update.

Este runbook documenta la mecánica validada. El criterio de cuándo usarla, qué runtime tocar y cuándo detenerse vive en [[hermes-agent-operator]].

## Precondiciones

- Ejecutar como el usuario de servicio `hermes` salvo que un paso indique otra autoridad.
- Checkout esperado bajo `~/.hermes/hermes-agent` y venv bajo `./venv`.
- No asumir que el perfil sticky, `HERMES_HOME`, el perfil del servicio y el perfil de un comando bare son equivalentes.
- Antes de reiniciar, identificar el supervisor real de cada PID con `ps`, `pstree` y `/proc/<pid>/cgroup`.
- No imprimir tokens, `.env` completos ni secretos. Para comparar credenciales compartidas usar hash del valor, nunca el valor.

## Baseline antes del update

1. Registrar versión y SHA:

```bash
cd ~/.hermes/hermes-agent
./venv/bin/python -m hermes_cli.main --version
git status --short
git rev-parse HEAD
```

2. Inventariar listeners y runtimes relevantes:

```bash
ss -lntp | grep -E ':(9119)\b' || true
ps -eo pid,ppid,lstart,args | grep -E '[h]ermes|[u]vicorn'
```

3. Inventariar unidades user instaladas y activas. Si la shell SSH no puede abrir el user bus, usar explícitamente:

```bash
export XDG_RUNTIME_DIR=/run/user/$(id -u)
export DBUS_SESSION_BUS_ADDRESS=unix:path="$XDG_RUNTIME_DIR/bus"
systemctl --user list-unit-files 'hermes*' --no-pager
systemctl --user --type=service --state=running --no-pager | grep hermes || true
```

4. Registrar el perfil sticky sin cambiarlo:

```bash
printf 'ACTIVE_PROFILE='
cat ~/.hermes/active_profile 2>/dev/null || echo '<missing>'
```

## Update

Ejecutar una sola vez el update normal:

```bash
hermes update
```

Si termina limpio, continuar igualmente a validación post-update. Si falla después de mover el checkout y reporta `mixed sys.modules`, `file_signature`, atributos faltantes, runtimes pre-update o auto-restart incompleto, **no repetir `hermes update` todavía**: pasar a Recovery.

## Recovery — checkout primero, procesos después

### 1. Demostrar que el checkout en disco es coherente

```bash
cd ~/.hermes/hermes-agent
git status --short
git rev-parse HEAD

grep -n '^def file_signature' utils.py || true
./venv/bin/python -c 'from utils import file_signature; print("IMPORT_OK", file_signature)'
```

Criterio: un proceso Python fresco debe importar el símbolo que falló. Si el import fresco también falla, el problema es checkout/dependencias y este runbook se detiene antes de reiniciar servicios.

### 2. Identificar exactamente los procesos stale

Para cada PID reportado por el updater:

```bash
ps -o pid,ppid,lstart,args -p <PID>
pstree -sp <PID>
cat /proc/<PID>/cgroup
```

No matar por PID si pertenece a una unidad supervisada. Resolver primero el nombre exacto de la unidad.

### 3. Reiniciar servicios supervisados con código nuevo

En el baseline certificado de Aranea:

```text
hermes-dashboard.service         -> dashboard loopback :9119
hermes-gateway-ariadna.service   -> gateway del perfil ariadna
```

Reiniciar uno por uno y validar cada uno antes del siguiente:

```bash
systemctl --user restart hermes-dashboard.service
systemctl --user status hermes-dashboard.service --no-pager

systemctl --user restart hermes-gateway-ariadna.service
systemctl --user status hermes-gateway-ariadna.service --no-pager
```

Criterios mínimos:

- PID nuevo respecto al proceso stale.
- dashboard: `HERMES_DASHBOARD_READY port=9119` y HTTP 200 local.
- gateway: servicio `active` y plataforma requerida reconectada.

### 4. No revivir gateways duplicados a ciegas

Si existe `hermes-gateway.service` además del gateway del perfil nombrado, **no iniciarlo sólo para satisfacer el updater**.

Primero comprobar:

```bash
systemctl --user status hermes-gateway.service --no-pager
systemctl --user cat hermes-gateway.service
```

Si default y perfil nombrado usan la misma credencial de Telegram, comparar sin revelar secreto:

```bash
for f in ~/.hermes/.env ~/.hermes/profiles/<perfil>/.env; do
  printf '%s -> ' "$f"
  grep -E '^TELEGRAM(_BOT)?_TOKEN=' "$f" 2>/dev/null \
    | cut -d= -f2- | sha256sum | cut -d' ' -f1
done
```

Hashes iguales significan que dos gateways en polling competirían por el mismo bot. En el baseline validado 2026-09-16, `default` y `ariadna` compartían token; `hermes-gateway.service` quedó `disabled` y el gateway real es `hermes-gateway-ariadna.service`.

### 5. Resolver warning persistente de restart pendiente

Hermes puede conservar un breadcrumb por perfil aunque los runtimes ya hayan sido reiniciados.

Ruta del marker para un perfil nombrado:

```text
~/.hermes/profiles/<perfil>/fleet_restart_pending
```

Inspeccionar, no borrar:

```bash
cat ~/.hermes/profiles/<perfil>/fleet_restart_pending 2>/dev/null || true
```

Verificar con el propio código de Hermes:

```bash
HERMES_HOME="$HOME/.hermes/profiles/<perfil>" ./venv/bin/python - <<'PY'
from pprint import pprint
from hermes_cli.update_cmd_fleet import (
    _current_checkout_sha,
    _read_fleet_marker_expected_sha,
    _marker_only_restart_obsolete,
    _receipt_owed_gateways,
)
from hermes_cli.update_receipt import collect_fleet_versions

print("checkout_sha =", _current_checkout_sha())
print("marker_sha   =", _read_fleet_marker_expected_sha())
print("obsolete     =", _marker_only_restart_obsolete())
print("fleet        =")
pprint(collect_fleet_versions())
print("owed         =")
pprint(_receipt_owed_gateways())
PY
```

Si el SHA coincide pero `obsolete=False`, revisar qué runtime `owed` falta. No borrar el marker mientras exista una obligación real no resuelta.

### 6. Distinguir receipt viejo de obligación actual

Los receipts de un perfil nombrado viven bajo:

```text
~/.hermes/profiles/<perfil>/logs/update_receipts/
```

Localizar primero, sin asumir el home:

```bash
find ~/.hermes -type f \
  \( -name 'latest.json' -o -name 'update_*.json' \) \
  -path '*/logs/update_receipts/*' -printf '%p\n' 2>/dev/null
```

Inspeccionar sólo metadata operacional:

```bash
jq '{
  outcome,
  exit_code,
  stop_reason,
  gateway_restart,
  plan_runtimes: (.plan.runtimes // []),
  fleet: (.fleet // [])
}' <latest.json>
```

Un receipt histórico que exige un gateway ahora retirado no justifica revivirlo si hacerlo viola el boundary actual (por ejemplo, bot Telegram duplicado). Primero retirar/deshabilitar formalmente el runtime legacy.

### 7. Limpiar marker sólo con evidencia

Cuando:

- checkout actual = `expected_sha` del marker;
- todos los runtimes vigentes necesarios corren el SHA actual;
- cualquier runtime legacy quedó retirado/deshabilitado de forma deliberada;
- dashboard/gateway tienen health funcional;

hacer backup y remover sólo el marker del perfil afectado:

```bash
MARKER="$HOME/.hermes/profiles/<perfil>/fleet_restart_pending"
BACKUP="${MARKER}.bak-$(date +%Y%m%d-%H%M%S)"
cp -a "$MARKER" "$BACKUP" && rm "$MARKER"
```

Luego demostrar que Hermes ya no ve obligación pendiente:

```bash
HERMES_HOME="$HOME/.hermes/profiles/<perfil>" ./venv/bin/python - <<'PY'
from hermes_cli.update_cmd_fleet import _pending_fleet_restart_needed
print("PENDING_RESTART =", _pending_fleet_restart_needed())
PY
```

Resultado requerido: `PENDING_RESTART = False`.

## Validación final

1. Proceso fresco sin warning de update:

```bash
HERMES_HOME="$HOME/.hermes/profiles/<perfil>" \
./venv/bin/python -m hermes_cli.main --version
```

2. Dashboard:

```bash
curl -fsS -o /dev/null -w 'HTTP %{http_code}\n' http://127.0.0.1:9119/
```

3. Gateway:

```bash
systemctl --user is-active hermes-gateway-<perfil>.service
```

4. Estado actual de Telegram, si aplica:

```bash
jq '.platforms.telegram' ~/.hermes/profiles/<perfil>/gateway_state.json
```

PASS requiere `state=connected`, `error_code=null` y `needs_attention=false`.

## Rollback / recuperación

- Reinicio de servicio: volver a la unidad previa no aplica; el checkout determina el código. Si el checkout fresco falla, detener y recuperar el checkout/dependencias antes de seguir.
- `fleet_restart_pending`: restaurar el backup creado junto al marker si la limpieza fue prematura.
- Gateway legacy deshabilitado: re-habilitar sólo si se demuestra que debe existir y no duplica credenciales/plataformas.
- Nunca resolver un warning levantando dos pollers con el mismo token.

## Evidencia validada — 2026-09-16

- Hermes Agent quedó en `v0.21.3 (2026.9.14)`, SHA `8c8003f80b528377d4387b96faa2c00283168d68`.
- `hermes-dashboard.service` reinició con PID nuevo y `HTTP 200` en `127.0.0.1:9119`.
- `hermes-gateway-ariadna.service` reinició con PID nuevo y Telegram `connected`, `needs_attention=false`.
- El gateway default estaba `inactive`, `enabled` y compartía token Telegram con Ariadna; quedó `disabled` para evitar doble polling.
- El marker de Ariadna se respaldó y removió sólo después de demostrar `PENDING_RESTART = False`.
- Un proceso Hermes fresco terminó `Up to date` sin warning de `mixed sys.modules`.
