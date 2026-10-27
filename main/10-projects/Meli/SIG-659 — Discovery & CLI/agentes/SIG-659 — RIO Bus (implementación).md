---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Meli]]"
parent: "[[SIG-659 — Discovery & CLI]]"
sprint:
start: "2026-10-27"
due:
progress: 83
repo: https://github.com/melisource/fury_rio-sdk-events
jira:
prs:
aliases:
  - RIO Bus implementación
  - implementación del transporte Discovery
tags:
  - kind/project
  - area/meli
created: "2026-10-27"
updated: "2026-10-27"
---

# SIG-659 — RIO Bus (implementación)

%% Naming: SIG-659 — RIO Bus (implementación) es el link canónico del proyecto; aliases guarda variantes humanas; tags/slugs son solo automatización. %%

> [!info]+ SIG-659 — RIO Bus (implementación)
> **Área:** [[Meli]] · **Estado:** active · **Prioridad:** P1 · **Parent:** [[SIG-659 — Discovery & CLI]] · **Sprint:** —
> _parent / sprint / repo / jira / prs son opcionales._

> [!abstract]- Ownership del proyecto (`owner`) — humano vs agente
> `owner: me` → **proyecto humano**: la iniciativa/esfuerzo que conduces tú.
> `owner: agent` → **proyecto de agente**: un curro delegado, con detalle pesado que escribe y sigue un agente. Casi siempre es subproyecto de uno humano y vive en la subcarpeta `agentes/` de su iniciativa.
> `root: true` solo en **iniciativas raíz** (sin `parent`). Todo subproyecto debe setear `parent`; si no, aparece como huérfano en [[Panel de Proyectos]].
>
> **Tarea puente:** cuando este proyecto es `owner: agent`, en su proyecto **padre** debe existir UNA sola tarea humana que lo representa (arrancar + seguimiento). Así tu cockpit ve una línea por curro delegado, no las tareas internas del agente. Ejemplo, en el padre:
> `- [ ] [[SIG-659 — RIO Bus (implementación)]] arrancar + seguimiento #owner/me #type/supervision #area/meli`

## 🎯 Objetivo

- Implementar el **RIO Bus** tal como lo definen [SIG-718](https://spellbook.adminml.com/projects/SIG/specs/SIG-718) (funcional) y [SIG-719](https://spellbook.adminml.com/projects/SIG/specs/SIG-719) (técnica): un tópico `rio-bus`, un mensaje de cuatro atributos (`envelope_version`, `process`, `scope`, `body`), publicación y consumo en rio-sdk-events, publicación de los contratos Discovery al arrancar desde el SDK y el process `discovery` en rio-playmaker.
- Las specs son la fuente del diseño. Este proyecto sólo ordena la ejecución: qué se hace en cada fase, con qué evidencia se cierra y qué no se toca.
- Fuera de este proyecto: el modelo Discovery V2 y `DiscoveryMessageReader` (Brenda, [SIG-644](https://spellbook.adminml.com/projects/SIG/specs/SIG-644)), el `DiscoveryContractProvider` de [[rio-controlplane-kafka]] (Brenda, [SIG-697](https://spellbook.adminml.com/projects/SIG/specs/SIG-697)), la ingesta en MySQL ([SIG-671](https://spellbook.adminml.com/projects/SIG/specs/SIG-671)) y la creación del tópico y del consumer en Fury (owner).

## 📊 Estado actual

- **2026-10-27 — F1 implementada y pusheada; publicación pendiente.** G0 aceptado y D-10 resuelto por el owner. `rio-sdk-events@feature/rio-bus` commit `df9ef57bb09ac349a06e4a4bc9e13c000e249c2f`, base `35b1a43`; worktree limpio. Tres gates PASS, 2.496 tests sin fallos/omitidos, hooks pre/post-commit PASS. Código nuevo: 100% líneas/ramas, 99,66% instrucciones; 24 archivos dentro del presupuesto (16 + 8).
- **Próximo paso:** resolver con el owner el `PLAN_CONFLICT` del spike 2 y publicar `0.0.1-rio-bus`: Fury requiere esa versión en `build.gradle`, pero el paquete prohíbe modificar `version` y el SHA pusheado conserva `1.5.0`. La consulta para autorizar exclusivamente la versión de prueba está pendiente. G1 permanece `pending` y T1.6 `[/]` hasta completar la publicación; F2 no iniciada.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [`rio-sdk-events`](https://github.com/melisource/fury_rio-sdk-events) | `feature/rio-bus` | `origin/feature/discovery-v2-05-contract-hasher` @ `35b1a43` | [SIG-718](https://spellbook.adminml.com/projects/SIG/specs/SIG-718) | [SIG-719](https://spellbook.adminml.com/projects/SIG/specs/SIG-719) | F1 código y gates listos; publicación pendiente |
| [`rio-playmaker`](https://github.com/melisource/fury_rio-playmaker) | `feature/rio-bus` (create) | `origin/develop` | [SIG-718](https://spellbook.adminml.com/projects/SIG/specs/SIG-718) | [SIG-719](https://spellbook.adminml.com/projects/SIG/specs/SIG-719) | F2 pendiente |

## 🧩 Subproyectos

```base
filters:
  and:
    - 'type == "project"'
    - 'file.hasLink(this.file)'
views:
  - type: cards
    name: Subproyectos
    order:
      - file.name
      - note.status
      - note.priority
```

## Alcance

**IN:** lo que SIG-719 lista en "Archivos afectados" para rio-sdk-events y rio-playmaker, y la verificación en el scope de test.

**OUT:** migrar tópicos o controllers existentes; tocar el modelo Discovery V2, el linter, el validador, el writer o el hasher; escribir `DiscoveryMessageReader`; persistir contratos; cambiar CPs; crear infraestructura en Fury; abrir PRs; liberar versiones productivas; agregar flags, interfaces, registros o configuración que SIG-719 no nombra.

## Línea base y evidencia

Relevado el 2026-10-27 en refs remotas: `rio-sdk-events@origin/feature/discovery-v2-05-contract-hasher 35b1a43`, `rio-sdk-events@origin/master b928149`, `rio-playmaker@origin/develop 0c0e319c9`.

| Requisito | Estado | Evidencia |
|---|---|---|
| Paquete `bus` del SDK | `missing` | `HEAD`: no existe en ninguna rama del SDK |
| `DiscoveryContractProvider` / `DiscoveryContractPublisher` | `missing` | `HEAD`: el paquete `discovery` de la rama V2 trae sólo el modelo, `DiscoveryContractValidator`, `DiscoveryContractWriter` (`toJson`, `requireValid`) y `ContractHasher` |
| Segmento aplicado por `BigQueueClientImpl` | `partial` | `HEAD`: el builder con `withSegmentID` se descarta; el fix existe sin mergear en `origin/fix/producerbuilder-segment-buffering-discarded` (`c67d65e` fix + `f1194a4` tests) |
| `DiscoveryMessageReader` con entrada JSON (DD-8) | `missing` | `HEAD`: SIG-644 §7.3 lo define; no existe en las ramas `discovery-v2-0*`. Lo entrega Brenda (H-2) |
| Process `discovery` en playmaker | `missing` | `HEAD`: no hay `/rio-bus` ni `bus/` en `origin/develop` |
| Segmento por perfil en playmaker | `done` | `CONTRACT`: `bigqueue.segment` = `nonsite` en `application.yml`, `-production`, `-beta`; `nonprod` en `-stage`, `-test` |
| Tópico `rio-bus` y consumer | `missing` | Lo crea el owner en Fury (H-1) |
| `DiscoveryContractProvider` del CP Kafka | `missing` | Lo entrega Brenda (H-3) |

## Registro de decisiones

| ID | status | resolución | fuente/evidencia | fase |
|---|---|---|---|---|
| D-1 | CONFIRMED | Un solo tópico `rio-bus`; el `process` separa los flujos | SIG-719 DD-1 | F1, F2 |
| D-2 | CONFIRMED | `RioBusMessage(envelope_version, process, scope, body)`, los cuatro obligatorios, `envelope_version = 1` | SIG-718 RF-2, SIG-719 Contrato | F1 |
| D-3 | CONFIRMED | `RioBusPublisher` deriva los filtros `process:<process>` y `scope:<scope>`; su API no acepta filtros | SIG-719 DD-2 | F1 |
| D-4 | CONFIRMED | Un consumer por app y scope hacia `POST /rio-bus`; `RioBusReader` elige el process por nombre | SIG-719 DD-4 | F1, F2, F3 |
| D-5 | CONFIRMED | Configuración `rio.bus.topic`, `rio.bus.scope: ${SCOPE}`, `rio.bus.segment-id` (`nonprod` o `nonsite`) | SIG-719 Contrato | F1, F2 |
| D-6 | CONFIRMED | `DiscoveryContractPublisher` vive en el SDK; el CP sólo aporta `DiscoveryContractProvider` | SIG-719 DD-9 | F1 |
| D-7 | CONFIRMED | El bus sale en la línea del modelo Discovery V2 (Boot 4.1.1 + Jackson 3) | SIG-719 DD-7 | F1 |
| D-8 | CONFIRMED | Discovery es el único cliente; nada existente se migra | SIG-718 Fuera de Alcance | F1, F2 |
| D-9 | TECHNICAL_RESOLUTION | Rama del SDK desde `origin/feature/discovery-v2-05-contract-hasher` @ `35b1a43`, la cabeza de la pila V2 | `HEAD` | F1 |
| D-10 | TECHNICAL_RESOLUTION | Corrección manual sólo en `BigQueueClientImpl`: usar `producerBuilder.build()` conservando segmento y buffering; mantener `version`, sin cambios en `ProducerFactory`. Reemplaza el cherry-pick previsto de `c67d65e`/`f1194a4` | 2026-10-27: autorización explícita del owner en el chat ante `PLAN_CONFLICT` | F1 |
| D-11 | TECHNICAL_RESOLUTION | En playmaker, `rio.bus.segment-id` toma el valor de `bigqueue.segment` del mismo perfil | `CONTRACT` yml de playmaker | F2 |
| D-12 | TECHNICAL_RESOLUTION | Hasta que exista la ingesta de SIG-671, `DiscoveryBusProcess.run` registra la recepción en log (`component_type`, `contract_version`, `producer.service_name`) y no persiste | SIG-719 "rio-playmaker"; SIG-671 sin implementar | F2 |
| D-13 | TECHNICAL_RESOLUTION | Versiones de prueba `0.0.N-rio-bus`, CHANGELOG bajo `[Unreleased]`, push de la rama sin PR | Policy del owner | F1, F2 |

## Puntos de control humanos

| ID | Qué | Quién | Habilita |
|---|---|---|---|
| H-1 | Tópico `rio-bus` (segmentos `nonprod`, `nonsite`) y consumer de playmaker del scope de test con filtro `scope:<scope>` hacia `POST /rio-bus` | Owner, en Fury | F3 |
| H-2 | Versión de prueba del SDK que trae el bus y `DiscoveryMessageReader` con entrada JSON (DD-8) | Brenda + owner | F2 |
| H-3 | rio-controlplane-kafka desplegado en test con su `DiscoveryContractProvider` y el bloque `rio.bus` | Brenda | F3 |
| H-4 | rio-playmaker de la rama `feature/rio-bus` desplegado en el scope de test | Owner | F3 |

## Gates

| Gate | estado | responsabilidad del agente de fase | evidencia de aceptación del owner | habilita |
|---|---|---|---|---|
| G0 | accepted | — | 2026-10-27: el owner confirma en el chat «Sí, acepto G0 y autorizo F1» | F1 |
| G1 | pending | Dejar `review` con la evidencia de F1 | SHA pusheado, salida de los gates, coverage y versión de prueba | H-2, F2 |
| G2 | pending | Dejar `review` con la evidencia de F2 | SHA pusheado, gates y Lore del repo, coverage | H-4, F3 |
| G3 | pending | Dejar `review` con la evidencia de F3 | Logs de playmaker y del CP en test | Cierre |

## Paquetes autónomos

### Paquete autónomo Fase 1 — rio-sdk-events: bus y publicación de Discovery

**Misión exacta**

Agregar a rio-sdk-events los paquetes `bus` y la publicación de Discovery de SIG-719, corregir el segmento de `BigQueueClientImpl` y publicar la versión de prueba `0.0.1-rio-bus`.

**Precondiciones verificables**

- G0 aceptado en la tabla de gates de `VAULT_ROOT/10-projects/Meli/SIG-659 — Discovery & CLI/agentes/SIG-659 — RIO Bus (implementación).md`.
- `git fetch origin` hecho y `origin/feature/discovery-v2-05-contract-hasher` resuelve a `35b1a43` o a un descendiente.

**Lectura obligatoria**

- SIG-719 completa (`spellbook specs view 7655389d-e1e5-44aa-b89b-12b9d947b4c4`) y SIG-718 (`spellbook specs view 84d44553-1e04-4cdb-bd73-f15a2f1fa635`).
- Este proyecto: Alcance, Registro de decisiones y este paquete.
- Repo: `CLAUDE.md`, `AGENTS.md` y la regla que referencia, `CODING_GUIDELINES.md`.
- Código: `BigQueueClient`, `BigQueueClientImpl`, `BigQueueClientFactory`, `BigQueueTopicProperties`, `RioStreamsAutoConfiguration`, `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`, `DiscoveryContractMessage`, `DiscoveryContractWriter`, y los commits `c67d65e` y `f1194a4`.

**Decisiones cerradas**

D-1 a D-10 y D-13. No hay decisiones de diseño abiertas en esta fase.

**Implementación paso a paso**

1. Crear un worktree fuera del clone actual con `git worktree add ../rio-sdk-events-rio-bus -b feature/rio-bus origin/feature/discovery-v2-05-contract-hasher`. No tocar el clone existente (tiene cambios del owner).
2. Corrección manual autorizada por D-10 sólo en `BigQueueClientImpl`: usar el builder configurado, conservar `version` y `ProducerFactory`. Adaptar y correr tests que prueben segmento y buffering.
3. Crear el paquete `bus` con las firmas exactas de SIG-719 "Contrato": `RioBusMessage`, `RioBusPublisher`, `RioBusProcess`, `RioBusRejectedException`, `RioBusPublishException`, `RioBusOutcome`, `RioBusReader`, `RioBusController`, `RioBusProperties`, `RioBusAutoConfiguration`.
4. `RioBusReader`: validaciones en el orden de SIG-719 y outcomes de su tabla de errores; claves duplicadas rechazadas al parsear; body entregado a `parse` como texto JSON.
5. `RioBusController`: `POST /rio-bus`, body `byte[]`, outcome → HTTP según DD-5.
6. Crear `DiscoveryContractProvider` y `DiscoveryContractPublisher` en el paquete `discovery`, con `PROCESS = "discovery"` y el manejo de fallos de SIG-719.
7. Registrar `RioBusAutoConfiguration` en `AutoConfiguration.imports` con las condiciones de SIG-719; Spring Web como `compileOnly` en `build.gradle`.
8. Tests de la tabla "Tests" de SIG-719 para el SDK.
9. Gates: `./gradlew check`, `./gradlew test`, `./gradlew jacocoTestCoverageVerification`. El código nuevo llega a 95% de coverage cubriendo primero los caminos de la tabla de errores.
10. Entrada en `CHANGELOG.md` bajo `[Unreleased]`.
11. Commit, `git push -u origin feature/rio-bus` y versión de prueba `0.0.1-rio-bus` desde esa rama (spike 2 si no está claro el comando).
12. Escribir la evidencia en este proyecto y dejar G1 en `review`.

**Archivos esperados**

- create: los 12 archivos de `bus/` y `discovery/` que lista SIG-719 "Archivos nuevos" para rio-sdk-events.
- modify: `BigQueueClientImpl.java` (corrección manual autorizada por D-10), `AutoConfiguration.imports`, `build.gradle`, `CHANGELOG.md`.
- tests: un test por clase nueva con lógica (`RioBusPublisher`, `RioBusReader`, `RioBusController`, `DiscoveryContractPublisher`, `RioBusAutoConfiguration`) más un test de integración publisher → push → controller → process. Presupuesto: 16 archivos de código y 8 de tests como máximo.

**No tocar**

- Clases del modelo Discovery V2, linter, validador, writer, hasher y sus tests.
- APIs existentes de `bigqueue/` y `streams/`, salvo la corrección interna de `BigQueueClientImpl` autorizada por D-10.
- `version` de `build.gradle`, otras ramas, PRs, versiones productivas.

**Spikes permitidos**

- Spike 1: si `BigQueueClientFactory` sólo crea clientes desde `events.bigqueue.topics`, construir el `BigQueueClient` del bus desde `rio.bus.topic` y `rio.bus.segment-id` con las clases existentes (`BigQueueTopicProperties`, `BigQueueClientImpl`), sin agregar configuración nueva. Salida: una línea en la Bitácora con la forma elegida.
- Spike 2: confirmar en el historial del repo o en `.fury` cómo se publicaron versiones de prueba anteriores. Salida: el comando usado.
- Cualquier otra duda de arquitectura es `PLAN_CONFLICT`: se detiene el paso y se anota en la Bitácora.

**Tests y asserts**

- El mensaje publicado tiene los cuatro atributos y los filtros son exactamente `["process:<process>", "scope:<rio.bus.scope>"]`.
- Cada fila de la tabla de errores de SIG-719 produce su outcome y su HTTP.
- Dos processes en la misma app reciben cada uno sólo sus mensajes por `POST /rio-bus`; dos con el mismo nombre fallan el arranque.
- El body que recibe `parse` es el JSON del body publicado, sin el envelope.
- `DiscoveryContractPublisher` publica un mensaje por contrato válido con `process = discovery`; un contrato inválido o un fallo de BigQueue no corta el resto ni el arranque.
- El producer de `BigQueueClientImpl` lleva el segmento configurado.
- Ningún log ni tag contiene el body.

**Entregables/Gate G1**

- SHA de `feature/rio-bus` pusheado, salida de los tres comandos de gate, coverage del código nuevo, versión de prueba creada y `git diff --stat` contra la base dentro del presupuesto.

**Handoff a Fase 2**

- Versión de prueba del SDK y SHA. La API es la de SIG-719 sin cambios; si un spike cambió algo, queda en la Bitácora con el motivo.

### Paquete autónomo Fase 2 — rio-playmaker: process discovery

**Misión exacta**

Suscribir rio-playmaker al bus con el process `discovery` de SIG-719, sin persistir contratos (D-12).

**Precondiciones verificables**

- G1 aceptado y H-2 cumplido: existe una versión de prueba del SDK con el bus y `DiscoveryMessageReader` con entrada JSON. La anota el owner en la Bitácora de `VAULT_ROOT/10-projects/Meli/SIG-659 — Discovery & CLI/agentes/SIG-659 — RIO Bus (implementación).md`.

**Lectura obligatoria**

- SIG-719 secciones "Cambios por repo → rio-playmaker", "Manejo de errores" y "Tests".
- Este proyecto: Registro de decisiones y este paquete.
- Repo: `AGENTS.md`, `docs/architecture.md`, `testing.md`, `testing-scenarios.md`, `.grimoire/policy.json` y la regla Java que indica `CLAUDE.md`.
- Código: `config/SecurityConfig`, `config/ControllerExceptionHandler`, `config/ObjectMapperConfig`, el bloque `bigqueue:` de cada `application*.yml` y la dependencia `rio-sdk-events` de `build.gradle`.

**Decisiones cerradas**

D-4, D-5, D-8, D-11, D-12 y D-13.

**Implementación paso a paso**

1. Worktree: `git worktree add ../rio-playmaker-rio-bus -b feature/rio-bus origin/develop`. No tocar el clone existente.
2. Subir `rio-sdk-events` a la versión de prueba de H-2.
3. Crear `bus/DiscoveryBusProcess` (`name() = DiscoveryContractPublisher.PROCESS`, `parse` con `DiscoveryMessageReader`, `run` según D-12).
4. Agregar `/rio-bus` a `permitAll` en `SecurityConfig`.
5. Bloque `rio.bus` en cada perfil que hoy declara `bigqueue.segment`: `topic: rio-bus`, `scope: ${SCOPE}`, `segment-id` igual a `bigqueue.segment` (D-11).
6. Test de integración `POST /rio-bus` con un contrato válido y uno inválido, y los escenarios Lore que exija `.grimoire/policy.json`.
7. Gates del repo según `AGENTS.md` y `testing.md`, incluido el hook de pre-push. Coverage del código nuevo según el repo (95%).
8. Commit y `git push -u origin feature/rio-bus`. Sin PR.
9. Escribir la evidencia en este proyecto y dejar G2 en `review`.

**Archivos esperados**

- create: `bus/DiscoveryBusProcess.java`, su test unitario, un test de integración y los escenarios Lore que pida la policy.
- modify: `SecurityConfig.java`, los `application*.yml` con `bigqueue.segment`, `build.gradle`. Presupuesto: 3 archivos de código, los yml y 3 de tests más los Lore.

**No tocar**

- Controllers, consumers y producers existentes (`/events/**`), `ComponentTypeRegistryService*` y el registry, cualquier persistencia, `ObjectMapperConfig`.

**Spikes permitidos**

- Spike 3: confirmar que agregar el SDK con Jackson 3 no cambia los message converters HTTP de playmaker (por ejemplo, que un endpoint existente sigue serializando igual). Si cambian, `PLAN_CONFLICT`.

**Tests y asserts**

- `POST /rio-bus` con un contrato válido de `scope` propio responde 200 y `run` registra `component_type`, `contract_version` y `producer.service_name`.
- Un contrato inválido responde 200 con `REJECTED` y el log no contiene el body.
- Un `scope` ajeno responde 200 con `SCOPE_MISMATCH` y no llama a `run`.
- `/rio-bus` responde sin token de Tiger; los demás paths mantienen su seguridad.

**Entregables/Gate G2**

- SHA pusheado, salida de los gates y del pre-push, coverage del código nuevo, escenarios Lore y `git diff --stat` dentro del presupuesto.

**Handoff a Fase 3**

- SHA desplegable y lista de los logs que deja `run`, para buscarlos en test.

### Paquete autónomo Fase 3 — Verificación en el scope de test

**Misión exacta**

Demostrar E2E-1 de SIG-718 en el scope de test: los contratos que publica rio-controlplane-kafka al arrancar llegan al process `discovery` de playmaker.

**Precondiciones verificables**

- G2 aceptado y H-1, H-3 y H-4 cumplidos, anotados por el owner en la Bitácora de `VAULT_ROOT/10-projects/Meli/SIG-659 — Discovery & CLI/agentes/SIG-659 — RIO Bus (implementación).md`.

**Lectura obligatoria**

- SIG-718 E2E-1 y CA-1, CA-2, CA-9; SIG-719 "Observabilidad".
- Handoff de F2.

**Decisiones cerradas**

D-4, D-12.

**Implementación paso a paso**

1. Con `fury logs` del scope de test de rio-controlplane-kafka, ubicar el arranque y el resultado de publicar cada contrato.
2. Con `fury logs` del scope de test de playmaker, ubicar `process=discovery outcome=PROCESSED` y el log de `run` para cada `component_type` publicado.
3. Si falta un contrato, registrar el outcome que aparece (`SCOPE_MISMATCH`, `REJECTED`, `INVALID_MESSAGE`) y detenerse.
4. Escribir la evidencia en este proyecto y dejar G3 en `review`.

**Archivos esperados**

- Ninguno en los repos. Sólo este proyecto.

**No tocar**

- Infraestructura de Fury, deploys, configuración de las apps y código.

**Spikes permitidos**

- Ninguno.

**Tests y asserts**

- Cada `component_type` que publica el CP aparece una vez como `PROCESSED` en playmaker en la ventana del arranque.
- Ningún log contiene el body.

**Entregables/Gate G3**

- Extractos de log con timestamp, scope y `component_type`, sin payloads.

**Handoff**

- Resultado para el cierre del owner: el bus queda listo para que SIG-671 reemplace el cuerpo de `run`.

## ✅ Tareas

> [!note]+ Ownership y tarea puente
> `#owner/me` = tuya · `#owner/agent` = de un agente · sin owner = clasifícala.
> El board es **adaptativo según `owner` del frontmatter**:
> - **Proyecto humano** (`owner: me`): muestra tus tareas y las **tareas puente** (`#type/supervision`) que representan proyectos de agente. Las tareas de agente **no** aparecen acá; viven en su propio proyecto.
> - **Proyecto de agente** (`owner: agent`): muestra las tareas del agente.

> [!example]- Fuente de tareas — editar / mover de estado aquí
> %% Estados: [ ] To Do · [/] WIP · [r] Review · [x] Done · [-] Canceled. Owners: #owner/me, #owner/agent. Tipos: #type/dev #type/admin #type/research #type/pr-review #type/supervision. Flags: #blocked #waiting #urgent. Ver [[convenciones]]. %%
> - [r] T1.1 Worktree `feature/rio-bus` desde la base V2 y fix manual de segmento autorizado por D-10 con sus tests #owner/agent #type/dev #area/meli
> - [r] T1.2 Paquete `bus`: mensaje, publisher, process, excepciones y outcome con las firmas de SIG-719 #owner/agent #type/dev #area/meli
> - [r] T1.3 `RioBusReader` y `RioBusController` con la tabla de errores de SIG-719 #owner/agent #type/dev #area/meli
> - [r] T1.4 `DiscoveryContractProvider` y `DiscoveryContractPublisher` #owner/agent #type/dev #area/meli
> - [r] T1.5 `RioBusAutoConfiguration`, `AutoConfiguration.imports` y `build.gradle` #owner/agent #type/dev #area/meli
> - [/] T1.6 Tests, gates, CHANGELOG, push y versión `0.0.1-rio-bus`; G1 en review #owner/agent #type/dev #area/meli
> - [ ] T2.1 Worktree `feature/rio-bus` desde `origin/develop` y SDK en la versión de H-2 #owner/agent #type/dev #area/meli
> - [ ] T2.2 `DiscoveryBusProcess`, `permitAll` de `/rio-bus` y bloque `rio.bus` por perfil #owner/agent #type/dev #area/meli
> - [ ] T2.3 Tests, Lore, gates y push; G2 en review #owner/agent #type/dev #area/meli
> - [ ] T3.1 Verificar E2E-1 con logs del scope de test; G3 en review #owner/agent #type/research #area/meli
> - [ ] Aceptar G0 y despachar F1 #owner/me #type/supervision #area/meli
> - [ ] H-1 Crear el tópico `rio-bus` y el consumer de playmaker del scope de test #owner/me #type/admin #area/meli
> - [ ] H-2 Versión de prueba del SDK con el bus y `DiscoveryMessageReader` (con Brenda) #owner/me #type/supervision #area/meli
> - [ ] H-3 CP Kafka con `DiscoveryContractProvider` desplegado en test (Brenda) #owner/me #type/supervision #area/meli
> - [ ] H-4 Desplegar playmaker `feature/rio-bus` en test #owner/me #type/admin #area/meli

```dataviewjs
const meta={" ":["To Do","var(--text-muted)","var(--background-modifier-border)"],"/":["WIP","#ba7517","rgba(234,124,12,.18)"],"r":["Review","#185fa5","rgba(55,138,221,.18)"],"x":["Done","#3b6d11","rgba(99,153,34,.18)"],"X":["Done","#3b6d11","rgba(99,153,34,.18)"],"-":["Canceled","var(--text-faint)","var(--background-modifier-border)"]};
function linkify(s){return String(s).replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g,(m,a,b)=>`<a class="internal-link" href="${a}" data-href="${a}">${b||a}</a>`).replace(/#[\w/-]+/g,m=>`<span style="opacity:.55;font-size:12px">${m}</span>`).replace(/📅\s*(\d{4}-\d{2}-\d{2})/g,(m,d)=>`<span style="opacity:.7;font-size:12px">📅 ${d}</span>`).replace(/[⏫🔼🔽⏬🔺]/g,"").replace(/✅\s*(\d{4}-\d{2}-\d{2})/g,"");}
function has(t,tag){return new RegExp(`(^|\\s)#${tag}(\\s|$)`).test(String(t.text));}
function render(tasks){const el=dv.el('div','');el.innerHTML=tasks.map(t=>{const[label,fg,bg]=meta[t.status]||["?","var(--text-muted)","var(--background-modifier-border)"];return `<div style="display:flex;align-items:center;gap:8px;margin:5px 0;"><span style="font-size:11px;font-weight:600;padding:1px 9px;border-radius:999px;background:${bg};color:${fg};min-width:56px;text-align:center;flex:none;">${label}</span><span>${linkify(t.text)}</span></div>`;}).join("");}
function board(tasks){const cols=[[" ","🟦 To Do"],["/","🟡 WIP"],["r","🔵 Review"]];let any=false;for(const[st,label]of cols){const c=tasks.filter(t=>t.status===st);if(c.length){any=true;dv.el('h4',label);render(c);}}const done=tasks.filter(t=>t.status==="x"||t.status==="X");if(done.length){any=true;dv.el('h4',"✅ Done");render(done);}if(!any)dv.paragraph("_Sin tareas._");}
const owner=((dv.current().owner)==="agent")?"agent":"me";
const all=dv.current().file.tasks.array();
const primary=all.filter(t=>has(t,`owner/${owner}`));
const loose=all.filter(t=>!has(t,"owner/me")&&!has(t,"owner/agent"));
dv.header(3, owner==="agent"?"🤖 Tareas del agente":"🧍 Mis tareas");
board(primary);
if(loose.length){dv.header(3,"🧺 Sin owner (clasificar)");render(loose);}
```

## Despachos copiables

El prompt común lo entrega el owner en el chat junto con un solo despacho; no se guarda en el vault ni en los repos.

**Despacho Fase 1**

```text
FASE_ASIGNADA=1
PAQUETE_CANONICO=Paquete autónomo Fase 1 — rio-sdk-events: bus y publicación de Discovery
GATE_REQUERIDO=G0 accepted
TAREAS=T1.1-T1.6
SALIDA=feature/rio-bus pusheada en rio-sdk-events, versión 0.0.1-rio-bus, evidencia en este proyecto
STOP=G1 en review; prohibido empezar F2
```

**Despacho Fase 2**

```text
FASE_ASIGNADA=2
PAQUETE_CANONICO=Paquete autónomo Fase 2 — rio-playmaker: process discovery
GATE_REQUERIDO=G1 accepted y H-2 anotado
TAREAS=T2.1-T2.3
SALIDA=feature/rio-bus pusheada en rio-playmaker, evidencia en este proyecto
STOP=G2 en review; prohibido empezar F3
```

**Despacho Fase 3**

```text
FASE_ASIGNADA=3
PAQUETE_CANONICO=Paquete autónomo Fase 3 — Verificación en el scope de test
GATE_REQUERIDO=G2 accepted y H-1, H-3, H-4 anotados
TAREAS=T3.1
SALIDA=extractos de log en este proyecto
STOP=G3 en review; el cierre es del owner
```

## 📆 Bitácora

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-10-27** — Cierre de la ejecución reanudada: aplicados `agents-os-session-close` y `agents-os-session-feedback` desde la raíz absoluta del vault resuelta para esta sesión, con modelo exacto `gpt-6.1-sol` y superficie `[[Codex]]`. Continuidad y feedback se consolidan aquí por la prohibición explícita de crear archivos de evidencia; `agents-os-agent-run-register` revisado, sin materializar registro separado por esa misma instrucción. Segmento atribuible: implementación/testing, resultado código pusheado y verificado, publicación pendiente por contradicción del plan, evaluator agent, user_rework unknown. Feedback: el preflight evitó cambios de API/version no autorizados; pruebas críticas detectaron y eliminaron fuga heredada del body; hooks completos requirieron ajustes de calidad y pasaron sin bypass. Fricción pendiente: el paquete pide una versión de prueba mientras prohíbe escribir la versión que Fury requiere. Eficiencia REVIEW, high-water mark unknown; mejora concreta: confirmar el mecanismo de versión de librerías en el paquete antes del despacho. Sin nuevos artefactos, sin cierre del proyecto, sin aceptar G1 ni empezar F2.
- **2026-10-27** — Commit y push F1: `df9ef57bb09ac349a06e4a4bc9e13c000e249c2f` (`Add RIO Bus and Discovery startup publishing`), `git push -u origin feature/rio-bus` exit 0; sin PR. `pre-commit run --hook-stage post-commit` exit 0: notificación Websec y metadata Datasec PASS; formatter/Checkstyle/PMD sin archivos en esa etapa, ya PASS antes del commit. `git status --porcelain=v1` vacío en el worktree. `git diff 35b1a43 --stat`: **24 files changed, 1178 insertions(+), 21 deletions(-)**; 16 código/config/CHANGELOG y 8 tests. Gates finales: `./gradlew check` PASS, `./gradlew test` PASS (2.496/0 fallos/0 errores/0 omitidos), `./gradlew jacocoTestCoverageVerification` PASS, `./gradlew jacocoTestReport` PASS, con JDK25. Reporte final de clases nuevas: líneas 123/123 (100%), ramas 22/22 (100%), instrucciones 580/582 (99,66%); fix de BigQueue también cubierto directamente. Versión de prueba **no creada**: `version` conserva `1.5.0` por la restricción vigente, nunca publicada; pendiente resolver spike 2. G1 no pasa a review sin ese entregable.
- **2026-10-27** — Gates finales previos al commit: `JAVA_HOME=<JDK25> ./gradlew check` exit 0 (`BUILD SUCCESSFUL in 27s`), `./gradlew test` exit 0 (`25s`, suite completa), `./gradlew jacocoTestCoverageVerification` exit 0 (`780ms`) y `./gradlew jacocoTestReport` exit 0 (`773ms`). `pre-commit run --files <24 archivos del cambio>` exit 0: Websec, Datasec, formatter, Checkstyle y PMD PASS sin desactivar hooks ni reglas. Los intentos previos señalaron sólo formato/Javadoc/literales y preservación de API/seguridad; corregidos con cambios acotados. Cobertura directa de las dos nuevas líneas de `BigQueueClientImpl` desde `test.exec`: builder 4/4 instrucciones y log filtrado 5/5 instrucciones, ambas 100%, sin cambiar exclusiones. Presupuesto comprobado: 24 archivos totales = 16 código/config/CHANGELOG + 8 tests. T1.1–T1.5 pasan a `[r]`; T1.6 sigue `[/]`. Preflight de existencia `fury versions list --search 0.0.1-rio-bus --limit 20 --output json` devuelve exit 3, «No versions found for repository: fury_rio-sdk-events», sin crear ni modificar versiones.
- **2026-10-27** — Gate parcial F1: `JAVA_HOME=<JDK25> ./gradlew check jacocoTestReport` exit 0, `BUILD SUCCESSFUL in 25s`, 2.496 tests, 0 fallos, 0 errores, 0 omitidos. Incluye PASS del test de no filtración del transporte tras corregir el log y del test de publicación sin Spring Web. JaCoCo de los 12 archivos nuevos: líneas 121/121 (100%), ramas 22/22 (100%), instrucciones 580/582 (99,66%); dos instrucciones pendientes son el fallback de registry de la auto-configuración, sin impacto en el piso 95%. `BigQueueClientImpl` está excluido por el reporte heredado: sus nuevas líneas se comprobarán directamente desde `test.exec`, sin alterar exclusiones. Hooks completos del repo en ejecución; `./gradlew test` y `./gradlew jacocoTestCoverageVerification` explícitos pendientes antes del commit.
- **2026-10-27** — F1: 12 archivos de SIG-719 implementados, integración Spring Web en `compileOnly`, seis tests nuevos + dos existentes adaptados (máximo ocho). `JAVA_HOME=<JDK25> ./gradlew compileJava` exit 0; suite focalizada bus/Discovery publisher/BigQueue exit 0 después de corregir imports de tests y uso de registry. Prueba adicional `./gradlew test --tests '*BigQueueClientImplTest.filteredPublishNeverLogsTheBodyFromTransportExceptions' --tests '*RioBusAutoConfigurationTest.publishingOnlyDoesNotRequireSpringWeb'` reprodujo fuga heredada de RF-9: primer test FAIL por throwable con body, segundo PASS. Se elimina sólo el throwable del log de `sendWithFilters` en el archivo permitido, sin cambiar API ni el error entregado al caller; revalidación completa en curso. Herramientas MCP `analyze_dependencies`/`get_meli_security_context` exigidas por la regla Java no están expuestas en esta sesión; no se declaran ejecutadas.
- **2026-10-27** — `PLAN_CONFLICT` (spike 2/publicación): `fury versions create --help` y el parser instalado (`furycli/core/helpers/version_parser.py`, `parse_version`) confirman que una librería Java con `build.gradle` usa la versión del archivo, incluso con argumento explícito. El runbook `30-resources/agents/skills/fury-lib-consumer-deploy/SKILL.md` confirma que la versión correcta debe estar en el archivo, commiteada y pusheada. Hoy `version = '1.5.0'`; publicar con ese valor violaría D-13 y el despacho, pero cambiarlo contradice `No tocar version`. Sólo se detiene la publicación; consulta concreta al owner para autorizar `0.0.1-rio-bus`. No se ejecuta ningún create-version que pudiera publicar una versión productiva.
- **2026-10-27** — D-10 resuelto por el owner: «Autorizar corrección manual sólo en BigQueueClientImpl, conservando version». Se actualiza D-10 y su paso/alcance afectados, sin ampliar archivos ni API. `git fetch origin` exit 0; base remota permanece `35b1a43a3a7d0f7134486a6a430eba3561a6825b`, `git merge-base --is-ancestor 35b1a43 origin/feature/discovery-v2-05-contract-hasher` exit 0. Ejecutado el comando exacto del paquete: `git worktree add ../rio-sdk-events-rio-bus -b feature/rio-bus origin/feature/discovery-v2-05-contract-hasher`, exit 0. Worktree externo `rio-sdk-events-rio-bus`, rama `feature/rio-bus`; T1.2–T1.5 en `[/]`.
- **2026-10-27** — Reanudación F1: el owner acepta explícitamente G0 y autoriza F1 en el chat; G0 pasa a `accepted`, conflicto de G0 resuelto. T1.1 pasa a `[/]`; se continúa con fetch/worktree y código independiente. D-10 continúa detenido por el conflicto documentado, con consulta concreta al owner; ningún otro gate aceptado y tarea puente intacta.
- **2026-10-27** — Cierre solicitado: aplicados `agents-os-session-close` y `agents-os-session-feedback` desde `VAULT_ROOT` mediante sus `SKILL.md` canónicos; superficie Codex Desktop, modelo exacto `gpt-6.1-sol` verificado en metadata de la sesión. Continuidad y evidencia sólo en este plan, sin artefactos adicionales por instrucción del despacho. Feedback: la precondición G0 y el análisis del cherry-pick detectaron conflictos antes de modificar el repo; el sandbox devolvió un falso fallo de autenticación resuelto con la CLI fuera del sandbox; lecturas agrupadas demasiado grandes generaron truncado y se corrigieron con consultas enfocadas. Evaluación operativa 3/5; eficiencia REVIEW, high-water mark desconocido. Mejora concreta: filtrar la salida de Spellbook a contenido/estado y acotar cada lectura requerida; impacto medio y riesgo bajo. No se acepta ningún gate ni se inicia F2. Pendiente del owner: G0 y resolución de D-10 frente a los límites del paquete.
- **2026-10-27** — `PLAN_CONFLICT` (T1.1/D-10): `git show --stat c67d65e` y `git show c67d65e -- build.gradle CHANGELOG.md src/main/java/com/mercadolibre/rio/sdk/events/bigqueue/impl/ProducerFactory.java` prueban que el cherry-pick obligatorio agrega `ProducerFactory.createProducer(BigQueueTopicProperties, MQConfiguration)`, depreca la firma anterior, cambia `version` de `1.3.0` a `1.3.1` y agrega un CHANGELOG de release. Contradice `No tocar` (sólo `BigQueueClientImpl` permitido en `bigqueue`, no cambiar `version`, CHANGELOG sólo `[Unreleased]`), la lista de SIG-719 y el presupuesto (12 archivos nuevos + 5 modificados = 17, máximo 16). No se ejecuta el cherry-pick ni se inventa una excepción; la alternativa manual de D-10 está condicionada a que no aplique limpio, aún no comprobado por G0 pendiente. `f1194a4` prueba la nueva sobrecarga de `ProducerFactory`, por lo que también depende de resolver este conflicto.
- **2026-10-27** — Preflight independiente F1: leídas SIG-719 (`7655389d-e1e5-44aa-b89b-12b9d947b4c4`) y SIG-718 (`84d44553-1e04-4cdb-bd73-f15a2f1fa635`), ambas `review`; leídos `AGENTS.md`, `CLAUDE.md`, regla Java, `CODING_GUIDELINES.md` y clases requeridas en la ref V2 local. `spellbook specs view 7655389d-e1e5-44aa-b89b-12b9d947b4c4` falló inicialmente con `zsh:1: command not found: spellbook`; resuelto usando Node y CLI de `~/.nvm/versions/node/v24.19.0/bin`. Dentro del sandbox ambos specs devolvieron «Authentication failed. Check your token or run `spellbook login`.», pero el mismo acceso fuera del sandbox terminó exit 0: no requiere renovar token. Ref local V2 `35b1a43a3a7d0f7134486a6a430eba3561a6825b`; no se ejecutó fetch al estar pendiente G0. Clone preservado, sin worktree ni ramas nuevas; gates/coverage/commit/push/versión/diff de implementación no ejecutados. Spike 1 confirma que `BigQueueClientFactory` busca sólo en `events.bigqueue.topics`; la construcción permitida con `BigQueueTopicProperties` + `BigQueueClientImpl` queda por ejecutar tras resolver los conflictos.
- **2026-10-27** — `PLAN_CONFLICT` (preflight F1): el despacho recibido exige `GATE_REQUERIDO=G0 accepted`, mientras `Gates` mantiene `G0 pending` y el paquete exige aceptación registrada antes del worktree. Se detiene ese paso y se solicita confirmación del owner; G0 no se autoacepta, G1 permanece `pending`, T1.1–T1.6 siguen `[ ]` y la tarea puente no se toca. Continúan lecturas independientes del repo y acceso a las specs.
- **2026-10-27** — Plan creado desde SIG-718/719 (en `review`) con línea base en refs remotas. Tres fases (SDK, playmaker, verificación en test) y cuatro puntos de control humanos. Hallazgos que entran al plan: `DiscoveryMessageReader` no existe todavía en las ramas V2 (H-2) y el fix de segmento está sin mergear en dos commits (D-10).

## 🧭 Decisiones

- Ver [[#Registro de decisiones]].

## 🔗 Docs / Links

- Specs: [SIG-718](https://spellbook.adminml.com/projects/SIG/specs/SIG-718) · [SIG-719](https://spellbook.adminml.com/projects/SIG/specs/SIG-719) · [SIG-644](https://spellbook.adminml.com/projects/SIG/specs/SIG-644) · [SIG-697](https://spellbook.adminml.com/projects/SIG/specs/SIG-697) · [SIG-671](https://spellbook.adminml.com/projects/SIG/specs/SIG-671)
- Proyecto padre: [[SIG-659 — Discovery & CLI]]
- Apps: [[rio-sdk-events]] · [[rio-playmaker]] · [[rio-controlplane-kafka]]
