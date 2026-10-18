# REMEDIATION-PLAN — MT5 Zero Trades Forensics (2026-10-17)

Sólo plan: nada de esto se implementa en esta sesión. Ordenado por causalidad.

## R1 — Clamp de margen en el Money Management del template MQ5 (causa habilitante)

- **Qué:** en el generador de export SQX→MQL5 (template de Money Management "Fixed Amount"), después de computar `LotSize = RiskedMoney / oneLotSLDrawdown`, añadir clamp por margen: `lot_max_affordable = freeMargin × safety / margin_per_lot` usando `OrderCalcMargin` del propio template, operar `min(LotSize, lot_max_affordable)` y degradar a no-operar (con log explícito) sólo si el resultado cae bajo `Smallest_Lot`.
- **Dónde:** template/ emitter del export MT5 en `xKoRx/symphony` (generación del bloque de MM del MQ5; el bloque actual está en las líneas ~7206–7470 del MQ5 exportado y el chequeo abortivo en ~1964–1970).
- **Verificación:** replay físico de 2–3 de las 16 con el EX5 regenerado, mismas fechas/símbolo/inputs → deals > 0 y primera operación en la fecha de la primera señal SQX (2026-01-02 06:00 para Z23); verificación negativa: un lote teóricamente inalcanzable se degrada con log claro en vez de silencio.
- **Qué otros flujos afecta:** todo FlowRun con etapas MQ5/EX5/MT5/fidelity/ranking final (Final Reretester, `mt5_fidelity_shadow`, ranking `score_descending`, promoción). Cambiar el generador cambia el code-hash → nuevas StrategyVersions; no reinterpreta las existentes.
- **Alternativa menor (config, decisión owner):** subir el depósito del tester o revisar el sizing del robust run (riesgo $200 con SL 21 pips exige ~9.5 lotes); no corrige el defecto de plantilla.

## R2 — MagicNumber int32 (defecto latente de identidad)

- **Qué:** el export declara `input int MagicNumber = 261000910xx;` — MQ5 `int` es 32-bit y compila `valor mod 2³²` (26100091079 → 330287303; verificado en 3 HTM: Z23, Z15, C13). Inerte en backtest; rompería la atribución de posiciones si el EA corriera en vivo contra la mágica durable de `sqx.strategy_magic`.
- **Corrección mínima:** exportar el input como `input long MagicNumber` (o mapear a un rango int32 durable en el apply) y añadir aserción de round-trip en el pipeline (leer el valor del reporte HTM/ini y contrastar con la mágica durable).
- **Dónde/verificación:** mismo generador que R1; verificación = HTM regenerado con `MagicNumber == durable` exacto.
- **Qué otros flujos afecta:** handoff Forge→Echo (identidad de posiciones), auditorías por mágica, y cualquier comparación contra `sqx.strategy_magic`.

## R3 — Fidelidad comparable de la cohorte (consecuencia, sin código propio)

- **Qué:** los 14 con trades ejecutan sólo 6–27% de sus señales y con SLs 100× menores que el diseño — sus métricas MT5 no miden la estrategia SQX. Tras R1, recomputar `mt5_fidelity_shadow` y el ranking final antes de cualquier lectura de calidad.
- **Verificación:** re-emisión del score + ranking final sobre EX5 regenerados; expected: fidelidades no-nulas en las 16 y PnL MT5 con semántica comparable.

## No-correcciones explícitas

- Datos, símbolo, terminal, compilación, dependencias y lógica de señales: **sin defecto** — no tocar.
- La certificación técnica E2E PASS (FlowRun COMPLETED, 21 etapas selladas) queda intacta: el pipeline ejecutó fielmente; el defecto vive en el producto exportado, no en el funnel.
- No modificar los CFX del owner, la flota, ni re-ejecutar el E2E en esta sesión.
