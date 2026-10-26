---
type: change_log
schema_version: 1
scope: session
created: "2026-10-24"
updated: "2026-10-24"
area: "[[Trading]]"
project:
application:
entities: ["[[IMOX]]"]
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

# SQX 144 — Puesta al día y skill de diseño

## Cambio

Cinco recursos/fuentes adicionales IMOX, [[IMOX - Empezar con SQX 144 - Metodología y primera campaña]], actualización de índice/síntesis, y skill federada `30-resources/agents/skills/sqx144-campaign-design/SKILL.md`, enlazada en los índices de skills y agents. Se conserva una única fuente física de la skill; no se instala copia en carpetas de cliente.

## Validación

Clasificación skill: procedimiento reutilizable de diseño, separado del conocimiento humano en la guía y de ejecución técnica. Aplicación al caso real de Rodrigo: con migración declarada y sin catálogo exportado produce la guía de arranque, hipótesis/faltantes y cero presets supuestamente probados. No se ejecutó minado. Revisión de activación: positiva diseño de primera campaña; negativa consulta aislada de un indicador; adyacente operación de Forge con handoff a su procedimiento. Validación federada: lint dirigido sin errores/avisos y YAML estricto válido. El diagnóstico `quick_validate.py` del perfil portable rechaza las claves locales esperadas: aliases, area, created, entities, index_priority, indexable, load_policy, related, schema_version, scope, tags, type, updated; no se retiraron para forzar compatibilidad. No hay openai.yaml opcional. Aplicación manual al caso real y tres límites de activación revisados; sin prueba física de importación/exportación. Se añadió la sección Catálogo requerida que faltaba previamente en el índice de skills tocado. No se presenta como probada en una instalación SQX real.

## Rollback

Retirar únicamente los nuevos recursos/fuentes/skill y revertir las filas/párrafos de esta ingesta, preservando las anteriores y cambios ajenos. No hay estado de producción modificado.
