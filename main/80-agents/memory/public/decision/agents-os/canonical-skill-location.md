---
type: decision
scope: global
created: 2026-07-14
updated: 2026-07-14
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-install]]"
  - "[[AGENTS OS - Beta y Hardening]]"
aliases:
  - canonical skill location
  - ubicación canónica de skills
confidence: verified
source_session:
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/global
  - project/agentsos
  - tech/agents-os
---

# Skills de AGENTS OS viven en una única fuente canónica

## Contexto

- Los adapters o copias por cliente hacen portable el discovery a costa de
  crear fuentes físicas divergentes y estado fuera del sistema compartible.

## Decisión

- Toda skill de AGENTS OS vive físicamente sólo en
  `80-agents/skills/<skill>/`.
- Codex, Claude y otras superficies reciben reglas que las dirigen al
  `SKILL.md` canónico; no reciben copias, symlinks ni adapters.
- El discovery nativo de cada cliente se mide como capacidad u optimización de
  la superficie. Su ausencia no autoriza una segunda fuente.
- Metadatos específicos de una superficie pueden vivir dentro de la carpeta
  canónica de la skill cuando no duplican su procedimiento.

## Rationale

- Mantiene una sola fuente versionable, auditable y portable junto al vault.
- Evita drift entre clientes y permite mejorar una skill una sola vez.
- Separa la verdad del sistema de las capacidades de discovery de cada agente.

## Consecuencias

- La instalación configura reglas y elimina sólo adapters antiguos que AGENTS
  OS pueda identificar como generados por él.
- Los forward-tests deben comenzar en procesos frescos: una sesión abierta
  puede conservar un catálogo anterior en memoria.
- Sigue pendiente comparar rule-routing, path explícito y discovery nativo por
  tokens, latencia y tasa de éxito.

## Alternativas descartadas

- Copias o adapters por cliente: descartados por duplicación y riesgo de drift.
- Symlinks: descartados por portabilidad y diferencias entre máquinas.
- Carpetas globales de Codex o Claude como fuente: descartadas porque separan
  las skills del sistema que las gobierna.

## Validación

- Codex y Claude localizaron por nombre una skill canónica en smoke tests
  read-only sin copias por superficie.
- El instalador dejó de crear adapters y Graphify dejó de indexar el generador
  eliminado.
- La ejecución real y el benchmark de discovery permanecen en
  [[AGENTS OS - Beta y Hardening]].
