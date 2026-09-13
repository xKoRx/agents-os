---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Personal]]"
parent: "[[Project Lens]]"
sprint:
start: 2026-09-13
due:
progress: 0
repo:
jira:
prs:
aliases:
  - Project Lens v0.1
  - Lens Foundation
  - PL-F01
tags:
  - kind/project
  - area/personal
  - agent/owner
created: "2026-09-13"
updated: "2026-09-13"
cssclasses:
  - wide
---

# Project Lens — Foundation v0.1

%% Naming: Project Lens — Foundation v0.1 es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Project Lens — Foundation v0.1
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Project Lens]] · **Repo:** pendiente decisión owner
> Subproyecto de **fundación y ejecución v0.1** de Project Lens. Esta nota es el planificador único de la implementación (HOW / ORDER / GATES); el contrato de producto vive en su interior congelado (§ Product definition, § Domain model, § API). El padre [[Project Lens]] conserva las decisiones del owner y la tarea puente. Sesión de fundación (2026-09-13) produjo este planner con CERO código de producto.

## 🎯 Objetivo

- Entregar **Project Lens v0.1**: viewer local read-only del vault real — binario Go único (127.0.0.1) con SPA Vue 3 embebida que recupera el valor diario perdido con el veto de Obsidian: leer notas con links resueltos, cockpit de proyectos con rollup, tableros de tareas con ciclo de 5 estados, backlinks y búsqueda.
- Todo el estado derivado (índice, proyecciones, HTML renderizado) es reconstruible desde el vault: delete-all-derived → rescan → producto idéntico. Markdown es la única autoridad.
- v0.1 es un **walking skeleton productivo**: cada slice recorre el sistema real end-to-end (vault real → scan/parse/index → API → UI) y todo el código está destinado a sobrevivir. No hay prototype/, temp/ ni throwaway/.

## 📊 Estado actual

- **F0 FOUNDATION COMPLETA (2026-09-13):** sesión de rebase/arquitectura produjo este planner — dominio, identidad, matriz canonical/derived, boundaries, storage (sin SQLite), decisión Graphify (sin dependencia), API v0.1, roadmap vertical F1–F5, work packages atómicos T01–T17, modelo de subagents y gates. Cero product code.
- **Bloqueo de arranque (owner):** WP-A (scaffold) requiere decisión del owner sobre nombre canónico del repo y workspace externo (`repo:` vacío). Ver `Blockers`.
- **Muestreo del vault real (2026-09-13, evidencia del diseño):** 2741 notas .md; S2 real pequeño (10-projects 110, 30-resources 261, 20-areas 12, 40-archive 69, 90-system 4); 80-agents 2234 (mayoritariamente journal excluido de retrieval). Wikilinks: mayoría plain, 218 con alias, 20 con heading, 13 embeds, 0 block refs. Tasks: 349 con `#owner/*` en 10-projects. Sin sistema de `id:`/`uid:` global (solo incidental en tickets/ADRs) → identidad path-based. Frontmatter con valores legacy/malformados (p. ej. `status: PENDING|RUNNING|…`) → tolerancia obligatoria. Bloques dinámicos: 36 archivos con dataviewjs, 32 con base, 39 con tasks plugin → el valor diario está en proyectos/tasks/backlinks, no en render genérico.
- **Graphify (2026-09-13):** binario `graphify-obsidian` NO instalado en esta máquina (fallback filesystem usado durante toda la sesión). Contrato inspeccionado ([[graphify-contract]]): wikilinks → edges `references`; allowlist de relaciones tipadas desde frontmatter (`in_area`, `child_of`, `in_project`, `for_application`, `about`, `related_to`, `supersedes`); tags = facets, nunca edges. Refuerza la decisión de NO depender de Graphify (§ Graphify).
- **Sesión de fundación:** NO implementó producto, NO creó repo, NO lanzó subagents de implementación. El arranque NORMAL espera gates de owner (ver `Blockers`).

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `xKoRx/project-lens` (repo **por crear** — decisión owner pendiente) | `master` (fase v0.1) | — (repo nuevo) | [[Project Lens — Foundation v0.1]] § Product definition + § API contract + § Roadmap | [[Project Lens — Foundation v0.1]] § Domain model + § Architecture + § Work packages | **BLOCKED — decisión owner nombre/repo/workspace** |

- Política: ninguna implementación arranca sin repo creado + branch/base registrados en esta tabla (regla dura de `agents-os-entity-lifecycle`). Al crear el repo, actualizar esta fila (commit base inicial) y mover SPEC funcional/técnica del vault al repo (`specs/…`) según patrón vigente, enlazando desde aquí.
- Mientras el repo no exista, esta nota del vault es la única fuente de planificación (permitido por la regla "la nota es el planificador"); los T-tasks atómicos viven aquí.

## Product definition (v0.1, congelado)

- Aplicación **personal, local-first, read-only** para visualizar y consultar el vault Markdown/Agents-OS en la pega (MELI vetó Obsidian).
- Un binario Go que escanea el vault, mantiene un índice derivado **en memoria** y sirve JSON en `127.0.0.1` + SPA Vue 3 embebida (`go:embed`).
- Cinco capabilities: **(1)** leer cualquier nota con render server-side, frontmatter, links resueltos y backlinks; **(2)** cockpit de proyectos (cards por área/owner/estado/prioridad, huérfanos); **(3)** detalle de proyecto (envelope, task board 5 estados, subproyectos); **(4)** índice global de tareas filtrable; **(5)** búsqueda + página de diagnósticos.
- NO es: clon de Obsidian, editor, runtime de plugins, SaaS, base de datos canonical, framework de extensión.

## V0.1 committed scope

- F1 walking skeleton: scan+parse+index del vault real → API meta/notes/render → SPA mínima renderizando una nota real con links y backlinks end-to-end.
- F2 cockpit de proyectos: `/projects` + `/project/{name}` con rollup por área/owner/estado/prioridad, detección de huérfanos, detail con task board (5 estados: todo/wip/review/done/canceled) y subproyectos.
- F3 índice global de tareas (filtros owner/state/area/type/project) + panel de backlinks + áreas.
- F4 búsqueda (títulos + substring de contenido en memoria) + página de diagnósticos.
- F5 hardening: watcher incremental (fsnotify, debounce; scan completo sigue siendo el baseline de correctness), endpoint de rebuild, aristas visibles (links ambiguos/rotos), empaquetado `make build` binario único.

## Non-goals v0.1 (congelados, con por qué)

- **Editing/escritura:** el producto es read-only absoluto; escribir introduce autoridad mutable y superficie de riesgo; edición lejana es future driver, no v0.1.
- **Compatibilidad Obsidian plugins / Dataview / Bases:** no ejecutamos JS arbitrario (es exactamente la superficie que motivó el veto); Lens replica server-side SOLO las proyecciones concretas usadas (task board, project cards, rollups), no un engine de queries.
- **Runtime de plugins:** no repetir la superficie vetada; extension seams documentados, no implementados.
- **CouchDB sync / multi-device replicas:** single user, un solo lector, sin segundo writer; no hay conflicto que sincronizar.
- **MCP / API para agentes:** retrieval de agentes ya lo cubre Graphify; sin evidencia de necesidad actual; conversión futura es un adapter, no un rediseño.
- **Embeddings / búsqueda semántica / vector DB:** ningún query pattern actual lo pide; FTS primero si acaso.
- **SQLite / FTS5:** evidencia material en contra — 2741 notas, queries v0.1 son rollups/lookups sobre snapshot completo; en memoria sobra (§ Storage).
- **Electron / Wails / desktop wrapper:** binario + browser localhost basta; Wails v3 sigue alpha; deferred.
- **Cloud / auth / multi-user / deployment:** bind 127.0.0.1, personal, sin superficie remota.
- **Contenido remoto externo:** CSP estricta, cero fetch externo (seguridad local).

## Domain model (congelado)

Clasificación: **ENTITY** (identidad propia durable) · **VO** (value object, sin identidad) · **PROJECTION** (typed view cuya identidad ES la identidad de una Note) · **INDEX RECORD** (derivado con clave compuesta) · **INFRA** (concern de infraestructura).

- **Vault** — aggregate root; identidad = root path (config runtime, no persistida); dueño de la autoridad.
- **Note** — ENTITY. **Identidad (DocumentID) = path vault-relativo POSIX normalizado NFC, case-preserved.** Routing identity = TitleName (filename sin `.md`) + `aliases` de frontmatter. Evidencia: no existe sistema de `id:` global; Obsidian y Graphify resuelven por nombre/alias; el path es estable y único. Ciclo de vida = existencia del archivo (create/modify/delete/rename); rename cambia DocumentID (aceptable: los links resuelven por TitleName, no por path).
- **Frontmatter** — VO. Map YAML + proyección tipada del envelope (type, status, owner, root, parent, area, project, priority, progress, tags, aliases, entities, related, application, repo, slug). Campos desconocidos se preservan raw. Malformado → nota carga con body raw + diagnóstico; nunca se descarta.
- **Body** — VO. Bytes raw preservados + estructuras extraídas: headings, tasks, links, tags inline, callouts, bloques de código (incluye bloques dinámicos ` ```dataviewjs/base/tasks ` marcados como RAW).
- **Link** — VO. {source path, raw target, resolved target | unresolved, kind: wikilink|embed, anchor: heading|block|none, alias visual}. Clasificación de relación derivada de la ubicación: link en frontmatter allowlist → relación tipada (`in_area`, `child_of`, `in_project`, `for_application`, `about`, `related_to`, `supersedes`); link en body → `references`. Alineado con el modelo de Graphify sin acoplarse a él.
- **Task** — INDEX RECORD (derivado de Note, sin ciclo de vida propio). {note path, línea, state ∈ {todo, wip, review, done, canceled}, texto, tags, owner ∈ {me, agent, unassigned}, type (dev/admin/research/pr-review/supervision/…), flags (#blocked/#waiting/#urgent)}. Clave = (notePath, ocurrencia); rebuild regenera idéntico. El ciclo de 5 estados y los tags de owner/tipo son parte del modelo (evidencia: convenciones + 349 tasks con owner).
- **Tag** — VO. Nombre normalizado (lowercase, jerárquico `area/echo`); provenance: frontmatter | inline body | task. Tags son FACETS, nunca entidades ni edges (convergencia con Graphify).
- **Heading** — VO. Texto, nivel, línea, slug (targets de `[[nota#heading]]`).
- **Attachment** — VO. Asset no-.md referenciado por embed/link (evidencia: `90-system/attachments/`, 13 embeds). Identidad = path.
- **Projections** (PROJECTION, identidad = identidad de la Note origen):
  - **Project** = proyección tipada de Note (`type: project`): owner, root, parent, area, status, priority, progress, repo + rollup de tasks (conteos por estado) + subproyectos (child_of). **Principio validado con evidencia: Project IS a typed projection of Note** — todo el estado de proyecto vive en frontmatter + body de la nota; no existe segundo store.
  - **Area** = proyección tipada de Note (`type: area`).
  - **TypedEntityCard** genérico para el resto de `type:` (resource, concept, technology, application, …): type + envelope + links. Project y Area son los únicos bespoke en v0.1 (evidencia: Panel de Proyectos).
- **Backlink** — INDEX RECORD derivado: inverso del mapa de links.
- **SearchIndex** — INFRA derivada en memoria: mapa de títulos/aliases + substring scan de contenido.
- **Diagnostic** — INDEX RECORD: errores de parse, links ambiguos, targets no resueltos, valores de enum desconocidos.

**Invariante de identidad:** ningún concepto del dominio introduce una identidad no derivable de los archivos. Esto elimina deliberadamente la capa `VaultID/EntityID/TaskID` propuesta en la idea de agosto (YAGNI; evidencia: no hay id system en el vault).

## Canonical vs derived (matriz congelada)

| Concepto | Clase | Autoridad | Reconstruible |
|---|---|---|---|
| Archivo .md | CANONICAL | vault | — |
| Asset (attachment) | CANONICAL | vault | — |
| Frontmatter parseado | DERIVED (contenido canónico) | archivo | sí |
| Body AST / headings / tasks | DERIVED | archivo | sí |
| Link resuelto | DERIVED | archivo + vault | sí |
| Backlink | DERIVED | índice | sí |
| Project/Area projection | DERIVED (typed view) | archivo | sí |
| Índice en memoria | DERIVED | vault | sí |
| Respuestas HTTP/JSON | DERIVED (efímero) | índice | sí |
| HTML renderizado | DERIVED (efímero) | índice | sí |
| UI state | EPHEMERAL | — | — |

**Invariante de reconstrucción:** borrar todo estado derivado → rescan del vault → estado semánticamente idéntico, verificado por test (§ Work packages, T09). v0.1 no persiste NINGÚN estado derivado (sin DB, sin cache files). El watcher futuro es optimización con scan completo como baseline de correctness.

## Architecture (boundaries congelados)

```text
cmd/lens            main: config, wiring, flags, embed
internal/vault      DOMINIO puro y genérico del Markdown: Note, Frontmatter, Link, Task (símbolos→5 estados), Tag, Heading, Diagnostic. Cero deps externas, cero IO, cero semántica Agents-OS (no conoce owner/parent/progress ni tipos de entidad).
internal/parse      ADAPTER determinístico: goldmark+YAML → tipos de internal/vault. Único touchpoint de EXTRACCIÓN hacia el dominio; extrae tags/tasks raw sin interpretar convenciones del vault.
internal/index      APPLICATION: scanner (walk fs), build snapshot, proyecciones tipadas (Project/Area = semántica Agents-OS: owner/root/parent/progress/rollups/child_of), interpretación de tags (owner/type → facets), query surface (GetNote, Projects, Tasks, Backlinks, Search), rebuild invariante. Único IO read-only del vault. Aquí vive TODO lo que sabe de Agents-OS.
internal/serve      TRANSPORT: HTTP JSON /api/v1, bind 127.0.0.1, render HTML (goldmark sólo como presentador), sin lógica de negocio.
internal/web        PRESENTATION: SPA Vue 3 compilada + go:embed; habla SOLO HTTP.
```

- **Dependency direction:** `serve → index → vault ← parse`; `web → (HTTP)`. 
- **Forbidden deps:** `vault` NO importa parse/serve/fsnotify/net/http ni SQLite y NO conoce semántica de entidades del vault (Projects/Áreas/owner son cosas de `index`); `parse` NO lee el filesystem (recibe bytes) y NO interpreta convenciones (extrae, no decide); `index` NO importa `serve`; `web` NO toca fs ni llama a nada que no sea `/api/v1`; `cmd` es el único que conoce todo y hace wiring. goldmark puede usarse en `parse` (extracción) y en `serve` (render de presentación) — el dominio nunca lo ve.
- **Reason for existence de cada módulo:** vault = modelo genérico del Markdown + invariantes (lo que sobrevive a todo cambio de stack y de semántica del vault); parse = aislar goldmark/YAML (reemplazable sin tocar dominio); index = ownership del snapshot, de TODA query y de TODA la semántica Agents-OS (el único lugar que sabe qué es un Project; el seam futuro de storage vive aquí como package boundary, no como interface); serve = contrato HTTP estable para la SPA; web = única capa que muere y se rehace sin tocar backend.
- **Seams NO introducidos (YAGNI):** sin `SearchProvider`/`GraphProvider`/`SyncProvider` interfaces, sin factories, sin event bus, sin interface-per-class. Puntos de extensión futuros documentados: storage persistente = implementar la misma query surface detrás de `serve` (package boundary); MCP = adapter nuevo junto a `serve`; render/parse alternativo = reemplazar `internal/parse`. Interfaces sólo cuando exista volatilidad real — hoy no existe.

## Storage decision (congelada)

- **NO SQLite en v0.1.** Evidencia: 2741 notas (escaneo completo < 1s), queries v0.1 son rollups/lookups/filtros sobre snapshot completo en memoria, backlinks = mapa inverso trivial, rebuild = rescan. SQLite añadiría schema + driver + migraciones + cache files para cero valor actual.
- Criterios de re-apertura (disparadores futuros, no hoy): FTS5 para búsqueda ranking; volumen de notas ×10; queries de agentes sobre proyecciones persistentes; sync incremental entre procesos.
- Si se adopta: SIEMPRE derivada, nunca source of truth, con el mismo test de invariancia rebuild==incremental.

## Graphify decision (congelada)

- **Lens v0.1 NO integra Graphify y NO lo requiere.** Graphify es índice derivado orientado a agentes (CLI, cache machine-local); el binario ni siquiera está instalado en esta máquina (verificado 2026-09-13). Lens computa localmente las derivaciones que necesita (wikilinks→edges, frontmatter→relaciones tipadas, backlinks) en memoria en < 1s.
- **Alineación semántica sin acoplamiento:** el modelo de relaciones de Lens usa el mismo allowlist que Graphify (relaciones tipadas desde frontmatter; body links = `references`; tags = facets) para que una futura convergencia (MCP/agentes) no exija migración semántica.
- **Graceful degradation:** trivial — Graphify no es dependencia, luego no es SPOF. Sin duplicación material: las derivaciones duplicadas son ~40 líneas de resolución de links que Lens necesita de todos modos para su propia UI.

## API contract v0.1 (congelado; JSON, read-only, sin auth — loopback only)

- `GET /api/v1/meta` — vault root (relativo), counts (notas/projects/tasks/diagnostics), build info, last scan timestamp.
- `GET /api/v1/projects?status=&area=&owner=&include=archived` — cards de proyectos: name, path, envelope (owner/root/parent/area/status/priority/progress), rollup de tasks, has-children.
- `GET /api/v1/projects/{name}` — detail: envelope completo, tasks agrupadas por estado, subproyectos, parent, links de la nota.
- `GET /api/v1/areas` — áreas con conteos de proyectos/notas.
- `GET /api/v1/tasks?owner=&state=&area=&type=&project=` — índice global de tareas con note origen y línea.
- `GET /api/v1/notes/{path...}` — detail: envelope, tasks, links (raw + resolved + unresolved), attachments, backlinks, headings.
- `GET /api/v1/notes/{path...}/render` — HTML server-side (goldmark) con wikilinks → hrefs internos `/app/note/...`, callouts renderizados, bloques dinámicos como `<pre class="lens-raw-block">`.
- `GET /api/v1/search?q=&scope=titles|content&limit=` — matches con snippet y score simple.
- `GET /api/v1/diagnostics` — resumen de errores de parse, links ambiguos/rotos, valores desconocidos, por-nota.
- Errores: JSON `{error, code}` (`NOT_FOUND`, `BAD_QUERY`, `VAULT_UNAVAILABLE`); 404 para nota inexistente; nunca 500 por una nota individual malformada (va a diagnostics).
- Compatibilidad frontend/backend: el contrato vive en esta sección; cambios posteriores = versión `/api/v2`, no mutación silenciosa.

## Frontend (congelado)

- Vue 3 + Vite + TypeScript strict. **Sin React, sin Electron, sin dependency zoo.**
- vue-router: `/` (Home cockpit), `/project/:name`, `/note/*` (viewer), `/search`, `/diagnostics`.
- Estado: composables module-scope + `fetch`; **sin Pinia en v0.1** (estado compartido mínimo: meta + cache de project list; si crece, se evalúa entonces).
- Render Markdown: server-side (goldmark, § API); la SPA inserta HTML sanitizado, intercepta links internos y resalta el heading ancla. Sin parser markdown en el cliente.
- Graph visualization: **deferred a F6** (los datos de links ya existen desde F1; nada se bloquea). Candidatos a evaluar entonces: canvas propio ligero vs librería force-graph; decisión en su momento.
- UI: CSS propio mínimo, dark-first, sin UI kit pesado. Task board y cards replican la semántica de los tableros actuales (badges por estado, colores por owner).

## Error / consistency model (congelado)

- **Frontmatter malformado o incompleto:** nota sirve con body raw, sin proyección (no aparece en boards), diagnostic registrada. Nunca crash, nunca se oculta.
- **Wikilink roto:** link renderizado como unresolved (estilo distinto), contado en diagnostics.
- **Target ambiguo (nombres duplicados):** resolver shortest path (comportamiento Obsidian) y flag de ambigüedad en diagnostics.
- **Nota cambia/desaparece durante indexación:** consistencia por snapshot — el index construye desde un walk atómico y sirve el snapshot anterior hasta el swap; el watcher hace debounce y re-scan incremental post-swap.
- **Vault inaccesible al arranque:** el proceso falla con error claro (sin vault no hay producto). Vault inaccesible en runtime (unmount temporal): mantener último snapshot + health flag en `/meta` + retry en próximo trigger; degradación visible, no muerte silenciosa.
- **Valores de enum desconocidos (status/owner/type legacy):** preservados raw, sin proyección parcial inventada, diagnostic.
- **Identidad duplicada:** dos notas mismo nombre = ambigüedad documentada (ver arriba); nunca merge silencioso.
- **Principio:** partial availability + diagnostics sobre whole-app death; corrupción factual siempre visible.

## Test strategy (congelada)

- **Unit:** funciones puras del dominio (parse de task line, link, envelope projection, normalización de paths NFC).
- **Parser fixtures:** corpus real sanitizado en `internal/parse/testdata/` — subset representativo del vault real: project con dataviewjs, area, resource con callouts, skill, agent_memory con `memory_state: superseded`, nota legacy malformada, nota con embeds + heading links. Golden structures, no snapshots frágiles.
- **Index tests:** invariancia de rebuild (rescan ×2 == snapshot idéntico, hash de estructuras); conteos de proyecciones contra fixture vault; resolución shortest-path y ambigüedades.
- **API tests:** `httptest` sobre index con fixture vault; contrato JSON exacto por endpoint.
- **Frontend:** tests de componente SOLO para task board y helpers de routing de links (Vitest); el resto e2e manual.
- **E2E walking skeleton:** script manual verificable contra el vault real (las 5 capabilities, incluida una nota con frontmatter malformado y un link ambiguo).
- Sin mocking excesivo: parser+index reales sobre fixtures. Coverage: caminos críticos primero (parse tolerante, snapshot swap, resolución de links), piso ≥ 95% en `internal/vault` + `internal/index` (regla del owner). No se escribe test de ramas inalcanzables: se borran.

## Roadmap (vertical slices, cada F = capability verificable end-to-end)

- **F1 Walking skeleton:** repo scaffold + `internal/{vault,parse,index}` mínimos + API `meta/notes/render` + SPA que renderiza una nota real del vault con links resueltos y backlinks. Gate: binario único corre contra el vault real y muestra la nota.
- **F2 Projects cockpit:** API projects/areas + vistas Home y Project con rollup, huérfanos, task board. Gate: replicar el Panel de Proyectos + el board de un proyecto real con los mismos datos.
- **F3 Tasks + backlinks + áreas:** índice global de tareas filtrable + panel de backlinks en el viewer. Gate: el filtro `#owner/me #type/supervision` del Panel de Proyectos reproducible desde la API.
- **F4 Search + diagnostics:** búsqueda títulos+contenido + página de diagnósticos con conteos reales del vault. Gate: encontrar una nota por substring de contenido y ver sus diagnósticos.
- **F5 Hardening:** watcher fsnotify con debounce + rebuild endpoint + empaquetado `make build` + performance del scan medido. Gate: editar una nota del vault real y ver el cambio reflejado sin reiniciar.
- **Post-v0.1 (deferred):** F6 graph view · F7 SQLite/FTS si los disparadores del § Storage ocurren · F8 MCP adapter read-only · F9 export snapshot estático (plan B política) · F10 desktop wrapper · F11 limited editing (CQRS chico sobre Markdown, lejano) · F12 CouchDB sync · F13 rich Graphify interop.

## Subagent execution model (congelado)

Cuatro roles, no más. Sin escritura concurrente sobre el mismo package; ownership por package es la frontera.

- **R1 core-go** — scope: `internal/{vault,parse,index}` + fixtures. Read: esta nota + vault real + docs Go. Write: SOLO esos packages y sus tests. Ownership del dominio, parser e índice (T03–T09). Deps: ninguna (primero). Reasoning: high (decisiones de borde de parse/tolerancia).
- **R2 api-go** — scope: `internal/serve` + wiring en `cmd/lens`. Read: § API contract + surface de `internal/index`. Write: SOLO serve/cmd. Deps: R1 (surface de index). Reasoning: normal.
- **R3 frontend** — scope: `internal/web/**` (Vue) + glue de build embed. Read: § API contract + § Frontend + vault real por browser. Write: SOLO web + su build. Deps: contrato API congelado (R2 en paralelo). Reasoning: normal.
- **R4 integrator-verifier** — scope: Makefile, e2e script, gates finales, revisión de allowed-scope y de la invariancia rebuild. Read: todo. Write: SOLO cmd/Makefile/scripts de verificación + reporte. Deps: R1+R2+R3. Reasoning: high.

- Cadencia: WP-A → R1 (WP-B, WP-C) → R2 (WP-D) ∥ R3 (WP-E, arranca tras freeze del contrato) → R4 (WP-F). `TOP` (esta nota + decisiones) es editado por el orchestrator/sesión de fundación; `NORMAL` (R1–R3) implementa tasks mecánicamente sin rediseñar contratos; desviación → volver a esta nota, no fork mental.

## Long-run orchestration contract (congelado)

- **Única fuente de planificación:** esta nota (§ Work packages + `## ✅ Tareas` + `## 📆 Bitácora` + `progress:`). Ningún plan paralelo en chat ni scratch durable.
- **Ciclo del orchestrator:** LOAD esta nota → SELECT próxima task con deps `[x]` → DISPATCH rol correspondiente con su task + allowed files + AC → VERIFY contra AC + gates → UPDATE tasks/estado/bitácora en esta nota → NEXT. Crash/restart/new session = re-leer esta nota y continuar; la nota basta para retomar sin preguntar al owner.
- **Handoff de sesión:** al pausar, `## 📆 Bitácora` registra qué task quedó en qué estado y qué evidencia existe; `progress:` refleja el porcentaje real de tasks `[x]` sobre T01–T17.

## Work packages y atomic tasks

Formato de task: objetivo · allowed files · AC · tests · deps · non-goals. Los T-tasks viven aquí (el repo no existe aún); al crearse el repo, WP-A traslada TASKS a `specs/` según patrón vigente y esta tabla queda como work packages.

**WP-A Scaffold (T01–T02)** — bloqueado por decisión owner (repo/workspace).
- **T01 Go scaffold:** objetivo = módulo Go + `cmd/lens` (flag `--vault`, config) + Makefile `build/test/lint`. Allowed: `go.mod`, `cmd/lens/**`, `Makefile`, `README.md`. AC: `make build` produce binario que arranca con `--vault` apuntando al vault real y sirve 404 en `/api/v1/meta` (stub). Tests: smoke de arranque. Deps: repo creado. Non-goals: ningún handler real.
- **T02 Web scaffold:** objetivo = Vite + Vue 3 + TS + vue-router con rutas vacías + pipeline `make web` que compila a `internal/web/dist` y `go:embed` lo sirve en `/`. Allowed: `internal/web/**`, Makefile, `cmd/lens` (solo mount del embed). AC: browser en `127.0.0.1:<port>/` muestra el shell con routing. Tests: smoke de build. Deps: T01. Non-goals: vistas reales.

**WP-B Parse core (T03–T05)** — R1.
- **T05 fixtures primero:** objetivo = corpus sanitizado en `internal/parse/testdata/` (project con dataviewjs, area, resource con callouts, skill, agent_memory superseded, legacy malformada, embeds + heading links + alias links, nota con `#owner/*` tasks y estados 5). Allowed: `internal/parse/testdata/**`. AC: fixture vault reproduce los 8 casos de evidencia del muestreo. Deps: T01. Non-goals: parser.
- **T03 Frontmatter parser:** objetivo = YAML front matter → map + envelope tipado, tolerante (malformado → raw + diagnostic, sin panic). Allowed: `internal/parse/**`, `internal/vault/**`. AC: 100% del corpus parsea sin panic; malformada produce diagnostic y body raw; NFC normalización de paths. Tests: fixtures golden. Deps: T05. Non-goals: YAML completo con anchors/aliases exóticos (fail-closed tolerante).
- **T04 Body extraction:** objetivo = goldmark AST → headings, tasks (5 estados + tags owner/type/flags + 📅), wikilinks (plain/alias/heading/embed), inline tags, callouts detectados, bloques de código (dinámicos marcados RAW). Allowed: `internal/parse/**`. AC: todas las estructuras del corpus extraídas con línea correcta; block refs → ignorados sin error (0 en vault). Tests: fixtures. Deps: T05, T03. Non-goals: render HTML (va con T11 render), math/mermaid (raw).

**WP-C Index (T06–T09)** — R1.
- **T06 Scanner + snapshot:** objetivo = walk del vault (excluye `.obsidian`, `.git`), build de snapshot inmemoria inmutable, swap atómico. Allowed: `internal/index/**`. AC: escanea el vault real < 1s; snapshot inmutable; rescan determinístico. Tests: determinismo ×2. Deps: T03+T04.
- **T07 Projections + task index:** objetivo = Project/Area proyecciones (owner/root/parent/area/status/priority/progress/rollup/children) + índice global de tareas + typed relations desde frontmatter (allowlist Graphify) + facets de tags. Allowed: `internal/index/**`, `internal/vault/**`. AC: Panel de Proyectos reproducible: cards filtrables por type/owner/status/parent + huérfanos detectados en el vault real. Tests: conteos contra corpus + vault real smoke. Deps: T06.
- **T08 Link resolution + backlinks:** objetivo = resolver wikilinks por TitleName + aliases, shortest-path ante duplicados, ambigüedades flaggeadas, mapa inverso de backlinks. Allowed: `internal/index/**`. AC: 0 resolución incorrecta en corpus; ambigüedades y rotos van a diagnostics. Tests: fixtures + invariant. Deps: T06.
- **T09 Rebuild invariance test:** objetivo = test de la invariante central: delete-all-derived → rescan → snapshot idéntico (hash de estructuras completas). Allowed: `internal/index/**` (tests). AC: PASS sobre corpus y sobre vault real. Deps: T07+T08. Non-goals: incremental (watcher es F5).

**WP-D API (T10–T12)** — R2.
- **T10 meta/projects/areas:** objetivo = endpoints según § API contract sobre la surface de index. Allowed: `internal/serve/**`, `cmd/lens` wiring. AC: JSON exacto al contrato; filtros funcionan; bind 127.0.0.1. Tests: httptest con fixture vault. Deps: T07.
- **T11 notes/render/search/tasks:** objetivo = `notes/{path}`, `render` (goldmark HTML con wikilinks reescritos, callouts, bloques dinámicos raw), `tasks`, `search`. Allowed: `internal/serve/**` (+ goldmark aquí, no en parse: render es presentación de transporte). AC: una nota real del vault renderiza legible con links navegables; búsqueda por substring encuentra. Tests: httptest. Deps: T08+T10.
- **T12 diagnostics + error model:** objetivo = endpoint diagnostics + errores JSON `{error, code}` + health flag en meta. AC: nota malformada del vault real aparece en diagnostics y NO rompe ningún otro endpoint. Tests: httptest. Deps: T11.

**WP-E Frontend (T13–T16)** — R3, arranca tras freeze del contrato (ya congelado en esta nota).
- **T13 Shell + routing + fetch composable:** objetivo = SPA con rutas, layout dark, composables de fetch y error handling. AC: navega las 5 rutas contra API real. Deps: T02, T10.
- **T14 Note viewer:** objetivo = `/note/*` con HTML renderizado, envelope visible, backlinks panel, links internos interceptados. AC: leer una nota real con frontmatter, un dataviewjs visible como raw block, y volver por un wikilink. Deps: T11+T13.
- **T15 Projects cockpit + detail + task board:** objetivo = Home cards (por área/owner/estado/prioridad, huérfanos) + `/project/:name` con board 5 estados y subproyectos. AC: replicar visualmente el contenido real del Panel de Proyectos y el board del proyecto padre. Deps: T11+T13.
- **T16 Search + diagnostics pages:** objetivo = `/search` con resultados/snippets + `/diagnostics` con conteos y detalle. AC: flujo completo de búsqueda y diagnóstico sobre vault real. Deps: T12+T13.

**WP-F Gates (T17)** — R4.
- **T17 E2E + hardening final:** objetivo = script e2e manual (5 capabilities + caso malformado + link ambiguo), `go vet`+`gofmt`+`go test -race -cover` (piso 95% vault/index), build binario único verificado en máquina personal, README mínimo. AC: todos los gates PASS + bitácora con evidencia. Deps: T14+T15+T16.

**Dependency graph:**

```text
T01 → T02
T01 → T05 → T03 → T04
T03+T04 → T06 → T07
T06 → T08
T07+T08 → T09
T07 → T10 → T11 → T12        (T11 también depende de T08)
T02+T10 → T13 → T14 (T11) ∥ T15 (T11) → T16 (T12)
T14+T15+T16 → T17
```

## TOP / NORMAL boundaries

- **TOP:** esta nota (contratos, decisiones, allowed scope), el padre [[Project Lens]] (decisiones owner) y la creación del repo. NO source Go.
- **NORMAL:** R1–R3 implementan T-tasks mecánicamente contra el contrato congelado. No rediseñar FR/AC, no ampliar allowed files, no introducir dependencias no listadas, no "arreglar" el vault (read-only siempre).
- **GOD (decisiones que escalan al owner):** nombre/repo/workspace; cualquier cambio del contrato API o del domain model; cualquier feature fuera de § V0.1 committed scope.

## Blockers

- **B1 (owner, bloquea WP-A):** nombre canónico + repo + workspace externo. No inventarlo. Mientras tanto, WP-B/C/D/E no arrancan (sin repo no hay allowed files). Única alternativa permitida: arranque del owner explícito para trabajar en workspace local sin repo — NO asumido.
- No bloquear por: Graphify stale/ausente, frontmatter legacy del vault, o notas malformadas — todo eso es input válido del dominio con manejo definido.

## Acceptance gates (F0→ejecución)

- [x] Project Lens existente cargado.
- [x] Agents-OS actual inspeccionado (convenciones, schema contract, templates, patrón parent/agentes, Echo E-01 como referencia).
- [x] Muestra real del vault inspeccionada (tipos, links, tasks, lifecycle, attachmeents, identidad, bloques dinámicos).
- [x] Graphify inspeccionado (contrato + estado real: binario ausente en esta máquina).
- [x] Vue 3 congelado como frontend.
- [x] Domain entities definidas con clasificación ENTITY/VO/PROJECTION/INDEX RECORD/INFRA.
- [x] Identity model definido (path-based, evidencia).
- [x] Canonical vs derived definido (matriz + invariante de reconstrucción).
- [x] Boundaries definidos con forbidden deps.
- [x] Dependency direction definida.
- [x] v0.1 scope cerrado (5 capabilities, F1–F5).
- [x] Future drivers separados (F6–F13 explícitos).
- [x] CouchDB NO implementado · MCP NO implementado · Plugin runtime NO implementado · Semantic search NO implementado · SQLite NO implementado.
- [x] Architecture seams mínimas justificadas (package boundaries; cero interfaces especulativas).
- [x] Roadmap vertical definido.
- [x] Tasks atomizadas (T01–T17 con AC/deps/non-goals).
- [x] Acceptance gates por fase definidos.
- [x] Test strategy definida (fixtures reales, invariancia, piso 95% crítico-primero).
- [x] Subagent execution strategy definida (4 roles, ownership por package).
- [x] Long-run orchestration definida (nota = única fuente; ciclo LOAD→DISPATCH→VERIFY→UPDATE).
- [x] Adversarial architecture pass ejecutado (2026-09-13; correcciones aplicadas — ver Bitácora).
- [x] Project Lens Agents-OS actualizado (padre reestructurado + este planner + idea promovida).
- [x] Cero product code implementado.
- [ ] **OWNER:** política MELI validada (gate de riesgo, no técnico).
- [ ] **OWNER:** nombre/repo/workspace decidido → desbloquea WP-A.

## Risks

- **R1 Política corporativa MELI (owner):** que el veto a Obsidian extienda el veto a binarios propios. Mitigación: desarrollo y uso en máquina personal; F9 (export estático) es el plan B documentado; decisión owner ANTES de invertir horas.
- **R2 Unicode/encoding en paths:** áreas con acentos y `&` ("Economía de Tokens", "Casa & Energía"). Mitigación: NFC + case-preserved + tests desde T03.
- **R3 Frontmatter legacy/malformado:** evidenciado (valores `PENDING|RUNNING|…`, tipos no contractuales). Mitigación: tolerancia fail-open por nota + diagnostics desde T03.
- **R4 Dialecto Obsidian del Markdown:** callouts (`> [!info]`), embeds, comentarios `%% %%`, wikilinks a headings. Mitigación: corpus real como fixture desde T05; render subset declarado (lo no soportado queda raw legible).
- **R5 Scope creep hacia "knowledge runtime":** la idea de agosto propone SQLite day-1, MCP y Context Bundles. Mitigación: non-goals congelados con por qué; future drivers con disparadores de re-apertura explícitos.
- **R6 Repo sin crear:** toda la ejecución depende de B1; el planner del vault es válido pero SPEC/TASKS deben migrar al repo cuando exista (patrón vigente).

## Closure conditions (v0.1)

- T01–T17 `[x]`; gates de T17 PASS (test/race/cover ≥95% vault+index/vet/gofmt); invariancia rebuild PASS sobre vault real; e2e de las 5 capabilities con evidencia en bitácora; `## 🧱 Entrega de desarrollo` actualizada con repo/branch/base reales; entrega a Review (`[r]` en tarea puente del padre); cero código throwaway.

## 🧩 Subproyectos

_No aplica — este es el subproyecto de fundación/implementación de Project Lens; no crea más hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Ver [[convenciones]]. %%
> - [ ] WP-A Scaffold: T01 Go scaffold + T02 Web scaffold #owner/agent #type/dev #area/personal #blocked
> - [ ] WP-B Parse core: T05 fixtures → T03 frontmatter → T04 body #owner/agent #type/dev #area/personal
> - [ ] WP-C Index: T06 scanner → T07 projections → T08 links/backlinks → T09 rebuild invariance #owner/agent #type/dev #area/personal
> - [ ] WP-D API: T10 meta/projects/areas → T11 notes/render/search/tasks → T12 diagnostics #owner/agent #type/dev #area/personal
> - [ ] WP-E Frontend: T13 shell → T14 viewer ∥ T15 cockpit → T16 search/diagnostics #owner/agent #type/dev #area/personal
> - [ ] WP-F Gates: T17 e2e + hardening + build binario único #owner/agent #type/dev #area/personal

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

## 📆 Bitácora

- **2026-09-13 (F0 — sesión de fundación/rebase):** rebase completo del proyecto sobre el Agents-OS vigente: inspeccionado el proyecto de agosto, la convención parent/agentes (referencia Echo E-01), schema contract, convenciones, el vault real (muestreo: 2741 notas; sin id system → identidad path-based; 218 alias links / 20 heading / 13 embeds / 0 block refs; 349 tasks con owner; estados legacy malformados presentes) y Graphify (contrato + binario ausente en esta máquina). Decisión de dominio validada con evidencia: Project/Area = typed projections de Note; identidad = path + TitleName/aliases; 5 estados de task + owner tags en el modelo. Storage: sin SQLite (in-memory snapshot). Graphify: sin dependencia, semántica alineada. Escrito este planner: dominio, matriz canonical/derived, boundaries con forbidden deps, API v0.1, roadmap F1–F5 + deferred F6–F13, T01–T17 con AC, 4 roles de subagent, orchestration contract, gates, riesgos y DoD. Adversarial pass ejecutado con 5 correcciones aplicadas: (1) eliminada la capa VaultID/EntityID de la idea de agosto (duplicaba autoridad de identidad sin evidencia); (2) interfaces SearchProvider/GraphProvider retiradas del diseño por YAGNI (queda package boundary + puntos de extensión documentados); (3) goldmark render movido a `internal/serve` (es presentación de transporte, no extracción de dominio); (4) proyecciones Project/Area sacadas de `internal/vault` hacia `internal/index` — el core genérico no filtra semántica Agents-OS (owner/parent/progress viven sólo en index); (5) resuelta contradicción del "único touchpoint" de parsing: goldmark permitido en `parse` (extracción) y `serve` (render de presentación), nunca en el dominio. Bloqueo registrado: B1 decisión owner nombre/repo/workspace. Cero product code.

## 🧭 Decisiones (frozen ADRs con matriz CURRENT NEED? / EXPENSIVE TO CHANGE?)

- **ADR-L1 Markdown = única autoridad; todo derivado reconstruible (Y+Y).** Invariante verificada por test (T09). No hay estado irreconstruible en v0.1.
- **ADR-L2 Note identity = path vault-relativo NFC; routing = TitleName + aliases; sin id system (Y+Y).** Evidencia: no existe `id:`/`uid:` global en el vault (solo incidental en tickets/ADRs); Obsidian y Graphify resuelven por nombre/alias.
- **ADR-L3 Go binario único + SPA Vue 3 embebida `go:embed` + bind 127.0.0.1 (Y+Y).** Sin Electron/Wails en v0.1 (Wails v3 alpha; wrapper = future driver).
- **ADR-L4 Índice in-memory; NO SQLite v0.1 (Y+N → opción más simple).** 2741 notas; queries = rollups/lookups. Re-apertura solo por disparadores del § Storage.
- **ADR-L5 Project/Area = typed projections de Note; una sola fuente de verdad (Y+Y).** Validado con evidencia: todo el estado de proyecto vive en frontmatter+body.
- **ADR-L6 Render Markdown server-side (goldmark); SPA consume HTML sanitizado (Y+N → más simple).** Evita duplicar parser en cliente; bloques dinámicos = raw.
- **ADR-L7 Sin dependencia de Graphify; semántica de relaciones alineada a su allowlist (N+Y → seam mínimo).** Convergencia futura (MCP) sin acoplamiento ni SPOF; binario ausente en esta máquina lo confirma como decisión, no como accidente.
- **ADR-L8 Bloques dinámicos (dataviewjs/base/tasks) = código crudo + panels propios equivalentes donde existan (Y+N).** Lens replica las proyecciones concretamente usadas, no un engine de queries.
- **ADR-L9 Ciclo de task de 5 estados (todo/wip/review/done/canceled) + owner/type/flags como parte del modelo (Y+Y).** Evidencia: convenciones + 349 tasks con `#owner/*`.
- **ADR-L10 Modelo de seguridad local: read-only, loopback-only, path traversal prohibido, sin contenido remoto, CSP (Y+Y).** Es la razón de ser del producto tras el veto.

## 🔗 Docs / Links

- [[Project Lens]] — proyecto padre (owner decisions, tarea puente).
- [[2026-08-25-project-lens-knowledge-runtime]] — idea de agosto (insumo histórico; promovida; su SQLite-day-1/MCP quedan como future drivers F7/F8).
- Convenciones vigentes: [[convenciones]] · contrato de schema: `80-agents/skills/_shared/schema-contract.md` · Graphify: [[graphify-contract]].
- Referencia de patrón de ejecución: [[Echo — E-01 Canonical SDK Foundation S0]] (parent/agentes/SPEC/TASKS/gates).
- Refs técnicas: goldmark (parse/render), fsnotify (watcher F5), Vue 3 + Vite + vue-router. Sin más deps.

## 💡 Ideas

### Backlog de ideas

- MCP adapter read-only (`lens.search/get_document/list_projects/query_tasks/backlinks/build_context`) — F8, sólo con evidencia de necesidad de agentes.
- Graph view de entidades — F6; datos de links ya existen desde F1.
- Export snapshot estático (HTML navegable) — F9, plan B si la política MELI prohíbe binarios propios.
- CLI `lens index|serve|query` — se decide con el repo; `cmd/lens` ya es la semilla.

### Motivos / principios

- Una fuente por hecho: el vault es la autoridad; esta nota es el plan; el repo será el código.
- Small core, clear boundaries, few abstractions: boundaries de package reales, cero interface-per-class.
- Read-only primero: Lens nunca compite con el editor ni repite la superficie vetada.
