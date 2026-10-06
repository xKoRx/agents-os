---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-PLAN]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01-SOURCE-BAR-SDK-REMEDIATION

## Propósito

Persistir el resultado verificable del remedial SDK de BTG-S01 sobre barras OHLC nativas. Este hito corrige dos defectos del candidate en serialización TRADE y atomicidad de rechazo por modo; no certifica el corpus NQ ni ejecuta el backtest histórico.

## Contenido

### Resultado

Estado `READY_FOR_INDEPENDENT_REVIEW` en `xKoRx/echo` branch `codex/btg-s01-source-bars-remediation`, commit `407e03dd7ebce1f93b04ea5ff5bb5a33f1bac1ef`, publicado al remoto. El cambio repara F1: omite el modo `TRADE` redundante del JSON de `Builder` y lo reconstruye desde evidencia persistida, preservando el modo explícito `OHLC_1M` y su source high-water en restore; repara F2: preflight de conflictos TRADE/OHLC para todos los builders antes de admitir input, avanzar guardia, mutar grillas o agregar. Los artefactos SDD están en `xKoRx/echo:specs/btg-s01-source-bars-remediation/`.

### Evidencia

Los reproducers externos se ejecutaron sin editar sus originales, mediante archivos overlay temporales. El mismo trace sobre baseline certificado `cd451972b242c8933321e03001decd4b6d778c61` y el código corregido produjo bytes idénticos en `BarRecord`, `Builder`, `OwnerState` y `Version`; las pruebas permanentes pinnean hashes SHA-256 capturados del baseline, incluso Builder vacío, aceptado y descartado. El repro de modo mixto ahora rechaza con `SOURCE_MODE_CONFLICT`, cero efectos, owner input sequence sin delta, guard sin avance y estado de builders idéntico. La cobertura de `source_bar.go` fue 129/135 (95,56%); `ValidateTradeMode`, JSON marshal/unmarshal y recuperación de evidencia TRADE quedaron en 100%; `applySourceBar` dio 38/41 (92,7%) antes de documentar tres ramas redundantes inalcanzables. Los logs y perfiles del shot quedaron en `reports/source-bars-remediation/` en el workspace.

### Validación y límites

Pasaron las suites `v3/sdk/futures/bars`, `v3/sdk/futures/analytics` y `v3/sdk/futures/strategies/s2`, `go vet` de esos paquetes, `gofmt` y `git diff --check`, todo con `GOPROXY=off GOSUMDB=off` y namespace de red aislado para Go. La regresión permanente del older-closed-region y el calendario festivo verifican errores alcanzables sin mutación. Ningún parser, driver, venue, S2, GerardMM, accounting, economía, infraestructura o D6 cambió.

El corpus real sigue `NOT_ACQUIRED` porque la ACL de Windows denegó lectura del área visible; el rerun histórico queda `NOT_RUN`. Este gate es de SDK y sus unidades, no de resultado de mercado, owner acceptance ni cierre de BTG-S01. Tests nuevos son `PERMANENT_REGRESSION`; los overlays y logs son evidencia de verificación `DISPOSABLE_REPRODUCER`; reusable behavior candidates `NONE`; `PRO_CHAT_POOL_DELTA: 0`.

## Fuentes

- [[Echo Futures]] y [[BTG-PLAN]] — authority y continuidad del proyecto.
- `xKoRx/echo@cd451972b242c8933321e03001decd4b6d778c61` — baseline certificado para la comparación exacta de bytes.
- `xKoRx/echo@407e03dd7ebce1f93b04ea5ff5bb5a33f1bac1ef` — source candidate de remediation enviado a revisión independiente.
- `xKoRx/echo:specs/btg-s01-source-bars-remediation/VERIFICATION.md` — reproducción, correcciones, cobertura y límites de este gate.
