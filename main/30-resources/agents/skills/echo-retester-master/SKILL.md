---
type: skill
schema_version: 1
name: echo-retester-master
description: Gatea el desarrollo y backtesting de cada nueva estrategia o variante de Echo Futures, impidiendo históricos largos antes de correctness, smoke individual, rollover y al menos un challenge aprobado en un contrato trimestral comprobado. Cargar al implementar/validar nuevas estrategias para Echo Futures, ClutiFX o cursos futuros; no para operar LIVE ni analizar únicamente campañas ya terminadas.
scope: area
created: "2026-10-24"
updated: "2026-10-24"
entities:
  - "[[Echo Futures]]"
related:
  - "[[30-resources/runbooks/echo-futures-strategy-qualification-runbook]]"
  - "[[30-resources/agents/skills/e2e-gated-validation/SKILL]]"
  - "[[30-resources/agents/skills/release-certification/SKILL]]"
aliases:
  - echo-retester-master
  - echo strategy research gates
  - qualification first backtesting
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/area
  - area/echo
  - tech/backtester
  - action/validate
---

# echo-retester-master

## Purpose

Gobernar **cada identidad nueva** de Strategy/variante/MM que deba evaluarse con Echo Futures: primero corregir e instrumentar; después demostrar actividad y un pase físico en un contrato trimestral; sólo entonces autorizar cómputo del histórico completo. Esta skill es el criterio y el selector de gates. El runbook enlazado contiene ejecución, artefactos, recibos y recuperación.

**Activar:** creación/importación/revisión de señales y variantes para futuros o Forex en Echo Futures, incluidos ClutiFX y cursos posteriores. **No activar:** sólo consulta retrospectiva, optimización de infraestructura sin estrategias, despliegue o trading LIVE. No suplanta a `agents-os-bootstrap`, `e2e-gated-validation` ni las reglas económicas del Owner.

## Minimal Read

1. Esta skill y `30-resources/runbooks/echo-futures-strategy-qualification-runbook.md`.
2. Planner activo de [[Echo Futures]], catálogo/matriz aprobada de la fuente y contratos vigentes Strategy/MM/Provider; lectura por delta.
3. Sólo los comandos reales del checkout/corpus/supervisor afectados; nunca inventar CLI ni recargar la historia del proyecto.

## Procedure

1. **Congelar universo e identidades.** Distinguir `strategy_id` (señal), `variant_id` (lógica) y `profile_id` (MM). Catálogo finito; etiquetas SOURCE/OP/HIP; ninguna expansión cartesiana ni perfiles no autorizados. Deduplicar únicamente equivalencias de señales demostradas, manteniendo trazabilidad de IDs.
2. **Declarar dataset y contrato de prueba antes del primer motor.** Elegir el contrato trimestral físico más reciente con cobertura efectiva suficiente (objetivo ~3 meses, mínimo operacional 45 sesiones elegibles de mercado con datos y warmup causal); preferir el último disponible si cumple. Si el último es incompleto, identificar el contrato trimestral completo inmediatamente anterior y declarar el fallback. Si ninguno califica, `DATA_REQUIRED`, jamás sustituir por un histórico multicontrato encubierto.
3. **Gatear CADA identidad en orden estricto:** `G0 IMPLEMENTED` → `G1 CORRECTNESS_PASS` → `G2 INDIVIDUAL_SMOKE_PASS` → `G3 ROLLOVER_READINESS_PASS` → `G4 QUARTER_PASS` → `G5 FULL_HIST_ELIGIBLE`. Los detalles y evidencias exigibles son los del runbook. Un resultado heredado de otra variante no satisface un gate.
4. **Distinguir corrección técnica de descubrimiento comercial.** `ready=0`, ventanas incongruentes, ausencia de triggers, warmup perpetuo o desvío del contrato ⇒ `FAILED_CORRECTNESS`; localizar el primer eslabón causal, arreglar y repetir el gate afectado. `ready>0` con cero señales ⇒ probar setup positivo y predicados reales; si es genuinamente raro, `LOW_FREQUENCY`, no inventar entradas.
5. **Aplicar el gate económico trimestral del Owner.** Una identidad sólo pasa a histórico si sobre el **contrato trimestral calificado** produce ≥1 `CHALLENGE_PASSED` físico, con compras/fills/cierres/costos conciliados y todos los gates técnicos PASS. Cero pases ⇒ `QUARTER_NO_PASS`, no se ejecuta G5. No computar señales, cuentas pendientes ni proyecciones como pase. Una aprobación en tres meses es filtro de costo, NO certificación de calidad ni probabilidad futura.
6. **Usar presupuesto por gate y concurrencia controlada.** Antes del G4 no correr DEV de cientos de sesiones ni histórico 2023–2026. En G4/G5 usar el supervisor único existente con techo **global** de seis motores (incluidos oráculos), objetivo cinco-seis cuando RAM/PSI/swap lo permitan; cancelar nuevas admisiones ante presión. Cero OOM y cero procesos huérfanos prevalecen sobre mantener seis.
7. **Habilitar G5 sólo por evidencia verificable en la cola.** Una fila sin recibo G0–G4 propio, o cuyo SHA de Strategy/variante/MM/build/dataset difiera, falla cerrada antes de `prepare/run/resume`. Reejecutar sólo resultados invalidados por cambio semántico; no mezclar bytes de versiones.
8. **Terminar con decisión completa por identidad.** `PROMOTED_FOR_HIST`, `NO_PROMOTE_LOW_ACTIVITY`, `NO_PROMOTE_NO_PASS`, `FAILED_CORRECTNESS`, `DATA_REQUIRED` o `BLOCKED_ENGINE`, más prueba/causa. Separar ranking retrospectivo, familias distintas, frecuencia, economía y aceptación Owner.
9. **Persistir y cerrar según instrucción del Owner.** Registrar avance en planner, agent-run y change_log; feedback event-driven. Si se solicitó cierre de sesión, ejecutar `agents-os-session-close`. No prometer vigilancia autónoma ni habilitar LIVE.

## Output

```text
QUALIFICATION: <dataset/contrato/fechas/sesiones reales>
CATALOG: <identidades declaradas/implementadas/aliases/data-blocked>
PER_IDENTITY_GATES: <G0 G1 G2 G3 G4 G5 + receipt/hash/rationale>
QUARTER_FUNDED: <passed challenge/purchased/operaciones/dias activos/costo>
FULL_HISTORY_AUTHORIZED: <lista exacta de ids con gate PASS>
FULL_HISTORY_FORBIDDEN: <lista exacta de ids + causa>
RESOURCES: <concurrencia global/RSS/MemAvailable/PSI/swap/OOM>
OWNER_ACCEPTANCE: REVIEW
AGENTS_OS: <planner/run/feedback/close>
```

## Hard Rules

- **Prohibido G5 antes de G4 PASS propio**, incluso cuando otra variante comparte módulo/Strategy.
- **Prohibido DEV largo como sustituto del contrato trimestral**; los canarios de rollover son breves, no 444 sesiones.
- No relajar setup, filtros, stops, riesgo, reglas de prop ni calendario sólo para obtener un pase. Toda hipótesis nueva requiere versión declarada y nueva evidencia.
- Nunca declarar PASS por `exit=0`, `COMPLETE` vacío, promedio diario alto o compra sin `CHALLENGE_PASSED`.
- No contar variantes de MM como estrategias independientes; tampoco descartar sin diagnóstico una variante con cero operaciones.
- Un gate `FAIL`, `INCONCLUSIVE`, `DATA_REQUIRED` o no ejecutado bloquea los posteriores. Resultados previos se preservan.
- Sin órdenes reales, deploy, cambios de ProviderRuleSet ni workstreams vecinos. Los bloqueos ajenos quedan documentados, no maquillados.
