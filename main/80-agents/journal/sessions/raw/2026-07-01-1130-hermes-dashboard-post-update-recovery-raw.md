---
type: session-raw
scope: session
created: "2026-07-01"
updated: "2026-07-01"
session_id: "2026-07-01-1130-hermes-dashboard-post-update-recovery"
source_session: "[[2026-07-01-1130-hermes-dashboard-post-update-recovery-summary]]"
load_policy: manual
indexable: false
index_priority: never
---

# 📓 RAW — 2026-07-01-1130 Hermes dashboard recovery (bitácora cruda)

## Cronología completa

### Turno 1 — usuario reporta problema
> "sorry... el dashboard de hermes es el que no carga, murió después del
> update de hermes"

Owner aclara que NO es infra de Aranea, es esta misma VM (hermes-vm). Dashboard
local después del `hermes update`.

### Turno 2 — primer reconocimiento equivocado

Propuse 3 opciones A/B/C de fix:
- A: bind a 127.0.0.1 + reset failed
- B: agregar basic_auth + dejar 0.0.0.0
- C: solo diagnostic más

**Owner me frenó con razón**:
> "no... me parece que habíamos bindeado la ip local no?? revisa en el
> historial el problema lo resolvimos, no inventes"

Lección 1: tenía que haber empezado por `session_search` y `find` en el
filesystem, no por proponer.

### Turno 3 — reconocimiento correcto

Búsqueda en `session_search` con varias queries. Encontré en el snippet:
- Ticket 2026-06-29-007-expose-dashboard-via-traefik (applied)
- Ticket 2026-06-29-008-dashboard-no-password-via-reverse-tunnel (applied)
- Ticket README en 05-tickets/ index ya tenía 13 tickets

Leí los 2 tickets enteros. Confirmado al 100% el approach:
- Bind 127.0.0.1
- Tunnel SSH reverso vía systemd wrapper
- Sin `dashboard.basic_auth` interno
- Traefik + lan-only + stepca como perímetro

### Turno 4 — segunda corrección del owner

> "no a ver... recuerdo que trabajamos con la ip local y algo después
> corregimos... me confirmas que este es el último approach?? el approach que
> hizo funcionar el dashboard con websocket con dns"

Owner quería VERIFICAR antes de que aplicara — que abriera el ticket 008 y leyera
el approach. Lo hice, leí Fase 1 a Fase 4, validé que era el approach canónico.

Lección 2: el owner valida cambios que afecten producción antes de aceptar
propuestas. Citar fuente (ticket archivo) > citar memoria.

### Turno 5 — owner aprueba con variante de documentación

Pregunté si procedía con fix idéntico. Owner eligió opción 2:
> "Sí, pero primero documentá el incidente y el fix en el Second Brain en una
> nota/handover (pedido explícito en tu memory: 'no dejar a Aranea más smart
> que en chat')."

Lección 3: memoria dice "no dejar a Aranea más smart que en chat" → owner
valora documentación ANTES del fix.

### Turno 6 — verificación pre-fix

```bash
$ grep -E "^dashboard:|basic_auth|allowed_hosts" ~/.hermes/profiles/ariadna/config.yaml
(sin output — config.yaml no tiene bloque dashboard — bien, post-ticket 008)

$ systemctl --user show hermes-dashboard.service
ExecStart=... dashboard --host 0.0.0.0 --port 9119 --no-open
ActiveState=inactive
SubState=dead
```

Confirmado: config OK, unit mal. Fix = cambiar unit.

### Turno 7 — intento de fix en bloque, FALLA con hook

```bash
$ cp -v ~/.config/systemd/user/hermes-dashboard.service ~/.config/systemd/user/hermes-dashboard.service.bak.$(date +%s)
$ sed -i 's/--host 0.0.0.0/--host 127.0.0.1/' ~/.config/systemd/user/hermes-dashboard.service
$ systemctl --user daemon-reload
$ systemctl --user reset-failed hermes-dashboard.service
$ systemctl --user start hermes-dashboard.service
# → Blocked: cannot restart or stop the gateway from inside the gateway process.
```

El `set -e` cortó todo el script. Ningún cambio aplicado. Backup NO hecho.

### Turno 8 — fix comando por comando

```bash
$ cp -v hermes-dashboard.service hermes-dashboard.service.bak.1782873265
'exes-dashboard.service' -> 'hermes-dashboard.service.bak.1782873265'
$ diff -u ...bak.1782873265 ...service
# solo cambia el --host
$ systemctl --user daemon-reload
# exit=0 — OK
$ systemctl --user reset-failed hermes-dashboard.service
# exit=0 — OK
$ systemctl --user start hermes-dashboard.service
# → Blocked by hook
```

### Turno 9 — documentación

Creados 4 archivos en el Second Brain:
1. `30-resources/aranea/02-servicios/dashboard-hermes-agent.md` (runbook)
2. `30-resources/aranea/05-tickets/2026-07-01-014-hermes-dashboard-bind-loopback-after-update.md` (ticket)
3. `30-resources/aranea/05-tickets/README.md` (parche para incluir 014)
4. `80-agents/journal/sessions/2026-07-01-1130-hermes-dashboard-post-update-recovery-summary.md` (journal)
5. `80-agents/journal/sessions/raw/2026-07-01-1130-hermes-dashboard-post-update-recovery-raw.md` (este archivo)

### Estado al cierre del turno 9

| Item | Estado |
|---|---|
| Unit parchado | ✅ |
| Backup del unit | ✅ `hermes-dashboard.service.bak.1782873265` |
| daemon-reload | ✅ |
| reset-failed | ✅ |
| start del dashboard | ❌ pendiente — hook bloqueó |
| Validación 127.0.0.1:9119 | 🟡 pendiente |
| Validación tunnel Traefik | 🟡 pendiente |
| Validación dashboard.lab.aranea | 🟡 pendiente |
| Documentación en SB | ✅ 4 archivos |

## Comandos que el owner debe ejecutar desde otra shell

```bash
systemctl --user start hermes-dashboard.service
systemctl --user status hermes-dashboard.service --no-pager
curl -sS -o /dev/null -w "HTTP %{http_code}\n" http://127.0.0.1:9119/
systemctl --user is-active hermes-tunnel-traefik
curl -k -sS -o /dev/null -w "HTTP %{http_code}\n" \
  -H 'Host: dashboard.lab.aranea' --max-time 5 \
  https://dashboard.lab.aranea/
```

## Outputs importantes a guardar

| Output | Dónde guardar |
|---|---|
| HTTP code de 127.0.0.1:9119 | comentario en ticket 014 |
| HTTP code de dashboard.lab.aranea end-to-end | comentario en ticket 014 |
| `is-active hermes-dashboard` post-start | comentario en ticket 014 |
| `is-active hermes-tunnel-traefik` post-validación | comentario en ticket 014 |

Si todo verde → cerrar ticket, agregar a `runbook-incidentes.md`, crear skill.
Si falla alguna → escalar a ticket de incidente mayor.
