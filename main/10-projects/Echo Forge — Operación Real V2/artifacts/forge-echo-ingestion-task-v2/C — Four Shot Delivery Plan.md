---
type: doc
schema_version: 1
status: active
area: '[[Echo]]'
related:
- '[[10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2|Echo Forge — Operación Real V2]]'
- '[[Echo — Producto Integrado]]'
aliases: []
tags:
- kind/doc
created: '2026-10-27'
updated: '2026-10-28'
---

# C — Four Shot Delivery Plan

## Propósito

Gestionar la implementación, la revisión adversarial y la certificación dentro de exactamente cuatro shots, con evidencias separadas por gate.

## Contenido

### Estado vigente y siguiente ejecución — 2026-10-28

**SHOT4_READY_WITH_ADJUDICATED_FINDINGS.** Se recibe Shot 3 con hallazgos y alcance parcial y se avanza a correcciones completas + verificador final LOCAL fresco dentro de Shot 4. No otra vuelta de Shot 2/3 ni Shot 5. Adjudicación canónica de los nueve findings y precisiones de evidencia: [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/E — Independent Adversarial Report|E — Independent Adversarial Report]]. El resumen inicial de tres P1 no agota el trabajo: 02/07 son P1 de integridad; 04 es P2 de contrato; 01/03/09 y todos los casos pendientes siguen obligatorios.

Candidatos de entrada remotos intactos: Symphony `7731cb844446062f861f04d19dea60a34d425373`, Echo `24af786232fa362cc1599df1b9d90b1c8347b557`, contracts .2 inmutable. A INCOMPLETE, B/C E2E NOT_RUN, D BLOCKED_EXTERNAL con lectura auténtica parcial reportada; E release NOT_AUTHORIZED. Las cifras 47,1%/80,4% de E son reportadas y requieren perfiles, scope y unión reproducibles. El piso ≥95% del código nuevo sigue vigente, incluyendo adiciones en archivos existentes.

**NEXT EXACT:** ejecutar [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT4 — Correction and Final Verification Mandate|SHOT4 — Correction and Final Verification Mandate]]. Primero el corrector entrega candidato integrado con los nueve cierres, Fresh/Upgrade, Generic/Group reales, Gateway/Lab, goldens y coverage. Después otro verificador sin autoría reconstruye ese SHA y verifica de forma independiente. F — Final Certification conserva por separado ambos aportes; sólo evidencia suficiente permite adjudicar FORGE_ECHO_INGESTION_TASK_VERIFIED con límites explícitos. Si persiste un bloqueo, se reporta dentro de Shot 4 sin PASS forzado ni nuevo shot automático. B/addendum permanecen congelados; Agents-OS abierto.

### Recepción histórica del auditor — 2026-10-28 (anterior a adjudicación)

**Shot 3 ejecutado y entregado** ([[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/E — Independent Adversarial Report|E — Independent Adversarial Report]]; veredicto de alcance en D 2026-10-28, pendiente de adjudicación del Primary Manager). Candidato congelado auditado sin cambios de SHAs; 3 findings P1 reproducidos (runner sin 017/018; decision_ref sintético/CHECK; data_only workflow colgado en `begin_workflow_span`), 4 P2/P3 y cobertura real por statements 47,1% delta / 80,4% nuevos. Gates: A PARCIAL, B/C NOT_RUN (smoke PG real PASS), D BLOCKED con lectura auténtica parcial (ETCD/PG PROD), E NOT_AUTHORIZED. **NEXT EXACT: Shot 4 — el implementador corrige los findings de E y después un verificador final fresco reconstruye el SHA y repite los oráculos críticos dentro del mismo Shot 4.** Gate objetivo: `FORGE_ECHO_INGESTION_TASK_VERIFIED`. No hay Shot 5 ni otra vuelta de Shot 2/3.

### Decisión histórica del Owner y admisión a Shot 3 — 2026-10-27

**SHOT3_READY_WITH_KNOWN_GAPS.** El Owner ordenó expresamente avanzar al QA adversarial independiente y **no realizar más iteraciones de Shot 2**. Se congela la segunda entrega como candidato para auditoría. Esta decisión supersede las instrucciones administrativas anteriores de continuar Shot 2 antes de QA; los antecedentes técnicos se conservan para confirmación/falsificación sobre el SHA actual. No concede FORGE_ECHO_TASK_IMPLEMENTED_LOCAL ni PASS de calidad por relato, y no cambia el piso ≥95% ni la SPEC.

Refs remotas verificadas por el Manager: Symphony `7731cb844446062f861f04d19dea60a34d425373` (+3 commits desde `07c914251760a938293b7fa7fe4e6d7b4d330640`, sin divergencia); Echo `24af786232fa362cc1599df1b9d90b1c8347b557` (+1 desde `2c66e9402ba96ff354681552587c895ec92f4a28`, sin divergencia). Son **descendientes**, corrigiendo el uso invertido de «ancestro» en la segunda entrega. Contracts `.2`: objeto `7496b05b6932517e1d51b757c42cf72dad2cc1bd` → Echo `24af7862…`, subtree `cb88aece4f04b648fd724568de3823604dc064ab`; go.mod/go.sum Symphony alineados. El tag `.1` mantiene su objeto original `d24b17b217245c47a33cea810410da41cf6ad978`. Fuente efectiva, cold builds y runtime se verificarán localmente.

El implementador afirma M01–M08 corregidos. El Manager **no ejecutó otra auditoría exhaustiva ni pruebas runtime** en esta admisión; se comprobó identidad/ancestry/pins y se preparó la falsificación independiente. No heredar ni sus PASS ni los P1 adjudicados al candidato anterior. La migración018 figura modificada en el diff: Shot 3 probará Fresh y Upgrade desde la 018 anterior ya aplicada, sin reescribir ledger/checksums.

Brechas conocidas al entrar: cobertura reportada **68,0% como promedio de 85 funciones**, pendiente de recalcular por statements con scope/denominador verificable; B/C E2E con worker/Temporal/Lab reales pendientes; goldens cruzados pendientes; D con canales MCP expirados reportados y sin fuente auténtica leída. Las 515 filas del harness no acreditan fuente Forge auténtica. E sigue NOT_AUTHORIZED. El incidente PG queda reportado y fuera del harness de QA; no se autoriza restaurar/borrar el template compartido.

**NEXT EXACT:** ejecutar [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT3 — Independent Adversarial QA Mandate|SHOT3 — Independent Adversarial QA Mandate]] en GLM-5.3-Flash Max LOCAL/ZCode fresco y sin autoría, con estos candidatos fijos. Puede crear pruebas/harness y levantar Temporal aislado; no corregir producto durante QA. Los findings reproducidos y déficits de evidencia alimentan **Shot 4: corrección + otro verificador fresco dentro de Shot 4**. Sólo un riesgo grave concreto de ejecución insegura suspende el escenario afectado; los demás casos seguros continúan. No nueva vuelta Shot 2 ni Shot 5. Agents-OS permanece abierto, sin feedback/L0/L1.

### Estado histórico tras la entrega inicial de Shot 2 — 2026-10-27

**SHOT2_INCOMPLETE.** El manager recibió y verificó las refs Symphony `07c914251760a938293b7fa7fe4e6d7b4d330640` y Echo `2c66e9402ba96ff354681552587c895ec92f4a28`, ambas descendientes directas de las bases elegidas. El tag contracts `.1` apunta al candidato Echo y permanece inmutable. La revisión acotada de código identificó bloqueos de composición/snapshot, fidelidad de historia, entrega/receipt, resultado durable y consumidor/Lab; se detallan en [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/D — Implementation Evidence|D — Implementation Evidence]] (M01–M09).

Siguiente acción: el mismo implementador termina el alcance y sus pruebas dentro de Shot 2 mediante [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/SHOT2 — Local Implementation Mandate|SHOT2 — Local Implementation Mandate]]. No se adjudica FORGE_ECHO_TASK_IMPLEMENTED_LOCAL ni se inicia Shot 3. Se conservan los cuatro shots y el diseño congelado. A INCOMPLETE; B/C/D NOT_RUN según entrega; coverage ≥95% y goldens pendientes; E NOT_AUTHORIZED. El incidente del template PG compartido permanece reportado, con impacto/restauración no verificados desde CLOUD y sin permiso de reconstrucción compartida implícito.

La revisión del manager es fuente/contrato, no QA runtime. Las ejecuciones declaradas por GLM y las atribuciones a baseline se conservan como tales hasta disponer de comandos/logs/evidencia. El diseño y el estado inicial descritos abajo son la historia del arranque; esta sección rige la continuidad actual.

### Identidad del programa y rectificación del despacho

**Program ID: `forge-echo-ingestion-task-v2`.** Programa nuevo de la task nativa configurable `echo_ingestion_v2`, gestionado en Echo Forge. Sus cuatro shots son propios de esta funcionalidad.

| Programa | Entrega y estado | Relación |
|---|---|---|
| Echo / Ingestion V2 — Operational Integration | Endpoint, contratos, registry/historias, adapter/persistencia/CLI productor; cuatro shots anteriores ejecutados, VERIFIED_WITH_FINDINGS histórico | Dependencia y baseline. Sus reportes siguen vigentes para su alcance. |
| Forge / forge-echo-ingestion-task-v2 | Resolver fuentes durables → construir DTO → task declarativa Temporal → entrega/recovery → Echo/Lab | Programa nuevo. Shot 3 recibido con hallazgos y alcance parcial; Shot 4 vigente para correcciones y verificación final fresca, sin nuevos shots. |

Symphony 22f337ca y Echo f93cd4f8 son resultados consolidados del programa anterior y bases intencionales del nuevo. Crear una feature desde esos commits conserva trabajo verificado; no exige volver a b2b3ebfe/a0c68d1, borrar código ni reejecutar la implementación anterior.

El primer despacho local no pudo cargar el ZIP ni estas autoridades, que aún no estaban publicadas. Esa ausencia fue real; la clasificación posterior como campaña duplicada/stale fue una inferencia incorrecta entre programas distintos. El Owner autorizó después la publicación íntegra. El despacho vigente lee estas rutas desde un commit remoto verificado y no depende de un ZIP.

Si la sesión GLM anterior escribió una memoria que marca este encargo como stale/duplicado, rectificar específicamente esa conclusión conservando la traza y enlazando este mandato. No borrar ni invalidar los reportes históricos de Ingestion V2. La ubicación local exacta de esa marca no fue verificada desde CLOUD; no se afirma haberla modificado remotamente.

**Prueba de alcance en Symphony 22f337ca:** `HTTPIngressV2.Ingest` recibe un DTO ya construido; `sqx/cmd/echo-ingest-v2/main.go` lee ECHO_INGEST_V2_INPUT y decodifica ese JSON. En cambio, los switches de `runGenericSQXWorkflow` y `GroupSQXWorkflow` en `sqx/workflows/generic_workflow.go` no tienen case echo_ingestion_v2, y `sqx/cmd/sqx-worker/main.go` no registra su activity. TaskSpec.Type es string: que pueda deserializar un nombre no significa que el runner lo soporte. Las fuentes exactas están en A y B.

### Estado y autoridad

Programa nuevo dentro de [[10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2|Echo Forge — Operación Real V2]], con consumidor [[Echo — Producto Integrado]]. El mandato Owner del 27-10-2026 autoriza al Primary Manager a adjudicar el diseño técnico y organizar exactamente cuatro shots. No cambia las autorizaciones de infraestructura, flota, recursos compartidos ni trading. La fuente de decisiones TARGET es [[10-projects/Echo Forge — Operación Real V2/artifacts/forge-echo-ingestion-task-v2/B — Frozen Design|B — Frozen Design]]; el contrato del consumidor conserva su autoridad en [[10-projects/Echo/Ingestion V2 — Operational Integration/Forge Task — Contract Addendum|Forge Task — Contract Addendum]].

**Estado inicial del programa — histórico al freeze:** investigación de fuente terminada; diseño independiente recibido, revisado y adjudicado por el Primary Manager: FORGE_ECHO_TASK_DESIGN_FROZEN. La capacidad nueva no está implementada. Los PASS históricos de Ingestion V2 son dependencias con excepciones, no pruebas de esta task.

### Baseline reproducible

| Superficie | Baseline fuente |
|---|---|
| Symphony, base productora | `lab-v4/shot4-symphony@22f337ca434549c492b2d402fd158e23ac4758a8` |
| Symphony, master observado | `dd4af7d05c03db9b39b5467b46e2c2c7d0c1fa19`; ancestro de la base, que contiene tres commits adicionales |
| Echo, base consumidora | `lab-v4/shot4-integration@f93cd4f80085e328f9176c1215e42e6c8e0b2404` |
| Contracts consumido antes del cambio | `v3/sdk/contracts/v0.0.1-lab-v4-shot2.1` → `52f8d509e0e9127a9f263f02d76565dae508a2f6`; **no igual** al contrato del Echo candidato |
| Documentación | `xKoRx/agents-os/master`, cambios directos y con protección frente a concurrencia |

Refrescar refs al empezar cada shot y revisar sólo deltas materiales. El registro del nuevo contrato debe incluir tag inmutable, commit, subtree, checksum y consumidores efectivos. No reutilizar un checkout desconocido como prueba de distribución. El refresh final identificó la convergencia paralela publicada Echo `feature/echo-runtime-lab-v4-integration@2daa58daddfbebaf57e2d1c934a25ec644bf0a94` y Symphony `feature/echo-runtime-lab-v4-integration@3dfaa5facb96fcc297c062c46ca77085f882cc1c`, con verificación local reportada y ejecución física pendiente. La comparación acotada conserva los findings de contracts, adapter y Lab; sólo el write-ahead de artifacts canónicos del servicio de historias es un precedente reutilizable mediante port mínimo. Sus migraciones Echo 087–091 son referencias de colisión, no una orden de merge. La nueva rama Symphony nace del linaje V2 consolidado; una extensión Echo nace del linaje del candidato consumidor. No mezclar el workstream Dynamic Groups ni la convergencia de Echo Runtime. Si esas ramas avanzaron, preservar sus commits y demostrar compatibilidad antes de integrar; no realizar una reconciliación general por anticipación.

### Los cuatro shots

| Shot | Ejecutor y outcome | Gate del manager | Artefacto |
|---|---|---|---|
| 1 — Arquitectura y source forensics | GOD Architect independiente, apoyado por investigaciones acotadas de fuente y contratos; sin código de producto | `FORGE_ECHO_TASK_DESIGN_FROZEN` sólo tras revisar decisiones, límites, mapping, ejemplo de configuración y oráculos | A Source Authority, B Frozen Design, este plan, addendum Echo |
| 2 — Implementación completa | GLM-5.3-Flash Max LOCAL/ZCode; implementación autónoma, builds, pruebas propias y harness integrado | Candidato congelado para QA por decisión Owner; brechas conocidas registradas, sin PASS independiente ni otra iteración Shot 2 | D Implementation Evidence: SHAs, manifiesto de fuentes/binarios, fixtures, pruebas, config y resultados |
| 3 — QA adversarial | GLM-5.3-Flash Max LOCAL fresco y sin autoría de implementación; expected propio, falsificación y readback | `FORGE_ECHO_TASK_ADVERSARIAL_REVIEW_COMPLETE`; significa revisión completa, puede incluir findings | E Independent Adversarial Report: severidad, evidencia, reproducción, expected/actual, owner y criterio de corrección |
| 4 — Corrección y certificación | GLM-5.3-Flash Max LOCAL corrige hallazgos adjudicados; después otro verificador independiente reconstruye y verifica el SHA final | `FORGE_ECHO_INGESTION_TASK_VERIFIED` únicamente con evidencia suficiente y límites explícitos | F Final Certification: correcciones, SHA final, oráculos independientes, gates y handoff |

La verificación final independiente pertenece al Shot 4. Los errores normales se resuelven dentro del shot activo. No se crean Shot 5, microshots ni nuevas revisiones premium por inercia. El implementador entrega candidato; el manager adjudica contra evidencia y QA independiente.

### Orden interno de Shot 2 y ownership

| Frente | Ownership | Dependencia y criterio de salida |
|---|---|---|
| Contrato compartido y consumidor | Echo contracts y sus consumidores existentes | Addendum implementado una vez, paquete distribuido y pin real; DTO/decoder/validator/digest/receipt únicos; regresiones legacy y goldens |
| Fuente y transformación | Symphony domain/capabilities/adapters de evidencia | Resolución exacta, definición válida, metadata/MetricSet/TradeSet y artefactos acreditados; ausencia versus corrupción diferenciadas; ningún cálculo analítico nuevo |
| Orquestación y recovery | Symphony runtime/workflows/activities/DI y HTTPIngressV2/ControlPlane existentes | Task declarativa conectada, composición sin SQCLI cuando sólo lee evidencia, snapshot/manifest previos a red, receipts y refs atómicos, retries/restart/concurrencia |
| Harness y fidelidad del consumidor | Orquestador local con oráculos integrados | Temporal + PG/Mongo/MinIO + Gateway + Lab en recursos propios; aislamiento demostrado; A/B/C ejecutables; D sólo con fuente auténtica autorizada |

El contrato público se estabiliza antes de unir los frentes dependientes. El TOP puede paralelizar por ownership de paquetes, pero entrega **un SHA integrado por repositorio y un manifiesto único del candidato**. Ningún handler desconectado, script manual o CLI que recibe JSON terminado sustituye la task.

Las extensiones de productores se limitan a hacer disponible evidencia real del Retester u otro productor compatible; la task de ingesta sigue consumiendo evidencia existente. No abre SQX para leer Mongo o publicar HTTP, ni instala plugins de flota. Los defects de Lab se corrigen en los adaptadores que pierden evidencia; no se crea otro motor ni se reabre la plataforma completa.

### Gates A–E: resultados separados

| Gate | Evidencia suficiente | Qué no lo prueba |
|---|---|---|
| A — Functional Contract | Task declarativa, source resolver, mapper, persistencia, retry/recovery, aislamiento por estrategia y regresiones | Sólo compilar o ejecutar tests del HTTP adapter |
| B — Echo Ingestion E2E | Request auténtico o fixture tipado identificado, Gateway real, validación de receipt y readback de registry/versión/historias | HTTP 202, receipt sin comparar, mock de Echo |
| C — The Lab E2E | Outbox/worker, revisión efectiva, curvas y métricas posibles, rankings/screener y estados de insuficiencia coherentes | Declarar cuatro curvas completas con moneda/costes/Q_i/cobertura desconocidos |
| D — Authentic Forge Source | Ejecución/export autorizado con refs de PG/Mongo, artefactos/hashes/lineage, fuente exacta y origen acreditado | Fixture sintético, archivo con nombre convincente, resultado agregado |
| E — Release/Deploy | Proceso posterior autorizado, identidad source→build→runtime y smoke real | A/B/C/D, una rama publicada o un test local |

Al terminar Shot 1, A/B/C/D quedan **NOT_RUN en este programa**; E queda **NOT_AUTHORIZED/NOT_RUN**. No se declara que falte toda fuente auténtica: esta superficie sólo verificó repositorios. El TOP local debe intentar acceso read-only mediante canales autorizados; si no obtiene el recurso concreto, documenta el bloqueo de D con evidencia y continúa A/B/C. Un gap implementable de producto nunca se reclasifica como `BLOCKED_EXTERNAL`.

### QA mínimo obligatorio

Los oráculos de B y del addendum son vinculantes. La revisión independiente debe cubrir los casos de origen Full Precision acreditado; mismo routing renombrado; otro productor válido; linaje Retester/Exporter; etiquetas iguales con identidades distintas; varias Evaluations/MetricSets/TradeSets; ausencia de TradeSet; corrupción o discrepancias PG/Mongo/MinIO; costes/moneda/FX/Q_i/tiempos/cobertura desconocidos; replay y duplicados; crash antes/después de manifest y POST; timeout con commit; key con body distinto; caída Mongo después de snapshot; restart; concurrencia; divergencia de SDK/digest; receipt inválido/ausente; corrección de historia; integración Temporal; no-regresión; readback de Echo/Lab y no-interferencia.

Priorizar caminos críticos y negativos. El código nuevo conserva el piso Owner de **95% de coverage**, con denominador y scope explícitos; el porcentaje no sustituye los oráculos. No mascarar failures históricos: reproducir baseline para atribuir los relevantes y conservar expected. No ejecutar suites que puedan escribir ETCD real. Los tests valiosos creados por el auditor se clasifican como PERMANENT_REGRESSION, E2E_CANDIDATE, HARNESS_TOOLKIT_CANDIDATE o DISPOSABLE_REPRODUCER, y se promueven dentro del Shot 4 cuando corresponde.

### Scope físico y release

El [[Echo + Echo Forge — Environment Contract]] rige: Forge tiene un ambiente operacional único, con candidatos aislados por recursos propios; Echo utiliza DEV/harness. Antes de registrar workers, demostrar endpoint, namespace, cola, prefijo, base/colección, PID y ownership efectivos. Ningún label candidate-local acredita aislamiento por sí solo. Source real empieza read-only; las escrituras de pruebas se realizan sólo en recursos propios autorizados.

No hay autorización en este programa para trading, órdenes, mutar Echo PROD, desplegar servicios compartidos, reiniciar workers de producción, interrumpir campañas, cambiar estrategias en extracción, sustituir SQX/plugins de flota, alterar datasets oficiales o aplicar migraciones a bases compartidas. No inventar Forge DEV. Las credenciales viven en stores aprobados; Flow JSON y Git sólo describen intención y referencias seguras.

### Persistencia y continuidad

A/B/C y los reportes D/E/F viven dentro de este mismo directorio del proyecto Forge. Echo conserva el addendum de su contrato. Código, fixtures y evidencia ejecutable/voluminosa permanecen en sus repositorios y workspaces; Agents-OS conserva decisiones, localizadores, hashes, resultados y continuidad compacta. No crear un tercer proyecto.

Actualizar proyecto, checkpoint y change_log consolidado tras cada gate material. El Owner autorizó la publicación íntegra de este paquete en Agents-OS público el 2026-10-27; el bloqueo previo queda resuelto para esta documentación. Agents-OS siempre en master, sin PR ni rama. Preservar cambios concurrentes mediante lectura reciente y conflicto optimista. No cerrar la sesión ni crear feedback/L0/L1: el Owner lo hará explícito. Esta instrucción específica prevalece sobre el cierre automático genérico de workers.

### Mandato reproducible de Shot 1 — ya despachado

Este paquete registra el encargo al arquitecto independiente. **No es una nueva orden de repetir el diseño.** El resultado vigente y la adjudicación están en B.

/goal

Actuar como GOD Principal Integration Architect independiente ONE-SHOT y entregar diseño ejecutable de una task configurable Forge → Echo V2, sin implementar. Resultado: DESIGN_CANDIDATE_READY_FOR_MANAGER_REVIEW. El Primary Manager decide el freeze después de inspeccionar evidencia.

/authorities

Cargar el mandato Owner de nueva task, las autoridades de este proyecto, el contrato de ambientes, Symphony CONSTITUTION y reglas 00/02/03/13/14. Baseline V2 consolidado y consumidor fijados en este plan. Leer A y Contract Source Review, no tratar los PASS históricos como pruebas nuevas.

/baseline

CURRENT_TASK_STATE: task nativa inexistente; HTTPIngressV2, ControlPlane V2 y CLI existen como dependencias. El pin SDK diverge del contrato candidato. Los stores reales, bindings y límites económicos están reconstruidos por especialistas. Dynamic Groups y Runtime son workstreams paralelos; no heredarlos ni reconciliarlos globalmente.

/frozen

KISS/YAGNI/SOLID; source_folder opaco; identidad desde contratos durables; ningún latest implícito; un contrato Go compartido y un adapter HTTP; The Lab como autoridad analítica; registro separado de habilitación; cero inferencias económicas; sin flota, deploy, campañas ni cambios de producto en Shot 1.

/scope

Resolver TaskSpec/TaskSource/cohort/evidencia, autoridad de definición/versión, transformación exacta de DTO, metadata fuente, histories, composición data-only, persistencia/recovery, límites por estrategia y compatibilidad. Proponer únicamente extensiones aditivas indispensables al contrato o stores existentes.

/execute

Elegir nombre y configuración concreta serializable; describir resolver determinista, puertos existentes/ampliaciones, activity/wiring, snapshot/manifest, key/scopes, receipts y errores. Distinguir missing/corrupt/ambiguous/unknown-outcome. Entregar mapping de todos los campos usados, file map y ejemplo completo alineado al modelo vigente. No pedir al Owner nombres de interfaces ni resolver ausencias inventando datos.

/verify

Cerrar oráculos A–E, rename, otro productor, identidades coincidentes por label, historia ausente/corrupta, costes/Q_i/FX/cobertura, crash/restart/concurrencia, SDK goldens y readback consumidor. No certificar runtime por source. Explicitar evidencia no disponible.

/reuse

Identificar y reutilizar resolvers, stores, readers, contratos, cliente y persistencia; descartar ETL framework, otro registry, otro cliente HTTP y otro motor analítico.

/improve

Sólo candidatos concretos observados o NONE; no editar skills ni generar feedback sin pedido Owner.

/close

Devolver diseño completo, decisiones con evidencia, gaps y handoff directo al Primary Manager. Éste materializa y publica en Agents-OS master. No ejecutar cierre de sesión. La entrega del especialista no se autoaprueba como freeze.

## Fuentes

- Mandato Owner del 2026-10-27.
- [[B — Frozen Design]] y [[Forge Task — Contract Addendum]].
- [[Echo + Echo Forge — Environment Contract]].
