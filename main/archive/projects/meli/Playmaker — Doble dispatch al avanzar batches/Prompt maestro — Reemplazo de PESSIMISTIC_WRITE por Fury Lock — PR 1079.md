---
type: prompt
schema_version: 1
status: active
area: "[[Meli]]"
target: "Codex orquestador con Luna para desarrollo y Zord para review y autoría del PR"
prompt_version: 1
inputs:
  - Rama feature/serialize-batch-completed-listener y PR #1079
  - Commit de referencia Fury Lock cf154b16e de feature/serialize-batch-completed-listener-test
  - Implementación vigente con PESSIMISTIC_WRITE en f7d4f4881
  - Tests de comportamiento concurrente y documentación local del PR
outputs:
  - Implementación Fury Lock sin PESSIMISTIC_WRITE para el avance de batches
  - Tests conductuales que reproducen 2 dispatches sin lock y exactamente 1 con Fury Lock
  - Review Zord cerrado y correcciones implementadas por Luna
  - Commit, push, descripción local/GitHub y versión Fury verificadas
application: "[[rio-playmaker]]"
project: "[[Playmaker — Doble dispatch al avanzar batches]]"
aliases:
  - Prompt maestro Fury Lock PR 1079
  - Rehacer listener lock con Fury Lock
related:
  - "[[Descripción PR — rio-playmaker — Hotfix doble dispatch]]"
  - "[[Prompt maestro — Auditoría independiente del doble dispatch]]"
tags:
  - kind/prompt
  - area/meli
  - project/playmaker-double-dispatch
  - app/rio-playmaker
created: "2026-08-27"
updated: "2026-08-27"
---

# Prompt maestro — Reemplazo de PESSIMISTIC_WRITE por Fury Lock — PR 1079

## Propósito

Ejecutar de punta a punta el reemplazo del lock MySQL `PESSIMISTIC_WRITE` del PR #1079 por Fury Lock, tomando como referencia controlada la variante que ya fue probada en la rama de test. El agente raíz sólo orquesta: Luna realiza todos los cambios de código, configuración y tests; Zord realiza el review y genera la descripción final del PR. El proceso termina con validación conductual, commit, push, actualización local/GitHub, release y cierre de Agents OS.

## Contrato de entrada

- Repositorio: `melisource/fury_rio-playmaker`.
- PR: `#1079`.
- Rama objetivo: `feature/serialize-batch-completed-listener`.
- Estado vigente conocido: commit `f7d4f4881`, con serialización mediante `PESSIMISTIC_WRITE` sobre `pipeline_execution`.
- Referencia Fury Lock validada por el usuario: commit `cf154b16e`, tag `0.0.10-listener-lock`, perteneciente a `feature/serialize-batch-completed-listener-test`.
- Advertencia crítica: el tip posterior `35848d871` de la rama de test revierte Fury Lock. No copiar la rama completa ni usar su HEAD como diseño objetivo.
- Versión esperada: `0.0.11-listener-lock`, porque `0.0.10-listener-lock` ya existe. Confirmar tags y versiones al ejecutar y usar el siguiente identificador libre sin sobrescribir ninguno.
- Evidencia obligatoria: el flujo sin exclusión debe reproducir exactamente 2 dispatches; el flujo con Fury Lock debe producir exactamente 1.

## Contrato de salida

- Rama objetivo limpia y sincronizada con origin, sin reescritura destructiva de historia.
- Un nuevo commit lógico que retire el lock MySQL del hotfix y use Fury Lock como única barrera distribuida del avance de batch.
- Suite focal y completa verdes, cobertura medida y checks del PR verificados.
- Review real con Zord, hallazgos aplicables corregidos exclusivamente por Luna y rerun final sin blockers.
- Descripción generada con Zord Author, guardada localmente y publicada en GitHub.
- Descripción final sin las expresiones `PESSIMISTIC_WRITE`, `pessimistic lock`, `MySQL row lock`, `QKVS` ni `KVS`; debe explicar Fury Lock, su identidad, retries, comportamiento y límites.
- Nueva versión Fury finalizada correctamente o blocker externo documentado sin crear versiones sucesivas para ocultar fallos.
- Cierre de Agents OS por delta con continuidad y evidencia atribuible a cada superficie/modelo.

## Prompt

```text
Actúa como ORQUESTADOR PRINCIPAL de la corrección completa del PR #1079 en rio-playmaker. No implementes código Java, Gradle, YAML ni tests directamente: toda modificación de desarrollo debe ser realizada por un único subagente Luna reutilizable. Usa Zord de manera real para code review y Zord Author para la descripción del PR. Tú inspeccionas, decides alcance, delegas, ejecutas validaciones, gestionas Git/GitHub/Fury y cierras la sesión.

OBJETIVO

Reemplazar la implementación vigente basada en PESSIMISTIC_WRITE sobre pipeline_execution por Fury Lock, conservando el comportamiento idempotente, la relectura fresca, el retry coalescido y las protecciones introducidas en el commit final f7d4f4881. El patrón de Fury Lock probado por el usuario vive en el commit exacto cf154b16e de feature/serialize-batch-completed-listener-test. El HEAD posterior 35848d871 revierte ese experimento: no lo uses como fuente objetivo.

AUTORIZACIÓN Y LÍMITES

- Estás autorizado a modificar la rama feature/serialize-batch-completed-listener, ejecutar tests/builds, crear commits, pushear, actualizar el body del PR #1079 en GitHub, actualizar su descripción local, crear la siguiente versión Fury libre y cerrar Agents OS.
- No hagas merge del PR.
- No hagas reset --hard, rebase destructivo, force-push ni borres historia. "Rollback" significa retirar lógicamente el enfoque MySQL mediante un nuevo cambio revisable.
- No cherry-pickees cf154b16e ni copies la rama de test completa: las historias divergieron y contienen artefactos KVS/MySQL anteriores. Porta únicamente el patrón Fury Lock aplicable sobre el estado final de la rama objetivo.
- Conserva cambios ajenos del worktree. Si hay modificaciones no atribuibles a esta tarea que se solapan con archivos objetivo, detente y pide decisión.
- No modifiques Swagger, ClickHouse, Flink, Kafka, segmentos KVS ni configuración ajena al batch listener.
- La dependencia java-toolkit-kvs puede seguir existiendo por otros casos de uso del proyecto; no la elimines globalmente sólo porque este hotfix deja de usarla.

ROLES OBLIGATORIOS

1. ORQUESTADOR RAÍZ
   - No edita archivos de desarrollo.
   - Resuelve contexto, prepara tareas acotadas, revisa diffs, corre comandos, decide disposition de findings, hace commit/push/release y actualiza documentación.
   - Mantiene un único plan y emite actualizaciones breves; no vuelca logs extensos en contexto.

2. LUNA — DESARROLLO
   - Usa un solo subagente Luna para toda la implementación y sus correcciones; envíale follow-ups en vez de crear agentes nuevos.
   - Luna es la única que modifica Java, Gradle, YAML y tests.
   - Cada entrega de Luna debe informar archivos cambiados, invariantes preservados, tests ejecutados y riesgos, sin pegar archivos completos.

3. ZORD — REVIEW
   - Ejecuta Zord sobre el diff real de la rama objetivo.
   - Exige revisión de concurrencia, distributed locking, TTL/lease, owner-safe release, retries, fail-closed, transacciones, I/O boundaries, idiomacy, tests conductuales y residuos del lock MySQL.
   - No simules Zord manualmente. Registra herramienta/backend/modelo real. Si Zord no puede ejecutarse después de agotar su fallback documentado, detente y reporta el blocker.

4. ZORD AUTHOR — PR
   - Genera el body desde el diff final, template del repo, tests y riesgos confirmados.
   - Usa un dossier pequeño dentro del repo sólo si Zord Author lo exige; elimínalo o muévelo fuera antes del commit.
   - Elimina cualquier título duplicado que Zord Author inserte dentro del body.

ECONOMÍA DE TOKENS

- Carga primero AGENTS OS por bootstrap y sólo la entidad [[Playmaker — Doble dispatch al avanzar batches]], este prompt, el diff de la rama objetivo y los archivos exactos del commit cf154b16e.
- No releas todo el vault ni todo el repositorio. Usa rg, git diff, git show y proyecciones por archivo.
- No pegues outputs completos de Gradle/Zord en conversación: conserva el log en archivo temporal y reporta resumen, exit code, tests y fallos relevantes.
- Corre tests focales durante iteraciones y la suite completa una sola vez al final, salvo que una corrección posterior invalide ese resultado.
- Máximo dos ciclos Zord → Luna → validación. Si persisten blockers después del segundo ciclo, no maquilles el resultado: detente con evidencia concreta.
- Paraleliza sólo verificaciones independientes. No ejecutes dos agentes editando el mismo worktree.

FASE 0 — PREFLIGHT Y FUENTES

1. Resuelve el repo y confirma:
   - branch actual y origin;
   - worktree limpio o cambios preexistentes preservados;
   - PR #1079 abierto y apuntando a feature/serialize-batch-completed-listener;
   - HEAD local/remoto y merge base efectivo del PR;
   - tags/versiones 0.0.9-listener-lock y 0.0.10-listener-lock.
2. Fetch read-only de refs si hace falta. No cambies de base ni mezcles develop sin una necesidad demostrada.
3. Inspecciona como fuentes mínimas:
   - implementación final f7d4f4881;
   - git show cf154b16e^..cf154b16e;
   - build.gradle y clases Fury Lock en el snapshot cf154b16e;
   - tests concurrentes actuales;
   - template y body vigente del PR.
4. Confirma explícitamente que cf154b16e usa:
   - com.mercadolibre:lockclient:3.0.1;
   - LockApiClient + NamespaceLockClient;
   - lock(key, ttl) que retorna Lock;
   - AlreadyLockedException como contención esperada;
   - LockClientException como indisponibilidad;
   - unlock(lock) para release.
5. No asumas semántica no observada de la librería. Luna debe inspeccionar firmas/Javadocs/decompilado local si ownership, TTL o thread-safety no están claros.

FASE 1 — DISEÑO DE DELTA PARA LUNA

Entrega a Luna una tarea acotada con estos invariantes:

A. Retirar únicamente el enfoque MySQL del hotfix
   - Eliminar PipelineExecutionRepository.lockForBatchAdvance y sus imports @Lock, QueryHint y LockModeType.
   - Eliminar BatchAdvanceDatabaseLockContendedException si queda sin usos.
   - Eliminar del listener/orchestration el camino de retry específico de lock DB.
   - No eliminar actualizaciones legítimas de status de PipelineExecution ni otros locks del proyecto.

B. Incorporar Fury Lock limpiamente
   - Agregar o conservar exactamente la dependencia lockclient compatible confirmada por la referencia probada.
   - Crear una configuración con nombre Fury Lock; no conservar nombres BatchListenerLockKvsConfig ni propiedades kvs.* para este mecanismo.
   - Namespace recomendado: rio-playmaker-batch-advance, configurable.
   - Identidad del mutex: (pipelineExecutionId, nextBatchOrder), materializada como clave estable dentro del namespace.
   - AlreadyLockedException = BUSY: no dispatch, retry acotado.
   - LockClientException/errores de transporte = UNAVAILABLE: fail closed, nunca continuar sin lock.
   - Liberar el Lock exacto devuelto por el cliente en finally. Un error de release se registra y mide sin ocultar la excepción principal.
   - Validar TTL positivo y acotado. Confirmar con la API real si existe renovación; no inventarla. Si no existe, documentar que la sección crítica debe terminar antes del lease y medir hold duration.

C. Preservar las correcciones valiosas del estado final
   - Cargar contexto con proyección escalar, sin navegar asociaciones LAZY fuera de transacción.
   - Adquirir Fury Lock antes de abrir la transacción de evaluación/materialización.
   - Tras adquirirlo, abrir REQUIRES_NEW, releer run, deployment, prerequisites y materialización desde DB fresca.
   - Mantener idempotencia por componentes ya materializados del mismo group.
   - Mantener retries coalescidos por (executionId,nextBatchOrder), presupuesto que no se reinicia, cancelación de retries obsoletos y backoff acotado.
   - Mantener fail-closed ante identidades incompletas, scheduler rejection y agotamiento de retries.
   - Mantener métricas de acquired, contended, unavailable/retry exhaustion, release failure y hold duration sin labels de alta cardinalidad.
   - No mantener una transacción ni worker bloqueado durante el backoff.

D. Mantener el cambio pequeño
   - No schema migration, nuevos estados, cambios HTTP, CPs, topics, outbox ni DLQ en este hotfix.
   - No arrastrar Swagger ni application-staging-nonprod.yml de la rama experimental salvo evidencia estricta de que Fury Lock lo requiere.
   - No agregar fallback PESSIMISTIC_WRITE ni fallback KVS. Fury Lock es la única exclusión de este hotfix.

FASE 2 — TESTS CONDUCTUALES OBLIGATORIOS, IMPLEMENTADOS POR LUNA

Los tests deben probar comportamiento observable, no estructura interna:

1. Contrafactual sin lock:
   - dos callbacks legítimos de componentes distintos del mismo batch;
   - ambos leen el mismo snapshot no materializado;
   - resultado obligatorio: exactamente 2 invocaciones/efectos de dispatch.

2. Flujo con Fury Lock:
   - dos listeners o instancias independientes comparten un fake/backend de lock común;
   - uno adquiere y materializa; el otro recibe AlreadyLockedException, reintenta, relee y termina no-op;
   - resultado obligatorio: exactamente 1 dispatch total.

3. Cobertura mínima adicional:
   - misma execution + mismo nextBatchOrder colisiona;
   - execution u order distintos no colisionan;
   - LockClientException y excepción unchecked no despachan;
   - agotamiento de retries no despacha;
   - scheduler rejection no despacha y limpia el estado coalescido;
   - callback fresco exitoso cancela retry pendiente/obsoleto;
   - unlock ocurre en éxito y excepción de negocio;
   - unlock recibe exactamente el Lock adquirido;
   - fallo de unlock no produce un segundo dispatch;
   - TTL/config inválidos fallan al iniciar;
   - materialización parcial despacha sólo faltantes;
   - identidad o asociaciones incompletas fallan cerradas.

4. Si es viable con las dependencias existentes, agregar integración representativa del wiring Spring de NamespaceLockClient. No reemplazar los dos tests conductuales obligatorios por mocks que sólo verifiquen llamadas.

FASE 3 — VALIDACIÓN LOCAL INICIAL

1. Revisa el diff producido por Luna y rechaza cambios fuera de alcance.
2. Ejecuta git diff --check.
3. Ejecuta tests focales del listener, Fury Lock, concurrencia, orchestration y métricas.
4. Si fallan por implementación, devuelve a la misma Luna sólo el diagnóstico mínimo y el output relevante.
5. No hagas commit todavía.

FASE 4 — REVIEW ZORD Y CORRECCIONES

1. Ejecuta Zord sobre el diff completo no commiteado o el rango exacto contra la base efectiva del PR.
2. Pide findings priorizados y verificables. Zord debe revisar especialmente:
   - uso idiomático/real de lockclient;
   - atomicidad de adquisición y owner-safe release;
   - expiración del lease durante dispatchBatch;
   - fail-open accidental;
   - retry storms, reset de presupuesto y stale callbacks;
   - transacción fresca después del lock;
   - I/O realizado dentro del lease;
   - residuos de PESSIMISTIC_WRITE/QKVS/KVS en este hotfix;
   - tests que sólo prueban implementación en vez de conducta;
   - configuración local, CI y runtime.
3. Clasifica cada finding como apply, defer con riesgo explícito o reject con evidencia.
4. Entrega a la misma Luna sólo los findings apply. Luna corrige; el raíz no edita código.
5. Repite tests focales y Zord una vez. No cierres con blocker/major sin resolver o aceptar explícitamente con razón y límite.

FASE 5 — SUITE FINAL Y GATES

Sobre el diff final:

1. ./gradlew test jacocoTestReport --no-daemon
2. ./gradlew check --no-daemon
3. git diff --check
4. Resume número total de tests, failures, errors, skipped y coverage global/de clases modificadas.
5. Inspecciona el diff efectivo del PR contra su base, no sólo commits intermedios.
6. Gate de términos/código:
   - no debe quedar lockForBatchAdvance;
   - no debe quedar BatchAdvanceDatabaseLockContendedException;
   - el batch listener no debe importar APIs JPA de lock pesimista;
   - no debe quedar fallback DB o KVS;
   - Fury Lock debe ser la única barrera del avance.
7. Gate conductual innegociable: sin lock = 2 dispatches; con Fury Lock = 1.

FASE 6 — COMMIT Y PUSH

1. Confirma worktree y staged diff exactos; excluye dossiers/reportes Zord y artefactos temporales.
2. Crea un único commit final, salvo que la política del repo exija separación. Mensaje sugerido:
   fix: serialize batch advancement with fury lock
3. Push no destructivo a origin/feature/serialize-batch-completed-listener.
4. Verifica HEAD local = HEAD remoto y guarda el SHA final.
5. Espera checks GitHub; si falla uno, diagnostica desde evidencia antes de tocar código.

FASE 7 — DESCRIPCIÓN CON ZORD AUTHOR

1. Genera con Zord Author un body nuevo desde el diff final y el template real del repo.
2. Debe incluir:
   - causa funcional: dos BatchCompletedEvent podían materializar dos veces el siguiente batch;
   - Fury Lock por executionId + nextBatchOrder;
   - contención con retry/backoff y relectura idempotente;
   - fail-closed y límites del lease/retries en memoria;
   - tests exactos 2 sin lock / 1 con lock;
   - suite, coverage y versión objetivo reales.
3. El body NO debe mencionar PESSIMISTIC_WRITE, MySQL row lock, QKVS ni KVS, ni siquiera como historia descartada. Valídalo con búsqueda case-insensitive antes de publicar.
4. Evita el defecto anterior de Zord Author: no repetir el título dentro del body y no conservar mecánicamente prosa obsoleta.
5. Actualiza la nota local [[Descripción PR — rio-playmaker — Hotfix doble dispatch]].
6. Publica con gh pr edit 1079 --body-file <archivo>.
7. Relee GitHub y verifica contenido, updatedAt, title, branch y SHA. No afirmes actualización sólo porque el comando devolvió exit 0.

FASE 8 — RELEASE

1. Lista tags y versiones primero. 0.0.10-listener-lock ya fue usada por la prueba; la candidata esperada es 0.0.11-listener-lock.
2. Crea la siguiente versión libre desde el SHA final con tests habilitados.
3. Espera estado terminal. Si la creación falla por un error transitorio y la herramienta soporta retry idempotente de la misma versión, permite un único retry con la misma identidad. No crees 0.0.12 para ocultar un fallo de 0.0.11.
4. Verifica tag remoto, commit de la versión y estado FINISHED.
5. No despliegues a producción ni merges el PR.

FASE 9 — CIERRE

1. Actualiza la nota canónica del proyecto por delta: approach Fury Lock, commit, tests, PR, versión y riesgos pendientes.
2. Registra agent_run separado para raíz, Luna y Zord cuando corresponda; no inventes modelos.
3. Persiste feedback sólo si hubo fricción real.
4. Reindexa Graphify sólo si cambió memoria/entity indexable; si el gate falla por deuda ajena, registra el blocker sin arreglarla fuera de alcance.
5. Cierra Agents OS.

CONDICIONES DE PARADA

- Detente y consulta sólo si aparece una elección material no resoluble por código/documentación: versión incompatible de lockclient, semántica de lease contradictoria con la prueba, cambios ajenos solapados o necesidad de ampliar el alcance.
- Si Zord encuentra un blocker real, no hagas release hasta resolverlo.
- Si el test con Fury Lock no demuestra exactamente 1 dispatch o el test sin lock no demuestra exactamente 2, el trabajo no está completo.
- Si Fury Lock queda fail-open, el trabajo no está completo.
- Si el PR body contiene cualquiera de los términos prohibidos, no lo publiques.

REPORTE FINAL

Entrega un resumen breve y comprobable con:
- SHA y sincronización de rama;
- URL/estado del PR y confirmación del body Zord Author;
- resultado Zord y correcciones Luna;
- evidencia 2 dispatches sin lock / 1 con Fury Lock;
- suite, coverage y checks;
- versión Fury y estado;
- riesgos aceptados y único próximo paso real.

Finaliza literalmente con: por favor gracias
```

## Límites

- Este prompt autoriza el cambio completo del PR y su release de prueba, pero no merge ni promoción a producción.
- El commit `cf154b16e` es una referencia de implementación probada, no una base para copiar sin revisión ni una garantía suficiente de producción.
- Fury Lock reemplaza exclusivamente la barrera del avance de batches; no se deben eliminar usos KVS legítimos de otros dominios del proyecto.
- La solución sigue siendo un hotfix con retry en memoria. Outbox, DLQ, persistencia de transición y unicidad cross-execution permanecen fuera de alcance.
