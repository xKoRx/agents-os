---
agent: knowledge-architect
role: Knowledge Architecture
task_id: KBC-A
status: COMPLETE
project: "[[Echo — Knowledge Base Consolidation]]"
baseline: vault 9a5299f1 · echo f7ddea18 (feature/e02-control-safety-journal-recovery) · symphony 9fad768c (feature/f04-magic-version-handoff)
inputs: planner KBC (10-projects/Echo/agentes/Echo — Knowledge Base Consolidation.md), 30-resources/00-RESOURCE-WIKI.md, 80-agents/skills/agents-os-resource-wiki/SKILL.md, 30-resources/applications/00-index.md, 30-resources/agents/00-index.md, 20-areas/Echo.md, inventario docs de xKoRx/echo y xKoRx/symphony (sólo nombres/estructura, no contenido funcional)
scope: diseño topología documental, read-only
output_contract: este archivo es el único path escrito por este agente
started_at: 2026-09-12T23:15:00-03:00
updated_at: 2026-09-12T23:30:10-03:00
---

# KBC-A — Knowledge Architecture

## Assignment

Diseñar la topología documental objetivo de la campaña Echo — Knowledge Base Consolidation: inventario orientado a decisión, topología canonical bajo `30-resources/`, contraste con el patrón LLM Wiki vigente, reglas de publicación segura, plan de migración a alto nivel y handoff a las fases B–F. Read-only: ninguna publicación canonical en esta fase. Scope DEFAULT/personal, sin contexto MELI. Repos referenciados como `repo + path relativo` (`xKoRx/echo`, `xKoRx/symphony`), nunca paths de máquina.

## Baseline

- Vault Agents-OS: declarado `9a5299f1` master clean; HEAD real al escribir este artifact es `09746b3` (master, tree clean, 2 commits "sync" posteriores al baseline declarado). No bloquea: son avances del vault, no cambios de los repos.
- `xKoRx/echo`: `feature/e02-control-safety-journal-recovery` @ `f7ddea18`, working tree clean. Coincide con el baseline declarado.
- `xKoRx/symphony`: `feature/f04-magic-version-handoff` @ `9fad768c`, working tree con 1 archivo dirty. Coincide con el baseline declarado; sólo lectura, sin checkout/reset/stash.
- Reglas leídas y respetadas: constitución (invariantes 5, 11, 12, 13), `00-RESOURCE-WIKI.md` (dominios, escalado de índices, provenance, supersedes), skill `agents-os-resource-wiki` (ingest/query/lint), planner KBC.

## Findings

### Wiki canónica vigente en `30-resources/`

- Dominio activo `applications/`: índice plano con ~27 filas (16 apps + 11 recursos de arquitectura), por encima del umbral ~20 del contrato de escalado de `00-RESOURCE-WIKI.md`. Apps Echo: `echo-core.md`, `echo-forge.md`, `stager-app.md`.
- Páginas de app canónicas pero thin/stale: `applications/echo-core.md` (49 líneas, updated 2026-07-03) y `applications/echo-forge.md` (81 líneas, updated 2026-08-14); ambas previas a los freezes de contratos 2026-09-06/12 y sin el corte estable/volátil que exige el contrato para apps.
- Recursos Echo/Forge en `applications/`: 4 contratos frozen `Echo Forge — F-01…F-04 … Contract` (F-04 verificado 2026-09-12), 2 contratos V1 (`Echo SDK — Canonical Forge Integration and Analytics Contract V1`, `Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1`), 2 reviews Fable 5.1 (Durability, SDK Freeze), 3 auditorías datadas 2026-09-06 (`Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026`, `Independent Reality Check and Time-to-Value Plan`, `Evidencia de revisión independiente 2026-09-06`), y 2 notas `type: source` (Fuentes Echo / Echo Forge 2026-09-06).
- `applications/echo-core-changelog.md`: bitácora canónica de cambios de Echo Core.
- Sueltos en la raíz `30-resources/` (type: doc, fuera de todo dominio): `APIs.md`, `Diagrama visual — Entidades y persistencia de Echo Forge.md`, `GUIA_WORKER_TEMPORAL_MT5.md`, `LLM Wiki.md` (origen del patrón, enlazado por 00-RESOURCE-WIKI — proteger).
- `sqx/`: 4 archivos deep-research (gemini/gpt), colección sin `00-index.md`, no es dominio activo.
- `dashboards/echo-forge/Echo Forge WFM Dashboard.md` y `runbooks/` (15 curados: Echo/Forge en `symphony-zeus-troubleshooting`, `2026-07-25-fix-pack-for-gate-handoff-review` y `symphony/` con 8 runbooks de operación).
- `methodologies/sdd/sources/`: 3 notas `symphony-sdd-*` (adoption-plan, manual, runtime-governance).
- `knowledges/`, `vibe-coding/` y `agents/` (21 páginas curadas): sin páginas Echo específicas.
- `aranea/02-servicios/ml-ia`: menciona el host echo como infra; frontera infra/producto, no duplicar aquí el contenido de producto.

### Repo `xKoRx/echo` @ f7ddea18 (clean) — ~780 Markdown

- Fuente primaria de cartografía Echo: `v3/docs/` con `ARCHITECTURE.md`, `DATA_MODEL.md`, `FLOWS.md`, `OBSERVABILITY.md`, `TROUBLESHOOTING.md`, `AI_CONTEXT.md`, `the-lab-formulas.md`; subcarpetas `rfcs/` (44), `prompts/` (39), `old/` (22), `lab/` (2), `runbooks/` (1). Módulos con docs: `v3/front/` (233), `v3/sdk/` (9), `v3/core/`, `v3/gateway/`, `v3/hasura/`, `v3/kafka/`, `v3/bridge/`, `v3/clients/`.
- `docs/` (105): `00-contexto-general.md`, `01-arquitectura-y-roadmap.md`, `adr/001-005` (+README), `lab/00-08`, `rfcs/` (~50; incluye un RFC marcado `[DEPRECATED]`), `reports/` (i3, i5, i17), `sdd/` (plan de adopción 00-10), `runbooks/` (deploy_v3, escalation_prompt, specs), `PRD-copiador-V1.md`, `roadmap-copiear-v1.md`, `trade-copier-context.md`.
- `specs/` (73): 12 features `FEAT-*` en formato SDD (SPEC/PLAN/TASKS/VERIFICATION) + catálogo `specs/SPECS.md`; entre ellas `FEAT-FORGE-INGESTION-E1`, `FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2`, `FEAT-SDK-CANONICAL-CONTRACT`, `FEAT-CROSS-IDENTITY-BWC-E0` (los features de la rama activa).
- Legacy y proceso: `v2/` (119), `v1/` (7), `vibe-coding/` (34), `pipe/` (6); root con `README.md`, `QUICK_START.md`, `ESTRUCTURA_PROYECTO.md`, `SCAFFOLDING_SUMMARY.md`, `CONSTITUTION.md`, `AGENTS.md`, `CLAUDE.md`, 2 notas de fix/prompt sueltas.
- Scaffolding agéntico repo-owned: `.agents/` (43) — rules `00-*` a `11-*` + graphify, personalities y skills (sdd-* ×8, go-static-validation, anti-test-masking-guard, graphify).

### Repo `xKoRx/symphony` @ 9fad768c (dirty, NO tocar) — ~330 Markdown

- Fuente primaria de cartografía Forge/SQX: `sqx/` (`README.md`, `PRD.md`, `RFC.md`, examples etcd, `exporter-plugin/docs/ROLLBACK.md`) y `docs/` (56: `prd/` 26, `sdd/` 14, `rfc/` 7, `services/` 4, `deployment/` 1).
- `specs/` (147): ~30 features `FEAT-SQX-*` en formato SDD.
- `reports/echo-forge/` (7): stage reports 1–4, spec approval review, documentation alignment report, spec implementation audit.
- Root: `AGENTS.md`, `CLAUDE.md`, `CONSTITUTION.md`, `README.md`, `VERIFICATION.md`, `resumen_dev.md`, `pr_body.md`; proceso en `vibe-coding/` (31) e `internal/services/camunda/` (3).
- `.agents/` (65): rules `00-*` a `14-*`; 21 skills de las cuales sólo 3 están declaradas app-owned en el skills INDEX (`sqx-plugin-lifecycle`, `echo-forge-wfm-troubleshooting`, `sqx-temporal-failure-audit`); el resto son copias locales de skills federadas/core (`aranea-mcps-expert` con runbooks SSH/POSTGRES/MONGODB, sdd-* ×9, go-static-validation, anti-test-masking-guard, graphify) y otras propias (`echo-forge-testing`, `worker-ssh`, `worker-troubleshooting`, `sqx-deployer`, `sqx-watcher`, `sqx-instrument-sync`).

### Proyectos y entidad en el vault

- `10-projects/Echo/`: 13 notas de proyecto/iteración (E-01…E-05, F-01…F-04, Live Platform V1, Factory V2 Completion, Discovery y Estado, Auditoria POC, Cierre Lab, Reporte Lab) + `Echo — Producto Integrado` (root, owner: me) + planner KBC. Son historia de campaña/estado, no wiki canónica.
- `20-areas/Echo.md`: entidad de área, thin; enruta a proyectos, no a docs funcionales.

### Hallazgos transversales

- Los `AGENTS.md` de ambos repos referencian paths absolutos `file:///Users/rjara/...` (máquina distinta a la actual); deuda declarada para la fase I (agents-md-gardener), no corrijo nada aquí.
- Duplicación de skills: `xKoRx/symphony` replica localmente la skill federada `aranea-mcps-expert`, lo que contradice la regla de ownership del router aranea ("el vault cura, el repo owner posee lo suyo"); también el skills INDEX declara 3 app-owned cuando el repo tiene 21. Riesgo de context budget; fase J/I.
- Graphify CLI no estaba disponible en esta sesión; el inventario se hizo por búsqueda enfocada (find/grep sobre nombres y estructura, sin releer contenido funcional).

## Proposed Topology

Decisión estructural: crear el subdominio `30-resources/applications/echo/` (con su propio `00-index.md`, compartiendo `applications/log.md`) en lugar de un dominio top-level nuevo. Motivos: los contratos y páginas de Echo ya viven en `applications/`; el catálogo raíz de apps supera el umbral de escalado; el contrato de la wiki define exactamente este mecanismo (sub-índices jerárquicos, precedente `aranea/`); y evita duplicar el rol del catálogo de aplicaciones. La frontera Echo↔Forge es un recurso compartido dentro de ese subdominio, no un tercer producto ni un track paralelo. No se toca ninguna fila Meli del catálogo.

| # | Path objetivo (relativo a VAULT_ROOT) | Acción | Propósito | Fuentes de ingesta | Supersedes | Índice |
|---|---|---|---|---|---|---|
| 1 | `30-resources/applications/echo/00-index.md` | NEW | Sub-índice curado del subdominio Echo (una fila vigente por página) | este diseño; mantenido por ingest | — | `applications/00-index.md` deja una fila puntero |
| 2 | `30-resources/applications/echo/echo-core.md` | MOVE + UPDATE | Página canónica de Echo Core con corte estable/volátil y provenance | Fase B: `xKoRx/echo` `README.md`, `v3/docs/ARCHITECTURE.md`, `v3/docs/DATA_MODEL.md`, `v3/docs/FLOWS.md`, `v3/docs/OBSERVABILITY.md`, `docs/adr/`, `docs/00-contexto-general.md` | misma identidad, no copia | 1 |
| 3 | `30-resources/applications/echo/echo-forge.md` | MOVE + UPDATE | Página canónica de Echo Forge/SQX con corte estable/volátil | Fase C: `xKoRx/symphony` `README.md`, `sqx/PRD.md`, `sqx/README.md`, `docs/prd/` | misma identidad | 1 |
| 4 | `30-resources/applications/echo/echo-core-changelog.md` | MOVE | Bitácora de cambios de Echo Core | existente | — | 1 |
| 5–8 | `30-resources/applications/echo/Echo Forge — F-01…F-04 … Contract.md` (×4) | MOVE | Contratos frozen; source-of-record contractual, no se re-deriva | existentes (F-01…F-04) | — | 1 |
| 9 | `30-resources/applications/echo/Echo SDK — Canonical Forge Integration and Analytics Contract V1.md` | MOVE | Contrato compartido SDK/integración vigente | existente | — | 1 |
| 10 | `30-resources/applications/echo/Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1.md` | MOVE | Contrato de ingestión vigente lado Echo | existente | — | 1 |
| 11 | `30-resources/applications/echo/Echo — Forge Integration Boundary V1.md` (nombre provisional, final en fase F) | NEW | Página canónica de la frontera Forge→Echo: estado implementado de ingestion/handoff/identidad visto desde ambos repos; enlaza los contratos 5–10, no los repite | Fase D (frontera) + evidencia B/C; specs `FEAT-FORGE-INGESTION-E1` (echo), `FEAT-SQX-*` (symphony) | — | 1 |
| 12–13 | `30-resources/applications/echo/Echo — Fuentes de arquitectura y producto 2026-09-06.md` y `Echo Forge — Fuentes … 2026-09-06.md` | MOVE | Ledger de provenance histórico (type: source) | existentes; fase F agrega notas source nuevas por baseline (`f7ddea18`, `9fad768c`) | — | 1 |
| 14–18 | Las 3 auditorías datadas 2026-09-06 + 2 reviews Fable 5.1 (Durability, SDK Freeze) | MOVE, luego SUPERSEDE | Retención histórica; pierden autoridad vigente cuando las páginas 2/3/11 estén publicadas y verificadas | existentes | `superseded_by` → 2/3/11 | 1 (fila histórica) |
| 19 | `30-resources/applications/stager-app.md` | Sin cambio | App independiente del área Echo; queda en el catálogo raíz | — | — | catálogo raíz |

Sin cambio estructural (quedan donde están): `runbooks/` (incluido `symphony/` y los 2 sueltos de Echo Forge), `dashboards/echo-forge/`, `methodologies/sdd/sources/`, `LLM Wiki.md` (protegido, origen del patrón) y `00-RESOURCE-WIKI.md` (sólo recibe el impacto declarado de actualizar la lista de dominios/subdominios activos).

Candidatos a archivar (decide fase E con manifest, no en esta fase): `30-resources/sqx/` (4 deep-research), `GUIA_WORKER_TEMPORAL_MT5.md` (migrar contenido operativo a `runbooks/symphony/` o archivar), `Diagrama visual — Entidades y persistencia de Echo Forge.md` (absorber en `echo-forge.md` o archivar), `APIs.md` (clasificar).

Modelo de ownership por capa: la wiki del vault posee identidad, responsabilidad, contratos vigentes, frontera de integración, índices y provenance; los repos poseen el detalle técnico vivo y los artefactos SDD (`specs/`, `docs/adr/`, `v3/docs/`), referenciados siempre como `xKoRx/echo` o `xKoRx/symphony` + path relativo; los runbooks poseen la operación mecánica; los `AGENTS.md` de los repos serán routers (fase I); la entidad `20-areas/Echo.md` y los proyectos son routing/estado, no conocimiento funcional. Regla anti-duplicación dura: una página wiki no re-deriva contenido que vive en docs del repo; enlaza y sostiene sólo síntesis estable/volátil con provenance.

## Migration / Archive Plan

1. Fases B, C, D (cartógrafos): producir evidence packs dirigidos a las páginas 2, 3 y 11, citando `repo + path relativo` contra los baselines `f7ddea18` / `9fad768c`.
2. Fase E (legacy-doc-curator): manifest de clasificación sobre el inventario de este artifact — auditorías datadas (14–18) como SUPERSEDED-when-ready, sueltos de la raíz de `30-resources/` y `sqx/` como ARCHIVE/MERGE, docs legacy de repos (`v1/`, `v2/`, `v3/docs/old/`, rfcs viejos) marcados como evidencia histórica sin acción de escritura (el repositorio no se modifica en esta campaña salvo AGENTS.md en fase I).
3. Fase F (llm-wiki-documentarian): redactar las páginas objetivo con el contrato de la wiki (templates vía `materialize_schema_note.py`, frontmatter por contrato, corte estable/volátil, notas `type: source` nuevas por baseline), cerrar naming final de la página 11 y resolver el solapamiento 9/10/11.
4. Fase G (documentation-verifier): refutación adversarial contra los repos reconciliados; PASS requerido antes de publicar.
5. Fase H (vault-publisher-reconciler): publication manifest + reconciliación `documented_baseline..HEAD` revalidando sólo lo DOCUMENTATION_RELEVANT.
6. Parent: única ejecución de escritura en `30-resources/` (subdominio, movimientos, índices, supersedes, log), en el orden de Publication Safety.
7. Fases I (AGENTS.md), J (context budget) y K (hygiene) corren después de la publicación canonical.

## Publication Safety

- Orden obligatorio de publicación: (1) crear `applications/echo/00-index.md` y mover físicamente las páginas 2–13 y 14–18 en el mismo cambio; (2) actualizar `applications/00-index.md` en el mismo cambio: quitar las filas movidas y dejar una sola fila puntero al sub-índice (regla anti-drift: mover filas, nunca dos catálogos compitiendo); (3) actualizar 2 y 3 y crear 11; (4) sólo después de verification PASS, marcar 14–18 `status: superseded` con `superseded_by` bidireccional; (5) append a `applications/log.md` por operación; (6) reindex de Graphify al cierre del batch (es índice derivado, reconstruible); (7) impacto declarado en `00-RESOURCE-WIKI.md` (subdominio activo) y en `10-projects/Echo/Echo — Producto Integrado.md` si corresponde; (8) AGENTS.md de los repos recién en fase I, después de la wiki.
- Metadata: supersedes/superseded_by siempre en pares; una sola fila vigente por entidad en cada índice; prohibido crear copias `-v2`; páginas nuevas nacen de template vía script, nunca frontmatter canónico a mano; links por nombre canónico; sin paths de máquina ni absolutos.
- Riesgos principales: mover ~17 páginas rompe wikilinks si la actualización del índice raíz no va en el mismo cambio; el working tree dirty de `xKoRx/symphony` prohíbe cualquier operación git que no sea lectura; los repos avanzan en paralelo, así que toda afirmación publicada debe llevar su baseline y la fase H reconcilia antes de publicar.

## Conflicts / Unknowns

- Vault HEAD real (`09746b3`) está 2 commits adelantado al baseline declarado (`9a5299f`), tree clean: avance post-baseline, no contradicción de verdad; se registra para que la fase H reconcilie contra HEAD vigente.
- Graphify no disponible en esta sesión: el inventario se construyó por búsqueda enfocada; existe riesgo bajo de páginas Echo no detectadas en dominios que no apliqué al problema (`knowledges/`, `grids/`, `tools/`, `rio-atlas/`, `vibe-coding/`, `ideas/`, `meetings/`).
- Solapamiento entre los contratos 9/10, los F-0x y la futura página de frontera 11: riesgo real de duplicación; constraint declarada (contratos = source-of-record congelado, página 11 = estado implementado con links); la resolución fina es de la fase F.
- Naming final de la página 11 y de nuevas notas source: placeholder propuesto siguiendo el patrón vigente; la convención exacta se valida contra `90-system/convenciones.md` en fase F.
- No leí contenido funcional de specs/docs de los repos (fuera del alcance de esta fase); las fuentes listadas son candidatas, no verdad verificada.
- La lista de skills de `xKoRx/symphony/.agents/skills/` (21) vs el skills INDEX (3 app-owned) es una discrepancia observable; clasificar cada skill es trabajo de las fases I/J, no de esta.

## Handoff

- Fase B (echo cartographer): fuentes primarias listadas en Findings (`v3/docs/` raíz + `docs/adr/` + `docs/00-01`); página objetivo 2; baseline `f7ddea18`; citar siempre `xKoRx/echo` + path relativo.
- Fase C (forge cartographer): fuentes `sqx/` raíz + `docs/prd/` + `docs/services/`; página objetivo 3; baseline `9fad768c`; working tree dirty: sólo lectura, jamás checkout/reset/stash.
- Fase D (integration cartographer): partir de los contratos 5–10 y los specs `FEAT-FORGE-INGESTION-E1` / `FEAT-CONTROL-SAFETY-JOURNAL-RECOVERY-E2` (echo) y `FEAT-SQX-*` relevantes (symphony); página objetivo 11; la frontera es recurso compartido, no tercer producto.
- Fase E (legacy curator): clasificar sobre este inventario; candidatos archive ya señalados (sueltos de raíz, `sqx/`, auditorías datadas); nada DELETE sin manifest.
- Fase F (wiki documentarian): ejecutar la topología de Proposed Topology con el contrato de `agents-os-resource-wiki` (subdominio `applications/echo/`, notas source por baseline, naming final, ingest → índice → log).
- Fase G/H (verificación y publicación): usar Publication Safety como checklist de orden y los baselines de la sección Baseline (reconciliar contra HEAD vigente al publicar).
- Fase I (AGENTS.md gardener): además del diseño de routers, corregir los paths `file:///Users/rjara/...` de ambos AGENTS.md; el skills INDEX requiere reconciliar las 21 skills de symphony vs las 3 declaradas.
- Fase J (context budget): auditar duplicación (skills symphony vs vault; proyecto notes E-0x/F-0x vs wiki; `aranea/02-servicios/ml-ia` vs páginas de producto) y leakage MELI/ARANEA/DEFAULT sobre el corpus resultante.
