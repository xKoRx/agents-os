---
type: idea
schema_version: 1
status: seed
priority: P3
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[local-agents-pipeline-cli]]"
related:
  - "[[AGENTS OS]]"
  - "[[Fuentes — Workspace de repositorios]]"
visibility: public
governed_by: user
promotion_target:
source: "[[local-agents-pipeline-cli-source]]"
aliases: []
tags:
  - kind/idea
  - area/personal
  - idea/validation
  - size/small
created: "2026-08-26"
updated: "2026-08-26"
---

# 💡 Review gate local para el vault

> [!tip]+ Review gate local para el vault
> _Idea en bruto. Estados: seed → exploring → promoted → discarded. Si madura, promover a proyecto, tarea o aprendizaje._

## 🧠 La idea

- Construir una versión integrada del patrón Zord para el ecosistema personal: un comando local que detecte diffs de repos, ejecute checks deterministas baratos primero, invoque revisión LLM solo cuando corresponde y guarde un artefacto Markdown/JSON enlazado desde el vault.

## 🎯 Motivo / por qué

- `local-agents-pipeline-cli` ya resuelve el orquestador, prompts configurables, providers múltiples, síntesis, IDs de findings y fixes selectivos; el vault ya tiene una capa de provenance, índices y logs donde esos resultados podrían quedar trazables.
- La oportunidad no es copiar el repositorio al vault, sino usarlo como referencia para un workflow de calidad que conecte `repo + commit/PR + findings + decisión humana + siguiente acción` sin duplicar el código fuente.

## 🧭 Routing

- **Área:** [[Personal]]
- **Proyecto:** [[AGENTS OS]]
- **Aplicación:** 
- **Entidades:** [[local-agents-pipeline-cli]]

## 🏷️ Clasificación

- **Tamaño:** medium
- **Tipo:** opportunity
- **Prioridad:** P3
- **Estado:** seed
- **Visibilidad:** public
- **Gobernada por:** user
- **Criterio de promoción:** promover a tarea/proyecto si requiere más de una acción o si impacta una iniciativa activa.

## 🔗 Relacionado

- [[local-agents-pipeline-cli]], [[AGENTS OS]], [[Fuentes — Workspace de repositorios]]

## 🌱 Próximo paso

- [ ] Elegir un solo repo piloto y definir el contrato mínimo del artefacto `review.json`/Markdown, sin implementar todavía #owner/me #type/research #area/personal
