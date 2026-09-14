---
type: session-feedback
schema_version: 1
created: "2026-09-14"
updated: "2026-09-14"
area: "[[Aranea]]"
project: "[[HERMES — Bootstrap & Self-Sufficiency]]"
entities:
  - "[[HERMES — Bootstrap & Self-Sufficiency]]"
  - "[[AGENTS OS]]"
aliases: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/feedback
  - scope/session
---

# 2026-09-14-hermes-b2-session-feedback

## Qué funcionó

- OWNER ACTION BUNDLE con descubrimiento de usuario por evidencia (`stat /home/*/.cursor/mcp.json`) + validación de fingerprint pre/post: cero re-trabajos de autoridad; una sola intervención del owner cerró todo B2.
- Patrón ACL scoped sobre paths puntuales del consumer: permitió onboarding real sin dar home access amplio; el rollback quedó demostrado byte-identical.
- Skill `mcp-access-plane-operations` + referencia de transporte: evitó re-diagnóstico de los quirks 406/notifications/SSE.

## Friction (Pain Pattern Candidate)

- **Heredoc-through-ssh corrompe scripts Python con `${...}`/regex:** los patrones `${env:VAR}` de la config MCP chocan con la expansión del shell remoto; dos runs falladas antes de cambiar a `scp` de artefactos versionados en `hermes-managed/bin`. Regla operativa: artefactos multi-línea siempre por `scp`/base64-file, nunca heredoc anidado en `ssh '...'`.

## Gaps detectados

- El proxy auth de las capabilities sólo soporta un bearer single-token por `map nginx` (`__MCP_BEARER_TOKEN__`): el consumer onboarding con bearer dedicado nuevo requiere recrear el container proxy (mutación del plane). Para B3 conviene decidir si el template pasa a multi-bearer o si cada capability acepta N consumers por re-minteo.
- El chain KDE de kor es inaccesible para un identity distinta (correcto); los smokes consumer-side necesitan el bearer inyectado externamente o confiar sólo en la resolución `${env:}`. Documentado como límite del patrón.

## Next

- B3.1 `aranea-mcp-plane-operator` (skill) con los operadores de `hermes-managed/bin` como semilla.
