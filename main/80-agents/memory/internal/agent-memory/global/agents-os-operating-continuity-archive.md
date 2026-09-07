---
type: agent_memory
schema_version: 1
scope: project
created: 2026-06-27
updated: 2026-09-03
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-operating-continuity]]"
aliases:
  - agents os operating continuity archive
  - agents os history
confidence: high
memory_state: archived
continuity_key: global/agents-os-operating-continuity
superseded_by: "[[agents-os-operating-continuity]]"
load_policy: manual
indexable: true
index_priority: low
tags:
  - agent/internal
  - area/personal
  - kind/agent-memory
  - project/agents-os
  - scope/project
---

# AGENTS OS Operating Continuity — Archive

## Continuidad

Histórico de continuidad pre-Hot-Path. Cada sección tiene fecha y se preserva como evidencia de las decisiones que llevaron al estado actual.

## Señales de carga

- Cargar manualmente sólo al depurar una decisión histórica específica de [[AGENTS OS]]; nunca como parte del startup.

## Próxima acción

- Ninguna; es un archivo histórico y no una fuente de estado vigente.

## 2026-06-27 — Setup inicial

- Codex forward-testeó bootstrap, context retrieval y Graphify maintenance.
- `graphify-obsidian update` puede fallar en sandbox sobre `~/.cache`;
  resuelto con wrappers `graphify-personal` y `graphify-obsidian` que
  redirigen `XDG_CACHE_HOME` localmente.

## 2026-07-07 — Clean install de graphifyy

- Instalado `graphifyy` (v0.9.4) limpio desde PyPI. Wrappers custom en
  `/usr/local/bin` separan personal vs obsidian, logs en `~/.config/` y
  copian reportes al vault automáticamente.

## 2026-07-08 — Higiene y session artifact naming

- Limpieza del obsoleto `60-actions/`; movido dashboard log a
  `80-agents/journal/logs/` y removidas referencias del healthcheck policy.
  Graphify reindexado después.
- Diagnóstico UUID filenames: el closeout requería L0/L1 pero no prohibía
  usar IDs externos como nombre visible. Fix en `agents-os-session-close`
  y `_shared/metadata-schema`: `YYYY-MM-DD[-HHMM]-human-topic-{raw,summary}.md`,
  UUID/hash/conversation IDs solo en `source_session`.
- Owner correction: NO correr closeout completo automáticamente al cerrar
  tarea. Closeout completo = L0/L1/feedback/distillation/reindex, requiere
  petición explícita. Log público:
  `2026-07-08-agents-os-explicit-closeout-only.md`.
- Residual: migrar 26 artefactos históricos con UUID/hash-visible names +
  directorios `sessions/{summary,summaries,system-1}` no canónicos con
  link-safe migration, luego reindex.

## 2026-07-02 a 07-05 — Resource Wiki / Economía de Tokens / Context Router

- Formalizada la **Resource Wiki** (LLM Wiki pattern) sobre `30-resources/`:
  nueva regla + mandamiento 16 (versión original) en constitución; nuevo
  `70-templates/index.md`; nueva skill `agents-os-resource-wiki`; nuevo
  runbook `resource-wiki-lint-reindex`; schema doc
  `30-resources/00-RESOURCE-WIKI.md`; piloto `applications/00-index.md` +
  `log.md`.
- Modelo mental: LLM Wiki = capa de contenido (verdad en `30-resources/`);
  Graphify = índice derivado. Componen, no compiten. NO confundir la wiki
  curada con Graphify `--wiki` (derivado, desechable, `graphify-out/`).
- Graphify arreglado vía `.graphifyignore`: removidos 512 trash + 170 json
  + 190 archive nodes → grafo AST limpio de 3163 nodos (trash/archive/json
  = 0).
- **DECISION 2026-07-03:** operar con INDEXES only, sin capa semántica.
  Retrieval primario = `00-index.md` curado; Graphify corre `update` (AST,
  free) como índice estructural. Semantic `extract --mode deep` PARKEADO:
  deepseek-r1 local quality poor; Gemini free tier insuficiente
  (gemini-2.0-flash quota 0, gemini-3-flash 5 rpm → 429). `GEMINI_API_KEY`
  removido de `~/.zshrc`. NO reintentar extract sin billing pago.
- CLI truth: `--mode deep` pertenece a `extract`, NO `update`
  (`update` = AST only).
- Query hygiene: usar **canonical entity names**, nunca tokens genéricos
  (matchean god-nodes).

### ADR token-economy-indexing-architecture

- 2026-07-03: creado ADR — 4-layer retrieval (tags → index.md → graph.json
  → body), cada capa filtra antes de la siguiente; load body-only.
- Veredicto: Graphify indices-only APORTA (lint/traversal/audit) si está
  limpio; estorba si se usa como markdown retrieval/semantic layer. Owner
  quiere thin wrapper sobre `graph.json` (no parchear site-packages; fork
  solo si necesario) + retrieval skill con las 4 capas.
- Experimentos+feedback system parkeado como idea.

### Builder / wikilinks chronicle

- 2026-07-03 (SUPERSEDED 2026-07-04): hallazgo inicial "graphify AST no
  captura `[[wikilinks]]`" → necesitaría custom builder. CORREGIDO:
  graphify SÍ parsea wikilinks, upstream los resolvía folder-relative;
  resuelto por fork vault-aware `graphify-obsidian` (no standalone builder).
  Vía A adoptada. grep=find / graphify=relate / semantic=meaning sigue
  válido.
- 2026-07-03: evaluado repo completo `/Users/rjara/fuentes/graphify`
  (corrido sobre sí mismo: 10316 nodes/17320 edges → fuerte en CODE).
  Root cause confirmado en `detect.py`: `.md` → DOC_EXTENSIONS → DOCUMENT →
  semantic-LLM-only; NO structural markdown/wikilink extractor. PERO
  extraction schema es pluggable (`{nodes,edges}` + `merge-graphs` +
  `--mcp` + `benchmark`). Plan builder: emitir schema graphify desde
  `[[wikilinks]]` y mergear; no reemplazar graphify. Evaluación completa
  en `10-projects/Economía de Tokens/`.

### Generalización del Context Router

- 2026-07-03: insight generalizado a principio global — constitución Regla
  Base "Una fuente canónica por hecho; comportamiento en skills,
  explicación en docs que enlazan (no repiten)". "Audience Split" añadido
  a `_shared/skill-contract.md`. Creada skill `agents-os-skill-authoring`
  (lean, referencia note-types/skill-contract/template, sin duplicación).
  Pendiente (aprobado por owner): slim `agents-os.md` a mapa+concepts,
  moviendo procedimiento duplicado a skills. **(Hecho en Hot Path P1,
  2026-07-25.)**

### 2026-07-04 (closeout) — Kaizen + hygiene pass

- Primer Kaizen report en `journal/feedback/kaizen-reports/2026-07-04-kaizen-report.md`
  (67 feedbacks escaneados vía subagent para ahorrar contexto; Graphify
  ~3.8/5 — fuerte en código, débil en markdown → valida el modelo de 4
  capas).
- Promovido el blocking pitfall a L3: known-error
  `graphify-markdown-wikilink-and-backend-gaps` ahora advierte **never
  invent Graphify CLI commands and never `rm graph.json`** (verify real CLI
  first). Hygiene report en `journal/hygiene/2026-07-04-token-economy-hygiene-review.md`;
  arreglados `tools/` links ambiguos, planner drift y missing canonical-change
  log.
- Para el code-phase agent: PoC specs (link-graph builder + thin wrapper)
  viven en `[[Economía de Tokens]]`; aplicar 4-layer router, soft budgets
  y el graphify pitfall known-error. Open Kaizen proposals (necesitan OK
  owner): tactical lightweight close, register lazy skills, delegation-chain
  skill, skill-frontmatter linter. **(Tactical close hecho en P2;
  delegation-chain y frontmatter linter cubiertos por `agents-os-doctor`
  en P3.)**

### 2026-07-04 (broad audit)

- Auditado TODO Sistema 1 (no solo token-economy). Arreglados: la
  **Session-Close duplication** (constitución vs `agents-os.md` competían/
  divergían → skill es ahora el procedimiento canónico, ambos docs apuntan
  a ella); template `learning.md` Evidencia (source-citation, no prose);
  skill frontmatter (hermes, operational-healthcheck); ADR cap language.
- PENDING (owner-flagged, hecho después): compactar los `## Evidencia`
  blocks de ~8 learnings de agents-os; reclassify
  `hermes-dashboard-recovery` (runbook-shaped skill).

### 2026-07-04 (both DONE)

1. Compactados 7 agents-os learnings' `## Evidencia` a citation form
   (link + concrete proof), por archivo, evidencia real preservada; 2
   archivos no tenían esa sección.
2. `hermes-dashboard-recovery` reclassificado — owner eligió **thin bridge**:
   borrada la skill masquerading de `80-agents/skills/`, creado `type:
   index` bridge en `memory/public/reference/hermes-dashboard-recovery.md`
   rutando a la skill live externa + runbook canónico
   `[[dashboard-hermes-agent]]` (sin procedimiento duplicado).
- Log: `journal/logs/2026-07-04-token-economy-two-hygiene-passes.md`.
  Token-economy doc/hygiene backlog vacío; solo code PoCs pendían (agente
  fresco). NOTA: `reference/` es hogar Sistema-1 para pointer/bridge nodes.

### 2026-07-04 (consistency implementation pass)

- 4 gaps DEFINE≠IMPLEMENT arreglados en Economía de Tokens:
  1. `agents-os-context-retrieval` ahora IMPLEMENTA el Context Router:
     4 capas cheap→expensive, intent→route table, context-pack output,
     Layer-2 wikilink caveat, sufficiency-first budget (reemplazó el fixed
     ~3,000-token target).
  2. `context-router.md`: principle 2 "tope duro"→soft per-tier ceiling
     (fact<relation<synthesis), + Layer-2 caveat callout.
  3. `_shared/graphify-contract.md`: `.graphifyignore` promoted a live +
     nueva sección "markdown wikilinks" structural-limitation.
  4. ADR: grep=find/graphify=relate/semantic=meaning formalizado.
- NO se tocó `agents-os.md` (project guard: high-authority, design+
  approval only). **(Hecho en P1 2026-07-25.)**
- Log: `journal/logs/2026-07-04-context-router-implemented-consistency.md`.

### 2026-07-04 (doc phase)

- Owner ordenó TODOS los docs primero, código al final (agente separado,
  contexto limpio, sistema mejorado). **Énfasis: SIN hard token cap en
  ningún lado — un cut crudo puede dropear la línea más relevante.**
- Arreglado: "Budget semantics" canónico definido UNA vez en
  `_shared/graphify-contract.md` (soft ceiling, escalate-on-miss, nunca
  guillotina) → cada `--budget N` disperso (incl. agents-os.md's 1200)
  hereda, así que no hace falta editar cada uno. Purgado cap wording en
  bootstrap + retrieval + graphify-maintenance. Añadido: index-escalation
  policy (00-RESOURCE-WIKI), typed-links design para relations
  graphifeable (ADR: relation written once in `## Relaciones`, edge-list
  GENERATED by builder not hand-curated), nuevas hygiene checks +
  recurring DEFINE==IMPLEMENT consistency audit, wiki pattern generalized
  to `tools/` (00-index.md+log.md; README demoted a conventions para matar
  el catálogo duplicado).
- 5to consistency gap encontrado: agents-os.md § Retrieval todavía enseñaba
  su propia graphify recipe (competía con el router) → diff PROPOSED, NOT
  applied (guard: high-authority file, needs owner approval). **(Hecho en
  P1.)**

### 2026-07-04 (doc-alignment pass)

- Propagado el diagnóstico CORREGIDO de wikilinks a todo Sistema 1. El
  claim viejo quedó SUPERADO; `graphify-obsidian` resuelve `[[wikilinks]]`
  como edges `references` (Capa 2 FUNCIONA; relaciona por **links**, no
  tags; builder standalone DESCARTADO en favor de Vía A).
- Alineados: ADR, known-error (reencuadrado RESUELTO, historia preservada,
  pitfall CLI/`graph.json` intacto), `context-router.md` (callout), skill
  `agents-os-context-retrieval`, `_shared/graphify-contract.md`.
- Caveat backlinks: `graphify-obsidian affected "<nota>.md" --relation
  references` (con `.md` Y la relación). ⚠️ Workaround "consultar por
  file-node id" es INCORRECTO (da vacío).
- `journal/` (logs/sessions/feedback) NO se tocaron: historia auditable
  con fecha.

### 2026-07-05 — Close budget + builder review

- **Close Artifact Budget** añadido a `agents-os-session-close` — soft
  ~1–1.5k ceiling en scaffolding efímero (L0/L1/feedback), vía
  `[[wikilink]]` reference (Layer 2 lo resuelve) no truncation; L3 exempt.
- Review del builder live: fork `graphify-obsidian` 0.9.5, 853 `references`
  edges (0 dangling), `affected --relation references` traverse backlinks.
  No code fix needed. Fixed last stale doc line (`context-router.md` Links
  section). Session-1 doc set fully consistent con "Layer 2 works in the
  vault". Project progress → 80%.

## 2026-07-08 MCP catalog check

- Refrescado `meli-claude-marketplace` con
  `claude plugin marketplace update meli-claude-marketplace`. El catálogo
  incluye `tp-to-feed-tbl` (skill plugin TP → FEED_TBL), pero no hay
  Template Processing MCP server standalone declarado; Codex sigue sin
  Template Processing MCP configurado.
- `claude plugin validate` en el marketplace upstream falla por
  inconsistencias manifest pre-existing (entry/plugin version drift), no
  por cambios locales.

## 2026-07-16 MCP access check

- En la sesión Codex actual, el tool registry expuesto no tiene tool que
  matchee `associations-assistant-mcp`, `association`, `meli`, ni `mercado`;
  tratar ese MCP como unavailable salvo que el connector se habilite en
  sesión futura.

## 2026-07-08 → 07-10 — Previous Price Motors TP chronicle

- Direct `ConsumerPriceDiscountMotors` replacement planeado como
  BigQueue-to-BigQueue transform en `vis-items-loader-tagging`: consumir
  `vis-items-history-save` con `vertical:motors` y `price`, mapear
  `msg.item_id/seller_id/category_id` → `id/sellerId/categoryId`, publicar
  a `topic-item-to-process[-test]` con filtros
  `process:price_before_discount_motors` y `vertical:motors`. Credenciales
  Tiger disponibles, pero sin Template Processing MCP configurado.
- **No crear ni desplegar sin confirmación explícita de target-scope.** El
  output schema/operación BigQueue exacto del TP sigue requiriendo
  verificación antes de creación externa.

### 2026-07-09 TP retry con nuevo nombre

- Intentado `tp-price-discount-motors-to-process-test` vía Fury CLI con
  VPN/network activo. Template creation devolvió 500; reintentos devolvieron
  `TSA-DUPLICATED_SERVICE_ERROR`, mientras `list`/`details` reportaban no
  template y child input creation devolvía `TSA-TEMPLATE_NOT_FOUND_ERROR`.
  El service name quedó reservado por creación parcial/orphaned.
- 2026-07-08 creation attempt: Fury CLI generó blueprints ENGINE/BQ_CONSUMER/
  BQ_TOPIC y `POST /tp/templates` devolvió 500. Retry devuelve
  `TSA-DUPLICATED_SERVICE_ERROR` para `price-discount-motors-to-process-test`,
  mientras `details` y `list` reportan no template. Tratar como orphaned
  platform service/name reservation; no usar suffix ni borrar servicio
  desconocido sin dirección de Rodrigo.

## 2026-07-10 — AGENTS OS team-adoption evaluation

- Grid local canónico: `10-projects/Economía de Tokens/agentes/AGENTS OS - Evaluación y Adopción/agents-os-evaluacion-grid.html`
  (source spec y editable SVG al lado). `outputs/agents-os-evaluacion-grid.html`
  es solo redirect.
- El Grid incluye seis casos de uso concretos + ejemplo explícito "cuando
  NO usar el circuito completo"; cada caso declara scenario, flow, value,
  limitation.
- Veredicto: mantener el core Markdown/canonical-entity/Context-Router/
  audit, pero recomendar **piloto controlado** antes que estandarización
  de equipo hasta completar beta formal E2E, benchmark propio de economics,
  cross-surface matrix, internal-memory governance, Graphify portability/
  noise fixes y prompt/rules pack regularization.
- Evaluación vive en el agent-owned child project `[[AGENTS OS - Evaluación y Adopción]]`
  bajo `[[Economía de Tokens]]`, con una human bridge task en Review. Su
  cover mapea Constitución, Context Router, memory layers, skills,
  feedback, Graphify, Sistema 1 y Sistema 2 antes del reporte crítico.
  Tras owner review, LLM Wiki explícito como Sistema 2 content-compilation
  layer y Context Router Layer 1, etiquetado honestamente como parcialmente
  implementado; no se cambiaron reglas públicas de AGENTS OS.
- Prepublication revision: removido el pill visual `COBERTURA PARCIAL`,
  cambiado el footer signature a `Baticoders · vis-nexus`, corregido el
  evidence disclaimer para distribución Grid. El blocker temporal
  Google/IAP se resolvió después.
- 2026-07-14: publicación del Grid completada desde el HTML local canónico.
  Remote private doc `01KXGAY6QKSZWEBR5SCY5JSWCE`, version 1, verified
  ready via Grid API; remote download difiere solo por runtime injection
  estándar de Grid.
- 2026-07-14 closeout: el agent project alcanzó 100% y su parent bridge
  pasó a Review tras verificar publicación privada en Grid. L0/L1 y ambos
  feedback notes creados. El known error público existente registra el
  Graphify engine rejection cuando local skill_version queda atrás del
  server; futuro upload debería health-check-ear la versión requerida.

## 2026-07-11 — ChatGPT iteration handoff

- Rodrigo quería un context pack compacto, presentation-style, para iterar
  AGENTS OS en ChatGPT a menor costo que sesiones Codex/Claude full-vault.
- Shape recomendada: progressive disclosure con short root README pointer,
  un portable canonical handoff, y apéndices opcionales; excluir memoria
  interna, raw sessions, logs, archives y output Graphify generado.
- Preservar el README root existente como landing del vault en vez de
  duplicar el project completo ahí. El handoff debe sintetizar fuentes
  públicas/canónicas verificadas y separar explícitamente facts actuales,
  evidence, gaps y proposals.
- Implementado bajo `10-projects/AGENTS OS/chatgpt-pack/`. El builder emite
  `outputs/agents-os-chatgpt/` + `outputs/agents-os-chatgpt.zip`, preserva
  rutas relativas canónicas, crea manifest SHA-256 y bundle verbatim base,
  rechaza internal-memory/journal leakage. Snapshot inicial copió 110
  archivos; ZIP SHA-256 starts `967f3a30b2506c45`. Source helpers y copias
  generadas excluidas de Graphify.
