---
type: known_error
scope: project
created: 2026-07-29
updated: 2026-07-31
area: "[[Echo Forge]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[EchoForgeTradeListExporter]]"
entities:
  - "[[EchoForgeTradeListExporter]]"
  - "[[BuildMinIOPath]]"
  - "[[ExportTradeListActivity]]"
related:
  - "[[sqx-main-00_configs-v1-NDX-H1-L-1785373312]]"
  - "[[echo-forge-g3-false-closure-runtime-path]]"
  - "[[2026-07-31-minio-storage-path-must-be-deterministic-by-logical-identity]]"
aliases:
  - trade-list-exporter-empty-robust
  - source-order-count-zero
  - resolveMainResultKey-orphan
  - buildminiopath-requestid-mismatch
  - sqx-build142-reflection-contract
  - SampleTypes.FullSample 127
  - ef-g27
  - ef-g28
confidence: verified
source_session: cursor-2026-07-31-echo-forge-reflection-contract-rca
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - tech/sqx-exporter
  - tech/minio
  - tech/atomicity
  - scope/public
  - change/updated
---

# Trade List Exporter: `source_order_count=0` → sin `_SUCCESS`

## Síntoma

- Activity `trade_list_exporter` falla: `no se encontró _SUCCESS en .../EchoForgeTradeListExporter/tradelist`.
- `export_run.json` raíz: `status=partial`, `written_count=0`, `error_count=1`, `artifact_dirs=[]`.
- Scope dirs `<strategyId>___FULL/` se crean vacíos (mkdir previo al extract).
- Síntoma secundario: en MinIO se crean **dos carpetas duplicadas** para el mismo proyecto, una con `cfgID` y otra con el `RunID` de Temporal.

## Causa raíz (corregida 2026-07-31, EF-G27)

> **Importante:** el diagnóstico previo (2026-07-29/31) apuntaba al plugin Java
> como raíz (`resolveMainResultKey` ciego, etc.). Ese diagnóstico era
> **incorrecto** — el plugin Java reportó fielmente lo que recibió. La causa
> raíz está aguas arriba, en la construcción del path de MinIO.

La raíz real es `BuildMinIOPath` (SDK Go): hasta el fix, inyectaba un segmento
`requestID` que se resolvía de **tres formas distintas** según el productor:

| Productor | `requestID` |
|---|---|
| watcher `SaveConfigStep` / worker `dbRegister` | `cfgID` = `NDX_example_flow_49_v1_wtest` |
| `robust_activity`, `trade_list_exporter_activity` | `req.RequestID` → **RunID de Temporal** |
| `minio_storage.UploadObject` | `meta.RunID` |

Cada etapa escribía bajo un segmento distinto → la siguiente etapa no encontraba
el artefacto, o bajaba uno residual equivocado (p.ej. un XAUUSD/D1 huérfano de
una corrida previa) → `source_order_count=0` → ausencia de `_SUCCESS`.

### Los "tres defectos" previos eran síntomas, no raíz

1. `resolveMainResultKey` aceptando `getMainResultKey()` "ciego" — en realidad
   operaba sobre un `.sqx` equivocado bajado por path mismatch (no sobre el
   artefacto correcto). El parche Java de validación sigue siendo defensivo
   válido, pero no era la causa.
2. Búsqueda de `_SUCCESS` en raíz vs scope dir — defecto real independiente,
   corregido, pero no causaba el `source_order_count=0`.
3. Naming `trades.v1.ndjson.gz` vs `trades.ndjson.gz` — defecto real
   independiente, corregido.

## Fix (aplicado 2026-07-31)

**Rollback a la convención plana** — eliminar por completo el segmento
`requestID` del path de MinIO. La firma de `BuildMinIOPath` pierde `ctx` y
`requestID`:

```go
// Antes
BuildMinIOPath(ctx, wave, inst, dir, tf, strat, ver, requestID, folder, file)
// Ahora
BuildMinIOPath(wave, inst, dir, tf, strat, ver, folder, file)
```

Path resultante, **determinístico por identidad lógica**:

```
wave_<wave>/<instrument>/<dir_tf>/<strategy>/<version>/[folder]/[filename]
```

10 call sites actualizados; `go build`/`go vet`/`go test` verdes. Documentado
en `specs/FEAT-SQX-STRATEGY-EVALUATION/G6_HANDOFF.md` §10.3 (EF-G27).

## CAUSA RAÍZ DEFINITIVA (2026-07-31, flow 57 — aislada con `javap`)

EF-G27 (path) es un fix correcto pero **nunca explicó este síntoma**. La causa
real son **tres roturas del contrato de reflexión** del plugin contra el SDK de
SQX Build 142. El exporter de trade lists **nunca funcionó**; no es regresión.

Contrato real (`javap -constants` sobre `Zeus:/home/kor/sqx/internal/libs/SQTradingLib.jar`):

| Símbolo | Valor/firma real | Lo que el plugin asumía |
|---|---|---|
| `SampleTypes.FullSample` | `127` | `0` |
| `SampleTypes.InSample` | `10` | `1` |
| `SampleTypes.OutOfSample` | `20` | `2` |
| `Directions` | **clase** con `byte Both=0` | **enum** |
| `OrdersList.get` | `get(int)` | `get(Integer)` |
| `OrdersList.filterWithClone` | `(String, byte, byte)` | `(String, Enum, byte)` |

Semántica del filtro (bytecode del privado `filter(String,byte,byte,ZZZ)`):
`direction==0` desactiva el filtro de dirección y **`sampleType==127` desactiva
el filtro de sample**. Pasar `0` como sample activa la comparación y no matchea
ninguna orden.

Cada defecto por separado fuerza `source_order_count=0`:

1. **sample byte 0** → el filtro compara `Order.SampleType==0`; ninguna orden vale 0.
2. **`isEnum()` sobre `Directions`** → `filterWithClone` nunca se enlaza (silencioso).
3. **`getMethod("get", Integer.class)`** → `NoSuchMethodException` por elemento;
   toda `OrdersList` se materializa vacía aunque `size()` diga 65.

**Meta-defecto**: toda la reflexión está en `catch (Throwable ignore)`. Tres
roturas duras se degradan a un único síntoma ambiguo, y la cadena de fallback
(`resultKey → strategyId → "" → rawList`) las enmascara. Por eso el bug "mutaba"
entre releases.

`result_key=Main: XAUUSD_darwinex/D1` **no es un bug del plugin**: es lo que el
`.sqx` realmente contiene (`Results/Main: XAUUSD_darwinex_LOM_D1/`), porque los
templates `.cfx` tienen el símbolo hardcodeado — bug separado (EF-G29).

## Bugs derivados tipificados (2026-07-31)

| GAP | Qué es |
|---|---|
| **EF-G28** | Este contrato de reflexión roto. Causa raíz de `source_order_count=0`. |
| **EF-G29** | Los 4 `.cfx` hardcodean `XAUUSD_darwinex`; `config.json` declara NDX/H1. Todo el pipeline backtestea el instrumento equivocado. |
| **EF-G30** | Go escribe 4 de 10 claves en `exporter.properties`; el plugin rellena con defaults `req-001`/`run-001`/**`EURUSD`**. |
| **EF-G31** | El JAR no está en `deploy/manifest.json`, no tiene versión ni sha verificables. Fuentes del plugin sin commitear. |

Diseño de solución y orden de remediación: `G6_HANDOFF.md` §10.4–§10.8.

## Detección

- Log Java con `source_order_count=0` **y** `.sqx` cuyo `Fingerprint trades="N"`
  es > 0 → contrato de reflexión roto, no falta de datos. El `Fingerprint` del
  `settings.xml` dentro del `.sqx` es el oráculo.
- `result_key=Main: <simbolo>/<tf>` que no calza con el nombre del archivo →
  revisar el `.cfx`, no el plugin.
- `export_run.json` con `request_id=req-001` / `run_id=run-001` → properties
  incompletas (EF-G30).

## Regla operativa aprendida

Nunca cerrar un GAP de este pipeline con `go build` + `go test` verdes. Un GAP
se cierra **falsando el síntoma original con evidencia de runtime**. EF-G26 y
EF-G27 se marcaron `resolved` mientras el síntoma seguía vivo; eso produjo tres
releases (0.2.8 → 0.2.17) atacando capas equivocadas.

## Evidencia

- Log: `Zeus:.../EchoForgeTradeListExporter/tradelist/trade_list_20260731_214542.log`.
- Artefacto: `Zeus:.../databanks/input/NDX_L_H1_example_flow_57_v1_Strategy_4.1.18.h0.sqx`
  (`Results/Main: XAUUSD_darwinex_LOM_D1/`, `Fingerprint trades="65"`).
- Contrato: `javap` / `javap -constants -c -p` sobre `SQTradingLib.jar` en Zeus.
- Auditoría previa 2026-07-31: [[74b70470-92f5-42bc-9810-afaf19eb5db1]]
  (diagnóstico incorrecto en su núcleo).
- Handoff: `specs/FEAT-SQX-STRATEGY-EVALUATION/G6_HANDOFF.md` §10.3–§10.8.

