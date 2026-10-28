---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[A — Source Baseline and Branch Integration]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-28"
updated: "2026-10-28"
---

# CIERRE LAB V4 + INGESTION V2 — Ventana 2026-10-28

## Resultado

`DEV_OPERATIONAL` — The Lab V4 + Ingestion V2 operan de punta a punta en DEV (Owner confirmó: NO desplegar en PROD). Cadena verificada con evidencia física: ingesta V2 autenticada (202 + receipt), persistencia con estados honestos, replay idempotente, conflicto 409, artifact readback por digest, acción Hasura vía auth hook del gateway, screener V4 mostrando la estrategia con NO_HISTORY/NO_PUBLISHED_ANALYTICS y detalle sin ceros inventados. El alcance PROD de la misión fue DESCARTADO por orden explícita del Owner durante la ventana.

## Candidatos integrados

| Repo | Rama | SHA | Contenido |
|---|---|---|---|
| xKoRx/echo | `wrk-labprod/c-int` | `347eee8bdab7f7628629af6383d1e45520815abd` | master 40cb63eb + B 2daa58da (runtime+Lab V4+Ingestion V2, 91 commits) + C 24af7862 (forge-task contracts, 4 commits) + correctivos de integración |
| xKoRx/symphony | `wrk-labprod/prod-v2` | `3632591fd499d8c0e5a969f1fb4c5ab108873479` | productor 7731cb8 + Shot 4 (P1 QA-S3-05/06/08 + 9 defectos del run E2E) |

Ancestría verificada: master 40cb63eb es ancestro del candidato echo (merge fast-forward posible). El tag inmutable `v3/sdk/contracts/v0.0.1-forge-ingestion-task.2` coincide byte a byte con los contratos del candidato — no fue necesario publicar tag nuevo ni re-pinnear el productor.

## Conflictos de integración resueltos (por contrato, no ours/theirs)

1. `handler_test.go` (automation): el oráculo de valor exacto de master (JSONEq con jsontext.Value) prevalece sobre la relajación de B.
2. `master_observation_service.go`: EC-03 del addendum — `available_at` es evidencia VERSIONAL; el journal NO la acredita (UNKNOWN/NOT_DECLARED_BY_JOURNAL) y JAMÁS se infiere del max-close de actividad.
3. `strategy_history_v2_{put,service}.go`: guard EC-03 (existing_ref sin redeclaración no toca metadata versional) + write-ahead pre-tx y artefacto real de B (H14/B-06); `NewNativeHistoryServiceV2` (store obligatorio ruta nativa) conservado.
4. `1622c762`: master remoto NO compilaba v3/core — `.gitignore:73 echo-runtime-control` (patrón para el binario) sepultaba `expected_roster.go` + 2 tests sin commitear. Rescatados con `add -f` y patrones anclados a `v3/core/`.

## Verificación independiente (agentes frescos sin autoría)

- **Echo @347eee8b — INTEGRABLE Y CORRECTO, NO REFUTADO.** Traza/ancestría/tag idéntico byte a byte; merges con cero ediciones semánticas ocultas (`diff-tree --cc` vacío); master REALMENTE no compilaba sin el rescate (repro incluido); oráculo anti-takeover presente y más estricto; suites sdk/postgres (161s), contracts, E11 y gateway RC=0 contra PG18 real. Notas no materiales: el commit del rescate en historia es `8185c306` (amend de 1622c762); ambigüedad de atribución ACK sólo si un writer declara `kind` Y `kind/default` — degrada a BLOCKED, jamás concede READY ilegítimo.
- **Symphony @3632591 — GO CON RESERVA → resuelta.** P1s cerrados probados sobre PG real; sin contra-ejemplos en validadores de evidencia (prueba empírica con `Evaluation.Validate()` productivo); contrato/build/vet sin regresiones. Defecto material D1: guardas `IsRegisteredLastAndAdditive` de 015/016 esperaban ser últimas → corregidas a aditividad ordenada en `c532150` (suite completa verde 58s), pusheado. Pre-existente no atribuible: `TestDecisionStore_ListFlowRunSelectionDecisions` (falla en base y candidato). UNKNOWN resuelto: el PG QA quedó con 017/018/019 en ledger (qavertical aplicó con el runner corregido).

## Correctivos del productor (symphony, 13 commits en Shot 4)

- QA-S3-05: `ordered` incluye 017/018/019 + init-panico que congela "toda migración embebida ∈ ordered".
- QA-S3-06: migración 019 aditiva (decision_ref opcional, CHECK retirado, unique queda como guarda legacy); SaveManifest manda NULL real; meta nil jamás fabrica `decision:<key>`.
- QA-S3-08: worker data_only registra begin/group span + FlowRunStart/Seal con Foundation fail-closed; el gate de ciclo de vida queda ACCEPTING tras `w.Start()` (en Starting el gate rechazaba toda activity con `worker_draining`).
- Del run E2E real: SpanID nil-guard en el workflow (el span es observabilidad, no identidad); TelemetryCarrier en los 3 requests de la task; sink de snapshot/report con identidad canónica (IdentitySchemaVersionV1, refs UUID deterministas, sujeto FLOW con Ref+Digest, Ref por NewEvaluationRef del agregado, BuildRef, documentos `{}`).

## Campaña E2E real (harness aislado QA + binarios candidatos)

Stack: Temporal 7233 (ns qa-shot3), etcd 7439, Mongo 27417 (forge_qa), Garage S3 8344, PG 56438 (productor) + PG18 54338 (Echo, catálogo 091) + gateway candidato :8095. Task nativa `echo_ingestion_v2` sometida por workflow raíz Generic real (`sqx-main-v1-<token>`).

Demostrado: flow_run_start → begin_workflow_span (la actividad colgada del QA) → resolve (snapshot sellado en Mongo) → batch (lee trades+definición reales de S3) → finalize (reporte tipado) → seal. Reporte del run: selected=1, phase MAPPING, `ENVELOPE INVÁLIDO` en el ítem — el POST final no parte porque la validación compartida del envelope rechaza el fixture (semilla sin filas de identidad `sqx.strategy_versions`/`strategy_magic` — qavertical no las siembra). Última milla pendiente de un campo; el mapper M04 sigue CONFIRMADO por su batería de oráculos en-suite. NOTA: el stack QA es compartido con otra sesión activa del programa (qa4) — no tocar sus procesos/fixture nuevos.

## Caso C completo por HTTP real (gateway candidato :8095 + PG18 + artifact store)

- POST `/api/v2/strategy-ingestions` REGISTER_ONLY histories=[] con source_evidence válida → **202 INGEST_ACCEPTED**, receipt `1291300d-3304-4bad-9a58-ca70d6372a22`, versión `sha256:e4fa2eea…`, runtime `sv2:7d347eb2…`.
- GET por receipt_id → 200 mismo snapshot; GET por `by-key` → 200 mismo receipt.
- Replay mismo body+key → 200 mismo receipt (`replayed=true`, cero duplicados).
- Misma key con body distinto → **409 IDEMPOTENCY_CONFLICT**.
- Persistencia: `strategy_versions`=1, `strategy_version_metadata` rev 1 sellada, `strategy_histories`=0 (sin historia ficticia), snapshot del receipt con `HISTORY_NOT_REQUESTED`, sin outbox de dispatch (REGISTER_ONLY), definición runtime `sv2:` creada.
- Artifact readback: bytes canónicos del request en el store direccionados por sha256 (`e05001d0…`), redecodifican al mismo envelope.
- Envelope aceptado también por el servicio contra PG directo (probe `AcceptIngestionV2`): receipt `a079e294…` + replay idempotente.
- La receta del digest de definición es `DigestTagged("echo-strategy-definition-content.v1", manifest)` (no sha256 plano del canónico) — nota operacional para productores manuales.

## Suites del candidato echo @347eee8b (PG18 54338, catálogo 091 completo)

- `v3/sdk/contracts` (GOWORK=off): OK — incluye goldens fakeconsumer.
- `v3/sdk/postgres` (LABV4_TEST_DSN): OK completo tras 3 tests stale actualizados al contrato congelado + fix de identidad declarada en AcceptACK.
- `v3/toolkit/cmd/apply-migration` E11 (TestIntegration): OK.
- `v3/gateway`, `v3/lab-worker`, `v3/bridge/internal` (catálogo completo), `v3/futures-bridge`, `v3/futures-projector`, `v3/core/cmd/echo-runtime-control`, `v3/core/cmd/echo-core`: OK.
- Fails pre-existentes adjudicados (NO introducidos por la integración, presentes en master y en B): `core/internal/functions` TestEconomicMinimumCoreTypedConfigAndProtectionParity (fixture LIVE usa autoridad fixed-OHLC que el guard congelado rechaza — recordatorio shot4), `v3/e2e` TestFullFlow, módulos v1/v2, wiring del backtester (fuera de alcance).

## Despliegue DEV (daedalus)

- Release construida con VCS: `/opt/echo-dev/releases/347eee8b…/` (echo-core, echo-gateway, echo-runtime-control, lab-worker; vcs.revision sellado, vcs.modified=false).
- `current` → candidato; `echo-gateway-dev` y `echo-lab-worker-refresh-dev` activos sobre él.
- ETCD DEV `/echo/development/gateway/lab_v4/*` provisionado (cursor_key, artifact_root, identities lab-cert producer_ingest+lab_readonly, service token; credenciales en `etc/lab-v4-dev-creds.env`, mode 600).
- Rutas V2 montadas: POST sin auth → 401; con auth → 400 estricto. Core/Flink SIN tocar.

## Preparación PROD

- Backup `echo` @.220: `backups/echo-prod-20261028T160339Z.dump` (27,8 MB, Fc) — restauración ensayada 105/105 tablas en PG18 local, estado pre-067 confirmado (sin ledger, prereqs 067 4/4).
- Plan de migraciones sellado desde el candidato: 24 entradas (067–080 + 082–091; 081 excluida por colisión de linaje; 087–091 convergencia con .verify.sql; PG17+ requerido por MAINTAIN en 087+). Manifest: `/tmp/lint-plan.json` (regenerable con `-integration-plan -print-manifest`).
- Hasura PROD v2.38.0: metadata consistente. El repo `v3/hasura/` NO contiene event_triggers ⇒ delta manual obligatorio preservando triggers/headers/permisos productivos (antecedente 2026-09).
- Bloqueo único demostrado: `echo_v4_registry_owner` ausente y ningún credencial accesible (echo_user, mcp_echo_dev_rw, sqx) tiene CREATEROLE; superusuarios `postgres`/`admin` existen en .220 sin credencial disponible. La migración 068 (bytes congelados) ejecuta `CREATE ROLE echo_v4_registry_owner NOLOGIN` guardado por IF NOT EXISTS.


## Operación DEV ejecutada (tras el desbloqueo del Owner)

1. **BD `echo-develop`**: rol `echo_v4_registry_owner` + membresía (Owner); GRANT CREATE en schemas echo/execution al rol (071-owner). Catálogo completo: 24/24 V4 (067–091; 090/091 aplicadas como `sqx` con search_path=public por verificación de dueño; FK exigía prefijo de schema) + banda legacy 061–066 convergida (061 requería traspaso OWNER de 11 tablas históricas de `admin` → `echo_user`, ejecutado por el Owner). Postcondiciones: 24 entradas de ledger APPLIED, función protegida owned por el rol, `strategy_definitions.id` → text.
2. **Hallazgo PG17**: el REVOKE UPDATE de 061 (write-once identidad) rompía el `FOR KEY SHARE` del chequeo FK en PostgreSQL 17 (exige UPDATE en la tabla referenciada). Resuelto con GRANT UPDATE a `echo_user`; la inmutabilidad REAL queda garantizada por el trigger `trg_strategy_versions_write_once` (verificado: UPDATE de negocio sigue bloqueado con IDENTITY_BWC_WRITE_ONCE).
3. **Gateway/worker/front DEV**: binarios del candidato 347eee8b activos (gateway :8090, lab-worker D4, labv4-worker V4 nuevo con unit `echo-labv4-worker-dev`, front :4173 con build horneado VITE_SESSION_TOKEN=lab_readonly).
4. **Hasura DEV** (.75:8080): actualizado v2.38 → v2.50 (la acción query exige el formato nuevo), recreado con source `echo_lab_v4` + `ECHO_LAB_V4_SERVICE_TOKEN` (Bearer) + auth hook `:8090/api/v1/auth/hasura`. Delta aditivo sin apply ciego: source añadida, 15 vistas `lab.v4_*` trackeadas, 30 permisos select (lab_readonly/lab_config_operator), custom types + acción `lab_v4_screener_page` (kind sync/type query) + permisos de acción. Metadata consistente (0 inconsistentes), 6 event_triggers productivos preservados verificados en export pre/post.
5. **Smoke V2 en DEV real**: POST autenticado `dev-smoke-register-4` → **202 INGEST_ACCEPTED** receipt `6502f6e3-bf3a-415d-95fe-78b4c0a0e89e`, versión `sha256:e4fa2eea…` (idéntica a la del caso C local — determinismo cross-entorno), runtime `sv2:00cca3ed…`; replay → 200 mismo receipt; GET id/key → 200; persistencia lab-cert verificada (metadata rev 1, histories=0, HISTORY_NOT_REQUESTED, instruments [NQ]).
6. **UI The Lab V4** (navegador real): screener muestra "QA Register Only" con Resolución NO_HISTORY, Estado analítico NO_HISTORY+NO_PUBLISHED_ANALYTICS y guiones — sin curva plana, score cero ni rank inventado. Detalle: identidad, curva "sin puntos publicados (…sin ceros inventados)", calendario "GAP/OUTSIDE_COVERAGE ⇒ sin datos, nunca verde cero falso", operaciones/candidatas/copias honestos. Captura de screener en artifacts de sesión.
7. **PROD**: DESCARTADO por orden Owner ("NO VAMOS A DESPLEGAR EN PRODUCCIÓN"). El backup `echo-prod-20261028T160339Z.dump` y el plan sellado quedan como material de preparación sin ejecutar contra PROD; ninguna mutación PROD ocurrió (sólo lecturas y el backup).

## Nota de alcance

La sección de acción externa del informe intermedio quedó obsoleta: el Owner creó el rol, concedió la membresía y ejecutó los traspasos de OWNER en `echo-develop`; PROD fue descartado explícitamente. No queda ninguna acción externa pendiente para DEV.
