---
type: "index"
schema_version: 1
status: "active"
icon: "🧭"
slug: "skills-index"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: "2026-06-28"
updated: "2026-10-30"
reviewed: "2026-10-27"
aliases: ["skills index", "catálogo de skills", "registro de habilidades"]
cssclasses: ["wide"]
tags: ["kind/index", "tech/agents-os", "tech/skills"]
---

# 🧭 AGENTS OS Skills — Índice

> [!info] Registro de habilidades en formato wiki
> Este índice es el catálogo curado de las skills. El core (`80-agents/skills/`) contiene sólo comportamientos de AGENTS OS; las skills de dominio y transversales viven curadas en `30-resources/agents/skills/` y las app-owned en el repo owner. Se carga en el cold start del `agents-os-bootstrap` para que el agente sepa qué tiene disponible. Reglas de la wiki: [[30-resources/00-RESOURCE-WIKI|Resource Wiki]].

## 📊 De un vistazo

- **Core AGENTS OS:** comportamientos del sistema enumerados en el catálogo; el índice no duplica sus procedimientos.
- **Federadas transversales y de dominio:** catálogo curado en `30-resources/agents/skills/`; Echo I+D dispone de manager global, manager Futures y manager Forex reutilizado.
- **Domain/app-owned:** se descubren mediante el registro de routers y el repo owner; no forman parte del índice always-load.
- **Regla de lugar:** una skill vive en el core sólo si cambia el comportamiento de AGENTS OS itself; todo lo demás vive federado y se enlaza, no se copia.

## 📂 Catálogo

### Core — comportamientos de AGENTS OS

| Skill | Una línea | Cuándo cargar |
|---|---|---|
| [[80-agents/skills/agents-os-bootstrap/SKILL.md|agents-os-bootstrap]] | Clasifica cold/warm/cambio de entidad y carga el contexto mínimo correspondiente. | Una vez en cold start; en warm reutilizar y recuperar sólo el delta. |
| [[80-agents/skills/agents-os-context-retrieval/SKILL.md|agents-os-context-retrieval]] | Orquesta la recuperación enfocada de contexto mediante Graphify y filtros. | Al buscar contexto de entidades. |
| [[80-agents/skills/agents-os-context-scout/SKILL.md|agents-os-context-scout]] | Recupera contexto canónico con evidencia y feedback por invocación; mejora sólo su propia skill/runbook. | Scout obligatorio para contexto no trivial del vault; routing desde bootstrap. |
| [[80-agents/skills/agents-os-code-scout/SKILL.md|agents-os-code-scout]] | Describe diseño existente, patrones, rules y puntos críticos de repos; no diseña ni modifica producto. | Scout obligatorio para comprensión no trivial de código; feedback y ownership acotados. |
| [[80-agents/skills/agents-os-session-close/SKILL.md|agents-os-session-close]] | Cierra por delta y preserva sólo estado/conocimiento justificado; no exige L0/L1 rituales. | Sólo cuando el usuario pida explícitamente cerrar sesión. |
| [[80-agents/skills/agents-os-session-feedback/SKILL.md|agents-os-session-feedback]] | Captura fricción real, degradación o gaps con evidencia; no genera policy automáticamente. | Por evento o pedido explícito, no por cada cierre. |
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

Las skills transversales viven curadas en el vault bajo
`30-resources/agents/skills/`. Los routers scoped y sus especialistas se
descubren únicamente desde `30-resources/agents/domain-router-registry.md`; las
skills de una aplicación viven y se descubren en su repo owner.

### Dominio y transversales — `30-resources/agents/skills/`

| Skill | Una línea | Dominio / uso |
|---|---|---|
| [[30-resources/agents/skills/pr-description/SKILL.md|pr-description]] | Produce descripciones de PR con evidencia real y las materializa como recurso del proyecto. | Transversal; respeta template y policy del repo activo. |
| [[30-resources/agents/skills/human-first-technical-writing/SKILL.md|human-first-technical-writing]] | Reduce la carga cognitiva del lector mediante narrativa técnica causal. | Transversal: PRs, specs, reportes, incidentes, guías. |
| [[30-resources/agents/skills/technical-project-manager/SKILL.md|technical-project-manager]] | Gestiona entregas técnicas acotadas con el Owner, decisiones explícitas, mandatos completos y verificación independiente. | Transversal; entregas técnicas delegadas. Para el programa evergreen Echo I+D usar su manager específico. |
| [[30-resources/agents/skills/sync-local-branch/SKILL.md|sync-local-branch]] | Sincroniza ramas Git exclusivamente locales con pull literal, merge conservador, commit y push. | Dev-workflow genérico. |
| [[30-resources/agents/skills/sdd-workflow/SKILL.md|sdd-workflow]] | Clasifica y ejecuta fases SDD sin mezclar specification, plan, tasks, implementation y verification. | Features/cambios no triviales; metodología en `30-resources/methodologies/sdd/`. |
| [[30-resources/agents/skills/sdd-developer/SKILL.md|sdd-developer]] | Entrega una SPEC SDD ready mediante implementación one-shot, verificación adversarial independiente y corrección/gate final, preservando regresiones/E2E reutilizables. | Transversal; IMPLEMENT+VERIFY de features SDD listas. |
| [[30-resources/agents/skills/e2e-gated-validation/SKILL.md|e2e-gated-validation]] | Orquesta validaciones E2E como secuencia de gates con evidencia y criterios PASS/FAIL. | E2E, golden runs o certificaciones físicas; transferible. |
| [[30-resources/agents/skills/echo-retester-master/SKILL.md|echo-retester-master]] | Gobierna desarrollo/conformidad teoría→regla→código→operación y G0–G5 por identidad Futures; histórico sólo con cualificación propia. | Echo Futures, ClutiFX y futuras campañas de extracción/implementación de estrategias; no LIVE. |
| [[30-resources/agents/skills/release-certification/SKILL.md|release-certification]] | Certifica que release/binario corresponde al source autorizado (baseline, blob equality, SHA256). | Antes de certificar/probar sobre una release. |
| [[30-resources/agents/skills/deployment-proof/SKILL.md|deployment-proof]] | Demuestra por jerarquía de evidencia que el runtime ejecuta la release nueva, sin aceptar exit 0. | Tras cualquier deploy que participe en una validación. |
| [[30-resources/agents/skills/readonly-production-probe/SKILL.md|readonly-production-probe]] | Crea probes temporales read-only contra sistemas reales con cleanup obligatorio. | Inspección física de producción sin modificar estado. |
| [[30-resources/agents/skills/distributed-incident-triage/SKILL.md|distributed-incident-triage]] | Triage forense multi-subsistema: timeline común, side effects y primer punto de divergencia. | Fallos que cruzan orquestador/object store/DBs/logs. |
| [[30-resources/agents/skills/evidence-channel-discovery/SKILL.md|evidence-channel-discovery]] | Descubre y persiste qué canales de evidencia existen realmente por pregunta. | Al empezar en un sistema desconocido o tras canales muertos. |
| [[30-resources/agents/skills/write-once-conflict-triage/SKILL.md|write-once-conflict-triage]] | Investiga conflictos de inmutabilidad clasificando duplicate/race/stale/contract-defect. | Ante CONTRACT_CONFLICT, checksum mismatch o violaciones de idempotencia. |
| [[30-resources/agents/skills/observability-metrics-standard/SKILL.md|observability-metrics-standard]] | Diseña, audita, migra o revisa métricas custom (nombre/tipo/tags/emisión) con un método portable, sin grammar de Meli. | Aranea/homelab o proyectos personales; nunca Meli/RIO/Signals (→ meli-agent-dev). |
| [[30-resources/agents/skills/operational-healthcheck-policy/SKILL.md|operational-healthcheck-policy]] | Diferencia cuándo validar manualmente componentes vigilables y cuándo confiar en la automatización. | Ante una señal concreta de problema o antes de acciones masivas. |
| [[30-resources/agents/skills/echo-production-operational-audit/SKILL.md|echo-production-operational-audit]] | Auditoría operacional E2E read-only de Echo PROD: gates G1–G12 (incluye config-flow trigger→gateway→topic→cache y consistencia de estado), trazas E2E reales y veredicto OPERATIONAL_*. | Al auditar el funcionamiento real de Echo PROD tras una ventana de cambios. |
| [[30-resources/agents/skills/echo-prod-deploy/SKILL.md|echo-prod-deploy]] | Despliegue autorizado de Echo a PROD (BD, ETCD, Hasura, deploy-prod.sh, front) con verificación y rollback. **Owner-gated**: sólo por pedido explícito del owner de usarla. | Única vía para mutar PROD Echo desde el agente; requiere autorización y secretos de cada corrida. |
| [[30-resources/agents/skills/course-knowledge-extraction/SKILL.md|course-knowledge-extraction]] | Extrae conocimiento de videos de curso a una biblioteca por capítulo (transcript citable + 1 frame/min + frames bajo demanda + revisión POR MINUTO); prohíbe explícitamente el grind MKE por claim (44 h/video medidos). | Al procesar videos de cursos (Clutifx 2 y siguientes) o generar knowledge libraries desde video. |
| [[30-resources/agents/skills/course-knowledge-worker/SKILL.md|course-knowledge-worker]] | Contrato de los subagentes ONE-SHOT de la skill anterior (EXTRACTOR / MINUTE_REVIEWER / DOCUMENTATION_VERIFIER): paquete de entrada, invariantes y contrato de salida por rol; workers sin acceso a archivos canónicos. | Al despachar workers de extracción/revisión/verificación de un capítulo; lo carga el orquestador y se incluye en cada paquete. |

### Echo I+D — gestión y diseño de investigación

| Skill | Una línea | Dominio / uso |
|---|---|---|
| [[30-resources/agents/skills/echo-rnd-manager/SKILL.md|echo-rnd-manager]] | Gestiona el programa permanente Echo I+D con el Owner: dos mercados, prioridades, WIP, agentes, aprendizaje y continuidad. | Dirección global y decisiones entre líneas; no ejecución de producto. |
| [[30-resources/agents/skills/echo-futures-research-manager/SKILL.md|echo-futures-research-manager]] | Gestiona cobertura, hipótesis, specs, mandatos y economía challenge/funded de Futures; deriva G0–G5 al retester. | Investigación Futures; NQ inmediato según el planner. |
| [[30-resources/agents/skills/sqx144-campaign-design/SKILL.md|sqx144-campaign-design]] | Diseña hipótesis, presets compatibles y sondas SQX 144 con evidencia de IMOX. | Trading; diseño previo, no ejecución ni cambios de Forge. |
| [[30-resources/agents/skills/imox-strategy-research/SKILL.md|imox-strategy-research]] | Manager de la línea Forex/CFD de Echo I+D: roadmap, cobertura, campañas, agentes y aprendizaje, reutilizando IMOX/SQX/Forge. | Forex/CFD; conserva F0→F3 y deriva presets/operación. Para Futures usar su manager. |

Mapa operativo del programa: [[Echo I+D — Mapa de capacidades]] (etapa → skill/runbook → planner → superficie → evidencia). Metodología común de gestión: [[30-resources/runbooks/echo-rnd-cycle-runbook|echo-rnd-cycle-runbook]]. Las secuencias técnicas siguen en sus autoridades de mercado.

### Conocimiento de comunidades

| Skill | Una línea | Uso |
|---|---|---|
| [[30-resources/agents/skills/imox-update/SKILL.md|imox-update]] | «actualiza imox»: sincroniza fuentes con Chrome del owner y manifiesto de descargas entre sesiones. | Sólo Codex en Hefesto; consulta en origen, escritura local de resources. |
| [[30-resources/agents/skills/community-knowledge-ingest/SKILL.md|community-knowledge-ingest]] | Inventario, lectura, exclusiones y sincronización con fronteras verificables. | Circle/IMOX ahora; otras comunidades cuando se incorporen. |

## 🔗 Links

- [[30-resources/agents/00-index|Agents — Índice del dominio wiki]] (páginas curadas y registro de operaciones)
- [[30-resources/00-RESOURCE-WIKI|Resource Wiki — reglas del formato]]
- [[80-agents/agents-os/agents-os|agents-os]] — mapa conceptual del sistema
