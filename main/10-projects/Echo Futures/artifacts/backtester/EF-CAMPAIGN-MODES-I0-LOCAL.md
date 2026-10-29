---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[EF-CAMPAIGN-MODES-DESIGN]]"
  - "[[Echo Futures — Optimización de Campañas]]"
  - "[[EF-S04-INTEGRATION-RECONCILIATION]]"
aliases:
  - "Echo Futures — Mandatos Go-only C06"
tags:
  - kind/doc
created: "2026-10-28"
updated: "2026-10-29"
---

# EF-CAMPAIGN-MODES-I0-LOCAL

## Propósito

**C06 GO-ONLY — paquete vigente GO-S02, GO-S03 y GO-S04.** Se conserva el path histórico para que los agentes existentes resuelvan la continuidad sin otro planner. I0 Python y todos sus prompts/merge gates quedan SUPERSEDED_FOR_DELIVERY por la instrucción Owner del 29-10-2026. No ejecutar ni mergear `feature/ef-campaign-modes-i0` como producto final. Sus retornos siguen siendo evidencia histórica, no permisos nuevos.

GO-S01 es el diseño/plan de la sesión manager actual. A continuación hay exactamente **tres shots locales**: implementación, revisión adversarial y correcciones. Cada uno puede usar workers internos finitos y especializados; esos workers no son managers permanentes ni cambian la autoridad del Owner. Ejecutar sólo el shot despachado, no los tres de una vez.

Diseño único: [[EF-CAMPAIGN-MODES-DESIGN]] C06. Planner único y plan detallado: [[Echo Futures — Optimización de Campañas]], W0–W6/R01–R12/A01–A16. Mandato funcional: [[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]]. I+D conserva selección/economía; Runtime Pools/R6/SDK y retester conservan contratos/gates. Este paquete no es otra SPEC.

La copia íntegra del paquete Python anterior se conserva byte-idéntica como `artifacts/backtester/history/EF-CAMPAIGN-MODES-I0-LOCAL-before-C06.txt` (blob `c08e8992ce27cb0491366bb18f1c4c4768b97220`), sólo histórico no operativo.

## Contenido

### Contrato común de los tres shots

- Bootstrap vigente `xKoRx/agents-os/master`, `main/AGENTS.md`, vault `main/`; leer por routing, no reconstruir la historia completa. Skills necesarias: technical-project-manager como handoff, sdd-workflow/sdd-developer y autoridades retester/qualification del alcance. Workers cargan agents-os-agent-run-register cuando aplique, agents-os-session-feedback y agents-os-session-close.
- Producto `xKoRx/echo`. Source observado master `2baf319ddcba622d9557bc9f23a13787b44c58a7`; ref I0 `01a38c13b0a1b280eefb9d18f6d2b167e3cd8739` es sólo histórico. Rama propuesta `feature/ef-campaigns-go`, desde master reconciliado. Resolver refs/worktrees/WIP realmente, sin reset/force/stash destructivo ni tocar trabajo ajeno.
- Leer Echo AGENTS.md, CONSTITUTION.md, v3/backtester/README.md, reglas SDD08/09, specs/SPECS.md y change owner. Source/tests ejecutables prevalecen sobre comentarios viejos. No asumir cambios locales/SHAs que no se observaron.
- Owner define Go-only, tres modalidades, módulos reutilizables, NQ, USD4000 caja conjunta/cero aportes/reinversión100% net received, payout variable y reglas por perfil, sin caps financieros propios. Los instrumentos, términos y umbrales de producción no se investigan ni redefinen por este mandato.
- G0–G5 y S04-F01/F02 se conservan por alcance. Cada escenario económico real requiere identidad, datos, horizonte, profile, gates y budget. Tests funcionales Go no son certificación estadística, de prop o LIVE. FUNDED-only no hereda un pase challenge de otro MM; D05 no se salta.
- Go como autoridad de Campaign/economía y reporting. No puerto literal de Python, no intérprete embebido, wrappers a scripts, Python fallback, segunda lógica de Strategy/MM/Provider, otro scheduler/bankroll service/DSL/framework. Reusar owners existentes y documentar cambios realmente necesarios.
- La capa oficial que se entrega incluye lifecycle y ejecución, no sólo métricas. Una corrida conjunta tiene mercado/reloj/scheduler y caja únicos, no suma de runs independientes. Una activa por asociación, muchas asociaciones posibles.
- Ningún agente puede autorizar su propio merge/release/deploy/LIVE, cambiar las reglas para obtener verde o decir que ejecutó todas las estrategias cuando sólo validó catálogo. Manager y programa permanecen abiertos.
- Recursos: una entrega finita por shot, workers con scope/inputs/Allowed Files/output, un integrador, presupuesto global del supervisor vigente para motores de investigación (hasta seis incluidos oráculos, con recursos medidos). Paralelismo de desarrollo no equivale a concurrencia de motores. Sin polling/vigilancia indefinida ni multiplicar configuraciones por rutina.
- Cada subagente devuelve ID real/modelo/surface/rol, path/SHA, tests realmente ejecutados, límites, activos reutilizables y feedback o NONE. Si el host no puede delegar, no inventar subagentes ni trabajar silenciosamente como supuesto orquestador; devolver dependencia de capacidad. No sustitución de modelos sin registrar la discrepancia.
- Agents-OS master, sin ramas/PR/force. Sólo el orquestador escribe su retorno/agent-run/change_log y propone el delta del planner; no writers concurrentes sobre el diseño/planner. Usar materializador/validadores vigentes para notas nuevas, rutas vault relativas. Si publicación falla, conservar bytes/localizadores y marcar NOT_PUBLISHED; readback sólo cuando realmente observado. Consumo Pro confirmado o UNKNOWN. Cerrar únicamente worker/shot, no programa/manager.

### GO-S02 — implementación Go-only (activar ahora)

```text
# ECHO FUTURES — GO-S02: IMPLEMENTACIÓN GO-ONLY DE CAMPAÑAS

ROLE: TOP por función de submanager de implementación; modelo GLM-5.3-Flash
por instrucción Owner explícita. Registrar identificador efectivo del host.
SURFACE: LOCAL (Hefesto/checkout autorizado).
WORK FUNCTION: orquestador temporal + integrador de implementación.
EXECUTION MODEL: ONE-SHOT con subagentes implementadores GLM-5.3-Flash
frescos y especializados, por olas y archivos disjuntos.

/goal
Entregar IMPLEMENTATION_CANDIDATE de la capacidad completa C06:
CHALLENGE, FUNDED y SIMULATION Go; Strategy/MM reutilizables; N cuentas y
rotación; composición causal multi-asociación/multi-perfil con caja única;
economía/evidencia/KPI Go; tooling/admisión/runner Go; migración legacy
trazable y retiro de Python del flujo oficial. No entregar únicamente un
reporter Go ni presentar una configuración como otra implementación Campaign.

/authorities
Ejecutar íntegramente el contrato común de este paquete.
Leer EF-CAMPAIGN-MODES-DESIGN C06 y el planner único Optimización de Campañas,
especialmente W0–W6, R01–R12 y A01–A16. No usar el diseño Python de C05 como
arquitectura vigente. No crear otro manager, planner o diseño.

/baseline
Master source observado 2baf319ddcba622d9557bc9f23a13787b44c58a7.
Crear o reconciliar feature/ef-campaigns-go desde el master real verificado.
La rama I0 Python no se integra ni es base. Recuperar módulos S04, fixtures,
catálogos y receipts sólo como referencia de compatibilidad y casos.
Si master avanzó, revisar delta material antes de fijar BASE_SHA efectivo.
No tocar cambios ajenos ni restaurar archivos para fingir árbol limpio.

/execute
1. W0: inventariar entrypoints/consumidores Python, owners Go y rutas de
   ejecución; fuente/catálogo/89 IDs de referencia y aliases; estado S04-F01
   y guard F02; congelar SPEC/PLAN/TASKS/Allowed Files antes de programar.
2. Despachar workers por W1 economía/contratos, W2 lifecycle+perfiles,
   W3 composición/runtime-routing y W4 CLI/admisión/migración. No asignar el
   mismo archivo a dos writers. Sólo avanzar una dependencia cuando su
   artefacto/commit esté integrado y probado; paquetes de worker frescos,
   objetivos verificables, no instrucciones vagas de "hazlo escalable".
3. Usar los tipos monetarios y owners del SDK, PlatformCampaign, registro de
   cuentas, controles, scheduler, dataset/analytics y factories actuales.
   Concentrar las decisiones técnicas ordinarias en el integrador; no pedir
   al Owner confirmar cada helper ni inventar defaults económicos faltantes.
4. Extender semántica por versión: legacy intacto por identidad/replay,
   nueva Campaign configurable. Resolver perfil global/RuleSet por binding,
   callbacks account-scoped y camino de mercado común sin otro engine.
   Pausa/rotación de cuenta nunca pausa/recrea Strategy. No simular varias
   asociaciones alternando un puntero global sin routing de sus efectos.
5. Caja Go única en SIMULATION: 4000 iniciales, cero aportes, pagos netos
   recibidos reinvertidos; reservas, provisión, adquisición/activación,
   retrasos, pérdidas y reversos conciliados. Nominal PnL nunca se deposita.
   La evidencia del productor identifica linaje y aplicación real; reporting
   deriva sin reinterpretar ni convertirse en checkpoint del motor.
6. CLI oficial Go y admisión común en todas las rutas run/resume/batch.
   Portar lo necesario del supervisor, sin dos owners simultáneos. Inventario
   Python con disposición por consumer y pruebas del reemplazo; no conservar
   Python ejecutable bajo otro nombre/carpeta como dependencia oficial.
7. Migrar configuraciones, no reescribir historia. Cada source→target lleva
   SAME_SEMANTICS demostrado o NEW_EXPERIMENT. V1/Unclipped y ResearchCash
   histórico no se renombran silenciosamente. No añadir ClutiFX entero.
8. W5: matriz funcional de todas las identidades admitidas, E2E por los tres
   modos y composición conjunta, dos MM y dos perfiles, sin Python instalado.
   Investigación histórica sólo donde los gates y inputs concretos lo permiten;
   registrar bloqueos fila por fila, no forzar trades ni cambiar señales.
9. W6: integrar un candidato único, documentar comandos realmente disponibles,
   hashes/receipts, coverage, capacidad y dependencias. No mover master.

/verify
R01–R12 y A01–A16 trazados a pruebas/receipts o estado explícito.
Pruebas Go nuevas y regresiones SDK/runtime/backtester afectadas; cobertura
>=95% del desarrollo nuevo, críticos primero. No ocultar deuda baseline.
Go-only se prueba en entorno sin Python en build/test/CLI/guard/report oficial,
no sólo buscando imports. Inspectar el proceso real de prepare/run/report y
resume/reproduce, outputs completos y dinero causal. Cero eventos de negocio
duplicados. SOURCE/BUILD/TEST/E2E/QUALIFICATION/ECONOMIC_RESULT separados.
Fixture positivo debe producir entrada/salida/fills/round-trip y lifecycle,
no sólo exit 0. Multi-prop funcional puede usar perfiles TEST_ONLY declarados;
no equivale a validar reglas comerciales actuales.

/stop
PLAN_CONFLICT por contradicción material con C06/R6; BLOCKED_DATA o
BLOCKED_QUALIFICATION sólo en el alcance afectado. No lanzar históricos para
resolver falta de spec. Preservar el resto del trabajo; no entregar stubs como
completo ni autoabrir otro shot. No merge/deploy/gasto/trading.

/return
Publicar EF-CAMPAIGN-MODES-GO-S02-RETURN.md en el directorio artifacts/backtester
existente, siguiendo contrato canónico. Incluir STATUS, BASE_SHA, BRANCH,
CANDIDATE_SHA, BUILD_ID, DIFF_SCOPE, REUSE_MAP, PYTHON_DISPOSITION, GO_ONLY,
R01_R12_MATRIX, LEGACY_MIGRATION_MATRIX, EXECUTION_MATRIX, GATES_PER_IDENTITY,
TEST_COMMANDS_RECEIPTS, COVERAGE, PERFORMANCE_MEASURED, NOT_EXECUTED, UNKNOWN,
REUSABLE_ASSETS, SUBAGENT_RECEIPTS, AGENTS_OS_PATHS_SHA, PRO_CHAT_POOL_DELTA.
Estado IMPLEMENTATION_CANDIDATE sólo para lo realmente entregado; de lo
contrario PARTIAL/BLOCKED con lista material y checkpoint exacto.
Cargar run-register/feedback/session-close; cierre exclusivo de este shot.
NEXT: GO-S03 sobre CANDIDATE_SHA exacto; no ejecutarlo por tu cuenta.
```

### GO-S03 — revisión adversarial GOD local (sólo contra retorno y SHA S02)

```text
# ECHO FUTURES — GO-S03: GOD LOCAL / REVISIÓN ADVERSARIAL GO-ONLY

ROLE: GOD.
MODEL: GPT-6 Astra o identificador real correspondiente en el host; no
simular independencia de modelo. SURFACE: LOCAL.
WORK FUNCTION: submanager temporal de revisión adversarial.
EXECUTION MODEL: ONE-SHOT, contexto fresco, producto READ_ONLY.
GOD razona/adjudica el review y manda a ejecutar a subagentes reales:
Luna para inventario, comprobaciones mecánicas, recopilación/reproducción;
Sol para tests/harness Go, causalidad, contratos y falsificación compleja.
No es el Primary Manager ni implementa correcciones de producto.

/goal
Intentar falsificar el candidato C06 completo con evidencia LOCAL, y devolver
VERIFY_PASS/FINDINGS/BLOCKED. No es otra investigación de arquitectura y no
aprueba merge, campañas económicas fuera de gates ni producción.

/authorities
Contrato común de este paquete, diseño C06, planner W0–W6/R01–R12/A01–A16,
GO-S02-RETURN, SDD y contratos runtime/R6/retester vigentes.
Descubrir capacidades/modelos de delegación reales del host antes de despachar.
Luna no decide semántica financiera; Sol no reemplaza autoridad Owner.

/baseline
Resolver BASE_SHA/CANDIDATE_SHA/branch del retorno S02 publicado y verificar
remoto+árbol+diff. Si falta el retorno o SHA, NOT_DISPATCHED/BLOCKED; no revisar
master por sustitución ni confiar en la última rama abierta. Producto/tests
del autor READ_ONLY; harness/fixtures propios fuera de su working tree.

/execute
1. Reconstruir sólo llamadas reales y fuente necesaria para cada riesgo:
   Strategy/MM factories→driver→pools/Provider/accounting→Campaign→report→CLI.
   Detectar funciones duplicadas, segunda caja, runtime alternativo o Python
   escondido en shell, Make, go generate, CI, datasets, qualification o resume.
2. Delegar review independiente por frentes: A economía/linaje/idempotencia;
   B market-clock/account-routing/claims/RuleSets/MM parity; C migración/admisión/
   tooling Go-only; D E2E física/capacidad/abort/resume. Un owner por harness,
   ningún escritor del producto. Paquetes finitos con source SHA y esperado
   derivado del contrato, no helpers/expected del autor.
3. Falsificar al menos: dos demandas por última caja; payout pendiente que
   intenta financiar; free/paid reset y unidad; cargo pagado no provisionado;
   fees netos/activación; reverso y doble emisión; same RunID/different attempt;
   control encolado vs aplicado; evento futuro/latencia de observación;
   dos cuentas long/short bajo un mercado; dos MM simultáneos sin contaminar
   estado; rotación con órdenes/reservas activas; RuleSet ajeno; venue callback
   dirigido a cuenta incorrecta; legacy con V1 distinto; resume/batch bypass.
4. Ejecutar el CLI Go real sin Python con un pequeño input determinista que
   atraviese engine/Strategy/MM/Provider/fills/Campaign y reporte; comparar con
   un oráculo independiente. Repetir replay/failure recovery y coste atribuido.
   No sustituir owners productivos por mocks para anunciar E2E.
5. Comprobar matriz completa de migración/ejecuciones: 89 es referencia de
   catálogo, no 89 estrategias independientes ni 89 históricos realizados.
   Verificar todos los bloqueos/gates declarados; no autorizar G5 sin G4.
6. Revisar maintained surface, contracts versionados y deprecación real.
   Tests/coverage/mismo failure set no prueban verdad económica por sí solos.
   La modificación necesaria del adapter Go no es razón para pedir otro
   engine; interfaces especulativas deben tener consumidores concretos.
7. Devolver findings con prioridad/impacto/caso reproducible/source locator,
   minimal repair y autoridad. Refutar explícitamente falsificadores que no
   sostienen defecto. Cero P1/P2 abiertos para VERIFY_PASS.

/verify
A01–A16 deben tener receipts o NOT_EXECUTED/UNKNOWN justificados. Separar pruebas
funcionales de cualificación/rentabilidad. GOD revisa el trabajo de subagentes;
no suma PASSs sin leer contraejemplos y límites. No cambiar reglas/presets/
fuentes para arreglar defectos. Preservar corpus y hashes del verificador.

/return
EF-CAMPAIGN-MODES-GO-S03-RETURN.md con STATUS, EXACT_REVIEWED_SHA, REVIEW_MATRIX,
FINDINGS, REPRO_HARNESS_MANIFEST, INDEPENDENT_E2E, GO_ONLY, LEGACY/PARITY,
MODEL_AND_EXECUTION_INDEPENDENCE, RESOURCE_RECEIPTS, NOT_EXECUTED/UNKNOWN,
REUSABLE_ASSETS, SUBAGENT_RETURNS, AGENTS_OS_PATHS_SHA, PRO_CHAT_POOL_DELTA.
Cada finding queda como WITHIN_SPEC_CORRECTION o NEEDS_OWNER_DECISION.
Los primeros pueden ser entrada de S04; los segundos bloquean sólo la
corrección afectada hasta adjudicación del manager. No corregir producto ni
autoarrancar S04. Cerrar sólo review/workers; programa y manager abiertos.
```

### GO-S04 — corrección GLM local TOP y cierre del entregable

```text
# ECHO FUTURES — GO-S04: CORRECCIÓN Y GATE FINAL GO-ONLY

ROLE: TOP por mandato Owner para el corrector/submanager local.
MODEL: GLM-5.3-Flash efectivo, no GPT-6 Sol por inferencia del rol.
SURFACE: LOCAL. EXECUTION MODEL: ONE-SHOT con workers implementadores por owner
cuando sea necesario, un integrador y un worker fresco para retest que no haya
escrito los cambios críticos. No es el manager del programa.

/goal
Resolver findings aceptados GO-S03 y cerrar la implementación Go completa con
FINAL_SHA y evidencia. La capacidad final son campañas reales del backtester,
no un reporte traducido. Cero Python en el camino oficial entregado.

/authorities
Contrato común, C06, planner, SPEC/PLAN/TASKS efectivos, retornos S02 y S03 y
adjudicación del manager. Aplicar run-register/feedback/session-close.
Cargar el corpus del verificador intacto y su manifiesto de checksums.

/baseline
Base: SHA exacto revisado en S03; rama de producto GO-S02. Reconciliar HEAD/WIP.
No reparar otro SHA ni fusionar cambios ajenos sin revisión del delta.
Sin S03 o findings materiales que contradigan C06 no adjudicados: bloquear
la parte afectada; no adivinar reglas económicas ni otro diseño.

/execute
1. Traducir findings WITHIN_SPEC_CORRECTION a tareas/Allowed Files por owner.
   Clasificar root causes compartidas para corregir en el dueño Go, no agregar
   parches Python ni divergencia runtime/backtest. No reimplementar módulos.
2. Aplicar correcciones mínimas manteniendo contracts legacy y nuevos scopes.
   No mover expected/fixtures del verificador para obtener verde. TCR sólo con
   evidencia de oráculo equivocado y aprobación aplicable; registrar intent.
3. Promover a regresiones Go los falsificadores durables. Preservar los bytes
   originales del harness independiente y ejecutar ese corpus contra FINAL_SHA.
   Corregir defectos ordinarios adicionales dentro del mismo scope, no iniciar
   un ciclo de microfixes sin presupuesto ni ocultar fallos restantes.
4. Integrar y ejecutar gate completo: módulos Go afectados/paridad runtime,
   unit/integration/E2E/campaign paths, Go-only sin Python, migración exhaustiva,
   lifecycle de los tres modos, una SIMULATION conjunta con competencia de
   caja, múltiples perfiles y señales opuestas; replay/failure recovery;
   restricciones qualification en run/resume y exporters no autoritativos.
5. Ejecutar pruebas de datos reales sólo en el alcance/gates/budget admitidos;
   no confundir ese estudio con fixtures funcionales. Entregar por fila
   qué configuración se migró/validó/corrió/no corrió y por qué. Cero promesas
   de "todas ejecutadas" basadas en compilación o configuración.
6. Revisar diff final y documentos: comandos reales, decisiones/versiones,
   sin código Python/dependencia oficial, cobertura>=95% del desarrollo nuevo,
   capacidad medida, no secretos/receipts mutados, sin nueva arquitectura.
7. Publicar candidato FINAL_SHA en rama con readback. No merge a master,
   release/deploy, compras ni LIVE. La aceptación final pertenece al Owner.

/verify
No READY_FOR_OWNER_REVIEW con P1/P2 abiertos, stubs, R01–R12 omitidos ni Python
necesario. No inferir PASS de pruebas no ejecutadas. Identificar si un bloqueo
es de producto, datos, gate comercial o herramienta. Un histórico bloqueado
no invalida por sí solo la mecánica Go demostrada, pero tampoco cuenta como
estrategias evaluadas. Conservar invariantes y arquitectura KISS de C06.

/return
EF-CAMPAIGN-MODES-GO-S04-RETURN.md: STATUS, BASE/REVIEWED/FINAL_SHA, DIFF_SCOPE,
FINDINGS_DISPOSITION, R01_R12/A01_A16, GO_ONLY_PROOF, MIGRATION/EXECUTION_MATRIX,
FINAL_GATE_RECEIPTS, INDEPENDENT_CORPUS_RESULTS, COVERAGE, PERFORMANCE,
S04_F01_F02/D05_REMAINING, NOT_EXECUTED/UNKNOWN, RELEASE_ROLLBACK,
REUSABLE_ASSETS, SUBAGENT_RECEIPTS, AGENTS_OS_PATHS_SHA, PRO_CHAT_POOL_DELTA.
Estado final READY_FOR_OWNER_REVIEW o PARTIAL/BLOCKED con causa exacta. No
programar un quinto shot automáticamente. Cerrar sólo este shot y sus workers;
el manager y el programa Echo Futures permanecen abiertos.
```

## Fuentes

Decisión Go-only del Owner en este turno; [[EF-CAMPAIGN-MODES-DESIGN]] C06; planner único; FUT-R01 y contratos del repo Echo. Presupuestos y gates de investigación siguen los runbooks vigentes; no confundirlos con autorización de producción.
