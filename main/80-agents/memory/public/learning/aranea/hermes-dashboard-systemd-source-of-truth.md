---
type: learning
scope: project
created: 2026-07-01
updated: 2026-07-01
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
  - Para todos los servicios Hermes (dashboard, gateway, TUI), el unit systemd debe ser la única fuente de verdad operacional. Nunca procesos manuales compitiendo.
entities:
  - "[[Aranea]]"
  - "[[Hermes]]"
  - "[[systemd]]"
related:
  - "[[../../../30-resources/aranea/02-servicios/dashboard-hermes-agent]]"
  - "[[../../../30-resources/aranea/05-tickets/2026-07-01-014-hermes-dashboard-bind-loopback-after-update]]"
  - "[[../../../80-agents/journal/sessions/2026-07-01-1130-hermes-dashboard-post-update-recovery-summary]]"
aliases:
  - systemd source of truth
  - single source of truth dashboard
  - manual processes competing with units
  - dashboard unit drop-in
confidence: verified
source_session: 2026-07-01-1130-hermes-dashboard-post-update-recovery
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - hermes
  - dashboard
  - systemd
  - runit
  - drop-in
  - override
  - area/aranea
  - kind/learning
  - priority/high
  - project/agents-os
  - scope/project
---

# Hermes Dashboard — Systemd unit como única fuente de verdad

## Aprendizaje (resumen ejecutivo)

**No dejar el dashboard Hermes corriendo como proceso manual si existe systemd unit.** El unit debe ser la única fuente de verdad, incluyendo profile, env vars, PATH y flags. Si hay proceso manual y unit con flags distintos, el debugging se vuelve ambiguo y los fixes no tienen efecto sobre el proceso real.

## Contexto

Durante el incidente **2026-07-01-014**, existían dos fuentes de verdad para el dashboard:

| Aspecto | Proceso manual (PID 79382, parent 8794) | Unit `hermes-dashboard.service` |
|---|---|---|
| Comando | `... dashboard --port 9119 --host 127.0.0.1 --open-profile ariadna --no-open` | `... dashboard --port 9119 --host 127.0.0.1 --no-open` |
| Profile | `--open-profile ariadna` activo | sin profile explícito |
| Env vars | Heredadas del gateway agent (sin `HERMES_PYTHON_SRC_ROOT`, sin PATH Hermes-first) | vacías |
| Parent | systemd --user instance, pero nacido fuera del unit | systemd --user unit |
| Runtime | desde 2026-07-01 03:01 | active pero no usado (el unit consumía sus propios reintentos) |

Cuando modifiqué el unit (`--host 127.0.0.1`), el dashboard real (PID 79382) **NO fue afectado** porque no era hijo del unit — era un proceso que estaba bindeado a `127.0.0.1:9119` y el unit era solo un fantasma elegante. **Cada "fix" propuesto contra el unit no se aplicaba al proceso real.**

## Por qué pasó esto

El proceso manual probablemente se originó durante una sesión previa donde se inició manualmente el dashboard con `--open-profile ariadna` para que el chat abriera con ese perfil. La persona que lo hizo (yo o vos) olvidó que el unit existía. **El unit nunca se reinició con `--open-profile ariadna`** porque nadie actualizó el unit.

Después, el incidente me llevó a leer `/proc/79382/environ` y descubrir que las env vars del agent gateway (no del unit) eran las que se heredaban.

## El fix definitivo

1. **Backup del unit base** (no eliminar, preservar).
2. **Crear drop-in override** (`~/.config/systemd/user/hermes-dashboard.service.d/override.conf`):
   - Override `ExecStart` con `ExecStart=` (vacío) para resetear el del unit base.
   - Definir nuevo `ExecStart` con el path completo + todos los flags incluido `--open-profile ariadna`.
   - Añadir las Environment vars necesarias (`HERMES_HOME`, `HERMES_PYTHON_SRC_ROOT`, `HERMES_PYTHON`, `PATH` con Hermes Node primero).
3. **Matar el proceso manual huérfano**: `kill -TERM <PID>`. Verificar con `/proc/<PID>` que ya no existe.
4. **`systemctl --user enable --now hermes-dashboard.service`**: systemd arranca el nuevo proceso con el merge del unit base + drop-in.
5. **Validar env vars reales en `/proc/<PID_NUEVO>/environ`** para confirmar que se aplicaron.

## Por qué drop-in override > modificar unit base

Modificar `~/.config/systemd/user/hermes-dashboard.service` directamente:
- Cambia diffs históricos del archivo.
- Dificulta el rollback (hay que recordar el estado anterior).
- Mezcla systemd + lógica de negocio en un solo archivo.

Drop-in override:
- Mantiene el archivo base inmutable (es la "spec" del servicio).
- Cada cambio queda aislado en `/etc/systemd/system/<service>.d/override.conf` o equivalent user path.
- Rollback: `rm -rf <drop-in dir>` + `daemon-reload`.
- Permite múltiples drop-ins coexistiendo (`override.conf`, `secret.conf`, `prod-env.conf`).

## Patrones relacionados

- [[agents-os/manual-validation-vs-automated-healthcheck-policy]] — `systemctl is-active active` no es suficiente para declarar funcional. Smoke test real con browser.
- `agents-os/known-error/aranea-agent-ro-sudo-nopasswd-blocked.md` — patrón paralelo: configuración bloqueada por falta de NOPASSWD, manifestada como servicio que no se puede administrar.

## Anti-patrones

- ❌ Lanzar el dashboard con `hermes dashboard &` desde una terminal sin usar el unit. **El proceso sobrevive al log-out del shell** y entra en competencia silenciosa con el unit.
- ❌ Actualizar el unit sin matar el proceso manual previo. Los cambios no toman efecto en el proceso existente (hasta que systemd decida reiniciarlo bajo `Restart=on-failure` y el proceso no había fallado).
- ❌ Confiar en `systemctl is-active` cuando el proceso real es huérfano del unit. Validar con `pgrep` o `ps -eo cmdline`.

## Confirmación operativa

Aplicado el 2026-07-01 16:48 UTC:
- PID 79382 (manual) muerto tras `kill -TERM`.
- PID 83975 (unit) activo con env vars completas.
- `systemctl --user is-active hermes-dashboard.service` → active.
- Owner confirmó chat funcional desde Safari con perfil ariadna.

## Referencias

- Ticket [[../../../30-resources/aranea/05-tickets/2026-07-01-014-hermes-dashboard-bind-loopback-after-update]]
- Runbook [[../../../30-resources/aranea/02-servicios/dashboard-hermes-agent]]
- Backup del unit: `~/reset-backups/hermes-dashboard.service.before-env-profile-20260701-164244.txt`
- Skill: `~/.hermes/profiles/ariadna/skills/devops/hermes-dashboard-recovery/`
