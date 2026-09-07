---
type: decision
schema_version: 1
scope: application
created: "2026-08-30"
updated: "2026-08-30"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Symphony]]"
related:
  - "[[2026-08-29-exporter-double-execution-root-cause]]"
  - "[[2026-08-29-durable-artifact-verified-reads-final-e2e-normal]]"
  - "[[echo-forge-golden-e2e]]"
aliases:
  - ARTIFACT VERIFIED READS cierre final
  - exporter hop correction certified
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-FINAL-E2E-RERUN-NORMAL
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/application
  - project/echo-forge
---

# 2026-08-30-durable-artifact-verified-reads-final-e2e-rerun

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Tras el RCA de doble ejecución del `overview_exporter` y la corrección `e241dd9` (sin E2E físico por mandato), quedaba pendiente el FINAL PHYSICAL E2E de Artifact Verified Reads. El intento previo 0.2.79 quedó BLOCKED (exporter fantasma, Kronos sin rotación, rollout solapado al intake).

## Decisión

- `EXPORTER_HOP_CORRECTION: PHYSICALLY_CERTIFIED` y `ARTIFACT_VERIFIED_READS: CERTIFIED_CLOSED / FROZEN` sobre release `0.2.80` (source `e241dd9`, SDK `ea09cc1`), golden run RequestID `final-verified-reads-e2e-normal-20260830T141439Z-5a1abb43`, FlowRun `646cdfbc-fe1d-4586-abef-ad2ad5d87eaa`, workflow COMPLETED y FlowRun COMPLETED.
- Contrato congelado: productor único de overview en durable V1 es el Builder inline (`01_builder/overview.ndjson` expected/written 20/20, job sqx `20260830_142021` dentro de la activity `project` id 11 / StageExec `488797b3`); `metadata/` top-level sin artefactos de exporter; `overview_exporter` ZERO en main y 36 children; `databank_metadata` 20/20 con `SaveExportRun` legacy DB ZERO; verified reads byte-exactos en toda la cadena.

## Rationale

- Evidencia física: flota 4/4 en `0.2.80` demostrada por path de binario del stager + SHA256 (`b0db6489…` linux, `0a763852…` windows) == manifest == builds locales, con Kronos `798248` rotado y verificado ANTES del RequestID; OLD_RELEASE_ELIGIBLE_POLLERS ZERO al despacho (ventana de rollout 240s con verificación en vivo). Cadena del representativo `00b6c838` (canónico `XAUUSD_L_H1_example_flow_25_v1_Strategy_6.1.21.k0`): F/M/E/H byte-exactos vs refs sellados (0e6ae132/9173d4be/bbe2688d/710b86a7); Apply con `stage_producer_outputs` (record-before-put) y evaluación sellada `e63e4691` consumida por el final reretester; write-once y N1/N2 físicos PASS en namespace aislado.

## Consecuencias

- No agregar más micro-tracks de Artifact Verified Reads; la feature queda CLOSED/FROZEN como los demás tracks durables certificados. NEXT EXACT: `DURABLE-RETESTER-OPTIMIZER-RECOVERY-RCA-TOP`.
- Deuda operativa observada (no bloqueante): exclusión `SCORE_NOT_COMPARABLE` en el ranking global es comportamiento de dominio preexistente (código intacto por `e241dd9`); Windows MT5 sigue sin canal de versión directa; canal SSH `echo-forge-worker` quedó validado como evidencia on-host.

## Alternativas descartadas

- Reintentar con la release 0.2.79 o reutilizar IDs (violación de la regla FIX → NEW RELEASE → NEW REQUEST ID → NEW FLOW RUN).
- Probes negativos físicos destructivos sobre el golden run (N3–N10): cubiertos por tests de integración exactos citados en el checkpoint; no montar mecanismos destructivos ad-hoc.
