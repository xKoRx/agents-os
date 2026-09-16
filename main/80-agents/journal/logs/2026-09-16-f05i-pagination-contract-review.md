---
type: change_log
schema_version: 1
scope: session
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Echo Forge]]"
project: "[[Echo Forge — F-05-I Cohesive release and read surfaces]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[Echo Forge — F-05-I Release Matrix and Read Surface Contract]]"
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

# 2026-09-16-f05i-pagination-contract-review

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - [[Echo Forge — F-05-I Cohesive release and read surfaces]]: entrada de bitácora con el review/decisión F05I-PAGINATION-C1 (tareas intactas: T6 permanece `[r]`, nada Done).
  - [[80-agents/journal/agent-runs/2026-09-16-zcode-glm-5.3-flash-f05i-pagination-contract-review.md]] (nuevo, materializado vía `materialize_schema_note.py`).
  - Repo `xKoRx/symphony`: SIN cambios (misión de sólo lectura; corrección especificada, no implementada).

## Motivo

- Manager review de T6 @ `1a1926a` bloqueada por contradicción: checklist C1 exige "recorrer todas las páginas usando los cursores retornados", pero `sqx-campaign-list.v1` sólo expone `schema`+`campaigns[]` (`sqx/core/forge/inspect.go:131`), `runCampaignList` no emite cursor (`sqx/cmd/sqx-flowkit/inspect.go:215`) y `encodeCampaignCursor` tiene cero callers productivos (sólo el codec test). Receta inejecutable vía contrato público; además los docs llaman "opaco" al cursor y a la vez documentan su encoding (`f05-read-surface.md:34/81`).

## Fuentes usadas

- SPEC [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]] (read surface contract, C1.6, exit codes).
- Source @ `1a1926a`/`cbf520b`: `sqx/core/forge/inspect.go`, `sqx/core/capabilities/forge_inspect_query.go`, `sqx/adapters/registry-postgres/forge_campaign_list.go` (+test traversal), `sqx/cmd/sqx-flowkit/inspect.go` (+tests).
- Docs T6 `docs/echo-forge/{f05-read-surface.md,f05-conformance-checklist.md,f05-certification-manifest-template.json}` y proyecto F-05-I.

## Resolución aplicada

- **Veredicto:** `PASS — OPTION A — SERVER-ISSUED OPAQUE CURSOR`. Contrato final `sqx-campaign-list.v1` (aditivo pre-release, permanece v1 — nunca publicada): campo `next_cursor: string | null` SIEMPRE presente, generado por el servidor; algoritmo: query keyset con `LIMIT N+1`; si hay N+1 filas → emitir N y `next_cursor = encode(última fila emitida)`; si ≤N → `next_cursor = null` (exacto: null ⟺ no existe fila posterior al boundary al momento de la query; una página llena nunca va seguida de vacía por construcción). Página vacía sigue válida (exit 0, `campaigns: []`, `next_cursor: null`). El consumidor NO construye ni interpreta el token; el encoding base64url-JSON queda documentado informativamente como detalle reservado del servidor. Empates `created_at` correctos por el boundary (created_at, ref) + predicate T2 ya aprobado. Determinismo preservado (token derivado de fila durable). Sin cambios de port ni adapter (T2/T3 frozen); `encodeCampaignCursor` gana su caller productivo.
- **Impacto especificado:** source a cambiar: `sqx/core/forge/inspect.go` (campo + probe N+1 + codec movido desde cmd), `sqx/cmd/sqx-flowkit/inspect.go` (delegar codec; decode sigue PRE-BOOT → cursor inválido exit 2 sin infra); tests: `inspect_test.go` de forge (probe/boundary/token) y de flowkit (codec, golden de página vacía `{"schema":"sqx-campaign-list.v1","campaigns":[],"next_cursor":null}\n`, nuevo walk por next_cursor retornado); adapter test SIN cambios. Docs T6: read-surface §2.2/§1/ejemplo vacío; checklist C1 (receta con cursores retornados, ahora ejecutable literal), C3 bytes, I5 golden; manifest template SIN cambios.
- **D1:** wording, no código — `run get` expone `schema_version` (`ForgeResult`, modelo F-02 congelado, NO se renombra); corregir la frase general "campo `schema` obligatorio" en `f05-read-surface.md:19` y SPEC indicando la excepción.
- **D2:** excepción explícita — "flags/ruta de éxito/códigos propios (0/2/20/30/40/50) byte-idénticos, salvo el único delta pre-dispatch aprobado (SPEC C1.6): boot global fallido (etcd caído) pre-parseo pasaba de exit 1 a exit 10 `config_error` dentro de push-output" en `f05-read-surface.md:37` y checklist H1 (H2 ya lo documenta).
- **Reaperturas:** T4 SÍ formal (delta en `InspectService.Campaigns` + shape del documento, ya manager-approved); T5 scope extendido (sigue Review); T2/T3 NO; T6 aplica correcciones dentro de su Review; T7 continúa después del fix, sin rediseño.

## Validación

- Desk review: baseline verificado `1a1926a` en `codex/f05-release-prep`, dirty ajeno preservado; evidencia anclada a file:line; cero ejecución de tests/certificación requerida por el brief (No implementar / No certificar).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Eliminar la entrada de bitácora añadida al proyecto F-05-I, este log y el agent-run asociado. El repo no fue tocado.
