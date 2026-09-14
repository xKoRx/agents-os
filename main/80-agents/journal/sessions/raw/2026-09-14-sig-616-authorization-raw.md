---
type: raw_session
schema_version: 1
scope: session
created: "2026-09-14"
updated: "2026-09-14"
area: "[[Meli]]"
project: "[[SIG-616 — Autorización de operaciones por equipo]]"
application:
entities:
  - "[[SIG-616 — Autorización de operaciones por equipo]]"
related:
  - "[[rio-playmaker]]"
aliases: []
confidence: verified
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-raw.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# SIG-616 — diseño de autorización por equipo (raw)

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: Codex.
- Proyecto o entidad: [[SIG-616 — Autorización de operaciones por equipo]].
- Objetivo de la sesión: entender SIG-616, ubicar su alcance en el código y registrar el diseño inicial solicitado por el owner.

## Transcript

```text
Usuario: pidió revisar SIG-616 en Spellbook y explicar alcance e impacto en Playmaker y los control planes.
Agente: leyó SIG-616 y el código de rio-playmaker; identificó que cubre actions, componentes, relaciones, pipelines, deployments e inactivación, con enforcement en Playmaker.
Usuario: pidió un diseño SOLID y reusable, sin un service de negocio transversal usado por otros services.
Agente: propuso separar validación Tiger/ACME de un helper/guard que aplique políticas estáticas por operación.
Usuario: precisó que acepta un service para Tiger/ACME y preguntó dónde vive el team.
Agente: verificó que el team vive en DataProduct.teamName; Component referencia su Data Product y sourceComponentId representa procedencia de importación.
Usuario: pidió crear el proyecto en el vault, dejando el diseño inicial y la referencia a la SPEC, y cerrar sesión con feedback.
```

## Evidencia externa

- [SIG-616 — Spellbook](https://spellbook.adminml.com/projects/SIG/specs/SIG-616)
