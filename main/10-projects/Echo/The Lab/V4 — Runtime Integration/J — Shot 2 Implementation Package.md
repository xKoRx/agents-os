---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[0 — Shot 1 Gate and Baseline]]"
  - "[[I — Go API SQL Executable Spec]]"
  - "[[H — Test Matrix Independent Oracles]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-22"
updated: "2026-10-22"
---

# J — Shot 2 Implementation Package

## Propósito

Paquete completo para que GLM implemente Shot 2 del programa único de cuatro shots, con interfaces cerradas, superficies delimitadas y aceptación trazable. No inicia implementación, QA Shot 3 ni correcciones Shot 4; GOD conserva el gate final Shot 1 en [[0 — Shot 1 Gate and Baseline]]. «Documento completo» no equivale a aprobación GOD ni a ejecución física. La implementación debe entregar todo I1 compatible más D17–D21 sobre runtime; ningún pendiente funcional se convierte en backlog por comodidad.

## Contenido

### 1. Mandato cerrado y autoridades

**Programa exactamente cuatro shots:** (1) diseño detallado actual con investigación/redacción ONE-SHOT; (2) GLM implementa e integra y valida con datos auténticos aislados; (3) GOD coordina QA adversarial independiente mediante especialistas y valida evidencia compacta; (4) GLM corrige TODOS los findings y completa revisión independiente de cambios finales dentro del mismo shot. No Shot5, subshots recurrentes, nuevo freeze perpetuo ni extensión del programa por handoff. J entrega instrucciones para Shot2, no pone en marcha3/4.

Lectura ejecutable mínima GLM: [[0 — Shot 1 Gate and Baseline]] y [[I — Go API SQL Executable Spec]], luego secciones contractuales A–G afectadas y matriz completa [[H — Test Matrix Independent Oracles]]. [[F — Decision Register]] D09/D10/D11/D16–D24 es autoridad producto. A runtime/correlación; B ingesta/provisión; C historias/economía/selección; D curvas/métricas/worker/precisión; E ranking/módulo; F SQL/migraciones/grants; G Hasura/UX. I mapea interfaces/archivos y nunca sustituye las autoridades. Ante contradicción de implementación, presentar evidencia y corrección mínima dentro del shot; no pedir al owner ratificar decisiones técnicas ya resueltas ni omitir un panel/algoritmo.

**Baseline único Echo:** `xKoRx/echo`, `feature/ef-runtime-pools@2ee61791deb3139be23e1c9be3708b1d41da8d6b`; Symphony `master@daded14cbe0bc85f6fafda8d079e94036f715b47`. Son cortes fuente leídos localmente y no certificados runtime. Antes de escribir GLM verifica branch/HEAD/status/AGENTS y ownership de workspace; preserva delta ajeno. Si HEAD legítimo cambió, registra delta relevante contra este contrato y vuelve a comprobar interfaces, sin traer ramas legacy. No merge/rebase/cherry-pick/adapters de `feature/lab-v4-shot4` ni backtester. La extracción de estrategias en curso queda intacta; su futura migración al runtime es trabajo separado D24.

### 2. Responsables y superficies

| Responsable | Entrega y boundary |
|---|---|
| GLM implementador/integrador Shot2 | Dueño del cambio source y de completar verticales; arma harness propio/fixtures/oráculos/regresiones, integra Echo/Symphony/Hasura/front, registra source/delta y evidencia. No absorbe rol de auditor independiente ni declara PASS físico por unit tests |
| Especialista runtime/ingesta | Si GLM delega ejecución autorizada, A/B/C sobre superficies I; valida correlación/QI/owners/recovery/readiness. Mantiene un solo writer/engine, sin activar cuentas reales |
| Especialista SQL/analytics | F/D/E; esquema/runner/fences/cálculo/cohort y shared module. Revisa constraints e índices en PG desechable, sin tocar BD compartida |
| Especialista Hasura/frontend | G; auth scoped/query action/read bundles/screener/detalle completo con consultas reales, sin secretos front ni fórmulas JS |
| Especialista verificador dentro de Shot2 | Puede revisar ejecución local del implementador y regresiones, dejando autoría/evidencia explícitas. No reemplaza QA independiente Shot3 ni extiende el programa |
| GOD Shot1/Shot3 | Decide interfaces/gate de diseño actual y luego coordina QA; recibe hallazgos compactos. No es ejecutor de suites/source masivo ni fallback premium |
| GLM+revisor independiente Shot4 | Corrige findings de Shot3 y regresiones, valida cambios finales dentro de Shot4 con evidencia. No se inicia por este documento |

Allowed Files de código son exactamente los paquetes/archivos y tests asociados de I§5 más runner `v3/toolkit/cmd/apply-migration/main.go` y tests del protocolo F. Los nuevos filenames concretos de F prevalecen sobre aliases de I; no renombrar aplicado001–066. No tocar sync.sh/.sync ni código/producto en Shot1. En Shot2 las superficies de configuración module YAML/ETCD/metadata son preparación source y aplicación sólo en harness propio; no permisos sobre runtime/credenciales/servicios compartidos. Cambios en componentes puros actuales son acotados al recorrido G; inventario antes del corte, sin borrar consumidores por ausencia en logs.

### 3. Harness y permiso físico

Seguir [[Echo + Echo Forge — Environment Contract]]: Echo DEV/PROD separados; Forge tiene un único ambiente operacional, nunca construir un «Forge DEV» nuevo. Shot2 puede trabajar código/harness local aislado con todos sus procesos, DBs, accounts, provider simulados, topics, artifacts y namespace identificados en manifest. H fija guard failclosed ANTES de red/mutación: sólo loopback y recursos manifest-owned autorizados, credenciales dedicadas, cuentas ficticias del harness sin dinero, no puertos/pollers/colas compartidos, no kill/delete amplios. ETCD local propio por SDK conserva configuración real sin env bypass hacia producción. Aislamiento se prueba y cleanup detiene procesos físicos propios, no sólo marca jobs terminales.

Reutilizar artefacto auténtico Forge disponible por lectura autorizada con source refs/digest y traducción V2; no disparar campañas/retesters de flota ni tocar Zeus/Hera/Kronos/worker Windows para obtenerlo. Si falta artefacto/acceso/ownership, gate auténtico físico queda `BLOCKED_EXTERNAL_ARTIFACT|BLOCKED_EXTERNAL_PERMISSION` con causa/owner/recurso concreto. El código, parser, productor, contratos, UI, tests numéricos/protocolo, migraciones y harness deben completarse igual. Fixtures sintéticos verifican semántica pero jamás prueban Forge E2E auténtico. Sólo gates físicos pueden quedar bloqueados externamente; no diferir algoritmos/panels/seguridad/readiness funcional por ausencia de un deploy compartido.

Presupuesto de máquina H:4vCPU/16GiB, versiones/procesos/dataset declarados y CPU/RAM/PG/Hasura medidos. No usar tests seed que puedan alterar ETCD real. Sin deploy/restart/cutover/metadata apply de compartidos, PROD, cuentas/órdenes reales, campañas, flota activa, merges destructivos ni adopción de ownership ajeno. Publicación del módulo prerelease E es una operación fuente/versionada distinta del rollout; ningún tag productivo limpio desde feature y nunca mover tag existente.

### 4. Orden vertical de implementación — sin saltar gates dependientes

| Paso | Archivos/owner contractual | Trabajo concreto y salida reviewable | Gate local que permite seguir |
|---|---|---|---|
| S2-01 baseline y seguridad harness | I§5, H01–H02/H47–H48 | Registrar refs/status/ownership; construir manifest/guard/teardown; infra local propia y auth dedicada. Preparar SPEC/PLAN/TASKS/VERIFICATION del feature según repo, sin sustituir contrato vault | Hash/ownership correctos, guard rechaza endpoint/puerto/token ajeno antes de escribir, cleanup idempotente |
| S2-02 protocolo SQL y contratos | F067–068, SDK contracts/wire B/C, toolkit runner | Runner tx+checksum bytes/ledger/manifest/signature; registry recipes, Magic nullable/primera asignación certificada única/scanners compatibles y tipos exactos; decoder estricto/hash universal; fixtures wire interoperables | Fallo DDL rollback completo, checksum conflict antes DDL, reapply idempotente, recipe refs históricos intactos y source timestamp nano preservado |
| S2-03 registro/historias mínimo V2 | F069/071, B/C application services/Gateway | POST V2 montado y PUT CAS con artifact write-ahead+receipt+immutable snapshot+dirty; GET scoped/by-key; historia real Forge traducida con Q/costos/currency desconocidos honestos | POST/replay/timeout/by-key, CAS412 vs409, races20calls y headers/body, snapshots N recuperables; no ReplaceHistory V1 |
| S2-04 provisioning + ruta master auténtica del contrato | A/B/F069/070, Core/Bridge/Gateway/Projector | Binding/run/config pin, definición/mappings/policies autorizadas, outbox/ACK efectivo/incarnation/readiness; ReferenceEvent→writer journal→outbox history; master t_first_byte+60s del harness con worker LAB parado | Acceptance separada READY; missing/stale ACK bloquea NEW OPEN y conserva observación; READY no ejecuta aperturas viejas; journal/version/run sin dependencia analytics |
| S2-05 ciclo runtime + economía | A/C/F070–071, SDK runtime/accounting/projector | Sidecar y facts v2/QI_SEALED en decisión real antes fill; reducer atribuible por Operation, costes/movimientos, correlaciones exactas y proyección histórica. Native runner real admitido, sin migrar EA Forge | Un solo engine; caso A/B5vs15; fill/effect replay/conflicto; suma por movimiento y CLOSED_SUMMARY exclusiva; recovery checkpoint real, jamás SQL engine reconstruction |
| S2-06 cuatro perfiles/worker/selección | C/D/F071–072 | Registry4 perfiles, timeline/metric factory, fixed24+bound, queue/fence/CAS bundle completo, selection principal/alternativas temporal; encolado automático tras revisión/perfil | Oráculos D01–D23, missing Q/costs/currency, causal order, exhaustion, pre/post/as-known y N/N+1; todos estados terminales publicables sin loading infinito |
| S2-07 módulo único + ambos rankings | E/F073 y `v3/shared-analytics`, Symphony wrapper | Implementar kernel puro+goldens, comparar al ranker Forge SHA-pinned antes de quitar fórmula duplicada; adaptar métricas HE24→float bits, cohort atómica e invalidación completa | H27–H33: Edge/Calidad exactos, ties/min=max, missing30x30, outlier afecta todos, cohorte race rollback. Module frío mismo prerelease/checksum en consumidores |
| S2-08 API lectura/Hasura/auth | F074/G/I, gateway BundleService/cursor/action | Read bundles pinneados RR corto+ordinal sort sellado, vistas select-only namespace/principal con roles nuevos lab_readonly/lab_config_operator y source echo_lab_v4/login leastpriv sobre misma DB, hook mapeado sin acceso legacy, GraphQL action query autenticada firma/verifica Go, REST mismo servicio | Missing session failclosed; crossns/body/cursor spoof no filtra; N cursor conserva N tras publicación; SQL query plan indexado sin SELECT head mutable |
| S2-09 UX completa y D11/copia | G/I§5, frontend+commands Echo | `/lab` screener→detalle real, selectores independientes, filtros/sorts globales/paginación, calendario/DD/distrib/prepost/historias/movimientos, comparación explícita de copias y composición estática flat/C0 separado. Quitar admin/control secret del bundle | G01–G09/H24–25/H36–43 en navegador con requests/refs, error/carga/back/deep-link y N+1 reproducibles; sin fixtures visibles como realidad |
| S2-10 escala/integración/cierre de Shot2 | H44–H49, I§6 | Dataset largo132805, catálogo20k, cola/correcciones/recovery y E2E auténtico aislado cuando disponible; clean source/manifest/capacidad/coverage; inventario/cutover/rollback preparado sin apply compartido | Matriz completa con PASS/FAIL/NOT_RUN/BLOCKED veraces y paquete de evidencia para Shot3; no iniciar Shot3 |

Aplicar migraciones067→074 en orden F para cada DB desechable; S2-03/S2-04 pueden desarrollar servicio antes de consumir tablas posteriores, pero nunca ejecutar071 antes070. No crear transacciones ad hoc ni tests de integración sólo con tablas recortadas que evadan FKs. Se puede integrar verticalmente con scaffolding, pero la entrega final no conserva TODO/stubs/fixture fallback en rutas de negocio. Falla de un gate crítico se corrige dentro de Shot2; no se oculta como limitación física si es código/configuración propia.

### 5. Matriz de aceptación de entrega

IDs H son autoridad de prueba independiente, no tests que esta nota declare ejecutados. Cifras en fixtures H/D/E son oráculos sintéticos deliberados; UI real usa fuente auténtica separada. Los estados de esta tabla en Shot1 son todos NOT_RUN.

| Acceptance de paquete | Trace contractual y pruebas H | Evidencia exigida / condición de éxito |
|---|---|---|
| P01 identidad/auth/ingesta universal | A/B/C/F; H01–H14/H35/H43 | Source refs, wire golden/digests, receipt/query recovery, namespaces/writer grants/recipes/version/run exactos, CAS412 y replay idempotente sin nueva historia/orden |
| P02 Forge operacional→master→journal→LAB | A/B; H03–H14/H49 | Manifest Forge auténtico+receipt+binding/config revision/digest+ACK/checkpoint/lease, master simulado a t_first_byte+60s, row journal y HistoryRev correlacionadas. Worker detenido no bloquea journal; sin Operation ficticia de master externo |
| P03 economía/revisiones/selección | C/D/F; H15–H26/H34–H36 | Parciales/costes/summary/Q causal, monedas probadas/unknown, immutable snapshot, source→representation crosswalk, selector temporal/correcciones/knowledge, numeric bounds24 y retención íntegra |
| P04 cuatro perfiles y métricas | D01–D23; H16–H26/H34/H44 | Cuatro specs registradas y calculadas automáticamente, C0/r configurables, Q vs B distintos, causal sizing/timestamp, ventanas/DD/carry-in/samples/agotamiento, fixed24 exacto con cota; ningún display como input |
| P05 dos rankings/módulo/paridad | E G01–G10; H27–H33/H45 | Edge1:1 y Calidad5:4:4:3, extrema/cohort completa, métricas/calendario/sample definidos, null/ties/outlier correctos. Kernel único stdlib, wrapper preservado, imports y mismo tag/commit/h1/zip de cachefría |
| P06 Hasura/scoped lectura coherente | F/G05/G03; H35–H36/H41–H43 | Introspection/SELECT de lab_readonly+lab_config_operator reales del harness, denegación DML/ns spoof/action directo, firma cursor Go y bundle owner, sin admin secret/credentials en assets/log/URL |
| P07 screener/detalle funcional | G01–G09; H36–H42 | Browser recorrido limpio/deep-link/back, selectors independientes, sorting/filter antes página, fuente real/version/TF declarado, calendario/DD/distrib/prepost/historias/costs/movements y estados honestos; N/N+1 no mezcla |
| P08 copia+composición estática | C§8/D/G07–08; H24–H25 | Links referencia/copia y denominadores/cobertura; sin matching heurístico. D11 pesos/cash/capital separado/flat start/exclusión pre-start; faltante positivo no cash/rebalance ni I2 |
| P09 capacidad/recuperación/no interferencia | D23/F/G§8; H44–H49 |132805 ops íntegramente retenidas,4perfiles≤300s/workerRSS≤2GiB; ingest≤120s; ambos rankings20k≤30s/cohorte; paginación20k100requests p95≤2s y subgates G estrictos; backpressure/correction/lease/recovery/cleanup medidos en4vCPU16GiB |
| P10 calidad/corte/handoff | H§10; I§6 | Coverage≥95% nuevo con auth/races/economía crítica primero; assertions/oráculos independientes, suite/race/static/build/frontend/migrations dirigidas al delta y requeridas repo. Retirement ledger y rollback por binding, sin borrar fuentes/certificados históricos |

G exige además10 lectores concurrentes/corrección1%, page50 warm p95≤500ms/cold≤2s, prepare≤2s y≤1MiB; detalle≤2000puntos p95≤1s/≤2MiB y memoria de browser acotada. No se reduce dataset/carga tras fallo. Hardware/distribución/versions/concurrencia/EXPLAIN/CPU/RSS/backlog se guardan junto a los resultados. Estas metas son TARGET, no garantía física actual ni certificación20k engines.

### 6. Artefactos que GLM debe entregar al terminar Shot2

Entregar feature SPEC/PLAN/TASKS/VERIFICATION en las superficies repo requeridas, manifest source por repo (base/head/branch/status y archivos reales cambiados), manifest de build/pin del módulo, manifest migraciones bytes/checksums/ledger/catalog signatures y candidato metadata completo. Evidencia voluminosa/binarios/capturas/queries se guarda fuera del vault; vault conserva refs seguras repo+path+SHA y resumen, nunca tokens/dumps/paths absolutos locales. Un change_log consolidado/control del vault es responsabilidad del coordinador, no de cada especialista.

El reporte compacto debe tener una fila por H01–H49 con estado y evidence_ref, resumen numérico de discrepancias/oráculos, tablas fuentes→receipt→version/binding/run/config→journal→history revision→curve generation→ranking cohort→read bundle, coverage por paquete delta, límites/capacidad y verificación de cleanup. `PASS` requiere outcome de la capa dueña; build verde/mock/fixture no prueba integración real, y ECHO_OPERATIONAL_READY requiere applied/recovery/leases reales del scope. Prueba no ejecutada=NOT_RUN; permiso/artefacto externo faltante=BLOCKED_EXTERNAL tipado; defecto producto=FAIL con severity/owner/reproducción, nunca downgrade administrativo.

Checklist residual permitido sólo físico: artefacto Forge auténtico inaccesible, acceso/ownership de deploy/migración/metadata en compartidos, autorización de cuentas/broker/dinero, distribución prerelease inaccesible por permiso externo concreto. Preparar source/rollback/test harness completo y reportar bloqueo exacto; no sustituir versión inaccesible por copia/replace ni marcar paridad distribución PASS. Ni scheduler/TopN/rotación/rebalanceo/I2 ni migración del backtester forman pendientes de este paquete porque D22/D24 los excluyen explícitamente. Curvas, dos rankings, readiness funcional, copias, selección/D11, Hasura/screener/detalle sí se terminan en Shot2.

### 7. Transición sin ejecución adelantada

Al finalizar Shot2 GLM entrega paquete y se detiene en `IMPLEMENTED_LOCAL_AWAITING_SHOT3`, con `PHYSICAL_GATES` separado cuando corresponda. El estado no proclama aceptación final ni activa auditoría por sí solo. El siguiente mandato Shot3 usa especialistas independientes, H y evidencia compacta para abrir findings; Shot4 corrige todos y somete sus cambios a revisión independiente dentro del mismo shot. Nunca se necesita rescatar una rama legacy, inventar un quinto shot o abrir otra entrevista de producto para continuar lo ya ratificado.

## Fuentes

- [[F — Decision Register]], [[0 — Shot 1 Gate and Baseline]] y [[Echo — Producto Integrado]].
- [[A — Runtime CURRENT TARGET]], [[B — Forge Ingestion Readiness]], [[C — Histories Revisions Economy]], [[D — Curves Metrics Workers]], [[E — Rankings Shared Go Parity]], [[F — SQL Migrations Ownership]], [[G — Hasura UX Functional Spec]], [[H — Test Matrix Independent Oracles]], [[I — Go API SQL Executable Spec]].
- [[Echo + Echo Forge — Environment Contract]] para ambiente/permisos y [[SHOT4_HANDOFF]] sólo como requisitos compatibles históricos, sin heredar código ni PASS.
