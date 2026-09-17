---
type: change_log
schema_version: 1
scope: session
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Echo]]"
project: "[[Echo Forge — F-05-I Cohesive release and read surfaces]]"
application:
entities:
  - "[[Echo Forge]]"
related: []
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

# 2026-09-16-f05i-pagination-c2-server-issued-cursor

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - Repo `xKoRx/symphony` @ `codex/f05-release-prep` (commit atómico sobre `1a1926a`, push normal): `sqx/core/forge/inspect.go` (shape `CampaignListDocument` + `next_cursor *string` sin omitempty; N+1 en `InspectService.Campaigns` con validación pre-reader de limit y overflow; codec `EncodeCampaignCursor`/`DecodeCampaignCursor`), `sqx/core/forge/inspect_test.go` (casos A–G + traversal hermético `TestInspectServiceCampaignsKeysetTraversalUsesReturnedCursorOnly`), `sqx/cmd/sqx-flowkit/inspect.go` (CLI sin codec local; `runCampaignList` decodifica con `forge.DecodeCampaignCursor`), `sqx/cmd/sqx-flowkit/inspect_test.go` (golden vacío con `next_cursor: null`; guard estructural sin segunda implementación de encoding), `sqx/cmd/sqx-flowkit/inspect_golden_test.go` (golden `sqx-campaign-list.v1` con `next_cursor: null`), `docs/echo-forge/f05-read-surface.md` y `docs/echo-forge/f05-conformance-checklist.md` (correcciones F05I-PAGINATION-C2).
  - [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]]: campo de versión con excepción ForgeResult `schema_version`; semántica server-issued opaque cursor + N+1 en campaign list; estado de branch y tablero.
  - [[Echo Forge — F-05-I Cohesive release and read surfaces]]: bitácora de la implementación y tablero (T4 `[r]` por delta pagination; T5/T6 `[r]`; T7 bloqueada hasta manager review del fix).
  - [[80-agents/journal/agent-runs/2026-09-16-zcode-glm-5.3-flash-f05i-pagination-c2-implementation.md]] (nuevo, materializado vía `materialize_schema_note.py`).

## Motivo

- Implementar la decisión contractual frozen de F05I-PAGINATION-C1 (`PASS — OPTION A — SERVER-ISSUED OPAQUE CURSOR`), aceptada por manager, que corrige el gap pre-release detectado en la manager review de T6: `sqx-campaign-list.v1` no exponía cursor, haciendo inejecutable la receta C1 del checklist.

## Fuentes usadas

- SPEC [[Echo Forge — F-05-I Release Matrix and Read Surface Contract]] y proyecto F-05-I (estado y contratos frozen).
- Source @ `1a1926a`: `sqx/core/forge/inspect.go`, `sqx/core/capabilities/forge_inspect_query.go` (port, sin cambios), `sqx/adapters/registry-postgres/forge_campaign_list.go` (adapter, sin cambios), `sqx/cmd/sqx-flowkit/inspect.go` + tests + golden, docs T6.
- Change_log previo `2026-09-16-f05i-pagination-contract-review` (contrato completo de la decisión).

## Resolución aplicada

- `next_cursor` (`string | null`, SIEMPRE presente) server-issued: probe `LIMIT N+1`, emite N, cursor del boundary = última fila EMITIDA, null exacto cuando no hay fila posterior; consumidor pass-through puro. Codec en core (`sqx/core/forge`), misma codificación base64url de JSON compacto (RFC3339Nano, ref); Encode valida el boundary; boundary durable inválido ⇒ `CONTRACT_INCONSISTENCY`. Validación de `limit ≥ 1` y overflow movida al service ANTES del reader (regresión `limit=0` cerrada). CLI consumidor/composición sin dueño del protocolo. Docs y SPEC alineadas (D1 wording `schema_version`, D2 BWC push-output acotada al delta pre-dispatch aprobado). Sigue `sqx-campaign-list.v1` (F-05-I nunca released; sin v2). Sin migration, sin cambio de port ni adapter/SQL, sin `internal/di`, sin release-matrix, sin ForgeResult, sin push-output, sin gates físicos.

## Validación

- gofmt OK · `go test ./sqx/core/forge/...` PASS · `go test ./sqx/cmd/sqx-flowkit/...` PASS · `go test ./sqx/adapters/registry-postgres/... -run TestListForgeCampaigns` PASS · `-race` PASS · `go vet` PASS · `go build ./sqx/cmd/sqx-flowkit/...` PASS · `git diff --check` OK · `go build ./sqx/...` falla sólo en `sqx/tools` (mains duplicados BASELINE_KNOWN preexistentes). Baseline `1a1926a` ancestro; dirty ajeno `specs/FEAT-SQX-STRATEGY-EVALUATION/fixtures/phase4_performance.json` preservado intacto.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revert del commit de la corrección en `codex/f05-release-prep` restaura el contrato previo (`1a1926a`); las notas del vault registran ambos estados y el tablero vuelve con el revert. Ningún efecto físico: sin release, deploy ni certificación.
