---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[TRADESGERARD-B-PLAN]]"
  - "[[TRADESGERARD-CONTROL]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-12"
updated: "2026-10-12"
---

# TRADESGERARD-B-T0

## Propósito

Reporte de la tanda T0 KISS-1: implementación del módulo B (señal SIG-B + gestión económica), pruebas críticas y smoke sobre datos reales. Resultado: **T0 COMPLETE** — el módulo opera de extremo a extremo sobre la plataforma A con economía coherente; un PnL negativo del smoke no afecta la habilitación de T1.

## Identidad

| Elemento | Valor |
|---|---|
| Base | `xKoRx/echo` @ `d752b3e1` (freeze A, rama `codex/tradesgerard-platform-a`) |
| Checkout B | `ARANEA_ROOT/work/tradesgerard-b-glm-20261012/echo`, rama local `codex/tradesgerard-b-glm` (sin push) |
| Commit B | `67ec0099d1c66781e57350275d5ba042446ade84` (14 archivos, +2615/−10) |
| Binario B | SHA256 `60accecc00fe40383fec7b737a7102092bcbd0d6566043ef117a2616b90c4fed`, go1.27.1 linux/amd64, vcs.revision=67ec0099, modified=false |
| Toolchain | go1.27.1 instalada en el host, verificada en build (`go version -m`) |
| Perfil comercial | `E2T_GAU50_PURCHASE_GE_20260706_OBS_20261012_SCENARIO_V1` de A, sin cambios |

## Composición pública implementada

- **Strategy `tg`** (`v3/sdk/futures/strategies/tg`, spec `TRADESGERARD_SIG_B_V1`): estocástico lookback 20 sobre cierres 1m, %K lenta SMA3 (D SMA3 informativa), LONG cuando previa <20 y actual ≥20, SHORT cuando previa >80 y actual ≤80; cada cruce se consume una vez; rango high=low → %K=50 neutro; reset determinista ante cambio de contrato; ATR20 Wilder (semilla SMA de 20 TR + recursión (19p+x)/20) transportado como TechnicalStop = cierre ∓ ρ×ATR alineado a tick conservador; horario de diseño A sobre el boundary de cierre en America/New_York: entradas [10:00,15:50), liquidación CLOSE_ALL una vez por día en [15:50,15:55), plano en ≥15:55 (cutoff del proveedor); `WarmupReadiness` (anillo 26 barras, ATR sembrado, recursión de %K lenta completa) y `CycleAware`.
- **MM `tgmm`** (`v3/sdk/futures/strategies/tgmm`): presupuestos R/T racionales exactos por configuración; T efectivo = min(Tref, remanente del objetivo aplicable) — evaluación: min(870 − PnL del día, 3000 − progreso de etapa); funded: retiro configurado − progreso elegible; R = T×ρ (ρ=Rref/Tref ≥ 1, nunca invertido); tope de headroom real (pausa interna 1000, DailyLoss del RuleSet, headroom duro entregado) con reducción proporcional que conserva ρ; sizing entero desde la geometría SL=ρ×ATR / TP=1×ATR neta de costos declarados (fee 2,49/contrato/lado, slippage 1 tick), acotado por el ladder del RuleSet; tras el fill, precios económicos SL/TP recalculados desde las primitivas compartidas del ciclo (promedio FIFO, costos debitados, costos de salida estimados) con redondeo conservador a tick; presupuestos congelados en MMState (una operación abierta nunca recalcula importes); salida fija únicamente: sin adds, sin BE, sin extensión (intento de add declinado con diagnóstico `TG_ADD_NOT_IN_ITERATION1`); re-plan de aplanado idempotente bajo terminación pendiente.
- **Registro en composición compartida** (`config`): `ModuleTG` y `MMModuleTG`; `TGMMDef` validada fail-closed (racional exacto, ρ ≥ 1, retiro ∈ {2300,3000}, sin bloques de scaling/plans de GerardMM); la CLI resuelve el par registrado con factories cero (`REGISTERED_CONFIG_V1`).
- **Proyección de economía del backtester** (propietario, dos puntos): las views y la entrega ACCOUNT_ECONOMICS del day-roll transportan la instantánea completa de la revisión (balance/equity/stage/best-day), igual que la observación de fills/quotes — el MM decide con la misma autoridad que publicó el ledger.

## Pruebas críticas (mandato §8, mínimos cubiertos)

Oráculo de indicadores (ATR Wilder y %K contra serie a mano, replay byte-idéntico); cruce LONG/SHORT y consumo único sin re-emisión dentro de banda; warmup sin señales y readiness honesta; high=low neutro; reset por cambio de stream; ventanas de sesión (bloqueo 09:59, primera entrada 10:00, CLOSE_ALL único 15:50, nada ≥15:55, rearme por día); geometría del stop técnico (K03 3/2 exacto, alineación conservadora); sizing y presupuestos: referencia, remanente 330 con Tref 500, K03 racional exacto (T=1000/3, R=500), K05 headroom proporcional, sin headroom, funded con remanente de retiro; fail-closed de entrada (ruleset, geometría, economía stale/sin balance, marca, objetivo cumplido, cantidad mínima); precios económicos post-fill LONG/SHORT con redondeo conservador (pérdida ≤ R, ganancia ≥ T); presupuestos congelados ante recálculo posterior; TP por net liquidation con cancelación y salida; señales de gestión (CLOSE cierra, OPEN declinado); ladder por bandas; validación de configuración (ρ<1, retiro 2250 rechazado, sin TG block, scaling con tgmm rechazado); resolución registrada en composición con factories cero; E2E de plataforma registrado en sintético: cruce → entrada dimensionada → stop económico → salida por objetivo → liquidación 15:50 del ciclo siguiente → plano, caja conciliada, cero adds. Cobertura nueva: `tg` 96,6%, `tgmm` 95,3% (piso 95% cumplido en código nuevo).

## Smoke sobre datos reales (NQZ5, ventana recheck de A)

Ventana de A ya validada (2025-10-28, warmup desde 2025-10-13), descriptor y corpus exactos del recheck; prepare/batch por la CLI pública (`platform-prepare` + `platform-batch`, `REGISTERED_CONFIG_V1`), campaña K02/retiro2300.

| Dato | Valor |
|---|---|
| Recibo | `runs/t0-smoke-final2/62a242640ebafe6d29b3d105207c2f3bdcee4b1361e14ce8bd35a59db331417a`, state COMPLETE, attempt 1, sin reintentos |
| Ejecución | COMPLETE, `HORIZON_CENSORED`, conciliado=true |
| Operación | LONG 1 NQZ5 @ 26042,00 (10:28 NY); stop económico 26017,50 (= entrada − R500/20 + costos, al tick); stop disparado a 26017,25 a las 14:41Z |
| Economía | stage_net −499,98 USD (pérdida dentro del presupuesto R=500); cuenta ELIGIBLE, sin fallo de reglas; caja 4880 USD (compra única de 120), sin pagos |
| Recursos | wall 4:32, RSS pico 22,8 MB, directorio del lote 95 KB (límites 256 MiB/16 MiB sobradamente cumplidos) |
| Limpieza | scratch propio del batch drenado por el ejecutor; corpus, binarios y evidencias A intactos |

Se probaron además dos corridas previas del mismo smoke durante el desarrollo (receipts `7ab07bf1…` y `c2d9e3ce…` en `runs/t0-smoke-k02-r2300` y `runs/t0-smoke-diag`): documentan el diagnóstico de dos defectos reales corregidos (entrega de day-roll sin balance; re-plan de terminación), conservados como evidencia de causa.

## Regresión

Comparación A vs B del mismo árbol de pruebas en curso de ejecución (sets de fallos ambientales preexistentes en A: postgres, telemetry, y tres tests de futuresvertical que fallan también en el freeze A). Resultado final de esta comparación se registra en [[TRADESGERARD-B-T1]]; los paquetes afectados por el delta (config, tg, tgmm, futuresvertical paridad, backtester plataforma) pasan en B.

## Límites

El smoke no certifica rentabilidad ni ejecución física; los fixtures sintéticos prueban el motor. El perfil comercial conserva los UNKNOWN de A. Sin push, merge ni release: rama local de desarrollo.
