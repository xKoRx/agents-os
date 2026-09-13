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
last_verified: "2026-09-13"
confidence: verified
aliases:
  - Echo — Forge Integration Boundary V1
  - Echo Forge Integration Boundary
  - frontera Forge Echo
tags:
  - kind/resource
  - area/echo
created: "2026-09-13"
updated: "2026-09-13"
---

# echo-forge-integration-boundary

Página compartida de la frontera Forge→Echo. Los contratos frozen son el source-of-record ([[Echo SDK — Canonical Forge Integration and Analytics Contract V1]], [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]], [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] y F-01…F-03); esta página documenta el ESTADO IMPLEMENTADO y los GAPS contra esos contratos, con baseline por repo. No crea un tercer producto ni un track paralelo.

**Baselines:** `xKoRx/echo@f7ddea18` (branch `feature/e02-control-safety-journal-recovery`; master `a99f9a63`) · `xKoRx/symphony@9fad768c` (branch `feature/f04-magic-version-handoff`; master `0b9742b0`; F-04 branch-only). Pin compartido: `sqx/go.mod` → `xKoRx/echo/v3/sdk/contracts v0.0.0-20260910031519-91671f6f46ff`, superficie idéntica al baseline Echo (diff = 1 línea de test).

## Contrato vigente (estable)

- Autoridad S0 compartida: paquete `v3/sdk/contracts` — `IngestionContractVersion = "forge-echo-ingestion.v1"`, `IdentityModelVersion = 2`, `HandoffManifestV1` (bloques producer/strategy/version/promotion; cross-checks G08–G12), receipt con único estado `INGESTED` ("never an activation"), recetas frozen `IdempotencyKey`/`PayloadDigest`/`StrategyVersionRef`.
- Receptor (SPEC E-04 v1.0.2, Spec-Active): endpoints frozen `POST /api/v1/forge/promotions` + GET by-key/by-receipt, auth `forge:ingest` con namespace `forge-live` desde credencial (nunca del body), orden §9 (replay lookup antes de artifact I/O, transacción única), matriz de errores (201/200/400/403/404/409×3/413/422×7/503), non-effects §11, separaciones `INGESTED ≠ PROVISIONED ≠ ACTIVE` y `INGESTION ≠ PROVISIONING ≠ OBSERVATION ≠ ELIGIBILITY ≠ CAPITAL ≠ ACTIVATION`. Detalle normativo: [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]].
- Productor (F-04 frozen en branch): producer `echo-forge-handoff` 1.0.0, membership exclusivamente estructural desde Decision `FINALIST_PROMOTION` V2 (rank/score nunca leídos, F-02), cero finalistas ⇒ cero manifests (G22), puerto `HandoffIngress` y máquina de estados `DeliverHandoff` (write-once, byte-equality gate, `UNKNOWN_RECEIPT` sin re-POST). Detalle: [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]].

## Estado implementado (volátil · last_verified: 2026-09-13)

- **Forge (emisor):** capacidad completa a nivel librería, SÓLO en branch F-04: `BuildHandoffManifest`, `DeliverHandoff`, stores PG 015 (`sqx.handoff_manifests` write-once G24, `sqx.handoff_deliveries` 6 estados), `SealStrategyVersion` (sin caller), `FakeConsumerIngress` (única ingress, in-process, tests CONTRACT). Pipeline cableado termina en FinalistPromotion V2 + Apply; magic V1 cableado en EXACTAMENTE un punto (Apply, opt-in `UseDurableMagicAllocation`, namespace `forge-live`, estampado en config del EA — no viaja en ningún handoff emitido).
- **Echo (receptor):** operable en reposo y presente también en master: rutas montadas al spec, Bearer constant-time, misconfig 503 fail-closed, `IngestionService.Ingest` con orden §9 completo y transacción única, copy de artefactos con allowlist + `FilesystemStore`, DB write-once (`echo.promotion_records` CHECK INGESTED, UNIQUEs G24, REVOKE), 30+ tests CONTRACT + non-effects.
- **Producción HOY:** ningún byte de handoff cruza la frontera. La única integración real es el pin del módulo `contracts` (tipos y recetas compartidas).

## Cadena end-to-end tal como está hoy

Builder→…→FinalistPromotion V2→Apply (Forge, operativo) → ✂ ROTURA 1: seal→manifest sin cablear → ✂ ROTURA 2: sin transporte de red (sólo FakeConsumer in-process) → receptor Echo completo y esperando (con ROTURA 3 en el primer accept: `unavailableArtifactSource` 503, G3) → tras INGESTED: NADA (cero consumidores downstream, E-06+ futuro).

## Gaps conocidos (la wiki los documenta, no los resuelve)

- **G1 (central):** no existe transporte real Forge→Echo; cierre requiere cablear seal→manifest→deliver en el pipeline Forge (ubicación hoy desconocida), cliente E-04 real que implemente `HandoffIngress`, y merge de F-04 a symphony master.
- **G2:** `SealStrategyVersion` sin caller — el manifest no puede construirse con datos sellados reales en producción.
- **G3 (bloqueante E2E):** Echo V1 sin backend de artefactos (`unavailableArtifactSource` 503 fail-closed); ningún primer accept posible aunque G1 se cierre. Forge tiene los artefactos en MinIO `sqx-strategies`; Echo no integra MinIO en V1.
- **G4:** reconciliación `UNKNOWN_RECEIPT` sin consumidor en Forge (el GET idempotente de Echo ya existe).
- **G5 (gate):** `FORGE_GOLDEN_FIXTURE_PENDING` — corpus S0 synthetic, producer del corpus `forge` ≠ `echo-forge-handoff`; T21/AC-37 CROSS_LANE GOLDEN no puede declararse PASS; E-04 INTEGRATED pero FINAL CLOSED = NO.
- **G6 (documental, repo-side):** spec conceptual `FEAT-SQX-ECHO-INGESTION` diverge del frozen (superseded de facto, citar sólo como historia); `FEAT-SQX-ECHO-DEPLOYMENT-LINK` (LinkDemoDeployment) sin receptor ni contrato.
- **G7 (unknown):** observability cross-boundary sin traza/métrica compartida definida. Nota de diseño (no gap): el header `Idempotency-Key` deberá derivarlo el cliente HTTP real vía `contracts.IdempotencyKey`.

## Lo que esta wiki NO afirma

- Que Forge publique/envíe estrategias a Echo (falso hoy). Que exista un flujo automático post-FinalistPromotion (no cableado). Que Echo pueda ingerir end-to-end (fallaría en artifact fetch, G3). Que CROSS_LANE/GOLDEN o el join Forge esté certificado (T21/AC-37 PENDING). Que el spec conceptual Forge describa el contrato real (superseded de facto). Que magic sea asignado o validado por Echo (Forge-only). Simetría de integración entre repos (receptor en master Echo; productor branch-only en symphony). Que INGESTED implique activación, provisioning, capital o eligibility en cualquier grado.

## Evidencia y provenance

- Cartografía Echo: artifact `02-echo-cartography.md` · Forge: `03-forge-cartography.md` · frontera: `04-echo-forge-boundary.md` (campaña [[Echo — Knowledge Base Consolidation]], verificación adversarial PASS con unknowns documentados).
- Repos (paths citables): `xKoRx/echo: v3/sdk/contracts/promotion.go` · `xKoRx/echo: v3/gateway/internal/forge_ingest_handler.go` · `xKoRx/echo: v3/sdk/postgres/ingestion_service.go` (+ `ingestion_service_test.go` / `ingestion_noneffects_test.go` como corpus de gates) · `xKoRx/symphony: sqx/core/forge/handoff_producer.go` · `xKoRx/symphony: sqx/core/capabilities/handoff.go` (+ `delivery_test.go` / `handoff_producer_test.go`).

## 🔗 Links

- Páginas: [[echo-forge]] · [[echo-core]] · [[echo-core-changelog]] · Índice: [[30-resources/applications/echo/00-index|Echo — Índice]]
- Contratos: F-01 · F-02 · F-03 · [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] · [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] · [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]
