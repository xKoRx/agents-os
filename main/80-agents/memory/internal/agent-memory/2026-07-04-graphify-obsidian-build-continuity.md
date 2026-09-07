---
type: agent_memory
schema_version: 1
scope: tool
created: 2026-07-04
updated: 2026-07-07
memory_state: archived
continuity_key: tool/graphify-obsidian-build
superseded_by: "[[graphify-contract]]"
entities:
  - "[[graphify]]"
  - "[[Economía de Tokens]]"
load_policy: manual
indexable: false
index_priority: never
tags:
  - agent/internal
  - kind/agent-memory
  - scope/tool
  - tech/graphify
  - project/agents-os
---

# Continuidad — build aislado `graphify-obsidian` (wikilinks vault-aware)

> [!warning] Archivada
> Paths de outputs y distribución de wheels de esta nota son históricos. Usar
> `[[graphify-contract]]` y `[[graphify-obsidian-install]]` como estado vigente.

Para el próximo agente que toque graphify, el vault-graph o [[Economía de Tokens]].

## Señales de carga

- No cargar en startup ni para operación vigente. Consultar sólo como evidencia
  histórica cuando se investigue la evolución del build aislado de Graphify.

## Continuidad

Hay **3 binarios/wrappers de graphify**, deliberadamente separados:

- `~/bin/graphify` (Work) y `~/bin/graphify-personal` → apuntan al `uv tool`
  **PyPI `graphifyy` 0.8.39** en `~/.local/bin/graphify`. **NO tocar** con
  experimentos: son los contextos limpios.
- `~/bin/graphify-obsidian` → apunta a un **build AISLADO** en
  `~/.local/share/graphify-obsidian/venv/bin/graphify` (fork, `0.9.5`). Este es
  el único que tiene el extractor de wikilinks vault-aware.

El fork vive en `/Users/rjara/fuentes/graphify`, rama
`feat/obsidian-vault-wikilinks` (commit `9c393b7`, solo `graphify/extract.py`).
El venv es un **snapshot** (no editable): editar el fork NO cambia el build
hasta reinstalar.

## Cómo reinstalar el build aislado (tras cambiar el fork)

```bash
uv pip install --python ~/.local/share/graphify-obsidian/venv/bin/python \
  '/Users/rjara/fuentes/graphify[all]'
```

(Checkout de la rama primero. NO usar `uv tool install` del fork: pisaría el
`graphifyy` de PyPI y rompería Work/personal.)

## Señales que me costó levantar

- **graphify SÍ parsea wikilinks** (`extract_markdown`, PR #1376). El gap era
  que resolvía `[[X]]` **relativo a la carpeta de la nota**, no vault-wide. El
  fix es un resolver por nombre/alias gated por `GRAPHIFY_MD_VAULT_ROOT` (lo
  exporta el wrapper). Sin esa env var = idéntico a upstream.
- **Caché AST versionada por esquema, no por versión de paquete.** `update` es
  incremental y reusa `graphify-out/cache/ast/vX/...`. Si arrastrás un
  `graphify-out/` viejo al tmp, reusa extracciones SIN wikilinks. El wrapper ya
  lo excluye del rsync → extracción fresca. Si dudás de un resultado, sospechá
  de caché stale primero.
- **El id del edge debe ser la ruta REAL resuelta** de la nota destino; el
  post-pass `id_remap` de `extract()` (registra `_make_id(str(path))` y
  `_make_id(str(path.resolve()))`) la canoniza al id del nodo-archivo → merge.
- **Caveat de query (CORREGIDO 2026-07-04):** la consulta correcta de backlinks es
  `graphify-obsidian affected "<nota>.md" --relation references` — con el sufijo
  `.md` **y** la relación explícita (`references` no está en las relaciones por
  defecto de `affected`). `affected "<nombre-pelado>"` (sin `.md`) cae en el heading
  `# nombre` si H1==filename → vacío. ⚠️ Lo que antes decía esta nota —"consultá por
  file-node id"— es **INCORRECTO** (da vacío); no lo repitas. El grafo es
  **no-dirigido** (`update` no acepta `--directed`), pero `affected` con
  `--relation references` recorre los edges igual.

## Update 2026-07-05 — página de recurso reconciliada

`30-resources/tools/graphify.md` estaba desfasada (decía VM Hermes, venv
`~/.local/share/graphify-venv/`, `graphifyy 0.9.4`, wrapper `~/.local/bin/`). Ya
**reconciliada** contra el sistema vivo: host **Mac**, build aislado
`~/.local/share/graphify-obsidian/venv` (`0.9.5`), wrapper real `~/bin/graphify-obsidian`;
PyPI Work/personal = `0.8.39`. Añadida la capacidad de wikilinks vault-aware + caveat de
query. Salida viva 2026-07-05: 3311 nodos / 3898 edges (853 `references`, 0 colgantes).
Solo doc; no se tocó código ni wrapper. Log:
`journal/logs/2026-07-05-graphify-resource-page-reconciliation.md`. Para el próximo agente:
si la página vuelve a divergir, la verdad es el `--version` del binario y `~/bin/graphify-obsidian`,
no el frontmatter.

## Update 2026-07-05 — compilado portátil + runbook/skill de instalación

El vault se comparte con varias máquinas/agentes, pero el fork fuente
(`/Users/rjara/fuentes/graphify`) solo está en el Mac del owner. Para instalar en máquinas
que **solo comparten el vault** se dejó un **compilado portátil** que viaja con el vault:

- **`95-graphify/dist/graphifyy-0.9.5-py3-none-any.whl`** — wheel del fork (pure-python,
  `py3-none-any`; deps de PyPI vía extra `[all]`). + copia canónica del wrapper + `BUILD.md`.
- Instalación limpia (sin el fork): `uv pip install "<whl>[all]"` en el venv aislado + copiar
  el wrapper a `~/bin`. Procedimiento en el runbook [[graphify-obsidian-install]].
- Skill `agents-os-graphify-install` decide *cuándo* (comando ausente / exit 42 / venv roto /
  máquina nueva) y ejecuta el runbook.
- Regenerar el compilado: `cd /Users/rjara/fuentes/graphify && uv build --wheel` → copiar a `dist/`.
- **Pendiente:** el install end-to-end en una máquina limpia NO se probó (este Mac ya tiene el
  venv). En la primera máquina nueva, verificar que `uv pip install "<whl>[all]"` resuelva las
  deps de PyPI. Log: `journal/logs/2026-07-05-graphify-obsidian-install-runbook-skill.md`.

## Estado

Feature entregado y validado (852/852 edges resueltos en 576 notas). Falta la
capa de **contexto-mínimo con tope de tokens** sobre el link-graph y
`graphify benchmark`. Ver [[Economía de Tokens]] y el log
`journal/logs/2026-07-04-graphify-obsidian-wikilinks.md`.

## Update 2026-07-07 — Reanudación

El usuario Rodrigo Jara (`rjara`) solicitó retomar el proyecto de Graphify. Se cargó el estado actual y se le informó sobre las tareas pendientes de la Economía de Tokens y el build aislado de `graphify-obsidian`.

## Update 2026-07-07 — Review de "Links Tipados en el Cuerpo" (el owner la implementó)

El owner implementó la mejora de links tipados (ADR § "Relaciones graphifeables") en
`graphify/extract.py` (working tree, **SIN commitear** sobre `9c393b7`). Diseño: verbo antes
del wikilink → `relation` del edge; sin verbo → `references`. Mecánica: `_MD_TYPED_WIKILINK_RE`
+ `_MD_TYPED_INLINE_LINK_RE`, `add_link(..., relation=...)`, y dedup por span (typed corre
primero, el genérico salta spans ya procesados). **Deployment OK:** venv aislado reinstalado,
byte-identical a la fuente (verificado), wheel `dist/graphifyy-0.9.5` regenerada.

**Hallazgos del review (validados ejecutando `extract_markdown` del venv):**

1. **[ALTO] No hay scoping a `## Relaciones`.** El ADR dice que los typed links viven en una
   sección `## Relaciones`, 1 por línea. El parser escanea **todo el body** → prosa incidental
   y, peor, **negaciones** generan edges falsos. Probado: "ya **no depende de** [[servicio-legacy]]"
   → crea edge `depende_de` (invierte el significado); "el usuario **consume** [[api-incidental]]
   en una frase" → crea `consume`. Rompe el determinismo que la feature buscaba (determinístico
   pero incorrecto).
2. **[MEDIO] Fragmentación por variantes bare.** El impl agregó `depende` y `reemplaza` (bare),
   que el ADR **no** lista (canónicos: solo `depende de`, `reemplaza a`). `depende de`→`depende_de`
   pero `depende`→`depende` (relaciones DISTINTAS); idem `reemplaza_a` vs `reemplaza`. Parte el
   grafo: `affected --relation depende_de` no captura los `depende`. Fix: quitar las bare, o
   normalizar ambas al mismo `relation` canónico.
3. **[BAJO/by-design] 1 relación por target.** El dedup `linked_targets` es por nodo destino →
   solo sobrevive el PRIMER edge a un target; un segundo verbo al mismo destino se descarta en
   silencio. Consistente con "un edge por par", pero no se puede expresar 2 relaciones tipadas
   al mismo nodo.
4. **[NIT] Sin tests dedicados** en la suite (solo scratch `test_typed_links.py`). `end` sin uso
   en `start, end = m.span()` (ambos loops genéricos). ReDoS: no aplica (regex lineal, input propio).
5. Vocabulario de relaciones en español mezclado con el core inglés (`references/imports/calls`) —
   ok para fork personal, notar si se upstrea.

**Orden de la alternación SÍ es correcto** (`depende de` antes de `depende`, `reemplaza a` antes
de `reemplaza`) → leftmost-match resuelve bien las formas con partícula. El span-dedup evita
edges dobles. Esas dos cosas están bien.

Recomendación al owner: el #1 es decisión de diseño (scopear a `## Relaciones` vs aceptar
whole-doc); no lo toqué sin aprobación. #2 y #4 son fixes claros. Nada commiteado aún.

**CORREGIDO 2026-07-07** (owner aprobó "vamos por lo definido"): #1 scopeado a `## Relaciones`
(flag `in_relations_section`, abre en heading Relaciones/Relations accent-insensitive, cierra
en heading de nivel ≤; sub-headings profundos mantienen); #2 quitadas las formas bare (regex
= `consume|decora|depende de|expone|reemplaza a`); #3 nit `end` corregido. Nuevo
`tests/test_obsidian_typed_links.py` 6/6 + regresión 56/56. Venv reinstalado + wheel portátil
regenerada + `graphify-obsidian update` limpio (0 edges tipados espurios). ADR y `graphify.md`
reconciliados (ADR = fuente canónica; graphify.md enlaza, no duplica). Log:
`journal/logs/2026-07-07-typed-links-review-corrections.md`.

**COMMIT + VERSIÓN 2026-07-07:** commiteado en la rama como `220fb0a` (local, NO pusheado).
Versión bumpeada **`0.9.5`→`0.9.6`** (el contenido de la wheel cambió → la versión debe
cambiar, anti-drift). Venv reinstalado a 0.9.6; wheel `graphifyy-0.9.6-...whl` desplegada en
`95-graphify/dist/` y la 0.9.5 removida. `dist/BUILD.md` actualizado + nuevo `dist/README.md`
(changelog de versiones). Runbook, `tools/graphify.md` y `tools/log.md` reconciliados a 0.9.6.
Para el próximo agente: la verdad de la versión es `~/.local/share/graphify-obsidian/venv/bin/graphify --version`
y el `pyproject.toml` del fork, no los frontmatter. **Único pendiente real: pushear `220fb0a`
si corresponde** (el runbook instala con glob `graphifyy-*.whl | tail -1`, version-agnóstico).
