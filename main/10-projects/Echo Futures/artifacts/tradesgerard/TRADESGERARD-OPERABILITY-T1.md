---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-13"
updated: "2026-10-13"
---

# TRADESGERARD-OPERABILITY-T1

## Propósito

Ejecutar F0 sin filtros con mínimos económicos, retiro EOD, pausa temporal y autoridad monetaria corregidos. Diez configuraciones: K01–K05 × solicitudes brutas2300/3000, misma ventana y perfil C4. Estado **RUNNING**, todavía sin resultados completos auditados. No es aprobación económica ni aceptación final del Owner.

## Contenido

Lanzamiento real supervisado con concurrencia1. Primer proceso PID/PGID2924374, F0–K01–r2300; `implementer/inputs/o7-F0-K01-r2300-plan.json`. Manager leyó progreso durable y confirmó proceso vivo con ps. Las nueve configuraciones restantes están en cola. Harness del integrador mantiene grupo, exit code, recibos y límites; no daemon ni promesa de ejecución fuera de esta sesión. Desarrollo H1 en checkout distinto del source/build congelado de T1; auditor consume únicamente COMPLETE íntegros con escritores drenados.

Identidad común: source `4f7594511d381483a161fc59cf0ae7ba00e2cbd1`, binario SHA256 `4ea8b12f3ea0a9ab2b47f5cbb173fb71b424d70cefde004ad82f9df6948ff9ac`, árbol limpio. Gate `verifier/independent-o7-gate.json` SHA256 `6a47a4fad3b5bc7cab8082f879ae180a6d596e98beb160ba41b4c5b4592d236b`, INDEPENDENT_PASS exacto; cobertura299/312=95,8333% de bloques afectados. Perfil `E2T_GAU50_PURCHASE_GE_20260706_OBS_20261012_SCENARIO_V1`. Warmup2025-10-13T17:51Z, trade_start2025-10-14T13:30Z, end_exclusive2025-11-25T23Z; entradas10:00–15:50NY por contrato. Inputs NQZ5 y sus hashes están congelados en `implementer/evidence/o7-freeze-manifest.json`; no MNQ, calendario alternativo ni reoptimización.

El control C4 conserva755cruces base en31fechas y caja final K01/K04=4760,K02=4280,K03/K05=4520 para cada retiro. Comparar después de auditoría completa: C4 permanece como observado, y el nuevo F0 incluye también reparación de valoración stale probada en C4, de modo que no se atribuirá toda diferencia al fallback o al retiro de cuentas. Rachas de campaña y cuenta/fase se conservarán separadas, con caja y ledger conciliados.

Admisión de recursos:792.200.724bytes nuevos existentes +40×4MiB reserva de trazas +64MiB de resultados/logs/filas =1.027.081.748bytes previstos, inferior al agregado1.610.612.736. Los4MiB por traza son reserva, no tamaño prometido: smoke gzip34708bytes/23operaciones, extrapolación755≈1,14MB. Disco libre10.961.649.664bytes y memoria available64.815.595.520bytes observados en admisión; load2,52. Se mantienen8GiB de reserva física,16MiB por traza/log físico,256MiB por lote y expansión de lectura, y scratch global≤2GiB. Medición continua puede detener un lote por límite real, que se reportará como fallo técnico y no pérdida de trading.

La salida NDJSON_GZIP_V1 preserva dinero, operaciones, cuentas, días y causas; recibo incluye encoding/path y hash de bytes cerrados. Decodificación streaming y reconstrucción MM_SIZING_ANCHOR_DELTA_V1 verificadas independientemente. No se han acreditado retiros nuevos ni se ha declarado clasificación económica de T1 en este corte de lanzamiento.

## Fuentes

- [[TRADESGERARD-OPERABILITY-T0]], [[TRADESGERARD-OPERABILITY-T0-VERIFY]], [[TRADESGERARD-OPERABILITY-K05-STREAK]], [[TRADESGERARD-ENTRY-REPAIR]].
- Evidencia relativa a ARANEA_ROOT: `work/tradesgerard-operability-20261013/implementer/evidence/T1-progress.json`, `T1-harness.log`, `o7-freeze-manifest.json`; planes individuales bajo `implementer/inputs/` y gate independiente bajo `verifier/` del mismo root.
- Requested TOP model `gpt-6.1-sol`, served UNKNOWN; integrador único y verificador independiente LOCAL. Manager coordina y documenta, no escribe producto/tests/scripts.
