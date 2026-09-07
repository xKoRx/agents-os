---
type: change_log
scope: project
created: 2026-07-05
updated: 2026-07-05
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-session-close]]"
  - "[[context-router]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
---

# 2026-07-05 — Close Artifact Budget en `agents-os-session-close`

## Motivo

Idea del owner: poner un techo (~1–1.5k tokens) a los archivos de cierre y promover
`[[wikilinks]]` para comprimir sin perder contexto. Encodeada en su versión **segura**
(evita repetir el error del cap de retrieval).

## Cambio

- Nueva sección **"Close Artifact Budget (soft ceiling + link, don't describe)"**:
  - Techo **blando** ~1–1.5k sobre el **andamiaje efímero** (L0 + L1 + feedback), no guillotina.
  - Se cumple **enlazando** (`[[wikilink]]`, que la Capa 2 del fork resuelve), **no truncando**.
  - **L3 exento**: learnings/decisions/known-errors nunca se recortan para caber en un número
    → eso repetiría el error de diseño del cap de contexto. Si no cabe, va a un L3 enlazado.

## Validación

- Coherente con budget semantics de `_shared/graphify-contract.md` (techo blando) y con la
  regla "memorias compactas" de la constitución.
- Primera auto-aplicación del sistema de economía de tokens a su propio cierre (dogfooding):
  este mismo cierre no generó L0/L1/feedback nuevos — enlaza a los del cierre previo.
