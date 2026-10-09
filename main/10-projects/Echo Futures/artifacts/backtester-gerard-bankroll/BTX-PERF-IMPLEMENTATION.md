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

Artefacto S02 (TOP LOCAL fresh-context ONE-SHOT, Daedalus): implementación, integración y performance del backtester con referencia corregida, según la adenda Owner de 2026-10-09 y [[BTX-PERF-DESIGN]]. Este documento contiene la sección única `PERF_CONTRACT` sellada ANTES del primer cambio de rendimiento; el bloque congelado conserva sus bytes y hash en la evidencia transportable. Estado devuelto: `READY_FOR_S03_REVIEW` condicionado a los resultados abajo; no hay aceptación de producto.

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

ESTADO: pendiente de ejecución; sólo mecanismos del perfil §2 dentro de los contratos del diseño: read models observacionales estrechos (eliminar clonación defensiva por lectura en `bars.Ring.Recent`), índice mantenido para `Builder.findSource`, compresión BestSpeed sin pérdida, con fallback exacto y biyección tipada control→candidato. Selección y descartes se registran aquí tras la medición.

## 7. Resultados del candidato y comparación

ESTADO: pendiente de ejecución post-sello.

## 8. Evidencia transportable (fuera del vault)

Raíz: `/home/kor/aranea/work/btx-perf-s02-20261009/` — `inputs/` (derivados mecánicos con hash), `logs/` (recibos stdout/stderr), `measure/` (time -v, rc, sellos), `probe/` (variante instrumental + perfiles CPU/heap), `out-control-R/` (artefacto causal del control), `bin/` (binarios con SHA). Sin secretos ni dumps en Markdown.

## Fuentes

- Adenda Owner 2026-10-09 y [[BTG-PLAN]]: secuencia vinculante, sello antes de optimizar.
- [[BTX-PERF-DESIGN]]: contratos técnicos (§5 topología, §6 hot path, §8 repairs, §9 replay, §10 superficie).
- E1: `BTX-PERF-E1-EVIDENCE.md` + cápsula verificada (15/15 SHA256).
- Source `50250a2b` y rama `codex/btx-perf-s02` @ `d609ca24` (publicada).
