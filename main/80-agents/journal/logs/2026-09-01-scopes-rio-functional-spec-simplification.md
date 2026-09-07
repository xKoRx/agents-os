---
type: change_log
schema_version: 1
scope: session
created: "2026-09-01"
updated: "2026-09-01"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application:
entities: []
related:
  - "[[scope-naming-standard]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-01-scopes-rio-functional-spec-simplification

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - Spellbook `SIG-599` — reescritura del contenido funcional; conserva título, tipo y estado `draft`.
  - `10-projects/Meli/Estandarización de Scopes RIO/Estandarización de Scopes RIO.md` — estado y decisiones vigentes alineados con el SPEC.

## Motivo

- Simplificar el contrato para que cualquier integrante de Signals entienda cómo una misma identidad de ambiente se mantiene a lo largo del flujo, sin mezclar la solución de plataforma.

## Fuentes usadas

- Solicitud del owner del proyecto: scopes de frontend simples por ambiente; backend con tipos claros `api` y `consumer`; detalle técnico reservado para el SPEC técnico.
- [SIG-599](https://spellbook.adminml.com/specs/d11690fe-cb01-4869-97e9-18addb3d013c) y estado canónico de [[Estandarización de Scopes RIO]].

## Resolución aplicada

- La verdad funcional vigente usa `production`, `staging`, `alpha`, `beta` y `gamma`.
- Frontend se nombra únicamente con el ambiente; backend usa `<environment>-api` y `<environment>-consumer` según la función que cumple la aplicación.
- `consumer` se eligió sobre `bq` porque expresa una responsabilidad funcional estable y no una tecnología de transporte.
- El ambiente efectivo de backend forma parte de la identidad de la operación y debe conservarse en llamadas, eventos, reintentos y resultados; una inconsistencia falla de forma explícita.
- Segmentos Fury, headers, cookies, tópicos, filtros, aprovisionamiento y migración quedan en el futuro SPEC técnico.
- El Grid conserva su contenido actual como inventario/propuesta física; no se modificó y no reemplaza el contrato funcional.
- Este delta actualiza una decisión vigente de la entidad Sistema 2 [[Estandarización de Scopes RIO]]; no corresponde a memoria de comportamiento del agente.

## Validación

- Spellbook releyó `SIG-599` después del `PUT`: UUID, número, título, tipo y estado correctos; contenido remoto idéntico byte a byte al Markdown publicado (`11343` bytes).
- Scan test y mental-model test de `human-first-technical-writing`: el camino principal queda `problema → modelo → nombres → continuidad → aceptación` y no depende de conocer la implementación actual.
- Verificación textual: el contrato funcional no usa `prod`, `stage`, `nonprod`, `nonsite` ni `bq` como nombres de scopes objetivo.
- Lint estricto de la entidad y este change log: `ERROR=0`, `WARN=0`. `graphify-obsidian update` quedó bloqueado antes de indexar por 25 errores y 6 warnings de frontmatter preexistentes en fuentes no modificadas; el Markdown canónico sí quedó actualizado.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Restaurar una versión anterior de `SIG-599` desde el historial de Spellbook y revertir el delta del proyecto si el equipo rechaza este contrato.
