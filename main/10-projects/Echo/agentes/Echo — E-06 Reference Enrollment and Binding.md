---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo — Live Platform V1]]"
sprint:
start: 2026-09-16
due:
progress: 15
repo: xKoRx/echo
jira:
prs:
aliases:
  - Echo E-06
  - Reference enrollment and binding
  - E-06 RuntimeBinding
  - FEAT-REFERENCE-ENROLLMENT-BINDING-E6
tags:
  - kind/project
  - area/echo
  - agent/owner
created: "2026-09-16"
updated: "2026-09-17"
cssclasses:
  - wide
---

# Echo — E-06 Reference Enrollment and Binding

%% Naming: Echo — E-06 Reference Enrollment and Binding es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo — E-06 Reference Enrollment and Binding
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo — Live Platform V1]] · **Repo:** `xKoRx/echo`
> Subproyecto de **implementación** de la fase E-06 / Reference enrollment and binding. No es Integration. El contrato WHAT vive en el SPEC de Echo; esta nota es HOW / ORDER / GATES.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo — Live Platform V1]] enlaza aquí. La supervisión humana del track live sigue en [[Echo — Producto Integrado]].

## 🎯 Objetivo

Crear `RuntimeBinding` verificable: enrollment canónico por StrategyVersion, mapping observado account+broker+magic, operator ACK, read-back físico, coverage start barrier y attach manual verificado V1. Principio: **INGESTED / CONFIGURED / DB-BOUND ≠ OBSERVING**. Unlock: reloj forward atribuible para E-07/E-10.

## 📊 Estado actual

- **E06_WPA_C2_READY_FOR_MANAGER_REVIEW (2026-09-17, NORMAL WP-A corrección C2 de T01–T03).** Manager auditó `c021983f`; 1 defecto residual corregido en `1614028b` (push FF sobre `feature/e06-reference-enrollment-binding`; mismo carril, SPEC v1.2.2 intacto, sin merge/master). **C2:** `uq_e6_canonical_admission` pasa de `state <> 'CLOSED'` a `state IN ('PREPARED','OBSERVING','SUSPENDED')` — la reserva ya no se retiene en DRAINING (SPEC §11: el conflicto CANONICAL protege al CANONICAL OPEN-admitting; drenar sella `accepts_opens_to` y el switch de cuenta canónica explícito admite el sucesor PREPARED en OTRA physical account durante DRAINING; CLOSED libera; SUSPENDED sigue sin reemplazo implícito). Ninguna transición enumerada §6 re-entra al índice desde DRAINING/CLOSED (DRAINING→SUSPENDED no existe) ⇒ `uq_e6_canonical_open_admitting` permanece defensa en profundidad sin camino de fallo; `uq_e6_overlap_live` sin cambios (SUSPENDED y DRAINING siguen reteniendo la overlap key same-account ⇒ handover sólo hacia otra physical account; same-account rollover exige CLOSED + inventario vacío C1-1/C1-2). `reference_binding_store.go` sin cambios (ya clasifica el constraint como `ErrCanonicalExists`). **Evidencia A–G** en `13_uniqueness.sql` (A/B/C conflictos con titular PREPARED/OBSERVING/SUSPENDED; D sucesor admitido con viejo DRAINING en otra physical key; E sucesor observa porque el viejo DRAINING ya no es OPEN-admitting; F overlap same-account rechazada con viejo DRAINING; G CLOSED libera y admite sucesor fresco) y `TestCanonicalUnique` refleja el mismo lifecycle; `10_migrate_up.sql` aserta el predicado exacto sin DRAINING/CLOSED. **PG REAL PASS:** PG 17.11 descartable (Zonky + PGDG psql, cluster efímero recién initdb'd); `run.sh` PASS ×2 completo (rebuild, probe, up, aserciones 10, idempotencia, 12, 13 A–G, 14, down fail-closed, down ok, up/down/up final); Go E-06 13/13 PASS `-race`; failing set del paquete idéntico al baseline `c021983f` (53 = 53, colateral TC-06-1 + `TestScratch_QueryDB` preexistentes ⇒ cero regresiones); vet OK; builds sdk/gateway/bridge OK; skip-mode PASS. SOURCE: delta C2 = 6 archivos allowed; contracts/061–063 diff 0; tokens prohibidos 0. `TEST_CHANGE_REQUEST.md` intacto. Nota colateral documentada: el comentario de `14_watermark_view_revoke.sql` dice "binding 102 permanece vivo" y tras C2 el vivo es el 109 (14 no es allowed file de C2; fixture SHADOW funciona idéntico). E-06 NO CLOSED; T04–T22 no iniciados; siguiente gate: Manager review C2.
- **E06_WPA_C1_READY_FOR_MANAGER_REVIEW (2026-09-17, NORMAL WP-A corrección C1 de T01–T03).** Manager auditó `429e5c03`; 4 defectos corregidos en `c021983f` (push FF sobre `feature/e06-reference-enrollment-binding`; mismo carril, SPEC v1.2.2 intacto, sin merge/master). **C1-1:** `uq_e6_overlap_live` retiene la overlap key también en SUSPENDED (`{PREPARED, OBSERVING, DRAINING, SUSPENDED}`); liberación = CLOSED con inventario vacío. **C1-2:** trigger DRAINING→CLOSED exige read-back durable `MATCHED` al binding, misma physical key, collector epoch autorizado, `KNOWN` con position_count=0 ∧ pending_count=0 y `received_at >=` instante auditado OBSERVING→DRAINING (fila append-only) ⇒ `E06_CLOSE_REQUIRES_EMPTY_INVENTORY`; protege UPDATE SQL directo; PREPARED→CLOSED nunca observado sigue sin evidencia. **C1-3:** SUSPENDED→OBSERVING exige `coverage_quality=PROVEN` (`E06_RECOVERY_QUALITY`); `Recover()` sella PROVEN + `accepts_opens_from=received_at` + `accepts_opens_to=NULL`, watermark inmutable, gap queda UNKNOWN. **C1-4:** nueva `uq_e6_canonical_admission` UNIQUE `(ns, version_ref) WHERE CANONICAL AND state<>'CLOSED'` serializa el segundo PREPARED CANONICAL desde el POST (§14) ⇒ `ErrCanonicalExists` en `InsertPrepared`; SUSPENDED sin reemplazo implícito; switch explícito tras DRAINING/CLOSED; SHADOW coexiste; `uq_e6_canonical_open_admitting` queda como defensa en profundidad. **PG REAL PASS:** PG 17.11 descartable (Zonky + PGDG psql, cluster efímero `/tmp/e06-pg17`); `run.sh` PASS completo (rebuild, probe, up, aserciones 10 con las dos nuevas, idempotencia, 12 con C1-2/C1-3 neg+pos, 13 con C1-4/C1-1/switch post-CLOSED, 14, down fail-closed, up/down/up final); Go E-06 13/13 PASS `-race`; vet OK; builds sdk/gateway/bridge OK. SOURCE: delta C1 = 9 archivos allowed; contracts/061–063 diff 0; tokens prohibidos 0. Fixtures cross-file 004/201 → SHADOW (probaban borrado/watermark, no la clase). `TEST_CHANGE_REQUEST.md` intacto. E-06 NO CLOSED; T04–T22 no iniciados; siguiente gate: Manager review C1.
- **E06_WPA_READY_FOR_MANAGER_REVIEW (2026-09-17, NORMAL WP-A Persistencia T01–T03).** Implementado en `feature/e06-reference-enrollment-binding` @ `429e5c03` (push FF sobre `acf996ad`; base `5dd998f1`; sin merge/master). **T01 064:** `reference_bindings`/`reference_readbacks`/`binding_transitions`; FK compuesta a tupla Version 061 + FK accounts; UNIQUE parciales CANONICAL OPEN-admitting / collector claim / overlap vivo; triggers INSERT-siempre-PREPARED, write-once identidad, transiciones enumeradas §6 con auditoría obligatoria (SECURITY DEFINER, actor/reason por GUC) y watermark inmutable `max(proof,barrier)` validado por trigger; vista `v_reference_bindings` sin proof crudo; revokes; widen `active_positions.strategy_id`→text; down fail-closed abort con `octet_length>50`. **T02 store:** `InsertPrepared` con recetas §5.1/§13 computadas server-side (pin contra `strategy_identity_mappings`), replay same key+digest convergente, conflict digest distinto, Ack/MarkObserving/Recover/Drain/Suspend/Close/AdvanceReadback; errores `CANONICAL_EXISTS`/`COLLECTOR_CONFLICT`/`ACCOUNT_MAGIC_OVERLAP`/`NOT_OBSERVING`. **T03:** unicidad CANONICAL/COLLECTOR/OVERLAP con evidencia UNIQUE SQL directa + API. **PG REAL PASS:** PostgreSQL 17.11 descartable (binarios Zonky + cliente PGDG, cluster efímero local) — harness `tests/reference_binding_e6/run.sh` PASS completo (rebuild 061→062→063, probe interrupción, up, idempotencia, máquina de estados, unicidad, watermark/vista/revokes, down fail-closed, up/down/up final); tests Go E-06 13/13 PASS con DATABASE_URL y `-race`; go vet OK. SOURCE: diff contracts y 061–063 = 0; OrderSend/forbidden tokens = 0. Tests ajenos rotos por la existencia de 064 (helper `identityBWCDB`, harnesses identity_bwc/analytics_a0) documentados en `TEST_CHANGE_REQUEST.md` sin editar archivos ajenos. T02 queda `[/]` sólo por AC-18 (HTTP, cierra con T05). E-06 NO CLOSED; T04–T22 no iniciados.
- **E06_FORGE_PRODUCER_C1_READY_FOR_MANAGER_REVIEW (2026-09-17, corrección C1 lane Forge).** Manager auditó `508b4a2` y mandó 4 defectos; corregidos en `b738a6d` (push FF sobre `feature/e06-runtime-attestation-exporter`; mismo delta de 2 archivos). C1-1: injector preserva control flow de OnInit — return de éxito guardado por if/else sin llaves se reescribe como bloque compuesto `{ Publish(); return X; }`, boundary no demostrable rechaza fail-closed, cadenas if/else terminales instrumentables (prueba acotada), returns de fallo byte-idénticos. C1-2: invalidación `c=0` es hard gate antes de cualquier payload. C1-3: `SetField` comprueba retorno documentado de `GlobalVariableSet` (`datetime != 0`) + `GetLastError`; cleanup de chunks distingue inexistente (`GlobalVariableCheck`) de fallo real de `GlobalVariableDel`; fallo material de cleanup impide commit. C1-4: generate+assert+instrumentación en staging aislado (mismo basename) y promoción por rename atómico (fallback mismo-volumen) sólo tras post-condiciones; exportación fallida no deja MQ5 publicable ni sobrescribe preexistente. Tests C1: 9 casos (guard same/next-line, if/else, else-if, nested, bloque llaves, boundary ambiguo, fault injection GV CONTRACT/model 10 escenarios + pins textuales, publicación staged). Suite §17 A–O + RobustRun/WFM + JUnit trades 13/13 PASS; build PASS; `verify_build.sh` FAIL_BASELINE_KNOWN reproducido 3/3 en `508b4a2` puro. PHYSICAL_PENDING (AC-34/35 sin terminal MT5/SQX). E-06 NO CLOSED.
- **E06_FORGE_PRODUCER_IMPLEMENTED_PHYSICAL_PENDING (2026-09-17, lane A NORMAL).** Producer atestación §7.2a inyectado en `EchoForgeMT5Exporter.java` (Forge `feature/e06-runtime-attestation-exporter` @ `508b4a2` desde `3d0e8c9` F-05-I; push FF; sin merge). Contract §17 A–O PASS, build plugin PASS, idempotencia byte-stable, MagicNumber/mmLots intactos. PHYSICAL_PENDING (sin terminal MT5/SQX aquí; AC-34/AC-35 esperan físico). Auditado por Manager ⇒ corrección C1 (ver bullet superior). E-06 NO CLOSED; NORMAL Echo (WP-A…WP-E) no lanzado.
- **E06_PLANNING_READY_FOR_IMPLEMENTATION_REVIEW (2026-09-16, docs-only, SPEC v1.2.2).** Erratum de liveness del refresh §7.2a.4: MQL5 no garantiza ticks cada 5 s ⇒ el `MUST` de republicación vía `OnTick` era garantía irrealizable. Decisión Manager frozen: `OnTimer` existente realmente activado con período ≤5 s **preferido** (prohibido modificar `EventSetTimer`/crear timer); si sólo `OnTick`, renovación **oportunista** — 5 s = intervalo mínimo entre publicaciones, no frecuencia; sin tick ni timer compatible **sin promesa de liveness continua** (expiración 15 s fail-closed `SUSPENDED + UNKNOWN`; recovery §6 con nueva atestación matching; ninguna actualización de `ts` desde Echo/Bridge/Gateway/config). Tests AC-37a…d. CASE B **intacto**; encoding v1 intacto. Corrección previa del transporte §7.2a: encoding `echo.attest.v1.<acct16>.<chart16>.<field>` con `mh`/`ml` uint32 exactos, commit par, `ts` escrito (nunca `GlobalVariableTime`), `chart_ref` obligatorio, FNV-1a32 de `ACCOUNT_SERVER`. Inyección Forge: post-`generate`+`assertNonZeroLots` en `EchoForgeMT5Exporter.java`, scanner estructural, fail-closed, **no implementada**. Branch Forge observada `codex/f05-release-prep` @ `0ddd4db` (blob `cfbd5b78`); `master` `0b9742b` no es la de desarrollo. HEAD Echo `acf996ad043f87d6bbe6ae7b6190d1eb801e908a` (contrato `28afc47faf72b70e67b141b39224b8674f98458b`; old `336c723b`; push FF). Baseline `origin/master` `5dd998f16aea7b2821f460188718d7a6d279829c`. **0 líneas productivas en `v3/**`; 0 bytes Forge mutados.** Master intacto. NORMAL no lanzado. No E-07. No PR. Next gate = IMPLEMENTATION REVIEW.
- **RuntimeBinding key:** PK `binding_id` UUID; pin S0 `binding_ref = H("echo-reference-binding.v1",[ns,binding_id,version_ref,account_registration_ref,broker_server_ref,platform,magic_decimal,observation_class])`.
- **Lifecycle:** PREPARED → (ACK + matching read-back) → OBSERVING → DRAINING → CLOSED; staleness → SUSPENDED + UNKNOWN. PREPARED/ACK solos ≠ OBSERVING.
- **Read-back authority:** Echo collector `reference_status` → Bridge `REFERENCE_READBACK.v1` → Gateway. Operator ACK es CONFIG, no suficiente. Heartbeat/UnifiedBatch/config **no** son OBSERVING.
- **Coverage barrier:** `coverage_started_at = max(proof.recorded_at, capture_barrier_at)`. Prohibido created_at/ingestion/ACK clocks.
- **CANONICAL/SHADOW:** 1 CANONICAL OPEN-admitting por Version; SHADOW no suma. Duplicate collector y same-account overlap fail-closed.
- **Migración:** `064_reference_enrollment_binding` exclusiva E-06; FK a 061; SHARED DEV apply gated por 061 APPLIED (hoy NOT_APPLIED). 062/063 no-touch.
- **PHYSICAL:** AC-01…15 + AC-26…32; producer real `reference_status`; fakes ≠ OBSERVING. GAP-ECHO-006 = PHYSICAL_PENDING, no PASS.
- **Hipótesis accounts/policies solos:** REFUTADA en source/PG. Bastan accounts/policies (intent) + `reference_bindings` (hecho). No `deployments`.
- **AUTHORITY_CONFLICT:** ninguno. S0 ACTIVE/CLOSED = envelope de pin; lifecycle operacional = Live Authority §5. O1/O3 technical default Fable.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `feature/e06-reference-enrollment-binding` | `5dd998f16aea7b2821f460188718d7a6d279829c` | [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] §§5–6; O1/O3 Fable; C-3 collector + excepción Manager §7.2a | `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/SPEC.md` v1.2.2 (encoding v1 + erratum liveness refresh; HEAD `acf996ad`, contrato `28afc47f`; previo `336c723b`) | E06_WPA_C2_READY_FOR_MANAGER_REVIEW @ `1614028b` (corrección C2 de T01–T03; PG REAL PASS; T04–T22 pendientes) |
| xKoRx/symphony (Forge) | `feature/e06-runtime-attestation-exporter` @ `508b4a2` (parent `3d0e8c9` = cierre F-05-I; push FF; base `codex/f05-release-prep`) | `3d0e8c958765da23840e00bf1a0ac017fc47597a` (blob exporter `cfbd5b78` verificado pre-write) | F-04 sello/readback magic | SPEC §7.2a v1.2.2 implementada: inyección post-`generate`+`assertNonZeroLots` en `EchoForgeMT5Exporter.java` (scanner estructural no-regex, fail-closed, idempotente `ECHO_ATTEST_V1_*`, encoding v1, refresh §7.2a.4). Tests §17 A–O contract PASS; build plugin PASS; **PHYSICAL_PENDING** (sin terminal MT5/SQX) | E06_FORGE_PRODUCER_IMPLEMENTED_PHYSICAL_PENDING · lane propio, gate Manager pendiente |

## 🗺️ Source map (baseline `5dd998f1` + PG/Hasura)

- Accounts/policies: intent mutable; sin version/hash/terminal/read-back.
- ClientConfig/Kafka/handshake: config delivery; login+company; **sin** ACCOUNT_SERVER; **sin** ACK de EA.
- Bridge heartbeat: liveness vestigial; MQL Reference **no emite** heartbeat; payload ignorado. UnifiedBatch = Execution-only. AccountRegistry no es unique físico.
- 061 source sí / SHARED DEV no. 062+063 DEV sí. `reference_bindings` ausente.
- S0 `RuntimeBinding` READ ONLY. E-04 INGESTED no-touch. E-02 CONFIG REUSE. Hook SQX de coverage OUT_OF_SCOPE (C-3 DEFER). Echo collector `reference_status` + relay de atestaciones IN SCOPE (§7.2a). Producer del strategy EA = Forge exporter (`EchoForgeRobustRunExporter` estampa `MagicNumber` input; `EchoForgeMT5Exporter` genera; `magic-readback` verifica; sello F-04 exige allocated==readback).
- `reference_v3.mq{4,5}`: sin magic input propio; `GetEffectiveMagicNumber` = POSITION_MAGIC o fallback ClientConfig (prohibido como atestación). Cero `GlobalVariable*`/`ACCOUNT_SERVER`/`CHART_EXPERT_NAME` hoy: helpers net-new T09b (reconstrucción encoding v1, sólo lectura).

## 🎯 Target physical state

```text
v3/sdk/postgres/migrations/064_reference_enrollment_binding.{up,down}.sql
echo.reference_bindings + reference_readbacks + binding_transitions
echo.v_reference_bindings
POST /api/v1/reference/bindings[+ /ack /drain /suspend /close]
echo.reference-readback.v1   # Bridge → Gateway, solo desde reference_status
ClientConfig additive pin fields
v3/clients/mt{4,5}/reference_v3.mq{4,5}  # reference_status mínimo + relay verbatim atestaciones §7.2a (NORMAL futuro)
v3/hasura/metadata/tables/reference_bindings.yaml  # SELECT only
(xKoRx/symphony) EchoForgeMT5Exporter.java  # inyección atestación §7.2a — lane Forge, un archivo
```

Ningún cambio a `v3/sdk/contracts/**`. MQL sólo el delta collector T09b. Ningún E-07 DEAL. Ningún apply 061/064 a Aranea en NORMAL. Resto de Forge intocado.

## 🕸️ Dependency graph

Ver TASKS.md. T01 persistencia → T05 HTTP → T09b collector status → T11 OBSERVING. Emitter T10 ∥ HTTP. PHYSICAL T21 al final con producer real.

No ejecutar E-07…E-13. No reabrir E-01…E-05. E-04 T21 no bloquea. 061 DEV NOT_APPLIED no bloquea development (descartable); bloquea apply 064 SHARED DEV. No abrir hook SQX.

## Allowed scope NORMAL

Exacto PLAN.md. Development en `feature/e06-reference-enrollment-binding` desde `5dd998f1`. Worktree dedicado; no reutilizar checkout de otra fase. Prohibido `origin/master` push/merge. Prohibido `v3/sdk/contracts/**`. Prohibido 061/062/063. 064 exclusiva. Prohibido hook SQX exportado. Permitido `reference_status` en Echo collector. Prohibido Aranea PROD. Prohibido apply 064 SHARED DEV hasta 061 APPLIED (ops aparte).

## 📦 Work packages

- **WP-A Persistencia** T01–T03. 064 + stores + UNIQUEs.
- **WP-B Enrollment HTTP** T04–T07. PREPARED/ACK/drain + ClientConfig.
- **WP-C Read-back** T08–T11 + T09b. Envelope, collector `reference_status`, Bridge emitter, Gateway consumer, OBSERVING.
- **WP-D Gates negativos** T12–T15. Duplicate, overlap, mismatch, stale, DB-only.
- **WP-E READ/BWC/cert** T16–T22. Hasura, widen, SOURCE, coverage, PHYSICAL.

## TOP / NORMAL boundaries

- TOP: SPEC, esta nota, TASKS, PLAN puente, linkage padre. No source Go/SQL/HTTP productivo (cumplido). Corrigió el transporte §7.2a a encoding v1 (sin cambiar CASE B). No implementó la inyección.
- NORMAL: **no lanzado** (gate Manager). T01–T22+T09b desbloqueados por v1.2.0: zero-order = atestación runtime §7.2a + KNOWN_EMPTY; fail-closed `RUNTIME_ATTESTATION_ABSENT`/`MISMATCH`. No sintetizar OBSERVING, no hook SQX de coverage, no E-07, no apply 061. La inyección Forge (un archivo) corre en lane Forge con gate propio.
- GOD: NONE.

## Frozen decisions

1. `reference_bindings` es el hecho; accounts/policies son intent; no `deployments`.
2. OBSERVING exige ACK CONFIG **y** `reference_status` matching. Heartbeat/UnifiedBatch/config/PG no bastan.
3. Un CANONICAL OPEN-admitting por Version; SHADOW no suma.
4. Duplicate collector: UNIQUE physical key + epoch **del producer EA**; segundo 409. Gateway no mint identity.
5. Same-account overlap magic prohibido hasta CLOSED+inventario vacío.
6. Pin Version write-once en PREPARED; config posterior no reinterpreta.
7. `coverage_started_at = max(proof.recorded_at, capture_barrier_at)`.
8. Stale > 15000ms sin `reference_status` → SUSPENDED + UNKNOWN.
9. Migración 064; FK 061; interlock SHARED DEV explícito.
10. Certificación sin órdenes. Unit fakes ≠ PHYSICAL OBSERVING. PHYSICAL exige producer `reference_status` + Version con inyección §7.2a.
11. `observed_magic` = inventario broker; `runtime_attestations` = reconstrucción lossless encoding v1 §7.2a; sin backfill/mint desde config/PG/Version. **Zero-order (Manager CASE B): `effective_magic == binding.magic_decimal` atestiguado por la instancia EA strategy; ausente/mismatch ⇒ fail-closed. Nunca trade/pending/DEAL artificial.** `chart_ref` obligatorio. Vigencia = `ts` escrito, nunca `GlobalVariableTime`.
12. `*_trade_allowed` se capturan; no gatean OBSERVING. VALID_NO_SIGNAL es E-07.
13. C-3: hook SQX de **coverage** DEFER; excepción §7.2a = **sólo** atestación de identidad runtime mínima (sin signals/deals/coverage/métricas/lifecycle/telemetría/estado). Echo collector status + relay IN SCOPE.
14. Identidad de Version: inyectar atestación cambia bytes ⇒ **nuevo** `strategy_version_ref` (canonical_strategy_id estable). Versions históricos nunca se mutan; fail-closed `RUNTIME_ATTESTATION_ABSENT`. Re-enroll = nueva exportación + ingestion + nuevo `binding_id`.

## Migrations

Una: `064_reference_enrollment_binding` (exclusiva E-06). Depende de 061 **para apply**. Independiente de 062/063 semánticamente. 065+ fuera. Gate up/down/up en PG descartable 061→062→063→064. No apply PROD. No apply SHARED DEV sin 061.

## Dependency delta

NONE de terceros. `v3/sdk` importa contracts (mismo parent). Kafka topic nuevo sobre producer existente.

## Compatibility strategy

HTTP nuevo. ClientConfig additive. Hasura SELECT nueva. EA/journal legacy intactos. `active_positions.strategy_id` → text (deuda E-03).

## Testing / gates

SPEC AC-01…AC-25 + AC-26…AC-33. SOURCE + CONTRACT + PG REAL + HTTP + PHYSICAL producer `reference_status` zero-order + HASURA yaml. Ver VERIFICATION.md stub.

## Prohibited files

`v3/sdk/contracts/**`, `migrations/061-063_*`, `v3/clients/**` salvo collector `reference_status`+relay §7.2a, `v3/front/**`, `v3/core/**`, Docker/Compose/deploy/workflows, Forge/symphony **salvo la inyección de un archivo §7.2a en lane Forge propio**, `sync.sh`.

## Blockers

**Planning: ninguno** (transporte v1.2.1 cerrado; CASE B intacto). Development: ninguno adicional (PG descartable incluye 061). SHARED DEV 064 apply: **061 NOT_APPLIED** (ops/E-03). PHYSICAL producer real: GAP-ECHO-006 si no hay terminal collector **y/o** Version Forge con inyección §7.2a.5; **no** se sustituye por fake. E-04 T21 no bloquea. La inyección Forge requiere lane/gate Forge propio **y** reidentificar branch de WRITE (`codex/f05-release-prep` observada; `master` no autorizada por el hecho de ser master) — bloquea sólo los AC PHYSICAL de atestación, no CONTRACT.

## Handoff requirements

Implementation review de v1.2.2 (erratum liveness + encoding v1 + CASE B intacto) → autoriza NORMAL. **NORMAL no arranca antes.** No merge/deploy. No E-07. Hook SQX de coverage sigue DEFER. No apply 061/064 Aranea. La inyección Forge se ejecuta como expansión de borde de un archivo con gate Manager/Forge **después** de reidentificar la branch autorizada.

## Closure conditions

Esta sesión TOP **no** cierra E-06. Cierre futuro: T01–T22 `[x]`; AC-01…AC-25; independent verifier; Manager; controlled integration. PHYSICAL SHARED DEV/PROD son gates aparte.

## 🧩 Subproyectos

_No aplica — hijo de implementación de E-06; no crea Integration ni más hijos._

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> Checklist atómico en `xKoRx/echo` `specs/FEAT-REFERENCE-ENROLLMENT-BINDING-E6/TASKS.md`. Aquí sólo work packages. NORMAL no arranca hasta manager review.
> - [x] TOP planning SPEC/PLAN/TASKS/VERIFICATION v1.0.0 → Manager Review #owner/agent #type/docs #area/echo
> - [x] TOP planning correction #1 v1.1.0 zero-order physical authority → Manager Review #owner/agent #type/docs #area/echo
> - [x] TOP authority reconciliation zero-order magic → CASE C blocked #owner/agent #type/docs #area/echo
> - [x] TOP planning correction #2 v1.2.0 Manager CASE B + producer discovery §7.2a → Manager Review #owner/agent #type/docs #area/echo
> - [x] TOP transport contract correction v1.2.1 encoding GV lossless → Manager Review #owner/agent #type/docs #area/echo
> - [x] TOP refresh liveness erratum v1.2.2 (OnTimer compatible / OnTick oportunista / sin liveness continua prometida) → Implementation Review #owner/agent #type/docs #area/echo
> - [r] WP-A Persistencia 064 + stores + UNIQUEs #owner/agent #type/dev #area/echo
> - [ ] WP-B Enrollment HTTP PREPARED/ACK/drain + ClientConfig #owner/agent #type/dev #area/echo
> - [ ] WP-C Read-back Bridge→Gateway desde `reference_status` y transición OBSERVING #owner/agent #type/dev #area/echo
> - [ ] WP-D Gates negativos duplicate/overlap/mismatch/stale/DB-only #owner/agent #type/dev #area/echo
> - [ ] WP-E Hasura/BWC/SOURCE/PHYSICAL no-trading #owner/agent #type/dev #area/echo

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

## 📆 Bitácora

- **2026-09-17 (NORMAL WP-A corrección C2 — audit fix de la corrección C1, `E06_WPA_C2_READY_FOR_MANAGER_REVIEW`)** — Baseline verificado pre-write: worktree dedicado `/tmp/echo-e06-reference-enrollment` en `feature/e06-reference-enrollment-binding` @ `c021983f` == origin, worktree limpio, parent `429e5c03`, merge-base `origin/master` = `5dd998f1`. Defecto único del Manager corregido sin reabrir el SPEC ni tocar otras semánticas: el predicado de `uq_e6_canonical_admission` (C1-4) `state <> 'CLOSED'` retenía la reserva CANONICAL durante DRAINING, contradiciendo §11 (el conflicto protege al CANONICAL OPEN-admitting; el switch de cuenta canónica es explícito con el viejo DRAINING/CLOSED). **Fix:** predicado ahora `state IN ('PREPARED','OBSERVING','SUSPENDED')`; DRAINING/CLOSED liberan la titularidad; se demuestra en el trigger que ninguna transición enumerada §6 re-entra al índice desde DRAINING/CLOSED (DRAINING→SUSPENDED no existe) ⇒ `uq_e6_canonical_open_admitting` queda sin camino de fallo alcanzable (defensa en profundidad, sin cambios); `uq_e6_overlap_live` sin cambios (SUSPENDED y DRAINING siguen reteniendo la overlap key ⇒ handover en DRAINING sólo hacia otra physical account; same-account rollover exige CLOSED + inventario vacío por C1-1/C1-2). `reference_binding_store.go` sin cambios (ya clasifica el constraint como `ErrCanonicalExists`). **Tests:** `13_uniqueness.sql` añade casos A (titular PREPARED ⇒ conflicto en INSERT), B (OBSERVING ⇒ conflicto), C (SUSPENDED ⇒ conflicto), D (sucesor CANONICAL PREPARED admitido en otra physical key con viejo DRAINING), E (sucesor pasa a OBSERVING con el viejo aún DRAINING — ya no es OPEN-admitting — con gates normales ACK/barrier/watermark), F (overlap same-account+same-magic rechazada con viejo DRAINING), G (cerrados viejo y sucesor con evidencia C1-2 cada uno, un CANONICAL PREPARED fresco inserta — switch post-CLOSED intacto); `TestCanonicalUnique` reescrito con el mismo lifecycle (conflictos PREPARED/OBSERVING/SUSPENDED, sucesor admitido y observando durante DRAINING, sucesor fresco post-CLOSED); `10_migrate_up.sql` aserta el índice con el conjunto exacto y sin DRAINING/CLOSED. **PG REAL:** PostgreSQL 17.11 descartable (Zonky + PGDG psql, cluster efímero `/tmp/e06-pg17/data-c2` recién initdb'd, cero SHARED DEV/PROD): `run.sh` PASS completo ×2 (rebuild 001–063, probe BEGIN/ROLLBACK, up `-1`, aserciones 10, idempotencia, 12 máquina de estados, 13 unicidad A–G, 14 watermark/vista/revokes, down fail-closed >50 bytes, down ok 31, up/down/up final). Go E-06 **13/13 PASS** con `DATABASE_URL` y `-race`. **Regresión:** failing set del paquete `sdk/postgres` completo idéntico al baseline puro `c021983f` corrido en worktree aparte (53 = 53; todo colateral TC-06-1 `identityBWCDB` + `TestScratch_QueryDB` preexistentes) — cero regresiones nuevas. `go vet` OK (sdk/gateway/bridge); builds sdk/gateway/bridge OK; skip-mode CONTRACT PASS (sólo falla el `TestScratch_QueryDB` preexistente). **SOURCE:** delta vs `c021983f` = 6 archivos (064 up, 10, 13, store test, TASKS, VERIFICATION), todos allowed; contracts y 061–063 diff 0; `OrderSend`/`deployments`/`AllocateMagic` = 0 en el delta (única mención: la lista documental de tokens en VERIFICATION, patrón C1); `TEST_CHANGE_REQUEST.md` intacto. Nota colateral documentada en VERIFICATION: el comentario de `14_watermark_view_revoke.sql` (no allowed file) dice "el binding 102 permanece vivo" y tras C2 el 102 termina CLOSED mientras el CANONICAL vivo al cierre de 13 es el 109; su fixture 201 SHADOW funciona idéntico. Commit `1614028bc2c3831a689f76094ccd7a5a8e0577c4`, push FF `c021983f..1614028b`, sin merge/PR/master. E-06 NO CLOSED; T04–T22 no iniciados. **Siguiente gate: Manager review de la corrección C2.**

- **2026-09-17 (NORMAL WP-A corrección C1 — audit fix de T01–T03, `E06_WPA_C1_READY_FOR_MANAGER_REVIEW`)** — Baseline verificado pre-write: worktree dedicado `/tmp/echo-e06-reference-enrollment` en `feature/e06-reference-enrollment-binding` @ `429e5c03` == origin, worktree limpio, parent `acf996ad`, merge-base `origin/master` = `5dd998f1`. Cuatro defectos del Manager corregidos sin reabrir el SPEC ni introducir estados/políticas nuevas. **C1-1:** `uq_e6_overlap_live` pasa de `{PREPARED, OBSERVING, DRAINING}` a `{PREPARED, OBSERVING, DRAINING, SUSPENDED}` — un binding suspendido aún puede conservar posiciones, así que la overlap key sólo se libera con CLOSED (decisión frozen 5 del proyecto). **C1-2:** la transición DRAINING→CLOSED en `fn_e6_bindings_before_update` ahora exige evidencia durable consultando `echo.reference_readbacks`: fila `match_status='MATCHED'` con `matched_binding_id` del binding, igualdad de `broker_server_ref`/`account_registration_ref`/`platform` (otra cuenta rechazada), igualdad de `collector_id`/`collector_epoch` con el claim autorizado (otro epoch rechazado), `inventory_completeness='KNOWN'` con `position_count=0 AND pending_count=0` (UNKNOWN/NULL rechazados) y `received_at >=` al `at` de la fila OBSERVING→DRAINING de `binding_transitions` (append-only, immutable — read-back anterior al drain rechazado; sin fila de auditoría ⇒ `E06_CLOSE_DRAIN_AUDIT_MISSING` fail-closed); sin evidencia ⇒ `E06_CLOSE_REQUIRES_EMPTY_INVENTORY`, gate vigente también ante UPDATE SQL directo; `PREPARED→CLOSED` nunca observado permanece permitido y la evidencia exigida cabe completa en el schema congelado (sin columnas nuevas; down sin cambios). **C1-3:** trigger SUSPENDED→OBSERVING exige `coverage_quality='PROVEN'` (`E06_RECOVERY_QUALITY`) y `Recover()` la sella junto con `accepts_opens_from=received_at`, `accepts_opens_to=NULL`, `last_physical_readback_at=received_at`; `coverage_started_at`/`capture_barrier_at` inmutables (ya bloqueados por trigger) y `suspended_at` preservado; el gap queda UNKNOWN sin reescribir historia. **C1-4:** nueva UNIQUE parcial `uq_e6_canonical_admission` sobre `(registry_namespace, strategy_version_ref) WHERE observation_class='CANONICAL' AND state <> 'CLOSED'` — el segundo POST PREPARED CANONICAL de la misma Version (distintas physical keys, distinto binding_id) viola el UNIQUE en el INSERT y `InsertPrepared` lo clasifica como `ErrCanonicalExists` (SPEC §14: serialización desde POST; también mapeado en `classifyTransitionError`); SUSPENDED no habilita reemplazo implícito; el switch sigue explícito tras DRAINING/CLOSED; SHADOW coexiste en otras cuentas; `uq_e6_canonical_open_admitting` se conserva como defensa en profundidad (sin camino de fallo posible bajo la reserva). **Tests:** SQL — `12_state_machine.sql` añade cierre sin evidencia (rechazo) + fixture de read-back de cierre CONTRACT/PG REAL y recovery sin PROVEN (rechazo) + assertions de calidad vigente; `13_uniqueness.sql` reescribe el caso canónico (segundo PREPARED falla en INSERT por `uq_e6_canonical_admission`, SUSPENDED reintenta y sigue rechazado, recovery C1-3, drain → cierre con evidencia C1-2 → re-insert positivo del switch post-CLOSED) y añade overlap con titular SUSPENDED; `10_migrate_up.sql` aserta las dos nuevas propiedades de índices; `14` ajusta su fixture a SHADOW (mismo motivo cross-file que el binding 004 de `12`: la reserva C1-4 opera sobre fixtures preexistentes que probaban borrado/watermark, no la clase). Go — `TestCanonicalUnique` reescrito (POST ⇒ `CANONICAL_EXISTS` sin fila persistida, evidencia SQL directa, SUSPENDED sin reemplazo, recovery PROVEN, switch con evidencia), `TestOverlapUnique` añade SUSPENDED-retain + liberación real, `TestTransitions_EnumeratedOnly`/`TestCollectorUnique` añaden negativo+positivo de C1-2, `TestCoverageStartImmutable` aserta PROVEN post-recovery, helper `seedCloseEvidence` documenta que el fixture es CONTRACT/PG REAL nunca PHYSICAL (AC-32). **PG REAL:** PostgreSQL 17.11 descartable (mismo patrón `/tmp/e06-pg17`, cluster efímero recién initdb'd, cero SHARED DEV/PROD): `run.sh` PASS completo dos veces (rebuild 001–063, probe interrupción, up, aserciones 10 actualizadas, idempotencia, máquina de estados, unicidad, watermark/vista/revokes, down fail-closed >50 bytes, down ok, up/down/up final). Go E-06 **13/13 PASS** con `DATABASE_URL` y `-race`; `go vet` OK (sdk/gateway/bridge); builds sdk/gateway/bridge OK; skip-mode CONTRACT PASS. **SOURCE:** delta vs `429e5c03` = 9 archivos (064 up, store, store test, 4 SQL del harness, TASKS, VERIFICATION), todos allowed; contracts y 061–063 diff 0 vs `5dd998f1`; `OrderSend`/`deployments`/`AllocateMagic` = 0 en el delta; `TEST_CHANGE_REQUEST.md` intacto (TC-06-1/TC-06-2 preservados sin arreglos ajenos). Commit `c021983f` push FF `429e5c03..c021983f`, sin merge/PR/master. E-06 NO CLOSED; T04–T22 no iniciados. **Siguiente gate: Manager review de la corrección C1.**

- **2026-09-17 (NORMAL WP-A — Persistencia T01–T03, `E06_WPA_READY_FOR_MANAGER_REVIEW`)** — Baseline verificado pre-write: worktree dedicado `/tmp/echo-e06-reference-enrollment` en `feature/e06-reference-enrollment-binding` @ `acf996ad` == origin, merge-base `origin/master` = `5dd998f1`, worktree limpio. **T01:** migración `064_reference_enrollment_binding.{up,down}` con tablas §16, FK tupla Version 061, UNIQUE parciales §5.1/§9/§10, triggers de lifecycle §6 (INSERT siempre PREPARED `E06_INSERT_NOT_PREPARED`; write-once identidad `E06_WRITE_ONCE`; transiciones enumeradas con precondiciones; auditoría obligatoria `binding_transitions` via AFTER trigger SECURITY DEFINER con actor/reason por GUCs `echo.e6.*`; watermark `E06_WATERMARK_RECIPE` validado en trigger como `GREATEST(proof_recorded_at, capture_barrier_at)`; recovery mueve `accepts_opens_from` y reabre `accepts_opens_to` sin mover watermark; DELETE/TRUNCATE denegados), vista `v_reference_bindings` redactando proof a `proof_sha256_hex`, revokes patrón 061/063 (roles con guard de existencia + PUBLIC), widen `active_positions.strategy_id`→text con recreación de `v_trade_stream` (057) y down fail-closed `MIGRATION_064_DOWN_ABORTED` si `octet_length(strategy_id)>50` (umbral exacto 50). Decisiones de diseño bajo SPEC: collector claim claim-together (`E06_COLLECTOR_CLAIM_PARTIAL`) e inmutable una vez seteado; pin del mapping `E06_MAGIC_PIN_MISMATCH` exigido en INSERT (igualdad string decimal == bigint::text); recetas `fn_e6_hash_tagged`/`fn_e6_binding_ref`/`fn_e6_map_revision` en SQL con escaping `to_json` == `wire.appendJSONString` (verificado golden cruzado SQL==Go `sha256:7e03590a…`). **T02:** `reference_binding_store.go` — `InsertPrepared` (validación S0, recetas, replay §14 por PK+digest sellado, clasificación de UNIQUE/FK por constraint name), `Ack` (idempotente, conserva `acked_at` original), `MarkObserving` (exige ACK; sella barrier/watermark/accepts_from/collector/last_readback; `CANONICAL_EXISTS`/`COLLECTOR_CONFLICT` mapeados), `Recover`, `Drain`, `Suspend`, `Close`, `AdvanceReadback` (no-op ante replay); transacciones ReadCommitted con GUCs de auditoría en la misma txn. **T03:** tests Go con evidencia UNIQUE directa (`uq_e6_canonical_open_admitting`, `uq_e6_collector_claim`, `uq_e6_overlap_live` via UPDATE/INSERT SQL) y positiva SHADOW coexistente + reattach post-CLOSED. **PG REAL:** PostgreSQL 17.11 descartable en `/tmp/e06-pg17` (binarios server Zonky 17.11 + cliente PGDG psql 17.9; sin docker/sudo; cluster efímero local, cero Aranea): harness `run.sh` PASS — rebuild 001–063, seed pre-064, probe BEGIN/ROLLBACK, up `-1`, aserciones 10 (objetos/FK/uniques/triggers/vista/widen/golden), segundo apply idempotente, 12 máquina de estados (≈25 negativos + positivos), 13 unicidad (incl. overlap cross-namespace O3), 14 watermark/vista/revokes `has_table_privilege`, down fail-closed con fila de 60 bytes (aborta, objetos intactos), down ok → 31 (objetos ausentes, varchar(50) exacto, `v_trade_stream` recreada), up final. Go: 13/13 PASS `DATABASE_URL` + `-race` PASS; `go vet` OK; build sdk/gateway/bridge OK; skip-mode sin DATABASE_URL = sólo `TestScratch_QueryDB` FALLA (DSN hardcodeado preexistente, bit-idéntico a master, documentado E-05). **SOURCE:** diff `v3/sdk/contracts` y 061–063 vs `5dd998f1` = 0; delta = 17 archivos allowed; `OrderSend`/`deployments`/`AllocateMagic` = 0 en delta. **Colateral documentado en `TEST_CHANGE_REQUEST.md` (TC-06-1/TC-06-2, repro incluido):** `identityBWCDB` TRUNCATE falla en schema-064 por FK nueva; harnesses `identity_bwc`/`analytics_a0` aplican 064 sin 061 (interlock §16 opera) — fixes recomendados, no aplicados (fuera de allowed files). Commit `429e5c035d471c83ebc50af5e9637d1e7a283189`, push FF `acf996ad..429e5c03`, sin merge/PR/master. T01 `[x]`, T02 `[/]` (AC-18 → T05), T03 `[x]`. **Siguiente gate: Manager review de WP-A → autoriza T04+ (WP-B).** E-06 NO CLOSED.

- **2026-09-17 (corrección C1 — Forge producer, audit fix)** — Manager auditó `508b4a2` y detectó 4 defectos materiales; corregidos en el worktree dedicado `symphony-e06-attestation` (branch `feature/e06-runtime-attestation-exporter`, delta sólo los 2 archivos autorizados; fixture ajeno del worktree principal preservado intocado). **C1-1:** la inserción textual antes de un `return INIT_SUCCEEDED` guardado por `if` sin llaves (same-line o next-line) desasociaba el return de su guard y lo volvía incondicional. Scanner ahora clasifica el boundary de cada return de éxito: previo `;`/`{`/`}`/inicio ⇒ inserción plana segura; cuerpo directo de `if/else/for/while/switch` sin llaves (palabra guard obtenida del par de paréntesis cerrado inmediatamente anterior, con pila para no dejar que llamadas anidadas la sombreen; o `else` literal) ⇒ reescritura del span exacto del statement como `{ EchoAttestV1_Publish(); return X; }`; cualquier otro boundary (`case:`/label/expresión) ⇒ rechazo fail-closed. Fall-through: además de último segmento `return`, cadenas if/else terminales se aceptan con prueba estructural acotada (regionTerminates/ifTerminates: sólo `return`, bloques y cadenas if/else; cualquier otra forma ⇒ false ⇒ fail-closed); segmentos que empiezan con `else` se fusionan con su `if` (el splitter partía el statement en el `;` del arma then). Returns de fallo quedan byte-idénticos (sólo se clasifica boundary donde se inserta). **C1-2:** la invalidación `c=0` ignoraba su resultado ⇒ ahora hard gate: si falla, Publish retorna false sin escribir payload ni commit. **C1-3:** `SetField` sólo chequeaba `GetLastError` ⇒ ahora comprueba el retorno documentado (`datetime != 0`) además del error; cleanup residual de chunks distingue inexistente (`GlobalVariableCheck`) de fallo real de `GlobalVariableDel` y un fallo material de cleanup bloquea el commit; commit final mantiene chequeo + invalidación best-effort + false; Revoke sigue contrato §7.2a.2 (c=0 basta, Del residual tolerado). **C1-4:** exporter generaba directo al path final y luego instrumentaba ⇒ si el injector fallaba quedaba MQ5 sin instrumentar publicable. Nuevo flujo: staging aislado `.echoforge-e06-staging-<rand>/` (mismo basename), generate→assertNonZeroLots→instrument→validación→promoción `Files.move` con `ATOMIC_MOVE` (fallback renombrado mismo-volumen documentado; staging es hijo del outDir, mismo filesystem), limpieza recursiva en finally restringida a su propio namespace. Evidencia no-STOP: staging sólo cambia el directorio destino de `SourceCode.generate` (parámetro explícito; suite existente ya generaba a paths arbitrarios), `.sqx` de entrada/basename/bytes sellados sin cambio. **Tests (+9):** guard same-line y next-line (el defecto reproducido y ahora rechazado por simulador de control flow), if/else success-failure, cadena else-if, nested if sin llaves, return en bloque con llaves, boundary ambiguo (case-label) fail-closed, fault injection GV model 10 escenarios (invalidación ⇒ cero escrituras posteriores; mh; ml; chunk; cleanup real; ts; sh; commit final; chunk inexistente no es fallo; happy path con residuos) clasificados CONTRACT/model con pins textuales del bloque emitido, publicación staged (rechazo ⇒ nada publicable ni residuo; preexistente preservado byte-idéntico; éxito ⇒ sólo MQ5 instrumentado, mismo nombre, MagicNumber/mmLots intactos; fallo del generador ⇒ nada). Simulador de control flow en tests (parser acotado a las formas de los fixtures) demuestra equivalencia, no presencia textual. **Verificación:** build.sh PASS; suite main 32/32 OK (23 previas + 9 C1); RobustRun/WFM OK; JUnit trades 13/13; `verify_build.sh` FAIL_BASELINE_KNOWN reproducido 3/3 en baseline puro `508b4a2` (carrera SIGPIPE conocida) con verificación semántica manual 5/5 exporters y 0 test-support en prod. Regresiones §8: idempotencia, encoding v1, magic int64 máximo, FNV golden, UTF-8, OnDeinit, timers, OnTick, zero trading calls — todas verdes. PHYSICAL_PENDING (sin terminal MT5/SQX; AC-34/AC-35 esperan físico). Commit `b738a6db19bc19b4b12362583f50bee85a3790af`, push FF `508b4a2..b738a6d`, sin merge/PR/master. **Verdict: `E06_FORGE_PRODUCER_C1_READY_FOR_MANAGER_REVIEW`**; E-06 NO CLOSED.

- **2026-09-17 (NORMAL Forge lane A — producer atestación §7.2a)** — Implementada la inyección del producer `echo.attest.v1` en `EchoForgeMT5Exporter.java` (único archivo productivo, repo `xKoRx/symphony`). Baseline verificado pre-write: `origin/codex/f05-release-prep` @ `3d0e8c958765da23840e00bf1a0ac017fc47597a` (parent `0ddd4db`), blob exporter `cfbd5b78` exacto; worktree dedicado limpio (el worktree principal tenía un fixture de benchmark ajeno modificado, preservado sin tocar). Branch `feature/e06-runtime-attestation-exporter` @ `508b4a253dfb6cf6419dc5fc3f1be94801745a93`, push FF, sin merge/PR/master. Implementación: inserción por offsets tras `generate`+`assertNonZeroLots` (no movido), scanner estructural state-machine (comentarios/strings/chars/preprocessor, braces, duplicados), helper MQL5 `EchoAttestV1_*` con encoding v1 congelado (split mh/ml uint32 exactos — roundtrip max int64 verificado, `ts` escrito con `TimeGMT`, commit par ≥2, invalidación c=0, cleanup residual n(K+1)..n15, FNV-1a32 UTF-8 de ACCOUNT_SERVER con goldens, chunking big-endian n0..n15, límites nl 1..63), publish sólo en `return INIT_SUCCEEDED` literal (returns no literales o fall-through ⇒ fail-closed export), revoke primera sentencia de OnDeinit (append mínimo si falta), refresh §7.2a.4 v1.2.2 (OnTimer compatible preferido: `EventSetTimer(P)` único literal, statement top-level de OnInit, 0<P≤5, sin tocar EventSetTimer/EventKillTimer; si no OnTick oportunista; sin sitio exporta sin liveness prometida), idempotencia byte-stable por marcadores, post-condiciones byte-level (readback FromMQ5 espejo, línea MagicNumber y mmLots idénticas), cero llamadas de trading en el bloque. Contract tests §17 A–O + missing-OnInit PASS (22/22 suite), JUnit trades 13/13, RobustRun/WFM OK; build.sh PASS; `verify_build.sh` FAIL_BASELINE_KNOWN (carrera SIGPIPE `grep -q`+`pipefail`, falla igual en baseline puro 3/3; verificación semántica equivalente a mano: 5/5 exporters, 0 test-support). PHYSICAL_PENDING: sin terminal MT5 ni SQX Build 142 en esta máquina (no compile MQ5, no export real; AC-34/AC-35 esperan entorno físico; JDK portable Temurin 17 en /tmp fue requerido). Echo repo y resto de Forge intactos; Versions históricos intactos (identidad nueva por export futuro). Estado del lane: `IMPLEMENTED` + `SOURCE_VERIFIED` + `PHYSICAL_PENDING`. **E-06 NO CLOSED**; handoff al Manager.

- **2026-09-16 (TOP refresh liveness erratum — v1.2.2)** — Defecto: §7.2a.4 v1.2.1 exigía «MUST republicar al menos cada 5 s» con sitio `OnTick`; MQL5 no garantiza ticks cada 5 s ⇒ garantía temporal irrealizable. Decisión Manager frozen (sólo semántica de refresh): `OnTimer` existente realmente activado con período ≤5 s preferido; prohibido modificar `EventSetTimer` existente ni crear timer; si sólo `OnTick`, renovación oportunista — 5 s = intervalo mínimo entre publicaciones, no frecuencia garantizada; sin tick ni timer compatible nunca se promete liveness continua; expiración 15 s fail-closed `SUSPENDED + UNKNOWN`; recovery exige nueva atestación física matching con las transiciones §6 congeladas; ninguna actualización de `ts` desde Echo/Bridge/Gateway/config; cero cambios de trading. Tests AC-37a…d (contractual+físico; PHYSICAL gated por Version con inyección §7.2a.5). Scanner §7.2a.5: ausencia de sitio de refresh deja de ser fail-closed en export. CASE B, encoding v1 y resto de gates intactos. Source mutations 0 (Echo y Forge). HEAD `acf996ad043f87d6bbe6ae7b6190d1eb801e908a` (contrato `28afc47faf72b70e67b141b39224b8674f98458b`; old `336c723b`); push FF. Estado `E06_PLANNING_READY_FOR_IMPLEMENTATION_REVIEW`.
- **2026-09-16 (TOP transport contract correction — encoding v1)** — Defecto: `GlobalVariableSet` no transporta `{program_name, chart_ref, magic}` ni int64 magic sin pérdida; `GlobalVariableTime` no es publicación. SPEC v1.2.1 cierra encoding fragmentado lossless, vigencia `ts`, correlación chart/cuenta, inyección estructural Forge (no implementada). CASE B intacto. Source mutations 0 (Echo y Forge). HEAD `336c723ba46a7c04a1a6cc4390c6d5a4f15b56d7` (contrato `662c0dcef9fb17a5308ddcb974eabb6074c748aa`; old `e8fba410`); push FF. Estado `E06_TRANSPORT_CONTRACT_READY_FOR_MANAGER_REVIEW`.
- **2026-09-16 (TOP planning correction #2 — Manager CASE B)** — Manager resolvió CASE C: zero-order exige `effective_magic` físicamente atestiguado por la instancia strategy EA (excepción C-3 §7.2a: bootstrap runtime identity attestation, sin signals/deals/coverage/métricas/lifecycle/telemetría/estado). Discovery físico READ ONLY: producer = exporter Forge `EchoForgeMT5Exporter.java` (stamp `MagicNumber` input por `EchoForgeRobustRunExporter`; verificado por `magic-readback`; sello F-04). Transporte: variables globales terminal → relay verbatim collector `reference_status`. Identidad: bytes cambian ⇒ nuevo `strategy_version_ref`; históricos intactos fail-closed. SPEC v1.2.0; caso AC-26a/b/c; bloque CASE-C removido; reconciliación preservada en VERIFICATION.md. AutoTrading B2 intacto; coverage hook sigue DEFER. Source mutations 0 (Echo y Forge). HEAD `e8fba410347f6c60d036f9d03b2d0b1946d53e28` (contrato `3d5a5d627f5ed66e48479e24f6b664c5a973899b`; old `349b6ac8`); push FF. Estado `E06_PLANNING_V1_2_READY_FOR_MANAGER_REVIEW`.
- **2026-09-16 (TOP authority reconciliation)** — CASE C. Live Authority §5 vs Fable C-3 no cierran si zero-order exige echo físico de magic. SPEC v1.1.0 sin bump; §7.3 KNOWN_EMPTY no es implementable. AutoTrading B2 intacto. C-3 DEFER intacto. HEAD `349b6ac8` (contrato `1c794d5a`; old `3e190d86`). Source delta `v3/` = 0. Estado `E06_PLANNING_BLOCKED — MANAGER_DECISION_REQUIRED`. *(Resuelto después por Manager CASE B; ver entrada superior.)*
- **2026-09-16 (TOP planning correction #1)** — v1.1.0 @ `3e190d86` (contrato `ef8a96f3`; old `9989f399`). Heartbeat/UnifiedBatch no son autoridad zero-order. Producer congelado: `reference_status` Echo collector. Magic = inventario; KNOWN_EMPTY no se fabrica. AutoTrading = capability (B2). C-3 DEFER SQX conservado. Source mutations 0. Estado `E06_PLANNING_CORRECTED_READY_FOR_MANAGER_REVIEW`.
- **2026-09-16 (TOP planning one-shot)** — SPEC/PLAN/TASKS/VERIFICATION v1.0.0 @ `9989f399`. Hipótesis accounts/policies solos refutada; `reference_bindings` + intent. O1/O3 applied. 064 reservada. 0 source. Estado `E06_PLANNING_READY_FOR_MANAGER_REVIEW`. Puente padre → Review.

## 🧭 Decisiones (ejecución, no semántica nueva)

- Hijo de implementación de E-06; ownership sigue en [[Echo — Live Platform V1]], no Integration.
- OBSERVING nunca se sintetiza desde SQL/ACK/config/heartbeat/UnifiedBatch.
- Apply 064 SHARED DEV es ops gated por 061, no NORMAL.
- PHYSICAL V1 exige producer `reference_status`; fake ≠ PHYSICAL. Terminal MT5 real GAP-ECHO-006 pendiente no se disfraza de PASS.
- Hook SQX de coverage **no** se abre (C-3 DEFER). La excepción §7.2a es identidad runtime mínima, registrada como decisión Manager posterior explícita (2026-09-16), no reescritura del freeze C-3.
- Zero-order magic = fail-closed congelado (CASE B): atestación runtime == pin o no hay OBSERVING.
- Transporte §7.2a = encoding v1 sobre GVs del mismo terminal; magic nunca viaja como `double`; una GV existente no es instancia viva.
- Liveness §7.2a.4 (erratum v1.2.2): refresh = `OnTimer` compatible preferido sin tocar `EventSetTimer` / `OnTick` oportunista (5 s = intervalo mínimo entre publicaciones); sin sitio ⇒ sin liveness continua prometida; la expiración de 15 s es la autoridad fail-closed.

## 🔗 Docs / Links

- [[Echo — Live Platform V1]]
- [[Echo — E-04 Forge Ingestion E1]]
- [[Echo — E-03 Identity and BWC Foundation E0]]
- [[Echo — E-02 Control Safety, Auth and Journal Recovery]]
- [[Echo — E-05 Analytics Convergence A0]]
- [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]
- [[Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1]]
- [[Echo — Access & Physical Capability Matrix]]
- [[Echo — Producto Integrado]]

## 💡 Ideas

### Backlog de ideas

- Hook EA SQX exportado de **coverage**: DEFER (C-3), no V1. La excepción §7.2a (identidad runtime mínima) NO es ese hook y no lo preimplementa.

### Motivos / principios

- Ingestion no inicia el reloj. Una fila SQL no observa.

### Memoria pública / interna

- **Memoria pública:** contratos enlazados + SPEC del repo.
- **Memoria interna:** continuidad en esta nota.
- **Motivo:** el padre conserva el roadmap; este hijo conserva HOW/GATES.
