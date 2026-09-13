---
agent: legacy-doc-curator
role: Legacy Document Archaeology
task_id: KBC-E
status: COMPLETE
baseline: echo f7ddea18 (feature/e02-control-safety-journal-recovery) · symphony 9fad768c (feature/f04-magic-version-handoff, dirty=1 read-only) · vault a87aa62 (a87aa629db75fe3fc660031dc4962f5e077dc4fc)
inputs: 01-knowledge-architecture.md, 02-echo-cartography.md, 03-forge-cartography.md, 04-echo-forge-boundary.md, repos RO, vault 30-resources/40-archive
scope: clasificación y manifest de migración/deprecación, read-only
started_at: 2026-09-13T00:45:00-03:00
updated_at: 2026-09-13T01:20:00-03:00
---

# KBC-E — Legacy Document Audit

## Assignment

Arqueología documental sobre repos Echo (`xKoRx/echo`) y Echo Forge (`xKoRx/symphony`) y el vault: inventariar y clasificar cada doc relevante como CANONICAL / MERGE / SUPERSEDED / ARCHIVE / DELETE_CANDIDATE con justificación y evidencia contra la verdad implementada de las fases B/C/D, detectar duplicación, staleness y contradicciones, mapear inbound links antes de recomendar movimientos, y producir el manifest de migración/deprecación en este único archivo. READ-ONLY total salvo este artifact; cero borrados o movimientos; sin subagentes; proyectos agent son planning vivo y no se reclasifican.

## Baseline

- Vault Agents-OS HEAD al iniciar: `a87aa629db75fe3fc660031dc4962f5e077dc4fc` (a87aa62 "sync 00:32"), adelantado al baseline declarado del planner (9a5299f1) y al de Fase D (9d4b311) — drift esperado de bitácora, tree clean, no bloquea.
- `xKoRx/echo` @ `f7ddea18` verificado con `git rev-parse --short HEAD`; `xKoRx/symphony` @ `9fad768c` verificado igual. Ambos coinciden con el baseline de campaña. Ningún checkout/reset/stash; ningún test corrido.
- Verdades implementadas usadas como autoridad de clasificación: artifacts 02 (Echo: Flink StateFun no Temporal, receptor Forge completo pero ocioso, unavailableArtifactSource 503 fail-closed), 03 (Forge: pipeline termina en FinalistPromotion V2 + Apply, handoff sin cablear, única ingress FakeConsumerIngress), 04 (G1 sin transporte real, G3 sin backend de artefactos, G6 spec conceptual desactualizado; "cualquier afirmación de que Forge publica a Echo es hoy FALSA").
- Archivo `40-archive/` y `archive/`: sólo proyectos meli, agents-os y VIS; NADA de Echo/Forge archivado aún — no hay riesgo de clasificación duplicada con el archivo existente.

## Inventory & Classification

Tabla orientada a decisión; paths de vault relativos a VAULT_ROOT, paths de repo como `xKoRx/echo:...` / `xKoRx/symphony:...`. "in-situ" = no mover. Clase + acción (la acción la ejecuta el parent en Fase F/H, no yo).

### Vault — dominio `30-resources/applications/`

| Doc | Ubicación | Clase | Razón | Destino | Inbound links | Claims únicos |
|---|---|---|---|---|---|---|
| echo-core.md | applications/ | MERGE (MOVE+UPDATE) | Thin (49 líneas, updated 2026-07-03): sin corte estable/volátil, sin E-02/E-01, path máquina `/Users/rodrigojara/...` obsoleto | `applications/echo/echo-core.md` (topología #2), reescribir con evidencia Fase B | 00-index, echo-core-changelog, log.md, aranea/ARANEA_RUNBOOK_MIGRACION_HTTPS_TRAEFIK, 2 memory notes | ninguno que no viva en repo: descripción migrada textual a la página nueva |
| echo-forge.md | applications/ | MERGE (MOVE+UPDATE) | Thin/stale (updated 2026-08-14): afirma "entrega únicamente las estrategias aprobadas (finalistas) a Echo Core mediante su API" y "Echo Core: destino downstream" — CONTRADICHO por G1/G3 (Fase D) | `applications/echo/echo-forge.md` (#3), corregir claim de entrega y enlazar página frontera | 10 archivos (00-index, contratos, auditorías, proyectos, runbook triage) | distinción echo-forge vs SQX tool comercial + link [[strategyquant-x]] — migrar esa nota a la página nueva |
| echo-core-changelog.md | applications/ | CANONICAL (MOVE) | Bitácora de cambios vigente por identidad; se mueve intacta | `applications/echo/echo-core-changelog.md` (#4) | 7 archivos | ninguna (registro apendable) |
| F-01…F-04 Contracts (4) | applications/ | CANONICAL (MOVE) | Contratos frozen, source-of-record contractual, F-04 verificado 2026-09-12; no se re-deriva ni corrige en campaña | `applications/echo/Echo Forge — F-0x … Contract.md` (#5–8) | F-01:18, F-02:16, F-03:18, F-04:56 archivos (proyectos, log, memory, auditorías) | n/a — son la fuente |
| Echo SDK — Canonical Forge Integration and Analytics Contract V1 | applications/ | CANONICAL (MOVE) | Contrato compartido vigente; solapamiento con página frontera se resuelve en Fase F (11 enlaza, no repite) | `applications/echo/…V1.md` (#9) | 41 archivos | n/a — fuente |
| Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1 | applications/ | CANONICAL (MOVE) | Contrato de ingestión vigente lado Echo (authoridad del SPEC E-04) | `applications/echo/…V1.md` (#10) | 28 archivos | n/a — fuente |
| Echo — Fuentes de arquitectura y producto 2026-09-06 | applications/ | CANONICAL (MOVE) | Ledger de provenance histórico (type: source); Fase F agrega notas source nuevas por baseline f7ddea18/9fad768c, no las reemplaza | `applications/echo/…2026-09-06.md` (#12–13) | 9 archivos | provenance de echo master 04c16bd — vive sólo aquí |
| Echo Forge — Fuentes … 2026-09-06 | applications/ | CANONICAL (MOVE) | Ídem lado Symphony (source a10c26c) | `applications/echo/…2026-09-06.md` | 9 archivos | provenance Symphony a10c26c — vive sólo aquí |
| Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026 | applications/ | SUPERSEDED (MOVE + marcar) | Auditoría datada 2026-09-06: queda histórica cuando páginas 2/3/11 estén publicadas y verificadas (Fase G PASS); hasta entonces retiene autoridad descriptiva | `applications/echo/` con fila histórica; `superseded_by` → páginas 2/3/11 | 20 archivos (incluye los 2 contratos V1 y las otras auditorías) | 32 deudas + gaps + calendario/roadmap — migrar diff no cubierto por páginas canónicas ANTES de marcar superseded |
| Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan | applications/ | SUPERSEDED (MOVE + marcar) | Ídem: triage reachability e hitos congelados al 2026-09-06, desplazados por cartografía B/C/D verificada | `applications/echo/` histórico; superseded_by → 2/3/11 | 18 archivos | hitos y mínimo V1 definidos aquí — revisar contra roadmap vivo antes de archivar autoridad |
| Echo + Echo Forge — Evidencia de revisión independiente 2026-09-06 | applications/ | ARCHIVE (MOVE) | Fotografía física datada de binarios/DB/front al 2026-09-06; valor referencial, sin autoridad vigente | `applications/echo/` histórico | 13 archivos | límites de provenance declarados aquí — se conservan como evidencia |
| Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1 | applications/ | SUPERSEDED (MOVE + marcar) | Revisión de proceso (2026-09-07) que produjo el freeze; el freeze resultado vive en los contratos; pierde autoridad al publicarse páginas 2/3/11 | `applications/echo/` histórico; superseded_by → 9 + 11 | 14 archivos | matriz de correcciones C-1…C-7 aplicadas — sólo historia |
| Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1 | applications/ | SUPERSEDED (MOVE + marcar) | Ídem: FR-1…FR-5 ya materializados en el contrato frozen #9 | `applications/echo/` histórico; superseded_by → 9 | 21 archivos | matriz de identidad del freeze — sólo historia |
| stager-app.md | applications/ | CANONICAL in-situ | App independiente del área Echo; fuera del subdominio | ninguno | 1 (00-index) | — |
| 00-index.md (applications) | applications/ | CANONICAL in-situ | Índice raíz vigente; requiere update declarado (quitar filas movidas, fila puntero al sub-índice, mismo cambio) | update en el mismo cambio de movimientos | es el hub principal (apunta a todo lo anterior) | — |
| log.md (applications) | applications/ | CANONICAL in-situ | Bitácora compartida del dominio; el subdominio echo la comparte (topología) | append por operación | — | — |

### Vault — sueltos y colecciones `30-resources/`

| Doc | Ubicación | Clase | Razón | Destino | Inbound links | Claims únicos |
|---|---|---|---|---|---|---|
| GUIA_WORKER_TEMPORAL_MT5.md | raíz 30-resources | MERGE | Guía operativa auto-declarada "canónica legacy… requiere verificación antes de uso operativo" (created 2026-08-10, PRE-implementación del worker MT5 real); está fuera de dominio (type: doc sin índice) | contenido operativo → `runbooks/symphony/` (runbook nuevo) tras verificación contra `sqx/cmd/sqx-mt5-worker` + `adapters/mt5`; si el verifier la encuentra contradicha, ARCHIVE | 2 (journal log 2026-08-06, proyecto Echo Forge Etapa 6) | secuencia de implementación del task mt5 que precede al worker real — extraer sólo lo que el worker vigente confirma |
| Diagrama visual — Entidades y persistencia de Echo Forge | raíz 30-resources | ARCHIVE | Visual de referencia created 2026-08-10, anterior a migraciones 007–016 (stage_producer_outputs, finalist V2, forge campaign, magic/handoff): modelo de entidades desactualizado | `40-archive/` o fila histórica del subdominio; no absorber sin re-verificar | 1 (journal graphify lint; sin inbound real de contenido) | ninguna única: el modelo vigente vive en migraciones sqx/ |
| sqx/deep-research-gemini(.2).md, deep-research-gpt(.2).md (4) | 30-resources/sqx/ | ARCHIVE (carpeta completa) | Deep-research de fondo sin 00-index, no es dominio activo; el conocimiento operante vive en código (exporter-plugin Java) y contratos F | `40-archive/` la carpeta sqx/ completa | 1 (journal raw 2026-07-07) | detalle de API Java SQX Build 142 posiblemente no cubierto en ningún otro lugar — referenciar como fuente de fondo si Fase F lo necesita, no archivar conocimiento citable sin nota |
| APIs.md | raíz 30-resources | FUERA DE SCOPE (flag) | No es doc de conocimiento Echo: es una nota de credenciales API vivas (z.ai, minimax). No la clasifico ni muevo; declaro el hallazgo de seguridad al orchestrator | ninguna acción en campaña; decisión humana fuera de KBC | — | — |
| LLM Wiki.md | raíz 30-resources | CANONICAL in-situ | Origen del patrón, protegido por 00-RESOURCE-WIKI | ninguno | 1 (00-RESOURCE-WIKI) | — |
| runbooks/ (15 + symphony/ 8 + 00-index + log) | runbooks/ | CANONICAL in-situ | Runbooks curados poseen la operación mecánica; los 2 sueltos Echo Forge y symphony-zeus-troubleshooting quedan; GUIA_WORKER_TEMPORAL_MT5 es el único MERGE entrante potencial | ninguno (recibe merge #GUIA) | — | — |
| dashboards/echo-forge/, methodologies/sdd/sources/ | — | CANONICAL in-situ | Fuera de retrieval Echo product; sin cambio (topología Fase A) | ninguno | — | — |
| aranea/02-servicios/ml-ia (menciones echo-host) | aranea/ | CANONICAL in-situ | Frontera infra/producto: menciona el host echo como infra; no duplicar contenido de producto aquí | ninguno | — | — |

### Repos — `xKoRx/echo` @ f7ddea18 (regla de campaña: cero escritura en repos; clasificación = evidencia)

| Grupo | Ubicación | Clase | Razón / destino |
|---|---|---|---|
| README.md + v3/docs/ raíz (ARCHITECTURE, DATA_MODEL, FLOWS, OBSERVABILITY, TROUBLESHOOTING, AI_CONTEXT, the-lab-formulas) + v3/kafka/README | repo | CANONICAL in-situ | Detalle técnico vivo junto al código; la wiki enlaza (`xKoRx/echo: v3/docs/…`), nunca copia. Son las fuentes de ingesta de la página 2 |
| docs/adr/001–005 (+README) | repo | CANONICAL in-situ | Decisiones arquitecturales con estado propio (draft/aprobado/superseded); forman parte del artefacto repo; la wiki cita, no las duplica |
| specs/ (12 FEAT-* + SPECS.md) | repo | CANONICAL in-situ | Artefactos SDD con status model propio; SPECS.md citable como índice de estado por feature, no como fuente de comportamiento (Fase B) |
| docs/sdd/, docs/runbooks/, docs/architecture, docs/diagrams | repo | CANONICAL in-situ | Proceso y operación repo-owned |
| docs/00-contexto-general.md, 01-arquitectura-y-roadmap.md, 02/03 correcciones | repo | ARCHIVE (sin acción) | Narrativa histórica pre-v3; se conserva como evidencia histórica sin acción de escritura (decisión Fase A: el repo no se modifica en esta campaña) |
| docs/rfcs/ (~50, incl. 1 marcado [DEPRECATED]) | repo | ARCHIVE in-situ | RFC históricas de iteraciones 0–i17; excepción: las RFC citadas por código vivo (p.ej. RFC-007 news blackout, referenciada por NewsBlackoutEvaluator) quedan de facto CANONICAL in-situ |
| v1/, v2/, v3/docs/old/ (22), docs/lab/00-08, docs/v2/, pipe/, vibe-coding/ | repo | ARCHIVE in-situ | Generaciones legacy y proceso; evidencia histórica; go.work aún referencia v1/v2 (no tocar) |
| docs/PRD-copiador-V1.md, roadmap-copiear-v1.md, trade-copier-context.md, docs/reports/ (i3,i5,i17) | repo | ARCHIVE in-situ | Producto histórico (copiador) e informes datados |
| v3/core/cmd/echo-functions (código, no doc) | repo | señal ARCHIVE | Binario DEPRECATED compilable ("Use echo-core instead") — candidato a señal de legacy dentro del activo para handoff a fases I/K, no acción documental |

### Repos — `xKoRx/symphony` @ 9fad768c (dirty=1 intocado)

| Grupo | Ubicación | Clase | Razón / destino |
|---|---|---|---|
| sqx/README.md | repo | CANONICAL in-situ | Operación del cluster SQX (workers Zeus, hosts, IPs) junto al código; fuente de ingesta página 3 |
| docs/prd/SQX_Adaptive_E2E_Pipeline_PRD.md + _RFC.md | repo | CANONICAL in-situ | PRD canónico de Echo Forge declarado por su propio header (y ratificado por sqx/PRD.md) |
| specs/ FEAT-SQX-* (~30) | repo | CANONICAL in-situ | SDD vigente; excepciones abajo |
| specs/FEAT-SQX-ECHO-INGESTION/SPEC.md | repo | SUPERSEDED de facto | Contrato conceptual PRE-frozen (idempotencia wave_key+strategy_id+version, trade history inline, EchoStrategyRef) contradicho por el frozen S0 de 4 componentes y por el SPEC E-04 (G6 de Fase D); no fue marcado superseded ni reconciliado — la corrección es repo-side, fuera de esta campaña |
| specs/FEAT-SQX-ECHO-DEPLOYMENT-LINK/SPEC.md | repo | SUPERSEDED de facto | LinkDemoDeployment sin endpoint receptor ni contrato en Echo (G6b); NEED-INFO NI-DL-1 obsoleto |
| sqx/PRD.md | repo | SUPERSEDED (auto-declarado) | Su propio header dice "DOCUMENTO NO CANÓNICO / HISTÓRICO (sqx-flowkit, 2025)" y apunta al PRD canónico; correcto tal cual, sin acción |
| sqx/RFC.md, docs/rfc/ (7 modularización/observability) | repo | ARCHIVE in-situ | Historia de modularización; el estado actual vive en el código y README |
| docs/services/ (api-*, camunda, feed*, mde, tasks) | repo | ARCHIVE in-situ | Sistema legacy de feeds/Zeebe del módulo root, NO Forge (confirmado Fase C §8) |
| docs/services/sqx-mt5-worker-windows.md | repo | CANONICAL in-situ | Operación del worker MT5 vigente |
| reports/echo-forge/ (7 stage reports/audits/approval) | repo | ARCHIVE in-situ | Informes datados de stages 1–4; evidencia histórica de implementación |
| VERIFICATION.md (root) | repo | ARCHIVE in-situ | Verificación puntual de un fix (apply_selected_run fallback), no doc de sistema |
| docs/prd/sqx_stage_2.md, docs/prd/prompts.md, docs/deployment/stager-publisher-integration.md | repo | ARCHIVE / CANONICAL in-situ | sqx_stage_2 y prompts: histórico; stager-publisher: operativo de staging, vigente |
| docs/manifest.json, manifest copy.json, arqui.excalidraw, start-symphony-worker.sh, XAUUSD*.sqx | repo | ARCHIVE in-situ | Artefactos sueltos; "manifest copy.json" es duplicado evidente de manifest.json (candidato limpieza repo-side, fuera de campaña) |

## Contradictions Found

- Doc `applications/echo-forge.md` dice "entrega únicamente las estrategias aprobadas (finalistas) a Echo Core mediante su API" y "Echo Core: destino downstream de estrategias finalistas aprobadas"; la implementación (Fase D, G1+G3) dice que NO existe transporte Forge→Echo (cero callers de producción de BuildHandoffManifest/DeliverHandoff/SealStrategyVersion, cero cliente HTTP) y que el receptor Echo fallaría en artifact fetch (`unavailableArtifactSource` → 503). La fila de `applications/00-index.md` repite la contradicción ("entrega finalistas a Echo Core"). Evidencia: 04-echo-forge-boundary.md §Gaps G1/G3, §End-to-End Flow pasos 6–9.
- Doc `symphony:specs/FEAT-SQX-ECHO-INGESTION/SPEC.md` describe un contrato API conceptual (idempotencia de 3 componentes, payload con métricas/warnings/trade history inline, EchoStrategyRef, operación IngestTradeHistory separada) que difiere del contrato frozen implementado (idempotencia S0 de 4 componentes, HandoffEvidence sólo por refs, sin trade-history endpoint). Evidencia: Fase D CT-4 y GAP G6; el spec no fue superseded.
- Doc `30-resources/GUIA_WORKER_TEMPORAL_MT5.md` se declara "canónica legacy… requiere verificación" y describe la implementación del task mt5 como proyecto; la implementación real (Fase C: `sqx/cmd/sqx-mt5-worker`, `adapters/mt5/runner.go`, workflows MT5 dedicados) ya existe y puede diferir de la guía. Contradicción probable, resolución requiere verificación (no la afirmo como falsa sin leerla completa).
- Doc `30-resources/Diagrama visual — Entidades y persistencia de Echo Forge.md` representa el modelo de entidades al 2026-08-10; las migraciones 007–016 de sqx (stage_producer_outputs, finalist V2, forge campaign, magic/handoff) posteriormente ampliaron el modelo. Visual desactualizado en superficie, no en contradicción dura (puede seguir siendo válido para el núcleo).
- Doc `applications/echo-core.md` declara `path: /Users/rodrigojara/...` (máquina inexistente en este entorno); misma deuda en los AGENTS.md de ambos repos (ya declarada para Fase I). Regla de campaña: sin paths de máquina.
- Sin contradicciones detectadas entre los contratos frozen del vault y la implementación: F-01…F-04 y los V1 son consistentes con B/C/D (F-04 C4/C5 verificados 2026-09-12).

## Migration / Deprecation Manifest

Orden seguro por dependencias de links; ejecución es del parent (Fases F/H), nunca de este agente. Regla raíz: mover páginas y actualizar índices en el MISMO cambio (anti-drift), supersedes/superseded_by siempre en pares, una sola fila vigente por entidad, append a `applications/log.md` por operación.

1. Crear `30-resources/applications/echo/00-index.md` (sub-índice curado) — primero, porque las filas puntero lo necesitan.
2. En el mismo cambio: MOVE físico de las 17 páginas (echo-core, echo-forge, changelog, F-01…F-04, 2 contratos V1, 2 Fuentes, 3 auditorías, 2 Fable reviews) desde `applications/` hacia `applications/echo/`; los wikilinks son por nombre canónico y no se rompen (identidad de archivo preservada).
3. En el mismo cambio: update `applications/00-index.md` — quitar las filas movidas, dejar una sola fila puntero al sub-índice, corregir la fila echo-forge para eliminar el claim de entrega a Echo Core.
4. MERGE-UPDATE `applications/echo/echo-core.md` con evidencia de Fase B (arquitectura v3, StateFun no Temporal, E-02 auth, cuarentena+journalctl), corregir path de máquina, corte estable/volátil.
5. MERGE-UPDATE `applications/echo/echo-forge.md` con evidencia de Fase C; reemplazar el claim "entrega finalistas a Echo Core" por el estado real (pipeline termina en FinalistPromotion V2 + Apply; handoff sin cablear) y enlazar la página frontera.
6. Crear `applications/echo/Echo — Forge Integration Boundary V1.md` (página frontera #11) desde el evidence pack de Fase D; enlaza contratos #5–10, no los repite.
7. MERGE GUIA_WORKER_TEMPORAL_MT5: Fase F/verifier extrae lo que `sqx/cmd/sqx-mt5-worker` + `adapters/mt5` confirman → nuevo runbook en `runbooks/symphony/`; marcar la guía superseded con puntero; si el verifier la contradice entera, ARCHIVE directo. Único claim-unique a rescatar.
8. ARCHIVE: mover `30-resources/sqx/` (4 deep-research) a `40-archive/` (o fila histórica del sub-índice si Fase F cita la API Java SQX como fuente de fondo); mover `Diagrama visual — …Echo Forge.md` a `40-archive/` (inbound real: ninguno de contenido).
9. Sólo después de Fase G PASS (verification adversarial): marcar las 5 piezas históricas (3 auditorías + 2 Fable reviews) `status: superseded` con `superseded_by` → páginas 2/3/11/9; antes de marcar, confirmar que los claims únicos (32 deudas, hitos, matrices de corrección) están cubiertos o referenciados en las páginas canónicas.
10. Append a `applications/log.md` por cada operación; reindex Graphify al cierre del batch; impacto declarado en `00-RESOURCE-WIKI.md` (subdominio activo).
11. Repos: NINGUNA acción de escritura en esta campaña (decisión Fase A). Los SUPERSEDED de facto repo-side (FEAT-SQX-ECHO-INGESTION, FEAT-SQX-ECHO-DEPLOYMENT-LINK, sqx/PRD.md ya auto-marcado) quedan declarados aquí como deuda documental para una fase repo-side posterior (I/K), con el identificador exacto para el PR/issue.
12. DELETE_CANDIDATE: NINGUNO (default de campaña archive > delete). `APIs.md` se reporta como hallazgo de seguridad, no como candidato.

## Inbound Link Map

- Hub `applications/00-index.md` apunta a todas las 17 páginas a mover: es el único rompible si el update no va en el mismo cambio que el MOVE.
- Contratos F-0x: 56 (F-04) / 18 (F-01) / 16 (F-02) / 18 (F-03) archivos entrantes — principalmente notas de proyecto Echo Forge (F-01…F-04), log.md, memory notes de agentes y las auditorías; no se rompen por MOVE (links por nombre canónico).
- Contratos V1: SDK 41 entrantes, Ingestion/Live Authority 28 — misma naturaleza.
- Auditorías/Fable reviews (3+2): 20/18/13/14/21 entrantes — se citan mutuamente, más log.md, contratos V1 y proyectos; al quedar en el subdominio con fila histórica y superseded_by, los links siguen resolviendo.
- echo-forge.md: 10 entrantes (proyectos, runbook symphony-zeus-troubleshooting vía texto, memory notes); echo-core.md: 1 entrante directo (changelog) + índice; changelog: 7.
- GUIA_WORKER_TEMPORAL_MT5: 2 entrantes (journal log 2026-08-06, proyecto Echo Forge Etapa 6) — si se mueve a runbooks/symphony, actualizar esos 2.
- Diagrama visual: sin inbound real de contenido (sólo un journal lint) — archivable sin costo de links.
- sqx/deep-research: 1 entrante (journal raw 2026-07-07) — aceptable perder por archive.
- Fuera de 30-resources, las menciones `echo-core` en `80-agents/memory/internal/agent-memory/` (2026-07-16, 2026-09-06) son históricas y no requieren edición.

## Conflicts / Unknowns

- APIs.md contiene credenciales API aparentemente vivas en texto plano dentro del vault: fuera de mi scope de clasificación Echo, lo declaro al orchestrator/humano para decisión aparte (rotación/ubicación de secretos). No lo toqué más allá del head.
- Exactitud interna de GUIA_WORKER_TEMPORAL_MT5 no verificada línea a línea (leí head + contexto de creación): la decisión MERGE vs ARCHIVE queda gateada por el verifier en el paso 7 del manifest; no la declaro stale sin evidencia completa.
- Conteo de inbound links por grep de fragmentos de nombre: puede incluir autocitas y menciones textuales sin wikilink; sirve como mapa de riesgo, no como lista exacta de backlinks de Graphify (Graphify no disponible en esta sesión).
- Los documentos de proyecto Echo Forge (F-01…F-04 subproyectos) contienen historia de negociación de contratos; son planning vivo y NO los reclasifico; si Fase F necesita el trail, vive en ellos y en los change logs de `applications/log.md`.
- deep-research de `sqx/` documentan la API Java de SQX Build 142 (CustomAnalysis/exporters) con detalle que el repo sólo muestra en código: si Fase F cita ese detalle, archivar la carpeta entera pierde la fuente — mitigación: citar como fuente histórica desde la página 3 antes de mover.
- `docs/rfcs/` de echo contiene RFCs citadas por código vivo (RFC-007 news blackout); mi clasificación por grupo (ARCHIVE in-situ) no debe interpretarse como que esas RFC específicas son obsoletas.

## Recommendations

- Ejecutar el manifest en un solo cambio de publicación (pasos 1–3) para eliminar el riesgo de doble catálogo; los pasos 4–6 son ediciones de contenido; el paso 9 es el único que debe esperar verification.
- Corregir el claim "Forge entrega a Echo Core" en TODO lugar donde aparezca (echo-forge.md, fila del 00-index, y auditarel runbook symphony-zeus-troubleshooting durante la publicación): es la contradicción mayor de la campaña.
- Para Fase F: cerrar naming final de la página frontera y el solapamiento contratos V1 (#9/#10) vs frontera (#11) con la constraint ya declarada (contratos = source-of-record, frontera = estado implementado con links).
- Para el orchestrator/humano: decidir tratamiento de `APIs.md` (secreto expuesto en vault, fuera de KBC) y, eventualmente, fase repo-side para los 2 specs Forge SUPERSEDED de facto y el `manifest copy.json` duplicado en symphony.

## Handoff

- A wiki documentarian (Fase F): topología destino = `30-resources/applications/echo/` con las 18 páginas de la tabla; fuentes de ingesta = artifacts B/C/D + docs CANONICAL in-situ listados (nunca copiar contenido de repo, sólo sintetizar con provenance); las notas type: source nuevas deben llevar baseline `echo f7ddea18` / `symphony 9fad768c`.
- A publisher reconciler (Fase H): el orden de Publication Safety del artifact 01 sigue vigente y este manifest lo instancia en 12 pasos; el único gate duro antes del paso 9 es Fase G PASS; repos quedan byte-idénticos (symphony con su dirty file intacto).
- A documentation-verifier (Fase G): los 2 claims a refutar con prioridad son (1) el estado real de la frontera Forge→Echo según G1–G6 y (2) la vigencia de GUIA_WORKER_TEMPORAL_MT5 contra el worker MT5 implementado.
- Ningún archivo fuera de este artifact fue creado, modificado o movido; repos y vault leídos en modo estrictamente read-only.
