---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[F — Decision Register]]"
  - "[[SHOT3_ADVERSARIAL_REPORT]]"
  - "[[SHOT3_COVERAGE_MATRIX]]"
  - "[[SHOT2_IMPLEMENTATION_REPORT]]"
aliases: []
tags:
  - kind/doc
  - area/echo
created: "2026-10-26"
updated: "2026-10-26"
---

# SHOT4_FIX_PACKAGE — Ingestion V2

## Propósito

Entrega única a GLM-5.3-Flash Max LOCAL (D4): findings adjudicados del Shot 3 con criterio de corrección verificable, alcance restante J/L/F y manejo de excepciones históricas. Shot 4 = fixes + regresiones + verificación independiente dentro del mismo shot (D26). No Shot5. Este paquete no autoriza deploy, cutover ni integración a runtime.

## Contenido

### F1. Contexto congelado del paquete

- Artefacto base: xKoRx/echo `lab-v4/shot4-integration@d223d9f816338a831f5cf4c1acdc1c1ea9145917` (== candidate `feature/lab-v4-ingestion-v2`; remoto verificado por Shot3; trabajo nuevo desde HEAD refrescado con A4).
- Specs: [[B — Frozen Architecture]] (única SPEC), [[C — Implementation Shots and Acceptance Gates]] (gates), [[E — Executable Contract Examples]].
- Repros Shot3 conservados fuera del vault: `/srv/echo-work/ingestion-v2-shot3-20261026/harness/` (drivers `edriver-bin`/`odriver-bin` re-ejecutables, oráculos Python `oracle/wire_oracle.py` bit-exacto verificado, `qdriver/` con timing real de lease, E11 con PGs propias, perfiles de cobertura). Los repros de los findings se re-ejecutan en el SHA final con expected propio del verificador.

### F2. Findings a corregir (de [[SHOT3_ADVERSARIAL_REPORT]] R2)

| ID | Sev | Atribución | Corrección requerida | Criterio de aceptación (repro del auditor) |
|---|---|---|---|---|
| S3-A-01 | P2 | historical | Routing exacto en `handleStrategyIngestionV2` (v3/gateway/internal/lab_v4_gateway.go): POST sólo con path exacto `/api/v2/strategy-ingestions`; subtree sólo GET por id/by-key; sufijos ⇒ 404 sin efectos | POST `/api/v2/strategy-ingestions/extra` ⇒ 404 y cero filas en `strategy_ingestion_receipts`; E01 sigue PASS; regresión gateway rc=0 |
| S3-A-02 | P3 | new_delta (`2cef162c`) | Media type exacto en POST V2: parse (p.ej. `mime.ParseMediaType`) y comparar type/subtype == `application/json`; parámetros (charset) ⇒ 415 o decisión documentada en B3 con evidencia | `application/json; charset=utf-8` y `application/json-patch+json` ⇒ 415; POST válido 202; E03 sigue PASS |
| S3-A-03 | P2 | new_delta (`b085b8c0`/`d223d9f8`) | Eliminar `v3/core/echo-core` (ELF 40 MB, `vcs.modified=true`) con `git rm` en commit forward (sin rewrite/force-push); prevenir re-agregado (gitignore o regla de build) | `git ls-tree HEAD v3/core/echo-core` vacío en SHA final; historia intacta; build del harness `vcs.modified=false` |
| S3-A-04 | P2 | scope | Completar J (B7/B8: managed_context, journal owner único, dispatch mínimo, UNKNOWN_OUTCOME, gates con identidad exacta), L (B9: consumidor outbox, HistoryServiceV2 helper, snapshot N+1, delivered por event_refs) y F (B10: adapter Symphony durable + entry point candidate-local) con sus gates C3 (J01–J06, L01–L05, F01–F03) re-ejecutables | 13+ filas H NOT_RUN de J/L/F pasan a PASS/FAIL con evidencia; B7–B10 implementados según SPEC; sin campaña Forge ni merge Symphony compartido |
| S3-A-05 | P3 | evidence | Publicar cobertura del delta (QA01) en el reporte de cierre: por archivo, lógica ≥ 95% y wiring con plan explícito (clase estructural V4) | Reporte Shot4 incluye perfiles de cobertura del delta; los archivos lógicos nuevos/cambiados ≥ 95% statements |
| S3-A-06 | P3 | observación | Declarar identidad de build por buildinfo (`vcs.revision`+`vcs.modified`), no por SHA de bytes; registrar el fenómeno de no-reproducibilidad byte-level en el reporte | Nota en reporte Shot4; sin cambio de producto requerido |

Excepciones históricas (no se corrigen en este paquete, se reportan con no-regresión): H45 prepare p95 ≤ 2 s a 20k (FAIL histórico con piso medido del COPY; prohibido relajar presupuesto) y QA-01 V4 85,8/85,2 (adjudicación Owner pendiente del cierre V4). AUTH_FORGE sigue BLOCKED_EXTERNAL (X_AUTH_ARTIFACT): limita autenticidad, no gates con fixtures etiquetados.

### F3. Regresiones y re-verificación obligatoria de Shot 4

1. Repros de los 6 findings con los drivers/oráculos de Shot3 (expected propio del verificador independiente, no heredado).
2. Gates afectados por cada fix: E01 (routing), E03 (media type), E12 (inventario) tras S3-A-01/02; E10 regresión completa contracts + sdk/postgres + gateway rc=0; E11 re-run del protocolo de migraciones si Shot4 añade SQL (B11: números libres ≥ 086, jamás editar 067–085).
3. Superficies E+O que hoy PASS no deben degradar: H02/H03/H04/H06/H09/H10/H14/H35/H43/H46/H47/H48 se re-verifican en el SHA final (mínimo: los casos cuyos archivos toque el fix + gates E/O completos).
4. Al completar J/L/F: sus gates C3 completos + las 13+ filas H asociadas + conciliación de conteos en la matriz.
5. Verificación independiente interna de Shot4 (D26/D4): otra instancia GLM-5.3-Flash Max LOCAL fresca verifica SHA final, repros y regresiones con expected propio; sin auto-certificación.

### F4. Límites

- Sin fixes fuera de findings/delta; sin tocar runtime `feature/ef-runtime-pools`, flota, cuentas, extracción, sync.sh/.sync; PROD read-only; sin órdenes reales; harness propio con guard y cleanup por ownership (H47/H48); evidencia fuera del vault con índice de digests; documentación Agents-OS directo master con change_log consolidado; no cerrar Agents-OS; no iniciar Shot5.

## Fuentes

- Mandato Owner 2026-10-26 (D4); [[F — Decision Register]] D25–D27; [[SHOT3_ADVERSARIAL_REPORT]]; [[SHOT3_COVERAGE_MATRIX]]; [[SHOT2_IMPLEMENTATION_REPORT]]; [[B — Frozen Architecture]]; [[C — Implementation Shots and Acceptance Gates]]; [[H — Test Matrix Independent Oracles]].
