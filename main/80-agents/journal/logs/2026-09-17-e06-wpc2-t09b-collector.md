---
type: change_log
schema_version: 1
scope: session
created: "2026-09-17"
updated: "2026-09-17"
area: "[[Echo]]"
project: "[[Echo — E-06 Reference Enrollment and Binding]]"
application: "[[xKoRx/echo]]"
entities:
  - "[[Echo — E-06 Reference Enrollment and Binding]]"
related:
  - "[[Echo — Live Platform V1]]"
  - "[[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]"
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

# 2026-09-17-e06-wpc2-t09b-collector

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — E-06 Reference Enrollment and Binding.md` (nuevo bullet de estado `E06_WPC2_T09B_READY_FOR_MANAGER_REVIEW` + fila de la tabla Entrega de desarrollo actualizada a `4009db7a` + nueva entrada de Bitácora)
  - `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-e06-wpc2-t09b-reference-collector.md` (creado)
  - Repo `xKoRx/echo`: branch `feature/e06-reference-enrollment-binding` @ `4009db7a` (push FF `32332c04..4009db7a`, sin merge/master) — `v3/clients/mt{5,4}/EchoCommon.mqh` (helpers read-only §7.2a: ACCOUNT_SERVER, FNV-1a32, GV entera, UTF-8 estricto, hex16, grammar, `EchoAttestV1_Scan`), `v3/clients/mt{5,4}/reference_v3.mq{5,4}` (identidad durable collector_id/epoch en sandbox Files, inventario MT5/MT4, builder `reference_status`, retry del mismo hecho, hooks OnInit/OnTimer), `v3/sdk/domain/messages.go` (+`ReferenceStatusPayload`/`ParseReferenceStatus`), `v3/sdk/domain/messages_test.go` (nuevo, 11 tests), `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/{TASKS,VERIFICATION}.md` (T09b `[x]` + evidencia §WP-C2/T09b)

## Motivo

- Ejecución de la misión E-06 NORMAL WP-C2 / T09b (mandato del Manager tras aceptar WP-C1 C1): extender los collectors Reference MT5/MT4 para emitir periódicamente `type=reference_status` por el named pipe existente con inventario físico zero-order y retransmisión read-only de las atestaciones runtime §7.2a de SPEC v1.2.2, más el parser Go compatible con el contrato T08. Prohibiciones respetadas: sin T10/T11+, sin Forge, sin contracts/migrations 061–064, sin Gateway/Bridge/Core/ClientConfig, sin OrderSend/comandos, sin escribir atestaciones (`GlobalVariableSet`/`Del`/`Time` = 0 en el delta), sin backfill desde config/PG, sin FILE_COMMON, sin master/PR.

## Fuentes usadas

- SPEC v1.2.2 (`specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/SPEC.md` §§7.1/7.2/7.2a.1–7.2a.6, AC-26/27/36/37a)
- TASKS.md T09b; contrato T08 (`v3/sdk/domain/reference_readback.go`)
- Entity `[[Echo — E-06 Reference Enrollment and Binding]]` (baseline, allowed files, bitácora)

## Resolución aplicada

- Identidad del collector persistida en el sandbox Files del terminal (mismo almacenamiento local que TradeMapper) con fail-closed ante archivo corrupto/escritura fallida (status deshabilitado, nunca id inestable); epoch = contador persistido + 1 por OnInit.
- Retry del mismo hecho por bytes retenidos (mismo `source_event_id`); snapshot nuevo ⇒ identidad nueva; buffer FIFO sin adelantar snapshots.
- Inventario UNKNOWN con fallo de scan: conteos ausentes (pointers) y sin array parcial — jamás parcial como KNOWN; magic 0 excluido de `observed_magic` (no es canónico; T08 lo rechazaría).
- Ventana de vigencia congelada como `#define ECHO_ATTEST_FRESHNESS_MS 15000` y pinada desde tests Go contra el MQL real (CONTRACT/SOURCE; `MQL_COMPILE=NOT_RUN` sin compilador en el entorno; `PHYSICAL=PENDING` GAP-ECHO-006).

## Validación

- `go test` y `go test -race ./v3/sdk/domain/` PASS (11 tests nuevos; golden zero-order; `TestAttestation_TicklessWindow_SlotExpires` AC-37a); `go vet` OK; builds sdk/gateway/bridge OK; failing sets skip-mode de bridge/gateway/sdk idénticos por nombre al baseline `32332c04` en worktree aparte ⇒ cero regresiones; grep tokens prohibidos = 0 pinado en test.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Repo: `git revert 4009db7a` (delta aditivo sobre la branch feature; master intocado). Vault: los tres archivos son adjuntos del mismo cambio; restaurar la fila de estado previa `E06_WPC1_C1_READY_FOR_MANAGER_REVIEW @ 32332c04`.
