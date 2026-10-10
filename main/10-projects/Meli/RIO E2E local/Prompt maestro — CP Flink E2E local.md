---
type: prompt
schema_version: 1
status: active
area: "[[Meli]]"
target: "Agente de desarrollo local con revisión independiente"
prompt_version: 1
inputs: ["Proyecto y diseño vigentes", "PRs y heads F1 actuales", "Repositorio y contratos del CP"]
outputs: ["SPEC y tareas READY", "Integración física local", "Verificación y continuidad"]
application: "[[rio-controlplane-flink]]"
project: "[[RIO E2E local]]"
aliases: []
related: ["[[RIO E2E local — Diseño revisado]]", "[[rio-playmaker]]", "[[rio-controlplane-kafka]]", "[[Descripción PR — rio-playmaker]]", "[[Descripción PR — rio-controlplane-kafka]]"]
tags:
  - kind/prompt
  - project/rio-e2e-local
created: "2026-10-09"
updated: "2026-10-09"
---

# Prompt maestro — CP Flink E2E local

## Propósito

Implementar F3 del proyecto con el CP Flink, alineado con el transporte Kafka y el harness F1 publicados. Exige demostrar primero submit/monitor/cancel de un job real; el transporte solo no certifica el motor.

## Contrato de entrada

Proyecto [[RIO E2E local]], [[RIO E2E local — Diseño revisado]], PRs/heads vigentes de [[Descripción PR — rio-playmaker]] y [[Descripción PR — rio-controlplane-kafka]], repos reales y sus AGENTS/contratos. Recuperar refs actuales antes de SPEC. Usar este prompt en una sesión separada; no ejecutar ambas integraciones simultáneamente sobre el mismo runtime.

## Contrato de salida

SPEC funcional/técnica y tareas READY por repo, ramas reviewables, transporte embebido y efectos físicos probados, regresiones/cobertura/aislamiento, matriz por caso y cleanup propio con reproducción independiente. Gates bloqueados conservan evidencia y próximo paso concreto.

## Prompt

```text
Implementa y verifica la integración local del CP Flink con PM y el broker de F1 usando transporte Kafka embebido. El objetivo físico incluye un job Flink real y su cancelación por DEPROVISION. Empieza por demostrar el seam mínimo: hoy ese criterio está BLOCKED. Transportar mensajes o producir FAILED reales es una entrega parcial válida y claramente etiquetada, pero no cierra el objetivo con PASS.

## Autoridad, contexto y arranque

Este pedido autoriza el discovery y fetch de los repos involucrados, ramas/worktrees aislados, implementación local, builds/pruebas y recursos locales propios necesarios para completar este alcance. Avanza autónomamente con decisiones rutinarias y corrige findings hasta el gate final. No autoriza deploy remoto, merge de PR, desactivar validaciones, operar una VM o borrar recursos ajenos. Si una decisión exige inventar semántica de negocio, resuélvela en SPEC/PLAN antes de implementar; no escondas la incertidumbre en un stub exitoso.

Respeta AGENTS.md. En cold start resuelve VAULT_ROOT desde AGENTS_OS_VAULT, luego ~/.config/agents-os/vault-root, luego el workspace sólo si contiene 80-agents/agents-os/agents-os.md; valida el marker. Lee y ejecuta una sola vez el bootstrap canónico 80-agents/skills/agents-os-bootstrap/SKILL.md. En warm reutiliza la base y haz sólo routing/delta de entidad. Recupera sdd-workflow y sdd-developer desde el catálogo/routing canónico que seleccione bootstrap; no inventes ubicaciones, no copies skills a Codex/Claude ni releas todo el vault. Las únicas skills canónicas viven en 80-agents/skills: resuelve allí las skills SDD vigentes mediante bootstrap; las copias legacy fuera de esa raíz no son autoridad. Si falta una skill necesaria, registra el bloqueo concreto sin inventar una ubicación.

Lee por delta el proyecto /Users/rjara/obsidian/SecondBrain/main/10-projects/Meli/RIO E2E local/RIO E2E local.md y el diseño /Users/rjara/obsidian/SecondBrain/main/10-projects/Meli/RIO E2E local/RIO E2E local — Diseño revisado.md. Lee AGENTS/security/contratos de cada repo antes de editar. Usa Markdown como verdad y Graphify sólo como índice. No cierres sesión de AGENTS OS sin pedido explícito.

Referencia F1 final publicada: CP Kafka https://github.com/melisource/fury_rio-controlplane-kafka/pull/86; companion Playmaker https://github.com/melisource/fury_rio-playmaker/pull/1286. Los heads/checks finales están enlazados en la continuidad del proyecto. Recuperar los dos PRs/heads de PM y CP Kafka desde la continuidad del proyecto o del mensaje del owner. Si al pegar este prompt se aportan URLs/refs, inspecciona su head y checks; si faltan, recupera los entregables y deja registrada su identidad real. Los checkouts de referencia son /Users/rjara/fuentes/rio-playmaker-rio-e2e-local y /Users/rjara/fuentes/rio-controlplane-kafka-rio-e2e-local; lee local/RIO_E2E.md y meli/features/20261009-rio-e2e-local/{1-functional/spec.md,2-technical/spec.md,3-tasks/tasks.md,4-implementation/VERIFICATION.md,4-implementation/SIMPLIFICATION_REVIEW.md} donde corresponda. En PM lee también 4-implementation/PR_INTEGRATION_REVIEW.md y PM_UPSTREAM_AUTH_MERGE_REVIEW.md: son la aceptación vigente tras integrar auth upstream; SIMPLIFICATION_REVIEW es historia. Respeta el estado CodeQL publicado: evidencia local no vuelve verde un workflow fallido. PM 90dfef733dc56138ccacdebe915c0e29ff81f4ac y CP b0d4587f0e0fc90180ddb5ceb05bdd96c3147dc8 son referencias históricas de la recertificación previa a PR, NO bases/head finales actuales. PM develop avanzó durante la publicación con fixes de auth de actions/history: relee y conserva esos guards. No asumas que los antiguos jars, conteos ni hashes certifican el head nuevo.

Antes de SPEC registra por repo origin, branch, HEAD, status ajeno y base remota real. Haz fetch autorizado y lee el delta hasta la ref actual; ls-remote sin recuperar los objetos no demuestra que hayas leído el código. No inferir SHAs vigentes del diseño del 09/10 ni de este prompt. Conserva originales sucios y worktrees HTTP/históricos; no reset/clean/stash ni merges implícitos para obtener un verde. Reutiliza un worktree adecuado o crea otro aislado fuera del vault con base/ref explícita y nombre descriptivo; registra dependencia de la integración F1 y del fix DEPROVISION si todavía no está integrado upstream, sin cherry-pick duplicado ni exigir merge previo.

SDD es obligatorio: discovery concreto → SPEC funcional → SPEC técnica/PLAN → TASKS READY y coherentes por repo afectado → implementación. Reutiliza las SPEC F1 como antecedente, no como autorización de decisiones nuevas. Resuelve el módulo canónico de tests y su owner en PLAN; no escondas ejecutables en carpetas de documentación. Ejecuta el loop de tres shots: IMPLEMENT, VERIFY por otro agente independiente sobre candidato congelado, CORRECT/final gate. Delega trabajo con límites de escritura explícitos; el verificador no arregla producto y deriva probes propios de aceptación. Congela commits/árbol y hashes de archivos/jars; si cambia fuente, invalida y repite sólo los gates afectados que correspondan. No compiles ni ejecutes Gradle simultáneamente sobre el mismo build dir.

## Invariantes F1 a conservar

PM es la única entrada HTTP de negocio. Triggers y resultados Kafka viajan embebidos en las apps, sin bridge/relay Kafka→HTTP ni llamadas loopback al controller HTTP. Un adapter puede invocar el handler in-process sólo si demuestra paridad; REST/SQL nativo del motor sí es una frontera de negocio legítima. Usa SDK JSON crudo snake_case, preserva árbol/campos desconocidos/context; no envelope msg en el broker ni tipado/reparseo que pierda datos. Keys deployment_id/action_id según canal. Conserva tópicos compartidos rio-deployment-trigger-local/rio-deployment-result-local y rio-action-trigger-local/rio-action-result-local, una partición, acks=all, publicación confirmada y productor idempotente conforme al contrato vigente.

Un broker y red rio-local pertenecen al Compose del CP Kafka. PM queda en host; cada nuevo CP/motor usa su propio Compose y se une a esa red externa, sin crear ni destruir broker/red. La topología del ecosistema la suministra el orquestador PM por RIO_LOCAL_TOPICS; no hardcodees un mapa 1..128 ni repartas ownership del broker entre repos. Group distinto por CP para cada canal que consume; PM mantiene su group de resultados. El observer usa assign sin group.id. Demuestra que un tipo ajeno se descarta igual que en el contrato productivo y que un trigger propio llega a exactamente el CP correcto: no compartir el group entre CPs.

Reutiliza la solución Spring Kafka F1, adaptada al CP actual, sin reescribir poll/rebalance/seek/lifecycle manuales. Factory RECORD, auto commit y auto topic creation apagados, consumidor raw bytes. ACK fuente sólo después de recepción productiva aceptada o DLT confirmada; fallo/timeout de DLT retiene fuente. FixedBackOff de 1000 ms × 2 y resetStateOnExceptionChange(false), poison no retry; FAILED de negocio es resultado normal, no DLT ni retry de negocio. DLT conserva key y bytes originales, Unicode/UTF8 inválido, envelope/trailing tokens y límite de 256 KiB por bytes; fallo de decode es distinto de fallo transitorio del servicio real. Productor pendiente/fallido, retries alternando excepciones, commit failure, rebalance/revocación, late ACK y shutdown tienen pruebas del framework configurado, no sólo mocks de getters. Shutdown debe exceder el ACK wait, drenar/cerrar ordenadamente y no proclamar concluido trabajo async aceptado que aún no terminó. Readiness local detecta container padre/hijo detenido, estado inesperado o falta de assignment; /ping solo no basta.

Comprueba versiones efectivamente resueltas y bytecode/runtime por repo; no copiar un pin a ciegas. F1 encontró VerifyError Spring Kafka 4.1.1 con Kafka clients 3.9.2; en CP Kafka el cliente 4.2.1 se limitó a classpaths locales y producto conservó 3.9.2 sin Spring Kafka. Eso es antecedente, no versión vigente obligatoria para otros CPs. No aflojes pins de seguridad productivos para resolver un adapter local. Nuevas clases/config/dependencias locales fuera del jar productivo; inventario permanente demuestra versiones exactas y ausencia de assets locales. Cualquier seam main mínimo necesario va separado, justificado y probado; reusa los publishers/controllers/procesadores/guards/idempotencia productivos.

Tiger/ACME/templates/KVS son sólo fronteras locales explícitas. Conserva auth de actions/history y todas las validaciones/approvals. Usa identidades/grants sintéticos mínimos; no deshabilitar auth para hacer pasar fixtures. KVS/locks debe conservar CAS/TTL/claim requeridos y declarar memoria por JVM sin persistencia/coordinación cross-process. No convertir una operación productiva, un resultado COMPLETED o un efecto físico en fixture. Conserva fix DEPROVISION, correlación por operación, prior ComponentRuns intactos, locks y afterCommit; redeploy PM emite el contrato realmente observado (F1 usa PROVISION reconciliado), no forzar UPDATE sólo para coincidir con una tabla vieja. El publisher-loss gap y el GCP provider unmapped de F1 se preservan y se prueban como tales; no prometer exactly-once ni recuperación que el negocio no tiene.

## Ownership, runtime y evidencia

Contexto conocido saludable: colima-rio-kafka-e2e-01a0f8e0. Revalida su disponibilidad, disco/RAM y baseline antes de usarlo y selecciónalo explícitamente por comando; no cambiar docker context activo ni adoptar stacks ajenos. El perfil original colima-rio permanece offline con cleanup del run 36868d2dbe3d NO CERTIFICADO. Su estado+identity+cp-owner+credentials privado está en /Users/rjara/fuentes/.rio-e2e-interrupted-state/36868d2dbe3d. No tocar, operar, restaurar, borrar ni mezclar esa VM/ledger en este alcance; no declarar su limpieza o reparación. Si el contexto sano no puede usarse sin afectar terceros, conserva evidencia y reporta el bloqueo concreto.

Una sola autoridad de runtime y suites seriales. Coordina lease/handoff con otros agentes o la otra integración; no lanzar ambos prompts contra el mismo ambiente a la vez. Mantén launcher ledger/nonce/labels, root/context/path exactos, PID birth+PGID+argv, máscara/restore de señales, child groups retenidos y drain antes de teardown, bloqueo test/stop, metadatos bootstrap recuperables y rechazo íntegro de estado preexistente/claim collision. Conserva restart bajo el runner propietario con rendezvous owned; tests no obtienen permiso Docker global. No global prune, kill por substring, borrar por nombre prefijado sin prueba de ownership ni detener VMs. Logs/receipts sin credenciales; las credenciales efímeras viven privadas y se eliminan con el estado propio.

Las pruebas mantienen fixtures nuevos y cleanup por método; serialización no implica dependencia entre tests. Demuestra ausencia de recursos/procesos propios contra IDs/labels capturados y preservación del baseline de containers/networks/volumes/images. Puertos no son inmediatamente libres sólo porque Compose down terminó: F1 observó limactl/TCP residuales y bare binds libres a los 54.244 s dentro de una espera de 60 s; conserva diagnóstico, espera acotada y prueba fresh-start real, sin señalar procesos compartidos ni atribuir una causa no aislada.

## Gate final y entrega

Tests focalizados significativos, regresión productiva completa y contratos/capabilities obligatorios de cada repo; conserva tests existentes/umbrales y skips heredados claramente identificados. Al menos 95% líneas Y ramas de código local crítico nuevo y main modificado: deriva cobertura de exec/classes completados, verifica class IDs y no excludes para esconder huecos ni XML viejo tras recompilar con otro JDK. Tests de paridad usan controller/filtros/validación reales y clientes sólo en la frontera; incluyen guards/dispatch/métricas/MDC/context/errores, sin equivalencia tautológica.

Certifica por APIs PM + eventos/offsets + estado/logs PM y efectos físicos directos del motor. Espera readiness y terminales por condición, no delays para estabilizar. Dos suites completas seguidas en el mismo stack vivo, recreación vacía y repetición, y reproducción exclusiva por otro agente desde clones exactos limpios/cwd arbitrario/paths con espacios. Mantén normal con presupuestos productivos; un caso destructivo que requiere timeout corto va en tarea/tag separado, presupuesto explícito acotado, ambos modos repetidos. No fijes un conteo mágico que permita omitir escenarios: catálogo de casos/métodos y receipts no vacíos con cero failures/errors/skips, restart real cuando corresponde, source/jar hashes. Si cambian fuentes tras el verificador, éste revalida el delta y sus gates.

Registra cada artefacto como PERMANENT_REGRESSION, E2E_CANDIDATE, HARNESS_TOOLKIT_CANDIDATE o DISPOSABLE_REPRODUCER; los findings corregidos estables vuelven a tests canónicos. VERIFICATION por caso, estado PASS/FAIL/BLOCKED/NO_EJECUTADO, comandos, bases/head/diffs/hashes, oráculos, limitaciones, retries y limpieza. No llamar verde remoto a un exit local ni certificar el proyecto de cinco apps por una fase backend. Entrega ramas/commits reviewables y evidencia reproducible; si el owner pide PRs, usa heads/checks actuales y adjunta enlaces, sin merge/deploy implícitos. Evalúa feedback reusable concreto (NONE válido), persiste continuidad suficiente y no cierres sesión sin pedido explícito.

## Discovery/spike físico obligatorio antes de codificar

Resuelve repo/worktree rio-controlplane-flink desde la entidad canónica, fetch y lee el delta vigente. 7c645ea/579a6ce y el cambio ajeno observado son historia. Relee SDK, controller handleDeploymentTrigger, guards/claims/context/métricas, processors, builders de flink-sql/job, publishers real/local, módulos cloud y rutas de actions realmente soportadas. No copiar capacidades de CP Kafka o CH a Flink ni inferir un SDK con context sólo porque PM lo tiene.

El antecedente es específico: AWS usa KDA SDK con US_EAST_1 sin endpointOverride; GCP usa Fury Cloud Controller + Dataproc; FlinkCloudAdapter sólo monitorea; LocalBigQueueDeploymentPublisher es logger y el publisher real tiene perfil excluyente. Una imagen Flink encendida no demuestra que el CP le envíe un job. Investiga primero la cadena completa desde params/artefacto de negocio hasta submit/start/monitor/cancel y resultado productivo. Identifica quién posee estado/IDs y qué llamadas/credenciales/red son inevitables; no ejecutar operaciones remotas cloud con este pedido local.

Produce evidencia de sólo lectura y un spike físico local mínimo cuando pueda hacerse con recursos propios: versiones/SDKs APIs efectivas, constructor/config/profile seam, lifecycle, dependencia de storage/artifacts, recursos RAM/disco/CPU medidos y endpoints. Evalúa versiones de Flink/job artifact/Java/connector/SQL gateway según código actual y docs primarias, sin latest, downgrade arbitrario ni pins productivos relajados. Si necesitas Cloud Controller o un adapter de runtime local, cuantifica el cambio mínimo y sus tests antes de READY; una respuesta 200 stub no cuenta.

Un seam puede usar REST/SQL Gateway nativo o Cloud Controller local que REALMENTE alcance el runtime, sólo si respeta la semántica productiva y reduce el cambio. El negocio/provisioning no puede ser un dummy que duerme o devuelve job_id falso. Un emulador KDA/Dataproc/LocalStack sin ejecución Flink física tampoco acredita el objetivo. No crear un nuevo framework cloud para evitar el análisis. Si exige refactor main mínimo, separa/justifica el puerto y adapter local y prueba la paridad; no modificar productive cloud behavior de oficio. Si no hay seam legítimo viable, marca F3 físico BLOCKED con evidencia, alternativas y cambio mínimo requerido; no sustituirlo por stub o bajar el criterio a transporte.

## Implementación condicionada a seam y SPEC READY

Listener local Spring Kafka y BigQueueClient bajo el publisher productivo, con lo mínimo de perfiles para excluir logger/file publisher en el perfil explícito local-kafka. Comprueba beans efectivos; el contrato de publish/error del CP Flink se descubre, no se presume idéntico al gap CP Kafka. Group rio-cp-flink-local y DLTs propias; mismos tópicos deployment/action sólo para canales realmente implementados. Mantén árbol SDK/unknown/context, guards productivos y paridad HTTP↔Kafka incluyendo filtros/binding/validación/excepciones/MDC. No despachar directamente al processor saltándose el intake.

El Compose Flink une CP y runtime/motores auxiliares necesarios a la red externa rio-local del broker CP Kafka. Identifica JobManager/TaskManagers/SQL gateway/storage requeridos por el seam demostrado; ni bridge de triggers/resultados ni broker adicional. Puertos y memory limits se eligen con medición y sin colisión; nuevas dependencias/config locales fuera del jar productivo. KVS/claim/lock fixtures tienen semántica real necesaria y límites por JVM declarados; AWS claim y ausencia de claim GCP no se homogeneizan por conveniencia.

Si F2 ClickHouse ya está integrada, recupera su PR/head/SPEC actuales y añade Flink a la configuración de N CPs del mismo runner, según la decisión del owner; no copies el runner. Si F2 todavía no existe, el spike Flink puede avanzar y una slice PM+Kafka+Flink puede verificarse explícitamente; no declarar el X1 de tres CP ni la fase F3 completa hasta tener CH certificado, y no implementar CH de oficio en esta tarea. En cualquiera de los dos casos, el crecimiento del runner es concreto: lista/configuración pequeña de CPs con checkout/Compose/project/ports/owner/readiness/restart target de Flink y runtime, ledger/drain/cleanup probado. Si el runner todavía sólo acepta Kafka, generalízalo a N CPs conservando compatibilidad F1 y demostrando los CPs presentes; no crear plugins ni framework anticipado. Broker y red siguen CP Kafka; baja Flink/runtime y demás CPs antes del broker/red.

## Matriz Flink y evidencia física

| Caso | Oráculos requeridos |
|---|---|
| F1 fallo real del contrato vigente | flink-sql PROVISION por API PM para proveedor/env no disponible: FAILED productivo con razón correcta, PM FAILED y ausencia de job/efecto propio. No un FAILED prefabricado por el adapter. Relee si este camino cambió upstream. |
| F2 tipo ajeno | Trigger kafka-topic/ClickHouse capturado o emitido por PM: Flink no procesa, no publica resultado de ese deployment_id ni crea/cancela jobs; mantiene ACK/drop conforme al controller real. |
| F3 PROVISION físico | API PM→trigger raw/key→controller/processor/publisher real; estados/progress del contrato, PM COMPLETED; job_id real, artefacto/SQL relacionado con params, JobManager/TaskManager efectivos, job RUNNING y evidencia de ejecución con input/output o métricas suficientes para ese contrato. Sólo encontrar un contenedor sano no basta. |
| F3 DEPROVISION físico | Nueva correlación lifecycle; ejecuciones previas PM intactas; cancel/stop real del job exacto propio, estado runtime esperado y ausencia de jobs propios activos; PM terminal correcto. No matar procesos/containers como sustituto del undeploy de negocio. |
| X1 | Si están presentes Kafka+CH+Flink, un trigger por tipo y results/effects de un único CP por ID, con groups distintos. Sin CH, registra esa porción NO_EJECUTADO/BLOCKED, no PASS. |
| X2/X4 | Poison raw en canales disponibles, no JSON/msg/trailing/UTF8/binary/byte cap; DLT original y commit sólo tras ACK, PM/negocio sin efecto; resultados inválidos PM y duplicados/tardíos preservan estado según contrato. |
| X3 | Restart físico del CP con trabajo ya terminal: nuevo miembro, mismos offsets, no relectura de accepted work ni resultados nuevos. Si la arquitectura permite restart del runtime, prueba aparte qué conserva realmente jobs/IDs; no asumir persistencia o recuperación por el KVS local. |

Incluye errores de submit/SQL/artefacto/runtime unavailable/cancel, params/binding/auth, PM rechazo antes del wire vs FAILED CP con wire, orden por operación y replay/idempotencia conforme a los claims actuales. No exigir soporte UPDATE/PEEK/list-warehouse/list-database si no lo tiene este CP ni fabricar endpoints. Si el journey Flink requiere actions reales, descubre/especifica esas actions y pruébalas con el runtime; front/browser sigue fase F4 y no se certifica por API.

Readiness conjunta comprueba motores y groups Stable asignados antes de mutar; readiness Flink debe verificar que el seam hacia submit/monitor/cancel está utilizable, no sólo /ping. Espera terminales y evidencia física antes de parar; un ACK del trigger puede preceder el trabajo async y no es prueba de completion. Prueba transporte pending/failed DLT y cierre real de callbacks con el framework configurado y clientes de frontera controlados, además del E2E físico. Conserva baseline/jobs ajenos; cleanup cancela/elimina sólo artefactos/recursos inequívocamente propios y demuestra ausencia.

No declarar F3 físico PASS mientras el seam esté sin demostrar. Si transport/guards/FAILED pasan y físico no, entrega tabla separada con esos PASS y físico BLOCKED, evidencia del obstáculo, seam/cambio mínimo propuesto, recursos medidos y continuidad ejecutable. La meta completa de cinco apps conserva el criterio físico original; no se redefine para cerrar la sesión con verde. Cuando el seam sea viable, completa los gates, repeticiones/recreación y verificador independiente definidos arriba, preservando regresiones F1 y F2 disponibles.
```

## Límites

Autoriza desarrollo y recursos locales propios. PR, merge y deploy requieren pedido específico. No operar la VM original offline ni certificar su cleanup pendiente. Conservar guards productivos, F1 y el criterio físico del proyecto; no sustituir efectos reales por callbacks exitosos. El agente consulta skills canónicas por bootstrap y cierra AGENTS OS sólo por pedido explícito.
