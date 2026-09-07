---
type: learning
scope: global
created: 2026-07-01
updated: 2026-07-01
area: "[[Meli]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[Meli]]"
aliases:
  - conflicto de politica de repo externo
  - preguntar antes de escribir RFC en repo con reglas propias
confidence: verified
source_session: "2026-07-01-rfc-destaques-de-precio-hito2-mla-mlm-rollout-summary"
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - area/meli
  - kind/learning
  - priority/high
  - project/agents-os
  - scope/global
---
# Surface External Repo Policy Conflicts Before Writing

## Aprendizaje

Cuando una tarea implica escribir o actualizar contenido en un repositorio
externo al vault de Obsidian (ej. `sb-main`, el Brain compartido del squad),
el agente debe leer primero las reglas propias de ese repo (`CLAUDE.md`,
`.claude/rules/*`) antes de asumir que las convenciones del vault aplican
igual. Si el estado real (un archivo legacy ya existente) choca con una
regla vigente del repo (ej. "RFC y specs no viven localmente, van en Google
Doc/Spellbook"), no resolver el conflicto en silencio en ninguna dirección
(ni migrar sin permiso, ni ignorar la regla nueva) — preguntar al usuario
qué camino tomar antes de escribir.

## Regla Operativa

- Antes de escribir en un repo externo al vault, buscar y leer su
  `CLAUDE.md` / reglas de agente propias si existen.
- Si el contenido legacy contradice una regla vigente de ese repo, tratarlo
  como una decisión del usuario, no del agente: presentar las opciones
  reales (seguir en el legacy como excepción, migrar al esquema nuevo, u
  otra alternativa) y avanzar solo con la opción elegida.
- Registrar la decisión tomada en la nota del proyecto (Sistema 2) para que
  una futura sesión no vuelva a tropezar con la misma ambigüedad.

## Error Que Evita

Escribir specs/RFCs nuevos en un repo externo violando una política vigente
que el agente no había leído, o migrar contenido legacy a un esquema nuevo
sin que el usuario lo haya pedido, en ambos casos sin dar al usuario la
oportunidad real de elegir.
