---
type: change_log
schema_version: 1
scope: session
created: 2026-08-10
updated: 2026-08-10
area: "[[Echo]]"
project: "[[Stager - Cross-Platform Deployment Lifecycle]]"
application: "[[stager-app]]"
entities:
  - "[[Stager]]"
  - "[[Echo Forge]]"
related:
  - "[[2026-08-10-stager-f01-readonly-capture-raw]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-08-10-stager-f01-readonly-capture-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/echo
---

# Stager F0.1 read-only capture

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Stager - Cross-Platform Deployment Lifecycle.md`
  - `10-projects/Echo Forge/Echo Forge.md`

## Motivo

- F0.1 requiere capturar el estado efectivo de Zeus, Hera y Kronos antes de cualquier diseño o mutación posterior. El intento inicial quedó bloqueado por la vía SSH estándar; el owner autorizó después el troubleshooting read-only.

## Fuentes usadas

- [[Stager - Cross-Platform Deployment Lifecycle]] — alcance, gate F0 y checklist vigente.
- Configuración SSH local y respuestas de conexión read-only del 2026-08-10.
- [[2026-08-10-stager-f01-readonly-capture-raw]] — trazabilidad compacta de la sesión.

## Resolución aplicada

- La tarea F0.1 pasó a Done; F0.2 se reabrió para reconciliar el diff offline que había documentado correctamente la ausencia de captura.
- La autorización quedó acotada al uso read-only de `sqx/tools/ssh_pty.py`; no autoriza mutaciones, elevación interactiva ni persistir credenciales.

### Captura read-only — 2026-08-10

Los tres hosts son equivalentes en las seis clases requeridas:

| Clase | Zeus / Hera / Kronos |
|---|---|
| Binario | `/usr/local/bin/stager`, `root:root`, `0755`, SHA-256 `0113b3b80825…5792630` |
| Wrapper | `/usr/local/sbin/symphony-stager-go`, `root:root`, `0755`, SHA-256 `d7747136ba21…941c8b0b`; ejecuta Stager, actualiza `current` y proyecta `PENDING` |
| Env redacted | unit define `STAGER_BIN`, `STAGER_ROOT`, `PENDING_FILE`; `/etc/symphony/stager.env` existe con `0600 symphony:symphony`; valores no leídos ni persistidos |
| Units/timer | `symphony-stager.service` oneshot `User/Group=symphony`; timer enabled `OnBootSec=1min`, `OnUnitActiveSec=30s`; `symphony-worker.service` enabled/active, `User/Group=kor` |
| Permisos | `/opt/symphony` y `releases` `0755 symphony:symphony`; `current` symlink; `/var/lib/symphony` `0777 kor:kor` |
| Layout | `CURRENT=0.2.40`, `current → releases/0.2.40`, única release `0.2.40`; `/opt/symphony/PENDING` `0644 symphony:symphony`; `/var/lib/symphony/PENDING` ausente al muestreo |

## Validación

- Intento inicial SSH directo a Zeus/Hera/Kronos: autenticación rechazada; bastión `develop`: timeout.
- Con autorización explícita del owner, `sqx/tools/ssh_pty.py` conectó y ejecutó lecturas en los tres hosts.
- La salida capturó metadatos/hash de binarios, definición/estado de units, esquema de env redactado, wrapper efectivo, permisos y layout. `sudo -n` no pudo leer el env `0600`; no se intentó elevación interactiva.
- No se ejecutaron comandos mutantes ni se persistieron credenciales.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** no incluye credenciales, valores de entorno, outputs de host ni paths absolutos de máquina.

## Rollback

- Revertir sólo el estado/documentación si una captura posterior contradice estos hechos; no hay cambios de runtime que revertir.
