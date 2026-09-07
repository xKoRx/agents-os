---
type: change_log
scope: global
created: 2026-07-07
updated: 2026-07-07
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[graphify]]"
  - "[[AGENTS OS]]"
related:
  - "[[token-economy-indexing-architecture]]"
tags:
  - kind/changelog
  - area/personal
  - project/agents-os
  - tech/graphify
---

# 2026-07-07 — Review + correcciones de "Links Tipados en el Cuerpo"

Review de la implementación de links tipados que hizo el owner en `graphify-obsidian`
(ver log previo `2026-07-07-graphify-obsidian-typed-links.md`). Se validó contra el ADR
[[token-economy-indexing-architecture]], se detectaron 3 defectos y se corrigieron.

## Defectos detectados (validados ejecutando `extract_markdown`)

1. **[ALTO] Sin scoping a `## Relaciones`.** El parser escaneaba todo el body → prosa y
   negaciones forjaban edges tipados falsos ("no depende de [[X]]" creaba `depende_de`).
   Rompía el determinismo que la feature buscaba.
2. **[MEDIO] Fragmentación por formas bare.** `depende`/`reemplaza` (sin partícula) daban
   `relation` distinto de `depende_de`/`reemplaza_a` → partía el grafo. El ADR solo lista
   las formas con partícula.
3. **[BAJO] Nit:** `end` sin uso en `start, end = m.span()`.

## Cambios aplicados

### Código (`graphify/extract.py`, fork rama `feat/obsidian-vault-wikilinks`)
- Regex tipados reducidos a verbos canónicos del ADR: `consume|decora|depende de|expone|reemplaza a` (se quitaron `depende`/`reemplaza` bare).
- Parseo tipado gateado por `in_relations_section`: se activa en un heading `Relaciones`/`Relations` (accent-insensitive) y se cierra en un heading de nivel ≤ al que la abrió; sub-headings más profundos la mantienen. Fuera de la sección, los links caen a `references`.
- Nit `end` corregido (`start = m.start()`).

### Tests
- Nuevo `tests/test_obsidian_typed_links.py` (6 casos: verbos canónicos, scoping, negación en prosa → references, sub-heading mantiene sección, heading hermano la cierra, sin formas bare). 6/6 verdes; regresión obsidian/markdown/wiki 56/56 verdes.

### Versión + Deployment
- **Commit** `220fb0a` en la rama `feat/obsidian-vault-wikilinks` (local, NO pusheado): extract.py + tests + bump de versión.
- **Versión bumpeada `0.9.5`→`0.9.6`** (`pyproject.toml`): el contenido de la wheel cambió (typed links), así que la versión debe cambiar (anti-drift).
- Venv aislado reinstalado a `0.9.6` (`uv pip install --python ~/.local/share/graphify-obsidian/venv/bin/python '/Users/rjara/fuentes/graphify[all]'`).
- Wheel portátil regenerada (`uv build --wheel`) → `95-graphify/dist/graphifyy-0.9.6-py3-none-any.whl` desplegada; **wheel 0.9.5 removida** del dist.
- `graphify-obsidian update` sobre el vault real: 3379 nodos / 3966 edges (867 `references`, 0 edges tipados espurios porque aún no hay secciones `## Relaciones` con contenido). Sin crashes.

### Documentación (economía de tokens: una fuente canónica por hecho)
- **ADR** § "Relaciones graphifeables": pasó de "mejora futura, aún no implementada" a contrato implementado (verbos canónicos, mapeo espacio→`_`, scoping a `## Relaciones`, sin bare, query con `--relation`). Fuente canónica del hecho.
- **`30-resources/tools/graphify.md`**: la línea de typed links se corrigió y ahora **enlaza al ADR** en vez de duplicar la lista de verbos (evita drift); menciones de versión → `0.9.6`.
- **`95-graphify/dist/`**: `BUILD.md` actualizado (versión, commit, filename, fecha) + nuevo `README.md` con changelog de versiones (0.9.6 typed links / 0.9.5 wikilinks).
- **Runbook** [[graphify-obsidian-install]] y **`tools/log.md`**: versión reconciliada a `0.9.6`.

## Pendiente
- Commit `220fb0a` está **local** (no pusheado); pushear si/cuando corresponda.
- Sin contenido real: ninguna nota tiene `## Relaciones` todavía. Cuando se pueble, correr `graphify-obsidian update` y validar edges tipados con `affected --relation <tipo>`.
