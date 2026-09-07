---
type: project
owner: me
root: true
status: active
priority: P2
area: "[[Personal]]"
parent:
sprint:
start: 2026-07-03
due:
progress: 80
repo:
jira:
prs:
aliases:
  - token economy
  - sistema de indexación
  - token economy indexing
  - proyecto de economía de tokens
tags:
  - project
  - area/personal
  - project/agents-os
created: 2026-07-03
updated: 2026-07-10
---

# Economía de Tokens

%% Naming: Economía de Tokens es el link canónico; aliases guarda variantes. %%

> [!info]+ Economía de Tokens
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P2
> Iniciativa raíz. Sistema de indexación/tageo para que un agente entienda lo necesario
> cargando **solo el mínimo** al contexto. Cero basura.

## 🎯 Objetivo

- Construir un sistema de indexación óptimo en tokens: **tags → índice curado → grafo → cuerpo**,
  cada capa filtra antes de la siguiente. Fuente de verdad = markdown; retrieval = mínimo.
- Arquitectura canónica en el ADR [[token-economy-indexing-architecture]]; el "cómo cargar"
  lo gobierna el concepto [[context-router]].
- **Destino:** este sistema se **compartirá y evangelizará a un equipo de TI** → debe ser
  útil y aportar valor, no solo prolijo.

## 📊 Estado actual

- ADR aprobado (4 capas + roles). Piloto de wiki en `applications/` andando.
- Graphify AST limpio (3163 nodos, sin basura). Semántica LLM parqueada (free tier insuficiente).
- **Capa 2 del vault RESUELTA 2026-07-04:** el fork vault-aware `graphify-obsidian` convierte los
  `[[wikilinks]]` en edges `references` (852/852 resueltos, 0 colgantes). El grafo relaciona por
  **links**, no por tags. El diagnóstico viejo ("graphify no captura wikilinks → hace falta
  builder") quedó **superado** (era resolución no vault-wide, no ausencia de extractor); builder
  standalone descartado en favor de la Vía A (fork). Ver § Decisiones.

## 🔬 Evaluación de graphify (repo completo en `/Users/rjara/fuentes/graphify`, 2026-07-03)

- **En CÓDIGO es potente y NO es humo:** corrido sobre su propio repo dio **10.316 nodos /
  17.320 edges / 899 comunidades**; `explain "extract"` = grado 218 con edges reales
  `imports/calls/contains` (EXTRACTED). Ese es el payoff para tus proyectos de código.
- **En MARKDOWN es estructuralmente inerte:** `detect.py` mete `.md/.txt/.rst/.html/.yaml`
  en `DOC_EXTENSIONS` → tipo `DOCUMENT`, que **solo** pasa por la capa semántica (LLM). NO
  hay extractor estructural de markdown ni de wikilinks (los `extractors/` son solo lenguajes
  de código). Por eso sin LLM un `.md` es casi un nodo suelto → confirma el hallazgo.
- **El schema de extracción es ENCHUFABLE** (`ARCHITECTURE.md`): todo extractor devuelve
  `{nodes, edges}`, `validate.py` lo valida y `build_graph → cluster → analyze → export →
  serve` lo consumen. Además existe `merge-graphs` (combinar grafos) y `serve.py --mcp`
  (exponer el grafo como tool a agentes) y `benchmark.py` (medir ahorro de tokens).
- **Consecuencia para el builder:** no reemplazamos graphify — **emitimos su schema**. Nuestro
  builder escanea `[[wikilinks]]` → produce `{nodes, edges}` (confidence EXTRACTED) → y lo
  enchufamos al pipeline de graphify (build/cluster/analyze/export/MCP) **gratis y sin LLM**.

## 🛠️ PoC builder de link-graph — spec de handoff (para otra IA)

> [!warning] SUPERADO 2026-07-04 — spec histórica, NO implementar
> Este builder standalone quedó **descartado**: se resolvió por la **Vía A (fork
> `graphify-obsidian`)**, que ya emite los `[[wikilinks]]` como edges `references`. La spec de
> abajo se conserva como registro de la investigación; **no la reimplementes**. Ver § Decisiones
> y la nota interna `2026-07-04-graphify-obsidian-build-continuity`.

> Auto-contenida: otra IA debe poder construirla **sin esta conversación**. Leer también
> [[token-economy-indexing-architecture]] (arquitectura) y [[context-router]] (para qué sirve).

- **Objetivo:** escanear los `[[wikilinks]]` del vault y emitir un grafo en el **schema de
  graphify** (`{nodes, edges}`), integrable a su pipeline. Determinístico, sin LLM.
- **Por qué:** graphify (AST) NO parsea wikilinks de markdown (verificado; ver Evaluación).
- **Input:** raíz del vault `/Users/rjara/obsidian/SecondBrain/main`, **respetando
  `.graphifyignore`** (excluir trash/json/archive/journal/inbox/salidas de graphify).
- **Output (schema graphify, ver `ARCHITECTURE.md` del repo):**
  - `nodes`: una por nota `.md`. **`id` DEBE seguir la convención de graphify
    `{parent_dir}_{stem}`** (ver `graphify/extract.py`, "File-level node ID") o el `merge`
    no unirá los nodos. `label` = título/filename; `source_file` = ruta relativa.
  - `edges`: por cada `[[target]]`/`[[target|alias]]` en el cuerpo → `{source, target,
    relation:"references", confidence:"EXTRACTED"}`. Resolver `target` a nota canónica
    (filename/alias) antes de emitir.
- **Integración:** validar contra `validate.py` y combinar con `graphify merge-graphs`
  (o `--out`), reusando `build/cluster/analyze/export/serve --mcp`.
- **Criterios de aceptación (medibles):**
  1. `graphify explain "recommendations-decoration-sdk"` **encuentra** el nodo.
  2. `graphify affected "java-polycard-sdk"` devuelve las ≥3 notas que lo enlazan.
  3. `graphify path "vpp-backend" "vis-octopus-lib"` **resuelve** un camino.
  4. 0 nodos desde `trash/`, `*.json`, `40-archive/` (respeta `.graphifyignore`).
- **Referencias:** repo en `/Users/rjara/fuentes/graphify` (`ARCHITECTURE.md`,
  `graphify/extract.py`, `graphify/detect.py`, `graphify/validate.py`, `merge-graphs`).

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Ver [[convenciones]]. %%
> - [r] [[AGENTS OS - Evaluación y Adopción]] arrancar + seguimiento #owner/me #type/supervision #area/personal — Grid v2 publicado y verificado; listo para revisión humana.
> - [x] Formalizar en el ADR la distinción **grep=encontrar / graphify=relacionar / semántica=significado** #owner/me #type/research #area/personal
> - [x] Agregar **política de escalado del índice** (plano → sub-índices jerárquicos tipo aranea) a `00-RESOURCE-WIKI.md` #owner/me #type/dev #area/personal
> - [x] Diseñar **índices graphifeables**: links tipados en cuerpos (`consume [[X]]`, `decora [[Y]]`) + evaluar `RELATIONS.md`/MOC por dominio #owner/me #type/research #area/personal — decidido: relación se escribe 1 vez en `## Relaciones` del cuerpo; edge-list/MOC se GENERA con el builder, no a mano. En ADR.
> - [x] PoC **builder de link-graph propio**: escanea `[[wikilinks]]` → emite `{nodes,edges}` en **schema de graphify** (confidence EXTRACTED) → integrar vía `merge-graphs` o extractor propio. Reusa build/cluster/analyze/export/MCP, gratis y sin LLM #owner/me #type/dev #area/personal — **2026-07-04 RESUELTO por vía A (fork), no builder standalone.** `extract_markdown` de graphify ya emitía nodo+headings pero resolvía `[[X]]` solo a hermanos de carpeta; agregado resolver **vault-aware** (nombre de nota + alias de frontmatter). Validado en vault real: **852/852 reference edges resueltos, 0 colgantes**; `affected`/`path`/`explain` recorren el link-graph.
> - [x] Evaluar 2 vías de integración: (A) **fork** con extractor obsidian en `graphify/extractors/` (upstreameable), (B) **standalone** que emite schema + `merge-graphs` (bajo riesgo). Empezar por B #owner/me #type/research #area/personal — **decidido A (fork)** por pedido del owner: modificación en `graphify/extract.py` (rama `feat/obsidian-vault-wikilinks`, commit 9c393b7), gated por `GRAPHIFY_MD_VAULT_ROOT` (sin override = idéntico a upstream). **Compilado como build aislado `graphify-obsidian`** (venv uv propio en `~/.local/share/graphify-obsidian/venv`); `graphify` (Work) y `graphify-personal` siguen en PyPI 0.8.39 intactos.
> - [ ] PoC **wrapper/capa delgada** sobre índice + link-graph → contexto mínimo con tope de tokens #owner/me #type/dev #area/personal — el wrapper `graphify-obsidian` ya produce el link-graph real; falta la capa de contexto-mínimo con tope de tokens encima.
> - [x] **Skill de retrieval**: encodear el protocolo de 4 capas + el [[context-router]] (extender `agents-os-context-retrieval` + `_shared/graphify-contract.md`) #owner/me #type/dev #area/personal
> - [x] **Context Router**: refinar el concepto [[context-router]] con el equipo (routing table, context pack) y volverlo material de evangelización #owner/me #type/research #area/personal — doc ya es material de evangelización (routing table, context-pack, valor para el equipo). Falta solo la sesión con el equipo.
> - [x] **Corregir el token budget del [[context-router]]**: el "≤1500" era ilustrativo y ES un error de diseño. Reemplazar por **suficiencia-first + techos blandos por tier (fact<relation<synthesis) + progressive disclosure**; el número es smell-test, no guillotina #owner/me #type/dev #area/personal
> - [/] **Auditoría de consistencia AGENTS OS** (doc ↔ artefactos): garantizar que lo que se DEFINE a los agentes es lo que se IMPLEMENTA; que no existan 2 approaches para la misma abstracción; que ninguna regla se contradiga entre constitución, agents-os.md, skills y docs. Integrar como chequeo recurrente del proceso de higienización #owner/me #type/research #area/personal — 1ª pasada 2026-07-04: 4 gaps DEFINE≠IMPLEMENTA corregidos (router en skill, budget blando, wikilinks en graphify-contract, grep/graphify/semántica en ADR) + 5º gap (2 recetas de retrieval; 2 catálogos en tools/). **Ya integrada como chequeo recurrente en `agents-os-hygiene-review`.**
> - [x] **Adelgazar `agents-os.md`** a mapa+conceptos (mover procedimiento duplicado con `bootstrap` a las skills). SOLO diseño+diff primero; NO editar el archivo vivo sin aprobación (alta autoridad, carga en cada arranque) #owner/me #type/dev #area/personal — **APLICADO 2026-07-04 con aprobación del owner: sección Retrieval → puntero único al router (concepto + skill + contrato); eliminada la receta `--budget 1200` que competía con la skill. Log: `journal/logs/2026-07-04-agents-os-md-retrieval-slimmed.md`.**
> - [x] **Actualizar el proceso de higienización** (`agents-os-hygiene-review`): frescura de índice, cobertura de links curados, huérfanos, compliance de tags, escalado de índice #owner/me #type/dev #area/personal — + auditoría de consistencia DEFINE≠IMPLEMENTA como chequeo recurrente.
> - [x] Generalizar patrón wiki (`00-index.md` + `log.md`) a `tools/` y demás dominios de resources #owner/me #type/dev #area/personal — `tools/` alineado (00-index.md + log.md; README demovido a convenciones). Falta replicar a `runbooks/`, `ideas/`, `meetings/` si se justifica.
> - [ ] Medir ahorro real (`graphify benchmark` + conteo de tokens por query) #owner/me #type/research #area/personal
> - [x] **Compactar ~8 learnings de AGENTS OS** con `## Evidencia` inflada (`memory/public/learning/agents-os/`): pasada per-file con juicio (link+1 línea), NO reescribir en masa. Causa raíz ya corregida en el template `learning.md` #owner/me #type/dev #area/personal — **2026-07-04: 7 learnings compactados (los 2 sin `## Evidencia` quedaron fuera). Evidencia real preservada (SHA, versión SDK, clases, citas del owner, logs). Log: `journal/logs/2026-07-04-token-economy-two-hygiene-passes.md`.**
> - [x] **Reclasificar `hermes-dashboard-recovery`**: es un runbook vestido de skill + copia-espejo de una skill viva externa. Decidir si se mueve a runbook o se deja como puente documentado #owner/me #type/research #area/personal — **2026-07-04: decisión del owner = puente delgado. Skill eliminada de `80-agents/skills/`; creado puente `type: index` en `memory/public/reference/hermes-dashboard-recovery.md` que enruta al skill vivo externo + runbook canónico `[[dashboard-hermes-agent]]`, sin duplicar procedimiento.**

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`);}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const all=dv.current().file.tasks.array();
board(all.filter(t=>has(t,"owner/me")));
```

## 📆 Bitácora

- **2026-07-14** — El owner solicitó una nueva iteración del Grid; la tarea
  puente vuelve de Review a WIP mientras se prepara y verifica la versión 2
  local. La publicación remota no forma parte automática de esta iteración.
- **2026-07-10** — Creado el subproyecto de agente [[AGENTS OS - Evaluación y Adopción]] y su tarea puente. El Grid crítico y el mapa de componentes quedan agrupados bajo esta iniciativa para revisión del owner.
- **2026-07-14** — [[AGENTS OS - Evaluación y Adopción]] entregó Grid v2 publicado y verificado; la tarea puente vuelve a Review para aceptación humana.
- **2026-07-14** — El subproyecto completó todas sus tareas y publicó la versión 1 en Grid privado. La tarea puente queda en Review para aceptación humana.
- **2026-07-03** — Proyecto creado. ADR + piloto listos. Hallazgo: graphify no captura wikilinks → builder propio. Idea de experimentos parqueada.
- **2026-07-03** — Evaluado repo completo `/Users/rjara/fuentes/graphify`. Corrido sobre sí mismo (10.316 nodos). Confirmado: fuerte en código, sin extractor estructural de markdown; schema enchufable (`merge-graphs`, MCP, benchmark). Camino del builder: emitir schema de graphify, no reemplazarlo.
- **2026-07-03** — Cierre de sesión: Context Router documentado; principio "una fuente por hecho" en constitución; skill de autoría creada. Backlog ampliado (fix token budget, auditoría de consistencia, adelgazar agents-os.md — todo diseño, sin tocar el sistema vivo). Known-error de Graphify destilado. Graphify reindexado (3298 nodos). **Fase de diseño lista; PoC pendiente (otra IA).**
- **2026-07-04** — **Implementación de consistencia (DEFINE≠IMPLEMENTA).** El Context Router pasó de documento a **implementado** en la skill `agents-os-context-retrieval` (4 capas, tabla intención→ruta, context-pack, caveat Capa 2, budget por suficiencia). Corregido el token budget del `context-router` (techo blando por tier, no guillotina). `graphify-contract` actualizado: `.graphifyignore` real + limitación de wikilinks. ADR: formalizado grep/graphify/semántica. `agents-os.md` vivo intacto (guard). Log: `journal/logs/2026-07-04-context-router-implemented-consistency.md`.
- **2026-07-04 (fase doc)** — **Barrido de caps + resto de documentación.** Semántica de budget definida UNA vez en `graphify-contract` ("Budget semantics": techo blando, escala on-miss, nunca guillotina) → todo `--budget N` disperso hereda eso; purgados los caps de `bootstrap` y wording de retrieval. Añadidos: política de **escalado del índice** (plano→jerárquico) en `00-RESOURCE-WIKI`, diseño de **relaciones graphifeables** (links tipados) en el ADR, **chequeos nuevos + auditoría de consistencia recurrente** en `agents-os-hygiene-review`, y patrón wiki generalizado a **`tools/`** (00-index.md + log.md; README→convenciones). Diff de `agents-os.md` propuesto (espera aprobación). Log: `journal/logs/2026-07-04-doc-phase-token-economy.md`. **Pendiente: aplicar diff agents-os.md (aprobación) + PoCs de código (otro agente, contexto limpio).**
- **2026-07-04 (cierre + audit + reglas)** — Aplicado con aprobación: `agents-os.md` §Retrieval y §Cierre → punteros (un solo método canónico). **Kaizen** (67 feedbacks, 1er reporte) + **higiene**; known-error de Graphify ampliado (pitfall CLI/`graph.json`). Reglas nuevas en constitución: **memorias compactas** + **memoria interna = canal obligatorio entre agentes con opt-out del owner**. Formalizado **cierre táctico**. **Auditoría amplia del Sistema 1**: deduplicado Cierre de Sesión (constitución vs agents-os.md), template `learning.md` (Evidencia=cita), frontmatter de skills, lenguaje de cap del ADR. `agents-os-hygiene-review` reconvertida en **validar+regularizar TODO el Sistema 1** (`full-system-1`, delegación a subagente, checks completos). Logs `journal/logs/2026-07-04-*`. **Solo queda código + 2 pendientes menores (compactar 8 learnings, reclasificar hermes-skill).**
- **2026-07-04 (higiene final)** — Cerrados los 2 pendientes menores. **7 learnings de agents-os** con `## Evidencia` inflada compactados a cita (link + prueba concreta), preservando evidencia real; los 2 sin sección quedaron fuera. **`hermes-dashboard-recovery` reclasificado** (decisión del owner: puente delgado): skill eliminada del namespace, reemplazada por puente `type: index` en `memory/public/reference/` que apunta al skill vivo externo + runbook canónico, sin duplicar procedimiento. Log: `journal/logs/2026-07-04-token-economy-two-hygiene-passes.md`. **Ya no quedan pendientes de doc/higiene — solo los PoCs de código (otro agente, contexto limpio).**
- **2026-07-04 (PoC de código: wikilinks)** — **Primer PoC de código ejecutado.** Vía A (fork de graphify), no builder standalone. Diagnóstico afinado: el `extract_markdown` de graphify (PR #1376) **sí** parsea `[[wikilinks]]` pero los resolvía solo relativos al dir de la nota → en un vault (links por nombre/alias cross-folder) quedaban colgantes. Fix: resolver **vault-aware** (índice stem+alias de frontmatter, cache por raíz) en `graphify/extract.py`, gated por `GRAPHIFY_MD_VAULT_ROOT` (sin override = idéntico a upstream; 68 tests markdown verdes). Compilado como **build aislado `graphify-obsidian`** (venv uv propio); `graphify`/`graphify-personal` intactos en PyPI 0.8.39. Wrapper `~/bin/graphify-obsidian` actualizado (apunta al build aislado, exporta la raíz del vault, excluye `graphify-out/` para forzar extracción fresca sin caché stale). **Validado en vault real (576 notas): 852/852 reference edges resueltos, 0 colgantes; backlinks de hubs (java-polycard-sdk 9, search-middleware 14); criterios de aceptación 1-4 OK.** Caveat conocido (corregido 2026-07-04): la query correcta de backlinks es `graphify-obsidian affected "<nota>.md" --relation references` (con `.md` **y** la relación explícita; `references` no está en las relaciones por defecto de `affected`). `affected "<nombre-pelado>"` (sin `.md`) cae en el heading `# nombre` cuando H1==filename → vacío. ⚠️ Lo que esta entrada decía originalmente —"consultar por file-node id devuelve los backlinks"— es **INCORRECTO** (da vacío); no repetir. Rama `feat/obsidian-vault-wikilinks` commit 9c393b7. Log: `journal/logs/2026-07-04-graphify-obsidian-wikilinks.md`. **Falta: capa de contexto-mínimo (tope de tokens) sobre el link-graph + `graphify benchmark`.**

- **2026-07-05 (review + reconciliación final)** — Revisada la implementación: el **builder (fork vault-aware `graphify-obsidian` 0.9.5) funciona en vivo** — 853 edges `references`, 0 colgantes, `affected --relation references` recorre backlinks reales. Sin correcciones de código. Barrido de consistencia doc↔realidad: todo ya reconciliado por sesiones previas salvo **1 línea stale** en `context-router.md` (corregida). **Pendiente: solo el wrapper de contexto-mínimo + `graphify benchmark`.** Log: `journal/logs/2026-07-05-implementation-review-and-final-reconciliation.md`.
- **2026-07-07 (links tipados: review + fix)** — El owner implementó **links tipados en el cuerpo** (ADR § Relaciones graphifeables). Review detectó 3 defectos, corregidos con su ok: (1) faltaba **scoping a `## Relaciones`** → prosa/negaciones ("no depende de [[X]]") forjaban edges falsos; (2) **fragmentación** por formas bare `depende`/`reemplaza`; (3) nit `end`. Ahora tipa solo dentro de `## Relaciones` con verbos canónicos (`consume`, `decora`, `depende de`, `expone`, `reemplaza a`; espacio→`_`); el resto cae a `references`. Nuevo `tests/test_obsidian_typed_links.py` 6/6 + regresión 56/56; venv + wheel portátil regenerados; `graphify-obsidian update` limpio (0 edges tipados espurios, aún sin contenido `## Relaciones`). ADR marcado **implementado** (fuente canónica); `graphify.md` enlaza al ADR sin duplicar. **Falta: commitear el fork.** Log: `journal/logs/2026-07-07-typed-links-review-corrections.md`.

## 🧭 Decisiones

- Arquitectura de 4 capas: ver [[token-economy-indexing-architecture]].
- Operar con índices, no con semántica LLM (free tier Gemini insuficiente; semántica solo para código vía API).
- ~~**graphify AST NO captura `[[wikilinks]]` de Obsidian**~~ (verificado 2026-07-03) → **SUPERADO 2026-07-04.** El hallazgo era parcial: graphify **sí** tiene `extract_markdown` con soporte de wikilinks (PR #1376), pero resolvía `[[X]]` solo a hermanos de la misma carpeta → en un vault (links cross-folder por nombre/alias) los edges quedaban colgantes. **Resuelto con fork vault-aware** (rama `feat/obsidian-vault-wikilinks`), compilado como `graphify-obsidian`. graphify ya construye el grafo de relaciones del vault; no hace falta builder standalone.

## 🔗 Docs / Links

- [[token-economy-indexing-architecture]] — ADR de arquitectura.
- [[context-router]] — concepto "cómo cargar contexto" (material de evangelización).
- [[30-resources/00-RESOURCE-WIKI|Resource Wiki]] — esquema/reglas de la wiki.
- [[graphify]] · [[LLM Wiki]] · skill `agents-os-resource-wiki` · runbook `resource-wiki-lint-reindex`.
- Idea parqueada: `30-resources/ideas/2026-07-03-sistema-experimentos-feedback-retrieval.md`.

## 💡 Ideas

### Backlog de ideas
- Índice de relaciones (edge-list/MOC) generado por el builder, no a mano.
- `graphify benchmark` como métrica de ahorro de tokens.

### Motivos / principios
- Cero basura al contexto. Cada capa filtra antes de la más cara. Curar reduce la necesidad de semántica.
- **Suficiencia > presupuesto:** no cortar contexto por un número fijo; cargar barato→caro y parar al ser suficiente. El budget es techo blando por tier, no guillotina.
- **Consistencia como requisito duro:** definir A y hacer B es inconsistencia; 2 approaches para la misma abstracción es inconsistencia. La doc de AGENTS OS y sus artefactos deben decir y hacer lo mismo (ver principio de constitución "Una fuente canónica por hecho").
