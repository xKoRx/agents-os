---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[TRADESGERARD-B-PLAN]]"
  - "[[TRADESGERARD-B-T0]]"
  - "[[TRADESGERARD-CONTROL]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-13"
updated: "2026-10-13"
---

# TRADESGERARD-B-T1

## Propósito

Reporte de la tanda T1 KISS-1: las diez configuraciones económicas sobre una ventana común continua, campañas completas y conciliadas. Resultado: **T1 COMPLETE 10/10** — **ninguna configuración cobró**; ninguna alcanzó aprobación de evaluación. La caja neta de campaña empató en 4.760 USD para las diez.

## Contenido

## Estado técnico y cobertura

> Corrección identificable ENTRY-REPAIR-C01 (2026-10-13): COMPLETE10/10 y conciliación históricos se conservan. El readback independiente encontró755 OPEN por configuración,169 intentos/137 rechazos por cinco perfiles y338/274 para los diez;162/253 no concilia. Las afirmaciones posteriores que equiparan31 intentos K01 con todos los cruces del mes y atribuyen toda la baja actividad al sizing quedan analíticamente afectadas. El detalle, la reproducción y el reemplazo en curso están en [[TRADESGERARD-ENTRY-REPAIR]]. La tabla «Operaciones (fills)» cuenta registros FILL; por ejemplo36 corresponden a18 operaciones con fills.

| Elemento | Valor |
|---|---|
| Configuraciones esperadas / completas / fallidas / pendientes | 10 / 10 / 0 / 0 |
| Identidad | commits `67ec0099` + `10d406b3`, binario `f00efd668eee8b121f7efb65b1b92923620e47beaac650a99491b425027486e8` (go1.27.1, vcs.modified=false) |
| Ventana común | NQZ5 **2025-10-13T17:51Z → 2025-11-25T23:00Z** (validate-catalog COMPLETE: 44 días de cuenta, ~31 sesiones, 42.969 minutos abiertos, 0 huecos) |
| Motor | `platform-prepare`/`platform-batch` CLI, `REGISTERED_CONFIG_V1`, campañas continuas (una por configuración, sin partir ni reiniciar caja) |
| Ejecución | 3 carriles concurrentes medidos (GOMAXPROCS=4 c/u, RSS pico 23–30 MB); wall por carril 44–58 min |
| Reanudación | no fue necesaria (0 reintentos, 0 fallos); receipts COMPLETE por ítem en `runs/t1-L{1,2,3}` |

Ventana elegida tras validar cobertura una vez (mandato §6): all13 sigue NOT_READY; el export NQZ5 tiene micro-huecos de apertura dominical (sep/oct) y Thanksgiving sin overrides del calendario funcional que impiden ventanas mayores; **no existe un año continuo usable** — esta ventana es la carencia declarada, no «un año».

## Resultado por configuración (USD; mismo intervalo, campañas independientes)

| Config | Operaciones (fills) | Entradas admitidas | Rechazos por sizing | stage_net | best_day | Compras+renovación | Cobros | Caja final | Conciliado |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| K01-r2300 | 0 | 0 | 31 | 0,00 | 0,00 | 240 | 0 | 4.760,00 | ✓ |
| K01-r3000 | 0 | 0 | 31 | 0,00 | 0,00 | 240 | 0 | 4.760,00 | ✓ |
| K02-r2300 | 36 | 18 | 18 | −1.984,64 | +875,04 | 240 | 0 | 4.760,00 | ✓ |
| K02-r3000 | 36 | 18 | 18 | −1.984,64 | +875,04 | 240 | 0 | 4.760,00 | ✓ |
| K03-r2300 | 14 | 7 | 29 | **+690,14** | +680,04 | 240 | 0 | 4.760,00 | ✓ |
| K03-r3000 | 14 | 7 | 29 | **+690,14** | 680,04 | 240 | 0 | 4.760,00 | ✓ |
| K04-r2300 | 2 | 1 | 30 | −499,98 | 0,00 | 240 | 0 | 4.760,00 | ✓ |
| K04-r3000 | 2 | 1 | 30 | −499,98 | 0,00 | 240 | 0 | 4.760,00 | ✓ |
| K05-r2300 | 12 | 6 | 29 | −979,88 | 0,00 | 240 | 0 | 4.760,00 | ✓ |
| K05-r3000 | 12 | 6 | 29 | −979,88 | 0,00 | 240 | 0 | 4.760,00 | ✓ |

Lecturas de contabilidad: caja final = 5.000 − 120 compra inicial − 120 renovación del escenario (día 30) + 0 cobros; caja mínima = final (monótona salvo los dos débitos). stage_net es el PnL neto retenido de la cuenta (ya neto de comisiones y slippage del modelo: fee 2,49/contrato/lado, slippage 1 tick); **no es caja del Owner** y no se vuelve a descontar. Los pares r2300/r3000 son idénticos por diseño: el objetivo de retiro solo gobierna la fase funded y ninguna cuenta llegó a ella — el aislamiento de configuraciones se sostiene (el eje retiro no contamina la evaluación).

## Mecánica observada

- **K01 frente a K02** (250/250 vs 500/500): K01 no operó ni una vez — con SL=1×ATR (ρ=1) el riesgo por contrato superó 250 USD en los 31 cruces diurnos del mes (`TG_SIZE_BELOW_MINIMUM`, sin ninguna excepción). K02 operó 18 ciclos: es el único perfil que completó el objetivo diario 870 algún día (best_day +875,04) y aun así cerró −1.984,64: los días malos (stops a 500 con ρ=1 y ATR alto) dominaron. Mayor frecuencia ≠ mejor caja.
- **K02/K03/K04** (techo R500, T 500/333/250): a igual techo de riesgo, K03 (ρ 3:2) fue la única positiva (+690,14 con 7 entradas); K04 (ρ 2:1) solo cupo una vez en el mes (1 entrada, stop −499,98) y K02 perdió. El TP corto de K03 cobró donde el TP largo de K02 devolvió.
- **K04 frente a K05** (500/250 vs 1000/250): R mayor no compró frecuencia: K05 cupo 6 veces (−979,88) y K04 una (−499,98); el riesgo 4:1 por contrato con presupuesto 1.000 rechazó 29 de 35 cruces por sizing. Ninguna de las dos se acercó a caja.
- **Motivos de no llegar a 870/día**: sizing inviable (dominante en K01/K03/K04/K05) y pérdidas de ciclo; ningún fallo de reglas (0 brechas DLL/floor/ladder en las diez campañas), ningún burn de cuenta (1 cuenta por campaña, las diez ELIGIBLE/PAUSED_SESSION al horizonte), ninguna pausa por −1.000 diaria.
- **Rachas/percentiles por operación**: la proyección compacta del lote no retiene trazas por operación; lo durable por campaña son los conteos y estados arriba. Si el Owner quiere mediana/rachas por operación, el siguiente corte puede habilitar la retención compacta de fills por operación (nota de producto, no ejecutada).

## Recursos

Wall por carril 44:03 (L2, 3 campañas) y 58:20 (L1, 4 campañas); RSS pico 23 MB; salida durable ~1 MB por campaña (límite 256 MiB/lote); disco reservado ≥8 GiB verificado antes de cada lanzamiento; temporales propios limpiados tras verificar receipts. Comparación de regresión A vs B del mismo árbol de pruebas: **sets de fallos idénticos** (5 tests preexistentes/ambientales en el freeze A) — el delta B no introduce regresiones.

## Dictamen

- **Ninguna configuración de esta muestra es útil para el objetivo de caja**: 0 cobros en 10 campañas continuas de ~31 sesiones; ninguna evaluación aprobó. Probabilidad de cobro: **no estimable con esta muestra** (n=1 campaña por configuración, sin cohortes independientes).
- K03 es la menos mala (única caja positiva de cuenta, +690,14 retenidos no cobrados); esa diferencia está en la cuenta, no en la caja del Owner — se reporta, no se disfraza.
- El resultado dominante del mes fue el sizing inviable (162 de 253 cruces diurnos rechazados entre las diez): la geometría SL=ρ×ATR con presupuestos ≤1.000 queda fuera del rango de volatilidad real de NQ 1m buena parte del tiempo. Esto es un hecho de la muestra, no una recomendación de ampliar presupuestos.
- Conclusión de muestra: **resultado insuficiente para recomendar campaña**; el trabajo de profundización sigue el criterio congelado del plan (abajo).

## Profundización T1-L (criterio fijado antes de ver resultados)

Caja neta de campaña empatada (4.760,00 las diez) → desempate por tiempo al primer crédito (ninguno acreditó) → **ID estable: K01 y K02**, ambos retiros (4 configuraciones) sobre el tramo reservado fuera de muestra **2025-11-30 → 2025-12-15** (validate-catalog COMPLETE, 11 sesiones, 14.040 minutos, 0 huecos; fijado y validado antes de cerrar T1). La diferencia entre el criterio frozen (K01/K02) y la menos mala por stage_net (K03) queda explícita: K03 no se profundiza porque el criterio de selección es la caja de campaña, no el PnL de cuenta. Reporte y límites en [[TRADESGERARD-B-RESULTADO]].
