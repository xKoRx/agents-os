---
type: skill
schema_version: 1
name: echo-retester-master
description: Gatea el desarrollo y backtesting de cada nueva estrategia o variante de Echo Futures, impidiendo históricos largos antes de correctness, smoke individual, rollover y al menos un challenge aprobado en un contrato trimestral comprobado. Cargar al implementar/validar nuevas estrategias para Echo Futures, ClutiFX o cursos futuros; no para operar LIVE ni analizar únicamente campañas ya terminadas.
scope: area
created: "2026-10-24"
updated: "2026-10-27"
entities:
  - "[[Echo Futures]]"
related:
  - "[[Echo I+D — Futures]]"
  - "[[30-resources/runbooks/echo-rnd-cycle-runbook]]"
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
  - tech/agents-os
  - tech/backtester
  - action/validate
---

# echo-retester-master

## Purpose

Gobernar **cada identidad nueva** de Strategy/variante/MM que deba evaluarse con Echo Futures: primero corregir e instrumentar; después demostrar actividad y un pase físico en un contrato trimestral; sólo entonces autorizar cómputo del histórico completo. Esta skill es el criterio y el selector de gates. El runbook enlazado contiene ejecución, artefactos, recibos y recuperación.

**Activar:** creación/importación/revisión de señales y variantes para futuros en Echo Futures, incluidos ClutiFX, investigación propia y cursos posteriores. **No activar:** investigación Forex/CFD (derivar a `imox-strategy-research`), sólo consulta retrospectiva, optimización de infraestructura sin estrategias, despliegue o trading LIVE. No suplanta a `agents-os-bootstrap`, `e2e-gated-validation` ni las reglas económicas del Owner.

La gestión permanente y la selección del siguiente trabajo pertenecen a [[Echo I+D — Futures]]; esta skill gobierna desarrollo, conformidad y cualificación técnica/económica de las identidades despachadas. **Alcance de ejecución vigente: NQ.** Otros instrumentos requieren decisión Owner y contratos/datos propios antes de ejecutar. Los ejemplos E2T/GAU50 son escenarios históricos versionados, no cuentas actuales del Owner ni proveedor universal; cada mandato identifica su ProviderRuleSet/AccountPolicy efectivo y autorizado.

## Minimal Read

1. Esta skill y `30-resources/runbooks/echo-futures-strategy-qualification-runbook.md`.
2. [[Echo I+D — Futures]], planner único del trabajo despachado, catálogo/matriz aprobada de la fuente y contratos vigentes de [[Echo Futures]] Strategy/MM/Provider; lectura por delta. Optimización de Campañas conserva sus entregas, recibos y laboratorio, no sustituye al manager de mercado.
3. Sólo los comandos reales del checkout/corpus/supervisor afectados; nunca inventar CLI ni recargar la historia del proyecto.

## Procedure

1. **Congelar universo e identidades.** Distinguir `strategy_id` (señal), `variant_id` (lógica) y `profile_id` (MM). Catálogo finito; etiquetas SOURCE/OP/HIP; ninguna expansión cartesiana ni perfiles no autorizados. Deduplicar únicamente equivalencias de señales demostradas, manteniendo trazabilidad de IDs.
2. **Declarar dataset y contrato de prueba antes del primer motor.** Elegir el contrato trimestral físico más reciente con cobertura efectiva suficiente (objetivo ~3 meses, mínimo operacional 45 sesiones elegibles de mercado con datos y warmup causal); preferir el último disponible si cumple. Si el último es incompleto, identificar el contrato trimestral completo inmediatamente anterior y declarar el fallback. Si ninguno califica, `DATA_REQUIRED`, jamás sustituir por un histórico multicontrato encubierto.
3. **Gatear CADA identidad en orden estricto:** `G0 IMPLEMENTED` → `G1 CORRECTNESS_PASS` → `G2 LAST-CONTRACT` (split `G2A readiness/signals` · `G2B SESSION_COMPATIBILITY` · `G2C FULL-TRADE LIFECYCLE`) → `G3 ROLLOVER_READINESS_PASS` → `G4 QUARTER_PASS` → `G5 FULL_HIST_ELIGIBLE`. Cada variante ejecutable pasa individualmente por el último contrato físico NQ disponible (un solo contrato, sin concatenar); el PASS de otra variante no satisface un gate ajeno. G2C exige al menos **una operación completa real y conciliada** en ese contrato: apertura ejecutada → posición registrada → cierre ejecutado → resultado conciliado con la identidad de la operación conservada (≥1 fill de entrada, ≥1 fill de salida, ≥1 round-trip reconstruido desde los fills); no basta orden enviada, orden rechazada ni entrada sin cierre. No exige que gane: debe informar win/loss/break-even. Los detalles y evidencias exigibles son los del runbook.
4. **Distinguir corrección técnica de descubrimiento comercial.** `ready=0`, ventanas incongruentes, ausencia de triggers, warmup perpetuo o desvío del contrato ⇒ `FAILED_CORRECTNESS`; localizar el primer eslabón causal, arreglar y repetir el gate afectado. `ready>0` con cero señales ⇒ probar setup positivo y predicados reales; si es genuinamente raro, no inventar entradas. El funnel por transición (datos→barras→requirements→evaluaciones→detectores→oportunidades→señales→sesión→cuenta→MM→proveedor→órdenes→fills→lifecycle→ledger→reconciliación) se registra con cantidades, rechazos y motivo: **todo cero relevante tiene explicación verificable**. Cada transición rechazada se correlaciona por `SignalID`, jamás por la razón predominante del día. Una variante que no opera NO termina como `0 trades` sin diagnóstico: el runbook posee la tabla causal (nunca-ready / ready-sin-oportunidades / oportunidades-sin-señales / señales-fuera-de-sesión / señal-sin-fill / entrada-sin-cierre / roundtrips-perdedores / trimestre-sin-pase) y la clasificación persistente correspondiente.
5. **Aplicar el gate económico trimestral del Owner.** Una identidad sólo corre el trimestre si superó G0–G3 **con G2C PASS propio** y compatibilidad de sesión (G2B `SESSION_COMPATIBLE`); la admisión del quarter es fail-closed y valida esa cadena desde la identidad de ejecución sellada (`execution_purpose`, `strategy_id`, `variant_id`, `profile_id`, `contract_set`, `window_identity`, `plan_digest`, `build_digest`, `qualification_receipt`) — jamás desde etiquetas de `tier` del propio job ni desde duraciones arbitrarias. Un horizonte multicontrato corto es `HISTORICAL` por conjunto de contratos, no por días. Sobre el **contrato trimestral calificado** la promoción exige ≥1 `CHALLENGE_PASSED` físico con compras/fills/cierres/costos conciliados y todos los gates técnicos PASS; cero pases ⇒ `QUARTER_NO_PASS`, no se ejecuta G5. Las campañas bit-idénticas ya ejecutadas no se repiten: su recibo existente prueba que la campaña ya corrió. Una aprobación en tres meses es filtro de costo, NO certificación de calidad ni probabilidad futura. **Cero pases exige la auditoría de factibilidad del runbook (§6): demostrar con números del motor si la causa es `MATHEMATICALLY_UNREACHABLE_WITH_OBSERVED_TRADES` (estrategia que opera pero no puede aprobar: frecuencia × ganador-techo < target) o `NEGATIVE_EDGE` (muestra perdedora), más el funnel de frecuencia y el control de defecto común con baseline existente — una estrategia que opera no es una estrategia capaz de aprobar, y distinguirlo es parte del veredicto, no un extra.**
6. **Usar presupuesto por gate y concurrencia controlada.** Antes del G4 no correr DEV de cientos de sesiones ni histórico 2023–2026. En G4/G5 usar el supervisor único existente con techo **global** de seis motores (incluidos oráculos), objetivo cinco-seis cuando RAM/PSI/swap lo permitan; cancelar nuevas admisiones ante presión. Cero OOM y cero procesos huérfanos prevalecen sobre mantener seis.
7. **Habilitar G5 sólo por evidencia verificable en la cola.** Una fila sin recibo G0–G4 propio, o cuyo SHA de Strategy/variante/MM/build/políticas difiera, falla cerrada antes de `prepare/run/resume`. El dataset del trimestre y el histórico SON corpus diferentes por diseño: verificar cada SHA contra su propio manifiesto y exigir compatibilidad demostrada de fuente/calendario/roll/semántica de mercado; nunca exigir hashes iguales de ventanas distintas. Reejecutar sólo resultados invalidados por cambio semántico; no mezclar bytes de versiones.
8. **Terminar con decisión completa por identidad.** La clasificación final de investigación es exactamente una de: `QUALIFIED_LAST_CONTRACT` (operación completa real y conciliada con gates funcionales PASS — jamás una variante sin round-trip propio), `NEEDS_ITERATION`, `SOURCE_REVIEW_REQUIRED`, `VALID_RARE_NO_ACTIVITY`, `SESSION_INCOMPATIBLE`, `BLOCKED_SPEC`, `BLOCKED_DATA`, `ENGINE_DEFECT`, `ALIAS_VERIFIED`, `QUARTER_NO_PASS`, `PROMOTED_FOR_HIST`. Los gates y la clasificación son dimensiones distintas: el ledger conserva ambas, sin etiquetar un bloqueo de conocimiento como pérdida comercial. Cuando la lógica no puede validarse y la fuente es la duda, emitir una ficha del Knowledge Review Loop (`CLF-KNOWLEDGE-REVIEW-QUEUE.md`: una entrada por problema material, con claim/frame IDs, comportamiento esperado vs implementado, primera divergencia causal, causa raíz, pregunta concreta al Owner y objetivo de revisión de video; timestamp no recuperable ⇒ `NOT_RESOLVED`, jamás inventado; `RETEST_SCOPE` jamás el histórico completo por defecto). Separa además ranking retrospectivo, familias distintas, frecuencia, economía y aceptación Owner.
9. **Persistir y cerrar según instrucción del Owner.** Registrar avance en planner, agent-run y change_log; feedback event-driven. Entregar el resultado al manager de mercado para actualizar su celda de cobertura y elegir la siguiente investigación. Mejorar esta skill mediante el ciclo de [[30-resources/runbooks/echo-rnd-cycle-runbook]]: fricción o contraejemplo real, delta acotado, validación y trazabilidad; cambios de gates, presupuestos, reglas económicas o autonomía requieren decisión Owner. Si se solicitó cierre de sesión, ejecutar `agents-os-session-close`. No prometer vigilancia autónoma ni habilitar LIVE.

### Conformidad teoría → regla → código → ejecución

G1 debe demostrar que cada regla material tiene fuente o hipótesis declarada, operacionalización determinista, predicado efectivo y evidencia positiva/contraejemplo. Separar obligación, opción, contexto e incertidumbre; no atribuir al instructor un MM experimental propio. La configuración debe llegar al gate que decide la señal: serializar un parámetro no prueba que el eje esté activo. Verificar causalidad en `decision_time`, trigger, dirección, invalidación, stop técnico, filtros, expiración y cierre. Una duda material de especificación se conserva como `BLOCKED_SPEC` o `SOURCE_REVIEW_REQUIRED`, sin adaptar la teoría retrospectivamente al código.

G2 añade a sus recibos una revisión trazable de entradas, no-entradas y cierres contra esa especificación. Elegir la muestra por reglas predeclaradas que cubran casos y límites de la lógica, no por rentabilidad; conservar `SignalID`, valores de predicados, órdenes, fills y cierre. Un replay, tabla o gráfico anotado puede ayudar a inspeccionar; la prueba sigue siendo determinista y conciliada. Los fixtures prueban lógica, el último contrato prueba comportamiento físico y G4 prueba el filtro económico trimestral: ninguna evidencia sustituye a la otra ni exige ganar en G1/G2.

El procedimiento y los artefactos de conformidad se detallan en G1/G2 del runbook existente; no crear otra cadena de gates. El campo de salida heredado `QUARTER_FUNDED` informa la economía del quarter `CHALLENGE_ONLY`: no acredita supervivencia funded ni retiros, que deben evaluarse explícitamente en el mandato económico aplicable.

## Output

```text
QUALIFICATION: <dataset/contrato/fechas/sesiones reales + last-contract físico>
CATALOG: <IDs de matriz / identidades ejecutables / implementadas / aliases / blocked_spec / blocked_data>
PER_IDENTITY_GATES: <G0 G1 G2A G2B G2C G3 G4 G5 + receipt/hash/rationale>
LAST_CONTRACT_FUNNEL: <por identidad: evaluaciones/ready/oportunidades/señales/sesión/admisiones/órdenes/entry-fills/exit-fills/roundtrips/open@horizonte>
CLASSIFICATION: <un veredicto final por identidad del vocabulario de decisión>
QUARTER_FUNDED: <passed challenge/purchased/operaciones/dias activos/costo>
FULL_HISTORY_AUTHORIZED: <lista exacta de ids con gate PASS; vacía si 0 pases>
FULL_HISTORY_FORBIDDEN: <lista exacta de ids + causa>
KNOWLEDGE_REVIEW: <fichas emitidas con REVIEW_ID y claim IDs>
RESOURCES: <concurrencia global/RSS/MemAvailable/PSI/swap/OOM>
OWNER_ACCEPTANCE: REVIEW
AGENTS_OS: <planner/run/feedback/close>
```

## Hard Rules

- **Prohibido G5 antes de G4 PASS propio**, y **prohibido G4 sin cadena funcional propia con G2C PASS** (≥1 operación completa conciliada en el último contrato), incluso cuando otra variante comparte módulo/Strategy.
- **Prohibido DEV largo como sustituto del contrato trimestral**; los canarios de rollover son breves, no 444 sesiones.
- No relajar setup, filtros, stops, riesgo, reglas de prop ni calendario sólo para obtener un pase. Toda hipótesis nueva requiere versión declarada y nueva evidencia; cambiar parámetros conservando identidad está prohibido.
- Nunca declarar PASS por `exit=0`, `COMPLETE` vacío, promedio diario alto o compra sin `CHALLENGE_PASSED`; una variante sin operación completa no puede recibir `QUALIFIED_LAST_CONTRACT`.
- No contar variantes de MM como estrategias independientes; tampoco descartar sin diagnóstico una variante con cero operaciones. Alias sólo con equivalencia demostrada (`ALIAS_VERIFIED`), no por compartir StrategySpec.
- Un gate `FAIL`, `INCONCLUSIVE`, `DATA_REQUIRED` o no ejecutado bloquea los posteriores. Resultados previos se preservan y se reutilizan mientras su identidad y versiones sigan válidas; las campañas bit-idénticas ya verificadas no se re-ejecutan.
- Sin órdenes reales, deploy, cambios de ProviderRuleSet ni workstreams vecinos. Los bloqueos ajenos quedan documentados, no maquillados. No modificar conocimiento fuente para justificar una implementación.
