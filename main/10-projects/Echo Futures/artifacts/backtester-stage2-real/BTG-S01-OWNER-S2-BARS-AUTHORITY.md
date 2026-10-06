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

# BTG-S01-OWNER-S2-BARS-AUTHORITY

## Propósito

Registrar la instrucción Owner recibida el 2026-10-06 que permite continuar S01 con S2 actual + GerardMM actual y corpus de barras reales 1m de NinjaTrader, con simulación pesimista declarada. Esta autoridad sustituye el bloqueo de alias; no prueba bytes de corpus ni una configuración instalada ausente.

## Contenido

### Decisiones Owner

- Strategy del primer test: S2 actual, source SpecID `S2_H4_TREND_BB_PULLBACK_V1`, H4 trend + 5m señal/entry, MARKET @ BAR_CLOSE. No modificar señal ni parámetros para mejorar métricas.
- GerardMM actual compartido permanece como autoridad económica. No optimización, campaign engine, bankroll ni sweet spot en este primer test.
- Corpus principal solicitado: NQ Last 1m, 2023-10-01 → 2026-10-06, aproximadamente tres años. Dataset real descargado/visible en NinjaTrader según Owner; cobertura física exacta, gaps y digests requieren inspección.
- Ante SL y TP tocados dentro de la misma vela, asumir SL primero. Es regla modelada de ejecución; no convierte OHLC en orden temporal observado ni prueba pesimismo global de adds/targets dinámicos.
- Rollover explícito y determinista por contratos físicos; cambio de precio entre expiries no produce PnL de una exposición en otro contrato. No interpolar gaps silenciosamente.

### Disponibilidad informada por Owner, pendiente de comprobación física

NinjaTrader 8 con conexión Earn2Trade/NinjaTrader, Global merge policy `MergeNonBackAdjusted`. Secuencia visible: NQ 12-23; 03/06/09/12-24; 03/06/09/12-25; 03/06/09-26; NQ 12-26 como instrumento current usado para la solicitud. NQ 12-23 muestra Last/Minute Sep–Dec 2023. No asumir que cada expiry contiene todo el rango ni que una serie merged posee una única identidad física.

Tick Last visible para NQ 03-26, 2026-01-02 → 2026-03-20; download de NQ 12-23 retornó sin datos. La aspiración de validar el último año con ticks no equivale a un año adquirido: inventariar la cobertura real y conservar los límites. No inventar BBO desde Last.

### Ocho pruebas requeridas para el primer test

1. Consumo del histórico NQ auténtico.
2. Reconstrucción determinista y causal de 5m/H4 desde 1m.
3. Expiries/rollover sin PnL ficticio.
4. S2 actual sin cambios de estrategia.
5. GerardMM actual sin cambios de política para métricas.
6. Trades y métricas reproducibles en proceso fresco.
7. Gaps reales reportados sin datos inventados/interpolación silenciosa.
8. Baseline funcional auditable antes de buscar sweet spot; cuentas quemadas o PnL negativo son resultados válidos.

### Estado comprobado y trabajo autorizado

Owner no conoce la ubicación del archivo y pidió investigar el disco. Worker NORMAL inspeccionó filesystem Windows mediante capacidades RO vigentes: identidad `echo-dev`, raíz `KoR` visible, lectura de Documents/db/minute, Downloads y Public denegada. No se recuperaron originales. La investigación agotó esta superficie; un export GUI a stage legible es la mínima acción externa, sin pedir al Owner descubrir rutas ni ampliar ACL/perfiles como workaround.

Worker TOP verificó en source certificado `cd451972` que `HistoricalRecord` sólo ingresa TRADE/QUOTE y el venue requiere BBO/modelo explícito; OHLC y SL-first aún no están implementados. El delta de velas necesita un seam nativo con provenance de barras, causalidad y simulación declaradas; no basta convertir CSV a pseudo-ticks. Informe/tareas acotadas en [[BTG-S01-S2-1M-FORENSICS]], inventario en [[BTG-S01-NQ-1M-DATASET]].

B01 (alias exacto) queda RESOLVED_BY_OWNER para este test S2. Configuración MM/scaling/account/provider/horizonte sigue a sus autoridades: day1/2 SL USD 2.000 / TP USD 1.500 ya definidos; rows day3+ y FUNDED no heredan valores de fixtures. SL-first no decide por sí solo el orden de adds adversos/favorables ni de targets dinámicos dentro del minuto; el seam debe evidenciar esa ambigüedad sin llamarla observación histórica.

## Fuentes

- Owner, mensajes directos 2026-10-06: paquete HISTORICAL DATA AVAILABLE — NQ y regla pesimista SL-first; posterior instrucción de investigar el disco.
- [[BTG-PLAN]], [[BTG-S01-REAL-GERARD-RESULT]], [[BTG-S01-IDENTITY-CONFIG]], [[BTG-S01-NINJATRADER-ACQUISITION]].
- Source `xKoRx/echo@cd451972`, `v3/sdk/futures/strategies/s2/s2.go:43`; refs Echo master/S04/D6 refrescados sin delta durante esta reanudación.
