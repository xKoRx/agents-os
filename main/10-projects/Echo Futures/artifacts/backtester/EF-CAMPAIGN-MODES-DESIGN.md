---
type: doc
schema_version: 1
status: active
area: "[[Trading]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo I+D — Futures]]"
  - "[[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]]"
  - "[[Echo Futures — Optimización de Campañas]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-28"
updated: "2026-10-29"
---

# EF-CAMPAIGN-MODES-DESIGN

## Propósito

**C06 — GO-ONLY. Decisión Owner del 29-10-2026.** Entregar CHALLENGE, FUNDED y SIMULATION reutilizables, su ejecución/orquestación, migración y reporting oficial en Go, sobre el runtime y backtester existentes. Cien Strategies y cien MM NO implican cien implementaciones de Campaign.

Este documento sustituye como diseño vigente C01–C05 y sus paquetes I0 Python. Conserva sus requisitos económicos válidos, pero **revoca la recomendación de merge del I0 Python**. `feature/ef-campaign-modes-i0@01a38c13b0a1b280eefb9d18f6d2b167e3cd8739` es REFERENCE_ONLY / SUPERSEDED_FOR_DELIVERY: no merge, no cherry-pick de su reporter, no dependencia de ejecución. Sus contraejemplos son candidatos de pruebas Go, no un oráculo de verdad ni una especificación para traducción línea a línea.

Estado: DESIGN_READY_FOR_IMPLEMENTATION; PRODUCT_IMPLEMENTATION_NOT_EXECUTED por esta revisión CLOUD. Es diseño autorizado dentro del mandato Owner, no certificación del código futuro. Planner único: [[Echo Futures — Optimización de Campañas]]. Mandatos: [[EF-CAMPAIGN-MODES-I0-LOCAL]] (se conserva el path histórico; su contenido vigente es GO-S02/S03/S04). El manager existente y el programa permanecen abiertos. PROD sigue FROZEN_BY_OWNER. Ningún merge de producto o trading queda autorizado por diseñar o implementar.

## Contenido

### 1. Baseline y evidencia: qué existe realmente

Corte source inspeccionado: `xKoRx/echo@2baf319ddcba622d9557bc9f23a13787b44c58a7`, master remoto al iniciar. El ejecutor reconcilia cualquier avance/WIP antes de escribir. No partir de la rama I0 Python.

| Fuente existente en Echo | Evidencia y reutilización | Límite que C06 debe resolver |
|---|---|---|
| `v3/backtester/README.md` | Motor Go, reloj virtual, cursor, scheduler, Strategy/MM/Provider/accounting compartidos; APIs NewRunWithComposition, AdvanceUntil, EnqueueControl, Finish, ReplaceAccount | README contiene snapshots históricos; código y contratos ejecutables prevalecen |
| `v3/backtester/cmd/echo-backtest/main.go`, `experiment.go`, `platform.go`, `campaign.go`, `reproduce.go` | Un CLI Go ya tiene run, reproduce, experiment, campaign, platform-prepare/batch, daily-report, validate-catalog y publish; experiment ya distingue experiment identity y attempt físico | Extenderlo, no crear un binario/orquestador alternativo |
| `v3/backtester/platform_campaign.go`, `platform_profile.go`, `platform_registry.go`, `platform_operability.go`, `platform_research.go` | Lifecycle, inventario, selección/rotación, fees, pagos demorados y caja existen en Go | Perfil E2T/GAU50, constantes y políticas específicas; FUNDED_ONLY instala una seed; selected es global |
| `v3/backtester/compose_account.go` | compone Strategy una vez; accountCompartment conserva MM/Provider/accounting/venue; NewSealedMoneyManagerCatalog/WireSealedMoneyManagers/SealedAccountPolicy reutilizan runtime | composeAccount exige exactamente una cuenta; cablear catálogo no demuestra ejecución multi-asociación |
| `v3/sdk/futures/config/snapshot.go`, `composition.go` | StrategyDef, AccountDef, PoolDef, PoolAssociationDef y factories compartidas | Validación global de RuleSet y composición monocuenta requieren extensión versionada, no bypass |
| `v3/backtester/ohlc_driver.go`, scheduler/controls actuales | Una causalidad de mercado y controles | La trayectoria OHLC legacy puede depender de la exposición seleccionada; no es modelo común válido para cuentas opuestas simultáneas |
| `v3/backtester/platform_search.go` | RunPlatformBatch, receipts, límites de evidencia, recorder compacto y publicación existentes | Reusar runner; un batch de runs independientes no es SIMULATION conjunta |
| `tools/tradesgerard/campaign-lab/{campaign_lab,research_lab,s02_trials}.py` bajo backtester | Python S04 existente: planes, ejecución del binario Go, análisis y experimentos auxiliares | Legado, NO diseño oficial futuro. Inventariar consumidores, sustituir capacidades necesarias y retirar dependencia |
| `EF-S04-INTEGRATION-RECONCILIATION` | S04 SOURCE integrado; V1 histórico no equivale automáticamente al V1 de master; guard Python ausente en corte | Resolver paridad afectada y admisión Go antes de nuevas campañas económicas |

Estas lecturas acreditan SOURCE, no builds, tests físicos, capacidad del host ni deploy. El I0 Python y sus gates previos no certifican esta arquitectura Go.

### 2. Fronteras obligatorias

- **Strategy:** decisiones técnicas, requisitos/analytics y continuidad de señal. No sabe de compras de cuentas ni caja comercial. Una cuenta pausada no pausa ni reconstruye Strategy. No replay de señales antiguas al relevar cuenta.
- **MM y AccountPolicy:** sizing/gestión monetaria, objetivos/pausas por su contrato. Una configuración reusable produce estado aislado por cuenta/operación. Campaign no recalcula DD, lotes o targets técnicos para reemplazar estos owners.
- **Provider/accounting/runtime pools:** reglas, reservas, órdenes, fills, PnL nominal, claims/fencing/afinidad/drain. Mantener autoridades SDK/R6 y paridad con runtime; backtester se adapta al runtime.
- **Campaign Go:** compras, derechos/provisión, intentos, activación, obligaciones, retiros y caja comercial; reacciona a hechos de los owners, no vuelve a evaluar sus reglas.
- **Reporting Go:** proyección pura de evidencia Go y compatibilidad legacy, KPI/completitud/conciliación. No toma decisiones de trading/compras ni genera estado de resume.
- **Runner/supervisor Go:** jobs físicos independientes, recursos, cancelación, attempts y receipts. Es distinto del scheduler causal del motor; ambos conservan un único owner, sin otro servicio de scheduling.

No crear Campaign por Strategy/prop, implementaciones paralelas de Strategy/MM, otro motor contable, un runtime de investigación alternativo, DSL, plugins dinámicos ni factories abstractas sin consumidores. No importar `core/internal` desde backtester. Las funciones compartidas viven en su owner SDK cuando corresponda; la adaptación de simulación permanece en backtester.

### 3. Modelo reusable y configuraciones

Los siguientes nombres describen contratos propuestos; NO son APIs ya existentes. Materializarlos sobre tipos existentes y adapters concretos mínimos.

**CampaignDefinition:** versión semántica, modalidad, perfil comercial y refs selladas de Provider/RuleSet, políticas de adquisición/rotación/retiro, condiciones iniciales, horizonte y reglas de observación. **CampaignInstance:** ocurrencia y cohorte, bindings/associations, inventario de cuentas y referencia a su ámbito de caja/mercado. **Association:** Pool + Strategy/config + MM/config/version; referencia el contrato R6, no inventa otro tipo de afinidad. Una Strategy puede estar asociada a varios MM sin duplicar código de Strategy ni compartir estado financiero mutable.

Ejemplos: GAU50/E2T CHALLENGE y GAU50/E2T FUNDED son dos configuraciones del mismo lifecycle por etapa, no dos motores y mucho menos dos implementaciones por Strategy. N cuentas están disponibles en el pool, una sola activa a la vez por asociación; varias asociaciones pueden operar simultáneamente. Relevo sólo ante la decisión/estado aplicable: pérdida, pase, pausa, elegibilidad o terminación comercial no son eventos equivalentes. Conservar prioridad/antigüedad y retorno diario bajo las reglas R6 vigentes; no inventar CreatedAt para seeds legacy.

**Evidencia separada de ejecución:** definition/request digest inmutable; experiment/run identity determinista; attempt físico generado por runner; instance/association/account IDs scoped; artifact/receipt revision y hash. Igual RunID no prueba mismo attempt. Un hash de archivo no fabrica una compra. Revision sólo sustituye la proyección identificada con provenance y definición compatible; nunca last-input wins entre reejecuciones distintas.

No producto cartesiano implícito Strategy×MM×prop. Un plan finito enumera combinaciones admitidas. Añadir Strategy o MM requiere su módulo/config/registro y pruebas, pero no cambiar Campaign/scheduler/venue.

### 4. Tres modalidades, una implementación de cada comportamiento

**CHALLENGE:** lifecycle de evaluación, cohortes pagadas, provisión, intentos, resets/renovaciones y pase/fallo/pendiente. Al pasar, no iniciar funded salvo que se trate del recorrido SIMULATION. Medir costes de todas las unidades, no sólo ganadoras. Permitir política explícita de compras/demanda y rotación; no introducir financiación ilimitada por defecto. Una modalidad analítica de acumulación de costes histórica se conserva etiquetada como tal, nunca se renombra a caja finita.

**FUNDED:** origen obligatorio (seed exógena, contexto derivado de un pase concreto, o distribución modelada identificada), inventario inicial N, MM por etapa, pérdidas y pagos repetidos. Todas las cuentas iniciadas integran el denominador; cero pagos no elimina cuentas. Una seed exógena no demuestra adquisición financiada. Instalar contextos mediante los controles reales, no cambiando un string de phase.

**SIMULATION:** compone etapas, asociaciones, cuentas y props en UNA trayectoria causal. Caja comercial inicial USD4.000 UNA VEZ, cero aportes, reinversión del 100% del neto efectivamente recibido. Cuentas operan/concluyen/cobran en el mismo histórico y compiten por esa caja. La comparación CHALLENGE/FUNDED independiente son dos jobs relacionados, no un cuarto modo ni una SIMULATION por suma de curvas.

Los comportamientos de etapa se reutilizan en SIMULATION. No ejecutar `RunPlatformCampaign` por participante y sumar resultados. Policies nuevas usan tipos/configuraciones concretas versionadas; el switch de modalidad del controlador existente es suficiente mientras haya tres casos.

### 5. Composición multi-asociación: adaptación necesaria, no promesa de cero refactor

Extender el driver Go existente de forma acotada: conservar un cursor/mercado/reloj/scheduler por SIMULATION; indexar owners de cuenta por AccountID y routing por association/assignment/claim. Cada compartimento mantiene Provider, ledger nominal, MM/Operation, venue, órdenes, reservas, contexto y timers financieros propios. Strategy/analytics comparten sólo estado compatible con identidad causal/config; nunca por coincidencia de módulo.

Un turno global mutable no puede ser autoridad de todos los callbacks. El evento, callback, control y timer conserva AccountID/association/epoch explícitos; su ejecución accede al compartimento correcto aunque otra cuenta rote. No alternar un puntero global después de que ya se generaron callbacks ni duplicar el cursor por cuenta. Reutilizar pool reducer, claims, fanout y controles existentes. La ejecución de una trayectoria es determinista y serializa efectos causales; paralelismo físico sólo entre experimentos independientes/preparación inmutable.

**RuleSets:** resolver la versión sellada por binding/account contra el catálogo compartido. Ampliar la validación/composición Go para permitir RuleSets heterogéneos en el nuevo formato, con consistencia entre términos comerciales y riesgo de cada binding. Mantener validación legacy sin desactivar guards ni sustituirla por defaults. Un perfil faltante/incompatible falla cerrado. Dos perfiles TEST_ONLY prueban multi-prop; no se inventan reglas actuales de una empresa para anunciarla soportada.

**Mercado común:** en TRADE/BBO observado todos reciben la misma secuencia normalizada. En OHLC, la nueva composición exige un modelo común explícito, independiente de posiciones. Propuesta técnica implementable: variante versionada de camino compartido con orden de extremos LOW_FIRST u HIGH_FIRST sellado ANTES de ejecutar; no elegirlo según resultados ni por cuenta. Ambos preservan el mecanismo causal/lazy actual y se prueban con cuentas long/short simultáneas. No son ticks observados ni una garantía de peor caso. El modelo V2 legacy dependiente de una cuenta se conserva para replay antiguo y se rechaza para nueva composición simultánea. La variación de modelo produce NEW_EXPERIMENT.

El orden de desempate entre solicitudes de compra de igual frontera es determinista y predeclarado, reutilizando la coordenada del scheduler y un identificador estable de asociación. La política puede definir prioridades explícitas; no depende del orden de goroutines. El primer compromiso reduce disponible antes de evaluar el segundo. Cambiar prioridad es configuración versionada, no prudencia financiera añadida.

### 6. Caja y lifecycle comercial: un owner Go

Reutilizar la caja y mecanismos de cargo/pago de Campaign existentes, extrayendo funciones comunes pequeñas cuando los tres modos las necesiten. Un owner de bankroll por trayectoria; no un servicio financiero nuevo. Los ledgers nominales SDK continúan independientes.

`cash_settled = initial_cash + payouts_net_received + refunds_received - external_costs_paid`.
`cash_available = cash_settled - outstanding_unpaid_commitments`.

No sumar PnL nominal ni dinero solicitado/aprobado; no volver a restar pérdida nominal, fee ya deducido del payout neto o una obligación al reservarla y al pagarla. Registrar liberación de reserva al liquidar/cancelar. Financiación externa sólo puede existir en perfiles legacy explícitos de investigación, nunca en SIMULATION nueva.

Una adquisición cobrada existe aunque su derecho esté pendiente. Bundle K conocido crea K unidades comerciales con un pago; coste asignado suma exactamente la factura. K desconocido en legacy mantiene gasto y cardinalidad UNKNOWN. Reset contractual abre intento económico; retry técnico no. Renovación no fabrica adquisición. Refund modifica caja/coste neto una vez y conserva la cohorte bruta cobrada. Transiciones provisión/pase/activación/cobro fallidas o pendientes permanecen al horizonte.

Activación funded se acredita al aplicar el control/instalar contexto, no por `review_at`, `credentials_at`, `compliant_at` programado ni `FUNDING_INSTALL_PENDING`. Fees de setup pertenecen a adquisición; costes funded operativos posteriores quedan separados. Payout tiene solicitud, aprobación, débito aplicado, crédito efectivo y eventuales reversos con identidades propias. Primer cobro positivo se conserva como hecho histórico aunque un reverso posterior reduzca el neto.

Retiro variable: importe, momento, continuidad y máximo contractual se declaran por política/perfil; no imponer 3000, cuatro payouts ni 25% del legacy a escenarios nuevos. No optimizar con los datos de evaluación. En este ciclo se implementa la capacidad y parámetros; elegir retiro óptimo sigue siendo investigación I+D.

### 7. Evidencia nueva completa; lectura legacy conservadora

Ampliar el journal/recorder Go existente con un contrato de eventos comerciales versionado. Campos mínimos cuando aplican: schema/producer/build, definition/request digest, instance y economic scope, association, acquisition unit/right/economic attempt/account, obligation/payment IDs, event/cause ID, importe exacto/moneda, etapa, términos/perfil/RuleSet sellados, efectivo y compromisos antes/después, tiempo económico y coordenada de observación/aplicación. No añadir DB, broker, bus o event-sourcing framework.

Identidad de efecto estable dentro del scope; mismo ID y payload idéntico es replay idempotente, mismo ID con términos distintos es conflicto que impide afirmar conciliación. Tiempo efectivo puede diferir del momento en que el driver observa/acredita: cash sólo financia compras desde la aplicación causal, nunca retroactivamente por ordenar `CreditAt`. Mantener precisión nanosegundo/coordenadas de Go; iguales timestamps no eliminan el orden causal.

Dinero con tipos exactos existentes SDK y política explícita de redondeo contractual; no float64 para dinero ni aproximar importes al reconstruir. Ratios conservan numerador/denominador; redondeo sólo presentación. Los documentos originales, configs y artifacts sellados nunca se reescriben.

Reporting normal consume eventos y resultados tipados, NO reinterpreta arrays JSON mediante heurísticas Python. Adaptador Go legacy explícito por schema devuelve hechos recuperables, provenance y lagunas. No inferir AccountID de importes/fechas, ni control aplicado por un estado futuro. Los nombres de campos legacy conservan significado del productor Go (`other_spend=STOW_FEE+PLATFORM_FEE` en ResearchFundingSummary observado). El parser no es otro motor comercial.

### 8. KPI y completitud

CHALLENGE: U=unidades inicialmente cobradas con cantidad demostrada, P_U=unidades con pase, A=intentos económicos iniciados y P_A=intentos con pase. P_U/U y P_A/A separados; coste de cohorte por pase y por funded realmente disponible; muestra, seguimiento H, censura, pérdidas/pending y causa. Cero éxito produce N/A con gasto visible; desconocido nunca se transforma en cero. El umbral Owner 1/3 sólo se adjudica con unidad/resets/refunds/horizonte explícitos; el reporte descriptivo no elige esos términos.

FUNDED: N iniciadas, pagadoras, pagos/ciclos, W neto recibido, F_op externo no incluido en W/adquisición, pérdidas antes/después del cobro. W/N y (W-F_op)/N por todas las iniciadas, no sólo pagadoras. Origen exógeno queda visible.

Q(H)=raíces pagadas con primer neto positivo recibido y linaje causal compra→intento→pase→activación aplicada→crédito, dentro de H. Q/U no se obtiene multiplicando tasas aisladas. Mantener Q_proven como límite observado cuando quedan gaps; q completa requiere evidencia y denominador completos. Un cargo/refund/reverso/approved-only o cash de otra cuenta/otra ventana no prueba primer payout. Ausencia de observación funded=NOT_OBSERVED; cadena incompleta=UNKNOWN/INCOMPLETE_LINEAGE.

SIMULATION: cash inicial/final/mínimo, disponible/comprometido, desembolsos/recepciones, tiempo sin financiación, adquisiciones/pases/activaciones/pérdidas/pending, atribuciones por Strategy/MM/prop/account y concentración temporal. Suma de atribuciones concilia con total sin repartir la misma caja varias veces. No tratar cuentas correlacionadas o replays como muestras IID. No prometer crecimiento infinito ni throughput sin medirlo.

### 9. Go-only operativo y estructura mínima de código

Mantener `v3/backtester` paquete `backtest` como owner de Campaign/economía y driver. Extender archivos existentes y, si evita monolitos, crear archivos vecinos `campaign_v2_contract.go`, `campaign_economic_events.go`, `campaign_economic_report.go`, `campaign_composition.go`, `campaign_legacy_adapter.go` (nombres propuestos CREATE, no APIs existentes). No otro módulo Go ni librería financiera independiente. SDK sólo para contratos/runtime compartidos con consumidor real.

El CLI `cmd/echo-backtest` sigue delgado. Superficie objetivo propuesta `echo-backtest lab <validate|plan|prepare|run|resume|report|compare|migrate|qualify|export>` con handlers Go sobre owners actuales; la gramática se implementa y documenta, no se afirma disponible ahora. Reutilizar `experiment`, `platform-*`, `reproduce`, `daily-report`, publicación, identidad/attempt y preparación existentes. Un paquete interno pequeño de aplicación/lab sólo si separa comandos de dominio; nunca negocio en main.

Inventario por cada entrypoint Python usado: REUSE_GO, IMPLEMENT_GO o RETIRE_REFERENCE_ONLY con consumidor, reemplazo y prueba. Cubrir planes/derivación de variantes admitidas, validación, materialización, run/resume, caracterización/reconciliación/reportes, comparación/ranking finito autorizado, export/manifest y guard. No recrear proyectores estadísticos antiguos sin consumidor; BINARY_DIAGNOSTIC/SESSION_BLOCKS no se convierten en SIMULATION ni en certificados. Su retiro requiere registro explícito, conservando artifacts históricos, no desaparición silenciosa de una función activa.

Al cerrar: build, tests, CLI, admisión, runner y reporting oficiales de Echo Futures no requieren Python/venv/pip ni invocan scripts Python. El código Python S04 de ese alcance y bytecode se retiran del árbol activo después de disponer consumidores; su historia permanece en Git. No se añade copia ejecutable bajo `legacy/` a master. JSON/catálogos/datos permanecen neutrales. Esta regla no exige reescribir UI/infra ajena ni herramientas propias de Agents-OS: inventariar referencias ajenas y no borrarlas unilateralmente. No declarar Go-only si queda una dependencia ejecutable en el flujo oficial.

### 10. Migración y compatibilidad

Leer catálogos/planes sellados y producir un manifiesto source→target por identidad: Strategy/variante/MM/policy/profile/mode, hashes, schema, campos recuperables, cambio semántico, gates y estado. Censo de referencia S04=26 nativas+63 SG=89 ejecutables, más 15 aliases; revalidar contra fuente, no repetir campañas para obtener el censo.

- SAME_SEMANTICS requiere equivalencia demostrada. Cambios de capital, modo, política, fees, modelo OHLC o reglas generan NEW_EXPERIMENT.
- V1 histórico y V1 master conservan identidades y la discrepancia S04-F01. No renombrar masivamente V1→Unclipped. Fixture Go de frontera requested-risk>headroom positivo, igualdad y piso, con comparación exacta de fuentes. Si reproduce divergencia, documentar mapeo de comportamiento sin cambiar runtime para encajar resultados.
- Legacy BASIC/CAMPAIGN funcional y Platform mantienen rutas de lectura/replay versionadas sobre el motor compartido. No mantener dos implementaciones nuevas de lifecycle. Where the old contract cannot be represented unchanged, keep the old Go compatibility path explicitly versioned until an authorized retirement; never claim equivalence.
- No borrar resultados ni historiales, modificar catálogos sellados o fusionar la rama I0 Python. Extraer fixtures neutrales por intención y rederivar oráculos desde Go/reglas, no copiar assertions defectuosas.

### 11. Admisión, ejecución y reanudación

Portar/adaptar el guard a Go en el owner de admisión del runner, reutilizado por todas las entradas capaces de ejecutar (incluido resume). No dejar un comando legacy como bypass. Derivar propósito de corpus/ventana/contratos y validar chain/identidad/SHA: G0→G1→G2A/B/C→G3→G4→G5 sin redefinirlos. FUNDED-only o MM distinto no hereda G4; D05 requiere resolución Owner/retester para investigación histórica afectada. La implementación y tests funcionales deterministas no están bloqueados por esa decisión comercial. No reclasificar un histórico como fixture.

Reusar supervisor único y presupuesto global vigente del runbook (hasta seis motores incluyendo oráculos, sujeto a presión real); medir memoria/CPU/PSI/swap, detener admisiones si falta capacidad. No nuevo supervisor simultáneo Python+Go. El reemplazo de su implementación conserva el mismo owner y protocolo; el corte operativo no deja dos writers.

Resume inicial KISS: reanudar jobs ya completos por receipt válido; un attempt incompleto se reconstruye desde inputs sellados en una nueva ejecución aislada con el mismo RunID determinista y otro AttemptID, o usa el replay existente. No sumar su dinero al resultado anterior. No prometer checkpoint a mitad de mercado sin estado completo de todos los owners, journal, reservas, timers y cola; ese formato no se improvisa. Fallar un append/sello deja artifact INCOMPLETE, no publicar resultado canónico COMPLETE.

### 12. Aceptación del producto y límites

El plan del planner define tareas y tres shots. Cierre funcional exige CHALLENGE y FUNDED con N cuentas/rotación, comparación independiente y SIMULATION conjunta 1×1 y multi-asociación/multi-perfil, reportes correctos, migración trazable y zero dependencia Python. No basta portar un reporter ni pasar fixtures de factories.

Separar: SOURCE/BUILD/UNIT/INTEGRATION/E2E/FUNCTIONAL_MATRIX/QUALIFICATION/ECONOMIC_RESULTS/MERGE/DEPLOY. Verificación sintética demuestra mecánica; histórico físico y profit no se infieren. Cada configuración migrada queda VALIDATED/EXECUTED/BLOCKED con causa exacta; probar catálogo no significa ejecutar las 89 campañas. No expandir automáticamente combinaciones ni reejecutar histórico bit-idéntico.

D01 unidad y D02 horizonte, términos comerciales/profile versionados, parámetros de retiro/búsqueda y D05 son inputs obligatorios de campañas económicas, no defaults que inventa el implementador. Pueden bloquear una corrida o selección, no justificar entregar sólo tooling. No es necesario elegir un óptimo de retiro para construir y probar la capacidad configurable.

## Fuentes y trazabilidad

Requisitos Owner de este turno y [[FUT-R01-CAMPANAS-CHALLENGE-FUNDED-SIMULATION]]. Código source del corte `2baf319d` en las rutas de §1; evidencia heredada en [[EF-S04-INTEGRATION-RECONCILIATION]]. Los retornos I0 se preservan como historia sin aceptar sus métricas como contratos.

Snapshot íntegro del diseño anterior: `artifacts/backtester/history/EF-CAMPAIGN-MODES-DESIGN-before-C06.txt`, blob original `ffd13341f7786740558a28cc66e2e7f4bf71f61d`, copia byte-idéntica no operativa. La fuente vigente sigue siendo este archivo. No existe segundo manager ni segundo planner.
