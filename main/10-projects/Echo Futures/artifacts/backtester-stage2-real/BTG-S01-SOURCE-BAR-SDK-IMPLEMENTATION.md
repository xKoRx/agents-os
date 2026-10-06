---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTG-S01-S2-1M-FORENSICS]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-06"
updated: "2026-10-06"
---

# BTG-S01-SOURCE-BAR-SDK-IMPLEMENTATION

## Propósito

Dejar auditable la implementación del prerequisito BTG-S01: ingestión SDK de
barras OHLC nativas de un minuto, sin depender de los bytes del corpus elegido.
La implementación no declara adquirido el corpus ni habilita un run real.

## Contenido

### Resultado

Commit `27cb4ceaf62151a042494022cad08e47672a06f2` en la rama
`codex/btg-s01-source-bars`, pusheada a `origin`. Añade `bars.SourceBar`,
validación y agregación directa a cada timeframe demandado; provenance
`OHLC_1M` conserva cada referencia y el conteo real, sin sintetizar eventos
TRADE. Los builders rechazan mezcla de modos, duplicados con payload distinto,
reordenamiento, solapamiento y corrección de agregados cerrados. `analytics`
admite sólo una causa de entrada, impone disponibilidad contra su reloj y
emite snapshots, cierres y timers por las rutas compartidas.

Estado: candidate congelado para revisión; **no aceptado**. La revisión TOP de
`27cb4cea` encontró una divergencia contra SPEC: `BarRecord` JSON/Version
coinciden con `cd451972`, pero la nueva persistencia de `Builder.InputMode`
añade `input_mode:"TRADE"` al JSON de `Builder`/`OwnerState` para entradas
TRADE. Los tests actuales no incluyen un oráculo byte-a-byte de esos envelopes.
El owner indicó mantener este SHA intacto y resolverlo con un worker remedial
separado; esta rama no se debe usar como aceptación final.

El estado mantiene visibles los minutos faltantes mediante referencias y
conteo; este SDK no completa huecos ni determina readiness de corpus. `Ring`,
forming snapshots y cada entrega de cierre copian la metadata mutable del
source para aislar a los consumidores.

### Archivos

- `v3/sdk/futures/bars/source_bar.go` y `source_bar_test.go` (nuevos).
- `v3/sdk/futures/bars/bar.go`, `builder.go` y `ring.go` (metadata OHLC,
  fencing persistente mínimo y copias de ownership).
- `v3/sdk/futures/analytics/engine.go` y `source_bar_test.go` (nueva causa,
  validación causal, preflight multi-timeframe y efectos compartidos).
- `specs/btg-s01-source-bars/{SPEC,PLAN,TASKS,VERIFICATION}.md`.

No se tocaron Strategy, MM, contabilidad de provider, driver/parser/venue,
infraestructura, trade-feed egress, archivos de NT ni estrategia general.

### Verificación

Desde `v3/`, en aislamiento de red y con `GOPROXY=off GOSUMDB=off`:

- `go test ./sdk/futures/bars ./sdk/futures/analytics ./sdk/futures/strategies/s2` — PASS.
- `go vet ./sdk/futures/bars ./sdk/futures/analytics ./sdk/futures/strategies/s2` — PASS.
- `gofmt -d` en los siete archivos Go cambiados — sin diferencias.
- `git diff --check` — PASS.

Oráculos incluyen valores OHLCV esperados independientes para 1m→5m y 1m→H4,
minuto faltante visible, límites half-open/break, repetición DST, disponibilidad
no lookahead, replay idéntico/conflictivo, orden/corrección/cierre, fence de
Builder tras descarte, falta de sesión y aislamiento de referencias para ring,
snapshot y subscribers.

Coverage bruto del package incluye código previo (bars 74.7%, analytics
32.6%). Para el source seam: `bars/source_bar.go` cubre 122/130 statements;
las ocho exclusiones son inválido timeframe después de `NewBuilder`, dos
órdenes viejos ya rechazados por el high-water previo, errores repetidos tras
validación pura de la misma fuente y `BarRecord.Validate` fallando por estado
interno corrupto. El cuerpo analytics `applySourceBar` cubre 47/52 statements;
las cinco exclusiones son builder persistido inválido o resultados de
resolución/aplicación repetidos después de preflight sin mutación intermedia.
Tras excluir únicamente esas defensas imposibles en el estado válido del
contrato, la cobertura aplicable de ambos caminos es 100%, superior al gate de
95%; perfiles brutos y líneas excluidas están descritos en
`specs/btg-s01-source-bars/VERIFICATION.md`.

### Límite de la evidencia

Los bytes del corpus NQ 1m siguen inaccesibles. No se añadió parser, driver,
venue, smoke-run ni afirmación de lectura del corpus, readiness real, aceptación
de S2 o rentabilidad. Las pruebas de paquetes pasan, pero la divergencia de
serialización persistida descrita arriba deja este candidato pendiente.

## Fuentes

- `BTG-S01-S2-1M-FORENSICS.md`, cápsula TOP `191bed4cc886c7ecf43664a292f1de48cdf0e59c`, apartado de SDK/source bars.
- Autoridad de owner `BTG-S01-OWNER-S2-BARS-AUTHORITY.md`.
- Especificación congelada y plan: `specs/btg-s01-source-bars/` en el commit del producto.
