---
type: index
schema_version: 1
status: active
created: 2026-06-28
updated: 2026-09-11
entities:
  - "[[AGENTS OS]]"
  - "[[agents-os]]"
related:
  - "[[agents-os-bootstrap]]"
next_audit: 2026-08-25
tags:
  - kind/index
  - tech/agents-os
  - tech/skills
---

# Catálogo de Habilidades Operativas (Skills)

Este índice detalla las habilidades configuradas para los agentes en el Agent Memory System (AGENTS OS).

---

## 📊 De un vistazo

- **Cobertura:** core AGENTS OS, skills portables y referencias app-owned.
- **Auditoría siguiente:** 2026-08-25.

## 📂 Catálogo

## 🛠️ Catálogo de Skills

| Carpeta / ID | Descripción | Uso Recomendado |
|---|---|---|
| [[80-agents/skills/agents-os-bootstrap/SKILL.md|agents-os-bootstrap]] | Clasifica cold/warm/cambio de entidad y carga el contexto mínimo correspondiente. | Ejecutar una vez en cold start; en warm reutilizar y recuperar sólo el delta. |
| [[80-agents/skills/agents-os-context-retrieval/SKILL.md|agents-os-context-retrieval]] | Orquesta la recuperación enfocada de contexto mediante Graphify y filtros. | Al buscar contexto de entidades. |
| [[80-agents/skills/agents-os-session-close/SKILL.md|agents-os-session-close]] | Ejecuta el flujo estricto de cierre de sesión (L0 raw, L1 summaries, etc.). | Solo cuando el usuario pida explícitamente cerrar sesión. |
| [[80-agents/skills/agents-os-session-feedback/SKILL.md|agents-os-session-feedback]] | Escribe notas de observación del agente sobre dolores o mejoras operativas. | Al cerrar la sesión. |
| [[80-agents/skills/agents-os-memory-distillation/SKILL.md|agents-os-memory-distillation]] | Promueve y destila conocimientos hacia ADRs, known errors o runbooks. | Para actualizar la memoria persistente. |
| [[80-agents/skills/agents-os-entity-lifecycle/SKILL.md|agents-os-entity-lifecycle]] | Gestiona la creación de entidades de Sistema 2 asegurando uso de templates. | Al crear proyectos, áreas o apps. |
| [[80-agents/skills/agents-os-entity-update/SKILL.md|agents-os-entity-update]] | Actualiza la información y el estado en los archivos Markdown canónicos. | Al cambiar el estado de un proyecto/app. |
| [[80-agents/skills/agents-os-agent-project-workflow/SKILL.md|agents-os-agent-project-workflow]] | Define cómo ejecutar un proyecto de agente: la nota es el planificador único, y gestiona el ciclo de la tarea puente (WIP→Review→Done humano, o vuelta a WIP si el humano rechaza). | Al iniciar, retomar, avanzar o cerrar trabajo sobre un proyecto `owner: agent`. |
| [[80-agents/skills/agents-os-agent-run-register/SKILL.md|agents-os-agent-run-register]] | Registra una ejecución de código atribuible por superficie×modelo con evidencia, outcome, verificación y rework. | Al completar o pausar un segmento material de coding/debug/review/testing, o durante cierre explícito si falta el registro. |
| [[80-agents/skills/agents-os-conflict-resolution/SKILL.md|agents-os-conflict-resolution]] | Resuelve contradicciones de información entre notas y memoria. | Al detectar discrepancias de verdad. |
| [[80-agents/skills/agents-os-graphify-maintenance/SKILL.md|agents-os-graphify-maintenance]] | Ejecuta reindexaciones y mantenimiento del grafo de conocimiento. | Al modificar archivos del vault. |
| [[80-agents/skills/agents-os-graphify-install/SKILL.md|agents-os-graphify-install]] | Instala/repara `graphify-obsidian` por máquina; binario e índice quedan fuera del vault y las queries hacen auto-refresh local. | En máquina nueva o cuando falta/está roto `graphify-obsidian`. |
| [[80-agents/skills/agents-os-install/SKILL.md|agents-os-install]] | Instala, personaliza y valida AGENTS OS, incluyendo perfil, workspaces, aplicaciones, Codex, Claude, Graphify e higiene. | Onboarding de una persona o reparación de instalación. |
| [[80-agents/skills/agents-os-requirement-interview/SKILL.md|agents-os-requirement-interview]] | Cierra la brecha de contexto de una solicitud ambigua vía entrevista dirigida por evidencia: mapa de decisiones, filtro de valor por pregunta y ledger de supuestos. | Antes de planificar o implementar algo no trivial, o cuando el usuario pide una entrevista. |
| [[80-agents/skills/agents-os-implementation-planning/SKILL.md|agents-os-implementation-planning]] | Convierte una iteración compleja en un proyecto por fases, con gates y continuidad verificable. | Al planificar una implementación estructural o multi-etapa. |
| [[80-agents/skills/agents-os-project-impact-brief/SKILL.md|agents-os-project-impact-brief]] | Audita una propuesta contra la implementación vigente y entrega al owner sólo el impacto crítico para decidir con seguridad. | Al validar implementabilidad, impacto, migración, riesgos y go/no-go de un proyecto. |
| [[80-agents/skills/agents-os-kaizen-memory/SKILL.md|agents-os-kaizen-memory]] | Audita y analiza feedbacks agregados para proponer optimizaciones L3. | Periódico o a demanda del usuario. |
| [[80-agents/skills/agents-os-hygiene-cycle/SKILL.md|agents-os-hygiene-cycle]] | Orquesta higiene, Kaizen incremental, promociones, changelog compartible y reindex de Graphify. | Semanal/mensual, por acumulación de feedback o antes de compartir mejoras. |
| [[80-agents/skills/agents-os-behavior-config/SKILL.md|agents-os-behavior-config]] | Configura preferencias de comportamiento del agente. | A demanda del usuario. |
| [[80-agents/skills/agents-os-note-capture/SKILL.md|agents-os-note-capture]] | Captura y normaliza notas rápidas. | Al registrar ideas o apuntes. |
| [[80-agents/skills/agents-os-resource-wiki/SKILL.md|agents-os-resource-wiki]] | Mantiene `30-resources/` como wiki compilada (ingest/query/lint); páginas canónicas + `00-index.md` + `log.md`. | Al ingerir/consultar/mantener recursos. Parte mecánica en runbook `resource-wiki-lint-reindex`. |
| [[80-agents/skills/agents-os-skill-authoring/SKILL.md|agents-os-skill-authoring]] | Autoría/refino de skills según el contrato + principios (lean agent-facing, una fuente por hecho, explicación rica en doc humano aparte). | Al crear/refinar una skill o clasificar skill vs runbook vs memoria. |
| [[80-agents/skills/signals-code-review/SKILL.md|signals-code-review]] | Revisa branches y PRs de Rodrigo en Meli/Signals con Zord, specs, descripción del PR y análisis de impacto transversal sobre documentación y código owner de RIO. | Al hacer code review o validar afectaciones cross-app en RIO; ejecución mecánica en el runbook homónimo. |
| [[80-agents/skills/human-first-technical-writing/SKILL.md|human-first-technical-writing]] | Reduce la carga cognitiva y construye progresivamente el modelo mental del lector mediante una narrativa técnica causal. | Al crear o corregir PRs, specs, reportes, propuestas, incidentes o guías destinadas a personas. |
| [[80-agents/skills/pr-description/SKILL.md|pr-description]] | Produce descripciones de Pull Request con evidencia real y las materializa como recurso del proyecto en el vault. | Al preparar la descripción de un PR sin crear ni publicar el PR. |
| [[80-agents/skills/signals-func-spec-authoring/SKILL.md|signals-func-spec-authoring]] | Escribe y revisa specs FUNCIONALES de Signals/Ads en Spellbook, con las convenciones del equipo. La creación se hace con Grimoire. | Al redactar o revisar un spec funcional de Signals, Ads, RIO o playmaker. |
| [[80-agents/skills/signals-tech-spec-authoring/SKILL.md|signals-tech-spec-authoring]] | Escribe, corrige y revisa specs TÉCNICAS de Signals/Ads y design docs de backend RIO: DD-N, diagrama con marcadores de cambio, calibración de largo. | Al redactar, arreglar o acortar la spec técnica que deriva de un funcional. |
| [[80-agents/skills/agents-os-relation-maintenance/SKILL.md|agents-os-relation-maintenance]] | Mantiene relaciones estructurales y links en el vault. | Mantenimiento periódico. |
| [[80-agents/skills/agents-os-retrofit-raw-session/SKILL.md|agents-os-retrofit-raw-session]] | Procesa sesiones raw pasadas pendientes de indexar. | Mantenimiento de memoria. |
| [[80-agents/skills/agents-os-tagging-system/SKILL.md|agents-os-tagging-system]] | Audita y normaliza etiquetas/tags del vault. | Higiene del vault. |
| [[80-agents/skills/agents-os-vault-refactor/SKILL.md|agents-os-vault-refactor]] | Orquesta reestructuraciones y refactorizaciones de carpetas. | Tareas complejas de ordenación. |
| [[80-agents/skills/agents-os-hygiene-review/SKILL.md|agents-os-hygiene-review]] | Revisa el estado de salud de notas y archivos del vault. | Higiene periódica. |
| [[80-agents/skills/agents-os-doctor/SKILL.md|agents-os-doctor]] | Lint ejecutable de AGENTS OS: paths, closed club `always`, refs de skills, secretos internos, peso del startup, índice y proyectos. Propone reparaciones; no las aplica sin autorización. | Tras una iteración estructural, cuando algo se sienta raro, o periódico. |
| [[80-agents/skills/e2e-gated-validation/SKILL.md|e2e-gated-validation]] | Orquesta validaciones E2E como secuencia de gates con evidencia y criterios PASS/FAIL; no avanza al gate N+1 sin veredicto del anterior. | Al ejecutar E2E, golden runs o certificaciones físicas (Echo Forge/Symphony y transferible). |
| [[80-agents/skills/release-certification/SKILL.md|release-certification]] | Certifica que release/binario corresponde al source autorizado: baseline, blob equality, carriers, vcs.revision, pins de SDK, SHA256. | Antes de certificar/probar sobre una release; gates de baseline/source. |
| [[80-agents/skills/deployment-proof/SKILL.md|deployment-proof]] | Demuestra por jerarquía de evidencia (directa o compuesta) que el runtime ejecuta la release nueva, sin aceptar exit 0 como prueba. | Tras cualquier deploy cuyo runtime deba participar en una validación. |
| [[80-agents/skills/readonly-production-probe/SKILL.md|readonly-production-probe]] | Crea probes temporales read-only contra sistemas reales usando el DI/config real, con cleanup obligatorio. | Para inspección física de producción sin modificar estado. |
| [[80-agents/skills/distributed-incident-triage/SKILL.md|distributed-incident-triage]] | Triage forense multi-subsistema: timeline común, side effects, primer punto de divergencia y clasificación causal producto/infra/skew. | Ante fallos que cruzan orquestador/object store/DBs/logs. |
| [[80-agents/skills/evidence-channel-discovery/SKILL.md|evidence-channel-discovery]] | Descubre y persiste qué canales de evidencia existen realmente por pregunta, con autoridad y limitaciones. | Al empezar en un sistema desconocido o tras encontrar canales muertos. |
| [[80-agents/skills/write-once-conflict-triage/SKILL.md|write-once-conflict-triage]] | Investiga conflictos de inmutabilidad identificando writers/bytes/timeline y clasificando duplicate/race/stale/contract-defect. | Ante CONTRACT_CONFLICT, checksum mismatch o violaciones de idempotencia. |
| [[80-agents/skills/operational-healthcheck-policy/SKILL.md|operational-healthcheck-policy]] | Diferencia cuándo validar manualmente componentes vigilables del vault (sync, backups, servicios) y cuándo confiar en la automatización. | Ante una señal concreta de problema o antes de una acción masiva sobre el vault. |

## 🌐 Registro federado (fuentes fuera del core)

El registry **enlaza, no copia** (D6/D14). El core AGENTS OS vive arriba en
`80-agents/skills/`. Las skills transversales viven curadas en el vault bajo
`30-resources/agents/skills/`; las de una aplicación viven en el repo owner.

### Transversales — `30-resources/agents/skills/`

| Carpeta / ID | Descripción | Uso Recomendado |
|---|---|---|
| [[30-resources/agents/skills/sync-local-branch/SKILL.md|sync-local-branch]] | Sincroniza ramas Git exclusivamente locales con pull literal, merge, resolución conservadora, commit y push. | Dev-workflow genérico: sincronizar una rama con develop/master u otra local. |
| [[30-resources/agents/skills/fury-lib-consumer-deploy/SKILL.md|fury-lib-consumer-deploy]] | Publica versiones test de librerías Java con Fury e importa esas versiones en apps consumidoras. | Metodología Fury cross-app: `java-polycard-sdk -> search-middleware`, `vis-octopus-lib -> vpp-backend`. |
| [[30-resources/agents/skills/sdd-workflow/SKILL.md|sdd-workflow]] | Clasifica y ejecuta fases SDD sin mezclar specification, plan, tasks, implementation y verification. | Features/cambios no triviales, backfill brownfield, artefactos SDD y handoffs. Metodología en `30-resources/methodologies/sdd/`. |

### App-owned — repo `xKoRx/symphony` (Echo Forge / SQX)

Ownership real = repo de la app. `xKoRx/symphony` usa `.agents/skills/` como home canónica con discovery nativo en Cursor y Antigravity. El registry enlaza por `repo + path relativo`; nunca copia ni persiste un path absoluto de máquina (constitución, invariante 11).

| Carpeta / ID | Descripción | Estado / ubicación |
|---|---|---|
| `xKoRx/symphony` → `.agents/skills/sqx-plugin-lifecycle/SKILL.md` | Modifica, compila, despliega y valida plugins Java de SQX con classpath efectivo, build contra SDK real, backup, canary y rollback. | ✅ **migrada** (piloto, 2026-08-07) al repo owner; ya no vive en el vault |
| `xKoRx/symphony` → `.agents/skills/echo-forge-wfm-troubleshooting/SKILL.md` | Troubleshooting de validación de robustez Walk-Forward (WFM). | ✅ migrada al repo owner; fuente única |
| `xKoRx/symphony` → `.agents/skills/sqx-temporal-failure-audit/SKILL.md` | Audita una ejecución fallida de un workflow Temporal del SQX Worker recabando evidencia agnóstica sin proponer fix. | ✅ migrada al repo owner; fuente única junto a su README humana |
