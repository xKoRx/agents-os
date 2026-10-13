---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[TRADESGERARD-B-T1]]"
  - "[[TRADESGERARD-B-RESULTADO]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-13"
updated: "2026-10-13"
---

# TRADESGERARD-B-T1-L

## Propósito

Profundización de la iteración 1 según el criterio congelado en [[TRADESGERARD-B-PLAN]] antes de ver resultados. Resultado: **T1-L COMPLETE 4/4**, fuera de muestra, **sin cobros y sin mejora del signo**.

## Selección (criterio frozen, aplicado sin cambios)

Caja neta de campaña empatada en T1 (4.760,00 las diez) → desempate por tiempo al primer crédito (ninguna campaña acreditó) → **ID estable: K01 y K02**, ambos retiros (4 configuraciones, máximo respetado). La menos mala por PnL de cuenta era K03; el criterio declarado es la caja de campaña y no se cambió tras ver resultados — la diferencia queda reportada en [[TRADESGERARD-B-T1]].

## Horizonte real y su límite

«Hasta tres años» no existe con este corpus: el export NQZ5 cubre 2025-09→2025-12 con huecos estructurales (aperturas dominicales faltantes y Thanksgiving sin overrides del calendario funcional) y all13 sigue NOT_READY. El tramo reservado ejecutado es **2025-11-30 → 2025-12-15** (validate-catalog COMPLETE: 11 sesiones, 14.040 minutos abiertos, 0 huecos; fijado y validado antes de cerrar T1). No hay segmento de selección dentro de esta ventana: la configuración llegó congelada desde T1. **No es validación independiente completa**: comparte instrumento, mes adyacente y régimen de mercado con la ventana de T1; su valor es comprobar trayectoria congelada fuera del intervalo de selección, con potencia estadística nula (n=1 campaña por configuración).

## Resultado por configuración (USD)

| Config | Operaciones (fills) | Entradas | Rechazos sizing | stage_net | best_day | Cobros | Caja final | Conciliado |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| K01-r2300 | 0 | 0 | 10 | 0,00 | 0,00 | 0 | 4.880,00 | ✓ |
| K01-r3000 | 0 | 0 | 10 | 0,00 | 0,00 | 0 | 4.880,00 | ✓ |
| K02-r2300 | 20 | 10 | 3 | −1.714,80 | +505,02 | 0 | 4.880,00 | ✓ |
| K02-r3000 | 20 | 10 | 3 | −1.714,80 | +505,02 | 0 | 4.880,00 | ✓ |

Caja final 4.880,00 = 5.000 − 120 compra (sin renovación: la ventana es menor a 30 días). K01 confirma su comportamiento determinista (0 operaciones: el sizing R250/ρ1 jamás cupo — 10 de 10 cruces rechazados). K02 mantiene fuera de muestra el signo negativo de T1 (−1.714,80 en 10 ciclos). Ninguna brecha de reglas, ningún burn, 0 cobros.

## Recursos

Wall 13:23 para las 4 campañas (1 carril), RSS pico 20,6 MB, salida durable < 1 MB por campaña, receipts COMPLETE en `runs/t1l-reserve`, sin reintentos.
