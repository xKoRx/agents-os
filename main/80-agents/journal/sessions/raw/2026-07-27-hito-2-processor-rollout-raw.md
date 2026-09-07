---
type: raw_session
scope: session
created: "2026-07-27"
updated: "2026-07-27"
area: "[[Meli]]"
project: "[[Implementación Hito 2 - Destaques de Precio]]"
application: "[[vis-items-loader-tagging]]"
entities:
  - "[[Hito 2 - vis-items-loader-tagging]]"
related:
  - "[[Bajó de Precio]]"
aliases: []
confidence: verified
source_session:
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
  - area/meli
---

# Hito 2 — Processor estándar y rollout

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: Codex
- Proyecto o entidad: [[Hito 2 - vis-items-loader-tagging]]
- Objetivo de la sesión: corregir el diseño unitario para reutilizar las
  capabilities existentes y cerrar la sesión.

## Transcript

**Usuario**

> me parece bien, solo que lo de signals no me gustó.. no quiero agregar
> capabilities nuevas porque necesito salir rápido con lo que ya hay. me
> gustaría crear un process paralelo al actual, con el RO destaque de precio
> que se ejecute el nuevo con todas las reglas y el de discount price de manera
> deprecada para que procese la cola de mensajes que aún den vuelta por ahí, en
> un segundo despliegue eliminar el procesor discount price y dejar el nuevo que
> contempla esta lógica. me parece bien aislar las responsabilidades en
> servicios utils, helpers, o la wea que más se ajuste a la arqui del repo. así
> que rehace esta parte para que reutilice las capabilities actuales y no
> intente crear un nuevo concepto. luego cierra sesión

**Resolución aplicada**

- Se eliminó `signals` del diseño.
- Se definió `vehicle_price_highlight_motors` como processor estándar que
  ejecuta las tres reglas.
- Se preserva temporalmente `price_before_discount_motors` solo para drenaje.
- El segundo despliegue retira únicamente la instancia/configuración Motors
  antigua, sin afectar Real Estate.
- Se actualizaron el proyecto de agente, el proyecto padre y la continuidad
  técnica; no se modificó código.

## Evidencia externa

- Plan validado con 3 fases, 3 gates y 0 errores.
- Repositorio inspeccionado en `feature/price-drop-motors-backfill`,
  HEAD `fbb1bbf0`; working tree del usuario preservado.
