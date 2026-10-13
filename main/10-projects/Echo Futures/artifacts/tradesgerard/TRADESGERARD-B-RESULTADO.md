---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[TRADESGERARD-B-PLAN]]"
  - "[[TRADESGERARD-B-T0]]"
  - "[[TRADESGERARD-B-T1]]"
  - "[[TRADESGERARD-B-T1L]]"
  - "[[TRADESGERARD-CONTROL]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-13"
updated: "2026-10-13"
---

# TRADESGERARD-B-RESULTADO

## Propósito

Resultado final de la iteración 1 KISS-1 (I1) con su profundización T1-L, y las decisiones pendientes del Owner para activar I2. **Dictamen: ninguna configuración de la tabla frozen deja evidencia suficiente para recomendar campaña con objetivo de caja.**

## Estado de I1 (definición de terminado, mandato §11)

| Requisito | Estado |
|---|---|
| Código y configuración reproducibles | ✓ commits `67ec0099` + `10d406b3`, binario `f00efd66…c4fed`, planes sellados por campaña, replay y batch identity del motor de A |
| Estados de las diez configuraciones | ✓ 10/10 COMPLETE (T1) + 4/4 COMPLETE (T1-L), todas conciliadas, 0 reintentos |
| Reportes T0/T1/T1-L | ✓ [[TRADESGERARD-B-T0]], [[TRADESGERARD-B-T1]], [[TRADESGERARD-B-T1L]] |
| Higiene verificada | ✓ receipts durable, temporales propios limpiados tras verificar entrega, disco con reserva, corpus/binarios/evidencias A intactos |
| Continuidad de I2 | ✓ pendientes formulados abajo (PENDING_OWNER_RULE, no implementados) |
| Cobertura de datos | Carencia declarada: ventana continua máxima 2025-10-13→11-25 (~31 sesiones) + tramo reservado 11-30→12-15; no existe año continuo usable en el corpus entregado |

## Resultado económico consolidado (campañas completas, todas conciliadas)

| Tanda | Configs | Cobros acreditados | Cajas finales | stage_net por perfil |
|---|---:|---:|---|---|
| T1 (10/10) | K01–K05 × 2 retiros | **0** | 4.760,00 todas | K01 0 (sin operaciones); K02 −1.984,64; K03 +690,14; K04 −499,98; K05 −979,88 |
| T1-L (4/4, fuera de muestra) | K01, K02 × 2 retiros | **0** | 4.880,00 todas | K01 0 (sin operaciones); K02 −1.714,80 |

- **Ninguna cuenta aprobó evaluación** (objetivo 3.000) ni cobró; los dos ejes de retiro (2.300/3.000) nunca se activaron. Probabilidad de cobro: **no estimable con esta muestra** (n=1 campaña por configuración; las cuentas dentro de una campaña no son cohortes independientes).
- La caja del Owner nunca estuvo en riesgo de ruina: peor path consumió compra+renovación (240) por campaña; el resto del stage_net negativo vive en la cuenta simulada, no en caja.
- Comparaciones pedidas: K01<K02 en actividad (0 vs 18 entradas: el sizing decide); K03>K02>K04 en caja de cuenta a igual techo 500 (el TP corto 3:2 cobró donde el 1:1 devolvió); K05 no compró frecuencia con más riesgo (6 entradas, −979,88). Mejor día individual +875,04 (K02) muestra que el objetivo diario 870 es alcanzable con este motor; el mes completo lo invierte.

## Qué respalda la conclusión y qué no

Respalda: 14 campañas continuas exactas y conciliadas sobre datos reales validados sin huecos, motor con paridad A + regresión A≡B, causes de rechazo por configuración, y un tramo fuera de muestra congelado. **No respalda**: generalizar a otros regímenes de mercado, a horizontes mayores ni a probabilidad de cobro; el corpus no da para más (carencia declarada, no silenciada). Un mes desfavorable de K02/T1-L no «prueba» que K02 pierde siempre; tampoco K03 «es rentable»: es la menos mala de la muestra y así se reporta.

## Pendientes I2 — decisión del Owner (PENDING_OWNER_RULE, nada implementado)

1. **Add B2**: definir X (velas cerradas antes del add), el rango del estocástico que debe conservarse tras la entrada, y el límite de repeticiones del add. Sin estos tres números I2-add no se implementa.
2. **Validación del movimiento / salida anticipada**: definir el criterio exacto de «no se confirma, salir» (qué observa la salida y en cuántas velas).
3. **BE y extensión** (+200 → BE, 500 → extensión): confirmar si entran a I2 como salidas explícitas y su temporalidad única de comparación.
4. **Evidencia nueva para la decisión (hecho, no propuesta de matriz)**: en esta muestra el sizing con SL=ρ×ATR y presupuestos ≤1.000 quedó fuera de rango en 162 de 253 cruces diurnos (K01 100% del mes sin operar). Cualquier I2 que quiera medir gestión sobre más cruces necesita primero que el Owner decida si los presupuestos/geometría frozen se mantienen (y se acepta la baja frecuencia) o se ajustan por versión.
5. **Datos**: si se quiere horizonte mayor (~1 año+), hace falta corpus nuevo validado prospectivamente (all13 sigue NOT_READY por huecos estructurales); una campaña nueva de descarga/reconstrucción no está autorizada por este mandato.

## Continuidad

El carril B queda liberado: procesos propios terminados y verificados, receipts en `ARANEA_ROOT/work/tradesgerard-b-glm-20261012/runs/`, rama local `codex/tradesgerard-b-glm` (sin push/merge/release), freeze A intacto. Feedback de sesión y cierre de Agents-OS: solo por pedido explícito del Owner.
