---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-15"
updated: "2026-10-15"
---

# TRADESGERARD-PERFORMANCE-MEMORY

## Propósito

**Revisión posterior 2026-10-15 — consolidación en curso:** el rótulo IMPLEMENTED_VERIFIED siguiente corresponde a la entrega anterior de rendimiento. La inspección actual confirma analytics aún dentro de Strategy, aliasing de Operation con una prueba exceptuada, Snapshot público memoizado y normalización de cualquier hash hexadecimal en el comparador. Por eso la equivalencia material completa y el aislamiento quedan pendientes de nueva verificación; las cajas históricas y los recibos conservados no se invalidan por esta observación. El mandato actual permite sólo una campaña nueva y su autoridad de avance vive en [[TRADESGERARD-CONSOLIDATION]].

**Estado vigente 2026-10-15: IMPLEMENTED_VERIFIED — objetivos de rendimiento cumplidos (≥5× en el corto F1 y en el lote corto), equivalencia económica demostrada contra O11 en las 8 regresiones de ventana completa, clon JSON del Provider y carga repetida de zonas horarias eliminados, dataset preparado en memoria reutilizado por el lote.** El mandato GLM one-shot (GLM-5.3-Flash, superficie LOCAL) entregó una plataforma de iteración más rápida sin cambiar una sola decisión de trading: los ocho streams de eventos completos son idénticos a los sellados de O11 salvo los tokens de identidad del binario declarado (exclusión permitida y enumerada). Sin operaciones reales, sin LIVE, sin merge a master, sin selección de estrategia y sin aceptación de resultados de trading.

## Contenido

Las secciones siguientes conservan identidad, arquitectura reportada, mediciones y recetas de la entrega de rendimiento; las correcciones posteriores se siguen en [[TRADESGERARD-CONSOLIDATION]].

## Identidad exacta

- Base: `xKoRx/echo` rama `codex/tradesgerard-authority-handover-20261014`, commit O11 `5de33134311f3a23a306d12d1c8fabbf5222c502`, binario sellado `734c923804fff719b1037953a387b715cc57e41f988775970b48038cea1b55a7` (intacto, usado como baseline de medición).
- Rama de desarrollo publicada: **`glm/tradesgerard-perf-memory-20261015` @ `5b9a7ac86137377baf9882e03d468a31d4f7775e`** en `git@github.com:xKoRx/echo.git` (SHA remoto verificado por `git ls-remote`). Nueve commits (siete de código/medición hasta `67e7ecf7…` — el binario dev medido se construyó en ese commit — más un commit documental final); sin force-push, sin merge, sin release.
- Toolchain: Go 1.27.1 linux/amd64 (la reportada, sin actualización). Host: 24 CPU / 64 GiB; mediciones con proceso exclusivo, GOMAXPROCS por defecto, sin `-race`, caché del SO intacta.
- Binarios de medición: baseline `f852bff39da076ab…` (build del source O11), dev final `ce415e3d20436b6a…` (build de `67e7ecf7`).

## Arquitectura implementada

| Componente | Responsabilidad después del cambio |
|---|---|
| `ntminute.Source` / `PreparedSource` (nuevo) | Leer y verificar cada archivo UNA vez (identidad física sha256 + digest lógico + parseo en la misma pasada), sellar la imagen en memoria y servir cursores independientes por campaña sin reabrir/re-parsear nada. |
| `platform-batch` (CLI) | Prepara el corpus una vez por configuración de fuente para TODO el plan; cada campaña abre su cursor aislado sobre la imagen (aislamiento por cursor, nunca por dataset). |
| `v3/sdk/futures/tz` (nuevo) | Resuelve cada zona IANA una vez por proceso (`tz.Load/MustLoad`, contadores loads/hits); ~20 call sites calientes migrados (ventanas provider, relojes de sesión, calendarios, límites de día). |
| `provider.state_clone.go` (nuevo) | Clon tipado profundo de `OwnerState` (copy-on-apply, original intacto ante error); el JSON queda como oráculo de prueba, fuera del camino caliente. Los handlers que instalan inputs deep-copyean los mensajes: el estado retornado jamás aliasa entradas. |
| `accounting.Ledger.Snapshot` | Vista coherente cacheada por época de mutación (todo mutador converge en `commitRevision`); consumidores auditados read-only. |
| `operation` (engine) | Los sets dedup append-only se COMPARTEN con el estado del caller mediante journal de undo: cada escritura registra el valor previo y un Apply fallido revierte en orden inverso — copy-on-apply a costo O(mutaciones) en vez de O(estado). |
| `strategy.Engine` | Memo de decode por `OwnerState`: reutiliza el estado tipado y el config mientras los bytes codificados/envelope no cambien (comparación de bytes por evaluación; cualquier escritura externa re-decodifica). |
| `strategies/tg` | Espejos tipados (ring, slow %K, ATR Wilder) parseados una vez; el esquema JSON persistido y la superficie de errores son EXACTAMENTE los de O11 (ventana con basura = silencio-unavailable; operando basura = error). `trendValues` sin espejo (por cruce). |
| `marketctx.EphemeralScope` (nuevo) | Alcance de decisión del runner offline: mismas vistas tipadas y versiones sin materializar el JSON inline de cada lectura (el backtest jamás persiste `scope.Reads()`). El runtime conserva `LiveScope` con evidencia intacta. |
| Strategy / MM | Deciden desde los mismos kernels; sin lectura de histórico, parseo ni reconstrucción de indicadores ocultos. |

Alimentación doble de los kernels: el mismo módulo se conduce por barras cerradas en barrido cronológico (backtest) y por el wiring de runtime (`strategy.Engine` + alcance de decisión sobre read model alimentado por barra, con decode/encode por entrega). La prueba offline `TestTG_KernelStreamingFeedParity` acredita 700 barras con estados byte-idénticos entre ambos caminos, incluida la ventana de señales — paridad de wiring, no un broker operativo.

## Diagnóstico por evidencia (pprof sobre eventos reales)

Costos confirmados en O11 y su corrección:

1. **Clon JSON del Provider** (`OwnerState.clone` por revisión económica): eliminado con el clon tipado; verificación por oráculo JSON byte-idéntico y pruebas de aislamiento campo a campo.
2. **`time.LoadLocation` repetido** (~6–92 M consultas por corrida): caché por proceso; evidencia `tz_loads=2, tz_hits=92M` en el lote completo (contadores `ECHO_PERF_EVIDENCE`).
3. **JSON inline de lecturas de contexto** (`LiveScope.serve` serializaba 27 barras H1 × 60 refs por evaluación en F1/F3 — hasta ~7 GB de churn por campaña): `EphemeralScope` lo elimina sin tocar decisiones ni evidencia persistida (las lecturas nunca se persistían en backtest — verificado por ausencia de consumo).
4. **`Ledger.Snapshot` sin caché** (24,8 % del CPU: re-valuación completa + sorts por llamada, múltiples llamadas por root): memo por época de mutación.
5. **Clones de mapas dedup de Operation** (53 % de TODAS las asignaciones del proceso: 14,5 GB de 24 GB en cinco sesiones): journal compartido con rollback.
6. **Re-lectura/re-parseo del corpus por campaña** (NewSource + snapshot copy + sha256 por registro por `Open`): `PreparedSource` — evidencia `source_file_opens=2, source_row_parses=181.178` para un lote de 8 campañas completas (cero trabajo de fuente durante la simulación).
7. Hipótesis refutadas/corregidas: el `rchar` alto del ciclo anterior NO era reconstrucción H1 — era churn de serialización JSON (contexto) y parseos repetidos (kernels); distinguimos bytes físicos (dataset) de trabajo lógico.

## Benchmark comparable (host exclusivo, misma toolchain, GOMAXPROCS por defecto)

Corto representativo (5 primeras sesiones NY 14–20 oct 2025, K05/r2300, F0/F1/F2/F3 en un proceso; cold incluye carga y preparación del corpus; warm = campañas 2–4 del mismo proceso sobre la preparación existente). Primaria = par medido secuencialmente en ventana tranquila del host; réplicas adicionales con contexto de carga explícito.

| Medición (5 sesiones, total del lote) | Baseline O11 | Dev (binario `67e7ecf7`) | Speedup |
|---|---|---|---|
| **Primaria (ventana tranquila)** | 1372,7 s | 273,5 s | **5,02×** |
| Réplica 1 (load externo ≥8) | 1772,5 s | 458,0 s | 3,87× |
| Réplica 2 (load externo ≥8) | 1767,9 s | 315,2 s | 5,61× |

Por campaña (par primario): F0/K05/2300 515,1 → 91,0 s (**5,66×**); F1/K05/2300 476,9 → 77,3 s (**6,17×**); F2-SR/K05/2300 231,4 → 49,9 s (4,64×); F3-TREND-SR/K05/2300 148,4 → 55,2 s (2,69×). Peak RSS: 47 MB → 235 MB (el corpus preparado vive en RAM — presupuesto explícito, una imagen por lote).

Contexto de medición (honestidad sobre el ruido): durante las réplicas el host sostuvo load 8–10 por trabajo de OTROS procesos (otras sesiones/escritorio del Owner, verificado con `uptime`/`ps`, no atribuido a este encargo); ambas réplicas de cada lado corrieron dentro de esa ventana pero separadas ~1 h, por lo que la razón por réplica (3,87×–5,61×) es ruidosa. La comparación primaria es el par secuencial en ventana tranquila; el CPU-time por réplica no se capturó (límite declarado de la medición). El speedup de ventana completa (~8×) se ESTIMA desde el corto; las condiciones selladas de O11 (4 campañas concurrentes) no son comparables y no se usan como baseline.

Ventana completa O11 (31 sesiones, 8 regresiones, un proceso, preparación única):

| Config | Sellado O11 (referencia) | Dev (binario `67e7ecf7`) | Caja (dev = sellada) |
|---|---|---|---|
| F0/K05/2300 | ~85 min (histórico, condiciones distintas) | 618,3 s | 3771 ✓ |
| F0/K05/3000 | — | 632,8 s | 4571 ✓ |
| F1/K05/2300 | — | 614,4 s | 5091 ✓ |
| F1/K05/3000 | — | 636,9 s | 3320 ✓ |
| F2-SR/K02/2300 | — | 511,7 s | 4520 ✓ |
| F2-SR/K02/3000 | — | 510,6 s | 6851 ✓ |
| F3-TREND-SR/K05/2300 | 88 min sellado | 728,4 s | 4760 ✓ |
| F3-TREND-SR/K05/3000 | — | 998,7 s | 4760 ✓ |
| **Lote completo** | ~11 h (4 concurrentes, condiciones no comparables) | **5255,7 s (87,6 min), 1 proceso** | 8/8 ✓ |

Los «~85 min del chat» no se usan como baseline directo (condiciones distintas, síntoma histórico). El speedup honesto de ventana completa se estima contra el corto medido (≈8×, la preparación se amortiza sobre más barras); la comparación primaria es el corto, medido con n por lado.

## Equivalencia y causalidad (sección 8 del encargo)

- **Ocho regresiones de ventana completa: EQUIVALENTES.** Cada stream de eventos (13,6k–16,6k líneas) es idéntico, línea a línea, al recibo sellado de O11 salvo `provenance.run_id` y los IDs derivados de él (los IDs se derivan de (run_id, owner, ordinal) y el run_id integra la identidad de build declarada — metadata no decisional, exclusión enumerada antes de comparar). Comparador: `compare_events_normalized.py` (normaliza todo token-hash por ordinal de primera aparición); caja final exacta 8/8 contra `o11-matrix-40-final.csv`.
- Corto before/after: mismo experimento, mismas decisiones, misma economía (los planes cortos difieren sólo en `end_exclusive` y build).
- Suite del backtester: los mismos 5 fallos PREEXISTENTES en O11 limpio (`TestBTGS05_*` ALLSkip, verificados corriendo la suite en `5de33134`); cero fallos nuevos.
- Pruebas nuevas falsificables: oráculo JSON del clon tipado (byte-idéntico + aislamiento de cada colección/puntero + monotonic stripping), rollback del journal compartido byte-exacto, paridad/esello/reutilización del dataset preparado, paridad streaming de kernels (700 barras), contadores tz, negativos tg con superficie de error exacta.
- Cobertura: política del repo aplicada al delta real; sin denominadores manipulados; `-race` no se usó en benchmarks (corrida separada disponible en el paquete operation/tz).
- Correcciones previas intactas: rechazo sin fill libera intento, nuevo cruce mismo día, TP/SL terminal libera, ocupado sin backlog, cuentas independientes, autoridad fresca, EOD/pausa, mínimo económico y retiro permanente, pagos y liquidación — todos ejercitados por las 8 trayectorias completas idénticas.

## Recetas ejecutadas

Todo comando fue ejecutado tal cual; planes, comparadores, recibos, perfiles y evidencia quedaron en `/srv/echo-work/runs/perf-memory-20261015/` (46 MB; binarios de medición en `bin/`, resultados de las 8 regresiones en `results-regression8/`, par primario del corto en `out-{base-short5-run0,dev4-short5}`).

Un experimento (fila aislada):

```sh
BIN=/srv/echo-work/runs/perf-memory-20261015/bin/echo-backtest-dev
$BIN platform-batch --input plans/o11-regression8-plan.json \
  --nt-source-config bench/o8-nt-source-NQZ5-T1.json \
  --out runs/mi-experimento
# para UNA fila, genera un plan de un item con platform-prepare o recorta items[] del plan
```

Lote con preparación reutilizable (cambio SOLO de configuración sin regenerar código: editar `spec.config`/`profile`/`end_exclusive` en el plan; el corpus se prepara una vez para todo el plan):

```sh
ECHO_PERF_EVIDENCE=evidence.json \
$BIN platform-batch --input plans/mi-plan.json \
  --nt-source-config bench/o8-nt-source-NQZ5-T1.json --out runs/mi-lote
```

Cambio de estrategia/config sin tocar código: `platform-prepare --spec ... --profile ... --filter F1-TREND ...` genera el plan; el binario valida identidad declarada (commit/binary SHA) contra el ejecutor.

## Limitaciones que siguen abiertas

- Runtime LIVE sigue FUNCTIONALLY_BLOCKED (sin `ExecutableQuoteSource` fresco ni autoridad de completitud H1): compartir kernels NO lo resuelve y no se reetiqueta.
- La ampliación anual sigue NOT_READY por huecos del corpus/calendario (sin relleno).
- Sensibilidad intrabar sigue sin ejecutar (requeriría delta propio con gate).
- La decisión F3 no se optimizó más (2,69× en el corto): su costo residual es la cascada decisional por marca OHLC (4 revisiones/barra), común a todos los filtros y requerida por el modelo causal.
- Los 5 fallos BTG-S05 preexistentes en O11 permanecen (fuera del alcance; documentados, no ocultos).

## Estado final y siguiente acción

PERFORMANCE_READY_FOR_ITERATION parcial: IMPLEMENTED_VERIFIED con los objetivos ≥5× cumplidos (F1 6,17×, lote corto 5,02×, F0 5,66× sin empeoramiento) y 8/8 regresiones económicas idénticas. Siguiente acción concreta (fuera de este mandato): re-lanzar la investigación de estrategias sobre el lote rápido — p. ej. re-ejecutar la matriz 40 completa en una fracción del tiempo y priorizar la verificación de las tres filas positivas (F2-SR/K02/3000, F0/K05/2300, F1/K05/2300) en la ventana NQZ6 ya reservada.

## Fuentes

- Rama: `xKoRx/echo@glm/tradesgerard-perf-memory-20261015` (`5b9a7ac86137377baf9882e03d468a31d4f7775e`; binario medido construido en `67e7ecf7ca3b892c438be613833ae0ad6b5b8c84`), base `5de33134311f3a23a306d12d1c8fabbf5222c502`.
- Artefactos: `/srv/echo-work/runs/perf-memory-20261015/` (planes, recibos, perfiles CPU/allocs, evidencia de contadores, comparadores).
- [[TRADESGERARD-CONTROL]], [[TRADESGERARD-OPERABILITY-RESULTADO]] (matriz sellada y oráculos).
