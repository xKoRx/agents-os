---
type: index
schema_version: 1
status: active
icon: 🧭
slug: "skills-index"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-06-28
updated: 2026-09-12
reviewed: 2026-09-12
aliases:
  - "skills index"
  - "catálogo de skills"
  - "registro de habilidades"
cssclasses:
  - wide
tags:
  - kind/index
  - tech/agents-os
  - tech/skills
---

# 🧭 AGENTS OS Skills — Índice

> [!info] Registro de habilidades en formato wiki
> Este índice es el catálogo curado de las skills. El core (`80-agents/skills/`) contiene sólo comportamientos de AGENTS OS; las skills de dominio y transversales viven curadas en `30-resources/agents/skills/` y las app-owned en el repo owner. Se carga en el cold start del `agents-os-bootstrap` para que el agente sepa qué tiene disponible. Reglas de la wiki: [[30-resources/00-RESOURCE-WIKI|Resource Wiki]].

## 📊 De un vistazo

- **Core AGENTS OS:** 28 skills de comportamiento del sistema.
- **Federadas (vault):** 19 skills curadas en `30-resources/agents/skills/`.
- **App-owned:** 3 skills en repos dueño.
- **Regla de lugar:** una skill vive en el core sólo si cambia el comportamiento de AGENTS OS itself; todo lo demás vive federado y se enlaza, no se copia.

## 🛠️ Catálogo core — comportamientos de AGENTS OS

| Skill | Una línea | Cuándo cargar |
|---|---|---|
| [[80-agents/skills/agents-os-bootstrap/SKILL.md|agents-os-bootstrap]] | Clasifica cold/warm/cambio de entidad y carga el contexto mínimo correspondiente. | Una vez en cold start; en warm reutilizar y recuperar sólo el delta. |
| [[80-agents/skills/agents-os-context-retrieval/SKILL.md|agents-os-context-retrieval]] | Orquesta la recuperación enfocada de contexto mediante Graphify y filtros. | Al buscar contexto de entidades. |
| [[80-agents/skills/agents-os-session-close/SKILL.md|agents-os-session-close]] | Ejecuta el flujo estricto de cierre de sesión (L0 raw, L1 summaries, etc.). | Sólo cuando el usuario pida explícitamente cerrar sesión. |
| [[80-agents/skills/agents-os-session-feedback/SKILL.md|agents-os-session-feedback]] | Escribe notas de observación del agente sobre dolores o mejoras operativas. | Al cerrar la sesión. |
| [[80-agents/skills/agents-os-memory-distillation/SKILL.md|agents-os-memory-distillation]] | Promueve y destila conocimientos hacia ADRs, known errors o runbooks. | Para actualizar la memoria persistente. |
| [[80-agents/skills/agents-os-entity-lifecycle/SKILL.md|agents-os-entity-lifecycle]] | Gestiona la creación de entidades de Sistema 2 asegurando uso de templates. | Al crear proyectos, áreas o apps. |
| [[80-agents/skills/agents-os-entity-update/SKILL.md|agents-os-entity-update]] | Actualiza la información y el estado en los archivos Markdown canónicos. | Al cambiar el estado de un proyecto/app. |
| [[80-agents/skills/agents-os-agent-project-workflow/SKILL.md|agents-os-agent-project-workflow]] | Define cómo ejecutar un proyecto de agente: la nota es el planificador único, y gestiona el ciclo de la tarea puente (WIP→Review→Done humano, o vuelta a WIP si el humano rechaza). | Al iniciar, retomar, avanzar o cerrar trabajo sobre un proyecto `owner: agent`. |
| [[80-agents/skills/agents-os-agent-run-register/SKILL.md|agents-os-agent-run-register]] | Registra una ejecución de código atribuible por superficie×modelo con evidencia, outcome, verificación y rework. | Al completar o pausar un segmento material de coding/debug/review/testing. |
| [[80-agents/skills/agents-os-conflict-resolution/SKILL.md|agents-os-conflict-resolution]] | Resuelve contradicciones de información entre notas y memoria. | Al detectar discrepancias de verdad. |
| [[80-agents/skills/agents-os-graphify-maintenance/SKILL.md|agents-os-graphify-maintenance]] | Contrato y diagnóstico del índice Graphify; las queries auto-refrescan y el `update` explícito es sólo mantenimiento. | Ante índice stale, update bloqueado o dudas del contrato. |
| [[80-agents/skills/agents-os-graphify-install/SKILL.md|agents-os-graphify-install]] | Instala/repara `graphify-obsidian` por máquina; binario e índice quedan fuera del vault. | En máquina nueva o cuando falta/está roto `graphify-obsidian`. |
| [[80-agents/skills/agents-os-install/SKILL.md|agents-os-install]] | Instala, personaliza y valida AGENTS OS, incluyendo perfil, workspaces, aplicaciones, Codex, Claude, Graphify e higiene. | Onboarding de una persona o reparación de instalación. |
| [[80-agents/skills/agents-os-requirement-interview/SKILL.md|agents-os-requirement-interview]] | Cierra la brecha de contexto de una solicitud ambigua vía entrevista dirigida por evidencia. | Antes de planificar o implementar algo no trivial. |
| [[80-agents/skills/agents-os-implementation-planning/SKILL.md|agents-os-implementation-planning]] | Convierte una iteración compleja en un proyecto por fases, con gates y continuidad verificable. | Al planificar una implementación estructural o multi-etapa. |
| [[80-agents/skills/agents-os-project-impact-brief/SKILL.md|agents-os-project-impact-brief]] | Audita una propuesta contra la implementación vigente y entrega sólo el impacto crítico para decidir. | Al validar implementabilidad, impacto y go/no-go de un proyecto. |
| [[80-agents/skills/agents-os-kaizen-memory/SKILL.md|agents-os-kaizen-memory]] | Audita y analiza feedbacks agregados para proponer optimizaciones L3. | Periódico o a demanda del usuario. |
| [[80-agents/skills/agents-os-hygiene-cycle/SKILL.md|agents-os-hygiene-cycle]] | Orquesta higiene, Kaizen incremental, promociones, changelog compartible y mantenimiento de Graphify. | Semanal/mensual, por acumulación de feedback o antes de compartir mejoras. |
| [[80-agents/skills/agents-os-hygiene-review/SKILL.md|agents-os-hygiene-review]] | Revisa el estado de salud de notas y archivos del vault. | Higiene periódica. |
| [[80-agents/skills/agents-os-behavior-config/SKILL.md|agents-os-behavior-config]] | Configura preferencias de comportamiento del agente. | A demanda del usuario. |
| [[80-agents/skills/agents-os-note-capture/SKILL.md|agents-os-note-capture]] | Captura y normaliza notas rápidas. | Al registrar ideas o apuntes. |
| [[80-agents/skills/agents-os-resource-wiki/SKILL.md|agents-os-resource-wiki]] | Mantiene `30-resources/` como wiki compilada (ingest/query/lint); páginas canónicas + `00-index.md` + `log.md`. | Al ingerir/consultar/mantener recursos. |
| [[80-agents/skills/agents-os-skill-authoring/SKILL.md|agents-os-skill-authoring]] | Autoría/refino de skills según el contrato (lean agent-facing, una fuente por hecho). | Al crear/refinar una skill o clasificar skill vs runbook vs memoria. |
| [[80-agents/skills/agents-os-relation-maintenance/SKILL.md|agents-os-relation-maintenance]] | Mantiene relaciones estructurales y links en el vault. | Mantenimiento periódico. |
| [[80-agents/skills/agents-os-retrofit-raw-session/SKILL.md|agents-os-retrofit-raw-session]] | Procesa sesiones raw pasadas pendientes de indexar. | Mantenimiento de memoria. |
| [[80-agents/skills/agents-os-tagging-system/SKILL.md|agents-os-tagging-system]] | Audita y normaliza etiquetas/tags del vault. | Higiene del vault. |
| [[80-agents/skills/agents-os-vault-refactor/SKILL.md|agents-os-vault-refactor]] | Orquesta reestructuraciones y refactorizaciones de carpetas. | Tareas complejas de ordenación. |
| [[80-agents/skills/agents-os-doctor/SKILL.md|agents-os-doctor]] | Lint ejecutable de AGENTS OS: paths, closed club `always`, refs de skills, secretos internos, peso del startup, índice y proyectos. | Tras una iteración estructural, cuando algo se sienta raro, o periódico. |

## 🌐 Registro federado (enlaza, no copia)

Las skills de dominio y transversales viven curadas en el vault bajo
`30-resources/agents/skills/` con su [[30-resources/agents/00-index|índice wiki de dominio]]; las de una aplicación viven en el repo owner. El enrutamiento por dominio lo poseen [[30-resources/agents/skills/meli-agent-dev/SKILL.md|meli-agent-dev]] y [[30-resources/agents/skills/aranea-agent-dev/SKILL.md|aranea-agent-dev]].

### Dominio y transversales — `30-resources/agents/skills/`

| Skill | Una línea | Dominio / uso |
|---|---|---|
| [[30-resources/agents/skills/meli-agent-dev/SKILL.md|meli-agent-dev]] | Router del dominio Meli: boundary, preferencias scoped y skill especializada por tarea. | Todo trabajo corporativo Meli. Excluye MCPs `aranea-*`. |
| [[30-resources/agents/skills/aranea-agent-dev/SKILL.md|aranea-agent-dev]] | Router del dominio Aranea (homelab): boundary, preferencias scoped y puerta única del acceso MCP. | Todo trabajo homelab Echo/Forge/mcps. Excluye Meli/corporativo. |
| [[30-resources/agents/skills/aranea-mcps-expert/SKILL.md|aranea-mcps-expert]] | Selecciona y gobierna capabilities MCP de Aranea (ambiente antes que autoridad) bajo `aranea-agent-dev`. | Sólo dominio Aranea. **MUST NOT** para MELI/corporativo. |
| [[30-resources/agents/skills/signals-code-review/SKILL.md|signals-code-review]] | Revisa branches y PRs exclusivamente Meli con Zord; en Signals/RIO agrega el revisor `rjara-rio-impact`. | Vía `meli-agent-dev`. Fuera de Meli termina sin ejecutar Zord. |
| [[30-resources/agents/skills/signals-func-spec-authoring/SKILL.md|signals-func-spec-authoring]] | Escribe y revisa specs FUNCIONALES de Signals/Ads en Spellbook. | Vía `meli-agent-dev`. |
| [[30-resources/agents/skills/signals-tech-spec-authoring/SKILL.md|signals-tech-spec-authoring]] | Escribe, corrige y revisa specs TÉCNICAS de Signals/Ads y design docs backend RIO. | Vía `meli-agent-dev`. |
| [[30-resources/agents/skills/pr-description/SKILL.md|pr-description]] | Produce descripciones de PR con evidencia real y las materializa como recurso del proyecto. | Vía `meli-agent-dev` u obra propia del vault. |
| [[30-resources/agents/skills/human-first-technical-writing/SKILL.md|human-first-technical-writing]] | Reduce la carga cognitiva del lector mediante narrativa técnica causal. | Transversal: PRs, specs, reportes, incidentes, guías. |
| [[30-resources/agents/skills/fury-lib-consumer-deploy/SKILL.md|fury-lib-consumer-deploy]] | Publica versiones test de librerías Java con Fury y las importa en apps consumidoras. | Vía `meli-agent-dev`. |
| [[30-resources/agents/skills/sync-local-branch/SKILL.md|sync-local-branch]] | Sincroniza ramas Git exclusivamente locales con pull literal, merge conservador, commit y push. | Dev-workflow genérico. |
| [[30-resources/agents/skills/sdd-workflow/SKILL.md|sdd-workflow]] | Clasifica y ejecuta fases SDD sin mezclar specification, plan, tasks, implementation y verification. | Features/cambios no triviales; metodología en `30-resources/methodologies/sdd/`. |
| [[30-resources/agents/skills/e2e-gated-validation/SKILL.md|e2e-gated-validation]] | Orquesta validaciones E2E como secuencia de gates con evidencia y criterios PASS/FAIL. | E2E, golden runs o certificaciones físicas; transferible. |
| [[30-resources/agents/skills/release-certification/SKILL.md|release-certification]] | Certifica que release/binario corresponde al source autorizado (baseline, blob equality, SHA256). | Antes de certificar/probar sobre una release. |
| [[30-resources/agents/skills/deployment-proof/SKILL.md|deployment-proof]] | Demuestra por jerarquía de evidencia que el runtime ejecuta la release nueva, sin aceptar exit 0. | Tras cualquier deploy que participe en una validación. |
| [[30-resources/agents/skills/readonly-production-probe/SKILL.md|readonly-production-probe]] | Crea probes temporales read-only contra sistemas reales con cleanup obligatorio. | Inspección física de producción sin modificar estado. |
| [[30-resources/agents/skills/distributed-incident-triage/SKILL.md|distributed-incident-triage]] | Triage forense multi-subsistema: timeline común, side effects y primer punto de divergencia. | Fallos que cruzan orquestador/object store/DBs/logs. |
| [[30-resources/agents/skills/evidence-channel-discovery/SKILL.md|evidence-channel-discovery]] | Descubre y persiste qué canales de evidencia existen realmente por pregunta. | Al empezar en un sistema desconocido o tras canales muertos. |
| [[30-resources/agents/skills/write-once-conflict-triage/SKILL.md|write-once-conflict-triage]] | Investiga conflictos de inmutabilidad clasificando duplicate/race/stale/contract-defect. | Ante CONTRACT_CONFLICT, checksum mismatch o violaciones de idempotencia. |
| [[30-resources/agents/skills/operational-healthcheck-policy/SKILL.md|operational-healthcheck-policy]] | Diferencia cuándo validar manualmente componentes vigilables y cuándo confiar en la automatización. | Ante una señal concreta de problema o antes de acciones masivas. |

### App-owned — repo `xKoRx/symphony` (Echo Forge / SQX)

Ownership real = repo de la app. `xKoRx/symphony` usa `.agents/skills/` como home canónica. El registry enlaza por `repo + path relativo`; nunca copia ni persiste un path absoluto de máquina (constitución, invariante 11).

| Skill | Una línea | Estado / ubicación |
|---|---|---|
| `xKoRx/symphony` → `.agents/skills/sqx-plugin-lifecycle/SKILL.md` | Modifica, compila, despliega y valida plugins Java de SQX con build contra SDK real, backup, canary y rollback. | ✅ migrada (piloto, 2026-08-07) al repo owner. |
| `xKoRx/symphony` → `.agents/skills/echo-forge-wfm-troubleshooting/SKILL.md` | Troubleshooting de Echo Forge/WFM; delega el acceso MCP a [[aranea-mcps-expert]]. | ✅ repo owner; fuente única de routing de dominio. |
| `xKoRx/symphony` → `.agents/skills/sqx-temporal-failure-audit/SKILL.md` | Audita una ejecución fallida de un workflow Temporal del SQX Worker sin proponer fix. | ✅ migrada al repo owner. |

## 🔗 Links

- [[30-resources/agents/00-index|Agents — Índice del dominio wiki]] (páginas curadas y registro de operaciones)
- [[30-resources/00-RESOURCE-WIKI|Resource Wiki — reglas del formato]]
- [[80-agents/agents-os/agents-os|agents-os]] — mapa conceptual del sistema
