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
created: "2026-10-12"
updated: "2026-10-12"
---

# TRADESGERARD-CONTROL

## Propósito

Fuente única de estado de la etapa A del mandato GOD LOCAL del Owner, recibido el 2026-10-12. Estado técnico: **READY_FOR_GLM**. Implementación y verificación independiente material de §10 completas sobre la identidad congelada de abajo. Aceptación final del Owner pendiente; manager y proyecto permanecen abiertos. GLM-5.3-Flash no fue lanzado.

## Contenido

### Autoridad y límites

[[TRADESGERARD-MANDATE-SNAPSHOT]] autoriza desarrollo offline por TOPs, verificación independiente y correcciones. El manager coordinó, adjudicó evidencia y documentó; no escribió ni integró código, scripts de producto ni tests. Sin merge productivo, deploy, servicios, egress de trading, compras/resets reales ni reconstrucción de cuentas personales. BTG-PLAN, BTX-PERF y D1–D6 conservan sus gates históricos.

Inputs preservados: caja inicial USD 5.000, compra individual USD 120 a demanda, reinversión sólo de efectivo acreditado, una cuenta y una operación agregada ejecutando, turno persistente. Evaluación con target ordinario USD 870 netos y pausa −USD 1.000 sin reset; fallo oficial previo prevalece. NY flat/cancelado al cierre. Funded no hereda 870 ni consistencia de evaluación. Retiros brutos 2.250/2.300/2.500/3.000. Sin límite vitalicio de 41 cuentas ni horizonte fijo de dos semanas.

### Entrega aceptada técnicamente

| Entrega | Estado | Evidencia |
|---|---|---|
| Contrato, propietarios y frontera A/B | COMPLETE | [[TRADESGERARD-CONTRACT]]; SDD en el repo de desarrollo. |
| Perfil GAU50 versionado | COMPLETE_WITH_EXPLICIT_SCENARIOS | [[TRADESGERARD-PROP-PROFILE]] distingue hechos oficiales, supuestos y UNKNOWN; no certificación comercial. |
| Catálogo finito | VERIFIED_FOR_B_IMPLEMENTATION | `catalog.json` único, design-2, 53 IDs / 44 habilitados / 8 retirados / NY-OPEN inactivo. 23.040 tuplas, 7.680 incompatibles, 192 alias y 15.168 únicas compatibles; baseline 3. Toolkit integrado: 53 checks PASS y Python 119/121 = 98,347%. Ninguna variante B ejecutada. |
| Motor y composición | IMPLEMENTED_AND_VERIFIED | Cuentas preservadas, caja/cobros, relojes, turnos, reglas por fase, Strategy/MM alternativo por API, protecciones económicas y drenaje físico. |
| Salida y lote | IMPLEMENTED_AND_VERIFIED | Paridad compacta/detallada, límites, integridad y fallos durables; reanudación sólo de completos idénticos. |
| Verificación independiente §10 | PASS_MATERIAL_CONTRACT | `evidence/recheck/CANDIDATE-RECHECK.md`; pruebas propias y regresiones sobre el freeze exacto. F01/F02/F03 resueltos; ningún gap material ni defecto nuevo identificado. |
| Cobertura Go nueva ≥95% | VERIFIED | 1349/1420 = 95,000%, 20 perfiles PASS compatibles por SHA/coordenadas, 108 fuentes instrumentadas; baseline separado, sin paths excluidos. Auditor reprodujo el conteo; no se afirma que su propia selección produzca por sí sola ese 95%. |
| Manual, recetas y handoff | COMPLETE | Manual existente `v3/backtester/README.md`; `evidence/recheck/RECIPES.md`, comandos ejecutados y [[TRADESGERARD-EVIDENCE-A]]. |
| Prompt maestro GLM | PREPARED_NOT_LAUNCHED | [[TRADESGERARD-GLM-MASTER]]; lanzamiento manual del Owner. |

### Identidad exacta

Repo `xKoRx/echo`; rama `codex/tradesgerard-platform-a`; checkout relativo a ARANEA_ROOT: `work/tradesgerard-platform-a-20261012/echo`. Baseline `873f5f1c7df25086271af1de1896095f1cade2a9`. Source entregado: **`d752b3e124386330e6f8e4b270958cc2db892734`**.

Binario relativo a ARANEA_ROOT: `work/tradesgerard-platform-a-20261012/evidence/corrector/bin/echo-backtest`. SHA256 **`8abe7379483e4845f3e6f16167ac3a3d4db630d6b42b600542f4ca739fcc98ff`**; Go1.27.1 linux/amd64, VCS idéntico, modified=false. Manager corroboró HEAD limpio y hash antes/después; auditor comparó 1.359 archivos Go sin cambios durante el carril. Código local de desarrollo, sin push/merge/release productivo afirmados.

SDD `specs/FEAT-TRADESGERARD-PLATFORM-A/`. Único cambio de test heredado aprobado por TCR: literal INTRADAY_TRAILING→UNKNOWN_TRAILING en el caso de variante desconocida; asserts intactos. Tests nuevos y correcciones están identificados en los commits y manifests.

### Alcance de la evidencia y adjudicaciones

Publicación remota solicitada explícitamente por el Owner después de la entrega: rama `codex/tradesgerard-platform-a` pusheada a `git@github.com:xKoRx/echo.git` y verificada por `git ls-remote` en `d752b3e124386330e6f8e4b270958cc2db892734`. Acceso para revisión: https://github.com/xKoRx/echo/tree/codex/tradesgerard-platform-a . Push de la rama de desarrollo, sin merge ni release. Los recibos externos a Git conservan sus referencias locales.

El recheck independiente demostró compra/caja/reinversión >41, turnos sin solapamiento, pausas, calendarios y cuentas inactivas/DST, pase exacto/negativo30%, cuatro targets/cap5000/fees/latencias, terminalidad, composición/aislamiento, causalidad, disco/lote y regresiones. Smoke real NQZ5: cuatro fills, neto −109,96; BASIC/replay IDENTICAL 94.798 registros. Fixtures son prueba del motor, no rentabilidad.

El caso de piso antes de −1000 se acepta por readback físico ligado a source/binario: cuenta efectivamente seleccionada 50360→49860, pérdida diaria −500, piso50000 y fallo TRAILING_DRAWDOWN. El test que suponía account0 conserva rc1; no se declara suite PASS. Un probe adicional de parcial combinado con breach quedó NOT_DEMONSTRATED por su fixture; las capacidades materiales se demostraron mediante parciales/finality públicos, breach long/short público y contratos SDK de reducción/reservas. No se traslada un gap de A a B ni se oculta ese límite.

Los agregados históricos con timeout siguen NOT_PASS. La cobertura final sólo usa perfiles PASS compatibles; el denominador histórico1425 mezclaba versiones y fue reemplazado por recálculo auditado baseline→freeze, preservando recibo y mapa. [[TRADESGERARD-EVIDENCE-A]] conserva primeras causas, alcance y referencias físicas.

### Recursos y cierre del carril

Un escritor y un carril de build/pruebas/campaña, GOMAXPROCS=4 y Go -p1. Reserva ≥8 GiB, scratch ≤2 GiB, durable por lote/corrida ≤256 MiB, logs ≤16 MiB. Antes del último bloque CLI/replay se fijó prospectivamente presupuesto agregado de auditoría de 384 MiB; no cambió el límite del lote ni se borró historia.

Recibo final independiente: propios 113.355.152 bytes, archivo agregado 261.178.223 bytes, libres 10.214.326.272 bytes, scratch final0, logs100.820 bytes y procesos propios0. Picos observados cada0,25s: scratch133.103.985 bytes, durable113.846.479 bytes, RSS441.664 KiB; reserva mínima10.123.841.536 bytes. Son máximos muestreados. Binarios, corpus, caches y temporales históricos sin atribución permanecieron intactos; no se afirma cleanup histórico total.

Todos los TOPs terminaron sus shots; solicitado `gpt-6.1-sol`, servido UNKNOWN. Corrector y auditor liberaron explícitamente el carril. No se consumió CLOUD Pro ni se asumió disponibilidad de GLM en este harness. Agents-OS se mantuvo en master con autosync observado, sin atribuir sus commits/push al manager.

### Siguiente acción y alcance B

El Owner puede lanzar manualmente [[TRADESGERARD-GLM-MASTER]] con esta identidad y las recetas verificadas. B debe IMPLEMENTAR la Strategy TradesGerard, indicadores y todas las políticas/variantes vigentes; verificar baseline3, enumerar y ejecutar todas las combinaciones compatibles con continuidad, validar y rankear caja/cobros. No recibe reconstrucción estructural pendiente de scheduler/accounting/lifecycle/recorder.

all13 sigue NOT_READY por gaps/prefijos; nuevas ventanas requieren validación prospectiva. Los UNKNOWN comerciales siguen explícitos. READY_FOR_GLM es readiness técnico, no aceptación del Owner, autorización LIVE ni prueba de rentabilidad. No se ejecuta feedback ni cierre de sesión del manager sin petición explícita.

### Estado B — KISS-1 gobierna (GLM LOCAL, 2026-10-12)

El Owner lanzó el mandato KISS-1 (GLM-5.3-Flash, superficie LOCAL) y reemplaza la selección experimental del prompt maestro anterior: **el catálogo `catalog.json` design-2 (15.168 combinaciones) queda HISTÓRICO** — no es orden vigente de implementación; se conserva por Git/referencia con sus 53 IDs fuente y ninguna variante B del catálogo se ejecuta. La investigación vigente es la selección finita de KISS-1: 5 perfiles económicos {K01 250/250, K02 500/500, K03 500/1000÷3, K04 500/250, K05 1000/250} × {retiro2300, retiro3000} = **10 configuraciones por ventana**; iteración1 con salida fija (sin adds, sin Gerard, sin progresiones, sin BE/extensión), señal SIG-B sobre cierres 1m (estocástico lookback20, K lenta SMA3, cruce 20/80 consumido una vez), geometría TP 1×ATR / SL ρ×ATR, horario de diseño A (entradas 10:00–15:50 NY, liquidación desde 15:50, flat antes 15:55), remanente T=min(Tref, pendiente del objetivo) con R proporcional. I1 terminada el 2026-10-13: T0 COMPLETE, T1 10/10 y T1-L 4/4 conciliadas sobre NQZ5 validado (0 huecos) con **0 cobros y ninguna evaluación aprobada** — ninguna configuración recomienda campaña con este frozen; K03 menos mala (+690,14 de cuenta, no caja). Defectos B corregidos con commits `67ec0099`+`10d406b3` (binario `f00efd66…`), regresión A≡B verificada. Dictamen, higiene y pendientes I2: [[TRADESGERARD-B-RESULTADO]]. Plan, tandas y estado: [[TRADESGERARD-B-PLAN]].

### Reparación de entradas — 2026-10-13

IN_PROGRESS bajo el mandato GOD LOCAL: [[TRADESGERARD-ENTRY-REPAIR]] es el único informe de reparación KISS-1. B físico preservado `10d406b3cddbd9c738dbc64b5db38c16ff7527b9`, binario `f00efd668eee8b121f7efb65b1b92923620e47beaac650a99491b425027486e8`. C2 congelado `63fb24996d422f3dfee28e706ad1528eb948bff8`, binario `8eff860eca8db7d2aaf84e40903b0de4e03f367aad798a79d2c371bf1ecf8f50`, supera gate independiente funcional/oráculo/cobertura sobre identidades exactas:42969 barras/755 oportunidades NY, sin divergencias de indicadores, regresiones permanentes y rearme/finality/compra acreditados. C1 recuperó K01 corto0→3 y largo0→85, pero su compra indebida al vencer pausa lo deja REFERENCE_ONLY; C2 corrige esa frontera. Diez planes finales sellados; comparación10/10 y casos largos pertinentes pendientes antes de CORRECTED_AND_VERIFIED. T1/T1-L conservan COMPLETE histórico; ENTRY-REPAIR-C01 marca afectada la explicación de frecuencia/denominadores de I1. Design-2 permanece histórico; no se activan I2 ni nuevos parámetros ni LIVE.

V-F02 confirmado después del gate acotado C2: al reanudar sesión se conserva indebidamente el turno de una cuenta posterior. Reproducción pública independiente de dos días RED y subcaso payout2300 B PASS/C2 FAIL, sin modificar asserts ni horizonte. C2 supersedido y drenado. C3 `26f3459cba47fd05f5ef9aed3d205c3c5bbad81a`, binario `92e27ef71d22bc9897af7f3c26d1fbe980f5f591b749224258747fd40c2584c9`, corrige turno y pasa los cuatro pagos/lifecycle/regresiones, gate independiente exacto y CLI singleton; manager comprobó identidad. Comparación final2/10 COMPLETE y verificadas: K01r2300 de0 a19 operaciones y K02r2300 de18 a53, con755 cruces por configuración conciliados. K01 queda luego limitado por margen EOD15,28 inferior al mínimo físico/costos NQ19,98; una posible política de indisponibilidad económica persistente se propone separadamente y no se aplica. K03/K04 y B observado K01 continúan, comparación completa pendiente. Detalle y recibos en [[TRADESGERARD-ENTRY-REPAIR]].

## Fuentes

- [[TRADESGERARD-MANDATE-SNAPSHOT]], §§10–12; [[TRADESGERARD-CONTRACT]]; [[TRADESGERARD-EVIDENCE-A]].
- `evidence/recheck/{CANDIDATE-RECHECK.md,VERIFY-END.json,FINAL-RESOURCES.json,PROCESS-CLEANUP.json,closeout-metadata.json,RECIPES.md}` relativos al workspace de la iniciativa.
- [[Echo Futures]] y `xKoRx/echo:v3/backtester/README.md`.
