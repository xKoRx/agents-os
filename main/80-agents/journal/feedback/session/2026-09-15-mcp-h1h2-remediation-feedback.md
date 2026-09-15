---
type: feedback
scope: session
created: 2026-09-15
updated: 2026-09-15
area: "[[Aranea]]"
project: "[[AGENT-PLATFORM - MCP Access Plane]]"
entities:
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
  - "[[ACCESS-CERTIFICATION]]"
  - "[[aranea-mcp-plane-operator]]"
related:
  - "[[HERMES — Bootstrap & Self-Sufficiency]]"
aliases: []
agent: Ariadna (Hermes)
session_goal: Cerrar H1 (export_metadata exposure en hasura PROD-RO) y H2 (viewer enforcement en ssh-mcp) con enforcement server-side real, certificación Daedalus y drift cero.
source_session:
confidence: high
load_policy: manual
indexable: false
index_priority: low
tags:
  - kind/feedback
  - scope/session
  - area/aranea
  - tech/mcp
---

# Session Feedback - 2026-09-15 - MCP H1+H2 remediation

## Context

- Agent surface: Ariadna (Hermes TUI)
- Agent model: glm-5.3-flash (zai)
- Session goal: cierre de los dos HIGH del access plane sin abrir B3.3
- Main entity: [[AGENT-PLATFORM - MCP Access Plane]]
- Skills used: mcp-access-plane-operations, aranea-mcp-plane-operator (vault)
- Retrieval mode: scoped (workstream + runbooks familia)
- Artifacts changed: ACCESS-CERTIFICATION.md, aranea-hasura-mcp.md, aranea-ssh-mcp.md, HERMES — Bootstrap & Self-Sufficiency.md

## Friction

1. **`sed -i` con comandos multi-step sobre archivos root-owned vía mcps-ops truncó `metadata.go` a 0 bytes** (combinación `sed -n ... h; d; G` mal anidada). Recovery inmediato desde backup previo con verificación sha256 byte-identical — sin daño real. Lección operativa: para edits quirúrgicos en `mcps`, escribir el patcher en Python local, subirlo por `scp` y ejecutarlo contra copia temporal + `cp` de vuelta; nunca `sed` compuesto a través del wrapper.

2. **Sesión MCP del hasura proxy (`mcp-proxy` 6.7.16): `notifications/initialized` dispara el teardown del child stdio en ciertos momentos** — la misma secuencia pasaba/fallaba según timing del restart del backend. El smoke estable resultó: sesión nueva por llamada (init-only sin notification) para tools/list y cada tools/call. Documentar en el skill del plane si vuelve a aparecer en otra capability.

3. **`get_schema` (Hasura) confirmado como M5 no-regresión**: la respuesta de introspección (~11 MB) mata el child stdio del proxy (`Connection closed` → `Not connected`). Reproducido idéntico en la imagen DEV sin el patch H1, y directamente por stdio con `--admin-secret` el call responde OK (~11.2 MB). El defecto vive en el transporte proxy↔stdio, no en el backend ni en Hasura.

## What worked

- Patrón baseline→patch→rebuild→recreate→server-smoke→consumer-smoke→post-condición de `aranea-mcp-plane-operator` aplicado limpio en dos capabilities; drift cero verificado por sha/mounts/ports.
- Bearer cruzado host-to-host por stdin (`mcps-ops` → `daedalus-ops`) sin persistencia intermedia.
- Tests unitarios upstream del ssh-mcp corrieron en container efímero node:22-slim (digest pinneado) sin instalar node en el LXC.

## Suggestions

- Añadir al skill del plane: "edits de source en `mcps` → patcher Python por scp, nunca sed remoto" (cubrirá también el caso de volúmenes de config root-owned).
- M5 (`get_schema`) merece runbook propio de diagnóstico de transporte antes de CERT-E04-01: podría resolverse con `--no-eventStore` o ajuste de buffer del proxy; no bloquea pero degrada la superficie PROD-RO a 2/3 tools útiles.
