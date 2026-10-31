---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
related: []
aliases: []
tags:
  - kind/doc
created: "2026-10-31"
updated: "2026-10-31"
---

# Research — E1 Fee Model Conformance W1-q 2026-10-31

## Propósito

- Cerrar el incremento **offline** de conformidad del modelo documentado de fee que W1-p dejó como draft: comprobar la **aritmética y la contabilidad** del modelo `fee = C × rate × p × (1 − p)` con **elegibilidad `e = 1` solamente**, usando fixtures **sintéticos**, sin captura nueva, sin re-score del episodio, sin cuenta ni fondos y sin tocar L, los escenarios congelados A/S ni los gates de piloto.
- El criterio de aceptación es la **conformidad matemática/contable del modelo** con las fuentes y supuestos declarados. No es prueba de fee cobrada: `REAL_FEE_READY` sigue en `false` y el gap U-02 (`base_fee` ↔ `feeRate` ↔ settlement) sigue **abierto**.

## Contenido

### Resultado

- El modelo documentado con `e = 1` queda **conforme matemática y contablemente**, con **costo exacto** y sin redondeo del venue: 100 shares a `$0.50` con rate `0.05` cuestan `$1.25` (y `$1.75` a `0.07`, `$1.00` a `0.04`), el máximo de la curva está en `p = 0.5` y vale `C·rate/4`, `p` y `1 − p` cuestan lo mismo, `k·C` cuesta exactamente `k` veces, `rate 0` cuesta exactamente `0`, y la curva **no es globalmente monótona** (`p = 0.9` cuesta `0.45` contra `0.9375` de `p = 0.25`).
- El cobro por lado queda conforme con las fuentes: **BUY** paga `notional + fee` (la fee va por encima del collateral) y **SELL** recibe `notional − fee` (neto). Los roles quedan explícitos: el maker paga `0` **sólo** bajo la premisa `takerOnly` establecida; sin esa premisa su fee queda **sin resolver**, y lo desconocido **no** se convierte en `0` ni en una cota inventada.
- La elegibilidad queda limitada al modelo documentado: `e ≠ 1` **falla cerrado** (`KindUnsupported`) **únicamente en la vía documentada**, sin romper el contrato legacy que sigue admitiendo exponentes positivos. El legacy `TRUNCATE_6DP` (6 decimales) queda **intacto**: no se renombra ni se presenta como regla del venue.
- El redondeo del venue sigue **NO ADJUDICADO** (5 decimales, mínimo no nulo `0.00001`, sin floor/ceil/nearest publicados). La comprobación contra el camino truncante usa una **banda explícitamente HIPOTÉTICA**, condicionada al modelo `e = 1` y a los modos de redondeo considerados: **no es una cota certificada de cobro** ni una afirmación sobre fees reales.
- Verificación real: preflight `safe: true` (`writer_sites 48`, `source_files 38`, `sealed_unchanged: true`), **focal** `-run '^TestW1Q'` verde en `internal/regimes` y `internal/economics`, **suite completa** de los dos paquetes verdes, **build** de los dos paquetes con exit 0, `gofmt -l` vacío, `git diff --check` limpio y **commit local** `dee7a97` sobre la base `7c9adae`, **sin push**.
- No se conectó ningún helper a piloto, gate o estrategia: los escenarios A/S y L quedan sin cambios, `REAL_FEE_READY=false`, y no se certifica identidad de activo USDC/pUSD ni cobro alguno del pasado.

### El modelo y sus límites (lo que queda dicho y lo que no)

- **Fórmula**: `fee = C × rate × p × (1 − p)`, con `C` en **shares**, `p` precio de la share, `rate` el decimal documentado (nunca una re-interpretación en bps del cap `1000`) y la fee en **cash, la misma unidad condicional del quote**. Las fuentes no prueban identidad entre la etiqueta USDC (página de fees) y pUSD (collateral V2): el modelo declara su unidad **con incertidumbre**.
- **Redondeo**: la venue publica 5 decimales y mínimo `0.00001` pero **no** el modo; por eso la producción devuelve el valor **exacto** y no escoge redondeo del venue. La banda de los tests es un **dispositivo de modelado**, no una cota certificada.
- **Roles**: `takerOnly` es una **premisa** que entra como dato explícito (`nil` = desconocida). El maker paga `0` sólo con la premisa establecida; el fee del maker sin ella es *desconocido*, no cero.
- **Cobro**: BUY `notional + fee`; SELL `notional − fee`, con guarda que **falla cerrado** si el modelo dejara neto negativo (el `fee ≤ proceeds` está probado en el camino de proceeds, no como techo universal del lado BUY).
- **No se afirma**: que la fórmula, el coeficiente, el cap o la implementación fueran los del episodio del 29-10-2026; que se cobrara comisión alguna; ni que `fee_rate_bps = "0"` signifique ausencia de cobro.

### El cambio de producto (seam mínimo) y su alcance

- `internal/regimes/schedule.go`: la aritmética de `LevelCost` se extrajo a un helper **sin redondeo** compartido (`exactCost`), y se añadió `DocumentedE1Cost`, que devuelve el valor **exacto** del modelo documentado y **falla cerrado** con `KindUnsupported` cuando el exponente no es `1`. `LevelCost`, `truncate6` y `FeeSchedule.Validate` conservan firma, semántica, tipos de error y valores.
- `internal/economics/scheduled.go`: se añadió una vista del modelo documentado sobre el `WalkSideDetailed` y el `FeeSchedule` existentes (`DocumentedRole`, `DocumentedE1Quote`, `BuildQuoteDocumentedE1`): fee exacta por nivel, rol con premisa explícita, débito BUY y neto SELL. `BuildQuoteScheduled`, `BuildQuote`, `WalkSide` y `WalkSideDetailed` quedan intactos.
- **No** se añadió CLI, módulo, framework, adaptador de SDK, estado nuevo ni regla de estrategia; **no** se duplicó un calculador (la aritmética vive una sola vez) ni se actualizó ningún parámetro a partir de resultados.

### Finding real de dominio (detectado en revisión de fuente, corregido)

- **Defecto**: `BuildQuoteDocumentedE1` sólo invocaba la aritmética documentada en la rama **TAKER**. La rama **MAKER** (fee `0` bajo `takerOnly = true`, o fee del maker sin resolver) devolvía el quote **sin validar el dominio de precio de los takes consumidos**, porque `WalkSideDetailed` no valida precios: un book con `price = 0`, `1`, `−0.5` o `1.01` podía volver como quote MAKER resuelto, contra el dominio documentado de precios en `(0,1)`. Los tests de precio inválido existentes sólo ejercitaban el rol TAKER.
- **Corrección mínima**: el bucle por nivel se movió **antes** de la rama de rol, de modo que el dominio se valida para **todos** los roles antes de resolver fee o caja, reutilizando la validación y la aritmética del `FeeSchedule` (sin segundo validador ni generalización de exponentes). El rechazo conserva la causa propia del schedule y se clasifica `KindInvalidInput`; cualquier otro fallo sigue `KindInvariantViolation`. El motor legacy queda intacto.
- **Alcance de la evidencia**: el defecto se demostró **leyendo el flujo de control**, no con una corrida roja: la regresión `TestW1QDocumentedE1QuoteMakerRefusesInvalidPriceDomain` (MAKER × {premisa `true`, desconocida, `false`} × precios `{0, 1, −0.5, 1.01}` × {BUY, SELL} → rechazo; y book válido bajo `takerOnly` → fee `0` y caja igual al notional) **no se ejecutó contra el borrador defectuoso**, así que no se afirma línea base roja.
- **Ajuste de honestidad**: el helper de test `w1qVenueBand` pasó a `w1qHypotheticalBand` y los comentarios dejaron de presentar el intervalo `[floor5, ceil5]` como lo que el venue podría cobrar; es banda hipotética de modelado. La producción sigue devolviendo exactos y sin elegir redondeo del venue.

### Pruebas ejecutadas (resultados reales)

- **Focal**: `go test -p 1 -count=1 -timeout 5m -run '^TestW1Q' ./internal/regimes ./internal/economics` → `ok internal/regimes 0.008s`, `ok internal/economics 0.007s`.
- **Suite de los paquetes afectados**: `go test -p 1 -count=1 -timeout 10m ./internal/regimes ./internal/economics` → `ok internal/regimes 2.330s`, `ok internal/economics 0.010s`.
- **Build**: `go build -p 1 ./internal/regimes ./internal/economics` → exit 0, sin salida.
- **Higiene**: `gofmt -l` vacío en los cuatro paths; `git diff --check` limpio; `git status` con sólo los cuatro paths autorizados; preflight `safe: true` antes y después del focal.
- **Conteo honesto**: **11 funciones de test `TestW1Q`** en los dos paquetes (5 en `internal/regimes`, 6 en `internal/economics`), cada una con sus subcasos. No se afirma ninguna métrica de cobertura: la auditoría no la midió.

### Commit

- `dee7a977cdf67ad6aabdff374abecc9b0d0cdd0d` — `W1-q: conformidad offline del modelo documentado e=1` — 4 archivos, 1059 inserciones, 2 eliminaciones — **local, sin push**, sobre la base `7c9adaea59251b39ac1559db1ed63d4566996206`.

### Qué queda listo y qué falta para el siguiente paso prospectivo

- **Listo**: el modelo `e = 1` conforme y con costo exacto; la contabilidad por lado; la semántica de roles con premisa explícita; el límite de elegibilidad; la banda de redondeo declarada como hipótesis; la regresión del guard de dominio.
- **Falta**: (1) **recepción point-in-time** de la versión y la fuente del parámetro antes de cada decisión (el `fd` crudo observado no tiene respaldo de vigencias por mercado); (2) **precisión, unidad y premisas** con fuente fechada (modo de redondeo adjudicado, USDC frente a pUSD, etiqueta de fee-category, `rebateRate`, overrides); (3) **clasificación exploratoria frente a OOS** antes de que exista contenido que pueda contaminarse; (4) **criterios dados sin tuneo**; (5) la **decisión de L** del Owner, que requiere elegirla explícitamente —incluido si el código actual la incluye o la excluye como literal v1— y **no** puede derivarse de resultados ni cambiar la referencia de detección existente.
- **No se ejecutó nada prospectivo** en esta sesión: no hubo captura, ni replay, ni campaña, ni piloto, ni cuenta, ni micros, ni tokens, ni fondos. Para seguir offline no hace falta cuenta ni fondos. La aprobación de piloto o gate es aparte.

## Fuentes

- Vault: [[Research — Fee Formula Documentary W1-p 2026-10-31]] (fórmula, unidades, precisión no adjudicada, cobro por lado, roles y límites del gap U-02), [[Research — Target Fee Inventory W1-o 2026-10-31]], [[Research — Default Suite Isolation W1-nR 2026-10-30]], [[Polymarket Engine — MVP]].
- Producto: `internal/regimes/schedule.go` (`FeeSchedule`, `Validate`, `LevelCost`, `exactCost`, `DocumentedE1Cost`, `truncate6`), `internal/regimes/feeresolver.go`, `internal/economics/scheduled.go` (`WalkSideDetailed`, `ScheduledQuote`, `BuildQuoteScheduled`, `DocumentedE1Quote`, `BuildQuoteDocumentedE1`), `internal/economics/economics.go`, `internal/foundation/{decimal,units,errors}.go`.
- Tests nuevos: `internal/regimes/w1q_documented_e1_test.go`, `internal/economics/w1q_documented_e1_test.go`.
- Artefactos del shot: `validated-baseline/w1-q-e1-conformance-20261031/` (`implementation-ready.json`, `conformance.md`, `run-receipt.json`, `prereg-draft.md`, `scout-pack.json`).
