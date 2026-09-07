---
type: session
scope: session
created: "2026-06-30"
updated: "2026-07-01"
area: "[[Meli]]"
project: "[[Destaques de Precio]]"
application:
entities:
  - "[[Destaques de Precio]]"
  - "[[Bajó de Precio]]"
  - "[[Bajo y Muy Bajo Precio]]"
related:
  - "[[AGENTS OS]]"
aliases:
  - rfc pricing motors fipe mlb summary
confidence: high
source_session: "80-agents/journal/sessions/raw/2026-06-30-rfc-pricing-motors-fipe-mlb-hitos-raw.md"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
  - area/meli
---

# 2026-06-30 - RFC Pricing Motors, pivot FIPE MLB y organizacion por hitos - summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Reportar el avance del RFC de Destaques de Precio (segunda parte del proyecto Previous Price) via AGENTS OS.
- Incorporar al RFC una decision de reunion sobre un problema de calidad de datos FIPE en MLB, con pivot de diseno para ese site.
- Reordenar el RFC en Hito 1 (Bajo de Precio) e Hito 2 (Destaques de Precio), en ese orden.
- Dejar como tarea pendiente del subproyecto Bajo de Precio la reconciliacion entre documentacion e implementacion real.
- Cerrar la sesion siguiendo el protocolo de AGENTS OS.

## Contexto cargado

- AGENTS OS: guia operativa (`agents-os.md`), constitucion y perfil de usuario (via bootstrap).
- Graphify: query `"Destaques de Precio Bajo y Muy Bajo avance RFC"` para ubicar las entidades canonicas.
- Entidades Sistema 2: [[Destaques de Precio]] (iniciativa), [[Bajó de Precio]] (Hito 1), [[Bajo y Muy Bajo Precio]] (Hito 2, tiers via Sugeridor).
- RFC externo (fuera del vault, en repo compartido del squad): `01_Projects/previous-price-motors/rfc.md`.
- Reglas del repo `sb-main` (`CLAUDE.md`, `.claude/rules/sdd-process.md`): RFC/specs deberian vivir en Google Docs/Spellbook, no como `.md` local; el `rfc.md` actual es legado segun esa politica, pero sigue siendo el documento de trabajo real y no se migro en esta sesion (fuera de alcance del pedido).

## Trabajo realizado

- Se identifico el proyecto activo via Graphify + lectura de entidades y se reporto el estado (Hito 1 en code review, Hito 2 en fase de propuesta/RFC).
- Se incorporo al RFC una seccion nueva "Problema de Catalogacion FIPE en MLB (pivot 2026-06-30)" con el contexto de la reunion (calidad de datos FIPE, comentario de Cris sobre vehiculos verificados, dos ideas planteadas) y la decision resultante (MLB pasa a un destaque unico basado en FIPE; el resto de los sites mantiene Sugeridor 2.0 con dos tiers).
- Se marco explicitamente como placeholder/no confirmado el rango -10%/-1% mencionado en la reunion, evitando presentarlo como regla definitiva.
- Se propago el fork por site a las secciones de Alcance, Principios de Diseno, Sugeridor 2.0, Reglas de Destaques, Labels, Contrato Persistido, Proceso Masivo, Cambios por Componente, Rollout, Riesgos y Pendientes de Definicion.
- Se reestructuro el RFC completo en dos hitos ordenados: Hito 1 - Bajo de Precio (Estado Implementado + Experimentos) primero, Hito 2 - Destaques de Precio (Sugeridor, problema FIPE, reglas, proceso masivo, componentes, rollout) despues. Antes, la seccion de estado implementado de Hito 1 aparecia despues de todo el diseno de Hito 2.
- Se agrego una tarea pendiente en el subproyecto [[Bajó de Precio]] para reconciliar el RFC (seccion Estado Implementado) con el estado real de implementacion/despliegue por componente.
- Se actualizaron bitacoras y decisiones de [[Destaques de Precio]] y [[Bajo y Muy Bajo Precio]] para reflejar el pivot y el nuevo alcance (MLB fuera del esquema de tiers via Sugeridor).

## Artifacts creados o modificados

- `01_Projects/previous-price-motors/rfc.md` (fuera del vault): reescrito completo, mismo contenido base + pivot FIPE MLB + reorganizacion por hitos.
- Obsidian: [[Destaques de Precio]], [[Bajó de Precio]], [[Bajo y Muy Bajo Precio]] (bitacora, decisiones, tareas, `updated:` en frontmatter).
- AGENTS OS: L0 raw session, este L1 summary, feedback general, feedback Graphify, change logs de entidad y de memoria publica, posible ajuste de `rjara-agent-profile.md`.

## Memoria propuesta o creada

- Se propone agregar una preferencia de trabajo estable a `rjara-agent-profile.md` (Sistema 1): marcar explicitamente como placeholder cualquier cifra/regla que el usuario indique como inventada/de ejemplo en una reunion, y organizar documentos con hitos secuenciales explicitamente por hito y en orden. Confianza `verified` (instruccion explicita del usuario, aplicada con evidencia directa en el RFC resultante).
- No se crea ADR ni known error nuevo: el pivot FIPE-MLB es conocimiento de dominio del proyecto (Sistema 2), ya reflejado directamente en las entidades y en el RFC.

## Decisiones

- MLB (Hito 2): destaque unico basado en precio FIPE, no en Sugeridor 2.0. Resto de sites: sin cambios, dos tiers via Sugeridor 2.0, sin FIPE.
- El rango de elegibilidad -10%/-1% para MLB queda documentado como ilustrativo, no confirmado.
- El RFC se organiza y se debe seguir organizando por hito, en orden (Hito 1 antes de Hito 2).
- El gap de documentacion-vs-implementacion de Hito 1 se gestiona como tarea pendiente del subproyecto [[Bajó de Precio]], no como edicion retroactiva silenciosa del RFC.

## Pendiente

- Todas las nuevas definiciones abiertas por el pivot FIPE (fuente tecnica del precio FIPE, rango real de elegibilidad, wording final, ETA de la lista marca/modelo/año, trigger de reproceso para MLB) quedan listadas en el RFC bajo "Puntos abiertos (MLB)" y "Pendientes de Definicion".
- Reconciliar el RFC (Hito 1, Estado Implementado) con el estado real de implementacion — tarea pendiente en [[Bajó de Precio]].
- Evaluar si conviene tambien actualizar las specs tecnicas de Search/VIP (`Destaques de Precio — Polycard Search/VIP — Spec Tecnica Propuesta.md`) para reflejar el fork FIPE/MLB; no se tocaron en esta sesion por alcance explicito del pedido del usuario.
- Reindexar Graphify tras estos cambios y validar con una query enfocada.

## Addendum 2026-07-01 - correccion de alcance padre/hijo

- El usuario corrigio: `[[Bajo y Muy Bajo Precio]]` es la "parte 2" del RFC / **Hito 2 completo** (fase de diseno), no solo el esquema de tiers via Sugeridor. Incluye tanto el destaque unico FIPE de MLB como los 2 tiers via Sugeridor del resto de sites, ambos dentro de este mismo proyecto.
- Se corrigieron `Bajo y Muy Bajo Precio.md` y `Destaques de Precio.md` (ver `80-agents/journal/logs/2026-07-01-bajo-y-muy-bajo-precio-scope-correction-entity-updated.md`).
- Se promovio a aprendizaje L3 el patron de error (asignar contenido nuevo al proyecto padre en vez de verificar el hijo real): `80-agents/memory/public/learning/agents-os/verify-parent-child-project-ownership-before-splitting-content.md`.
- Nota de fecha: esta sesion mezclo referencias a `2026-06-30` (fecha usada para el pivot FIPE, asumida sin confirmacion explicita del usuario) y `2026-07-01` (fecha real de sistema en el momento de esta correccion). No se hizo un barrido retroactivo de fechas por estar fuera del alcance pedido; si el usuario confirma la fecha real de la reunion, corregir en una proxima sesion.
