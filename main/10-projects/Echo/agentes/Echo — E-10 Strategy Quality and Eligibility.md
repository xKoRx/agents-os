---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo — Live Platform V1]]"
sprint:
start: 2026-09-21
due:
progress: 0
repo: xKoRx/echo
jira:
prs:
aliases:
  - Echo E-10
  - E-10 Strategy Quality
  - Strategy Quality and eligibility
  - FEAT-STRATEGY-QUALITY-ELIGIBILITY-E10
tags:
  - kind/project
  - area/echo
  - agent/owner
created: "2026-09-21"
updated: "2026-09-21"
---

# Echo — E-10 Strategy Quality and Eligibility

%% Naming: Echo — E-10 Strategy Quality and Eligibility es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ Echo — E-10 Strategy Quality and Eligibility
> **Área:** [[Echo]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[Echo — Live Platform V1]] · **Repo:** `xKoRx/echo`
> Subproyecto de **implementación** de la fase E-10 / Strategy Quality and eligibility. No es Integration. El contrato WHAT vive en esta SPEC FREEZE y luego en el SPEC de Echo; esta nota es HOW / ORDER / GATES hasta que NORMAL materialice los docs en la branch.

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> Este proyecto es `owner: agent`. El padre [[Echo — Live Platform V1]] enlaza aquí. La supervisión humana del track live sigue en [[Echo — Producto Integrado]].

## 🎯 Objetivo

Medir Strategy Quality como observación forward Reference-only de una `StrategyVersion` sellada contra su `Expectation` sellada pre-forward, con coverage honesto como prerrequisito, DQ antes que economía, veredictos versionados con abstención como salida válida de primera clase, y `EligibilityDecision` emitida **sólo** con política de observación ratificada y resuelta (fail-closed sin ella). Principios: `EXPECTATION_SEALED_BEFORE_FORWARD`; `UNKNOWN ≠ INSUFFICIENT ≠ FAIL`; cobertura no es edge; nueva versión = evidencia nueva (reset); ausencia de datos ≠ rendimiento cero; SQ ≠ EF ≠ Forge fidelity. Unlock: el owner entiende la calidad real de la versión observada y E-11 recibe candidatos explícitos con abstención registrada (CASH si no hay evidencia).

## 📊 Estado actual

- **E10_PLANNING_FROZEN v1.0.0 (2026-09-21, sesión TOP documental; sin código):** SPEC FREEZE §📐 + PLAN §🗺️ + TASKS + VERIFICATION + NORMAL-PROMPT en esta nota. Migración **069 reservada exclusiva E-10** (disponibilidad verificada físicamente en el baseline: última migración existente = `068_strategy_version_forge_platform`). Branch proyectada `feature/e10-strategy-quality-eligibility` desde `d69e1ee3`; NORMAL no lanzado; gate = Manager review de esta planificación.
- **Baseline READ ONLY verificado:** `origin/feature/e09-execution-copy-reconciliation-fidelity` @ `d69e1ee35d95f84ddaec812a956f5837d799fbe3` (ls-remote 2026-09-21); `master` @ `5dd998f16aea7b2821f460188718d7a6d279829c` intacto. Verificación de identidad: worktree local @ `097e39eb767319801130be772de524e7e846e968` == SHA exacto contrastado por la decisión Manager C4, con delta `097e39eb→d69e1ee3` de 3 commits **exclusivamente tests/scripts/VERIFICATION.md** (11 archivos, evidencia C4) ⇒ el **source de producto** del baseline es idéntico al verificado localmente. Todos los contratos citados en §📐 fueron verificados file:symbol contra ese árbol.
- **Estados reconocidos (sin asumir observaciones inexistentes):** E-05 `CLOSED — SOFTWARE / INTEGRATED` @ master `5dd998f1`, migración 063 `APPLIED / VERIFIED` en DEV compartido, writer canónico + calculator frozen disponibles. E-06 source disponible en baseline (WP-A persistencia: migración 064 + stores `reference_binding/binding_lookup/reference_readback`, commits `429e5c03`/`c021983f`/`1614028b` del 2026-09-17); gates físicos independientes pendientes (G0 PASS / G1 `PROMOTION_SEAL_MISSING`, T21 blocked; sin binding `OBSERVING` real). E-07 `SOURCE/CONTRACT/PG PASS` + `MQL_COMPILE_PENDING` + `PHYSICAL_PENDING` (sin hechos reales de EA enriquecido). E-08/E-09 quedan **fuera del data-scope de E-10** (SQ ≠ EF): sus gates (`COVERAGE_GATE_PENDING`, `PHYSICAL_PENDING`, `ECONOMIC_ACTIVATION_PENDING`) **no bloquean E-10**.
- **Contrato de decisión Manager 2026-09-21 (E-09 C4):** E-10 planifica contra `d69e1ee3` READ ONLY, depende de E-05/E-06/E-07, **NO del cierre porcentual de E-09**. La arista E09→E10 del DAG maestro se interpreta como *interpretación conjunta de resultados y read surfaces* (unlock E-13/E-11), no como dependencia de datos: ninguna tabla 067 es input de E-10 (§📐 S11).
- **Precondiciones físicas de DEV compartido (registradas, no acción de este carril):** `echo-develop` tiene 063 aplicada; **064–068 NO aplicadas** (Environment Contract §5.2–§5.4; identidad parcial 061 existe por recovery E-04). La aplicación 064→069 por flujo de release es precondición de clase B/C (§🗺️), gated owner.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | `feature/e10-strategy-quality-eligibility` (proyectada; NORMAL la crea) | `d69e1ee3` (consolidada E-06/E-07/E-08/E-09/E-04; master `5dd998f1` intacto) | Esta nota §📐 SPEC FREEZE v1.0.0 → materializada como `specs/FEAT-STRATEGY-QUALITY-ELIGIBILITY-E10/SPEC.md` en T00 | `.../PLAN.md` + `.../TASKS.md` + `.../VERIFICATION.md` + `.../NORMAL-PROMPT.md` (mismos contenidos §🗺️/§✅/§🧪/§🚦) | E10_PLANNING_FROZEN v1.0.0 · NORMAL clase A PENDING · clase B/C GATED |

## 📐 SPEC FREEZE v1.0.0

### S1. Unidad de evaluación y fuente de verdad (Reference-only)

La unidad de evaluación es `(canonical_strategy_id, strategy_version_ref)` **dentro de una ventana de observación** acotada a bindings con `observation_class='CANONICAL'`. La verdad es exclusivamente el comportamiento **Reference observado**: hechos `echo.trade_lifecycle`/`echo.trade_deals` (065) con `attributed='CANONICAL'` y `strategy_version_ref` NOT NULL (version-proven), cobertura `echo.reference_coverage` (065), bindings/transiciones/readbacks 064, identidad 061. Reference = operación observada en la cuenta Reference, jamás señal ideal pre-broker (Live Authority §6; la no-distinción señal-rechazada vs sin-señal se preserva como límite declarado). Prohibido: consumir E-08/E-09 como calidad, reciclar evidencia de otra versión, inferir calidad desde members/ranking Forge.

### S2. StrategyExpectation V1 (portable acotada)

Registro durable **write-once** `echo.strategy_expectations` (069) sellado **antes** del forward que valida: identidad (`strategy_version_ref` sha256:…, `canonical_strategy_id`, `promotion_record_ref` de un `PromotionRecord INGESTED` real de E-04), refs de evidencia baseline **ya ingeridas** (TradeSet/MetricSet/artifact digests tal como fueron entregados por Forge — Echo no fabrica baseline, sólo referencia evidencia verificada), bases/unidades declaradas, períodos/labels de contexto de selección (IS/OOS/WFM como refs declaradas, no catálogo exhaustivo), `allowed_comparisons` (pares clave-catalog↔basis **validados contra el catálogo S0 `1.0.0`** vía `contracts.Catalog`; no se admite basis AUTO ni claves no canónicas), `unsupported_metrics`, `quality_flags`, `minimum_observation_policy_ref` + `policy_digest`, `sealed_at` + actor/reason. Identidad: `expectation_ref = H("echo-strategy-expectation.v1", campos canónicos ordenados)` sha256. Validaciones: `sealed_at` precede a `accepts_opens_from` del binding (o a la ventana declarada si aún sin binding); toda ref de baseline debe existir en persistencia E-04/E-05. **Decisión S0:** V1 define el tipo **local a Echo (069)**; NO se promueve a `v3/sdk/contracts` en este carril (S0 READ ONLY; promoción = cambio contractual separado, decisión pendiente §🧭). Falta de Expectation válida ⇒ la versión **no es evaluable** ⇒ `INSUFFICIENT_EVIDENCE/EXPECTATION_MISSING` (S5).

### S3. Ventana de observación y coverage

Ventana = intersección de `[accepts_opens_from, accepts_opens_to)` del binding con la ventana de política, en **event-time con basis verificada** (Live Authority §6 Time authority; `event_at_utc` sólo con conversor verificado, si no ⇒ `time_quality=UNKNOWN`). Coverage se ensambla **sólo** desde `echo.reference_coverage` (065): `KNOWN_COMPLETE` aporta intervalo cubierto; `PARTIAL` aporta con flag; `UNKNOWN`/ausencia aporta UNKNOWN y **jamás denominador**; `VALID_NO_SIGNAL` aporta exposición sin operaciones (denominador de frecuencia); `MARKET_CLOSED`/`STRATEGY_DISABLED` se excluyen del exposure por regla de política y se reportan. El vector derivado es durable (tabla `echo.quality_assessments`, inputs digests) y reconstruible; el vector de evidencia original nunca se borra (append-only E-07). Prohibido "días offline como señales ausentes" (master §19).

### S4. Baseline Forge y provenance

La baseline proviene exclusivamente de evidencia **ya ingerida y verificada** por E-04 (PromotionRecord INGESTED + artefactos/digests) referida por la Expectation. Echo no re-ejecuta Forge, no recalcula membership, no inventa métricas Forge: las comparaciones ocurren entre `MetricSet`s canónicos (E-05) — baseline referida por la Expectation y forward derivado de hechos Reference — usando `analytics/calculator.Compute` frozen y el catálogo S0 `1.0.0`. R canónica Echo continúa `profit_pips/risk_pips` (Live Authority §6); si la baseline Forge no expresa R comparable, la comparación usa sólo bases compatibles declaradas en `allowed_comparisons` y "R no comparable" se declara (Reality Check, Quality defendible). Los sets canónicos del forward se persisten vía el **writer canónico de E-05** (`v3/sdk/postgres/canonical_writer.go`, scopes nuevos, write-once idempotente por digest) — cero ALTER a 063.

### S5. Taxonomía de veredictos (UNKNOWN ≠ INSUFFICIENT ≠ FAIL)

Estados de evaluación versionados por política (master §9 Evidence Gate), con reasons durables: `INSUFFICIENT_EVIDENCE` (muestra/coverage/calendario bajo los mínimos declarados por la política, o prerequisitos ausentes: `EXPECTATION_MISSING`, `POLICY_UNAVAILABLE`, `COVERAGE_INSUFFICIENT`, `RISK_BASIS_UNKNOWN`), `VALIDATING` (ventana activa con coverage mínimo y aún bajo mínimo de decisión), `ELIGIBLE` (política satisfecha, comparaciones compatibles sin flags DQ), `WATCH` (warnings/DQ no materiales o flags de comparabilidad), `DEGRADED` (degradación económica **demostrada** según criterios declarados en la política; sólo si la política aprobó análisis de degradación — shadow simple SHOULD V1), `QUARANTINED` (fallo DQ material: conflicto de identidad/atribución, coverage contradictoria, violación de invariante). Distinción operativa: **UNKNOWN** = no determinado por ausencia de datos/coverage (razón durable, jamás 0); **INSUFFICIENT** = datos presentes, muestra bajo política; **FAIL** (`DEGRADED`/`QUARANTINED`) = evidencia positiva demostrada. Toda abstención se registra con causa; la abstención es salida válida y esperada (CASH para E-11).

### S6. Data quality antes de scoring

Gates en orden estricto, corto-circuito fail-closed: (1) identidad — `strategy_version_ref` + binding inmutable + expectativas consistentes; (2) liveness/coverage — vector S3 con mínimo de política; (3) atribución — hechos version-proven, `initial_risk_state='KNOWN'` para métricas R, `economics_completeness` UNKNOWN manejado como UNKNOWN; (4) **sólo entonces** evaluación económica (comparaciones S4). Un fallo en cualquier gate temprano produce `QUARANTINED` (material) o `INSUFFICIENT`/`UNKNOWN` con razón — jamás scoring con datos de calidad insuficiente.

### S7. Reset por StrategyVersion

Nueva `strategy_version_ref` ⇒ nueva Expectation + ventana desde su admission barrier + evidencia segmentada. Prohibido combinar v1/v2 como una sola serie, reciclar evidencia de versión anterior como nueva, o mover retrospectivamente el cutoff. La Reference permanente sigue observando aunque la allocation esté pausada; pausas de allocation no reinician ventanas ni detienen la observación (master §9 Version changes; segmentación conserva enrollment provenance). Comparación cross-versión requiere regla analítica declarada — **out of scope V1**.

### S8. Elegibilidad sólo con política autorizada (fail-closed)

`echo.eligibility_decisions` (069, write-once, `decision_ref` sha256) se emite **sólo** si la política referida por `minimum_observation_policy_ref` resuelve en `echo.quality_policies` (069, write-once) con `policy_digest` coincidente. E-10 **no hardcodea thresholds** (jamás 50 trades/80% coverage por conveniencia — master §9): el contenido (calendario mínimo 3–6 meses owner, coverage mínimo, N trades, criterios WATCH/DEGRADED/QUARANTINED, método estadístico con supuestos declarados) es un artefacto **ratificado por el owner**. Sin política resolvible ⇒ `INSUFFICIENT_EVIDENCE/POLICY_UNAVAILABLE` fail-closed. La decisión registra scope de mandato y expiry, abstención explícita, e inputs digest (idempotencia por replay). `echo.economic_copy_authorizations` (066) **no es plano de E-10** (dueño = plano config owner; E-08 lector exclusivo): eligibility de calidad ≠ autorización de copia económica ≠ activación (E-08/E-12 + owner).

### S9. Calendario mínimo y restricciones

El requisito DQ1 (~3–6 meses + trade coverage; master §19) vive **dentro de la política** (S8); E-10 lo aplica como criterio versionado y el Calendar Gate es mecánico: ninguna decisión puede ser `ELIGIBLE` con ventana calendaara < mínimo de política o coverage < mínimo — el gate no se omite por fecha objetivo. El software de abstención/CASH queda listo independientemente del calendario; el tiempo no suple falta de trades (master §19).

### S10. Ausencia de datos ≠ rendimiento cero

Denominadores honestos: intervalos UNKNOWN se excluyen del denominador y se reportan; sin trades en intervalo cubierto ⇒ `VALID_NO_SIGNAL` cuenta exposición; fills/fees ausentes son UNKNOWN (NULL ≠ 0, signos preservados — invariante 14); PF con cero pérdidas es **indefinido** (no 0, no admisión automática); DD de trades cerrados ≠ equity intradía (S0: `drawdown.max` sobre curva cerrada declarada); Sharpe/Sortino fuera del catálogo V1. Las métricas de frecuencia comparan contra tiempo observado (S3), no días de calendario crudos.

### S11. Separación absoluta SQ / EF

Ningún artefacto de E-08/E-09 entra al assessment de calidad: E-10 no lee 066/067 (excepto negación estructural), no consume las claves EF del catálogo (`execution.missing_ratio`, `slippage.mean`) como calidad, no emite órdenes, no aplica transiciones de bindings, no escribe 001–068. E-10 es **READ-ONLY sobre 001–068**; escribe exclusivamente su esquema 069 (+ scopes canónicos nuevos vía writer E-05). Los read models de calidad (`echo.quality_assessments`, decisiones) **no son autoridad** hasta que E-13 les dé superficie certificada; una Decision consume la referencia exacta persistida, no el query del día (master §10).

### S12. Persistencia 069 y límites de escritura

`069_strategy_quality_eligibility_e10.up.sql` (exclusiva E-10; 070+ fuera de scope) crea: `echo.strategy_expectations`, `echo.quality_policies`, `echo.quality_assessments`, `echo.eligibility_decisions` + guardas write-once por trigger, REVOKEs, interlock de existencia con 063/064/065 (guards, patrón E-09), índices de ventana. FKs internas de 069; refs cross-schema por texto + patrón sha256 (precedente E-05: sin FK hacia 061). Down-migration simétrica. Driver `ECHO_E10_STRATEGY_QUALITY` **default OFF fail-closed** + wiring mínimo (patrón E-08/E-09); sin cron productivo en clase A (sólo harness/tests).

### S13. Fuera de scope

ML/meta-score/optimización continua; régimen aprendido (sólo si la política lo declara, POST); MAE/MFE (sin captura verificado ⇒ no disponible); bandas normales automáticas con sample pequeño (NIST; bootstrap sólo si la política lo declara con supuestos); eligibility automática sin política; catálogo exhaustivo de Expectation; comparación cross-versión; API/UI read (E-13); escritura en `economic_copy_authorizations`; Forge/E-11/E-12.

## 🗺️ PLAN v1.0.0 — clases y work packages

**Clase A (implementable HOY, cero meses de observación; mandato NORMAL §🚦):** contratos + persistencia/read models + cálculo y tests con fixtures deterministas sobre PG descartable. No requiere E-06 `OBSERVING` físico ni hechos E-07 reales.

| WP | Contenido | Dependencias | Gate |
|---|---|---|---|
| T00 | Materializar SPEC/PLAN/TASKS/VERIFICATION/NORMAL-PROMPT desde esta nota en `specs/FEAT-STRATEGY-QUALITY-ELIGIBILITY-E10/` (docs-only, commit separado); reconciliar baseline (fetch; HEAD==origin; worktree limpio; failing set baseline) | nota E-10 (SHA en provenance) | SPEC materializada byte-verificable |
| T01 | Dominio `strategy_quality.go`: Expectation + receta digest + validaciones S2; Window/CoverageVector S3; veredictos S5 + transiciones con reasons; decisiones S8 (tipos y reglas, sin IO) | T00 | CONTRACT rojo→verde dominio |
| T02 | Migración 069 + guardas write-once + REVOKEs + interlock + down (S12) | T01 | PG up/down/up en descartable |
| T03 | Stores 069: expectations/policies/assessments/decisions con CAS de contenido, idempotencia por digest, conflictos fail-closed | T02 | PG tests físicos |
| T04 | Ensamblador de coverage/ventana: S3 sobre `reference_coverage`/`trade_lifecycle` (READ-ONLY), digests de inputs, UNKNOWN-first | T03 | Matriz coverage |
| T05 | Gates DQ S6 + derivación de sets canónicos del forward vía writer E-05 + comparaciones con calculator/catálogo S0 (S4) | T04 | CONTRACT+PG |
| T06 | Veredictos y política: resolución fail-closed de policy (digest match), evaluación de mínimos, veredictos S5, abstención | T05 | Matriz veredictos |
| T07 | `EligibilityDecision` durable + idempotencia + reset por versión (S7) + prohibiciones cross-version | T06 | PG tests |
| T08 | Driver `ECHO_E10_STRATEGY_QUALITY` OFF + wiring mínimo + fixtures de arranque | T07 | cero efectos OFF demostrado |
| T09 | Matriz E10-01…E10-16 (VERIFICATION §🧪) + cobertura ≥95% funcional-critica-primero (preferencia DURA owner) con inventario durable de residuo (lección E-09: artefacto persistente con SHA, jamás /tmp) | T08 | COVERAGE_GATE |
| T10 | Gates G1–G5 (§🧪), no-efectos sobre 001–068 (fingerprint+greps), failing set apples-to-apples, push FF, VERIFICATION con evidencia | T09 | HANDOFF Manager |

**Clase B (GATED — integración con observación física auténtica):** primera evaluación con datos Reference reales. Prerrequisitos exactos: E-06 binding `OBSERVING` físico real (G1 `PROMOTION_SEAL_MISSING` resuelto + T21; entorno E-06 designado), E-07 `PHYSICAL` (EA enriquecido en terminal real + protocolo V1.1), aplicación de 064–069 en DEV compartido por flujo de release. Clase B jamás corre con datos sintéticos presentados como reales.

**Clase C (GATED — certificación de calendario y elegibilidad real):** política de observación **ratificada por owner** (contenido exacto: calendario, mínimos, criterios WATCH/DEGRADED, método estadístico con supuestos) + write path de `echo.quality_policies` owner-operado + ventana real ≥ política. Producto: negativo-PnL alto-DQ no elegible por ese score; nueva versión = reset demostrado; Calendar Gate no omitido; abstención demostrada como salida válida; read model no autoridad. `PHYSICAL/PRODUCT_CAPABILITY` no se certifica con mocks.

## ✅ Tareas

> [!example]- Fuente de tareas — editar / mover de estado aquí
> - [ ] E-10 T00: materializar SPEC/PLAN/TASKS/VERIFICATION en branch `feature/e10-strategy-quality-eligibility` desde `d69e1ee3` (tras gate Manager) #owner/agent #type/dev #area/echo
> - [ ] E-10 T01–T03: dominio Expectation/veredictos + migración 069 + stores fail-closed #owner/agent #type/dev #area/echo
> - [ ] E-10 T04–T06: coverage UNKNOWN-first + DQ gates + scoring E-05 + política fail-closed #owner/agent #type/dev #area/echo
> - [ ] E-10 T07–T08: eligibility decisions + reset por versión + driver OFF + wiring #owner/agent #type/dev #area/echo
> - [ ] E-10 T09–T10: matriz E10-01…16 + COVERAGE_GATE ≥95% + gates G1–G5 + push FF + handoff #owner/agent #type/dev #area/echo
> - [ ] E-10 clase B: primera evaluación con Reference física real (GATED: E-06 OBSERVING + E-07 PHYSICAL + 064–069 en DEV) #owner/agent #type/dev #area/echo #blocked
> - [ ] E-10 clase C: certificación calendario/elegibilidad con política owner (GATED: política ratificada + ventana real) #owner/agent #type/dev #area/echo #blocked

## 🧪 VERIFICATION (gates clase A)

- **G1 SOURCE:** delta ⊆ archivos autorizados (specs + `069_*` + paquetes strategy-quality nuevos + wiring mínimo + tests); `go.mod` delta 0; migraciones 001–068 byte-intactas; cero nombres E-10 en el failing set de otros carriles (apples-to-apples por nombre).
- **G2 CONTRACT:** dominio y recetas digest con tabla roja→verde (T01); `contracts.Catalog` valida todo `allowed_comparisons`; `analytics.Calculator` frozen consumido sin fork.
- **G3 PG:** PG 17.11 descartable con arnés de identidad (patrón C4-S del mandato E-09: preflight RO + marcador exclusivo `echo_harness.e10_harness_marker` sobre base `echo_e10_harness` + predelete transaccional + guard Go), up/down/up 069, guardas write-once, REVOKEs, interlock 063/064/065, `-race` por paquete aislado.
- **G4 COVERAGE_GATE:** ≥95% sobre archivos nuevos con **funcionalidad crítica primero** (preferencia DURA del owner); ramas inalcanzables se borran con justificación; residuo declarado en artefacto persistente con SHA/digest + clasificación crítica-vs-defensa (corrección de la deuda E-09 `E09-COVERAGE-146-EVIDENCE`: jamás resúmenes en /tmp).
- **G5 NO-EFECTOS:** fingerprint + greps demuestran cero escrituras a 001–068 y cero efectos con driver OFF; cero Kafka produce económico; cero E-11/E-12 code; PHYSICAL/INTEGRATION `PENDING` declarados; `FINAL_CLOSED=NO`.

**Matriz E10-01…E10-16 (fixtures deterministas):** 01 Expectation sellada pre-barrier PASS; 02 `EXPECTATION_MISSING` fail-closed; 03 ventana honesta con vector mixto KNOWN/PARTIAL/UNKNOWN; 04 UNKNOWN excluye denominador y reporta; 05 `VALID_NO_SIGNAL` cuenta exposición; 06 política satisfecha ⇒ `ELIGIBLE`; 07 bajo mínimo ⇒ `VALIDATING`/`INSUFFICIENT`; 08 `POLICY_UNAVAILABLE` fail-closed; 09 digest de política divergente ⇒ rechazo; 10 comparación no permitida ⇒ rechazo + `WATCH` flags; 11 PF indefinido ≠ 0; 12 conflicto de atribución ⇒ `QUARANTINED`; 13 nueva versión ⇒ evidencia nueva, cero herencia; 14 replay idempotente (mismo digest ⇒ cero escrituras); 15 driver OFF ⇒ cero efectos; 16 abstención registrada como decisión válida consumible por E-11 (read-only).

**STOP conditions (NORMAL escala al Manager y no continúa):** falta o drift del baseline; necesidad de ALTER a 001–068 o de tocar `economic_copy_authorizations`; necesidad de un tipo S0 nuevo; solicitud de inventar thresholds/política; datos sintéticos presentados como observación física; coverage <95% sin inventario durable; cualquier efecto fuera del esquema 069 y scopes canónicos nuevos.

## 🚦 NORMAL-PROMPT (mandato exacto clase A)

- **Rol:** NORMAL (GLM-5.3 Flash) ejecuta SPEC FREEZE v1.0.0 de esta nota. **Gate previo obligatorio:** Manager autoriza tras revisar esta planificación; sin esa autorización no hay escrituras.
- **Repo:** `xKoRx/echo` READ-ONLY hasta el gate. Crear `feature/e10-strategy-quality-eligibility` desde `d69e1ee35d95f84ddaec812a956f5837d799fbe3` (fetch, HEAD==origin verificado, worktree limpio). `master` y 001–068 intocables. Sin merge a master, sin push a otras ramas, sin release, sin deploy, sin Forge, sin PROD, sin activación económica, sin E-11/E-12, sin reabrir E-01…E-09.
- **Secuencia:** T00→T10 de §🗺️, un commit atómico por tarea, push FF `HEAD==origin` al cierre. Migración 069 exclusiva. Arnés con identidad (G3). Cobertura crítica-primero con inventario durable (G4). Materializar esta nota (SPECS) verbatim como T00 con su SHA de provenance.
- **Al terminar:** VERIFICATION v1.0.0 con evidencia por gate + matriz E10-01…16 + agent_run + cambio de estado de esta nota → handoff Manager (no hay certificaciones físicas en clase A; `PHYSICAL_PENDING`/`INTEGRATION_PENDING` declarados).

## 🧭 Decisiones

- E-10 es **Reference-only**: la calidad se valida contra comportamiento Reference observado, jamás contra señal ideal; E-08/E-09 no entran al assessment (la arista DAG E09→E10 es interpretación conjunta, no dependencia de datos — reconciliado con mandato Manager 2026-09-21).
- `StrategyExpectation` V1 vive en 069 (Echo-owned, write-once, refs a evidencia ingerida); la promoción a tipo S0 es cambio contractual separado.
- La política de observación mínima es artefacto owner-ratificado; E-10 falla cerrado sin ella y jamás hardcodea thresholds; abstención/CASH es salida válida de primera clase.
- El tiempo de calendario no suple falta de trades: coverage y exposición honestas antes que cualquier score; DQ antes que economía.

### Decisiones pendientes del owner (exactas, no bloquean clase A)

1. **Contenido de la política de observación mínima** (calendario 3–6 meses, coverage mínimo, N trades, criterios WATCH/DEGRADED/QUARANTINED, método estadístico con supuestos declarados) y su write path (propuesta: `echo.quality_policies` 069 write-once owner-operado; alternativa ETCD). Requerida para clase C.
2. **Promoción de StrategyExpectation a S0** si algún día Forge debe producir expectations end-to-end (fuera de este carril).
3. **Aplicación 064–069 en DEV compartido** por flujo de release (precondición física de clase B/C; no forzar 061 completa — Environment Contract §7).
4. **Corrección documental E-06:** la línea "NORMAL no lanzado" del roadmap del padre es anterior a la implementación WP-A/T09–T10 hoy presente en el baseline (commits 2026-09-17); delta docs-only registrado aquí y aplicado en la actualización del padre de esta sesión.

## 📆 Bitácora

- **2026-09-21 — E-10 TOP planning one-shot (sin código):** SPEC FREEZE v1.0.0 + PLAN (clases A/B/C, T00–T10) + VERIFICATION (G1–G5 + matriz E10-01…16) + NORMAL-PROMPT congelados en esta nota contra baseline `d69e1ee3` READ ONLY. Contratos verificados físicamente file:symbol: 064 `reference_bindings`/`binding_transitions`/`reference_readbacks` + stores; 065 `trade_lifecycle` (`attributed`, `initial_risk_state`, `economics_completeness`, `strategy_version_ref` nullable) + `reference_coverage` (estados `KNOWN_COMPLETE/PARTIAL/UNKNOWN`, vector 7 estados, UNKNOWN≠cero); 063 `canonical_*` write-once + writer + calculator + catálogo S0 `1.0.0`; 066 `economic_copy_authorizations` fuera de scope; 067 fuera de scope (SQ≠EF); **069 libre** (última = 068). S0 **no** tiene tipo Expectation (sólo `ExpectationRef` en promotion.go:228) ⇒ Expectation V1 local 069. Migración 063 ya aplicada en DEV compartido; 064–068 no aplicadas (precondición clase B/C registrada). Estados reconocidos: E-05 integrado; E-06/E-07 source disponible con gates físicos pendientes; E-08/E-09 fuera del data-scope y sin bloquear. Próximo gate: **Manager review de esta planificación → NORMAL clase A**.

## 🔗 Docs / Links

- Provenance de esta planificación: baseline `d69e1ee35d95f84ddaec812a956f5837d799fbe3` (ls-remote 2026-09-21) · worktree de verificación local `097e39eb767319801130be772de524e7e846e968` (source de producto idéntico por delta C4: 11 archivos tests/docs) · catálogo S0 `v3/sdk/contracts/catalog.go` (`InitialCatalogVersion 1.0.0`) · `v3/sdk/contracts/promotion.go:228` (`ExpectationRef`) · `v3/sdk/analytics/calculator/calculator.go:144` (`Compute`) · `v3/sdk/postgres/canonical_writer.go` · migraciones `063/064/065/066/067/068` (`v3/sdk/postgres/migrations/`).
- [[Echo — Live Platform V1]] · [[Echo — E-05 Analytics Convergence A0]] · [[Echo — E-06 Reference Enrollment and Binding]] · [[Echo — E-07 Raw Facts DEAL Coverage Trade Lifecycle]] · [[Echo — E-09 Execution Copy Reconciliation and Execution Fidelity]] · [[Echo — Producto Integrado]]
- [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] (§5 binding/enrollment, §6 Reference/coverage/time authority, §8 invariantes 1–18)
- [[Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026]] (§9 Strategy Quality blueprint, §10 Analytics, §19 Calendar-latency)
- [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan]] (§5 Quality defendible, D-14/D-16/D-26, A08 opción A)
- [[Echo + Echo Forge — Environment Contract]] (DEV/PROD; §5–§7 estados AS-BUILT y reconciliación pendiente)
- [[Echo + Echo Forge — Deferred Certification Backlog]] (gates físicos E-06/E-07/E-08/E-09 — externos a E-10)
