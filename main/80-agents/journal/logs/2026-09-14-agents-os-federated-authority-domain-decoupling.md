---
type: change_log
schema_version: 1
scope: session
created: "2026-09-14"
updated: "2026-09-14"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[AGENTS OS - Context Hygiene and Canonical Integrity]]"
  - "[[doctor-verde-falso-por-duplicados-core-federado]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-14-agents-os-domain-decoupling-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# AGENTS OS — autoridad federada y desacoplamiento de dominio

## Cambio

- **Tipo:** updated / deleted / created.
- **Archivo(s):** autoridad de skills y runbooks; bootstrap, constitución, context-router e índice; templates; core-export; conformance harness; canonical-linter CL-21; proyecto y memoria de soporte.

## Motivo

- Una migración incompleta mantenía 13 skills y 9 runbooks bajo dos raíces escribibles. El artefacto distribuido incluía policy operativa de dominio en startup, seis memorias Meli-scoped y templates que generaban metadata y paths Meli/Aranea en instalaciones DEFAULT.

## Fuentes usadas

- [[AGENTS OS - Context Hygiene and Canonical Integrity]], [[doctor-verde-falso-por-duplicados-core-federado]], `core-export/sources.list`, builder, routers y runbooks federados vigentes.

## Resolución aplicada

- `30-resources/` quedó como autoridad federada única; el registro opcional de dominios quedó fuera del core; el export proyecta sólo las skills portables seleccionadas y excluye seis memorias scoped completas; los templates quedaron DEFAULT-neutral; CL-21 impide reintroducir duplicados de identidad.
- El builder valida metadata y cuerpos ejecutables del artefacto, resuelve cada `area` distribuida y materializa 44 tipos canónicos en un vault DEFAULT temporal. Las excepciones son paths exactos con motivo, nunca patrones.
- `[[Personal]]` quedó como fallback resoluble de los templates compartidos. Consecuencia aceptable pero no invisible: una entidad destinada a Meli o Aranea queda en DEFAULT si el flujo scoped no ajusta `area`, tags y destino en el mismo cambio.

## Validación

- Cero duplicados de skill/runbook; Doctor fuente y export publicado `0/0/0`; export con 37 skills, nueve filas federadas, seis exclusiones scoped y 44/44 materializaciones DEFAULT; registry selftest PASS; canonical selftest 9/9; context-budget selftest 21/21; routing DEFAULT/Meli/Aranea y fail-closed sin FAIL nuevos.
- Prueba negativa: un placeholder de `area` no resoluble pasó el pre-render y fue rechazado post-render en la entidad materializada. Cero referencias estructuradas de dominio en los templates publicados.
- Revisión independiente reprodujo los gates y eliminó una entrada muerta del allowlist; sólo permanecen los dos fixtures que contienen metadata intencionalmente inválida.
- El L0 global conserva dos FAIL preexistentes fuera del slice: schema entrypoint y vocabulario `load_policy`.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** los artefactos distribuibles no incluyen identidad, paths locales, memoria interna, memoria scoped de un dominio ausente ni policy operativa de dominio.

## Rollback

- Restaurar en conjunto las copias retiradas, `sources.list`, builder, hot path, índice y harness. No revertir sólo la deduplicación o sólo el builder: rompería autoridad o descubribilidad.
