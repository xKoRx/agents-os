---
type: doc
schema_version: 1
status: active
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
related:
  - "[[Research — W1-j Causal Gate Diagnosis 2026-10-30]]"
  - "[[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]]"
  - "[[Preregistration — PE-005-R1 Economic Candidate W1-g 2026-10-29]]"
  - "[[Research — Public Market Capture W1-d 2026-10-28]]"
  - "[[Research — Prospective Metadata Quality W1-e 2026-10-28]]"
  - "[[Polymarket Engine — Continuidad Five-POC 2026-09-20]]"
aliases:
  - "W1-l minimal economic instrumentation"
  - "W1-l spec instrumentación mínima"
tags:
  - kind/doc
  - topic/research-ops
created: "2026-10-29"
updated: "2026-10-29"
---

# Plan — Minimal Economic Instrumentation W1-l 2026-10-30

## Propósito

- Especificación mínima implementable (SIN implementar) de la instrumentación económica del piloto PE-005-R1: qué ya existe en el journal y en el harness, qué falta exportar al reporte JSON, y qué corresponde a decisión Owner. Entregable único: lista priorizada de deltas imprescindibles con archivos afectados, criterio de aceptación y clasificación (instrumentación técnica vs cambio económico Owner). Este shot no ejecuta código, tests, build, replay, extractor ni captura; no reanaliza el episodio; no crea framework ni replay duplicado — reutiliza el Engine y la ruta de revisión existente.
- Adjudicación Metis aplicada (autoritativa): el veredicto W1-k de conformidad estricta por silencio NO fue aceptado. La v2 ([[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]]) reemplaza en alcance las siete correcciones W1-h y MANTIENE el enunciado v1; su única atadura temporal («señal, elegibilidad y referencia usan sólo frames recibidos ≤ instante de decisión», v2 §5) usa el operador ‘≤t’, compatible tanto con INCLUIR como con EXCLUIR el frame actual de la referencia. El estado correcto del documento es AMBIGÜEDAD DOCUMENTAL de la regla de L: sin afirmar bug temporal (ninguna referencia lee frames posteriores al instante de decisión — hecho de código verificado) y sin afirmar conformidad estricta (el texto no fija la regla). Errata aplicada al inicio del informe existente con historia preservada.

## Fuentes leídas en este shot (lectura directa, sin inventario por shell)

- Código (checkout `polymarket-engine`, rama `w0/offline-causal-replay-20261027`): `internal/strategy/pocs/sports/sports.go` (congelado v0.1), `cmd/researchpilot/economics.go` (análisis + revisión W1-j), `cmd/researchpilot/supervisor.go`, `internal/economics/economics.go` (WalkSide/Sweep/BuildQuote), `internal/economics/scheduled.go` (WalkSideDetailed/LevelTake/BuildQuoteScheduled), `internal/regimes/schedule.go` (FeeSchedule.LevelCost price_square_v1 TRUNCATE_6DP), `internal/regimes/feeresolver.go` (FeeResolverV1/BpsToFeeCoefficient).
- Documentos: informe W1-j/k, prereg v1 y v2 (completos), continuidad §§18 (bullets 24–33), W1-d, W1-e. Manifiestos autorizados: `validated-baseline/w1-d-public-capture-20261028/selection-manifest-v6.json` y `capture-manifest-v6.json` (4 mercados 6013297/6013337/6013387/6013310, kickoffs 2026-11-18; 103 registros; prereg binding `5069f924…`).
- Fees oficiales: NO se consultaron nuevas fuentes web; valen las citas ya registradas as-of 2026-10-29 en el prereg v1 §5 (docs.polymarket.com `trading/fees`, `changelog/predictions`, clasificación VERIFICADO/NOT_VERIFIED en la spec W1-g), con vigencia desconocida para nuestros mercados.

## Hallazgo central: déficit de REPORTE, no de captura

- El journal sellado contiene los libros completos por frame: el harness reconstruye el libro desde los payloads WS (`economics.go` `isMarketWSData`/drain, líneas 312–321 y 355–378) y renderiza cada frame con `shardSnapshot` (líneas 254–268) incluyendo `BidBest`, `AskBest`, `Quality`, `Seq`, `LastSourceMs` y `Extras` con los niveles (`pocdata.ExtrasAsksTop/ExtrasBidsTop`). La ruta de revisión además ya calcula spread y mid por frame desde bid/ask (`spreadBpsReplica`, líneas 966–994; anillo en 1251–1257).
- Por lo tanto la ventana de referencia con identidad (seq + bid/ask/mid por frame), L, la entrada realmente barrida, la salida full-size H con WalkSide, las razones de no ejecución y los timestamps efectivos son EXPORTACIÓN de datos ya presentes en memoria del harness. La frase del informe «el bid/mid del frame de referencia no viajan en la fuente autorizada» describe el ARTEFACTO sellado (`93e7fe79…` / `a1fc1d73…`), cuyo formato de fila omite esos campos — no el contrato del journal. Confundir esto con necesidad de otra captura sería falso.
- UNKNOWN declarado (sin inventar): si `pocdata.EncodeLevels` acota la cantidad de niveles codificados en `Extras` (paquete pocdata no leído en este shot). Es irrelevante para top-of-book bid/ask/mid y para reproducir exactamente lo que la estrategia congelada usó (ella misma consume `DecodeSide` de esos mismos Extras); sí acotaría la granularidad de un análisis de profundidad más fino que el usado por el gate.

## Deltas imprescindibles (priorizados)

### P0-1 — Regla de L explícita en preregistro (Owner; documental)

- Qué: el próximo preregistro que toque el piloto debe fijar explícitamente si `ref` (detección) y `L` (nivel de referencia) incluyen o excluyen el frame de señal, eliminando la ambigüedad documental que la v1 dejó y la v2 no cerró (‘≤t’ admite ambas lecturas). Hoy el código opera: `ref` excluye (pre-append, `sports.go:262` + `:319-331`), `L` incluye (post-append, `:282` + `:335-346` + `:514`).
- Archivos: prereg v3 (futuro); este shot ya aplicó la errata de clasificación al informe W1-j/k y a la continuidad.
- Criterio de aceptación: el texto del preregistro enuncia la regla para ref y para L de forma no ambigua; el informe y la continuidad quedan clasificados como ambigüedad documental (hecho).
- Clasificación: cambio económico Owner (definición de la referencia del estimando); la redacción/errata es nuestra y ya está aplicada. Ninguna dirección de la regla es look-ahead bajo v2 §5; el efecto numérico depende del lado del shock, no identificable en el episodio sellado.

### P0-2 — Exportación de la ventana de referencia con identidad (técnica)

- Qué: extender el anillo de réplica para retener por observación `{seq, wall, bid, ask, mid, spread_bps}` en lugar de `{spreadBps, mid}` (`cmd/researchpilot/economics.go`, `spreadObsR` líneas 943–947; append en 1251–1257), y exportar por fila de rechazo (y de ACCEPT cuando existan) la ventana pre-append acotada a 10 observaciones + la observación del frame de señal marcada como tal, con `ref_bps` y `L` exportados como valores y re-derivable desde la ventana. Los escenarios A y S comparten la misma ventana (universos contables independientes sobre los mismos frames).
- Archivos afectados: sólo `cmd/researchpilot/economics.go` (harness). Código congelado y artefactos sellados intactos.
- Criterio de aceptación: para cada fila, la última observación de la ventana ampliada es el frame de señal (seq == `signal_seq`); las medianas recomputadas desde la ventana exportada reproducen `ref_bps` y `reference_level` exportados (mediana inferior, empates deterministas); `replication_match` se mantiene true en todas las filas; original pinneado `8fc7ec9d…` sin drift.
- Clasificación: instrumentación técnica (los datos ya están en memoria del harness; es wiring de salida).

### P0-3 — Fila de round trip ACCEPT con descomposición completa (técnica; inerte en el episodio sellado)

- Qué: ampliar `signalRow` (líneas 122–135) con: L, spread/ref/widening del frame de señal, bid/ask/mid del frame de señal, entrada `{seq, wall, best_ask, size, notional, vwap, fee_al_bound, worst_price, levels_touched, takes_por_nivel}` (reutilizando `economics.WalkSideDetailed`/`LevelTake` que YA existen, `scheduled.go:12-86`), salida `{seq, wall, best_bid, side=SELL, size, notional, vwap, fee_al_bound, remaining, takes_por_nivel}`, fees por pata, gross mark-to-L, B\*, H (wall = señal+300s), frames y segundos señal→entrada y salida→H, índice/fin de segmento (causa exacta de `invalid_gap`), reason codes estructurados (hoy sólo `detail` en texto). La réplica de L ya existe en la ruta de revisión (`buildRejectRow`, líneas 1338–1468) — reutilizarla, no duplicarla.
- Archivos afectados: `cmd/researchpilot/economics.go`. Nota honesta: con 0 ACCEPTs en el episodio sellado esta pieza no produce filas hoy; su valor es que cualquier re-score offline o dato futuro nazca con la descomposición completa (la lección W1-j: sin ella hubo segundo pase extractivo).
- Criterio de aceptación: cada fila tiene todos los campos o null con razón explícita (sin rellenos); la suma de filas cuadra con los agregados del escenario (`proceeds/notional/fees/net`); la taxonomía de 7 estados de v2 §5 queda intacta; `REAL_FEE_READY=false`.
- Clasificación: instrumentación técnica.

### P1-4 — Prueba mínima de la fórmula de fee por nivel (técnica, test-only, próximo shot)

- Qué: prueba offline que fije el contrato de `regimes.FeeSchedule.LevelCost` y `economics.BuildQuoteScheduled` con fixture de provenancia explícita: (i) `LevelCost(take, price) == truncate6(rate·price^e·(1−price)^e·take)` para casos de fixture `price_square_v1`/`TRUNCATE_6DP`/`SYNTHETIC_FIXTURE` con rate sintético; (ii) la suma de costes por nivel sobre los `Takes` de `WalkSideDetailed` == `FeeTotal`; (iii) con fee INTERVAL [0,500] y schedule presente, `FeeResolved=false` y ningún POINT inventado (`scheduled.go:128-131` — el camino del piloto nunca colapsa el intervalo); (iv) con fee POINT de estrés y provenance `REAL_UNVERIFIED`, el total se etiqueta como no-certificación. Sin tarifa real ni POINT sin correspondencia mercado/asof; `REAL_FEE_READY=false` en todo artefacto.
- Archivos afectados: test-only bajo `internal/economics/` (o `internal/regimes/`), según descubrimiento del shot implementador; cero código de producto.
- Criterio de aceptación: suite test-only PASS sin tocar producto; los cuatro oráculos anteriores verdes; ningún artefacto cambia `real_fee_ready`.
- Clasificación: instrumentación técnica (certifica la FÓRMULA que el engine aplica, no una tasa del venue). Evidencia capturada que NO certifica schedule real: tick `0.01`, `maker/taker_base_fee_bps = 1000` legacy (resuelto INTERVAL [0,1000] a nivel condición; UNRESOLVED a nivel asset; `fd {e:1,r:0.05,to:true}` preservado verbatim sin interpretar; `fee_observed 0` = sin trades) — W1-e sobre capture-v6.

### P1-5 — Procedencia de fees exportada en los artefactos (técnica)

- Qué: añadir en `episodeAnalysis`/`episodeAnalysisRevision` campos explícitos `fee_formula_applied` (= «linear_bound: notional × bps/10000 per leg via BuildQuote») y `fee_schedule_applied` (= null con razón «never applied in this pilot»), junto a la evidencia capturada citada (tick 0.01, mbf/tbf 1000 legacy, fd verbatim, INTERVAL/UNRESOLVED). Hoy esa distinción vive sólo en texto de `assumptions`/erratas.
- Archivos afectados: `cmd/researchpilot/economics.go` (structs y literales).
- Criterio de aceptación: ningún lector del JSON puede confundir el bound lineal con una tarifa aplicada del venue; los campos viajan con valor o null explícito, nunca ausentes.
- Clasificación: instrumentación técnica.

### P2-6 — Timestamps efectivos y gaps por fila (técnica)

- Qué: exportar por fila H, latencias (señal→entrada, salida→H) e identificación del segmento; la cobertura a nivel de corrida ya existe (`buildRevisionCoverage`, líneas 1524+, `revisionCoverage`) — este delta la baja a fila para que `invalid_gap` identifique el fin de segmento que lo causa.
- Archivos afectados: `cmd/researchpilot/economics.go` (fila y estado `invalid_gap`).
- Criterio de aceptación: toda fila `invalid_gap` declara el fin de segmento real que la causa (no el deadline planeado); todos los timestamps son de recepción real.
- Clasificación: instrumentación técnica.

## Qué NO es un delta (registrado para cerrar la puerta)

- No adoptar `bestAsk < L` como detector nuevo ni margen numérico alguno (es aritmética ya necesaria del gate congelado; adoptarlo cambia la estrategia — Owner/Metis con enmienda de prereg). No umbral 12%. No tuning de parámetros. No POINT de fee sin correspondencia mercado/asof. No nueva captura para estas piezas. No framework ni replay duplicado: la ruta de revisión existente con original pinneado (`8fc7ec9d…`) es el vehículo.

## Prueba offline antes de pedir captura

- SÍ existe: P0-2 + P1-5 (y la ventana que habilita clasificar bid-led/ask-led/mixto por señal, hoy NO identificable desde el artefacto sellado) se satisfacen re-exportando el episodio YA capturado y sellado por la ruta de revisión — datos existentes, cero captura. Ninguna ventana nueva está justificada hasta adjudicar esa re-exportación y la regla de L.

## Próximo bloqueo REAL

- (1) Adjudicación Owner/Metis en dos piezas: fijar la regla de L (incluir/excluir el frame de señal, para ref y L) en el próximo preregistro, y autorizar el re-procesamiento offline del episodio sellado por la ruta de revisión ampliada (artefacto nuevo nominado con run-id; originales pinneados intactos). Este shot no ejecuta nada por mandato.
- (2) Perfil del hook por-shot: las formas de toolchain (go test/build, extractor) requieren registro previo del lanzador (patrón W1-j bullet 29→30).
- (3) Change_log: [[2026-10-27-polymarket-engine-entity-updated]] no fue actualizable en este shot — su lectura fue denegada por el hook («Outside W1-k offline causal-diagnosis scope», 1 intento, sin variantes). El delta queda registrado en la continuidad §18 bullet (34) y en este plan; anexar a la bitácora consolidada queda como tarea de superficie con permiso.

## Próximo shot acotado (propuesta W1-m, requiere adjudicación)

- Implementar P0-2 + P0-3 (wiring) + P1-4 (test-only) + P1-5 en `cmd/researchpilot/economics.go` (+ test propio), y correr UNA vez la ruta de revisión ampliada sobre el episodio sellado (`analyze` a ruta de revisión, original `8fc7ec9d…` pinneado y re-verificado, salida nueva `analysis-revision-*-w1m` con run-id propio). Entregables: ventana de referencia con identidad por señal (clasificación bid-led/ask-led/mixto por observación), sensibilidad de L incluir/excluir como DIAGNÓSTICO (sin adopción), provenance de fees exportada, `replication_match` exigido, `REAL_FEE_READY=false`. Sin captura nueva, sin cambios de estrategia ni parámetros, sin producto.

## Fuentes

- Código citado con ruta relativa al repo `polymarket-engine` (leído 2026-10-29 en este shot): `cmd/researchpilot/economics.go`, `cmd/researchpilot/supervisor.go`, `internal/strategy/pocs/sports/sports.go` (congelado), `internal/economics/economics.go`, `internal/economics/scheduled.go`, `internal/regimes/schedule.go`, `internal/regimes/feeresolver.go`.
- [[Research — W1-j Causal Gate Diagnosis 2026-10-30]] (informe corregido con errata W1-l), [[Preregistration — PE-005-R1 Economic Candidate v2 W1-h 2026-10-29]] §5 (atadura temporal ‘≤t’) y §1 (siete correcciones), [[Preregistration — PE-005-R1 Economic Candidate W1-g 2026-10-29]] (v1, historia; citas oficiales de fees as-of 2026-10-29), [[Polymarket Engine — Continuidad Five-POC 2026-09-20]] §18 bullets (24)–(33).
- [[Research — Public Market Capture W1-d 2026-10-28]] y [[Research — Prospective Metadata Quality W1-e 2026-10-28]] (evidencia capturada tick/fee), manifiestos `validated-baseline/w1-d-public-capture-20261028/selection-manifest-v6.json` y `capture-manifest-v6.json`.
