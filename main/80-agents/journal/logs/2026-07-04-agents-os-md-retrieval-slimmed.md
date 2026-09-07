---
type: change_log
scope: project
created: 2026-07-04
updated: 2026-07-04
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os]]"
  - "[[context-router]]"
  - "[[Economía de Tokens]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
---

# 2026-07-04 — `agents-os.md` § Retrieval adelgazado (aplicado con aprobación)

## Motivo

Cierre del gap "2 approaches para una abstracción": el maestro `agents-os.md` enseñaba su
propia receta de retrieval (`graphify query --budget 1200`) que competía con el método
canónico (Context Router implementado en la skill). El diff quedó propuesto en
`2026-07-04-doc-phase-token-economy.md` como "NO aplicado — requiere aprobación"; el owner
aprobó explícitamente ("dale si sigue") y se aplicó.

## Cambios

- **`80-agents/agents-os/agents-os.md` § Retrieval:** reemplazada la receta + comandos +
  `--budget 1200` por un **puntero único** a las tres fuentes canónicas: concepto
  ([[context-router]]), implementación (skill `agents-os-context-retrieval`) y contrato
  (`_shared/graphify-contract.md`). Se conserva solo la regla mínima de nivel-mapa
  (subir capas barato→caro, parar al ser suficiente, no cortar por número fijo).
  `updated:` bumped a 2026-07-04.
- **Higiene de links en `tools/`:** `[[00-index|…]]` y `[[README|…]]` (basenames NO únicos:
  3 y 17 ocurrencias) corregidos a ruta absoluta del vault
  (`[[30-resources/tools/00-index|…]]`, `[[30-resources/tools/README|…]]`) para evitar
  wikilinks ambiguos.

## Validación

- `agents-os.md` ya no contiene una segunda receta de retrieval ni `--budget` fijo → un
  solo método canónico en todo el sistema.
- Auditoría de consistencia (subagente, 2026-07-04): sin contradicciones entre los 8
  canónicos.
- Links de `tools/` resuelven a nota única.

## Heads-up pendiente (no bloqueante)

- `30-resources/tools/README.md:102` tiene link pre-existente `[[../00-index|00-index]]` a
  un `30-resources/00-index.md` inexistente (roto de antes; fuera de scope de este cambio).
