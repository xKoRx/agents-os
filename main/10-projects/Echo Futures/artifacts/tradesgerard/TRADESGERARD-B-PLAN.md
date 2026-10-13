---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[TRADESGERARD-CONTROL]]"
  - "[[TRADESGERARD-CONTRACT]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-12"
updated: "2026-10-12"
---

# TRADESGERARD-B-PLAN

## Propósito

Plan de trabajo B bajo KISS-1: tabla finita de 10 configuraciones económicas, tandas T0/T1/T1-L y pendientes I2. Precedencia: KISS-1 y las exclusiones de §12 del mandato sobre el catálogo histórico design-2 (HISTÓRICO, no orden vigente).

## Identidad B

| Elemento | Valor |
|---|---|
| Base | `xKoRx/echo` @ `d752b3e124386330e6f8e4b270958cc2db892734` (freeze A, rama `codex/tradesgerard-platform-a`) |
| Checkout desarrollo B | `ARANEA_ROOT/work/tradesgerard-b-glm-20261012/echo`, rama local `codex/tradesgerard-b-glm` (sin push) |
| Binario B | propio de cada build B; identidad separada del binario A (`8abe7379…fcc98ff`) |
| Perfil comercial | `E2T_GAU50_PURCHASE_GE_20260706_OBS_20261012_SCENARIO_V1` (A, [[TRADESGERARD-PROP-PROFILE]]) |
| Módulos B | Strategy `tg` (SIG-B) + MM `tgmm` registrados en la composición compartida; CLI `platform-prepare`/`platform-batch` |

## Tabla de configuraciones (10 por ventana)

R = pérdida neta presupuestada, T = beneficio neto objetivo del ciclo; T efectivo = min(Tref, remanente del objetivo aplicable), R proporcional conservando ρ. Retiro = solicitud bruta antes de split/cargos.

| Config | ID campaña | K | Rref | Tref | ρ | Retiro |
|---|---|---|---:|---:|---:|---:|
| 1 | `tg-i1-k01-r2300` | K01 | 250 | 250 | 1:1 | 2300 |
| 2 | `tg-i1-k01-r3000` | K01 | 250 | 250 | 1:1 | 3000 |
| 3 | `tg-i1-k02-r2300` | K02 | 500 | 500 | 1:1 | 2300 |
| 4 | `tg-i1-k02-r3000` | K02 | 500 | 500 | 1:1 | 3000 |
| 5 | `tg-i1-k03-r2300` | K03 | 500 | 1000/3 | 3:2 | 2300 |
| 6 | `tg-i1-k03-r3000` | K03 | 500 | 1000/3 | 3:2 | 3000 |
| 7 | `tg-i1-k04-r2300` | K04 | 500 | 250 | 2:1 | 2300 |
| 8 | `tg-i1-k04-r3000` | K04 | 500 | 250 | 2:1 | 3000 |
| 9 | `tg-i1-k05-r2300` | K05 | 1000 | 250 | 4:1 | 2300 |
| 10 | `tg-i1-k05-r3000` | K05 | 1000 | 250 | 4:1 | 3000 |

Geometría: TP 1×ATR / SL ρ×ATR (ATR20 Wilder, estocástico lookback20 K lenta SMA3 — defaults fijos, no optimizables). Iteración1: sin adds, sin Gerard, sin progresiones tras ganancia, sin BE, sin extensión, sin salida por falta de confirmación. Una campaña continua por configuración sobre la ventana común; sin FIT-EQUAL ni reparto artificial del día.

## Tandas

| Tanda | Alcance | Estado |
|---|---|---|
| T0 | Implementación `tg`+`tgmm`, pruebas críticas (oráculo indicadores, cruce/consumo único, warmup/gap/roll, sizing ATR/ρ, remanente 330 con Tref500, recorte proporcional, R/T congelados, cierre sesión, aislamiento, ambos retiros) + smoke real NQZ5 corto + recursos | COMPLETE — [[TRADESGERARD-B-T0]] (commit `67ec0099`, binario `60accecc…`, smoke reconciliado; T1 EN EJECUCIÓN) |
| T1 | Validar cobertura de la ventana común más larga disponible (requisitos reales TradesGerard; all13 NOT_READY declarado), correr las 10 configuraciones sobre el mismo intervalo, campañas continuas | COMPLETE 10/10 conciliadas — [[TRADESGERARD-B-T1]]; ventana NQZ5 2025-10-13→11-25 validada (0 huecos); 0 cobros; binario `f00efd66…` (fix `10d406b3`) |
| T1-L | Hasta 3 años sobre los 2 perfiles mejor posicionados por caja neta de T1 (AMBOS retiros, máx 4 configs; criterio fijado antes de ver resultados); tramo reservado fuera de muestra si existe | COMPLETE 4/4 fuera de muestra — [[TRADESGERARD-B-T1L]] (2025-11-30→12-15; K01 0 ops; K02 −1.714,80; 0 cobros) |
| I2 | PENDING_OWNER_RULE: X del add B2, rango a conservar, límite de repeticiones, criterio «no se confirma, salir»; BE +200/extensión 500 como salidas explícitas. No implementar sin decisión del Owner | BLOQUEADO — preguntas formuladas en [[TRADESGERARD-B-RESULTADO]] §Pendientes |

## Ventanas y corpus

| Uso | Corpus/ventana | Estado |
|---|---|---|
| T0 smoke | NQZ5 recheck `evidence/recheck/inputs/cli-real` (2025-10-28, 1h + warmup) | validada por A |
| T1 | por determinar: `validate-catalog` sobre el corpus derivado `work/btx-perf-last-20261010/integrator/package/corpus`; ventana común válida más larga; si < 1 año, declarar duración exacta | PENDING |
| T1-L | mismo corpus, extensión según cobertura real + tramo reservado | PENDING |

## Recursos y límites

Reserva ≥8 GiB (disco hoy 9,5G libres — margen justo, vigilar), salida durable ≤256 MiB por lote, trazas/resultado ≤16 MiB, logs ≤16 MiB, GOMAXPROCS=4 por carril de campaña; concurrencia de campañas independientes sólo con CPU/RAM/disco medidos. Compacto desde el productor; limpieza de temporales propios tras verificar entrega.
