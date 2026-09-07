---
type: runbook
scope: global
created: "2026-07-02"
updated: "2026-09-03"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Graphify]]"
related:
  - "[[graphify]]"
  - "[[graphify-contract]]"
aliases:
  - resource wiki lint reindex
  - reindex y lint de la resource wiki
  - graphify corpus purge
confidence: high
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - area/personal
  - project/agents-os
  - tech/graphify
  - scope/global
---

# Resource Wiki — Lint & Reindex (con purga de corpus Graphify)

%% Routing: area/project/entities/related usan links canónicos. Aliases son variantes. %%

## Propósito

Procedimiento mecánico para (1) mantener el corpus de Graphify limpio y (2) validar
la salud de la resource wiki (cobertura del índice + huérfanos). Lo invoca la skill
`agents-os-resource-wiki` (operación *lint*) o un humano. No decide *cuándo* se
ejecuta; ejecuta cuando lo llaman.

## Precondiciones

- Wrapper `graphify-obsidian` disponible (query/explain sin reindex; sin arg = reindex).
- `.graphifyignore` en la raíz del vault (`main/`) actualizado.

## Contexto (por qué existe la purga)

Auditoría 2026-07-02 del grafo vivo (3806 nodos) encontró corpus contaminado:
- 512 nodos desde `30-resources/trash/` (no estaba en `.graphifyignore`).
- 170 nodos desde un `*.json` (schema): keys `$schema/type/properties/enum` entraban
  como god-nodes genéricos y arruinaban la precisión de las queries.
- 190 nodos desde `40-archive/` **pese a estar** en `.graphifyignore` → los ignores
  nuevos no purgan nodos ya cacheados: **requiere rebuild limpio**.
- `_origin` = 100% `ast` → el grafo era un esqueleto estructural (headings/identifiers),
  sin capa semántica. Por eso las queries devolvían tokens de heading, no entidades.

## Procedimiento

1. **Verificar exclusiones** en `main/.graphifyignore` (deben estar): `trash/**`,
   `**/*.json`, `95-graphify/**`, `graphify-out/**`, `**/GRAPH_REPORT.md`,
   `**/graph.json`, `**/graph.html`, `40-archive/**`, `80-agents/journal/**`,
   `00-inbox/**`.
2. **Rebuild — SOLO `update` (AST, sin LLM). Modo canónico del vault.**
   El wrapper construye en un temporal único y promueve el grafo al cache local.
   ```bash
   graphify-obsidian update           # subcomando 'update' = AST only, no LLM
   ```
   > **Decisión 2026-07-03: la wiki se opera con ÍNDICES, no con capa semántica.**
   > Retrieval primario = `00-index.md` curado de cada dominio. Graphify (grafo AST)
   > = índice estructural derivado para navegación/paths/lint. Que el grafo sea 100%
   > `_origin: ast` es lo **esperado**, NO un defecto.
   >
   > **Capa semántica (`extract --mode deep`) — PARQUEADA, no usar.** `--mode deep`
   > es de `extract`, no de `update` (`update` da `error: unknown update option: --mode`).
   > El free tier de Gemini NO alcanza (verificado 2026-07-03): `gemini-2.0-flash`
   > quota 0; `gemini-3-flash` solo 5 req/min → el extract del vault (7 chunks) cae
   > por 429. Encender solo con billing pago si algún día se justifica. No es
   > requisito para la wiki.
3. **Validar corpus** (los 3 deben dar 0):
   ```bash
   GRAPH_DIR="$(graphify-obsidian cache-path)" python3 - <<'EOF'
import os
import json
from pathlib import Path
d=json.loads((Path(os.environ["GRAPH_DIR"]) / "graph.json").read_text())
n=d["nodes"]
def cnt(p): return sum(1 for x in n if (x.get("source_file","") or "").startswith(p))
print("trash:", sum(1 for x in n if "/trash/" in (x.get("source_file","") or "")))
print("archive:", cnt("40-archive/"))
print("json:", sum(1 for x in n if (x.get("source_file","") or "").endswith(".json")))
import collections
print("_origin:", dict(collections.Counter(x.get("_origin","?") for x in n)))
EOF
   ```
4. **Validar retrieval** con nombre canónico (no tokens genéricos):
   ```bash
   graphify-obsidian explain "search-middleware"
   graphify-obsidian query "search-middleware application decoración" --budget 1000
   ```
   Con grafo AST devuelve el documento + sus headings (navegación estructural), NO
   nodos basura `type/properties/resource` (esos ya se purgaron). Para el "¿qué página
   abro?" fino, el retrieval real es el `00-index.md`, no el grafo.
5. **Lint de la wiki** — cobertura del índice y huérfanos de un dominio:
   ```bash
   DOM=~/obsidian/SecondBrain/main/30-resources/applications
   # páginas sin fila en el índice (posibles faltantes en 00-index.md):
   for f in "$DOM"/*.md; do b=$(basename "$f" .md); \
     case "$b" in 00-index|log) continue;; esac; \
     grep -q "\[\[$b\]\]" "$DOM/00-index.md" || echo "FALTA en índice: $b"; done
   ```
6. Registrar el resultado en el `log.md` del dominio (`## [fecha] lint | ...`).

## Validación

- Paso 3: `trash=0`, `archive=0`, `json=0`. `_origin` = 100% `ast` es lo esperado
  (operamos con índices, sin capa semántica).
- Paso 4: `explain`/`query` retornan la nota/estructura esperada, sin nodos basura.
- Paso 5: sin líneas "FALTA en índice" (o registradas como pendientes en `log.md`).

## Rollback / recuperación

- El grafo es **derivado y desechable**: si un rebuild sale mal, se re-corre. No hay
  pérdida de verdad (la verdad son los `.md`).
- El wrapper conserva el último índice válido y sólo promueve resultados completos.
  Para reconstruir explícitamente, correr `graphify-obsidian update`.
- Los cambios a `.graphifyignore` son texto plano versionable: revertir con el editor.

## Evidencia

- Auditoría de nodos 2026-07-02 (sesión piloto Resource Wiki).
- [[graphify]] · [[30-resources/00-RESOURCE-WIKI|Resource Wiki]] ·
  skill `agents-os-resource-wiki`.
