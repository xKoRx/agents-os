---
type: feedback
scope: session
created: "2026-10-02"
updated: "2026-10-02"
area: "[[Echo]]"
project: "[[Echo Futures]]"
entities:
  - "[[Echo Futures]]"
related:
  - "[[agents-os-session-close]]"
  - "[[aranea-ssh-mcp]]"
aliases: []
agent_surface: "[[ZCode]]"
session_goal: D6 Shot 1 Manager QA remediation (F-MGR-01/02/03) + canonical session close with feedback.
source_session: ""
confidence: high
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
  - area/echo
---

# Session Feedback — D6 Shot 1 Manager QA Remediation (2026-10-02)

## Qué funcionó bien

- **Subagentes en worktrees separados por scope** (S7 freshness, S9 warm-up del Shot 1; base compartida por commits): merges limpios sin conflictos semánticos y paralelismo real; el patrón "un worktree por scope + commit atómico por scope" escaló sin fricción.
- **Reflexión ANTES de codificar contra las DLL físicas** (patrón N1-R3): el shadow-compile del AddOn de ejecución falló primero con los errores reales de la API 8.1.8.3 y una sola pasada de corrección bastó — cero ensayo-y-error contra el producto.
- **Verificación de escrituras ETCD con doble read-back** (writer + MCP RO plano) detectó un artefacto de matching difuso del MCP que hubiera contaminado el estado reportado; el cliente etcd crudo por miembro resolvió la verdad.

## Pain patterns / fricción (menor)

- `aranea-ssh` MCP con sesión expirada no se re-inicializa desde el cliente (persistió >30 min); el workaround (driver HTTP directo del protocolo MCP con session id manual) funcionó pero es frágil y no reutilizable tal cual. Candidato a pain pattern si recurre.
- `etcd_get_value` del MCP RO puede responder `found=true` con el valor de OTRA clave bajo el prefijo (matching difuso); para escrituras guardadas, corroborar siempre con lectura cruda por clave exacta.
- Medición de cobertura por-hunks del diff es sensible al orden de ejecución de tests con goroutines (dos corridas del mismo profile dieron ±3 stmts); fijar `-count=1` y suites en orden canónico antes de medir.
