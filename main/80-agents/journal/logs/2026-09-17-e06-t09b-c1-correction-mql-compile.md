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

# 2026-09-17-e06-t09b-c1-correction-mql-compile

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo — E-06 Reference Enrollment and Binding.md` (nuevo bullet de estado `E06_T09B_C1_READY_FOR_MANAGER_REVIEW` + fila de la tabla Entrega de desarrollo actualizada a `fc2d4e5d` + nueva entrada de Bitácora)
  - `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-e06-t09b-c1-correction-mql-compile.md` (creado)
  - Repo `xKoRx/echo`: branch `feature/e06-reference-enrollment-binding` @ `fc2d4e5d` (push FF `4009db7a..fc2d4e5d`, sin merge/master) — `v3/clients/mt{5,4}/reference_v3.mq{5,4}` (C1-1 identidad fail-closed con tres estados de archivo inequívocos + validadores estrictos + relectura + intento único por OnInit; C1-2 elegibilidad del retry por vigencia restante del slot más antiguo incluido), `v3/clients/mt{5,4}/EchoCommon.mqh` (`EchoAttestV1_Scan` suma `outOldestRemainMs`, fuera del JSON contractual), `v3/sdk/domain/messages_test.go` (4 tests C1 nuevos), `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/{TASKS,VERIFICATION}.md` (T09b actualizado + evidencia §WP-C2 CORRECTION C1)

## Motivo

- Ejecución del mandato E-06 NORMAL T09b correction C1 (defectos detectados por Manager en `4009db7a`): C1-1 la identidad del collector no estaba garantizada ante errores de archivo (fallo de lectura tratado como ausencia ⇒ podía remintear UUID y sobrescribir; validaciones débiles; `FileWrite` sin verificar; durable sin relectura; retry por tick incrementaba epoch sin OnInit) y C1-2 `g_PendingStatusMsg` retransmitía hechos con atestaciones que ya habrán expirado (limitar a 15 s desde el build era insuficiente con una atestación de 14 s al capturarse). Prohibiciones respetadas: sin reiniciar T09b, sin avanzar T10/T11, sin Forge, sin `messages.go`/contrato T08/migration 064/Gateway/Bridge/contracts, sin FILE_COMMON/PG, sin escribir atestaciones, sin refrescar `ts`, sin claves wire nuevas, sin master/PR.

## Fuentes usadas

- SPEC v1.2.2 (`specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/SPEC.md` §§7.1/7.2/7.2a/7.5)
- TASKS.md T09b + corrección C1 WP-C1 (patrón de corrección sin reinicio); VERIFICATION.md §WP-C2/T09b
- Entity `[[Echo — E-06 Reference Enrollment and Binding]]` (baseline, allowed files, bitácora)
- Host de compilación autorizado `mt5-kronos.lab.aranea.cl` (evidencia física E-03 previa)

## Resolución aplicada

- C1-1: `FileIsExist` antes de cualquier `FileOpen` distingue inexistente (nacimiento) de existente-ilegible y corrupto (ambos fail-closed sin remint ni sobrescritura); `ReferenceValidUUIDv7` (formato completo lowercase, versión 7, variante) y `ReferenceValidEpochText` (decimal canónico sin overflow, `StringToInteger` prohibido) más chequeo de contenido extra; `FileWrite` verificado, flush/cierre y relectura completa antes de `g_RefIdentityDurable=true`; intento único en OnInit (epoch exactamente una vez por sesión; fallo ⇒ status deshabilitado toda la sesión; legacy TradeIntent/Close intocado).
- C1-2: `EchoAttestV1_Scan` reporta la vigencia restante del slot más antiguo EMITIDO con descuento conservador de la resolución 1 s de `ts` (`max(0, 15000−(age_s+1)·1000)`) fuera del JSON; el tick guarda instante+restante y evalúa caducidad antes de retransmitir: hecho vigente ⇒ mismos bytes/id; vencido ⇒ descarte sin transmitir y snapshot físico nuevo con id nuevo; hecho sin atestaciones no caduca por vigencia. Cero claves wire nuevas.
- MQL_COMPILE=PASS por primera vez en el proyecto: compilación real de ambos productores en `mt5-kronos.lab.aranea.cl` (MetaEditor64 5.0.0.6090 / metaeditor 5.0.0.2418, layout terminal con includes reales byte-exactos SHA-verificados): MT5 0 errors/1 warning (preexistente fuera del delta; ex5 hasheado) y MT4 0 errors/1 warning (preexistente del scanner; ex4 hasheado); sin deploy, sin terminales, sin órdenes; key SSH temporal de transferencia revocada y verificada.
- Sin probar expresamente (sin runtime MQL ejecutable): estados reales del archivo de identidad, relectura física y retry contra GVs reales — los tests Go son pines SOURCE + tablas de decisión espejo; PHYSICAL sigue GAP-ECHO-006.

## Validación

- `go test`/`go test -race ./v3/sdk/domain/` PASS (4 tests C1 nuevos + 11 de T09b); `go vet` OK; builds sdk/gateway/bridge OK; failing sets de `sdk/... bridge/... gateway/...` idénticos por nombre al baseline `4009db7a` corrido en worktree aparte (colateral preexistente automation/seed/scratch/jaeger) ⇒ cero regresiones; `go.mod`/`go.sum` delta 0; delta = exactamente los 7 archivos allowed.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales de máquina, memoria interna ni secretos (los paths del host de compilación son evidencia del proyecto, no rutas de vault)

## Rollback

- Repo: `git revert fc2d4e5d` (delta sobre la branch feature; master intocado). Vault: los tres archivos son adjuntos del mismo cambio; restaurar la fila de estado previa `E06_WPC2_T09B_READY_FOR_MANAGER_REVIEW @ 4009db7a`.
