---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo I+D — Futures]]"
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
updated: "2026-10-30"
---

# Echo Futures — Optimización de Campañas

## Estado vigente — C06 GO-ONLY, 29-10-2026

**CURRENT_TASK_STATE: CONTINUATION. DESIGN: READY_FOR_IMPLEMENTATION. GO-S02: EJECUTADO — IMPLEMENTATION_CANDIDATE `062b6df77845d2042e398bb6174700e80bb58b60`. GO-S03: EJECUTADO — FINDINGS ([[EF-CAMPAIGN-MODES-GO-S03-RETURN]]). GO-S03R1: EJECUTADO — REVIEW_COMPLETENESS COMPLETE, PRODUCT_VERDICT FINDINGS ([[EF-CAMPAIGN-MODES-GO-S03R1-RETURN]]). GO-S04: EJECUTADO — **C06_DELIVERY = PARTIAL** · **FIRST_STRATEGY_CANDIDATE = SELECTED_FOR_REVALIDATION** (retorno [[EF-CAMPAIGN-MODES-GO-S04-RETURN]]). FINAL_SHA `baca3c602e57d53a48f79f5c6c6c300d27e980df` en `feature/ef-campaigns-go` (remoto == local, readback); build SHA256 `4b09aebf…`; 31 archivos, +5.706/−165, 16 commits sobre `062b6df7`; master sin mover (`2baf319d`). **Corregidos**: F1 (bindings sellados TGMM/RGMM por asociación vía costuras runtime, guardia HISTORICAL_POLICY_ONLY intacta), F2 (perfiles/RuleSets/MM heterogéneos reales simultáneos + defecto real del seed que instalaba el RuleSet global en vez del binding), F3 (FUNDED multi-asociación con denominadores separados), F4 (CloseSafety v2 consumida por el runtime), F5 parcial (productor de REVERSO con identidad propia y caja ajustada una vez; el productor REFUND de lifecycle NO existe — no hay transición declarada consumidora: inventarla sería economía nueva), F6 (estado honesto `LEGACY_PATH_PRESERVED` + builder real de materialización GO_V2), F8 (clasificación física de propósito en las 4 puertas legacy ejecutables; el miembro ausente ya no es bypass: QUARTER/HISTORICAL sin receipts ⇒ RECEIPT_MISSING pre-engine, exit 78; la alternativa ledger-only se descartó), F9 (capacidad K=5 asociaciones simultáneas medida: 5 compras, cash 2.380 USD, reconciliado), NF1 (AccountSlots = inventario CONCURRENTE de asientos, NO cap de compras de por vida — adjudicación del Owner), NF2 (owner del motor ganador instalado: el flip que moría con OPERATION_OWNER_MISSING corre limpio con cash idéntico), NF3 (activación acreditada por control observado; compliant_at gobierna sólo la autoridad de cobro), NF4 (replay nombrado `reproduce --result-json` con verificación de digest del request sellado) + 2 defectos ordinarios pre-existentes (clasificador de read-set que contradecía su propio test; assertion no determinista del log de eventos = el "FAIL único no reproducido" de S03R1). **Matriz de migración/materalización (104 filas, censo delta CERO)**: 26 `LEGACY_PATH_PRESERVED` · 27 `V2_ADMITTED` (26 TGMM + 1 RGMM, requests materializados y admitidos en seco con digests) · 62 `BLOCKED` con causa única exacta (la account policy RG no está declarada en las autoridades selladas del repo; los presets sellados de R01/R03 **sí** la declaran por identidad ⇒ un manifest Owner las desbloquearía sin código nuevo) · 15 aliases `CATALOG_VALIDATED` · **HISTORICALLY_EXECUTED = 0**. **Verificación**: conjunto de fallos final **23 = 23 idéntico al baseline S03** (0 nuevas, 0 resueltas); corpus del verificador re-ejecutado con bytes intactos ⇒ 15/21 PASS y 5 FAIL **exactamente** las mutaciones TCR (flip NF2 ahora limpio; heterogeneía/FUNDED-multi/segundo-perfil ahora rechazados por la causa correcta y más fuerte); Go-only físico en sandbox sin python3 (`lab migrate --materialize-v2` exit 0, 28 artefactos, 104 filas). **Residuales honestos**: F7 cobertura **79,6% diff-aware statement-based** (piso 95% NO alcanzado, statement-based y no promedio-por-función); productor REFUND de lifecycle ausente; `-race` NOT_EXECUTED (host sin gcc); **F10 persistido — el verificador final no-GLM NO estuvo disponible** (surface = `account:zai-start-plan/GLM-5.3-Flash`; 4 subagentes despachados, 2 completados, 2 reanudados tras muerte del host; todo el trabajo es del mismo modelo del equipo autor: **no** se etiqueta como GOD a ninguna ejecución GLM). **Candidata económica #1 = `LAB-SG-FBC-CH300-15M-R500`** (SG FBC-CH300-15M @ RG GROSS500): 26 compras → 9 pases (0,346), coste/pase 666,67 USD, 0,73 entradas/día, mediana tiempo-a-pase 27 días, 2026 = 11→5 (su mejor tramo) frente a MR-09-R750 (13→5, 936 USD/pase, 92 días, 2026 = 2→0);.Request v2 materializado (`sha256:f03c66d6…`) y admitido, ejecución MECÁNICA verde sobre corpus sintético; NO es revalidación histórica ni evidencia funded (NO_OBSERVADO). **Bloqueo LIVE de la candidata**: su MM `riskgeometry` es `HISTORICAL_POLICY_ONLY` (guardas intactas en `riskgeommm/manager.go:83` y `config/composition.go:184/357`) ⇒ LIVE_BLOCKED; el handoff al owner Runtime Pools ya existente prepara (a) el paquete de habilitación/servicio LIVE del módulo RG, (b) el manifest Owner de account policies RG por identidad, (c) la cadena G0–G5 Go + D01/D02/D05 + receipts para la ventana sellada HIST 2023-10-02→2026-10-06 (785 sesiones) — **sin** merge a master, release, deploy, compras ni armado de trading desde este shot. MERGE/DEPLOY/LIVE: NOT_AUTHORIZED. PROD: FROZEN_BY_OWNER.

La instrucción Owner actual reemplaza la entrega Python: campañas, control operativo y reporting oficial deben correr en Go. La rama `feature/ef-campaign-modes-i0@01a38c13b0a1b280eefb9d18f6d2b167e3cd8739` queda REFERENCE_ONLY; su gate PASS histórico no habilita merge. No hay código de producto implementado por esta actualización. `progress: 0` corresponde al nuevo alcance Go, no borra el trabajo previo del backtester.

**Una fuente por responsabilidad:** diseño técnico [[EF-CAMPAIGN-MODES-DESIGN]] C06; este archivo es el único planner; [[EF-CAMPAIGN-MODES-I0-LOCAL]] contiene los tres despachos vigentes Go (path histórico conservado, prompts Python retirados). I+D Futures conserva prioridad y decisiones económicas; Runtime Pools/SDK/R6 y retester conservan autoridades técnicas. No se crea manager competidor.

### Historial y otros frentes preservados

Se compacta el planner porque contenía múltiples cabeceras antiguas llamadas estado vigente. La copia íntegra anterior, byte-idéntica, queda en `artifacts/backtester/history/EF-CAMPAIGNS-PLANNER-before-C06.txt` (blob `3376fe2e2e780907f925feb97a7b49659e997a3e`); no es otro planner y no debe despacharse. Los retornos S04/I0 se conservan intactos. El resto de la evidencia histórica permanece en Git y en sus artefactos.

No cambia el estado de ClutiFX: priorizar [[10-projects/Echo Futures/artifacts/clutifx-strategy-research/e05r1/CLF-E05R1-STATUS|E05R1]] y [[10-projects/Echo Futures/artifacts/clutifx-strategy-research/k05/CLF-K05-SOURCE-CERTIFICATION|K05]], no Q04 superseded; no importar su rama por conveniencia. [[TRADESGERARD-CONTROL]] conserva histórico/datos; [[Echo Futures — Runtime Pools]] conserva runtime. A/B, selección de estrategias y calendario I+D no se bloquean por la corrección documental Go-only. Ningún gate previo se transfiere automáticamente a otra identidad.

## 1. Resultado comprometido y no objetivos

La entrega NO es un reporter Go equivalente al Python. El candidato debe incluir: tres modalidades reutilizables; CHALLENGE/FUNDED con inventario N y relevo; comparación aislada; SIMULATION con caja finita compartida y composición multi-asociación/multi-perfil; evidencia/KPI Go; tooling/admisión/runner Go; mapeo y retiro del legado Python; tests y resultados por identidad.

No objetivos: nuevos indicadores/estrategias, optimizar rentabilidad, decidir el retiro óptimo, construir UI, cambiar reglas reales de props, rediseñar infraestructura, publicar releases, LIVE, otra DB/framework/scheduler, checkpoint arbitrario de ejecución, cross-product masivo de cientos de estrategias y MM. Se debe poder añadir una configuración sin otra implementación Campaign.

No declarar todas las estrategias ejecutadas por haber validado catálogos ni probar factories con fixtures. La matriz de migración y la matriz de ejecuciones son distintas; cada fila conserva su condición real.

## 2. Baseline, rama y autoridades

- Producto: `xKoRx/echo`, master source `2baf319ddcba622d9557bc9f23a13787b44c58a7`; leer AGENTS.md, CONSTITUTION.md, .agents/rules/08-sdd-governance.md, 09-sdd-phase-permissions.md, specs/SPECS.md y v3/backtester/README.md. Reconocer refs/HEAD/worktrees/WIP locales al comienzo. Estado local hoy UNKNOWN desde CLOUD.
- Rama propuesta NUEVA: `feature/ef-campaigns-go`, desde master reconciliado, NO desde la rama Python. Reusar sólo si ya existe y corresponde al mismo mandato; ante otro trabajo, no reset/rebase/force/stash destructivo. Mantener la rama I0 como evidencia, sin merge/cherry-pick ciego.
- Diseño C06 y FUT-R01 son inputs funcionales. S04 READ_ONLY de referencia hasta adjudicar los deltas semánticos. Skills por routing: technical-project-manager, sdd-workflow/sdd-developer, echo-futures-research-manager cuando gestione selección, echo-retester-master + qualification runbook.
- En Echo, localizar la feature SDD owner antes de crear change: FEAT-CHALLENGE-HISTORY ya existe; usar un change nuevo para C06 y enlazar Runtime Pools donde cambien contratos. No crear segunda SPEC competidora ni sobrescribir el CHANGE-001 Python como si se hubiese implementado Go.
- Agents-OS: master directo con HEAD reconciliado, una escritura integrada por coordinador, change_log y readback; sin ramas/PR/force. Clones/worktrees/builds fuera del vault. Scripts de materialización de Agents-OS no son dependencias del producto Echo.

## 3. Matriz requisito → evidencia → aceptación

| ID | Resultado requerido | Estado source | Evidencia de salida |
|---|---|---|---|
| R01 | Una implementación Campaign por tipo, Strategy/MM en factories compartidas | Parcial Go | Misma Strategy con dos MM; módulo nuevo de test sin editar Campaign/scheduler |
| R02 | CHALLENGE N cuentas, una activa por asociación, continuidad técnica | Rotación legacy existe | Pase/fallo/pausa/drain/siguiente cuenta; fechas y causa, sin rewarmup |
| R03 | FUNDED N seeds/orígenes, cobros/pérdidas completos | Seed única legacy | Tres cuentas, rotación, pagadora luego perdida, pendiente sin cash |
| R04 | Etapas aisladas comparables sin mezclar caja | Batch existente | Dos jobs misma Strategy/diferente MM con scopes y denominadores separados |
| R05 | SIMULATION 1x1, USD4000/cero aportes/reinversión100% | Full journey parcial | Compra→pase→activación→payout recibido→nueva compra, conciliación |
| R06 | SIMULATION varias asociaciones/props en mercado y caja únicos | Composición singleton | Dos asociaciones operando a la vez, dos perfiles, disputa por último cash, long/short mismo mercado |
| R07 | Eventos, identidad, KPI y lectura legacy Go | I0 Python no aceptado como producto | Journal Go exacto, tests F/G/M rederivados y nuevos end-to-end |
| R08 | Plan/admisión/run/resume/report/export sin Python | Tooling S04 Python | Flujo completo en entorno sin Python, incluyendo rutas legacy capaces de ejecutar |
| R09 | Migración de catálogo y campañas antiguas | 89 IDs de referencia | Matriz source-target exhaustiva, equivalencia o nueva identidad, ningún receipt reescrito |
| R10 | Causalidad, replay/resume/idempotencia | Reutilización parcial | Continuación por rerun aislado idéntica, no doble gasto/cobro, error no publicado COMPLETE |
| R11 | G0–G5, runtime parity, HISTORICAL_ONLY y freeze | F01/F02 pendientes | Guard Go usado por todas las rutas; fixture frontera V1; no bypass de funded-only |
| R12 | Prueba física + código mantenible + evidencia de escala | No ejecutado para C06 | Tests, E2E, capacidad medida y revisión GOD independiente con corpus reusable |

## 4. Decisiones cerradas y parámetros obligatorios

Cerrado por Owner: Go-only; CHALLENGE/FUNDED/SIMULATION; módulos Strategy/MM separados; NQ; una activa por asociación; USD4.000 para caja comercial conjunta, cero aportes, reinversión completa del neto cobrado, payout variable, sin caps prudenciales añadidos, threshold challenge 1/3 con unidad/horizonte definidos, Forex separado. Runtime autoridad; no segundo motor.

Cerrado técnicamente por C06: reutilizar driver/SDK; versión nueva de contrato sin reinterpretar legacy; datos exactos; evidencia causal explícita; Go CLI existente; cash comercial único; paths OHLC comunes predeclarados para multi-asociación; resume por rerun aislado salvo soporte de checkpoint completo ya demostrado; deprecación Python por consumer inventory, sin puerto literal.

Inputs obligatorios que no inventa un agente: perfil/versiones y costes, origen funded, N, política MM por etapa, horizonte/corte, reglas de resets/refunds, prioridad de asignación de caja y política de retiro de cada escenario. Sin ellos, la corrida económica falla cerrada, pero el producto se puede desarrollar y probar con perfiles TEST_ONLY identificados. D05 G4 funded-only sigue decisión Owner/retester para histórico real; no bloquea la implementación ni acredita automáticamente una evaluación.

## 5. Tres shots de ejecución, no tres rondas por archivo

GO-S01 es el diseño/planning de esta sesión. Restan **tres shots**: GO-S02 implementación GLM-5.3-Flash local; GO-S03 review adversarial GOD local (razona/orquesta, delega Luna/Sol según tarea); GO-S04 corrección GLM local TOP/submanager, como pidió Owner. El uso de TOP para el corrector GLM es excepción explícita de este mandato; registrar modelo real, no etiquetarlo Sol por rol. No gastar otro shot GOD en diseñar de nuevo antes de implementar.

Las fases W0–W6 abajo son unidades de trabajo del Shot 2, no nuevos managers ni solicitudes Owner por cada archivo. El orquestador debe delegarlas con inputs/Allowed Files/return propios a workers frescos; puede avanzar dependencias técnicas dentro de su shot, pero no aceptar el gate Owner. Review y corrección sólo se despachan contra SHA exacto entregado por la fase anterior. El presupuesto es una entrega acotada por shot y un plan finito de tests; sin vigilancia indefinida, loops ilimitados ni promesas de tiempo. Si no cabe, devolver PARTIAL con trabajo y bloqueos exactos, nunca rebajar el alcance para decir terminado.

## 6. Plan detallado de implementación (GO-S02)

### W0 — reconciliación, inventario y contrato SDD

**Entrada:** C06, master/feature refs, código/SDD, S04 receipts/catalog, workers activos, herramientas disponibles. **Responsable:** orquestador + worker de inventario (read-only). **Depende:** nada.

1. Capturar branch/SHA, source tree, dirty/untracked, versiones y herramientas; comparar con 2baf319d. Resolver sólo deltas materiales. No volver a mergear S04 ni leer todo el vault.
2. Inventariar todo Python y sus invocaciones en flujo oficial Futures: scripts, imports, shell wrappers, CI, Make/go generate, data preparation, qualification, run/resume, report, fixtures y bytecode; separar producto, tests, histórico y ajeno. Matriz por entrypoint/consumer: REUSE_GO, IMPLEMENT_GO o RETIRE_REFERENCE_ONLY justificado. Usar búsquedas locales limitadas, no eliminar por extensión sin owner.
3. Recuperar interfaces Go exactas de Campaign, runner/supervisor, CLI, pools/fanout, RuleSet, scheduler, execution model y receipts. Validar los límites SOURCE C06. Registrar qué parte ya existe para no duplicarla.
4. SDD: SPEC del change C06, PLAN/Allowed Files por worker, TASKS atómicas y VERIFICATION vacío de claims; enumerar R01–R12 y pruebas. Registrar nuevo contrato semántico y compatibilidad sin alterar schemas legacy.
5. Matriz S04-F01: censo de planes V1 recuperado, tests Go de frontera a adjudicar; no migrar V1 a Unclipped por nombre. F02: ubicar guard histórico en su linaje sólo como contrato/fixtures; traslado a Go, no merge completo ClutiFX.

**Allowed:** documentos SDD del change y manifiestos de inventario; pruebas nuevas focales de baseline si autorizadas por SDD. **No tocar:** producto ajeno, datos, refs principales, runtime LIVE. **Gate interno W0:** base congelada, scopes de writers sin solape, contratos concretos/requisitos trazados. Conflicto material incompatible con C06 => PLAN_CONFLICT, no parche inventado.

### W1 — contratos Go, eventos económicos y proyección

**Depende:** W0. **Responsable:** worker Go economía/contratos, orquestador integra. **Leer:** platform_campaign.go, platform_research.go, cash/accounting/recorder existentes, identidad experiment/attempt, C06 §§3,6–8.

1. Definir formato nuevo versionado de campaña/composición y validadores tipados, refs de perfiles/MM/RuleSets y scopes; usar factories existentes. Los nombres futuros de C06 pueden ajustarse al repo sin alterar significado.
2. Centralizar cambios de caja/comprisos en el owner Campaign Go y emitir el evento identificable de la misma transición aplicada. Idempotencia, payload conflict, append failure y reconciliación antes de COMPLETE. No cálculo de PnL nuevo.
3. Implementar proyección Go reutilizable por ejecución online del backtest y lectura offline: mismas definiciones, ninguna decisión de trading. Estados UNKNOWN por métrica, numeradores exactos, cutoff a igual frontera, fuentes/linaje.
4. Adaptadores legacy por schema: no inference de primera funded/payout/attempt por etiquetas, monto+fecha o hash. Los casos Python F1–F11/G1–G4/M1–M4 sirven como entradas neutrales; expected se deriva de contratos Go y aritmética independiente.
5. Validar setup/operating fees, refunds, bundles paid-unprovisioned, resets/intentos, net received/reversals, causal attribution, replay y incomplete evidence. Precisión monetaria y tiempo nanosegundo/coordinate del runtime.

**Allowed:** campaign/profile/research/recorder/result Go del owner y archivos CREATE pequeños de contrato/eventos/report/adapter; tests nuevos. Cambios SDK sólo contrato compartido realmente consumido. **No tocar:** Strategy/MM de señales, risk arithmetic, v1 sellado, Python como implementación. **Gate W1:** unitarios con positivos/negativos y raw evidence, emisión y lectura concilian; no sólo tipos stubs.

### W2 — modalidades Go y N cuentas, primer vertical completo

**Depende:** W1. **Responsables:** workers lifecycle y perfiles/rotación, archivos disjuntos; integración única. **Leer:** RunPlatformCampaign, PlatformProfile/Validate, selectTurn/activateFunded/tickPayment, platform_registry, policies y controls.

1. Reutilizar controlador y extraer stage behavior común; materializar CHALLENGE/FUNDED/SIMULATION de C06 en nuevo request versionado. Aislar hardcodes GAU50/3000/cuatro pagos/5000 a su perfil legacy; el nuevo perfil exige campos contractuales sin defaults encubiertos.
2. CHALLENGE: múltiples derechos/cuentas, provisión, attempt/reset, pausa/pase/fallo, relevo drenado y continuidad Strategy/analytics. No comprar sucesora por un evento de pausa si policy no lo ordena.
3. FUNDED: N seeds/contextos con provenance, instalación real y MM de fase, inventario/selección, pagos repetidos, pérdidas antes/después, costes y pendientes. No exigir que CHALLENGE ejecute primero en una prueba aislada.
4. SIMULATION 1x1: mismo código de ambas etapas; inicio4000, cero aportes, demoras comerciales, compras/fees y cash acreditado financian siguiente compra. Payout configurable. No reportar financiable con cargo obligatorio omitido.
5. E2E Go de cada modalidad con fuente pequeña determinista que produzca órdenes/fills/round-trips y efectos comerciales. Emitir resultados y reportes Go del MISMO run; seeds de control señaladas TEST_ONLY.

**Allowed:** owner Campaign/platform/profile/registry y handlers/adapters Go del change, tests nuevos. **No tocar:** source de estrategias para forzar ganancia, guard, diarios reales. **Gate W2:** trayectorias funcionales completas no vacías y contabilidad cerrada; pruebas N=3 con una activa por asociación; no restart técnico al rotar. Entregar demo CLI de las tres modalidades, no un reporter aislado.

### W3 — composición causal multi-asociación/multi-perfil

**Depende:** W1/W2 y contrato R6 leído. **Responsable:** worker especialista Go/runtime, integración serial de archivos compartidos. **Lectura:** compose_account.go, RunState, accountCompartment, platform_registry, scheduler/ohlc_driver, views/config/pool reducer/claims/fanout y composición runtime compartida.

1. Extender el formato nuevo para cuentas/contextos/RuleSets por binding. Mantener el camino legacy monocuenta y el fail-closed de configs; sin skip del validator global.
2. Generalizar routing del driver desde selected global a owners scoped. Un mercado/reloj/scheduler; callbacks/timers/órdenes/controlDispositions acceden por identidad explícita. No goroutines independientes dentro de una trayectoria ni lista de RunState independientes sumados.
3. Conectar asociaciones al reducer/claims/fanout existente. Una activa por asociación; varias simultáneas; AccountPolicy, MM y nominal ledgers aislados. Conservación de epoch/drain/no-expansión R6. Estrategia compartida sólo si coincide toda la identidad técnica causal.
4. Bankroll común serializa compromisos/recepciones; probar dos compras demandando el último saldo: sólo una adquiere derecho, la otra queda blocked/no cash según policy. Comprobar net nominal nunca financia.
5. Mercado observado común y OHLC nuevo explícito LOW_FIRST/HIGH_FIRST independiente de posiciones, ambos sellados. No aceptar V2 legacy exposición-dependiente para composición simultánea. Dos perfiles contractuales TEST_ONLY prueban heterogeneidad; no simular que se validó una segunda prop comercial real.
6. Reanudación/replay: job completo reuse; incompleto rerun aislado desde inputs con nuevo attempt y efectos deterministas. Probar crash/failure al debitar/creditar/publicar, no sumar attempts ni pagos. No entregar checkpoint parcial que olvide MM/venue/reservas/timers.

**Allowed:** RunState/compose/registry/scheduler-routing/ohlc adaptation y mínimos contratos config/views SDK listados por SDD; no reescribir scheduler ni engine. Cambios semánticos comunes requieren regresiones runtime/backtester. **Gate W3:** dos asociaciones, dos perfiles, varias cuentas realmente activas simultáneamente, señales/fills/fees correlacionados, cash y estados conciliados; una única trayectoria demostrada. Si sólo funciona 1x1, R06 queda NOT_DELIVERED, no declarar capacidad completa.

### W4 — tooling Go, admisión y migración (puede avanzar en paralelo tras W1)

**Responsables:** worker CLI/migración y worker admisión/tests en owners disjuntos. **Leer:** cmd/echo-backtest/{main,experiment,platform,campaign,reproduce}.go, platform_search.go, Python inventory W0, catálogos JSON y qualification runbook.

1. Extender CLI Go existente (superficie lab propuesta) con validate/plan/prepare/run/resume/report/compare/migrate/qualify/export. Adaptadores de input llaman a funciones Go, no shell Python. Report es read-only, run/resume requieren admisión y budget.
2. Usar manifest/receipt/AttemptID/output publication existentes. Validar cantidad/identidad de variantes, fechas, dataset, policy y fuente. Cache sólo de material inmutable con clave causal completa, no de resultados por nombre.
3. Portar la admisión G0–G5 a Go con reglas y fixtures vigentes. Un owner común debe cubrir todas las entradas ejecutables antiguas/nuevas, también resume, sin bypass por etiquetas. No importar módulos Python ni usar sandbox con Python para el gate. Preservar D05 funded-only bloqueado cuando corresponda a histórico real.
4. Conservar supervisor único y límite global vigente seis motores incl. oráculos; medir recursos antes de nuevas corridas y respetar presión. Si su owner actual es Python, reemplazar esa implementación por Go bajo el mismo contrato operativo, no desplegar un supervisor paralelo.
5. Migrar matriz S04 referencia 26 nativas+63 SG y 15 aliases, revalidando inventario. Para cada una, formato old/new, semántica igual/nueva, MM/policy efectiva, campos UNKNOWN, gate y artefactos. Resolver el fixture V1 sin alterar autoridad del runtime. No declararla reproducible por conservar el JSON.
6. Cada comando Python tiene disposición y consumer actualizado. No port literal de herramientas sin utilidad; retirar explícitamente proyectores auxiliares sin consumidor preservando sus artifacts. Toda capacidad necesaria para flujo oficial tiene implementación Go, no shell legacy.
7. Retirar código/bytecode Python S04 del árbol activo del alcance una vez con reemplazo/retirement trazado; preservar Git history y JSON/datos. Cambiar README, AGENTS routing, builds/CI/runbooks propios que lo invoquen. No borrar archivos ajenos por extensión; si afectan GO_ONLY y no se pueden resolver, declarar alcance pendiente.

**Gate W4:** catálogo/migrador/admission CLI funcionan en proceso real sin Python instalado; el intento de ejecutar histórico sin qualification bloquea ANTES de motor. Todas las rutas al engine inspeccionadas y testeadas; Python retirado del camino oficial. Golden legacy pequeños se leen sin ejecutar scripts.

### W5 — matrix funcional, E2E y capacidad medida

**Depende:** W2/W3/W4 integrados al mismo SHA. **Responsable:** worker de pruebas funcionales no autor de los seams críticos, sin sustituir GO-S03.

1. Suite go test de módulos afectados y regresiones de runtime/SDK/paridad. Ejecutar race donde el host lo soporte; falta de compilador no equivale a PASS y debe resolverse en host compatible aprobado o quedar residual explícito. Coverage de desarrollo nuevo >=95% según policy, invariantes primero, no tests tautológicos.
2. Positive/negative oracles para todas las capacidades R01–R12: caja real4000, paid-not-provisioned, bundle conocido/desconocido, gratis/pagado reset, delays, payout variable, setup, refunds/reversals, missing/conflicting event, gaps causales, same RunID/different attempts, shared-cash collision, two RuleSets, opposite exposures, rollover, days paused, MM separation, failure recovery.
3. Censo completo de configuraciones aprobadas (referencia89) para validación/materialización Go y smoke técnico con datos admitidos. No expandir estrategias/variants ni cambiar sus parámetros para llenar celdas. Ninguna excluida silenciosamente. Aliases separados de ejecutables.
4. Campañas con datos históricos físicos sólo de identidades elegibles, con presupuesto y ventana sellados en manifest. G0–G5 siguen vigentes; sin dato/qualification/D05: BLOCKED con causa, no falso PASS ni histórico de cientos de sesiones. Separar catálogo validado, campañas ejecutadas y resultados económicos; matrices exhaustivas.
5. Gate GO_ONLY en entorno limpio: binario Go y archivos de configuración/datos, sin Python/venv/pip. Ejecutar prepare→admit→run→report→resume/reproduce/export y gates oficiales sin Python. Inspección de dependencias/procesos/CI; JSON output determinista e inputs intactos.
6. Medir corpus, eventos, asociaciones, cuentas, RSS, CPU, tiempo y throughput para tamaños 1/10/100 de configuración con fixtures acotados según recursos; no extrapolar infinito ni confundir cien configuraciones con cien engines físicos. Demostrar memoria sin crecimiento por cuentas retiradas, cancelación/drain y cero huérfanos.

**Gate W5:** manifiesto de acceptance y pruebas en SHA integrado, diferencias baseline explicadas por causa (no sólo nombres de fallos), ejemplos reproducibles sin comandos inventados y sin gastos/trading. Toda celda no demostrada conserva su estado. Resultado negativo de Strategy no es bug de Campaign ni permiso de ajustar señal.

### W6 — integración del candidato y handoff de implementación

**Responsable:** orquestador GO-S02, único integrador. Revisar diff final, doc, SDD, movimientos de código legado y consumo de recursos. Publicar rama producto de trabajo y comprobar remoto. No merge a master ni release.

Entregar `GO-S02-IMPLEMENTATION-RETURN` con base/branch/SHA/build hashes, matriz R01–R12, inventario Python y disposición, matriz legacy→nuevo, Go-only, pruebas exactas/outputs, workflows por modalidad, measured capacity, qualification ledger, pendientes y corpus adversarial reusable. Los names de archivos de retorno se resuelven en el paquete de prompts; no crear otro planner. Resultado IMPLEMENTATION_CANDIDATE o PARTIAL/BLOCKED, no aceptación Owner.

## 7. Revisión adversarial — GO-S03

GOD LOCAL actúa como submanager del review, no implementa producto. Debe leer código/diff/source + diseño y **probar** falsificadores por delegación real. Luna: inventario, reproducción, captura/logs/checksums/dependencias. Sol: controles/claims/event-order/MM-parity/RuleSets, cash/lineage, replay, escenarios simultáneos y harness Go independiente. Independencia de autor, de corpus y de modelo se registran por separado; no sustituir modelo sin declarar/autorizar.

Un worker de review no edita main product; harness Go propio y fixtures inmutables. Oráculos no copian helpers ni expected del implementador. Revisar especialmente cash cero compartido, fecha efectiva vs aplicada, cualquier launcher como bypass, señales comunes con distintos MM, jobs/retries, ausencia de Python y migration semantics. Perturbaciones de datos contradictorios deben producir error/UNKNOWN, no métricas perfectas. Review no decide producto nuevo ni relaja reglas para obtener verde.

Output: VERIFY_PASS/FINDINGS/BLOCKED con severidad, fuente, expected/actual, comandos ejecutados y archivos/hashes reproducibles. Findings con fix local compatible quedan aceptables como entrada de corrección en GO-S04; cambio de regla económica/arquitectura requiere manager. No quinta auditoría amplia por rutina. Keeper de corpus S03 permanece distinto del implementador durante el cierre.

## 8. Corrección y gate final — GO-S04

GLM LOCAL TOP/submanager corrige el alcance adjudicado, con subagentes implementadores por owners y un worker fresco de retest que no escribió esos parches. Integrar a tests permanentes los falsificadores durables, manteniendo originals del review como evidencia. Ejecutar corpus S03 **sin debilitar assertions** y todas las regresiones afectadas en FINAL_SHA.

TCR únicamente por oráculo erróneo sustentado en contrato vigente, con viejo/nuevo expected y razón; nunca cambiar tests para aprobar sin revisión. Si emerge un defecto ordinario dentro del scope, corregirlo en este shot; si contradice requisitos, PARTIAL/BLOCKED exacto. No ocultar bloqueos porque se acabó el shot ni iniciar loop infinito.

Gate final devuelve READY_FOR_OWNER_REVIEW sólo con R01–R12 entregados en su alcance, cero defectos materiales pendientes, código limpio/modular, Go-only completo, matrices de migración/ejecución y límites honestos. Si una corrida histórica está bloqueada por gates externos, distinguir producto listo de estudio económico pendiente; no declarar todas las estrategias corridas. Merge/promoción y LIVE siguen fuera del mandato.

## 9. Matriz mínima de aceptación adversarial

| Gate | Oráculo independiente exigido |
|---|---|
| A01 reutilización | Dos Strategies y dos MM concretos via factories, misma Campaign; test plugin fixture no cambia scheduler/ledger |
| A02 rotación | Tres cuentas: perdida/pasada/pausada; una activa/asociación; estado técnico continuo, financiero aislado |
| A03 funded | N seeds con origen; una paga dos veces y luego pierde; contabilizar todas N y ambos pagos |
| A04 caja | 4000-100 compra-500 setup+780 recibido=4180; nominal loss no resta; approved-only no compra |
| A05 pendiente/bundle | Dos compras100, una no provisionada y otra pasa => U2, P1, coste/pase200; bundle2 por180 no dos cargos |
| A06 idempotencia | Mismo event ID idéntico una vez; distinto payload conflicto; reinicio/rerun no duplica saldo ni factura |
| A07 simultaneidad | Dos asociaciones y dos perfiles mismo clock; última caja alcanza una compra; desempate estable independiente de concurrencia física |
| A08 mercado | Long/short comparten secuencia; OHLC común explícito, sin ruta elegida por beneficio o posición de cada cuenta |
| A09 causalidad | Payout antes de pase/activación, event futuro/unknown, crédito de otra cuenta => rechazo/gap, nunca Q probado |
| A10 evidencia | Cutoff y saldo misma frontera; temporal/final estados separados; errores técnicos y censura visibles |
| A11 migration | V1/Unclipped no cambiados sin identidad; legacy outputs sellados byte-intactos; nuevos escenarios declarados |
| A12 admisión | Direct run, platform-batch, campaign, lab/resume no pueden saltar guards; propósito por inputs reales |
| A13 Go-only | Todos los comandos oficiales y gates funcionan en entorno sin Python; no wrapper/venv/pip/exec python |
| A14 recuperación | Mid-debit/credit/publication failure, rerun o replay existente: resultado final igual, una publicación canónica |
| A15 cobertura catálogo | Inventario completo referencia89 y aliases; cada fila VALIDATED/EXECUTED/BLOCKED; no expansión cartesiana |
| A16 rendimiento | Medición reproducible y presupuesto, sin OOM/huérfanos; no confundir benchmark sintético con histórico certificado |

## 10. Gate control, entregables, rollout y rollback

| Shot | Entrada | Salida verificable | Puede aceptar Owner o mergear |
|---|---|---|---|
| GO-S02 implementación | C06 + base reconciliada | Candidato Go completo, matrices y receipts | No |
| GO-S03 GOD adversarial | SHA exacto S02 + corpus | Reporte independiente + harness reusable | No |
| GO-S04 GLM TOP corrección | Findings S03 adjudicados | FINAL_SHA + regresiones + GO_ONLY + matrices | No |

Cambios de campo/parámetro que alteran semántica tienen schema/policy version nuevo. No cambiar como fallback un perfil antiguo para satisfacer test. Habilitación nueva opt-in hasta aceptación, sin Python fallback. Mantener lectura/replay de historia sobre Go. El corte de supervisor no permite dos owners; si falla, abortar admisiones nuevas sin encender automáticamente Python.

Rollback: detener nuevas ejecuciones del candidato, conservar artifacts/receipts y rama; revertir sólo commits propios bajo policy, no reset ni force ni borrar historia. No desplegar a runtime ni mutar cuentas/configuración productiva. Una eventual vuelta a binario legacy requiere decisión explícita, no reinstala Python como autoridad oficial. Consumo Pro solamente confirmado o UNKNOWN.

## 11. Continuidad y operación de agentes

Cada delegación contiene capability/modelo real/surface/work function, input SHA, task, Allowed/No tocar, presupuesto finito, pruebas, output y stop. Un integrador por wave; workers sin permiso de editar planner/diseño/quotas. Matriz de archivos/owners evita writers concurrentes. Persistir checkpoints de phase en el mismo planner sólo por orquestador y después de evidencia, sin crear nota por microtarea.

Workers ONE-SHOT cargan agents-os-agent-run-register cuando aplique, agents-os-session-feedback y agents-os-session-close; entregan activos reutilizables y feedback concreto o NONE, paths/SHA/estado. Cierran exclusivamente su encargo. Los submanagers locales no reemplazan al manager de esta conversación ni al manager I+D. Sesión coordinadora y programa no se cierran automáticamente.

## Bitácora

2026-10-29 — Owner revoca Python como solución final y pide diseño+plan Go-only y tres shots locales. Se publica C06; el merge I0 previamente preparado queda cancelado como vía de entrega. No se cambia código Echo. Se compactan fuentes activas y se preservan byte-snapshots históricos para no perder continuidad. La siguiente acción es el despacho GO-S02 del paquete [[EF-CAMPAIGN-MODES-I0-LOCAL]].

2026-10-29 (GO-S02 ejecutado) — Shot de implementación Go-only completado como IMPLEMENTATION_CANDIDATE: 7 commits sobre `feature/ef-campaigns-go` (base `2baf319d`), tres modalidades E2E reales, composición multi-asociación causal con paridad monocuenta byte-idéntica, guard G4/G5 en Go en 5 puertas, migración 26+63+15 por identidad (censo delta CERO) y retiro Python del alcance con registro. Regresión = baseline ambiental exacto; Go-only probado sin python3 en PATH; hallazgos de verificación corregidos en-shot (orden causal Q(H), canary del gate). Residual honesto: coverage parcial, sin `-race`, cero corridas económicas históricas (D01/D02/D05 Owner). W5 perdió delegación por quota del host (cierre por integrador; independencia de autor diferida a GO-S03). Retorno canónico: [[EF-CAMPAIGN-MODES-GO-S02-RETURN]]. Siguiente: GO-S03 sobre `062b6df7` exacto; no ejecutarlo desde este shot.

2026-10-30 (GO-S03 ejecutado, GOD local) — Review adversarial sobre `062b6df7` exacto: STATUS **FINDINGS** (retorno [[EF-CAMPAIGN-MODES-GO-S03-RETURN]]). Adjudicación por delta, separando lo reportado por el autor de lo demostrado por el review: build/diff/regresión/Go-only/migración-catálogo/economía v2 del alcance VERIFICADOS independientemente (sonda GOD con 7 rechazos nombrados reproducidos por entrada pública; suites 23=23 idénticas al baseline; matriz reconciliada con censo CERO y 5 SEALED; lab report identidad byte-idéntica sin Python). NO demostrado por S02 y dimensionado aquí: (F1/F2, P1) TGMM/RGMM y cualquier heterogeneidad de MM/perfil/RuleSet por asociación imposibilitada por la admisión v2 — el claim "2 perfiles/2 RuleSets" no está materializado (los tests ligan el mismo perfil); (F3, P1) FUNDED multi-asociación sin implementar; (F4, P2) CloseSafety sin superficie v2; (F5, P2) reverso/refund sin productor; (F6, P2) MIGRATED=LEGACY_PATH con SAME_SEMANTICS por resolución de constantes; (F7, P2) coverage <95% en 6/9 archivos re-medido y perfil crudo del autor vacío; (F8, P3, NEEDS_OWNER_DECISION) puertas legacy con guard opt-in; (F9, P3) capacidad sólo anillo 1×N; (F10) independencia de modelo NO lograda — la cuota del host mató los 4 despachos clf-flash (incluido el contrapeso del propio review, reintentado hoy por pedido del usuario) y el review lo ejecutó el GOD directamente. 0 NEW_REGRESSION; -race NOT_EXECUTED (sin gcc). GO-S04 queda READY_FOR_DISPATCH sobre `062b6df7` con el paquete A–E del retorno; harness/receipts reutilizables en `~/echo-work/c06-s03/`. Cierre exclusivo de GO-S03; manager y programa abiertos.

2026-10-30 (GO-S03R1 ejecutado, relevo del review — MODEL_MISMATCH declarado) — Complemento de GO-S03 sobre el mismo `062b6df7`: **REVIEW_COMPLETENESS COMPLETE / PRODUCT_VERDICT FINDINGS** (retorno [[EF-CAMPAIGN-MODES-GO-S03R1-RETURN]]). La superficie volvió a exponer GLM-5.3-Flash; el mismatch se declaró antes de gastar la batería y el Owner decide si re-dispacha el contrapeso no-GLM. Completado: contrapeso F1–F10 (F1–F7 confirmados con source re-leído y sondas re-ejecutadas; F8 RECLASSIFIED a defecto WITHIN_C06 — bypass físico demostrado: `platform-batch` corrió el mismo request v2 sin miembro qualification mientras el lab lo clasifica y gatea; C06 §11 ya cerró la regla, la alternativa ledger-only del S03 se descarta; F9 cerrado con K=2/K=3 simultáneos medidos, sin fuga; F10 persiste); harness económico independiente 13/13 con oráculos derivados del contrato (cash 4140/3880/3760/3640 exactas, linaje Q(H) con orden estricto, emisor idempotente/conflicto, fallo de publicación nunca COMPLETE, proyector procesa refund que el lifecycle nunca emite); DOS hallazgos nuevos P2 (NF1 `AccountSlots` sin cap en CHALLENGE — 3 unidades con inventario 1; NF2 disputa de caja asimétrica por motor — `OPERATION_OWNER_MISSING` al invertir prioridades a favor de s2b) y NF3/NF4 P3 (activación funded ~1 min tras PASS sin consumir el calendario de compliance; `reproduce --result` sin artefacto .gz en items del lab); causa raíz de `lab prepare` corregida — el base-spec de W5 era `{}` placeholder y el error saltaba ANTES de cargar NT, la cadena física validate→plan→prepare→run→report→resume(REUSE)→export quedó verde sin python3 con corpus sintético propio (digest `3d281190…`), BLOCKED_EXTERNAL refutado como clasificación. Cuota de delegación muerta re-verificada con 1 despacho propio. GO-S04 READY_FOR_DISPATCH sobre `062b6df7` con el paquete ÚNICO consolidado (A–E + E1–E6). Cierre exclusivo de GO-S03R1; manager y programa abiertos.

2026-10-30 (GO-S04 ejecutado, corrección GLM local TOP) — Shot de corrección cerrado sobre el SHA revisado exacto `062b6df7`: **C06_DELIVERY = PARTIAL**, **FIRST_STRATEGY_CANDIDATE = SELECTED_FOR_REVALIDATION** (retorno [[EF-CAMPAIGN-MODES-GO-S04-RETURN]], FINAL_SHA `baca3c60`, 16 commits). Disposición: F1–F4, F6, F8, F9, NF2, NF3 y NF4 **corregidos**; F5 **parcial** (el productor de REVERSO existe; el de REFUND de lifecycle no, y no hay transición declarada que lo dispare — inventarla sería economía nueva prohibida); F7 **parcial** (cobertura 79,6% diff-aware statement-based, bajo el piso 95%, declarado sin maquillaje); F10 **persistido** (no hubo verificador no-GLM: todo el trabajo es GLM-5.3-Flash). NF1 se corrigió **según la adjudicación del Owner** (inventario concurrente de asientos, sin cap de compras de por vida), no según el mínimo propuesto por el revisor. Dos defectos ordinarios pre-existentes se corrigieron de paso (clasificador de read-set que contradecía su propio test de tabla; assertion no determinista del log de eventos = el "FAIL único no reproducido" de S03R1). Materialización real del catálogo: 104 filas, 27 `V2_ADMITTED` con digests, 62 `BLOCKED` con causa exacta, 26 `LEGACY_PATH_PRESERVED`, 15 aliases, 0 históricas; el desbloqueo de las 62 es un manifest Owner de account policies RG por identidad (los presets sellados de R01/R03 ya las declaran). Verificación: conjunto de fallos **23 = 23 idéntico al baseline**; corpus del verificador re-ejecutado con bytes intactos (15/21 PASS; los 5 FAIL son exactamente las mutaciones TCR); Go-only físico sin python3 (`lab migrate --materialize-v2` exit 0, 28 artefactos); capacidad K=5. Candidata económica #1 `LAB-SG-FBC-CH300-15M-R500` (26→9, 666,67 USD/pase, 0,73/día, mediana 27 días) materializada, admitida y ejecutada mecánicamente — **no** revalidada históricamente, **no** evidencia funded, y **LIVE_BLOCKED** por `riskgeometry` HISTORICAL_POLICY_ONLY (guardas intactas). Handoff al frente Runtime Pools ya existente con 4 puntos concretos (habilitación LIVE del módulo RG; manifest de account policies RG; cadena G0–G5 + D01/D02/D05 + receipts sobre la ventana sellada de 785 sesiones; presupuesto/ventana de revalidación). Sin merge a master, release, deploy, compras ni armado de trading. Cierre exclusivo de GO-S04; manager y programa abiertos.
