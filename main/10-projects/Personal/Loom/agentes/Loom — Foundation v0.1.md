---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Personal]]"
parent: "[[Loom]]"
sprint:
start: 2026-09-13
due:
progress: 0
repo: xKoRx/loom
jira:
prs:
aliases:
  - Loom v0.1
  - Loom Foundation
  - Project Lens — Foundation v0.1
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

# Loom — Foundation v0.1

%% Naming: Loom — Foundation v0.1 es el link canónico del proyecto; aliases guarda variantes humanas e históricas (Project Lens); tags/slugs son solo automatización. %%

> [!info]+ Loom — Foundation v0.1
> **Área:** [[Personal]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Loom]] · **Repo:** `xKoRx/loom` (declarado por owner; **existencia NO verificada**)
> Subproyecto de **fundación y ejecución v0.1** de Loom (renombrado desde Project Lens el 2026-09-13; alias histórico preservado). Esta nota es el planificador único de la implementación (HOW / ORDER / GATES); el contrato de producto vive en su interior congelado (§ Product definition, § Domain model, § API). El padre [[Loom]] conserva las decisiones del owner y la tarea puente. Sesión de fundación (2026-09-13) produjo este planner con CERO código de producto.

## 🎯 Objetivo

- Entregar **Loom v0.1**: viewer local read-only del vault real — binario Go único (127.0.0.1) con SPA Vue 3 embebida que recupera el valor diario perdido con el veto de Obsidian: leer notas con links resueltos, cockpit de proyectos con rollup, tableros de tareas con ciclo de 5 estados, backlinks y búsqueda — **reflejando cambios del vault sin reiniciar el proceso**.
- Todo el estado derivado (índice, proyecciones, HTML renderizado) es reconstruible desde el vault: delete-all-derived → rescan → producto idéntico. Markdown es la única autoridad.
- v0.1 es un **walking skeleton productivo**: cada slice recorre el sistema real end-to-end (vault real → scan/parse/index → API → UI) y todo el código está destinado a sobrevivir. No hay prototype/, temp/ ni throwaway/.

## 📊 Estado actual

- **FOUNDATION FINALIZATION (2026-09-13):** decisiones owner aplicadas — rename canónico **Project Lens → Loom** (aliases históricos preservados), repo `xKoRx/loom` + workspace `~/go/src/github.com/xKoRx/loom` + módulo `github.com/xKoRx/loom` + binario `loom` + branch `master` declarados (**repo NO verificado: no existe en GitHub ni en workspace — acción física del owner pendiente, sin SHA inventado**); live refresh promovido a comportamiento CORE de F1 (backend dueño exclusivo del fs: watch fsnotify → debounce → rebuild → snapshot inmutable → swap atómico → generation++; Vue observa generation por polling y refetch); **MAX_CONCURRENT_LOOM_SUBAGENTS = 1** (secuencia estricta, sin R2∥R3, sin delegación recursiva); invariante de seguridad HTTP DocumentID registrada.
- **F0 FOUNDATION COMPLETA (2026-09-13):** sesión de rebase/arquitectura produjo este planner — dominio, identidad, matriz canonical/derived, boundaries, storage (sin SQLite), decisión Graphify (sin dependencia), API v0.1, roadmap vertical F1–F5, work packages atómicos T01–T17, modelo de subagents y gates. Cero product code.
- **FOUNDATION REVIEW (2026-09-13):** arquitectura y roadmap **ACCEPTED** por el owner con 4 correcciones load-bearing aplicadas: (1) identity/API por path, (2) separación conceptual genérico↔Agents-OS dentro de `internal/index`, (3) scan best-effort + snapshot inmutable + swap atómico, (4) rationale MCP corregido. Stack Go+Vue 3, Markdown authority, in-memory index, Graphify/SQLite deferred, roadmap F1–F5, subagent model y package topology: **sin cambios**.
- **Muestreo del vault real (2026-09-13, evidencia del diseño):** 2741 notas .md; S2 real pequeño (10-projects 110, 30-resources 261, 20-areas 12, 40-archive 69, 90-system 4); 80-agents 2234 (mayoritariamente journal excluido de retrieval). Wikilinks: mayoría plain, 218 con alias, 20 con heading, 13 embeds, 0 block refs. Tasks: 349 con `#owner/*` en 10-projects. Sin sistema de `id:`/`uid:` global (solo incidental en tickets/ADRs) → identidad path-based. Frontmatter con valores legacy/malformados (p. ej. `status: PENDING|RUNNING|…`) → tolerancia obligatoria. Bloques dinámicos: 36 archivos con dataviewjs, 32 con base, 39 con tasks plugin → el valor diario está en proyectos/tasks/backlinks, no en render genérico.
- **Graphify (2026-09-13):** binario `graphify-obsidian` NO instalado en esta máquina (fallback filesystem usado durante toda la sesión). Contrato inspeccionado ([[graphify-contract]]): wikilinks → edges `references`; allowlist de relaciones tipadas desde frontmatter (`in_area`, `child_of`, `in_project`, `for_application`, `about`, `related_to`, `supersedes`); tags = facets, nunca edges. Refuerza la decisión de NO depender de Graphify (§ Graphify).
- **Sesiones de fundación/review/finalización:** NO implementaron producto, NO crearon repo, NO lanzaron subagents de implementación. El arranque NORMAL espera la acción física del owner sobre el repo (ver `Blockers`).

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `xKoRx/loom` (repo **declarado por owner; NO verificado/por crear**) | `master` (fase v0.1) | `—` (repo nuevo; **sin SHA — no se inventa**) | [[Loom — Foundation v0.1]] § Product definition + § API contract + § Roadmap | [[Loom — Foundation v0.1]] § Domain model + § Architecture + § Work packages | **OWNER ACTION PENDING — crear repo + workspace; luego registrar commit base real** |

- Política: ninguna implementación arranca sin repo creado + branch/base registrados en esta tabla (regla dura de `agents-os-entity-lifecycle`). Al existir el repo, actualizar esta fila con el commit base real y mover SPEC funcional/técnica del vault al repo (`specs/…`) según patrón vigente, enlazando desde aquí.
- Mientras el repo no exista, esta nota del vault es la única fuente de planificación (permitido por la regla "la nota es el planificador"); los T-tasks atómicos viven aquí.

## Product definition (v0.1, congelado)

- Aplicación **personal, local-first, read-only** para visualizar y consultar el vault Markdown/Agents-OS en la pega (MELI vetó Obsidian).
- Un binario Go (`loom`, módulo `github.com/xKoRx/loom`, workspace `~/go/src/github.com/xKoRx/loom`) que escanea el vault, mantiene un índice derivado **en memoria**, vigila el filesystem (fsnotify + debounce, reconstrucción automática) y sirve JSON en `127.0.0.1` + SPA Vue 3 embebida (`go:embed`).
- Cinco capabilities: **(1)** leer cualquier nota con render server-side, frontmatter, links resueltos y backlinks; **(2)** cockpit de proyectos (cards por área/owner/estado/prioridad, huérfanos); **(3)** detalle de proyecto (envelope, task board 5 estados, subproyectos); **(4)** índice global de tareas filtrable; **(5)** búsqueda + página de diagnósticos — **todo con live refresh sin reinicio de proceso**.
- NO es: clon de Obsidian, editor, runtime de plugins, SaaS, base de datos canonical, framework de extensión.

## V0.1 committed scope

- F1 walking skeleton + **live refresh mínimo**: scan+parse+index del vault real → watcher fsnotify con debounce → rebuild automático → snapshot inmutable → publicación/swap atómico → `generation++` expuesto en `/api/v1/meta` → SPA renderiza una nota real con links y backlinks y observa generation por polling HTTP, refetch de la vista actual al cambiar → **proof: modificar una nota real del vault se ve en Loom SIN reiniciar el proceso**.
- F2 cockpit de proyectos: `/projects` + `/project/*path` con rollup por área/owner/estado/prioridad, detección de huérfanos, detail con task board (5 estados: todo/wip/review/done/canceled) y subproyectos.
- F3 índice global de tareas (filtros owner/state/area/type/project) + panel de backlinks + áreas.
- F4 búsqueda (títulos + substring de contenido en memoria) + página de diagnósticos.
- F5 **hardening del live refresh** (NO su primera implementación): eventos burst/coalescidos, rename, delete, ráfagas de escritura, restart/recovery del watcher, vault temporalmente inaccesible, lecturas concurrentes durante rebuild, race tests, correctness de rebuild, performance medida, diagnósticos stale/health; más endpoint de rebuild, aristas visibles (links ambiguos/rotos) y empaquetado `make build` binario único.

## Non-goals v0.1 (congelados, con por qué)

- **Editing/escritura:** el producto es read-only absoluto; escribir introduce autoridad mutable y superficie de riesgo; edición lejana es future driver, no v0.1.
- **Compatibilidad Obsidian plugins / Dataview / Bases:** no ejecutamos JS arbitrario (es exactamente la superficie que motivó el veto); Loom replica server-side SOLO las proyecciones concretas usadas (task board, project cards, rollups), no un engine de queries.
- **Runtime de plugins:** no repetir la superficie vetada; extension seams documentados, no implementados.
- **CouchDB sync / multi-device replicas:** single user, un solo lector, sin segundo writer; no hay conflicto que sincronizar.
- **MCP / API para agentes:** v0.1 no tiene consumidor agent-facing (ningún agente consulta Loom hoy), luego deferred. **Reopen trigger: necesidad demostrada de query/retrieval programático sobre Loom.** Graphify NO sustituye esta API: es un índice derivado independiente para el retrieval de agentes, no la interface de consultas de Loom; la conversión futura es un adapter, no un rediseño.
- **WebSockets / SSE / event bus / push infra:** el polling ligero de `generation` en `/api/v1/meta` es el mecanismo suficiente y simple para v0.1; si evidencia futura muestra que es insuficiente, la decisión se reabre.
- **Acceso del frontend al filesystem:** `internal/web` no lee, no vigila, no enumera ni resuelve paths del vault; todo el fs es del backend (ver § Filesystem ownership).
- **Embeddings / búsqueda semántica / vector DB:** ningún query pattern actual lo pide; FTS primero si acaso.
- **SQLite / FTS5:** evidencia material en contra — 2741 notas, queries v0.1 son rollups/lookups sobre snapshot completo; en memoria sobra (§ Storage).
- **Electron / Wails / desktop wrapper:** binario + browser localhost basta; Wails v3 sigue alpha; deferred.
- **Cloud / auth / multi-user / deployment:** bind 127.0.0.1, personal, sin superficie remota.
- **Contenido remoto externo:** CSP estricta, cero fetch externo (seguridad local).

## Domain model (congelado)

Clasificación: **ENTITY** (identidad propia durable) · **VO** (value object, sin identidad) · **PROJECTION** (typed view cuya identidad ES la identidad de una Note) · **INDEX RECORD** (derivado con clave compuesta) · **INFRA** (concern de infraestructura).

- **Vault** — aggregate root; identidad = root path (config runtime, no persistida); dueño de la autoridad.
- **Note** — ENTITY. **Identidad (DocumentID) = path vault-relativo POSIX normalizado NFC, case-preserved.** Routing identity = TitleName (filename sin `.md`) + `aliases` de frontmatter. Evidencia: no existe sistema de `id:` global; Obsidian y Graphify resuelven por nombre/alias; el path es estable y único. Ciclo de vida = existencia del archivo (create/modify/delete/rename); rename cambia DocumentID (aceptable: los links resuelven por TitleName, no por path).
- **Frontmatter** — VO **genérico**: map YAML crudo con acceso tipado y campos desconocidos preservados raw; malformado → nota carga con body raw + diagnóstico, nunca se descarta. El **EntityEnvelope de Agents-OS** (type, status, owner, root, parent, area, project, priority, progress, repo, slug, …) NO vive aquí: es una proyección de `internal/index` sobre el map crudo.
- **Body** — VO. Bytes raw preservados + estructuras extraídas: headings, tasks, links, tags inline, callouts, bloques de código (incluye bloques dinámicos ` ```dataviewjs/base/tasks ` marcados como RAW).
- **Link** — VO. {source path, raw target, resolved target | unresolved, kind: wikilink|embed, anchor: heading|block|none, alias visual}. Clasificación de relación derivada de la ubicación: link en frontmatter allowlist → relación tipada (`in_area`, `child_of`, `in_project`, `for_application`, `about`, `related_to`, `supersedes`); link en body → `references`. Alineado con el modelo de Graphify sin acoplarse a él.
- **Task** — INDEX RECORD (derivado de Note, sin ciclo de vida propio). {note path, línea, state ∈ {todo, wip, review, done, canceled}, texto, tags, owner ∈ {me, agent, unassigned}, type (dev/admin/research/pr-review/supervision/…), flags (#blocked/#waiting/#urgent)}. Clave = (notePath, ocurrencia); rebuild regenera idéntico. Separación conceptual: la extracción genérica (parse→vault) produce líneas de task con símbolos y tags **raw**; la interpretación como campos filtrables (owner/type/state proyectados) es la **Task projection de Agents-OS** en `internal/index` (evidencia: convenciones + 349 tasks con owner).
- **Tag** — VO. Nombre normalizado (lowercase, jerárquico `area/echo`); provenance: frontmatter | inline body | task. Tags son FACETS, nunca entidades ni edges (convergencia con Graphify).
- **Heading** — VO. Texto, nivel, línea, slug (targets de `[[nota#heading]]`).
- **Attachment** — VO. Asset no-.md referenciado por embed/link (evidencia: `90-system/attachments/`, 13 embeds). Identidad = path.
- **Snapshot generation** — INFRA: contador monotónico que incrementa en CADA publicación/swap atómico de snapshot; es el único canal de change-detection para la UI.
- **Projections** (PROJECTION, identidad = identidad de la Note origen):
  - **Project** = proyección tipada de Note (`type: project`): owner, root, parent, area, status, priority, progress, repo + rollup de tasks (conteos por estado) + subproyectos (child_of). **Identidad: Project identity == source Note path (DocumentID)** — el TitleName/alias es sólo routing/search convenience y NUNCA clave autoritativa de API ni de UI. **Principio validado con evidencia: Project IS a typed projection of Note** — todo el estado de proyecto vive en frontmatter + body de la nota; no existe segundo store.
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

**Invariante de reconstrucción:** borrar todo estado derivado → rescan del vault → estado semánticamente idéntico, verificado por test (§ Work packages, T09). v0.1 no persiste NINGÚN estado derivado (sin DB, sin cache files). El watcher es parte del ciclo de publicación (scan completo como baseline de correctness; watch = trigger del rebuild, nunca fuente de verdad).

## Architecture (boundaries congelados)

```text
Módulo github.com/xKoRx/loom · binario loom · branch master · workspace ~/go/src/github.com/xKoRx/loom

cmd/loom            main: config, wiring, flags, embed
internal/vault      DOMINIO puro y genérico del Markdown: Note, Frontmatter, Link, Task (símbolos→5 estados), Tag, Heading, Diagnostic. Cero deps externas, cero IO, cero semántica Agents-OS (no conoce owner/parent/progress ni tipos de entidad).
internal/parse      ADAPTER determinístico: goldmark+YAML → tipos de internal/vault. Único touchpoint de EXTRACCIÓN hacia el dominio; extrae tags/tasks raw sin interpretar convenciones del vault.
internal/index      APPLICATION con DOS capas conceptuales (sin paquetes nuevos): (a) capa GENÉRICA: snapshot inmutable de estructuras raw de vault + scanner best-effort (walk fs) + watcher fsnotify con debounce + rebuild automático + query surface (GetNote, Notes, Backlinks, Search); (b) capa AGENTS-OS: EntityEnvelope proyectado del frontmatter crudo, Project/Area, Task projection (owner/type/state interpretados), typed relations, facets. ÚNICO dueño del filesystem del vault (scan/read/watch). Publicación: snapshot inmutable + swap atómico + generation++ en cada swap. Aquí vive TODO lo que sabe de Agents-OS.
internal/serve      TRANSPORT: HTTP JSON /api/v1, bind 127.0.0.1, render HTML (goldmark sólo como presentador), sin lógica de negocio.
internal/web        PRESENTATION: SPA Vue 3 compilada + go:embed; habla SOLO HTTP. NUNCA lee/vigila/enumera/resuelve el filesystem del vault; NUNCA conoce el vault root físico.
```

- **Dependency direction:** `serve → index → vault ← parse`; `web → (HTTP)`. 
- **Forbidden deps:** `vault` NO importa parse/serve/fsnotify/net/http ni SQLite y NO conoce semántica de entidades del vault (Projects/Áreas/owner son cosas de `index`); `parse` NO lee el filesystem (recibe bytes) y NO interpreta convenciones (extrae, no decide); `index` NO importa `serve` (fsnotify vive en `index`); `web` NO toca fs ni browser filesystem APIs ni conoce el vault root; llama SOLO a `/api/v1`; `cmd` es el único que conoce todo y hace wiring. goldmark puede usarse en `parse` (extracción) y en `serve` (render de presentación) — el dominio nunca lo ve.
- **Reason for existence de cada módulo:** vault = modelo genérico del Markdown + invariantes (lo que sobrevive a todo cambio de stack y de semántica del vault); parse = aislar goldmark/YAML (reemplazable sin tocar dominio); index = ownership EXCLUSIVO del filesystem, del snapshot, de TODA query y de TODA la semántica Agents-OS (el único lugar que sabe qué es un Project; el seam futuro de storage vive aquí como package boundary, no como interface); serve = contrato HTTP estable para la SPA; web = única capa que muere y se rehace sin tocar backend.
- **Seams NO introducidos (YAGNI):** sin `SearchProvider`/`GraphProvider`/`SyncProvider` interfaces, sin factories, sin event bus, sin interface-per-class. Puntos de extensión futuros documentados: storage persistente = implementar la misma query surface detrás de `serve` (package boundary); MCP = adapter nuevo junto a `serve`; render/parse alternativo = reemplazar `internal/parse`. Interfaces sólo cuando exista volatilidad real — hoy no existe.

## Filesystem ownership (invariante congelada)

- **BACKEND = dueño exclusivo del filesystem del vault:** scan/read, parse, watch fsnotify, debounce, rebuild/reindex, construcción de snapshot inmutable, publicación/swap atómico, increment de generation.
- **FRONTEND = CERO responsabilidad de filesystem:** `internal/web` NUNCA lee el vault, NUNCA vigila paths, NUNCA enumera directorios, NUNCA resuelve paths locales, NUNCA usa browser filesystem APIs contra el vault, NUNCA conoce el vault root físico. La UI sólo observa el estado publicado por el backend a través de HTTP (polling de `generation` en `/api/v1/meta` → invalidate/refetch de la vista actual).

## Storage decision (congelada)

- **NO SQLite en v0.1.** Evidencia: 2741 notas (escaneo completo < 1s), queries v0.1 son rollups/lookups/filtros sobre snapshot completo en memoria, backlinks = mapa inverso trivial, rebuild = rescan. SQLite añadiría schema + driver + migraciones + cache files para cero valor actual.
- Criterios de re-apertura (disparadores futuros, no hoy): FTS5 para búsqueda ranking; volumen de notas ×10; queries de agentes sobre proyecciones persistentes; sync incremental entre procesos.
- Si se adopta: SIEMPRE derivada, nunca source of truth, con el mismo test de invariancia rebuild==incremental.

## Graphify decision (congelada)

- **Loom v0.1 NO integra Graphify y NO lo requiere.** Graphify es índice derivado orientado a agentes (CLI, cache machine-local); el binario ni siquiera está instalado en esta máquina (verificado 2026-09-13). Loom computa localmente las derivaciones que necesita (wikilinks→edges, frontmatter→relaciones tipadas, backlinks) en memoria en < 1s.
- **Alineación semántica sin acoplamiento:** el modelo de relaciones de Loom usa el mismo allowlist que Graphify (relaciones tipadas desde frontmatter; body links = `references`; tags = facets) para que una futura convergencia (MCP/agentes) no exija migración semántica.
- **Graceful degradation:** trivial — Graphify no es dependencia, luego no es SPOF. Sin duplicación material: las derivaciones duplicadas son ~40 líneas de resolución de links que Loom necesita de todos modos para su propia UI.

## API contract v0.1 (congelado; JSON, read-only, sin auth — loopback only)

- **Identity rule:** toda referencia autoritativa a proyecto o nota en la API es el **path del vault** (DocumentID = source Note path); `name`/`alias` existen SOLO como convenience de routing/search y resuelven a path (shortest-path, fail-closed ante ambigüedad). Los parámetros que referencian proyectos (p. ej. `tasks?project=`) toman el path.
- **Security invariant (DocumentID resolution):** los path parameters HTTP que representan DocumentIDs de Note/Project **NUNCA se concatenan al vault root para abrir archivos** (`vaultRoot + requestPath → os.Open(...)` está PROHIBIDO). Flujo obligatorio: request path → validar/normalizar como DocumentID → resolver EXCLUSIVAMENTE contra los DocumentIDs presentes en el snapshot/index publicado → usar la identidad ya indexada. Rechazar en el boundary HTTP/aplicación: paths absolutos, `..`, intentos de traversal, paths que escapen del vault, encoding inválido, DocumentIDs no normalizados e identidades ausentes del snapshot publicado. Las lecturas de filesystem pertenecen al backend de indexación/scanning, NUNCA a request paths arbitrarios. Sin subsistema de seguridad separado — es una regla del boundary, probada por tests de aceptación en T10/T11.
- `GET /api/v1/meta` — vault root (relativo), counts (notas/projects/tasks/diagnostics), build info, last scan timestamp, **`generation` (entero monotónico, ++ por cada publicación/swap de snapshot)**, health flag. Conceptual: `{"generation": 42, "last_scan": "...", "healthy": true}` — sin sobre-especificar campos más allá de lo ya congelado.
- `GET /api/v1/projects?status=&area=&owner=&include=archived` — cards de proyectos: `path` (identidad), `name` (convenience), envelope (owner/root/parent/area/status/priority/progress), rollup de tasks, has-children.
- `GET /api/v1/projects/{path...}` — detail por path: envelope completo, tasks agrupadas por estado, subproyectos, parent, links de la nota.
- `GET /api/v1/projects/resolve?name=&alias=` — convenience lookup name/alias → `{path}` (o `AMBIGUOUS`/`NOT_FOUND`); nunca sustituye el addressing por path.
- `GET /api/v1/areas` — áreas con conteos de proyectos/notas.
- `GET /api/v1/tasks?owner=&state=&area=&type=&project=<path>` — índice global de tareas con note origen y línea.
- `GET /api/v1/notes/{path...}` — detail: envelope, tasks, links (raw + resolved + unresolved), attachments, backlinks, headings.
- `GET /api/v1/notes/{path...}/render` — HTML server-side (goldmark) con wikilinks → hrefs internos, callouts renderizados, bloques dinámicos como `<pre class="lens-raw-block">`.
- `GET /api/v1/search?q=&scope=titles|content&limit=` — matches con snippet y score simple.
- `GET /api/v1/diagnostics` — resumen de errores de parse, links ambiguos/rotos, valores desconocidos, por-nota.
- Errores: JSON `{error, code}` (`NOT_FOUND`, `BAD_QUERY`, `VAULT_UNAVAILABLE`); 404 para nota inexistente; nunca 500 por una nota individual malformada (va a diagnostics).
- Compatibilidad frontend/backend: el contrato vive en esta sección; cambios posteriores = versión `/api/v2`, no mutación silenciosa.

## Frontend (congelado)

- Vue 3 + Vite + TypeScript strict. **Sin React, sin Electron, sin dependency zoo.**
- vue-router: `/` (Home cockpit), `/project/*path` (identity = path codificado; el nombre nunca es clave de ruta), `/note/*path` (viewer), `/search`, `/diagnostics`.
- **Live refresh (KISS):** polling ligero de `generation` en `/api/v1/meta`; al cambiar → invalidar los datos derivados afectados/actuales → refetch de la vista actual por la API HTTP existente. Sin WebSockets, sin SSE, sin event bus interno, sin acceso browser al filesystem, sin push infra en v0.1 (reabrible por evidencia).
- **Hard boundary:** la SPA no conoce el vault root físico y no tiene ninguna responsabilidad de filesystem (ver § Filesystem ownership).
- Estado: composables module-scope + `fetch`; **sin Pinia en v0.1** (estado compartido mínimo: meta/generation + cache de project list; si crece, se evalúa entonces).
- Render Markdown: server-side (goldmark, § API); la SPA inserta HTML sanitizado, intercepta links internos y resalta el heading ancla. Sin parser markdown en el cliente.
- Graph visualization: **deferred a F6** (los datos de links ya existen desde F1; nada se bloquea). Candidatos a evaluar entonces: canvas propio ligero vs librería force-graph; decisión en su momento.
- UI: CSS propio mínimo, dark-first, sin UI kit pesado. Task board y cards replican la semántica de los tableros actuales (badges por estado, colores por owner).

## Error / consistency model (congelado)

- **Frontmatter malformado o incompleto:** nota sirve con body raw, sin proyección (no aparece en boards), diagnostic registrada. Nunca crash, nunca se oculta.
- **Wikilink roto:** link renderizado como unresolved (estilo distinto), contado en diagnostics.
- **Target ambiguo (nombres duplicados):** resolver shortest path (comportamiento Obsidian) y flag de ambigüedad en diagnostics.
- **Nota cambia/desaparece durante indexación:** el walk del filesystem **NO es atómico** — la semántica congelada es **best-effort scan + immutable snapshot + atomic publication/swap**: el scan puede observar el vault en distintos instantes, el snapshot se construye en memoria y se publica por swap completo (el punto de consistencia es la publicación, no el walk); los requests siempre ven un snapshot completo coherente, nunca estados intermedios. Sin locking ni infraestructura adicional. El watcher (fsnotify + debounce) dispara el rebuild; cada rebuild termina en swap atómico con `generation++`.
- **Vault inaccesible al arranque:** el proceso falla con error claro (sin vault no hay producto). Vault inaccesible en runtime (unmount temporal): mantener último snapshot + health flag en `/meta` + retry en próximo trigger; degradación visible, no muerte silenciosa.
- **Valores de enum desconocidos (status/owner/type legacy):** preservados raw, sin proyección parcial inventada, diagnostic.
- **Identidad duplicada:** dos notas mismo nombre = ambigüedad documentada (ver arriba); nunca merge silencioso.
- **Principio:** partial availability + diagnostics sobre whole-app death; corrupción factual siempre visible.

## Test strategy (congelada)

- **Unit:** funciones puras del dominio (parse de task line, link, normalización de paths NFC) y del boundary HTTP (validación/normalización de DocumentIDs: absolutos, `..`, traversal, encoding inválido, no normalizados → rechazo).
- **Parser fixtures:** corpus real sanitizado en `internal/parse/testdata/` — subset representativo del vault real: project con dataviewjs, area, resource con callouts, skill, agent_memory con `memory_state: superseded`, nota legacy malformada, nota con embeds + heading links. Golden structures, no snapshots frágiles.
- **Index tests:** invariancia de rebuild (rescan ×2 == snapshot idéntico, hash de estructuras); conteos de proyecciones contra fixture vault; resolución shortest-path y ambigüedades; **live refresh**: modificar un archivo del fixture vault → watcher dispara rebuild → generation++ → nuevo snapshot contiene el cambio.
- **API tests:** `httptest` sobre index con fixture vault; contrato JSON exacto por endpoint; **security tests de DocumentID/path** (traversal, `..`, absoluto, encoding inválido, identidad ausente del snapshot → rechazo en boundary, nunca os.Open sobre request path).
- **Frontend:** tests de componente SOLO para task board, helpers de routing de links y la lógica de polling/invalidate-refetch de generation (Vitest); el resto e2e manual.
- **E2E walking skeleton:** script manual verificable contra el vault real (las 5 capabilities + live refresh sin reinicio + una nota con frontmatter malformado + un link ambiguo + intento de traversal por HTTP rechazado).
- Sin mocking excesivo: parser+index reales sobre fixtures. Coverage: caminos críticos primero (parse tolerante, snapshot swap/publicación, resolución y validación de DocumentIDs, ciclo watcher→rebuild→swap), piso ≥ 95% en `internal/vault` + `internal/index` (regla del owner). No se escribe test de ramas inalcanzables: se borran.

## Roadmap (vertical slices, cada F = capability verificable end-to-end)

- **F1 Walking skeleton + live refresh mínimo:** repo scaffold + `internal/{vault,parse,index}` mínimos + API `meta` (con `generation`)/notes/render + SPA que renderiza una nota real con links resueltos y backlinks; backend con watcher fsnotify + debounce + rebuild automático + snapshot inmutable + swap atómico + generation++; SPA observa generation por polling y refetch de la vista actual. Gate: binario único corre contra el vault real, muestra la nota, y **modificar una nota real del vault se refleja en la UI SIN reiniciar Loom**.
- **F2 Projects cockpit:** API projects/areas + vistas Home y Project con rollup, huérfanos, task board. Gate: replicar el Panel de Proyectos + el board de un proyecto real con los mismos datos.
- **F3 Tasks + backlinks + áreas:** índice global de tareas filtrable + panel de backlinks en el viewer. Gate: el filtro `#owner/me #type/supervision` del Panel de Proyectos reproducible desde la API.
- **F4 Search + diagnostics:** búsqueda títulos+contenido + página de diagnósticos con conteos reales del vault. Gate: encontrar una nota por substring de contenido y ver sus diagnósticos.
- **F5 Hardening del live refresh (NO su introducción):** robustez y performance del MISMO mecanismo de F1 — eventos burst/coalescidos, rename, delete, ráfagas de escritura, restart/recovery del watcher, vault temporalmente inaccesible, lecturas concurrentes durante rebuild, race tests, correctness de rebuild, performance medida, diagnósticos stale/health — más endpoint de rebuild, aristas visibles (links ambiguos/rotos) y empaquetado `make build` binario único. Gate: suite de hardening PASS (incluye race) y build binario único verificado en máquina personal.
- **Post-v0.1 (deferred):** F6 graph view · F7 SQLite/FTS si los disparadores del § Storage ocurren · F8 MCP adapter read-only (reopen trigger: necesidad demostrada de query/retrieval programático sobre Loom — no por disponibilidad de Graphify) · F9 export snapshot estático (plan B política) · F10 desktop wrapper · F11 limited editing (CQRS chico sobre Markdown, lejano) · F12 CouchDB sync · F13 rich Graphify interop.

## Subagent execution model (congelado)

Cuatro roles, no más. Ownership por package es la frontera de archivos; la EJECUCIÓN es estrictamente secuencial.

- **LÍMITE DURO OPERACIONAL: `MAX_CONCURRENT_LOOM_SUBAGENTS = 1`.** La capacidad global de ejecución está compartida con otros dos tracks independientes de larga duración: Loom puede tener **a lo más UN subagente activo en todo momento**. No hay `R2 ∥ R3`, no hay lanzamiento especulativo de workers, no hay delegación recursiva. Este límite overridea la independencia file-level.
- **Un especialista Loom NUNCA lanza otro subagente.** Si identifica trabajo paralelo útil: lo registra como READY/propuesto (con deps y rol sugerido) en esta nota y lo deja en cola — NO lo lanza.
- **R1 core-go** — scope: `internal/{vault,parse,index}` + fixtures. Read: esta nota + vault real + docs Go. Write: SOLO esos packages y sus tests. Ownership del dominio, parser e índice (T03–T09). Deps: ninguna (primero). Reasoning: high (decisiones de borde de parse/tolerancia).
- **R2 api-go** — scope: `internal/serve` + wiring en `cmd/loom`. Read: § API contract + surface de `internal/index`. Write: SOLO serve/cmd. Deps: R1 (surface de index). Reasoning: normal.
- **R3 frontend** — scope: `internal/web/**` (Vue) + glue de build embed. Read: § API contract + § Frontend + vault real por browser. Write: SOLO web + su build. Deps: contrato API congelado (ejecuta DESPUÉS de R2, en secuencia). Reasoning: normal.
- **R4 integrator-verifier** — scope: Makefile, e2e script, gates finales, revisión de allowed-scope, de la invariancia rebuild y del live refresh. Read: todo. Write: SOLO cmd/Makefile/scripts de verificación + reporte. Deps: R1+R2+R3. Reasoning: high.

- **Cadencia (secuencia estricta):** WP-A → R1 (WP-B, WP-C) → R2 (WP-D) → R3 (WP-E) → R4 (WP-F). `TOP` (esta nota + decisiones) es editado por el orchestrator; `NORMAL` (R1–R3) implementa tasks mecánicamente sin rediseñar contratos; desviación → volver a esta nota, no fork mental.

## Long-run orchestration contract (congelado)

- **Única fuente de planificación:** esta nota (§ Work packages + `## ✅ Tareas` + `## 📆 Bitácora` + `progress:`). Ningún plan paralelo en chat ni scratch durable.
- **Ciclo del orchestrator (con límite duro de 1 worker):** LOAD esta nota → SELECT una task READY (deps `[x]`) → DISPATCH a lo más UN subagente Loom → WAIT hasta que el worker TERMINE COMPLETAMENTE → VERIFY contra AC + gates → reconciliar source/planner → CLOSE worker → UPDATE task/estado/evidencia en esta nota → SELECT siguiente task → dispatch del siguiente worker único. Crash/restart/new session = re-leer esta nota y continuar; la nota basta para retomar sin preguntar al owner.
- **Handoff de sesión:** al pausar, `## 📆 Bitácora` registra qué task quedó en qué estado y qué evidencia existe; `progress:` refleja el porcentaje real de tasks `[x]` sobre T01–T17.

## Work packages y atomic tasks

Formato de task: objetivo · allowed files · AC · tests · deps · non-goals. Los T-tasks viven aquí (el repo no existe aún); al existir el repo, WP-A traslada TASKS a `specs/` según patrón vigente y esta tabla queda como work packages.

**WP-A Scaffold (T01–T02)** — requiere acción física del owner: crear repo `xKoRx/loom` (branch `master`) + workspace `~/go/src/github.com/xKoRx/loom` (ver `Blockers`).
- **T01 Go scaffold:** objetivo = módulo Go `github.com/xKoRx/loom` + `cmd/loom` (flag `--vault`, config) + Makefile `build/test/lint` que produce el binario `loom`. Allowed: `go.mod`, `cmd/loom/**`, `Makefile`, `README.md`. AC: `make build` produce `loom`, que arranca con `--vault` apuntando al vault real y sirve 404 en `/api/v1/meta` (stub). Tests: smoke de arranque. Deps: repo `xKoRx/loom` creado y workspace inicializado (acción owner). Non-goals: ningún handler real.
- **T02 Web scaffold:** objetivo = Vite + Vue 3 + TS + vue-router con rutas vacías + pipeline `make web` que compila a `internal/web/dist` y `go:embed` lo sirve en `/`. Allowed: `internal/web/**`, Makefile, `cmd/loom` (solo mount del embed). AC: browser en `127.0.0.1:<port>/` muestra el shell con routing. Tests: smoke de build. Deps: T01. Non-goals: vistas reales.

**WP-B Parse core (T03–T05)** — R1.
- **T05 fixtures primero:** objetivo = corpus sanitizado en `internal/parse/testdata/` (project con dataviewjs, area, resource con callouts, skill, agent_memory superseded, legacy malformada, embeds + heading links + alias links, nota con `#owner/*` tasks y estados 5). Allowed: `internal/parse/testdata/**`. AC: fixture vault reproduce los 8 casos de evidencia del muestreo. Deps: T01. Non-goals: parser.
- **T03 Frontmatter parser:** objetivo = YAML front matter → **map crudo con acceso tipado** (genérico, sin semántica Agents-OS), tolerante (malformado → raw + diagnostic, sin panic). El EntityEnvelope se proyecta en index (T07), no aquí. Allowed: `internal/parse/**`, `internal/vault/**`. AC: 100% del corpus parsea sin panic; malformada produce diagnostic y body raw; NFC normalización de paths. Tests: fixtures golden. Deps: T05. Non-goals: YAML completo con anchors/aliases exóticos (fail-closed tolerante).
- **T04 Body extraction:** objetivo = goldmark AST → headings, tasks (5 estados + tags owner/type/flags + 📅), wikilinks (plain/alias/heading/embed), inline tags, callouts detectados, bloques de código (dinámicos marcados RAW). Allowed: `internal/parse/**`. AC: todas las estructuras del corpus extraídas con línea correcta; block refs → ignorados sin error (0 en vault). Tests: fixtures. Deps: T05, T03. Non-goals: render HTML (va con T11 render), math/mermaid (raw).

**WP-C Index + live refresh (T06–T09)** — R1.
- **T06 Scanner + snapshot + watcher + generation:** objetivo = walk best-effort del vault (excluye `.obsidian`, `.git`; el walk NO es atómico), build de snapshot inmutable en memoria, publicación/swap atómico del snapshot completo con **increment de `generation` monotónico**; **watcher fsnotify + debounce corto** que dispara rebuild automático (mismo pipeline scan→snapshot→swap) sin reinicio de proceso. Allowed: `internal/index/**`. AC: escanea el vault real < 1s; snapshot inmutable; publicación atómica (nunca estados intermedios visibles); determinístico ante vault idéntico; vault mutado durante el scan → snapshot best-effort válido; **modificar una nota del vault real → generation++ y snapshot nuevo con el cambio, sin reiniciar Loom**. Tests: determinismo ×2 + swap concurrente + ciclo evento→rebuild→swap. Deps: T03+T04.
- **T07 Projections + task index (capa Agents-OS de index):** objetivo = EntityEnvelope proyectado del frontmatter crudo + Project/Area proyecciones (owner/root/parent/area/status/priority/progress/rollup/children, **identidad = path**) + Task projection (owner/type/state interpretados sobre la extracción raw) + índice global de tareas + typed relations desde frontmatter (allowlist Graphify) + facets de tags. Allowed: `internal/index/**`, `internal/vault/**`. AC: Panel de Proyectos reproducible: cards filtrables por type/owner/status/parent + huérfanos detectados en el vault real. Tests: conteos contra corpus + vault real smoke. Deps: T06.
- **T08 Link resolution + backlinks:** objetivo = resolver wikilinks por TitleName + aliases, shortest-path ante duplicados, ambigüedades flaggeadas, mapa inverso de backlinks. Allowed: `internal/index/**`. AC: 0 resolución incorrecta en corpus; ambigüedades y rotos van a diagnostics. Tests: fixtures + invariant. Deps: T06.
- **T09 Rebuild invariance test:** objetivo = test de la invariante central: delete-all-derived → rescan → snapshot idéntico (hash de estructuras completas). Allowed: `internal/index/**` (tests). AC: PASS sobre corpus y sobre vault real. Deps: T07+T08. Non-goals: optimizaciones incrementales (hardening del watcher es F5).

**WP-D API (T10–T12)** — R2.
- **T10 meta/projects/areas + security boundary:** objetivo = endpoints según § API contract sobre la surface de index, incluida **exposición de `generation` en `/api/v1/meta`**; validación/normalización de DocumentIDs en el boundary (sin `vaultRoot + requestPath → os.Open`; resolución exclusiva contra el snapshot publicado; rechazo de absolutos, `..`, traversal, encoding inválido, no normalizados, identidades ausentes). Allowed: `internal/serve/**`, `cmd/loom` wiring. AC: JSON exacto al contrato; filtros funcionan; bind 127.0.0.1; **security tests de path/traversal/identidad-desconocida PASS**. Tests: httptest con fixture vault. Deps: T07.
- **T11 notes/render/search/tasks:** objetivo = `notes/{path}`, `render` (goldmark HTML con wikilinks reescritos, callouts, bloques dinámicos raw), `tasks`, `search` — todos resolviendo DocumentIDs solo contra el snapshot (security invariant). Allowed: `internal/serve/**` (+ goldmark aquí, no en parse: render es presentación de transporte). AC: una nota real del vault renderiza legible con links navegables; búsqueda por substring encuentra; requests con paths maliciosos rechazados en boundary. Tests: httptest incl. security. Deps: T08+T10.
- **T12 diagnostics + error model:** objetivo = endpoint diagnostics + errores JSON `{error, code}` + health flag en meta. AC: nota malformada del vault real aparece en diagnostics y NO rompe ningún otro endpoint. Tests: httptest. Deps: T11.

**WP-E Frontend (T13–T16)** — R3, ejecuta DESPUÉS de R2 (secuencia estricta; sin paralelismo).
- **T13 Shell + routing + fetch composable + generation polling:** objetivo = SPA con rutas, layout dark, composables de fetch y error handling + **polling ligero de `generation` en `/api/v1/meta`**: al cambiar → invalidar datos derivados afectados/actuales → refetch de la vista actual por la API existente. AC: navega las 5 rutas contra API real; **modificar una nota del vault real mientras la SPA está abierta → la vista se actualiza sin reiniciar ni recargar manualmente**. Deps: T02, T10.
- **T14 Note viewer:** objetivo = `/note/*path` con HTML renderizado, envelope visible, backlinks panel, links internos interceptados. AC: leer una nota real con frontmatter, un dataviewjs visible como raw block, y volver por un wikilink. Deps: T11+T13.
- **T15 Projects cockpit + detail + task board:** objetivo = Home cards (por área/owner/estado/prioridad, huérfanos) + `/project/*path` con board 5 estados y subproyectos (deep-linking por path, no por nombre). AC: replicar visualmente el contenido real del Panel de Proyectos y el board del proyecto padre. Deps: T11+T13 (secuencial tras T14).
- **T16 Search + diagnostics pages:** objetivo = `/search` con resultados/snippets + `/diagnostics` con conteos y detalle. AC: flujo completo de búsqueda y diagnóstico sobre vault real. Deps: T12+T13 (secuencial tras T15).

**WP-F Gates (T17)** — R4.
- **T17 E2E + hardening del live refresh:** objetivo = script e2e manual (5 capabilities + live refresh sin reinicio + caso malformado + link ambiguo + traversal HTTP rechazado), hardening del mecanismo F1 (burst/coalesced events, rename, delete, ráfagas de escritura, restart/recovery del watcher, vault temporalmente inaccesible, lecturas concurrentes durante rebuild, race tests, correctness de rebuild, performance medida, diagnósticos stale/health), `go vet`+`gofmt`+`go test -race -cover` (piso 95% vault/index), build binario único `loom` verificado en máquina personal, README mínimo. AC: todos los gates PASS + bitácora con evidencia. Deps: T14+T15+T16.

**Dependency graph:**

```text
T01 → T02
T01 → T05 → T03 → T04
T03+T04 → T06 → T07
T06 → T08
T07+T08 → T09
T07 → T10 → T11 → T12        (T11 también depende de T08)
T02+T10 → T13 → T14 → T15 → T16   (secuencia estricta; antes T14 ∥ T15 — eliminado por MAX_CONCURRENT_LOOM_SUBAGENTS=1)
T14+T15+T16 → T17
```

## TOP / NORMAL boundaries

- **TOP:** esta nota (contratos, decisiones, allowed scope), el padre [[Loom]] (decisiones owner) y la creación del repo. NO source Go.
- **NORMAL:** R1–R3 implementan T-tasks mecánicamente contra el contrato congelado. No rediseñar FR/AC, no ampliar allowed files, no introducir dependencias no listadas, no "arreglar" el vault (read-only siempre).
- **GOD (decisiones que escalan al owner):** cambio del contrato API o del domain model; feature fuera de § V0.1 committed scope; relajar MAX_CONCURRENT_LOOM_SUBAGENTS.

## Blockers

- **B1 (acción física del owner, bloquea WP-A):** crear el repo GitHub `xKoRx/loom` con branch default `master` y dejarlo disponible en el workspace local `~/go/src/github.com/xKoRx/loom` (clonar o `git init` + remote). **Estado: la decisión está tomada (nombre/repo/workspace/módulo/binario registrados), pero la existencia del repo NO fue verificada hoy (no existe en GitHub ni en el workspace).** No se inventa SHA ni base; al existir, registrar el commit base real en `## 🧱 Entrega de desarrollo`. Mientras tanto, WP-B/C/D/E no arrancan (sin repo no hay allowed files). Única alternativa permitida: arranque del owner explícito para trabajar en workspace local sin repo — NO asumido.
- No bloquear por: Graphify stale/ausente, frontmatter legacy del vault, o notas malformadas — todo eso es input válido del dominio con manejo definido.

## Acceptance gates (F0→ejecución)

- [x] Project Lens existente cargado (hoy canónico Loom).
- [x] Agents-OS actual inspeccionado (convenciones, schema contract, templates, patrón parent/agentes, Echo E-01 como referencia).
- [x] Muestra real del vault inspeccionada (tipos, links, tasks, lifecycle, attachments, identidad, bloques dinámicos).
- [x] Graphify inspeccionado (contrato + estado real: binario ausente en esta máquina).
- [x] Vue 3 congelado como frontend.
- [x] Domain entities definidas con clasificación ENTITY/VO/PROJECTION/INDEX RECORD/INFRA.
- [x] Identity model definido (path-based, evidencia).
- [x] Canonical vs derived definido (matriz + invariante de reconstrucción).
- [x] Boundaries definidos con forbidden deps.
- [x] Dependency direction definida.
- [x] v0.1 scope cerrado (5 capabilities, F1–F5, live refresh en F1).
- [x] Future drivers separados (F6–F13 explícitos).
- [x] CouchDB NO implementado · MCP NO implementado · Plugin runtime NO implementado · Semantic search NO implementado · SQLite NO implementado · WebSockets/SSE/event bus NO implementados.
- [x] Architecture seams mínimas justificadas (package boundaries; cero interfaces especulativas).
- [x] Roadmap vertical definido (F1 = walking skeleton + live refresh mínimo; F5 = hardening del mismo).
- [x] Tasks atomizadas (T01–T17 con AC/deps/non-goals, incl. live refresh y security tests).
- [x] Acceptance gates por fase definidos.
- [x] Test strategy definida (fixtures reales, invariancia, security tests de DocumentID, piso 95% crítico-primero).
- [x] Subagent execution strategy definida (4 roles, ownership por package, MAX_CONCURRENT_LOOM_SUBAGENTS=1, sin delegación recursiva).
- [x] Long-run orchestration definida (nota = única fuente; ciclo LOAD→DISPATCH 1→WAIT→VERIFY→CLOSE→UPDATE).
- [x] Adversarial architecture pass ejecutado (2026-09-13, ×3: fundación, review y finalización — ver Bitácora).
- [x] Proyecto Agents-OS actualizado y renombrado a Loom (padre + este planner + idea promovida; aliases históricos preservados).
- [x] Cero product code implementado.
- [x] **OWNER:** nombre canónico (Loom) + repo (xKoRx/loom) + workspace (~/go/src/github.com/xKoRx/loom) + módulo + binario + branch decididos.
- [ ] **OWNER:** política MELI validada (gate de riesgo, no técnico).
- [ ] **OWNER:** crear repo `xKoRx/loom` (branch `master`) + workspace local → desbloquea WP-A; registra commit base real.

## Risks

- **R1 Política corporativa MELI (owner):** que el veto a Obsidian extienda el veto a binarios propios. Mitigación: desarrollo y uso en máquina personal; F9 (export estático) es el plan B documentado; decisión owner ANTES de invertir horas.
- **R2 Unicode/encoding en paths:** áreas con acentos y `&` ("Economía de Tokens", "Casa & Energía"). Mitigación: NFC + case-preserved + tests desde T03.
- **R3 Frontmatter legacy/malformado:** evidenciado (valores `PENDING|RUNNING|…`, tipos no contractuales). Mitigación: tolerancia fail-open por nota + diagnostics desde T03.
- **R4 Dialecto Obsidian del Markdown:** callouts (`> [!info]`), embeds, comentarios `%% %%`, wikilinks a headings. Mitigación: corpus real como fixture desde T05; render subset declarado (lo no soportado queda raw legible).
- **R5 Scope creep hacia "knowledge runtime":** la idea de agosto propone SQLite day-1, MCP y Context Bundles. Mitigación: non-goals congelados con por qué; future drivers con disparadores de re-apertura explícitos.
- **R6 Repo sin crear (acción owner):** toda la ejecución depende de B1; el planner del vault es válido pero SPEC/TASKS deben migrar al repo cuando exista (patrón vigente).
- **R7 Concurrency limit:** MAX_CONCURRENT_LOOM_SUBAGENTS=1 alarga el wall-clock de ejecución (antes T14∥T15). Mitigación: secuencia definida por dependencias reales; trabajo paralelo identificado se encola como READY para review del owner.

## Closure conditions (v0.1)

- T01–T17 `[x]`; gates de T17 PASS (test/race/cover ≥95% vault+index/vet/gofmt); invariancia rebuild PASS sobre vault real; e2e de las 5 capabilities + live refresh sin reinicio con evidencia en bitácora; `## 🧱 Entrega de desarrollo` actualizada con repo/branch/base reales; entrega a Review (`[r]` en tarea puente del padre); cero código throwaway.

## 🧩 Subproyectos

_No aplica — este es el subproyecto de fundación/implementación de Loom; no crea más hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Ver [[convenciones]]. %%
> - [ ] WP-A Scaffold: T01 Go scaffold (module github.com/xKoRx/loom, binario loom) + T02 Web scaffold #owner/agent #type/dev #area/personal #blocked
> - [ ] WP-B Parse core: T05 fixtures → T03 frontmatter → T04 body #owner/agent #type/dev #area/personal
> - [ ] WP-C Index + live refresh: T06 scanner/snapshot/watcher/generation → T07 projections → T08 links/backlinks → T09 rebuild invariance #owner/agent #type/dev #area/personal
> - [ ] WP-D API: T10 meta/projects/areas + security boundary → T11 notes/render/search/tasks → T12 diagnostics #owner/agent #type/dev #area/personal
> - [ ] WP-E Frontend (secuencial): T13 shell + generation polling → T14 viewer → T15 cockpit → T16 search/diagnostics #owner/agent #type/dev #area/personal
> - [ ] WP-F Gates: T17 e2e + hardening live refresh + build binario único #owner/agent #type/dev #area/personal

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

- **2026-09-13 (FOUNDATION FINALIZATION):** decisiones owner + execution constraints aplicadas al planner aceptado, sin reabrir arquitectura. **(1) Rename:** Project Lens → **Loom** (git mv con historial; `10-projects/Personal/Loom/Loom.md` + `agentes/Loom — Foundation v0.1.md`; aliases históricos preservados en frontmatter; links activos actualizados; artifacts de auditoría conservan el nombre viejo). **(2) Repo/workspace:** `xKoRx/loom` · `~/go/src/github.com/xKoRx/loom` · módulo `github.com/xKoRx/loom` · binario `loom` · branch `master` declarados; verificación física del repo: **NO existe** (gh + ls-remote fallan; workspace sin carpeta loom) → acción exacta registrada en Blockers, sin SHA inventado, `Entrega de desarrollo` truthful. **(3) Live refresh core en F1:** backend dueño exclusivo del fs (watch fsnotify → debounce → rebuild → snapshot inmutable → swap atómico → generation++), `generation` expuesto en `/api/v1/meta`, Vue observa generation por polling HTTP y refetch de la vista actual; sin WebSockets/SSE/event bus/push; F5 reclasificado como hardening del mismo mecanismo (burst, rename, delete, ráfagas, recovery del watcher, concurrencia, race, performance, health). T06/T10/T13/T17 extendidos; hard boundary frontend (cero fs) registrada como § Filesystem ownership. **(4) Concurrencia:** `MAX_CONCURRENT_LOOM_SUBAGENTS = 1` — secuencia estricta LOAD→SELECT→DISPATCH 1→WAIT→VERIFY→reconcile→CLOSE→UPDATE→NEXT; sin R2∥R3 (dependency graph ajustado T14→T15→T16); especialista no lanza subagents; trabajo paralelo útil se encola como READY. **(5) Security invariant:** DocumentIDs HTTP se resuelven EXCLUSIVAMENTE contra el snapshot publicado; jamás `vaultRoot + requestPath → os.Open`; rechazo en boundary de absolutos/`..`/traversal/encoding inválido/no normalizados/identidades ausentes; security tests en T10/T11. Adversarial pass de finalización: checklist completo PASS (rename canónico activo, sin repo/SHA inventado, backend dueño único del fs, cero fs en frontend, sin push infra, sin paralelismo residual, invariantes previas intactas). Cero product code.

- **2026-09-13 (FOUNDATION REVIEW — CORRECTION):** review del owner: arquitectura y roadmap ACCEPTED; 4 correcciones load-bearing aplicadas a este planner — (1) **Identity/API:** Project identity == source Note path; API re-addressada (`/projects/{path...}`, `resolve?name=&alias=` como convenience fail-closed, `tasks?project=<path>`, rutas Vue `/project/*path`); (2) **Boundary:** EntityEnvelope/Task projection separadas conceptualmente de la extracción raw — Frontmatter VO ahora es map crudo genérico en vault/parse y el envelope vive en la capa Agents-OS de index (T03/T07 alineados); (3) **Scan:** congelado best-effort scan + immutable snapshot + atomic publication/swap, sin locking (T06 y error model); (4) **MCP rationale:** deferred por falta de consumidor agent-facing en v0.1; reopen trigger = necesidad demostrada de query/retrieval programático sobre el producto; eliminado el claim "Graphify cubre retrieval de agentes" (también del padre). Adversarial pass sobre las 4 correcciones: sin residuos de name-as-identity; invariante de rebuild (T09) intacta; sin capas ceremoniales nuevas; decisiones accepted no reabiertas.

- **2026-09-13 (F0 — sesión de fundación/rebase):** rebase completo del proyecto sobre el Agents-OS vigente: inspeccionado el proyecto de agosto, la convención parent/agentes (referencia Echo E-01), schema contract, convenciones, el vault real (muestreo: 2741 notas; sin id system → identidad path-based; 218 alias links / 20 heading / 13 embeds / 0 block refs; 349 tasks con owner; estados legacy malformados presentes) y Graphify (contrato + binario ausente en esta máquina). Decisión de dominio validada con evidencia: Project/Area = typed projections de Note; identidad = path + TitleName/aliases; 5 estados de task + owner tags en el modelo. Storage: sin SQLite (in-memory snapshot). Graphify: sin dependencia, semántica alineada. Escrito este planner: dominio, matriz canonical/derived, boundaries con forbidden deps, API v0.1, roadmap F1–F5 + deferred F6–F13, T01–T17 con AC, 4 roles de subagent, orchestration contract, gates, riesgos y DoD. Adversarial pass ejecutado con 5 correcciones aplicadas: (1) eliminada la capa VaultID/EntityID de la idea de agosto (duplicaba autoridad de identidad sin evidencia); (2) interfaces SearchProvider/GraphProvider retiradas del diseño por YAGNI (queda package boundary + puntos de extensión documentados); (3) goldmark render movido a `internal/serve` (es presentación de transporte, no extracción de dominio); (4) proyecciones Project/Area sacadas de `internal/vault` hacia `internal/index` — el core genérico no filtra semántica Agents-OS (owner/parent/progress viven sólo en index); (5) resuelta contradicción del "único touchpoint" de parsing: goldmark permitido en `parse` (extracción) y `serve` (render de presentación), nunca en el dominio. Bloqueo registrado: B1 decisión owner nombre/repo/workspace. Cero product code.

## 🧭 Decisiones (frozen ADRs con matriz CURRENT NEED? / EXPENSIVE TO CHANGE?)

- **ADR-L1 Markdown = única autoridad; todo derivado reconstruible (Y+Y).** Invariante verificada por test (T09). No hay estado irreconstruible en v0.1.
- **ADR-L2 Note identity = path vault-relativo NFC; routing = TitleName + aliases; sin id system (Y+Y).** Evidencia: no existe `id:`/`uid:` global en el vault (solo incidental en tickets/ADRs); Obsidian y Graphify resuelven por nombre/alias.
- **ADR-L3 Go binario único + SPA Vue 3 embebida `go:embed` + bind 127.0.0.1 (Y+Y).** Sin Electron/Wails en v0.1 (Wails v3 alpha; wrapper = future driver).
- **ADR-L4 Índice in-memory; NO SQLite v0.1 (Y+N → opción más simple).** 2741 notas; queries = rollups/lookups. Re-apertura solo por disparadores del § Storage.
- **ADR-L5 Project/Area = typed projections de Note; una sola fuente de verdad (Y+Y).** Validado con evidencia: todo el estado de proyecto vive en frontmatter+body.
- **ADR-L6 Render Markdown server-side (goldmark); SPA consume HTML sanitizado (Y+N → más simple).** Evita duplicar parser en cliente; bloques dinámicos = raw.
- **ADR-L7 Sin dependencia de Graphify; semántica de relaciones alineada a su allowlist (N+Y → seam mínimo).** Convergencia futura (MCP) sin acoplamiento ni SPOF; binario ausente en esta máquina lo confirma como decisión, no como accidente.
- **ADR-L8 Bloques dinámicos (dataviewjs/base/tasks) = código crudo + panels propios equivalentes donde existan (Y+N).** Loom replica las proyecciones concretamente usadas, no un engine de queries.
- **ADR-L9 Ciclo de task de 5 estados (todo/wip/review/done/canceled) + owner/type/flags como parte del modelo (Y+Y).** Evidencia: convenciones + 349 tasks con `#owner/*`.
- **ADR-L10 Modelo de seguridad local: read-only, loopback-only, path traversal prohibido, sin contenido remoto, CSP (Y+Y).** Es la razón de ser del producto tras el veto.
- **ADR-L11 Live refresh es comportamiento core de v0.1 (owner, 2026-09-13): backend dueño exclusivo del fs — fsnotify + debounce → rebuild → snapshot inmutable → swap atómico → generation monotónico expuesto en `/api/v1/meta`; Vue observa generation por polling HTTP y refetch (Y+Y).** Sin WebSockets/SSE/event bus/push infra en v0.1 (reabrible por evidencia); F5 = hardening del mismo mecanismo, nunca su introducción.
- **ADR-L12 Ejecución estrictamente secuencial (owner, 2026-09-13): `MAX_CONCURRENT_LOOM_SUBAGENTS = 1`; sin delegación recursiva; capacidad global compartida con otros tracks (N+Y → constraint operacional, no arquitectura).** Overridea la independencia file-level; el ownership R1–R4 por package se preserva.
- **ADR-L13 Security invariant HTTP/DocumentID (owner, 2026-09-13): los path parameters NUNCA se unen al vault root para abrir archivos; resolución exclusiva contra el snapshot publicado; rechazo de absolutos/`..`/traversal/encoding inválido/no normalizados/identidades ausentes en el boundary (Y+Y).** Sin subsistema de seguridad separado; probado en T10/T11.

## 🔗 Docs / Links

- [[Loom]] — proyecto padre (owner decisions, tarea puente; nombre histórico: Project Lens).
- [[2026-08-25-project-lens-knowledge-runtime]] — idea de agosto (insumo histórico; promovida; su SQLite-day-1/MCP quedan como future drivers F7/F8).
- Convenciones vigentes: [[convenciones]] · contrato de schema: `80-agents/skills/_shared/schema-contract.md` · Graphify: [[graphify-contract]].
- Referencia de patrón de ejecución: [[Echo — E-01 Canonical SDK Foundation S0]] (parent/agentes/SPEC/TASKS/gates).
- Refs técnicas: goldmark (parse/render), fsnotify (watcher F1, hardening F5), Vue 3 + Vite + vue-router. Sin más deps.

## 💡 Ideas

### Backlog de ideas

- MCP adapter read-only (`loom.search/get_document/list_projects/query_tasks/backlinks/build_context`) — F8, sólo con evidencia de necesidad de agentes (reopen: query/retrieval programático sobre Loom).
- Graph view de entidades — F6; datos de links ya existen desde F1.
- Export snapshot estático (HTML navegable) — F9, plan B si la política MELI prohíbe binarios propios.
- CLI `loom serve|query` — se decide con el repo; `cmd/loom` ya es la semilla.

### Motivos / principios

- Una fuente por hecho: el vault es la autoridad; esta nota es el plan; el repo será el código.
- Small core, clear boundaries, few abstractions: boundaries de package reales, cero interface-per-class.
- Read-only primero: Loom nunca compite con el editor ni repite la superficie vetada.
- El backend es el único que toca el vault; la UI sólo ve snapshots publicados.
