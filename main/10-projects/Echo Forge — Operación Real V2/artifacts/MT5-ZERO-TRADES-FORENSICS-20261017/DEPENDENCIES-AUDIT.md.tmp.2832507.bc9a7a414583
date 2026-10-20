# DEPENDENCIES-AUDIT — EX5 de flow_example_2 w9 (2026-10-17)

## Alcance

Auditoría real de dependencias runtime de los 30 EX5 del FlowRun `8248f7fa-e3bd-45e4-b0de-66dcfcd564db`, sobre los artefactos durables (MinIO `durable/mt5-export/v1/8248f7fa…/`) y el terminal físico donde ejecutó el Strategy Tester (worker-kronos, `C:\MT5\slots\slot-1`, verificado por SSH read-only).

## Superficie estática (30/30 MQ5 inspeccionados)

- **Includes:** solo `<Trade/*.mqh>`, `<Expert/Expert.mqh>`, `<Object.mqh>`, `<MovingAverages.mqh>`, `<Generic\HashMap.mqh>` — biblioteca estándar, se compilan dentro del EX5; no son dependencias runtime.
- **DLLs / `#import` / `#resource`:** **cero en los 30** (grep `^#import|\.dll|#resource` = 0). No hay dependencias nativas.
- **Indicadores custom vía `iCustom`:** `SqATR` (p.ej. `iCustom(NULL,0,"SqATR",200)`), `SqHeikenAshi`, `SqSessionOHLC` (creado dinámicamente por sesión), `SqSRPercentRank`. Los handles se crean en `OnInit` (líneas ~824/827 del MQ5).
- **Archivos de `MQL5\Files`:** el EA usa un panel de información; el warning benigno `cannot open another one!` aparece sólo en C1 (bloqueo de archivo del panel, no bloquea trading — C1 operó 220 deals).
- **EX5 ejecutado = EX5 durable:** el `.tester.ini` apunta a `EchoForge\flow-example-2-20261017T023000Z-e2e-w9\backtest\5-1\final-<ref>.ex5`, materializado por el worker desde el artifact `durable/mt5-export/v1/8248f7fa…/<ref>/sha256:<codehash>/12_mt5_ex5/final-<ref>.ex5`; el `run_id` sellado dentro de cada TradeSet SQX coincide con ese mismo `sha256:<codehash>` (verificado en los 20 casos leídos). MetaEditor 0 errores (`12_mt5_ex5/final-<ref>.compile.log`, 17122 bytes uniformes).

## Superficie física (terminal del tester, worker-kronos)

- `C:\MT5\slots\slot-1\MQL5\Indicators\` contiene los indicadores SQX compilados (listado 2026-10-07): **SqATR.ex5 (9658 B), SqHeikenAshi.ex5 (9608 B), SqSessionOHLC.ex5 (16898 B), SqSRPercentRank.ex5 (11654 B)** presentes, junto al catálogo Sq* completo.
- El EX5 corrió serial en el agente local `Tester\Agent-127.0.0.1-3000` del mismo slot (testero.log: `log file C:\MT5\slots\slot-1\Tester\Agent-127.0.0.1-3000\logs\20261017.log written`).
- Especificación efectiva del símbolo impres **por el propio EA dentro del tester** (agent.log): `Contract size: 10`, `Point value: 10.00 USD`, precios H1 con tick 0.1. El catálogo de historial del símbolo está en `Bases\Custom\history\NDX_SQX\` (y réplica de tester en `Tester\bases\Darwinex-Demo\history\NDX_SQX\`); la cuenta del tester es `Darwinex-Demo (Build 6230)`, depósito 100 000 USD, leverage 1:100, **100% real ticks**.
- Intento de extracción directa del registro `symbols.custom.dat` (4096 B) no contiene la entrada NDX_SQX (sólo el header `SymbolsCustom`); el rate de margen puntual queda acotado empíricamente en [4.2%, 5.6%] por los bounds del informe (ver `ZERO-TRADES-REPORT.md` §cadena causal). No se modificó nada del terminal.

## Veredicto

**MISSING_RUNTIME_DEPENDENCY = NO (30/30).** Cada EX5 ejecutó con todas sus dependencias disponibles en el contexto real del tester; la evidencia funcional (miles de señales coherentes por estrategia, SL/MM calculados según diseño) demuestra que los handles de indicadores resolvieron y `CopyBuffer` entregó datos durante todo el período. La ausencia de trades no proviene de dependencias ni de recursos runtime.
