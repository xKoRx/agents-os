---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[F — Decision Register]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-26"
updated: "2026-10-26"
---

# SHOT2_IMPLEMENTATION_REPORT — Ingestion V2

## Propósito

Reporte de ejecución de Shot 2 (C2/D2): implementación, gates, integraciones y estado exacto de entrega al workstream Ingestion V2. Modelo: GLM-5.3-Flash Max LOCAL. Sesión Agents-OS abierta; no auto-certificación; no inicio automático de Shot 3.

## Contenido

### S1. SHAs e integración (A4)

| Marca | Valor |
|---|---|
| BASE_SHA (remoto refrescado al inicio) | `b2b3ebfe3337b3b44034c5be3bf00b8379c8f1ce` (origin/lab-v4/shot4-integration, ls-remote 2026-10-26, ANCESTRY_OK) |
| Rama de trabajo | `feature/lab-v4-ingestion-v2` (nueva, desde BASE_SHA; nombre libre verificado en remoto) |
| ENDPOINT_SHA (gate E) | `0e45ebf4f499cc1a086c627b92977b022397b7f1` |
| Early merge E (A4.5) | ff-only `b2b3ebfe..0e45ebf4` → lab-v4/shot4-integration, push normal, ls-remote verificado |
| FINAL_SHA integrado (E+O) | `d223d9f816338a831f5cf4c1acdc1c1ea9145917` (ff-only `0e45ebf4..d223d9f8`, push normal, ls-remote verificado) |
| RESUME_BASE_SHA | `d223d9f816338a831f5cf4c1acdc1c1ea9145917` |
| Build auditado | echo-gateway-harness `vcs.revision=d223d9f8` `vcs.modified=false` SHA256 `9e01ded4b063ece0d913b22f8c20712c3ecc3fbdc3c0124ee18fc2bed6a45eec` (go1.27.1 linux/amd64 -trimpath -buildvcs=true) |
| Worktree de Shot2 | `/srv/echo-work/ingestion-v2-shot2-20261026/echo` (rama `feature/lab-v4-ingestion-v2` == d223d9f8, limpio) |

Commits del candidato (todos autocontenidos, sin commits ajenos intercalados — parent graph verificado contra destino): `613a0f16` (incremento E B2–B4), `2cef162c` (B3 Content-Type 415), `0e45ebf4` (firstCodeV2 sentinels), `b085b8c0` (incremento O B5/B6), `d223d9f8` (head CAS fuera de CreateBindingTx, cuentas no creadas por producto, digests sin stamps, installers SDK compartidos, seeds de operador). Divergencia 125/64 y colisión SQL 081: no se trasplantó nada de `feature/ef-runtime-pools` (referencia only; su HEAD remoto avanzó a `c2d71357` durante la sesión — registrado, sin acción).

### S2. Gate E — ECHO_INGESTION_V2_ENDPOINT_INTEGRATION_PASS (12/12 PASS)

Gates ejecutados con driver externo (`harness/edriver`, oráculo H/D receta propia sin importar SDK; readback SQL por conexión independiente read-only; worker detenido; gateway-harness real sobre PG propia 56127, artifact root propio, loopback 56229). Primera certificación en `0e45ebf4`; re-validación completa en `d223d9f8`: **12/12 PASS** (GATE_SUMMARY.json digest `a4161ec348ac11ee…`). Casos: E01 router/build (202/404/405/segmentos exactos), E02 auth/scopes (401/403/404 + cero efectos), E03 contrato (unknown/dup/UTF-8/415/413/declared_ref 422/definition digest 422/Idempotency-Key 400; version_ref recomputado por oráculo independiente), E04 registry (paquete definition-v1, crosswalk, definitions/links/instruments, Magic NULL, cero allocation events), E05 8 historias/413 en 9/última inválida revierte todo/PROVISION_REFERENCE sin efectos, E06 restart Gateway+PG snapshot idéntico + artifact bytes, E07 20 paralelos misma key (1×202 + 19×200, un receipt; respuesta-perdida → GET-by-key/misma key), E08 key-body 409/reutilización versión/paquete distinto 409 sqx-v1/race crosswalk converge/cero mutación original, E09 SIGKILL mid-POST sin estado intermedo/artifact store roto 503 sin efectos, E10 regresión (contracts+postgres+gateway suites rc=0 en el SHA), E11 migraciones runner V4 ledger (067–085: fresh+upgrade, reapply ALREADY_APPLIED schema idéntico, tamper → MIGRATION_CHECKSUM_CONFLICT pre-DDL, mid-fail 068 → rollback sin DDL parcial, ledger intacto), E12 loopback-only/0 órdenes/inventario.

Nota E05: la expectativa del POST dedicado de bindings evolucionó con el incremento O — la indisponibilidad transitoria 503 de E (`OPERATIONAL_PROVISIONING_NOT_AVAILABLE`) fue eliminada al implementar B5; en el SHA final, POST sin grant ⇒ 403 fail-closed (autorización antes que existencia). El camino PROVISION_REFERENCE dentro del envelope de ingesta sigue 503 sin efectos (el binding va por su endpoint/tx propia; B4).

### S3. Gate O — B5/B6 (5/5 PASS)

Implementación O (commit `b085b8c0` + `d223d9f8`): `contracts/runtime_binding_config_v2.go` (descriptor de profile, config canónica, stamps, catálogo cerrado CORE|BRIDGE|STATEFUN); `sdk/postgres/runtime_binding_service.go` (ProvisionBindingTx: profile resuelto server-side, assertions exactas, CAS de head por revisión con re-verificación bajo lock, receipt de mutación 085 append-only, replay key+digest, outbox para TODOS los required consumers del profile); `runtime_config_installer.go` en SDK (store de config + installer real apply→LOOKUP→proof estructurada; adaptadores B13 en `core/cmd/echo-core/` y `bridge/internal/` con wiring de producción en core main: sin `ECHO_LAB_NAMESPACE`/`ECHO_CORE_CONSUMER_ID` el supervisor queda fail-closed); supervisor V2 con claim scoped por (ns,kind,id), verificación de proof (digest/revision leídos) antes de ACK; `RenewACKLease` sólo con lookup exacto; readiness con DEGRADED (lease/incarnación perdida tras APPLIED); cuentas jamás creadas por producto (422 ACCOUNT_MISSING); migración 085 con runner/ledger.

Gates (driver `harness/odriver`, supervisores e installers REALES del SDK, perfil OBSERVE_MASTER, cero órdenes): O01 grants/targets alterados/CAS dos writers (1×202+1×412)/key conflict 409/cuentas sin creación automática; O02 consumidor detenido ⇒ PROVISIONING, apply+ACK exactos de todos ⇒ ECHO_OPERATIONAL_READY con expected/applied por consumidor, lookup real en stores Core y Bridge, trade_journal intacto; O03 lease vencida → recovery → redeliver idempotente, restart nuevo epoch mata READY, ACK con digest ajeno/regresivo rechazado, renewal con lookup correcto sí / divergente no; O04 gate nativo resuelve HEAD: READY pasa, REVOKED deniega, lease perdida ⇒ DEGRADED deniega; O05 dos bindings (runs/cuentas/consumers distintos) ambos READY, stores sin cross-talk, sin selección LIMIT1 arbitraria. Digest `O_GATE_SUMMARY.json` `ef67ba989ecffaef…`. Cobertura suites: contracts rc=0, sdk/postgres rc=0 (suite completa), gateway/internal rc=0.

### S4. Incrementos J/L/F — NO INICIADOS (diff restante exacto)

Por presupuesto de la sesión Shot2 no se inició J/L/F: cero código parcial escrito (nada que integrar a medias). Alcance restante según B7–B10/B13 sobre `RESUME_BASE_SHA=d223d9f8`:

- **J (B7/B8, gates J01–J06):** `managed_context` en envelopes reference/close/modify (`sdk/domain/reference_event.go` y envelopes); MasterObservationFn→JournalObservationServiceV2 (owner único, intake/receipt/ciclo pinneado/journal_change_outbox en la tx del journal, seq monotónico, compare-and-reject de mappings); legacy TradeJournalFn omite eventos V2; dispatch mínimo `execution.reference_dispatch_outbox` (B11, PK (ns,command_key)) insertado en la tx del journal para SIMULATED_EXECUTION; planner reconsulta head/readiness/grants/policy/MM con identidad exacta (eliminar `ORDER BY..LIMIT 1` del gate nativo por strategy); UNKNOWN_OUTCOME con lookup por command ID; simulador de broker/provider del harness.
- **L (B9, gates L01–L05):** consumidor del journal_change_outbox en `labv4-worker` (claim/fence/scope B11), HistoryServiceV2 helper transaccional para versión existente, snapshot N+1 acumulativo por grupo exacto `(ns,version,run_mode,run,source_instance,account,role)`, delivered sólo de event_refs incluidos, regresión de 4 curvas/2 rankings/cohortes/read bundle/UI (matemática V4 intacta).
- **F (B10, gates F01–F03):** `symphony` candidate-local hija de `lab-v4/shot4-symphony@a0c68d154b733049c97bf46e69c4629078d40c05` (refrescar al retomar): IngestionPersistenceV2 sobre handoff_manifests/deliveries existentes, entry point `sqx/cmd/echo-ingest-v2`, validación de receipt (schema/digest/producer/scope), AUTH_FORGE sigue bloqueo externo separado.

### S5. Evidencia, recursos y limpieza

- Evidencia completa FUERA del vault: `/srv/echo-work/ingestion-v2-shot2-20261026/harness/evidence/{e-gates,o-gates}/` (filas C1 por caso con source_sha/build_sha256/expected/actual/elapsed, GATE_SUMMARY.json `a4161ec3…`, O_GATE_SUMMARY.json `ef67ba98…`, regression.txt, logs del gateway por run). En el vault sólo este resumen con digests.
- Harness: manifest `harness_manifest.v1` run `935aa272` (namespace `labv4qa935aa272`-derivados por run; PG18.3 embedded propia en 56127 con ledger 067–085; PG auxiliares E11 en 56231/56233; artifact root propio; gateway loopback 56229/56241/56229 por driver; sin ETCD/Kafka/Hasura; PROD intocado; cero órdenes; `trade_journal` y tablas compartidas jamás tocadas fuera del harness).
- Limpieza ejecutada al cierre: pgboot propios (56127/56231/56233) detenidos por PID ownership, drivers/gateways propios terminados, sin killall ni borrado ajeno; residuo conocido pre-existente: `/tmp/w4-gomod-cold` (root-owned, 525M, de sesión anterior, NO tocado). Disco: sesión liberó 24G de go-build cache propio al inicio (`go clean -cache`).
- Limitaciones declaradas: AUTH_FORGE sigue BLOCKED_EXTERNAL (limita sólo autenticidad futura, no estos gates); H45/QA-01 históricos del Shot4 V4 se reportan con no-regresión (no re-abiertos); PG del harness es 18.3 (el contrato decía PG16; mismo protocolo de DDL, versión registrada honesta); StateFun/Flink no participó en O (perfil OBSERVE_MASTER no lo exige; su stamp/lookup entra con J/F sobre Kafka propio).

### S6. Handoff a Shot 3

Entrada: `RESUME_BASE_SHA=d223d9f8` en `lab-v4/shot4-integration` (== candidate branch). Verificaciones previas del auditor: SHAs remotos, `git log --oneline b2b3ebfe..d223d9f8` (5 commits, todos del Shot2, sin ajenos), module sums, migraciones 084/085 con ledger, evidence digests de S2/S3. Los gates E y O son re-ejecutables con los drivers en `harness/{edriver,odriver}` (no importan helpers del producto para los oráculos de identidad). Shot3 debe derivar expected propio desde fuente/raw facts; ningún PASS de este reporte se hereda.

## Fuentes

- Mandato Owner 2026-10-26 (D2); [[F — Decision Register]] D25–D27; [[B — Frozen Architecture]]; [[C — Implementation Shots and Acceptance Gates]]; [[A — Source Baseline and Branch Integration]]; [[E — Executable Contract Examples]]; [[H — Test Matrix Independent Oracles]]; [[Echo + Echo Forge — Environment Contract]].
