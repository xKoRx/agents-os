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

### Continuidad de tandas

T0 políticas y racha → T1 F0×10 → T2 F1×10 → T3 F2×10 → T4 F3×10 → clasificación de40configuraciones y ampliación disponible de hasta cuatro configuraciones activas. Hallazgos materiales se corrigen y las trayectorias afectadas se repiten. No hay garantía de cobro; cobro acreditado y caja neta se informan por separado.

## Fuentes

- Mandato Owner TRADESGERARD — GOD LOCAL: OPERABILIDAD, CAMPAÑAS Y FILTROS KISS, PROMPT_VERSION1,2026-10-13.
- [[TRADESGERARD-ENTRY-REPAIR]], [[TRADESGERARD-CONTROL]], [[TRADESGERARD-B-PLAN]], [[TRADESGERARD-PROP-PROFILE]].
- Recepción física manager: Git HEAD/status, sha256sum, df y free; dispatch local y acuse del integrador en la sesión activa.
