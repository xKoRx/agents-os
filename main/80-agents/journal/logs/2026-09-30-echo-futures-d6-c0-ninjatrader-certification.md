---
type: change_log
schema_version: 1
scope: session
created: "2026-09-30"
updated: "2026-09-30"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
related:
  - "[[aranea-ssh-mcp]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-30-aranea-ssh-mcp-pool-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo Futures — D6 C0 NinjaTrader physical transport certification

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `10-projects/Echo Futures/artifacts/d6-ninjatrader-certification-20260930/C0-NINJATRADER-PHYSICAL-TRANSPORT-CERTIFICATION.md` (creado — artifact durable del shot con handoff `D6_C0_NINJATRADER = BLOCKED`)
  - `10-projects/Echo Futures/Echo Futures.md` (updated — sección `D6 C0 — NinjaTrader physical transport certification — 2026-09-30` tras el bloque TRANSPORT CERTIFICATION TARGET)
  - `80-agents/journal/agent-runs/2026-09-30-zcode-glm-5.3-flash-d6-ninjatrader-c0.md` (creado)
  - `80-agents/journal/feedback/system-1/2026-09-30-aranea-ssh-mcp-pool-session-feedback.md` (creado)
  - `80-agents/journal/sessions/raw/2026-09-30-d6-ninjatrader-c0-raw.md` (creado, L0)
  - Workspace externo (fuera del vault): `~/aranea/work/d6-nt-cert-20260930/` — helpers MCP, poller, logs de red

## Motivo

- Mandato del owner (shot D6 C0): certificar físicamente sin órdenes la ruta GAU50 → Tradovate → NinjaTrader Desktop como superficie de ejecución candidata, con cierre Agents-OS explícito.

## Fuentes usadas

- Artifact preflight D6 (`d6-earn2trade-preflight-20260930/EARN2TRADE-FIRST-PARTY-PREFLIGHT-RESEARCH.md`); [[Echo + Echo Forge — Environment Contract]]; runbooks [[aranea-ssh-mcp]] y [[aranea-mcp-capability-plane]]; evidencia física en vivo sobre `dev-win` (192.168.31.132) por `aranea-ssh` perfiles `dev-win`/`dev-win-operator`.

## Resolución aplicada

- `D6_C0_NINJATRADER = BLOCKED` (accionable): PASS físico de instalación/versión (NT 8.1.8.3), proceso vivo y conexión estable a `demo.tradovateapi.com:443` ×2 + gateway MD Tradovate `:31655` + endpoints licencia NT; BLOCKED de cuenta GAU50/balance/NQ/market data/posiciones/órdenes/logs por frontera demostrada de la identidad de automatización (ACL perfil KoR denegada, CIM denegado, sesión GUI inaccesible); NOT_TESTABLE_NOW reconnect/restart con poller físico armado. ORDERS_SENT = 0; nada congelado D5/D6 fue tocado; credenciales del owner no persistidas (verificado grep).

## Validación

- Evidencia por comandos con salida capturada (netstat con DNS cruzado, VersionInfo, Get-Process, ACL negativas reproducidas); poller corriendo (`nt-conn-poll.log`); smoke del plano tras recovery (`docker restart ssh-mcp` → initialize 200 + sid + 202). Graphify no validado en esta sesión (binario ausente del PATH de la máquina) — auto-refresh quedará demostrado en la próxima query; journal/agent-runs/feedback/L0/change_log están fuera del índice por contrato.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin credenciales, sin account IDs completos, sin paths de secretos; sólo rutas relativas del vault y workspace registrado.

## Rollback

- Revertir los archivos listados (ninguno muta contratos, código ni configuración de producto); en `dev-win` no hubo ninguna mutación de filesystem/servicios (sólo lecturas y el poller); el único efecto de infra fue `docker restart ssh-mcp` en `mcps` (appliance MCP, recovery documentado del runbook, sin rollback necesario — el servicio quedó healthy con la misma imagen y config).
