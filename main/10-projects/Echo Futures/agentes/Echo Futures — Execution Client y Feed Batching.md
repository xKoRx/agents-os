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
progress: 0
repo: "xKoRx/echo"
jira:
prs:
aliases: []
tags:
  - kind/project
  - area/echo
created: "2026-10-20"
updated: "2026-10-20"
---

# Echo Futures — Execution Client y Feed Batching

## 🎯 Objetivo

Entregar dos cambios coordinados: (1) procesamiento por lote sin serialización masiva por evento ni pérdida de durabilidad; (2) Execution Client NinjaTrader con el patrón común de capabilities, colas y batch de MT4/MT5, Bridge sin negocio, barras nativas completas y ticks ALL/LAST configurables. Una sola autoridad funcional/técnica: [[EXECUTION-FEED-BATCHING-DESIGN]]. Matriz de evidencia: [[EXECUTION-FEED-BATCHING-VERIFICATION]].

## 📊 Estado actual

**READY_FOR_S01 / NO_IMPLEMENTATION_YET — 2026-10-20.** Owner pidió crear proyecto, diseño y despacho de implementación; este manager congela FEFB V1 para ese encargo. S1 está autorizado exclusivamente para desarrollo/pruebas aisladas; G1–G3 pending. Los gates pertenecen a ESTE proyecto, no a Runtime Pools. No hay pruebas de producto ni deploy realizados por esta preparación documental.

Base leída: `112ccccdbbf32bc3ca486fd04a28ab0afa0451a4`, rama `feature/ef-runtime-pools`. Antes de ejecutar, revalidar HEAD y avances concurrentes, sin reset ni rebase. Este proyecto absorbe el trabajo pendiente de capacidad/cliente de RESUME-06; [[Echo Futures — Runtime Pools]] conserva la autoridad histórica y la certificación CERT-NT-01. No ejecutar ambos frentes sobre los mismos archivos simultáneamente. No modificar backtester ni sus controles.

Parent humano: [[Echo Futures]]. Primary Manager: esta conversación con KoR. Submanager LOCAL obligatorio en S1 con workers GLM one-shot; S2 es auditor fresh-context read-only; S3 corrige hallazgos adjudicados. El manager acepta cada gate y emite el despacho siguiente. Owner conserva permisos de operación física.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| xKoRx/echo | feature/ef-runtime-pools | 112ccccdbbf32bc3ca486fd04a28ab0afa0451a4 | [[EXECUTION-FEED-BATCHING-DESIGN]] §§1–7 | misma, §§8–12 | Pendiente S1; no rama nueva de producto creada aquí |
| xKoRx/agents-os | master | HEAD concurrente, no force | Mandato Owner 2026-10-20 | Este plan + diseño | Documentación; sin ramas/PRs |

## Decisiones y límites

D1–D10 del diseño están CONFIRMED para implementación; no preguntas de producto bloqueantes. S1 decide nombres/símbolos dentro de los módulos autorizados y documenta mapping legacy→extendido, no inventa otro diseño. Default ALL; flush50ms independiente de window. SnapshotIntervalMs legacy no se reutiliza para 50ms. No garantías de exactly-once de terminal ni pérdida imposible de datos externos.

Fuera de alcance: deploy/arming, cuentas reales o SIM compartidas, más infra, bus/servicio nuevo, fork StateFun, sharding de un stream, fórmulas de trading, muestreo silencioso, salto de offsets y reescritura MT. No borrar checkpoints. Runtime y backtester convergen después mediante contratos/fixtures, sin paralizar la rama de investigación.

## Roadmap, carga y gates

Tres shots/gates globales, no cinco fases implícitas. S1 carga alta: dos líneas de producto y su integración, delegadas con ownership acotado. S2 carga media-alta: pruebas de falsificación y capacidad. S3 carga según findings: corrección y regresión, sin nuevas funciones. No promesa temporal ni despachos automáticos al completar una fase.

| Gate | current state | Responsabilidad del agente | Aceptación | Habilita |
|---|---|---|---|---|
| G1 | pending | S1 entrega implementación íntegra/evidencias, review o blocked | Sólo Primary Manager sobre SHA exacto | S2 |
| G2 | pending | S2 entrega dictamen independiente, incluso si encuentra defects | Sólo Primary Manager adjudica findings y scope | S3 |
| G3 | pending | S3 entrega correcciones + verificación final, review o blocked | Sólo Primary Manager; no equivale a LIVE | Nueva certificación operativa por mandato separado |

## ✅ Tareas

- [x] T1.1 Congelar mapping de contratos, ownership y baseline; inspeccionar SDK pinneado y superficie MT/NT real. Dep: mandato Owner. #owner/agent #type/dev #area/echo — DONE S1 2026-10-20: baseline verificado (HEAD=origin=112ccccd, limpio, sin RESUME-06 concurrente), validadores PASS, tarea puente agregada al padre, SDK v3.3.0 inspeccionado (sin hook fin-de-request; unidad transaccional = request HTTP), anexo T1.1 con contratos C1–C6 y ownership W1–W4 en el diseño.
- [ ] T1.2 Implementar lote Core, semántica estado/efectos/retry y medición con estado maduro; representación compacta sólo si necesaria. Dep: T1.1. #owner/agent #type/dev #area/echo
- [ ] T1.3 Extender configuración/negociación común, colas/sender NT, ALL y LAST independientes de flush. Dep: T1.1. #owner/agent #type/dev #area/echo
- [ ] T1.4 Implementar cierres/revisiones nativos por timeframe, cobertura/backfill y única autoridad. Dep: T1.3. #owner/agent #type/dev #area/echo
- [ ] T1.5 Integrar Bridge dummy, ACK durable/routing Kafka preservando batch, orden, ejecución M2 y legacy. Dep: T1.1, T1.3. #owner/agent #type/dev #area/echo
- [ ] T1.6 Conectar config→cliente→Kafka→Core→analytics; tests de pérdida/retry/compatibilidad y compilación NT aislada. Dep: T1.2, T1.4, T1.5. #owner/agent #type/dev #area/echo
- [ ] T1.7 Validar AC01–AC16, capacidad/recuperación, cobertura y entregar G1 sobre SHA publicado. Dep: T1.6. #owner/agent #type/dev #area/echo
- [ ] T2.1 Fijar candidato G1 accepted y reconstruir alcance/evidencia independientemente. Dep: G1. #owner/agent #type/pr-review #area/echo
- [ ] T2.2 Crear ataques de batching, persistencia, orden, huecos, sampling, memoria y parámetros; comparar baseline. Dep: T2.1. #owner/agent #type/pr-review #area/echo
- [ ] T2.3 Reproducir capacidad/gates y publicar dictamen G2 con reproductores durables, sin fixes. Dep: T2.2. #owner/agent #type/pr-review #area/echo
- [ ] T3.1 Corregir sólo hallazgos adjudicados por Manager y preservar reproductores. Dep: G2. #owner/agent #type/dev #area/echo
- [ ] T3.2 Regresión completa, capacidad, restore/migración y compilación aislada sobre SHA final. Dep: T3.1. #owner/agent #type/dev #area/echo
- [ ] T3.3 Publicar entrega final, instalación/rollback y G3 review; cierre propio sin deploy. Dep: T3.2. #owner/agent #type/dev #area/echo

## Orquestación interna de S1

Submanager no implementa todo solo. Hace preflight T1.1, asigna contratos y coordina cuatro workers GLM fresh-context, cada uno ONE-SHOT sin subdelegación. Máximo dos simultáneos, sólo con worktrees y paths disjuntos; sin aislamiento, secuencial. El submanager integra mecánicamente y devuelve correcciones acotadas al owner del código antes de G1. Ningún resultado se acepta por su resumen verbal.

| Worker | Ownership exclusivo | Encargo y handoff |
|---|---|---|
| W1 Core | market_stream, estado/serialización de market y tests | T1.2; no tocar cliente ni config compartida; prueba partición de batch, rollback y capacidad |
| W2 Cliente/contratos | ClientConfig/extensión feed acordada, C# AddOn y fixtures contrato | T1.3–T1.4; common schema fijado antes de W3; ALL/LAST, outbox, barras/reconexión, compile completo aislado |
| W3 Bridge/routing | bridges/adaptadores/messaging wiring y tests | T1.5; consume contratos W2, conserva M2 y legacy, ACK tras publicación, sin negocio |
| W4 Integración/QA interna | composición, manifiestos source, analytics serving y nuevos tests de integración | T1.6–T1.7; después de W1–W3; no redefine contratos ni borra asserts para PASS |

Interfaz compartida se acuerda en T1.1 con un único writer. W1 y W2 pueden arrancar en paralelo; W3 tras contrato W2; W4 después de integrar W1–W3. Cambios de representación afectan a W1 y al replay de W4, coordinados. S2 sigue siendo independiente aunque W4 haga QA interna.

Registrar cada worker DESPACHADO→RECIBIDO→REVISADO→INTEGRADO|RECHAZADO|BLOCKED con modelo/superficie, base/commit, paths, comandos/exit/evidencias, límites, cierre y feedback. Sin subagentes reales disponibles: SUBAGENTS_UNAVAILABLE, no sustituir por ejecución solitaria. No usar GOD/TOP sin mandato nuevo.

## Paquetes autónomos

### Paquete autónomo Fase 1 — IMPLEMENTAR

**Misión exacta:** implementar ambos frentes FEFB V1 en la rama runtime, con transporte completo y persistencia segura, sin deploy.
**Precondiciones verificables:** bootstrap, repo y baseline; documento de diseño/validación presente; worktree sin dirty ajeno; subagentes disponibles; tests aislados de ETCD/Kafka compartidos.
**Lectura obligatoria:** `VAULT_ROOT/10-projects/Echo Futures/artifacts/execution-feed-batching/EXECUTION-FEED-BATCHING-DESIGN.md` y `VAULT_ROOT/10-projects/Echo Futures/artifacts/execution-feed-batching/EXECUTION-FEED-BATCHING-VERIFICATION.md`; prompt S1; source mínimo de §10 y Environment Contract.
**Decisiones:** D1–D10 congeladas. Inspección SDK/mapping no es otra fase de diseño. Guardar addendum de símbolos/contratos, sin alternativas interminables.
**Implementación paso a paso:** T1.1 primero; W1/W2; W3 tras contrato; W4 e integración; devolver defectos internos al especialista; completar AC01–AC16.
**Archivos esperados:** allowlist §10, fixtures/pruebas en owners actuales y docs de instalación; un ownership por path.
**No tocar:** infra compartida, cuentas, código/rama backtester, matemática de Strategy/MM, M2, fuentes ajenas, master de producto.
**Spikes permitidos:** inspección SDK3.3.0 e API NT instalada/compile aislado; probar antes de inventar hooks. Bloqueo material de arquitectura vuelve al Manager.
**Tests y asserts:** AC01–AC16, rojo→verde en defectos, bitácora fuente/commit; >=95% código nuevo tras pruebas críticas; suites de baseline comparadas por causa, no conteo.
**Entregables/Gate:** SHA publicado, diff, contratos aplicados, pruebas/coverage/race/capacidad, límites NT, G1 review o blocked. Código ausente no se transfiere silenciosamente a S3.
**Handoff:** snapshot mínimo en este planner + matriz de evidencia; cerrar subagentes/submanager con Agent-OS, STOP hasta Manager. No aceptar G1.

**Despacho Fase 1**
```text
FASE_ASIGNADA=1
WORK_FUNCTION=SUBMANAGER_IMPLEMENTACION_LOCAL
PAQUETE_CANONICO=Paquete autónomo Fase 1
PROMPT=EXECUTION-FEED-BATCHING-S01-PROMPT
TAREAS=T1.1-T1.7
ENTRADA=mandato Owner + diseño FEFB V1 + baseline 112ccccd
SALIDA=G1 review|blocked; SHA y AC01-AC16
STOP=S2 no iniciado; sin deploy
```

### Paquete autónomo Fase 2 — VERIFICAR ADVERSARIALMENTE

**Misión exacta:** falsar el candidato S1 sin corregir producto ni confiar en conclusiones del implementador.
**Precondiciones verificables:** G1 accepted por Manager y SHA fijo; checkout aislado; originales intactos.
**Lectura obligatoria:** `VAULT_ROOT/10-projects/Echo Futures/artifacts/execution-feed-batching/EXECUTION-FEED-BATCHING-DESIGN.md` y `VAULT_ROOT/10-projects/Echo Futures/artifacts/execution-feed-batching/EXECUTION-FEED-BATCHING-VERIFICATION.md`; evidencia S1 y diff completo.
**Decisiones:** D1–D10; no autorizar approximate/ALL mezclado ni interpretación nueva de persistencia.
**Implementación paso a paso:** T2.1 comparar baseline; T2.2 tests propios en copia; T2.3 dictamen y artefactos. Un finding no cancela el resto salvo riesgo.
**Archivos esperados:** sólo reproductores NUEVOS en sandbox aislado + evidencia/planner; source productivo read-only.
**No tocar:** tests existentes/expectativas, rama runtime, terminal/cuentas/infra. No auto-fix ni subdelegación.
**Spikes permitidos:** inyección de fallo/transporte en sandbox, replay de datos existentes, parser NT/StateFun real aislado.
**Tests y asserts:** pérdida de ACK, Kafka parcial, crash antes/tras reply, mutable effects, evicción/cache entre keys, barras ausentes/revisadas, native-vs-derived, cierre simultáneo, consumidor incompatible con LAST y legacy min100; carga con productor independiente, estados maduros y recuperación, no sólo throughput vacío.
**Entregables/Gate:** dictamen CONFORME_EN_ALCANCE|REQUIERE_CORRECCION|BLOQUEADO; Fxx con severidad/requisito/source/repro/esperado-observado. G2 review o blocked, nunca accepted. Separar gap físico y defecto.
**Handoff:** tests clasificados PERMANENT_REGRESSION/E2E_CANDIDATE/HARNESS_TOOLKIT_CANDIDATE/DISPOSABLE_REPRODUCER, hashes/rutas durables; cierre y feedback propios; Manager adjudica S3.

**Despacho Fase 2**
```text
FASE_ASIGNADA=2
WORK_FUNCTION=VERIFICADOR_INDEPENDIENTE_LOCAL_ONE_SHOT
PAQUETE_CANONICO=Paquete autónomo Fase 2
GATE_REQUERIDO=G1 accepted por Manager
TAREAS=T2.1-T2.3
SALIDA=dictamen + reproductores + G2 review|blocked
STOP=sin fixes; S3 no iniciado
```

### Paquete autónomo Fase 3 — CORREGIR Y CERRAR ENTREGA

**Misión exacta:** corregir findings adjudicados, demostrar regresión y preparar candidato final, no desplegarlo.
**Precondiciones verificables:** G2 accepted como dictamen + lista de findings autorizados; SHA de auditoría y worktree identificados.
**Lectura obligatoria:** `VAULT_ROOT/10-projects/Echo Futures/artifacts/execution-feed-batching/EXECUTION-FEED-BATCHING-DESIGN.md`, `VAULT_ROOT/10-projects/Echo Futures/artifacts/execution-feed-batching/EXECUTION-FEED-BATCHING-VERIFICATION.md` y reproductores S2 completos.
**Decisiones:** ninguna funcional nueva. Resolver defectos del fix dentro de S3; contradicción real vuelve a Manager, no quinto shot automático.
**Implementación paso a paso:** T3.1 rojo→verde preservando oráculos; T3.2 suites integradas/restores/carga; T3.3 diff contra baseline y candidato, release manifest y docs.
**Archivos esperados:** owners de findings y sus tests; matriz evidencia; instalación actualiza una sola clase NT en perfil aislado.
**No tocar:** features nuevas, políticas monetarias, deploy/egress y runtime ajeno. No eliminar tests para PASS ni convertir deuda material en residual menor.
**Spikes permitidos:** sólo reproducción/medición que los findings requieran.
**Tests y asserts:** AC01–AC16 finales en SHA exacto, >=95% desarrollo nuevo, race, compatibilidad MT, serde batch, ACK durable, barras gap/recovery, sostenida ALL50ms y compile aislado. Límites físicos explícitos.
**Entregables/Gate:** candidato final publicado, G3 review o blocked; no merge ni READY_FOR_LIVE.
**Handoff:** cierre/feedback/agent_run propios, estado seguro intacto; Manager decide aceptación y próximo mandato CERT-NT.

**Despacho Fase 3**
```text
FASE_ASIGNADA=3
WORK_FUNCTION=IMPLEMENTADOR_CORRECTIVO_LOCAL_ONE_SHOT
PAQUETE_CANONICO=Paquete autónomo Fase 3
GATE_REQUERIDO=G2 accepted como dictamen + findings adjudicados
TAREAS=T3.1-T3.3
SALIDA=SHA final + evidencia + G3 review|blocked
STOP=sin merge/deploy; no cerrar al Manager
```

## Evidencia por fase

S1: NOT_RUN. S2: NOT_RUN. S3: NOT_RUN. Fuente leída y planificación no equivalen a implementación. La matriz tiene campos para registrar cada ejecución atribuible y separar compile/SIM/laboratorio/terminal real.

## 📆 Bitácora

- 2026-10-20 — Owner solicita nuevo proyecto completo y diseño de batching + Execution NT. Manager crea esta autoridad, diseño, matriz de pruebas y prompt S1; no toca producto ni CERT-NT desplegado. Tres fases congeladas; documentación registrada en master de Agents-OS. Validación documental y readback constan en [[2026-10-20-echo-futures-execution-feed-batching-created]].
- 2026-10-20 — S1 submanager (GLM-5.3-Flash, LOCAL) ejecuta preflight T1.1: baseline `112ccccd` revalidado (local=origin, worktree limpio, cero ejecutores RESUME-06 concurrentes); `validate_plan` PASS en vault real (phases=3 gates=3 dispatches=3 errors=0) y linter canónico sin hallazgos en las notas FEFB; tarea puente única agregada a [[Echo Futures]] preservando historia; SDK StateFun Go v3.3.0 inspeccionado en module cache (request=un batch de UN address, error descarta request completa, sin hook fin-de-request → lote por invocación es el camino obligatorio); anexo T1.1 congelado en el diseño (mapping símbolos, contratos C1–C6, ownership W1–W4, notas de verificación). Despacho W1+W2 en paralelo a continuación.

## 🧭 Decisiones

D1–D10 en el diseño. Serialización no se difiere a una cola externa; sí outbox durable para transporte del cliente. El lote no pierde eventos; LAST es otra política. No ampliar scope por cumplimiento cosmético de cobertura ni repetir las auditorías históricas. No corresponde cierre de la sesión del Manager.

## 🔗 Docs / Links

[[EXECUTION-FEED-BATCHING-DESIGN]] · [[EXECUTION-FEED-BATCHING-VERIFICATION]] · [[EXECUTION-FEED-BATCHING-S01-PROMPT]] · [[Echo Futures]] · [[Echo Futures — Runtime Pools]].
