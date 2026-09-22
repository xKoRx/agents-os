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
updated: "2026-09-21"
---

# POC KISS — Routing de scopes en Playmaker

> [!danger] REGLA BÁSICA — LEER ANTES DE TOCAR ESTE PROYECTO
> **EL `ENVIRONMENT` DEL PIPELINE NO ES LO MISMO QUE EL SCOPE DE FURY.** Este proyecto alinea scopes de infraestructura Fury. El `Environment` del pipeline es dominio de negocio existente y queda completamente fuera. La lane de infraestructura se deriva exclusivamente del `SCOPE` del runtime de Fury y se usa para publicar `scope:<lane>` como filtro BigQueue. Está prohibido persistirla en `PipelineExecution`, usarla en idempotencia/history, compararla con el pipeline environment o crear un campo llamado `environment_scope`.

> [!info]+ Estado ejecutivo
> **Ready phase:** Fase 0 · **Gate actual:** G0 `pending` · **Base local observada:** `origin/master@f350fb26091d` · **Principio KISS:** runtime Fury → lane → filtro BigQueue; cero carrier por request, cero DB, cero SDK DTO, cero cambios al dominio del pipeline.

## 🎯 Objetivo

Implementar y certificar en `rio-playmaker` la POC mínima de SIG-599: hacer seguro el arranque de los scopes canónicos, derivar la lane desde `ScopeUtils.getScopeValue()` y estampar `scope:<lane>` en los mensajes publicados por `DeploymentTriggerProducerImpl.publish` y `DeploymentResultProducerImpl.publish`. La solución debe cubrir el primer batch, el batch N+1, el retry por timeout y el result sin leer `X-Rio-Scope` ni transportar metadata desde una request.

## 📊 Estado actual

- `ScopeUtils.getScopeValue()` ya lee `System.getenv("SCOPE")` y usa `local` cuando la variable no está disponible.
- `ScopeUtils.calculateScopeSuffix()` sólo reconoce `local | test | stage | production`; para un scope sin esos tokens termina usando el primer token como profile.
- `alpha-api-nonprod` intenta activar `alpha`, profile que no existe y deja el servicio sin datasource; `prod-api-nonsite` intenta activar `prod`, aunque el profile productivo se llama `production`; `beta-api-nonprod` activa el profile `beta`, cuyo archivo apunta a `playmkrprod`, `rio-deployment-trigger-prod` y segmento `nonsite`.
- `application.yml` no define datasource y sus defaults BigQueue usan segmento `nonsite`; el fallback base no es seguro para una lane nonprod nueva.
- `DeploymentTriggerProducerImpl.publish` y `DeploymentResultProducerImpl.publish` llaman hoy `producer.send(message)`; mqclient `3.4.9` ya ofrece `producer.send(message, Filters)`.
- El primer batch, el batch N+1 y el retry de `DeploymentTimeoutJob` convergen en `DeploymentTriggerProducerImpl.publish`; el result converge en `DeploymentResultProducerImpl.publish`.
- Fury aplica el filtro server-side por decisión del owner; no es una condición de investigación ni un gate externo de esta POC.
- No se toca `PipelineExecution`, `EnvironmentModel`, DB, migrations, idempotencia, history, controllers, services de deploy, dispatch, consumers ni payloads SDK.

## Resultado esperado

Un runtime con `SCOPE=alpha-api-nonprod` o `SCOPE=alpha-consumer-nonprod` resuelve `lane=alpha`, arranca con configuración stage/nonprod y publica mediante ambos producers con `Filters(List.of("scope:alpha"))`. Un runtime con lane no resoluble o fuera del vocabulario publica sin filtro, que es el comportamiento legacy actual.

## Matriz requisito → evidencia

| ID | Requisito | Estado | Evidencia actual | Trabajo restante |
|---|---|---|---|---|
| R1 | Separar pipeline environment de Fury scope | `confirmed` | Regla innegociable del owner | Proteger con no-touch y revisión |
| R4 | Publicar `scope:<lane>` en los dos producers | `partial` | mqclient expone `Producer.send(message, Filters)` | Implementar derivación y overload filtrado |
| R5 | Mantener SDK y payloads intactos | `done` | Los filtros pertenecen al envelope de mqclient | No modificar SDK ni DTOs |
| R7 | Mantener fallback legacy | `partial` | Ambos producers usan hoy `send(message)` | Usarlo cuando la lane no sea válida |
| R10 | Resolver profiles canónicos sin caer en profiles peligrosos | `pending` | `ScopeUtils.calculateScopeSuffix()` no conoce `prod | alpha | beta | gamma` | Mapear `prod → production` y `stage | alpha | beta | gamma → stage` |
| R11 | Hacer seguro el default base | `pending` | Base sin datasource y con segmento `nonsite` | Configurar datasource `playmkrstg` y segmento `nonprod` |
| R12 | Cubrir los cuatro caminos de publicación | `pending` | Tres usan trigger producer y uno result producer | Certificar primer batch, N+1, timeout retry y result |

## Alcance, no alcance y decisiones

### Alcance

- Resolución segura del Spring profile para scopes Fury canónicos en `ScopeUtils.calculateScopeSuffix()`.
- Derivación de lane como primer token normalizado de `ScopeUtils.getScopeValue()`, válida sólo para `prod | stage | alpha | beta | gamma`.
- Defaults base de stage: datasource `playmkrstg` y segmento `nonprod`.
- Filtro `scope:<lane>` en `DeploymentTriggerProducerImpl.publish` y `DeploymentResultProducerImpl.publish`.
- Compatibilidad legacy cuando la lane no se puede resolver.
- E2E alpha con más de un batch, result y retry por timeout.
- Observabilidad bounded `routing_mode:legacy|filtered` sin usar la lane como tag dinámico.

### No alcance

- Lectura, validación o propagación de `X-Rio-Scope` dentro de Playmaker; Fury Routes usa ese header antes de entregar la request.
- Pipeline environment, `PipelineExecution`, `EnvironmentModel`, repositories, idempotencia, history/detail/logs, DB y migrations.
- Campos nuevos en entidades, commands, dispatches o payloads, especialmente `environment_scope`, `fury_scope` o equivalentes.
- Cambios en controllers, deploy flow, `DispatchRequest`, consumers, parsing de envelopes o servicios de dominio.
- Cambios o release en `rio-sdk-events`, topics nuevos, Actions, inactivation, `DataProductChanged`, Materializer o producción.
- Solución durable para aislar retries por lane en la base compartida.

### Registro de decisiones

| ID | Estado | Resolución | Fuente | Fase que consume |
|---|---|---|---|---|
| DD-1 | `CONFIRMED` | Pipeline environment y scope Fury son ejes independientes; la lane sale sólo del `SCOPE` del runtime | Owner | F0–F2 |
| DD-4 | `CONFIRMED` | Playmaker no lee `X-Rio-Scope`; Fury Routes lo usa para seleccionar la instancia y los producers derivan el tag localmente | Owner | F1–F2 |
| DD-5 | `TECHNICAL_RESOLUTION` | Usar mqclient `Producer.send(message, Filters)` sin cambiar SDK ni payloads | Contrato existente | F1 |
| DD-6 | `CONFIRMED` | Lane ausente, inválida o desconocida publica sin filtro; no se adivina una lane | Owner | F1–F2 |

## Arquitectura objetivo

```text
frontend -- X-Rio-Scope --> Fury Routes --> instancia Playmaker
                                             │
                                             │ SCOPE=<lane>-<role>-...-<segment>
                                             ▼
                                   ScopeUtils.getScopeValue()
                                             │
                                             ├─ profile seguro
                                             │  prod → production
                                             │  stage|alpha|beta|gamma → stage
                                             │
                                             └─ primer token válido → lane
                                                        │
                              ┌─────────────────────────┴─────────────────────────┐
                              ▼                                                   ▼
             DeploymentTriggerProducerImpl.publish             DeploymentResultProducerImpl.publish
                              │                                                   │
                              └──────── send(message, Filters([scope:<lane>])) ───┘

PipelineExecution / Pipeline Environment / controller / dispatch / consumer / SDK: SIN CAMBIOS
```

## Secuencia de datos y control

1. El frontend envía `X-Rio-Scope`; Fury Routes lo usa para elegir una instancia y Playmaker no lee el header.
2. La instancia expone su scope en `SCOPE`; `ScopeUtils.getScopeValue()` es la única fuente de verdad dentro de Playmaker.
3. `ScopeUtils.calculateScopeSuffix()` traduce el primer token canónico a un Spring profile seguro y conserva compatibilidad con profiles legacy.
4. La derivación de lane toma el primer token en lowercase y sólo lo acepta si pertenece a `prod | stage | alpha | beta | gamma`.
5. Cada invocación de `DeploymentTriggerProducerImpl.publish` o `DeploymentResultProducerImpl.publish` calcula la lane del runtime y publica con `Filters(List.of("scope:" + lane))`.
6. Si la lane no se resuelve, el producer ejecuta `producer.send(message)` sin filtro.
7. Fury entrega cada mensaje únicamente al binding compatible con el filtro.

## Contratos y edge cases

La autoridad completa es [[SPEC técnica — Routing KISS por scope en rio-playmaker]]. Contratos congelados:

- Runtime: `ScopeUtils.getScopeValue()` lee `SCOPE`; no existe input HTTP para Playmaker.
- Lane: primer token del scope, normalizado a lowercase y validado contra `prod | stage | alpha | beta | gamma`.
- Profiles: `prod → production`; `stage | alpha | beta | gamma → stage`; `local | test | production` mantienen compatibilidad existente.
- Defaults: `application.yml` define datasource `playmkrstg` y `bigqueue.segment: nonprod`.
- Producer: lane válida usa `producer.send(message, new Filters(List.of("scope:" + lane)))`; lane no válida usa `producer.send(message)`.
- Payload: `DeploymentTriggerMessage` y `DeploymentResultMessage` no cambian.
- Segmento: `ProducerBuilder.withSegmentID` permanece independiente del filtro scope.
- Resultado: el consumer no parsea ni valida `envelope.filters`; procesa únicamente lo que entregue su binding.
- Seguridad: no usar el valor dinámico de lane como metric tag ni loguear variables de entorno completas.

## Roadmap dependency-ordered

| Fase | Resultado | Carga relativa | Gate |
|---|---|---|---|
| F0 | `ScopeUtils` resuelve el vocabulario canónico y el default base queda en stage/nonprod | Media por riesgo de configuración | G0 |
| F1 | Ambos producers estampan la lane del runtime y conservan fallback legacy | Baja, dos puntos de publicación | G1 |
| F2 | E2E alpha demuestra trigger inicial, result, batch N+1 y timeout retry con `scope:alpha` | Media por orquestación | G2 |

## Mapa de archivos y símbolos

| Acción | Superficie | Fase |
|---|---|---|
| `modify` | `ScopeUtils.calculateScopeSuffix()` y nueva derivación de lane en `ScopeUtils` | F0 |
| `modify` | `application.yml` para datasource `playmkrstg` y segmento `nonprod` | F0 |
| `modify` | Tests de `ScopeUtils` y de carga/configuración base | F0 |
| `modify` | `DeploymentTriggerProducerImpl.publish` y tests | F1 |
| `modify` | `DeploymentResultProducerImpl.publish` y tests | F1 |
| `modify` | Tests de integración/E2E y evidencia de los cuatro caminos | F2 |
| `no-touch` | Controllers, deploy services, `DeploymentGroupService`, `BatchDispatchService`, `DispatchRequest`, factories, adapters y consumers | Todas |
| `no-touch` | Models JPA, repositories, migrations, idempotencia, history y pipeline environment | Todas |
| `no-touch` | `rio-sdk-events`, DTOs, nombres de topics y otros producers/eventos | Todas |

## Estrategia de validación

- Unit F0: `stage-api-nonprod → lane stage/profile stage`; `alpha-api-nonprod → lane alpha/profile stage`; `alpha-consumer-nonprod → lane alpha/profile stage`; `beta-api-nonprod → lane beta/profile stage`; `gamma-api-nonprod → lane gamma/profile stage`; `prod-api-nonsite → lane prod/profile production`.
- Compatibilidad F0: `local`, `test`, `production` y scopes legacy soportados mantienen su resolución; scope vacío, malformed o desconocido no produce una lane válida.
- Config F0: el contexto base dispone de datasource `playmkrstg` y segmento `nonprod`; ningún scope canónico nonprod carga `application-beta.yml` ni recursos productivos.
- Unit F1: ambos producers usan exactamente `Filters(List.of("scope:alpha"))` en runtime alpha y `send(message)` cuando la lane no se resuelve.
- Wire F1: payloads de trigger/result son byte-compatible y el tag sólo vive en el envelope mqclient.
- E2E F2: deploy alpha con más de un batch captura filtros del trigger inicial, result, batch N+1 y retry por timeout.
- No-regression: ninguna migration, query, model, controller, dispatch, consumer ni payload cambia.
- Calidad: tests críticos primero, checks del repo y ≥95% de cobertura sobre código nuevo.

## Compatibilidad, observabilidad, rollout y rollback

- Compatibilidad: scopes legacy o desconocidos siguen publicando sin filtro; profiles legacy continúan resolviéndose.
- Observabilidad: `routing_mode:legacy|filtered` es la única dimensión nueva; nunca se usa la lane dinámica como tag.
- Rollout: F0 sanea profile/defaults antes de crear scopes canónicos; F1 habilita filtros en ambos producers; F2 despliega las instancias alpha web y consumer y ejecuta la matriz E2E.
- Rollback: revertir el artefacto/configuración de Playmaker a la versión anterior; no hay schema, backfill, feature flag ni estado persistido que revertir. El header del frontend no participa en el rollback de Playmaker.
- Release: ninguna promoción productiva desde feature branch.

## Limitación aceptada de la POC

Las lanes nonprod comparten la base `playmkrtst` y `DeploymentRepository.findByStatusInAndTimeoutAtBefore` selecciona por `status + timeout_at` sin discriminador de lane. Por ello, `DeploymentTimeoutJob` de una lane puede reclamar un deployment creado por otra y `DeploymentTriggerProducerImpl.publish` estampará la lane del runtime que ejecutó el retry. Esta limitación es asumible para la POC; resolverla requiere estado durable y una decisión separada. Está prohibido agregar columnas o tocar `PipelineExecution` para ocultarla.

## Riesgos y controles

| Riesgo | Mitigación | Control humano |
|---|---|---|
| Mezclar Pipeline Environment con Fury Scope | Regla inicial, no-touch y tests de diff | Rechazar gate |
| Scope canónico activa un profile inexistente o productivo | F0 precede cualquier alta de scope y prueba toda la matriz | Aceptar G0 antes de F1 |
| Lane desconocida recibe un tag inventado | Fallback explícito a publish legacy | Revisar tests F1 |
| Algún camino publica sin pasar por los dos producers | Trazar y probar los cuatro caminos en F2 | Revisar evidencia E2E |
| Timeout job cruza deployments entre lanes | Limitación explícita y uso sólo POC | Decisión durable futura |
| Scope creep a HTTP, carrier, consumer, DB o SDK | Lista no-touch y revisión del diff | Rechazar gate |

## Definition of Done

- G0–G2 están `accepted` por el owner; ningún agente acepta su propio gate.
- La regla `Pipeline Environment ≠ Fury Scope` permanece visible y protegida por no-touch.
- Los scopes canónicos resuelven profiles seguros y los defaults base apuntan a stage/nonprod.
- `SCOPE=alpha-api-nonprod` y `SCOPE=alpha-consumer-nonprod` producen exactamente `scope:alpha` en ambos producers.
- Primer batch, result, batch N+1 y retry por timeout llevan `scope:alpha` en el E2E.
- Lane no resoluble conserva publicación legacy sin filtro.
- Pipeline domain, controller/dispatch/consumer, DB, SDK y payloads permanecen sin cambios.
- Checks, cobertura ≥95%, E2E y rollback quedan enlazados.

## Control de gates

| Gate | current state | phase agent responsibility | owner acceptance evidence | enables |
|---|---|---|---|---|
| G0 | `pending` | Dejar profile mapping, defaults stage/nonprod y tests en `review` | Matriz canónica verde, beta no carga prod y diff acotado | F1 |
| G1 | `pending` | Dejar ambos producers, fallback y tests en `review` | Filtro exacto, payload intacto y cero carrier/consumer/DB/SDK | F2 |
| G2 | `pending` | Dejar E2E y rollback en `review` | Cuatro caminos alpha, legacy y limitación registrada | cierre |

### Paquete autónomo Fase 0 — Profiles y defaults seguros

**Misión exacta**

Hacer que todos los scopes canónicos arranquen con un profile seguro y que cualquier configuración base caiga en datasource stage y segmento nonprod antes de crear nuevas lanes.

**Precondiciones verificables**

- Ninguna; es la fase inicial y no depende de evidencia externa de Fury.
- Crear branch `feature/sig-599-playmaker-scope-filter-poc` desde una base fresca sin tocar untracked ajenos.

**Lectura obligatoria**

- `VAULT_ROOT/10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing KISS por scope en rio-playmaker.md` completa.
- `ScopeUtils`, `ScopeUtilsTest`, `Application`, `application.yml`, `application-stage.yml`, `application-production.yml`, `application-beta.yml` y tests de contexto/configuración.
- `VAULT_ROOT/30-resources/rio-atlas/architecture/scope-naming-standard.md`, especialmente vocabulario y convención `<environment>-<role>[-<qualifier>]-<segment>`.

**Decisiones cerradas del owner**

- Pipeline environment no participa.
- El vocabulario de lane es `prod | stage | alpha | beta | gamma`.
- `prod` usa profile `production`; `stage | alpha | beta | gamma` usan profile `stage`.
- El default base es datasource `playmkrstg` y segmento `nonprod`.
- No se toca DB schema ni `PipelineExecution`.

**Implementación paso a paso**

1. Escribir la matriz de tests de lane/profile y compatibilidad legacy.
2. Agregar en `ScopeUtils` una derivación de lane que normalice el primer token y devuelva ausencia cuando no pertenezca al vocabulario.
3. Ajustar `ScopeUtils.calculateScopeSuffix()` para resolver el vocabulario canónico al profile seguro sin romper `local | test | production` ni scopes legacy soportados.
4. Mover a `application.yml` los defaults mínimos de datasource `playmkrstg` y establecer `bigqueue.segment: nonprod`.
5. Probar que alpha/beta/gamma no cargan un profile homónimo y que `prod` carga `production`.
6. Ejecutar checks y dejar G0 `review`, nunca `accepted`.

**Archivos esperados**

- `modify`: `ScopeUtils`, `ScopeUtilsTest`, `application.yml` y tests mínimos de configuración.
- `conditional`: deduplicación segura con `application-stage.yml` si el reviewer demuestra que evita drift sin ampliar alcance.

**No tocar**

- Producers, controllers, services de deploy, dispatch, consumers, JPA/DB, SDK, topics y untracked del usuario.

**Spikes permitidos**

- Inspección read-only de cómo Spring combina `application.yml` con profiles. Si surge un cambio de recursos más allá de datasource/segmento, registrar `PLAN_CONFLICT`.

**Tests y asserts**

- Matriz canónica completa de lane/profile.
- `beta-api-nonprod` no activa `application-beta.yml`.
- `prod-api-nonsite` activa `production`.
- Base tiene `playmkrstg` y `nonprod`.
- ≥95% de cobertura sobre código nuevo.

**Entregables/Gate G0**

- Diff de F0, matriz de tests, evidencia de contexto seguro y G0 en `review`.

**Handoff a Fase 1**

- El agente recibe G0 `accepted`, la API exacta de derivación de lane y la branch validada.

### Paquete autónomo Fase 1 — Filtro desde la lane del runtime

**Misión exacta**

Estampar el tag de lane en los mensajes de trigger y result usando exclusivamente `ScopeUtils.getScopeValue()` y la derivación validada de F0.

**Precondiciones verificables**

- G0 `accepted`.

**Lectura obligatoria**

- `VAULT_ROOT/10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing KISS por scope en rio-playmaker.md`, contratos de runtime/BigQueue y no-touch.
- `DeploymentTriggerProducerImpl`, `DeploymentResultProducerImpl`, sus interfaces, constructores y tests.
- mqclient `Producer.send(Object, Filters)` y `Filters(List<String>)`.

**Decisiones cerradas del owner**

- La única fuente del tag es la lane del `SCOPE` local.
- Lane fuera de vocabulario publica sin filtro.
- Fury filtra server-side.
- No existe carrier por request y no se lee el header.

**Implementación paso a paso**

1. Escribir tests filtered/legacy para los dos producers.
2. Hacer que `DeploymentTriggerProducerImpl.publish` resuelva la lane en cada publicación y use el overload con `Filters` sólo cuando sea válida.
3. Aplicar la misma regla en `DeploymentResultProducerImpl.publish` sin duplicar el vocabulario ni la semántica.
4. Agregar la señal bounded `routing_mode:legacy|filtered` usando el mecanismo de observabilidad existente más pequeño.
5. Probar que el payload no cambia y que no aparecen parámetros, campos ni carriers nuevos fuera de los producers/utility.
6. Ejecutar checks y dejar G1 `review`, nunca `accepted`.

**Archivos esperados**

- `modify`: `DeploymentTriggerProducerImpl`, `DeploymentResultProducerImpl` y sus tests.
- `conditional`: helper mínimo compartido sólo si evita duplicación real sin crear una abstracción nueva innecesaria.

**No tocar**

- Controllers, deploy/group/batch services, `DispatchRequest`, factories, adapters, result consumer, JPA/DB, SDK, payloads, timeout job, topics y otros producers.

**Spikes permitidos**

- Ninguno. Si mqclient no acepta el filtro contratado, registrar `PLAN_CONFLICT`; no cambiar payload ni SDK.

**Tests y asserts**

- Ambos producers llaman exactamente `send(message, Filters(["scope:alpha"]))` con scope alpha.
- Scope desconocido llama exactamente `send(message)`.
- El mensaje serializado no cambia.
- Sólo se emite `routing_mode:legacy|filtered`; no hay tag dinámico de lane.
- ≥95% de cobertura sobre código nuevo.

**Entregables/Gate G1**

- Diff acotado a utility/producers/tests, checks verdes y G1 en `review`.

**Handoff a Fase 2**

- El agente recibe G1 `accepted`, candidate nonprod y matriz unitaria; sólo resta la certificación E2E.

### Paquete autónomo Fase 2 — Certificación alpha multibatch y retry

**Misión exacta**

Certificar en alpha que los cuatro caminos de publicación llevan `scope:alpha`: trigger inicial, result, trigger de batch N+1 y retry por timeout.

**Precondiciones verificables**

- G1 `accepted`.
- Scopes `alpha-api-nonprod` y `alpha-consumer-nonprod` creados con bindings compatibles.
- Candidate generado por proceso autorizado.

**Lectura obligatoria**

- `VAULT_ROOT/10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing KISS por scope en rio-playmaker.md`, rollout, DoD y limitación aceptada.
- Flujo de primer batch, avance de batch, `DeploymentTimeoutJob` y result producer.
- Evidencia G0–G1 y runbook nonprod.

**Decisiones cerradas del owner**

- Fury filtra server-side; no se repite un spike de esa capability.
- La POC incluye multibatch y retry por timeout.
- El riesgo cross-lane del timeout job se documenta y no se resuelve con estado durable.
- Sólo alpha/nonprod; no promoción productiva.

**Implementación paso a paso**

1. Desplegar el candidate en los scopes web y consumer alpha y verificar profile stage, datasource `playmkrstg` y segmento `nonprod`.
2. Ejecutar smoke con un scope legacy/desconocido controlado y confirmar publish sin filtro.
3. Ejecutar un deploy alpha con más de un batch y capturar el filtro del trigger inicial.
4. Capturar un result publicado por el runtime alpha y verificar `scope:alpha`.
5. Permitir el avance al batch N+1 desde el consumer y verificar el nuevo trigger `scope:alpha`.
6. Provocar de forma controlada un timeout elegible y verificar que el retry publicado por `DeploymentTimeoutJob` lleva `scope:alpha`.
7. Confirmar que no hubo cambios de schema, payload, pipeline environment, controller/dispatch/consumer ni SDK.
8. Ejecutar rollback del artefacto/configuración si corresponde, enlazar evidencia y dejar G2 `review`; no promover producción.

**Archivos esperados**

- `modify`: tests E2E/runbook/evidencia; código sólo si un bug reabre F0 o F1.

**No tocar**

- Producción, DB/schema, topics, datos no descartables, consumidores, eventos fuera de alcance y untracked ajenos.

**Spikes permitidos**

- Ninguno. Un fallo contractual reabre F0/F1 o registra `PLAN_CONFLICT`; no se parchea durante la certificación.

**Tests y asserts**

- Trigger inicial, result, batch N+1 y timeout retry contienen exactamente `scope:alpha`.
- Los runtimes web y consumer derivan la misma lane desde scopes diferentes.
- El fallback legacy sigue publicando sin filtro.
- El E2E registra la limitación cross-lane sin intentar resolverla.

**Entregables/Gate G2**

- Evidencia de los cuatro caminos, no-regression, rollback y G2 en `review` para Rodrigo.

**Handoff a Fase 3**

- No existe Fase 3. Con G2 aceptado, cualquier aislamiento durable por lane abre una decisión y proyecto separados.

## ✅ Tareas

- [ ] **T0.1** Escribir matriz canónica de scope→lane→profile | `ScopeUtilsTest` | precondición: ninguna | implementación: tests primero | evidencia: casos prod/stage/alpha/beta/gamma #owner/agent #type/dev #area/meli
- [ ] **T0.2** Resolver lane y profile seguro | `ScopeUtils` | precondición: T0.1 | implementación: primer token + mapping | evidencia: unit tests #owner/agent #type/dev #area/meli
- [ ] **T0.3** Asegurar defaults base stage | `application.yml` | precondición: T0.1 | implementación: datasource playmkrstg + nonprod | evidencia: context/config tests #owner/agent #type/dev #area/meli
- [ ] **T1.1** Filtrar trigger producer | `DeploymentTriggerProducerImpl.publish` | precondición: G0 accepted | implementación: lane válida/legacy | evidencia: producer tests #owner/agent #type/dev #area/meli
- [ ] **T1.2** Filtrar result producer | `DeploymentResultProducerImpl.publish` | precondición: T1.1 | implementación: misma derivación | evidencia: producer tests #owner/agent #type/dev #area/meli
- [ ] **T1.3** Verificar wire y observabilidad | ambos producers | precondición: T1.2 | implementación: payload intacto + routing_mode | evidencia: contract tests #owner/agent #type/dev #area/meli
- [ ] **T2.1** Desplegar alpha y smoke legacy | candidate nonprod | precondición: G1 accepted | implementación: profiles/config/fallback | evidencia: run #owner/agent #type/dev #area/meli
- [ ] **T2.2** Certificar multibatch | E2E alpha | precondición: T2.1 | implementación: trigger+result+N+1 | evidencia: envelopes #owner/agent #type/dev #area/meli
- [ ] **T2.3** Certificar timeout retry y rollback | E2E alpha | precondición: T2.2 | implementación: timeout controlado+revert | evidencia: envelope+runbook #owner/agent #type/dev #area/meli

## Prompt común del executor/reviewer

Trabaja únicamente la fase indicada de [[POC KISS — Routing de scopes en Playmaker]]. Antes de actuar, repite y aplica esta invariante: `Pipeline Environment ≠ Fury Scope`. Playmaker no lee `X-Rio-Scope`; la única fuente de lane es el primer token validado de `ScopeUtils.getScopeValue()`. Está prohibido tocar `PipelineExecution`, `EnvironmentModel`, repositories, migrations, idempotencia, history, controllers, deploy/group/batch services, `DispatchRequest`, factories, adapters, consumers, payload DTOs o SDK. Conserva cambios/untracked ajenos. Escribe primero tests críticos, apunta a ≥95% de cobertura nueva y ejecuta checks del repo. Si necesitas tocar `No tocar`, detente y registra `PLAN_CONFLICT`; no improvises. Actualiza tareas y gate. Puedes dejar tu gate `review`, `blocked` o `rejected`, nunca `accepted`, y no inicies la fase siguiente.

**Despacho Fase 0**

```text
FASE_ASIGNADA=0
PAQUETE_CANONICO=Paquete autónomo Fase 0 — Profiles y defaults seguros
GATE_REQUERIDO=none
TAREAS=T0.1-T0.3
SALIDA=scope→lane→profile seguro + defaults stage/nonprod + tests + G0 review
STOP=detener al dejar G0 review/blocked/rejected; prohibido modificar producers o iniciar F1
```

**Despacho Fase 1**

```text
FASE_ASIGNADA=1
PAQUETE_CANONICO=Paquete autónomo Fase 1 — Filtro desde la lane del runtime
GATE_REQUERIDO=G0 accepted
TAREAS=T1.1-T1.3
SALIDA=dos producers filtrados + fallback legacy + payload intacto + G1 review
STOP=detener al dejar G1 review/blocked/rejected; prohibido iniciar E2E F2
```

**Despacho Fase 2**

```text
FASE_ASIGNADA=2
PAQUETE_CANONICO=Paquete autónomo Fase 2 — Certificación alpha multibatch y retry
GATE_REQUERIDO=G1 accepted
TAREAS=T2.1-T2.3
SALIDA=trigger inicial + result + batch N+1 + timeout retry con scope:alpha + rollback + G2 review
STOP=detener al dejar G2 review/blocked/rejected; prohibido promover producción o agregar estado durable
```

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| `rio-playmaker` | `feature/sig-599-playmaker-scope-filter-poc` | `origin/master@f350fb26091d` local; refrescar antes de implementar | [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) / [[scope-naming-standard]] | [[SPEC técnica — Routing KISS por scope en rio-playmaker]] | `ready_for_phase_0`; código no iniciado |

## 📆 Bitácora

- **2026-09-21** — Plan objetivo listo para revisión: F0 profiles/defaults seguros, F1 filtros derivados del runtime y F2 certificación alpha multibatch/retry.

## 🔗 Docs / Links

- Funcional: [SIG-599](https://spellbook.adminml.com/projects/SIG/specs/SIG-599) · [[scope-naming-standard]]
- Técnica: [[SPEC técnica — Routing KISS por scope en rio-playmaker]]
- Parent: [[Estandarización de Scopes RIO]]
- Front: [[SPEC técnica — Routing dinámico de backend en ads-signals-frontend]]
