---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[EF-CAMPAIGN-MODES-DESIGN]]"
  - "[[Echo Futures — Optimización de Campañas]]"
  - "[[EF-S04-INTEGRATION-RECONCILIATION]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-28"
updated: "2026-10-28"
---


# EF-CAMPAIGN-MODES-I0-LOCAL

## Propósito

Paquete concreto de implementación del primer incremento de campañas bajo el manager y planner existentes. C04 incorpora las precisiones Owner y la revisión SOURCE de reutilización/composición; la instrucción vigente pide este mandato ajustado antes de confirmar despacho. Este artefacto fija alcance/base/presupuesto; no ejecuta código ni acepta S04 por estar en master.

## Contenido

**Estado post-S2 2026-10-29:** I0-S1 IMPLEMENTATION_CANDIDATE en `feature/ef-campaign-modes-i0@b964e13d` (base `2baf319d`). I0-S2 FINDINGS (4×P1 + 6×P2 +1×P3), SOURCE/receipt remoto verificado, harness LOCAL reportado. I0-S3 READY_FOR_DISPATCH/NOT_EXECUTED con manager adjudication más abajo; GOD-COMPOSITION sigue reservado. S04-F01 semántica pendiente y guard S04-F02 no portado; manager/programa abiertos.

**Fuente de verdad de diseño:** [[EF-CAMPAIGN-MODES-DESIGN]], revisión C04. **Planificador único:** [[Echo Futures — Optimización de Campañas]]. **Reconciliación:** [[EF-S04-INTEGRATION-RECONCILIATION]]. No se crea otro planner, manager, DSL o motor.

| Shot | Outcome | Recurso y presupuesto | Gate |
|---|---|---|---|
| I0-S1 | Contrato/report opt-in y recibo focal S04 | Ejecutor GLM LOCAL existente, un writer, ≤150 min | IMPLEMENTATION_CANDIDATE; sin campañas |
| I0-S2 | Intento independiente de falsificar el reporter | TOP LOCAL fresco, ≤90 min | VERIFY_PASS/FINDINGS/BLOCKED; no arregla producto |
| I0-S3 | Corrección aceptada y gate completo | GLM LOCAL fresco, ≤120 min | READY_FOR_OWNER_REVIEW; no autoaceptación |
| Reserva 4 — GOD-COMPOSITION | Adjudicar primera decisión Go real de composición, cuando su incremento sea concreto | GOD, LOCAL sólo si evidencia local necesaria, ≤90 min | Dictamen/delta mínimo; no código ni despacho automático |

Los presupuestos son límites de trabajo de estos encargos; no son límites prudenciales del modelo económico. Recursos concretos del host se miden antes de una eventual campaña futura. En I0 el límite de motores es cero.

### Próximo prompt preparado — I0-S1, cuando el Owner confirme su despacho

```text
# ECHO FUTURES — I0-S1: CONTRATO Y REPORTE ECONÓMICO DE CAMPAÑAS

ROLE: NORMAL
MODEL: GLM-5.3-Flash, identificador efectivo registrado por el host.
SURFACE: LOCAL, Hefesto, mediante el ejecutor existente.
WORK FUNCTION: implementador del slice I0 y recuperación focal de evidencia.
EXECUTION MODEL: ONE-SHOT, contexto fresco. No eres manager ni quien acepta el gate. Un writer de producto; no lanzar subagentes en este shot.

/goal

Entregar IMPLEMENTATION_CANDIDATE de I0: un contrato/reporte económico opt-in que proyecte evidencia existente sin lanzar motores y corrija F01/F02 de C02. Recuperar en la misma pasada la evidencia focal S04-F01/F02; no rehacer la integración.

Estado inicial CONTINUATION. Salidas: IMPLEMENTATION_CANDIDATE, PARTIAL o BLOCKED con causa exacta. S04, implementación I0 y aceptación Owner son ejes independientes; no fabricar PASS para avanzar.

/authorities

Bootstrap xKoRx/agents-os/master, vault main/, entrada main/AGENTS.md. Cargar por routing technical-project-manager como contrato de handoff, sdd-workflow, sdd-developer, echo-retester-master y qualification runbook. Leer agents-os-agent-run-register, agents-os-session-feedback y agents-os-session-close.

Planner único: main/10-projects/Echo Futures/agentes/Echo Futures — Optimización de Campañas.md.
Mandato funcional: main/10-projects/Echo I+D/artifacts/FUT-R01/FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION.md.
Contrato corregido: main/10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-DESIGN.md, revisión C04.
Hallazgos SOURCE: main/10-projects/Echo Futures/artifacts/backtester/EF-S04-INTEGRATION-RECONCILIATION.md.
Review original: main/10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-REVIEW.md.
Este despacho: main/10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-I0-LOCAL.md.

En xKoRx/echo: AGENTS.md, CONSTITUTION.md, .agents/rules/08-sdd-governance.md, .agents/rules/09-sdd-phase-permissions.md, catálogo SDD y v3/backtester/README.md. Resolver la feature existente FEAT-CHALLENGE-HISTORY antes de materializar el change de I0. Runtime/R6 conserva autoridad técnica; I+D conserva selección y decisiones económicas.

/baseline

Repo producto correcto: xKoRx/echo.
Base SOURCE observada: 2baf319ddcba622d9557bc9f23a13787b44c58a7.
S04 ancestro: ae1b09bc10370806f7648f076c5fa0825c9efa4e.
Merge existente: 2188ac3e23d4e4a73ca0edb9aad952029deec951; padres 347eee8bdab7f7628629af6383d1e45520815abd y ae1b09bc10370806f7648f076c5fa0825c9efa4e.

SOURCE está demostrado. BUILD/TEST son EXECUTOR_REPORTED; informe independiente completo no recuperado por CLOUD. No repetir merge, resetear ni recrear trabajo.
Resolver checkout, ramas y WIP del ejecutor. Reusar rama correcta del slice si existe. Si no existe, crear feature/ef-campaign-modes-i0 desde la base exacta; no tocar WIP ajeno. Un descendiente se usa sólo tras reconciliar delta y registrar base efectiva; una diferencia material devuelve PLAN_CONFLICT.
La aceptación semántica completa de S04 está abierta; el source puede servir para el reporte derivado aislado, sin acreditar sus resultados ni habilitar campañas.

PRIOR_ARTIFACTS:
- Decisiones Owner y C04: ACCEPTED_INPUT como requisitos del slice descriptivo; decisiones D01–D06 conservan estado explícito.
- C02 F01–F03: ACCEPTED_INPUT para reparación.
- SOURCE master/catalog/manifest: ACCEPTED_INPUT para inspección; equivalencia histórica UNREVIEWED.
- Build/test/review de integración: EXECUTOR_REPORTED, pendientes de receipts.
- R03/89, 25%, USD5.000 y perfiles antiguos: REFERENCE_ONLY para nuevos modos; preservar identidad histórica.
- C01 foto master347/IN_PROGRESS: SUPERSEDED para estado actual.

/frozen

Tres tipos; NQ; Strategy/MM/Provider separados; runtime como autoridad; legacy intacto.
USD4.000 son caja comercial, cero aportes y Forex separado; reinversión del 100% del cash neto recibido. Payout variable; sin caps prudenciales agregados.
I0 NO decide prop, horizonte, sizing, óptimo de retiro, financiación no resuelta ni D05. El 1/3 no se adjudica sin unidad/resets/refunds/cohorte/H explícitos. No tocar adjudicación legacy de 25%.
CHALLENGE/FUNDED aisladas no prueban adquisición financiada ni q longitudinal. No promover HISTORICAL_ONLY a LIVE.
G0–G5 y PROD_FROZEN_BY_OWNER intactos. Tests de reporte no son campañas ni cualificación de una Strategy.

/architecture

Aplicar C04 §§4.2 y 14.1–14.4. Hay un único modelo reusable de Campaign por modalidad; GAU50/E2T challenge/funded son perfil+tipo+config, no implementaciones por Strategy. Este shot sólo implementa proyección: no nuevas campañas, driver ni SIMULATION.

- Preservar definición/config, instancia lógica, request digest original, RunID derivado, attempt físico y revisión/hash de receipt como dimensiones distintas. No renombrar campos legacy para fingir que ya eran contratos universales.
- Registrar scope de evidencia: aislada/comparación/junta cuando esté demostrado; referencia de bankroll/mercado y asociación/config Strategy/MM cuando existan. Una instancia compuesta no recibe otra caja 4.000. Missing scope=UNKNOWN, sin adivinar composición por número de filas.
- AccountID/EventID locales se interpretan dentro de origen/scope autoritativo. Mismos strings en campañas independientes no colisionan. Relectura del mismo receipt no duplica efectos; revisión posterior sustituye el derivado afectado sin borrar originales. Attempt técnico no es compra nueva.
- Archivo/fila/hash identifica evidencia, no es un nuevo EventID comercial. Si Go no emitió linaje/ID suficiente, mostrar UNKNOWN localizado. Conservar tiempos económicos, coordenadas y orden observados; no construir una secuencia por ordenar timestamps.
- Python adapta evidencia y calcula métricas/conciliación pura. Go/SDK/Campaign conserva compra admisible, transiciones, sizing, fills, PnL, pago recibido y estado de reanudación. El reporte no es ledger ejecutable ni input de resume.
- La rotación real actual conserva una Strategy continua y compartimentos con estado MM/Provider/ledger propios, una cuenta activa a la vez; N funded iniciales y multi-asociación no están implementados por este contrato.
- Los gaps de perfil E2T/GAU50, objectiveCapacity TGMM, RunState monocuenta, RuleSet global y trayectoria OHLC por venue pertenecen a cambios Go posteriores. No resolverlos en I0 ni fabricar una API física para I4.
- Migración I0 = lectura derivada y mapa source→proyección, no reescritura/ejecución de presets/receipts. Mantener diferenciados Platform y CAMPAIGN legacy, ResearchCash con aportes, FIRST_PASS histórico, 25%,5.000,cuatro payouts y V1/Unclipped.

/scope

Presupuesto total máximo 150 minutos: hasta 30 para reconciliación focal, trabajo restante dentro del slice y 20 finales reservados a evidencia/feedback/cierre. Una ejecución acotada; no polling ni watch persistente. CERO motores de campaña, CERO compras, CERO trading, CERO deploy.

Allowed Files de producto, a fijar por task antes de IMPLEMENT:
- v3/backtester/tools/tradesgerard/campaign-lab/campaign_lab.py.
- v3/backtester/tools/tradesgerard/campaign-lab/research_lab.py, únicamente extensión opt-in de proyección/reporting.
- Tests nuevos, fixtures pequeños y documentación del mismo owner; módulo puro contiguo sólo si evita acoplamiento real.
- Artefactos SDD del change I0 según el catálogo y la feature existentes.

READ_ONLY: SDK/Core/Go driver, datos, contratos comerciales históricos, catalog-v1.json, R02-HISTORICAL-MANIFEST.json, campañas/receipts/planes sellados, presets y working trees ajenos. No tocar run/resume/launcher ni agregar otra vía de spawn. No modificar tests existentes sin TEST_CHANGE_REQUEST adjudicado según la policy; preferir nuevos tests para el contrato opt-in.

Agents-OS: publicar sólo el retorno propio I0, agent-run, feedback cuando aplique y change_log; el manager integra el planner único. master directo, HEAD reconciliado, sin rama/PR/force y sin sobrescribir escritores concurrentes.

/execute

1. Reconciliar el frente existente y recuperar receipts originales: SHA/binario/build, comandos/logs de suites, failure sets con causas e informe completo del verificador. Si faltan, marcar UNKNOWN. Igualdad de nombres de fallos no demuestra causa ambiental.

2. Resolver la pregunta focal S04-F01 sin correr 89 campañas: los 26 nativos del catálogo declaran STRATEGIC_ENTRY_BUDGET_V1; native_mm_block copia ese campo. ae1b09bc no pre-veta headroom en V1; 2baf319d sí devuelve TG_ENTRY_BUDGET_EXCEEDS_HEADROOM. Recuperar planes efectivos sellados de las 26 nativas, censar policy/hash y contrastar con generador actual. Un fixture acotado desde journeys existentes puede comparar la frontera R>headroom positivo, igualdad y floor cruzado, sin cambiar producto ni lanzar campañas. No sustituir V1 por Unclipped ni afirmar que todos los resultados cambiaron sin evidencia. Si requiere otra corrección, devolver el alcance exacto y mantener abierta la aceptación S04.

3. Confirmar S04-F02: qualification_guard.py no estaba en el master pre-ClutiFX inspeccionado. Registrar seam/delta necesario para una posterior adaptación del guard de run/resume. No importarlo ni saltarlo en I0. Esta ausencia no convierte el reporter no-spawn en un launcher permitido.

4. Materializar SPEC/PLAN/TASKS/VERIFICATION del slice conforme al repo antes de código, enlazando C04 sin duplicar autoridad. Congelar Allowed Files y criterios. Adjuntar mapping de campos reales→contrato §4.2 (fuente, recuperable/UNKNOWN, scope, revisión/linaje/tiempo) antes de fijar el schema opt-in. No elegir ahora el layout físico de I4. Puedes resolver nombres internos y extracción local sin rediseñar arquitectura ni inventar economía.

5. Implementar proyección pura opt-in sobre eventos/evidencia existentes:
   - U: unidades comerciales inicialmente cobradas, cantidad conocida, también pendientes de provisión. Facturas/cargos/derechos/cuentas/intentos/retries separados.
   - Bundle conocido: K raíces y un cargo; K desconocido: gasto visible y UNKNOWN_CARDINALITY. No inferir K por precio.
   - Reset contractual crea intento vinculado; renovación/retry no crean compra. Refund ajusta coste una vez y conserva cohorte pagada bruta descriptiva; no aplica por sí solo D01 al umbral.
   - P_U/U y P_A/A, costes agregados por pase/funded disponible, censura/seguimiento. Cero éxito produce N/A con razón y gasto visible. UNKNOWN nunca se convierte en cero.
   - FUNDED: todas las iniciadas, pagadoras, pagos repetidos, pérdidas antes/después, W neto y F_op sin repetir activación ni fees retenidos.
   - Q/q: raíces de U con primer payout positivo efectivamente recibido por linaje compra→intento→pase→activación→payout. Una raíz cuenta una vez. CHALLENGE sin observar funded es NOT_OBSERVED; seeds exógenas o linaje insuficiente no producen q inventado.
   - Conservar primer crédito y reversos/cash retenido por separado. Pago solicitado/aprobado no es cash disponible.
   - Cada efecto financiero tiene identidad/fecha/causa/procedencia; duplicado idéntico idempotente, mismo ID con términos distintos conflicto. No inventar IDs de efectos legacy.
   - Dinero/fracciones exactos; output determinista con completitud, numerador, denominador, razón, cutoff y refs por métrica. Totales y atribución deben conciliar.
   - Datos y receipts sellados byte-intactos. El reporte nuevo no alimenta silenciosamente el selector legacy ni reinterpreta 25%/5.000/120/4 payouts.

6. Conectar el reporter al CLI/herramienta ya existente por el camino mínimo que no invoque motores. Documentar sólo comandos y flags realmente implementados/verificados. No crear un framework de políticas, motor contable, DB, scheduler o DSL.

7. Retornar al manager al término del slice o presupuesto. No iniciar I1/I2a ni otra campaña.

/verify

Aplicar C04 V01–V10/V16–V19/V25–V36 y C02 RC01–RC04/RC08 dentro del alcance de reporter. RC05/RC06/RC07 con scheduler/guard real son futuros; no presentarlos ejecutados por fixtures de proyección.

Oráculos independientes:
- USD100 + USD100, una pasada y otra no provisionada: U=2, P=1, coste=200, coste/pase=200.
- Bundle K=2 por180: U=2 y coste180; si K falta, conservar coste180 y U=UNKNOWN. Caso separado de dos compras100+100: refund100 mantiene U bruta2 y deja coste neto100.
- Reset gratis/pagado, renovación, retry y evento duplicado; conflicto mismo ID.
- Dos pagos780+460 de una raíz y luego pérdida: Q=1, pagos=2, W=1240; approved-only y refund no aumentan Q.
- CHALLENGE10/3 + FUNDED exógena3/1 no demuestra q=1/10.
- Pérdida nominal no debita caja; activación/fees no duplicados; crédito posterior al corte no se adelanta.
- No origen/cargo/event_id: UNKNOWN localizado, input intacto.
- Dos receipts de campañas distintas con el mismo account_id/event_id local no se fusionan. Relectura del mismo receipt no duplica cash; revisión/attempt nuevo no fabrica otra compra.
- Batch independiente no obtiene etiqueta de SIMULATION conjunta ni dos bankrolls propios dentro de una composición. Un importe conocido puede conservar atribución UNKNOWN.
- Instante económico anterior a su observación no autoriza reordenar decisiones; no producir estado que Go consuma como ledger/resume.
- Repetición del comando de reporting produce la misma salida semántica y cero spawn/egress, acreditado mediante sentinel.
- Compatibilidad legacy por fixtures/bytes y regresiones afectadas; no ejecutar suites ajenas de infraestructura.
- E2E LOCAL del reporter real con un artefacto existente recuperable; fixtures sintéticos claramente rotulados para datos ausentes. Si no hay artefacto, declarar esa limitación.
- ≥95% de coverage del desarrollo nuevo y caminos críticos cubiertos primero, conforme a policy. Si un requisito queda sin evidencia, no declararlo PASS.

/reuse

Reusar campaign_lab, research_lab, parsers/money/digest, reconciliador y comandos existentes. Clasificar tests/probes como PERMANENT_REGRESSION, E2E_CANDIDATE, HARNESS_TOOLKIT_CANDIDATE o DISPOSABLE_REPRODUCER. Conservar invariantes durables; no duplicar helpers ni congelar resultados incorrectos para obtener verde.

/improve

REUSABLE_BEHAVIOR_CANDIDATES con evidencia concreta o NONE. Feedback sólo real o pedido del mandato. No crear skills/managers/runbooks por rutina. No inferir consumo Pro por rol/modelo.

/close

Persistir candidato de producto en su rama propia y verificar remoto según policy; no merge a master ni deploy. Mantener todos los changes dentro del scope. Retorno documental canónico create: main/10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-I0-IMPLEMENTATION-RETURN.md.
Registrar agent-run atribuible, feedback, change_log y cierre exclusivo de esta ONE-SHOT conforme a las skills. Agents-OS master directo con HEAD/lease/readback; manager/programa siguen abiertos. Si se bloquea publicación, preservar artefactos locales y declarar el bloqueo; no fingir SHA remoto.

Devolver:
STATUS; BASE_SHA; BRANCH_REAL; CANDIDATE_SHA; DIFF_SCOPE;
S04_SOURCE/BUILD/TEST/ACCEPTANCE/DEPLOY; S04_F01_DISPOSITION; S04_F02_DISPOSITION;
SPEC_PLAN_TASKS_REFS; TEST_COMMANDS_AND_RECEIPTS; COVERAGE;
INPUT_CHECKSUMS; REPORT_EXAMPLES; IDENTITY_SCOPE_MAPPING; RECEIPT_REVISION_POLICY;
LEGACY_TO_PROJECTION_MAPPING; NO_SPAWN_EVIDENCE; LEGACY_COMPATIBILITY;
NOT_EXECUTED; UNKNOWN; REUSABLE_ASSETS; FEEDBACK; CLOSE_SCOPE;
AGENTS_OS_PATHS_SHA; PRO_CHAT_POOL_DELTA (confirmado o UNKNOWN);
NEXT: I0-S2 LOCAL independiente sobre SHA exacto, sin autoaceptación.
```

### Prompt posterior — I0-S2, sólo con retorno y SHA candidato

```text
# ECHO FUTURES — I0-S2: VERIFICACIÓN ADVERSARIAL LOCAL

ROLE: TOP
MODEL: GPT-6 Sol, identificador efectivo registrado por el host.
SURFACE: LOCAL, contexto fresco.
WORK FUNCTION: verificador independiente de I0; no implementador ni manager.
EXECUTION MODEL: ONE-SHOT. Un verificador; no modifica producto ni recibe la confianza del autor como evidencia.

/goal

Intentar falsar el contrato/reporting I0 en el SHA candidato exacto. Entregar VERIFY_PASS, FINDINGS o BLOCKED con casos reproducibles. No convertir el estado de S04 ni el permiso de implementar I0 en aceptación económica.

/authorities

Bootstrap agents-os/master, main/AGENTS.md. Leer C04 EF-CAMPAIGN-MODES-DESIGN, EF-CAMPAIGN-MODES-REVIEW, EF-S04-INTEGRATION-RECONCILIATION, este paquete y EF-CAMPAIGN-MODES-I0-IMPLEMENTATION-RETURN. Planner único de Optimización de Campañas.
Cargar sdd-workflow/sdd-developer, echo-retester-master/runbook, agents-os-agent-run-register, agents-os-session-feedback y agents-os-session-close.
En Echo leer AGENTS.md, CONSTITUTION.md, reglas SDD 08/09 y SPEC/PLAN/TASKS/VERIFICATION efectivos del slice.

/baseline

CURRENT_TASK_STATE: REVIEW.
BASE_SHA proviene del retorno I0-S1 y debe ser 2baf319d o descendiente allí reconciliado.
CANDIDATE_SHA obligatorio: resolver desde el retorno publicado I0-S1 y verificar HEAD/ancestro/diff. No inferir por nombre de branch ni probar master en vez del candidato.
Si falta retorno o SHA, estado NOT_DISPATCHED/BLOCKED; no ejecutar este shot contra un candidato inventado.
La implementación es UNREVIEWED. C04/C02 son ACCEPTED_INPUT para invariantes; declaraciones de tests son pistas a verificar.

/frozen

Mismas definiciones de U/Q, costes, UNKNOWN/NOT_OBSERVED, causalidad y legacy de C04. NQ, tres modos, caja 4.000/zero aportes y reinversión son contratos del proyecto, no permiso de campaña. D01–D06 y G0–G5 intactos. SOURCE/BUILD/TEST/ACCEPTANCE/DEPLOY separados.

/scope

Máximo90 minutos, últimos15 para informe/cierre. Cero motores de campaña, trading, compras, deploy o mutaciones de infra.
Producto y tests del autor READ_ONLY. Puedes crear un harness/fixtures independientes en workspace propio y entregar sus archivos para promoción posterior. No reemplazar funciones del producto por mocks para afirmar E2E.
No escribir planner compartido ni modificar los informes de S1/C02. Agents-OS sólo reporte propio, agent-run/feedback/change_log, master con lease.

/execute

1. Validar base/candidato/Allowed Files y vinculación SPEC→criterios→diff. Detectar cambios de defaults, adjudicación legacy, launcher o runtime fuera del slice.
2. Construir casos desde la SPEC, sin copiar las respuestas calculadas por helpers del autor. Ejecutar el comando real de reporting como proceso y comparar con una conciliación independiente.
3. Atacar compra pagada no provisionada, bundle desconocido, pagos parciales del mismo pedido sin duplicar raíz, resets/renovaciones/retries, refund/reverso, coste común no atribuible y cardinalidad múltiple no soportada.
4. Atacar q: doble payout, payer después quemado, approved-only, CHALLENGE sin observación funded, seeds exógenas, raíz faltante y linaje futuro. Distinguir cero observado de ausencia de observación.
5. Atacar duplicados/event_id conflictivos, IDs locales iguales entre scopes independientes, relectura/revisión de receipt y retry fallido seguido de COMPLETE, eventos posteriores al cutoff, money exacta, U/P/Q desconocidos y JSON incompleto. Distinguir tiempo económico de coordenada observada. No inventar una regla que permita reordenar eventos concurrentes sin autoridad. Verificar que el reporte no se consuma como estado autoritativo Go, que no fusione batch independiente como SIMULATION y que los mappings legacy no reescriban identidad.
6. Probar input intacto, output determinista, no escritura sobre recibos/legacy y cero spawn/egress mediante sentinel del proceso. Revisar imports/rutas que podrían invocar run/resume.
7. Ejecutar regresiones afectadas contra base/candidato y evaluar coverage nuevo por invariantes. No limpiar ni ocultar fallos preexistentes. Revisar la disposición S04-F01: plan sellado y fixture sólo respaldan su alcance exacto; si permanece UNKNOWN, no llamarlo corregido.
8. Si encuentras un defecto, registrar esperado/real/archivo/coordenada/mínima corrección; NO corregir producto.

8. Falsificadores SOURCE focales del manager (a REPRODUCIR o REFUTAR; no se consideran tests ya ejecutados):
   - P1: refunds suman cash pero `cash_final_projected`/`cash_residual` usan gross costs sin refunds. Opening200/PURCHASE100/REFUND100/final200 debería conciliar en cero.
   - P1: `Q` agrega cada `paid_out` sin exigir los `passed` y `activated` calculados; crédito sin pase o activación acreditada no puede generar compra→primer cobro demostrada.
   - P1: `_account_funded_evidence` admite `review_at`; cuenta PASS_REVIEW aún no activada no cuenta como funded iniciada.
   - P1: cutoff previo al último flujo compara cash parcial con `cash_final` terminal; exigir cash a frontera comparable o UNKNOWN, no residual falso.
   - P2: `_ts` es comparación lexicográfica y no normaliza offset RFC3339; probar UTC equivalente y timestamp ausente bajo cutoff.
   - P2: `funded_since` usa `credentials_at` y puede computar setup/activation como F_op funded anterior a activación; separar fase, no sumar dos veces.
   - P2: dos PURCHASE del mismo AccountID, bundles y reintentos; no usar AccountID distinto como proxy universal de raíz comercial sin evidencia.
   - P2: dos attempts con mismo campaign_id y SHA distinto no son necesariamente revisiones del mismo receipt; demostrar la relación o devolver UNKNOWN.
   Para cada punto: expected/actual, caso independiente, causa, severidad, reproducción y destino del fixture. El verificador no corrige producto ni ejecuta Go/campañas. Hallazgo no reproducido debe quedar identificado como tal.

/verify

El gate exige E2E real del reporter en LOCAL más falsificación independiente; repetir sólo la suite del autor o review CLOUD no basta. E2E reporter no prueba trading/SIMULATION.
Separar casos implementados, no ejecutados, bloqueados y no aplicables. Exigir conservación legacy y ausencia de adjudicación automática de 1/3/G4.
Un caso documental o fixture de reducer no satisface RC05/RC06 de competencia del driver ni resume comercial de I3.

/reuse

Clasificar cada prueba independiente: PERMANENT_REGRESSION, E2E_CANDIDATE, HARNESS_TOOLKIT_CANDIDATE o DISPOSABLE_REPRODUCER, con razón y owner destino. Conservar especialmente los falsificadores que encontraron defectos.

/improve

Feedback concreto o NONE; no nueva skill/manager. Declarar independencia de ejecución frente al autor y límites de independencia histórica sin inferirla sólo por contexto fresco.

/close

Publicar create: main/10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-I0-VERIFY-RETURN.md, con manifiesto/hashes de harness y cómo reproducirlo. Registrar agent-run, feedback y change_log; cerrar sólo esta ONE-SHOT. Agents-OS master directo con HEAD reconciliado/readback, sin PR/force.
Devolver STATUS; BASE/CANDIDATE_SHA; INDEPENDENT_E2E; FINDINGS con severidad/esperado/real; REPRO_REFS; LEGACY/NO_SPAWN; NOT_EXECUTED/UNKNOWN; REUSABLE_ASSETS; AGENTS_OS_PATHS_SHA; PRO_CHAT_POOL_DELTA confirmado o UNKNOWN.
El manager adjudica el alcance de corrección. No aceptar el gate Owner ni iniciar I0-S3 por tu cuenta.
```

### I0-S2 — adjudicación MANAGER para I0-S3 (2026-10-29, vinculante)

**Retorno validado:** [[EF-CAMPAIGN-MODES-I0-VERIFY-RETURN]]. I0-S2 = FINDINGS, **4 P1 + 6 P2 + 1 P3**, E7/E8b REFUTED. El resumen abreviado de verificador/agent-run dice nueve pero el retorno detallado documenta F1–F11: usar la tabla detallada, no la cifra abreviada. Código base b964e13df59e20b06349eb7e0ad4f4ed057d04a0; R03 E2E y legacy 34+124 PASS reportados independientemente en LOCAL; harness persiste en ~/echo-work/i0-s2-verify/.

**F1–F4 (P1) ACCEPTED / BLOCKING:** F1 fórmula cash con REFUND; F2 Q sin pase+activación acreditados; F3 funded inflada por review_at/credentials_at; F4 cutoff contra cash_final terminal.
**F5–F10 (P2) ACCEPTED / REQUIRED:** F5 RFC3339 UTC vs strings; F6 post-cutoff mantenerse en effects con marca; F7 timestamp faltante→UNKNOWN y métricas de ventana no completas; F8 setup fees no computan F_op; F9 attempt físico ≠ revisión del mismo receipt; F10 payout sin atribución no produce q=0 OBSERVED. **F11 (P3) ACCEPTED:** no emitir reconciliation True constante. **E7 y E8b REFUTED:** preservar comportamiento correcto.

**Criterios operativos del manager para corrección:**
- F1 incluir refunds recibidos una sola vez en cash proyectado/residual y cost_net. Cuenta/timing de la devolución quedan según evidencia y alcance.
- F2+F10 exigir cadena compra→intento→pase→activación funded APLICADA→primer payout CREDITED asociado, dentro de horizonte. Si falta cualquier costura, usar INCOMPLETE_LINEAGE/UNKNOWN o NOT_OBSERVED según evidencia; no inferir 0 observado. Las cantidades de cobros pueden seguir reportadas globalmente aunque falte atribución.
- F3+F8 review_at/credentials_at son preactivación. compliant_at es fecha *programada* de compliance y NO prueba timestamp de activación. Para frontera real usar estado/control instalado y su evidencia en el artefacto; si no existe, conservar UNKNOWN específico para funded iniciado, fecha y F_op, sin convertir estado del último receipt en historia temporal.
- F4+F5+F6+F7 mantener la lista de efectos con su clasificación temporal comparada en UTC; cash de cutoff sólo se reconcilia contra estado al mismo corte. Si un efecto no puede datarse, no incluirlo como previo al corte y marcar incompletitud del total afectado. E2E legado sin cutoff conserva número bruto correcto.
- F9 NO sumar dos attempts ejecutados como compras nuevas ni descartar uno por tener mismo campaign_id. Revisión legítima exige identidad de receipt/provenance; dos RunIDs diferentes no prueban una misma revisión. Si origen/relación no demostrados, enseñar ambos resultados/per-attempt spend y total conjunto UNKNOWN/NOT_COMPOSABLE. No elegir arbitrariamente last input como autoridad comercial; no leer/escribir historia fuera del scope autorizado.
- F11 reconciled/sums_by_assignment sólo True si calculado con datos completos y sin conflictos; si no, False o UNKNOWN con razón explícita, sin inventar ledger.
- Usar harness E1–E8 de ~/echo-work/i0-s2-verify/, integrar falsificadores nuevos como regresiones durables dentro del owner, conservar E7/E8b, sin reescribir fixtures del verificador ni tests legacy sin TCR.
- Verificar SDD, 34+N tests de contrato, 124 legacy, cobertura nueva >=95% (o estado bloqueado), E2E R03 doble determinista, inputs sellados intactos, no-spawn/egress sentinel, diff/rollback y ausencia de cambios Go/launcher. No auto-merge de xKoRx/echo.

**Independencia:** el verificador I0-S2 fue otro worker/harness fresco, pero agent-run declara GLM-5.3-Flash (no GPT-6 Sol TOP solicitado). Registrar la limitación; el manager realizará challenge del delta final en otra superficie antes de recomendar aceptación. No consumir el shot GOD para el reporter por rutina.

**Salida esperada:** READY_FOR_OWNER_REVIEW sólo con F1–F11 resueltos y evidencia local; en caso contrario PARTIAL/BLOCKED con dependencia concreta. No resolver D01–D06 ni S04-F01/F02 en este shot.

### Prompt posterior — I0-S3, sólo con retorno S2 y findings adjudicados

```text
# ECHO FUTURES — I0-S3: CORRECCIÓN Y GATE FINAL

ROLE: NORMAL
MODEL: GLM-5.3-Flash, identificador efectivo registrado por el host.
SURFACE: LOCAL, contexto fresco.
WORK FUNCTION: corrector final del slice I0; no manager ni verificador independiente.
EXECUTION MODEL: ONE-SHOT, un writer. No iniciar otro incremento.

/goal

Corregir los findings aceptados de I0-S2, preservar sus falsificadores durables y entregar READY_FOR_OWNER_REVIEW en un SHA exacto con gate afectado completo. Si S2 no encontró defectos, reconciliar y ejecutar ese mismo gate final; no inventar cambios.

/authorities

Bootstrap agents-os/master desde main/AGENTS.md. C04 diseño, planner único Optimización de Campañas, EF-CAMPAIGN-MODES-I0-LOCAL y retornos IMPLEMENTATION-RETURN/VERIFY-RETURN. Adjudicación explícita del manager del alcance de findings (sección vinculante I0-S2 de este paquete, publicada 2026-10-29).
Cargar sdd-workflow/sdd-developer, retester/runbook y run-register/feedback/session-close. Leer reglas SDD 08/09, constitution, SPEC/PLAN/TASKS/VERIFICATION del repo.

/baseline

CURRENT_TASK_STATE: REPAIR o FINAL_VERIFY según retorno.
BASE y CANDIDATE_SHA se resuelven del retorno I0-S1 y coinciden con el SHA verificado por S2. Resolver branch/WIP real sin modificar trabajo ajeno.
Si falta S2, su SHA no coincide o hay un finding de semántica sin adjudicar, bloquear la corrección afectada y devolver dependencia. No interpretar silencio como aceptación de un cambio económico.

/frozen

U/Q/linaje/costes/causalidad/UNKNOWN y compatibilidad legacy C04. No tocar Strategy/MM/Provider, guard de campañas, presets históricos ni reglas del Owner para satisfacer un test.
D01–D06 permanecen decisiones aplicables propias; I0 no adjudica 1/3. PROD congelado. Cero motores de campaña, compras, trading o deploy.

/scope

Máximo120 minutos, últimos20 evidencia/cierre. Un writer y mismo Allowed Files del slice, más pruebas independientes que protejan invariantes dentro de su owner.
Tests existentes sólo mediante TCR aplicable; no debilitar assertions ni cubrir código muerto artificialmente.
No merge a master de producto ni release. Agents-OS master directo; retorno propio y evidencia, no planner compartido.

/execute

1. Reconciliar candidato exacto, findings aceptados, corpus independiente y estado de S04-F01/F02.
2. Corregir los defectos dentro de SPEC; si una corrección exige cambiar significado económico, volver al manager con caso, sin decidir silenciosamente.
3. Integrar en tests permanentes los falsificadores deterministas que protejan invariantes durables, eliminando duplicados sin perder el caso adversarial.
4. Ejecutar suite completa afectada, E2E real del reporter y probes críticos independientes. Revalidar input byte-intacto, no-spawn, ausencia de mutación legacy y cobertura nueva.
5. Revisar diff contra base y contra S1; documentar exactamente qué se corrigió y qué permanece fuera del alcance.
6. Emitir gate final con SHA, evidencia ejecutada y limitaciones. No se promete ni ejecuta una cuarta ronda; defectos ordinarios encontrados dentro del presupuesto se corrigen aquí, contradicciones reales vuelven al manager.

/verify

Todos los criterios I0 de C04 deben tener test/receipt o estado explícito no probado. Cero P1/P2 aceptados pendientes para READY_FOR_OWNER_REVIEW. Coverage nueva≥95% según policy, críticos primero.
No usar «mismo failure set» como prueba de equivalencia V1. No declarar resuelto el guard por haber prohibido motores en I0. E2E reporte no certifica runtime ni historia.
Si el entorno impide una prueba necesaria, PARTIAL/BLOCKED con causa y alcance, nunca PASS ficticio.

/reuse

Inventario y destino de tests/harness/fixtures promovidos; conservar los del verificador que demostraron defectos. Reportar assets descartados y razón; no crear otro toolkit si ya existe owner.

/improve

REUSABLE_BEHAVIOR_CANDIDATES con evidencia o NONE. Feedback/cierre propios; sin promover skills/runbooks automáticamente y sin inferir cuota Pro.

/close

Publicar create: main/10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-I0-FINAL-RETURN.md. Actualizar artefactos SDD de producto y persistir commits propios de la rama; verificar remoto, sin merge/deploy.
Registrar agent-run, feedback y change_log. Agents-OS master sin ramas/PR/force, lease y readback; cerrar sólo el worker. El manager y el programa siguen abiertos.
Devolver STATUS=READY_FOR_OWNER_REVIEW|PARTIAL|BLOCKED; FINAL_SHA; BASE/CANDIDATE_SHA; FINDINGS_DISPOSITION; FINAL_GATE_EVIDENCE; COVERAGE; LEGACY; NO_SPAWN; S04_REMAINING; REUSABLE_ASSETS; AGENTS_OS_PATHS_SHA; PRO_CHAT_POOL_DELTA confirmado o UNKNOWN; siguiente outcome recomendado.
```

### Prompt reservado — GOD-COMPOSITION, no ejecutar antes de I0 por rutina

Este cuarto shot se activa sólo cuando el manager entregue un incremento Go concreto y el source efectivo que debe resolverlo. No es una investigación nueva ni un gate adicional para el reporter. Si basta una cápsula de source, resolver la decisión CLOUD; LOCAL se justifica por evidencia/checkout/prueba local material. La selección de este presupuesto no registra consumo todavía.

```text
# ECHO FUTURES — GOD-COMPOSITION: ADJUDICACIÓN FOCAL DEL PRÓXIMO CAMBIO GO

ROLE: GOD
MODEL: GPT-6 Astra, registrar identificador efectivo del host.
SURFACE: LOCAL sólo bajo el disparador descrito; contexto fresco.
WORK FUNCTION: revisor/arquitecto adversarial ONE-SHOT del incremento concreto. No eres manager, implementador ni Owner.

/goal

Adjudicar la menor adaptación que preserve Campaign reutilizable por tipo y permita la capacidad concreta asignada, sin duplicar SDK/runtime/scheduler ni convertir Python en autoridad. Retornar DESIGN_READY, DESIGN_READY_WITH_MINOR_DELTAS o DESIGN_BLOCKED con causa precisa. No rediseñar Echo ni anticipar todo I4.

/authorities

Bootstrap xKoRx/agents-os/master, main/AGENTS.md; technical-project-manager, sdd-workflow, echo-retester-master/qualification y reglas Echo por routing. Cargar agents-os-agent-run-register, agents-os-session-feedback y agents-os-session-close.
Planner único: main/10-projects/Echo Futures/agentes/Echo Futures — Optimización de Campañas.md.
Diseño único: main/10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-DESIGN.md, revisión vigente; leer especialmente4.2,8,10.3,14.1–14.4,17 y26.
Paquete: main/10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-I0-LOCAL.md.
Mandato funcional FUT-R01 vigente. Runtime/R6 y los owners compartidos conservan autoridad; I+D conserva economía.
Echo: AGENTS.md, CONSTITUTION.md, v3/backtester/README.md, reglas SDD y SPEC/PLAN del incremento efectivo.

/baseline

Corte observado por C04: xKoRx/echo@2baf319ddcba622d9557bc9f23a13787b44c58a7.
REQUISITO DE DESPACHO: el manager identifica incremento/consumidor, base/branch/SHA real, estado del retorno I0 y pregunta pendiente. Si sólo está este prompt reservado, devolver NOT_DISPATCHED; no inventar candidato ni ampliar scope.
Resolver checkout/WIP local; comparar delta material respecto de C04, sin reset/merge/stash ni tocar trabajo ajeno. Los límites conocidos no necesitan otra auditoría completa.

/frozen

Tres modalidades reutilizables, Strategy/MM independientes; máximo una activa por asociación y varias asociaciones simultáneas sólo cuando esa capacidad se implemente. NQ. SIMULATION conjunta con un mercado/reloj/bankroll4.000, cero aportes y reinversión100% cash neto recibido. No sumar backtests aislados.
Strategy decide técnicamente; MM sizing/gestión; Provider/Runtime reglas/operativa; Campaign lifecycle comercial; reporter deriva métricas; composición usa las mismas autoridades.
Sin nueva Campaign por Strategy, DSL, scheduler, framework financiero, factory abstracta sin consumidor, fórmula paralela de PnL ni import Core/internal desde backtester. No cambiar G0–G5, D05, HISTORICAL_ONLY ni freeze PROD. Preservar identidades legacy y S04-F01/F02 abiertos en su alcance.

/scope

Una pasada≤90min, últimos15 para retorno/persistencia. Producto/tests/datos/infra read-only; no implementación, refactor preventivo, nuevas campañas, builds/suites generales, gastos ni trading. Lectura local y trazado de llamadas reales; cualquier comprobación física adicional debe estar expresamente incluida en el despacho y usar comandos existentes inspeccionados. No afirmar ejecución por leer un test.
Agents-OS: sólo retorno propio, registro atribuible, feedback y change_log. Manager integra diseño/planner; no escritores concurrentes sobre esos dos.

/execute

1. Confirmar qué capacidad necesita el incremento y su diferencia entre campañas independientes, rotación intrainstancia y composición conjunta. Reusar los hallazgos SOURCE C04, invalidándolos sólo con delta real.
2. Trazar los puntos que bloquean ese consumidor: RunPlatformCampaign/Validate/selectTurn; CompositionFactories; platform_preset/Profile/objectiveCapacity; composeAccount/RunState/accountCompartment; pool reducer/claims/assignment/fanout existentes. Un registro de módulo no implica otra Campaign; una lista de admisión no se elimina para simular genericidad.
3. Si entra simultaneidad: indicar exactamente qué owners/campos/colas/timers son compartidos y cuáles account/association-scoped; cómo conservar mercado/reloj/scheduler y drenar/correlacionar efectos de varias cuentas. Un for sobre RunPlatformCampaign o el test de catálogo no demuestra esa capacidad.
4. Si entra multi-prop: resolver la restricción ConfigSnapshot.Validate que iguala bindings al Provider.RuleSet global. Proponer la mínima composición/variante opt-in validada, con el owner competente; jamás un skip del validator ni duplicar Provider.
5. Si entra OHLC conjunto: adjudicar una única trayectoria causal coherente para cuentas con exposiciones opuestas; hoy intrabarPathDirection usa el neto del venue seleccionado. No cambiar el modelo histórico ni seleccionar rutas distintas para cada cuenta dentro de la misma simulación. Si el incremento usa otro execution model, declarar el alcance y no resolver OHLC fuera de scope.
6. Comprobar el contrato I0 de identidad/scope/revisión/eventos/linaje y la frontera Python/Go. Para el contrato/proyección I0, proponer sólo los cambios aditivos necesarios; no convertir el informe en ledger o checkpoint. Verificar mapping de campañas antiguas a configuración nueva, SAME_SEMANTICS vs NEW_EXPERIMENT y evidencias que se conservan.
7. Entregar una opción mínima recomendada con archivos/símbolos reales, invariantes, impacto en compatibilidad, aceptación adversarial y rollback. Descartar alternativas sólo con evidencia de duplicación/acoplamiento real; no generar un catálogo de arquitecturas.

/verify

Cada finding debe incluir contraejemplo, causa en fuente, scope afectado y si debe corregirse antes del incremento o puede esperar. Separar DEMOSTRADO_EN_SOURCE, NOT_EXECUTED y UNKNOWN.
Cuando corresponda, definir oráculos para misma Strategy+dosMM, rotación sin reset técnico ni estado financiero compartido, dos cuentas expuestas al mismo mercado, dos demandas por el último cash disponible, eventos homónimos en scopes distintos y reanudación sin doble gasto/cobro. Definirlos no equivale a ejecutarlos.
No exigir implementar I4 antes de I0. No aceptar otro gate por interpretación.

/reuse

Reusar contratos/runner/supervisor/receipts/SDK existentes. Conservar pruebas durables ya presentes; cambios concretos de tests quedan para mandatos posteriores. Activos reutilizables y feedback concreto o NONE; no crear skill, manager ni planner.

/close

Persistir retorno propio en main/10-projects/Echo Futures/artifacts/backtester/EF-CAMPAIGN-MODES-ARCH-LOCAL-RETURN.md sólo al ejecutar efectivamente este encargo. No crear un diseño/planner paralelo. Registrar agent-run cuando aplique, feedback y change_log; cerrar exclusivamente esta ONE-SHOT.
Agents-OS master directo, HEAD reconciliado, sin ramas/PR/force, readback remoto. Manager y programa abiertos. Consumo Pro sólo confirmado o UNKNOWN.
Devolver STATUS; INCREMENT_AND_SCOPE; BASE/BRANCH/SHA; SOURCE_REFS; MATERIAL_FINDINGS; MINIMAL_DELTA; I0_COMPATIBILITY; LEGACY_MIGRATION; ACCEPTANCE/ROLLBACK; NOT_EXECUTED/UNKNOWN; REUSABLE_ASSETS; AGENTS_OS_PATHS_SHA; CLOSE_SCOPE; PRO_CHAT_POOL_DELTA.
```

## Fuentes

- Orden Owner de continuidad: diseñar campañas y comenzar implementación; límites del mandato C-MANAGER y freezes conservados.
- [[EF-CAMPAIGN-MODES-DESIGN]], [[EF-CAMPAIGN-MODES-REVIEW]] y [[EF-S04-INTEGRATION-RECONCILIATION]].
- Source observado: [xKoRx/echo@2baf319d](https://github.com/xKoRx/echo/commit/2baf319ddcba622d9557bc9f23a13787b44c58a7).
- [[30-resources/agents/skills/technical-project-manager/SKILL|technical-project-manager]], [[30-resources/agents/skills/sdd-workflow/SKILL|sdd-workflow]], [[30-resources/agents/skills/sdd-developer/SKILL|sdd-developer]]; retester y runbook vigentes.

