---
type: session_feedback
schema_version: 1
date: 2026-09-15
project: "[[HERMES — Bootstrap & Self-Sufficiency]]"
area: "[[Aranea]]"
tags:
  - kind/feedback
  - area/aranea
  - system-1
---

# 2026-09-15 — B3.3 observability session feedback

## Fricción

- El security scan del `terminal` flaggea toda URL con IP RFC1918 como MEDIUM; en un dominio homelab-only (todo `mcps-ops`/`curl` interno) genera ruido repetitivo y un timeout de aprobación abortó un comando combinado legítimo (curl + greps locales), costando un turno completo.
- El wrapper `mcps-ops` loguea argv completo por diseño (auditoría); sin un canal stdin documentado, el primer intento natural de pasar el token Grafana lo habría escrito en `~/.hermes/logs/mcps-ops.log`. Riesgo de fuga evitado sólo por conocimiento del agente, no por diseño del path.
- **Recurrencia en la sesión de cierre (mismo día):** el patrón `mcps-ops 'sudo bash -s' <<heredoc` volvió a disparar el gate de aprobación y abortó por timeout (2ª vez, mismo coste). Confirmado como anti-patrón: scripts siempre por `scp` + `sudo -n bash /tmp/x.sh` one-liner; el wrapper resultó ser passthrough stdin puro (transferencia del token vía pipe funcionó sin fricción).

## Gaps

- Docker Hub gateway requiere `%2F` en namespaces anidados; el 404 resultante se confunde fácilmente con "tag inexistente". El digest final debe salir siempre de `registry-1.docker.io` o del tag API con encoding correcto.
- Graphify degradado al cierre: `query` timeout (60s) y `explain` reporta "índice stale; el refresh ya falló" sin resolver notas nuevas del día. Recomendado: corrida de `agents-os-graphify-maintenance` (rebuild explícito) fuera de esta sesión.

## Pain Pattern Candidate

- Security scan: allowlist RFC1918/`.lab.aranea.cl` para operaciones ya autorizadas por management path — un solo ajuste eliminaría la fricción recurrente de aprobaciones/timeout en todo trabajo Aranea.
