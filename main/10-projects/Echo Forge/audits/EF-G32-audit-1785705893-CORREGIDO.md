---
type: doc
schema_version: 1
status: active
tags: [kind/doc, kind/audit, project/echo-forge, run/1785705893, tech/sqx, audit/correction]
created: 2026-08-02
updated: 2026-09-04
---

# Auditoría EF-G32 (CORREGIDA) — Run sqx-main-00_configs-v1-NDX-H1-L-1785705893

## Propósito

Re-auditar la corrida `1785705893` con foco en evidencia física directa y corregir imprecisiones materiales del reporte anterior ([EF-G32-audit-1785705893.md](EF-G32-audit-1785705893.md)).

## Contenido

Resumen ejecutivo de veredictos, hallazgo crítico del robust run (evidencias A–E), bug de instrumento en `reretester`, verificaciones confirmadas, recomendaciones priorizadas y artefactos físicos.

## Resumen ejecutivo — qué es verdad y qué no

| Afirmación del reporte anterior | Veredicto | Evidencia física (Hera 192.168.31.111) |
|---|---|---|
| "12 activities OK" | ✅ CIERTO | logs del worker JSON `activity.ok` + logs sqcli `EchoForgeMT5Exporter`/`EchoForgeRobustRunExporter` |
| "4 .mq5 distintos" | ✅ CIERTO | `mq5/` con 4 archivos, cada uno con StrategyID/CustomComment únicos |
| "El robust no modificó parámetros de trading, solo MagicNumber" | ✅ CIERTO y reforzado | `orders.bin` md5 **idéntico** entre base y robust (`c329ba82df...`) → ningún backtest nuevo |
| "Persistencia en Postgres y MinIO" | ✅ CIERTO | `Object uploaded successfully` en worker log |
| **"XAUUSD_darwinex mal etiquetado en base y robust"** | ❌ **FALSO** para esta corrida | `grep -a XAUUSD base/*.sqx robust/*.sqx` = **0 matches**. Resultados internos: `Results/NDX_L_H1_example_flow_67_v1_Strategy_*/dailyEquity.bin` |
| "ETCD caído" | ✅ CIERTO | `nc -zv 192.168.31.45 2379` = `Connection refused` |
| "OTLP caído" | ✅ CIERTO | `nc -zv 192.168.31.45 4317` = `Connection refused` |
| "HOST_KEY=h0 pero sufijo k0" | ✅ CIERTO | `echo $HOST_KEY=h0`; archivos terminan en `_k0.sqx` |
| "Run disparado por Temporal, no por watcher" | ✅ CIERTO | `/var/lib/symphony/input/processed` sin `20260802_172453_*`; worker log sin `1785705893` |

## Hallazgo crítico real — el "robust run" es cosmético

### Evidencia A — `orders.bin` idéntico

```text
$ md5sum _extract_base/orders.bin _extract_robust/orders.bin
c329ba82df518e573b2d774c1b2fd714  _extract_base/orders.bin
c329ba82df518e573b2d774c1b2fd714  _extract_robust/orders.bin
```

`orders.bin` (las órdenes reales del backtest) es **binariamente idéntico** entre base y robust.
El robust no re-corrói backtest alguno: las órdenes son las del base.

### Evidencia B — diff `strategy_Portfolio.xml`

```text
$ diff _extract_base/strategy_Portfolio.xml _extract_robust/strategy_Portfolio.xml
346c346
<         <value>11111</value>      ← base
---
>         <value>888111</value>     ← robust
```

**Una sola línea** de diferencia en 395. Solo `MagicNumber`.

### Evidencia C — diff `settings.xml`

Solo **4 líneas** de diferencia, todas cosméticas sobre `ResultName`:
`"WF Matrix - NDX_..." → "NDX_..."` (se elimina el prefijo "WF Matrix - ").

### Evidencia D — logs del sqcli

```text
TASK STARTED at 2026.08.02 13:53:55.643
Task: Custom analysis, Type: CustomAnalysis
Databanks before start: Results (0), output (0), input (1)
TASK FINISHED at 2026.08.02 13:53:55.692 in 49 ms.
Databanks after finish: Results (0), output (1), input (1)
```

**49–53 ms** por invocación del plugin. Un backtest WF toma minutos.
El plugin opera exclusivamente sobre metadata del `ResultsGroup` sin re-ejecutar nada.

### Evidencia E — `automator.properties` real en disco (Hera)

```properties
wfm.runs_count=7
wfm.oos_percent=28
strategy.magic_number=888111
strategy.parameter.symmetry.enabled=true
```

El Go sí está escribiendo `runs_count=7, oos_percent=28` (no 10/20 como decía
el default del plugin Java). Es decir, la **intención** de seleccionar la celda
WF (7, 28) está presente, pero el efecto final sobre el `.sqx` es nulo:
`getBestParameters(wfCell)` retorna un string que, aplicado con `setParameters`,
no cambia ningún valor presente en el XML (los nombres del paramMap no coinciden
con los `Variable` del strategy XML).

### Diagnóstico raíz (código Java)

`EchoForgeRobustRunExporter.processDatabank` (líneas 57–148 de
`sqx/exporter-plugin/src/SQ/CustomAnalysis/EchoForgeRobustRunExporter.java`):

1. Obtiene `WalkForwardMatrixResult` del `ResultsGroup`.
2. Llama `getBestParameters(wfCell)` — implementado con **reflection** sobre
   campos cuyos nombres contienen `period`/`parameter`/`param` (líneas 197–258).
3. Llama `setParameters(rg, bestParameters, symmetricVariables)` (línea 80).
4. Parchea `MagicNumber` en el `Variables/Variable` del strategy XML.

`setParameters` (líneas 153–195) itera sobre `variables.getChildren("Variable")`
y `variables.getChildren("variable")`, parcheando `value` solo si `name` existe
**literalmente** en `paramMap`. Si el string `bestParameters` no trae claves
que coincidan con los nombres de los `Variable` del strategy XML, no se
modifica nada — que es exactamente lo observado.

> **Causa raíz probable:** el string que retorna `getBestParameters` usa
> identificadores internos del WF cell que no son los mismos `name` que
> aparecen en `Variables/Variable@name` del XML de estrategia. El parche
> se ejecuta sin error pero es no-op. El único cambio efectivo es el
> MagicNumber porque se hace en un bloque aparte (líneas 99–141) con
> matching hardcodeado del nombre `"MagicNumber"`.

## Hallazgo nuevo — bug de instrumento está en `reretester`, NO en robust/base

El reporte anterior dijo que `XAUUSD_darwinex` estaba presente en base/robust/reretester.
**Falso para esta corrida**:

```text
$ for f in base/*.sqx robust/*.sqx reretester/*.sqx; do
    echo "$(grep -ca XAUUSD "$f") matches in $f"
  done
0 matches in base/NDX_L_H1_example_flow_67_v1_Strategy_3.1.21.k0.sqx
0 matches in robust/NDX_L_H1_example_flow_67_v1_Strategy_3.1.21.k0.sqx   (y 8 más)
2 matches in reretester/NDX_L_H1_example_flow_67_v1_Strategy_3.1.21.k0.sqx   (y 11 más)
```

Inspección del zip del reretester:

```text
$ unzip -l reretester/NDX_L_H1_example_flow_67_v1_Strategy_3.1.21.k0.sqx
...
  42874  2026-08-02 21:54   Results/Main: XAUUSD_darwinex_LOM_D1/dailyEquity.bin
      0  2026-08-02 21:54   Results/CrossCheck_HigherPrecision/dailyEquity.bin
```

**Solo el `reretester` arrastra `XAUUSD_darwinex_LOM_D1`** como path interno
del `dailyEquity.bin`. Los `base/` y `robust/` usan el path correcto
`Results/NDX_L_H1_example_flow_67_v1_Strategy_*/dailyEquity.bin`.

> El agente anterior mezcló evidencia de una corrida anterior con esta.
> El bug existe, pero vive en la actividad `project(05_reretester)`, no
> en `EchoForgeRobustRunExporter`.

## Lo que sí está correcto

- 4 `.mq5` con parámetros y StrategyID únicos — el flujo *downstream* del
  robust al MT5 sí funciona y produce EAs distintos.
- `MagicNumber = 888111` efectivamente embebido en los `.mq5` (verificado
  por `grep MagicNumber mq5/*.mq5`).
- `apply_selected_run` completa con `APPLIED` y persiste `RobustRunSetup`
  con `parameter_patch_applied_successfully`.
- Subida a MinIO en `wave_test/ndx/l_h1/example_flow_67/v1/mt5_eas/`.

## Observaciones adicionales confirmadas

1. **ETCD caído** — `nc -zv 192.168.31.45 2379` → `Connection refused`.
   Aun así el worker funcionó porque carga config al boot y opera con caché.
2. **OTLP caído** — `nc -zv 192.168.31.45 4317` → `Connection refused`.
   Métricas/traces no se exportan.
3. **`HOST_KEY=h0` en Hera; sufijo de archivo `_k0`** — mismatch entre
   hostname actual y sufijo preservado de corridas anteriores.
4. **Run disparado por Temporal** — `/var/lib/symphony/input/processed`
   no tiene `20260802_172453_*`; worker log no contiene `1785705893`.

## Recomendaciones (reordenadas por prioridad real)

### Bloqueante

1. **Robust run no parchea parámetros de trading.** El bug está en
   `EchoForgeRobustRunExporter.java`, **NO en `robust_activity.go`**.
   El Go sí está escribiendo `runs_count=7, oos_percent=28` correctamente
   en `automator.properties`. El problema es que
   `getBestParameters()` + `setParameters()` del plugin Java no logra
   emparejar claves con `Variable@name`. Acciones:
   - Auditar el string que retorna `getBestParameters(wfCell)` para una
     corrida real (agregar `System.out.println("Best parameters: " + bestParameters)`
     en el plugin y re-correr una estrategia).
   - Validar si `setParameters` debe operar sobre `Variables/Variable`
     o sobre `Settings/Variables/Variable` (ver
     `StrategyParametersHelperV2.java` que usa este último path).

2. **Bug de instrumento en `reretester`**, no en robust. Reabrir la
   investigación sobre `project(05_reretester)`: por qué el backtest
   retoma el símbolo histórico `XAUUSD_darwinex_LOM_D1` en lugar de
   `NDX`.

### Corto plazo

3. **Levantar ETCD** (`192.168.31.45:2379`).
4. **Levantar OTLP collector** (`192.168.31.45:4317`).
5. **Auditar el sufijo `k0` vs `HOST_KEY=h0`** — limpiar o estandarizar.

### Mediano plazo

6. **Agregar tests de consistencia** entre `<symbol>` interno del `.sqx`
   y el nombre canónico del archivo en MinIO, ejecutados desde Go
   apenas se descarga el SQX.
7. **Agregar aserción post-apply**: tras `EchoForgeRobustRunExporter`,
   el worker Go debe comparar `orders.bin` del source vs el target.
   Si `md5` coincide, marcar el setup como `WARNING_NO_PARAMETER_CHANGE`
   (no `APPLIED`) para que el pipelines no se crea que robusteció algo.

## Artefactos físicos

- `/tmp/audit-EF-G32-1785705893/` en Hera — dir del agente anterior
  con `base/`, `robust/`, `reretester/`, `mq5/`.
- `/tmp/audit-EF-G32-1785705893/_extract_base/`, `_extract_robust/` —
  descompresiones de los `.sqx` para esta re-auditoría.
- `/tmp/diff_settings.txt`, `/tmp/diff_lastsettings.txt` — diffs completos.
