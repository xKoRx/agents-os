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

S01 completado para revisión del Manager; G1 `review`, **READY_FOR_MANAGER_REVIEW** condicionado a readback/validación registrados abajo. S02 no iniciado ni autorizado. Proyecto sigue activo; sesión S01 se cierra por mandato Owner, sesión Manager y proyecto Echo Futures siguen abiertos. Próxima acción: Manager revisa R6, acepta o rechaza G1 y prepara el prompt S02. Ningún agente acepta su gate ni ejecuta el siguiente shot.

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

Cuatro contextos/shot como contrato Owner. S02 concentra la implementación en ocho tareas ordenadas; no se divide en nuevos shots/gates. Su mayor carga está en concurrencia/wiring y fixtures, no en operaciones reales. S03 es independiente y read-only; S04 sólo hallazgos, regresión e integración local. Ningún despliegue se traslada silenciosamente: certificación física/egress posterior requiere autorización Owner y queda reportada como obligación no ejecutada, fuera de estos cuatro shots. Si S02 no completa su alcance, entrega G2 blocked en lugar de pasar deuda escondida a S04.

| Gate | current state | phase agent responsibility | owner acceptance evidence | enables |
|---|---|---|---|---|
| G1 | review | GOD S01 entrega diseño/rama/paquetes/validaciones y cierra sólo S01 | Pendiente Manager, sin autoaceptación | S02 sólo tras accepted |
| G2 | pending | GLM S02 entrega implementación/fixtures/limitaciones verificadas en review o blocked | Pendiente Manager sobre SHA exacto | S03 sólo tras accepted |
| G3 | pending | GLM S03 entrega dictamen reproducible sin autocorregir en review o blocked | Pendiente Manager sobre hallazgos | S04 sólo tras accepted |
| G4 | pending | GLM S04 entrega fixes/tests y residual explícito en review o blocked | Pendiente Manager; egress real requiere Owner aparte | Fin del plan, no quinto shot |

## ✅ Tareas

Cada ítem define objetivo | archivos/símbolos | precondición | implementación | tests | evidencia. Estado [x] significa trabajo S01 realizado, no aceptación del gate.

- [x] T1.1 Preparar rama | Git producto | checkout/refs inspeccionados | fetch y crear desde SHA exacto en worktree aislado | rev-parse/status/diff | base=HEAD y estado limpio. #owner/agent
- [x] T1.2 Cerrar diseño | R6 §12–18 y símbolos §15 | R5/contratos | auditoría localizada y resolución técnica | matriz requisitos/source refs | autoridad actualizada, sin producto editado. #owner/agent
- [r] T1.3 Validar y cerrar S01 | este planner, log/feedback/run | T1.1–2 | validadores/readback/commit/push/cierre | schema/plan/refs/Git | G1 review + evidencias cierre. #owner/agent
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

Lee bootstrap canónico una vez y el paquete ASIGNADO de este proyecto. Usa diseño R6 como autoridad única y revisa sólo símbolos allowlisted §15; no reconstruyas historia ni controles TradesGerard. Resuelve worktree desde echo-go-workspace y verifica branch/base/HEAD/cleanliness antes de tocarlo; preserva WIP ajeno. Una sola fase por contexto y sin subagentes salvo mandato futuro explícito. HEAD/code → contratos → reports; nunca tests/interfaces como prueba física. Invariantes: Signal intacta, Strategy siempre técnica, MM/Provider únicos dueños económicos, PoolManager sólo selección/facts, afinidad permanente, exclusividad account-wide, cursor anti-replay, drenaje/fence, no migración MMState/PnL, analytics compartido causal y NinjaTrader dummy. Respeta mandato sin egress real. Toda tarea progresa en esta nota; evidencia portable y SHA exacto. Test failure no se oculta cambiando tests/expectativas: nueva regresión y finding; cualquier cambio legítimo de test requiere motivo trazable a R6. Fuera de allowlist o semántica contradictoria ⇒ PLAN_CONFLICT/Gn blocked al Manager. No force-push ni reset/stash/clean. Ningún agente acepta su gate ni inicia otro shot. Devuelve gate review/blocked, evidencia ejecutada, límites y STOP.

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

### Paquete autónomo Fase 2 — S02 GLM implementación

**Misión exacta:** implementar íntegramente R6 aprobado en branch runtime, tests/evidencia local; no operación real.

**Precondiciones verificables:** G1 accepted por Manager en esta tabla con referencia de aceptación; HEAD descendiente de base S01, worktree propio; ningún drift no atribuido. Leer contrato del ambiente antes de cualquier acceso físico.

**Lectura obligatoria:** este proyecto decisiones/tasks/gates; `VAULT_ROOT/10-projects/Echo Futures/artifacts/runtime/ECHO-FUTURES-RUNTIME-POOL-DESIGN.md` §12–18; repository AGENTS/CONSTITUTION y reglas de módulos/config/tests; source exacto §15 por tarea. No reabrir fuentes de campañas excepto seam declarado.

**Decisiones cerradas:** D1–D10, en especial distinguir account policy de TerminationIntent y clamp por piso de otras reglas de MM.

**Implementación paso a paso:** ejecutar T2.1→T2.8 en orden. Antes de implementation económica verificar schema y provenance de accounting.Revision; preparar reducers/facts primero, luego fanout/ejecución, analytics, gateway y composición. Mantener atomicidad state+egress y probar restart antes de integrar. Registrar work-in-progress en este planner.

**Archivos esperados:** modify/create exactos R6 §15; nuevos tests runtime_pool_test.go por paquete; ningún archivo de backtester driver ni infraestructura aplicada. Si un helper adicional exige otro archivo, proponer delta al mapa al Manager antes de ampliar. Los artefactos de prueba pesados viven fuera del vault; guardar comando/hash/resumen/ubicación portable.

**No tocar:** fórmulas técnicas/económicas ajenas, datos originales, rama backtester, controles TradesGerard, secretos, servicios o cuentas reales, gates futuros. No convertir pools en control de señales.

**Spikes permitidos:** P0-NT (subtarea T2.1, no quinto shot) máximo dos intentos de compile/harness local antes de dictamen; insumos assemblies/API instalada autorizada, source AddOn y dos lanes ficticias. Resultado: API compile/limitación, matriz cinco bindings y prueba contractual callbacks/identity/cancel/replace/restart. Si falta terminal/assemblies, PHYSICAL_NOT_DEMONSTRATED y prohibición de egress, sin fingir PASS. Spike contable local: serializar revisión existente y demostrar mapping de cuenta/contexto/day/causa monotónicos; ausencia de fuente LIVE queda explicitada, no se fabrica. Contradicción API/semántica que invalide arquitectura ⇒ G2 blocked/PLAN_CONFLICT, sin rediseño unilateral.

**Tests y asserts:** R6 §16 (todos); nuevos tests safety/concurrency/causality primero, race + ≥95% nuevo código después. Ejecutar `go test -race -coverprofile=<external-output> ./futures/...` desde v3/sdk sólo tras confirmar ausencia de efectos externos; Core suites explícitas internal/functions/internal/futuresruntime/internal/futuresvertical y bridge paquetes locales seleccionados; vet/staticcheck sobre mismo scope. Tests de integration no pueden alcanzar endpoints reales. Reutilizar harness SDK StateFun y luego builder real; SIM no certifica NT. Añadir tests C# contractuales y compilar si toolchain autorizado presente.

**Entregables/Gate G2:** SHA commits/push runtime, diff inventory, matriz tests→requisito con comandos/resultados y coverage, matriz P0-NT, siete secuencias, limits físicos y residual, G2 review o blocked. No omitir una obligación S02 para delegarla a S04. No accepted.

**Handoff a Fase 3:** Manager acepta G2 sobre SHA; auditor recibe base/HEAD y comandos reproducibles, no una conclusión de autoaprobación. STOP sin disparar S03.

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
PAQUETE_CANONICO=Paquete autónomo Fase 2
GATE_REQUERIDO=G1 accepted por Manager
TAREAS=T2.1-T2.8
SALIDA=SHA implementación runtime, pruebas, matriz física, límites
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
- Validación documental: pendiente registro de ejecución final abajo. El validador mecánico no certifica arquitectura ni comportamiento de producto.
- Cierre explícito autorizado: `agents-os-session-close` por delta sobre este proyecto/diseño + change_log; no cerrar Manager ni Echo Futures; `agents-os-session-feedback` solicitado. Agent run aplicable por auditoría material de código que produjo contrato implementable (task_type planning), sin claim de coding generado. No L0/L1 duplicados ni checkpoint interno paralelo al proyecto.

## Evidencia S02

Pendiente ejecución por GLM tras G1 accepted; ninguna ejecución atribuida.

## Evidencia S03

Pendiente ejecución independiente tras G2 accepted; ningún dictamen atribuido.

## Evidencia S04

Pendiente corrección tras G3 accepted; ningún fix atribuido.

## 📆 Bitácora

- 2026-10-16 — S01: bootstrap una vez, R5 y límites fuente seleccionados; master remoto d74b6525, branch/worktree limpio. Diseño R6 y paquetes congelados para Manager, sin producto editado ni siguiente shot iniciado.
