---
type: prompt
schema_version: 1
status: active
area: "[[Meli]]"
target: AI coding/research agent with repository and Git history access
prompt_version: 1
inputs:
  - Local rio-playmaker repository
  - Incident evidence and database extracts
  - Prior diagnosis project note, withheld until contrast phase
  - Optional runtime logs and current remote refs
outputs:
  - Frozen independent investigation report
  - Evidence-based contrast report
  - Alternative solution matrix
  - Recommended design with tests rollout and rollback
application: "[[rio-playmaker]]"
project: "[[Playmaker — Doble dispatch al avanzar batches]]"
aliases:
  - Prompt de investigación independiente Playmaker
  - Prompt doble dispatch
related:
  - "[[RIO]]"
  - "[[playmaker-deploy-flow]]"
tags:
  - kind/prompt
  - area/meli
  - app/rio-playmaker
created: 2026-08-21
updated: 2026-08-21
---

# Prompt maestro — Auditoría independiente del doble dispatch

## Propósito

Investigar desde fuentes primarias un incidente de concurrencia y consistencia en el avance de batches de `rio-playmaker`, construir hipótesis y alternativas sin quedar anclado por un diagnóstico previo, y sólo después contrastar los resultados con la evidencia y propuestas ya documentadas.

El mecanismo anti-sesgo principal no es una declaración de “sé objetivo”: es una **barrera secuencial verificable**. La IA debe congelar un reporte independiente antes de abrir la nota de contraste.

## Contrato de entrada

- `REPO_PATH`: ruta local del repositorio `rio-playmaker`. Default: `/Users/rjara/fuentes/rio-playmaker`.
- `INCIDENT_EVIDENCE`: datos entregados en el prompt o archivos externos de logs/DB. Puede estar incompleto.
- `CONTRAST_NOTE`: diagnóstico previo que no debe abrirse durante la fase independiente. Default: `/Users/rjara/obsidian/SecondBrain/main/10-projects/Meli/Playmaker — Doble dispatch al avanzar batches/Playmaker — Doble dispatch al avanzar batches.md`.
- `PHASE1_REPORT`: archivo fuera del repo donde congelar la investigación independiente. Default sugerido: `/tmp/playmaker-double-dispatch-phase1.md`.
- Acceso opcional a logs, DB y refs remotas. No asumir que están disponibles; declarar limitaciones.

## Contrato de salida

Entregar un reporte autosuficiente que contenga:

1. Diagnóstico independiente congelado y su checksum o evidencia equivalente de que precede al contraste.
2. Reconstrucción del lifecycle y de las transacciones con referencias `file:line` y commits.
3. Hipótesis alternativas, evidencia a favor/en contra, falsadores y confianza.
4. Contraste explícito contra `CONTRAST_NOTE`: coincidencias, desacuerdos, omisiones y correcciones.
5. Matriz de soluciones descubiertas por la investigación, sin favorecer por defecto el menor diff ni un patrón conocido.
6. Recomendación final justificada, incluyendo invariantes, pseudocódigo/transacciones, schema si aplica, failure/retry/crash recovery, observabilidad, pruebas, migración, rollout y rollback.
7. Preguntas abiertas y evidencia adicional requerida.

## Prompt

```text
Actúa como principal engineer especializado en sistemas distribuidos, concurrencia transaccional, Spring/JPA y diseño de workflows asíncronos. Debes investigar un incidente real en rio-playmaker y proponer una solución de arquitectura. No debes implementar ni modificar código de producto: esta tarea es de investigación y diseño.

Tu obligación principal es evitar sesgo de anclaje. Existe un diagnóstico previo, pero está prohibido abrirlo hasta congelar tu propio análisis desde fuentes primarias.

VARIABLES

REPO_PATH=/Users/rjara/fuentes/rio-playmaker
CONTRAST_NOTE=/Users/rjara/obsidian/SecondBrain/main/10-projects/Meli/Playmaker — Doble dispatch al avanzar batches/Playmaker — Doble dispatch al avanzar batches.md
PHASE1_REPORT=/tmp/playmaker-double-dispatch-phase1.md

Si una ruta no existe, localízala o informa el bloqueo. No sustituyas evidencia faltante con suposiciones silenciosas.

INCIDENTE MÍNIMO CONOCIDO

- Una operación posterior sobre un componente flink-sql falla en PipelineServiceImpl.batchBuildStateResultMap con `IllegalStateException: Duplicate key 5120`.
- La DB contiene dos Deployment activos para `service_id=5120`, mismo component/config, mismo `deployment_group_id`, mismo `pipeline_execution_id`, mismo desired-state hash y mismo segundo de creación; tienen correlation IDs distintos.
- El control plane reportó `Application already exists` para KinesisAnalyticsV2.
- En la execution había dos componentes de run_order 0 que terminaron casi simultáneamente y dos componentes de run_order 1, uno de los cuales era flink-sql.
- Los deployments históricos múltiples pueden ser legítimos. Lo que debes determinar es la cardinalidad e invariantes reales, el origen de estas filas concretas y cómo evitar recurrencia.

REGLAS DE EVIDENCIA Y SEGURIDAD

1. Lee y respeta todos los AGENTS.md aplicables antes de investigar.
2. Trabaja read-only sobre el repo. No cambies código, schema, tests, datos, branches ni refs. No hagas fetch/pull sin autorización explícita.
3. Registra branch, HEAD, fecha de refs y dirty state. Preserva cambios ajenos.
4. Prioridad de evidencia: código/schema/tests y datos runtime > historial git/commit diff > backlog/docs > diagnóstico previo.
5. Mensajes de commits, comentarios y backlog son pistas, no prueba de que el comportamiento descrito siga vigente.
6. Para cada afirmación importante, clasifícala como OBSERVADO, INFERIDO o HIPÓTESIS y cita `file:line`, commit o dato concreto.
7. Busca activamente evidencia que falsaría tu hipótesis favorita. No cierres la investigación al encontrar la primera explicación plausible.
8. No asumas que el bug debe resolverse con locks, estados nuevos, constraints, idempotency keys ni ninguna técnica particular. Descubre opciones desde los invariantes y failure modes.
9. No optimices por tamaño del diff. Compara corrección, operabilidad, costo y riesgo con criterios explícitos.
10. Distingue siempre: causa raíz, trigger, amplificador, síntoma de lectura, corrupción persistida y reparación de datos existentes.

PROTOCOLO ANTI-ANCLAJE OBLIGATORIO

FASE 1 — INVESTIGACIÓN INDEPENDIENTE

No abras, busques dentro, resumas ni permitas que otro agente lea CONTRAST_NOTE. Tampoco uses notas que reproduzcan ese diagnóstico como autoridad. Puedes leer documentación general del sistema si la encuentras naturalmente, pero debes basarte en código y evidencia.

A. Reconstruye el modelo:

- PipelineExecution, DeploymentGroup, ComponentRun, Deployment, Service y ComponentDefinition.
- Cardinalidades, lifecycle, estados, `is_active`, retries y redeploys.
- Constraints e índices reales en migrations/schema.
- Qué identidad lógica representa un intento y cuál representa el estado vigente.

B. Traza end-to-end al menos estos caminos:

- creación inicial del pipeline deployment;
- dispatch del primer batch;
- consumo de STARTED/COMPLETED/FAILED;
- decisión de avanzar al siguiente batch;
- creación de Deployment y publicación hacia el control plane;
- actualización de ComponentRun/group/execution;
- redeploy posterior;
- lectura que construye el estado del pipeline.

Para cada paso documenta:

- método/clase;
- transaction boundary y propagation;
- sync/async y executor;
- estado leído y escrito;
- locks/constraints/guards;
- qué ocurre ante dos invocaciones concurrentes;
- qué ocurre ante redelivery at-least-once;
- qué ocurre ante crash antes y después del commit.

C. Enumera hipótesis sin limitarte a las siguientes categorías:

- dos requests de deploy;
- dos eventos legítimos del mismo batch;
- redelivery duplicado del mismo resultado;
- retry interno;
- duplicación del plan/run;
- carrera check-then-act;
- stale/replica reads;
- comportamiento del control plane;
- callbacks fuera de orden;
- paths legacy y moderno actuando sobre el mismo service.

Para cada hipótesis entrega evidencia a favor, evidencia en contra, dato que la falsaría y confianza.

D. Inspecciona historial git de las clases relevantes:

- identifica cuándo apareció el comportamiento;
- compara la versión anterior y actual;
- busca fixes o tests concurrentes en todas las refs locales;
- no concluyas por el nombre de una branch o commit.

E. Evalúa tests existentes:

- qué concurrencia reproducen realmente;
- qué dobles/mocks esconden transacciones reales;
- qué escenario falta para reproducir el incidente determinísticamente.

F. Descubre alternativas de solución por tu cuenta. No leas aún las propuestas previas. Para cada alternativa define:

- invariante que protege;
- unidad de exclusión o identidad;
- transaction boundary exacto;
- conducta idempotente;
- crash/retry/recovery;
- compatibilidad con deployments históricos y redeploys;
- impacto en schema/API/consumidores;
- observabilidad;
- pruebas necesarias;
- rollout/rollback;
- riesgos y casos no cubiertos.

G. Congela el resultado:

- Escribe PHASE1_REPORT fuera del repo.
- Incluye timestamp, branch, HEAD, fuentes leídas, hipótesis, opciones y recomendación independiente.
- Calcula y conserva un SHA-256 del archivo, o un mecanismo equivalente que demuestre que no fue modificado durante la fase de contraste.
- Después de congelarlo no edites ese reporte. Si descubres una corrección en fase 2, regístrala como addendum separado.

Si no puedes persistir un checkpoint verificable, detente al finalizar fase 1 y pide al usuario `CONTINUAR CON CONTRASTE`. No simules independencia dentro de un único texto después de haber leído el diagnóstico previo.

FASE 2 — CONTRASTE

Sólo después de congelar fase 1 puedes abrir CONTRAST_NOTE.

1. Trátala como una revisión externa potencialmente equivocada.
2. Extrae por separado:
   - hechos/datos;
   - inferencias;
   - hipótesis;
   - propuestas;
   - trabajo pendiente e historial mencionado.
3. Contrástala punto a punto con PHASE1_REPORT.
4. Para cada diferencia, vuelve a la fuente primaria antes de decidir.
5. Identifica:
   - coincidencias independientes;
   - evidencia que el diagnóstico previo vio y tú no;
   - evidencia que tú encontraste y el diagnóstico previo omitió;
   - afirmaciones previas refutadas o demasiado fuertes;
   - soluciones previas que no cubren todos los failure modes;
   - cambios en tu recomendación y causa exacta del cambio.
6. No modifiques PHASE1_REPORT; escribe un addendum de contraste.

FASE 3 — SÍNTESIS Y PROPUESTA FINAL

Deriva los invariantes antes de elegir mecanismos. Como mínimo decide explícitamente:

- si el avance del batch debe tener efecto exactamente una vez o efecto idempotente bajo at-least-once;
- identidad lógica de un dispatch/attempt/retry;
- cardinalidad permitida de Deployment por component, service, group y execution;
- significado exacto de `is_active`;
- política de redeploy e historial;
- comportamiento ante dos executions concurrentes para el mismo service;
- recuperación de estados/claims pegados;
- autoridad final: aplicación, DB o ambas.

Construye una matriz comparativa de todas las alternativas descubiertas. Usa al menos estos criterios, sin asumir su peso:

- corrección intra-execution;
- corrección cross-execution;
- redelivery y orden de eventos;
- atomicidad cuando no existe fila previa;
- crash consistency;
- retries legítimos;
- impacto de schema/migration;
- impacto de API/estado público;
- contención/deadlocks;
- observabilidad;
- testabilidad;
- complejidad operativa;
- rollout y reversibilidad.

Tu recomendación puede ser una composición de mecanismos, pero separa:

1. fix de la causa funcional;
2. backstop de integridad en DB;
3. hardening de lectores/observabilidad;
4. reparación de datos ya corruptos.

Para el diseño recomendado entrega:

- diagrama o secuencia before/after;
- pseudocódigo de la sección transaccional;
- queries/constraints conceptuales, si aplican;
- transiciones de estado;
- conducta ante duplicate, retry y crash;
- cómo evitar que un intento válido termine FAILED por una segunda invocación idempotente;
- plan de pruebas determinista;
- migración y preflight sobre datos existentes;
- rollout por etapas, métricas y alarmas;
- rollback;
- riesgos residuales.

FORMATO FINAL

1. Resumen ejecutivo.
2. Alcance, snapshot y limitaciones.
3. Diagnóstico independiente congelado (referencia + SHA-256).
4. Modelo de dominio e invariantes observados.
5. Timeline y transaction map.
6. Hipótesis con evidencia/falsadores/confianza.
7. Causa raíz, trigger, síntomas y daños persistidos.
8. Contraste con diagnóstico previo.
9. Matriz de alternativas.
10. Recomendación final.
11. Diseño transaccional y de datos.
12. Tests de concurrencia y failure injection.
13. Migración, rollout, observabilidad y rollback.
14. Preguntas abiertas y evidencia faltante.
15. Apéndice de referencias `file:line`, commits y comandos read-only ejecutados.

No entregues frases genéricas como “agregar locking” o “hacerlo idempotente”. Toda propuesta debe decir qué fila/clave se protege, en qué transacción, qué gana la carrera, qué observa el perdedor y cómo se recupera un crash.
```

## Límites

- El prompt no autoriza cambios en código, DB, branches, refs ni servicios externos.
- La independencia real requiere que `CONTRAST_NOTE` permanezca sin abrir hasta congelar fase 1.
- El archivo de fase 1 debe vivir fuera del repo para no ensuciar el worktree.
- Una recomendación no se considera validada sin prueba concurrente determinística y revisión de semántica de retries.
- Las refs locales pueden estar desactualizadas; cualquier conclusión sobre “no existe un fix” debe declarar la fecha de actualización o verificarse con autorización.
