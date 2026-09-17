---
type: feedback
schema_version: 1
created: 2026-09-16
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
tags:
  - kind/feedback
  - area/aranea
---

# 2026-09-16 — Backup/DR R0 session feedback

## Friction

- `delegate_task` falló al inicio de sesión: provider `minimax` configurado como default de delegación pero sin `MINIMAX_API_KEY` utilizable; el spawn muere con error de credenciales. Workaround: ejecutar el trabajo documental directamente (funcionó, a costa de más tokens de contexto). Sugerencia: fijar delegation.provider a uno con credenciales activas (zai/nous/openrouter) o proveer la key.
- El wrapper `agent-read` no expone nada del plano PBS (datastore, jobs, verify, versión PBS): la verificación Backup/DR de R2+ requerirá datos PBS owner-side o extensión del wrapper. GAP real, no bypass.

## Degradation

- Ninguna bloqueante. Ping ICMP Hermes→Pi-hole .149 sin respuesta con resolución DNS funcionando vía stub — observado, no diagnosticado (posible firewall ICMP; vigilar en R1 porque afecta recovery independence DNS).

## Pain Pattern Candidate

- Docs evergreen con `status: active` años después de ser reemplazados (5 archivos legacy en 03-storage lo evidenciaron): los agent-projects de "cleanup" quedan paused y el drift documental se acumula silencioso. Candidato: política de que todo doc superseded se marca en el MISMO cambio que introduce su reemplazo.
