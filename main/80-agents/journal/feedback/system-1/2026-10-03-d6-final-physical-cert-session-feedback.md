---
type: feedback
schema_version: 1
scope: session
created: 2026-10-03
updated: 2026-10-03
area: "[[Echo]]"
project: "[[Echo Futures]]"
entities:
  - "[[Echo Futures]]"
related:
  - "[[aranea-ssh-mcp]]"
  - "[[agents-os-session-close]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
agent_run: "[[2026-10-03-zcode-glm53-d6-final-physical-certification-attempt1]]"
session_goal: D6 final physical certification attempt 1 (OD-D6-1 authorized); ladder blocked by CME weekend closure; honest NOT_READY disposition.
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - area/echo
---

# Session Feedback — D6 Final Physical Certification intento 1 (2026-10-03)

## Qué funcionó bien

- **Chequeo de calendario ANTES de cualquier egress**: el reloj CT + el estado del topic Kafka (último `event_ts` viernes 21:38Z) identificaron el bloqueo en minutos, sin gastar una sola orden ni mutación — el ladder murió por calendario, no por ensayo-y-error.
- **Evidencia física multi-plano barata**: Kafka end-offset doble muestra + counters del evidence sink + netstat PID + certutil hash remoto cruzados entre sí dieron una cadena P1–P7 completa sin escribir nada.

## Pain patterns / fricción

- `aranea-ssh` perfil `dev-win` (viewer) rechaza TAMBIÉN `read-command` ("Clear readOnly on the profile to allow them") ⇒ toda lectura del Windows exige el perfil operator, rompiendo la separación viewer/operator. Ya había matado `read-command` en contextos MT4; aquí quedó inutilizable también por policy. Recurre ⇒ candidato pain pattern.
- El shell remoto de dev-win es **PowerShell**: sintaxis cmd (`2>nul`, `&`) rompe; `$` se elimina en tránsito. Los comandos deben ser PS-cortos (ya en memoria ZCode, pero el vault no lo registra como runbook de dev-win).
- Nota de memoria incorrecta detectada y corregida: el relay nt-feed NO corre como unidad systemd `echo-nt-feed-relay` — es un proceso raw (`/home/kor/opt/echo-dev/releases/<sha>/nt-feed-relay`, stdout a socket). La nota "unidad activa" de N1-R1 arrastra esa imprecisión.

## Missing Support

- **G-STOP no tiene parámetros físicos frozen standalone** (side/qty/precio): el prompt obliga a STOP+OWNER_DECISION_REQUIRED si faltan, y hoy sólo existe el ciclo E2E congelado que los deriva de GerardMM en vivo. Registrar en el próximo despacho que G-STOP se ejercita dentro de G-E2E o congelar parámetros explícitos si se quiere gate independiente (decisión Manager, ya anotada en el artifact §5/§17).
