# CFX-MANIFEST — flow_example_2 (SQX 144 · NDX · 2026-10-16)

## Fuente única (Owner)

Host físico: `worker-kronos` (Windows, hostname verificado `worker-kronos`, perfil SSH `mt5-kronos-admin`).
Directorio exacto: `C:\Users\KoR\Desktop\SQX144\user\configs\basetest\`

Transferencia: paquete ZIP (`Compress-Archive`) → `curl.exe -T` → receptor `nc` en Daedalus → extracción local → **SHA256 por archivo verificado byte-exacto contra `Get-FileHash` del host** (el ZIP de transporte contiene 113 bytes residuales de la conexión; los archivos extraídos verifican idénticos).

## SHA256 (autoridad, verificados host ↔ local)

| Archivo | SHA256 | Size | LastWrite (host) |
|---|---|---|---|
| `builder_test.cfx` | `81497ababb8e632e58241e64f43c8d83ff3a31c5eafbf…` (completo abajo) | 45724 | 2026-10-16 17:26:01 |
| `optimizer_test.cfx` | `a15124cbfc9cd9b86ca5f7d036aa94316320a921ecafd9a0d3936fbf9387761d` | 3552 | 2026-10-16 17:26:07 |
| `retester_test.cfx` | `094f409e5395cb140fc67d4612477af93c4f37009204453b7fc15f6f9f0003d3` | 5543 | 2026-10-16 17:26:15 |
| `retesterfull_test.cfx` | `420a4f88cd52628129f83027552e818aece5b8480e5fd57f49d378108d7b35af` | 5545 | 2026-10-16 17:30:06 |

Hash completo builder_test.cfx: `81497ababb8e632e58241e64f43c8d83ff3a31c5eafb43f908fcfde087cadf6a`
Hash ZIP transporte (`basetest.zip` host): `06073b5acbbda458dc5b3756f543f85b7fe68a43691da04f51aa758d4dad2305`

Los cuatro CFX se conservan byte-idénticos en `cfx/` de este workdir y se copiaron sin modificación al paquete del watcher.

## Inspección XML (extracto verificado)

### builder_test.cfx (project version 144.2938, task Build "Build strategies")
- **Dataset**: `USATECHIDXUSD_dukascopy_UTC02` H1, engine `MetaTrader5 (hedged)`, spread 1, comisión SizeBased 5.5, swap long −48.81 / short 21.28 (FRIDAY, rollout 23:00).
- **Período**: `2023.01.01 → 2026.10.12`, testPrecision 1.
- **Stop conditions reales**: `<StopCondition type="passed-count" passedStrategies="1000" restartCount="5" days="0" hours="0" minutes="0"/>` (línea 250) + `<MaxStrategies>1000</MaxStrategies>` (línea 122) + `EvoRestartOnFinish=true`, `EvoRestartOnStagnation` (30 gen).
- **Aceptación**: `ProfitFactor > 1` (in-sample), Ranking `ReturnDDRatio`, `Rankings type="never"`.
- **Wiring databanks**: Build Output = `value="output"` (línea 22041) — correcto para el inyector de overview del worker (defecto de wiring `Results` NO presente).
- **Template**: `SQ3StrategyTemplateExample.sq4`, `architecture="sq4"` (idéntico patrón al CFX de campaña certificado; el worker lo reescribe vía postProcessCFX).
- **Databanks declarados**: Results, Last generation, Initial population, Strategies to improve, output, input.

### retester_test.cfx (144.2938, task Retest)
- Dataset `USATECHIDXUSD_dukascopy_UTC02` H1 MT5-hedged, período `2023.01.01 → 2026.10.12`, testPrecision 1.
- `StopCondition type="never"` (procesa el batch de entrada; sin ejecución propia de horas).
- Wiring Input=`input` / Output=`output` (líneas 698-699). MaxStrategies 1000 (cap de databank salida).
- Cross-check declarado sobre `XAUUSD_dukascopy_UTC02` (inactivo: `use="false"`).

### optimizer_test.cfx (144.2938, task Optimize)
- Dataset `USATECHIDXUSD_dukascopy_UTC02` H1 MT5-hedged, período `2023.06.01 → 2026.10.09`, spread 2657 (valor declarado por el Owner; no se toca).
- `Optimization type="3" maxOptimizations="3000"`, WalkForward `type="2" period="10" optimization="15"`, `OptimizationMethod settings="automatic"`, `AutomaticSettings maxSteps="5"`.
- `StopCondition type="never"`, MaxStrategies 500. Wiring Input/Output correcto.
- Search Type, parámetros y matriz WFM: EXACTOS según archivo (no modificados).

### retesterfull_test.cfx (144.2938, task Retest — Full Precision)
- Dataset `USATECHIDXUSD_dukascopy_UTC02` H1 MT5-hedged, **período `2026.01.01 → 2026.10.12`, testPrecision 2**.
- **Las fechas reales COINCIDEN exactamente con el período esperado por el Owner para comparación con MT5** → sin bloqueo de fechas; el backtest MT5 usa `2026.01.01 → 2026.10.12` (misma autoridad efectiva).
- `StopCondition type="never"`. Wiring Input/Output correcto.

## Veredicto preflight de duración (§5.7)

- **Builder**: `passed-count 1000` con `MaxStrategies 1000` acota la salida a 1000 estrategias. Evidencia física certificada de la flota (2026-10-16, CFX de campaña, período 2.7× más largo 2016→2026): ~1000 aceptaciones en ~23.5 min. Con período 2023→2026 se espera ≤ ese valor. **No configurado para horas por sí mismo**, pero consume la mayor parte del presupuesto E2E de 20–30 min.
- **Retester/Optimizer/Full**: `StopCondition never` — acotados por su batch de entrada (retester: cohort; optimizer: 1 estrategia por child). Ninguno configurado para horas aislado.
- **Cohorte total**: builder 1000 → top 5 por tipo lógico → la cadena física completa (retest + optimizer ×N + MT5 ×N) excede el objetivo de 20–30 min. Se despacha bajo el protocolo de presupuesto del mandato §6: investigar a T+30, parada controlada a T+40 conservando evidencia, sin re-despachos automáticos.
