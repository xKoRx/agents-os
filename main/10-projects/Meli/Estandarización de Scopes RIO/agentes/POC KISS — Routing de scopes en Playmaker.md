---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[Estandarización de Scopes RIO]]"
sprint:
start: 2026-09-16
due:
progress: 5
repo: https://github.com/melisource/fury_rio-playmaker
jira: SIG-599
prs:
aliases:
  - POC Playmaker scope alpha
  - Routing KISS de scopes en rio-playmaker
tags:
  - kind/project
  - area/meli
  - project/scopes-rio
  - tech/rio-playmaker
created: "2026-09-16"
updated: "2026-09-17"
---

# POC KISS — Routing de scopes en Playmaker

> [!danger] REGLA BÁSICA — LEER ANTES DE TOCAR ESTE PROYECTO
> **EL `ENVIRONMENT` DEL PIPELINE NO ES LO MISMO QUE EL SCOPE DE FURY.** Este proyecto alinea scopes de infraestructura Fury. El `Environment` del pipeline es dominio de negocio existente y queda completamente fuera. El scope Fury llega desde el frontend en `X-Rio-Scope`, hoy Playmaker no lo usa, y esta POC comienza a usarlo exclusivamente para publicar `scope:<valor>` como filtro BigQueue. Está prohibido persistirlo en `PipelineExecution`, usarlo en idempotencia/history, compararlo con el pipeline environment o crear un campo llamado `environment_scope`.

> [!info]+ Estado ejecutivo
> **Ready phase:** Fase 0 · **Gate actual:** G0 `pending` · **Base local verificada:** `origin/master@f350fb26091d` · **Principio KISS:** header transitorio → filtro BigQueue; cero DB, cero SDK DTO, cero cambios al dominio del pipeline.

## 🎯 Objetivo

Implementar y certificar en `rio-playmaker` la POC mínima de SIG-599: capturar `X-Rio-Scope: alpha`, propagarlo por el command/dispatch in-memory y publicar el trigger existente con `filters.modified_fields=["scope:alpha"]`. El control plane preserva el filtro al publicar el result y Playmaker conserva el filtro del envelope durante esa request. El proyecto debe poder ser revisado y ejecutado por agentes fase a fase sin reabrir la separación conceptual ni ampliar alcance.

## 📊 Estado actual

- Planner y [[SPEC técnica — Routing KISS por scope en rio-playmaker]] corregidos el 2026-09-17 después de detectar una mezcla inválida entre pipeline environment y Fury scope.
- Playmaker hoy recibe todos los headers en `PipelineDeploymentController`, pero `X-Rio-Scope` no tiene uso funcional.
- El producer actual llama `producer.send(message)`; mqclient `3.4.9` ya ofrece `producer.send(message, Filters)`.
- El SDK ya modela `BigQueueMessage.filters`/`modified_fields`; no necesita cambios.
- El flow `AFTER_COMMIT` ya usa `DispatchRequest` como carrier in-memory; éste es el seam para la POC.
- No hay y no habrá cambios en `PipelineExecution`, `EnvironmentModel`, DB, migrations, idempotencia, history o payload DTOs.
- Baseline local de `rio-playmaker`: `origin/master@f350fb26091d`, tag `202609.16.0`; F0 debe refrescarla con GlobalProtect sin tocar untracked ajenos del checkout.
- Estado planner: `ready_for_phase_0`. La incertidumbre sobre filtrado server-side de Fury es un spike con stop condition, no una excusa para persistir scope.

## Resumen ejecutivo y trabajo restante

El cambio útil es pequeño: leer un header que hoy se ignora, validar su sintaxis, transportarlo hasta el producer y usarlo como tag de filtro. En el result path se deja de descartar el bloque `filters` para poder continuar el valor durante esa request. La compatibilidad es natural: sin header/filtro, el comportamiento legacy se mantiene.

La POC certifica un golden deploy de un batch. Retry, timeout, restart y reanudación sin request activa quedan fuera porque preservar un dato transitorio en esos escenarios requeriría una decisión durable separada. Ningún agente puede “resolver” esa limitación alterando entidades del pipeline.

## Matriz requisito → evidencia

| ID | Requisito | Estado | Evidencia | Trabajo restante |
|---|---|---|---|---|
| R1 | Separar pipeline environment de Fury scope | `replaced` | Corrección explícita del owner 2026-09-17 | Proteger con regla, no-touch y tests |
| R2 | Capturar `X-Rio-Scope` | `partial` | `HEAD` `PipelineDeploymentController.deployPipeline` ya recibe headers en `rio-playmaker@f350fb26091d:src/main/java/com/mercadolibre/rio/playmaker/controller/PipelineDeploymentController.java:L97` | Extraer y validar el header |
| R3 | Transportar el scope sin persistir | `partial` | `HEAD` `DispatchRequest` es carrier inmutable a través de `AFTER_COMMIT` | Propagar argumento/value object hasta el request |
| R4 | Publicar `scope:alpha` | `partial` | `CONTRACT` mqclient 3.4.9 ofrece `Producer.send(message, Filters)` | Usar overload filtrado con header presente |
| R5 | Mantener SDK/payload intactos | `done` | `CONTRACT` `rio-sdk-events@3e3acd1` ya modela filtros | No modificar SDK ni payload |
| R6 | Conservar filtro en result request | `partial` | `HEAD` controller recibe envelope pero descarta `filters` | Pasar routing scope al consumer/orchestration |
| R7 | Compatibilidad legacy | `partial` | `HEAD` publish/consume sin filtros funciona hoy | Header/filtro ausente conserva flujo actual |
| R8 | Fury filtra server-side | `blocked` | Requisito SIG-599 sin evidencia runtime adjunta | F0 obtiene evidencia o bloquea G0 |
| R9 | Retry/restart scoped | `replaced` | Decisión KISS: fuera de la POC | Documentar limitación; no implementar |

## Alcance, no alcance y decisiones

### Alcance

- Endpoint de pipeline deploy sólo para capturar/propagar `X-Rio-Scope`.
- Carrier in-memory hasta `DispatchRequest` y producer BigQueue.
- `scope:<x>` en `rio-deployment-trigger` usando filtros existentes.
- Conservación/parsing del filtro en `rio-deployment-result` durante esa request.
- Golden deploy alpha de un batch, compatibilidad legacy, observabilidad bounded y rollback por ausencia de header.

### No alcance

- Pipeline environment, `PipelineExecution`, `EnvironmentModel`, repositories, idempotencia, history/detail/logs, DB y migrations.
- Campos nuevos en entidades o payloads, especialmente `environment_scope` o equivalentes.
- Retry, timeout, restart, multi-batch desacoplado o carrier durable.
- Cambios/release en `rio-sdk-events`, topics nuevos, Actions, inactivation, `DataProductChanged`, Materializer o producción.
- Código de Flink o infraestructura Fury dentro de este repo.

### Registro de decisiones

| ID | Estado | Resolución | Fuente/evidencia | Fase que consume |
|---|---|---|---|---|
| D1 | `CONFIRMED` | Pipeline environment ≠ Fury scope; el primero no cambia ni valida al segundo | Corrección de Rodrigo 2026-09-17 | F0–F3 |
| D2 | `CONFIRMED` | Scope Fury entra por `X-Rio-Scope` y sólo se usa para construir `scope:<valor>` | Corrección de Rodrigo 2026-09-17 | F1–F3 |
| D3 | `CONFIRMED` | No persistir scope Fury en `PipelineExecution` ni otra entidad durante la POC | Corrección de Rodrigo + KISS | F0–F3 |
| D4 | `TECHNICAL_RESOLUTION` | Propagar por parámetros/value object/`DispatchRequest`, nunca `ThreadLocal` o JPA | Boundary async existente | F1–F2 |
| D5 | `TECHNICAL_RESOLUTION` | Sin header se usa publish legacy; no hace falta feature flag | Compatibilidad KISS | F1–F3 |
| D6 | `TECHNICAL_RESOLUTION` | Usar mqclient `Producer.send(message, Filters)`; SDK y payload intactos | Contratos existentes | F1 |
| D7 | `TECHNICAL_RESOLUTION` | Result conserva el filtro sólo durante la request y malformed se ACKea sin handler | Envelope SDK existente | F2 |
| D8 | `CONFIRMED` | Retry/restart durable queda fuera; cualquier persistencia futura exige nueva decisión | Corrección POC KISS | F0–F3 |
| D9 | `TECHNICAL_RESOLUTION` | Branch `feature/sig-599-playmaker-scope-filter-poc` desde `origin/master` revalidado después de G0 | Aislamiento de cambios | F1 |

## Arquitectura actual y objetivo

### Actual

```text
headers HTTP ─► deploy flow ─► DispatchRequest ─► producer.send(payload)
result envelope ─► controller descarta filters ─► consumer/handler

Pipeline Environment: dominio existente
Scope Fury del front: no usado por Playmaker
```

### Objetivo

```text
X-Rio-Scope ─► parse sintáctico ─► routingScope in-memory ─► DispatchRequest
                                                           │
                                                           ▼
                                             send(payload, scope filter)

result envelope.filters ─► parse routingScope ─► consumer/orchestration de esa request

Pipeline Environment / PipelineExecution / DB / idempotencia / history: SIN CAMBIOS
```

## Secuencia de datos y control

1. El frontend envía `X-Rio-Scope: alpha`; Fury Route usa el header para dirigir la request.
2. Playmaker extrae el mismo header, normaliza/valida sintaxis y crea un routing scope transitorio.
3. El deploy flow mantiene intacto el pipeline environment y pasa el routing scope como metadata hasta `DeploymentGroupService`/batch dispatch.
4. `DispatchRequest` cruza `AFTER_COMMIT` con `routingScope=alpha`.
5. El producer publica el payload actual con `Filters(["scope:alpha"])`.
6. Flink alpha recibe el trigger y publica el result con el mismo filtro.
7. Playmaker conserva `envelope.filters`, valida estructura y pasa el routing scope durante esa request.
8. El golden path termina; retry/restart no forma parte de esta POC.

## Contratos y edge cases

La autoridad completa es [[SPEC técnica — Routing KISS por scope en rio-playmaker]]. Contratos congelados:

- HTTP: `X-Rio-Scope`; regex `^[a-z0-9][a-z0-9-]{0,62}$`; malformed `400`; ausente = legacy.
- Carrier: nullable/optional sólo en memoria; no JPA, no DB, no global context.
- Envelope: `filters.modified_fields` contiene exactamente `scope:<header>` para el path filtered.
- Producer: header presente usa overload con `Filters`; ausente usa overload actual.
- Result: filtro válido se conserva; malformed se ACKea sin handler; ausente conserva legacy.
- Dominio: `envName`, `EnvironmentModel`, `environmentId`, delta, hash, idempotencia y history nunca leen routing scope.
- Seguridad: no loguear mapa de headers ni valor malformed crudo; no usar el valor dinámico como metric tag.
- Edge operativo: un restart/retry pierde el scope transitorio; es limitación declarada, no bug oculto de esta POC.

## Roadmap dependency-ordered

| Fase | Resultado | Carga relativa | Gate |
|---|---|---|---|
| F0 | Revisión independiente de separación/KISS, base fresca y filtro Fury verificado | Media por incertidumbre externa, cero código | G0 |
| F1 | Header → carrier in-memory → trigger filter, con legacy intacto | Media por boundary async | G1 |
| F2 | Result envelope conserva filtro y continuidad dentro de la request | Media por consumer/orchestration | G2 |
| F3 | E2E alpha de un batch, negativos y rollback | Media por múltiples sistemas | G3 |

## Mapa de archivos y símbolos

| Acción | Superficie | Fase |
|---|---|---|
| `create` opcional | `RoutingScope`/helper y tests | F1 |
| `modify` | `PipelineDeploymentController`, `PipelineDeployService`/impl y services/factories intermedios sólo para pasar metadata | F1 |
| `modify` | `DispatchRequest`, `DispatchRequestFactory`, `BigQueueDispatchAdapter`, `DeploymentTriggerProducer`/impl | F1 |
| `modify` | `DeploymentResultConsumerController`, consumer contract/impl y orquestación inmediata si corresponde | F2 |
| `no-touch` | Models JPA, repositories, migrations, idempotencia, history, pipeline environment | Todas |
| `no-touch` | `rio-sdk-events`, DTOs, topics, segment ID, timeout job y otros eventos | Todas |
| `no-touch` | Untracked del checkout existente | Todas |

## Estrategia de validación

- Unit: header syntax, `scope:<x>` exacto, parsing de result y malformed guard.
- Contract: payload SDK byte-compatible y filtro sólo en envelope.
- Workflow: valor cruza controller→service→batch→`DispatchRequest`→producer sin persistencia.
- Legacy: sin header/filtro usa paths actuales.
- No-regression: ninguna migration, query, model ni test de pipeline environment/idempotencia/history cambia.
- E2E: header alpha → trigger alpha → result alpha → finalización de un batch; Fury demuestra filtering server-side.
- Calidad: tests críticos primero, checks del repo y ≥95% de cobertura sobre código nuevo.

## Compatibilidad, observabilidad, rollout y rollback

- Compatibilidad por ausencia: header/filtro ausente conserva comportamiento actual.
- Métricas bounded: `routing_mode:legacy|filtered`, `invalid_header`, `malformed_filter`; nunca tag con scope dinámico.
- Rollout: código compatible → Flink preserva filtro → frontend empieza a emitir header → golden deploy alpha.
- Rollback: frontend deja de emitir header; Playmaker vuelve naturalmente al overload legacy. No hay schema, backfill, config flag ni estado persistido que revertir.
- Release: ninguna promoción productiva desde feature branch.

## Riesgos, supuestos y controles humanos

| Riesgo/supuesto | Mitigación | Control humano |
|---|---|---|
| Agente vuelve a confundir Environment con scope Fury | Regla inicial, no-touch, tests y stop behavior | Rechazar gate |
| Ref local stale | F0 refresca sin tocar worktree ajeno | Rodrigo acepta G0 |
| Fury no filtra server-side | `PLAN_CONFLICT`; no compensar con DB/app guard inventado | Rodrigo/Fury decide |
| El carrier no llega a `DispatchRequest` sin tocar dominio | `PLAN_CONFLICT`; revisar seam, no persistir | Rodrigo acepta cambio de diseño |
| Result flow pierde filtro antes de siguiente publish | Acotar golden path a un batch o mantenerlo en parámetros de la misma request | Reviewer valida G2 |
| Retry/restart pierde scope | Limitación explícita; fuera de POC | Nueva decisión futura |
| Scope creep a SDK/topics/events | No-touch + review KISS | Rechazar gate |

## Definition of Done

- G0–G3 `accepted` por el owner; ningún agente acepta su gate.
- Regla `Pipeline Environment ≠ Fury Scope` visible en proyecto, SPEC y tests/no-touch.
- `X-Rio-Scope: alpha` produce exactamente `scope:alpha` en el trigger.
- Result conserva `scope:alpha` y Fury demuestra filtro server-side.
- Pipeline domain, DB, migrations, idempotencia, history y SDK permanecen sin cambios.
- Legacy sin header/filtro sigue funcionando.
- Retry/restart queda explícitamente fuera, sin persistencia encubierta.
- Checks, cobertura ≥95%, E2E y rollback quedan enlazados.

## Control de gates

| Gate | current state | phase agent responsibility | owner acceptance evidence | enables |
|---|---|---|---|---|
| G0 | `pending` | Dejar revisión en `review`, adjuntar SHA fresco y evidencia Fury o marcar `blocked` | Rodrigo confirma separación, KISS y capability | F1 |
| G1 | `pending` | Dejar header/carrier/producer/tests en `review` | Diff sin JPA/DB/SDK y filtro exacto | F2 |
| G2 | `pending` | Dejar result parsing/continuidad/tests en `review` | Envelope conservado, malformed seguro, legacy intacto | F3 |
| G3 | `pending` | Dejar E2E/rollback/evidencia en `review` | Golden batch, negativos y rollback aceptados | cierre |

## Paquetes autónomos

### Paquete autónomo Fase 0 — Revisión independiente de separación y KISS

**Misión exacta**

Revisar como agente independiente que la solución sólo transforma header Fury en filtro BigQueue, refrescar la base y verificar las capabilities externas sin escribir código.

**Precondiciones verificables**

- Ninguna; fase inicial.
- GlobalProtect para refrescar refs/consultar Fury; sin él, la revisión local avanza pero G0 queda `blocked`.

**Lectura obligatoria**

- `VAULT_ROOT/10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing KISS por scope en rio-playmaker.md` completo.
- `VAULT_ROOT/30-resources/rio-atlas/architecture/scope-naming-standard.md`, US-12 y E2E-6.
- `rio-playmaker/AGENTS.md`, controller/deploy/dispatch/result files citados y tests.
- SDK: `BigQueueMessage`, `BigQueueFilters`, payload DTOs; mqclient `Producer`/`Filters`.

**Decisiones cerradas**

- Pipeline environment no participa.
- No DB/JPA/migrations/idempotencia/history/SDK/retry.
- Si algo parece requerir persistencia, se detiene con `PLAN_CONFLICT`.

**Implementación paso a paso**

1. Refrescar `origin/master`, registrar SHA/tag y comparar símbolos sin tocar el checkout sucio.
2. Confirmar firmas mqclient/SDK.
3. Trazar el camino mínimo controller→deploy→group/batch→`DispatchRequest`→producer y confirmar que admite metadata in-memory.
4. Confirmar que Fury preserva el header, no cruza a prod y filtra `modified_fields` server-side.
5. Confirmar que Flink puede copiar el filtro al result usando el envelope existente.
6. Auditar que SPEC/planner no contienen persistencia, pipeline matching o scope creep.
7. Actualizar evidencia y dejar G0 `review`, `blocked` o `rejected`, nunca `accepted`.

**Archivos esperados**

- `modify`: planner/SPEC sólo si la evidencia contradice referencias.
- Código/config/infra: ninguno.

**No tocar**

- Cualquier repositorio, JPA/DB, infraestructura y untracked del usuario.

**Spikes permitidos**

- Read-only: fetch, `git show`, `javap`, inspección de route/binding y prueba no mutante. Stop ante deploy/publicación real.

**Tests y asserts**

- Los símbolos/firmas persisten en la base fresca.
- El plan requiere cero cambios de pipeline domain/DB/SDK.
- Existe evidencia de header route + filtering server-side + continuidad Flink.

**Entregables/Gate G0**

- Review independiente, baseline fresco, mapa del carrier y evidencia Fury/Flink. G0 queda `review`.

**Handoff a Fase 1**

- Agente recibe G0 `accepted`, base/branch y path exacto de propagación sin redescubrir dominio.

### Paquete autónomo Fase 1 — Header a filtro del trigger

**Misión exacta**

Capturar `X-Rio-Scope`, validarlo sintácticamente, propagarlo sólo en memoria hasta `DispatchRequest` y publicar `scope:<x>` con mqclient existente.

**Precondiciones verificables**

- G0 `accepted`.
- Branch `feature/sig-599-playmaker-scope-filter-poc` desde la base aceptada; untracked ajenos intactos.

**Lectura obligatoria**

- `VAULT_ROOT/10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing KISS por scope en rio-playmaker.md`, contratos HTTP/BigQueue, propagación y no-touch.
- Controller, deploy interface/impl, group/batch services, `DispatchRequest`/factory, adapter, producer y tests de la base aceptada.

**Decisiones cerradas**

- Header ausente = legacy; malformed = 400.
- Valor no se compara con `envName`, `EnvironmentModel` ni runtime/pipeline data.
- Carrier in-memory; payload y DB intactos.

**Implementación paso a paso**

1. Escribir tests de header, propagación, filtered publish y legacy.
2. Crear helper/value object mínimo para normalización/tag si reduce duplicación real.
3. Extraer header en controller y agregar argumento opcional al deploy flow.
4. Propagarlo por group/batch/factory sin usarlo en decisiones de dominio.
5. Agregar `routingScope` opcional a `DispatchRequest`.
6. Cambiar producer para usar `send(message, Filters)` con scope y `send(message)` sin scope.
7. Probar payload intacto y ausencia total de cambios JPA/DB/SDK.
8. Ejecutar checks y dejar G1 `review`.

**Archivos esperados**

- `create` opcional: helper/value object + tests.
- `modify`: controller, deploy/group/batch contracts mínimos, carrier/factory, adapter, producer y tests.

**No tocar**

- Models, repositories, migrations, history, idempotencia, `ScopeUtils` de profiles, SDK, timeout job, otros producers y untracked ajenos.

**Spikes permitidos**

- Inspección puntual del menor set de firmas intermedias. Si exige entidad persistida, `PLAN_CONFLICT`.

**Tests y asserts**

- `alpha` genera exactamente `Filters(["scope:alpha"])`.
- Ausente conserva `send(message)`; malformed no despliega.
- `DispatchRequest` transporta el valor tras `AFTER_COMMIT`.
- Ningún payload/campo/query/migration cambia; ≥95% de cobertura nueva.

**Entregables/Gate G1**

- Diff acotado, tests y fixture del envelope. G1 queda `review`.

**Handoff a Fase 2**

- Agente recibe G1 `accepted` y contrato exacto del trigger/filter; no toca el producer salvo bug que reabra G1.

### Paquete autónomo Fase 2 — Conservar filtro del result

**Misión exacta**

Dejar de descartar `envelope.filters`, validar su estructura y mantener el routing scope disponible durante la request del result sin consultar ni alterar entidades del pipeline.

**Precondiciones verificables**

- G1 `accepted`.

**Lectura obligatoria**

- `VAULT_ROOT/10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing KISS por scope en rio-playmaker.md`, consumo, límite POC y errores.
- `DeploymentResultConsumerController`, consumer interface/impl, orchestration inmediata y tests.

**Decisiones cerradas**

- Filtro válido: exactamente un `scope:` con sintaxis válida.
- Filtro ausente: legacy actual.
- Malformed: ACK 200, reason bounded, no handler.
- No correlación/validación contra `PipelineExecution` o `EnvironmentModel`.

**Implementación paso a paso**

1. Escribir tests para valid/legacy/malformed.
2. Cambiar consumer contract para recibir envelope o routing scope parseado sin perder `msg`.
3. Reutilizar el parser de F1; no crear segunda semántica.
4. Pasar scope sólo a cualquier siguiente publish que ocurra dentro de la misma request y sea parte del golden path.
5. Mantener handlers de dominio intactos.
6. Agregar reason bounded sin tag dinámico.
7. Ejecutar checks y dejar G2 `review`.

**Archivos esperados**

- `modify`: result controller, consumer interface/impl, caller inmediato si necesita continuidad y tests.
- `conditional`: métrica existente para reason bounded.

**No tocar**

- JPA/DB/repositories/history/idempotencia, handlers de negocio, SDK, Flink, timeout job, producer de F1 y untracked ajenos.

**Spikes permitidos**

- Inspección del siguiente publish sincrónico. Si ocurre fuera de la request o requiere persistencia, acotar E2E a un batch y registrar limitación; no ampliar diseño.

**Tests y asserts**

- `scope:alpha` válido llega al consumer/orchestration sin tocar dominio.
- Ausente mantiene legacy.
- Multiple/malformed scope tags retornan 200, no llaman handler y emiten reason bounded.
- No query/model/migration cambia; ≥95% de cobertura nueva.

**Entregables/Gate G2**

- Diff, tests de envelope y evidencia de no-domain-change. G2 queda `review`.

**Handoff a Fase 3**

- Agente recibe G2 `accepted`, build candidato y matriz local; sólo resta E2E de un batch.

### Paquete autónomo Fase 3 — Certificación alpha de un batch

**Misión exacta**

Certificar el golden path alpha, negativos y rollback por ausencia de header sin habilitar persistencia, retries ni producción.

**Precondiciones verificables**

- G2 `accepted`.
- Fury Route/filter y Flink alpha listos según sus SPECs.
- Candidate generado por proceso autorizado.

**Lectura obligatoria**

- `VAULT_ROOT/10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing KISS por scope en rio-playmaker.md`, rollout, DoD y limitación POC.
- Evidencia G0–G2 y SPECs frontend/Flink/Fury aprobadas.

**Decisiones cerradas**

- Un solo batch; no provocar ni certificar retry/restart.
- Sólo alpha/nonprod; no topics nuevos ni producción.
- Rollback = dejar de enviar header y verificar legacy.

**Implementación paso a paso**

1. Desplegar candidate compatible y ejecutar smoke sin header.
2. Confirmar route/header, consumer filter server-side y Flink echo del filtro.
3. Ejecutar golden deploy con `X-Rio-Scope: alpha` y capturar filtros trigger/result.
4. Ejecutar header malformed, filtro malformed y mensaje sin filtro; comprobar comportamientos definidos.
5. Confirmar que no hubo cambios de DB/schema/pipeline environment.
6. Retirar header y ejecutar smoke legacy como rollback.
7. Enlazar evidencia y dejar G3 `review`; no promover producción.

**Archivos esperados**

- `modify`: planner/runbook/evidencia; código sólo si un bug reabre su fase/gate.

**No tocar**

- Producción, DB, topics, retries, datos no descartables, eventos fuera de alcance y untracked ajenos.

**Spikes permitidos**

- Ninguno. Un fallo contractual reabre F1/F2 o marca `PLAN_CONFLICT`; no parchear durante E2E.

**Tests y asserts**

- Header `alpha` produce trigger/result `scope:alpha` y finalización del batch.
- Malformed se rechaza/ACKea según contrato; legacy sin header/filtro funciona.
- Rollback no requiere schema/config flag.

**Entregables/Gate G3**

- Golden E2E, negativos, prueba de no-persistencia y rollback. G3 queda `review` para Rodrigo.

**Handoff a Fase 4**

- No existe Fase 4. Con G3 aceptado, cualquier retry/restart o expansión abre un proyecto/decisión separada.

## ✅ Tareas

- [ ] **T0.1** Auditar separación KISS | planner+SPEC | precondición: ninguna | implementación: buscar cualquier mezcla Environment/scope | tests: no-touch completo | evidencia: review #owner/agent #type/pr-review #area/meli
- [ ] **T0.2** Revalidar baseline/carrier | repo+dependencias | precondición: GlobalProtect | implementación: fetch+trace read-only | tests: símbolos/firmas | evidencia: SHA+mapa #owner/agent #type/research #area/meli
- [ ] **T0.3** Verificar Fury/Flink | contratos externos | precondición: accesos | implementación: route/filter/echo | tests: server-side | evidencia: links o G0 blocked #owner/agent #type/research #area/meli
- [ ] **T1.1** Capturar header | controller+deploy contract | precondición: G0 accepted | implementación: optional/malformed | tests: HTTP cases | evidencia: unit tests #owner/agent #type/dev #area/meli
- [ ] **T1.2** Propagar carrier | group/batch/DispatchRequest | precondición: T1.1 | implementación: metadata in-memory | tests: AFTER_COMMIT | evidencia: workflow test #owner/agent #type/dev #area/meli
- [ ] **T1.3** Publicar filtro | adapter+producer | precondición: T1.2 | implementación: mqclient Filters | tests: filtered+legacy+payload intacto | evidencia: envelope fixture #owner/agent #type/dev #area/meli
- [ ] **T2.1** Conservar envelope filters | result controller+consumer | precondición: G1 accepted | implementación: valid/legacy/malformed | tests: controller matrix | evidencia: unit tests #owner/agent #type/dev #area/meli
- [ ] **T2.2** Propagar durante result request | orchestration inmediata | precondición: T2.1 | implementación: parámetro transitorio o acotar a un batch | tests: no JPA/query | evidencia: workflow test #owner/agent #type/dev #area/meli
- [ ] **T2.3** Observabilidad bounded | metrics/logs | precondición: T2.1 | implementación: reason catalog | tests: no dynamic tags/raw | evidencia: metric tests #owner/agent #type/dev #area/meli
- [ ] **T3.1** Smoke legacy | candidate nonprod | precondición: G2 accepted | implementación: sin header | tests: comportamiento actual | evidencia: run #owner/agent #type/dev #area/meli
- [ ] **T3.2** Golden alpha de un batch | E2E | precondición: Fury/Flink listos | implementación: header→trigger→result | tests: filtro exacto | evidencia: IDs/logs redactados #owner/agent #type/dev #area/meli
- [ ] **T3.3** Negativos y rollback | E2E/config front | precondición: T3.2 | implementación: malformed+retirar header | tests: legacy restaurado | evidencia: G3 review #owner/agent #type/dev #area/meli

## Prompt común del executor/reviewer

Trabaja únicamente la fase indicada de [[POC KISS — Routing de scopes en Playmaker]]. Antes de actuar, repite y aplica esta invariante: `Pipeline Environment ≠ Fury Scope`. El scope Fury llega en `X-Rio-Scope` y en esta POC sólo se convierte en `scope:<valor>` dentro del envelope BigQueue. Está prohibido tocar `PipelineExecution`, `EnvironmentModel`, repositories, migrations, idempotencia, history, payload DTOs, SDK, timeout/retry u otros eventos. Propaga el dato sólo en memoria. Conserva cambios/untracked ajenos. Escribe primero tests críticos, apunta a ≥95% de cobertura nueva y ejecuta checks del repo. Si el dato no puede llegar al producer sin persistencia, si Fury no filtra server-side o si necesitas tocar `No tocar`, detente y registra `PLAN_CONFLICT`; no improvises. Actualiza tareas/Bitácora/gate. Puedes dejar tu gate `review`, `blocked` o `rejected`, nunca `accepted`, y no inicies la fase siguiente.

**Despacho Fase 0**

```text
FASE_ASIGNADA=0
PAQUETE_CANONICO=Paquete autónomo Fase 0 — Revisión independiente de separación y KISS
GATE_REQUERIDO=none
TAREAS=T0.1-T0.3
SALIDA=review conceptual + baseline/carrier fresco + evidencia Fury/Flink + G0 review/blocked
STOP=detener al dejar G0 review/blocked/rejected; prohibido escribir código o iniciar F1
```

**Despacho Fase 1**

```text
FASE_ASIGNADA=1
PAQUETE_CANONICO=Paquete autónomo Fase 1 — Header a filtro del trigger
GATE_REQUERIDO=G0 accepted
TAREAS=T1.1-T1.3
SALIDA=header+carrier in-memory+filtered publish+legacy tests+G1 review
STOP=detener al dejar G1 review/blocked/rejected; prohibido tocar result F2
```

**Despacho Fase 2**

```text
FASE_ASIGNADA=2
PAQUETE_CANONICO=Paquete autónomo Fase 2 — Conservar filtro del result
GATE_REQUERIDO=G1 accepted
TAREAS=T2.1-T2.3
SALIDA=result filters conservados+malformed guard+no-domain-change+G2 review
STOP=detener al dejar G2 review/blocked/rejected; prohibido iniciar E2E F3
```

**Despacho Fase 3**

```text
FASE_ASIGNADA=3
PAQUETE_CANONICO=Paquete autónomo Fase 3 — Certificación alpha de un batch
GATE_REQUERIDO=G2 accepted
TAREAS=T3.1-T3.3
SALIDA=smoke legacy+golden alpha+negativos+rollback+G3 review
STOP=detener al dejar G3 review/blocked/rejected; prohibido retry, persistencia o producción
```

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `rio-playmaker` | `feature/sig-599-playmaker-scope-filter-poc` — crear tras G0 | `origin/master@f350fb26091d` local; revalidar en F0 | [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) / [[scope-naming-standard]] | [[SPEC técnica — Routing KISS por scope en rio-playmaker]] | corregido; `ready_for_phase_0`; código no iniciado |

## 📆 Bitácora

- **2026-09-16** — Se creó el primer planner, pero mezcló incorrectamente scope Fury con estado de `PipelineExecution`; diseño invalidado.
- **2026-09-17** — Rodrigo corrige la semántica: pipeline environment y Fury scope son ejes totalmente distintos. Planner y SPEC reescritos desde cero. La POC queda reducida a header transitorio → filtro BigQueue, sin DB, migrations, idempotencia, history ni campo SDK. Retry/restart queda explícitamente fuera.

## 🧭 Decisiones

- La regla inicial gobierna todo el proyecto y prevalece ante cualquier texto histórico contradictorio.
- Cualquier propuesta de persistencia o comparación con pipeline environment se detiene como `PLAN_CONFLICT` y requiere una decisión nueva de Rodrigo.

## 🔗 Docs / Links

- Funcional: [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) · [[scope-naming-standard]]
- Técnica: [[SPEC técnica — Routing KISS por scope en rio-playmaker]]
- Parent: [[Estandarización de Scopes RIO]]
- Front: [[SPEC técnica — Routing dinámico de backend en ads-signals-frontend]]

## 💡 Ideas

- Si la POC funciona y se necesita retry/restart, abrir un diseño separado para continuidad durable del routing scope. No anticiparlo aquí.
