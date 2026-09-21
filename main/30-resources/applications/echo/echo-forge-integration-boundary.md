---
type: resource
schema_version: 1
status: active
area: "[[Echo]]"
sources:
  - "[[Echo — Fuentes de implementación 2026-09-12 (f7ddea18)]]"
  - "[[Echo Forge — Fuentes de implementación 2026-09-12 (9fad768c)]]"
  - "[[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]]"
  - "[[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]"
  - "[[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]"
last_verified: "2026-09-21"
confidence: verified
aliases:
  - Echo — Forge Integration Boundary V1
  - Echo Forge Integration Boundary
  - frontera Forge Echo
tags:
  - kind/resource
  - area/echo
created: "2026-09-13"
updated: "2026-09-21"
---

# echo-forge-integration-boundary

Página compartida de la frontera Forge→Echo. Los contratos frozen son el source-of-record ([[Echo SDK — Canonical Forge Integration and Analytics Contract V1]], [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]], [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] y F-01…F-03); esta página documenta el ESTADO IMPLEMENTADO y los GAPS contra esos contratos, con baseline por repo. No crea un tercer producto ni un track paralelo.

**Baselines (last_verified 2026-09-21):** `xKoRx/symphony` línea certificada `codex/f05-release-prep` @ `745bc8b` (release `0.2.105`; `origin/master` `0b9742b` ancestro, FF pendiente) · `xKoRx/echo` `origin/master` `5dd998f1` + rama consolidada `origin/feature/e09-execution-copy-reconciliation-fidelity` @ `7c843e9c` (contiene E-04 recovery `4aad647b`; Gateway DEV desplegado `3d260e81`) · pin compartido en `sqx/go.mod` @ `745bc8b`: `v0.0.0-20260910031519-91671f6f46ff` (S0); el delta post-cert `145d6be` lo mueve a `v0.0.0-20260916211235-5dd998f16aea` (contracts) + sdk `c7f11496` (rama, sin merge).

## Contrato vigente (estable)

- Autoridad S0 compartida: paquete `v3/sdk/contracts` — `IngestionContractVersion = "forge-echo-ingestion.v1"`, `IdentityModelVersion = 2`, `HandoffManifestV1` (bloques producer/strategy/version/promotion; cross-checks G08–G12), receipt con único estado `INGESTED` ("never an activation"), recetas frozen `IdempotencyKey`/`PayloadDigest`/`StrategyVersionRef`.
- Receptor (SPEC E-04 v1.0.2, Spec-Active): endpoints frozen `POST /api/v1/forge/promotions` + GET by-key/by-receipt, auth `forge:ingest` con namespace `forge-live` desde credencial (nunca del body), orden §9 (replay lookup antes de artifact I/O, transacción única), matriz de errores (201/200/400/403/404/409×3/413/422×7/503), non-effects §11, separaciones `INGESTED ≠ PROVISIONED ≠ ACTIVE` y `INGESTION ≠ PROVISIONING ≠ OBSERVATION ≠ ELIGIBILITY ≠ CAPITAL ≠ ACTIVATION`. Detalle normativo: [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]].
- Productor (F-04 frozen en branch): producer `echo-forge-handoff` 1.0.0, membership exclusivamente estructural desde Decision `FINALIST_PROMOTION` V2 (rank/score nunca leídos, F-02), cero finalistas ⇒ cero manifests (G22), puerto `HandoffIngress` y máquina de estados `DeliverHandoff` (write-once, byte-equality gate, `UNKNOWN_RECEIPT` sin re-POST). Detalle: [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]].

## Estado implementado (volátil · last_verified: 2026-09-21)

- **Forge (emisor):** capacidad completa CERTIFICADA y en release cohesiva `0.2.105` @ `745bc8b` (branch `codex/f05-release-prep`; `origin/master` `0b9742b` es ancestro directo y sigue 38 commits atrás — FF pendiente). Producer `echo-forge-handoff`, delivery `DeliverHandoff` (write-once, byte-equality, fail-closed), **HTTPIngress real** (`sqx/adapters/echo-handoff/http_ingress.go`, de `feature/f04-handoff-ingress-fixes` @ `a2321cc`, contenido en 0.2.105) construido por `sqx/cmd/sqx-worker/main.go` desde ETCD `/symphony/<env>/echo/ingest/{base_url,bearer_token}`; sin claves → terminal `HANDOFF_CREATED` (0 POST, diseño). CERT-F04-01/02 + CERT-F05-01/02/03 PASS (campaña FULL `0ce72173…`, 3 finalistas, `HANDOFF_CREATED ×3`).
- **Echo (receptor):** endpoint operable; **el ingest funcional vive en la cadena `feature/e04-dev-ingest-recovery` (`2360369c`→`4aad647b`), HOY contenido en `origin/feature/e09-execution-copy-reconciliation-fidelity` @ `7c843e9c` y NO en `origin/master` (`5dd998f1`)**. Gateway DEV desplegado @ `3d260e81` (contenido en esa rama): ArtifactSource filesystem, acepta `policy_id=finalist_promotion@2.0.0` y `target_platform=MetaTrader5`, migración 064→068, ETCD bootstrap explícito, seed tests aislados. `master` todavía tiene `unavailableArtifactSource` (503 fail-closed) y NO acepta el manifest auténtico ⇒ merge de la rama consolidada es prerrequisito del ingest en master. Join físico certificado: CERT-E04-01 + CERT-F04-03 PASS 2026-09-21T04:18Z — golden F04-02 5×201 INGESTED + replay 200 + GET by-key + 409 `CONTRACT_CONFLICT` sobre Gateway DEV.
- **Producción HOY:** ningún byte de handoff cruza la frontera (ETCD `/symphony/production/echo/ingest/*` ausente ⇒ fail-closed; DEV tiene `/echo/development/gateway/forge_ingest/*` + `/symphony/development/echo/ingest/base_url` sembrados 2026-09-21).

## Cadena end-to-end (2026-09-21)

Builder→…→FinalistPromotion V2→Apply→seal→`DeliverHandoff` (dentro del pipeline, actividad `forge_seal_handoff`): con ETCD configurado el POST es automático (ruta HTTPIngress certificada por harness; combinación "campaña viva + claves ETCD" aún sin demo física — smoke operacional del primer join, no certificado nuevo); sin ETCD → `HANDOFF_CREATED` (demostrado en F05-C). Receptor Echo completo con ingest real 5×201 (Gateway DEV). Tras INGESTED: consumo downstream pertenece a Echo (E-06+ enrollment/execución).

## Ownership transferido a Echo (2026-09-21, mandato de cierre)

El attach/monitoring de MT5 demo y el deployment-link (viejo GAP EF-G07 / `NI-MP-1` / `NI-DL-1`) son **OWNED_BY_ECHO**: la spec `FEAT-SQX-ECHO-DEPLOYMENT-LINK` (Spec-Active BLOQ NI-DL-1, adapter `sqx/adapters/echo-api/` inexistente) queda superseded de facto por la cadena live de Echo (E-06 enrollment, E-09 ejecución/fidelidad, terminal real); Forge no la implementa ni duplica. Magic allocation, seal, membership estructural y manifests siguen siendo Forge.

## Gaps al 2026-09-21 (la wiki los documenta, no los resuelve)

- **G1 RESUELTO (transporte):** HTTPIngress en-pipeline + fail-closed verificados; falta sólo el smoke en-campaign con ETCD configurado.
- **G2 RESUELTO:** `SealStrategyVersion` con caller real en el pipeline (seal→manifest en `forge_seal_handoff`, certificado F04/F05).
- **G3 RESUELTO EN RAMA:** ArtifactSource filesystem en `feature/e04-dev-ingest-recovery` (desplegado en DEV); pendiente merge a `master` echo.
- **G4 RESUELTO EN RAMA:** reconciliación GET-by-key de 201 truncado (`a2321cc`, F-INT-01/02).
- **G5 RESUELTO:** golden auténtico F04-02 (corpus durable) INGESTED en Echo DEV — CERT-E04-01/CERT-F04-03 PASS.
- **G6 PARCIAL:** `FEAT-SQX-ECHO-INGESTION` sigue superseded de facto; `FEAT-SQX-ECHO-DEPLOYMENT-LINK` → OWNED_BY_ECHO (ver arriba).
- **G7 (abierto):** observability cross-boundary sin traza/métrica compartida definida.

## Deuda git de migración (exacta, 2026-09-21)

`symphony origin/master` @ `0b9742b` (38 commits atrás de la línea certificada — FF requerido); `codex/f05-post-cert-delta` @ `145d6be` (+2: fix F-INT-04, pin contracts→`5dd998f16aea`, sdk→`c7f11496` en rama `codex/telemetry-stderr-opt-in` sin merge a sdk master, refresh matrix DONE) verificado pero sin release `0.2.106`; lanes E-06 divergentes (`feature/e06-…-r3` +5, `codex/f05-r3-integration` +7); Explorer `codex/forge-explorer-v0` (+8) DEFERRED; secretos versionados por limpiar antes de mover historial. `MIGRATION_READY: YES` — destino recomendado monorepo `xKoRx/echo`, baseline `0.2.105` @ `745bc8b`.

## Lo que esta wiki NO afirma

- Que un byte de handoff haya cruzado a producción (falso hoy; el único cruce físico es DEV con golden certificado). Que la combinación "campaña viva + ETCD configurado + POST automático" esté demostrada físicamente (cada componente sí lo está; el smoke conjunto pertenece al primer join real). Que `master` de Echo pueda ingerir hoy (no: falta merge de la rama consolidada; el ingest funcional está desplegado en DEV desde `3d260e81`). Que INGESTED implique activación, provisioning, capital o eligibility en cualquier grado. Que magic sea asignado o validado por Echo (Forge-only). Que Explorer v0 sea producto (DEFERRED_BY_OWNER).

## Evidencia y provenance

- Cartografía Echo: artifact `02-echo-cartography.md` · Forge: `03-forge-cartography.md` · frontera: `04-echo-forge-boundary.md` (campaña [[Echo — Knowledge Base Consolidation]], verificación adversarial PASS con unknowns documentados).
- Repos (paths citables): `xKoRx/echo: v3/sdk/contracts/promotion.go` · `xKoRx/echo: v3/gateway/internal/forge_ingest_handler.go` · `xKoRx/echo: v3/sdk/postgres/ingestion_service.go` (+ `ingestion_service_test.go` / `ingestion_noneffects_test.go` como corpus de gates) · `xKoRx/symphony: sqx/core/forge/handoff_producer.go` · `xKoRx/symphony: sqx/core/capabilities/handoff.go` (+ `delivery_test.go` / `handoff_producer_test.go`).

## 🔗 Links

- Páginas: [[echo-forge]] · [[echo-core]] · [[echo-core-changelog]] · Índice: [[30-resources/applications/echo/00-index|Echo — Índice]]
- Contratos: F-01 · F-02 · F-03 · [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] · [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] · [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]
