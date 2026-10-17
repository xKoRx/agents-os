---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo Futures]]"
sprint:
start:
due:
progress: 25
repo: "xKoRx/echo"
jira:
prs:
aliases: []
tags:
  - kind/project
  - area/echo
created: "2026-10-16"
updated: "2026-10-16"
---

# Echo Futures — Runtime Pools

## 🎯 Objetivo

Entregar extensión runtime de pools y asociaciones pool–Strategy–MM mediante cuatro shots independientes, con diseño verificable, implementación, auditoría adversarial y corrección. S01 diseña y prepara; no implementa producto. Autoridad funcional/técnica única: `VAULT_ROOT/10-projects/Echo Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md` (§1–11 decisiones compatibles R5; §12–18 contrato R6 prioritario). Este proyecto es el planificador único; no duplicar tasks/gates en otra SPEC.

## 📊 Estado actual

S01 revisado y **G1 `accepted` por Manager GPT-6** sobre R6 publicada en Agents-OS commit `6d73673ca4573d25e4552ad7a58a23f7b55ca69c`; producto branch `feature/ef-runtime-pools@d74b652500e673fc2bf4289f9f195f11960ba26e` confirmado remotamente idéntico a master en el gate. **S02 autorizado exclusivamente con SUBMANAGER LOCAL obligatorio y subagentes GLM one-shot en la rama runtime** conforme a §12–18 del diseño y al paquete Fase 2. G2 permanece pending. Cierre S01 ya ejecutado; Manager y proyecto global abiertos. No egress real ni certificación física autorizados. La demostración NinjaTrader multicuenta y el productor contable LIVE continúan `NOT_DEMONSTRATED`; fallas materiales → G2 blocked, no aceptación ficticia.

Base **HEAD** de producto: `xKoRx/echo@d74b652500e673fc2bf4289f9f195f11960ba26e`, `origin/master` después de fetch no destructivo. Checkout original `master@3596fc48` limpio se conserva; worktrees históricos/prunables no se limpiaron. Sin rama local/remota `feature/ef-runtime-pools` antes de crearla. Worktree externo `echo-runtime-pools` relativo a [[echo-go-workspace]], creado con `git worktree add -b feature/ef-runtime-pools <workspace>/echo-runtime-pools d74b652500e673fc2bf4289f9f195f11960ba26e`. HEAD inicial idéntico a base, sin diff ni untracked de producto. El tool de worktree de la app habría operado sobre el repo Agents-OS de este chat; se usó Git dirigido al repo producto. No reset/stash/clean/merge/rebase/cherry-pick ni alteración de rama backtester.

## 🧱 Entrega de desarrollo

| Repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | feature/ef-runtime-pools | d74b652500e673fc2bf4289f9f195f11960ba26e | [[ECHO-FUTURES-RUNTIME-POOL-DESIGN]] §1/5/7/13 | misma autoridad §12/14–18 | S01 review, cero implementación |
| xKoRx/agents-os | master | HEAD concurrente, commit documental final en historial de esta nota | Mandato S01 | Este planificador + diseño | Documentación por delta; readback y push sin force |

Contratos relacionados **CONTRACT**, sólo secciones seleccionadas: `VAULT_ROOT/10-projects/Echo Futures/Echo Futures Architecture Candidate V2.md` §2; `VAULT_ROOT/10-projects/Echo Futures/Echo Futures — Technical SPEC V1.md` §3,9–13,15–17,24–26; `VAULT_ROOT/10-projects/Echo Futures/Echo Futures — D2-08 Strategy Runtime.md` §3,5,6. R6 reemplaza cualquier cálculo de indicadores en consumidores o atribución de economía al PoolManager. Instrucciones repository se leen desde el checkout S01; mandato Owner prevalece sobre la ubicación histórica specs/ para este diseño/planner Agents-OS.

## Matriz requisito → evidencia → trabajo restante

| Requisito | Estado | Evidencia y gap | Shot |
|---|---|---|---|
| Rama/base sin alterar producto | done | HEAD Git S01 y controles de estado; push/readback de rama registrados al cierre | S01 |
| Signal/ciclo account-agnostic | done | HEAD `v3/sdk/futures/domain/signal.go`: Signal/DeriveSignalID; CONTRACT SPEC §9 | S02 preserva, S03 ataca |
| FIFO/afinidad/exclusividad/retorno diario | missing | HEAD provider.OwnerState no tiene claim/affinity; R6 §12 B–D cierra contrato | S02 |
| Fanout/dedup y targets históricos | partial | HEAD strategy.FanoutState; dedup por AccountStrategy no cubre rotación | S02 |
| MM y RuleSet por asociación/cuenta | partial | HEAD Compose(cfg.MM), SnapshotViews.EffectiveRuleSet global | S02 |
| Económica fuera de PoolManager | replaced | R5 aclarado; kernels contables/provider/MM existentes, facts/policy seam faltan | S02 |
| Presupuesto completo | replaced | HEAD TGMM EntryBudgetV1 rechaza; GerardMM aplica headroom. Política nueva R6 §12 F | S02, adaptación driver backtester diferida |
| Analytics compartido/distribuido | partial | HEAD TGSnapshot via BarClosed; MM usa puntero local; S2 calcula indicadores | S02 |
| Multiaccount físico/recovery | partial | HEAD Bridge.Run per-account y M2; AddOn single resolvedAccount y NTX ActiveConn | S02 P0-NT + implementación, S03 crítica, S04 fixes |
| Plan cuatro shots/cierre | done | Este plan, validadores y logs; G1 review no accepted | S01 |

## Alcance, decisiones y arquitectura

Alcance exacto: R6 §12–17; mapas source §15 son allowlist S02/S04. No-goals: backtester driver/control, campañas 40, estrategia/indicadores de matemática nueva, live/egress, infra real, UI, multi-Strategy por cuenta, múltiples cuentas simultáneas por asociación y quinto shot. No tocar `sync.sh`, `.sync/`, controles TradesGerard ni trabajo concurrente. Modificar declaraciones module.yaml de source en S02 para el nuevo owner está dentro del wiring; aplicarlas a ambientes está fuera.

| ID | status | resolution | source/evidence | phase consuming it |
|---|---|---|---|---|
| D1 | CONFIRMED | Strategy siempre evalúa según triggers; ninguna cuenta/pool/MM/economía en Signal | Mandato S01 §4; HEAD Signal | 1–4 |
| D2 | CONFIRMED | Un turno por asociación, afinidad permanente Strategy, pausa rota misma sesión, próximo día más antigua propia elegible | Owner §5–6; R6 §12 B–D | 1–4 |
| D3 | CONFIRMED | Presupuesto MM no se reduce/rechaza por remanente positivo | Owner §7; R6 §12 F | 1–4 |
| D4 | TECHNICAL_RESOLUTION | Claim/epoch/afinidad en provider_rules, PoolManager mínimo por pool y fanout único por Strategy | HEAD provider.OwnerState/FanoutState; R6 §12 A–E | 2–4 |
| D5 | TECHNICAL_RESOLUTION | Availability tipada desde revisión contable, policy MM y Provider; no derivar pausa desde cierre de trade | HEAD MMDecision, risk_eval, accounting.Revision; R6 §12 C | 2–4 |
| D6 | TECHNICAL_RESOLUTION | Cursor durable + destino/no-target por asociación; fence M1/M2 y release sólo con drenaje lógico/físico | HEAD Operation/M2; R6 §12 D–E | 2–4 |
| D7 | TECHNICAL_RESOLUTION | Dispatcher por key/TypeName, MM sellado y RuleSet por contexto | HEAD Registrations/main/Views; R6 §15 | 2–4 |
| D8 | TECHNICAL_RESOLUTION | Snapshots analíticos transportados; mover kernels S2 sin cambiar matemática; política presupuesto explícita compatible | HEAD TGSnapshot/S2/TGMM/GerardMM; R6 §12 E–F | 2–4 |
| D9 | TECHNICAL_RESOLUTION | NT una lane/conexión por binding dentro de AddOn único; P0-NT acotado en S02, sin quinto shot | HEAD AddOn/NTX; R6 §15 | 2–4 |
| D10 | CONFIRMED | Manager acepta G1–G4; Owner mantiene gate de egress; STOP entre shots | Mandato S01 §10/13 | 1–4 |

No decisiones de negocio abiertas. Incertidumbre física separada de arquitectura: no certificación NT multicuentas ni productor de economía LIVE observados en S01. P0-NT y contrato contable serializado tienen owners y stop condition abajo. S02 no inventará cuenta/calendario/umbrales para completar fixtures productivos.

Arquitectura actual/objetivo, secuencia, contratos versionados, ejemplos, fórmulas, observabilidad, migración y rollback viven por referencia en R6 §12–17; se consumen íntegros por cada ejecutor. El plan no los copia. El contraste actual es HEAD source; tests existentes son TEST y no se presentan como corridos. Resultado físico permanece NOT_DEMONSTRATED hasta evidencia real autorizada. Retrieving usó rg enfocado; `graphify-obsidian` no está en PATH, fallback explícito sin recorrer historia D1–D6.

## Roadmap, carga y gates

Cuatro shots/gates como contrato Owner. S02 mantiene las ocho tareas T2.1–T2.8, pero requiere SUBMANAGER LOCAL obligatorio y subagentes GLM especializados dentro del mismo shot, por mandato Owner posterior a S01. No se crean otros shots/gates. Su mayor carga está en concurrencia/wiring y fixtures, no en operaciones reales. S03 es independiente y read-only; S04 sólo hallazgos, regresión e integración local. Ningún despliegue se traslada silenciosamente: certificación física/egress posterior requiere autorización Owner y queda reportada como obligación no ejecutada, fuera de estos cuatro shots. Si S02 no completa su alcance, entrega G2 blocked en lugar de pasar deuda escondida a S04.

| Gate | current state | phase agent responsibility | owner acceptance evidence | enables |
|---|---|---|---|---|
| G1 | accepted | GOD S01 entregó diseño/rama/paquetes/validaciones y cerró S01 | Manager GPT-6: revisión independiente documental R6 §§12–18, plan T1–T4, fuente selectiva; GitHub branch/master comparados idénticos `d74b6525` y commit documental `6d73673c`. Se acepta la implementabilidad del diseño, NO el runtime ni el egress físico. | S02 habilitado |
| G2 | pending | SUBMANAGER LOCAL S02 integra subagentes GLM con tests y evidencias por worker; entrega G2 review o blocked | Pendiente Manager sobre SHA integrado; implementación solitaria no aceptable | S03 sólo tras accepted |
| G3 | pending | GLM S03 entrega dictamen reproducible sin autocorregir en review o blocked | Pendiente Manager sobre hallazgos | S04 sólo tras accepted |
| G4 | pending | GLM S04 entrega fixes/tests y residual explícito en review o blocked | Pendiente Manager; egress real requiere Owner aparte | Fin del plan, no quinto shot |

## ✅ Tareas

Cada ítem define objetivo | archivos/símbolos | precondición | implementación | tests | evidencia. Estado [x] significa trabajo S01 realizado, no aceptación del gate.

- [x] T1.1 Preparar rama | Git producto | checkout/refs inspeccionados | fetch y crear desde SHA exacto en worktree aislado | rev-parse/status/diff | base=HEAD y estado limpio. #owner/agent
- [x] T1.2 Cerrar diseño | R6 §12–18 y símbolos §15 | R5/contratos | auditoría localizada y resolución técnica | matriz requisitos/source refs | autoridad actualizada, sin producto editado. #owner/agent
- [x] T1.3 Validar y cerrar S01 | este planner, log/feedback/run | T1.1–2 | validadores/readback/commit/push/cierre | schema/plan/refs/Git | G1 review + evidencias cierre. #owner/agent
- [ ] T2.1 Spikes y contratos | R6 §15 NTX/AddOn, domain/config/pool | G1 accepted | P0-NT local, input contable serializado y contratos v1 | dos lanes/account identity, schema invalid | matriz de capacidades, decisión sobre ejecución verificable. #owner/agent
- [ ] T2.2 Asignación account-wide | pool, provider, futures_pool_manager | T2.1 | reducer claim/affinity/availability, account policy reusando MM | FIFO, day, concurrencia y restart | tests e invariantes S01 casos 1–4/7. #owner/agent
- [ ] T2.3 Fanout | domain/fanout, strategy/fanout, futures_signal_fanout | T2.2 | merge por asociación, cursores/no-target y manage-only | replay antes/después de rotar/evicción | una decisión por asociación/señal. #owner/agent
- [ ] T2.4 Ejecución y economía | operation/provider/MM/config y wrappers Core | T2.2–3 | epochs/reservas/revalidate, MM registry/pin, policy presupuesto y revisión causal | 53/300, 1/1000, breach real, no falsa pausa | aislamiento de estado y budget. #owner/agent
- [ ] T2.5 Analytics | analytics/TG/S2/marketctx/wrappers | T2.1 contratos | demandas unidas/snapshots/consumidores, kernels S2 extraídos | proceso separado, corte causal, equivalencia | Strategy/MM sin cálculo duplicado. #owner/agent
- [ ] T2.6 Física contractual | bridge/main/session/NTX/AddOn | T2.1/4 | lanes per binding, fence M2/drain, cancel/replace/recovery | ACK incierto, crash, late fill, identidad | SIM/API compile separados de físico real. #owner/agent
- [ ] T2.7 Composición y migración | futuresruntime/main/statefun/module.yaml source | T2.2–6 | dispatcher único por tipo, bootstrap idempotente, compat fixed/pool | builder real, roundtrip states, legacy claim, 200 cuentas | integración local de siete escenarios. #owner/agent
- [ ] T2.8 Validación y entrega | nuevos tests §15 + evidencia en planner | T2.1–7 | vet/staticcheck/race/coverage y SHA final | R6 §16 completo | G2 review/blocked, sin S03 ni deploy. #owner/agent
- [ ] T3.1 Auditoría semántica | diff base→SHA S02, R6 §12–17 | G2 accepted | trazar cada invariante y detectar gaps/bypass | escenarios reproducibles de señales/affinity/budget | findings con archivo/símbolo/severidad. #owner/agent
- [ ] T3.2 Auditoría concurrencia/recovery | fanout/provider/operation/analytics/bridge | T3.1 | permutar orden y restart; repetir suites en sandbox | duplicados, stale epochs, física y causalidad | evidencia independiente sobre SHA S02. #owner/agent
- [ ] T3.3 Dictamen | sección S03 de este planner | T3.1–2 | priorizar hallazgos y cobertura real; separar baseline/delta/no demostrado | reproducibilidad y revisión read-only | G3 review/blocked; no fixes ni autoaprobar. #owner/agent
- [ ] T4.1 Corregir hallazgos aprobados | sólo mapa §15 y líneas de finding | G3 accepted, scope Manager | fixes mínimos por finding | regresión antes/falla después/pasa | commits ligados a IDs de hallazgo. #owner/agent
- [ ] T4.2 Integrar y verificar | tests/contratos/config source runtime | T4.1 | suite relevante y regresión, resolver interacciones sin features nuevas | R6 §16 + S03 repros | SHA consolidado, cobertura y residual. #owner/agent
- [ ] T4.3 Entregar cierre del alcance | este planner/diseño si errata Manager | T4.1–2 | evidencia final/rollback/readback | refs/schema/plan y producto | G4 review/blocked, sin deploy ni quinto shot. #owner/agent

## Prompt común del ejecutor

Lee bootstrap canónico una vez y el paquete ASIGNADO de este proyecto. Usa diseño R6 como autoridad única y revisa sólo símbolos allowlisted §15; no reconstruyas historia ni controles TradesGerard. Resuelve worktree desde echo-go-workspace y verifica branch/base/HEAD/cleanliness antes de tocarlo; preserva WIP ajeno. Una sola fase por contexto; excepción explícita S02: SUBMANAGER LOCAL y subagentes GLM obligatorios, dentro de S02. S03/S04 mantienen independencia y no se delegan implícitamente. HEAD/code → contratos → reports; nunca tests/interfaces como prueba física. Invariantes: Signal intacta, Strategy siempre técnica, MM/Provider únicos dueños económicos, PoolManager sólo selección/facts, afinidad permanente, exclusividad account-wide, cursor anti-replay, drenaje/fence, no migración MMState/PnL, analytics compartido causal y NinjaTrader dummy. Respeta mandato sin egress real. Toda tarea progresa en esta nota; evidencia portable y SHA exacto. Test failure no se oculta cambiando tests/expectativas: nueva regresión y finding; cualquier cambio legítimo de test requiere motivo trazable a R6. Fuera de allowlist o semántica contradictoria ⇒ PLAN_CONFLICT/Gn blocked al Manager. No force-push ni reset/stash/clean. Ningún agente acepta su gate ni inicia otro shot. Devuelve gate review/blocked, evidencia ejecutada, límites y STOP.

### Paquete autónomo Fase 1 — S01 GOD LOCAL diseño

**Misión exacta:** diseño implementable R6, rama aislada y paquetes 2–4; ningún producto modificado.

**Precondiciones verificables:** mandato Owner S01; master remoto resoluble; instrucciones Agents-OS cargadas una vez.

**Lectura obligatoria:** `VAULT_ROOT/10-projects/Echo Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md`; contratos seleccionados arriba; boundaries source §15.

**Decisiones cerradas:** D1–D10; corrige R5 por mandato, no nuevo agregado técnico.

**Implementación paso a paso:** T1.1 refs/worktree; T1.2 lectura selectiva y R6; T1.3 plan/validación/persistencia/cierre.

**Archivos esperados:** modify diseño y padre Echo Futures por delta; create este proyecto canónico desde materializer, feedback/log/run si aplica. Ningún producto, test, config ni script de ejecución.

**No tocar:** Go/C#/scripts/config producto, backtester, TradesGerard, infra, sesión Manager y proyecto global.

**Spikes permitidos:** sólo inspección read-only de contratos actuales. No compilar/operar NT ni campañas.

**Tests y asserts:** validadores Agents-OS de schema/plan/refs; base=branch HEAD, diff vacío; bootstrap source sin delta remoto; readback de cambios.

**Entregables/Gate G1:** R6 + rama + este plan, review o blocked con evidencia. No accepted.

**Handoff a Fase 2:** Manager acepta G1 y envía prompt común + despacho 2 con SHA/artefactos; GOD STOP.

### Paquete autónomo Fase 2 — S02 SUBMANAGER LOCAL con subagentes GLM

**Misión exacta:** submanager LOCAL obligatorio coordina especialistas GLM one-shot W0–W7, integra R6 en branch runtime y verifica suites/evidencias para G2. Submanager orquesta, revisa e integra mecánicamente; no absorbe por sí solo las implementaciones. Sin operaciones reales.

**Precondiciones verificables:** G1 accepted por Manager, HEAD descendiente de S01, worktree sin drift y Environment Contract antes de cualquier acceso físico. Confirmar capacidad de lanzar subagentes LOCAL; si no existe, G2 blocked/SUBAGENTS_UNAVAILABLE sin ejecución solitaria.

**Lectura obligatoria:** este proyecto decisiones/tasks/gates; `VAULT_ROOT/10-projects/Echo Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md` §12–18; repository AGENTS/CONSTITUTION y reglas de módulos/config/tests; source exacto §15 por tarea. No reabrir fuentes de campañas excepto seam declarado.

**Decisiones cerradas:** D1–D10, en especial distinguir account policy de TerminationIntent y clamp por piso de otras reglas de MM.

**Implementación paso a paso:** ejecutar T2.1→T2.8 mediante workers W0–W7, según la matriz obligatoria aquí registrada. Congelar contratos W0, delegar owners disjuntos, integrar cada entrega sólo tras pruebas/inspección, luego integración W6 y QA fresca W7. Mantener atomicidad state+egress y prueba de restart; registrar progreso, evidencias y rechazo/rework por worker en este único planner.

**Archivos esperados:** modify/create exactos R6 §15; nuevos tests runtime_pool_test.go por paquete; ningún archivo de backtester driver ni infraestructura aplicada. Si un helper adicional exige otro archivo, proponer delta al mapa al Manager antes de ampliar. Los artefactos de prueba pesados viven fuera del vault; guardar comando/hash/resumen/ubicación portable.

**No tocar:** fórmulas técnicas/económicas ajenas, datos originales, rama backtester, controles TradesGerard, secretos, servicios o cuentas reales, gates futuros. No convertir pools en control de señales.

**Spikes permitidos:** P0-NT (subtarea T2.1, no quinto shot) máximo dos intentos de compile/harness local antes de dictamen; insumos assemblies/API instalada autorizada, source AddOn y dos lanes ficticias. Resultado: API compile/limitación, matriz cinco bindings y prueba contractual callbacks/identity/cancel/replace/restart. Si falta terminal/assemblies, PHYSICAL_NOT_DEMONSTRATED y prohibición de egress, sin fingir PASS. Spike contable local: serializar revisión existente y demostrar mapping de cuenta/contexto/day/causa monotónicos; ausencia de fuente LIVE queda explicitada, no se fabrica. Contradicción API/semántica que invalide arquitectura ⇒ G2 blocked/PLAN_CONFLICT, sin rediseño unilateral.

**Tests y asserts:** R6 §16 (todos); nuevos tests safety/concurrency/causality primero, race + ≥95% nuevo código después. Ejecutar `go test -race -coverprofile=<external-output> ./futures/...` desde v3/sdk sólo tras confirmar ausencia de efectos externos; Core suites explícitas internal/functions/internal/futuresruntime/internal/futuresvertical y bridge paquetes locales seleccionados; vet/staticcheck sobre mismo scope. Tests de integration no pueden alcanzar endpoints reales. Reutilizar harness SDK StateFun y luego builder real; SIM no certifica NT. Añadir tests C# contractuales y compilar si toolchain autorizado presente.

**Entregables/Gate G2:** SHA integrado runtime, handoffs verificables W0–W7, diff, matriz criterio→test ejecutado/comando/cobertura, matriz P0-NT, siete secuencias, findings QA interna y límites físicos. Cada T2.* con owner/handoff/evidencia. G2 review o blocked, nunca accepted; no trasladar obligaciones sin resolver a S04.

**Handoff a Fase 3:** Manager acepta G2 sobre SHA; auditor recibe base/HEAD y comandos reproducibles, no una conclusión de autoaprobación. STOP sin disparar S03.


#### S02 — Matriz obligatoria de submanager y subagentes (decisión posterior del Owner)

**Alcance:** ocho workers one-shot LOCAL GLM bajo un SUBMANAGER LOCAL persistente exclusivamente para S02. No son ocho shots adicionales, no crean gates G5+, no cambian T2.1–T2.8. El submanager registra y revisa cada handoff, integra los cambios y presenta G2; no implementa todo por sí solo. Ningún worker acepta G2. Si el harness no ofrece subagentes directos: SUBAGENTS_UNAVAILABLE, G2 blocked; sin inventar delegación ni volver a ejecución solitaria. No consumir cuota GOD/TOP sin nuevo permiso del Manager.

| Worker | Task y ownership de escritura EXCLUSIVO dentro de R6 §15 | Entrada necesaria | Entrega/test obligatorio |
|---|---|---|---|
| W0 — CONTRATOS | T2.1; spike read-only NTX/AddOn y economía/revisión, sin product mutation | G1 accepted | Freeze de contratos de mensajes, identidad, schema, source revision, P0-NT máximo dos pruebas locales/compile; capacidad real vs no demostrada. |
| W1 — POOL/PROVIDER | T2.2 y provider de T2.4; sdk/futures/pool, sdk/futures/provider, functions/futures_pool_manager.go y futures_provider_rules.go | W0 | Test de claims/afinidad, FIFO/day, policy-fact ingest/restart, stale epochs, exclusividad account-wide y estado serializado; sin PnL/target en PoolManager. |
| W2 — SIGNAL/FANOUT | T2.3; sdk/futures/domain/fanout.go, strategy/fanout.go, functions/futures_signal_fanout.go | W1 claim API | Tests de cursor durable, dedup por asociación a través de rotación/evicción/restart, management del destino anterior, no-target, targets unidos para dos pools. Signal byte-identical. |
| W3 — OPERATION/MM | T2.4; sdk/futures/operation, gerardmm, strategies/tgmm, domain/admission.go, reservation.go, operation.go, functions/futures_operation.go | W0, W1/W2 contratos | MM pin/contexto, policy económico puro, 53/300 y 1/1000, reservation revalidate/epoch, drain proofs y tests de idempotencia. NO escribir provider ni config. |
| W4 — ANALYTICS | T2.5; sdk/futures/analytics, marketctx, strategies/s2, functions/futures_market_analytics.go y futures_strategy_engine.go | W0 contrato observación | Compartir kernels, golden S2 igual, unión demandas Strategy/MM, snapshot causal entre owners/restart, no datos futuros; NO escribir config/views.go. |
| W5 — BRIDGE/NT | T2.6; únicamente futures-bridge allowlist §15 incluyendo NTX y AddOn C# | W0 P0-NT + fence contrato W1/W3 | Harness 2/5 lanes, identidad de cuenta, M2 lost ACK/ambiguous/late fill, cancel/replace y reconexión; API compile si disponible, evidencia PHYSICAL_NOT_DEMONSTRATED si no. |
| W6 — COMPOSICIÓN/INTEGRACIÓN | T2.7 y base T2.8; sdk/futures/config, core/internal/futuresruntime, core/cmd/echo-core, sdk/statefun, source module.yaml; integración/E2E | W1–W5 integrados y revisados | Dispatcher por TypeName/key, bootstrap idempotente, config/RuleSet/MM por cuenta, fixed compatibility, siete secuencias, tests StateFun serializados y 200 cuentas sintéticas. No rediseñar contratos. |
| W7 — QA FRESCA INDEPENDIENTE | T2.8; añadir sólo tests nuevos y reproductores, nunca modificar source productivo | SHA W6 integrado fijado | Pruebas de falsificación R6 §16 sin confiar en tests anteriores: no pausa Strategy, claim conflict, restarts, rotación/signal replay, stale epoch, wrong-account, presupuesto y drenaje físico; findings reproducibles con archivo, comando y salida. No sustituye S03. |

**Orden/dependencias:** W0 primero. W1 y W4 pueden ejecutarse con máximo dos simultáneos únicamente en worktrees/ramas temporales disjuntos, con ownership de paths no solapado y commits independientes; sin aislamiento, delegación SECUENCIAL. W2 depende de W1; W3 depende de W1/W2. W5 ejecuta el harness P0-NT leído en W0 y sólo integra fencing/M2 cuando reciba contratos W1/W3. W6 después de W1–W5 integrados. W7 después de W6, fresh context con SHA exacto. El submanager valida cada diff/test/contrato antes de integrar; rechazos se corrigen por worker con un mandato delimitado. Ningún concurrent writer en un mismo archivo; no merge destructivo, no force-push, no tocar ramas/worktrees ajenos.

**Antes del primer worker:** submanager congela una matriz R6 §16 (AC/invariante → módulo owner → test ejecutable → oráculo independiente → evidencia requerida) y un registro de interfaces compartidas/owner de archivos; asigna IDs W0–W7 y deja estado en este planner. Luego redacta **un prompt exacto one-shot por worker**, con ROLE=NORMAL, SURFACE=LOCAL, WORK_FUNCTION, tarea T2.*, base SHA, archivos permitidos/prohibidos, condiciones de inicio, implementación, test por contrato, criterios PASS/FAIL, evidencia, salida y cierre/feedback Agents-OS. No da libertad para rediseñar arquitectura, cambiar fórmulas ni ampliar scope. Subagentes no subdelegan ni ejecutan otro shot.

**Control de entregas:** para cada worker registrar DESPACHADO → RECIBIDO → REVISADO → INTEGRADO | RECHAZADO | BLOCKED en tareas y bitácora del mismo proyecto, con modelo/superficie reales, commits, SHA base/HEAD, changed-files, pruebas ejecutadas (comando, resultado y artefacto), coverage, limitaciones, readback, agent_run y cierre/feedback si procede. Un worker con tests ausentes no cuenta como integrado; un fallo crítico obliga a corrección/retorno acotado dentro de S02 o G2 blocked. No mantener ocho planificadores competidores ni mentir sobre runs.

**Foco de pruebas:** primero RED/green y tests que falsen invariantes de cuenta única, afinidad, rotación diaria, continuidad de Signal, presupuesto no clipeado, fencing, lost ACK/fill tardío y causalidad distribuida; después coverage >=95% de código nuevo. Test E2E debe atravesar serialización y dispatch reales, no sólo harness in-process. W7 construye nuevos casos negativos como auditor interno distinto del implementador. Submanager vuelve a correr tests integrados y verifica regresiones respecto baseline, no acepta un PASS de unit aislada. Sin E2E físico no declarar LIVE; PHYSICAL_NOT_DEMONSTRATED explícito.

**Handoff worker obligatorio:** WORKER_ID; ROLE/SURFACE/MODEL; TAREA; BASE_SHA; RESULT_SHA; paths; COMMANDS+RESULTS; CRITICAL_ASSERTS; NEGATIVE_TESTS; UNVERIFIED; BLOCKERS; AGENTS_OS_RUN; SESSION_CLOSE; FEEDBACK; STOP. Handoff de submanager al Manager sólo al final de S02: estado W0–W7, matriz AC→evidencia, SHA integrado, tests/coverage/race, bugs corregidos o residuales, límites físicos y G2 review/blocked. Submanager tiene prohibido aceptar G2, iniciar S03, desplegar o enviar órdenes reales.


### Paquete autónomo Fase 3 — S03 GLM adversarial independiente

**Misión exacta:** dictamen read-only de producto S02; buscar violaciones, sin autocorregir ni autoaprobar.

**Precondiciones verificables:** G2 accepted por Manager con SHA exacto; contexto fresco; checkout auditado sobre ese SHA, salida de pruebas fuera del source. Si difiere HEAD, bloquear dictamen hasta fijar artefacto.

**Lectura obligatoria:** `VAULT_ROOT/10-projects/Echo Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md` §12–18; este planner D1–D10, T3.* y evidencia S02; diff base S01→S02 y símbolos §15 involucrados.

**Decisiones cerradas:** requisitos R6; auditor evalúa conformidad, no cambia política ni interpreta gates físicos como PASS lógico.

**Implementación paso a paso:** T3.1 trazabilidad semántica y baseline/delta; T3.2 carreras/replay/causalidad/restart/identidad física; T3.3 reporte priorizado. Repro mínima fuera del árbol si nueva, sin editar source ni tests existentes; no commits de fixes.

**Archivos esperados:** producto no-touch completo; actualizar sólo sección «Evidencia S03»/gate/tareas de este planner en Agents-OS. Snippets/repros persistidos como evidencia pequeña aquí o artefacto externo hasheado, sin segundo planificador.

**No tocar:** código, tests, configuración producto, branch history S02, gates de aceptación, fixes automáticos, backtester, deploy/real egress.

**Spikes permitidos:** reproducir afirmaciones S02 en sandbox; permutación de mensajes/fault injection. Ninguna nueva investigación financiera/física. API NT no disponible se conserva no demostrada.

**Tests y asserts:** replay tras rotation/cache eviction; cuentas aliases/pools cruzados; fenced epoch y revalidación en vuelo; no pausa Strategy por economics; daily return correcto; TypeName registration real; MM modules sellados; cut analítico; foreign/late fills; quiescent falsa y M2 ambiguo. Repetir suite relevante en SHA exacto y distinguir fallas heredadas del delta.

**Entregables/Gate G3:** tabla finding ID/severidad/P0–P3/archivo:símbolo/trigger/observado/esperado/repro/comando/evidencia; cobertura de requisitos y residual físico. Dictamen reproducible CONFORME o REQUIERE_CORRECCIÓN, gate review/blocked; ningún accepted.

**Handoff a Fase 4:** Manager acepta dictamen y fija hallazgos a corregir; GLM S04 recibe IDs/repros/HEAD, sin redescubrir semántica. STOP sin S04.

### Paquete autónomo Fase 4 — S04 GLM corrección

**Misión exacta:** resolver findings S03 aprobados, regresiones e integración local del alcance existente, sin features nuevas.

**Precondiciones verificables:** G3 accepted por Manager con dictamen y scope, runtime HEAD verificado; findings trazables a S02. Si hay cero hallazgos, ejecutar T4.2–3 de integración/evidencia sin inventar cambios.

**Lectura obligatoria:** `VAULT_ROOT/10-projects/Echo Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md` §12–18; findings/repros S03 y mapa §15 sólo para superficies afectadas; este planner T4.*.

**Decisiones cerradas:** D1–D10 y alcance de remediación fijado por Manager; no adoptar funcionalidades nuevas bajo etiqueta fix.

**Implementación paso a paso:** T4.1 reproducir cada defecto antes del fix, corregir mínimo con regresión; T4.2 integración/race/coverage relevante; T4.3 SHA final/matriz resueltos/residual/readback y gate. No merge a master ni deploy por inferencia.

**Archivos esperados:** modify sólo archivos §15 implicados en findings y create tests de regresión en paquetes correspondientes; evidencia y gate en este planner. Cambios fuera del mapa/semántica requieren Manager.

**No tocar:** nuevas funcionalidades, backtester y sus controles, implementación de un quinto shot, infra/cuentas reales, aceptación G4.

**Spikes permitidos:** reproducción local necesaria de un finding, acotada a su hipótesis; contradicción de arquitectura ⇒ blocked al Manager, no nueva exploración.

**Tests y asserts:** cada repro S03 falla antes/pasa después; no romper siete secuencias R6; integration source completo; cobertura nueva ≥95% con safety first; física desconocida sigue reportada separada.

**Entregables/Gate G4:** SHA final runtime, commits/finding, tests/regresiones/coverage, residual y matriz real de evidencia física, readback Agents-OS, review/blocked. No autoaccepted, sin deploy.

**Handoff final:** Manager revisa G4; Owner decide egress cuando corresponda. Termina este plan de cuatro shots; no quinta fase automática.

## Despachos congelados

**Despacho Fase 1**
```text
FASE_ASIGNADA=1
PAQUETE_CANONICO=Paquete autónomo Fase 1
GATE_REQUERIDO=none; mandato Owner S01
TAREAS=T1.1-T1.3
SALIDA=R6, branch/base, planner, validación, cierre S01
STOP=G1 review|blocked; prohibido iniciar S02
```

**Despacho Fase 2**
```text
FASE_ASIGNADA=2
WORK_FUNCTION=SUBMANAGER_IMPLEMENTACION_LOCAL_OBLIGATORIO
SUBAGENTS=GLM_ONE_SHOT_W0_W7_OBLIGATORIOS
PAQUETE_CANONICO=Paquete autónomo Fase 2
GATE_REQUERIDO=G1 accepted por Manager
TAREAS=T2.1-T2.8
SALIDA=SHA integrado + handoffs W0–W7, matriz de comportamiento probado, QA fresca, límites físicos
STOP=G2 review|blocked; prohibido iniciar S03 o desplegar
```

**Despacho Fase 3**
```text
FASE_ASIGNADA=3
PAQUETE_CANONICO=Paquete autónomo Fase 3
GATE_REQUERIDO=G2 accepted por Manager sobre SHA
TAREAS=T3.1-T3.3
SALIDA=dictamen adversarial reproducible, findings, residual
STOP=G3 review|blocked; prohibido corregir o iniciar S04
```

**Despacho Fase 4**
```text
FASE_ASIGNADA=4
PAQUETE_CANONICO=Paquete autónomo Fase 4
GATE_REQUERIDO=G3 accepted por Manager y scope findings
TAREAS=T4.1-T4.3
SALIDA=SHA corregido, regresiones, evidencia final
STOP=G4 review|blocked; prohibido autoaceptar/desplegar/quinto shot
```

## Definition of Done y handoff

S01: rama aislada exacta y producto intacto; diseño A–H cerrado y límites físicos declarados; cuatro paquetes completos, tareas/gates/despachos coherentes; schema/plan/refs ejecutados; readback y commit/push; cierre/feedback de esta sesión. No significa G1 accepted. Alcance final: requisitos §16 verificables en implementación, fixes S03 resueltos o bloqueo explícito, trazabilidad a SHA y evidencia; residual de certificación física independiente de aceptación de código, egress Owner-gated.

Handoff común obligatorio: base SHA, source SHA, rama/worktree relativo, estado tracked/untracked, tareas/gate, comandos ejecutados y resultados reales, evidence refs, decisiones aplicadas, hallazgos/residual, próximo actor. Nunca declarar PASS de prueba no ejecutada.

## Evidencia S01 y cierre

- Source: inspección localizada de archivos/símbolos §15 en d74b6525; presupuesto TGMM y single-account NT comprobados en fuente; no tests de producto ni pruebas físicas ejecutadas.
- `python3 80-agents/skills/agents-os-implementation-planning/scripts/validate_plan.py <este-proyecto>`: phases=4/gates=4/dispatches=4/local_refs=4/errors=0/warnings=0. Reconciliación adicional: 17 tareas únicas (3+8+3+3), sin quinto shot.
- `python3 80-agents/skills/agents-os-entity-lifecycle/scripts/lint.py --strict <diseño> <planner> <log> <feedback> <agent_run>`: ERROR=0/WARN=0, cinco notas. Padre: lint estricto NO PASS (5 defectos históricos); función canónica lint_note comparada contra parent@00caab0d confirma baseline=5/current=5/new=0. No se saneó historia no solicitada.
- Referencias R6: expansión de paths con braces y comprobación de existencia en worktree d74b6525: 65 existentes y 11 create explícitos, cero paths inexistentes sin marcar. Referencias VAULT_ROOT resueltas por validate_plan. Query enfocada por ruta/título confirma fuente canónica; Graphify CLI no disponible, no se declara index PASS.
- `git diff --check`: sin defectos de whitespace. Producto: status --porcelain=v1 --untracked-files=all vacío, diff base vacío; HEAD=origin/master=origin/feature/ef-runtime-pools=d74b652500e673fc2bf4289f9f195f11960ba26e. Push rama exitoso y ls-remote confirma master/feature en el mismo SHA. Checkout original conserva 3596fc48daab93d58d29ab658f371f40e76f3e55 y estado limpio. Sin archivos Go/C#/test/script/config modificados por S01.
- Readback de Agents-OS: contenidos diseño/planner/gate/puente/closeout comprobados en master local y snapshot remoto al cierre; cron generó commits intermedios, no fueron alterados. Identificar snapshot final con `git log -1 --format=%H -- main/10-projects/Echo\ Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md` desde raíz repo o historial del diseño; SHA final comunicado al Manager. El validador mecánico no certifica arquitectura ni comportamiento de producto.
- Cierre explícito autorizado: `agents-os-session-close` por delta sobre este proyecto/diseño + change_log; no cerrar Manager ni Echo Futures; `agents-os-session-feedback` solicitado. Agent run aplicable por auditoría material de código que produjo contrato implementable (task_type planning), sin claim de coding generado. No L0/L1 duplicados ni checkpoint interno paralelo al proyecto.

## Evidencia S02

**Paso 0 del submanager (2026-10-16):** baseline verificado — worktree `/home/kor/go/src/github.com/xKoRx/echo-runtime-pools`, branch `feature/ef-runtime-pools`, HEAD `d74b652500e673fc2bf4289f9f195f11960ba26e`, status limpio, sin drift; G1 `accepted` vigente en este planner. Subagentes directos disponibles (Agent tool local, modelo GLM-5.3-Flash); delegación OBLIGATORIA activa. Build baseline `go build ./v3/sdk/... ./v3/core/... ./v3/futures-bridge/...` EXIT=0. Test baseline (salida fuera de producto, registro aquí): `sdk/futures/config` FAIL TestTGFilterSharedTypedLiveBacktestFactoryParity; `core/internal/functions` FAIL TestEconomicMinimumCoreTypedConfigAndProtectionParity; `core/internal/futuresvertical` FAIL TestBTGS05PublicFiniteExecutionDifferential, TestFuturesVertical_UnknownManualPosition, TestFuturesVertical_ThreePathSplitAtTheHarnessSeam; bridge paquetes ok; resto sdk/futures ok. Estos 5 fallos son la **línea base heredada** (d74b6525 limpio): regresión nueva = cualquier FAIL distinto. Toolchain C# y assemblies NinjaTrader ausentes en host ⇒ P0-NT contratado como inspección + matriz, resultado esperado `PHYSICAL_NOT_DEMONSTRATED` (sin fingir compile).

**Matriz AC congelada (R6 §16 → owner → oráculo):**

| AC | Invariante | Owner módulo | Oráculo independiente |
|---|---|---|---|
| A Continuidad Strategy | pausa de cuenta nunca detiene evaluación/timers/indicadores | W4+W6 | señal y strategy_eval_seq byte-idénticos pre/post pausa; sin rewarmup |
| B Rotación diaria | C01→C04 misma sesión; retorno día siguiente a más antigua propia | W1+W6 | PAUSED sólo por AccountAvailability de autoridad; orden FIFO (created_at,id); trade cerrado sin pausa no rota |
| C Concurrencia | sin doble claim account-wide; pools solapados serializados | W1 | permutaciones: ≤1 claim activo/cuenta, ≤1 ACTIVE/asociación; perdedor prueba siguiente candidata |
| D Afinidad | cuenta de A jamás a B (release/rollover/restart/config) | W1 | AFFINITY_MISMATCH en todo claim cruzado; epoch tombstone conservado |
| E Fanout | señal consumida no re-ejecuta tras rotación; no-target decidido; CLOSE al ciclo correcto | W2 | 0 deliveries duplicados por asociación; decisión journalizada con causa; cursor avanza sin target |
| F Riesgo | 53/300 y 1/1000 sin recorte/rechazo por remanente; breach real efecto | W3 | presupuesto solicitado = R exacto; sin rama headroom; PAUSE≠terminal; day reset no borra latch |
| G Recovery | crash en claim/install/activate/pause/fence/drain/release; lost ACK; late fill | W1+W3+W5 | misma solicitud re-enviada no crea segundo epoch; release bloqueado con incertidumbre; late fill refuta drenaje y reabre cuenta original |
| H Analytics | kernels una vez, corte causal entre owners, golden S2 intacto | W4 | S2 byte-identical; MM consume observación publicada, no recomputa; unión demandas sin multiplicar por cuenta |
| I Gateway físico | 5 bindings distinguibles; comando↔callback cuenta exacta; cancel/replace/restart sin contaminación | W5 | matriz command→account→ACK/fill→M2 contractual; SIM≠físico; lane reconnect no adopta cuenta por runtime ID |
| J Integración | registro único por TypeName, bootstrap idempotente, E2E atraviesa componentes | W6 | roundtrip ValueSpecs; 7 secuencias §13; 200 cuentas sintéticas; legacy fixed compat |

**Registro de workers W0–W7** (DESPACHADO→RECIBIDO→REVISADO→INTEGRADO | RECHAZADO | BLOCKED), modelo GLM-5.3-Flash, superficie LOCAL, one-shot:

| Worker | Tarea | Estado | Base→Result SHA | Tests/evidencia |
|---|---|---|---|---|
| W0 | T2.1 contratos + P0-NT | **INTEGRADO** | d74b6525→doc vault `S02-W0-CONTRACT-FREEZE.md` sha256 d0296352…3f7a (850 líneas); producto intacto (status limpio verificado) | freeze revisado contra R6 §12B–§15 por submanager; OQ(1–3) adoptadas (pairing EconomicMinimumV1→V2 en TGMM unclipped; ResumeBoundary=account_day_id; LastFactRevision por (account,context)); P0-NT: matriz contractual 5 bindings + PHYSICAL_NOT_DEMONSTRATED, 0/2 intentos (sin toolchain C#/assemblies en host); 0 PLAN_CONFLICT |
| W1 | T2.2+provider T2.4 | **INTEGRADO** | d74b6525→`32d86ed1` (18 archivos, +6610/−12; allowlist exacta verificada por submanager) | verificación independiente: build EXIT=0; pool 27/27 PASS; provider PASS; race pool+provider PASS; únicos fallos = 2 baseline heredados; spot-check invariantes (affinity@primer permiso admission.go:91, epoch++ sólo claim nuevo engine.go:545, stale ack absorbido); coverage pool 94.3% stmt (justificado, brazos defensivos), reportado; decisiones W1 registradas (campos additive PoolState/OwnerState read models; release sin Drain fabricado; egress provider→pool con tabla account→pools para W6) |
| W4 | T2.5 analytics | **INTEGRADO** | 32d86ed1→`c9d1740d` (14 archivos, +2280/−244; allowlist verificada; fixtures_test.go sin delta final) | verificación independiente: analytics+s2+tg PASS, functions con único fallo baseline; race 4 paquetes PASS; spot-check: strategies/s2 sin matemática propia (delegaciones puras a analytics/s2, "zero math here"), detector AST activo, fallo explícito sin fallback en camino pool; golden S2 intacto (tests preexistentes sin ajustar); coverage nuevo 99–100% (excepciones justificadas: ramas defensivas); residual semántico reportado: resolución de parámetros en unión de demandas = última declaración por identidad (pin S09 ring=96) — a ratificar por Manager; nota OwnerState: libro de demandas viaja en wrapper aditivo, SHA certificado byte-idéntico (re-fijación futura sugerida) |
| W2 | T2.3 fanout | **INTEGRADO** | c9d1740d→`cdddb56c` (6 archivos, +2222/−17; allowlist exacta; delta constants = 2 líneas autorizadas) | verificación independiente: build OK; strategy+domain PASS; race strategy PASS; functions con único fallo baseline; tests W2 ejecutidos en suite completa (replay tras rotación, evicción de TriggerDedup absorbida por watermark, merge sin borrar ajenos, gestión por ciclo al destino histórico, Signal byte-identical, legacy path intacto); residual registrado: ACCOUNT_FACTS_UNAVAILABLE/ASSOCIATION_DISABLED quedan como vocabulario reservado sin path de entrada en freeze v1 (modo→causa MANAGE_ONLY⇒ASSIGNMENT_DRAINING, NO_TARGET⇒NO_ELIGIBLE_ACCOUNT) — a ratificar por Manager |
| W3 | T2.4 operation/MM | **INTEGRADO** | cdddb56c→`26c2c5c6` (16 archivos; allowlist exacta; delta constants = 3 líneas autorizadas) | verificación independiente: build OK; operation/gerardmm/tgmm PASS; race operation PASS; tests clave re-ejecutados: TestEntryBudgetUnclippedConservesBudgetOverPositiveFloor (53/300→300), …1000OverFloorOne (1/1000→1000), breach real bloquea (ambos MM), decision tables AccountPolicy; roundtrip byte-estable install→…→drain; coverage nuevo 96–100% (2 bloques defensivos justificados); decisiones W3 registradas para W5/W7: fence viaja como OrderCommand.FenceEpoch additive (CommandKind intactos), ACK vía pool.Input{AssignmentAck}, entries nunca-publicados bajo fence convergen por rechazo provider-gate (drain no se wedgea); GerardMMDef vive en config/ ⇒ política como campo JSON en gerardmm.Config + validación pura módulo |
| W5 | T2.6 bridge/NT | **INTEGRADO** | 26c2c5c6→`ea8d86b9` (21 archivos, +3525/−305, todos bajo v3/futures-bridge; RuntimePoolContractTests.cs creado NO compilado) | verificación independiente: build OK; bridge 14/14 paquetes PASS (suite completa, sin fallos); race session+core PASS; spot-check: fence persistido antes de ACK (TestFencePersistsAcrossReopen/Monotonic/IOFailures), expansivo post-revocación absorbido con causa (absorb-before-send), cancel/replace reductivo pasa; guard .cs anti-cuenta-única activo; PHYSICAL_NOT_DEMONSTRATED (compile AddOn 0 intentos sin toolchain, terminal real); coverage nuevas funciones session 98–100% (I/O journalfs justificado); semántica marker-exact del fence documentada (INSTALL limpia a 0) para W7 |
| W6 | T2.7 composición + base T2.8 | DESPACHADO | ea8d86b9→ | — |
| W2 | T2.3 fanout | pending | — | — |
| W3 | T2.4 operation/MM | pending | — | — |
| W4 | T2.5 analytics | pending | — | — |
| W5 | T2.6 bridge/NT | pending | — | — |
| W6 | T2.7 composición + base T2.8 | pending | — | — |
| W7 | T2.8 QA falsificación | pending | — | — |

Orden delegación: W0 → W1 → W4 → W2 → W3 → W5 → W6 → W7 (secuencial; sin aislamiento de worktrees disjuntos, máximo 1 writer simultáneo sobre producto). Cada worker commitea su trabajo en la rama; submanager verifica diff/allowlist/tests ANTES de aceptar el commit como integrado. **Delta de orquestación del submanager (sin ampliar mapa §15):** W1 crea additivamente las filas Config/EXTEND de `v3/sdk/futures/config/snapshot.go` (PoolDef/PoolAssociationDef/ValidateAssociationIdentity + campos ConfigSnapshot/AccountDef + validación referencial) y `v3/sdk/futures/operation/account_policy.go` verbatim del freeze W0 §1.10 (interface pura sin integración en engine), porque W3/W6 consumen ambos y la delegación es secuencial; todo permanece dentro del allowlist §15 y del freeze W0. W6 hereda config y no reescribe lo validado por W1.

## Evidencia S03

Pendiente ejecución independiente tras G2 accepted; ningún dictamen atribuido.

## Evidencia S04

Pendiente corrección tras G3 accepted; ningún fix atribuido.

## 📆 Bitácora

- 2026-10-16 — S01: bootstrap una vez, R5 y límites fuente seleccionados; master remoto d74b6525, branch/worktree limpio. Diseño R6 y paquetes congelados para Manager, sin producto editado ni siguiente shot iniciado.

- 2026-10-16 — Manager G1: `accepted` sobre R6/plan, después de verificar en GitHub base/branch sin delta, AS-IS, paquetes/gates y cierre S01. S02 queda autorizado en rama runtime con pruebas aisladas; no acceso a trading LIVE, despliegue ni cuentas reales. P0-NT/economía LIVE siguen no demostrados. Antes de S02 revisar HEAD y cambios concurrentes, sin reset. No se ejecutaron tests de producto desde esta revisión.

- 2026-10-16 — Owner cambió S02 tras G1: obligatoriedad de SUBMANAGER LOCAL + W0–W7 GLM one-shot y QA interna; anterior prompt GLM solitario superseded. Cuatro shots/gates, 17 tareas, G1 accepted y G2 pending sin implementación iniciada.

## Sesión S01 cerrada

Cierre explícito ejecutado mediante agents-os-session-close por delta: diseño/planner/puente + [[2026-10-16-echo-futures-runtime-pools-s01]], sin duplicación de continuidad interna. Feedback ejecutado y persistido en [[2026-10-16-echo-futures-runtime-pools-session-feedback]]; evaluación material de source registrada en [[2026-10-16-codex-gpt-6-runtime-pools-s01]]. No se cierra Manager ni proyecto Echo Futures, no S02, no gate accepted. Próximo actor Manager; por favor gracias.
