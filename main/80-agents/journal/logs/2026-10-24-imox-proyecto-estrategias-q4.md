---
type: change_log
schema_version: 1
scope: session
created: "2026-10-24"
updated: "2026-10-24"
area: "[[Trading]]"
project:
application:
entities: ["[[Estrategias IMOX — Forex y CFD con Echo Forge]]", "[[IMOX]]"]
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: "local"
load_policy: "manual"
indexable: false
index_priority: "never"
tags: ["kind/change-log", "scope/session"]
---

# Proyecto de estrategias IMOX — Q4 2026

## Cambio

Proyecto humano raíz [[Estrategias IMOX — Forex y CFD con Echo Forge]] en Trading; contrato [[IMOX — Registro de campañas]], mapa [[IMOX — Cobertura de investigación]] y frente [[IMOX — NDX - Frente inicial]]. Skill federada `imox-strategy-research` y enlaces de navegación. No se modifica el planner técnico de Forge o Echo Futures ni se reasigna su ownership.

## Validación

Aplicación al pedido real: roadmap 24 octubre–31 diciembre con fases/gates, NDX primero, rescate 142 explícitamente diferido; no acceso a workers ni campaña ficticia. Activación positiva planificación/registro; negativa consulta aislada de indicador; adyacente preset delegado a `sqx144-campaign-design` y operación a owner técnico. YAML y referencias comprobados en cinco notas nuevas, enlaces resolubles. Lint federado dirigido sin errores/avisos tras retirar parent nulo de proyecto raíz. El validador portable rechaza las claves locales esperadas: aliases, area, created, entities, index_priority, indexable, load_policy, methodology_revision, related, schema_version, scope, tags, type, updated; no se quitó metadata para forzar compatibilidad. Graphify CLI no disponible; retrieval por búsqueda enfocada y referencias Markdown, sin índice generado dentro del vault. Sin prueba física de ejecución, porque la skill gobierna planificación y registro.

## Rollback

Retirar solo las cuatro notas/skill nuevas y revertir sus enlaces/entradas añadidos a índices/logs. Preservar publicaciones, fuentes y proyectos técnicos preexistentes.
