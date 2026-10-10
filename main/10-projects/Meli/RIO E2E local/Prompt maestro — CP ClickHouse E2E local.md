---
type: prompt
schema_version: 1
status: active
area: "[[Meli]]"
target: "Agente de desarrollo local con revisión independiente"
prompt_version: 1
inputs: ["Proyecto y diseño vigentes", "PRs y heads F1 actuales", "Repositorio y contratos del CP"]
outputs: ["SPEC y tareas READY", "Integración física local", "Verificación y continuidad"]
application: "[[rio-controlplane-clickhouse]]"
project: "[[RIO E2E local]]"
aliases: []
related: ["[[RIO E2E local — Diseño revisado]]", "[[rio-playmaker]]", "[[rio-controlplane-kafka]]", "[[Descripción PR — rio-playmaker]]", "[[Descripción PR — rio-controlplane-kafka]]"]
tags:
  - kind/prompt
  - project/rio-e2e-local
created: "2026-10-09"
updated: "2026-10-09"
---

# Prompt maestro — CP ClickHouse E2E local

## Propósito

Implementar F2 del proyecto con el CP ClickHouse, alineado con el transporte Kafka y el harness F1 publicados. Exige SQL y lifecycle físicos.

## Contrato de entrada

Proyecto [[RIO E2E local]], [[RIO E2E local — Diseño revisado]], PRs/heads vigentes de [[Descripción PR — rio-playmaker]] y [[Descripción PR — rio-controlplane-kafka]], repos reales y sus AGENTS/contratos. Recuperar refs actuales antes de SPEC. Usar este prompt en una sesión separada; no ejecutar ambas integraciones simultáneamente sobre el mismo runtime.

## Contrato de salida

SPEC funcional/técnica y tareas READY por repo, ramas reviewables, transporte embebido y efectos físicos probados, regresiones/cobertura/aislamiento, matriz por caso y cleanup propio con reproducción independiente. Gates bloqueados conservan evidencia y próximo paso concreto.

## Prompt

```text
Implementa y verifica F2 del proyecto RIO E2E local: agregar el CP ClickHouse real y su motor físico a F1, mediante el mismo transporte Kafka embebido. Incluye deployments MergeTree/materialized view y actions list-warehouse/list-database que usan los journeys iniciales. Conserva F1 y entrega certificación backend de este alcance; front/browser permanece F4 y no se marca PASS por estas pruebas.

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

## Discovery y decisiones particulares de ClickHouse

Resuelve el checkout real de rio-controlplane-clickhouse desde su entidad canónica; fetch y lectura del develop/ref actual son previos a SPEC. Los refs c8b20b6/ac4662a y los 10 cambios ajenos del discovery son historia, no estado actual. Inspecciona el SDK efectivo, DeploymentEventController.receiveEvent, @Valid/BindingResult, RoutingFilter, exception handlers, actions, publishers, BigQueueClientFactory/LocalFileBigQueueClient, KVS/lock/KMS locales y cliente on-prem. Descubre rutas/payloads reales de PM y CP por caso; no presumir las operaciones/progress/result shapes de CP Kafka.

A (adapter in-process) sólo si conserva limpiamente la capa MVC con paridad demostrada. CH es candidato a B: si @Valid/BindingResult, routing o excepciones exigen reimplementar MVC, extrae un intake estructural mínimo compartido por controller y listener, sin duplicar negocio ni extenderlo. Decide mediante pruebas y documenta el main delta mínimo antes de READY. Nunca MockMvc/HTTP dentro del runtime como sustituto del handler.

Sustituye el publisher local a archivo con BigQueueClient Kafka bajo el publisher productivo, usando seam @Primary/profile local si basta; incluye el canal de actions que de verdad existe. Valida selección de beans, serializers y destrucción única sin suprimir factories framework productivas. CP/motor se unen a rio-local; no un segundo broker. Group rio-cp-clickhouse-local y DLTs propias de deployment/actions, verificando no colisión con Kafka.

Fija una imagen ClickHouse concreta tras comprobar versión on-prem productiva si es accesible; si no, elige por pruebas físicas de compatibilidad y declara que no acredita paridad de versión productiva. No latest ni resolver incompatibilidad format= sólo cambiando un string sin probar el cliente real. Valida JDK/toolchain e imágenes actuales. MergeTree/MV single-node son el alcance mínimo; Kafka connector con ON CLUSTER/Keeper/S3 queda fuera salvo nuevo alcance explícito. Local ownership no-op existente y KMS/locks sustituidos deben quedar declarados, sin prometer autorización productiva por usar credenciales locales.

Aplica la decisión vigente del owner: generaliza el mismo runner a N CPs al sumar ClickHouse, sin copiarlo. Usa una lista/configuración pequeña de CPs con root/Compose/project/ports/nonce/readiness/restart target y cleanup; demuestra concretamente Kafka + ClickHouse. Conserva ledger y lifecycle ya probados. No construir plugins, librería SDK, clases base universales ni adapters especulativos de Flink; N CPs es configuración del orquestador, no un framework nuevo. La topología añade sus DLTs desde PM; CP Kafka sigue dueño broker/red. Los tests esperan terminales antes del teardown. Orden de cleanup: drenar los grupos de procesos propios, bajar CH y su motor, MySQL y CP Kafka/broker/red al final; no certificar completion de trabajo async sólo porque el proceso cerró. No romper CLI standalone/defaults de F1 sin compatibilidad documentada.

## Matriz obligatoria C1–C6, A1 y aislamiento

| Caso | Oráculos requeridos |
|---|---|
| C1 MergeTree PROVISION | Entrada API PM válida; trigger SDK/context/key; progress del contrato real (snapshot STARTED→IN_PROGRESS×4→COMPLETED); estado/logs PM; query física de DB, tabla/DDL/columnas, usuarios ro/rw y grants. Prueba acceso real mínimo conforme a esos permisos con secretos locales privados. |
| C2 cambio MergeTree | La operación que PM realmente emita y el reconcile/UPDATE vigente; terminal/logs PM y ALTER físico observado. Si UPDATE literal no se emite desde PM, prueba su contrato CP separado sin falsificar la ruta PM. |
| C3 DEPROVISION | API undeploy y camino inactivate pertinente; correlación nueva, ejecuciones previas intactas y terminal PM; tabla/usuarios propios ausentes, sin borrar sistema ni recursos ajenos. |
| C4 materialized view PROVISION/DEPROVISION | Vista y usuario reales, DDL/dependencia/datos correctos según contrato, estado PM y posterior ausencia física. |
| C5 context ausente/inválido | Distingue rechazo PM previo al wire de FAILED real CP sin STARTED cuando llegue al CP; sin efecto físico. No fabricar un successful callback ni desactivar validación para alcanzar la rama. |
| C6 materialized view UPDATE | Si el negocio vigente conserva no soportado: FAILED de negocio esperado en PM, razón correcta y vista/usuarios/datos sin cambio; no marcar FAIL técnico ni implementar UPDATE de oficio. |
| A1 list-warehouse/list-database | APIs actions PM reales y polling de la ruta vigente (snapshot /v2/actions/{id}); action_id/correlación/auth; publisher/resultado SDK real; resultados consistentes con consultas al motor y errores/locks/CAS/TTL del contrato. Sin listas hardcodeadas. |
| X1/X2/X3/X4 | Trigger por tipo procesado sólo por su CP; foreign type no crea resultados/efectos CH. Poison en ambos canales y resultados PM preservan bytes/key con DLT/offset barrier; restart CH físico cambia miembro y conserva offsets/PM/identidad física sin replay de trabajo ya aceptado. |

Cubre negativos del cliente/motor, params y binding, PM rejection vs CP FAILED, replay de trigger y resultados duplicados/tardíos, orden por operación y persistencia/correlación de lifecycle. No exigir que replay CH tenga el mismo comportamiento que Kafka: deriva isAlreadyCompleted/claims actuales y comprueba los efectos y mensajes productivos. Captura SQL/system.* para demostrar físico; log o fichero result no sustituye DB. Recursos con prefijo/owner único por método y operaciones seriales dentro de lifecycle.

Conserva la matriz backend F1 Kafka (incluido PEEK y publication-loss gap separado), sus paridades y sus límites. El gate del nuevo CP no puede certificar aislamiento multi-CP ejecutando sólo CH ni omitir regresiones Kafka. Si el delta descubierto contradice una expectativa del snapshot, documenta contrato vigente en SPEC antes de implementar, sin debilitar el objetivo físico. Cierre F2 exige C1–C6 y A1 backend acreditados; cualquier blocker material se entrega reproducible, no como PASS parcial silencioso.
```

## Límites

Autoriza desarrollo y recursos locales propios. PR, merge y deploy requieren pedido específico. No operar la VM original offline ni certificar su cleanup pendiente. Conservar guards productivos, F1 y el criterio físico del proyecto; no sustituir efectos reales por callbacks exitosos. El agente consulta skills canónicas por bootstrap y cierra AGENTS OS sólo por pedido explícito.
