---
type: feedback
schema_version: 1
created: "2026-09-15"
area: "[[Aranea]]"
project: "[[HERMES — Agent Access Operations]]"
related:
  - "[[mcp-access-plane-operations]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
---

# 2026-09-15 — Echo runtime access — session feedback

- **Fricción 1 — config bind-mounted de ssh-mcp:** el patcher escribió el config con modo/owner por defecto (644 root:root) y el container entró en crash loop dos veces (644 → "group/world accessible"; 600 root:root → EACCES). Fix: `600` + `65532:65532`. Lección ya convertida en gotcha del skill local y del runbook: cualquier patch del config debe fijar modo/owner explícitos antes del restart.
- **Fricción 2 — orden connect→policy en ssh-mcp:** el negative test del viewer staged no produjo POLICY_DENIED porque el pipeline upstream conecta antes de evaluar policy; el resultado inicial de la sonda lo clasificó como violación (falso). Clasificación corregida a pending-gate; quirk documentado en runbook + skill.
- **Fricción 3 — smoke template desactualizado para ssh-mcp:** `mcp-smoke.py` (canónico para proxys `/mcp`) da 404 contra el endpoint raíz de ssh-mcp y urllib no reenvía el session id del initialize; se resolvió con patrón init-only + header `Mcp-Session-Id` explícito. Candidato a extender el template del skill para la familia ssh.
- **Pain pattern candidate:** los templates de smoke asumen transporte `/mcp` + init-only; ssh-mcp usa `/` + notifications obligatorias + session header — un solo template parametrizable por familia evitaría rediscovery en cada certificación.
