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

`INTEGRATION_MERGED_TO_MASTER_PROD_BLOCKED_ON_PG_ROLE` — el candidato fue verificado independientemente (echo: INTEGRABLE Y CORRECTO sin defectos materiales; symphony: GO CON RESERVA, reserva resuelta con c532150), integrado por fast-forward a `xKoRx/echo:master` (`40cb63eb..347eee8b`), desplegado en DEV (gateway+worker+front) y con PROD preparado (backup + ensayo de restauración + plan sellado). El rollout físico de BD/Hasura/PROD queda bloqueado por UNA dependencia externa demostrada: crear el rol `echo_v4_registry_owner` en PostgreSQL 192.168.31.220 exige CREATEROLE y ningún credencial accesible lo posee.

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

Demostrado: flow_run_start → begin_workflow_span (la actividad colgada del QA) → resolve (snapshot sellado en Mongo) → batch (lee trades+definición reales de S3) → finalize (reporte tipado) → seal. Reporte del run: selected=1, phase MAPPING, `ENVELOPE INVÁLIDO` en el ítem — el POST final no parte porque la validación compartida del envelope rechaza el fixture (semilla sin filas de identidad `sqx.strategy_versions`/`strategy_magic` — qavertical no las siembra). Última milla pendiente de una sola campo; el mapper M04 sigue CONFIRMADO por su batería de oráculos en-suite.

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

## Acción externa única para reanudar

Ejecutar como superusuario de PostgreSQL en 192.168.31.220 (idempotente con el guard de 068):

```sql
CREATE ROLE echo_v4_registry_owner NOLOGIN;
```

Punto exacto de reanudación: (1) aplicar plan V4 a `echo-develop` y `echo` con `apply-migration -v4 -migration-name <cada entrada> -manifest /tmp/lint-plan.json`; (2) Hasura delta manual (roles lab_readonly/lab_config_operator, tablas V4/V2, preservar event_triggers con header Authorization); (3) rollout de binarios PROD (mismos hashes BUILD.md) + unidad labv4-worker + artifact store durable; (4) smoke autenticado + observación ≥30 min.

## Límites vigentes

- REGISTER_ONLY es el recorrido operativo de la task nativa; PROVISION_REFERENCE sigue 503 hasta B5.
- AUTH_FORGE (autenticidad Forge física) sigue BLOCKED_EXTERNAL: la campaña usa el harness aislado autorizado.
- H45 (prepare p95≤2s @20k) y QA-01 (cobertura V4 <95%) permanecen FAIL adjudicados, sin nueva remisión.
- `requested_curve_profiles` NO es control efectivo del consumidor (Addendum §6).
