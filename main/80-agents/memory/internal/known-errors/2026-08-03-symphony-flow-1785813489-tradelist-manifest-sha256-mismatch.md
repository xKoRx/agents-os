---
type: known_error
scope: session
tags:
  - kind/doc
  - kind/known-error
  - tech/symphony
  - tech/sqx
  - tech/echo-forge
  - severity/medium
  - status/diagnosed
created: 2026-08-03
updated: 2026-08-03
aliases:
  - 1785813489 sha256
  - tradelist manifest sha
  - sqx-main-1785813489 tradelist
---

# Known Error — Trade List manifest SHA256 no coincide con `.ndjson.gz`

## TL;DR

En los workflows `sqx-main-...-1785786248` y `sqx-main-...-1785813489`, el `sha256` declarado en `06_trade_list/*.trades.manifest.json` (`manifest.artifact.sha256`) **NO coincide** con el SHA256 real del archivo `*.trades.ndjson.gz`. El contenido del ndjson está bien (líneas correctas, schema válido), pero la integridad declarada es falsa.

## Síntomas

- `manifest.artifact.sha256` ≠ `sha256sum <file>.trades.ndjson.gz`
- Ejemplo verificado en `example_flow_71/Strategy_4.1.14`:
  - Archivo:  `40af38fa8ea23440683b96fb07f2df6ec8356bd1675735a8a4aeb9a804a47b1b`
  - Manifest: `189ac6feb38f37dcf49efb164fb45db686905411901734a840fd379d015d8f09`

## Causa raíz probable

El exporter calcula el SHA256 **antes** de que el `.gz` quede completamente cerrado en disco, o calcula el hash sobre el contenido uncomprimido (no sobre el archivo final comprimido). Patrón similar ya visto en bugs de publish MinIO del flow_69 (`Stat 404` resuelto en `0.2.29`, `Content-Type` en UserMetadata en `0.2.30`).

## Reproducibilidad

Determinable — afecta 100% de los `06_trade_list` de los flujos auditados (10/10 en `1785813489`, 13/13 en `1785786248`).

## Workaround

No bloqueante para la operativa. Validar integridad del `.ndjson.gz` directamente con `gunzip -t` + `wc -l` (debe coincidir con `manifest.trade_count`).

## Pendiente

Investigar el exporter que genera el manifest (probablemente `EchoForgeRobustRunExporter` o un paso posterior en el plugin Java) para calcular el SHA256 sobre el archivo final comprimido, no sobre el buffer intermedio.

## Referencias

- Auditoría `1785786248` (`example_flow_69`): mismo patrón.
- Auditoría `1785813489` (`example_flow_71`): patrón reproducido.
- Reporte: `/tmp/audit_e4_71/REPORT.md`