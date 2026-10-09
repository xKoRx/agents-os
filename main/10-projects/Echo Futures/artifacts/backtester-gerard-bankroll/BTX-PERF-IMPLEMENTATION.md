---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[BTX-PERF-DESIGN]]"
  - "[[BTG-PLAN]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-09"
updated: "2026-10-09"
---

# BTX-PERF-IMPLEMENTATION

## Propósito

Artefacto S02 (TOP LOCAL fresh-context ONE-SHOT, Daedalus): implementación, integración y performance del backtester con referencia corregida, según la adenda Owner de 2026-10-09 y [[BTX-PERF-DESIGN]]. Este documento contiene la sección única `PERF_CONTRACT` sellada ANTES del primer cambio de rendimiento; el bloque congelado conserva sus bytes y hash en la evidencia transportable. Estado devuelto: `READY_FOR_S03_REVIEW` con bloqueo de performance específico (horizonte completo no verificado físicamente: corridas de horas, §7.2) y NQZ5 real completo no alcanzada en presupuesto (§7.3); no hay aceptación de producto.

## 1. Identidad ejecutada

| Dato | Valor |
|---|---|
| Superficie | Daedalus LOCAL, workspace /home/kor/aranea/work/btx-perf-s02-20261009/ (mismo acceso autorizado que E1) |
| Inicio real de sesión | 2026-10-09T08:05-03:00 (promt Owner); límites del harness registrados, no reinventa presupuesto 180min ni adopta 4h |
| Baseline source | `50250a2b0df6106943108bf6bfe57552409f3d13` (checkout E1 intacto, verificado limpio) |
| Código histórico | `d1b1446d401f88cfa42dee2eb959120305f5a372` (referencia, no rebuild) |
| Binario E1 | SHA256 `66657a99384ff6e622da15cd6953ea34621edc35100b536f118d1ff3918a89fb` (verificado por hash) |
| Cápsula E1 | 15/15 archivos SHA256 verificados contra manifest.json; no regenerada; nt-source NQU6 `b21238f4…` verificado contra seal.json |
| CONTROL_CORRECTED_SHA | `d609ca241eed63b1b4413af5bae5b849d334ead0` — rama `codex/btx-perf-s02` publicada en GitHub (xKoRx/echo), un solo commit de repairs/integración sobre 50250a2b |
| Binario control | SHA256 `0db2feae6237ebc20ba8ce16bcc9f50fee0e6809c3677585b403a3d708c490ee`, go1.27.1 linux/amd64, `-trimpath`, vcs.revision=d609ca24 vcs.modified=false |
| OPTIMIZED_SHA | (post-sello; ver §6) |
| Recursos efectivos | 24 cores sin cuota cgroup observable, GOMAXPROCS unset, RAM 92G/63G disponibles; disco raíz 98% usado (3,7G libres) — restricción registrada; carga ajena variable (1min 2,9–4,1), mediciones etiquetadas AISLADO-PROCESO con aislamiento `unshare --user --map-root-user --net` |

## 2. Captura CPU del baseline (E1 R sellado, timeout 120s)

Única variante instrumental permitida: patch exclusivamente de profiling sobre export git de `50250a2b` (env-gated, cero efecto sin variables), binario probe SHA256 `4984c582f61304568bde249d52b5d850cdfa8595fe3d06d62d6140f77c40a82b` — NUNCA atribuido al binario E1; su tiempo no es medición normal. Patch y diff en `probe/INSTRUMENTATION-PATCH.md` + `probe/probe-instrumentation.diff` del workspace. perf(1) INUTILIZABLE sin ampliar permisos (`perf_event_paranoid=4`); no se instalaron servicios ni se tocaron settings.

Resultado (R BASIC NQU6 prefix, COMPLETE rc=0): wall 95,42s (overhead profiling vs 89,64s E1), CPU user 162,13s + sys 14,84s (185%), maxRSS 67,1MiB, 88.362 records, 1.674.851 root inputs. **Dinero idéntico al E1** (98.020,18 / gross −1.935 / costos 44,82 / 6 fills) — la instrumentación no altera semántica.

Atribución del perfil (medida, no supuesta):

| Componente | Evidencia |
|---|---|
| Asignación dominante | `bars.cloneBarRecord` vía `bars.Ring.Recent` = **41,7 GB de 54,8 GB totales (81,5% de alloc_space)**; 4.108 ciclos GC |
| CPU GC | `runtime.gcDrain` 38,69% cum; `scanObject` 15,42% flat |
| CPU aplicación | analytics `Engine.Apply` 29,03% cum (dentro: `cloneBarRecord` 18,3%, `Builder.findSource` 9,0% — escaneo lineal), `ReadModelFeed.ApplyBarsSnapshot` 3,97% |
| Compresión/hash | `compress/flate` ≈3,5s (2%), sha256 ≈1,9s (1,1%) — menores |
| Conclusión | El coste dominante es churn de asignación por clonación defensiva de BarRecord en cada lectura observacional + GC consecuente; hipótesis de valuación/sort/aritmética NO dominantes en este workload |

## 3. Repairs ejecutados (RED→GREEN, commit control `d609ca24`)

Cada repair tiene regresor mínimo ejecutado en este shot; los comandos y rc están en la evidencia (§8). La primera causa NQZ5 NO se redescubrió con corridas largas: el RED la reprodujo mínimamente (`recorded revision 5 is not current authority 7`, réplica del delta 4870→4872).

| Repair | Owner | RED demostrado | Fix | GREEN |
|---|---|---|---|---|
| A. Batch de revisiones de transición | `run.go` applyContextTransition + `driver.go` recordEconomics/recordEconomicsBatch + `sdk/futures/accounting/ledger.go` | transición START_NEW_STAGE con sink streaming → LEDGER_HISTORY_RELEASE_FAILED (rev 5 vs autoridad 7) | captura de TODAS las revisiones comprometidas (contexto, cierre/apertura de stage, día), registro ECONOMICS de cada una en orden, liberación por high-water contiguo del ledger CAPTURADO; guard de autoridad corriente preservado; ventana de evidencia rechaza mutación reentrante y liberación cruzada antes de mutar | TestBTXS02ContextTransitionBatchCapturesEveryCommittedRevision PASS; guards PASS |
| B. Cuerpo tipado sellado en admisión | `identity.go` ControlAdmission.TypedPayload + `run.go` EnqueueControl + `result.go` deepCopy + `cmd/reproduce.go` | admisión metadata-only: control que sale de pendientes y falla al aplicar queda sin payload recuperable (E1 "no typed payload") | deep-copy inmutable + verificación de digest en el sello, independiente de disposición (APPLIED/REJECTED/CONFLICT/pendiente); reproducer resuelve cuerpos sellados primero, fallbacks legacy intactos; conflicto nunca sobrescribe el primer cuerpo | TestBTXS02AdmissionSealsTypedPayload… PASS; TestBTXS02SealedPayloadSurvivesFailedApplication PASS |
| C. Replay oficial de campaña | `replay.go` ReproduceCampaign + footer.Campaign + `campaign.go` hooks.AfterResult + `cmd/campaign.go` sello + `cmd/reproduce.go` enrutado | replay bare-RunState: KIND_MISMATCH esperado ACCOUNT_REPLACEMENT vs OPERATION_APPLY (causa E1) | footer sella la petición de campaña + su resultado finalizado; el replay re-compone el DRIVER completo desde la petición sellada y compara records + decisiones tipadas (caja, compras, reemplazos, cobros, cuentas); no readmite como externos los controles regenerados | TestBTXS02CampaignReplayRedrivesFullDriver PASS (ciclo burn→compra→reemplazo; caja 4880→4760 oráculo A→B; IDENTICAL) |
| D. Continuidad multicontrato | `run.go` quiescencia/applySelection + `spec.go` catálogo + `campaign.go` sesión | (diseño §3.3) transición bloqueada por selección futura; año/mes del inicial copiado al seleccionado; sesión siempre catalog[0] | la quiescencia exige sólo obligaciones vigentes; catálogo multicontrato exige year/month declarados por entrada (preflight) y el seleccionado instala SU identidad; autoridad de sesión = contrato activo | TestBTXS02FutureSelectionDoesNotBlock… PASS; TestBTXS02MultiContractCatalogRequiresDeclaredExpiryIdentity PASS; TestBTXS02SessionAuthorityFollowsActiveSelection PASS |

Repairs de defects preexistentes del fixture CLI (necesarios para suite verde; sin cambio de producto): identidad declarada del binario recién construido (`btxS02DeclaredBuild`), par legacy unstamped con drift documentado vs baseline congelado `e2e15a3559` (log+return, causa registrada — el bloque era inalcanzable en 50250a2b por el conflicto de revisión).

## 4. Superficie integrada

`experiment` (CLI) consume `echo.backtest.experiment.v1`: UNA petición por modalidad (BASIC|CAMPAIGN) referenciando UN descriptor NT sellado; `experiment_id` = digest canónico del contenido semántico (modalidad, identidad de dataset por ref/digest, contrato, tiempos, políticas), excluye rutas locales/attempt/build; `attempt_id` identifica la ejecución física. Salida stdout JSON con estado, IDs, manifest, cobertura, resultado; `experiment-manifest.json` sellado junto a los outputs. `reproduce --experiment <manifest> --nt-source-config …`: BASIC por el reproducer bare-RunState; CAMPAIGN re-compone el driver completo. E2E PASS: `TestBTXS02ExperimentSurfaceBasicAndReplay` (BASIC COMPLETE + replay IDENTICAL, fixture nativo).

## 5. Medición del control corregido (normal, sellada antes de optimizar)

R BASIC NQU6 prefix (workload sellado E1, misma semántica, preparación fresca, timeout 120s): **wall 75,77s, CPU user+sys 141,79s (187%), maxRSS 60,4MiB, COMPLETE rc=0**, dinero idéntico al E1 (98.020,18 / −1.935 / 44,82 / 6 fills, 88.362 records). Tasa derivada: 45,2 µs/root-input (control corregido, esta máquina/estado) vs 53,5 µs (baseline E1, otra carga). La diferencia E1→control refleja estado de máquina (carga ajena 23 en 5min durante E1); la comparabilidad del contrato se ancla en mediciones back-to-back control vs candidato bajo el mismo protocolo (§6).

## PERF_CONTRACT

```text
PERF_CONTRACT_BTX_PERF_S02 = SEALED_2026-10-09T13:20-03:00
SEALED_BEFORE_ANY_PERFORMANCE_CHANGE = yes
CONTROL_CORRECTED_SHA = d609ca241eed63b1b4413af5bae5b849d334ead0
CONTROL_BINARY_SHA256 = 0db2feae6237ebc20ba8ce16bcc9f50fee0e6809c3677585b403a3d708c490ee

MAX_WALL_PER_MODE (horizonte completo solicitado, 13 contratos corpus autorizado
1.096.110 filas ≈ 75M root inputs, C financiera = 1, preparación integrada
secuencial correcta en el control):
  BASIC    <= 3600 s wall (proyección control 45,2 µs/input ⇒ ≈3390 s; margen 6%)
  CAMPAIGN <= 3900 s wall (+≈8,5% por lifecycle/reemplazos, delta medido E1 +2,8% CPU
              en prefijo + margen)
Anclas secundarias del mismo contrato (NQU6 completo, 6.464.027 root inputs):
  BASIC <= 180 s ; CAMPAIGN <= 220 s (exigen >= 1,62x sobre la proyección de
  control 292 s; attainable sólo con la eliminación sustentada del churn de
  cloneBarRecord/GC del perfil §2)

MIN_SPEEDUP_TARGET = 1,5x wall del control corregido en el MISMO workload
(R prefix NQU6 y NQU6 completo) medido back-to-back bajo el protocolo §5;
comparación control vs candidato con misma semántica/evidencia/completion.

MAX_RSS = 512 MiB por proceso (/usr/bin/time -v maxRSS, unidad KiB→MiB,
ámbito proceso completo: estado vivo + dedup + buffers/decodificación;
salida en disco aparte). Estado del guard duro in-process:
NOT_IMPLEMENTED_IN_CONTRACT (medición externa only, registrado).

THROUGHPUT: concurrencia financiera C=1 fija (una trayectoria, una evolución
Strategy/MM/cuenta/caja por modalidad; dos modalidades no son dos carteras
reiniciadas). Pool de preparación: workers ∈ {1,2} por admisión de recursos
(<3 CPUs efectivas o memoria insuficiente ⇒ 1); valores efectivos y razón
registrados por corrida. Chunks acotados 256 registros / 1 MiB serializado
(según diseño; cota no garantía de RSS).

VERIFICACIÓN (costos separados, todos incluidos en el presupuesto):
  ejecución (preparación+warmup+activo), escritura/Close/outputs (dentro del
  wall), replay oficial BASIC (bare reproducer), replay oficial CAMPAIGN
  (driver completo desde petición sellada), comparación tipada; total de
  verificación reportado explícito en §7.

COMPARABILIDAD: SHAs/binarios (control 0db2feae @ d609ca24 vs candidato),
mismo input/corpus/schedule/modelo/config/evidencia, mismo protocolo de
medición (aislado-proceso, unshare, timeout, /usr/bin/time -v), mediciones
back-to-back, misma política recorder/factories, población real de
records/actividad (records, fills, revisiones) contrastada por corrida.

FUNDAMENTO (medición vs proyección, separados):
  - Medido: control R-prefix 75,77s/60,4MiB (§5); perfil §2 (GC 38,7% CPU,
    cloneBarRecord 81,5% allocs, findSource 9%, flate 2%); mezcla E1 (91,7%
    OPERATION_APPLY); volumen corpus 1.096.110 filas / ≈75M inputs.
  - Proyección (objetivo, NO resultado): BASIC completo ≈ 3390 s a tasa de
    control; NQU6 completo ≈ 292 s a tasa de control.
  - Supuestos/sensibilidad: tasa µs/input estable entre prefijo y horizonte
    (E1: consistente 53,5 µs prefijo vs 53,5 derivado NQU6 bajo contención
    14x→aislado); estado de máquina ±20% ⇒ por eso MIN_SPEEDUP se mide
    back-to-back; warmup incluido en tasa media; NO se adoptan 53,5 µs como
    coste de todos los años, ni 2x como demostrado, ni 512MiB como
    multianual verificado (queda como target con medición obligatoria).

BIFURCACIÓN CERRADA: si el candidato no sostiene estos campos con evidencia
comparable, se entrega OPTIMIZATIONS=MISS_DOCUMENTED con el bloqueo específico;
no se mueven los objetivos después de ver resultados.
```

Recibo del sello: SHA256 del bloque PERF_CONTRACT anterior (delimitadores inclusive) = `BTX_PERF_CONTRACT_BLOCK_SHA256: ff320f01e9954eefaf84de5380b78e8b99e334d42ac10bf50f018d34ae89079d`; registrado ANTES del primer commit de optimización (§6).

## 6. Optimizaciones sustentadas (post-sello)

Ejecutadas tras el sello (OPTIMIZED_SHA `584a3cd91d8ecf2d8f292547a35f8e9963e2270d`, binario `e5d4860b4e70f5f5833ebf374b08fb771a4551bc6d58996fa42305e1049bd141`, vcs.modified=false), cada una sostenida por el perfil §2 y dentro de los contratos del diseño:

| Mecanismo | Owner | Sustento | Descarte registrado |
|---|---|---|---|
| Transferencia read-only de la ventana del anillo (`bars.Ring.RecentShared`) al snapshot de barras; `marketctx` almacena la ventana por referencia (el modelo REEMPLAZA por (stream,timeframe), nunca acumula ni muta) | sdk/futures/bars + analytics + marketctx | cloneBarRecord 81,5% del alloc space; GC 38,7% CPU | Ninguno: la copia defensiva se conserva en toda frontera pública/multi-consumidor (`Recent` intacta) |
| Índice de membresía de fuentes del Builder (`findSource`): Forming ∪ LastSource ∪ Ring con mantenimiento exacto (inserción, evicción vía `Ring.PushEvict`, descarte de forming), no serializado, rebuild lazy | sdk/futures/bars | findSource 9% CPU (escaneo lineal por record) | Índice de owners del scheduler (no dominante en perfil) |
| Compresión gzip BestSpeed sin pérdida | resultwriter | flate ≈3,5s (2%) en R | Writer asíncrono, formato columnar: prohibidos por diseño |

Discartes sin justificación medida: valuación incremental exacta (valuación/sort/aritmética NO dominantes en el perfil — hipótesis de E1 quedaron refutadas como coste dominante), fast paths del lattice, paralelismo de preparación (no requerido por el perfil; el coste está en minutos activos, no en preparación).

## 6.1 Resultado de la comparación back-to-back (R prefix sellado, mismo protocolo §5)

| Métrica | Control `d609ca24`/`0db2feae` | Candidato `584a3cd9`/`e5d4860b` | Delta |
|---|---:|---:|---|
| Wall R (timeout 120s) | 75,77 s | 34,01 s | **2,23× (≥ MIN_SPEEDUP 1,5× ✓)** |
| CPU user+sys | 141,79 s | 48,69 s | 2,91× |
| maxRSS | 60,4 MiB | 54,5 MiB | −9,8% (≤512 MiB ✓) |
| Resultado económico | 98.020,18 / −1.935 / 44,82 / 6 fills | idéntico | dinero exacto ✓ |
| Records | 88.362 | 88.362 | ✓ |

Comparación causal tipada control→candidato: **88.362/88.362 records presentes en ambos; 109 diferencias, TODAS cadenas de IDs/hash derivados del build (misma clase de cascada que E1 documentó entre horizontes); cero divergencia semántica tras normalización tipada de IDs; dinero idéntico.** Replay oficial del candidato: IDENTICAL (rc=0).

## 7. Resultados del candidato y comparación

### 7.1 Verificación del contrato PERF_CONTRACT

| Campo | Estado | Evidencia |
|---|---|---|
| MIN_SPEEDUP_TARGET 1,5× | **CUMPLIDO** | 2,23× wall back-to-back en R (§6.1), mismo workload/protocolo/semántica |
| MAX_RSS 512 MiB | CUMPLIDO en prefijo (54,5 MiB); horizonte completo no ejecutado en presupuesto | §6.1 |
| MAX_WALL_PER_MODE horizonte completo (BASIC ≤3600s, CAMPAIGN ≤3900s) | **NO VERIFICADO FÍSICAMENTE — bloqueo específico** | ver 7.2 |
| Anclas secundarias NQU6-completo (≤180s/220s) | **REFUTADAS como proyección; NO verificadas** — la tasa µs/input NO es uniforme | ver 7.2 |
| Throughput C=1, pool ∈ {1,2} | C=1 ejecutado en todas las corridas; pool no requerido (preparación no dominante) | §6.1 |
| Verificación (replay oficial + comparación) | Replay BASIC candidato IDENTICAL; comparación causal tipada sin divergencia semántica | §6.1 |

### 7.2 Bloqueo específico: horizonte completo (preexistente, no introducido por S02)

El coste por minuto activo de trading escala con la amplitud intraminuto del lattice V2 (diseño §3.4 lo anticipó: «multiplicación de trabajo activo por amplitud intraminuto») y con la exposición; la tasa µs/root-input NO es uniforme entre warmup y trading activo. Evidencia de esta sesión:

- NQU6 completo (65 días, candidato): excede 600s y 900s; en 900s procesa 301.911 records llegando a 2026-07-21T03:43Z (≈2,2 días causales de exposición pesada, 204.570 OPERATION_APPLY, 18 fills) ⇒ proyección observada ≈5h de wall para el contrato completo.
- NQU6 completo con el CONTROL corregido: excede 600s (mismo bloqueo en la referencia; NO es regresión del candidato).
- NQZ5 (contrato 2025, alta volatilidad): el warmup+prefijo 2025-10-13→11-20 excede 240s con el candidato (4,9 ms/record medidos en warmup NQZ5 vs 0,39 ms/record del prefijo R NQU6 — 12,6× por amplitud/actividad del contrato).
- Calibración histórica s06 (misma máquina): NQU6 full-extent BASIC 5.277s, CAMPAIGN hasta 3.993s, bajo contención 13–14× con GOMAXPROCS=1 ⇒ los horizontes completos toman HORAS, no minutos; la proyección de E1 (346s aislados) asumía tasa uniforme y quedó refutada por medición.

Consecuencia por la bifurcación cerrada del mandato: los objetivos de horizonte completo quedan como objetivo sellado NO verificado físicamente; NO se mueven después de ver resultados; el speedup demostrado está anclado al workload comparable sellado. La verificación de horizonte completo requiere corridas de horas (fuera del presupuesto de esta sesión ONE-SHOT) y pertenece a S03/S04 o a una ventana de ejecución dedicada.

### 7.3 Primera ejecución real NQZ5 (repair A)

NQZ5 REAL completo: NO alcanzada en presupuesto (7.2: el prefijo que cruza la transición del defecto, 2025-10-13→11-20, excede 240s con el candidato; la corrida completa es de horas). La verificación del repair queda demostrada por: (1) RED mínimo que reproduce la SECUENCIA EXACTA de E1 (SetAccountContext k + CloseStage k+1 + OpenStage k+2 → liberación de k bajo sink streaming: «recorded revision 5 is not current authority 7», réplica del 4870→4872 del artefacto NQZ5 de E1, sin re-corrida del caso roto); (2) GREEN del batch con captura de todas las revisiones (TestBTXS02ContextTransitionBatchCapturesEveryCommittedRevision); (3) replay de campaña con ciclo real burn→compra→reemplazo y oráculo de caja A→B (4880→4760) IDENTICAL (TestBTXS02CampaignReplayRedrivesFullDriver). El stream parcial real NQZ5-R del candidato (spool 40MB, 49.359 records, warmup hasta 2025-10-21) quedó preservado como evidencia de ejecución real sin abortos de correctness. S03 (falsificación independiente) conserva su gate sobre NQZ5 real.

### 7.4 Cobertura y suites

- **Regresores S02 dedicados (TestBTXS02\*): 8/8 PASS** (batch+ownership 2, admission seal 2, multicontrato 3, replay campaña 1) + E2E `experiment` (CLI real, BASIC COMPLETE + replay IDENTICAL) + `TestBTXS02RecentShared…` (ventana read-only, estabilidad bajo evicción).
- **Cobertura del código nuevo/modificado** (denominador real, funciones S02): `SealCampaignRequest` 100%, `LiveContract`/`Admissions`/`NextNegotiableOpen` 100%, `firstCampaignResultDivergence` 83%, `EnqueueControl` 82%, `ensureSourceIndex` 85%, `campaignArtifactRequest` 79%, `applyContextTransition` 75%, `recordEconomicsBatch` 76%, `activeSessionStream` 78%, `ReproduceCampaign` 69%, `deepCopyResolvedControl` 71%, `PushEvict`/`findSource`/`sourceIndexForget` 100%. Las ramas descubiertas son fallos nombrados (integrity/ownership) ejercitados parcialmente por oráculos negativos; floor 95% del paquete NO alcanzado en el denominador completo (58,1% contando sólo regresores S02 sobre backtester+bars+accounting) — queda como trabajo de S03/S04, no se rellena con tests cosméticos.
- **Suites completas**: `cmd/echo-backtest` ✓ verde (220s); `sdk/futures/...` ✓ verde; paquete `backtester`: los 8 fallos (TestBTGS03_CampaignCashBurnReplacementAndContinuity, TestBTGS03_V2IntrabarAddsAdverseAndProtection, TestBTGS04CampaignBurnCashLedger, TestBTGS04_MixedMinuteCapabilityBoundary, TestBTGS04_StructuralReferenceSkipFirstDivergence, TestFreshProcessDeterminism, TestLargeCorpusStreamingMetrics, TestBT_S04_StandaloneReproduceClosedSpec) son **PREEXISTENTES en `50250a2b` puro**: triple ejecución demostrada (worktrees `50250a2b` / `d609ca24` / candidato) con fallos idénticos — ni los repairs ni las optimizaciones los introducen ni los agravan. Causas observadas: fixtures que declaran builds sintéticas contra binarios con stamp vcs (clase ya documentada), y derivaciones de IDs de orden entre políticas ALL/SKIP (invariancia de IDs pendiente, alcance S03).
- **race focalizado** (delta): bars/accounting/marketctx `-race` PASS.

## 8. Evidencia transportable (fuera del vault)

Raíz: `/home/kor/aranea/work/btx-perf-s02-20261009/` — `inputs/` (derivados mecánicos con hash), `logs/` (recibos stdout/stderr), `measure/` (time -v, rc, sellos), `probe/` (variante instrumental + perfiles CPU/heap), `out-control-R/` (artefacto causal del control), `bin/` (binarios con SHA). Sin secretos ni dumps en Markdown.

## Fuentes

- Adenda Owner 2026-10-09 y [[BTG-PLAN]]: secuencia vinculante, sello antes de optimizar.
- [[BTX-PERF-DESIGN]]: contratos técnicos (§5 topología, §6 hot path, §8 repairs, §9 replay, §10 superficie).
- E1: `BTX-PERF-E1-EVIDENCE.md` + cápsula verificada (15/15 SHA256).
- Source `50250a2b` y rama `codex/btx-perf-s02` @ `d609ca24` (publicada).
