---
type: tool
schema_version: 1
status: active
scope: tool
area: "[[Personal]]"
project: "[[AGENTS OS]]"
source_url: https://github.com/safishamsi/graphify
command:
  - graphify
  - graphify-obsidian
  - graphify-personal
entities:
  - "[[Graphify]]"
  - "[[AGENTS OS]]"
related:
  - "[[graphify-contract]]"
  - "[[graphify-markdown-wikilink-and-backend-gaps]]"
  - "[[Economía de Tokens]]"
  - "[[token-economy-indexing-architecture]]"
aliases:
  - Graphify
  - graphify
  - graphify-obsidian
  - graphify-personal
load_policy: when_tool_loaded
indexable: true
index_priority: high
tags:
  - area/personal
  - kind/resource
  - kind/tool
  - priority/high
  - project/agents-os
  - project/agentsos
  - scope/tool
created: 2026-06-27
updated: 2026-09-03
installed_host: Mac (owner)
installed_obsidian: 2026-07-04
installed_path: ~/.local/share/graphify-obsidian/venv/bin/graphify
installed_version_obsidian: "0.9.6.post2"
installed_version_pypi: "0.8.39"
wrapper_path: ~/bin/graphify-obsidian
---

# graphify

> [!info]+ graphify
- **Proyecto:** [[AGENTS OS]]
- **Upstream:** https://github.com/safishamsi/graphify
- **Fork vault-aware:** repo `graphify` bajo [[Fuentes — Workspace de repositorios]] (rama `feat/obsidian-vault-wikilinks`)
- **Contrato operativo:** [[graphify-contract]]
- **Estado en el Mac del owner (2026-09-03):** ✅ **INSTALADO.** `graphify-obsidian` corre un build aislado del fork en el venv `~/.local/share/graphify-obsidian/venv/` (`graphify 0.9.6.post2`), invocado por `~/bin/graphify-obsidian`. Binario, índice, reportes y query logs son locales a la máquina; el vault contiene sólo Markdown y el wrapper canónico pequeño.

## Descripcion

Graphify (upstream) es un **skill de Claude Code** construido por Safi Shamsi:
lee archivos (código, Markdown, PDFs, imágenes vía Claude Vision), construye
un **grafo de conocimiento multimodal**, y devuelve estructura que no era
visible leyendo los archivos sueltos.

Es un *wrapper* práctico del sistema de retrieval que el proyecto
[[AGENTS OS]] ya define como canónico: en este vault, Graphify cumple el
rol de **índice derivado** sobre las notas Markdown, dejando Markdown
como fuente de verdad. Toda la "política de retrieval" de
[[AGENTS OS]] asume que Graphify es el mecanismo primario; este doc
detalla **qué hace concretamente** y **cómo se invoca**.

Cada edge del grafo está etiquetada como `EXTRACTED` (encontrada), `INFERRED`
(inferida por LLM con nivel de confianza) o `AMBIGUOUS` (dudosa). El reporte
siempre distingue lo encontrado de lo adivinado — requisito central de
honestidad operativa.

## Wikilinks del vault (fork vault-aware)

> Capacidad exclusiva del build `graphify-obsidian`. Fuente de verdad canónica:
> [[graphify-contract]], known-error [[graphify-markdown-wikilink-and-backend-gaps]],
> proyecto [[Economía de Tokens]].

El AST de graphify **sí** parsea los `[[wikilinks]]` de Obsidian (`extract_markdown`,
PR #1376), pero upstream los resolvía **relativos a la carpeta de la nota** → en un
vault (links cross-folder por nombre/alias) los edges quedaban colgantes, dando el
falso positivo de "no captura wikilinks". El **fork vault-aware** `graphify-obsidian`
—gated por `GRAPHIFY_MD_VAULT_ROOT`, que exporta el wrapper— los resuelve **vault-wide**
por nombre de nota + alias de frontmatter. Consecuencias:

- Los `[[wikilinks]]` del vault **son edges de relación `references`** (o relaciones tipadas específicas si se usa un prefijo verbal) en el grafo. `affected` y `path` los recorren. Validado en el vault real (2026-07-04): **852/852 reference edges resueltos, 0 colgantes**; salida viva 2026-07-05: **853 edges `references`, 0 colgantes**.
- **Enlaces tipados en el cuerpo (2026-07-07):** dentro de una sección `## Relaciones`, un verbo canónico antes del wikilink define el `relation` del edge (`depende de [[X]]` → `depende_de`). **Solo** se tipan ahí: fuera de esa sección un verbo es prosa (una negación "no depende de [[X]]" NO debe forjar el edge) y el link cae a `references`. Verbos canónicos y forma de escritura: fuente única en el ADR [[token-economy-indexing-architecture]] (§ Relaciones graphifeables); no se duplican acá para evitar drift.
- El grafo relaciona por **links** (`[[wikilinks]]` → edges `references`/tipados), **no por tags** — los tags quedan en Capa 0 (filtro de frontmatter), nunca son edges.
- No hace falta builder standalone: se resolvió por la **vía A (fork)**, no por un builder separado (spec de builder descartada; ver [[Economía de Tokens]]).
- Sin la env var `GRAPHIFY_MD_VAULT_ROOT`, el comportamiento es byte-idéntico a upstream (relative-only). El `graphify` (Work) y `graphify-personal` de PyPI **no** tienen esta capacidad.

### Caveat de query de backlinks (verificado)

```bash
graphify-obsidian affected "<nota>.md" --relation references
```

- Usar el **sufijo `.md`** Y la **relación explícita**: `references` no está entre las
  relaciones por defecto de `affected`, así que omitir `--relation references` se pierde
  esos edges.
- `affected "<nombre-pelado>"` (sin `.md`) cae en el nodo **heading** `# nombre` cuando
  el H1 == filename → resultado vacío.
- **No** consultar por file-node id como workaround: da vacío (una nota vieja lo
  afirmaba; era incorrecto).

## Funcionalidad real (upstream)

| Modo | Qué hace |
|---|---|
| `graphify <dir>` | Indexa un directorio completo en un grafo + reporte |
| `graphify <dir> --update` | Re-indexa solo lo cambiado (SHA256 cache) |
| `graphify <dir> --mode deep` | Más extracción de edges `INFERRED` |
| `graphify <dir> --watch` | Auto-sync mientras editás |
| `graphify <dir> --wiki` | Genera wiki navegable (index.md + artículos) |
| `graphify <dir> --svg / --graphml / --neo4j` | Exporta grafo visual |
| `graphify <dir> --mcp` | Levanta servidor MCP stdio |
| `graphify hook install` | Post-commit git hook que re-indexa |
| `graphify query "..."` | Pregunta libre sobre el grafo ya construido |
| `graphify path A B` | Camino entre dos nodos |
| `graphify explain "Entidad"` | Resume una entidad |

Inputs aceptados: `.py .ts .js .go .rs .java .c .cpp .rb .cs .kt .scala
.php` (AST tree-sitter + call-graph), `.md .txt .rst` (conceptos+rels
vía Claude), `.pdf` (citation mining + conceptos), imágenes.

Output estándar:

```text
graphify-out/
├── graph.html        grafo interactivo (vis.js)
├── obsidian/         vault Obsidian navegable a partir del grafo
├── wiki/             artículos estilo wiki (--wiki)
├── GRAPH_REPORT.md   god nodes, conexiones sorprendentes, preguntas sugeridas
├── graph.json        grafo persistente (consultable semanas después)
└── cache/            SHA256 cache para incremental
```

## Uso principal

- **Recuperar contexto barato** (cheapest path) antes de abrir carpetas
  o leer archivos. Patrón canónico: `<entidad> + <tipo de conocimiento>
  + <tema>`.
- **Auditar cohesión** conceptual, dependencias y rotura de relaciones.
- **Validar entidades canónicas** — alias, slug y links deben resolver a
  una sola nota Markdown.
- **Excluir del retrieval** raw sessions, logs, scratch y outputs de
  beta. Esto se hace vía `.graphifyignore`.

Reducción de tokens: ~**71× menos tokens por query** vs leer archivos
crudos, medida por el autor en corpus Karpathy (52 archivos). En el
vault actual la salida viva (2026-07-05) reporta **3311 nodos, 3898
edges (3038 `contains`, 853 `references`, 7 `calls`), 276 comunidades,
100% EXTRACTED** (sin INFERRED/AMBIGUOUS).

## Comandos (estado por entorno)

Los tres comandos son **wrappers del Mac del owner** (`~/bin/`), deliberadamente
separados para que el fork de Obsidian no contamine los contextos limpios de Work/personal:

| Comando | Función | Backend real |
|---|---|---|
| `graphify-obsidian` | Indexa y consulta **este vault** (único con wikilinks vault-aware) | ✅ Build aislado en `~/.local/share/graphify-obsidian/venv/bin/graphify`; wrapper `~/bin/graphify-obsidian`, caché resuelto por `cache-path` fuera del vault |
| `graphify` | Indexa repos de **Work/Meli** (reservado a `/Users/rjara/fuentes`) | ✅ Wrapper `~/bin/graphify` → PyPI `graphifyy 0.8.39` (`~/.local/bin/graphify`) |
| `graphify-personal` | Indexa **repos personales** del owner | ✅ Wrapper `~/bin/graphify-personal` → misma PyPI `graphifyy 0.8.39` |

> **Aislamiento (verificado 2026-07-05):** solo `graphify-obsidian` corre el fork
> (`0.9.6`) con el extractor de wikilinks; `graphify` y `graphify-personal` siguen en
> `graphifyy 0.8.39` de PyPI, intactos. Editar el fork en `/Users/rjara/fuentes/graphify`
> **no** cambia el build hasta reinstalar el venv aislado (ver más abajo). El wrapper legacy
> `graphify-aranea` **ya no existe** (retirado; no reintroducir).

## Estado actual (Mac del owner)

- ✅ **Build aislado del fork** en `~/.local/share/graphify-obsidian/venv/bin/graphify` (`graphify 0.9.6`, rama `feat/obsidian-vault-wikilinks`). Es el único con wikilinks vault-aware.
- ✅ Wrapper `~/bin/graphify-obsidian`: copia segura del vault a un temporal único, exporta `GRAPHIFY_MD_VAULT_ROOT`, publica atómicamente en caché local y auto-refresca ante queries cuando detecta cambios.
- ✅ `graphify` (Work) y `graphify-personal` en `graphifyy 0.8.39` de PyPI (`~/.local/bin/graphify` → `~/.local/share/uv/tools/graphifyy/`), **sin** la capacidad de wikilinks. No se pisan con el fork.
- ✅ Grafo derivado local fuera del vault; resolver con `graphify-obsidian cache-path`.
- ✅ Smoke tests: `query`, `explain`, `path`, `affected` operativos.

### Reinstalar el build aislado (tras cambiar el fork)

```bash
# checkout de la rama del fork primero
uv pip install --python ~/.local/share/graphify-obsidian/venv/bin/python \
  '/Users/rjara/fuentes/graphify[all]'
```

> ⚠️ **No** usar `uv tool install` del fork: pisaría el `graphifyy` de PyPI y rompería
> `graphify` (Work) y `graphify-personal`. El venv aislado es un snapshot: editar el fork
> NO cambia el build hasta reinstalar.

### Instalar en otra máquina

Cada máquina provisiona el fork desde un wheel local o desde un checkout indicado
por `AGENTS_OS_GRAPHIFY_SOURCE`. El vault no transporta wheels ni estado derivado:

- **Compilado local:** `~/.local/share/graphify-obsidian/dist/graphifyy-*.whl`.
- **Wrapper canónico:** `80-agents/skills/agents-os-graphify-install/scripts/graphify-obsidian`.
- **Runbook:** [[graphify-obsidian-install]] (`80-agents/memory/public/runbook/graphify-obsidian-install.md`).
- **Skill:** `agents-os-graphify-install` (decide cuándo y ejecuta el runbook).

Regenerar el compilado (Mac del owner): `cd /Users/rjara/fuentes/graphify && uv build --wheel`
y guardarlo fuera del vault bajo `~/.local/share/graphify-obsidian/dist/`.

## Instalación histórica (referencia — ya no es necesario correrla)

> Esta sección documenta **cómo se instaló** la primera vez. La instalación real está aplicada y operativa; no requiere repetición.

```bash
# Opción A — pipx (recomendada, vendor isolation)
uv tool install graphifyy
uv tool run graphify install   # o: ~/.local/bin/graphify install

# Opción B — pip con --user (si pipx no aplica)
uv pip install --system graphifyy   # en PEP 668 envs suele fallar
# Alternativa: uv pip install --system --break-system-packages graphifyy
graphify install

# Opción C — install manual del skill (sin paquete Python)
mkdir -p ~/.claude/skills/graphify
curl -fsSL https://raw.githubusercontent.com/safishamsi/graphify/v1/skills/graphify/skill.md \
  > ~/.claude/skills/graphify/SKILL.md
```

> Nota: esto documenta el install del paquete PyPI `graphifyy` (el que hoy usan
> `graphify`/`graphify-personal`). El build de `graphify-obsidian` es un fork aislado
> aparte — su (re)instalación está en "Estado actual (Mac del owner)".

Para indexar el vault se usa el wrapper (no el binario crudo):

```bash
graphify-obsidian query "AGENTS OS"   # refresca si está stale y luego consulta
```

Ubicación del output: `graphify-obsidian cache-path`.

## Operaciones / comandos

```text
update                 → refresca el índice AST (SIN LLM). Esqueleto estructural.
extract --mode deep    → extracción AST + semántica LLM (conceptos + edges INFERRED).
query <text> --budget  → devuelve candidatos, snippets o resúmenes enfocados
explain <entity>       → resume una entidad del grafo
path <a> <b>           → explica la relación o camino entre dos nodos
```

> ⚠️ **Corrección verificada contra el CLI real (2026-07-02 en v0.9.4; vigente en v0.9.6):**
> `--mode deep` pertenece a **`extract`**, NO a `update`. `graphify-obsidian update --mode deep`
> falla con `error: unknown update option: --mode`. `update` es AST puro (sin LLM):
> si solo se corre `update`, el grafo queda 100% `_origin: ast` (esqueleto de headings)
> y las queries devuelven títulos de sección, no entidades ni relaciones conceptuales.
> La capa semántica (nodos-concepto + `INFERRED`) requiere `extract` con backend
> (`--backend gemini|claude|openai|ollama|...`). Sin API key cloud, el único backend
> local disponible en el Mac es ollama (`deepseek-r1:14b`).
> `update` **sí** respeta `.graphifyignore` y purga paths recién excluidos en el rebuild.

## Entradas y salidas

- **Input:** un directorio (Markdown, código, PDFs, imágenes) + opcional `.graphifyignore`.
- **Output:** `graph.html` + `graph.json` + `GRAPH_REPORT.md` + opcional `wiki/` y/o `obsidian/`.

## Integraciones

- [[AGENTS OS]] (rol canónico: índice derivado)
- [[graphify-contract]] (contrato operativo en este vault)
- Índice local por máquina (`graphify-obsidian cache-path`)
- `~/aranea/topology/*` (cuando se aplique al homelab Aranea)
- `30-resources/aranea/` (documentación del cluster, indexable desde 2026-07+)

## Reglas de uso

- Graphify **es índice derivado, no fuente de verdad**. La nota
  canónica sigue siendo el `.md` original.
- **Nunca** crear entidades paralelas por diferencias de casing, acentos,
  singular/plural o alias — las variantes viven en `aliases`.
- Queries genéricas (`retrieval`, `pendiente`, `graphify`) son ruido
  conocido. Usar el patrón canónico de búsqueda.
- Distinguir siempre **lo que el grafo encontró** de **lo que
  inventó** (edge tags EXTRACTED/INFERRED/AMBIGUOUS). No presentar
  INFERRED como hecho.
- raw sessions, logs y scratch **no entran al grafo** (`.graphifyignore`
  debe excluirlos explícitamente).
- Nunca ejecutar el binario crudo `graphify` dentro del vault ni copiar
  `graphify-out/`, histories, reports, HTML, manifests, caches o wheels al vault.

## Links

- [[AGENTS OS]]
- [[graphify-contract]] — contrato operativo (fuente de verdad de comandos/wikilinks)
- [[graphify-markdown-wikilink-and-backend-gaps]] — known-error (gaps + caveat de query)
- [[Economía de Tokens]] — proyecto que resolvió los wikilinks vault-aware (vía A)
- [[token-economy-indexing-architecture]] — ADR de arquitectura de indexación
- [[Graphify Center]]
- Repo upstream: https://github.com/safishamsi/graphify
- Fork vault-aware: `/Users/rjara/fuentes/graphify` (rama `feat/obsidian-vault-wikilinks`)
- Estado y salida viva: `graphify-obsidian status` / `graphify-obsidian cache-path`
