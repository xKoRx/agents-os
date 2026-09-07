---
type: change_log
scope: project
created: 2026-07-04
updated: 2026-07-04
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Graphify]]"
related:
  - "[[Economía de Tokens]]"
  - "[[token-economy-indexing-architecture]]"
  - "[[context-router]]"
  - "[[agents-os-context-retrieval]]"
  - "[[graphify]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
  - tech/graphify
---

# 2026-07-04 — Diagnóstico de wikilinks corregido y propagado a todo el Sistema 1

## Motivo

El diagnóstico fundacional del proyecto [[Economía de Tokens]] —"graphify NO captura los
`[[wikilinks]]` de markdown → hace falta un builder standalone"— quedó **SUPERADO** tras el
PoC de código del 2026-07-04. Realidad verificada: graphify **sí** parsea wikilinks
(`extract_markdown`, PR #1376), pero upstream los resolvía **relativo a la carpeta de la nota**
→ en un vault (links cross-folder por nombre/alias) los edges quedaban colgantes. Se corrigió
con un **fork vault-aware** (`graphify-obsidian`, rama `feat/obsidian-vault-wikilinks`, commit
`9c393b7`, gated por `GRAPHIFY_MD_VAULT_ROOT`). El claim viejo seguía vivo en varios docs
canónicos del Sistema 1, contradiciendo la realidad. Esta pasada es **solo alineación de docs**
(no se tocó código de graphify ni el wrapper, ya validados).

## Cambios (docs canónicos alineados)

- **`agents-os/context-router.md`:** callout de Capa 2 pasó de `warning` "NO captura wikilinks
  → builder" a `success` "resuelto vía `graphify-obsidian`; wikilinks = edges `references`;
  relaciona por links, no tags" + query correcta de backlinks.
- **`skills/_shared/graphify-contract.md`:** sección "Structural limitation" reescrita como
  "Markdown wikilinks in the vault (resolved via `graphify-obsidian`)". Nueva subsección
  **"Backlinks query caveat"**: `affected "<note>.md" --relation references` (con `.md` Y la
  relación); `affected "<bare-name>"` cae en H1 → vacío; **NO** usar file-node id (da vacío).
- **ADR `token-economy-indexing-architecture`:** corolario grep/graphify/semántica actualizado
  (Capa 2 del vault funciona vía fork; relaciona por links, no tags). Sección de links tipados
  reencuadrada: `graphify-obsidian` ya emite `references`; los links tipados son enhancement
  futuro del fork (no de un builder separado).
- **known-error `graphify-markdown-wikilink-and-backend-gaps`:** reencuadrado como **RESUELTO**
  (banner `success`); síntoma/causa conservados como referencia histórica (causa matizada:
  era resolución no vault-wide, no ausencia de extractor); builder standalone marcado
  **DESCARTADO** en favor de Vía A; añadido caveat de query; **pitfall operacional (no inventar
  CLI / no borrar `graph.json`) INTACTO**; Evidencia actualizada con la validación 852/852.
- **skill `agents-os-context-retrieval`:** paso 5 y hard rule reescritos (usar
  `graphify-obsidian`; wikilinks = `references`; query de backlinks; no file-node id) +
  entrada en Progress Log.
- **Memoria interna:** corregido el caveat ERRÓNEO ("consultar por file-node id") en
  `2026-07-04-graphify-obsidian-build-continuity`; señal de continuidad en la global
  `agents-os-operating-continuity`.
- **Project note `Economía de Tokens`** (contradicciones que quedaban): panel "Estado actual"
  actualizado; caveat erróneo de la bitácora (file-node id) corregido inline; banner SUPERADO
  en la spec del builder standalone para que un agente fresco no la reimplemente.
- **`30-resources/tools/00-index.md:37`** (hallado por el subagente de consistencia, no por el
  grep inicial): catálogo decía graphify "fuerte en código, **sin extractor de wikilinks**"
  → reescrito a "captura los `[[wikilinks]]` del vault vía el fork `graphify-obsidian` (edges
  `references`)".

## Alcance / decisiones de scope

- **`journal/` NO se tocó** (logs, sessions, feedback del 2026-07-03/04): es historia auditable
  con fecha; reescribirla falsificaría el rastro. Registra lo que se creía entonces.
- **Código de graphify y wrapper NO tocados** (ya validados; fuera de scope).
- El grafo relaciona por **LINKS** (wikilinks → edges `references`), no por tags (tags = Capa 0,
  filtro de frontmatter): explicitado donde algún doc lo ambiguaba.

## Validación

- `grep -rniE "no captura.*wikilink|does not.*wikilink|NO ve los|sin extractor estructural de
  markdown|hace falta.*builder|Layer 2.*only for code|reliable only for code" 80-agents/` — las
  ocurrencias restantes quedan solo en `journal/` (historia, intencional).
- Cadena de referencias consistente: ADR ↔ context-router ↔ skill de retrieval ↔
  graphify-contract ↔ known-error dicen y hacen lo mismo (Capa 2 del vault funciona vía
  `graphify-obsidian`, relaciona por links, caveat de `affected` documentado).
- Pendiente de verificación final: skill `agents-os-hygiene-review` en modo `full-system-1`
  (chequeo DEFINE==IMPLEMENT).
