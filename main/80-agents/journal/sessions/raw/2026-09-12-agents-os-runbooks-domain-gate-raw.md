---
type: raw_session
schema_version: 1
scope: session
created: "2026-09-12"
updated: "2026-09-12"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[2026-09-12-agents-os-runbooks-domain-gate-summary]]"
related: []
aliases:
  - "runbooks y domain gate"
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

# 2026-09-12-agents-os-runbooks-domain-gate-raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: [[ZCode]] × GLM-5.3-Flash (continuación de la sesión de restructura de skills)
- Proyecto o entidad: [[AGENTS OS]]
- Objetivo de la sesión: verificar mudanza de skills; replicar la restructura en runbooks; diseñar e implementar la carga inteligente por dominio; cierre con feedback.

## Transcript

```
Usuario: moviste los archivos donde correspondía no?? no quedaron skills raras por ahi?? por otra parte necesito que hagas lo mismo con los runbooks. deja los de agents os solo en agents os, los demas se deben ir a resources a una carpeta de runbooks.

Agente: verificación limpia (28 core + 19 federadas, sin sobrantes). git mv de 10 runbooks + symphony/ a 30-resources/runbooks/; quedaron 5 agents-os en memory/public/runbook/. Duplicado mismo-día signals-code-review.md vs -runbook.md resuelto (superseded). Índice wiki 00-index.md + log.md; refs actualizadas (aranea-mcps-expert, signals-code-review, ml-ia, agents/00-index); dominio runbooks activado en 00-RESOURCE-WIKI. Doctor detectó ref relativa rota; corregida; HIGH=0.

Usuario: como carga la wea ahora? tanto los runbooks como los skills quedaron con index?

Agente: skills → INDEX.md en cold start; runbooks → índice wiki lazy, se llega vía skill; los 5 de AGENTS OS por path directo desde skills del core.

Usuario: me gustaria hacer algun mecanismo de carga inteligente en el context router... skills especialistas meli/aranea según el prompt inicial... 3 opciones... que meli no cargue weas de aranea ni viceversa. como lo ves?

Agente: gate de evidencia en bootstrap (dueño del startup), no en context-router; 3 salidas con fail-closed; señales: MCP prefixes, entidades, repo identity; defensa en profundidad (gate → router → skill con gate propio).

Usuario: es que todas las notas en el vault deben tener area, de ahi se saca, ademas los proyectos tambien tienen.

Agente: verificado con datos (80 proyectos, 32 aplicaciones con area; anomalía [[Symphony]] corregida a [[Echo]]). Implementado: paso 6 del cold start = domain gate por area ([[Meli]] → meli-agent-dev; [[Echo]]/[[Aranea]] → aranea-agent-dev; otra/ausente → sin router; ambiguo falla cerrado); entity swap re-aplica gate y reemplaza pack; context-router.md línea conceptual; change_log.

Usuario: vale, quedo todo lo demas listo no? graphify tambien no?

Agente: estructural listo y validado; graphify listo a nivel contractual pero binario no instalado en kor (sin wheel ni AGENTS_OS_GRAPHIFY_SOURCE) — validación física del índice pendiente.

Usuario: vale cierra sesion y deja feedback.
```

## Evidencia externa

- Ninguna; trabajo íntegro sobre el vault.
