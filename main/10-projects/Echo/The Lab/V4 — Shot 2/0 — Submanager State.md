---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[SHOT3_ADVERSARIAL_REPORT]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-21"
updated: "2026-10-21"
---

# V4 Shot 2 — Submanager State (durable)

## Propósito

Mantener el estado vigente del programa V4 y el handoff entre implementación, auditoría independiente y validación crítica.

## Contenido

**Role:** Implementation Submanager / Technical Integration Lead (mandato maestro 2026-10-20). **Engine:** GLM-5.3-Flash Max LOCAL. **Estado global:** ver [[F — Decision Register]] §V4 y [[Echo — Producto Integrado]].

## Shot 3 — resultado vigente y distribución de roles, 2026-10-21

**Instrucción actual Owner:** GPT-6-Luna o GPT-6.1-Sol sustituyen GLM según el trabajo; esta auditoría fue ejecutada íntegramente por **GPT-6.1-Sol / reasoning high**, auditor independiente en Codex LOCAL. No atribuir su trabajo a GLM. El auditor inspeccionó source, creó PG propio, escribió repros, ejecutó pruebas y produjo los informes; Astra fija criterio y valida evidencia compacta. Esta distribución sustituye las asignaciones antiguas al GOD presentes más abajo, que quedan como historia del programa. La excepción serial de Shot 2 no autoriza al GOD a absorber la investigación de Shot 3.

**Corte auditado fijo:** `xKoRx/echo@61ac1f720d07513e48b0310b84b5b415b80ff48f`, base `d74b652500e673fc2bf4289f9f195f11960ba26e`; clon detached independiente y PG16.3 propio en loopback 54339, data-dir separado. Árbol del implementador intacto; sin fixes, merge, deploy, servicios compartidos ni PROD.

**AUDIT BLOCKED; PRODUCT INCOMPLETE; VERDICT FAIL_DEFECTS_AND_INCOMPLETE_SCOPE.** La investigación funcional autorizada está entregada. El harness excluyó pruebas dinámicas de autenticación, autorización, aislamiento de seguridad y traversal; quedan **NOT_RUN — harness safety restriction** y no permiten declarar completa la auditoría original. No se reintentaron esos casos ni se sustituyó modelo/proveedor para eludir el límite.

**Evidencia propia:** 41 casos candidatos distintos = 17 PASS_EXECUTED / 24 FAIL_EXECUTED; siete TestLabV4 entregados reproducidos 7/7. Contraste de cinco tests comunes baseline = 5 PASS y candidato = 5 FAIL por fixtures incompatibles con nuevas FK. Once checks racionales independientes PASS sólo como oráculos. CAS real concurrente PASS; replay concurrente FAIL; go vet de tres superficies PASS. No suite completa, benchmark 20k, Forge físico o seguridad dinámica certificados. Coverage de repetición dirigida 7,1% no acredita el gate 95%.

**Hallazgos prioritarios:** ingesta terminal/multioperación rota; revisión mutable bajo mismo digest; sello SQL con NULL/monedas incompatibles; artefacto incompleto y sink opcional; receipts parciales; down 067 pierde fills si operations vacía. **I1 falta:** endpoints/Forge auténtico, Q_i y atribución por Operation/adapters, worker/cuatro perfiles/métricas, selección/dashboard/metadata, composición estática, sustitución/capacidad.

**Artefactos canónicos:** [[SHOT3_ADVERSARIAL_REPORT]], [[SHOT3_COVERAGE_MATRIX]], [[SHOT4_EXECUTION_PACKAGE]], [[GOD_REVIEW_BRIEF]], [[SHOT3_DIRECTED_EXTRACTS]]. Paquete reutilizable en workspace externo de este encargo: `outputs/SHOT3_AUDIT_EVIDENCE/`. Brief <1.500 palabras; seis fragmentos/152 líneas. **NEXT GOD_CRITICAL_VALIDATION.** Astra aún no aprobó la auditoría. Shot 4 no iniciado ni proyecto/sesión cerrados.

## Shot 4 — SHOT4_AUTHORIZED_CORRECTIONS_AND_I1_COMPLETION, 2026-10-21

**Mandato vigente:** Metis acepta Shot 3 como evidencia accionable. Shot 4 = corregir S3-F01–F08, completar S3-M01–M06, resolver S3-E01, conservar S3-E02 (NOT_RUN — harness safety restriction), integrar sobre un SHA final y entregar candidato verificable. No hay quinto shot, no freeze, no re-pedido D09/D10/D11/D16. Corte de entrada fijo `61ac1f720d07513e48b0310b84b5b415b80ff48f` (rama `feature/lab-v4-shot2`); evidencia del auditor verificada localmente en `outputs/SHOT3_AUDIT_EVIDENCE/` (repros + JSONs + MANIFEST íntegro). Workspace de escritura propio de Shot 4: `~/aranea/work/lab-v4-shot4-20261021/echo`, rama `feature/lab-v4-shot4`; PG descartable propio en puerto/data-dir nuevos (sin reutilizar 54329/54339). Engine efectivo: host declara GLM-5.3-Flash; el perfil GPT-6-Luna indicado en el encabezado del mandato no pudo verificarse desde este runtime y se registra la discrepancia; la dirección vigente del programa (sección siguiente) asigna Shot 4 a GLM-5.3-Flash Max LOCAL. Descomposición de ejecución: [[SHOT4_EXECUTION_PACKAGE]] P0–P9; workers ONE-SHOT opcionales y secuenciales para paquetes disjuntos; revisor final del delta en contexto fresco (mismo perfil autorizado, sesión separada, sin escritura de producto). Sin merge, deploy, PROD, trading ni servicios compartidos. NEXT: ejecución P0–P9 → revisión independiente → HANDOFF PRIMARY_MANAGER_FINAL_REVIEW.

## Dirección vigente del programa — Owner / Primary Manager, 2026-10-21

El Owner dispone de un GOD LOCAL y solicita continuar con **Shot 3 y Shot 4**, sin reabrir el bucle de diseño. **SHOT3_AUTHORIZED_ON_PARTIAL_CANDIDATE**: auditoría adversarial independiente de código y diseño sobre el corte entregado. Esta decisión sustituye la prohibición anterior de iniciar Shot 3, pero **NO** declara Shot 2 completo ni acepta como implementadas capacidades ausentes.

**Corte reportado por el implementador:** `feature/lab-v4-shot2@61ac1f72`, cuatro commits (`e85656bb`, `7d36dbf4`, `6b697f3b`, `61ac1f72`) sobre `d74b6525`. Fuente: handoff del bloque 1 + estado de esta nota. El GOD debe resolver y registrar el SHA completo LOCAL antes de auditar. La consulta GitHub de Metis no pudo resolver `61ac1f72`; no es prueba de inexistencia del commit local ni exige publicarlo para poder auditarlo.

**Admisión excepcional, no relajación del resultado:** Shot 3 verifica lo existente y registra por separado defectos, contradicciones materiales de diseño, alcance I1 todavía no implementado y límites de entorno. Los 7/7 tests son evidencia reportada por el implementador, no certificación independiente ni prueba de todos los gates.

**Shot 4:** GLM-5.3-Flash Max LOCAL corrige findings y completa los faltantes del alcance I1 ya aprobado que queden identificados al corte, sin agregar I2 ni reducir gates. Toda capacidad agregada después del corte auditado debe probarse en el gate final de Shot 4 y recibir revisión independiente del delta en contexto fresco. Ese control pertenece a Shot 4; no crea Shot 5 ni otra fase de freeze.

**Aislamiento:** solicitar al implementador fijar el corte y pausar nuevas escrituras de producto/despachos de Shot 2 para este handoff; no se afirma que ya esté pausado. GOD usa worktree/clone de auditoría separado, SHA fijo y PG descartable propio, sin borrar archivos ajenos ni compartir un árbol de escritura. No `git clean`, resets ni arreglos sobre el checkout del implementador.

**Diseño:** GOD puede señalar una contradicción con evidencia y recomendar el cambio técnico mínimo ejecutable en Shot 4; no una revisión 4 del freeze ni otra entrevista de D09/D10/D11/D16. No modificar código de producto durante Shot 3. Se mantienen los permisos operacionales originales: sin PROD, trading, bases/servicios compartidos ni merge de producto a master por esta decisión. Agents-OS sigue en master. No cerrar la sesión del submanager ni el proyecto.

## Gate de diseño aceptado — Primary Manager, 2026-10-21

**TECHNICAL_FREEZE_ACCEPTED_V3 — IMPLEMENTATION_AUTHORIZED.** Metis, Primary Manager, acepta el paquete revisión 3 para implementación en respuesta al Owner, quien exige terminar las revisiones preparatorias y continuar el programa original de cuatro shots. D09/D10/D11/D16 permanecen ratificadas, sin nuevas preguntas de producto.

**Corte aceptado:** `xKoRx/agents-os@eb9ad25e`, archivo `main/10-projects/Echo/The Lab/V4 — Shot 2/1 — TECHNICAL_FREEZE_PACKET.md`, blob `cee739a8f8ae7c0bfe2d7e30bc473c88ab608c78` (paquete publicado también en commit `5d6cae71`). El diseño GOD más las ratificaciones y esta concreción V3 forman el contrato de implementación. La etiqueta histórica READY del paquete no es un gate pendiente adicional.

Esta aceptación sustituye los dictámenes `TECHNICAL_FREEZE_REPAIR_REQUIRED` / `TECHNICAL_FREEZE_REPAIR_REQUIRED_V2` y las esperas de aceptación V2/V3 para este corte. También satisface la condición de aceptación técnica pendiente consignada el 20-10 en el registro y el proyecto padre; no modifica decisiones de producto ni declara resultados de implementación todavía inexistentes.

**Alcance del GO:** código, integración en la rama de trabajo, archivos de migración y pruebas locales/descartables dentro de I1 y del presupuesto autorizado. **No autoriza** deploy/reinicio en servicios compartidos, mutaciones de bases compartidas, PROD, trading, campañas, merge a master de producto ni retiro destructivo sin sus permisos específicos. Agents-OS sí continúa directamente en master.

**Estado honesto de entrega:** implementación autorizada; no demostrada aún por este registro. El freeze acepta contratos para construir, NO certifica las garantías, el rendimiento, la integración física ni la ausencia de defectos.

### Ejecución sin otra ronda de aprobación de diseño

- No preparar revisión 4, otro discovery, otro preflight general ni volver a pedir aceptación de D09/D10/D11/D16 o de este freeze.
- Las precisiones de ingeniería, bugs, comportamiento SQL, orden de migraciones, límites de memoria, publicación coherente y casos económicos se resuelven implementando y probando dentro del programa. Registrar el delta y evidencia; no convertir cada decisión técnica ordinaria en un nuevo gate humano.
- Se mantienen los invariantes y G1–G11/T01–T45 más los casos añadidos C01–C06. Ningún input fijado por un resultado puede cambiar silenciosamente: un append debe conservar su identidad reproducible mediante el contrato de revisión/snapshot. No se aprueba degradar requisitos o cambiar oráculos para conseguir verde.
- Escalar sólo una nueva decisión real de producto, contradicción irresoluble con lo ratificado, riesgo de pérdida de datos o acción fuera de los permisos disponibles. Un fallo de tests normalmente se corrige dentro del shot. Un bloqueo de entorno detiene la acción dependiente; no todo el trabajo independiente.
- **Excepción de ejecución autorizada por el Primary Manager, limitada a Shot 2:** preferir workers secuenciales con GLM-5.3-Flash Max. Si el harness vuelve a cancelar despachos, el submanager puede asumir explícitamente el rol de implementador/integrador y ejecutar en serie con ese mismo motor, registrando trabajo propio y ownership. No requiere otro permiso de diseño ni cambio de modelo/proveedor/cuota; no presentarlo como verificación independiente. Esta excepción sustituye únicamente el fallback restrictivo de §7/§10 del paquete. Shot 3 conserva auditor/contexto independiente de la implementación.

**Programa invariable:** Shot 1 diseño; Shot 2 implementación e integración; Shot 3 adversarial independiente; Shot 4 correcciones y gate final, incluyendo cierre de faltantes I1 identificados en el corte parcial autorizado. No hay nuevos shots ni nuevas autorizaciones generales de diseño.

## Baselines verificados por el submanager (2026-10-21, daedalus)

| Repo / superficie | Baseline | Verificación |
|---|---|---|
| `xKoRx/echo` origin/master | `d74b6525` (= baseline de diseño; re-verificado fetch 2026-10-21) | fetch + rev-list en clon Shot 2 |
| `xKoRx/echo` rama e04 | `feature/e04-dev-ingest-recovery` @ `4aad647b`: 5 commits exclusivos (seeds+wiring, policy_id, platform+migración 068, guard DeleteVar, renumber); 305 detrás de master | git log/cherry/diff en clon Shot 2 (EV-E01) |
| `xKoRx/echo` stream concurrente | `feature/ef-runtime-pools` @ `112ccccd` (FEFB S01) — dueña del grammar Java; renombres coordinados | NO integrar |
| `xKoRx/symphony` origin/master | `daded14` (release 0.3.2) | clone limpio existente |
| Workspace Shot 2 | `~/aranea/work/lab-v4-shot2-20261020/echo` rama `feature/lab-v4-shot2` @ `d74b6525`, limpio en el preflight | verificado por el submanager 2026-10-21; refrescar deltas antes de cambios dependientes |
| PG DEV `echo-develop` @ .220 | sin `schema_migrations`; efectos reportados 001→065 + CHECK 4 tokens aplicados a mano; `futures_*` ausente; 5 objetos lab legacy admin-owned; REFERENCE 137.276 filas (64,7% risk_money) | SELECT-only del submanager 2026-10-21 (EV-E05..E11); no reejecutado por Metis en esta aceptación |

## Correcciones históricas del preflight

065 SÍ presenta su schema en DEV; distribución del journal medida por el submanager p50=19/p75=33/p95=59/p99=24.682/max=56.884 por strategy+symbol. Los tamaños serializados V1 son referencia, no certificación del envelope V2. Ausencia de actividad del proyector en logs NO demuestra ausencia de consumidores.

El toolkit de migración real ejecuta `db.Exec` por archivo; no demuestra golang-migrate ni tracking histórico. No registrar 066 como aplicada ficticiamente. Creación aditiva V4 y retiro legacy tienen acciones/permisos separados.

## Restricciones activas

- Sin mutaciones PROD, trading o campañas. Deploys/reinicios DEV y migraciones en la compartida requieren ownership y autorización específicos; pruebas en recursos locales/descartables autorizados no quedan bloqueadas por ello.
- Preservar cambios ajenos, protecciones de seeds, event triggers/metadata compartidos e identidades selladas; no integrar indiscriminadamente E-04 o FEFB.
- Horario Owner: 08:00–02:30 CLST; al parar, estado durable y procesos propios seguros; sin presuponer reanudación automática.
- Agents-OS sobre master, cambios pequeños + change_log. No cerrar sesión del submanager ni generar feedback de cierre sin pedido del Owner.

## I1 — corte parcial entregado (2026-10-21, bloque 1)

**Rama reportada:** `feature/lab-v4-shot2` @ `61ac1f72` (4 commits sobre `d74b6525`: `e85656bb` fundación, `7d36dbf4` i-e04, `6b697f3b` suite verde, `61ac1f72` guard scratch). **PG desechable reportado:** pgboot embebido (fergusstrange/zonky) en `127.0.0.1:54329` db `echo_labv4` (datos en `~/aranea/work/lab-v4-shot2-20261020/pgdata`; relanzar con `pgboot` en `~/aranea/work/lab-v4-shot2-20261020/pgboot/`; sin root, sin docker). **Comando reportado de la suite:** `DATABASE_URL=postgres://labv4:labv4@127.0.0.1:54329/echo_labv4?sslmode=disable LABV4_MIGRATION_TEST=1 go test ./v3/sdk/postgres/ -run TestLabV4` (desde `v3/sdk`). El auditor debe comprobar el directorio de ejecución y el comando realmente válidos; no se certifica esa receta desde CLOUD.

**VERDE REPORTADO (pendiente reproducción independiente):** 7/7 `TestLabV4*` PASS — cadena 067→071 up/down/up con `lab_migration_state` exacta (C01); atomicidad por archivo con fallo forzado (C01); retiro legacy safe-by-default BLOCKED_SKIP→DROPPED armado (C01); recetas de identidad definition-v1/native-v1 con slots NULL y CYCLE_BUDGET sin evidencia rechazado (C02/C03); terminalidad DEFERRABLE net=Σ movements + movements append-only + CLOSED_SUMMARY legítimo (C03/C04/C05); ingesta POST/replay/409/CAS-412 + colisión de history_id imposible entre writers + analítica sin ejecutable + mapping no-venue sin magic (C02/C04/R04). Suite completa `./v3/sdk/postgres`: PASS reportado (scratch ahora skip-gated). Gateway `internal`: PASS reportado. i-e04 completo reportado con tests portados (plataforma sellada, policy gate v2, receipts por namespace, fs artifact source).

**Pendiente I1 (alcance aceptado; verificar al corte):** (1) handlers HTTP v2 en gateway (`strategy_history_v2_handler.go` nuevo + rutas POST `/api/v2/strategy-ingestions` y PUT `/api/v2/strategy-versions/{ref}/histories/{history_id}` con 128 MiB/413/412/409; el servicio ya está según handoff) + gate E2E Forge con fixture auténtico; (2) adapters: economía por Operation con correlación (caso A/B=5), QI_SEALED en la primera decisión MM, topic `echo.execution.operation-facts.v2`, adapter journal REFERENCE→v2 y backtester→v2 por el mismo servicio (caso T sobre esa ruta); (3) lab-worker-v4 (jobs SKIP LOCKED+lease+CAS, 4 perfiles, métricas B.6.5); (4) dashboard Vue + metadata Hasura aditiva; (5) composición estática, sustitución legacy autorizada y matriz G1–G11/T01–T45 completa. No interpretar una omisión en el resumen del bloque como retiro de alcance.

**Precisión de ingeniería registrada (dentro del contrato):** `run_mode` reutiliza el enum del producto ('LIVE','EXACT_REPLAY','BACKTEST') — REPLAY==EXACT_REPLAY, sin tokens nuevos; `identity_mappings.magic` NULLable solo para identidades no-venue con guard `magic_allocation_ref='labv4/no-venue'` (069) — el esquema 061 exigía NOT NULL y el freeze prohíbe magics ficticios; 068 (e04 verbatim) lleva el auto-registro del protocolo C01 añadido; el constraint trigger de terminalidad dispara en INSERT y UPDATE (sellos insertados directamente también se validan). Verificar invariantes y alcance durante Shot 3.

**Incidente de coordinación reportado:** el worker i-e04 eliminó temporalmente archivos untracked del submanager en el worktree compartido (los restauró incompletos). La mitigación del implementador fue commitear archivos propios y declarar archivos ajenos intocables. Para Shot 3/4 se exige además separación de worktrees de escritura; no dar la integridad de tests/harness por certificada sin contrastar el corte.

**Estado:** SHOT2_PARTIAL_DELIVERED; I1 NO COMPLETE. Admisión a Shot 3 autorizada sobre este estado sin ocultar pendientes.

## Siguiente acción vigente

**GOD_CRITICAL_VALIDATION:** Astra valida hasta tres conclusiones críticas mediante [[GOD_REVIEW_BRIEF]] y seis fragmentos dirigidos; el informe y la matriz conservan el resto. Priorizar correcciones P1 y completar I1 mediante [[SHOT4_EXECUTION_PACKAGE]], dentro de Shot 4 y con revisión independiente de todo delta final en contexto fresco. No reabrir discovery/freeze ni crear un quinto shot. AUDIT permanece BLOCKED mientras no pueda cubrirse el alcance dinámico excluido por el harness.

No iniciar fixes durante esta auditoría ni declarar aprobación por Astra anticipadamente. Sin merge, deploy, servicios compartidos, PROD ni cierre de proyecto/sesión por este handoff.

## Log de avance

- 2026-10-20: bootstrap; 4 autoridades; baselines; workspace; preflight U01–U06 por el submanager; paquete rev 1 (`TECHNICAL_FREEZE_READY`).
- 2026-10-21: dictamen Manager R01–R06 y paquete rev 2; investigación read-only y evidencia publicadas. Sin edición de producto.
- 2026-10-21: dictamen Manager C01–C06 y paquete rev 3 (`TECHNICAL_FREEZE_READY_V3`), entrega `eb9ad25e`; correcciones de identidad, riesgo, atribución económica, retención, transporte y migraciones documentadas. Sin edición de producto.
- 2026-10-21: Primary Manager acepta corte V3 `cee739a8f8ae7c0bfe2d7e30bc473c88ab608c78`: `TECHNICAL_FREEZE_ACCEPTED_V3 / IMPLEMENTATION_AUTHORIZED`. Termina el ciclo de revisión preparatoria; mantiene cuatro shots. Excepción explícita de ejecución serial propia dentro de Shot 2 ante fallo de workers, con atribución honesta e independencia de Shot 3 preservada. Esta actualización es documental, no evidencia de código implementado.
- 2026-10-21: Owner solicita continuar Shot 3/4 y ofrece GOD LOCAL. Primary Manager autoriza Shot 3 sobre candidato parcial reportado `61ac1f72`, sin reabrir freeze ni certificar I1; Shot 4 incluye faltantes del alcance aprobado y correcciones, con revisión independiente del delta final. Solo actualización documental; pausa del implementador y ejecución de auditoría aún no demostradas.

- 2026-10-21: auditor independiente GPT-6.1-Sol / reasoning high entrega Shot 3 funcional sobre SHA completo 61ac1f720d07513e48b0310b84b5b415b80ff48f: 41 casos candidatos 17 PASS / 24 FAIL, baseline común 5 PASS, 11 oráculos PASS. AUDIT BLOCKED por harness safety restriction; PRODUCT INCOMPLETE. Cuatro entregables más extractos y repros preservados; siguiente GOD_CRITICAL_VALIDATION. Sin fixes ni Shot 4. Envelope legacy migrado explícitamente a doc/schema_version 1 mediante materializador, preservando cuerpo histórico.
