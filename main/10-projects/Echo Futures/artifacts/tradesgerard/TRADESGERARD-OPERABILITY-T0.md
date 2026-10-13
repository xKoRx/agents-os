---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[TRADESGERARD-CONTROL]]"
  - "[[TRADESGERARD-ENTRY-REPAIR]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-13"
updated: "2026-10-13"
---

# TRADESGERARD-OPERABILITY-T0

## Propósito

Recibir C4 y verificar el cambio prospectivo de operabilidad del mandato GOD LOCAL del Owner, PROMPT_VERSION1, 2026-10-13. T0 es técnico; no acredita rentabilidad. Estado inicial **IN_PROGRESS**.

## Contenido

### Recepción y dispatch

C4 source `88ed70d1ff9910bb157f1c14c0fed1d2b8e7ec49`, árbol limpio comprobado con Git; SHA256 físico del binario `c8849bb6e5523e8625ead8282f0d97f98d8b02e14d72838e3c35de207c6bcd57`. Checkout relativo a ARANEA_ROOT: `work/tradesgerard-entry-repair-20261013/implementer/echo-c4`. La evidencia final C4 acredita diez campañas completas; bitácoras anteriores no se convierten en pendientes actuales. C4 y sus resultados se preservan.

TOP LOCAL implementador único `/root/operability_integrator`; TOP LOCAL verificador `/root/operability_verifier`. Modelo solicitado `gpt-6.1-sol`, servido UNKNOWN. Dispatch real mediante subagentes de esta sesión, sin nuevo manager ni dependencia GLM. El integrador recibió el delta de mínimo económico y retiro EOD; el verificador recibió primero la reconstrucción por operación de la racha K05, seguida de falsación independiente exacta. Sus entregas aún no constituyen gate aprobado.

Nueva evidencia relativa a ARANEA_ROOT: `work/tradesgerard-operability-20261013/{implementer,verifier}`. CONTROL pertenece al manager; cada worker conserva un informe propio. Escrituras canónicas por materializador y sincronización separada de su mera existencia local.

### Hallazgo K05 entregado

[[TRADESGERARD-OPERABILITY-K05-STREAK]] reconstruye doce operaciones desde C4 físico: sin pérdidas previas; once ganancias cuenta1=2495,22 y faltante504,78, una ganancia cuenta2=260,04. La racha agregada2755,26 cruza dos cuentas de evaluación; no existe pase/pago omitido en ese corte. El cambio proviene de pausa diaria y compra causal siguiente cruce. Caja4520 y neto de ledger−279,46 conciliados por separado. Readback manager y sync remoto `5ef845ce923d37e7025c506f54756f659663eba2`; la barrera TP económica postfill no retenida queda como límite de evidencia, sin inferirla del neto.

### Recursos y fronteras vigentes

Lectura física inicial del manager:13.190.447.104 bytes libres y aproximadamente62.612MiB de memoria available. Son observaciones puntuales. Se mantienen reserva disco≥8GiB, scratch agregado≤2GiB, lote≤256MiB y traza/log≤16MiB. Presupuesto agregado nuevo, dependencias, perfil, inputs y request real se fijan en el recibo del integrador antes de ejecutar; no se hereda un presupuesto por cambiar carpeta.

Sólo trabajo offline aislado. Ningún resultado económico nuevo todavía. No LIVE, cambios de servicios/permisos, operaciones reales ni promoción productiva. Aceptación final del Owner separada; el mandato permite continuar automáticamente entre las tandas acotadas después de su verificación técnica.

### Finding independiente en desarrollo — cap residual

El verificador identificó en `xKoRx/echo:v3/backtester/platform_campaign.go`, working tree T0, que `maybeRequest` todavía recorta `PayoutTarget` al remanente del cap. Ejemplos:3000→2000 después de un pago3000, o2300→400 después de4600. El mandato nuevo exige conservar el objetivo2300/3000 y no presentar un cobro menor como logro. Manager adjudicó corrección acotada del contrato nuevo, preservando C4; reproducer determinista independiente y corrección/gate pendientes. No es una pérdida de trading ni un resultado de las cuarenta campañas.

### Candidato T0 y HOLD del mínimo ejecutable

Candidato congelado `87e33b0c333a1f2f4178dfefe06126d50691c7ad`, limpio comprobado por manager. Cobertura de desarrollo `CONSERVATIVE_DIFF_BLOCKS_V1`:115/120=95,8333%, bloques Go completos que intersectan líneas productivas añadidas/reemplazadas; no cobertura AST ni global. Primer overlay independiente SDK PASS, pero no habilita T1 por sí solo.

Manager cuestionó que `MinimumExecutableRisk` añadiera un tick a los costos prefill y retirara una cuenta con margen15,28 al calcular19,98. Verificador inspeccionó el adapter: no acredita una distancia mínima de un tick desde mark. Ejemplo algebraico por falsar causalmente: fill LONG100,25, stop100, costos pendientes9,98 produce pérdida proyectada14,98≤15,28. Integrador reconoce que el tick adicional era un supuesto suyo, no restricción probada; se conserva el candidato y sus resultados como diagnóstico, sin campañas T1. Prueba Venue/Provider/reservas/fill/protección real y corrección acotada pendientes; no se modifica el simulador para sostener el supuesto. El mínimo definitivo deberá derivarse del contrato ejecutable y sus costos, sin hardcode ni afirmación de legalidad de broker.

### Adjudicación física del mínimo — V-MIN

Pruebas independientes conservadas sobre87e33b0c: Venue12casos LONG/SHORT×offset0/1×precio posterior sin cambio/favorable/adverso, PASS0,007s; ProviderRisk+Ledger20casos, PASS0,639s. Con spread cero y slippage1tick por lado, salida estática neta−14,98; con offsets bid1/ask1 del descriptor C4,−24,98. No son garantías frente a movimiento/slippage. Con C4 y margen15,28, la equity tras entrada cae a47997,79 frente piso48000: breach antes de protección. Con19,98, entrada todavía válida pero salida estática deja47995 y breach. Igualdad24,98 termina exactamente en48000 y activa regla de piso hit-inclusive;25,28 deja48000,30. La igualdad de presupuesto admite riesgo de fallo al stop; no se la transforma automáticamente en cuenta permanentemente perdida si la orden y una oportunidad causal son válidas.

Se rechaza el fundamento anterior tick-extra como mínimo legal demostrado. Integrador corrige desde el descriptor/costos estructurales, sin alterar el matching C4 ni endurecer el adapter. `implementer/echo-t0-corrected`, rama `codex/tradesgerard-operability-correction-20261013`, nace del candidato87; anterior quieto. El presupuesto nuevo único incluye ambos checkouts. Los probes Provider/Ledger no incluyen por sí solos Operation admission; la verificación final exigirá ese seam real además de los casos unitarios.

La prueba independiente de retiro/demanda finalmente PASS0,949s tras usar `nextNYOpen` real; fallos previos eran fixtures fuera de sesión y quedan registrados, no bugs de producto. Claims y matriz cap4casos PASS. Evidencia relativa a nuevo root: `verifier/{venue-minimum-87e33b0c-attempt2.log,provider-minimum-87e33b0c.log,backtester-demand-87e33b0c-attempt6.log}`. Gate T1 continúa HOLD hasta freeze corregido y recheck exacto.

### Freeze V2 y finding de valoración stale en callback

Source corregido `cb9cc0cd997e78bbf7f777a5291482b6c9870bfd`, árbol limpio comprobado; binario `implementer/bin/echo-backtest-c2` SHA256 `34a300eecabf3baa55519fc6322cb1b524161c2c9471a8602742231c7e407a45`, hash físico leído. Políticas `ECONOMIC_MINIMUM_V2` y `ECONOMIC_MINIMUM_RETIRE_V2`; perfil comercial y horizon C4 preservados. Delta cobertura177/181=97,790055% bloques completos; SDK, money/policy/NT físico, Core typed LIVE/BACKTEST offline y vet del autor PASS. No certificación de LIVE ni gate independiente final.

E2E independiente V2: seis negativos LONG/SHORT con R14,98/15,28/19,98 no generan fills. Al investigar positivos cercanos al mínimo, el verificador halló un defecto monetario: primer fill LONG14:01:06.666 a100,75 con cursor actual100,25, pero MM_FILL recibe equity50377,51 y Cycle.open_mark380/net_liquidation370,02 desde mark anterior119,75/cierre120. MM considera TP25,28 logrado y la salida siguiente a100 realiza−19,98. No se acepta como cierre inmediato legítimo; el supuesto de marca contemporánea está contradicho. Evidencia `verifier/e2e-cb9cc0cd/long-R25.28-trace.ndjson.gz` y resultado propio. Caso de fixture, no PnL del ranking; aún no se extrapola a todas las campañas C4.

Manager adjudicó HOLD y corrección upstream acotada de valoración/autoridad antes de callback, con reproducción de atribución y RED/GREEN en el mismo assert. No guard compensatorio TG, no alterar retrospectivamente fills/precios ni simulador para fabricar resultado. Original cb9 debe permanecer quieto; integrador único y verificador independientes continúan. T1 todavía no lanzada.

### Atribución de la valoración stale a C4

Verificador ejecutó el mismo assert monetario sobre C4 `88ed70d1`, con política nueva OFF, TGMM real resuelto por su factory y presupuesto500 que permite cantidad ATR. RED exit1 en2,027s para LONG y SHORT: OpenMark380/net370,02 publicados frente a OpenMark−15/net−24,98 exigidos por la cotización causal. `verifier/fill-authority-C4-red-attempt2.log` y resultados/traces correspondientes conservados. Primer intento usó un constructor legacy y no abrió operaciones; se conserva como error propio de harness, no evidencia del defecto.

La raíz preexistente omite marcar ledger en `processNativeStep`/`markNative` cuando está flat con entrada working antes del matching. Integrador corrige sólo la autoridad upstream incluyendo obligaciones pendientes; debe conservar guards de cuenta/contrato y ausencia de efectos cuando no hay inventario ni orden. Los resultados C4 se conservan como observados; la propiedad general de valoración contemporánea tras fill tiene un contraejemplo. Esto no demuestra que todas sus755oportunidades o todos sus netos estén errados. F0 nuevo incluirá este fix además de políticas mínima/retirada; no se atribuirá toda diferencia a una única causa ni se inventará PnL contrafactual.

### Tandas autorizadas por ejecutar

T0 políticas y racha → T1 F0×10 → T2 F1×10 → T3 F2×10 → T4 F3×10 → clasificación de40configuraciones y ampliación disponible de hasta cuatro configuraciones activas. Hallazgos materiales se corrigen y las trayectorias afectadas se repiten. No hay garantía de cobro; cobro acreditado y caja neta se informan por separado.

## Fuentes

- Mandato Owner TRADESGERARD — GOD LOCAL: OPERABILIDAD, CAMPAÑAS Y FILTROS KISS, PROMPT_VERSION1,2026-10-13.
- [[TRADESGERARD-ENTRY-REPAIR]], [[TRADESGERARD-CONTROL]], [[TRADESGERARD-B-PLAN]], [[TRADESGERARD-PROP-PROFILE]].
- Recepción física manager: Git HEAD/status, sha256sum, df y free; dispatch local y acuse del integrador en la sesión activa.
