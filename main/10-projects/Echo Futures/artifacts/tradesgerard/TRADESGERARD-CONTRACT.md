---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[TRADESGERARD-CONTROL]]"
  - "[[TRADESGERARD-PROP-PROFILE]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-12"
updated: "2026-10-12"
---

# TRADESGERARD-CONTRACT

## Propósito

Fijar la frontera técnica A/B y el mapa de propietarios, sin duplicar el manual público ni el estado de iniciativa. Source de desarrollo: repo `xKoRx/echo`, rama `codex/tradesgerard-platform-a`, baseline `873f5f1c7df25086271af1de1896095f1cade2a9`. Contratos ejecutables de desarrollo: `specs/FEAT-TRADESGERARD-PLATFORM-A/{SPEC,PLAN,TASKS}.md` en ese repo. Especificación/plan aprobados por el manager para desarrollo interno mediante la autorización expresa del mandato; gate final Owner separado.

## Contenido

### Capacidad, propietario, delta y consumidor

| Capacidad | Propietario inspeccionado | Reutilización / delta A | Prueba requerida | Consumidor B |
|---|---|---|---|---|
| Feed/causalidad/calendario | backtester driver/OHLC scheduler + SDK bars/analytics/calendar/simexecution | Reusar OHLC_CAUSAL_PATH_V2, separar NY de día prop | Cero hindsight, DST/cutoff/flat | SIG-B, NY, EXIT |
| Composición | SDK config/composition; backtester compose/compose_account | Fábricas públicas ya existentes; carrier de configuración sólo si hace falta | Strategy/MM deterministas distintos, estado aislado | Todas las políticas TradesGerard |
| Compartimentos | compose_account/seedAccountAuthorities | Conservar autoridades ledger/MM/provider/operation/venue al cambiar turno; ReplaceAccount legacy preservado | Suspender/reanudar sin reseed, sin órdenes físicas compartidas | ROT, FUND |
| Caja/ciclo campaña | campaign/cashBook exacto | Nuevo controlador secuencial multicuenta y obligaciones; no ledger de trades paralelo | Compra120 única, cobro acreditado, espera≠ruina, horizonte | PAY/SEQ/FUND |
| Reglas/pase | SDK provider/domain RuleSet/ProgramTerms | GAU50 versionado por fase, ladder/cupos |30% igualdad negativo, primer día no bloquea, piso antes de pausa | SEQ/RISK/ADD |
| Pausa interna | Context/operation/campaign policy |870 y−1000 independientes de fail/reset | Conservación financiera/historial y relojes inactivos | DAY/FIT |
| Cantidades y protecciones | SDK operation/MMInput/claims/accounting | Reusar cancel+new, no modify-price atómico; ampliar seam sólo si necesario | Partial/pending/late/reject, SL y TP económicos, BE costos | DYN/EXIT/RISK |
| Indicadores | SDK bars/analytics/strategies | Infraestructura compartida existente; ATR/estocástico concretos B | Fórmula/seed/warmup/discontinuidad de B | SIG-B/VOL |
| Salida | Recorder/history/resultwriter/artifactstore | Proyección compacta desde inicio y límites/failure receipt | Paridad economía, readback, cleanup propio/faults | Matriz completa |
| Lotes | CLI pública | Plan finito, identidad exacta, progreso y resume | Cambios invalidan skip, fallidos visibles | Matriz completa |
| Legacy | BASIC/CAMPAIGN/reproduce | Mantener defaults/esquemas y replay histórico | Regresión afectada ligada al SHA nuevo | Baseline verificable |

### Decisiones de integración

Un único feed y evolución causal de Strategy/analytics. Cada cuenta conserva su compartimento autoritativo; la selección no reinicia mercado ni consume otra vez una señal. Cambiar turno exige ausencia física de exposición y órdenes ejecutables, no sólo estado lógico cerrado. Los timers de todas las cuentas siguen avanzando. El controlador administra caja personal, admisión y obligaciones; el ledger SDK sigue siendo dueño del dinero negociado.

El perfil comercial se versiona por condición de compra, independientemente de la fecha del histórico de mercado. Los UNKNOWN externos se convierten sólo en escenarios nombrados/configurados; no hechos. Pasar evaluación no acredita caja. Activación, solicitud, aprobación, procesamiento y crédito son etapas distintas. El cierre LiveSim al cap se declara explícito; Live nunca hereda silenciosamente EOD ni omite costos.

Stage A entrega seams reales probados para qty/add/SLTP/BE, no la estrategia ganadora. Stage B implementa la señal TradesGerard, ATR20/estocástico20 con candidato3/3, sizing y todas las políticas del catálogo. GLM no recibe reconstrucción pendiente de scheduler/accounting/lifecycle/recorder disfrazada de variante.

### Catálogo y decisiones experimentales

Fuente editable única: `10-projects/Echo Futures/artifacts/tradesgerard/catalog.json` en Agents-OS. Las vistas generadas y planes de ejecución son derivados identificados por hash. Estado inicial DESIGN_PROPOSAL_UNIMPLEMENTED; ninguna variante ejecutada. Contiene los 53 IDs conservados, incluidos retirados y caso reglamentario negativo. Conteos iniciales del TOP están sujetos a auditoría independiente antes de congelar equivalencias.

Candidatos mínimos: un add de cantidad inicial a distancia25/50/75%; alpha1 sobre ganancia neta realizada positiva del día; bandaUSD10; ATR Wilder20 y K/D SMA3/3; entradas10:00–15:50NY, liquidación desde15:50 y flat antes15:55NY. Son decisiones de diseño prospectivas sustituibles por versión, no valores óptimos ni órdenes reales del Owner. NY-OPEN conserva propuesta inactiva; retiradas permanecen fuera.

### Recursos, corpus y evidencia

Un escritor y una campaña financiera a la vez; source estable durante build/medición. Reserve≥8GiB, temporales propios≤2GiB, durable≤256MiB, logs≤16MiB, GOMAXPROCS4. Limitar desde el productor, no escribir todas las trazas y borrarlas después ni trasladarlas enteras a RAM. Completar/drenar→guardar→leer/verificar/conciliar→limpiar sólo temporales propios; fallos también guardan estado/cause mínima.

Corpus derivado accesible: workspace Aranea `work/btx-perf-last-20261010/integrator/package/corpus`, con provenance de calendario e identidades físicas. Los originales del export tienen acceso denegado desde esta superficie, sin intento de ampliar permisos. all13 sigue NOT_READY por gaps/prefijos. Validar ventana nueva antes de smoke. Las ventanas históricas disponibles no son por sí solas una validación nueva ni un split experimental aceptado.

## Fuentes

- [[TRADESGERARD-MANDATE-SNAPSHOT]], [[TRADESGERARD-PROP-PROFILE]], [[TRADESGERARD-CONTROL]].
- TOP inventory: fuente y hashes inspeccionados, no builds/tests ejecutados. Manual leído blob `b66dacec9a0f6e0bc99ac13bde3a8e53cdb036e3`; binario histórico `49957b660e0a248cd03fc9f321461b8f8ae190856f1bd7740950807c475b64af` embebe source `48647d1ff9860bd4e1fff47e5fca7c9be273fb74`, no873.
- TOP catalog: JSON, generador y validación inicial; auditoría de equivalencias en curso. No resultados de mercado.
