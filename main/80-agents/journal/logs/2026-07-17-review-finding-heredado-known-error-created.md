---
type: change_log
scope: global
created: 2026-07-17
updated: 2026-07-17
area: "[[Meli]]"
entities:
  - "[[AGENTS OS]]"
  - "[[vpp-backend]]"
related:
  - "[[review-finding-heredado-confundido-con-regresion]]"
  - "[[2026-07-17-vpp-bajo-precio-motors-review-overedit-summary]]"
source_session: "codex-vpp-backend-2026-07-17-review-findings"
tags:
  - kind/change-log
  - scope/global
  - workflow/code-review
---

# Known error: finding heredado confundido con regresión

## Cambio

- `created`: `80-agents/memory/public/known-error/agents-os/review-finding-heredado-confundido-con-regresion.md`.
- `updated`: `80-agents/memory/public/user-preference/rjara-agent-profile.md` con una regla dura diff-first.
- `created`: continuidad interna y artefactos de cierre de la sesión.

## Tipo

- `created` / `updated`.

## Motivo

- En una sesión de review de `vpp-backend`, se interpretó un finding heredado de `develop` como regresión de la branch y se hicieron ediciones innecesarias antes de revertirlas.

## Duplicate check

- Se revisaron `preserve-legacy-semantics-when-extending-feature` y `diff-audit-diagnostic-leftovers`; el nuevo known error cubre específicamente el fallo de juicio “finding del review ≠ delta de la branch”.

## Evidencia

- El repositorio terminó con `git diff HEAD` vacío y el aprendizaje quedó respaldado por el diff/historial local de la sesión.
