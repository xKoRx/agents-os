---
type: doc
schema_version: 1
status: active
created: 2026-08-10
updated: 2026-09-03
tags:
  - kind/doc
  - kind/system
  - tech/agents-os
---

# AGENTS OS Executable Schema Contract

## Propósito

Esta nota es la autoridad machine-readable para el envelope, versiones, campos, estados, tags, secciones mínimas, template canónico y política de lint de cada tipo S1 y S2. Las guías humanas explican semántica; no duplican estos sets exactos.

## Contenido

### Semántica de versión

- `schema_version` es un entero obligatorio en toda nota creada desde este
  contrato y en todo template canónico.
- La versión actual y única soportada es `1`.
- Una nota live sin `schema_version` es legacy: se puede leer, pero no crear ni
  modificar sin migrarla primero a una versión soportada.
- Una versión futura o desconocida falla cerrada. Los upgrades son migradores
  explícitos; nunca se reescribe un corpus por inferencia.
- Cambiar reglas incompatibles crea una nueva versión y conserva fixtures de
  compatibilidad. Corregir prosa sin cambiar el contrato no incrementa versión.

### Contrato ejecutable

El bloque entre markers es JSON estricto para que Python stdlib pueda leerlo
sin introducir una dependencia YAML. No editar tablas paralelas en otro lugar.

<!-- AGENTS_OS_SCHEMA_START -->
```json
{
  "contract_version": 1,
  "schema_versions": {
    "current": 1,
    "supported": [1],
    "legacy_unversioned": "read_only",
    "unknown_version": "reject",
    "upgrade_policy": "explicit_migrator"
  },
  "field_types": {
    "type": {"kind": "string", "values": "systems.*.types keys"},
    "schema_version": {"kind": "integer", "values": "schema_versions.supported"},
    "created": {"kind": "date", "format": "YYYY-MM-DD"},
    "updated": {"kind": "date", "format": "YYYY-MM-DD"},
    "status": {"kind": "string", "values": "type.statuses"},
    "scope": {"kind": "string", "values": ["global", "user", "area", "project", "application", "service", "tool", "technology", "integration", "workflow", "session", "graphify"]},
    "owner": {"kind": "string", "values": ["me", "agent"]},
    "root": {"kind": "boolean"},
    "progress": {"kind": "integer", "minimum": 0, "maximum": 100},
    "priority": {"kind": "string", "pattern": "^P[0-4]$"},
    "confidence": {"kind": "string", "values": ["verified", "high", "medium", "low"]},
    "indexable": {"kind": "boolean"},
    "index_priority": {"kind": "string", "values": ["critical", "high", "medium", "low", "never"]},
    "share_scope": {"kind": "string", "values": ["local", "team"]},
    "tags": {"kind": "list", "items": "string"},
    "aliases": {"kind": "list", "items": "string"},
    "entities": {"kind": "list", "items": "canonical_wikilink"},
    "related": {"kind": "list", "items": "canonical_wikilink"},
    "sources": {"kind": "list", "items": "resolvable_reference"},
    "area": {"kind": "canonical_wikilink"},
    "project": {"kind": "canonical_wikilink"},
    "application": {"kind": "canonical_wikilink"},
    "load_policy": {"kind": "string", "rule": "concrete runtime trigger"},
    "memory_state": {"kind": "string", "values": ["active", "superseded", "archived"]},
    "continuity_key": {"kind": "string", "pattern": "^[a-z0-9]+(?:[a-z0-9/-]*[a-z0-9])?$"},
    "supersedes": {"kind": "canonical_wikilink"},
    "superseded_by": {"kind": "canonical_wikilink"},
    "target": {"kind": "string"},
    "prompt_version": {"kind": "integer", "minimum": 1},
    "inputs": {"kind": "list", "items": "string"},
    "outputs": {"kind": "list", "items": "string"},
    "agent_surface": {"kind": "canonical_wikilink"},
    "agent_model": {"kind": "string"},
    "agent_run": {"kind": "canonical_wikilink"},
    "model_source": {"kind": "string", "values": ["host", "user", "unknown"]},
    "task_type": {"kind": "string", "values": ["coding", "debugging", "review", "testing", "planning", "research", "docs", "ops", "mixed", "other"]},
    "task_complexity": {"kind": "string", "values": ["low", "medium", "high", "unknown"]},
    "outcome": {"kind": "string", "values": ["success", "partial", "failed", "blocked"]},
    "verification": {"kind": "string", "values": ["passed", "partial", "failed", "not_run"]},
    "evaluator": {"kind": "string", "values": ["agent", "owner", "mixed"]},
    "user_rework": {"kind": "string", "values": ["none", "minor", "major", "unknown"]},
    "score_correctness": {"kind": "integer", "minimum": 1, "maximum": 5},
    "score_autonomy": {"kind": "integer", "minimum": 1, "maximum": 5},
    "score_efficiency": {"kind": "integer", "minimum": 1, "maximum": 5},
    "score_tool_use": {"kind": "integer", "minimum": 1, "maximum": 5},
    "score_overall": {"kind": "integer", "minimum": 1, "maximum": 5}
  },
  "envelope": {
    "common": {
      "required": ["type", "schema_version", "created", "updated", "tags"],
      "optional": ["aliases", "entities", "related", "area", "project", "application", "slug"],
      "forbidden": []
    },
    "s1": {
      "required": ["scope"],
      "optional": ["confidence", "source_session", "load_policy", "indexable", "index_priority", "share_scope"],
      "forbidden": ["status", "draft"]
    },
    "s2": {
      "required": [],
      "optional": ["status", "priority", "repo", "path", "source_url"],
      "forbidden": []
    }
  },
  "tags": {
    "required_patterns": ["kind/<type-kebab>"],
    "s1_required_patterns": ["scope/<scope>"],
    "routing_prefixes": ["area/", "project/", "app/", "tech/", "priority/", "agent/", "change/"],
    "forbidden": ["important", "misc", "pending", "ai"],
    "rule": "tags_filter_links_route"
  },
  "creation": {
    "materializer": "80-agents/skills/_shared/scripts/materialize_schema_note.py",
    "policy": "canonical notes are materialized from the resolved template; direct template copies and handwritten frontmatter are rejected",
    "validation_scope": "creation validates the shared contract plus the requested type/template; full-corpus validation is reserved for contract changes, doctor, and release gates",
    "token_economy": "validation and type resolution are local programmatic filters; the full contract body is not an always-load context dependency",
    "entrypoints": [
      "80-agents/skills/agents-os-entity-lifecycle/SKILL.md",
      "80-agents/skills/agents-os-note-capture/SKILL.md",
      "80-agents/skills/agents-os-entity-update/SKILL.md",
      "80-agents/skills/agents-os-resource-wiki/SKILL.md",
      "80-agents/skills/agents-os-memory-distillation/SKILL.md",
      "80-agents/skills/agents-os-session-close/SKILL.md",
      "80-agents/skills/agents-os-session-feedback/SKILL.md",
      "80-agents/skills/agents-os-skill-authoring/SKILL.md",
      "80-agents/skills/agents-os-behavior-config/SKILL.md",
      "80-agents/skills/agents-os-conflict-resolution/SKILL.md",
      "80-agents/skills/agents-os-retrofit-raw-session/SKILL.md",
      "80-agents/skills/agents-os-install/SKILL.md",
      "80-agents/skills/agents-os-implementation-planning/SKILL.md"
    ]
  },
  "lint": {
    "baseline": "80-agents/skills/agents-os-entity-lifecycle/lint-baseline-v1.json",
    "fingerprint_algorithm": "sha256",
    "strict_policy": "explicit_paths_must_use_current_schema",
    "gate_policy": "current_findings_must_be_subset_of_baseline",
    "legacy_policy": "unversioned_notes_are_read_only_and_keep_legacy_validation_until_migrated",
    "legacy_required": {
      "s1": ["scope", "created", "updated", "tags"],
      "s2": ["created", "updated"],
      "types": {
        "area": ["status", "slug", "aliases"],
        "project": ["status", "owner", "area", "priority", "progress"],
        "application": ["status", "area"],
        "service": ["area"],
        "idea": ["area", "priority"],
        "methodology": ["area", "sources"]
      }
    },
    "semantic_rules": ["project_parent_or_root", "source_location"]
  },
  "systems": {
    "s1": {
      "template_root": "80-agents/templates",
      "types": {
        "constitution": {
          "template": "80-agents/templates/constitution.md",
          "required": ["confidence", "load_policy", "indexable", "index_priority"],
          "optional": ["entities", "related", "aliases"],
          "forbidden": [],
          "sections": ["## Reglas", "## Retrieval", "## Cierre de sesión"]
        },
        "user_preference": {
          "template": "80-agents/templates/user-preference.md",
          "required": ["confidence", "load_policy", "indexable", "index_priority"],
          "optional": ["entities", "related", "aliases", "area"],
          "forbidden": [],
          "sections": ["## Preferencias de interacción", "## Preferencias de trabajo"]
        },
        "agent_memory": {
          "template": "80-agents/templates/agent-memory.md",
          "required": ["load_policy", "indexable", "index_priority"],
          "optional": ["confidence", "entities", "related", "area", "project", "application", "memory_state", "continuity_key", "supersedes", "superseded_by"],
          "forbidden": [],
          "sections": ["## Continuidad", "## Señales de carga"]
        },
        "skill": {
          "template": "80-agents/templates/skill.md",
          "required": ["name", "description", "load_policy", "indexable", "index_priority"],
          "optional": ["entities", "related", "aliases"],
          "forbidden": [],
          "sections": ["## Purpose", "## Procedure", "## Hard Rules"]
        },
        "learning": {
          "template": "80-agents/templates/learning.md",
          "required": ["confidence", "load_policy", "indexable", "index_priority"],
          "optional": ["source_session", "entities", "related", "area", "project", "application"],
          "forbidden": [],
          "sections": ["## Aprendizaje", "## Aplicabilidad", "## Evidencia"]
        },
        "decision": {
          "template": "80-agents/templates/decision.md",
          "required": ["confidence", "load_policy", "indexable", "index_priority"],
          "optional": ["source_session", "entities", "related", "area", "project", "application"],
          "forbidden": [],
          "sections": ["## Contexto", "## Decisión", "## Consecuencias"]
        },
        "known_error": {
          "template": "80-agents/templates/known-error.md",
          "required": ["confidence", "load_policy", "indexable", "index_priority"],
          "optional": ["source_session", "entities", "related", "area", "project", "application"],
          "forbidden": [],
          "sections": ["## Síntoma", "## Causa", "## Mitigación"]
        },
        "runbook": {
          "template": "80-agents/templates/runbook.md",
          "required": ["confidence", "load_policy", "indexable", "index_priority"],
          "optional": ["source_session", "entities", "related", "area", "project", "application"],
          "forbidden": [],
          "sections": ["## Propósito", "## Procedimiento", "## Validación"]
        },
        "command": {
          "template": "80-agents/templates/command.md",
          "required": ["confidence", "load_policy", "indexable", "index_priority"],
          "optional": ["entities", "related", "area", "project", "application"],
          "forbidden": [],
          "sections": ["## Comando", "## Uso", "## Validación"]
        },
        "pattern": {
          "template": "80-agents/templates/pattern.md",
          "required": ["confidence", "load_policy", "indexable", "index_priority"],
          "optional": ["entities", "related", "area", "project", "application"],
          "forbidden": [],
          "sections": ["## Patrón", "## Aplicabilidad", "## Ejemplo"]
        },
        "feedback": {
          "template": "80-agents/templates/session-feedback.md",
          "required": ["load_policy", "indexable", "index_priority"],
          "optional": ["confidence", "source_session", "entities", "related", "area", "project", "agent_surface", "agent_model", "agent_run"],
          "forbidden": [],
          "sections": ["## Context"]
        },
        "agent_run": {
          "template": "80-agents/templates/agent-run.md",
          "required": ["agent_surface", "agent_model", "model_source", "task_type", "task_complexity", "outcome", "verification", "evaluator", "user_rework", "load_policy", "indexable", "index_priority"],
          "optional": ["score_correctness", "score_autonomy", "score_efficiency", "score_tool_use", "score_overall", "source_session", "entities", "related", "area", "project", "application"],
          "forbidden": [],
          "sections": ["## Trabajo", "## Evidencia", "## Evaluación", "## Resultado"]
        },
        "session": {
          "template": "80-agents/templates/session-summary.md",
          "required": ["load_policy", "indexable", "index_priority"],
          "optional": ["confidence", "source_session", "entities", "related", "area", "project", "application"],
          "forbidden": [],
          "sections": ["## Objetivo", "## Trabajo realizado", "## Pendiente"]
        },
        "raw_session": {
          "template": "80-agents/templates/raw-session.md",
          "required": ["load_policy", "indexable", "index_priority"],
          "optional": ["confidence", "source_session", "entities", "related", "area", "project", "application"],
          "forbidden": [],
          "sections": ["## Contexto", "## Transcript"]
        },
        "change_log": {
          "template": "80-agents/templates/change-log.md",
          "required": ["share_scope", "load_policy", "indexable", "index_priority"],
          "optional": ["confidence", "source_session", "entities", "related", "area", "project", "application"],
          "forbidden": [],
          "sections": ["## Cambio", "## Validación", "## Rollback"]
        },
        "scratch": {
          "template": null,
          "exemption": {"kind": "derived", "reason": "ephemeral or generated reports are not canonical reusable notes"},
          "required": ["load_policy", "indexable", "index_priority"],
          "optional": ["confidence", "source_session", "entities", "related", "area", "project", "application"],
          "forbidden": [],
          "sections": []
        }
      }
    },
    "s2": {
      "template_root": "70-templates",
      "types": {
        "area": {"template": "70-templates/area.md", "required": ["status", "slug", "aliases"], "optional": ["icon", "review"], "forbidden": [], "statuses": ["active", "archived"], "sections": ["## 🎯 Objetivo", "## 📊 Estado actual"]},
        "project": {"template": "70-templates/project.md", "required": ["status", "owner", "root", "area", "priority", "progress"], "optional": ["parent", "sprint", "repo", "jira", "prs", "start", "due"], "forbidden": [], "statuses": ["active", "paused", "review", "completed", "archived"], "sections": ["## 🎯 Objetivo", "## 📊 Estado actual", "## ✅ Tareas", "## 📆 Bitácora"], "rules": ["project_parent_or_root"]},
        "application": {"template": "70-templates/application.md", "required": ["status", "area"], "optional": ["repo", "path", "slug", "aliases", "lang", "github", "last_verified", "confidence"], "forbidden": [], "statuses": ["active", "deprecating", "deprecated", "archived"], "sections": ["## 🎯 Responsabilidad (estable)", "## 🔌 Contratos e interacciones (semi-estable)"]},
        "service": {"template": "70-templates/service.md", "required": ["status", "area"], "optional": ["repo", "path", "slug", "aliases"], "forbidden": [], "statuses": ["active", "deprecated", "archived"], "sections": ["## Propósito", "## Operación"]},
        "service-doc": {"template": "70-templates/service-operational.md", "required": ["status", "area"], "optional": ["aliases"], "forbidden": [], "statuses": ["draft", "partial", "active", "template"], "sections": ["## 🎯 Propósito", "## 🔧 Operación"]},
        "technology": {"template": "70-templates/technology.md", "required": ["status"], "optional": ["area", "slug", "aliases"], "forbidden": [], "statuses": ["active", "deprecated", "archived"], "sections": ["## Descripción", "## Uso"]},
        "tool": {"template": "70-templates/tool.md", "required": ["status"], "optional": ["scope", "area", "project", "source_url", "command", "load_policy", "indexable", "index_priority"], "forbidden": [], "statuses": ["active", "deprecated", "archived"], "sections": ["## Descripcion", "## Uso principal"]},
        "integration": {"template": "70-templates/integration.md", "required": ["status"], "optional": ["area", "entities", "related", "aliases"], "forbidden": [], "statuses": ["active", "deprecated", "archived"], "sections": ["## Propósito", "## Contrato"]},
        "workflow": {"template": "70-templates/workflow.md", "required": ["status"], "optional": ["area", "entities", "related", "aliases"], "forbidden": [], "statuses": ["active", "deprecated", "archived"], "sections": ["## Propósito", "## Flujo"]},
        "storage": {"template": "70-templates/storage.md", "required": ["status", "slug", "aliases"], "optional": ["area", "related"], "forbidden": [], "statuses": ["active", "deprecated", "archived"], "sections": ["## Propósito", "## Ubicación y contrato", "## Operación"]},
        "api": {"template": "70-templates/api.md", "required": ["status"], "optional": ["area", "application", "repo", "path", "entities", "related", "aliases"], "forbidden": [], "statuses": ["active", "deprecated", "archived"], "sections": ["## Propósito", "## Contrato", "## Versionado"]},
        "concept": {"template": "70-templates/concept.md", "required": ["status"], "optional": ["area", "related", "aliases"], "forbidden": [], "statuses": ["active", "deprecated", "archived"], "sections": ["## Definición", "## Límites"]},
        "entity": {"template": "70-templates/entity.md", "required": ["status"], "optional": ["area", "entities", "related", "aliases"], "forbidden": [], "statuses": ["active", "deprecated", "archived"], "sections": ["## Descripción", "## Relaciones"]},
        "agent": {"template": "70-templates/agent-profile.md", "required": ["status"], "optional": ["specialty", "model", "aliases"], "forbidden": [], "statuses": ["active", "deprecated", "archived"], "sections": ["## 📜 Directivas y Reglas de Comportamiento", "## 🛠️ Limitaciones Técnicas y Operativas"]},
        "resource": {"template": "70-templates/resource.md", "required": ["status", "area", "sources"], "optional": ["last_verified", "confidence", "aliases"], "forbidden": [], "statuses": ["active", "deprecated"], "sections": ["## Síntesis vigente", "## Evidencia y provenance"]},
        "prompt": {"template": "70-templates/prompt.md", "required": ["status", "area", "target", "prompt_version", "inputs", "outputs"], "optional": ["application", "project", "aliases", "related"], "forbidden": [], "statuses": ["active", "deprecated", "archived"], "sections": ["## Propósito", "## Contrato de entrada", "## Contrato de salida", "## Prompt", "## Límites"]},
        "methodology": {"template": "70-templates/methodology.md", "required": ["status", "area", "sources"], "optional": ["last_verified", "confidence", "aliases"], "forbidden": [], "statuses": ["draft", "active", "deprecated"], "sections": ["## Propósito", "## Procedimiento reusable"]},
        "source": {"template": "70-templates/source.md", "required": ["status", "area"], "optional": ["source_url", "repo", "path", "author", "published", "captured", "license", "checksum", "supersedes", "superseded_by", "aliases"], "forbidden": [], "statuses": ["active", "superseded", "archived"], "sections": ["## Referencia", "## Notas de provenance"], "rules": ["source_location"]},
        "idea": {"template": "70-templates/idea.md", "required": ["status", "priority", "area"], "optional": ["project", "application", "entities", "related", "visibility", "governed_by", "promotion_target", "source", "aliases"], "forbidden": [], "statuses": ["seed", "exploring", "promoted", "discarded"], "sections": ["## 🧠 La idea", "## 🎯 Motivo / por qué", "## 🌱 Próximo paso"]},
        "sprint": {"template": "70-templates/sprint.md", "required": ["status", "area"], "optional": ["quarter", "start", "end"], "forbidden": [], "statuses": ["planned", "active", "closed"], "sections": ["## 🎯 Objetivo del sprint", "## 🔗 Proyectos del sprint"]},
        "quarter": {"template": "70-templates/quarter.md", "required": ["status", "area"], "optional": ["start", "end"], "forbidden": [], "statuses": ["active", "closed"], "sections": ["## 🎯 Objetivo del quarter", "## 📅 Sprints"]},
        "meeting": {"template": "70-templates/meeting.md", "required": ["date"], "optional": ["area", "project", "attendees"], "forbidden": ["status"], "statuses": [], "sections": ["## 🗂️ Contexto / Agenda", "## 🧭 Decisiones", "## ✅ Action items"]},
        "index": {"template": "70-templates/index.md", "required": ["status"], "optional": ["icon", "slug", "area", "project", "reviewed", "aliases", "cssclasses"], "forbidden": [], "statuses": ["active", "archived"], "sections": ["## 📊 De un vistazo", "## 📂 Catálogo"]},
        "dashboard": {"template": "70-templates/dashboard.md", "required": ["status"], "optional": ["icon"], "forbidden": [], "statuses": ["active", "archived"], "sections": ["## Sección"]},
        "home": {"template": "70-templates/home.md", "required": ["status"], "optional": ["area", "aliases"], "forbidden": [], "statuses": ["active", "archived"], "sections": ["## Navegación", "## Estado"]},
        "doc": {"template": "70-templates/doc.md", "required": ["status"], "optional": ["area", "related", "aliases"], "forbidden": [], "statuses": ["active", "archived"], "sections": ["## Propósito", "## Contenido"]},
        "monitor": {"template": "70-templates/monitor.md", "required": ["status"], "optional": ["service", "last_check"], "forbidden": [], "statuses": ["ok", "warn", "alert", "active"], "sections": ["## Estado", "## Última revisión"]},
        "action": {"template": "70-templates/action.md", "required": ["status"], "optional": ["project"], "forbidden": [], "statuses": ["todo", "doing", "done", "canceled"], "sections": ["## Descripción", "## Checklist"]},
        "context_pack": {"template": "70-templates/ai-context-pack.md", "required": ["status", "snapshot_date", "source_of_truth"], "optional": ["area", "project", "entities", "related", "aliases"], "forbidden": [], "statuses": ["snapshot"], "sections": ["## Propósito", "## Jerarquía de autoridad", "## Fuentes"]}
      }
    }
  },
  "derived_templates": [
    {"path": "80-agents/templates/graphify-feedback.md", "type": "feedback", "reason": "specialized feedback capture; canonical creation defaults to session-feedback.md"},
    {"path": "80-agents/templates/hygiene-report.md", "type": "scratch", "reason": "derived operational report excluded from normal retrieval"}
  ],
  "fragments": [
    {"path": "70-templates/task.md", "reason": "task-line snippet without frontmatter; not a note type"}
  ],
  "fixtures": [
    {"path": "80-agents/skills/_shared/fixtures/schema/valid/project-v1.md", "expect": "valid"},
    {"path": "80-agents/skills/_shared/fixtures/schema/valid/prompt-v1.md", "expect": "valid"},
    {"path": "80-agents/skills/_shared/fixtures/schema/valid/agent-run-v1.md", "expect": "valid"},
    {"path": "80-agents/skills/_shared/fixtures/schema/legacy/project-unversioned.md", "expect": "legacy"},
    {"path": "80-agents/skills/_shared/fixtures/schema/invalid/project-v2.md", "expect": "invalid"}
  ]
}
```
<!-- AGENTS_OS_SCHEMA_END -->

### Ownership del contrato

- Esta nota define sets exactos y mappings ejecutables.
- `metadata-schema.md`, `note-types.md` y `90-system/convenciones.md` explican
  uso y fronteras sin redefinir las listas.
- En Fase 1, `validate_schema_contract.py` valida contrato, templates y
  fixtures. En Fase 2, el lint preventivo debe consumir este mismo bloque.
- El materializador valida de forma fail-closed sólo el slice del tipo pedido;
  el modo global sigue siendo obligatorio para cambios del contrato, Doctor y
  gates de release. Drift S1/S2 no relacionado se reporta globalmente pero no
  bloquea una creación cuyo propio tipo/template está sano.
- La resolución/materialización es programática y local: no carga este cuerpo
  en el contexto LLM. Esto implementa [[Economía de Tokens]] y
  [[token-economy-indexing-architecture]], no una nueva dependencia always-load.
