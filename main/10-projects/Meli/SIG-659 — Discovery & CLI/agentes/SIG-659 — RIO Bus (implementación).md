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
progress: 80
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
updated: "2026-10-28"
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

- **2026-10-28 — F1 entregada y H-2 ampliado; F2 en ejecución.** `rio-sdk-events@feature/rio-bus` pusheada en `7f507839989308ee8178467d97f411337a4d37f1`, base `35b1a43`; worktree limpio. [Versión de prueba 0.0.1-rio-bus](https://web.furycloud.io/rio-sdk-events/versions/detail/0.0.1-rio-bus) publicada y resuelta desde Maven; el backend de builds confirma `finished`, SHA y rama exactos. Tres gates PASS, 2.496 tests sin fallos/errores/omitidos, hooks pre/post-commit PASS. Código nuevo: líneas 123/123 y ramas 22/22 (100%), instrucciones 580/582 (99,66%); 24 archivos dentro del presupuesto (16 + 8).
- **F2 implementada; pendiente de gate retenido/push:** SDK `0.0.2-rio-bus` publicado y verificado en Maven, SHA `4ad071e`, con reader y tipos V1 intactos. Playmaker `feature/rio-bus` en commit local **`960fe1521`**, base `20e0a9109`, worktree limpio; **19 archivos** con ampliación D-15 autorizada. Gates Java/contratos/seguridad/tipos/lint PASS; regresión Java anterior 5.224 tests (3 omitidos heredados) + 64 localTest, suite Lore unitaria final **381/381**. Código Java nuevo: **100% líneas/ramas/instrucciones**. E2E backend real sin UI sobre el SHA final: **237/237 escenarios, 507/507 steps**, PROCESSED/REJECTED/SCOPE_MISMATCH y logs seguros verificados, **CLEANUP_CERTIFIED**, sin recursos propios remanentes. `./local/test-lore.sh --gate` exit 1: `local.adminml.com must resolve only to loopback. Add 127.0.0.1 local.adminml.com to /etc/hosts`; `sudo -n true` exit 1 (`sudo: a password is required`). Pendientes hosts, gate retenido, pre-push/Cleric y push; **G2 pending**, T2.3 `[/]`. G1 conserva `review`; no aceptación automática ni F3/deploy. Tarea puente intacta.

## 🧱 Entrega de desarrollo

| Aplicación / repo | Branch | Base | SPEC funcional | SPEC técnica | Estado |
|---|---|---|---|---|---|
| [`rio-sdk-events`](https://github.com/melisource/fury_rio-sdk-events) | `feature/rio-bus` | `origin/feature/discovery-v2-05-contract-hasher` @ `35b1a43` | [SIG-718 funcional](https://spellbook.adminml.com/projects/SIG/doc/SIG-718) | [SIG-718 técnica](https://spellbook.adminml.com/projects/SIG/doc/SIG-718) | [#64](https://github.com/melisource/fury_rio-sdk-events/pull/64) draft, apilado sobre #56 · [[Descripción PR — rio-sdk-events — RIO Bus]] |
| [`rio-playmaker`](https://github.com/melisource/fury_rio-playmaker) | `feature/rio-bus` | `origin/develop` | [SIG-718 funcional](https://spellbook.adminml.com/projects/SIG/doc/SIG-718) | [SIG-718 técnica](https://spellbook.adminml.com/projects/SIG/doc/SIG-718) | Local `fab68a57f`; push bloqueado por el gate Cleric (falta `.grimoire/lore-readonly.local.json`) · [[Descripción PR — rio-playmaker — RIO Bus]] |

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

**Excepción autorizada 2026-10-28 (D-14):** implementar el reader de SIG-644 con entrada de contrato JSON según DD-8, sus tipos/diagnósticos y tests requeridos, publicar el SDK `0.0.2-rio-bus` y usarlo en F2. El resto de las exclusiones se conserva.

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
| D-13 | TECHNICAL_RESOLUTION | Versiones de prueba `0.0.N-rio-bus`, CHANGELOG bajo `[Unreleased]`, push de la rama sin PR. Excepción F1 autorizada: escribir únicamente `version = '0.0.1-rio-bus'` en `build.gradle` antes de validar, commitear, pushear y publicar con Fury | Policy del owner; excepción confirmada en el chat el 2026-10-28 | F1, F2 |

| D-14 | TECHNICAL_RESOLUTION | El owner pide ejecutar playmaker tras confirmar `0.0.1-rio-bus` y autoriza «Sí, completar el reader y publicar 0.0.2-rio-bus». Se amplía H-2 sólo con `DiscoveryMessageReader` y tipos/tests de SIG-644, entrada JSON de DD-8; versión SDK `0.0.2-rio-bus` en la misma rama. Autoriza luego conservar intactos los cuatro tipos V1 del tag 1.5.0 para no impactar flujos existentes. Autoriza además instalar Grimoire 27.3.0, revisión `d00c6dbdfffe1eea3b531f83cdfc5e9ec145454d`, con los efectos globales y hooks descritos en AGENTS.md | Autorizaciones explícitas del owner en el chat 2026-10-28; G1 no autoaceptado | H-2, F2 |
| D-15 | TECHNICAL_RESOLUTION | Owner autoriza completar el E2E exclusivamente backend: `.lore/scripts/playmaker-e2e.ts` fija `SCOPE=local` sólo en Java aislado y observa outcomes/logs; `.lore/example/backend/playmaker/ui.ts` conecta el callback existente al smoke y `.lore/tests/unit/runner/playmakerUI.node.spec.ts` ajusta el fixture y verifica rechazo de ACK sin procesamiento o fuga de body. Amplía sólo esos archivos existentes y el presupuesto de tests, junto al escenario Lore permitido; sin frontend, cambios productivos, APIs, flags, dependencias ni archivos nuevos | Autorizaciones explícitas del owner en el chat 2026-10-28, incluida «Sí, autorizar ambos ajustes y sus tests» | F2 |

## Puntos de control humanos

| ID | Qué | Quién | Habilita |
|---|---|---|---|
| H-1 | Tópico `rio-bus` (segmentos `nonprod`, `nonsite`) y consumer de playmaker del scope de test con filtro `scope:<scope>` hacia `POST /rio-bus` | Owner, en Fury | F3 |
| H-2 | Versión de prueba del SDK que trae el bus y `DiscoveryMessageReader` con entrada JSON (DD-8); `0.0.2-rio-bus` publicada y verificada (Bitácora 2026-10-28) | Owner delegó implementación al agente | F2 |
| H-3 | rio-controlplane-kafka desplegado en test con su `DiscoveryContractProvider` y el bloque `rio.bus` | Brenda | F3 |
| H-4 | rio-playmaker de la rama `feature/rio-bus` desplegado en el scope de test | Owner | F3 |

## Gates

| Gate | estado | responsabilidad del agente de fase | evidencia de aceptación del owner | habilita |
|---|---|---|---|---|
| G0 | accepted | — | 2026-10-27: el owner confirma en el chat «Sí, acepto G0 y autorizo F1» | F1 |
| G1 | review | F1 entregada: `7f50783` pusheado, gates PASS, cobertura ≥95%, `0.0.1-rio-bus` publicada; evidencia final en Bitácora 2026-10-28 | Pendiente de aceptación del owner; no autoaceptado | H-2, F2 |
| G2 | pending | F2 local `960fe1521`; E2E backend completo PASS, gate retenido/pre-push/push detenidos por hosts | Gates/coverage PASS; `--gate` exit 1 por loopback, sudo sin contraseña no disponible (Bitácora 2026-10-28); aceptación pendiente | H-4, F3 |
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
- `version` de `build.gradle`, salvo escribir `0.0.1-rio-bus` en F1 por la excepción explícita de D-13; otras ramas, PRs, versiones productivas.

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
- modify: `SecurityConfig.java`, los `application*.yml` con `bigqueue.segment`, `build.gradle`. Presupuesto: 3 archivos de código, los yml y 3 de tests más los Lore. Excepción D-15: modificar además los tres archivos existentes del runner/worker/test allí enumerados para scope/observación/conexión y fixture del E2E backend (4 archivos de tests en total).

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
> - [r] T1.6 Tests, gates, CHANGELOG, push y versión `0.0.1-rio-bus`; G1 en review #owner/agent #type/dev #area/meli
> - [r] T2.1 Worktree `feature/rio-bus` desde `origin/develop` y SDK en la versión de H-2 #owner/agent #type/dev #area/meli
> - [r] T2.2 `DiscoveryBusProcess`, `permitAll` de `/rio-bus` y bloque `rio.bus` por perfil #owner/agent #type/dev #area/meli
> - [/] T2.3 Tests, Lore, gates y push; G2 en review #owner/agent #type/dev #area/meli
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

- **2026-10-28** — D-15 / E2E backend final **PASS** sobre **`960fe1521df7d9feb8858ea1caae44b9bd7eb9e4`**, SDK publicado **`0.0.2-rio-bus@4ad071e`**. `DOCKER_CONFIG=<config local temporal> ./local/test-lore.sh` **exit 0**, run **`run_mvsm856f2ae9aada8f`**, **237/237 escenarios y 507/507 steps**, 0 fallos/bloqueados/omitidos seleccionados, 0 tokens/coste, gate nativo aprobado, 0 requests a providers inesperados; runtime real playmaker + MySQL, sin servidor web ni navegador. Evidencia nativa de `step-8-assertions.json`: outcomes exactos **PROCESSED / REJECTED / SCOPE_MISMATCH**, identidad única exacta y **`body_logged=false`**, todos PASS; no se infiere procesamiento de HTTP 200. Worker-ready 49s, native-run 121s, cleanup 90s **CLEANUP_CERTIFIED**. Verificación posterior por etiqueta: 0 contenedores, volúmenes y redes propios. Los 179 contratos heredados bloqueados del catálogo siguen fuera de la selección y no se declaran resueltos. SHA local limpio; `git diff 20e0a91094fd827962932ebb4fead35a44c1184b --stat`: **19 files changed, 645 insertions(+), 71 deletions(-)**, dentro del presupuesto ampliado D-15. Cobertura Java nueva **12/12 líneas, 2/2 ramas, 45/45 instrucciones (100%)**; los controles del runner se verifican por sus tests y la ejecución nativa, sin atribuirles una cifra JaCoCo. SDK sin cambios ni nueva publicación requerida.

- **2026-10-28** — Paso de push detenido sobre el SHA final: `DOCKER_CONFIG=<config temporal> ./local/test-lore.sh --gate` **exit 1**, error textual **`local.adminml.com must resolve only to loopback. Add 127.0.0.1 local.adminml.com to /etc/hosts`**. `sudo -n true` **exit 1**, **`sudo: a password is required`**. No se modifica `/etc/hosts`, no se inicia otro runtime y no se omite el requisito. El servidor es de Lore para revisión independiente, no un frontend del producto. Pendiente acción del owner en hosts, ejecutar el gate retenido y el pre-push normal (incluidos Cleric y Git E2E de tooling), luego push y G2 en review. Hasta entonces **rama de playmaker sin push, pre-push/Cleric sin ejecutar, T2.3 [/], G2 pending**; no se declara aceptación ni se empieza F3. Clones del owner intactos: SDK `ad2c98b` con `graphify-out/`; playmaker `3433fc12b` con `graphify-out/` y `scripts/inactivate-probe/`; worktrees SDK `4ad071e` y playmaker `960fe1521` limpios.

- **2026-10-28** — Cierre operativo por delta y feedback explícitamente solicitados: aplicados `agents-os-session-close` y `agents-os-session-feedback` desde la raíz absoluta del vault, modelo exacto **`gpt-6.1-sol`**, superficie `[[Codex]]`. Continuidad, segmento atribuible de implementación/testing y evaluación quedan sólo en esta Bitácora por la restricción del owner; sin archivos L0/L1/feedback/agent_run adicionales ni memoria pública nueva. Resultado del segmento: E2E backend completo en commit local y gate de push detenido por prerrequisito local, no F2 cerrada. Feedback del agente: memoria/continuidad 4/5, skills 3/5, herramientas 4/5; la solicitud inicial de excepción quedó corta por no revisar de una vez el callback compartido y su fixture unitario. Mejora concreta: inspeccionar wiring y tests del runner antes de fijar el presupuesto de una excepción. Se corrigieron los asserts unitarios sin debilitar reglas ni gate; no se presenta un ACK como procesamiento. Próximo paso: hosts del owner → gate retenido sobre `960fe1521` → push normal con Cleric → evidencia/G2 review; no F3.

- **2026-10-28** — E2E backend D-15 en commit local **`960fe1521df7d9feb8858ea1caae44b9bd7eb9e4`** (`Verify Discovery processing in backend E2E`), worktree limpio, todavía sin push. Gates finales: `JAVA_HOME=<JDK25> SCOPE=local ./gradlew check test jacocoTestReport` PASS (11 tareas UP-TO-DATE, 1s; no cambios Java desde la regresión completa anterior); `node .lore/scripts/lore.mjs --lore <engine fijado> unit` PASS **381/381 en 18 archivos**, typecheck PASS, ESLint de los tres archivos TS PASS (0 errores, 27 warnings de patrones existentes/IO local; sin desactivar reglas), Prettier PASS; `./scripts/run-agentic-testing-contract.sh` PASS (10 sources/18 commands/12 documents), `git diff --cached --check` PASS, dispatcher `grimoire-hooks verify` PASS. Websec/Datasec explícitos PASS sobre los cuatro archivos; Java formatter/Checkstyle/PMD no aplican a este delta. Commit propio no publicado enmendado sólo para quedar después de esos checks. Cobertura Java nueva conservada: 12/12 líneas, 2/2 ramas, 45/45 instrucciones, 100%. Diff acumulado contra base `20e0a9109`: **19 files changed, 645 insertions(+), 71 deletions(-)** (ampliación D-15 autorizada). Preflight Lore PASS en engine/Node24/JDK25/Docker; conserva requisito de hosts para `--gate`. Se inicia `DOCKER_CONFIG=<config temporal> ./local/test-lore.sh` sin UI sobre este SHA final; no se declara su resultado aún. T2.3 [/], G2 pending, sin push/F3.

- **2026-10-28** — Owner autoriza ambos ajustes adicionales y sus tests: resuelto el `PLAN_CONFLICT` de conexión/fixture en D-15. Se conecta el callback existente para smoke sin nuevos APIs; el runner evita buscar ese ID en el catálogo de fixtures y observa sólo sus logs desde la preparación. El test unitario diferencia `/ping`, POST `/rio-bus` y paths privados, y exige que un ACK con SCOPE_MISMATCH en el caso válido o fuga del body bloquee el candidato. Se repiten typecheck, unit, lint, contratos y gates aplicables antes del commit y de la ejecución nativa sobre el SHA final.

- **2026-10-28** — Verificación del borrador D-15: comando oficial `node .lore/scripts/lore.mjs --lore <engine fijado> unit` **exit 1, 378 PASS / 1 FAIL**. Error textual: `Gate candidate contains incomplete or failed evidence` en el test `creates an explicit canonical candidate suite and reserves the live runtime for Cleric`; su servidor unitario contesta `pong` a todos los métodos/paths y no provee el nuevo probe. Hace falta ajustar únicamente ese fixture en `.lore/tests/unit/runner/playmakerUI.node.spec.ts` junto al worker ya identificado. Se precisa la consulta al owner con los dos archivos y la ampliación de tests; reemplaza la consulta anterior incompleta. No se modifican aún esos archivos ni se crea un commit incompleto. ESLint detectó un único error de espaciado en el runner, corregido; warnings de filesystem dinámico acordes al patrón del runner, sin desactivar reglas.

- **2026-10-28** — D-15 implementada en borrador: scope del Java aislado fijado en `local`; probe sólo del escenario Discovery, lectura desde el inicio del escenario y salida de outcomes/contadores/boolean de fuga (sin publicar logs ni body); escenario exige PROCESSED, REJECTED, SCOPE_MISMATCH, identidad exacta única y ausencia de body. Typecheck y parser nativo PASS, formato aplicado. `PLAN_CONFLICT` de conexión: `.lore/example/backend/playmaker/ui.ts::forTarget` retorna sólo `capabilities: [http]` para `kind=smoke`, por lo que no llama al callback existente del runner; éste además supone un caso del catálogo para todos los IDs. La excepción inicial de un único archivo no cubre ese worker. Se solicita ampliar sólo a ese segundo archivo existente para compartir el callback ya presente con el smoke; no nuevo API, frontend ni archivos. La ejecución nativa dependiente queda detenida hasta esa autorización, mientras se verifican los tests existentes.

- **2026-10-28** — Owner resuelve el `PLAN_CONFLICT` de E2E con D-15: autoriza el único archivo de runner existente y el escenario para observar procesamiento/rechazo/scope/logs de la aplicación empaquetada, sin frontend ni cambios productivos. T2.3 continúa `[/]`; se implementa y valida la excepción antes de un nuevo commit. El servidor MCP de release-process no está disponible en las herramientas/recursos de esta sesión; los comandos canónicos de AGENTS.md siguen siendo los gates aplicables.

- **2026-10-28** — E2E backend oficial sin UI: `DOCKER_CONFIG=<config local temporal> ./local/test-lore.sh` **PASS**, exit 0, sobre playmaker `2741dbeeb`. Run nativo **`run_mvslgxsd4ec172e8f9`**: **237/237 escenarios y 506/506 steps**, 0 fallos/bloqueados/omitidos seleccionados, 0 tokens/coste, gate nativo aprobado; runtime L0 real playmaker + MySQL, tareas originales `localTest` y `test` compiladas y ejecutadas offline con red sólo loopback, 0 requests a providers inesperados. Worker-ready 56s, native-run 121s, cleanup 90s **CLEANUP_CERTIFIED**. Los 179 contratos bloqueados heredados del catálogo no se seleccionan ni se declaran resueltos. El primer intento sin UI falló antes de crear recursos porque la configuración temporal Docker no heredaba `cliPluginsExtraDirs` (`unknown flag: --project-name`); se agregó sólo la ruta del plugin Compose ya instalado a esa configuración temporal, sin cambiar configuración global ni repo. Verificación por etiquetas: ese intento no dejó contenedores, volúmenes ni redes.

- **2026-10-28** — `PLAN_CONFLICT` cobertura E2E Discovery: la evidencia HTTP nativa anterior prueba ACK/seguridad, no que el contrato válido alcance `run`. `.lore/scripts/local-runner.mjs::isolatedWorkerEnv` elimina `SCOPE`, y `.lore/scripts/playmaker-e2e.ts` inicia Java sin fijarlo, mientras el paquete exige `rio.bus.scope: ${SCOPE}` y el escenario envía `scope: local`. No se declara PROCESSED a partir de un HTTP 200; los tests Spring sí prueban procesamiento/rechazo y ausencia del body en logs. Para una prueba nativa concluyente se necesita fijar `SCOPE=local` en el proceso aislado y observar los outcomes/logs mediante un probe de lectura del runner existente, además del escenario permitido. El paquete sólo enumera escenarios Lore entre los archivos esperados; se solicita excepción acotada para `.lore/scripts/playmaker-e2e.ts`, sin cambiar código/config productivos ni agregar archivos, flags o frontend. Se detiene sólo esa ampliación; no se debilitan el gate ni sus asserts. G2 pending, T2.3 [/], sin push/F3.

- **2026-10-28** — Owner aclara que la capacidad es exclusivamente backend y pide E2E backend en playmaker. Confirmado en `AGENTS.md` y `.lore/scripts/local-runner.mjs`: `./local/test-lore.sh` ejecuta la suite HTTP nativa sin navegador ni servidor web y no exige hosts; `--gate` sí inicia el servidor de Lore para la revisión independiente, sin abrir navegador. El dominio pertenece a la infraestructura de pruebas, no a un frontend del producto. Se ejecuta el modo oficial sin UI; no se debilita ni se sustituye el gate de push y G2 sigue pending. Corrección de la anotación anterior: hosts sí es obligatorio en modo `--gate`, como verificó su error posterior.

- **2026-10-28** — Continuidad y cierre operativo solicitados aplicados por delta con `agents-os-session-close` y `agents-os-session-feedback`, ejecutados desde la raíz absoluta del vault resuelta en esta sesión, modelo exacto **`gpt-6.1-sol`**, superficie `[[Codex]]`. Toda la evidencia/feedback queda sólo aquí por la restricción del owner; no se crean L0/L1, feedback ni `agent_run` separados. Segmento atribuible coding/testing: SDK publicado y F2 en commit local validado, pendiente sólo del gate nativo y push; evaluator agent, user_rework unknown. Feedback: Sistema 1/memoria 4/5 (continuidad y restricciones útiles), skills 3/5, herramientas 4/5; fricción principal: compatibilidad V1 y prerrequisitos locales del gate no incluidos en el paquete. Mejora: verificar APIs que el consumidor aún usa y los prerrequisitos Lore antes de publicar la dependencia. Se corrigió la propagación de errores al encadenar verificaciones y se revalidó el escenario antes de enmendar el commit propio. No se promueve nueva política ni conocimiento público. Clones originales verificados intactos: SDK `ad2c98b` con `graphify-out/`; playmaker `3433fc12b` con `graphify-out/` y `scripts/inactivate-probe/`. Próximo paso concreto: comprobar la entrada de hosts del owner, ejecutar Lore sobre `2741dbeeb`, completar pre-push/Cleric, push y dejar G2 en review; no aceptar gates ni empezar F3.

- **2026-10-28** — F2 preparada en commit local **`2741dbeebc9c64fd12b3d6b6b3fcd31afd792388`** (`Subscribe playmaker to Discovery contracts through RIO Bus`), base `20e0a91094fd827962932ebb4fead35a44c1184b`, worktree limpio. Contrato staged y hooks pre/post-commit PASS; parser Lore PASS. `git diff 20e0a9109 --stat`: **16 files changed, 477 insertions(+), 3 deletions(-)** (3 código/build, 9 yml, 3 tests, 1 Lore). `DOCKER_CONFIG=<config local temporal> ./local/test-lore.sh --gate` **exit 1**, error textual: `local.adminml.com must resolve only to loopback. Add 127.0.0.1 local.adminml.com to /etc/hosts`. No API/MySQL de este gate fue iniciado; `sudo -n true` exit 1 (`sudo: a password is required`), se espera acción del owner en hosts. Se detienen únicamente Lore y el push dependiente: rama de playmaker aún **no pusheada**, pre-push/Cleric aún **no ejecutados**, G2 permanece **pending**, T2.3 `[/]`; no se declara review ni se empieza F3. SDK `0.0.2-rio-bus` sí publicado, verificado y pusheado. No PRs, no deploys ni cambios en clones del owner.

- **2026-10-28** — Validación de sintaxis Lore: el parser nativo exige ledger y limpieza explícita para cualquier POST, incluso el handler Discovery sin persistencia. Se declaran IDs de los pushes como checks locales y verificación HTTP del runtime retenido, cuyo teardown completo corresponde al launcher; no se inventa un provider ni se afirma verificación SQL o de logs desde esos asserts HTTP. Parser fijado PASS después del ajuste. El primer commit local se creó pese al fallo de esa validación opcional por no propagar el exit de un comando encadenado; se corrige la propagación y se enmienda únicamente ese commit propio, todavía sin push, después de parser/contratos/hooks PASS. No se reemplaza la validación ni ejecución nativa requerida por este parse local.
- **2026-10-28** — `PLAN_CONFLICT` documental: AGENTS.md dispara actualizaciones de arquitectura/catálogo/Swagger y `/aoc-management update-internal`; el paquete y el owner limitan los archivos y prohíben agregar documentación/evidencia ajena a SIG-719. Se detiene sólo esa actualización adicional, por prioridad del plan, sin crear docs ni reportes; el contrato staged del repo PASS. `aoc-management`, `safe_add_dependency` y las herramientas AppSec referidas por reglas no están expuestas en la sesión; no se declaran ejecutadas. Se mantienen los hooks de seguridad obligatorios PASS.

- **2026-10-28** — Gates de playmaker con SDK publicado: `JAVA_HOME=<JDK25> SCOPE=local ./gradlew check --refresh-dependencies` PASS (3m17s), **5.224 tests, 0 fallos/errores y 3 omitidos heredados**, más `localTest` **64/0/0/0**; `./gradlew test jacocoTestReport` PASS (test UP-TO-DATE, reporte regenerado, 1s). Los omitidos existentes son `ImportedActionIntegrationTest.mysqlSharedReadersOverlapWhileRevocationWaitsAndThenDenies` y dos casos de `TopologicalSortServiceImplTest`; ningún test nuevo omitido. Código nuevo `DiscoveryBusProcess`: **12/12 líneas, 2/2 ramas, 45/45 instrucciones (100%)**. Spike 3 PASS: converter HTTP sigue siendo Jackson 2, snake_case, fecha UTC y omisión de nulls en el endpoint existente. Hooks y contrato staged PASS; se prepara el commit requerido por Lore/pre-push.

- **2026-10-28** — H-2 entregado: `fury list-versions --limit 5` confirma **0.0.2-rio-bus FINISHED** en `feature/rio-bus`; verificación física Maven PASS (`verifyRioBusPublishedArtifact`, exit 0, 19s), JAR publicado contiene reader, resultado, cuatro tipos V1 y controller del bus. SHA fuente `4ad071ecfbb1bc0ef16e4d6c5541ddb666fcf864`; la vista `BuildApi.get_build` todavía mostraba `creating`, por lo que el estado se contrasta con listado app y artefacto disponible, sin crear versiones duplicadas. Comienza `./gradlew check --refresh-dependencies` de playmaker con JDK25 y `SCOPE=local`, sin composite build: prueba la dependencia publicada real. [Versión de prueba 0.0.2-rio-bus](https://web.furycloud.io/rio-sdk-events/versions/detail/0.0.2-rio-bus).

- **2026-10-28** — `fury versions create --no-tests --auto-accept --confirmed` PASS: **0.0.2-rio-bus** creada desde `feature/rio-bus@4ad071e`; confirmación de CLI respondió sólo por esa versión autorizada. Backend de builds confirma SHA completo y estado `creating`; se espera publicación sin repetir create. Playmaker staged: `./scripts/run-agentic-testing-contract.sh` PASS (repository-contract 10 sources/18 commands/12 documents; manifest retirado), `git diff --cached --check` PASS, **16 files changed, 463 insertions(+), 3 deletions(-)**: 3 código/build, 9 yml, 3 tests y 1 escenario Lore. Catálogo validado con el engine fijado: 270 casos, 91 ready y 179 bloqueados heredados, sin generar archivos. No se cambia el catálogo ni se declara que sus bloqueados estén resueltos. G2 sigue pending hasta gates completos y push.

- **2026-10-28** — H-2, commit/push del SDK: `4ad071ecfbb1bc0ef16e4d6c5541ddb666fcf864` (`Add strict Discovery reader and preserve V1 consumer compatibility`), `git push -u origin feature/rio-bus` PASS, worktree limpio. Gates finales JDK25: `./gradlew check` PASS, `./gradlew test` PASS (**2.556 tests, 0 fallos/errores/omitidos**), `./gradlew jacocoTestCoverageVerification` PASS, `./gradlew jacocoTestReport` PASS; hooks pre/post-commit Websec, Datasec, formatter, Checkstyle y PMD PASS. Reader/resultados nuevos: **103/103 líneas, 50/50 ramas y 379/379 instrucciones (100%)**. Cuatro tipos V1 byte a byte iguales a `1.5.0`. Diff de esta ampliación contra `7f50783`: **19 files changed, 942 insertions(+), 3 deletions(-)**; acumulado contra `35b1a43`: **39 files changed, 2119 insertions(+), 23 deletions(-)**, ampliación de presupuesto autorizada por H-2/V1. Fury confirma que `0.0.2-rio-bus` aún no existe (list search exit 3 esperado); se solicita create de prueba, nunca versión productiva. Playmaker: 31 casos críticos PASS, process nuevo 12/12 líneas, 2/2 ramas y 45/45 instrucciones (100%), hooks PASS. Lore pendiente de hosts: `sudo -n true` exit 1, `sudo: a password is required`; se pide al owner agregar loopback para `local.adminml.com`, sin pedir contraseña.

- **2026-10-28** — Regresión local detectada antes de publicar: el publisher obligatorio del bus abría BigQueue aun en una app sólo consumidora, haciendo fallar contextos Spring existentes por `BIGQUEUE_TOPIC_RIO_BUS_TOPIC_NAME` ausente. Se mantiene el bean siempre registrado, con creación lazy del producer hasta que se solicite el publisher; no cambia firma, configuración ni outcomes de SIG-719. Test específico de arranque del consumidor sin producer añadido en el SDK. Se verifica además el límite numérico del parser con `LIMIT_EXCEEDED` para mantisas largas. Prueba de los perfiles lee los yml de main para evitar el archivo `application-test.yml` de tests que los oculta en el classpath. No se cambia TestConfig ni otros tests de playmaker.

- **2026-10-28** — Compatibilidad preservada: cuatro tipos V1 y sus tests restaurados desde `1.5.0`; no cambia el código del registry ni `/events/**`. Se conserva Jackson 2 sólo para compilar las anotaciones V1 y en sus tests, sin forzarlo al runtime; Micrometer core se declara runtime del SDK porque el bus lo usa y playmaker no trae actuator. No se agrega infraestructura ni un process adicional. Spike local con composite build: 8 tests unitarios/Spring de Discovery PASS, incluidos HTTP Jackson 2, seguridad, parse/rechazo/scope y logs capturados en TRACE sin body. Se añaden pruebas de los nueve perfiles y estímulos Discovery al escenario Lore ejecutable existente (sin nuevos adapters ni modificar el catálogo generado). Gates finales del SDK en curso antes de commit/push/publicación.

- **2026-10-28** — Owner resuelve `PLAN_CONFLICT` V1/V2: «conserva todo… lo que vamos a agregar ahora no tiene ningún tipo de impacto en ninguna funcionalidad… agregar otros mensajes a rio-bus será en otro momento». Se conservan sin cambios los cuatro tipos V1 y sus tests desde tag `1.5.0@3e3acd1b06e964244ad31324167f6238c643c824`, sólo como compatibilidad; ningún flujo existente se migra. Antes de esta ampliación, gates SDK PASS: check y test (2.534/0/0/0), jacocoTestCoverageVerification y report; reader/resultados 98/98 líneas, 48/48 ramas, 367/367 instrucciones. Se repiten por el cambio autorizado. Compilación de playmaker con SDK local confirmó el conflicto anterior: `./gradlew --include-build ../rio-sdk-events-rio-bus compileJava` exit 1, `cannot find symbol class CPCapabilityMessage` (y los otros tipos V1), 10 errores. Docker `colima-rio` ya estaba activo; config temporal del comando lo selecciona sin mutar el contexto global. Preflight Lore PASS (engine/Node24/JDK25/Docker); informa sólo requisito de hosts para UI, no requerido en modo gate.

- **2026-10-28** — Prerrequisitos de F2 recuperados sin cambiar fuentes/pins: transporte Git temporal sólo del comando hacia el mismo `melisource/fury_lore`, mediante el host SSH operativo; launcher oficial `./local/test-lore.sh --setup` PASS, engine exacto `8f53a774155358ab9cbde3c2b06232e279eb9222`, `npm ci` con lock sin cambios. Configuración global del usuario intacta. `./gradlew installGitHooks` PASS y `node scripts/grimoire-hooks.mjs verify` PASS. Tests unitarios y Spring de F2 escritos: recepción/rechazo/scope, ausencia de body en logs, seguridad y spike de HTTP Jackson 2; ejecución dependiente del contrato compatible del SDK.

- **2026-10-28** — Avance H-2/F2: reader, resultado sealed y cinco razones de SIG-644 implementados; 34 casos críticos PASS, primer reporte del código nuevo 100% líneas/ramas/instrucciones. Hooks del SDK Websec/Datasec/Checkstyle/PMD PASS; formatter aplicado. `./gradlew check` detectó dos contratos de tests anteriores al reader (vocabulario de 12 razones y prohibición general de Jackson público); se actualizan únicamente para las razones y la sobrecarga `JsonNode` que SIG-644 exige, manteniendo las otras APIs cerradas. Grimoire bootstrap PASS en la revisión autorizada; archivo legado 27.2.1 respaldado de forma reversible fuera de la ruta activa. Lore `--setup` exit 1: alias SSH exige una clave ausente; `git ls-remote` del mismo repo mediante el host SSH operativo PASS con rewrite sólo del worktree, pero el launcher clone no hereda esa configuración y sigue detenido. Process, POST permitAll y nueve perfiles de F2 escritos, sin tocar flujos existentes.
- **2026-10-28** — `PLAN_CONFLICT` compatibilidad V1/V2: SIG-644 elimina `CPCapabilityMessage`, `ComponentTypeCapability`, `ActionCapability`, `FieldDescriptor`; no están en el SDK base ni `0.0.1-rio-bus`. `rio-playmaker@20e0a9109` todavía importa los tipos V1 en `CpCapabilityConsumerController`, `ComponentTypeRegistryService` y su implementación, excluidos por «No tocar». Consulta concreta al owner para conservar sin cambios esos cuatro tipos del SDK 1.5.0 en `0.0.2-rio-bus`; se detiene únicamente esa decisión y la publicación dependiente, no las pruebas ni implementación independiente.

- **2026-10-28** — Inicio F2 autorizado por el owner («quiero que ahora implementes la parte de playmaker») tras verificar `0.0.1-rio-bus` publicada. `PLAN_CONFLICT` H-2 resuelto por autorización explícita para completar el reader de SIG-644/DD-8 y publicar `0.0.2-rio-bus`; no se amplía a persistencia, F3 ni despliegues. `git fetch origin` PASS en ambos repos; worktree de playmaker creado con el comando exacto del paquete, `feature/rio-bus` desde `20e0a91094fd827962932ebb4fead35a44c1184b`, clone del owner intacto. Check de Grimoire exit 1 por pin ausente/diferente; el owner autoriza revisión exacta `d00c6dbdfffe1eea3b531f83cdfc5e9ec145454d` y todos los efectos solicitados. Instalación autorizada detenida antes de escribir: `grimoire-bootstrap: BLOCKED: Legacy Cleric files take precedence over the pinned skill in the runner and are not verified: ~/.claude/commands/grimoire.cleric.md. Remove them (pre-v2 Grimoire installation) and rerun; verification made no changes`. Se revisa migración reversible del archivo Grimoire 27.2.1; continúa implementación independiente.

%% Log diario para las dailies. Una línea por día con lo avanzado / blockers. %%
- **2026-10-28** — GlobalProtect restablecida. PR #64 del SDK: `continuous-integration`, `code-coverage`, `static-analyzer`, `dependencies` y `workflow` SUCCESS, `Code Reviewer` SKIPPED, merge CLEAN (draft). `/etc/hosts` sigue sin `local.adminml.com` (archivo sin cambios desde 2025-09-11; resuelve a `10.54.29.x` por DNS), así que el gate de playmaker sigue bloqueado.
- **2026-10-28** — Bloqueo del push de playmaker diagnosticado: el perfil `.grimoire/lore-readonly.local.json` apunta al web de Lore local que levanta `./local/test-lore.sh --gate` (el cliente readonly acepta `https` o `http` en loopback), y `--gate` exige que `local.adminml.com` resuelva sólo a loopback (`checkLocalHost` en `.lore/scripts/local-runner.mjs`): falta `127.0.0.1 local.adminml.com` en `/etc/hosts` (requiere sudo del owner). Además GlobalProtect quedó desconectada (`gh`: IP allow list; `git ls-remote` falla), por lo que tampoco se pueden leer los checks del PR #64.
- **2026-10-28** — SIG-718 actualizada en el formato nuevo de Spellbook (`functional@r7`, `technical@r2`) con lo implementado. PR del SDK abierto: [#64](https://github.com/melisource/fury_rio-sdk-events/pull/64) (draft, base `feature/discovery-v2-05-contract-hasher`, head `332b0d9`). El push de playmaker falló en el pre-push: `gate:cleric-runner` BLOCKED por falta de `.grimoire/lore-readonly.local.json` (endpoint aprobado del MCP nativo de Lore + variable del token); repository/agentic contracts PASS. Descripciones en [[Descripción PR — rio-sdk-events — RIO Bus]] y [[Descripción PR — rio-playmaker — RIO Bus]].
- **2026-10-28** — Por pedido del owner: SDK `feature/rio-bus` pusheado `4ad071e..332b0d9` (`a38ff44` fixes de review + `332b0d9` versión) y **`0.0.3-rio-bus` FINISHED** en Fury (`fury versions create --no-tests --auto-accept --confirmed`). El JAR publicado trae `RioBusReader.subscribedOrUnknown`, `DiscoveryMessageReader.read(byte[]|String)` sin `JsonNode` y la publicación blindada. Playmaker sube a `0.0.3-rio-bus` en commit local `fab68a57f` (sin push): 51 tests de bus, seguridad y V1 PASS; suite completa `./gradlew test` 5.224 tests, 3 omitidos heredados, 0 fallos.
- **2026-10-28** — Code review del owner (Claude Code) sobre SDK `35b1a43..4ad071e` y playmaker `20e0a9109..960fe1521`. Corregido y commiteado **local, sin push**: SDK `a38ff44` (`DiscoveryContractPublisher` ya no puede abortar el arranque si el provider o un contrato fallan; tags/logs de `RioBusReader` acotados a processes suscritos; logs del publisher con `result=`; fuera `DiscoveryMessageReader.read(JsonNode)`; test de wire real mqclient → reader) con `check`/`test`/coverage PASS (2.557 tests); playmaker `a0311cdca` (javadoc de `/rio-bus`, pattern matching en `DiscoveryBusProcess`) con 34 tests de bus/seguridad PASS. Pendiente: push del SDK y versión `0.0.3-rio-bus`, y que playmaker la consuma; propuestas abiertas: bloque `rio.bus` sólo en el yml base y escenario Lore propio para Discovery.
- **2026-10-28** — **Entrega final F1 / G1 `review`:** SHA pusheado `7f507839989308ee8178467d97f411337a4d37f1` en `feature/rio-bus`, base `35b1a43a3a7d0f7134486a6a430eba3561a6825b`. Gates con JDK25 y versión final: `./gradlew check` PASS (exit 0, 33s), `./gradlew test` PASS (exit 0, 26s, 2.496 tests, 0 fallos/errores/omitidos), `./gradlew jacocoTestCoverageVerification` PASS (exit 0), `./gradlew jacocoTestReport` PASS; Websec, Datasec, formatter, Checkstyle y PMD PASS sobre el código, hooks pre/post-commit del cambio de versión PASS. Código nuevo: 123/123 líneas (100%), 22/22 ramas (100%), 580/582 instrucciones (99,66%); dos líneas del fix de BigQueue también cubiertas directamente, sin modificar exclusiones. `git diff 35b1a43 --stat`: **24 files changed, 1179 insertions(+), 22 deletions(-)**, 16 código/config/CHANGELOG y 8 tests. `fury versions create --no-tests --auto-accept --confirmed` creó **0.0.1-rio-bus**; `fury list-versions --limit 5` confirma FINISHED y el cliente autenticado `BuildApi.get_build` confirma `status=finished`, rama y SHA exactos. [Pipeline 65](https://rp-builds.furycloud.io/blue/organizations/jenkins/rio-sdk-events/detail/rio-sdk-events/65/pipeline/) finalizado. Verificación física Maven: resolución de `com.mercadolibre.library:rio-sdk-events:0.0.1-rio-bus` exit 0, JAR publicado con las 12 clases esperadas. Script de verificación temporal eliminado, sin archivos de evidencia nuevos. Worktree limpio, sin PR, ninguna versión productiva creada, G1 no aceptado y F2 no iniciada.
- **2026-10-28** — Handoff F1: API de SIG-719 sin cambios. Spike 1 materializado con `BigQueueTopicProperties` desde `rio.bus.topic`/`rio.bus.segment-id` y `BigQueueClientImpl`, sin ampliar configuración. D-10 manual y excepción de versión D-13 cuentan con autorización explícita del owner. Fricción de publicación: `fury versions get` consulta una vista que sigue mostrando `CREATING` sin CI; el listado que selecciona el backend de la aplicación y `BuildApi.get_build` confirman el build `finished`. La disponibilidad se confirmó además en Maven, sin repetir create. H-2 permanece bajo Brenda/owner y no se declara satisfecho por esta entrega.
- **2026-10-28** — Cierre solicitado aplicado mediante `agents-os-session-close` y `agents-os-session-feedback` desde `VAULT_ROOT`, con las rutas absolutas resueltas en ejecución y modelo exacto `gpt-6.1-sol` (`[[Codex]]`). Continuidad, evidencia y feedback consolidados únicamente en este plan por la prohibición de crear archivos adicionales. Feedback: autorización de versión resolvió el último conflicto; se corrigió el orden de una comprobación opcional de Gradle sin tocar código; la discrepancia entre vistas de Fury se resolvió consultando el backend que posee el build y verificando el artefacto Maven. Segmento atribuible final: metadata/publicación verificada, evaluator agent, user_rework unknown; sin registro separado de `agent_run` por la restricción explícita de archivos. Progreso ajustado al proyecto completo (6/10 tareas en review), no sólo a F1. STOP cumplido en G1 `review`; no se acepta gate ni se inicia fase siguiente.
- **2026-10-28** — Versión de prueba enviada a Fury después de gates/commit/push: commit final `7f507839989308ee8178467d97f411337a4d37f1` (`Set RIO Bus test version to 0.0.1-rio-bus`), `git push -u origin feature/rio-bus` exit 0, hooks post-commit Websec/Datasec PASS. Comando `fury versions create --no-tests --auto-accept --confirmed` exit 0; confirmación interna «Proceed with version 0.0.1-rio-bus» respondida conforme a la autorización del owner. Fury confirma app `rio-sdk-events`, branch `feature/rio-bus`, commit `7f5078399893`, versión `0.0.1-rio-bus`, estado inicial `pending`. Se verifica disponibilidad sin repetir create. Diff contra `35b1a43`: **24 files changed, 1179 insertions(+), 22 deletions(-)**, 16 archivos código/config/CHANGELOG + 8 tests. Worktree limpio; G1 sigue pendiente hasta resultado del build. [Build de prueba](https://web.furycloud.io/rio-sdk-events/versions/detail/0.0.1-rio-bus).
- **2026-10-28** — Revalidación de la única línea de versión autorizada: `pre-commit run --files build.gradle` exit 0 (Websec/Datasec PASS, hooks Java sin archivos); `JAVA_HOME=<JDK25> ./gradlew check` exit 0 (`33s`), `./gradlew test` exit 0 (`26s`, 2.496 tests, 0 fallos/errores/omitidos), `./gradlew jacocoTestCoverageVerification` exit 0. El intento opcional combinado `./gradlew jacocoTestReport generatePomFileForMavenJavaPublication jar` falló por dependencia implícita heredada entre `jacocoTestReport` y `compileJava`; resuelto sin cambios de código ejecutando `./gradlew jacocoTestReport` y `./gradlew generatePomFileForMavenJavaPublication jar` por separado, ambos exit 0. POM generado verificado con `version = 0.0.1-rio-bus`; existe `rio-sdk-events-0.0.1-rio-bus.jar`. Fury renovó autenticación y confirmó de nuevo que esa versión aún no existe. Pendientes commit, push y publicación.
- **2026-10-28** — Reanudación T1.6: el owner autoriza «version = 0.0.1-rio-bus para publicar la prueba», resolviendo `PLAN_CONFLICT` del spike 2. Excepción acotada registrada en D-13 y `No tocar`; no habilita versiones productivas ni otras fases. Worktree limpio en `feature/rio-bus@df9ef57bb09ac349a06e4a4bc9e13c000e249c2f`; se cambia sólo la versión, se revalidan gates y metadata de publicación antes de commit/push/create-version. Bootstrap warm: se reutiliza el contexto cargado.
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
