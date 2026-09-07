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
  - "[[context-router]]"
  - "[[Economía de Tokens]]"
  - "[[token-economy-indexing-architecture]]"
  - "[[agents-os-context-retrieval]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
---

# 2026-07-04 — Context Router implementado + auditoría de consistencia AGENTS OS

## Motivo

Auditoría de consistencia (proyecto [[Economía de Tokens]]): garantizar que lo que
AGENTS OS **define** a los agentes es lo que **implementa**. Cuatro inconsistencias
DEFINE≠IMPLEMENTA detectadas y corregidas. Sin tocar el `agents-os.md` vivo (guard
explícito del proyecto: alta autoridad, solo diseño+aprobación).

## Cambios

- **Skill `agents-os-context-retrieval` ahora IMPLEMENTA el Context Router** (era el
  hueco mayor: el ADR y `context-router.md` decían que la skill lo implementaba, pero
  la skill no lo mencionaba). Se añadió: las 4 capas (cheapest→expensive), la tabla
  intención→ruta, la salida "context pack", el caveat de Capa 2 (wikilinks) y budget
  por suficiencia (reemplaza el objetivo fijo ~3.000 tokens). Nuevas hard rules.
- **`context-router.md`:** principio 2 pasó de "tope duro" a **techo blando por tier**
  (`hecho<relación<síntesis`) + suficiencia-first (fix del token-budget marcado como
  error de diseño). Añadido callout de limitación de Capa 2 en el vault.
- **`_shared/graphify-contract.md`:** `.graphifyignore` promovido de "possible future"
  a **live/in use**; nueva sección "Structural limitation: markdown wikilinks" con el
  hallazgo verificado (AST no captura `[[wikilinks]]` → Capa 2 relacional solo para código).
- **ADR `token-economy-indexing-architecture`:** formalizada la distinción
  **grep=encontrar / graphify=relacionar / semántica=significado** (tabla + corolario).

## Fuentes usadas

- ADR, `context-router.md`, continuidad interna, project note de Economía de Tokens.
- Hallazgo verificado 2026-07-03 sobre el AST de graphify y wikilinks.

## Validación

- Cadena de referencias consistente: ADR ↔ context-router ↔ skill de retrieval ↔
  graphify-contract dicen y hacen lo mismo (4 capas, budget blando, limitación de Capa 2).
- Sin duplicar rationale en la skill (procedimiento en skill, explicación en docs — per
  constitución "una fuente canónica por hecho").
- Sin cambios al `agents-os.md` vivo ni a páginas canónicas de apps.
- Pendiente (otra pista): PoCs de código (builder de link-graph + wrapper) y update de
  `agents-os-hygiene-review`; adelgazar `agents-os.md` (solo diseño, requiere aprobación).
